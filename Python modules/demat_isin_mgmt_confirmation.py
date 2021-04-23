"""-----------------------------------------------------------------------------
PURPOSE                 :  This functionality sends notification email with
                           action details for the following requests:
                             * New 
                             * TopUp
                             * Reduce

                           This is called by Incomming ISIN MQ.
DEPATMENT AND DESK      :  Wholesale Founding
REQUESTER               :  Michelle Francis, Lucille Joseph
DEVELOPER               :  Gabriel Marko
CR NUMBER               :  CHNG0004439301
--------------------------------------------------------------------------------

HISTORY
================================================================================
Date        Change no       Developer       Description
--------------------------------------------------------------------------------
2017-03-28  CHNG0004439301  Gabriel Marko   Initial implementation
2019-10-23  FAOPS-676       Jaysen Naicker  Send email to PTS buisness user when 
                                            run in non-production environment
"""


import acm
import time
from datetime import datetime

import at_logging
import demat_config
from at_email import EmailHelper
from demat_isin_mgmt_menex import (
    current_authorised_amount,
    MMSS_ISIN_REQUEST_STATE_CHART_NAME
)

LOGGER = at_logging.getLogger()
DEBUG = False
DEBUG_RECIPIENTS = ["Gabriel.Marko@barclayscapital.com"]


ISIN_CONFIRMATION_TEMPLATE="""
<html>
  <body>
    <table border="1" style="border-collapse: collapse;" width="600">
      <col width="200">
      <col width="300">
      <tr>
        <th colspan="2" bgcolor="#8db3e2" color="#fff">
          ABSA CAPITAL Trade Details
        </th>
      </tr>
      <tr>
        <td>Counterparty</td>
        <td bgcolor="#dbe5f1" color="#fffff">{counterparty}</td>
      </tr>
      {html_content}
    </table>
  </body>
</html>
"""

def compute_rate_spread(instrument):
    """Compute spread rate based on instrument type and rolling period."""
    leg = instrument.Legs()[0]
    instype = instrument.InsType()

    if instype == 'CD':
        leg_rate = leg.FixedRate()
        rolling_period = leg.RollingPeriod()
        convention = {
            '0d': 'Yield',
            '1m': 'NACM',
            '3m': 'NACQ',
            '6m': 'NACS',
            '1y': 'Yield'
        }.get(rolling_period, '')
        return "%s%% %s" % (leg_rate, convention)

    elif instype == 'FRN':
        return "%s/%s" % (leg.FloatRateReference().Name(), leg.Spread())


def get_payment_dates(instrument):
    """Get the list of payment as </br> separated string.
    e.g. "01/01/2017</br>01/02/2017"
    """
    leg = instrument.Legs()[0]
    return "<br>".join(
        format_date(cfw.PayDate())
        for cfw in leg.CashFlows()
        if cfw.CashFlowType() in ['Fixed Rate', 'Float Rate']
    )


def get_counterparty_bpid(instrument):
    """Get the demat counterparty identificator of DEMAT instrument."""
    if len(instrument.Trades()) == 1:
        trade = instrument.Trades()[0]
        if trade.Status() == 'Simulated':
            return trade.AdditionalInfo().MM_DEMAT_CP_BPID()
    return ''


def format_date(date_string):
    """Convert date format from 2017-10-01 to 01/10/2017."""
    if not date_string:
        return ''
    return datetime.strptime(date_string, "%Y-%M-%d").strftime("%d/%M/%Y")


def format_nominal(nominal):
    """
    Add thousands separator to nominal

    Temporary solution for Python 2.6.6

    Example:

    After upgrade use:
    return "{:,}".format(nominal)
    """
    from itertools import izip_longest
   
    # Truncate decimal places

    nominal = int(nominal)

    # Get the sign of the number
    
    sign = '-' * int(nominal < 0)

    # Add thousands separtors ","

    nominal = str(abs(nominal))

    # Split the reversed string representation of the number
    # to equal chunks of length three
    #
    # Example results:
    #
    # "123456789" => ["987", "654", "321"]
    # "1234"      => ["432", "1"]

    chunks = []
    for part in izip_longest(*([iter(reversed(nominal))]*3), fillvalue=''):
        chunks.append("".join(part))

    return "%s%s" % (
        sign,                   # Add minus sign if nominal < 0
        ",".join(chunks)[::-1]  # Join the chunks using "," (["432", "1"] => "432,1"
                                # and reverse the string    "432,1"       => "1,234"
    )


def get_email_content(instrument):
    content = (
        ('Nominal Value', format_nominal(current_authorised_amount(instrument))),
        ('ISIN Number', instrument.Isin()),
        ('Issue Date', format_date(instrument.StartDate())),
        ('Maturity Date', format_date(instrument.EndDate())),
        ('Instrument', instrument.AdditionalInfo().MM_MMInstype()),
        ('Rate/Spread', compute_rate_spread(instrument)),
        ('Payment Dates', get_payment_dates(instrument)),
    )
    return content


def create_isin_confirmation(instrument):
    counterparty = get_counterparty_bpid(instrument)
    content = get_email_content(instrument)
    row_format = "<tr><td>%s</td><td>%s</td></tr>"
    html_content =  "\r".join(row_format % row for row in content)

    return ISIN_CONFIRMATION_TEMPLATE.format(
        counterparty=counterparty,
        html_content=html_content
    )


def send_email(email_helper, retries=5):

    if str(acm.Class()) == "FACMServer":
        email_helper.sender_type = EmailHelper.SENDER_TYPE_SMTP
        email_helper.host = EmailHelper.get_acm_host()

    msg = ("Sending email:\n"
           "    Subject:     %s\n"
           "    Sender:      %s\n"
           "    Recipients:  %s\n"
           "    SMTP Server: %s\n")

    msg = msg % (
        email_helper.subject,
        email_helper.mail_from,
        ", ".join(email_helper.mail_to),
        email_helper.host
    )

    for _ in range(retries):
        try:
            LOGGER.info(msg)
            email_helper.send(log=True)
            break
        except Exception as ex:
            LOGGER.error("Error while sending email: %s" % str(ex))
            time.sleep(5)
    else:
        LOGGER.error("Message wasn't sent! (Nr. of retries: %s)", retries)


def get_action_from_business_process(instrument):
    """Get New/TopUp/Reduce action from business process.

    1. The current status of business process must be Active
    2. The previous status must be New/TopUp/Reduce.
    """

    state_chart = acm.FStateChart[MMSS_ISIN_REQUEST_STATE_CHART_NAME]
    bp = acm.BusinessProcess.FindBySubjectAndStateChart(instrument, state_chart)[0]
    current_step = bp.CurrentStep()

    if current_step.State().Name() != 'Active':
        return

    previous_state = current_step.PreviousStep().State().Name()

    if previous_state == 'New ISIN Request Pending':
        return 'New'

    if previous_state == 'TopUp Reduce Request Pending':
        if current_step.DiaryEntry().Parameters()['Amount'] > 0:
            return 'TopUp'
        return 'Reduce'

    return None


def resend_isin_report(instrument_id, save_mail=False, path=None):
    instrument = acm.FInstrument[instrument_id]
    if not instrument:
        LOGGER.error("Invalid instrument %s." % instrument_id)
        return

    action = get_action_from_business_process(instrument)

    if not action:
        LOGGER.error("Instrument %s doesn't have valid action." % instrument_id)
        return

    send_isin_report(action, instrument, save_mail, path)


def send_isin_report(action, instrument, save_mail=False, path=None):
    env = acm.FInstallationData.Select('').At(0).Name().lower()
    sender = 'ABCapITRTBAMFrontAre@absa.africa'
    recipients = ["wholesalefunding@absa.africa"] if env == 'production' else ["CIBAfricaMarketOpe4@absa.africa"]
    subject = "Demat %s %s" % (instrument.Isin(), action)
    report = create_isin_confirmation(instrument)

    if DEBUG:
        recipients = DEBUG_RECIPIENTS
        subject = "TEST: Demat %s %s" % (instrument.Isin(), action)

    email_helper = EmailHelper(
        report,
        subject,
        recipients,
        sender,
    )

    if save_mail and path is not None:
        try:
            email_helper.save_mail(path)
            LOGGER.info("Email saved to: %s" % path)
        except Exception as ex:
            LOGGER.error("Email not saved: %s" % ex)

    send_email(email_helper, retries=5)

# Not used yet

# def send_exception_notification(exception):
#     config_dict = demat_config.get_config()
#     recipients = config_dict['mq_connection_notifications']
#     sender = 'ABCapITRTBFrontArena@absacapital.com'
#     message = str(exception)
# 
#     try:
#         environment = '- ' + acm.FInstallationData.Select('').At(0).Name()
#     except:
#         environment = ''
# 
#     subject = 'Front Arena Outgoing Custom Swift Failure %s' % environment
#     email_helper = EmailHelper(
#         message,
#         subject,
#         sender,
#         recipients
#     )
# 
#     send_email(email_helper, resend=1)


def __debug(bpid=954220, recipients=None):
    global DEBUG
    global DEBUG_RECIPIENTS

    debug_value = DEBUG
    debug_recipients = DEBUG_RECIPIENTS
    try:
        DEBUG = True
        if recipients is not None:
            DEBUG_RECIPIENTS = recipients
        instrument = acm.FBusinessProcess[bpid].Subject()
        send_isin_report("TEST", instrument)
    finally:
        DEBUG = debug_value
        DEBUG_RECIPIENTS = debug_recipients

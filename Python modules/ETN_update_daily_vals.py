"""----------------------------------------------------------------------------
PROJECT                 :   ETN Pricing
PURPOSE                 :   Daily market values update
DEPATMENT AND DESK      :   Prime Services, Commodities
REQUESTER               :   Byron Woods, Floyd Malatji
DEVELOPER               :   Ondrej Bahounek
CR NUMBER               :   CHG1000488229

Script calculates Accumulated Market pip for every ETN and saves it on a time serie.
Should be run daily (even on weekends) after COB when FX rates for given day are closed.
When a ETN rolling day is within 2 business days, an email is sent to business.

More info: https://confluence.barcapint.com/display/ABCAPFA/Commodities+-+ETN+solution

HISTORY
===============================================================================
Date        Change no      Developer        Description
-------------------------------------------------------------------------------
2018-08-07  CHG1000488229  Ondrej Bahounek  Initial Implementation
----------------------------------------------------------------------------"""

import acm
import CurrencyETNPricing
from at_ael_variables import AelVariableHandler
from at_logging import getLogger
from at_email import EmailHelper


TODAY = acm.Time.DateToday()
LOGGER = getLogger(__name__)
ael_variables = AelVariableHandler()


def select_etns():
    query = acm.CreateFASQLQuery(acm.FInstrument, 'AND')
    q = query.AddOpNode('AND')
    q.AddAttrNode('InsType', 'EQUAL', 'ETF')
    q.AddAttrNode('Underlying.InsType', 'EQUAL', 'EquityIndex')
    q.AddAttrNode('ValuationGrpChlItem.Name', 'EQUAL', 'CurrencyETN')
    return query.Select()


ael_variables.add(
    'inpt_etns',
    label='ETN(s)',
    cls='FETF',
    multiple=True,
    collection=select_etns(),
    alt='List of ETNs.'
    )
ael_variables.add(
    'start_date',
    label='Start Date',
    cls='date',
    default='Today',
    multiple=False,
    alt='Start day of the run.'
    )
ael_variables.add(
    'end_date',
    label='End Date',
    cls='date',
    default='Today',
    multiple=False,
    alt='End day of the run.'
    )
ael_variables.add(
    "email_recipients",
    label="Email Recipients",
    multiple=True,
    mandatory=False,
    alt=("Email recipients. Use comma separated email addresses "
         "if you want to send report to multiple users. "
         "Leave blank if no email needs to be sent."))


def format_email_data(etns_list):
    msg = "Hello Commodities and TCU Teams, <br /><br />"
    msg += "These ETNs are going to reset soon, ex-div date is:<br /><br />"

    for etn in etns_list:
        msg += "<b>{0}: {1}</b><br />".format(*etn)

    msg += "<br /><br />"
    msg += "If you wish to undo any of the resetting, please contact TCU. <br /><br />"
    msg += "For more information please visit <a href='{0}'>confluence page</a>".format(
        "https://confluence.barcapint.com/display/ABCAPFA/Commodities+-+ETN+solution")
    msg += "<br /><br />"
    msg += "Best regards,<br />{0}".format(
        "CIB Africa TS Dev - Prime and Equities")
    msg += "<br /><br /><br /><small>This is an automated message from '%s'</small>" % __name__
    return msg


def send_email(subj, addresses, body):
    environment = acm.FDhDatabase['ADM'].InstanceName()
    email_helper = EmailHelper(
        body,
        '{} - {}'.format(subj, environment),
        addresses,
    )
    if str(acm.Class()) == "FACMServer":
        email_helper.sender_type = EmailHelper.SENDER_TYPE_SMTP
        email_helper.host = EmailHelper.get_acm_host()
    try:
        email_helper.send()
    except:
        LOGGER.exception("Error while sending e-mail.")


def ael_main(ael_dict):
    LOGGER.msg_tracker.reset()
    etns = ael_dict['inpt_etns']
    addrss = list(ael_dict['email_recipients'])
    val_date = ael_dict['start_date'].to_string("%Y-%m-%d")
    end_date = ael_dict['end_date'].to_string("%Y-%m-%d")

    LOGGER.info("Start Date: '%s'", val_date)
    LOGGER.info("End Date: '%s'", end_date)

    while val_date <= end_date:
        if LOGGER.msg_tracker.errors_counter:
            LOGGER.error("Can not proceed for '%s', errors occurred in previous run", val_date)
            break

        reset_etns = []
        for etn in etns:
            try:
                LOGGER.info("%s: Updating for '%s'...", etn.Name(), val_date)
                CurrencyETNPricing.store_accumulated_mkt(etn, val_date)
                roll_date = CurrencyETNPricing.get_etn_roll_date(etn, val_date)
                LOGGER.info("%s: Reset Day: %s", etn.Name(), roll_date)
                cal = etn.Currency().Calendar()
                if cal.BankingDaysBetween(val_date, roll_date) <= 2 and val_date <= roll_date:
                    formatted_date = roll_date
                    if val_date == roll_date:
                        formatted_date = '<font color="red">{0}</font>'.format(roll_date)
                    reset_etns.append((etn.Name(), formatted_date))
            except:
                LOGGER.exception("%s update failed", etn.Name())

        if addrss and reset_etns:
            msg = format_email_data(reset_etns)
            send_email("ETN Reset Event", addrss, msg)

        val_date = acm.Time.DateAddDelta(val_date, 0, 0, 1)

    if LOGGER.msg_tracker.errors_counter:
        raise RuntimeError("ERRORS occurred. Please check the log.")

    LOGGER.info('Completed successfully.')

from datetime import datetime

import acm
from at_logging import getLogger
from at_ael_variables import AelVariableHandler
from at_email import EmailHelper


LOGGER = getLogger(__name__)
ael_variables = AelVariableHandler()

ael_variables.add("trades",
                  label="Trades",
                  cls="FTrade",
                  default="?ACS_tree_manual",
                  mandatory=False,
                  multiple=True)
ael_variables.add("email_recipients",
                  label="Email Recipients",
                  default="Ondrej.Bahounek@barclays.com",
                  multiple=True,
                  mandatory=False,
                  alt=("Email recipients. Use comma separated email addresses "
                       "if you want to send report to multiple users. "
                       "Leave blank if no email needs to be sent."))


def send_email(subject, body, recipients):
    environment = acm.FDhDatabase['ADM'].InstanceName()
    subject = "{0} {1} ({2})".format(subject, acm.Time.DateToday(), environment)
    email_helper = EmailHelper(
        body,
        subject,
        recipients,
    )
    if str(acm.Class()) == "FACMServer":
        email_helper.sender_type = EmailHelper.SENDER_TYPE_SMTP
        email_helper.host = EmailHelper.get_acm_host()

    try:
        email_helper.send()
    except Exception as exc:
        LOGGER.exception("Error while sending e-mail: %s", exc)


def to_html(rows):
    res_text = '<table width="200" border="1">'
    res_text += "<tr>" + "".join(map("<td><b>{0}</b></td>".format, rows[0])) + "</tr>"
    for row in rows[1:]:
        line = "<tr>" + "".join(map("<td>{0}</td>".format, row)) + "</tr>"
        res_text += line
    return res_text + "</table>"


def construct_body(trades):
    dir_date = acm.Time.DateToday()
    file_date = format_date(dir_date, "%y%m%d")
    msg = "Hello ACS, <br /><br />"
    msg += "Some manual bookings were done in the Front Arena ACS Tree.<br /><br />"
    msg += "Amount of manual trades: <b>%d</b><br /><br />" % trades.Size()

    rows = [("Trade", "Create User")] + \
        [(t.Oid(), t.CreateUser().Name()) for t in trades]

    msg += to_html(rows)

    msg += "<br /><br />"
    msg += "Please check <b>ACS_tree_manual</b> report for more details:<br /><br />"
    msg += r"y:\Jhb\FAReports\AtlasEndOfDay\TradingManager\{dir_date}\ACS_tree_manual_{file_date}.csv" \
        .format(dir_date=dir_date, file_date=file_date)
    msg += "<br /><br />"
    msg += "Best regards,<br />{0}".format(
            "CIB Africa TS Dev - Prime and Equities")
    msg += "<br /><br /><br /><small>This is an automated message from '%s'</small>" % __name__
    return msg


def format_date(the_date, date_format="%Y-%m-%d"):
    if '/' in the_date:
        dt = datetime.strptime(the_date, '%d/%m/%Y')
    else:
        dt = datetime.strptime(the_date, '%Y-%m-%d')
    return dt.strftime(date_format)


def ael_main(ael_dict):
    LOGGER.msg_tracker.reset()

    trades = ael_dict['trades']
    LOGGER.info("Trades amount: %d", trades.Size())

    if trades.Size() > 0:
        LOGGER.info("Sending email about trades existence...")
        subject = "ACS Tree trades"
        body = construct_body(trades)
        recipients = list(ael_dict["email_recipients"])
        send_email(subject, body, recipients)

    if LOGGER.msg_tracker.errors_counter:
        msg = "Errors occurred. Please check the log."
        LOGGER.error(msg)
        raise RuntimeError(msg)

    if LOGGER.msg_tracker.warnings_counter:
        LOGGER.warning("Completed with some warnings.")
    else:
        LOGGER.info("Completed successfully.")

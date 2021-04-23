"""-----------------------------------------------------------------------
HISTORY
================================================================================
Date       Change no     Developer          Description
--------------------------------------------------------------------------------
2018-05-15 CHG1000395772 Edmore Chagwedera  Listing non-rerated Prime Services
                                            deposits/call accounts.
2019-12-11 FAPE-169      Tibor Reiss        Specify mail_from for backend
-----------------------------------------------------------------------"""
import acm

from at_logging import getLogger
from at_ael_variables import AelVariableHandler
from at_email import EmailHelper


LOGGER = getLogger()

ael_variables = AelVariableHandler()
ael_variables.add("query_folder",
                  label="Query folder",
                  cls=acm.FStoredASQLQuery,
                  collection=sorted(acm.FStoredASQLQuery.Select("subType='FInstrument'")),
                  default=acm.FStoredASQLQuery["NonReratedCallAccounts_Prime"]
                  )
ael_variables.add("email_recipients",
                  label="Email Recipients",
                  multiple=True,
                  mandatory=True,
                  alt=("Email recipients. Use comma separated email addresses "
                       "if you want to send report to multiple users. "
                       "Leave blank if no email needs to be sent.")
                  )


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
    res_text += "<tr>" + "".join(map("<td><b>{0}</b></td>".format, ("Instrument", "LegEndDate"))) + "</tr>"
    for row in rows:
        line = "<tr>" + "".join(map("<td>{0}</td>".format, row)) + "</tr>"
        res_text += line
    return res_text + "</table>"


def construct_body(instruments):
    msg = "Hello TCU and PCG<br /><br />"
    msg += "The following list of call accounts were not rerated"
    msg += " on {} for date {}.<br /><br />".format(acm.Time.TimeNow(), acm.Time.DateToday())
    msg += "Amount of non-rerated call accounts: <b>{}</b><br /><br />".format(instruments.Size())
    rows = [(i.Name(), i.EndDate()) for i in instruments]
    msg += to_html(rows)
    msg += "<br /><br />"
    msg += "Best regards,<br />CIB Africa BTB Dev - Prime and Equities"
    msg += "<br /><br /><br /><small>This is an automated message from '{}'</small>".format(__name__)
    return msg


def ael_main(ael_dict):
    LOGGER.msg_tracker.reset()
    instrument = ael_dict['query_folder'].Query().Select()
    LOGGER.info("Instrument amount: {}".format(instrument.Size()))

    if instrument.Size() > 0:
        LOGGER.info("Sending email about Prime Services non rerated call accounts...")
        subject = "Non-rerated call accounts - Prime Services"
        body = construct_body(instrument)
        recipients = list(ael_dict["email_recipients"])
        send_email(subject, body, recipients)

    if LOGGER.msg_tracker.errors_counter:
        LOGGER.error("ERRORS occurred. Please check the log.")
    else:
        LOGGER.info("Completed successfully.")

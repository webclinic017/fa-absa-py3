'''--------------------------------------------------------------------------------------------------------
Date                    : 2020-02-05
Purpose                 : This script update the ZAR-MM-GM-Funding Curve, using the rate differences between JIBAR-3M,
                          Top20 rate and JIBAR 3M in the Short end and Long end is the spread points from ZAR-MM-dirtyFunding curve.
Department and Desk     : Treasury - FTP Desk
Requester               : Cebo Msomi and Tafara Dakwa
Developer               : Kabelo Rasethetho
Jira Number             : FAFO-81
--------------------------------------------------------------------------------------------------------
'''

import acm
import ael
from at_logging import getLogger
from at_email import EmailHelper
from at_ael_variables import AelVariableHandler

LOGGER = getLogger(__name__)
ael_variables = AelVariableHandler()

ael_variables.add("email_recipients",
                  label="Email Recipients",
                  default="xraFTPFunding1@absa.africa",
                  multiple=True,
                  mandatory=False,
                  alt=("Email recipients. Use comma seperated email addresses "
                       "if you want to send report to multiple users. "
                       "Leave blank if no email needs to be sent."))

ael_variables.add("cc_recipients",
                  label="cc recipients",
                  default="Abcap-IT-Front-Arena-Front-Office@absa.africa",
                  multiple=True,
                  mandatory=False,
                  alt=("Email recipients. Use comma seperated email addresses "
                       "if you want to send report to multiple users. "
                       "Leave blank if no email needs to be sent."))
ael_variables.add("sender_email",
                  label="sender email",
                  default="Abcap-IT-Front-Arena-Front-Office@absa.africa",
                  multiple=False,
                  mandatory=False,
                  alt=("Email recipients. Use comma seperated email addresses "
                       "if you want to send report to multiple users. "
                       "Leave blank if no email needs to be sent."))


def to_html(rows):
    res_text = '<table width="200" border="2">'
    res_text += "<tr>" + "".join(map("<td><b>{0}</b></td>".format, rows[0])) + "</tr>"
    for row in rows[1:]:
        line = "<tr>" + "".join(map("<td>{0}</td>".format, row)) + "</tr>"
        res_text += line
    return res_text + "</table>"


def construct_html_body(curve_levels):
    msg = "Hi FTP Desk, <br /><br />"
    msg += "Please note that ZAR-MM-GMFunding was updated successfully. See below for the  updated curve:<br /><br />"
    msg += to_html(curve_levels)
    msg += "<br /><br />"
    msg += "Best regards,<br />{0}".format(
        "Abcap-IT-Front-Arena-Front-Office")
    msg += "<br /><br /><br /><small>This is an automated message from '%s'</small>" % __name__
    return msg


def point_name(Date_count, Date_period):
    if Date_period == 'Months':
        curve_point = str(Date_count) + 'm'
    elif Date_period == 'Days':
        curve_point = str(Date_count) + 'd'
    else:
        curve_point = str(Date_count) + 'y'

    return curve_point


def current_market_price(obj):
    for price in obj.Prices():
        if price.Market().Name() == "SPOT":
            return price.Last()


def curve_updator():
    try:
        curve_data = {"Point Name": [], "Spread": []}
        curve = acm.FAttributeSpreadCurve["ZAR-MM-GMFunding"]
        dirty_curve = acm.FAttributeSpreadCurve["ZAR-MM-DirtyFundingSpr"]
        top20_rate_price = current_market_price(acm.FRateIndex["ZAR-ABSA-TOP20-CALL"])
        Jibar_3m_price = current_market_price(acm.FRateIndex["ZAR-JIBAR-3M"])
        Jibar_1m_price = current_market_price(acm.FRateIndex["ZAR-JIBAR-1M"])
        day1_point = Jibar_3m_price - top20_rate_price
        month1_point = Jibar_3m_price - Jibar_1m_price
        cpoints = [cp for cp in curve.Attributes()[len(curve.Attributes()) - 1].Spreads() if
                   point_name(cp.Point().DatePeriod_count(), cp.Point().DatePeriod_unit())]
        month1_point = Jibar_3m_price - Jibar_1m_price
        counter = 0
        headers = [("Point Name", "Spread")]
        values = []
        for p in dirty_curve.Attributes()[len(dirty_curve.Attributes()) - 1].Spreads():
            p_name = point_name(p.Point().DatePeriod_count(), p.Point().DatePeriod_unit())
            if p_name == "1d":
                cpoints[counter].Spread(day1_point / 100)
                values.append((p_name, round(float(cpoints[counter].Spread()), 4)))
            elif p_name == "1m":
                cpoints[counter].Spread(month1_point / 100)
                values.append((p_name, round(float(cpoints[counter].Spread()), 4)))
            elif p_name == "3m":
                cpoints[counter].Spread(0.0000)
                values.append((p_name, 0.0000))
            else:
                cpoints[counter].Spread(p.Spread())
                values.append((p_name, round(float(cpoints[counter].Spread()), 4)))
            counter += 1

        curve.Commit()
        table = headers + \
                values
        return table
    except Exception as e:
        LOGGER.info(e)


def ael_main(ael_dict):
    receipents = list(ael_dict["email_recipients"])
    cc_email = list(ael_dict["cc_recipients"])
    sender_email = ael_dict["sender_email"]
    try:
        curve_levels = curve_updator()
        LOGGER.info("ZAR-MM-GMFunding curve was updated successfully")
        subject = "ZAR-MM-GMFunding update for:" + " " + ael.date_today().to_string("%d-%m-%Y")
        email_helper = EmailHelper(
        construct_html_body(curve_levels),
        subject,
        receipents,
        sender_email,
        None,
        "html",
	"SMTP"
        )
        email_helper.mail_cc = cc_email
	email_helper.host = email_helper.get_acm_host()
        email_helper.send()
        LOGGER.info("Sent an email regarding the status for updating  the ZAR-MM-GMFunding curve.")
        LOGGER.info("Completed successfully.")
    except Exception as e:
        subject = "ZAR-MM-GMFunding curve update failed for:" + " " + ael.date_today().to_string("%d-%m-%Y")
        msg = "Hi FTP Desk, <br /><br />"
        msg += "Please note that ZAR-MM-GMFunding curve update failed.We are attending to the issue and we will provide feedback ASAP. <br /><br />"
        msg += "<br />"
        msg += "Best regards,<br />{0}".format(
            "Abcap-IT-Front-Arena-Front-Office")
        msg += "<br /><br /><br /><small>This is an automated message from '%s'</small>" % __name__
        email_helper = EmailHelper(
        construct_html_body(curve_levels),
        subject,
        receipents,
        sender_email,
        None,
        "html",
	"SMTP"
        )
        email_helper.mail_cc = cc_email
	email_helper.host = email_helper.get_acm_host()
        email_helper.send()
        LOGGER.error("Curve update failed.")
        LOGGER.info(e)
    




import acm, ael
from at_email import EmailHelper
from at_logging import getLogger
from at_ael_variables import AelVariableHandler
from FAFOUtils import WriteCSVFile
from IR_Delta_Calculation import get_calculation_space

LOGGER = getLogger(__name__)
ael_variables = AelVariableHandler()
ael_variables.add("email_recipients",
                  label="Email Recipients",
                  default='"NonZarMMTraders@ABSACORP.onmicrosoft.com","wholesalefunding@absa.africa","IntradayLiquidityM2@ABSA.co.za","SecondaryMM@absa.africa","Kalin.Ramsumer@absa.africa","Tafara.Dakwa@absa.africa","Cebo.Msomi@absa.africa"',
                  multiple=True,
                  mandatory=False,
                  tab='inputs',
                  alt=("Email recipients. Use comma seperated email addresses "
                       "if you want to send report to multiple users. "
                       "Leave blank if no email needs to be sent."))
ael_variables.add("cc_recipients",
                  label="cc recipients",
                  default="Tamara.Timothy@absa.africa",
                  multiple=True,
                  mandatory=False,
                  tab='inputs',
                  alt=("Email recipients. Use comma seperated email addresses "
                       "if you want to send report to multiple users. "
                       "Leave blank if no email needs to be sent."))

ael_variables.add("trade_filter_name",
                  label="trade filter name",
                  default="Test Trades_GT_Live",
                  multiple=False,
                  mandatory=True,
                  tab='inputs'
)
ael_variables.add("output_path",
                  label="output path",
                  default="/services/frontnt/Task/",
                  multiple=False,
                  mandatory=True,
                  tab='inputs'
)
                     
ael_variables.add("sender_email",
                  label="sender email",
                  default="Abcap-IT-Front-Arena-Front-Office@absa.africa",
                  multiple=False,
                  mandatory=False,
                  tab='inputs',
                  alt=("Email recipients. Use comma seperated email addresses "
                       "if you want to send report to multiple users. "
                       "Leave blank if no email needs to be sent."))
trd_filter = acm.FTradeSelection["Test Trades_GT_Live"]
def tradesheet_columns(trade, field_name):
    sheet_type = "FTradeSheet"
    column_id = field_name
    calc_space = get_calculation_space(sheet_type)
    node = calc_space.InsertItem(trade)
    return calc_space.CreateCalculation(node, column_id).Value()

def trades_checker(trade_filter_name):
    trd_filter = acm.FTradeSelection[trade_filter_name]
    trds_info = []
    if trd_filter:
        LOGGER.info("Trade Filter:{} exist in FA.")
        trds_list = trd_filter.Trades()
        if len(trds_list) >= 1:
            for trd in trds_list:
                ins = trd.Instrument()
                prf = trd.Portfolio()
                cpty = trd.Counterparty()
                buy_sell = tradesheet_columns(trd, "Bought or Sold")
                current_nominal = tradesheet_columns(trd, "Current Nominal")
                trds_info.append([trd.Name(), ins.Name(), trd.Price(), trd.Quantity(), trd.AcquireDay(), prf.Name(), trd.Currency().Name(), trd.Status(),
                                  cpty.Name(), trd.Trader().Name(), buy_sell, current_nominal, trd.Nominal()])
    return trds_info


def construct_html_body():
    msg = "Hi, <br /><br />"
    msg += "Please see attached file containing trades booked against counterparty: Test.<br /><br />"
    msg += "<br />"
    msg += "Best regards,<br />{0}".format(
        "Abcap-IT-Front-Arena-Front-Office")
    msg += "<br /><br /><br /><small>This is an automated message from '%s'</small>" % __name__
    return msg


def ael_main(ael_dict):
    trade_filter_name = ael_dict["trade_filter_name"]
    output_path = ael_dict["output_path"]
    email_sender = ael_dict["sender_email"]
    receipents = list(ael_dict["email_recipients"])
    email_cc = list(ael_dict["cc_recipients"])
    trades_info = trades_checker(trade_filter_name)
    report_headers = ["Trade", "Instrument", "Price", "Qty", "Acquire Day", "Portolio", "Trade Currency",
                        "Trade Status", "Counterparty", "Trader", "Buy/Sell", "Current Nominal", "Nominal"]
    file_name = "Trades_info_"+str(acm.Time.DateToday())+".csv"
    file_path = output_path+file_name
    
    if len(trades_info) >= 1:
        msg = "Hi, <br /><br />"
        msg += "Please find attached."
        msg += "<br /><br />"
        msg += "Best regards,<br />{0}".format(
            "Abcap-IT-Front-Arena-Front-Office")
        msg += "<br /><br /><small>This is an automated message from task: '%s'</small>" % __name__
    else:
        msg = "Hi, <br /><br />"
        msg += "Please note that there are no trades to report on."
        msg += "<br /><br />"
        msg += "Best regards,<br />{0}".format(
            "Abcap-IT-Front-Arena-Front-Office")
        msg += "<br /><br /><small>This is an automated message from task: '%s'</small>" % __name__
    WriteCSVFile(output_path, file_name, trades_info, report_headers)
    LOGGER.info("Output file created and populated with no errors.")
    LOGGER.info("Creating the notification email....")
    subject = "Test counterparty report for date:" + " " + str(acm.Time.DateToday())
    email_helper = EmailHelper(
    msg,
    subject,
    receipents,
    email_sender,
    [file_path],
    "html",
    "SMTP"
    )
    email_helper.host = email_helper.get_acm_host()
    email_helper.mail_cc = email_cc 
    email_helper.send()
    LOGGER.info("Sent a notification email.")
    LOGGER.info('Task completed successfully.')
        
        
        
    

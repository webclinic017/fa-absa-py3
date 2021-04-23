import acm, csv
import IR_Delta_Calculation
import FAFOUtils
from at_logging import getLogger
from at_email import EmailHelper
from at_ael_variables import AelVariableHandler

LOGGER = getLogger(__name__)

ael_variables = AelVariableHandler()
ael_variables.add(
    'portfolios',
    label='portfolios',
    multiple=True,
    mandatory = True,
    default = "'GT Funding','GT Funding ST','Int Term Fund Econ Alloc','GT 2657 - Corp','Int Term Fund Econ Alloc','LIABILITIES 2474','Economic Hedges 2474'",
    tab = "Task Inputs"
)

ael_variables.add(
    'file_path',
    label='file path',
    mandatory = True,
    default="/services/frontnt/Task/",
    tab = "Task Inputs"
)
ael_variables.add("email_recipients",
                  label="Email Recipients",
                  default='"wholesalefunding@absa.africa","xraFTPFunding1@absa.africa"',
                  tab = "Task Inputs",
                  multiple=True,
                  mandatory=True,
                  alt=("Email recipients. Use comma seperated email addresses "
                       "if you want to send report to multiple users. "
                       "Leave blank if no email needs to be sent."))
                       
ael_variables.add("sender_email",
                  label="sender email",
                  default="Abcap-IT-Front-Arena-Front-Office@absa.africa",
                  tab = "Task Inputs",
                  multiple=False,
                  mandatory=False,
                  alt=("Email recipients. Use comma seperated email addresses "
                       "if you want to send report to multiple users. "
                       "Leave blank if no email needs to be sent."))

def construct_html_body():
    msg = "Hi, <br /><br />"
    msg += "Please find attached report.<br /><br />"
    msg += "<br />"
    msg += "Best regards,<br />{0}".format(
        "Abcap-IT-Front-Arena-Front-Office")
    msg += "<br /><br /><br /><small>This is an automated message from '%s'</small>" % __name__
    return msg

def column_value(column_id, sheet_type, calc_obj):
    calcSpace = IR_Delta_Calculation.get_calculation_space(sheet_type)
    node = calcSpace.InsertItem(calc_obj)        
    calculation = calcSpace.CreateCalculation(node,  column_id)
    return calculation.Value().Number() 


def ael_main(ael_dict):
    prf_list= list(ael_dict['portfolios'])
    output_file = ael_dict['file_path']
    email_sender = ael_dict['sender_email']
    email_receipents = list(ael_dict['email_recipients'])
    file_headers = ['Portfolio Name', "Trade", "Trader spread", "instrument spread", "Spread Difference"]
    file_name = '\Treasury_spread_diff_'+str(acm.Time.DateToday())+".csv"
    file_path = output_file+file_name
    res = []
    try:
        for prf_name in prf_list:
            prf_obj = acm.FPhysicalPortfolio[prf_name]
            if prf_obj:
                trades = [trd for trd in prf_obj.Trades() if trd.Status() not in ('Simulated', 'Void') and  \
                  acm.Time.AsDate(trd.ExecutionTime()) == acm.Time.DateToday() and trd.Instrument().InsType() == 'Deposit']
                if len(trades) >= 1:
                    for trd in trades:
                        leg = trd.Instrument().Legs()[0]
                        if leg:
                            if leg.LegType() == 'Fixed':
                                ins_spread = round(column_value('Par Rate', 'FTradeSheet', trd)*100, 3)
                                trader_spread = round(leg.FixedRate(), 3)
                                print ins_spread, trader_spread 
                            else:
                                trader_spread = round(leg.Spread(), 3)
                                ins_spread = round(FAFOUtils.get_parSpread(trd), 3)
                            spread_diff = round(trader_spread - ins_spread, 3)
                            if  trd.Portfolio().Name() == 'GT 2657 - Corp':
                                if abs(spread_diff) > 0.375:
                                    res.append([trd.Portfolio().Name(), trd.Name(), trader_spread, ins_spread, spread_diff])
                            elif abs(spread_diff) > 0.05:
                                print trd.Portfolio().Name(), ',', trd.Name(), ',', trader_spread, ',', ins_spread
                                res.append([prf_obj.Name(), trd.Name(), trader_spread, ins_spread, spread_diff])
        if len(res) >= 1:
            IR_Delta_Calculation.WriteCSVFile(file_path, res, file_headers)
            LOGGER.info('file created...')
            subject = 'Treasury trader spread difference report_'+str(acm.Time.DateToday())
            email_helper = EmailHelper(
            construct_html_body(),
            subject,
            email_receipents,
            email_sender,
            [file_path],
            "html",
            "SMTP"
            )
            email_helper.host = email_helper.get_acm_host()
            email_helper.send()
            LOGGER.info("Sent an email regarding the treasury spread difference report.")
        LOGGER.info("Process completed successfully")
    except Exception as e:
        LOGGER.error("Process completed with errors: see log")
        LOGGER.info(e)
    

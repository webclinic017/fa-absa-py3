"""-----------------------------------------------------------------------
MODULE
    exchange_inital_margin_uploader

DESCRIPTION
    Date                : 2016-11-15
    Purpose             : Uploads daily YIELDX and SAFEX initial margin amounts from a flat file from GCMS.
    Department and Desk : TODO
    Requester           : TODO
    Developer           : Paseka Motsoeneng, Sihle Gaxa
    CR Number           : TODO

HISTORY
===============================================================================
Date       Change no    Developer          Description
-------------------------------------------------------------------------------

ENDDESCRIPTION
-----------------------------------------------------------------------"""
import acm
import ael,string
import os
import csv
import xlrd
import FRunScriptGUI
import FBDPGui
import FBDPString
from at_email import EmailHelper
import glob
import sys
import xml.dom.minidom as xml
from at_ael_variables import AelVariableHandler
cs = acm.Calculations().CreateStandardCalculationsSpaceCollection()

logme = FBDPString.logme

SCRIPT_NAME     = 'new_initial_margin'
LOG_INFO        = 'no initial margins will be uploaded.'

directorySelection = FRunScriptGUI.DirectorySelection()

mail_list = 'BAGLSafexYieldXAuto@internal.barclayscapital.com'

directorySelection.SelectedDirectory('Y:\Jhb\FAReports\AtlasEndOfDay\InitialMargin')

margins = {}

calendar = acm.FCalendar['ZAR Johannesburg']
TODAY = acm.Time().DateToday()

def get_start_day_config():
    """Generate date options to be used as drop downs in the GUI."""
    return {
        'Inception': acm.Time.DateFromYMD(1970, 1, 1),
        'First Of Year': acm.Time.FirstDayOfYear(TODAY),
        'First Of Month': acm.Time.FirstDayOfMonth(TODAY),
        'PrevBusDay': calendar.AdjustBankingDays(TODAY, -1),
        'TwoBusinessDaysAgo': calendar.AdjustBankingDays(TODAY, -2),
        'TwoDaysAgo': acm.Time.DateAddDelta(TODAY, 0, 0, -2),
        'Yesterday': acm.Time.DateAddDelta(TODAY, 0, 0, -1),
        'Custom Date': TODAY,
        'Now': TODAY,
    }

def enable_custom_start_date(ael_var):
    for var in ael_variables:
        if var[0] == 'startDateCustom':
            var.enabled = ael_var.value == 'Custom Date'
            enable_custom_end_date(ael_var)

def enable_custom_end_date(ael_var):
    for var in ael_variables:
        if var[0] == 'endDateCustom':
            var.enabled = ael_var.value == 'Custom Date'


def get_ael_variables():
    directory_selection = FRunScriptGUI.DirectorySelection()
    directory_selection.SelectedDirectory(
            'Y:\Jhb\FAReports\AtlasEndOfDay\InitialMargin')
    variables = AelVariableHandler()
    variables.add('date',
        label='Date:',
        collection=sorted(get_start_day_config().keys()),
        default='Now',
        alt='Date for which the file should be selected.',
        hook=enable_custom_start_date
    )
    variables.add('startDateCustom',
        label='Start Custom:',
        default=TODAY, 
        mandatory=False,
        alt='Custom date',
        enabled=False
    )
    variables.add('endDateCustom',
        label='End Custom:',
        default=TODAY, 
        mandatory=False,
        alt='Custom date',
        enabled=False
    )
    variables.add('fileName',
        label='File name:',
        default='Exchange file name',
        alt='File name prefix. Will be followed by the date specified'
    )
    variables.add('filePath',
        label='Directory:',
        cls=directory_selection,
        default=directory_selection,
        multiple=True,
        alt='Directory where files will be uploaded from. \n'
            'A date subfolder in the form yyyy-mm-dd will '
            'be automatically added.'
    )
    variables.add('emailAddress',
        label='Email Address:',
        alt='Use a comma as a separator',
        default=mail_list,
        multiple=True
    )
    variables.add('query_trades',
            label='Trades',
            cls="FTrade",
            default="?Exchange_IniMargin_Trades",
            multiple=True,
            alt='Query folder containing trades to which initial margin will be uploaded.'
    )
    variables.extend(FBDPGui.LogVariables())
    return variables

ael_variables = get_ael_variables()

def ael_main(dictionary):

    heading = '<tr><td class=''> </td><td>SubAccount Code</td><td> Trade</td><td> Status</td><td> Reason</td></tr>'
    
    logme.setLogmeVar(SCRIPT_NAME,
                      dictionary['Logmode'],
                      dictionary['LogToConsole'],
                      dictionary['LogToFile'],
                      dictionary['Logfile'],
                      dictionary['SendReportByMail'], 
                      dictionary['MailList'],
                      dictionary['ReportMessageType'])
    
    date = get_start_day_config()[dictionary['date']]
    
    if dictionary['date'] == 'Custom Date':
    
        end_date = dictionary['endDateCustom']
        if calendar.IsNonBankingDay(None, None, end_date):
            end_date = calendar.AdjustBankingDays(end_date, 1)
            
        start_date = dictionary['startDateCustom']
        if calendar.IsNonBankingDay(None, None, start_date):
            end_date = calendar.AdjustBankingDays(start_date, 1)
    
        if start_date <= end_date:
            date_range = []
            variable_date = start_date
            while variable_date <= end_date:    
                date_range.append(variable_date)
                variable_date = calendar.AdjustBankingDays(variable_date, 1)
        else:
            raise RuntimeError("Error: start date '%s' is not before end date '%s'" %(start_date, end_date))
    else:
        date_range = [date]    
    
    filepath  = dictionary['filePath'].SelectedDirectory().Text()
    safex_filename = 'Safex_Initial_Margin'
    yieldx_filename = 'YieldX_Initial_MarginABMN'
    safex_ext = "csv"
    yieldx_ext = "xls"

    print 'Date range:',date_range
    
    for date in date_range:
        filename = dictionary['fileName']
        for_date = ael.date(date).to_string('%Y-%m-%d')
        directory = os.path.join(filepath,for_date)
        
        print 'Source file path:',directory
        
        trades = None
        margins = None
        results = None

        for getfile in os.listdir(os.getcwd()):
            safex_file_list = glob.glob('%s/%s.%s' % (directory,safex_filename, safex_ext))
            yieldx_file_list = glob.glob('%s/%s.%s' % (directory,yieldx_filename, yieldx_ext))
            
        try:
            open(safex_file_list[0], 'r')
            margins = _readSafexMarginsRecords(safex_file_list[0])
        except Exception as e:
             logme('Failed to read Safex margin from file: %s, '
                  'Error:  %s' 
                  % (directory, e), 'ERROR')
        try:
            open(yieldx_file_list[0], 'r')
            margins = _readYieldXMarginsRecords(yieldx_file_list[0])
        except Exception as e:
             logme('Failed to read YieldX margin from file: %s, '
                  'Error:  %s' 
                  % (directory, e), 'ERROR')
        
        #margins = _readMarginsRecords(directory)
        trades = dictionary['query_trades']
        extern_Id = _getExternalId(trades)
        results = _uploadMargins(margins,extern_Id,date)
        
        print "=" * 80
        for k, v in results.items():
            print k, v
        #Populate html report with results     
        html_content = '<tr><td class=''> </td><td>%s</td><td> %s</td><td> %s</td><td> %s</td></tr>'%('SubAccount','Trade','Status','Reason')
        row_count = 1
    
        if results:
            for subaccount in results:
                data = (row_count,subaccount,results[subaccount][0],results[subaccount][1],results[subaccount][2])
                html_content = html_content+'<tr><td class=''>%s</td><td>%s</td><td> %s</td><td> %s</td><td> %s</td></tr>'%data
                row_count = row_count+1
        else:
            html_content = ''
            html_content = html_content+'<tr><td class=''>Margins source file called %s is missing</td><td>Pls contact the Run-The-Bank team</td><td></td><td> </td><td></td></tr>'%directory
        
        report = _createHtmlReport(html_content)
        
        email_addresses = dictionary['emailAddress']
        if email_addresses:
            print "sending emails..."
            email_report(report, 'Production: Exchange Initial Margins Upload Report %s'%(date), email_addresses, 'Production: Exchange Initial Margins Upload Log', None)
        
    print "Completed successfully."
            
class InvalidFileFormat(Exception):
    pass

def _createHtmlReport(html_content):
    report ='''<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN"
                "http://www.w3.org/TR/html4/strict.dtd">
                <html dir="ltr" lang="en">
                <head>
                <meta http-equiv="content-type" content="text/html; charset=utf-8">
                <meta http-equiv="content-style-type" content="text/css">
                <meta http-equiv="content-script-type" content="text/javascript">
                <title></title>
                <style type="text/css">
                h1{color:blue; background: silver;
                  text-align:center;
                  font-size:20;  
                  font-family: Verdana, Arial, Helvetica, sans-serif;
                }
                td.normal{
                  color: black; background: DeepSkyBlue;
                  font-size: .8em;
                  font-family: Verdana, Arial, Helvetica, sans-serif;
                }
                td.error{
                  color: black; background: orangered;
                  font-size: .8em;
                  font-family: Verdana, Arial, Helvetica, sans-serif;
                }
                td.failure{
                  color: black; background: crimson;
                  font-size: .8em;
                  font-family: Verdana, Arial, Helvetica, sans-serif;
                  font-weight:bold;
                }
                td.success{
                  color: black; background: SpringGreen;
                  font-size: .8em;
                  font-family: Verdana, Arial, Helvetica, sans-serif;
                }
                </style>
                <script type="text/javascript">
                function toggleMe(a){
                  var e=document.getElementById(a);
                  if(!e)return true;
                  if(e.style.display=="none"){
                    e.style.display="block"
                  } else {
                    e.style.display="none"
                  }
                  return true;
                }
                </script>
                </head>
                <body>
                <h1>Production: Exchange Initial Margins Upload Process Log</h1>
                <table border="1">
                %s
                </table>
                </body></html>'''%html_content    
    
    return report
    

def _readSafexMarginsRecords(filepath):

    print "Processing safex margins from file: '%s'" %filepath

    SUBACCOUNT_CODE_INDEX = 0
    INITIAL_MARGIN_MEMBER_INDEX = 4

    with open(filepath, 'r') as file:
        rows = csv.reader(file)        
        for num in range(9):
            next(rows)
        
        for row in rows:
            if not row or not row[INITIAL_MARGIN_MEMBER_INDEX]:
                continue
            subaccount_code = row[SUBACCOUNT_CODE_INDEX]
            #Read every row before the row with Total amounts in the file
            if row[SUBACCOUNT_CODE_INDEX] == 'Total':
                 break
            margin = -float(row[INITIAL_MARGIN_MEMBER_INDEX])
  
            if subaccount_code :
                margins[subaccount_code] = margin

    return margins
    
def _readYieldXMarginsRecords(filepath):

    print "Processing yieldx margins from file: '%s'" %filepath

    workbook = xlrd.open_workbook(filepath)
    sheet = workbook.sheet_by_index(0)
    
    for row_index in range(25, sheet.nrows):
        if sheet.cell(row_index-1, 0).value == xlrd.empty_cell.value:
            continue
        subaccount_code = sheet.cell(row_index-1, 0).value
        if sheet.cell(row_index-1, 7).value == xlrd.empty_cell.value:
            continue
        margin = -float((sheet.cell(row_index-1, 7).value))
        if sheet.cell(row_index-1, 1).value == 'Total':
            break
        margins[subaccount_code] = margin

    return margins

def _getExternalId(trades):
    externIds = {}
    for trade in trades:
        ins = trade.Instrument().ExternalId1()
        externIds[ins] = trade.Oid()
        
    return externIds

def _uploadMargins(margins, trades, the_date):
    
    print 'Margins to upload:',margins
    print 'To upload to trades:',trades
    print 'For dates:',the_date
    
    upload_status={}
    
    
    for subaccount_code in margins.keys():

        if subaccount_code in trades.keys():
            print '-' * 80
            
            tradeOid = trades[subaccount_code]
            
            margin = margins[subaccount_code]
            
            trade_object = acm.FTrade[tradeOid]
            callAccount = trade_object.Instrument()
        
            if trade_object.Status() not in ('Void', 'Simulated', 'Terminated'):
                money_flows = trade_object.MoneyFlows()
  
                for money_flow in money_flows:
                    money_flow_amount = money_flow.Calculation().Projected(cs).Number()
                    money_flow_type = money_flow.Type()
                    money_flow_payday = money_flow.PayDay()
                    
                    #Delete and re-upload cash flows everytime the script runs
                    if round((money_flow_amount), 4) == round(margin, 4) \
                        and money_flow_type == 'Fixed Amount' \
                        and money_flow_payday == the_date:
                        
                        cfoid = money_flow.CashFlow().Oid()
                        cflow = acm.FCashFlow[cfoid]
                        reset_oids = [r.Oid() for r in cflow.Resets()]
                        # this cf probably had never resets,
                        # but just to be sure let's try to delete them
                        for roid in reset_oids:
                            reset = acm.Freset[roid]
                            print "Deleting reset: %d" % roid
                            reset.Delete()

                        print "Deleting cf: %d" % cfoid
                        cflow.Delete()

                if margin:
                    result = False
                    print 'Trade:', trade_object.Oid()
                    print 'Subaccount-code:', subaccount_code
                    print 'margin:', margin
                    print 'date:', the_date

                    #upload margin 
                    result = callAccount.AdjustDeposit(margin, the_date, trade_object.Quantity())
                    print "Upload successful?", result
                    
                    #Store cashflow upload status for each trade
                    if result:
                        upload_status[subaccount_code] = [tradeOid, 'Success', margin]
                    else:
                        upload_status[subaccount_code] = [tradeOid, 'Fail', 'Unknown error']
                else:
                    upload_status[subaccount_code] = [tradeOid, "Can't upload", 'Margin = 0.0']
            else:
                upload_status[subaccount_code] = [tradeOid, 'Failed', 'This trade is in Void/Simulated status.']
        else:
            upload_status[subaccount_code] = [subaccount_code, 'Failed', 'No trade linked to this subaccount in FA.']
    
    return upload_status

def email_report(body, subject, emails, email_from, attachments=None):
    
    emailHelper = EmailHelper(body, subject, list(emails), email_from, attachments)
    
    if str(acm.Class()) == "FACMServer":
        emailHelper.sender_type = EmailHelper.SENDER_TYPE_SMTP
        emailHelper.host = EmailHelper.get_acm_host()
    try:
        emailHelper.send()
    except Exception as e:
        print("!!! Exception: {0}\n".format(e))

import acm
import ael
import os
import csv
import FRunScriptGUI
import FBDPGui
import FBDPString
from at_email import EmailHelper
import xml.dom.minidom as xml

cs = acm.Calculations().CreateStandardCalculationsSpaceCollection()

logme = FBDPString.logme

calendar = acm.FCalendar['ZAR Johannesburg']
TODAY = acm.Time().DateToday()
PREVIOUSDAY = calendar.AdjustBankingDays(TODAY, -1)

# Generate date lists to be used as drop downs in the GUI.
startDateList   = {'Custom Date':TODAY,
                   'PreviousDay':PREVIOUSDAY} 
startDateKeys = startDateList.keys()
startDateKeys.sort()

def enableCustomStartDate(index, fieldValues):
    ael_variables[1][9] = (fieldValues[0] == 'Custom Date')
    ael_variables[2][9] = (fieldValues[0] == 'Custom Date')
    return fieldValues

def getEnvironment():
        arenaDataServer = acm.FDhDatabase['ADM'].ADSNameAndPort()

        arenaDataServer = arenaDataServer.lower()

        environmentSettings = acm.GetDefaultValueFromName(acm.GetDefaultContext(), acm.FObject, 'EnvironmentSettings')
        environmentSetting = xml.parseString(environmentSettings)
        host = environmentSetting.getElementsByTagName('Host')
        environment = [e for e in host if e.getAttribute('Name').lower() == arenaDataServer]

        if len(environment) != 1:
            print ('ERROR: Could not find environment settings for %s.' % arenaDataServer)
            raise Exception('ERROR: Could not find environment settings for %s.' % arenaDataServer)

        return str(environment[0].getAttribute('Setting'))

FILE_PREFIX       = 'IMR_'
SCRIPT_NAME     = 'InitialMarginUpload'
LOG_INFO        = 'no initial margins will be uploaded.'

defaultTradeFilter = acm.FTradeSelection['IM_CallAccounts']
directorySelection = FRunScriptGUI.DirectorySelection()

environment_map = {'DE':'Development:','PR':'Live:','UA':'UserTesting:','DR':'DisasterRecovery:'}

environment = environment_map[getEnvironment()[0:2]]

print 'Initial margins running from:%s'%environment

mail_list = 'paseka.motsoeneng@absacapital.com,phindile.ndiweni@absacapital.com,jakub.tomaga@barclayscapital.com,ridwaan.arbee@absacapital.com'

if environment == 'Live:':
    mail_list = 'BAGLSafexYieldXAuto@internal.barclayscapital.com'

directorySelection.SelectedDirectory('/nfs/fa/reports/EMEA/prod/FAReports/AtlasEndOfDay/PrimeServices/')
    
ael_variables = FBDPGui.LogVariables(['date', 'Date', 'string', startDateKeys, 'PreviousDay', 1, 0, 'Date for witch the file should be selected.', enableCustomStartDate, 1],
                 ['customStartDate', 'Start Date', 'string', None, PREVIOUSDAY, 0, 0, 'Custom start date', None, 0],
                 ['customEndDate', 'End Date', 'string', None, PREVIOUSDAY, 0, 0, 'Custom end date', None, 0],
                 ['nettingAccounts', 'Netting Account', 'string', None, 'ABLM', 0, 0, 'nettingAccounts', None, 1],
                 ['emailAddr', 'Email Address', 'string', None, mail_list, 0, 1, 'Use a comma as a separator.', None, 1],
                 ['filePath', 'Directory', directorySelection, None, directorySelection, 1, 1, 'Directory where files will be uploaded from. \nA date subfolder in the form yyyy-mm-dd will automatically added.', None, 1],
                )

records = {}

def ael_main(dictionary):

    date_range = []
    
    heading = '<tr><td class=''> </td><td>SubAccount Code</td><td> Trade</td><td> Status</td><td> Reason</td></tr>'
    
    logme.setLogmeVar(SCRIPT_NAME,
                      dictionary['Logmode'],
                      dictionary['LogToConsole'],
                      dictionary['LogToFile'],
                      dictionary['Logfile'],
                      dictionary['SendReportByMail'], 
                      dictionary['MailList'],
                      dictionary['ReportMessageType'])
    
    date = startDateList[dictionary['date']]
    
    nettingAccounts = dictionary['nettingAccounts'].split(',')
    
    if dictionary['date'] == 'Custom Date':
    
        day_after_end_date = calendar.AdjustBankingDays(dictionary['customEndDate'], 1)
    
        if dictionary['customStartDate'] < dictionary['customEndDate']:
            variable_date = dictionary['customStartDate']
            
            while variable_date < day_after_end_date:    
                date_range.append(variable_date)
                variable_date = calendar.AdjustBankingDays(variable_date, 1)
        else:
            print 'Error startdate has to be before enddate'
            return
    else:
        date_range = [date]    
    
    filepath  = dictionary['filePath'].SelectedDirectory().Text()
    file_prefix  = FILE_PREFIX
    
    print 'Date range:', date_range
    
    for date in date_range:
    
        formated_date  = ael.date(date).to_string('%Y%m%d')
        filename  = '%s%s.csv'%(file_prefix, formated_date)

        directory = os.path.join(filepath, date, filename)
        
        print 'Source file path:', directory
        
        trades = None
        
        margins = None
        
        results = None
        
        try:            
            open(directory, 'r')
            
            margins = _readMarginsRecords(directory, nettingAccounts)
            
            trades = _getTrades()
        
            results = _uploadMargins(margins, trades, date)
        except IOError, exc:
            print 'Cant find file:%s,%s'%(directory, exc)
        
        print results
    
        html_content = '<tr><td class=''> </td><td>%s</td><td> %s</td><td> %s</td><td> %s</td></tr>'%('SubAccount', 'Trade', 'Status', 'Reason')
    
        row_count = 1
    
        if results:
            for subaccount in results:
                data = (row_count, subaccount, results[subaccount][0], results[subaccount][1], results[subaccount][2])
            
                html_content = html_content+'<tr><td class=''>%s</td><td>%s</td><td> %s</td><td> %s</td><td> %s</td></tr>'%data
                row_count = row_count+1
        else:
            html_content = ''
            html_content = html_content+'<tr><td class=''>Margins source file called %s is missing</td><td>Pls contact the Run-The-Bank team</td><td></td><td> </td><td></td></tr>'%directory
        
        report = _createHtmlReport(html_content)
    
        email_addresses = dictionary['emailAddr']

        if email_addresses :
            print 'Emailing report to'
            email_report(report, '%sInitialMarginsUpload Process Report %s'%(environment, date), email_addresses, 'Initial Margins Upload Process Log', None)
        else:
            print 'Email address cannot be sent'

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
                <h1>Initial Margins Upload Process Log</h1>
                <table border="1">
                %s
                </table>
                </body></html>'''%html_content    
    
    return report
        
def _getTrades():
    result_set = ael.asql(acm.FSQL['InitialMarginsQuery'].Text())

    tradeList = result_set[1][0]
    
    trades = {}

    for tradeRow in tradeList:
        tradeOid = tradeRow[0]
        subAccountId = tradeRow[1]
        trades[subAccountId] = tradeOid
    
    return trades

def _readMarginsRecords(filepath, nettingAccounts):

    print 'Processing margins from file:%s'%filepath

    margins = {}
    
    for nettingAccount in nettingAccounts:
        margins[nettingAccount] = []
    
    MEMBER_CODE_INDEX = 1
    CLIENT_CODE_INDEX = 2
    SUBACCOUNT_CODE_INDEX = 3
    INITIAL_MARGIN_INDEX = 4
   
    with open(filepath, 'r') as file:
        rows = csv.reader(file)
        next(rows)
        for row in rows:
            if not row:
                continue
            try:
                nettingAccountCode = row[MEMBER_CODE_INDEX]
                clientCode = row[CLIENT_CODE_INDEX]
                subAccountCode = row[SUBACCOUNT_CODE_INDEX]
                margin = float(row[INITIAL_MARGIN_INDEX])
                
                margins_list = margins[nettingAccountCode]
                
                if subAccountCode :
                    if nettingAccountCode in nettingAccounts:
                        margins_list.append({subAccountCode:margin})
                elif not clientCode and nettingAccountCode in nettingAccounts:
                    margins_list.append({nettingAccountCode:margin})
                    
            except Exception as e:
                error = 'Failed to read initial margin for row %s : %s'%(row, e)
                '''logme('Failed to read initial margin for row %s : %s' 
                      %(row, e), 'WARNING')'''
        
    return margins

def _uploadMargins(margins, trades, date):
    
    
    print 'Margins to upload:', margins
    
    print 'To upload to trades:', trades
    
    print 'For dates:', date
    
    upload_status={}
    
    for netting_account in margins:
    
        print 'netting_account:', netting_account
        for margin_record in margins[netting_account]:
            
            subaccount_code = margin_record.keys()[0]
            
            tradeOid = ''            
            
            if subaccount_code in trades:
                print '------------------------------------------------------------------------'
            
                tradeOid = trades[subaccount_code]
                trade_object = acm.FTrade[tradeOid]
            
                margin = margin_record[subaccount_code]
            
                if trade_object.Status() not in ['Simulated', 'Void']:
                    
                    money_flows = trade_object.MoneyFlows()
                    
                    already_uploaded = False
                    
                    redemption_day = None
                    
                    for money_flow in money_flows:
                        money_flow_amount = money_flow.Calculation().Projected(cs).Number()
                        money_flow_type = money_flow.Type()
                        money_flow_payday = money_flow.PayDay()
                        
                        if money_flow_amount == margin and money_flow_type == 'Fixed Amount' and money_flow_payday == date:
                            already_uploaded = True
                        
                        if money_flow_type == 'Redemption Amount':
                            redemption_day = money_flow.PayDay()
                            
                    if not already_uploaded:
                        if not margin == 0:
                            callAccount = trade_object.Instrument()
                            
                            result = False
                            
                            print 'Trade    :', tradeOid
                            print 'Subaccount-code  :', subaccount_code
                            print 'margin   :', margin
                            print 'date     :', date
                            
                            #upload margin
                            result = callAccount.AdjustDeposit(margin, date, callAccount.Trades()[0].Quantity())
                    
                            if result:
                                upload_status[subaccount_code] = [tradeOid, 'Success', '']
                            else:
                                if TODAY > redemption_day:
                                    upload_status[subaccount_code] = [tradeOid, 'Failed', 'Trade requires to be rerated(current Redemption Amount date =%s).'%redemption_day]
                                else:
                                    upload_status[subaccount_code] = [tradeOid, 'Failed', 'Cause unknown.Contact RTB\BTB.']
                        else:
                            upload_status[subaccount_code] = [tradeOid, "Can't upload", 'Margin = 0.0']
                    
                    else:
                        upload_status[subaccount_code] = [tradeOid, 'Failed', 'This margin %s already exists in subaccount for date %s.'%(margin, date)]
                else:
                    upload_status[subaccount_code] = [tradeOid, 'Failed', 'This trade is in Void/Simulated status.']
            else:
                upload_status[subaccount_code] = [tradeOid, 'Failed', 'No trade linked to this subaccount in FA.']
        
    return upload_status

def email_report(body, subject, emails, email_from, attachments=None):
    
    emailHelper = EmailHelper(body, subject, list(emails), email_from, attachments)
    
    if str(acm.Class()) == "FACMServer":
        emailHelper.sender_type = EmailHelper.SENDER_TYPE_SMTP
        
        print EmailHelper.SENDER_TYPE_SMTP
        emailHelper.host = EmailHelper.get_acm_host()
        print EmailHelper.get_acm_host()
    try:
        emailHelper.send()
    except Exception as e:
        print("!!! Exception: {0}\n".format(e))

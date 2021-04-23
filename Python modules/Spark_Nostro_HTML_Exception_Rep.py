'''-----------------------------------------------------------------------------
PROJECT                 :  Spark Non ZAR Cashflow Feed
PURPOSE                 :  Exception report for the feed of non zar settlements to MidasPlus
DEPATMENT AND DESK      :  PCG/Ops
REQUESTER               :  Nick Bance
DEVELOPER               :  Anwar Banoo
CR NUMBER               :  XXXXXX
--------------------------------------------------------------------------------

HISTORY
================================================================================
Date       Change no Developer                 Description
--------------------------------------------------------------------------------
2011-10-25 XXXXXX                              Initial Implementation
2012-08-22 ABITFA-1512   Anwar Banoo           Added support for FO and Terminated statuses as well as curr instrument
2015-03-16               Paseka Motsoeneng     Refactored to use Spark_Query_Module, global list for curr that have no cents.
2015-09-04               Bhavik Mistry         Allow report output to only generate html and no file
2018-07-19 CHG1000679237 Libor Svoboda         Fix the Front - Sparks
'''
import sys
import time
import xlwt
import acm
import ael
from datetime import datetime
from at_email import EmailHelper
from Sparks_Config import SparksConfig


calendar = acm.FCalendar['ZAR Johannesburg']
TODAY = acm.Time().DateToday()
PREVBUSDAY = calendar.AdjustBankingDays(TODAY, -1)
NEXTBUSDAY = calendar.AdjustBankingDays(TODAY, 1)


# Dashboard Settings/imports ---------------------------------------------------------
mongo_egg_path = 'c:\\Python27\\lib\\site-packages\\pymongo-3.3.0-py2.7-win-amd64.egg'
sys.path.append(mongo_egg_path)
from pymongo import MongoClient
# -------------------------------------------------------------------------------------


class CWordAutomate:
    header = '''<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN"
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
  color: black; background: #00bcd4;
  font-size: .8em;
  font-family: Verdana, Arial, Helvetica, sans-serif;
}
td.error{
  color: black; background: orangered;
  font-size: .8em;
  font-family: Verdana, Arial, Helvetica, sans-serif;
}
td.failure{
  color: black; background: #ffc107;
  font-size: .8em;
  font-family: Verdana, Arial, Helvetica, sans-serif;
  font-weight:bold;
}
td.exception{
  color: black; background: #f44336;
  font-size: .8em;
  font-family: Verdana, Arial, Helvetica, sans-serif;
  font-weight:bold;
}
td.success{
  color: black; background: #ccffcc;
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
<body>'''

    def __init__( self):
        self.__body = ''
        self.__body += self.header
        
    def StartTable(self):
        self.__body += '<table border="1">'
        
    def EndTable(self):
        self.__body += '</table>'
        self.__body += '<br/>'
    
    def Write(self, key, trade_num, row_data):
        if key == 'Failure':
            inputClass = 'failure'
        elif key == 'Exception':
            inputClass = 'exception'    
        elif key == 'Error':
            inputClass = 'error'
        elif key == 'Success':
            inputClass = 'success'
        else:
            inputClass = 'normal'
        
        self.__body += '<tr>'
        if trade_num:
            self.__body += '<td class=%s>%s</td>' %(inputClass, trade_num)
            
        for info in row_data:
            self.__body += '<td>%s</td>' %(info)
        self.__body += '</tr>'
    
    def WriteHeader(self, sTxt):
        self.__body += '<h1>%s</h1>' %sTxt
        
    def Quit(self):
        self.__body += '</body></html>'

    def GetBody(self):
        return self.__body
        
def email_report(body, subject, emails, email_from, attachments=None):
    
    emailHelper = EmailHelper(body, subject, list(emails), email_from, attachments)
    
    if str(acm.Class()) == "FACMServer":
        emailHelper.sender_type = EmailHelper.SENDER_TYPE_SMTP
        emailHelper.host = EmailHelper.get_acm_host()

    try:
        emailHelper.send()
    except Exception as e:
        print("!!! Exception: {0}\n".format(e))       

def __reportSelection(run_date):
    classifier = {}
    classifier_backdates = {}
    
    config = SparksConfig()
    client = MongoClient(config.mongo_db_repl_set_conn_str)
    db = client.spark_db
    posts = db.posts
    
    date_format = '%Y-%m-%d'
    run_date_timestamp = time.mktime(time.strptime(run_date, date_format))
    next_day_timestamp = time.mktime(time.strptime(calendar.AdjustBankingDays(run_date, 1), date_format))
    
    cursor = posts.find({'Timestamp': {'$gte': run_date_timestamp, '$lt': next_day_timestamp}})
    
    for c in cursor:
        trade_num = c['CashflowMessage']['Identifiers'].get('TradeNumber')
        defnostro = c['CashflowMessage']['Identifiers'].get('DefaultNostro')
        status = c['CashflowMessage']['Tracking'].get('@Status')
        error = c['CashflowMessage']['Tracking'].get('Error')
        acquirer = c['CashflowMessage']['Acquirer'].get('AcquirerName')
        portfolio = c['CashflowMessage']['Acquirer'].get('AcquirerPortfolio')
        counterparty = c['CashflowMessage']['Counterparty'].get('CounterpartyName')
        account = c['CashflowMessage']['Identifiers'].get('CFCAccount')
        curr = c['CashflowMessage']['Financials'].get('CurrencyName')
        amount = c['CashflowMessage']['Financials'].get('Amount')
        instype = c['CashflowMessage']['Identifiers'].get('InstrumentType')
        midas_ref = c['CashflowMessage']['Tracking'].get('@MidasPaymentReference')
        payday = c['CashflowMessage']['Financials'].get('PayDate')
        timestamp = datetime.fromtimestamp(float(c['Timestamp'])).strftime('%d-%m-%Y %H:%M:%S')
        
        if payday >= run_date:
            if not classifier.has_key(status):
                    classifier[status] = []
            
            classifier[status].append([
                status,
                int(trade_num),
                acquirer,
                portfolio,
                counterparty,
                account,
                curr,
                float(amount),
                instype,
                payday,
                midas_ref,
                timestamp,
                error,
                defnostro
            ])
        else:
            if not classifier_backdates.has_key(status):
                    classifier_backdates[status] = []
            
            classifier_backdates[status].append([
                status,
                int(trade_num),
                acquirer,
                portfolio,
                counterparty,
                account,
                curr,
                float(amount),
                instype,
                payday,
                midas_ref,
                timestamp,
                error,
                defnostro
            ])
    
    return classifier, classifier_backdates

#Set filename to None to only generate HTML output
def __reportOutput(classifier, classifier_backdates, filename=None):
    obWord = CWordAutomate()
    
    obWord.WriteHeader('Main')
    obWord.StartTable()
    headings = ['Status', 
                 'Count']
    obWord.Write(None, None, headings)
    
    for key in classifier.keys():           
        obWord.Write(key, key, [str(len(classifier[key]))])
        
    obWord.EndTable()
    
    obWord.StartTable()
    headings = ['Status',
                 'Trade Num', 
                 'Acquirer', 
                 'Portfolio', 
                 'Counterparty',
                 'Account',
                 'Currency', 
                 'Amount', 
                 'InsType', 
                 'PayDate',
                 'Payment Ref',
                 'Timestamp',
                 'Error',
                 'DefNostro']
    obWord.Write(None, None, headings)
    
    for key in classifier.keys():
        if key != 'Success':
            for row in classifier[key]:           
                obWord.Write(key, row[0], row[1:])

    obWord.EndTable()
    
    obWord.WriteHeader('Backdates')
    obWord.StartTable()
    headings = ['Status', 
                 'Count']
    obWord.Write(None, None, headings)
    
    for key in classifier_backdates.keys():           
        obWord.Write(key, key, [str(len(classifier_backdates[key]))])
        
    obWord.EndTable()
    
    obWord.StartTable()
    headings = ['Status',
                 'Trade Num', 
                 'Acquirer', 
                 'Portfolio', 
                 'Counterparty',
                 'Account',
                 'Currency', 
                 'Amount', 
                 'InsType', 
                 'PayDate',
                 'Payment Ref',
                 'Timestamp',
                 'Error',
                 'DefNostro']
    obWord.Write(None, None, headings)
    
    for key in classifier_backdates.keys():
        if key != 'Success':
            for row in classifier_backdates[key]:           
                obWord.Write(key, row[0], row[1:])

    obWord.EndTable()
    obWord.Quit()
    
    body = obWord.GetBody()
    
    if filename:
        try:    
            wb = xlwt.Workbook()
            
            main = wb.add_sheet('Main')
            rows = []
            for key in classifier.keys():
                rows += classifier[key] 
            for i, l in enumerate([headings]):
                for j, col in enumerate(l):
                    main.write(0, j, col)
            for i, l in enumerate(rows):
                for j, col in enumerate(l):
                    main.write(i+1, j, col)
                        
            backdates = wb.add_sheet('Backdates')
            rows = []
            for key in classifier_backdates.keys():
                rows += classifier_backdates[key] 
            for i, l in enumerate([headings]):
                for j, col in enumerate(l):
                    backdates.write(0, j, col)
            for i, l in enumerate(rows):
                for j, col in enumerate(l):
                    backdates.write(i+1, j, col)
            
            wb.save(filename)    
            print 'Wrote secondary output to: %s' %(filename) 
        except Exception, err:
            print 'ERROR: Error while writing file: %s' %(err)
        
    return body
    

ael_gui_parameters = { 'windowCaption':'Spark Settlement Feed Exception Report'}
#Variable Name, Display Name, Type, Candidate Values, Default, Mandatory, Multiple, Description, Input Hook, Enabled
ael_variables = [ ['Date', 'Date', 'string', ['TODAY', 'PREVBUSDAY', 'NEXTBUSDAY'], 'TODAY', 1, 0, 'Date', None, 1],
                  ['Filepath', 'File Path', 'string', None, 'F:\\', 1, 0, 'Path', None, 1],
                  ['email', 'Email', 'bool', [0, 1], 0, 0, 0, 'Email exception report?', None, 1]]     
   

def ael_main(parameter):    
    email = parameter['email']
    
    try:
        if parameter['Date'].upper() == 'TODAY':
            runDate = TODAY
        elif parameter['Date'].upper() == 'PREVBUSDAY':
            runDate = PREVBUSDAY
        elif parameter['Date'].upper() == 'NEXTBUSDAY':
            runDate = NEXTBUSDAY
        else:
            runDate = ael.date(parameter['Date'])
            runDate = parameter['Date']            
    except Exception, e:
        ael.log('Error parsing date input:' + str(e))
        raise Exception('Error parsing date input:' + str(e))
 
    config = SparksConfig('Send')
    Filepath = config.trades_cache_location
     
    classifier, classifier_backdates = __reportSelection(runDate)
    fileName = Filepath + 'SparkNostroReport%s.xls' %(ael.date_today().to_string('%Y%m%d'))
    body = __reportOutput(classifier, classifier_backdates, fileName)
    
    if email:
        email_report(body, 'Sparks Report - %s' %config.environment, config.email_group, 'Sparks.Feed@absa.africa', [fileName])
        
    ael.log('Wrote secondary output to:::' + fileName)

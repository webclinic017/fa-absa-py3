'''--------------------------------------------------------------------------------------------------------
Date                    : 2014-02-26
Purpose                 : This script updates Front Arena Dividends/Dividend Estimates with the Corp Action Diary record published by the JSE on a daily basis.
Department and Desk     : Trade Capture Utility
Requester               : Irfaan Karim
Developer               : Rohan van der Walt
CR Number               : 1959266
--------------------------------------------------------------------------------------------------------

HISTORY
================================================================================
Date       Change no Developer                 Description
--------------------------------------------------------------------------------
2014-02-26 1959266   Rohan vd Walt             Initial Implementation
2014-05-21 1996983   Rohan vd Walt             Trade Filter exclusion fix to include archived trades and only use first 6 decimals for update comparison
'''

import acm
import csv
import os
import string
import FRunScriptGUI
import SAGEN_IT_Functions

ael_variables = []
fileSelection = FRunScriptGUI.InputFileSelection()
fileSelection.FileFilter('CSV Files (*.csv)|*.csv')
directorySelection=FRunScriptGUI.DirectorySelection() 
nsTime = acm.Time()
PRECISION = 6

calendar = acm.FCalendar['ZAR Johannesburg']
today = acm.Time().DateNow()
nextBusinessDay = calendar.AdjustBankingDays(today, 1)
prevBusinessDay = calendar.AdjustBankingDays(today, -1)

customDateKey = 'Custom Date'
runDateList = {
                   'Next Business Day': nextBusinessDay,
                   customDateKey: today,
                   'Today': today,
                   'Previous Business Day': prevBusinessDay,
                   }
runDateKeys = runDateList.keys()
runDateKeys.sort()

def float_eq(a, b, precision=6):
    '''
    Used to perform float comparison up to precision decimals
    '''
    a = int(a*(10**precision))
    b = int(b*(10**precision))
    return a == b
        
def enableCustomDate(index, fieldValues):
    ael_variables[1][9] = (fieldValues[0] == customDateKey)
    return fieldValues

def emailFieldHook(index, fieldValues):
    test = (fieldValues[4] == 'Yes')
    ael_variables[5][9] = test
    ael_variables[5][5] = test
    return fieldValues

ael_gui_parameters = {'windowCaption':'Dividend Importing Script'}
# Variable Name, Display Name, Type, Candidate Values, Default, Mandatory, Multiple, Description, Input Hook, Enabled
ael_variables.append(['runDate', 'Run Date', 'string', runDateKeys, 'Today', 1, 0, 'System Date to use - ExDiv date will be compared to this date when determining if a dividend should belong in Actual or Estimate table', enableCustomDate, 1])
ael_variables.append(['runDateCustom', 'Custom Run Date', 'string', None, today, 1, 0, 'System Date to use - ExDiv date will be compared to this date when determining if a dividend should belong in Actual or Estimate table\nFormat: yyyy-mm-dd', None, 0])
ael_variables.append(['fileLocation', 'Input File Path', fileSelection, None, fileSelection, 1, 1, 'Location of Pipe Delimited Value File received from JSE via Prime IT', None, 1])
ael_variables.append(['reportLocation', 'Report Output Path', directorySelection, None, directorySelection, 1, 1, 'Import Summary Report Location\nFilename: DividendImport_YYYYMMDD.txt - using runDate\'s date', None, 1])
ael_variables.append(['sendMail', 'Send Email?', 'string', ['No', 'Yes'], 'No', 1, 0, 'Do background emailing of report?', emailFieldHook, 1])
ael_variables.append(['Emails', 'Email Recipients', 'string', None, None, 1, 1, 'Email destinations if running from backend. Use comma seperated email addresses if you want to send report to multiple users.', None, 1])

class Summary:
    def __init__(self):
        self.sectionDict = {}
        self.title = 'Summary'

    def addSection(self, sectionName):
        if sectionName not in self.sectionDict:
            self.sectionDict[sectionName] = []
        
    def addToSection(self, section, item):
        self.sectionDict[section].append(item)

    def setTitle(self, title):
        self.title = title

    def __str__(self):
        result = ''
        result += '='*(14+len(self.title)) + '\n'+' '*7+self.title+' '*7+'\n' + '='*(14+len(self.title)) +'\n'
        for sec in self.sectionDict:
            result += '='*len(sec) +'\n' + sec +'\n'+ '='*len(sec) +'\n'
            if len(self.sectionDict[sec]) > 1:  #Assume 1st line in section is always the header - e.g. Equity,ExDiv,Amount
                for i in self.sectionDict[sec]:
                    result += i +'\n'
            else:
                result += 'NONE\n'
            result += '=-'*(len(sec)/2) +'\n'
        return result
       
    def writeToFile(self, path, name):
        try:
            f = open(os.sep.join([path, name]), "a")
            f.write(str(self))
            f.close()
            print 'Summary written to', os.sep.join([path, name])
        except Exception, e:
            print 'ERROR: Could not write report', e
            raise e
        
def _toDate(yyyyMMdd):
    '''
    returns acm date from a string in 'yyyyMMdd' format
    '''
    year, month, day = yyyyMMdd[:4], yyyyMMdd[4:6], yyyyMMdd[-2:]
    return nsTime.DateFromYMD(year, month, day)   
   
   
class DividendHandler:
    '''
    Handler for a JSE Corp Action Cash Dividend (CD) Record.
    '''
    def __init__(self, divData, divImportSummary, sysDate):
        self.divData = divData
        self.divImportSummary = divImportSummary
        self.sysDate = sysDate
        
        for i in self.divData:
            self.divData[i] = self.divData[i].strip()
            
        print '=-'*15, self.divData['Code'], '-='*15
        self.rcrdDay = _toDate(self.divData['RecordDate'])
        self.pDay = _toDate(self.divData['PayDate'])
        self.exDate = _toDate(self.divData['ExDate'])
        self.amount = float(self.divData['GrossRateOption1'])/100
        self.cal = acm.FCalendar['ZAR Johannesburg']
        
    def equityExists(self):
        self.eq = acm.FStock['ZAR/' + self.divData['Code']]
        if self.eq:
            return True
        print "Stock 'ZAR/" + self.divData['Code'] + "' doesn't exist"
        return False
    
    def hasDivStream(self):
        '''
        if equity exists - checks (and allocates) if a dividend stream is mapped to the equity
        '''
        if self.eq:
            self.divStream = self.eq.MappedDividendStream().Parameter()
            if self.divStream:
                self.context = self.eq.MappedDividendStream().MappedInContext().Name()
                return True
        print "Instrument 'ZAR/" + self.divData['Code'] + "' has no mapped dividend estimate stream"
        return False
                
    def divEstimateExists(self):
        '''
        Tries to find (and allocate) a dividend estimate in the mapped div stream with the following rules
        - if existing dividend estimate's pay date is within 20 business days of JSE file's dividend - it is a match
        - if Description.lower() is 'spec' or 'special', it will not see it as a match.
        '''
        if self.divStream:
            print 'Checking if Dividend Estimate exists'
            for d in self.divStream.Dividends():
                if abs(self.cal.BankingDaysBetween(self.pDay, d.PayDay())) <= 20 and d.Description().lower() not in ['special', 'spec']:
                    self.divEstimate = d
                    print 'Dividend Estimate found'
                    return True
            print 'Not found'
        return False
    
    def divExists(self):
        '''
        Tries to find (and allocate) a dividend in the historical dividend table with the following rule
        - if existing dividend's pay date is within 20 business days of JSE file's dividend - it is a match
        - if Description.lower() is 'spec' or 'special', it will not see it as a match.
        '''
        if self.eq:
            print 'Checking if Dividend exists'
            for d in self.eq.Dividends():
                if abs(self.cal.BankingDaysBetween(self.pDay, d.PayDay())) <= 20 and d.Description().lower() not in ['special', 'spec']:
                    self.div = d
                    print 'Dividend found'
                    return True
        return False
   
    def createDividendEstimate(self):
        print 'Creating Dividend Estimate'
        d = acm.FDividendEstimate()
        d.DividendStream(self.divStream)
        d.Currency( acm.FCurrency['ZAR'] )
        d.DividendType(SAGEN_IT_Functions.GetEnum('DividendEstimationType', 'Declared') )
        d.ExDivDay(self.exDate)
        d.Amount(self.amount)
        d.RecordDay(self.rcrdDay)
        d.PayDay(self.pDay)
        d.Description(self.divData['DivType'])
        d.TaxFactor(1.0)
        d.Commit()
        print 'Done\nSetting Additional Info on Div Estimate'
        self.divImportSummary.addToSection('Dividend Estimates Created', ','.join([self.eq.Name(), self.exDate, str(self.amount)]))
        print 'Done'
   
    def updateDividendEstimate(self):
        '''
        Checks if dividend estimate is the same as JSE record, if not, update
        '''
        print self.divEstimate.ExDivDay(), self.exDate
        if self.divEstimate.DividendType() != 'Declared' or \
         not float_eq(self.divEstimate.Amount(), self.amount) or \
         self.divEstimate.ExDivDay() != self.exDate or \
         self.divEstimate.RecordDay() != self.rcrdDay or \
         self.divEstimate.PayDay() != self.pDay or \
         self.divEstimate.Description().lower() != self.divData['DivType'].lower() or \
         self.divEstimate.Currency() != acm.FCurrency['ZAR']:
            print 'Updating Dividend Estimate'
            oldAmount = self.divEstimate.Amount()
            self.divEstimate.DividendType(SAGEN_IT_Functions.GetEnum('DividendEstimationType', 'Declared') )
            self.divEstimate.Amount(self.amount)
            self.divEstimate.ExDivDay(self.exDate)
            self.divEstimate.RecordDay(self.rcrdDay)
            self.divEstimate.PayDay(self.pDay)
            self.divEstimate.Description(self.divData['DivType'])
            self.divEstimate.Currency(acm.FCurrency['ZAR'])
            self.divEstimate.Commit()
            self.divImportSummary.addToSection('Dividend Estimates Updated', ','.join([self.eq.Name(), self.exDate, str(oldAmount), str(self.amount) ]))
            print 'Done'
        else:
            print 'Nothing to update on Dividend Estimate'
    
    def createDividend(self):
        print 'Creating Dividend'
        d = acm.FDividend()
        d.Instrument(self.eq)
        d.Amount(self.amount)
        d.RecordDay(self.rcrdDay)
        d.PayDay(self.pDay)
        d.ExDivDay(self.exDate)
        d.Description(self.divData['DivType'])
        d.Currency( acm.FCurrency['ZAR'] )
        d.TaxFactor(1.0)
        d.Commit()
        self.divImportSummary.addToSection('Dividends Created', ','.join([self.eq.Name(), self.exDate, str(self.amount)]))
        print 'Done'
    
    def updateDividend(self):
        '''
        Checks if dividend is the same as JSE record, if not, update
        '''
        if not float_eq(self.div.Amount(), self.amount) or \
         self.div.ExDivDay() != self.exDate or \
         self.div.RecordDay() != self.rcrdDay or \
         self.div.PayDay() != self.pDay or \
         self.div.Description().lower() != self.divData['DivType'].lower() or \
         self.div.Currency() != acm.FCurrency['ZAR']:
            print 'Updating Historical Dividend'
            oldAmount = self.div.Amount()
            self.div.Amount(self.amount)
            self.div.ExDivDay(self.exDate)
            self.div.RecordDay(self.rcrdDay)
            self.div.PayDay(self.pDay)
            self.div.Description(self.divData['DivType'])
            self.div.Currency( acm.FCurrency['ZAR'] )
            self.div.Commit()
            self.divImportSummary.addToSection('Dividends Updated', ','.join([self.eq.Name(), self.exDate, str(oldAmount), str(self.amount)]))
            print 'Done'
        else:
            print 'Nothing to update on Historical Dividend'
        
    def removeDividendEstimate(self):
        if self.divEstimate:
            print 'Removing Dividend Estimate'
            self.divEstimate.Delete()
            self.divImportSummary.addToSection('Dividend Estimates Removed', ','.join([self.eq.Name(), self.exDate, str(self.amount)]))
            print 'Done'
            
    def updateEquityDividends(self):
        '''
        Main Dividend and Dividend Estimate Updating Logic
        '''
        if self.equityExists():
            if self.sysDate == self.exDate:
                try:
                    acm.BeginTransaction()
                    if self.divExists():
                        self.updateDividend()
                    else:
                        self.createDividend()
                    acm.CommitTransaction()
                except Exception, e:
                    print "Exception:", e
                    acm.AbortTransaction()
            else:
                self.divImportSummary.addToSection('Excluded because of exDiv date', ','.join([self.eq.Name(), self.exDate, str(self.amount)] ))

def _isValidRecord(row, divImportSummary):
    '''
    Only process records where Dividend Type is Final or Interim
    If the instrument is in the "Exclude Instruments Trade Filter, it will note it in the summary, and also not process the dividend further.
    '''
    try:
        return row['EventType'].strip() in ['CD', 'RE'] and row['DivType'].strip() in ['Final', 'Interim']
    except Exception, e:
        print 'ERROR: Skipped row:', e
        print 'ROW:', row
    return False        


def ael_main(dict):
    noErrors = True                                                     #Flag to use for Completed Successfully output
    if dict['runDate'] == 'Custom Date': 
        sysDate = dict['runDateCustom']
    else:
        sysDate = runDateList[dict['runDate']]
    print 'Using Run Date: ' + sysDate

    with open(str(dict['fileLocation']), 'r') as csvFile:
        reader = csv.DictReader(csvFile, delimiter='|')
        divImportSummary = Summary()
        divImportSummary.addSection('Dividends Created')
        divImportSummary.addToSection('Dividends Created', ','.join(['Equity', 'ExDiv Date', 'Amount']))
        divImportSummary.addSection('Dividends Updated')
        divImportSummary.addToSection('Dividends Updated', ','.join(['Equity', 'ExDiv Date', 'Old Amount', 'New Amount']))
        divImportSummary.addSection('Dividend Estimates Removed')
        divImportSummary.addToSection('Dividend Estimates Removed', ','.join(['Equity', 'ExDiv Date', 'Amount']))
        divImportSummary.addSection('Dividend Estimates Created')
        divImportSummary.addToSection('Dividend Estimates Created', ','.join(['Equity', 'ExDiv Date', 'Amount']))
        divImportSummary.addSection('Dividend Estimates Updated')
        divImportSummary.addToSection('Dividend Estimates Updated', ','.join(['Equity', 'ExDiv Date', 'Old Amount', 'New Amount']))
        divImportSummary.addSection('In-Scope but Actuals Excluded')
        divImportSummary.addToSection('In-Scope but Actuals Excluded', ','.join(['Equity', 'ExDiv Date', 'Amount']))
        divImportSummary.addSection('In-Scope but Estimates Excluded')
        divImportSummary.addToSection('In-Scope but Estimates Excluded', ','.join(['Equity', 'ExDiv Date', 'Amount']))              

        sampleRow = None
        for row in [r for r in reader if _isValidRecord(r, divImportSummary)]:
            try:
                DH = DividendHandler(row, divImportSummary, sysDate)
                DH.updateEquityDividends()
                if not sampleRow:
                    sampleRow = row
            except Exception, e:
                noErrors = False
                print 'ERROR:', e
                
        divImportSummary.setTitle('Dividend Import Summary - Business Date: ' + sampleRow['BusinessDate'] + '  Import Date: ' + sysDate + '  Actual Date: ' + nsTime.DateToday())
        print divImportSummary
        divImportSummary.writeToFile(str(dict['reportLocation']), 'DividendImport_'+sysDate+'.csv')

        if dict['sendMail'] == 'Yes':
            try:
                print 'Sending report email'
                try:
                    ENVIRONMENT = ' - ' + acm.FInstallationData.Select('').At(0).Name()
                except:
                    ENVIRONMENT = ''
                for address in dict['Emails']:
                    sendMail('ABCapITRTBFrontArena@absacapital.com', address, 'Front Arena Dividend Import Summary - ' + sampleRow['BusinessDate'] + ENVIRONMENT, str(divImportSummary))
                print 'Done sending report emails'
            except Exception, e:
                noErrors = False
                print 'ERROR: Could not send emails - ', e
            
        if acm.FCalendar['ZAR Johannesburg'].BankingDaysBetween(_toDate(sampleRow['BusinessDate'].replace('-', '')), sysDate) > 1:
            noErrors = False
            print '\nWARNING ONLY - File used to import is using old business date'
        if noErrors:
            print '\nCompleted Successfully'
        else:
            print '\nCompleted with Errors'

def sendMail(FROM, TO, SUBJECT, MSG):
    import smtplib
    HOST = acm.GetCalculatedValue(0, acm.GetDefaultContext().Name(), 'mailServerAddress').Value()
    BODY = string.join((
        "From: %s" % FROM,
        "To: %s" % TO,
        "Subject: %s" % SUBJECT,
        "", MSG), "\r\n")
        
    if not HOST:
        raise Exception("Could not initialise the smtp Host")

    server = smtplib.SMTP(HOST)
    server.sendmail(FROM, TO.split(','), BODY)
    server.quit()

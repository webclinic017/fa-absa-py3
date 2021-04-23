"""-----------------------------------------------------------------------------------------------------------------------------------------------

HISTORY
==================================================================================================================================================
Date                Change no Developer                 Description
--------------------------------------------------------------------------------------------------------------------------------------------------
                    Faize Adams                         Use the chorusHierarchy to retrieve data on all
                                                        portfolios in Front Arena and store it in the Text Object table.
                                                        Keep a history of changes in the chorus data.
                                                        
2017-08-14           Sihle Gaxa                         Added an add info 'Reg_Classification' on all Portfolios 
                                                        in FA to make Front regulatory classification aware as part of
                                                        Fix the Front project business ask
                                                        
--------------------------------------------------------------------------------------------------------------------------------------------------
"""
import json
import time
import acm
import ChorusHierarchy
import at_logging
import FBDPGui
from at_email import EmailHelper
from at_ael_variables import AelVariableHandler
from at_addInfo import save as save_add_info

TEXTOBJECTNAME = 'chorusHierarchyData'
DEFAULTLIBPATH = "S:\\Chorus\\chorusHierarchy\\"
HISTORYOBJECTNAME = 'chorusHistory'
MAXHISTORYOBJECTS = 10
LOGOUTPUT = True

calendar = acm.FCalendar['ZAR Johannesburg']
TODAY = acm.Time().DateToday()

LOGGER = at_logging.getLogger()

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
        if var[0] == 'CustomDate':
            var.enabled = ael_var.value == 'Custom Date'


def get_ael_variables(): 
    variables = AelVariableHandler()
    
    variables.add('date',
            label='Date:',
            collection=sorted(get_start_day_config().keys()),
            default='Now',
            alt='Date for which the file should be selected.',
            hook=enable_custom_start_date
        )

    variables.add('CustomDate',
            label='Custom Date:',
            default=TODAY, 
            mandatory=False,
            alt='Custom date',
            enabled=False
        )
    variables.add('name',
            label='Name of text object',
            default=TEXTOBJECTNAME,
            enabled=False)

    variables.add('libpath',
            label='Path to chorusHierardhy.dll',
            default=DEFAULTLIBPATH,
            enabled=True)
                      
    variables.add('emailAddress',
            label='Email Address:',
            alt='Use a comma as a separator',
            multiple=True)
        
    variables.extend(FBDPGui.LogVariables())
    return variables

ael_variables = get_ael_variables()

def log(message):
    if LOGOUTPUT:
        LOGGER.info(message)

def getFAPortfolios():
    """Query to get all portfolio number in Front Arena."""
    log('Getting all Front Arena portfolio numbers')
    portfolios = acm.FPhysicalPortfolio.Select("")
    result = ["%s" % port.Oid() for port in portfolios]
    log(result)
    return result

def saveAsTextObject(data):
    """Save data as a text object."""
    log("Saving text object %s" %(TEXTOBJECTNAME))
    try:
        textObject = acm.FCustomTextObject()
        textObject.Name(TEXTOBJECTNAME)
        log('Saving %s text object data :' %(TEXTOBJECTNAME))
        textObject.Text((data))
        textObject.Commit()
        log('%s succesfully saved in the database' %(TEXTOBJECTNAME))
    except Exception as e:
        log('Error: %s ' % str(e))

def getCurrentHistory():
    """Gets the historical chorus data from DB."""
    log('Getting the historical chorus data from database for text object %s' %(HISTORYOBJECTNAME))
    result = acm.FCustomTextObject.Select("name like %s*" % HISTORYOBJECTNAME)
    log('Objects in current history with name similar to %s :' %(HISTORYOBJECTNAME))
    log('%s' % result)
    return result


def moveToHistory(textObject):
    """If there was a change in chorus data, the old object is moved to history.
    Checks if we have reached the max history length, and trims it accordingly."""
    log('Checking if we have reached the max history length for chorus text objects, and trimming accordingly')
    currentHistory = getCurrentHistory()
    if len(currentHistory) >= MAXHISTORYOBJECTS:
        log('We have reached the max history length for text objects = %s'%MAXHISTORYOBJECTS)
        try:
            fullHistory = [(to.Name(), to.CreateTime()) for to in currentHistory]
            log('Chorus text objects currently in history: %s' % MAXHISTORYOBJECTS)
            log(fullHistory)
            oldestTEXTOBJECTNAME = min(fullHistory, key=lambda item: item[1])[0]
            log('Oldest text object name found in hitory list: %s'% oldestTEXTOBJECTNAME)
            oldestTextObject = acm.FCustomTextObject[oldestTEXTOBJECTNAME]
            log('Deleting oldest text object : %s from the list' %(oldestTextObject.Name()))
            oldestTextObject.Delete()
        except Exception as e:
            log('Error moving text object to chorus history list : %s' % str(e))
        
        newName = HISTORYOBJECTNAME + str(time.strftime("%Y%m%d%H%M%S"))
        
    try:
        log('Moving text object: %s to history' % newName)
        textObject.Name(newName)
        textObject.Commit()
        log('%s committed successfully as a text object' % newName)
    except Exception, e:
        log('Error moving current data to history: %s' % str(e))


def refreshData(freshChorusData, email_addresses, for_date):
    """Reads chorus data we have in Front Arena and compares it to the data
    recieved from the hierarchy control service. If there is a change, the old
    data is copied to history and new data is added to Front Arena.
    If there were no changes since the last update, we do nothing."""
    log('Reading chorus data stored in Front Arena and comparing it to the data recieved from the RDS hierarchy control service')
    jsonData = json.dumps(freshChorusData)
    currentTextObject = acm.FCustomTextObject[TEXTOBJECTNAME]
    if currentTextObject:
        log('Chorus text object %s found in Front Arena' % TEXTOBJECTNAME)
        dbChorusData = json.loads(currentTextObject.Text())
        log(dbChorusData)
        if freshChorusData != dbChorusData:
            log('Data has changed since last refresh \n'
                'Moving updated text object %s to Chorus History' %TEXTOBJECTNAME)
            moveToHistory(currentTextObject)
            saveAsTextObject(jsonData)
            updateFrontPorts(freshChorusData, email_addresses, for_date)
        else:
            log('Chorus hierarchy data in FA database is up to date.')
    else:
        saveAsTextObject(jsonData)

def updateFrontPorts(chorusData, email_addresses, for_date):
    print 'Updating Front Arena Portfolios with reg classification flag from RDS Chorus Service'
    html_content = '<tr><td class=''> </td><td>%s</td><td> %s</td><td> %s</td></tr>'%('Status', 'Classification', 'Error')
    row_count = 1
    try:
        for pfId in chorusData.keys():
            log('Processing portfolio number : %s' % pfId)
            if pfId == 'errorCode':
                log('Received portfolio id errorCode. Will be skipping this item.')
                continue
            portfolios = acm.FPhysicalPortfolio.Select('oid = %i'  %int(pfId))
            if len(portfolios) == 0:
                log('No portfolio in FA with id %s' % pfId)
                continue
            elif len(portfolios) == 1:
                regClassification = chorusData[pfId]['bankingTrading']
                pf = portfolios[0]
                bookName = pf.Name()
                log('Updating %s Reg_Classification add info' % bookName)
                save_add_info(pf, 'Reg_Classification', regClassification)
                log('Portfolio updated successfully')
                log('Portfolio: %s and Reg_Classification Add Info : %s' %(bookName, pf.add_info('Reg_Classification')))
            else:
                log('Multiple portfolios in FA with id %s' % pfId)
                continue
    except Exception as e:
        data = (row_count, 'Portfolio update error', 'Reg_Classification add info update in FA failed', str(e))
        html_content = html_content+'<tr><td class=''>%s</td><td>%s</td><td> %s</td><td>%s</td></tr>'%data
        row_count = row_count+1
        log("sending RTB an email...")
        log(str(e))
        report = _createHtmlReport(html_content)
        email_report(report, 'RDS Chorus Service Report %s' % for_date, email_addresses, 'RDS Chorus Service Error Notification', None)
        
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
                h1{color:black; background: pink;
                  text-align:center;
                  font-size:20;  
                  font-family: Verdana, Arial, Helvetica, sans-serif;
                }
                td.normal{
                  color: black; background: lightBlue;
                  font-size: .8em;
                  font-family: Verdana, Arial, Helvetica, sans-serif;
                }
                td.error{
                  color: black; background: orange;
                  font-size: .8em;
                  font-family: Verdana, Arial, Helvetica, sans-serif;
                }
                td.failure{
                  color: black; background: red;
                  font-size: .8em;
                  font-family: Verdana, Arial, Helvetica, sans-serif;
                  font-weight:bold;
                }
                td.success{
                  color: black; background: green;
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
                <h1>Banking Book Chorus Service Notification</h1>
                <table border="1">
                %s
                </table>
                </body></html>'''%html_content    
    
    return report
    
def email_report(body, subject, emails, email_from, attachments=None):
    '''Emailing relevant stakeholders when there is something wrong with the service'''
    emailHelper = EmailHelper(body, subject, list(emails), email_from, attachments)
    
    if str(acm.Class()) == "FACMServer":
        emailHelper.sender_type = EmailHelper.SENDER_TYPE_SMTP
        emailHelper.host = EmailHelper.get_acm_host()
    try:
        emailHelper.send()
    except Exception as e:
        print("Could not send mail - !!! Exception: {0}\n".format(e))

def ael_main(aelDict):
    updateStatus = {}
    for_date = aelDict['date']
    if aelDict['date'] == 'Custom Date':
        for_date = aelDict['CustomDate']
    else:
        for_date = get_start_day_config()[aelDict['date']]
    
    libPath = aelDict['libpath']
    email_addresses = aelDict['emailAddress']
    
    log('Library path: %s' %libPath) 
    if libPath == None or bool(libPath) == False:
        log('Please enter valid library path, Chorus library path cannot be empty or None type')
        return

    portfolios = getFAPortfolios()
    
    try:
        chorus = ChorusHierarchy.ChorusStreamDelegate(libPath)
        log('Retrieving current chorus data from RDS Chorus Service:')
        
        try:
            chorusData = chorus.getAllData(portfolios)
            log('Chorus Data:')
            log(chorusData)
            refreshData(chorusData, email_addresses, for_date)
        except Exception as e:
            updateStatus['No portfolios found in Chorus'] = ['Chorus Service may be down', str(e)]
    
    except Exception as e:
        updateStatus['Connection Error'] = ['RDS Chorus Service Connection failed', str(e)]
        log('Could not connect to chorus service using library path %s. Error: %s' %(libPath, str(e)))
        
    html_content = '<tr><td class=''> </td><td>%s</td><td> %s</td><td> %s</td></tr>'%('Status', 'Classification', 'Error')
    row_count = 1

    if updateStatus:
        for status in updateStatus:
            data = (row_count, status, updateStatus[status][0], updateStatus[status][1])
            html_content = html_content+'<tr><td class=''>%s</td><td>%s</td><td> %s</td><td>%s</td></tr>'%data
            row_count = row_count+1
            log("sending RTB an email...")
            report = _createHtmlReport(html_content)
            email_report(report, 'RDS Chorus Service Report %s'%for_date, email_addresses, 'RDS Chorus Service Error Notification', None)
    else:
        log('Front Arena contains updated chorus data')
        
    log("Completed")

'''
Date                    : 2010-06-04
Purpose                 : To check all newly created (after startdate variable) portfolios for SL Additional Info field values.
Department and Desk     : Securities Lending
Requester               : Linda Breytenbach, Natasha Williams
Developer               : Rohan van der Walt
CR Number               : 348355

HISTORY
================================================================================
Date       Change no Developer                 Description
--------------------------------------------------------------------------------
2010-06-04 348355    Rohan vd Walt             Initial Implementation
2010-06-29 356559    Rohan vd Walt             Formatting Changes and show list of "SL Additional Info Completed" portfolios
2014-04-03 1861240   Rohan vd Walt             Use smtplib to send emails and specify FROM address, and always output file report.
'''

import acm
import ael
import time
import string

def TaskOrFront(index, fieldValues):
    test = (fieldValues[0] == 'Yes')
    #ael_variables[4][9] = not test
    #ael_variables[4][5] = not test
    ael_variables[3][9] = test
    ael_variables[3][5] = test
    return fieldValues

def listOfPortfolios():
    return acm.FPhysicalPortfolio.Select('')

ael_variables = [
['sendMail', 'Send Email?', 'string', ['No', 'Yes'], 'No', 1, 0, 'Do background emailing?', TaskOrFront, 1],
['Portfolios', 'Portfolios', acm.FPhysicalPortfolio, listOfPortfolios(), acm.FCompoundPortfolio['9806'], 1, 1, 'Portfolios to do check on', None, 1],
['StartDate', 'StartDate', 'date', None, None, 0, 0, 'Start date from when new portfolios are checked. If left blank, will default to 5 days ago', None, 1],
['Emails', 'Emails', 'string', None, None, 1, 1, 'Email destinations if running from backend. Use comma seperated email addresses if you want to send report to multiple users.', None, 1],
['OutputPath', 'OutputPath', 'string', None, 'C:\\', 1, 0, 'Directory where output file should be written, if running on frontend', None, 1]
]

ael_gui_parameters = {'windowCaption':'New portfolio Additional info check report'}

def ael_main(dict):
    if not dict['StartDate']:   #Defaults to week ago if input was blank
        dict['StartDate'] = acm.Time().DateAddDelta(acm.Time().DateToday(), 0, 0, -7)
    nsTime = acm.Time()
    start = nsTime.AsDate(dict['StartDate'])
    listOfPortfolios = dict['Portfolios']
    result, result2 = [], []
    for i in listOfPortfolios:
        result, result2 = checkPortfolio(i, result, result2, start)
    missing = getMessage('New Portfolio SL Additional Info Report  -  Start Date: ' + start + '\n\nThe following portfolios do not have all the SL Additional Info fields set:\n', result, '--END OF REPORT--\n\n\n')
    complete = getMessage('The following portfolios have all the SL Additional Info fields set:\n', result2, '--END OF REPORT--\n')
    
    if dict['sendMail'] == 'Yes':
        for address in dict['Emails']:
            sendMail('ABCapITRTBFrontArena@absacapital.com', address, 'New Portfolio SL Additional Info Report  -  Start Date: ' + start, missing + complete)

    file = None
    try:
        filepath = dict['OutputPath']+'NewPortfolios_AdditionalInfoCheck_'+nsTime.DateToday()+'.csv'
        file = open(filepath, 'wt')
        file.write(missing + complete)
    except:
        print 'ERR: Could not open/write file'
    finally:
        if file:
            file.close()
            print 'File written to:', filepath
    print 'SL Additional Info check on portfolios - DONE'

def checkPortfolio(port, result, result2, start):
    if port.Compound():
        for ol in port.OwnerLinks():
            result, result2 = checkPortfolio(ol.MemberPortfolio(), result, result2, start)
    else:
        nsTime = acm.Time()
        if DateFromTime(port.CreateTime()) >= start:
            if (port.add_info('SL_AllocatedDesk') == '' or \
              port.add_info('SL_Portfolio_Type') == '' or \
              port.add_info('SL_ReservedStock') == '' or \
              port.add_info('SL_Sweeping') == ''):
                result.append([port.Name()])
            else:
                result2.append([port.Name()]) 
    return result, result2

def getMessage(header, result, footer):
    str = header
    for i in result:
        for j in i:
            str += j + '\t\t'
        str += '\n'
    if len(result) == 0:
        str += 'None\n'
    str += footer
    return str
    
def DateFromTime(secs):
    '''
    Custom epoch seconds conversion to instance of acm.FDateDomain
    FNamespaceTime.DateFromTime() did not work correctly if ran from backend
    '''
    ttime = time.localtime(secs)
    nsTime = acm.Time()
    date = nsTime.DateFromYMD(ttime[0], ttime[1], ttime[2])
    return date

def sendMail(FROM, TO, SUBJECT, MSG):
    import smtplib
    HOST = acm.GetCalculatedValue(0, acm.GetDefaultContext().Name(),
            'mailServerAddress').Value()
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

'''-----------------------------------------------------------------------
MODULE
    SAB_Trades

DESCRIPTION
    This module is called by the SAB_Trades.

    Department and Desk : Credit Desk
    Requester           : Digone Tselane
    Developer           : Faize Adams

    History:
    When: 	  Who:		What:       
    2015-11-10    Faize Adams	Created
    2010-11-12    Bushy Ngwako  Added email function

END DESCRIPTION
-----------------------------------------------------------------------'''

import acm, csv, re
from at_email import EmailHelper


ael_variables = [
                    ['input', 'Input File', 'string', None, 'C:\\Users\\adamsfai\\Desktop\\Trades_MDS.csv'],
                    ['outputLocation', 'Output Location', 'string', None, 'C:\\Users\\adamsfai\\Desktop\\SAB_Trades.csv'],
                    ['emailAddr', 'Email Address', 'string', None, 'DigoneThabiso.Tselane@barclays.com', 0, 1, 'Email', None, 1]
                ]

def writeOutput(output, outputLocation):
    outfile = open(outputLocation, 'wb')
    writer = csv.writer(outfile, dialect='excel')
    
    for line in output:
        writer.writerow(line)

def invertSign(number):
    if len(number) > 0:
        match = re.findall('[0-9]*[.]*[0-9]*', number)
        number = float("".join(match))
        return number * -1
    else:
        return 0
        
def normalizeFromUnicode(inString):
    if len(inString) > 0:
        match = re.findall('[-]*[0-9]*[.]*[0-9]*', inString)
        number = "".join(match)
        return number
    else:
        return ''
    
def readInput(input):
    output = []
    
    with open(input, 'rU') as file:
        contents = csv.reader(file)
        counter = 0 

        switch = {'Buy':'Sell', 'Sell':'Buy'}

        for row in contents:
            if counter < 5 and len(row) > 0:
                output.append(row)
                counter += 1
            elif len(row) > 12:
                colB = row[1]
                if type(row[5]) is unicode:
                    colF = row[5].encode('ascii', 'ignore')
                else:
                    colF = row[5]

                if "PB_CFD" in str(colF)[:6]: #portfolios that start with PB_CFD
                    colJ = row[9]
                    colJ.encode('ascii', 'ignore')
                    row[9] = colF[7:colF.index('_', 8, len(colF))] #change counter party to portfolio name
                    row[3] = invertSign(row[3]) #invert sign of quantity
                    row[5] = colF[:colF.index('_CR')] #remove _CR from portfolio names
                        
                    row[11] = switch[row[11].encode('ascii', 'ignore')] #switch buy<->sell
                else:
                    row[2] = normalizeFromUnicode(row[2]) #for some reason these rows contain weird chars
                    row[3] = normalizeFromUnicode(row[3])
                if colB != '':   
                    output.append(row)
    return output

def email_report(body, subject, emails, email_from, attachments=None):
    """ Wrapper method to email reports

    Arguments:
        body        -- body of email.
        subject     -- subject of email.
        emails      -- email addresses to send to.
        email_from  -- text to display as from.
        attachments -- attachments in a list.
    """

    emailHelper = EmailHelper(body, subject, list(emails), email_from, attachments)
    
    if str(acm.Class()) == "FACMServer":
        print 'im in '
        emailHelper.sender_type = EmailHelper.SENDER_TYPE_SMTP
        emailHelper.host = EmailHelper.get_acm_host()

    try:
        emailHelper.send()
    except Exception as e:
        print("!!! Exception: {0}\n".format(e))


def ael_main(parameter):

    inputpath = parameter ['input']
    output_filename = parameter ['outputLocation']
    email_address = parameter ['emailAddr']
    print 'output_filename:', output_filename
    
    formatted = readInput(inputpath)
    writeOutput(formatted, output_filename)
    
    body = 'Attached: SAB Trades report from Front Arena Production'
    
    if email_address:
        email_report (body, 'SAB Trades Report', email_address, 'Front Arena Production', [output_filename])

    print 'completed successfully'

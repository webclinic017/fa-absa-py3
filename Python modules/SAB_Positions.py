'''-----------------------------------------------------------------------
MODULE
    SAB_Positions

DESCRIPTION
    This module is called by the SAB_Positions.

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
                    ['input', 'Input File', 'string', None, 'C:\\Users\\adamsfai\\Desktop\\Position_MDS.csv'],
                    ['outputLocation', 'Output Location', 'string', None, 'C:\\Users\\adamsfai\\Desktop\\SAB_Positions.csv'],
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
    
def readInput(input):
    output = []
    
    with open(input, 'rU') as file:
        contents = csv.reader(file)
        counter = 0 #always copy first 6 rows
        for row in contents:
            if len(row) > 0 and counter < 5:
                output.append(row)
                counter += 1
            elif len(row) > 11:
                colA = row[0]
                colB = row[1]
                colK = row[10]
                        
                if "ZAR" in str(colA)[:3] and colK != '':
                    if '_CR' in str(colB):
                        row[1] = colB[:colB.index('_CR')] #remove _CR from portfolio names
                    if "PB_CFD" in str(colB)[:6]:
                        row[3] = invertSign(row[3])
                        row[4] = invertSign(row[4])
                        row[10] = invertSign(row[10])
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

#def main(inputLocation, outputLocation):
#    formatted = readInput(inputLocation)
#    writeOutput(formatted,outputLocation)
    
def ael_main(parameter):

    inputpath = parameter ['input']
    output_filename = parameter ['outputLocation']
    email_address = parameter ['emailAddr']
    print 'output_filename:', output_filename
    
    formatted = readInput(inputpath)
    writeOutput(formatted, output_filename)
    
    body = 'Attached: SAB Positions report from Front Arena Production'
    
    if email_address:
        email_report (body, 'SAB Positions Report', email_address, 'Front Arena Production', [output_filename])

    print 'completed successfully'

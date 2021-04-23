import acm
import ael
from at_email import EmailHelper

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

ael_gui_parameters = { 'windowCaption':'Spark Settlement Feed Exception Report'}

ael_variables = [ ['emailAddr', 'Email Address', 'string', None, '', 0, 1, 'Email', None, 1],
                ['source_path', 'File Source Path', 'string', None, '', 0, 1, 'source_path', None, 1]]     

def ael_main(parameter):    
    #BAGL PCG Markets SMT;  BAGL Markets Line Controllers; 
    email_addresses = parameter['emailAddr']
    source_path = parameter['source_path']
    
    file_datestamp = ael.date_today().to_string('%y%m%d')
    folder_datestamp = ael.date_today().to_string('%Y-%m-%d')
    output_filename = '%s/%s/Daily_Large_PNL_Rep_%s.xls'%(source_path[0], folder_datestamp, file_datestamp)
    ael.log('Reading report from:' + output_filename)
            
    body = 'Attached: Daily Large PNL report from Front Arena Production'
    
    if email_addresses:
            ael.log('Sending report to:' + str(email_addresses))
            email_report(body, 'Daily Large PNL report', email_addresses, 'Front Arena Production', [output_filename])
    else:
        ael.log('Invalid parameters')
    

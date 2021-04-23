import acm, csv
from datetime import datetime
from at_email import EmailHelper
from at_logging import getLogger
from at_ael_variables import AelVariableHandler

LOGGER = getLogger(__name__)
FILENAME = 'Blocked_ISIN_Report'+'.csv'
trade_status = ['BO Confirmed', 
                'FO Confirmed', 
                'BO-BO Confirmed']

blocked_isin_list =  []
header_list = ['Trade',
                'Instrument',
                'ISIN',
                'portfolio',
                'desk',
                'cpty']
                
final_result_list = []

ael_variables = AelVariableHandler()
ael_variables.add('source_csv_file',
    label='Source CSV File',   
    mandatory=True,   
    default='/services/frontnt/Task/Blocked_ISIN.csv')

ael_variables.add('output_path',
    label='Output CSV file',
    mandatory=True, 
    default='/services/frontnt/Task/')
    
ael_variables.add("email_recipients",
                  label="Email Recipients",
                  default='"AfricaSupervision@ABSACORP.onmicrosoft.com","AbcapT0MiddleOffice@absa.africa"',
                  multiple=True,
                  mandatory=True,
                  alt=("Email recipients. Use comma seperated email addresses "
                       "if you want to send report to multiple users. "
                       "Leave blank if no email needs to be sent."))
                       
ael_variables.add("sender_email",
                  label="sender email",
                  default="Abcap-IT-Front-Arena-Front-Office@absa.africa",
                  multiple=False,
                  mandatory=False,
                  alt=("Email recipients. Use comma seperated email addresses "
                       "if you want to send report to multiple users. "
                       "Leave blank if no email needs to be sent."))
def to_html(rows):
    res_text = '<table width="200" border="6">'
    res_text += "<tr>" + "".join(map("<td><b>{0}</b></td>".format, rows[0])) + "</tr>"
    for row in rows[1:]:
        line = "<tr>" + "".join(map("<td>{0}</td>".format, row)) + "</tr>"
        res_text += line
    return res_text + "</table>"


def construct_html_body(table_values):
    msg = "Hi, <br /><br />"
    msg += "Please see below table for trades with blocked Isns:<br /><br />"
    msg += to_html(table_values)
    msg += "<br /><br />"
    msg += "Best regards,<br />{0}".format(
        "Abcap-IT-Front-Arena-Front-Office")
    msg += "<br /><br /><br /><small>This is an automated message from '%s'</small>" % __name__
    return msg

def getLockedIsin(isin_input_file):
    '''returns a list of all blocked ISINs'''
    with open(isin_input_file, 'rU') as file_with_isins:
        results_reader = csv.reader(file_with_isins, delimiter=',')
        
        for row in results_reader:
            if len(row) != 0:
                isin = row[0]                
                blocked_isin_list.append(isin)                
    return blocked_isin_list


def getBlockedInstrument(trade_status, blocked_isin):
    '''Returns all the trades and instrument that do not have ISIN'''
    query = acm.CreateFASQLQuery(acm.FTrade, 'AND')
    query.AddAttrNodeString('Status', trade_status, 'EQUAL')
    query.AddAttrNodeString('Instrument.Isin', blocked_isin, 'EQUAL')
    trades = query.Select()    
    return trades


def writeCsvFile(output_file_location, results_list, header_list):
    """
    Create a file to store all results
    """
    with open(output_file_location, 'wb') as recon_breaks_file:
        recon_writer = csv.writer(recon_breaks_file, quoting=csv.QUOTE_ALL)
        recon_writer.writerow(header_list)
        for item_in_list in results_list:
            recon_writer.writerow(item_in_list)      


def ael_main(parameters):
    isin_input_file = parameters['source_csv_file']
    blocked_isin_list = getLockedIsin(isin_input_file)
    trades = getBlockedInstrument(trade_status, blocked_isin_list)
    table_values = []
    subject = "Blocked Isns Report for date:" + " " + str(acm.Time.DateToday())
    receipents = list(parameters["email_recipients"])
    sender_email = parameters["sender_email"]
    headers = [("Trade Number", "Instrument Name", "Issuer Name", "Isin", "Portfolio Name", "Desk Name", "Counterparty Name")]
    try:
        for trade in trades:
            trade_id = trade.Name()
            instrument = trade.Instrument()
            ins_name = instrument.Name()
            portfolio = trade.Portfolio().Name()
            desk = trade.Acquirer().Name()
            counterparty = trade.Counterparty().Name()
            isin = instrument.Isin() 
            if isin:
                print instrument.InsType()
                final_result_list.append([trade_id, ins_name, isin, portfolio, desk, counterparty])  
                table_values.append([trade_id, ins_name, instrument.Issuer().Name(), isin, portfolio, desk, counterparty])
            
        if len(table_values) >= 1:
            table = headers + \
                    table_values
            email_helper = EmailHelper(
            construct_html_body(table),
            subject,
            receipents,
            sender_email,
            None,
            "html",
	    "SMTP"
            )
	    email_helper.host = email_helper.get_acm_host()
            email_helper.send()
            LOGGER.info("Sent an email regarding the status of the Blocked Isns Report.")
            output_file_location = parameters['output_path'] + FILENAME
            writeCsvFile(output_file_location, final_result_list, header_list)
            LOGGER.info("Output file created and populated with no errors.")
        else:
            LOGGER.info("No exception found.")
        LOGGER.info("Completed successfully.")
    except Exception as e:
        LOGGER.error("Failed due to the following error: {}".format(e))

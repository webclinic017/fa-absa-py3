"""
Description             : Booking tool for the GRP TREASURY and Money Markets desks on Absa Unwinds [MM Unwinds Uploader]
Department and Desk     : GRP TREASURY and Money Markets
Requester               : Vicky Koutsouvelis and John Wade
Developer               : Delsayo Lukhele
JIRA                    : ABITFA-5394-MM_UnWinds_Uploader

History
==================================================================================================
Date       	Change no    		Developer           	Description
--------------------------------------------------------------------------------------------------
2018-12-05 	CHG1001197516     	Shalini Lala         	Change default email address.
                                            			Remove eof functionality.
"""

import acm
import FRunScriptGUI
from at_ael_variables import AelVariableHandler
import xlrd
from datetime import datetime
from at_logging import getLogger
from at_feed_processing import (SimpleCSVFeedProcessor,
                                SimpleXLSFeedProcessor,
                                notify_log)
from at_email import EmailHelper
import traceback

#List of input file type extensions
fileFilter = "CSV Files (*.csv)|*.csv|XLS Files (*.xls)|*.xls|XLSX Files (*.xlsx)|*.xlsx|"
inputFile = FRunScriptGUI.InputFileSelection(FileFilter=fileFilter)

"""Parameters for input file"""
ael_variables = AelVariableHandler()
ael_variables.add(
    'input_file',
    label = 'File',
    cls = inputFile,
    default = inputFile,
    mandatory = True,
    multiple = True,
    alt = 'Input file in CSV or XLS format.'
    )

"""Parameters for sending emails"""
ael_variables.add(
    'email_recipients',
    label='Email Recipients',
    default='secondarymm@barclayscapital.com',
    multiple=True,
    mandatory=True,
    alt=('Email recipients'))


LOGGER = getLogger(__name__)
TODAY = acm.Time.DateToday()
listOfTrades = []

def StartModule(eii):
    """Menu extension function to start the RunScript dialog for the input parameters"""
    modulename = eii.MenuExtension().At( "ModuleName")
    if modulename:
        try:
            acm.RunModuleWithParameters(str(modulename.AsString()), acm.GetDefaultContext())
        except Exception, msg:
            trace = traceback.format_exc()
            print trace
    else:
        acm.Log("FMenuExtension '%s': Missing parameter ModuleName"%(eii.MenuExtension().Name()))
    return

class DepositUnwindUploader():
    """Class reading data from input file"""
    def __init__(self):
        self.listOfTrades = []
        
    def _process_record(self, record, dry_run):
        """Process input data"""
        (_index, record_data) = record
        
        try:
            #Reading the input data from the spreadsheet template
        
            if str(record_data['TradeNumber'].replace(',', '')) == float:
                tradeNumber = str(record_data['TradeNumber'])[:-2]
            else:
               tradeNumber = str(record_data['TradeNumber'].replace(',', ''))
            
            if str(record_data['valueDate']) != " ":
                acquireDate = record_data['valueDate']
            else:
                return LOGGER.info("Please ensure the Value/Acquire Date is correct: %s" % (record_data['valueDate']))
            
            if float(record_data['Withdrawal'].replace(',', '')) <= 0.0:
                amountWithdrawn = float(record_data['Withdrawal'].replace(',', ''))
            else:
                amountWithdrawn = float(record_data['Withdrawal'].replace(',', '')) * -1
                LOGGER.info("The Withdrawal was positive it has been made negative: %s" % amountWithdrawn)
            
            if float(record_data['Rate']) > 0:
                withDrawprc = float(record_data['Rate'])
            else:
                return LOGGER.info("Please ensure the Rate is correct: %s" % (record_data['Rate']))
                
        except Exception as exc:
                msg = 'Row #%d: Failed to read data from file: %s' % (_index, str(exc))
                LOGGER.exception(msg)
                raise self.RecordProcessingException(msg)
            
        crtInstradeDay = acm.Time.DateFromTime(acm.FTrade[tradeNumber].Instrument().CreateTime())
        
        expInsDay = acm.Time.DateFromTime(acm.FTrade[tradeNumber].Instrument().ExpiryDate())
        
        numberOfDays = acm.Time.DateDifference(expInsDay, crtInstradeDay)
        
        trdPrice = acm.FTrade[tradeNumber].Price()
        
        anNumberOfDays = acm.Time.DateDifference(expInsDay, acquireDate)
        
        intCalc = amountWithdrawn * ((numberOfDays/365.0) * (trdPrice/100.0))
        
        premium = (amountWithdrawn + intCalc)/((1 + withDrawprc/100.0 * anNumberOfDays/365.0))
        
        closeTrd = acm.TradeActions().CloseTrade(tradeNumber, acquireDate, acquireDate, -amountWithdrawn, premium, None)
        
        if closeTrd.AdditionalInfo().MM_DEREC_TRADE() == None:
            closeTrd.AdditionalInfo().MM_DEREC_TRADE('True')
        
        if float(record_data['Rate']) >= 0:
            closeTrd.Price(withDrawprc)
            
        if len(closeTrd.YourRef()) != 0:
            closeTrd.YourRef('')
        
        closeTrd.Commit()
        self.listOfTrades.append(closeTrd)
    

def to_html(rws):
    """Construct output email"""
    res_text = '<table width="1800" border="1">'
    #Email table with its titled columns
    res_text += "<tr>" + "".join(map("<td><b>{0}</b></td>".format, ("Value Date", "FDE Trade Number", "Notional of Withdrawal",
                                    "Rate", "Unwind Trade Number", "Our Premium", "Our End Cash from Front"))) + "</tr>"
    for rows in rws:
        line = "<tr>" + "".join(map("<td>{0}</td>".format, rows)) + "</tr>"
        res_text += line
    return res_text + "</table>"
    
def construct_body(trades):
    """Construct output table rows given all the newly booked trades"""
    calc = acm.Calculations().CreateCalculationSpace(acm.GetDefaultContext(), 'FTradeSheet')
    msg = "<br /><br />"
    rows = [(i.ValueDay(), i.ContractTrdnbr(), i.Nominal(), i.Price(), i.Oid(), round(i.Premium(), 2), round(calc.CalculateValue(i, 'End Cash'), 2)) for i in trades]
    msg += to_html(rows)
    
    msg += "<br /><br />"
    return msg
    
def send_email(subject, body, recipients):
    """Email sender"""
    environment = acm.FDhDatabase['ADM'].InstanceName()
    subject = "{0} {1} ({2})".format(subject, acm.Time.DateToday(), environment)
    email_helper = EmailHelper(
            body,
            subject,
            recipients,
            "Front Arena {0}".format(environment),
            None,
            "html"
        )
        
    if str(acm.Class()) == "FACMServer":
        email_helper.sender_type = EmailHelper.SENDER_TYPE_SMTP
        email_helper.host = EmailHelper.get_acm_host()

    try:
        email_helper.send()
    except Exception as exc:
        LOGGER.exception("Error while sending e-mail: %s", exc)
    LOGGER.info("Email sent successfully.")
    
class CSVCreator(DepositUnwindUploader, SimpleCSVFeedProcessor):
  
    def __init__(self, file_path):
    
        DepositUnwindUploader.__init__(self)
        SimpleCSVFeedProcessor.__init__(self, file_path, do_logging=True)

class XLSCreator(DepositUnwindUploader, SimpleXLSFeedProcessor):
  
    def __init__(self, file_path):
        
        DepositUnwindUploader.__init__(self)
        SimpleXLSFeedProcessor.__init__(self, file_path, sheet_index=0, sheet_name=None)

def ael_main(ael_dict):
    file_path = str(ael_dict['input_file'])
    LOGGER.info("Input file: %s", file_path)
    
    #Check whether input file is .csv or .xls
    if file_path.endswith(".csv"):
        proc = CSVCreator(file_path)
    else:
        proc = XLSCreator(file_path)
    
    proc.add_error_notifier(notify_log)
    proc.process(False)
    
    #Set the subject of the email
    subject = "Absa life unwinds"
    
    #Construct the email output to be sent
    body = construct_body(proc.listOfTrades)
    
    #Set the list of email receipients
    recipients = list(ael_dict["email_recipients"])
    
    #Call email sender
    send_email(subject, body, recipients)
    
    LOGGER.info("Completed successfully.")

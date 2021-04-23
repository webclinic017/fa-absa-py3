"""
Description             : Booking tool for the GRP TREASURY and Money Markets desks on Absa Annuity Unwinds [MM Annuity Unwinds Uploader]
Department and Desk     : GRP TREASURY and Money Markets
Requester               : Vicky Koutsouvelis and John Wade
Developer               : Delsayo Lukhele
JIRA                    : ABITFA-5434 ZAR Funding Desk Annuity Uploader

History
==================================================================================================
Date       	Change no    		Developer           	Description
--------------------------------------------------------------------------------------------------
2019-01-07 	CHG1001262610     	Delsayo Lukhele        	Change to fix errors during data upload.
                                            			Remove eof functionality.
2019-09-26      Upgrade to v2018.4.7    Bhavnisha Sarawan       Remove setting of Contract and Connect 
                                                                Trade Ref so that FA sets it. This causes
                                                                FA to crash when opening the trade ticket.

"""

import acm
import FRunScriptGUI
from at_ael_variables import AelVariableHandler
from datetime import datetime
import xlwt
from xlsxwriter import Workbook
from at_logging import getLogger
from at_feed_processing import (SimpleCSVFeedProcessor,
                                SimpleXLSFeedProcessor,
                                notify_log)
from at_email import EmailHelper
import traceback

"""List of input file type extensions"""
fileFilter = "CSV Files (*.csv)|*.csv|XLS Files (*.xls)|*.xls|XLSX Files"
"(*.xlsx)|*.xlsx|"
inputFile = FRunScriptGUI.InputFileSelection(FileFilter=fileFilter)
outputFile = FRunScriptGUI.OutputFileSelection(FileFilter=fileFilter)

"""Parameters for input file"""
ael_variables = AelVariableHandler()
ael_variables.add(
    'input_file',
    label='File',
    cls=inputFile,
    default=inputFile,
    mandatory=True,
    multiple=True,
    alt='Input file in CSV or XLS format.'
    )

"""Parameters for sending emails"""
ael_variables.add(
    'email_recipients',
    label='Email Recipients',
    default='SecondaryMM@barclayscapital.com',
    multiple=True,
    mandatory=True,
    alt=('Email recipients')
    )
"""Parameters for output file"""
ael_variables.add(
    'output_File',
    label='File',
    cls=outputFile,
    default='F:\Bhavnisha\AbsaAnnuities.xlsx',
    multiple=True,
    mandatory=True,
    alt=('Output File')
    )

LOGGER = getLogger(__name__)
TODAY = acm.Time.DateToday()
listOfCloseTrades = []
listOfNewTrades = []
listOfOriginTrades = []
sumAmtList = []
wb = xlwt.Workbook()


def StartModule(eii):
    """Menu extension function to start the RunScript dialog for the input
    parameters"""
    modulename = eii.MenuExtension().At("ModuleName")
    if modulename:
        try:
            acm.RunModuleWithParameters(str(modulename.AsString()),
                                        acm.GetDefaultContext())
        except Exception, msg:
            trace = traceback.format_exc()
            print(trace)
    else:
        LOGGER.info("FMenuExtension '%s': Missing parameter ModuleName" %
                    (eii.MenuExtension().Name()))
    return


class DepAnnuityUnwindUploader():
    """Class reading data from input file"""
    def __init__(self):
        self.eof = False
        self._properties = []

    def _process_record(self, record, dry_run):
        """Process input data"""
        (_index, record_data) = record
        try:
            """Reading the input data from the spreadsheet template"""
            if str(record_data['valueDate']) != " ":
                acquireDay = datetime.strptime(record_data['valueDate'], '%d/%m/%Y').strftime("%Y-%m-%d")
            else:
                return LOGGER.info(
                    "Please ensure the Value/Acquire Date is correct: %s"
                    % (record_data['valueDate']))
            if str(record_data['TradeNumber'].replace(',', '')) == float:
                trade = str(record_data['TradeNumber'])[:-2]
            else:
                trade = str(record_data['TradeNumber'].replace(',', ''))
            if str(record_data['PenaltyFee'].replace(',', '')) <= 0.0:
                penaltyFee1 = str(record_data['PenaltyFee'].replace(',', ''))
            else:
                penaltyFee1 = str(record_data['PenaltyFee'].replace(',', ''))
        except Exception as exc:
            msg = 'Row #%d: Failed to read data from file: %s' % (_index, str(exc))
            LOGGER.exception(msg)
            raise self.RecordProcessingException(msg)
        trad = acm.FTrade[trade]
        if trad.Price() == 0:
            LOGGER.info(
                "Please ensure the Trade Price is correct: %s" % trad. Price()
                        )
            return
        """Returning the Original trade number in a list"""
        listOfOriginTrades.append(trad.Oid())
        """Converting the input valuedate format"""
        if '/' in acquireDay:
            acquireDay = datetime.strptime(acquireDay, '%d/%m/%Y').strftime
            ("%Y-%m-%d")
        """Returning the original trade Nominal"""
        nominal = acm.FTrade[trade].Nominal()
        """Looping through the original trade instrument cash flows to return
        the nominal factor and start date"""
        for payer in trad.Instrument().Legs():
            for cash_F in payer.CashFlows():
                if acquireDay < cash_F.PayDate() and cash_F.CashFlowType() == 'Fixed Rate' and cash_F.StartDate() <= acquireDay:
                    dates = cash_F.StartDate()
                    nom = cash_F.NominalFactor()
                    nominal = nominal * nom
        """Assigning nominal to premium, value date to valueDay, and original
        trade currency"""
        premuim = nominal
        valueDay = acquireDay
        curr = acm.FTrade[trade].Currency()
        """Cloning original Trade Instrument if Long Stub is set to true"""
        for long_stub in trad.Instrument().Legs():
            if long_stub.LongStub() is True:
                newIns = trad.Instrument().Clone()
                newIns.Name(trad.Instrument().SuggestName())
                newIns.Legs()[0].StartDate(acquireDay)
                for nw_Ins in newIns.Instrument().Legs():
                    if nw_Ins.LongStub() is True:
                        nw_Ins.LongStub('False')
            else:
                newIns = trad.Instrument().Clone()
                newIns.Name(trad.Instrument().SuggestName())
                newIns.Legs()[0].StartDate(acquireDay)
            for s in newIns.Legs():
                for c in s.CashFlows():
                    if c.PayDate() < acquireDay:
                        try:
                            c.Delete()
                        except Exception as exc:
                            LOGGER.exception(
                                        "Error while removing cash flows: %s",
                                        exc
                                        )
                    s.GenerateCashFlowsFromDate(acquireDay)
        """Committing Instrument and then return Instrument nominal"""
        try:
            newIns.Commit()
            insLot = newIns.NominalAmount()
        except Exception as exc:
            LOGGER.exception("Error while Commiting new instrument: %s", exc)
            return
        """The Termination fee payment to be added on the Closing trade ONLY"""
        termination_fee_payment = acm.FPayment()
        termination_fee_payment.Trade(trad)
        termination_fee_payment.Party(trad.Counterparty())
        termination_fee_payment.PayDay(acquireDay)
        termination_fee_payment.Type('Termination Fee')
        termination_fee_payment.Currency(curr)
        termination_fee_payment.Amount(penaltyFee1)
        termination_fee_payment.ValidFrom(acquireDay)
        """Perform Close Trade action"""
        closeTrd = acm.TradeActions().CloseTrade(
                                                trad, acquireDay, valueDay,
                                                -nominal, -premuim,
                                                termination_fee_payment
                                                )
        """Change the Closing trade instrument if the original trade had
        long stub selected"""
        for cl in closeTrd.Instrument().Legs():
            if cl.LongStub() is True:
                closeTrd.Instrument(newIns)
        """Ensure the new trade DEREC is set to Yes"""
        if closeTrd.AdditionalInfo().MM_DEREC_TRADE() is None:
            closeTrd.AdditionalInfo().MM_DEREC_TRADE('True')
        """Set the Funding Instype additional info field to FDI"""
        closeTrd.AdditionalInfo().Funding_Instype('FDI')
        """Set the field YourRef to nothing if it is not empty"""
        closeTrd.YourRef('')
        """The Cash payment to be added to the Closing trade ONLY"""
        cashAmt = acm.Time.DateDifference(dates, acquireDay) / 365.0 * nominal * trad.Price() / 100.0
        if cashAmt > 0:
            cashAmt = cashAmt * -1
        cash_payment = acm.FPayment()
        cash_payment.Party(closeTrd.Counterparty())
        cash_payment.PayDay(closeTrd.AcquireDay())
        cash_payment.Type('Cash')
        cash_payment.Currency(closeTrd.Currency())
        cash_payment.Amount(cashAmt)
        cash_payment.ValidFrom(closeTrd.AcquireDay())
        closeTrd.Payments().Add(cash_payment)
        closeTrd.Price(trad.Price())
        if closeTrd.Premium() > 0:
            closeTrd.Premium(closeTrd.Premium() * -1)
        try:
            closeTrd.Commit()
            listOfCloseTrades.append(closeTrd.Oid())
        except Exception as exc:
            LOGGER.exception("Error while Committing closing trade: %s", exc)
            return
        """Returning the Closing trade number in a list"""
        """Nominal to be used in the New trade using nominal size 5m"""
        nom = -5000000
        """Booking of the New Trade."""
        newTrade = acm.FTrade()
        newTrade.Instrument(newIns)
        if insLot:
            newTrade.Quantity(nom / insLot)
        newTrade.Premium(nom * -1)
        newTrade.Price(trad.Price())
        newTrade.Currency(trad.Currency())
        newTrade.Acquirer(trad.Acquirer())
        newTrade.Portfolio(trad.Portfolio())
        newTrade.Counterparty(trad.Counterparty())
        newTrade.TradeTime(TODAY)
        newTrade.ValueDay(acquireDay)
        newTrade.AcquireDay(acquireDay)
        newTrade.AdditionalInfo().Funding_Instype('FDI')
        newTrade.Status('Simulated')
        newTrade.Type('Normal')
        """This ensures the new trade doesn't have payments"""
        try:
            if newTrade.Payments():
                newTrade.Payments().Delete()
        except Exception as exc:
            LOGGER.exception("Error while deleting payment: %s", exc)
        try:
            newTrade.Commit()
            listOfNewTrades.append(newTrade.Oid())
        except Exception as exc:
            LOGGER.exception("Error while Committing new trade: %s", exc)
        """Returning the Termination fee amount"""
        if closeTrd:
            for p in closeTrd.Payments():
                if p.Type() == 'Termination Fee':
                    fee = p.Amount()
        sumOutAmt = premuim + cashAmt + fee
        sumAmtList.append(sumOutAmt)


def out_put_file(
                workbook,
                listOfCloseTrades,
                listOfOriginTrades,
                sumAmtList,
                listOfNewTrades,
                outpath
                ):
    """Process output data into a spread sheet"""
    workbook = Workbook(outpath)
    Report_Sheet = workbook.add_worksheet('Annuity Unwinds')
    Report_Sheet.write(0, 0, 'Trade Number')
    Report_Sheet.write(0, 1, 'Unwind Trade Number')
    Report_Sheet.write(0, 2, 'Sum Of Close out trade')
    Report_Sheet.write(0, 3, 'New trade number')
    Report_Sheet.write_column(1, 0, listOfOriginTrades)
    Report_Sheet.write_column(1, 1, listOfCloseTrades)
    Report_Sheet.write_column(1, 2, sumAmtList)
    Report_Sheet.write_column(1, 3, listOfNewTrades)
    workbook.close()
    return


def send_email(subject, body, recipients, outpath):
    """Email sender"""
    environment = acm.FDhDatabase['ADM'].InstanceName()
    subject = "{0} {1} ({2})".format(
                                    subject, acm.Time.DateToday(),
                                    environment
                                    )
    attach = [outpath]
    email_helper = EmailHelper(
            body,
            subject,
            recipients,
            "Front Arena {0}".format(environment),
            attach,
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


class CSVCreator(DepAnnuityUnwindUploader, SimpleCSVFeedProcessor):
    def __init__(self, file_path):
        DepAnnuityUnwindUploader.__init__(self)
        SimpleCSVFeedProcessor.__init__(self, file_path, do_logging=True)


class XLSCreator(DepAnnuityUnwindUploader, SimpleXLSFeedProcessor):
    def __init__(self, file_path):
        DepAnnuityUnwindUploader.__init__(self)
        SimpleXLSFeedProcessor.__init__(self, file_path, sheet_index=0,
                                        sheet_name=None)


def ael_main(ael_dict):
    file_path = str(ael_dict['input_file'])
    outpath = str(ael_dict['output_File'])
    LOGGER.info("Input file: %s", file_path)
    """Check whether input file is .csv or .xls"""
    if file_path.endswith(".csv"):
        proc = CSVCreator(file_path)
    else:
        proc = XLSCreator(file_path)
    proc.add_error_notifier(notify_log)
    proc.process(False)
    subject = "Absa Annuity Unwinds"
    body = "Please Find The Attached output file..."
    recipients = list(ael_dict["email_recipients"])
    """Calling the output data function"""
    out_put_file(
                wb, listOfCloseTrades, listOfOriginTrades, sumAmtList,
                listOfNewTrades, outpath
                )
    send_email(subject, body, recipients, outpath)
    LOGGER.info("Completed successfully.")


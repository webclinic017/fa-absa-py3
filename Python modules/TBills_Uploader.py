import acm
import FRunScriptGUI
import FUxCore
from at_ael_variables import AelVariableHandler
from at_logging import getLogger
from at_time import acm_datetime
from at_feed_processing import (SimpleXLSFeedProcessor, notify_log)

businessLogicHandler = acm.FBusinessLogicGUIDefault()

# List of input file type extensions
fileFilter = "XLSX Files (*.xlsx)|*.xlsx|"
inputFile = FRunScriptGUI.InputFileSelection(FileFilter=fileFilter)
outputFile = FRunScriptGUI.OutputFileSelection(FileFilter=fileFilter)

# Parameters for input file
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

CALENDAR = acm.FCalendar['ZAR Johannesburg']

ael_variables.add('settle_day',
                  label='Settlement Day',
                  mandatory=True,
                  default=CALENDAR.AdjustBankingDays(acm.Time().DateToday(), 3),
                  )

LOGGER = getLogger(__name__)
ZAR_CURRENCY = acm.FCurrency['ZAR']
CALENDAR = acm.FCalendar['ZAR Johannesburg']
TRADE_STATUS = "Simulated"
TODAY = acm.Time().DateToday()
#VALUE_DAY = None

ACM_CALC = acm.Calculations()
STD_CALCULATION_SPACE_COLLECTION = ACM_CALC.CreateStandardCalculationsSpaceCollection()

DIALOG_FUNC = acm.GetFunction('msgBox', 3)


def price_calculation(trade, value_date, face_value, price, sign):
    if sign == "B":
        p = -1 * (int(face_value) * (float(price) / 100))
    elif sign == "S":
        p = int(face_value) * (float(price) / 100)

    calc_price = trade.Calculation().PremiumToPrice(STD_CALCULATION_SPACE_COLLECTION, value_date, p)
    return calc_price


def premium_calculation(trade, value_date, calc_price):
    calc_premium = trade.Calculation().PriceToPremium(STD_CALCULATION_SPACE_COLLECTION, value_date, calc_price)
    return calc_premium


def StartModule(eii):
    modulename = eii.MenuExtension().At("ModuleName")
    if modulename:
        try:
            acm.RunModuleWithParameters(str(modulename.AsString()), acm.GetDefaultContext())
        except Exception, msg:
            trace = traceback.format_exc()
            print trace
    else:
        LOGGER.info("FMenuExtension '%s': Missing parameter ModuleName" % (eii.MenuExtension().Name()))
    return


class TBillCreator(object):
    TRD_ACQUIRER = acm.FParty[2246]  # "Money Market Desk"
    TRD_ISSUER_CP = acm.FParty[538]  # "SARB"

    CONTRACT_SIZE = 1000000

    def __init__(self, ins_id, sign, face_value, price, counterparty, portfolio, start, end):

        self.ins_id = ins_id
        self.sign = sign
        self.face_value = face_value
        self.price = price
        self.counterparty = counterparty
        self.portfolio = portfolio
        self.start = start
        self.end = end


    def create_tbill_instrument(self):
        """Create new tbill instrument"""
        instrument = acm.FBill()
        instrument.RegisterInStorage()
        instrument = acm.FInstrumentLogicDecorator(instrument, businessLogicHandler)
        instrument.Isin(self.ins_id)
        instrument.ExpiryDate(self.end)
        instrument.ExpiryPeriod_unit('Months')
        instrument.ExpiryPeriod_count(3)
        instrument.Currency(ZAR_CURRENCY)
        instrument.StrikeCurrency(ZAR_CURRENCY)
        instrument.PriceFindingChlItem('Close')
        instrument.Issuer(self.TRD_ISSUER_CP)
        instrument.ValuationGrpChlItem('AC_GLOBAL_SDGOVI')
        instrument.Quotation('Discount Rate')
        instrument.NominalAmount(self.CONTRACT_SIZE)
        instrument.SettleCategoryChlItem('Demat')
        instrument.AddInfoValue('Demat_Instrument', 'True')
        instrument.MtmFromFeed('False')
        instrument.SpotBankingDaysOffset(0)
        leg = instrument.CreateLeg(1)
        leg.StartDate(self.start)
        leg.EndDate(self.end)
        leg.DayCountMethod('ACT/365')

        return instrument

    def book_tbill_trade(self, ins, value_day):
        """Create new tbill trade"""
        trade = acm.FTrade()
        trade.Instrument(ins)

        if self.sign == "B":
            trade.AddInfoValue('MM_Original_Nominal', int(self.face_value))
            trade.AddInfoValue('MM_DEMAT_TransType', 'RVP')
            trade.FaceValue(int(self.face_value))

        elif self.sign == "S":
            trade.AddInfoValue('MM_Original_Nominal', -1 * int(self.face_value))
            trade.AddInfoValue('MM_DEMAT_TransType', 'DVP')
            trade.FaceValue(-1 * int(self.face_value))

        calc_price = price_calculation(trade, value_day, self.face_value, self.price, self.sign)
        premium = premium_calculation(trade, value_day, calc_price)
        trade.Counterparty(self.counterparty)
        trade.Currency(ZAR_CURRENCY)
        trade.TradeTime(TODAY)
        trade.ValueDay(value_day)
        trade.AcquireDay(value_day)
        trade.Price(calc_price)
        trade.Premium(premium)
        trade.Portfolio(self.portfolio)
        trade.Acquirer(self.TRD_ACQUIRER)
        trade.Status(TRADE_STATUS)
        trade.Trader(acm.User())
        if self.counterparty == self.TRD_ISSUER_CP:
            trade.AddInfoValue('Demat_Acq_BPID', 'ZA601840')
            trade.AddInfoValue('Demat_Acq_SOR_Ac', 'SCB/ZA100019/10003176')
            trade.AddInfoValue('MM_DEMAT_CP_BPID', 'ZA100109')
        trade.AddInfoValue('MM_Instype', 'TB')
        trade.AddInfoValue('MM_DEMAT_TRADE', 'Yes')
        trade.AddInfoValue('MM_Primary_Issue', 'No')
        trade.AddInfoValue('Demat_Deliv_vs_Paym', 'True')

        return trade


class CreateTBillTradesFromExcelXLS(SimpleXLSFeedProcessor):

    def __init__(self, file_path, value_day):
        self.tbill_trades = []
        SimpleXLSFeedProcessor.__init__(self, file_path, sheet_index=0, sheet_name=None)
        self.input_errors = False
        self.value_day = value_day

    def _process_record(self, record, dry_run):
        """Process input data"""
        (_index, record_data) = record

        for e in record_data:
            if str(record_data['ISIN']) != '':
                if acm.FInstrument[str(record_data['ISIN'])] == None:
                    if str(record_data[e]) == '':
                        self.input_errors = True
                        msg = 'Row #%d: Failed to read data from file: %s' % (_index, str(e))
                        LOGGER.exception(msg)
                elif acm.FInstrument[str(record_data['ISIN'])]:
                    if str(record_data[e]) == '' and e != 'Start' and e != 'End':
                        self.input_errors = True
                        msg = 'Row #%d: Failed to read data from file: %s' % (_index, str(e))
                        LOGGER.exception(msg)
            else:
                self.input_errors = True
                msg = 'Row #%d: Failed to read data from file: %s' % (_index, str(e))
                LOGGER.exception(msg)

        if self.input_errors == True:
            return

        else:
            # reading the input data from the spreadsheet
            try:
                ins_id = str(record_data['ISIN'])
                sign = str(record_data['Sign'])
                face_value = record_data['Face Value']
                price = record_data['Price']
                counterparty = str(record_data['Counterparty'])
                portfolio = str(record_data['Portfolio'])
                start = record_data['Start']
                end = record_data['End']
                instrument = acm.FInstrument[ins_id]

            except Exception as exc:
                msg = 'Row #%d: Failed to read data from file: %s' % (_index, str(exc))
                LOGGER.exception(msg)
                raise self.RecordProcessingException(msg)

            creator = TBillCreator(ins_id, sign, face_value, price,
                                   counterparty, portfolio, start,
                                   end)

            if instrument is None:
                '''
                creating new instrument
                '''
                try:
                    instrument = creator.create_tbill_instrument()
                    instrument.Commit()
                except Exception as exc:
                    LOGGER.exception("Error while commiting new instrument: %s", exc)

            if instrument:
                '''
                updating trade details as per the xls file
                '''
                new_trade = creator.book_tbill_trade(instrument, self.value_day)
                self.tbill_trades.append(new_trade)


class CreateTBillTradesOutput(FUxCore.LayoutDialog):
    """Embedding trading manager sheets into custom dialogs"""

    def __init__(self, caption, trades):
        self.caption = caption

        self.trade_sheet = None
        self.trade_portfolio = None

        trade_list = trades

        # Add trades to the sheet
        self.add_trades(trade_list)

    def initialise_test_sheet(self):
        """Change sheet default columns to the ones listed below."""
        default_columns = ('Trade Instrument',
                           'Trade Price',
                           'Trade Quantity',
                           'Trade Counterparty',
                           'Trade Nominal',
                           'Trade Value Day',
                           'Trade Portfolio',
                           'Trade Premium',
                           'Trade Status')

        context = acm.GetDefaultContext()
        default_columns = acm.GetColumnCreators(default_columns, context)
        columns = self.trade_sheet.ColumnCreators()
        columns.Clear()

        for i in range(default_columns.Size()):
            columns.Add(default_columns.At(i))

        self.trade_sheet.InsertObject(self.trade_portfolio, 'IOAP_LAST')
        self.trade_sheet.PrivateTestSyncSheetContents()

    def add_trades(self, trade_list):
        """Insert Items and add to the sheet."""
        self.trade_portfolio = acm.FASQLQueryFolder()
        self.trade_portfolio.Name('Bulk T-Bill Bookings')
        query = acm.CreateFASQLQuery('FTrade', 'OR')

        for trade in trade_list:
            query.AddOpNode('OR')
            query.AddAttrNode('Oid', 'EQUAL', trade.Oid())

        self.trade_portfolio.AsqlQuery(query)

    def CreateLayout(self):
        b = acm.FUxLayoutBuilder()
        b.BeginVertBox('None')

        b.AddSpace(5)
        b.AddSeparator()
        b.AddSpace(5)
        b.BeginVertBox()
        b.AddCustom('trade_sheet', 'sheet.FTradeSheet', 500, 250)
        b.EndBox()
        b.AddSpace(5)
        b.AddSeparator()

        b.AddSpace(10)
        b.BeginHorzBox()
        b.AddFill()
        b.AddButton('ok', 'OK')
        b.AddButton('cancel', 'Cancel')
        b.EndBox()
        b.EndBox()

        return b

    def HandleCreate(self, dialog, layout):
        self.dialog = dialog
        dialog.Caption(self.caption)

        # get a handle to the sheet
        ctrl = layout.GetControl
        self.trade_sheet = ctrl('trade_sheet').GetCustomControl()

        self.initialise_test_sheet()

    def HandleApply(self):
        return True


def ael_main(ael_dict):
    file_path = str(ael_dict['input_file'])
    LOGGER.info("Input file: %s", file_path)
    value_day = ael_dict['settle_day']

    proc = CreateTBillTradesFromExcelXLS(file_path, value_day)
    proc.add_error_notifier(notify_log)
    proc.process(False)
    trades = proc.tbill_trades
    errors = proc.input_errors

    if not errors:
        '''
        if there are no unpopulated cells in the input file, trades are booked
        '''
        for trade in trades:
            try:
                trade.Commit()
            except Exception as exc:
                LOGGER.exception("Error while commiting trade: %s", exc)

        if None in trades:
            message = 'Some or all of your bookings have failed. Please refer to log.'
            DIALOG_FUNC('Warning', message, 0)
        else:
            message = 'Trades booked successfully.'
            DIALOG_FUNC('Complete', message, 0)
            LOGGER.info("Completed successfully.")

        # calling the output data function
        shell = acm.UX().SessionManager().Shell()
        dlg = CreateTBillTradesOutput('T-Bill Trades', trades)
        dlgResult = dialogResult = acm.UX().Dialogs().ShowCustomDialogModal(shell, dlg.CreateLayout(), dlg)


    elif errors:
        '''
        if there are unpopulated cells in the input file, return details 
        '''
        message = 'Please populate the relevant fields before uploading and booking trades.'
        DIALOG_FUNC('Warning', message, 0)
        LOGGER.error("Unsucessful. Input file missing data.")

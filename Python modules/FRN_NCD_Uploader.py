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

LOGGER = getLogger(__name__)
ZAR_CURRENCY = acm.FCurrency['ZAR']
CALENDAR = acm.FCalendar['ZAR Johannesburg']
TRADE_STATUS = "Simulated"
TODAY = acm.Time().DateToday()
VALUE_DAY = CALENDAR.AdjustBankingDays(TODAY, 3)
DIALOG_FUNC = acm.GetFunction('msgBox', 3)

ACM_CALC = acm.Calculations()
STD_CALCULATION_SPACE_COLLECTION = ACM_CALC.CreateStandardCalculationsSpaceCollection()


def premium_calculation(trade, value_date, price):
    calc_premium = trade.Calculation().PriceToPremium(STD_CALCULATION_SPACE_COLLECTION, value_date, price)
    return calc_premium


def get_counterparty_BPID(trade):
    if trade.Counterparty():
        counterparty_BPID = [partyalias for partyalias in trade.Counterparty().Aliases() if
                             partyalias.Type().Name() == 'MM_DEMAT_Trader_BPID']
        print((len(counterparty_BPID)))
        if len(counterparty_BPID) == 1:
            for cpy_bpid in counterparty_BPID:
                return cpy_bpid.Name()
        else:
            return None
    else:
        return None


def get_acquirer_BPID(trade):
    if trade.Acquirer():
        acquirer_BPID = [acquireralias for acquireralias in trade.Acquirer().Aliases()]
        for bpid in acquirer_BPID:
            if bpid.Type().Name() == 'MM_DEMAT_Trader_BPID':
                return bpid.Name()
    else:
        return None


def StartModule(eii):
    modulename = eii.MenuExtension().At("ModuleName")
    if modulename:
        try:
            acm.RunModuleWithParameters(str(modulename.AsString()), acm.GetDefaultContext())
        except Exception, msg:
            trace = traceback.format_exc()
            print(trace)
    else:
        LOGGER.info("FMenuExtension '%s': Missing parameter ModuleName" % (eii.MenuExtension().Name()))
    return


class Creator(object):
    TRD_ACQUIRER = acm.FParty[2247]  # "Funding Desk"

    def __init__(self, instrument, ins_type, sign, face_value, price, asset_manager, plus_fund, portfolio):

        self.instrument = instrument
        self.ins_type = ins_type
        self.sign = sign
        self.face_value = face_value
        self.price = price

        if asset_manager and plus_fund:
            asset_manager = asset_manager.strip()
            plus_fund = plus_fund.strip()
            party_name = '%s%s%s' % (asset_manager, ' ', plus_fund)
            print(party_name)
            if acm.FParty[party_name]:
                self.counterparty = acm.FParty[party_name]
            else:
                self.counterparty = None
        else:
            if acm.FParty[asset_manager]:
                asset_manager = asset_manager.strip()
                self.counterparty = asset_manager
            else:
                self.counterparty = None
        self.portfolio = portfolio

    def book_trade(self):
        """Create new trade"""
        try:
            trade = acm.FTrade()
            trade.Instrument(self.instrument)
            ins_type = self.instrument.AdditionalInfo().MM_MMInstype()

            if self.sign == "B":
                trade.AddInfoValue('MM_DEMAT_TransType', 'RVP')
                trade.AddInfoValue('MM_DEREC_TRADE', 'Yes')
                trade.FaceValue(int(self.face_value))

            elif self.sign == "S":
                trade.AddInfoValue('MM_DEMAT_TransType', 'DVP')
                trade.FaceValue(-1 * int(self.face_value))

            trade.AddInfoValue('MM_DEMAT_PRE_SETT', 'True')
            trade.AddInfoValue('MM_DEMAT_TRADE', True)

            if self.ins_type == "FRN":
                trade.AddInfoValue('MM_Instype', ins_type)
            elif self.ins_type == "CD":
                trade.AddInfoValue('Funding Instype', ins_type)
                trade.AddInfoValue('Instype', ins_type)
            print(TODAY)
            premium = premium_calculation(trade, TODAY, self.price)
            trade.Counterparty(self.counterparty)
            trade.Currency(ZAR_CURRENCY)
            trade.TradeTime(TODAY)
            trade.ValueDay(TODAY)
            trade.AcquireDay(TODAY)
            trade.Price(self.price)
            trade.Premium(premium)
            trade.Portfolio(self.portfolio)
            trade.Acquirer(self.TRD_ACQUIRER)
            trade.Status(TRADE_STATUS)
            trade.Trader(acm.User())
            trade.AdditionalInfo().Demat_Deliv_vs_Paym(True)
            acquirer_BPID = get_acquirer_BPID(trade)
            trade.AdditionalInfo().Demat_Acq_BPID(acquirer_BPID)
            trade.AdditionalInfo().Demat_Acq_SOR_Ac('SCB/ZA100019/10003176')
            counterparty_BPID = get_counterparty_BPID(trade)
            trade.AdditionalInfo().MM_DEMAT_CP_BPID(counterparty_BPID)
            trade.Commit()
            return trade
        except Exception as exc:
            LOGGER.exception("Error while commiting new instrument: %s", exc)


class CreateTradesFromExcelXLS(SimpleXLSFeedProcessor):
    SELL_PORTFOLIO = "LIABILITIES 2474"

    def __init__(self, file_path):
        self.trades = []
        SimpleXLSFeedProcessor.__init__(self, file_path, sheet_index=0, sheet_name=None)

    def _process_record(self, record, dry_run):
        """Process input data"""
        (_index, record_data) = record

        # reading the input data from the spreadsheet
        try:
            ins_id = str(record_data['ISIN'])
            instrument = acm.FInstrument.Select('isin = "%s"' % ins_id)
            trades = instrument[0].Trades()
            sign = str(record_data['Sign'])
            if sign == "B":
                for trade in trades:
                    if trade.Status() in ["FO Confirmed", "BO Confirmed", "BO-BO Confirmed"]:
                        portfolio = trade.Portfolio().Name()
                        break
            elif sign == "S":
                portfolio = str(record_data['Portfolio'])
            face_value = record_data['Face Value']
            price = record_data['Price']
            asset_manager = str(record_data['Asset Manager'])
            plus_fund = str(record_data['Plus Fund'])


        except Exception as exc:
            msg = 'Row #%d: Failed to read data from file: %s' % (_index, str(exc))
            LOGGER.exception(msg)
            raise self.RecordProcessingException(msg)

        if instrument[0]:
            ins_type = instrument[0].InsType()
            creator = Creator(instrument[0], ins_type, sign, face_value, price, asset_manager, plus_fund, portfolio)
            new_trade = creator.book_trade()
            self.trades.append(new_trade)


class CreateTradesOutput(FUxCore.LayoutDialog):
    """Embedding trading manager sheets into custom dialogs"""

    def __init__(self, caption, trades):
        self.caption = caption

        self.trade_sheet = None
        self.trade_portfolio = None

        trade_list = trades

        # Add trades to the sheet
        self.add_trades(trade_list)

    def initialise_sheet(self):
        """Change sheet default columns to the ones listed below."""
        default_columns = ('Trade Counterparty',
                           'Instrument Type',
                           'Portfolio Profit Loss Period Position',
                           'Trade Position',
                           'Trade Instrument',
                           'ISIN',
                           'Trade Price',
                           'Trade Quantity',
                           'Trade Nominal',
                           'Trade Value Day',
                           'Trade Portfolio',
                           'Trade Premium',
                           'Trade Status',
                           'AdditionalInfo.MM_DEMAT_CP_BPID')

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
        self.trade_portfolio.Name('Simulated Bookings')
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

        self.initialise_sheet()

    def HandleApply(self):
        return True


def ael_main(ael_dict):
    file_path = str(ael_dict['input_file'])
    LOGGER.info("Input file: %s", file_path)

    proc = CreateTradesFromExcelXLS(file_path)
    proc.add_error_notifier(notify_log)
    proc.process(False)
    trades = proc.trades

    # calling the output data function
    shell = acm.UX().SessionManager().Shell()
    dlg = CreateTradesOutput('Trades Booked', trades)
    dlgResult = dialogResult = acm.UX().Dialogs().ShowCustomDialogModal(shell, dlg.CreateLayout(), dlg)

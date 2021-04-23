import acm
import FRunScriptGUI
import FUxCore
from at_ael_variables import AelVariableHandler
from at_logging import getLogger
from datetime import datetime
from at_feed_processing import (SimpleXLSFeedProcessor, notify_log)
import traceback
from GValidation import show_exception

businessLogicHandler = acm.FBusinessLogicGUIDefault()
ael_variables = AelVariableHandler()

#List of input file type extensions
fileFilter = "XLSX Files (*.xlsx)|*.xlsx|CSV Files (*.csv)|*.csv|"
inputFile = FRunScriptGUI.InputFileSelection(FileFilter=fileFilter)

LOGGER = getLogger(__name__)

#Parameters for input file
ael_variables.add('input_file',
                  label = 'File',
                  cls = inputFile,
                  default = inputFile,
                  mandatory = True,
                  multiple = True,
                  alt = 'Input file in CSV or XLS format.')
ael_variables.add('calendars',
                  label='Calendars',
                  mandatory=True,
                  multiple = True,
                  default='USD New York, GBP London,ZAR Johannesburg',
                  tab='Calendars')
ael_variables.add('underlyings',
                  label='Underlyings',
                  mandatory=True,
                  multiple = True,
                  default='XPT, XPD, XAU',
                  tab='Underlyings')
ael_variables.add('commodity_names',
                  label='Commodity Name',
                  mandatory=True,
                  multiple = True,
                  default='PLATINUM, PALLADIUM, GOLD',
                  tab='Underlyings')
ael_variables.add('paydaymethod',
                  label='Pay Day Method',
                  mandatory=True,
                  default='EOM',
                  tab='Pay Day')        
ael_variables.add('payoffset',
                  label='Pay Day Offset (Days)',
                  mandatory=True,
                  default='10',
                  tab='Pay Day')       
ael_variables.add('currency',
                  label='Instrument Currency',
                  mandatory=True,
                  default='USD',
                  tab='Instrument Details')     
         

class PriceSwapCreator(object):
    USD_CURRENCY = acm.FCurrency['USD']
    ZAR_CURRENCY = acm.FCurrency['ZAR']
    CALENDAR = acm.FCalendar['ZAR Johannesburg']
    TRADE_STATUS = "Simulated"
    TODAY = acm.Time().DateToday()
    VALUE_DAY = CALENDAR.AdjustBankingDays(TODAY, 2)
    TRD_ACQUIRER = acm.FParty[16492]  # "Gold Desk"
    LEGS = {1 : ['Float', 'False'], 2 : ['Fixed', 'True']}
    CONTRACT_SIZE = 1
    
    
    def __init__(self, price_ref, nominal, fixed_rate, counterparty, portfolio, start, end, count, underlyings, commodity_names, calendar, currency, payday_method, pay_offset):
        self.price_ref = price_ref
        self.nominal = nominal
        self.fixed_rate = fixed_rate
        self.counterparty = counterparty
        self.portfolio = portfolio
        self.start = start
        self.end = end
        self.count = count
        self.calendar = calendar
        self.currency = currency
        self.payday_method = payday_method
        self.pay_offset = pay_offset
        underlying_index = underlyings.index(self.price_ref)
        self.commodity = commodity_names[underlying_index]

    
    def get_instrument_name(self):
        #Create instrument name
        end_date = datetime.strptime(acm.Time.DateAddDelta('1899-12-30', 0, 0, self.end), '%Y-%m-%d')
        start_date = datetime.strptime(self.TODAY, '%Y-%m-%d')
        new_name = self.currency + '/' + self.commodity + '/' + 'THARISA' + '/' + end_date.strftime("%b") \
                    + end_date.strftime("%y") + '/' + str(self.fixed_rate) + '/' + start_date.strftime("%d") \
                    + start_date.strftime("%b") + start_date.strftime("%y") + '##' + str(self.count)
        return new_name
        
        
    def create_price_swap_instrument(self, name):
        #Create new price swap instrument
        instrument = acm.FPriceSwap()
        instrument.RegisterInStorage()
        instrument = acm.FInstrumentLogicDecorator(instrument, businessLogicHandler)
    
        for key, value in list(self.LEGS.items()):
            leg = instrument.CreateLeg(key)
            leg.LegType(value[0])
            leg.PayLeg(value[1])
            leg.StartDate(self.start)
            leg.EndDate(self.end)
            leg.ExtendedFinalCf(False)
            leg.EndPeriodUnit('Months')
            leg.FloatRateFactor2(1.0)
            leg.PayCalendar(acm.FCalendar[self.calendar[0]])
            leg.Pay2Calendar(acm.FCalendar[self.calendar[1]])
            leg.Pay3Calendar(acm.FCalendar[self.calendar[2]])
            leg.PayDayMethod(self.payday_method)
            leg.PayOffsetCount(self.pay_offset)
            
            leg.ResetCalendar(acm.FCalendar[self.calendar[0]])
            leg.Reset2Calendar(acm.FCalendar[self.calendar[1]])
            leg.ResetDayOffset(0)
            leg.ResetPeriodCount(1)
            leg.ResetType('Unweighted')
            leg.RollingPeriodBase(self.end)
            leg.RollingPeriodCount(1)
            leg.RollingPeriodUnit('Months')
            leg.StartPeriodCount(1)
            leg.StartPeriodUnit('Months')
            leg.AmortEndPeriodUnit('Months')
            leg.AmortStartDay(self.start)
            leg.AmortStartPeriodCount(1)
            leg.AmortStartPeriodUnit('Months')
            
            leg.DayCountMethod('ACT/360')
            leg.Currency(self.USD_CURRENCY)
            
            if leg.LegType() == 'Fixed':
                leg.FixedRate(self.fixed_rate)
                leg.FloatRateReference(None)
            elif leg.LegType() == 'Float':
                price_reference = 'London ' + self.price_ref + ' AM/PM Unweighted Arithmetic'
                leg.FloatRateReference(price_reference)

        instrument.Name(name)
        instrument.MtmFromFeed(False)    
        instrument.Currency(self.USD_CURRENCY)
        instrument.ValuationGrpChlItem('Compo_Average')
        instrument.Quotation('Ounce')
        instrument.NominalAmount(self.CONTRACT_SIZE)
        instrument.SpotBankingDaysOffset(2)
        instrument.StrikeCurrency(self.ZAR_CURRENCY)
        instrument.Commit()
        return instrument
        
        
    def book_price_swap_trade(self, ins):
        #Create new price swap trade
        trade = acm.FTrade()
        trade.Instrument(ins)
        
        trade.Quantity(self.nominal)
        trade.Counterparty(self.counterparty )
        trade.Currency(self.USD_CURRENCY)
        trade.TradeTime(self.TODAY)
        trade.ExecutionTime(self.TODAY)
        trade.ValueDay(self.VALUE_DAY)
        trade.AcquireDay(self.VALUE_DAY)
        trade.Portfolio(self.portfolio)
        trade.Acquirer(self.TRD_ACQUIRER)
        trade.Status(self.TRADE_STATUS)
        trade.Trader(acm.User())
        trade.Commit()
        return trade
    
    
class CreatePriceSwapTradesFromExcelXLS(SimpleXLSFeedProcessor):
    
    def __init__(self, file_path, underlyings, commodity_names, calendar, currency, payday_method, pay_offset):
        self.price_swap_trades = []
        SimpleXLSFeedProcessor.__init__(self, file_path, sheet_index=0, sheet_name=None)
        self.price_swap_trades = []
        self.calendar = calendar
        self.currency = currency
        self.underlyings = underlyings
        self.commodity_names = commodity_names
        self.payday_method = payday_method
        self.pay_offset = pay_offset
        
        
    def _process_record(self, record, dry_run):
        #Process input data
        (_index, record_data) = record
        
        #reading the input data from the spreadsheet
        try:
            price_ref = str(record_data['Price Ref'])
            if price_ref not in self.underlyings:
                raise Exception('Commodity underlying not included in list.')
            nominal = record_data['Nominal']
            fixed_rate = record_data['Fixed Rate']
            counterparty = str(record_data['Counterparty'])
            portfolio = str(record_data['Portfolio'])
            start = record_data['Start']
            end = record_data['End']
            count = str(_index)
        except Exception as exc:
            msg = 'Row #%d: Failed to read data from file: %s' % (_index, str(exc))
            LOGGER.exception(msg)
            raise self.RecordProcessingException(msg)
    
        creator = PriceSwapCreator(price_ref, nominal, fixed_rate, counterparty, portfolio, start, end, count, self.underlyings,
                                   self.commodity_names, self.calendar, self.currency, self.payday_method, self.pay_offset)
        instrument_name = creator.get_instrument_name()
        instrument = acm.FInstrument[instrument_name]
        
        if instrument:
            try:
                new_trade = creator.book_price_swap_trade(instrument)
                self.price_swap_trades.append(new_trade)
                LOGGER.info("Trade %s booked successfully." % new_trade.Oid())
            except Exception as exc:
                LOGGER.exception("Error while commiting: %s", exc)
        else:
            acm.BeginTransaction()
            try:
                instrument = creator.create_price_swap_instrument(instrument_name)
                new_trade = creator.book_price_swap_trade(instrument)
                acm.CommitTransaction()
                self.price_swap_trades.append(new_trade)
                LOGGER.info("Trade %s booked successfully." % new_trade.Oid())
            except Exception as exc:
                acm.AbortTransaction()
                LOGGER.exception("Error while commiting: %s", exc)
    
        
class CreatePriceSwapTradesOutput(FUxCore.LayoutDialog):
    #Embedding trading manager sheets into custom dialogs
    
    def __init__(self, caption, trades):
        self.caption = caption
        
        self.trade_sheet = None
        self.trade_portfolio = None
        
        trade_list = trades
        
        #Add trades to the sheet
        self.add_trades(trade_list)
            
            
    def initialise_sheet(self):
        #Change sheet default columns to the ones listed below     
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
        #Insert Items and add to the sheet.      
        self.trade_portfolio = acm.FASQLQueryFolder()
        self.trade_portfolio.Name('Price Swaps')
        query = acm.CreateFASQLQuery('FTrade', 'OR')
        
        for trade in trade_list:
            query.AddOpNode('OR')
            query.AddAttrNode('Oid', 'EQUAL', trade.Oid())
            
        self.trade_portfolio.AsqlQuery(query)


    def CreateLayout(self):
        #Create the dialog layout
        b = acm.FUxLayoutBuilder()
        b.BeginVertBox('None')
        
        b.  AddSpace(5)
        b.  AddSeparator()
        b.  AddSpace(5)
        b.  BeginVertBox()
        b.    AddCustom('trade_sheet', 'sheet.FTradeSheet', 500, 250)
        b.  EndBox()
        b.  AddSpace(5) 
        b.  AddSeparator()
        
        b.  AddSpace(10)
        b.  BeginHorzBox()
        b.    AddFill()
        b.    AddButton('ok', 'OK')
        b.    AddButton('cancel', 'Cancel')
        b.  EndBox()
        b.EndBox()
        
        return b


    def HandleCreate(self, dialog, layout):
        self.dialog = dialog
        dialog.Caption(self.caption)
        
        #get a handle to the sheet
        ctrl = layout.GetControl
        self.trade_sheet = ctrl('trade_sheet').GetCustomControl()
        
        self.initialise_sheet()
        
        
    def HandleApply(self):
        return True

        
def ael_main(ael_dict):
    
    proc = CreatePriceSwapTradesFromExcelXLS(str(ael_dict['input_file']), ael_dict['underlyings'], ael_dict['commodity_names'], 
                                             ael_dict['calendars'], ael_dict['currency'], ael_dict['paydaymethod'], ael_dict['payoffset'])
    proc.add_error_notifier(notify_log)
    proc.process(False)
    price_swap_trades = proc.price_swap_trades    
    
    #calling the output data function
    shell = acm.UX().SessionManager().Shell()
    dlg = CreatePriceSwapTradesOutput('Price Swaps', price_swap_trades)
    dlgResult = dialogResult = acm.UX().Dialogs().ShowCustomDialogModal(shell, dlg.CreateLayout(), dlg)
    
    LOGGER.info("Complete.")

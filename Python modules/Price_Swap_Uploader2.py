import acm
import FRunScriptGUI
import FUxCore
from at_ael_variables import AelVariableHandler
from at_logging import getLogger
from datetime import datetime
from at_feed_processing import (SimpleXLSFeedProcessor, notify_log)
import traceback
from GValidation import show_exception
from FAFOUtils import custom_resets

businessLogicHandler = acm.FBusinessLogicGUIDefault()
ael_variables = AelVariableHandler()

#List of input file type extensions
fileFilter = "XLSX Files (*.xlsx)|*.xlsx|CSV Files (*.csv)|*.csv|"
inputFile = FRunScriptGUI.InputFileSelection(FileFilter=fileFilter)

LOGGER = getLogger(__name__)

#Parameters for input file

ael_variables.add('booking_option',
                  label = 'Booking option',
                  default = 'FloatVsFixed',
                  collection = ['FloatVsFloat', 'FloatVsFixed'],
                  mandatory = True)

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
                  default='USD New York,GBP London,ZAR Johannesburg',
                  tab='Calendars')
ael_variables.add('underlyings',
                  label='Underlyings',
                  mandatory=True,
                  multiple = True,
                  default='XPT,XPD,XAU',
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
    #LEGS = {1 : ['Float', 'False'], 2 : ['Fixed', 'True']}
    CONTRACT_SIZE = 1
    
    
    def __init__(self, price_ref, nominal, fixed_rate, counterparty, portfolio, start, end, count, underlyings, commodity_names, calendar, currency, payday_method, pay_offset, LEGS, leg_dates, booking_option):
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
        self.ins_legs = LEGS
        self.booking_option = booking_option
        #self.dates = {'Pay start':leg_dates[0],'Pay end': leg_dates[1],'Rec start':leg_dates[2],'Rec end':leg_dates[3],'Pay pay date': leg_dates[4],'Rec pay date':leg_dates[5]}
        underlying_index = underlyings.index(self.price_ref)
        self.commodity = commodity_names[underlying_index]
        
        if self.booking_option == "FloatVsFloat":
            self.ins_legs= {1 : ['Float', 'False'], 2 : ['Float', 'True']}
            

    
    def get_instrument_name(self):
        #Create instrument name
        counter = 1
        end_date = datetime.strptime(acm.Time.DateAddDelta('1899-12-30', 0, 0, self.end), '%Y-%m-%d')
        start_date = datetime.strptime(self.TODAY, '%Y-%m-%d')
        if self.booking_option == 'FloatVsFloat':
            name_factor = self.commodity 
            
        else:
            name_factor = str(self.fixed_rate)
        new_name = self.currency + '/' + self.commodity + '/' + 'THARISA' + '/' + end_date.strftime("%b") \
                    + end_date.strftime("%y") + '/' + name_factor + '/' + start_date.strftime("%d") \
                    + start_date.strftime("%b") + start_date.strftime("%y") + '##' + str(counter)
        ins_obj = acm.FInstrument[new_name]
        while ins_obj:
            counter += 1
            new_name = self.currency + '/' + self.commodity + '/' + 'THARISA' + '/' + end_date.strftime("%b") \
                        + end_date.strftime("%y") + '/' + name_factor + '/' + start_date.strftime("%d") \
                        + start_date.strftime("%b") + start_date.strftime("%y") + '##' + str(counter)
            ins_obj = acm.FInstrument[new_name]
        return new_name
    
        
        
    def create_price_swap_instrument(self, name):
        #Create new price swap instrument
        instrument = acm.FPriceSwap()
        instrument.RegisterInStorage()
        instrument = acm.FInstrumentLogicDecorator(instrument, businessLogicHandler)
    
        for key, value in self.ins_legs.items():
            if self.booking_option == 'FloatVsFloat':
                if value[0] == 'Float' and value[1] == 'True':
                    LOGGER.info('key is {}'.format(key))
                    key = 1
                    LOGGER.info('key changed to {}'.format(key))
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
        #trade.Nominal(self.nominal)
        trade.Counterparty(self.counterparty)
        trade.Currency(self.USD_CURRENCY)
        trade.TradeTime(self.TODAY)
        trade.ExecutionTime(self.TODAY)
        trade.ValueDay(self.VALUE_DAY)
        trade.AcquireDay(self.VALUE_DAY)
        trade.Portfolio(self.portfolio)
        trade.Acquirer(self.TRD_ACQUIRER)
        trade.Status(self.TRADE_STATUS)
        trade.Trader(acm.User())
        #trade.Nominal(trade.Quantity())
        trade.Commit()
        return trade
        
    
    
class CreatePriceSwapTradesFromExcelXLS(SimpleXLSFeedProcessor):
    
    def __init__(self, file_path, underlyings, commodity_names, calendar, currency, payday_method, pay_offset, LEGS, booking_option):
        self.price_swap_trades = []
        SimpleXLSFeedProcessor.__init__(self, file_path, sheet_index=0, sheet_name=None)
        self.price_swap_trades = []
        self.calendar = calendar
        self.currency = currency
        self.underlyings = underlyings
        self.commodity_names = commodity_names
        self.payday_method = payday_method
        self.pay_offset = pay_offset
        self.Legs = LEGS
        self.option = booking_option
        
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
            payLeg_start = acm.Time.AsDate(record_data['PayLeg Start Date'])
            payLeg_end = acm.Time.AsDate(record_data['PayLeg End Date'])
            recLeg_start = acm.Time.AsDate(record_data['RecLeg Start Date'])
            recLeg_end = acm.Time.AsDate(record_data['RecLeg End Date'])
            payLeg_pay = acm.Time.AsDate(record_data['PayLeg Pay Date'])
            recLeg_pay = acm.Time.AsDate(record_data['RecLeg Pay Date'])
            count = str(_index)
        except Exception as exc:
            msg = 'Row #%d: Failed to read data from file: %s' % (_index, str(exc))
            LOGGER.exception(msg)
            raise self.RecordProcessingException(msg)
        leg_dates = [payLeg_start, payLeg_end, recLeg_start, recLeg_end, payLeg_pay, recLeg_pay]
        dates = {'Pay start':leg_dates[0],'Pay end': leg_dates[1],'Rec start':leg_dates[2],'Rec end':leg_dates[3],'Pay pay date': leg_dates[4],'Rec pay date':leg_dates[5]}
        creator = PriceSwapCreator(price_ref, nominal, fixed_rate, counterparty, portfolio, start, end, count, self.underlyings,
                                   self.commodity_names, self.calendar, self.currency, self.payday_method, self.pay_offset, self.Legs, leg_dates, self.option)
        instrument_name = creator.get_instrument_name()
        instrument = acm.FInstrument[instrument_name]
        
        if instrument:
            try:
                new_trade = creator.book_price_swap_trade(instrument)
                LOGGER.info('Trade nominal is {}'.format(new_trade.Nominal()))
                self.price_swap_trades.append(new_trade)
                LOGGER.info('Trade nominal is {}'.format(new_trade.Nominal()))
                LOGGER.info("Trade %s booked successfully." % new_trade.Oid())
                if  dates <> None:
                    custom_resets(new_trade, dates)
                    LOGGER.info('Cashflows for trade %s were changed.' % new_trade.Oid())
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
                if dates <> None:
                    custom_resets(new_trade, dates)
                    LOGGER.info('Cashflows for trade %s were changed.' % new_trade.Oid())
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
    LEGS = {1 : ['Float', 'False'], 2 : ['Fixed', 'True']}
    proc = CreatePriceSwapTradesFromExcelXLS(str(ael_dict['input_file']), ael_dict['underlyings'], ael_dict['commodity_names'], 
                                             ael_dict['calendars'], ael_dict['currency'], ael_dict['paydaymethod'], ael_dict['payoffset'], LEGS, ael_dict['booking_option'])
    
    proc.add_error_notifier(notify_log)
    proc.process(False)
    price_swap_trades = proc.price_swap_trades    
    
    #calling the output data function
    shell = acm.UX().SessionManager().Shell()
    dlg = CreatePriceSwapTradesOutput('Price Swaps', price_swap_trades)
    dlgResult = dialogResult = acm.UX().Dialogs().ShowCustomDialogModal(shell, dlg.CreateLayout(), dlg)
    LOGGER.info("Complete.")
    

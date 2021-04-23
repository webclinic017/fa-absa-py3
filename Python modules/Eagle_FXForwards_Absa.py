"""
----------------------------------------------------------------------------------------
DESCRIPTION
    Developer           : Mighty Mkansi
    Date                : 2017-10-09
    Purpose             : Creates an FX Forwards trade file for TDB
    Requestor           : Kieron Mcewan
    CR Number           : 
ENDDESCRIPTION

DATE        DEVELOPER           DESCRIPTION
----------------------------------------------------------------------------------------
2018-06-18  Ondrej Bahounek     Replace NGX currency with NGN.
----------------------------------------------------------------------------------------
"""

import acm
import csv
import sys
import FBDPGui
import FRunScriptGUI
import datetime
import math
import os
from at_ael_variables import AelVariableHandler
from at_logging import  getLogger

ael_variables = AelVariableHandler()

LOGGER = getLogger()

directory_selection=FRunScriptGUI.DirectorySelection()
today = acm.Time().DateToday()

rundate = datetime.datetime.strptime(today, '%Y-%m-%d').strftime('%Y%m%d')

EXTRA_CURR_MAPPING = {
    'NGX' : 'NGN'
    }
    
    
def get_currency(curr_name):
    return EXTRA_CURR_MAPPING.get(curr_name, curr_name)


class BaseInstrTrade:

    def __init__(self, trade, leg):
        self.trade = trade
        self.instrument = trade.Instrument()
        self.underlying = self.instrument.Underlying()
        self.originalTrade = trade.Contract()
        self.originalInstrument = None
        if self.originalTrade:
            self.originalInstrument = self.originalTrade.Instrument()
        self.leg = leg
    
    def _source_id(self):
        return 'ABS-FX'

    def _trade_id(self):
        return ('FXB' + str(self.trade.Oid()))[:30]

    def _leg_number(self):
        return 1
        
    def _dealt_rate(self):
        return format(self.trade.Price(), '0.8f')
    
    def _quoting_terms(self):
        trade_curr = self.trade.Currency().Name()
        und_curr = self.trade.Instrument().Underlying().Name()
        curr_pair = [trade_curr, und_curr]
        if 'USD' in curr_pair:
            base_currency = 'USD'
        else:
            if 'EUR' in curr_pair:
                base_currency = 'EUR'
            else:
                if 'GBP' in curr_pair:
                    base_currency = 'GBP'
                else:
                    usd_curr = acm.FCurrency['USD']
                    for price in usd_curr.Prices():
                        if price.Market().Name() == 'SPOT':
                            if price.Currency().Name() == curr_pair[0]:
                                price_pair_one = [price.Currency().Name(), price.Settle()]
                            if price.Currency().Name() == curr_pair[1]:
                                price_pair_two = [price.Currency().Name(), price.Settle()]
                            
                    ratio = price_pair_one[1]/price_pair_two[1]
                    if ratio < 1:
                        base_currency = price_pair_one[0]
                    else:
                        base_currency = price_pair_two[0]
        if base_currency == trade_curr:
            return 1
        return 0

    
    def _primary_amount(self):
        return format(-1*self.trade.BaseCostDirty(), '0.2f')        
    
    def _primary_currency(self):
        curr = self.trade.Currency().Name()
        return get_currency(curr)
        
    def _counter_amount(self):
        return format(self.trade.BaseCostDirty() * self.trade.Price(), '0.2f')
    
    def _counter_currency(self):
        curr = self.trade.Instrument().Underlying().Name()
        return get_currency(curr)
    
    def _ccy2_amount_npv_gbp(self):
        ccy2_spot = self.trade.Instrument().Underlying().UsedPrice(acm.Time.DateToday(), 'GBP', 'SPOT')
        return format(self.trade.BaseCostDirty() * self.trade.Price() * ccy2_spot, '0.2f')
    
    def _ccy1_amount_npv_gbp(self):       
        ccy1_spot = self.trade.Currency().UsedPrice(acm.Time.DateToday(), 'GBP', 'SPOT')
        return format(-1*self.trade.BaseCostDirty() * ccy1_spot, '0.2f')
    
    def _settlement_principal_amount(self):
        return ''
        
    def _settlement_currency(self):
        curr = self.trade.Currency().Name()
        if self.trade.Quantity() > 0:
            curr = self.trade.Instrument().Underlying().Name()
        return get_currency(curr)
        
    def _value_date(self):        
        return datetime.datetime.strptime(self.instrument.ExpiryDate(), '%Y-%m-%d %H:%M:%S').strftime('%Y%m%d')
    
    def _option_start_date(self):
        return ''
    
    def _fixing_date(self):
        return ''
    
    def _fixing_rate(self):
        return ''
    
    def _spot_rate(self):
        return ''
    
    def _ccy1_amount_npv_ccy(self):
        return ''
        
    def _instr_product_type(self):    
        if self.instrument.InsType() == 'Future/Forward':            
            return  'FXForward'
        return self.instrument.InsType()[:50]        
    
    def _book(self):
        book = self.trade.Portfolio().Name()
        return book[:15]   
   
    def _trade_date(self):       
        return datetime.datetime.strptime(self.trade.AcquireDay(), '%Y-%m-%d').strftime('%Y%m%d')  
    
    def _maturity_date(self):
        return datetime.datetime.strptime(self.instrument.ExpiryDate(), '%Y-%m-%d %H:%M:%S').strftime('%Y%m%d')        
    
    def _buy_sell(self):
        indicator = 'BUY'
        if self.trade.Quantity() < 0 :
            indicator = 'SELL'
        return indicator        
    
    def _trade_event(self):
        return 'NEW'
        
    def _sds_counterparty_id(self):
        return self.trade.Counterparty().AdditionalInfo().BarCap_Eagle_SDSID()
        
    def _absa_counterparty_id(self):
        return self.trade.Counterparty().Oid()
    
    def _trader_id(self):
        return self.trade.Trader().Name()

    def _broker_id(self):
        return self.trade.Trader().Name()[:20]
        
    def _internal_flag(self):
        return 'N'
    
    def _validation_flag(self):
        return ''
    
    def _comments(self):
        return ''
        
    def _execution_sales_person_id(self):
        return ''
    
    def _fixing_comments(self):
        return ''
    
    def _fixing_trader_id(self):
        return ''
    
    def _link_id(self):
        return ''
    
    def _parent_id(self):
        return ''
    
    def _rate_aggressor(self):
        return ''
    
    def _sales_credit_type(self):
        return ''
    
    def _trading_medium(self):
        return ''
    
    def _fixing_entry_date_time(self):
        return ''    
    
    def _sales_credit_type(self):
        return ''
    
    def _trading_medium(self):
        return ''
    
    def _fixing_entry_date_time(self):
        return ''
        
class FXForwardsAbsaTradeReport:
    def __init__(self, file):
        self.file  = file
      
    def field_names(self):
        fieldNames = ['SOURCE_ID',
            'SOURCE_TRADE_ID',
            'PRODUCT_TYPE',
            'SUB_TYPE',            
            'BOOK',            
            'TRADE_DATE',
            'MATURITY_DATE',
            'BUY_OR_SELL',
            'TRADE_EVENT',
            'SDS_COUNTERPARTY_ID',
            'ABSA_COUNTERPARTY_ID',
            'TRADER_ID',
            'BROKER_ID',
            'INTERNAL_FLAG',
            'VALIDATION_FLAG',
            'COMMENTS',
            'EXECUTION_SALES_PERSON_ID',
            'FIXING_COMMENTS',
            'FIXING_TRADER_ID',
            'LINK_ID',
            'PARENT_ID',
            'RATE_AGGRESSOR',
            'SALES_CREDIT_TYPE',
            'TRADING_MEDIUM',
            'FIXING_ENTRY_DATE_TIME',
            ]
            
        return fieldNames
        
    def write_header(self):
        
        writer = csv.writer(self.file, delimiter='|', quotechar='|', quoting=csv.QUOTE_MINIMAL)
       
        
    
    def write_column_names(self):
        fieldnames = self.field_names()
        try:
            writer = csv.DictWriter(self.file, delimiter='|', fieldnames=fieldnames)
            writer.writerow(dict((fn, fn) for fn in fieldnames))
        
        finally:
            print ''
            
    def write_trade_row(self, baseInstrTrade):
        fields =[baseInstrTrade._source_id(),
                baseInstrTrade._trade_id(),
                baseInstrTrade._instr_product_type(),
                baseInstrTrade._instr_product_type(),
                baseInstrTrade._book(),
                baseInstrTrade._trade_date(),
                baseInstrTrade._maturity_date(),
                baseInstrTrade._buy_sell(),
                baseInstrTrade._trade_event(),
                baseInstrTrade._sds_counterparty_id(),
                baseInstrTrade._absa_counterparty_id(),
                baseInstrTrade._trader_id(),
                baseInstrTrade._broker_id(),
                baseInstrTrade._internal_flag(),
                baseInstrTrade._validation_flag(),
                baseInstrTrade._comments(),
                baseInstrTrade._execution_sales_person_id(),
                baseInstrTrade._fixing_comments(),
                baseInstrTrade._fixing_trader_id(),
                baseInstrTrade._link_id(),
                baseInstrTrade._parent_id(),
                baseInstrTrade._rate_aggressor(),
                baseInstrTrade._sales_credit_type(),
                baseInstrTrade._trading_medium(),
                baseInstrTrade._fixing_entry_date_time(),
                baseInstrTrade._rate_aggressor(),
                baseInstrTrade._sales_credit_type(),
                baseInstrTrade._trading_medium(),
                baseInstrTrade._fixing_entry_date_time(),
            ]
            
        writer = csv.writer(self.file, delimiter='|', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(fields)
        
    def _write_footer(self, count, checksum):
        writer = csv.writer(self.file, delimiter='|', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(['090', count, checksum])           

class FXForwardsAbsaTradeControlFile:
    def __init__(self, contrlfile):        
        self.contrlfile = contrlfile 
    
    def write_column(self, count, checksum):
        
        source = 'SOURCE|ABS-FX'
        target = 'TARGET|TDB'
        data_file = 'DATAFILE|TDB_FX_ABSA_TRADE_%s'%rundate + '.dat'
        cob_date = 'COB DATE|%s'%rundate        
        extract_date = 'EXTRACT DATE|%s'%datetime.datetime.strptime(acm.Time.DateToday(), '%Y-%m-%d').strftime('%Y%m%d %H:%M:%S')
        number_of_records = 'NO OF RECORDS|%s'%count
        check_sum = 'CHECKSUM|%s'%checksum
        
        fields = [source, target, data_file, cob_date, extract_date, number_of_records, check_sum]        
        writer = csv.writer(self.contrlfile, quoting=csv.QUOTE_MINIMAL)
        
        for field in fields:
            writer = csv.writer(self.contrlfile, quoting=csv.QUOTE_MINIMAL)            
            writer.writerow([field,])

class FXForwardsAbsaLegReport:
    def __init__(self, file):
        self.file  = file        
      
    def field_names(self):
        fieldNames = ['SOURCE_ID',
            'SOURCE_TRADE_ID',
            'LEG_NUMBER',
            'DEALT_RATE',            
            'QUOTING_TERMS',            
            'PRIMARY_AMOUNT',
            'PRIMARY_CURRENCY',
            'COUNTER_AMOUNT',
            'COUNTER_CURRENCY',
            'CCY2_AMOUNT_NPVGBP',
            'CCY1_AMOUNT_NPVGBP',
            'SETTLEMENT_PRINCIPAL_AMOUNT',
            'SETTLEMENT_CURRENCY',
            'VALUE_DATE',
            'OPTION_START_DATE',
            'FIXING_DATE',
            'FIXING_RATE',
            'SPOT_RATE',
            'CCY1_AMOUNT_NPVCCY',            
            ]
            
        return fieldNames
        
    def write_header(self):
        
        writer = csv.writer(self.file, delimiter='|', quotechar='|', quoting=csv.QUOTE_MINIMAL)     
    
    
    def write_column_names(self):
        fieldnames = self.field_names()
        try:
            writer = csv.DictWriter(self.file, delimiter='|', fieldnames=fieldnames)
            writer.writerow(dict((fn, fn) for fn in fieldnames))
        
        finally:
            print ''
            
    def write_trade_row(self, baseInstrTrade):
        fields =[baseInstrTrade._source_id(),
                baseInstrTrade._trade_id(),
                baseInstrTrade._leg_number(),
                baseInstrTrade._dealt_rate(),
                baseInstrTrade._quoting_terms(),
                baseInstrTrade._primary_amount(),
                baseInstrTrade._primary_currency(),
                baseInstrTrade._counter_amount(),
                baseInstrTrade._counter_currency(),
                baseInstrTrade._ccy2_amount_npv_gbp(),
                baseInstrTrade._ccy1_amount_npv_gbp(),
                baseInstrTrade._settlement_principal_amount(),
                baseInstrTrade._settlement_currency(),
                baseInstrTrade._value_date(),
                baseInstrTrade._option_start_date(),
                baseInstrTrade._fixing_date(),
                baseInstrTrade._fixing_rate(),
                baseInstrTrade._spot_rate(),
                baseInstrTrade._ccy1_amount_npv_ccy(),              
                ]
        
        writer = csv.writer(self.file, delimiter='|', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(fields)   
    
        
    def _write_footer(self, count, checksum):        
        writer = csv.writer(self.file, delimiter='|', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(['090', count, checksum])           

class FXForwardsAbsaLegControlFile:
    def __init__(self, contrlfile):        
        self.contrlfile = contrlfile 
    
    def write_column(self, count, checksum):
        
        source = 'SOURCE|ABS-FX'
        target = 'TARGET|TDB'
        data_file = 'DATAFILE|TDB_FX_ABSA_LEG' + '.dat'
        cob_date = 'COB DATE|%s'%rundate        
        extract_date = 'EXTRACT DATE|%s'%datetime.datetime.strptime(acm.Time.DateToday(), '%Y-%m-%d').strftime('%Y%m%d %H:%M:%S')
        number_of_records = 'NO OF RECORDS|%s'%count
        check_sum = 'CHECKSUM|%s'%checksum
        
        fields = [source, target, data_file, cob_date, extract_date, number_of_records, check_sum]        
        writer = csv.writer(self.contrlfile, quoting=csv.QUOTE_MINIMAL)
        
        for field in fields:
            writer = csv.writer(self.contrlfile, quoting=csv.QUOTE_MINIMAL)            
            writer.writerow([field,])
            

ael_variables.add('tradeFilter',
    label = 'Trade Filters',
    cls = 'FTradeSelection',    
    mandatory = True,
    multiple=True,
    default='TDB_FX_NDF')

ael_variables.add('filePath',
    label='File Path',
    mandatory = True,
    default='/services/frontnt/Task/')

ael_variables.add('reportType',
    label='Report Type',
    collection=('Leg Report', 'Trade Report'),
    mandatory = True,
    default='Trade Report')

ael_variables.add('fileName',
    label = 'File Name',
    cls = 'string', 
    collection = ('TDB_FX_ABSA_LEG'+'.DAT', 'TDB_FX_ABSA_TRADE'+'.DAT'),  
    mandatory = True,    
    default='TDB_FX_ABSA_TRADE'+'.DAT')
    

def ael_main(parameters):
    
    if parameters['reportType'] == 'Trade Report':    
        filename = parameters['filePath'] + 'TDB_FX_ABSA_TRADE_'+'.DAT'
        contlFilename = parameters['filePath'] +'TDB_FX_ABSA_TRADE_'+ '.ctl'
    else:
        filename = parameters['filePath'] + 'TDB_FX_ABSA_LEG_'+'.DAT'
        contlFilename = parameters['filePath'] +'TDB_FX_ABSA_LEG_' + '.ctl'

    tfname = parameters['tradeFilter'][0]
    
    file = open(str(filename), 'wb') 
    
    contrlfile = open(str(contlFilename), 'wb')
    
    if parameters['reportType'] == 'Trade Report': 
        report = FXForwardsAbsaTradeReport(file)
        contrlReport =  FXForwardsAbsaTradeControlFile(contrlfile)
    else:
        report = FXForwardsAbsaLegReport(file)
        contrlReport =  FXForwardsAbsaLegControlFile(contrlfile)
    
    #Write header and column names as per spec requirement
    report.write_header()
    report.write_column_names()    
    checksum = 0
    count = 1
    
    for trade in tfname.Trades():
       
        baseInsr = BaseInstrTrade(trade, 0)
        report.write_trade_row(baseInsr)
        count += 1
        
        if parameters['reportType'] == 'Trade Report':
            amt = baseInsr._absa_counterparty_id()
            checksum += amt
        else:
            amt = float(baseInsr._primary_amount())
            checksum += amt
        
    #report._write_footer(count,checksum)    
    
    count = count
    contrlReport.write_column(count, int(checksum))
    #contrlReport._writeControlFile(count,checksum)
    
    file.close()
    contrlfile.close()    
   
    LOGGER.info(checksum)
    LOGGER.info('File Created Successfully')
    LOGGER.info('Wrote secondary output to::: %s', filename)

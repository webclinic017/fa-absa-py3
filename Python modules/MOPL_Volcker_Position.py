import acm, ael, string, time
from at_time import acm_date, ael_date, to_datetime, to_date
from datetime import datetime
import os.path
import csv
import FLogger
from at_ael_variables import AelVariableHandler
from collections import defaultdict, namedtuple

LOGGER = None
LOG_LEVEL = {'DEBUG': 2, 'INFO': 1, 'WARNING':3, 'ERROR':4}

END_DATES = {
    'Now': acm_date('Today'), 
    'TwoDaysAgo': acm_date('TwoDaysAgo'),
    'PrevBusDay': acm_date('PrevBusDay'),  
    'Yesterday': acm_date('Yesterday'), 
    'Custom Date': acm_date('Today'),}

ael_variables = AelVariableHandler()

ael_variables.add('inputPath', label = 'Input Path', cls = 'string', default ='C:\Share\Volcker\Midas FX Only')
ael_variables.add('log_level',label='Log Level',cls = 'string',collection = ['DEBUG', 'INFO', 'WARNING', 'ERROR'],default = 'INFO',)
ael_variables.add('outputPath', label = 'Output Path', cls = 'string', default ='C:\Share\Volcker\Midas FX Only')
ael_variables.add('output_fileName', label = 'Output File Name', cls = 'string', default = 'Volcker_Mopl_Position_Radial.dat')
ael_variables.add('endDate', label = 'Report Date', cls = 'string', collection = END_DATES.keys(), default = 'PrevBusDay',mandatory = True)

SPOT_TYPES = ['X1', 'X2','X5','C1', 'C2','R1', 'R2']

REPORT_ENTRY = namedtuple('volcker_report_entry', [
    'POSITION_ID', 'BOOK', 'SECURITY_IDENTIFIER','SECURITY_DESCRIPTION', 'PRODUCT_NAME', 'LONG_SHORT', 'CURRENCY',
    'ORIGINAL_NOTIONAL', 'MARKET_VALUE', 'DELTA', 'DELTA_INSTRUMENT', 'IR01', 'TENYRIR01',
    'SOURCE_SYSTEM', 'RISKMEASURE', 'TEN_YEAR_BOND_UNIT', 'IS_MARKET_MAKING',
    'SECONDARY_CURRENCY', 'FO_SUB_PRODUCT_TYPE',
])

def _init_logging(log_directory, log_level):
    '''initialize logging'''
    global LOGGER
    LOGGER = FLogger.FLogger('Volcker_IA_MIDAS_Feed')
    LOGGER.Reinitialize(
        level=LOG_LEVEL[log_level], 
        keep=False, 
        logOnce=False, 
        logToConsole=True, 
        logToPrime=True, 
        #logToFileAtSpecifiedPath=os.path.join(log_directory, 
        #    'Repcube_Hedge_Report_%s.log' % acm_datetime('TODAY')
        #), 
        filters=None)
        
def get_trade_id(trade):
    return trade['TradeNumber'] + "_" + trade['SourceSystemBookId']# concat trade date due to reuse of midas trade numbers
        
def get_trade_static_data(filepath):
    tradeLookup = {}
    LOGGER.LOG('Reading static data.')
    with open(filepath) as csvfile:
        reader = csv.DictReader(csvfile)                
        for row in reader:
            #not interested in fx spots
            if(row['InsType'] in SPOT_TYPES):
                continue
            tradeLookup[row['TradeNumber']]=row
    LOGGER.LOG('Successfully fetched static data.')
    return tradeLookup


def get_trade_scalar_data(filepath):
    tradeLookup = {}
    LOGGER.LOG('Reading scalar data.')
    with open(filepath) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            #not interested in fx spots
            if(row['InsType'] in SPOT_TYPES):
                continue
                
            trdId = get_trade_id(row)
            if(trdId in tradeLookup):
                tradeLookup[trdId].append(row)
            else:
                tradeLookup[trdId] = [row]
    LOGGER.LOG('Successfully fetched scalar data.')
    return tradeLookup 

def getPV(trdId, tradeScalars):
    marketVal = 0.00
    for scalar in tradeScalars[trdId]:
        if(scalar['Dictionary'] == 'COB' and scalar['Type'] == 'PV'):
            marketVal += float(scalar['_Value'])     
    return marketVal
    
def getFXFWD(trdId, tradeScalars, curr1, curr2):
    val = 0.00
    for scalar in tradeScalars[trdId]:
        if(scalar['Dictionary'] == 'COB' and scalar['Type'] == 'FXFWD' and curr1 in scalar['Index'] and curr2 in scalar['Index']):
            return float(scalar['_Value'])     
    return val

def file_data(trade, tradeScalars, repday, *rest):
    # calculated values #
    trdId = get_trade_id(trade)  
    
    marketVal = getPV(trdId, tradeScalars)       

    if round(marketVal , 2) == 0.00:
        data = []
    else:        
        
        instrumentDelta = getFXFWD(trdId, tradeScalars, trade['Ccy1'], trade['Ccy2'])
        
        internalTrade = 'No'
        if(trade['InsType'] == 'SH'):
            internalTrade = 'Yes'
        
        longShort = ''
        if float(trade['Nominal1']) >= 0:
            longShort = 'L'
        else:
            longShort = 'S'                   
        
        
        data = REPORT_ENTRY(            
            POSITION_ID = trdId, 
            BOOK = trade['SourceSystemBookId'], 
            SECURITY_IDENTIFIER = 'InstrumentName',             
            SECURITY_DESCRIPTION = 'InstrumentName',             
            PRODUCT_NAME = 'Future/Forward',
            LONG_SHORT = longShort,             
            CURRENCY = 'ZAR', 
            ORIGINAL_NOTIONAL = trade['Nominal1'],             
            MARKET_VALUE = str(round(marketVal, 2)), 
            DELTA = '0.00', 
            DELTA_INSTRUMENT= str(round(instrumentDelta, 2)),
            IR01= '0.00', 
            TENYRIR01 = '0.00', 
            SOURCE_SYSTEM = 'MIDAS',        
            RISKMEASURE = 'FXDelta',            
            TEN_YEAR_BOND_UNIT = '',            
            IS_MARKET_MAKING = '',
            SECONDARY_CURRENCY = trade['Ccy2'],
            FO_SUB_PRODUCT_TYPE = ''            
)
    
    return data
        
def ael_main(ael_dict,*rest):   
    
    _init_logging('', ael_dict['log_level'])       
    
    if ael_dict['endDate'] == 'Custom Date':
        endDate = ael_dict['enddateCustom']
    else:
        endDate = str(END_DATES[ael_dict['endDate']])    
    repday = ael.date_from_string(endDate)    
    
    fileName_Static = 'Midas_Static__' + repday.to_string('%Y%m%d') + '.csv'
    fileName_Scalar = 'Midas_Scalar__' + repday.to_string('%Y%m%d') + '.csv'
    
    tradeStatic = get_trade_static_data(os.path.join(ael_dict['inputPath'], fileName_Static))
    tradeScalars = get_trade_scalar_data(os.path.join(ael_dict['inputPath'], fileName_Scalar))
        
    #outFilePath = os.path.join(ael_dict['outputPath'], ael_dict['output_fileName'])
    outFilePath = os.path.join(ael_dict['outputPath'], datetime.strftime(to_date(END_DATES[ael_dict['endDate']]), '%Y%m%d'))
    if not os.path.exists(outFilePath):
        os.makedirs(outFilePath)
    outFilePath = os.path.join(outFilePath, ael_dict['output_fileName'])
    
    with open(outFilePath, 'w') as f:        
        writer = csv.DictWriter(
            f,
            REPORT_ENTRY._fields,
            delimiter='|',
            lineterminator = '\n'
        )
	writer.writerow(dict(list(zip(REPORT_ENTRY._fields, REPORT_ENTRY._fields))))
        for trade in tradeStatic:                                    
            line = file_data(tradeStatic[trade], tradeScalars, repday)
            LOGGER.LOG('Processing trade ' + trade)
            if type(line) == REPORT_ENTRY:
                writer.writerow(line._asdict())        
        LOGGER.LOG('Created  output file '  + outFilePath)
        LOGGER.LOG('Completed Successfully.')
            

           

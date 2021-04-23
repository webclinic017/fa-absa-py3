import acm, ael, string, time
from at_time import acm_date, ael_date, to_datetime, to_date
import os.path
from datetime import datetime
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
ael_variables.add('output_fileName', label = 'Output File Name', cls = 'string', default = 'Volcker_Mopl_Trade_Radial.dat')
ael_variables.add('endDate', label = 'Report Date', cls = 'string', collection = END_DATES.keys(), default = 'PrevBusDay',mandatory = True)

SPOT_TYPES = ['X1', 'X2','X5','C1', 'C2','R1', 'R2', 'CA']

REPORT_ENTRY = namedtuple('volcker_report_entry', [
    'TRADE_ID', 'LEG', 'POSITION_ID', 'BOOK', 'INSTRUMENT_IDENTIFIER_TYPE',
    'INSTRUMENT_IDENTIFIER', 'INSTRUMENT_DESCRIPTION', 'TRADE_DATE',
    'TRADE_TIME', 'PRODUCT_NAME', 'BUY_SELL', 'TRADE_STATUS', 'CURRENCY',
    'COUNTERPARTY_TYPE', 'COUNTERPARTY_ID', 'NOTIONAL', 'CONTRACT_SIZE',
    'NUMBER_OF_CONTRACTS', 'UNDERLYING_PRICE', 'PRICE_DELTA', 'INSTRUMENT_DELTA', 'IR01',
    'MARKET_VALUE', 'SOURCE_SYSTEM', 'OPTION_TYPE', 'STRIKE', 'COUPON',
    'UNDERLYING_SYMBOL', 'PRICE', 'MATURITY_DATE', 'CURVE', 'AGE', 
    'BCML_PRODUCT_SUB_TYPE_YN','QUANTITY','AGE_METHODOLOGY', 'RATE', 'TENYRBOND_IR01', 
    'RISKMEASURE', 'MATURITY','TEN_YEAR_BOND_UNIT', 'FO_PRODUCT_TYPE','SECTOR', 
    'COUNTRY', 'TRADE_VERSION', 'IS_MARKET_MAKING', 'SECONDARY_CURRENCY', 'FO_SUB_PRODUCT_TYPE',
    'IS_BLOCK_OR_ALLOCATION','IS_INTERNAL_TRADE'
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
    return trade['TradeNumber'] + "_" + trade['SourceSystemBookId']
    
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

def file_data(trade, tradeScalars, sdsIdLookup, repday, *rest):
    # calculated values #
    trdId = get_trade_id(trade)
    
    marketVal = getPV(trdId, tradeScalars)       
    if round(marketVal , 2) == 0.00:
        data = []
    else:
         
        
        price = float(trade['Strike'])  #Fwd price
        instrumentDelta = getFXFWD(trdId, tradeScalars, trade['Ccy1'], trade['Ccy2'])
        
        internalTrade = 'No'
        if(trade['InsType'] == 'SH'):
            internalTrade = 'Yes'
        
        buysell = ''
        if float(trade['Nominal1']) >= 0:
            buysell = 'B'
        else:
            buysell = 'S'        
    
        expiryDate =datetime.strptime(trade['ExpDay'], '%d/%m/%Y %H:%M:%S')
        # age #        
        trdDay = datetime.strptime(trade['TrdDay'], '%d/%m/%Y %H:%M:%S')
       
        age_date = ael_date(trdDay)        
        if(age_date < ael_date("Today")):
            return []
        age = age_date.days_between(repday)
        
        sdsId =''
        midasCtpy = str(trade['Ctpy_Id'])
        if midasCtpy in sdsIdLookup:
            sdsId = sdsIdLookup[midasCtpy]
        else:            
            LOGGER.LOG('Could not find Midas ctpy id in SDS mapping - (trade, midas  ctyp id)'  + trade['TradeNumber'] + "," + trade['Ctpy_Id'])
        
        data = REPORT_ENTRY(
            TRADE_ID = trdId,
            LEG = '2',  #spec says fro FX fwds this mshould be 2
            POSITION_ID = trdId, 
            BOOK = trade['SourceSystemBookId'], 
            INSTRUMENT_IDENTIFIER_TYPE = 'InstrumentName', 
            INSTRUMENT_IDENTIFIER = '', 
            INSTRUMENT_DESCRIPTION = trade['Ccy1'] +'/' + trade['Ccy2'], 
            TRADE_DATE = datetime.strftime(trdDay, '%Y%m%d'), 
            TRADE_TIME = '00:00', 
            PRODUCT_NAME = 'FX Fwd',
            BUY_SELL = buysell, 
            TRADE_STATUS = trade['Status'], 
            CURRENCY = 'ZAR', 
            COUNTERPARTY_TYPE = 'SDS', 
            COUNTERPARTY_ID = sdsId, 
            NOTIONAL = trade['Nominal1'], 
            CONTRACT_SIZE = '', 
            NUMBER_OF_CONTRACTS = '',
            UNDERLYING_PRICE = '0.00',   
            PRICE_DELTA = instrumentDelta,  
            INSTRUMENT_DELTA = '0.00',
            IR01 = '0.00', 
            MARKET_VALUE = str(round(marketVal, 2)), 
            SOURCE_SYSTEM = 'MIDAS', 
            OPTION_TYPE = '', 
            STRIKE = '', 
            COUPON = '', 
            UNDERLYING_SYMBOL = '', 
            PRICE = str(round(price, 6)),    
            MATURITY_DATE = datetime.strftime(expiryDate, '%Y%m%d'), 
            CURVE = '', 
            AGE = str(age), 
            BCML_PRODUCT_SUB_TYPE_YN = 'N', 
            QUANTITY = '', 
            AGE_METHODOLOGY = 'D',
            RATE = str(round(price, 6)),
            TENYRBOND_IR01 = '0.00',
            RISKMEASURE = 'FXDelta',
            MATURITY = datetime.strftime(expiryDate, '%Y%m%d'),
            TEN_YEAR_BOND_UNIT = '',
            FO_PRODUCT_TYPE = 'Future/Forward',
            SECTOR = '',
            COUNTRY ='',
            TRADE_VERSION = '1',
            IS_MARKET_MAKING = '',
            SECONDARY_CURRENCY = trade['Ccy2'],
            FO_SUB_PRODUCT_TYPE = '',
            IS_BLOCK_OR_ALLOCATION = '',
            IS_INTERNAL_TRADE = internalTrade   #Nina to confirm if only SH ( R1 is excluded )
)
    
    return data

def LoadClientData(filepath):
    sdsLookup = {}
    LOGGER.LOG('Reading client data.')
    with open(filepath) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            #not interested in fx spots            
            if(row['EnterpriseSourceSystem'] == 'SDS' and row['AliasSourceSystem']== 'Midas'):                
                sdsLookup[row['AliasId']] = row['EnterpriseId']
    LOGGER.LOG('Successfully loaded client data.')   
    return sdsLookup 
    
        
def ael_main(ael_dict,*rest):   
    
    _init_logging('', ael_dict['log_level'])       
    
    if ael_dict['endDate'] == 'Custom Date':
        endDate = ael_dict['enddateCustom']
    else:
        endDate = str(END_DATES[ael_dict['endDate']])    
    repday = ael.date_from_string(endDate)    
    
    fileName_Static = 'Midas_Static__' + repday.to_string('%Y%m%d') + '.csv'
    fileName_Scalar = 'Midas_Scalar__' + repday.to_string('%Y%m%d') + '.csv'
    
    #TODO remove Hard coded path to client file
    midasSDSMap = LoadClientData(os.path.join('/apps/frontnt/REPORTS/BackOffice/Atlas-End-Of-Day/Volcker/Static', 'ClientData.csv'))
    
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
            LOGGER.LOG('Processing trade ' + trade)
            line = file_data(tradeStatic[trade], tradeScalars, midasSDSMap, repday)            
            if type(line) == REPORT_ENTRY:
                writer.writerow(line._asdict())        
        LOGGER.LOG('Created  output file '  + outFilePath)
        LOGGER.LOG('Completed Successfully.')
            

           

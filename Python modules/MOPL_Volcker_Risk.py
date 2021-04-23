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
ael_variables.add('output_fileName', label = 'Output File Name', cls = 'string', default = 'Volcker_Mopl_Risk_Radial.dat')
ael_variables.add('endDate', label = 'Report Date', cls = 'string', collection = END_DATES.keys(), default = 'PrevBusDay',mandatory = True)

SPOT_TYPES = ['X1', 'X2','X5','C1', 'C2','R1', 'R2']

REPORT_ENTRY = namedtuple('volcker_report_entry', [
    'FEEDSYSTEM', 'RISKSYSTEMTYPE', 'RISKSYSTEMINSTANCE','RISKCONFIGURATIONID', 'RISKSUBJECTID', 'RISKSUBJECTVERSION', 'TYPENAME',
    'VALUATIONNAME', 'BOOKID', 'TRADECCY', 'SENSITIVITYNAME', 'SENSTIVITYCONFIGURATIONID', 'VALUE',
    'DATAOBJECT1ID',
    'DATAOBJECT1TYPE',
    'DATAOBJECT1CURVEID',
    'DATAOBJECT1CCY',
    'DATAOBJECT1INSTRUMENTTYPE',
    'DATAOBJECT1INDEX',
    'DATAOBJECT1INSTRUMENTID',
    'DATAOBJECT1PROJECTIONID',
    'DATAOBJECT1AXIS1',
    'DATAOBJECT1AXIS1PARAM1',
    'DATAOBJECT1AXIS1PARAM2',
    'DATAOBJECT1AXIS1PARAM3',
    'DATAOBJECT1AXIS2',
    'DATAOBJECT1AXIS2PARAM1',
    'DATAOBJECT1AXIS2PARAM2',
    'DATAOBJECT1AXIS2PARAM3',
    'DATAOBJECT1AXIS3',
    'DATAOBJECT1AXIS3PARAM1',
    'DATAOBJECT1AXIS3PARAM2',
    'DATAOBJECT1AXIS3PARAM3',
    'DATAOBJECT2ID',
    'DATAOBJECT2TYPE',
    'DATAOBJECT2CURVEID',
    'DATAOBJECT2CURVECCY',
    'DATAOBJECT2INSTRUMENTTYPE',
    'DATAOBJECT2INDEX',
    'DATAOBJECT2INSTRUMENTID',
    'DATAOBJECT2PROJECTIONID',
    'DATAOBJECT2AXIS1',
    'DATAOBJECT2AXIS1PARAM1',
    'DATAOBJECT2AXIS1PARAM2',
    'DATAOBJECT2AXIS1PARAM3',
    'DATAOBJECT2AXIS2',
    'DATAOBJECT2AXIS2PARAM1',
    'DATAOBJECT2AXIS2PARAM2',
    'DATAOBJECT2AXIS2PARAM3',
    'DATAOBJECT2AXIS3',
    'DATAOBJECT2AXIS3PARAM1',
    'DATAOBJECT2AXIS3PARAM2',
    'DATAOBJECT2AXIS3PARAM3',
    'DATAOBJECT3ID',
    'DATAOBJECT3TYPE',
    'DATAOBJECT3CURVEID',
    'DATAOBJECT3CURVECCY',
    'DATAOBJECT3INSTRUMENTTYPE',
    'DATAOBJECT3INDEX',
    'DATAOBJECT3INSTRUMENTID',
    'DATAOBJECT3PROJECTIONID',
    'DATAOBJECT3AXIS1',
    'DATAOBJECT3AXIS1PARAM1',
    'DATAOBJECT3AXIS1PARAM2',
    'DATAOBJECT3AXIS1PARAM3',
    'DATAOBJECT3AXIS2',
    'DATAOBJECT3AXIS2PARAM1',
    'DATAOBJECT3AXIS2PARAM2',
    'DATAOBJECT3AXIS2PARAM3',
    'DATAOBJECT3AXIS3',
    'DATAOBJECT3AXIS3PARAM1',
    'DATAOBJECT3AXIS3PARAM2',
    'DATAOBJECT3AXIS3PARAM3',
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
    
def getFXDelta(trdId, tradeScalars, curr1, curr2):
    val = 0.00
    for scalar in tradeScalars[trdId]:
        if(scalar['Dictionary'] == 'COB' and scalar['Type'] == 'FXFWD' and curr1 in scalar['Index'] and curr2 in scalar['Index']):
            return float(scalar['_Value'])     
    return val

def file_data(trade, riskType, riskValue, repday, *rest):
    # calculated values #
    trdId = get_trade_id(trade) # concat trd date due to reuse of midas trade numbers    
    
    if round(riskValue , 2) == 0.00:
        data = []
    else:
        data = REPORT_ENTRY(  
	FEEDSYSTEM  ='ABSA', 
	RISKSYSTEMTYPE = 'MIDAS',
	RISKSYSTEMINSTANCE = '',
	RISKCONFIGURATIONID = '',
	RISKSUBJECTID = trdId,
	RISKSUBJECTVERSION = '0',
	TYPENAME = 'Trade',
	VALUATIONNAME = datetime.strftime(to_datetime(repday), '%Y%m%d'),
	BOOKID =trade['SourceSystemBookId'],
	TRADECCY = 'ZAR',
	SENSITIVITYNAME = riskType,
	SENSTIVITYCONFIGURATIONID = 'SCALAR',
	VALUE = riskValue,
        DATAOBJECT1ID ='',  #TODO     
        DATAOBJECT1TYPE ='',       #TODO
        DATAOBJECT1CURVEID ='',       
        DATAOBJECT1CCY ='',       
        DATAOBJECT1INSTRUMENTTYPE ='',       
        DATAOBJECT1INDEX ='',       
        DATAOBJECT1INSTRUMENTID ='',       
        DATAOBJECT1PROJECTIONID ='',       
        DATAOBJECT1AXIS1 ='',       
        DATAOBJECT1AXIS1PARAM1 ='',       
        DATAOBJECT1AXIS1PARAM2 ='',       
        DATAOBJECT1AXIS1PARAM3 ='',       
        DATAOBJECT1AXIS2 ='',       
        DATAOBJECT1AXIS2PARAM1 ='',       
        DATAOBJECT1AXIS2PARAM2 ='',       
        DATAOBJECT1AXIS2PARAM3 ='',       
        DATAOBJECT1AXIS3 ='',       
        DATAOBJECT1AXIS3PARAM1 ='',       
        DATAOBJECT1AXIS3PARAM2 ='',       
        DATAOBJECT1AXIS3PARAM3 ='',       
        DATAOBJECT2ID ='',       
        DATAOBJECT2TYPE ='',       
        DATAOBJECT2CURVEID ='',       
        DATAOBJECT2CURVECCY ='',       
        DATAOBJECT2INSTRUMENTTYPE ='',       
        DATAOBJECT2INDEX ='',       
        DATAOBJECT2INSTRUMENTID ='',       
        DATAOBJECT2PROJECTIONID ='',       
        DATAOBJECT2AXIS1 ='',       
        DATAOBJECT2AXIS1PARAM1 ='',       
        DATAOBJECT2AXIS1PARAM2 ='',       
        DATAOBJECT2AXIS1PARAM3 ='',       
        DATAOBJECT2AXIS2 ='',       
        DATAOBJECT2AXIS2PARAM1 ='',       
        DATAOBJECT2AXIS2PARAM2 ='',       
        DATAOBJECT2AXIS2PARAM3 ='',       
        DATAOBJECT2AXIS3 ='',       
        DATAOBJECT2AXIS3PARAM1 ='',       
        DATAOBJECT2AXIS3PARAM2 ='',       
        DATAOBJECT2AXIS3PARAM3 ='',       
        DATAOBJECT3ID ='',       
        DATAOBJECT3TYPE ='',       
        DATAOBJECT3CURVEID ='',       
        DATAOBJECT3CURVECCY ='',       
        DATAOBJECT3INSTRUMENTTYPE ='',       
        DATAOBJECT3INDEX ='',       
        DATAOBJECT3INSTRUMENTID ='',       
        DATAOBJECT3PROJECTIONID ='',       
        DATAOBJECT3AXIS1 ='',       
        DATAOBJECT3AXIS1PARAM1 ='',       
        DATAOBJECT3AXIS1PARAM2 ='',       
        DATAOBJECT3AXIS1PARAM3 ='',       
        DATAOBJECT3AXIS2 ='',       
        DATAOBJECT3AXIS2PARAM1 ='',       
        DATAOBJECT3AXIS2PARAM2 ='',       
        DATAOBJECT3AXIS2PARAM3 ='',       
        DATAOBJECT3AXIS3 ='',       
        DATAOBJECT3AXIS3PARAM1 ='',       
        DATAOBJECT3AXIS3PARAM2 ='',       
        DATAOBJECT3AXIS3PARAM3 ='',       
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
            LOGGER.LOG('Processing trade ' + trade)
            #file_data(trade, riskType, riskValue, repday, *rest):
            tradeRow = tradeStatic[trade]           
            trade_id= get_trade_id(tradeRow)
            
            #MTM
            line = file_data(tradeRow, 'MARK_TO_MARKET_VALUE', getPV(trade_id, tradeScalars), repday)            
            if type(line) == REPORT_ENTRY:
                writer.writerow(line._asdict())        
            #FX Delta
            line = file_data(tradeRow, 'FXDELTA', getFXDelta(trade_id, tradeScalars, tradeRow['Ccy1'], tradeRow['Ccy2']), repday)            
            if type(line) == REPORT_ENTRY:
                writer.writerow(line._asdict())        
                
            #Notional
            line = file_data(tradeRow, 'NOTIONAL', float(tradeRow['Nominal1']), repday)            
            if type(line) == REPORT_ENTRY:
                writer.writerow(line._asdict())        
        LOGGER.LOG('Created  output file '  + outFilePath)
        LOGGER.LOG('Completed Successfully.')
            

           

'''----------------------------------------------------------------------------------------------------------
MODULE                  :       FC_CONSTANTS_GENERIC
PROJECT                 :       FX onto Front Arena
PURPOSE                 :       This module retreives and sets the generic variables from the environment
                                variables in Extension Manager.
DEPARTMENT AND DESK     :       All Departments and all Desks.
REQUASTER               :       FX onto Front Arena Project
DEVELOPER               :       BBD
CR NUMBER               :       XXXXXX
-------------------------------------------------------------------------------------------------------------
'''
'''----------------------------------------------------------------------------------------------------------
Class containing all the generic properties for the ATS.
----------------------------------------------------------------------------------------------------------'''
class FC_CONSTANTS_GENERIC(object):
    def __init__(self):
        self._KEY = 'key'
        self._KEY_TYPE = 'keyType'
        self._Response = 'RESPONSE'
        self._BatchEnd = 'BATCH_END'
        self._TRADE_NUMBER = 'tradeNumber'
        self._TRADE_NUMBERS = 'tradeNumbers'
        self._CURRENCY = 'currency'
        self._CUSTOM_LABEL = 'customLabel'
        self._VECTOR = 'Vector'
        self._COLUMN_SETTINGS = 'columnsettings'
        self._F_DATE_FORMATTER = 'FDateFormatter'
        self._F_DATE_TIME_FORMATTER = 'FDateTimeFormatter'
        self._F_NUM_FORMATTER = 'FNumFormatter'
        self._NO_METHOD_ = 'no Method '
        self._F_SYMBOL = 'FSymbol'
        self._PORTFOLIO_CURRENCY = 'Portfolio Currency'
        self._SETTLEMENT = 'settlement'
        self._SALES_CREDIT = 'salesCredit'
        self._SALES_CREDITS = 'salesCredits'
        self._MONEYFLOW = 'moneyflow'
        self._MONEYFLOWS = 'moneyflows'
        self._UNDERLYING_INSTRUMENTS = 'underlyingInstruments'
        self._LEG = 'leg'
        self._INSTRUMENT_JSON = 'instrument'
        self._INSTRUMENT = 'Instrument'
        self._PORTFOLIO = 'Portfolio'
        self._LEGS = 'legs'
        self._SCALAR = 'scalar'
        self._STATIC = 'static'
        self._SERIALIZATION_TYPE = 'serializationType'
        self._TRADE = 'trade'
        self._TRADE_DATA = 'tradeData'
        self._SETTLEMENT_DATA = 'settlementData'
        self._UPDAT_USRNBR_USERID = 'UPDAT_USRNBR.USERID'
        self._UPDAT_TIME = 'UPDAT_TIME'
        self._SEQNBR = 'SEQNBR'
        self._INSID = 'INSID'
        self._INSADDR = 'INSADDR'
        self._TRDNBR = 'TRDNBR'
        self._REQUEST = 'REQUEST'
        self._REQUEST_RT = 'REQUEST_RT'
        self._SINGLE_SETTLEMENT = 'SINGLE_SETTLEMENT'
        self._INSTRUMENT_SENSITIVITIES = 'INSTRUMENT_SENSITIVITIES'
        self._PORTFOLIO_SENSITIVITIES  = 'PORTFOLIO_SENSITIVITIES'
        self._SETTLEMENT_UPPER = 'SETTLEMENT'
        self._INSTRUMENT_TRADES = 'INSTRUMENT_TRADES'
        self._INSTRUMENT_UPPER = 'INSTRUMENT'
        self._SINGLE_TRADE = 'SINGLE_TRADE'
        self._TRADE_UPPER = 'TRADE'
        self._REAL_TIME__S = 'REAL_TIME_%s'
        self._TYPE = 'TYPE'
        self._TXNBR = 'TXNBR'
        self._SOURCE = 'SOURCE'
        self._FC_TRADE_SCALAR = 'FC_TRADE_SCALAR'
        self._FC_TRADE_STATIC = 'FC_TRADE_STATIC'
        self._FC_TRADE_INSTRUMENT = 'FC_TRADE_INSTRUMENT'
        self._FC_SETTLEMENT_SCALAR = 'FC_SETTLEMENT_SCALAR'
        self._FRONTCACHE_CREATE_BATCH_TRACKER = 'FrontCache.CreateBatchTracker'
        self._FRONT_CACHE_UPDATE_BATCH_TRACKER_END = 'FrontCache.UpdateBatchTrackerEnd'
        self._FRONTCACHE_UPDATE_BATCH_REQUEST_END = 'FrontCache.UpdateBatchRequestEnd'
        self._FC_SETTLEMENT_DATA = 'FC_SETTLEMENT_DATA'
        self._DATA = 'DATA'
        self._AMBA_TXNBR = 'AMBA_TXNBR'
        self._BATCH_ID = 'BATCH_ID'
        self._IS_EOD = 'IS_EOD'
        self._IS_DATE_TODAY = 'IS_DATE_TODAY'
        self._REPORT_DATE = 'REPORT_DATE'
        self._REQUEST_DATETIME = 'REQUEST_DATETIME'
        self._REQUEST_EVENT_TYPE = 'REQUEST_EVENT_TYPE'
        self._REQUEST_ID = 'REQUEST_ID'
        self._REQUEST_SOURCE = 'REQUEST_SOURCE'
        self._REQUEST_TYPE = 'REQUEST_TYPE'
        self._REQUEST_USER_ID = 'REQUEST_USER_ID'
        self._SCOPE_NAME = 'SCOPE_NAME'
        self._SCOPE_NUMBER = 'SCOPE_NUMBER'
        self._SENDER_SUBJECT = 'SENDER_SUBJECT'
        self._TOPIC = 'TOPIC'
        self._REQUEST_S = 'REQUEST_%s'
        self._REQUEST_BATCH_NO = 'REQUEST_BATCH_NO'
        self._REQUEST_BATCH_START_INDEX = 'REQUEST_BATCH_START_INDEX'
        self._REQUEST_BATCH_END_INDEX = 'REQUEST_BATCH_END_INDEX'
        self._REQUEST_BATCH_TRADE_COUNT = 'REQUEST_BATCH_TRADE_COUNT'
        self._REQUEST_COLLECTION_TRACKER_ID = 'REQUEST_COLLECTION_TRACKER_ID'
        self._REQUEST_COLLECTION_PRIMARY_KEYS = 'REQUEST_COLLECTION_PRIMARY_KEYS'
        self._EXPECTED_OBJECT_COUNT = 'EXPECTED_OBJECT_COUNT'
        self._RESPONSE_TYPE = 'RESPONSE_TYPE'
        self._CRITICAL = 'CRITICAL'
        self._MEDIUM = 'MEDIUM'
        self._DISCONNECT = 'Disconnect'
        self._MESSAGE = 'Message'
        self._FC_ERROR_MESSAGE = 'FC_ERROR_MESSAGE'
        self._RUNNING = 'RUNNING'
        self._WINDOWS = 'Windows'
        self._LINUX = 'Linux'
        self._SHUTTING_DOWN = 'SHUTTING DOWN'
        self._F_TRADE_SHEET = 'FTradeSheet'
        self._FPORTFOLIOSHEET = 'FPortfolioSheet'
        self._FVERTICALPORTFOLIOSHEET = 'FVerticalPortfolioSheet'
        self._F_MONEYFLOW_SHEET = 'FMoneyFlowSheet'
        self._F_SETTLEMENT_SHEET = 'FSettlementSheet'
        self._PORTFOLIO_TRADES = 'PORTFOLIO_TRADES'
        self._SETTLEMENT_INFO = 'settlementInfo'
        self._SETTLEMENT_BUILD_TIME = 'settlementBuildTime'
        self._STATIC_COUNT = 'staticCount'
        self._SCALAR_COUNT = 'scalarCount'
        self._SETTLEMENT_ERRORS = 'settlementErrors'
        self._TRADE_DOMAIN = 'tradeDomain'
        self._TRADE_INFO = 'tradeInfo'
        self._TRADE_BUILD_TIME = 'tradeBuildTime'
        self._INSTRUMENT_COUNT = 'instrumentCount'
        self._LEG_COUNT = 'legCount'
        self._UNDERLYINGINSTRUMENT_COUNT = 'underlyingInstrumentCount'
        self._MONEY_FLOW_COUNT = 'moneyflowCount'
        self._SALES_CREDIT_COUNT = 'salesCreditCount'
        self._PARENT_INSTRUMENT_ADDRESS = 'parentInstrumentAddress'
        self._REQUEST_BATCH_COUNT = 'REQUEST_BATCH_COUNT'
        self._S_START = '%s_START'
        self._FC_TRADE_MONEYFLOW = 'FC_TRADE_MONEYFLOW'
        self._FCASHFLOW = 'FCashFlow'
        self._FRESET = 'FReset'
        self._FMONEYFLOW = 'FMoneyFlow'
        self._FTRADE = 'FTrade'
        self._SALES_PERSON = 'salesPerson'
        self._STANDARD_SALES_CREDIT = 'standardSalesCredit'
        self._VALUEADDCREDITS = 'ValueAddCredits'
        self._TOTAL_VALUE_ADD_SALES_CREDIT = 'totalValueAddSalesCredit'
        self._SALESCREDITSUBTEAM1 = 'SalesCreditSubTeam1'
        self._SALESCREDITSUBTEAM = 'salesCreditSubTeam'
        self._SALES_PERSON_S = 'Sales_Person%s'
        self._SALES_CREDIT_S = 'Sales_Credit%s'
        self._SALES_PERSON = 'salesPerson'
        self._STANDARD_SALES_CREDIT = 'standardSalesCredit'
        self._VALUE_ADD_CREDITS_S = 'ValueAddCredits%s'
        self._TOTAL_VALUE_ADD_SALES_CREDIT = 'totalValueAddSalesCredit'
        self._SALES_CREDIT_SUB_TEAM_S = 'SalesCreditSubTeam%s'
        self._SALES_CREDIT_SUB_TEAM = 'salesCreditSubTeam'
        self._SALES_PERSON_NAME = 'salesPersonName'
        self._STANDARD_SALES_CREDIT = 'standardSalesCredit'
        self._TOTAL_VALUE_ADD_SALES_CREDIT = 'totalValueAddSalesCredit'
        self._SALES_CREDIT_SUB_TEAM_NAME = 'salesCreditSubTeamName'
        self._CALCULATION_RESULTS = 'calculationResults'
        self._CALCULATION_ERRORS = 'calculationErrors'
        self._FC_TRADE_LEG = 'FC_TRADE_LEG'
        self._FTRADEROW = 'FTradeRow'
        self._FC_DYNAMIC_DATA = 'FC_DYNAMIC_DATA'
        self._FC_DYNAMIC_SENSITIVITY = 'FC_DYNAMIC_SENSITIVITY'
        self._FC_DYNAMIC_INS_SENSITIVITY = 'FC_DYNAMIC_INS_SENSITIVITY'
        self._FC_OPERATIONS_DATA = 'FC_OPERATIONS_DATA'
        self._FC_UNDERLYING_INSTRUMENT = 'FC_UNDERLYING_INSTRUMENT'
        self._CONTAINER_NAME = 'Sensitivity'
        self._TEMPLATE_NAME = 'FCSVBasic'
        self._PORTFOLIO_PROFIT_LOSS_START_DATE = 'Portfolio Profit Loss Start Date'
        self._CUSTOM_DATE = 'Custom Date'
        self._PORTFOLIO_PROFIT_LOSS_START_DATE_CUSTOM = 'Portfolio Profit Loss Start Date Custom'
        self._PORTFOLIO_PROFIT_LOSS_END_DATE = 'Portfolio Profit Loss End Date'
        self._PORTFOLIO_PROFIT_LOSS_END_DATE_CUSTOM = 'Portfolio Profit Loss End Date Custom'
        self._VALUATION_DATE = 'Valuation Date'
        self._PORTFOLIO_CURRENCY = 'Portfolio Currency'
        self._FRONTCACHE_CREATE_REQUEST_COLLECTION_TRACKER = 'FrontCache.CreateRequestCollectionTracker'
        self._FRONTCACHE_UPDATE_REQUEST_COLLECTION_TRACKER_END = 'FrontCache.UpdateRequestCollectionTrackerEnd'
        self._FRONTCACHE_UPDATE_REQUEST_COLLECTION_TRACKER_START = 'FrontCache.UpdateRequestCollectionTrackerStart'
        self._FRONTCACHE_CREATE_REQUEST_ENTITY = 'FrontCache.CreateRequestEntity'
        self._FRONTCACHE_GET_INDEPENDENT_TRADE_COUNT = 'FrontCache.GetPortFolioTradeCount'
        self._FRONTCACHE_RECORD_FAILED_SELECTION = 'FrontCache.RecordFailedSelection'
        self._FRONTCACHE_CREATE_SETTLEMENT_ENTITY = 'FrontCache.CreateSettlementEntity'
        self._FRONTCACHE_CREATE_SENSITIVITY_ENTITY = 'FrontCache.CreateSensitivityEntity'
        self._FRONTCACHE_UPDATE_REQUEST_TRACKER_START = 'FrontCache.UpdateRequestStart'
        self._FRONTCACHE_UPDATE_REQUEST_TRACKER_END = 'FrontCache.UpdateRequestEnd'
        self._FRONTCACHE_GET_REQUEST_TRACKER_RESULT = 'FrontCache.GetRequestTrackerResult'
        self._FRONTCACHE_CREATE_TRADE_ENTITY = 'FrontCache.CreateTradeEntity'
        self._FRONTCACHE_GET_BOOK_NAMES = 'SELECT * FROM FrontCache.GetBookNames() ORDER BY 3 DESC'
        self._FRONTCACHE_GET_INSTRUMENT_NAMES = 'SELECT * FROM FrontCache.GetInstrumentNames() ORDER BY 4 DESC'
        self._FRONTCACHE_SEND_CONFIRMATION_TRACKER_RESULT = 'FrontCache.SendConfirmationTrackerResult'
        self._BUILD_CONTROL_MEASURES = 'BUILD_CONTROL_MEASURES'
        self._REPLAY = 'REPLAY'
        self._FRONTCACHE_CREATE_TRADE_ENTITIES_COLLECTION = 'FrontCache.CreateTradeEntitiesCollection'
        self._GET_SELECTION_DIFFERENCES = 'FrontCache.GetSelectionDifferenceByBatchIdAndReportDate'
        self._VECTOR_CALCULATION_S = 'Vector_Calculation%s'
        self._CASH_PER_CURRENCY = 'Cash_Per_Currency'
        self._ZAR_SWAP_CURVE_CALIBRATION_BOOKS = [1027, 1575, 2465, 2467, 9545, 9546, 12519, 12652, 12672, 12890, 14744, 7398]


    @property
    def ZAR_SWAP_CURVE_CALIBRATION_BOOKS(self):
        return self._ZAR_SWAP_CURVE_CALIBRATION_BOOKS
        
    @property
    def GET_SELECTION_DIFFERENCES(self):
        return self._GET_SELECTION_DIFFERENCES

    @property
    def FRONTCACHE_CREATE_TRADE_ENTITIES_COLLECTION(self):
        return self._FRONTCACHE_CREATE_TRADE_ENTITIES_COLLECTION        
        
    @property
    def BUILD_CONTROL_MEASURES(self):
        return self._BUILD_CONTROL_MEASURES

    @property
    def REPLAY(self):
        return self._REPLAY

    @property
    def FRONTCACHE_SEND_CONFIRMATION_TRACKER_RESULT(self):
        return self._FRONTCACHE_SEND_CONFIRMATION_TRACKER_RESULT
        
    @property
    def FRONTCACHE_CREATE_REQUEST_COLLECTION_TRACKER(self):
        return self._FRONTCACHE_CREATE_REQUEST_COLLECTION_TRACKER

    @property
    def FRONTCACHE_UPDATE_REQUEST_COLLECTION_TRACKER_END(self):
        return self._FRONTCACHE_UPDATE_REQUEST_COLLECTION_TRACKER_END
        
    @property
    def FRONTCACHE_UPDATE_REQUEST_COLLECTION_TRACKER_START(self):
        return self._FRONTCACHE_UPDATE_REQUEST_COLLECTION_TRACKER_START

    @property
    def FRONTCACHE_CREATE_REQUEST_ENTITY(self):
        return self._FRONTCACHE_CREATE_REQUEST_ENTITY

    @property
    def FRONTCACHE_CREATE_SETTLEMENT_ENTITY(self):
        return self._FRONTCACHE_CREATE_SETTLEMENT_ENTITY

    @property
    def FRONTCACHE_GET_INDEPENDENT_TRADE_COUNT(self):
        return self._FRONTCACHE_GET_INDEPENDENT_TRADE_COUNT

    @property
    def FRONTCACHE_RECORD_FAILED_SELECTION(self):
        return self._FRONTCACHE_RECORD_FAILED_SELECTION

    @property
    def FRONTCACHE_CREATE_SENSITIVITY_ENTITY(self):
        return self._FRONTCACHE_CREATE_SENSITIVITY_ENTITY

    @property
    def FRONTCACHE_UPDATE_REQUEST_TRACKER_START(self):
        return self._FRONTCACHE_UPDATE_REQUEST_TRACKER_START

    @property
    def FRONTCACHE_UPDATE_REQUEST_TRACKER_END(self):
        return self._FRONTCACHE_UPDATE_REQUEST_TRACKER_END

    @property
    def FRONTCACHE_GET_REQUEST_TRACKER_RESULT(self):
        return self._FRONTCACHE_GET_REQUEST_TRACKER_RESULT

    @property
    def FRONTCACHE_CREATE_TRADE_ENTITY(self):
        return self._FRONTCACHE_CREATE_TRADE_ENTITY
        
    @property
    def FRONTCACHE_GET_BOOK_NAMES(self):
        return self._FRONTCACHE_GET_BOOK_NAMES

    @property
    def FRONTCACHE_GET_INSTRUMENT_NAMES(self):
        return self._FRONTCACHE_GET_INSTRUMENT_NAMES

    @property
    def FC_DYNAMIC_DATA(self):
        return self._FC_DYNAMIC_DATA

    @property
    def FC_DYNAMIC_SENSITIVITY(self):
        return self._FC_DYNAMIC_SENSITIVITY

    @property
    def FC_DYNAMIC_INS_SENSITIVITY(self):
        return self._FC_DYNAMIC_INS_SENSITIVITY

    @property
    def FC_OPERATIONS_DATA(self):
        return self._FC_OPERATIONS_DATA

    @property
    def FC_UNDERLYING_INSTRUMENT(self):
        return self._FC_UNDERLYING_INSTRUMENT

    @property
    def CONTAINER_NAME(self):
        return self._CONTAINER_NAME

    @property
    def TEMPLATE_NAME(self):
        return self._TEMPLATE_NAME

    @property
    def PORTFOLIO_PROFIT_LOSS_START_DATE(self):
        return self._PORTFOLIO_PROFIT_LOSS_START_DATE

    @property
    def CUSTOM_DATE(self):
        return self._CUSTOM_DATE

    @property
    def PORTFOLIO_PROFIT_LOSS_START_DATE_CUSTOM(self):
        return self._PORTFOLIO_PROFIT_LOSS_START_DATE_CUSTOM

    @property
    def PORTFOLIO_PROFIT_LOSS_END_DATE(self):
        return self._PORTFOLIO_PROFIT_LOSS_END_DATE

    @property
    def PORTFOLIO_PROFIT_LOSS_END_DATE_CUSTOM(self):
        return self._PORTFOLIO_PROFIT_LOSS_END_DATE_CUSTOM

    @property
    def VALUATION_DATE(self):
        return self._VALUATION_DATE

    @property
    def PORTFOLIO_CURRENCY(self):
        return self._PORTFOLIO_CURRENCY

    @property
    def FC_TRADE_LEG(self):
        return self._FC_TRADE_LEG

    @property
    def FTRADEROW(self):
        return self._FTRADEROW

    @property
    def SALES_PERSON(self):
        return self._SALES_PERSON

    @property
    def STANDARD_SALES_CREDIT(self):
        return self._STANDARD_SALES_CREDIT

    @property
    def VALUEADDCREDITS(self):
        return self._VALUEADDCREDITS

    @property
    def TOTAL_VALUE_ADD_SALES_CREDIT(self):
        return self._TOTAL_VALUE_ADD_SALES_CREDIT

    @property
    def SALESCREDITSUBTEAM1(self):
        return self._SALESCREDITSUBTEAM1

    @property
    def SALESCREDITSUBTEAM(self):
        return self._SALESCREDITSUBTEAM

    @property
    def SALES_PERSON_S(self):
        return self._SALES_PERSON_S

    @property
    def SALES_CREDIT_S(self):
        return self._SALES_CREDIT_S

    @property
    def SALES_PERSON(self):
        return self._SALES_PERSON

    @property
    def STANDARD_SALES_CREDIT(self):
        return self._STANDARD_SALES_CREDIT

    @property
    def VALUE_ADD_CREDITS_S(self):
        return self._VALUE_ADD_CREDITS_S

    @property
    def TOTAL_VALUE_ADD_SALES_CREDIT(self):
        return self._TOTAL_VALUE_ADD_SALES_CREDIT

    @property
    def SALES_CREDIT_SUB_TEAM_S(self):
        return self._SALES_CREDIT_SUB_TEAM_S

    @property
    def SALES_CREDIT_SUB_TEAM(self):
        return self._SALES_CREDIT_SUB_TEAM

    @property
    def SALES_PERSON_NAME(self):
        return self._SALES_PERSON_NAME

    @property
    def STANDARD_SALES_CREDIT(self):
        return self._STANDARD_SALES_CREDIT

    @property
    def TOTAL_VALUE_ADD_SALES_CREDIT(self):
        return self._TOTAL_VALUE_ADD_SALES_CREDIT

    @property
    def SALES_CREDIT_SUB_TEAM_NAME(self):
        return self._SALES_CREDIT_SUB_TEAM_NAME

    @property
    def CALCULATION_RESULTS(self):
        return self._CALCULATION_RESULTS

    @property
    def CALCULATION_ERRORS(self):
        return self._CALCULATION_ERRORS

    @property
    def FC_TRADE_MONEYFLOW(self):
        return self._FC_TRADE_MONEYFLOW

    @property
    def FCASHFLOW(self):
        return self._FCASHFLOW

    @property
    def FRESET(self):
        return self._FRESET

    @property
    def FMONEYFLOW(self):
        return self._FMONEYFLOW

    @property
    def FTRADE(self):
        return self._FTRADE

    @property
    def S_START(self):
        return self._S_START

    @property
    def REQUEST_BATCH_COUNT(self):
        return self._REQUEST_BATCH_COUNT

    @property
    def TRADE_INFO(self):
        return self._TRADE_INFO

    @property
    def TRADE_BUILD_TIME(self):
        return self._TRADE_BUILD_TIME

    @property
    def INSTRUMENT_COUNT(self):
        return self._INSTRUMENT_COUNT

    @property
    def LEG_COUNT(self):
        return self._LEG_COUNT

    @property
    def UNDERLYINGINSTRUMENT_COUNT(self):
        return self._UNDERLYINGINSTRUMENT_COUNT

    @property
    def MONEY_FLOW_COUNT(self):
        return self._MONEY_FLOW_COUNT

    @property
    def SALES_CREDIT_COUNT(self):
        return self._SALES_CREDIT_COUNT

    @property
    def PARENT_INSTRUMENT_ADDRESS(self):
        return self._PARENT_INSTRUMENT_ADDRESS

    @property
    def PORTFOLIO_TRADES(self):
        return self._PORTFOLIO_TRADES

    @property
    def SETTLEMENT_INFO(self):
        return self._SETTLEMENT_INFO

    @property
    def SETTLEMENT_BUILD_TIME(self):
        return self._SETTLEMENT_BUILD_TIME

    @property
    def STATIC_COUNT(self):
        return self._STATIC_COUNT

    @property
    def SCALAR_COUNT(self):
        return self._SCALAR_COUNT

    @property
    def SETTLEMENT_ERRORS(self):
        return self._SETTLEMENT_ERRORS

    @property
    def TRADE_DOMAIN(self):
        return self._TRADE_DOMAIN

    @property
    def F_TRADE_SHEET(self):
        return self._F_TRADE_SHEET

    @property
    def FPORTFOLIOSHEET(self):
        return self._FPORTFOLIOSHEET

    @property
    def FVERTICALPORTFOLIOSHEET(self):
        return self._FVERTICALPORTFOLIOSHEET

    @property
    def F_MONEYFLOW_SHEET(self):
        return self._F_MONEYFLOW_SHEET

    @property
    def F_SETTLEMENT_SHEET(self):
        return self._F_SETTLEMENT_SHEET

    @property
    def DISCONNECT(self):
        return self._DISCONNECT

    @property
    def MESSAGE(self):
        return self._MESSAGE

    @property
    def FC_ERROR_MESSAGE(self):
        return self._FC_ERROR_MESSAGE

    @property
    def RUNNING(self):
        return self._RUNNING

    @property
    def WINDOWS(self):
        return self._WINDOWS

    @property
    def LINUX(self):
        return self._LINUX

    @property
    def SHUTTING_DOWN(self):
        return self._SHUTTING_DOWN

    @property
    def EXPECTED_OBJECT_COUNT(self):
        return self._EXPECTED_OBJECT_COUNT

    @property
    def RESPONSE_TYPE(self):
        return self._RESPONSE_TYPE

    @property
    def KEY(self):
        return self._KEY

    @property
    def KEY_TYPE(self):
        return self._KEY_TYPE

    @property
    def CRITICAL(self):
        return self._CRITICAL

    @property
    def MEDIUM(self):
        return self._MEDIUM

    @property
    def FC_TRADE_INSTRUMENT(self):
        return self._FC_TRADE_INSTRUMENT

    @property
    def FC_TRADE_STATIC(self):
        return self._FC_TRADE_STATIC

    @property
    def FC_TRADE_SCALAR(self):
        return self._FC_TRADE_SCALAR
        
    @property
    def Response(self):
        return self._Response

    @property
    def BatchEnd(self):
        return self._BatchEnd
        
    @property
    def TRADE_NUMBER(self):
        return self._TRADE_NUMBER
    
    @property
    def TRADE_NUMBERS(self):
        return self._TRADE_NUMBERS
    
    @property
    def CURRENCY(self):
        return self._CURRENCY
    
    @property
    def CUSTOM_LABEL(self):
        return self._CUSTOM_LABEL
    
    @property
    def VECTOR(self):
        return self._VECTOR
    
    @property
    def COLUMN_SETTINGS(self):
        return self._COLUMN_SETTINGS
    
    @property
    def F_DATE_FORMATTER(self):
        return self._F_DATE_FORMATTER
    
    @property
    def F_DATE_TIME_FORMATTER(self):
        return self._F_DATE_TIME_FORMATTER
    
    @property
    def F_NUM_FORMATTER(self):
        return self._F_NUM_FORMATTER
        
    @property
    def NO_METHOD_(self):
        return self._NO_METHOD_
        
    @property    
    def F_SYMBOL(self):       
        return self._F_SYMBOL
        
    @property    
    def PORTFOLIO_CURRENCY(self):    
        return self._PORTFOLIO_CURRENCY
        
    @property    
    def SETTLEMENT(self):    
        return self._SETTLEMENT
        
    @property    
    def SALES_CREDIT(self):    
        return self._SALES_CREDIT
        
    @property    
    def SALES_CREDITS(self):    
        return self._SALES_CREDITS
        
    @property    
    def MONEYFLOW(self):    
        return self._MONEYFLOW
        
    @property    
    def MONEYFLOWS(self):    
        return self._MONEYFLOWS
        
    @property    
    def UNDERLYING_INSTRUMENTS(self):        
        return self._UNDERLYING_INSTRUMENTS
        
    @property    
    def LEG(self):    
        return self._LEG
        
    @property    
    def INSTRUMENT_JSON(self):    
        return self._INSTRUMENT_JSON

    @property    
    def INSTRUMENT(self):    
        return self._INSTRUMENT
        
    @property    
    def PORTFOLIO(self):    
        return self._PORTFOLIO
        
    @property   
    def LEGS(self):    
        return self._LEGS
        
    @property   
    def SCALAR(self):    
        return self._SCALAR
        
    @property   
    def STATIC(self):    
        return self._STATIC
        
    @property   
    def SERIALIZATION_TYPE(self):    
        return self._SERIALIZATION_TYPE
        
    @property   
    def TRADE(self):    
        return self._TRADE
        
    @property   
    def TRADE_DATA(self):    
        return self._TRADE_DATA
        
    @property   
    def SETTLEMENT_DATA(self):    
        return self._SETTLEMENT_DATA
        
    @property   
    def UPDAT_USRNBR_USERID(self):    
        return self._UPDAT_USRNBR_USERID
        
    @property   
    def UPDAT_TIME(self):    
        return self._UPDAT_TIME
        
    @property   
    def SEQNBR(self):    
        return self._SEQNBR
        
    @property   
    def INSID(self):    
        return self._INSID
        
    @property   
    def INSADDR(self):    
        return self._INSADDR
        
    @property   
    def TRDNBR(self):    
        return self._TRDNBR
        
    @property   
    def REQUEST(self):    
        return self._REQUEST
        
    @property   
    def REQUEST_RT(self):    
        return self._REQUEST_RT
        
    @property   
    def SINGLE_SETTLEMENT(self):    
        return self._SINGLE_SETTLEMENT
        
    @property   
    def INSTRUMENT_SENSITIVITIES(self):    
        return self._INSTRUMENT_SENSITIVITIES       
        
    @property   
    def PORTFOLIO_SENSITIVITIES(self):    
        return self._PORTFOLIO_SENSITIVITIES
        
    @property   
    def SETTLEMENT_UPPER(self):    
        return self._SETTLEMENT_UPPER
        
    @property    
    def INSTRUMENT_TRADES(self):        
        return self._INSTRUMENT_TRADES
        
    @property    
    def INSTRUMENT_UPPER(self):    
        return self._INSTRUMENT_UPPER
        
    @property    
    def SINGLE_TRADE(self):            
        return self._SINGLE_TRADE
        
    @property    
    def TRADE_UPPER(self):    
        return self._TRADE_UPPER
        
    @property    
    def REAL_TIME_S(self):    
        return self._REAL_TIME__S
        
    @property    
    def TYPE(self):    
        return self._TYPE
        
    @property   
    def TXNBR(self):    
        return self._TXNBR
        
    @property    
    def SOURCE(self):   
        return self._SOURCE

    @property
    def FC_SETTLEMENT_SCALAR(self):
        return self._FC_SETTLEMENT_SCALAR

    @property
    def FRONTCACHE_CREATE_BATCH_TRACKER(self):
	    return self._FRONTCACHE_CREATE_BATCH_TRACKER

    @property
    def FRONT_CACHE_UPDATE_BATCH_TRACKER_END(self):
	    return self._FRONT_CACHE_UPDATE_BATCH_TRACKER_END

    @property
    def FRONTCACHE_UPDATE_BATCH_REQUEST_END(self):
	    return self._FRONTCACHE_UPDATE_BATCH_REQUEST_END

    @property
    def FC_SETTLEMENT_DATA(self):
        return self._FC_SETTLEMENT_DATA

    @property
    def FC_SENSITIVITY_VPS(self):
        return self._FC_SENSITIVITY_VPS
        
    @property
    def FC_SENSITIVITY_PS(self):
        return self._FC_SENSITIVITY_PS

    @property
    def DATA(self):
        return self._DATA

    @property
    def AMBA_TXNBR(self):
        return self._AMBA_TXNBR

    @property
    def BATCH_ID(self):
        return self._BATCH_ID

    @property
    def IS_EOD(self):
        return self._IS_EOD

    @property
    def IS_DATE_TODAY(self):
        return self._IS_DATE_TODAY

    @property
    def REPORT_DATE(self):
        return self._REPORT_DATE

    @property
    def REQUEST_DATETIME(self):
        return self._REQUEST_DATETIME

    @property
    def REQUEST_EVENT_TYPE(self):
        return self._REQUEST_EVENT_TYPE

    @property
    def REQUEST_ID(self):
        return self._REQUEST_ID

    @property
    def REQUEST_SOURCE(self):
        return self._REQUEST_SOURCE

    @property
    def REQUEST_TYPE(self):
        return self._REQUEST_TYPE

    @property
    def REQUEST_USER_ID(self):
        return self._REQUEST_USER_ID

    @property
    def SCOPE_NAME(self):
        return self._SCOPE_NAME

    @property
    def SCOPE_NUMBER(self):
        return self._SCOPE_NUMBER

    @property
    def SENDER_SUBJECT(self):
        return self._SENDER_SUBJECT        

    @property
    def TOPIC(self):
        return self._TOPIC

    @property
    def REQUEST_S(self):
        return self._REQUEST_S

    @property
    def REQUEST_BATCH_NO(self):
        return self._REQUEST_BATCH_NO

    @property
    def REQUEST_BATCH_NO(self):
        return self._REQUEST_BATCH_NO

    @property
    def REQUEST_BATCH_START_INDEX(self):
        return self._REQUEST_BATCH_START_INDEX

    @property
    def REQUEST_BATCH_END_INDEX(self):
        return self._REQUEST_BATCH_END_INDEX

    @property
    def REQUEST_BATCH_TRADE_COUNT(self):
        return self._REQUEST_BATCH_TRADE_COUNT

    @property
    def REQUEST_COLLECTION_TRACKER_ID(self):
        return self._REQUEST_COLLECTION_TRACKER_ID

    @property
    def REQUEST_COLLECTION_PRIMARY_KEYS(self):
        return self._REQUEST_COLLECTION_PRIMARY_KEYS

    @property
    def VECTOR_CALCULATION_S(self):
        return self._VECTOR_CALCULATION_S

    @property
    def CASH_PER_CURRENCY(self):
        return self._CASH_PER_CURRENCY

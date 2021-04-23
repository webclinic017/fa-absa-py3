import acm
import FSettlementParameters
import FConfirmationParameters
import FOperationsUtils as Utils
from FSettlementCorrectTradeRecaller import FSettlementCorrectTradeRecaller
import FSettlementCreatorSingleton as Singletons
import query_folder_result_analyzer
from at_logging import getLogger

logger = getLogger(__name__)

def is_satisfying_query_folders(fobj, query_folder_names, prevention_queries=False, show_query_results=False):
    all_passed = True
    for each in query_folder_names:
        try:
            query_satisfied = acm.FStoredASQLQuery[each].Query().IsSatisfiedBy(fobj)
            if prevention_queries:
                if query_satisfied:
                    all_passed = False
                    #Since prevention queries are for settlement or confirmation this is a specific code for them
                    try:
                        logger.warn("\t%s of type %s and amount %s is satisfying prevention query folder %s and it won't be created" % (fobj.ClassName(), str(fobj.Type()), str(fobj.Amount()), str(each)))
                    except Exception:
                        logger.warn("\t%s %s is satisfying prevention query folder %s and it won't be created" % (fobj.ClassName(), str(fobj.Oid()), str(each)))
                    if show_query_results:
                        logger.info("\t%s %s %s" % (fobj.ClassName(), str(fobj.Oid()), str(each)))
                        query_folder_result_analyzer.analyze_query_result_for(each, fobj)
            else:
                if not query_satisfied:
                    all_passed = False
                    logger.warn("\t%s %s is not satisfying query folder %s" % (fobj.ClassName(), str(fobj.Oid()), str(each)))
                    if show_query_results:
                        logger.info("\t%s %s %s" % (fobj.ClassName(), str(fobj.Oid()), str(each)))
                        query_folder_result_analyzer.analyze_query_result_for(each, fobj)                
        except Exception, e:
            print 'Exception for ', each, str(e)
    return all_passed

'''def get_all_settlements(trade):
    calendar = trade.Currency().Calendar()
    startDate = AdjustDateToday(calendar, -SettlementParams.maximumDaysBack)
    endDate = SettlementUtils.INFINITE_NUMBER_OF_DAYS
    if trade.Instrument().InsType() != InsType.FUTURE_FORWARD:
        endDate = AdjustDateToday(calendar, SettlementParams.maximumDaysForward)
    return trade.GenerateSettlements(startDate, endDate)'''
    
#creator = SettlementCreator()
#print dir(creator)
def get_settlements_to_be_created_for_trade(trade):
    settlements = []
    creator = Singletons.GetSettlementCreator()
    all_settlements_for_trade = creator._SettlementCreator__GetSettlements(trade)
    settlementCorrectTradeRecaller = FSettlementCorrectTradeRecaller()
    sett_will_be_created = True
    for settlementForTrade in all_settlements_for_trade:
        sett = creator._SettlementCreator__CreateSettlement(settlementForTrade, settlementCorrectTradeRecaller)
        if sett:
            settlements.append(sett)
    return settlements


'''def will_settlements_be_created_for_trade(trade):
    creator = Singletons.GetSettlementCreator()
    all_settlements_for_trade = creator._SettlementCreator__GetSettlements(trade)
    settlementCorrectTradeRecaller = FSettlementCorrectTradeRecaller()
    sett_will_be_created = True
    for settlementForTrade in all_settlements_for_trade:
        settlement = creator._SettlementCreator__CreateSettlement(settlementForTrade, settlementCorrectTradeRecaller)
        if settlement:
            sett_will_be_created = is_satisfying_query_folders(settlement, SettlementParams.preventSettlementCreationQueries, True)
    return sett_will_be_created'''


def analyze_settlements_for_trade(trade, show_query_results=False):
    settlements_for_trade = get_settlements_to_be_created_for_trade(trade)
    settlements_that_will_be_created = []
    for each_settlement in settlements_for_trade:
        settlement_will_be_created = is_satisfying_query_folders(each_settlement, FSettlementParameters.preventSettlementCreationQueries, True, show_query_results)
        if settlement_will_be_created:
            settlements_that_will_be_created.append((each_settlement.Type(), each_settlement.Amount()))

    for sett_type, amount in settlements_that_will_be_created:
        logger.info('\tFSettlement of type %s and amount %s should be created' % (str(sett_type), str(amount)))

def analyze_trade_for_operations(trade, check_confirmations=True, check_settlements=True, show_query_results=False ):
    logger.info('*'*40 + 'Trade '+ str(trade.Oid())+ '*'*40)
    if check_confirmations:
        logger.info('Checking if confirmations should be created for trade %s' % str(trade.Oid()))
        if is_satisfying_query_folders(trade, FConfirmationParameters.tradeFilterQueries, False, show_query_results):
            logger.info('\t%s %s is passing all trade filters from FConfirmationParameters'% (trade.ClassName(), str(trade.Oid())) )
   

    if check_settlements:
        logger.info('Checking if settlements should be created for trade %s' % str(trade.Oid()))
        if is_satisfying_query_folders(trade, FSettlementParameters.tradeFilterQueries, False, show_query_results):
            logger.info('\t%s %s is passing all trade filters from FSettlementParameters'% (trade.ClassName(), str(trade.Oid())) )
            analyze_settlements_for_trade(trade, show_query_results)

def create_trade_query():
    query = acm.CreateFASQLQuery(acm.FTrade, 'AND')
    op = query.AddOpNode('OR')
    op.AddAttrNode('Oid', 'EQUAL', None)
    op2 = query.AddOpNode('OR')
    op2.AddAttrNode('Status', 'EQUAL', None)
    return query

def validate_selection(seq_nbr, field_values):
    if not (field_values[-2] == 'true' or field_values[-3] == 'true'):
        logger.error('Tick atleast one of the checkboxes Check Confirmations/Check Settlements')
    
        #raise Exception('Tick atleast one of the checkboxes')
    
trade =acm.FTrade[99062206]
ael_variables = [('trades', 'Trades', 'FTrade', None, create_trade_query(), 0, 1, ''),
                 ('check_confirmations', 'Check Confirmations', 'bool', [False, True], True, 0, 0, '', validate_selection),
                 ('check_settlements', 'Check Settlements', 'bool', [False, True], True, 0, 0, '', validate_selection),
                 ('show_query_results', 'Show Query Results', 'bool', [False, True], False, 0, 0, '', '')
                    ]

def ael_main(dictionary):
    if dictionary.get('trades'):
        show_query_results = dictionary.get('show_query_results')
        for each_trade in dictionary.get('trades'):
            analyze_trade_for_operations(each_trade, dictionary.get('check_confirmations'), dictionary.get('check_settlements'), show_query_results)


 

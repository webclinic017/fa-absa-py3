import acm
import FConfirmationParameters as ConfirmationParams
from FConfirmationParameters import tradeFilterQueries
from FOperationsDateUtils import AdjustDateToday
#import FConfirmationUtils as ConfirmationUtils
import FSwiftParameters as SwiftParameters
#import FConfirmationCreator
#from FConfirmationCorrectTradeRecaller import FConfirmationCorrectTradeRecaller
#import FConfirmationSingletonOwner as Singletons



def is_satisfying_trade_filter(trade):
    all_satisfied = True
    for each in tradeFilterQueries:
        if not acm.FStoredASQLQuery[each].Query().IsSatisfiedBy(trade):
            all_satisfied = False
            #print 'Trade ',  trade.Oid(), ' not satifying trade filter query', each
    return all_satisfied

def get_all_Confirmations(trade):
    calendar = trade.Currency().Calendar()
    startDate = AdjustDateToday(calendar, -ConfirmationParams.maximumDaysBack)
    endDate = ConfirmationUtils.INFINITE_NUMBER_OF_DAYS
    if trade.Instrument().InsType() != InsType.FUTURE_FORWARD:
        endDate = AdjustDateToday(calendar, ConfirmationParams.maximumDaysForward)
    return trade.GenerateConfirmations(startDate, endDate)
    
#creator = ConfirmationCreator()
#print dir(creator)
def will_Confirmations_be_created_for_trade(trade):
    #creator = Singletons.GetConfirmationCreator()
    #all_Confirmations_for_trade = creator._ConfirmationCreator__GetConfirmations(trade)
    #ConfirmationCorrectTradeRecaller = FConfirmationCorrectTradeRecaller()
    #sett_will_be_created = True
    
    for ConfirmationForTrade in all_Confirmations_for_trade:
        Confirmation = creator._ConfirmationCreator__CreateConfirmation(ConfirmationForTrade, ConfirmationCorrectTradeRecaller)
        if Confirmation:
            for each_prevention_query in ConfirmationParams.preventConfirmationCreationQueries:
                if acm.FStoredASQLQuery[each_prevention_query].Query().IsSatisfiedBy(Confirmation):
                    sett_will_be_created = False
                    #print 'Confirmation is satifying prevention query', each_prevention_query, '. Confirmation will not be created for trade %d', trade.Oid() 
    return sett_will_be_created

l = ['98893909', '98893902', '98893897', '98893891', '98893885', '98893850', '98893717', '98893702', '98893548', '98892235', '98892217', '98892202', '98892128', '98892103', '98892100', '98892097', '98892094', '98892088', '98892084', '98892079', '98892075', '98892072', '98892068', '98892067', '98892066', '98892065', '98892051', '98892037', '98892036', '98892035', '98892033', '98892028', '98892027', '98872707', '99057434', '99057171', '99056671', '99056310', '99055782', '99055360', '99054620', '98993356', '98942429', '98942407', '98941183', '98936670', '98919201', '98918332', '98918317', '98918287', '98918271', '98918252', '98917873', '98917872', '98917838', '98917814', '98917692', '98917690', '98917176', '98917172', '98917167', '98917120', '98917052', '98916861', '98916744', '98916592', '98916578', '98916532', '98916457', '98916426', '98916400', '98916339', '98916131', '98916127', '98916034', '98915932', '98915774', '98915713', '98915454', '98914963', '98914727', '98914529', '98914383', '98914035', '98914007', '98913805', '98913701', '98913663', '98913614', '98913468', '98913448', '98913392', '98913263', '98913105', '98912033', '98912028', '98911999', '98911976', '98911258', '98911235', '98911206', '98910033', '98909961', '98909931', '98909286', '98908706', '98908232', '98907584', '98905715', '98905379', '98904849', '98904279', '98902542', '98902538', '98901702', '98878996', '97496421', '97496383', '97496194', '97496153', '97496086', '97496072', '97494786', '97492020', '97489458', '97488808']
should_generate = []
should_not_gen = []
for each in l:
    trade =acm.FTrade[int(each)]
    all_satisfied = is_satisfying_trade_filter(trade)
    #sett_will_be_created = will_Confirmations_be_created_for_trade(trade)
    if all_satisfied: #and sett_will_be_created:
        should_generate.append(each)
        #print 'Trade ', trade.Oid(), ' is passing trade filters and Confirmation prevention queries'
    else:
        should_not_gen.append(each)

print('Confos should generate for ', len(should_generate), should_generate)
print('Confos should not generate for ', len(should_not_gen), should_not_gen)


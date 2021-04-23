

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
            print('Trade ',  trade.Oid(), ' not satifying trade filter query', each)
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
def will_Confirmations_be_created_for_trade(conf):
    #creator = Singletons.GetConfirmationCreator()
    #all_Confirmations_for_trade = creator._ConfirmationCreator__GetConfirmations(trade)
    #ConfirmationCorrectTradeRecaller = FConfirmationCorrectTradeRecaller()
    conf_will_be_created = True
    
    for each_prevention_query in ConfirmationParams.preventConfirmationCreationQueries:
        if acm.FStoredASQLQuery[each_prevention_query].Query().IsSatisfiedBy(conf):
            conf_will_be_created = False
            print('Confirmation is satifying prevention query', each_prevention_query, '. Confirmation will not be created for trade %d', conf.Oid()) 
    return conf_will_be_created


trade =acm.FTrade[98966564]
all_satisfied = is_satisfying_trade_filter(trade)
if all_satisfied:#all_satisfied: #and sett_will_be_created:
    print('Trade ', trade.Oid(), ' is passing trade filters ')

conf = acm.FConfirmation[497369]
conf_will_be_created = will_Confirmations_be_created_for_trade(conf)

if conf_will_be_created:#all_satisfied: #and sett_will_be_created:
    print('Confirmation ', conf .Oid(), ' is passing  Confirmation prevention queries')

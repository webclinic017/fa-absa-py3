import acm
import copy
import FSheetUtils
from StiwCustomization import DefaultNotificationSettings, COMPLETED_REQUEST_STATES, Market
from RFQUtils import Status
from collections import Counter
from DealPackageDevKit import DealPackageUserException    

def GetNotificationSetting(settingKey):
    settings = DefaultNotificationSettings()
    assert 'Role' in settings, "Key 'Role' missing in 'DefaultNotificationSettings'. Valid values: 'Sales', 'Trading'"
    assert settings['Role'] in ['Sales', 'Trading'], "Invalid value ('%s') for key 'Role' in 'DefaultNotificationSettings'. Valid values: 'Sales', 'Trading'" % settings['Role']
    assert 'DefaultStatuses' in settings, "Key 'DefaultStatuses' missing in 'DefaultNotificationSettings'."
    assert 'EnabledByDefault' in settings, "Key 'EnabledByDefault' missing in 'DefaultNotificationSettings'."
    return settings[settingKey]


def QuoteRequestQueryResult(customerRequest):
    activeQuery = acm.Trading().CreateQuoteRequestQuery(Market().Name())
    activeQuery.CustomerRequestId(customerRequest.Id())
    activeQueryResult = activeQuery.Result()
    activeQuery.Send()
    return activeQueryResult
    
    
def FindQuoteRequestPrice(quoteRequests, role):
    for quoteRequest in reversed(quoteRequests):
        if quoteRequest.Role() == role:
            if quoteRequest.Answer():
                return abs(quoteRequest.Answer().AskPrice() if quoteRequest.BidOrAsk() == 'Ask' else quoteRequest.Answer().BidPrice())
    return None
    

def FrequentlyTraded(children):
    mostTraded = ''
    instruments = []
    for child in children:
        if child.QuoteRequestInfo().Role() == 'Sales' and child.Instrument():
            instruments.append(child.Instrument().Name())
    if instruments:
        mostCommonCount = -1
        for name, count in Counter(instruments).most_common():
            if mostCommonCount <= count:
                mostCommonCount = count
                if mostTraded:
                    mostTraded = str(mostTraded) + ', ' + str(name)
                else:
                    mostTraded = str(name)
    return mostTraded

def FrequentlyOrderTraded(orders):
    mostTraded = ''
    instruments = []
    for order in orders:
        if order.TradingInterface().Instrument():
            instruments.append(order.TradingInterface().Instrument().Name())
    if instruments:
        mostCommonCount = -1
        for name, count in Counter(instruments).most_common():
            if mostCommonCount <= count:
                mostCommonCount = count
                if mostTraded:
                    mostTraded = str(mostTraded) + ', ' + str(name)
                else:
                    mostTraded = str(name)
    return mostTraded

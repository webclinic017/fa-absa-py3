""" Compiled: 2020-09-18 10:38:49 """

#__src_file__ = "extensions/settlement/etc/FSettlementPayoutUpdateFromMtmPrice.py"
"""
FSettlementPayoutUpdateFromMtmPrice

DESCRIPTION: This script is intended to be used after an MTM price has been updated/inserted
             and you do not want to wait for the EOD-process to update/create the affected
             settlement record(s).

INPUT PARAMETERS: An expiry date of the affected instrument on the format YYYY-MM-DD
"""

import FOperationsUtils as Utils
import acm, ael
import FSettlementProcess
from FOperationsEnums import InsType, SettleType
from FSettlementNettingRuleQueryCache import SettlementNettingRuleQueryCache

defaultDate = ael.date_today().to_string(ael.DATE_ISO)
defaultDateList = defaultDate.split('-')

ael_variables = [['year', 'Expiry Year (yyyy)', 'string', None, defaultDateList[0], 1, 0],
                 ['month', 'Expiry Month (mm)', 'string', None, defaultDateList[1], 1, 0],
                 ['day', 'Expiry Day (dd)', 'string', None, defaultDateList[2], 1, 0]]

def ael_main(dictionary):
    
    fromDateString = dictionary['year'] + '-' + dictionary['month'] + '-' + dictionary['day']
    messageString = "FOperationsPayoutUpdateFromMtmPrice called CreateSettlementsFromTrade. No AMBA message as input."
    toDateString = acm.Time().DateAddDelta(fromDateString, 0, 0, 1)
    nettingRuleQueryCache = SettlementNettingRuleQueryCache()

    for trade in GetFutureForwardVarianceSwapTrades(fromDateString, toDateString):
        FSettlementProcess.CreateSettlementsFromTrade(trade, messageString, nettingRuleQueryCache)
    
    
def GetFutureForwardVarianceSwapTrades(fromDateString, toDateString):
    query = GetFutureForwardVarianceSwapQuery(fromDateString, toDateString)
    return query.Select()


def GetFutureForwardVarianceSwapQuery(fromDateString, toDateString):
        
    query = acm.CreateFASQLQuery(acm.FTrade, 'AND')
    or1 = query.AddOpNode('OR')
    or1.AddAttrNode('Instrument.InsType', 'EQUAL', Utils.GetEnum('InsType', InsType.FUTURE_FORWARD))
    or1.AddAttrNode('Instrument.InsType', 'EQUAL', Utils.GetEnum('InsType', InsType.VARIANCE_SWAP))
    query.AddAttrNode('Instrument.Otc', 'EQUAL', True)
    query.AddAttrNode('Instrument.SettlementType', 'EQUAL', Utils.GetEnum('SettlementType', SettleType.CASH))
    query.AddAttrNode('Instrument.ExpiryDate', 'GREATER_EQUAL', fromDateString)
    query.AddAttrNode('Instrument.ExpiryDate', 'LESS', toDateString)
    return query
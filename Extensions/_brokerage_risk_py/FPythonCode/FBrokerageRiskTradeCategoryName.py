""" Compiled: 2020-09-18 10:38:55 """

#__src_file__ = "extensions/BrokerageRisk/etc/FBrokerageRiskTradeCategoryName.py"
"""--------------------------------------------------------------------------
MODULE
    Brokerage Risk

    (c) Copyright 2016 SunGard Front Arena AB. All rights reserved.

DESCRIPTION

-----------------------------------------------------------------------------"""

import acm

name_map = { 'None' : 'Exposure' }

def BrokerageRiskTradeCategoryName(trade):
    name = trade.TradeCategory()
    return name_map.get( name, name ) # return mapped name if found, else the name as is

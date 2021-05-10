""" Compiled: 2020-09-18 10:38:55 """

#__src_file__ = "extensions/BrokerageRisk/etc/ConditionalModels.py"
"""--------------------------------------------------------------------------
MODULE
    Brokerage Risk

    (c) Copyright 2016 SunGard Front Arena AB. All rights reserved.

DESCRIPTION

-----------------------------------------------------------------------------"""

import acm

def MatchingCondition(instrument, model, portfolio, currency = None):
    parameters = acm.FConditionParameters()
    parameters.Instrument( instrument ) if instrument else None
    parameters.Portfolio( portfolio ) if portfolio else None
    parameters.Client( portfolio.PortfolioOwner() ) if portfolio else None
    parameters.Currency( currency ) if currency else None
    
    return model.MatchingCondition( parameters )




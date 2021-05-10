""" Compiled: 2020-09-18 10:38:55 """

#__src_file__ = "extensions/BrokerageRisk/etc/CollateralValuesCM.py"
"""--------------------------------------------------------------------------
MODULE
    BrokerageRisk

    (c) Copyright 2016 SunGard FRONT ARENA. All rights reserved.

DESCRIPTION

-----------------------------------------------------------------------------"""

import acm
import FBrokerageRiskExtensionPoints
    
def MatchingCondition(instrument, modelName, portfolio, currency = None):
    parameters = acm.FConditionParameters()
    parameters.Instrument( instrument ) if instrument else None
    parameters.Portfolio( portfolio ) if portfolio else None
    parameters.Client( FBrokerageRiskExtensionPoints.FindClient( portfolio.PortfolioOwner() ) ) if portfolio else None
    parameters.Currency( currency ) if currency else None
    
    model = acm.FConditionalValueModel[ modelName ]
    if not model:
        return None
    return model.MatchingCondition( parameters )


'''----------------------------------------------------------------------------------------------------------
MODULE                  :       PACE_MM_Recon_Functions
PROJECT                 :       PACE MM
PURPOSE                 :       This module contains functions used for the recon between FA and PACE MM
DEPARTMENT AND DESK     :       Money Market Desk
REQUASTER               :       PACE MM Project
DEVELOPER               :       Heinrich Cronje
CR NUMBER               :       822638
-------------------------------------------------------------------------------------------------------------

HISTORY
=============================================================================================================
Date            Change no       Developer                       Description
-------------------------------------------------------------------------------------------------------------
2011-09-01      822638          Heinrich Cronje                 Initial Implementation

-------------------------------------------------------------------------------------------------------------

DESCRIPTION OF MODULE:

    applyGlobalSimulation               :       Function to change Trading Manager portfolio settings.
    get_Trading_Manager_Column_Value    :       Functions to retreive a Trading Manager column on a Trade Sheet.
'''

import acm

calcSpace = acm.Calculations().CreateCalculationSpace(acm.GetDefaultContext(), 'FTradeSheet')

def applyGlobalSimulation(t, date, *rest):
    calcSpace.SimulateGlobalValue('Portfolio Profit Loss End Date', 'Custom Date')
    calcSpace.SimulateGlobalValue('Portfolio Profit Loss End Date Custom', date)
    calcSpace.Refresh()
    return date
    
def get_Trading_Manager_Column_Value(trade, columnName, *rest):
    trade = acm.FTrade[trade.trdnbr]
    
    value = calcSpace.CalculateValue(trade, columnName)
    if value:
        try:
            Numbervalue = value.Number()
        except:
            Numbervalue = value
        
        return Numbervalue
    return 0.00

"""----------------------------------------------------------------------------
MODULE
    FPersistentSpreadTable - Market Making specific.

    (c) Copyright 2011 by SunGard FRONT ARENA. All rights reserved.
 ---------------------------------------------------------------------------"""
import acm

absolute = 1
relative = 2
quantity = 1
amount = 2
tight = 1
wide = 2

""" createDefaultSpreadTables
Creates the default spread tables that aren't already in the database. """
def createDefaultSpreadTables():
    createDefaultSpreadTable()
    createLiquidityClass(1)
    createLiquidityClass(2)
    createLiquidityClass(3)
    createLiquidityClass(4)

""" createDefaultSpreadTable
Creates a spread table with only one spread rule with a max spread of 20
and a min quantity of 1."""
def createDefaultSpreadTable():
    defaultTable = acm.FPersistentSpreadTable['DEFAULT']
    
    if not defaultTable:
        newDefaultTable = acm.FPersistentSpreadTable()
        newDefaultTable.SpreadTableID('DEFAULT')
        
        ruleTight = acm.FPersistentSpreadRule()
        ruleTight.Min(0)
        ruleTight.MaxSpread(20)
        ruleTight.MaxSpreadType(absolute)
        ruleTight.MinQuoteSize(1)
        ruleTight.MinQuoteSizeType(quantity)
        ruleTight.Strategy(tight)
        ruleWide = ruleTight.Clone()
        ruleWide.Strategy(wide)
        
        newDefaultTable.AddSpreadRule(ruleTight)
        newDefaultTable.AddSpreadRule(ruleWide)
        
        acm.BeginTransaction()
        newDefaultTable.Commit()
        acm.CommitTransaction()


""" Designated Sponsoring Liquidity Class parameters
Will generate spread rules for Liquidity Class N of the following form:
limit(i) - limit(i+1) : spread(i), spreadType(i) : minQuoteAmount(N)
(assuming all Classes contain the same number of spread rules).
"""

""" spreadTableIds - one Spread Table ID for each Liquidity Class """
spreadTableIds = ['LiquidityClass1', 'LiquidityClass2', 'LiquidityClass3', 'LiquidityClass4', 'LiquidityClass5']

""" minLimits - one vector for each Liquidity Class [limit(1), limit(2), ..., limit(n)] """
minLimits = [[0.0, 1.0, 2.0, 8.0], [0.0, 1.0, 3.2, 8.0], [0.0, 1.0, 4.0, 8.0], [0.0, 1.0, 4.0, 8.0]]

""" maxSpread - one vector for each Liquidity Class [spread(1), spread(2), ..., spread(n)] """
maxSpreads = [[0.1, 10.0, 0.2, 2.5], [0.1, 10.0, 0.32, 4.0], [0.1, 10.0, 0.4, 5.0], [0.1, 10.0, 0.4, 5.0]]

""" minQuoteAmounts - one amount for each Liquidity Class """
minQuoteAmounts = [20000, 15000, 10000, 1]

""" spreadTypes - one spreadType for each spread rule """
spreadTypes = [absolute, relative, absolute, relative]

""" spreadRules - the number of spread rules in each LiquidityClass """
spreadRules = 4

""" createLiquidityClass
Creates the spread table for the desired Liquidity Class. """
def createLiquidityClass(liquidityClass):
    liquidityClassTable = acm.FPersistentSpreadTable[spreadTableIds[liquidityClass - 1]]
    
    if not liquidityClassTable:
        newLiquidityClass = acm.FPersistentSpreadTable()
        newLiquidityClass.SpreadTableID(spreadTableIds[liquidityClass - 1])
        
        i = 0
        while i < spreadRules:
            ruleTight = acm.FPersistentSpreadRule()
            ruleTight.Min(minLimits[liquidityClass - 1][i])
            ruleTight.MaxSpread(maxSpreads[liquidityClass - 1][i])
            ruleTight.MaxSpreadType(spreadTypes[i])
            ruleTight.MinQuoteSize(minQuoteAmounts[liquidityClass - 1])
            ruleTight.MinQuoteSizeType(amount)
            ruleTight.Strategy(tight)
            ruleWide = ruleTight.Clone()
            ruleWide.Strategy(wide)
        
            newLiquidityClass.AddSpreadRule(ruleTight)
            newLiquidityClass.AddSpreadRule(ruleWide)
            
            i = i + 1
            
        acm.BeginTransaction()
        newLiquidityClass.Commit()
        acm.CommitTransaction()
        

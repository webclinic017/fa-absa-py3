"""----------------------------------------------------------------------------------------------------
DESCRIPTION
    This module contains code to calculate and save sales credits for Bond, Swap and FRA trades.

-------------------------------------------------------------------------------------------------------
HISTORY
=======================================================================================================
Date            JIRA no       Developer               Requester               Description
-------------------------------------------------------------------------------------------------------
2020-01-22      FAFO-77       Amit Kardile            Denzil Pieterse         Initial Implementation
-------------------------------------------------------------------------------------------------------
"""

import acm
from at_logging import getLogger
LOGGER = getLogger()

def calculate_benchmark_delta(trade):
    calc_space = acm.FCalculationMethods().CreateStandardCalculationsSpaceCollection()
    calc = trade.Calculation().InterestRateBenchmarkDelta(calc_space)
    return calc.Number()

def calculate_sales_credit(benchmark_delta, sales_credit_percent, sales_credit_spread):
    sales_credit = abs(sales_credit_spread * sales_credit_percent * benchmark_delta)
    return sales_credit

def calculate_and_save_sales_credits(shell, obj):
    if obj.IsKindOf('FTrade') and obj.Instrument().InsType() in ['Bond', 'FRA', 'Swap'] and obj.AdditionalInfo().Sales_Credit_Spread() and obj.Status() == 'FO Confirmed':
        trade = obj
        sales_credit_spread = trade.AdditionalInfo().Sales_Credit_Spread()
        
        if trade.AdditionalInfo().SC_Multiply_Factor():
            sales_credit_percent = trade.AdditionalInfo().SC_Multiply_Factor()
        else:
            sales_credit_percent = 0.333
            
        benchmark_delta = calculate_benchmark_delta(trade)
        sales_credit = calculate_sales_credit(benchmark_delta, sales_credit_percent, sales_credit_spread)
        sales_person = trade.Trader().Name()
        trade.SalesCredit(sales_credit)
        trade.SalesPerson(sales_person)
        LOGGER.info('Successfully added sales credit %f and sales person %s to the trade.' %(sales_credit, sales_person))

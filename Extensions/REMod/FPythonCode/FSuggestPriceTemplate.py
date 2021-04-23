

"""----------------------------------------------------------------------------
MODULE
    FSuggestPriceTemplate - Module that handles the suggested price for 
    the underlying instrument when trading Repo/Reverse and SecurityLoan. 
    The suggested price is the market dirty price rounded to 2 decimals. 

    (c) Copyright 2011 by SunGard FRONT ARENA. All rights reserved.

RENAME this module to FSuggestPrice.

----------------------------------------------------------------------------"""
import ael
import acm

def suggest_undprice(trade):

    if not trade.insaddr:
        print ('No instrument found')
        return 0
    
    if not trade.insaddr.und_insaddr:
        print ('No underlying instrument found')
        return 0

    context = acm.GetDefaultContext()
    sheet_type = 'FDealSheet'
    calc_space = acm.Calculations().CreateCalculationSpace( context, sheet_type)    

    marketPrice_ColumnId = 'Instrument Market Price'
    marketPriceDirty_ColumnId = 'Instrument Market Price Dirty'
    fromQ_ColumnId = 'Standard Calculations From Quote'
    theorPrice_ColumnId = 'Standard Calculations Price Theor'
    fromQtn_ColumnId = 'Standard Calculations From Quotation'
    quote_ColumnId = 'Standard Calculations Quote To Quote'
    quoteDay_ColumnId = 'Standard Calculations From Quote Value Date'
    
    trd = acm.FTrade[trade.trdnbr]
    undIns = acm.FInstrument[trade.insaddr.und_insaddr.insid]
    round = acm.GetFunction('round', 3)

    if trade.insaddr.instype == 'BuySellback':
        price = calc_space.CreateCalculation( undIns, marketPrice_ColumnId ).Value().Number()
        if not acm.Math.IsFinite( price ):
            price = calc_space.CreateCalculation( undIns, theorPrice_ColumnId ).Value().Number()
        price = round(price, 2, 'Normal')
    else:   
        price = calc_space.CreateCalculation( undIns, marketPriceDirty_ColumnId ).Value().Number()
        if not acm.Math.IsFinite( price ):
            price = calc_space.CreateCalculation( undIns, theorPrice_ColumnId ).Value().Number()
            calc_space.SimulateValue( undIns, marketPrice_ColumnId, price )
            price = calc_space.CreateCalculation( undIns, marketPriceDirty_ColumnId ).Value().Number()
            calc_space.RemoveSimulation( undIns, marketPrice_ColumnId )

        price = round(price, 2, 'Normal')        
        calc_space.SimulateValue( undIns, fromQ_ColumnId, price )
        calc_space.SimulateValue( undIns, fromQtn_ColumnId, 'Pct of Nominal')    
        day = trd.ValueDay()
        calc_space.SimulateValue( undIns, quoteDay_ColumnId, day )        
        price = calc_space.CreateCalculation( undIns, quote_ColumnId ).Value().Number()    
        calc_space.RemoveSimulation( undIns, fromQ_ColumnId )
        calc_space.RemoveSimulation( undIns, fromQtn_ColumnId )
        calc_space.RemoveSimulation( undIns, quoteDay_ColumnId )

    return price


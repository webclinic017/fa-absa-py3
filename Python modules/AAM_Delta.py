"""-----------------------------------------------------------------------------
PURPOSE                 :  InstrumentPriceDetla calculation for Bond Options
DEPATMENT AND DESK      :  AAM
REQUESTER               :  Suvarn Naidoo
DEVELOPER               :  Rohan van der Walt
CR NUMBER               :  
--------------------------------------------------------------------------------

HISTORY
================================================================================
Date        Change no  Developer                 Description
--------------------------------------------------------------------------------
2015-08-11  XXXXXXX    Rohan vd Walt             Initial Implementation
"""

import acm
import at_calculation_space
import datetime
from PS_Functions import YieldToPrice_old

def insPriceDelta(instrument, pnldate):
    '''
    This will calculate the position delta by bumping the underlying's price by 1bp
    '''
    sheet_type = 'FPortfolioSheet'
    context = acm.GetDefaultContext()
    calc_space = acm.Calculations().CreateCalculationSpace( acm.GetDefaultContext(), sheet_type )
    calc_space.SimulateGlobalValue( 'Portfolio Profit Loss End Date', 'Custom' )
    calc_space.SimulateGlobalValue( 'Portfolio Profit Loss End Date Custom', pnldate )
    try:
        und_ins = instrument.Underlying()
        if not und_ins:
            return 0
        ins_nd = calc_space.InsertItem(instrument)
        und_ins_nd = calc_space.InsertItem(und_ins)
        calc_space.Refresh()
        curr_ins_price = calc_space.CalculateValue( ins_nd.Iterator().FirstChild().Tree(), 'Price Theor' )
        ins_und_price = calc_space.CalculateValue( und_ins_nd.Iterator().FirstChild().Tree(), 'Price Theor' )
        curr_undins_dirty_price = calc_space.CalculateValue( und_ins_nd.Iterator().FirstChild().Tree(), 'Instrument Market Price Dirty' )
        new_underlying_price = float(ins_und_price.Value()) + 0.01
        calc_space.SimulateValue( ins_nd.Iterator().FirstChild().Tree(), 'Portfolio Underlying Price', new_underlying_price )
        calc_space.Refresh()
        new_undins_dirty_price = YieldToPrice_old(und_ins, pnldate, new_underlying_price, True, False)
        underlying_price_delta = new_undins_dirty_price - curr_undins_dirty_price.Number()
        new_ins_theor_val = calc_space.CalculateValue( ins_nd.Iterator().FirstChild().Tree(), 'Price Theor' )
        ins_price_delta = (new_ins_theor_val - curr_ins_price)
        result = ins_price_delta.Number() / underlying_price_delta
        return result
    except Exception, e:
        print 'ERROR', e
    finally:
        calc_space.RemoveSimulation( instrument, 'Portfolio Underlying Price' )
        pass
    
    return 0

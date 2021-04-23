from __future__ import print_function
"""
Help functions to the Fixed Income Quote Sheet
"""

import acm

# Driver Name is the name displayed in the Fixed Income Quote Sheet
# Driver Type is the name stored inside the ADS
DRIVER_NAME_2_TYPE = {  'AswSpread'     : 'Asset Swap',
                        'DM'            : 'Disc Marg',
                        'Offset'        : 'Offset',
                        'Price'         : 'Price',
                        'Spread Bid Driver': 'Spread bid',
                        'Spread Bid Price': 'Price bid',
                        'YTM'           : 'YTM',
                        'Z-Spread'      : 'Yield',
                        'Gross Basis'   : 'Gross Basis',
                        'I-Spread'      : 'Par Rate'}

ASSET_SWAP        = {   'Bid'           : 'Proposed Quote Asset Swap Spread Bid',
                        'Ask'           : 'Proposed Quote Asset Swap Spread Ask',
                        'Mid'           : 'Proposed Quote Asset Swap Spread Mid',
                        'Curve'         : 'Asset Swap Curve'}
                
DM                = {   'Bid'           : 'Proposed Quote Asset Swap Spread Bid',
                        'Ask'           : 'Proposed Quote Asset Swap Spread Ask',
                        'Mid'           : 'Proposed Quote Asset Swap Spread Mid',
                        'Curve'         : 'Asset Swap Curve'}
                
OFFSET            = {   'Bid'           : 'Proposed Quote Offset Bid Base',
                        'Ask'           : 'Proposed Quote Offset Ask Base',
                        'Mid'           : 'Proposed Quote Offset Mid Base'}
                        
PRICE             = {   'Bid'           : 'Proposed Quote Price Spread Bid',
                        'Ask'           : 'Proposed Quote Price Spread Ask',
                        'Mid'           : 'Proposed Quote Price Spread Mid',
                        'Benchmark'     : 'Price Spread Benchmark'}

SPREAD_BID_DRIVER = {   'Ask'           : 'Proposed Quote Bid-Driver Spread Ask Base'}

SPREAD_BID_PRICE  = {   'Ask'           : 'Proposed Quote Bid-Price Spread Ask'}

YTM               = {   'Bid'           : 'Proposed Quote YTM Spread Bid',
                        'Ask'           : 'Proposed Quote YTM Spread Ask',
                        'Mid'           : 'Proposed Quote YTM Spread Mid',
                        'Benchmark'     : 'YTM Spread Benchmark'}

Z_SPREAD          = {   'Bid'           : 'Proposed Quote Z-Spread Bid',
                        'Ask'           : 'Proposed Quote Z-Spread Ask',
                        'Mid'           : 'Proposed Quote Z-Spread Mid',
                        'Curve'         : 'Z-Spread Curve'}

GROSS_BASIS       = {   'Bid'           : 'Proposed Quote Gross Basis Bid',
                        'Ask'           : 'Proposed Quote Gross Basis Ask',
                        'Mid'           : 'Proposed Quote Gross Basis Mid',
                        'Benchmark'     : 'Gross Basis Benchmark'}

I_SPREAD          = {   'Bid'           : 'Bid Proposed Quote I-Spread',
                        'Ask'           : 'Ask Proposed Quote I-Spread',
                        'Mid'           : 'Mid Proposed Quote I-Spread',
                        'Curve'         : 'I-Spread Curve'}

DRIVER_TYPE_2_DEF = {   'Asset Swap'    : ASSET_SWAP,
                        'Disc Marg'     : DM,
                        'Offset'        : OFFSET,
                        'Price'         : PRICE,
                        'Spread bid'    : SPREAD_BID_DRIVER,
                        'Price bid'     : SPREAD_BID_PRICE,
                        'YTM'           : YTM,
                        'Yield'         : Z_SPREAD,
                        'Gross Basis'   : GROSS_BASIS,
                        'Par Rate'      : I_SPREAD}
                
DEFAULT_DEF       = {  'Bid'           :'Proposed Quote Asset Swap Spread Bid',
                        'Ask'           :'Proposed Quote Asset Swap Spread Ask', 
                        'Mid'           :'Proposed Quote Asset Swap Spread Mid'}
                            

# Helper functions for getting/setting columns via DataSource (Sent on the wire if using Pace) 

def _get_column_value(quote_controller, column_id):
    data_source = quote_controller.CreateDataSource(column_id)
    if data_source:
        return data_source.Get()
    return None

def _set_column_value(quote_controller, column_id, value):
    data_source = quote_controller.CreateDataSource(column_id)
    if data_source:
        return data_source.Set(value)


# Other Helper Functions and Getters of Column values

def _get_driver_type_def(driver_type):
    if driver_type in DRIVER_TYPE_2_DEF:
        return DRIVER_TYPE_2_DEF[driver_type]
    else:    
        print ('Driver type: ', driver_type, ' not supported!')
        return None

def _get_driver_type_column_id(driver_type, key):
    driver_type_def = _get_driver_type_def(driver_type)
    if driver_type_def is not None:
        if key in driver_type_def:
            return driver_type_def[key]
    return None
    
def _get_driver_type_column_value(quote_controller, driver_type, key):
    column_id = _get_driver_type_column_id(driver_type, key)
    if column_id is not None:
        return _get_column_value(quote_controller, column_id)
    return None

def _driver_name_to_type(driver_name):
    """Returns corresponding driver type"""
    driver_type = 'Asset Swap'
    try:
        driver_type = DRIVER_NAME_2_TYPE[driver_name]
    except KeyError: 
        print ("Validation failed. Driver type: ", driver_name, " is not supported!")
        
    return driver_type

def _is_orderbook_interface(trading):
    """Returns True if trading is a order book interface"""
    return trading.Category() == 'OrderBookInterface'

def _is_spread_driver(driver):
    """ Returns True if the drive is a spread diver """
    return driver in ['Price bid', 'Spread bid']
             
def _invert_bid_or_ask(bid_or_ask):
    """Transform bid to ask and ask to bid"""
    if bid_or_ask == "Bid":
        return "Ask"
    elif bid_or_ask == "Ask":
        return "Bid"
    else:
        return ""

def get_instrument_spread(instrument):
    """Returns the instrument spread, None, or print error
    message if there are multiple instrument spread records
    """
    yield_curve = instrument.MappedDiscountLink().Link().YieldCurveComponent()

    if not yield_curve.IsKindOf("FInstrumentSpread"):
        print ("Mapped curve is not of type Instrument spread Bid/Ask")
        return None
    
    return yield_curve

def _get_current_driver_type(quote_controller, bid_or_ask):
    """Returns the value (i.e. the type) of the currently used driver"""
    driver_name = None
    if 'Bid' == bid_or_ask:
        driver_name = _get_column_value(quote_controller, 'Proposed Quote Driver Bid')
    else:
        driver_name = _get_column_value(quote_controller, 'Proposed Quote Driver Ask')
    
    return _driver_name_to_type(driver_name)  

def _get_driver_value(quote_controller, driver_type, bid_or_ask):
    """Returns the value of the driver used to drive the quote."""
    try:
        column_value = _get_driver_type_column_value(quote_controller, driver_type, bid_or_ask)
    except:
        # pylint: disable=W0702
        return float('nan')
        
    if acm.Math().IsFinite(column_value):
        return column_value
    else:
        return float('nan')
    
def _get_current_benchmark(quote_controller, driver_type):
    """Returns the currently used benchmark."""
    return _get_driver_type_column_value(quote_controller, driver_type, 'Benchmark')

def _get_current_swap_curve(quote_controller, driver_type):
    """Returns the currently used swap curve."""
    return _get_driver_type_column_value(quote_controller, driver_type, 'Curve')
 
# Function called by Pre-Input Hooks 

def pre_change_driver_type(row, new_driver, bid_or_ask, operation):
    quote_controller = row.QuoteController()
    if quote_controller:
        if str(operation) == 'remove':
            _remove_driver_value(quote_controller, bid_or_ask)
        else:
            new_driver_type = _driver_name_to_type(new_driver)
            new_driver_value = _get_driver_value(quote_controller, new_driver_type, bid_or_ask)
            _save_driver_value(quote_controller, new_driver_value, bid_or_ask)


# Functions called by Post-Input Hooks

def get_curve_type(row):
    """Check if the instrument is a FFrn and set correct spread type"""
    quote_controller = row.QuoteController()
    if quote_controller:
        instrument = quote_controller.Instrument()
        spread_type = 'AswSpread'
        if instrument and instrument.IsKindOf("FFrn"):
            spread_type = 'DM'
        return spread_type
    return None
                

def save_instrument_spread_info(quote_controller):
    """Save ALL instrument spread information used by the 
    current driver to the instrument spread curve.
    """

    if _get_column_value(quote_controller, 'Save Ins Spread On Input'):
        instrument = quote_controller.Instrument()

        if _is_orderbook_interface(quote_controller.TradingInterface()):
            instrument_spread = get_instrument_spread(instrument)
            if instrument_spread:
                # Bid side data
                driver_type_bid = _get_current_driver_type(quote_controller, 'Bid')
                current_spread_bid = _get_driver_value(quote_controller, driver_type_bid, 'Bid')
                
                # Ask side data
                driver_type_ask = _get_current_driver_type(quote_controller, 'Ask')
                current_spread_ask = _get_driver_value(quote_controller, driver_type_bid, 'Ask')
                
                # General data
                benchmark_bid = _get_current_benchmark(quote_controller,
                                                      driver_type_bid)
                benchmark_ask = _get_current_benchmark(quote_controller,
                                                      driver_type_ask)
                if benchmark_bid:
                    if benchmark_ask and (not benchmark_bid ==benchmark_ask):
                        print ('Ask and bid side do not use the same benchmark. Saving bid benchmark')
                    benchmark = benchmark_bid
                else:
                    benchmark = benchmark_ask
                
                curve_bid = _get_current_swap_curve(quote_controller, driver_type_bid)
                curve_ask = _get_current_swap_curve(quote_controller, driver_type_ask)
                if curve_bid:
                    if curve_ask and (not curve_bid == curve_ask):
                        print ('Ask and bid side do not use same curve. Saving bid curve')
                    curve = curve_bid
                else:
                    curve = curve_ask
                
                # Commit changes
                instrument_spread.SpreadType(driver_type_bid)
                instrument_spread.Spread(current_spread_bid)
                instrument_spread.SpreadTypeAsk(driver_type_ask)
                instrument_spread.SpreadAsk(current_spread_ask)
                instrument_spread.Benchmark(benchmark)
                instrument_spread.UnderlyingYieldCurve(curve)
                instrument_spread.Commit()            
                
def change_driver_value(row, from_driver, from_value, operation, side):
    if 'Mid' == side:
        _change_driver_value_mid(row, from_driver, from_value, operation)
    else:
        _change_driver_value_bid_or_ask(row, from_driver, from_value, operation, side)

def change_offset(row, value, column_id, bid_or_ask, operation):
    quote_controller = row.QuoteController()
    if quote_controller:
        val = float('NaN')
        if str(operation) != 'remove':
            multi_column_id = 'Offset Scaling ' + bid_or_ask + ' Multi'
            coeff = _get_column_value(quote_controller, multi_column_id)
            val = value / coeff
            
        change_driver_value(row, 'Offset', val, operation, bid_or_ask)

def change_price_spread(row, value, operation):
    """Change the spread between the raw proposed quotes"""
    quote_controller = row.QuoteController()
    if quote_controller is not None:
        fix_side = _get_column_value(quote_controller, 'Proposed Quote Driver Spread Side')
        if 'Mid' == fix_side:
            _change_price_spread_mid_fix(row, value, operation)
        else:
            # The input is the side we want to keep fix, i.e. we want to
            # change the other side
            side = _invert_bid_or_ask(fix_side)
            change_driver_value(row, "Spread Bid Price", value, operation, side)
            if _is_spread_driver(_get_current_driver_type(quote_controller, 'Ask')):
                change_driver_value(row, "Spread Bid Price", value, operation, 'Ask')

def change_driver_spread(row, value, operation):
    """ Change the spread between the bid and the ask driver"""
    quote_controller = row.QuoteController()
    if quote_controller is not None:
        fix_side = _get_column_value(quote_controller, 'Proposed Quote Driver Spread Side')
        if 'Mid' == fix_side:
            _change_driver_spread_mid_fix(row, value, operation)
        else:
            # The input is the side we want to keep fix, i.e. we want to
            # change the other side
            side = _invert_bid_or_ask(fix_side)
            _change_driver_spread_side_fix(row, value, operation, side)


# Helper Functions used by Pre/Post Input Hooks that modify the ADS (FPersistent) and/or set columns using helper functions  

def _change_driver_value_bid_or_ask(row, from_driver, from_value, operation, side):
    """Change a value on the bid or ask side"""
    quote_controller = row.QuoteController()
    if quote_controller is not None:
        if str(operation) == 'remove':
            _remove_driver_type_and_value(quote_controller, side)
        else:
            _modify_driver_value(quote_controller, from_driver, from_value, side)
            save_instrument_spread_info(quote_controller)

def _change_driver_value_mid(row, from_driver, from_value, operation):
    """Change a mid value"""
    quote_controller = row.QuoteController()
    if quote_controller is not None:
        if str(operation) == 'remove':
            _remove_driver_type_and_value(quote_controller, 'Bid')
            _remove_driver_type_and_value(quote_controller, 'Ask')
        else:
            spread = _get_column_value(quote_controller, 'Proposed Quote Bid-Driver Spread Ask')
            _modify_driver_value_mid(from_driver, from_value, quote_controller, spread)
            save_instrument_spread_info(quote_controller)

def _modify_driver_value_mid(from_driver, from_value, quote_controller, spread):
    """Modifies and saves new bid and ask values from a mid value"""
    mid_driver = _get_column_value(quote_controller, 'Proposed Quote Driver Mid')
    sign = _get_column_value(quote_controller, 'Bid Driver Sign')

    calculated_mid_value = _convert_between_drivers(quote_controller,
                                                    from_driver, from_value,
                                                    'Mid')
    offset = sign * spread / 2.0
    coeff = _get_column_value(quote_controller, 'Offset Scaling Mid')
    bid_value = calculated_mid_value - offset / coeff
    ask_value = calculated_mid_value + offset / coeff
    
    _modify_driver_value(quote_controller, mid_driver, bid_value, 'Bid')
    _modify_driver_value(quote_controller, mid_driver, ask_value, 'Ask')

            
def _convert_between_drivers(quote_controller, from_driver, from_value, side):
    """Convert value between two drivers. One driver is the from_driver and the
    other driver is the currently used driver of the side."""
    
    # Set the value entered from the sheet
    column_id = 'From Driver Value ' + side
    _set_column_value(quote_controller, column_id, from_value)
    
    # Set the driver corresponding to the column where the value has been entered in the sheet
    column_id = 'From Driver ' + side
    _set_column_value(quote_controller, column_id, from_driver)
    
    # Recalibrate the driver value based on the modification in the sheet
    column_id = 'Convert Between Drivers ' + side
    try:
        new_driver_value = _get_column_value(quote_controller, column_id)
    except:
        # pylint: disable=W0702
        new_driver_value = float('nan')
    
    return new_driver_value

def _modify_driver_value(quote_controller, from_driver, from_value, side):
    """ Calculate and save the new driver value"""
    calculated_driver_value = _convert_between_drivers(quote_controller,
                                                       from_driver,
                                                       from_value,
                                                       side)
                                                       
    _save_driver_value(quote_controller, calculated_driver_value, side)
    
def _remove_driver_type_and_value(quote_controller, bid_or_ask):
    """ Remove both type and value from the bid or ask side."""
    _remove_driver_type(quote_controller, bid_or_ask)
    _remove_driver_value(quote_controller, bid_or_ask)

def _remove_driver_value(quote_controller, bid_or_ask):
    _save_driver_value(quote_controller, '', bid_or_ask)

def _save_driver_value(quote_controller, new_value, bid_or_ask):
    # Set new driver value in sheet
    if bid_or_ask == 'Bid':
        _set_column_value(quote_controller, 'Proposed Quote Driver Value Bid', new_value)
    else:
        _set_column_value(quote_controller, 'Proposed Quote Driver Value Ask', new_value)

def _change_driver_spread_side_fix(row, value, operation, side):
    """ The bid or ask side should be fixed when changing the spread"""
    quote_controller = row.QuoteController()
    if quote_controller is not None:
        if str(operation) == 'remove':
            _remove_driver_type_and_value(quote_controller, side)
        else:
            coeff = _get_column_value(quote_controller, 'Offset Scaling Bid')
            val = value / coeff
            change_driver_value(row, "Spread Bid Driver", val, operation, side)
            if _is_spread_driver(_get_current_driver_type(quote_controller, 'Ask')):
                change_driver_value(row, "Spread Bid Driver", val, operation, 'Ask')
        
def _change_driver_spread_mid_fix(row, input_spread, operation):
    """ The mid value should be fixed when changing the spread"""
    quote_controller = row.QuoteController()
    if quote_controller is not None:
        if str(operation) == 'remove':
            _remove_driver_type_and_value(quote_controller, 'Bid')
            _remove_driver_type_and_value(quote_controller, 'Ask')
        else:
            spread = input_spread
            mid_driver_name = _get_column_value(quote_controller, 'Proposed Quote Driver Mid')
            mid_driver_type = _driver_name_to_type(mid_driver_name)
            mid_value = _get_driver_value(quote_controller, mid_driver_type, "Mid")
            _modify_driver_value_mid(mid_driver_name, mid_value, quote_controller, spread)
            save_instrument_spread_info(quote_controller)

def _change_price_spread_mid_fix(row, price_spread, operation):
    """Change the price spread while keeping the mid proposed quote
    price fixed."""
    quote_controller = row.QuoteController()
    if quote_controller is not None:
        mid_quote = _get_column_value(quote_controller, 'Proposed Quote Mid')
        offset = float(price_spread) / 2.0
        bid_quote = float(mid_quote) - offset
        ask_quote = float(mid_quote) + offset
        change_driver_value(row, 'Quote', bid_quote, operation, 'Bid')
        change_driver_value(row, 'Quote', ask_quote, operation, 'Ask')
        save_instrument_spread_info(quote_controller)

def _remove_driver_type(quote_controller, bid_or_ask):
    if bid_or_ask == 'Ask':
        _set_column_value(quote_controller, 'Proposed Quote Driver Ask', '')
    else:
        _set_column_value(quote_controller, 'Proposed Quote Driver Bid', '')
                   

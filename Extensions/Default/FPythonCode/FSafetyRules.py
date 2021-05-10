
"""----------------------------------------------------------------------------
MODULE
    FSafetyRules - Create custom safety rules.

    (c) Copyright 2013 by SunGard FRONT ARENA. All rights reserved.
 ---------------------------------------------------------------------------"""

import acm
   
""" Create safety rule using qExtraSafety extension attribute.
"""
def create_extra_safety_rule(setting, data_space):
    return acm.MarketMaking.CreateValueSourceSafetyRule(setting, data_space.GetDataSource('Extra Safety Status'))


    
""" Return True if instrument is an option; otherwise False.
"""
def is_option(factory):
    return factory.Instrument().IsKindOf('FOption')

""" Return True if instrument is a barrier; otherwise False.
"""    
def is_barrier_instrument(instrument, include_legs):
    if instrument.IsKindOf('FOption'):
        return instrument.IsBarrier()
    if include_legs and instrument.IsKindOf('FCombination'):
        legs = instrument.Instruments()
        for leg in legs:
            if is_barrier_instrument(leg, True):
                return True
    return False

""" Return True if instrument is a barrier; otherwise False.
"""           
def is_barrier(factory):
    return is_barrier_instrument(factory.Instrument(), False)

""" Return True if instrument or any of its legs is a barrier; 
    otherwise False.
"""        
def is_barrier_ex(factory):
    return is_barrier_instrument(factory.Instrument(), True)

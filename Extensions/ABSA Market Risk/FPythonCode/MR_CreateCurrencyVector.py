
"""----------------------------------------------------------------------------
MODULE
    MR_CreateCurrencyVector - Module that creates a currency parameter

    (c) Copyright 2015 SunGard FRONT ARENA. All rights reserved.

DESCRIPTION
    This module creates a currency vector as an FNamedParameter

----------------------------------------------------------------------------"""

import acm

def create_named_param(vector, name, obj):
    param = acm.FNamedParameters();
    param.AddParameter(name, obj)
    vector.Add(param)

def create_currency_vector(items):
    vector = acm.FArray()
    for i in items:
        create_named_param(vector, 'currency', i)        
    return vector

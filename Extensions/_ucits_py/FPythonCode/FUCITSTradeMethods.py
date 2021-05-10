""" Compiled: 2020-09-18 10:38:55 """

#__src_file__ = "extensions/UCITS/etc/FUCITSTradeMethods.py"
"""-------------------------------------------------------------------------------------------------------
MODULE
    FUCITSTradeMethods

    (c) Copyright 2015 SunGard FRONT ARENA. All rights reserved.

DESCRIPTION

-------------------------------------------------------------------------------------------------------"""

import FUCITSHooks
from FUCITSInstrumentMethods import UCITSValuationIssuer

NO_ISSUER_OR_COUNTERPARTY = "No UCITS Issuer Or Counterparty"

def IsIssuerSensitiveFromHook(ins):
    try:
        return FUCITSHooks.IsIssuerSensitive(ins)
    except Exception:
        return None

def IsCounterpartySensitiveFromHook(ins):
    try:
        return FUCITSHooks.IsCounterpartySensitive(ins)
    except Exception:
        return None

def UCITSIssuerOrCounterparty(trade):
    ins = trade.Instrument()
    if IsIssuerSensitiveFromHook(ins):
        return UCITSValuationIssuer(ins)
    elif IsCounterpartySensitiveFromHook(ins):
        return trade.Counterparty()
    else:
        return NO_ISSUER_OR_COUNTERPARTY
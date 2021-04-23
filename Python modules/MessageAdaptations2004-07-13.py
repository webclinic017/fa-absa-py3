"""-----------------------------------------------------------------------------
MODULE	  MessageAdaptations

Version: 1.1

DESCRIPTION

This module is for adding calculated values or extra info to AMBA messages.
It is hooked in the amba.ini file on the Front Arena Server.
Changes to this AEL will only take effect if the AMBA Server Services are restarted.

History:
Date	    	    Who     	    	    	    	    What
2004-04-01  	    Anton van Staden	    	    Added BESA and Midbase info
    	    	    Hardus Jacobs
		    Steyn Basson (CQS)
2004-04-15  	    Anton van Staden	    	    Re-Created AEL for more expandibility.
    	    	    Hardus Jacobs
ENDDESCRIPTION

-----------------------------------------------------------------------------"""

import ael
import string
import sys
import re

def amba_send(e, op):
    list = [["objtype", e.record_type]]
    BESA_Additionals = BESA(e, op)
    MIDBASE_Additionals = MIDBASE(e, op)
    MessageAdaptations = BESA_Additionals + MIDBASE_Additionals + list
    return MessageAdaptations

def BESA(e, op):
    if e.record_type == "Trade":
    	if op != "Delete":
  	    apvar = ael.Instrument[e.insaddr.insaddr].dirty_from_yield(e.value_day, None, None, e.price)
    	    cpvar = ael.Instrument[e.insaddr.insaddr].clean_from_yield(e.value_day, None, None, e.price)
	    covar = ael.Instrument[e.insaddr.insaddr].dirty_from_yield(e.value_day, None, None, e.price)*abs(e.quantity)*10000
    	    BESA_Adaptations = 	[["AllInPrice", `apvar`]] + [["CleanPrice", `cpvar`]] + [["Consideration", `covar`]]
    	    return BESA_Adaptations
	else:
	    BESA_Adaptations = [[]]
	    return BESA_Adaptations
    else:
	BESA_Adaptations = [[]]
	return BESA_Adaptations
	
def MIDBASE(e, op):
    if e.record_type == "Trade":
    	if op != "Delete":
    	    MIDBASE_Adaptations = [["PV", `e.present_value()`]] + [["Nominal", `e.nominal_amount()`]]
	    return MIDBASE_Adaptations
	else:
	    MIDBASE_Adaptations = [[]]
	    return MIDBASE_Adaptations
    else:
	MIDBASE_Adaptations = [[]]
	return MIDBASE_Adaptations

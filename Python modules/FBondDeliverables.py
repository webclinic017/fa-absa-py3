""" Standard_Queries:1.0.0 """

"""----------------------------------------------------------------------------
MODULE
	FBondDeliverables

    	(c) Copyright 2002 Front Capital Systems AB. All rights reserved.

DESCRIPTION
    	This module is used by the ASQL query .App/BondDeliverables in order to
        set the CTD.
----------------------------------------------------------------------------"""
import ael

def SetCTD(i, ins, selection, *rest):
    if selection in ("Yes", "yes", "y") :
    	cbond = ael.Instrument[ins].und_insaddr
	if cbond.und_insaddr == i: return "CTD (Saved)"
	cbond=cbond.clone()
	cbond.und_insaddr = i
	cbond.commit()
    	return "CTD (Saved)"
    else:
    	return "CTD (Unchanged)"

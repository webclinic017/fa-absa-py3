""" AbandonClose:1.0.7 """

"""----------------------------------------------------------------------------
MODULE
	FDMExtend.py - Customer extend module for FDM
	
VERSION
	DRAFT

DESCRIPTION
	This module should include operations that let's the user extend
	some functionality defined in the FDM modules.
	The file at the customer side should be called FDMExtend (in database)
	or FDMExtend and is not delivired by FRONT.
	This file works only as a template for describing the signatures.
        
REQUIREMENTS	
 	
HISTORY
        2001-05-31  Updated to use the new module FDMPosition and handled filtering implemented
                    in module FDMExtend

ENDDESCRIPTION
----------------------------------------------------------------------------"""


# aggregate_pos.py operations
def init_aggregate_filter(inifile, args):
    """ inifile - The name to the given inifile
        args    - A dictionary with parsed arguments
        """
    pass

def include_aggregate_position(prfid, insid):
    """ Return 1 to include and 0 to exclude """
    return 1


# position_maintenance.py operations
def init_position_filter(inifile, args):
    """ inifile - The name to the given inifile
        args    - A dictionary with parsed arguments
        """
    pass

def include_position_position(prfid, insid):
    """ Return 1 to include and 0 to exclude """
    return 1

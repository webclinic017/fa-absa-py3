""" Trade_Allocation:1.2.5 """

'''---------------------------------------------------------------------------------
 MODULE
     MessageAdaptationsTemplate - Includes all modifications of messages in AMBA.

     (c) Copyright 2000 by Front Capital Systems AB. All rights reserved.

 DESCRIPTION
     This module is intended to be modified at customer site. It should perform all
     message modifications necessary in the AMBA, either using functions in this
     module or in functions called in other modules. All message modifications
     defined by Front Capital Systems are included in the FMessageAdaptations module.
     FMessageAdaptions should not be modified and is overwritten for every new
     release of AMBA.

 REFERENCES
     Regular expressions in python:

     http://www.python.org/doc/current/lib/module-re.html

 ENDDESCRIPTION
---------------------------------------------------------------------------------'''
import FMessageAdaptations


def receiver_modify(m):

    message = FMessageAdaptations.receiver_modify(m)

    return message

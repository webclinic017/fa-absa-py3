""" Compiled: 2020-09-18 10:38:51 """

#__src_file__ = "extensions/corp_actions/etc/FCopyCorpAction.py"
#----------------------------------------------------------------------------
#    (c) Copyright 2020 SunGard Front Arena. All rights reserved.
#----------------------------------------------------------------------------
"""----------------------------------------------------------------------------
MODULE
    FCopyCorpAction - GUI Module to copy to a new corporate action definition.

DESCRIPTION
----------------------------------------------------------------------------"""

import acm
import FBDPGui
import importlib
importlib.reload(FBDPGui)
import FOpenCorpAction
import FCorpActionGuiCommon
importlib.reload(FCorpActionGuiCommon)

ael_variables = FCorpActionGuiCommon.ael_variables
ael_variables.Name[8] = FCorpActionGuiCommon.name_copy_cb

ael_gui_parameters = FBDPGui.makeGuiParameters(
        windowCaption='Copy Corporate action')

def ael_main(d):
    ca = acm.FCorporateAction[int(d['Oid'])].Clone()
    FOpenCorpAction.run_main(d, ca)

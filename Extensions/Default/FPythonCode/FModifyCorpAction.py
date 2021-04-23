""" Compiled: 2020-09-18 10:38:51 """

#__src_file__ = "extensions/corp_actions/etc/FModifyCorpAction.py"
#----------------------------------------------------------------------------
#    (c) Copyright 2020 SunGard Front Arena. All rights reserved.
#----------------------------------------------------------------------------
"""----------------------------------------------------------------------------
MODULE
    FModifyCorpAction - GUI Module to modify a corporate action definition.

DESCRIPTION
----------------------------------------------------------------------------"""


import acm
import ael
import FBDPGui
import importlib
importlib.reload(FBDPGui)
import FOpenCorpAction
import FCorpActionGuiCommon
importlib.reload(FCorpActionGuiCommon)

ael_variables = FCorpActionGuiCommon.ael_variables
ael_variables.Name[8] = FCorpActionGuiCommon.name_cb
ael_gui_parameters = FBDPGui.makeGuiParameters(
        windowCaption='Modify Corporate Action')

def ael_main(d):
    ca = acm.FCorporateAction[int(d['Oid'])]
    FOpenCorpAction.run_main(d, ca)

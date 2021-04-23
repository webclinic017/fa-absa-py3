""" Compiled: 2020-09-18 10:38:51 """

#__src_file__ = "extensions/corp_actions/etc/FNewCorpAction.py"
#----------------------------------------------------------------------------
#    (c) Copyright 2020 SunGard Front Arena. All rights reserved.
#----------------------------------------------------------------------------
"""----------------------------------------------------------------------------
MODULE
    FNewCorpAction - GUI Module to create a new corporate action definition.

DESCRIPTION
----------------------------------------------------------------------------"""


import acm
import FBDPGui
import importlib
importlib.reload(FBDPGui)
import FOpenCorpAction
import FCorpActionGuiCommon
importlib.reload(FCorpActionGuiCommon)

ael_gui_parameters = FBDPGui.makeGuiParameters(
        windowCaption='New Corporate Action')

ael_variables = FCorpActionGuiCommon.ael_variables

def ael_main(d):
    ca = None
    try:
        ca = acm.FCorporateAction[d['Name']]
    except Exception:
        pass

    if not ca:
        ca = acm.FCorporateAction()
    FOpenCorpAction.run_main(d, ca)

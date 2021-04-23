""" Compiled: 2020-09-18 10:38:49 """

#__src_file__ = "extensions/advanced_corporate_actions/./etc/FNewCorpActChoice.py"
"""----------------------------------------------------------------------------
MODULE
    FNewCorpActChoice - GUI Module to create to a new corporate action 
    Choice definition.

DESCRIPTION
----------------------------------------------------------------------------"""

import acm
import FBDPGui
import importlib
importlib.reload(FBDPGui)
import FOpenCorpActChoice
importlib.reload(FOpenCorpActChoice)
import FModifyCorpActChoice
importlib.reload(FModifyCorpActChoice)
import FBDPCurrentContext

ael_gui_parameters = FBDPGui.makeGuiParameters(
        windowCaption='New Corporate Action Choice')

ael_variables = FModifyCorpActChoice.ael_variables

if FBDPCurrentContext.ChoiceGUIUpdater():
    FBDPCurrentContext.ChoiceGUIUpdater()(ael_variables)

def ael_main(d):
    caChoice = None
    try:
        caChoice = acm.FCorporateActionChoice[int(d['Oid'])]
    except Exception:
        pass

    if not caChoice:
        caChoice = acm.FCorporateActionChoice()
    FOpenCorpActChoice.run_main(d, caChoice)

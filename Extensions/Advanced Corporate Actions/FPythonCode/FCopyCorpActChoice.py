""" Compiled: 2020-09-18 10:38:49 """

#__src_file__ = "extensions/advanced_corporate_actions/./etc/FCopyCorpActChoice.py"
"""----------------------------------------------------------------------------
MODULE
    FCopyCorpActChoice - GUI Module to copy to a new corporate action 
    Choice definition.

DESCRIPTION
----------------------------------------------------------------------------"""

import acm
import FBDPGui
import importlib
importlib.reload(FBDPGui)
import FOpenCorpActChoice

import FCorpActionChoiceGuiCommon

ael_variables = FCorpActionChoiceGuiCommon.ael_variables

FBDPGui.createAdditionalInfoVariables(ael_variables, FCorpActionChoiceGuiCommon.ADDITIONALINFO_RECORDTYPE)

ael_gui_parameters = FBDPGui.makeGuiParameters(
        windowCaption='Copy Corporate Action Choice')

def ael_main(d):
    caChoice = acm.FCorporateActionChoice[int(d['Oid'])].Clone()
    FOpenCorpActChoice.run_main(d, caChoice, 1)


""" Compiled: 2020-09-18 10:38:49 """

#__src_file__ = "extensions/advanced_corporate_actions/./etc/FModifyCorpActChoice.py"
"""----------------------------------------------------------------------------
MODULE
    FModifyCorpActChoice - GUI Module to modify a corporate action 
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
        windowCaption='Modify Corporate Action Choice')
        
def ael_main(d):
    choice = acm.FCorporateActionChoice[int(d['Oid'])]
    FOpenCorpActChoice.run_main(d, choice)

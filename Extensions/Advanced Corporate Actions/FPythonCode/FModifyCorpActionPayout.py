""" Compiled: 2020-09-18 10:38:49 """

#__src_file__ = "extensions/advanced_corporate_actions/./etc/FModifyCorpActionPayout.py"
"""----------------------------------------------------------------------------
MODULE
    FModifyCorpActionPayout - GUI Module to modify a corporate action 
    Payout definition.

DESCRIPTION
----------------------------------------------------------------------------"""

import acm
import FBDPGui
import importlib
importlib.reload(FBDPGui)
import FCorpActionPayoutGuiCommon
import FOpenCorpActionPayout

ael_variables = FCorpActionPayoutGuiCommon.ael_variables
    

ael_gui_parameters = FBDPGui.makeGuiParameters(
        windowCaption='Modify Corporate Action Payout')
        
def ael_main(d):
    payout = acm.FCorporateActionPayout[int(d['Oid'])]
    FOpenCorpActionPayout.run_main(d, payout)

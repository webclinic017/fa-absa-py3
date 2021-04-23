""" Compiled: 2020-09-18 10:38:49 """

#__src_file__ = "extensions/advanced_corporate_actions/./etc/FModifyCorpActionElection.py"
"""----------------------------------------------------------------------------
MODULE
    FModifyCorpActionElection - GUI Module to a modify corporate action 
    election definition.

DESCRIPTION
----------------------------------------------------------------------------"""

import acm
import FBDPGui
import importlib
importlib.reload(FBDPGui)
import FOpenCorpActionElection
import FCorpActionElectionGuiCommon

ael_variables = FCorpActionElectionGuiCommon.ael_variables

ael_gui_parameters = FBDPGui.makeGuiParameters(
        windowCaption='Modify Corporate Action Election')
        
def ael_main(d):
    election = acm.FCorporateActionElection[int(d['Oid'])]
    FOpenCorpActionElection.run_main(d, election)    

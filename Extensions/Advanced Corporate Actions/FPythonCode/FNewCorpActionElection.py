""" Compiled: 2020-09-18 10:38:49 """

#__src_file__ = "extensions/advanced_corporate_actions/./etc/FNewCorpActionElection.py"
"""----------------------------------------------------------------------------
MODULE
    FNewCorpActionElection - GUI Module to create to a corporate action 
    election definition.

DESCRIPTION
----------------------------------------------------------------------------"""

import acm
import FBDPGui
import importlib
importlib.reload(FBDPGui)
import FOpenCorpActionElection
importlib.reload(FOpenCorpActionElection)
import FModifyCorpActionElection
importlib.reload(FModifyCorpActionElection)
import FBDPCurrentContext


ael_gui_parameters = FBDPGui.makeGuiParameters(
        windowCaption='New Corporate Action Election')

ael_variables = FModifyCorpActionElection.ael_variables


if FBDPCurrentContext.ElectionGUIUpdater():
    FBDPCurrentContext.ElectionGUIUpdater()(ael_variables)


def ael_main(d):
    caElection = None
    try:
        caElection = acm.FCorporateActionElection[int(d['Oid'])]
    except Exception:
        pass

    if not caElection:
        caElection = acm.FCorporateActionElection()
    FOpenCorpActionElection.run_main(d, caElection, 1)

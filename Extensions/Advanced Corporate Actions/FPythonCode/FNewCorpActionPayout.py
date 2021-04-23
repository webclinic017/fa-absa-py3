""" Compiled: 2020-09-18 10:38:49 """

#__src_file__ = "extensions/advanced_corporate_actions/./etc/FNewCorpActionPayout.py"
"""----------------------------------------------------------------------------
MODULE
    FNewCorpActionPayout - GUI Module to create to a new corporate action 
    Payout definition.

DESCRIPTION
----------------------------------------------------------------------------"""

import acm
import FBDPGui
import importlib
importlib.reload(FBDPGui)
import FOpenCorpActionPayout
importlib.reload(FOpenCorpActionPayout)
import FModifyCorpActionPayout
importlib.reload(FOpenCorpActionPayout)
import FBDPCurrentContext

ael_gui_parameters = FBDPGui.makeGuiParameters(
        windowCaption='New Corporate Action Payout')

ael_variables = FModifyCorpActionPayout.ael_variables

if FBDPCurrentContext.PayoutGUIUpdater():
    FBDPCurrentContext.PayoutGUIUpdater()(ael_variables)

def ael_main(d):
    caPayout = None
    try:
        caPayout = acm.FCorporateActionPayout[int(d['Oid'])]
    except Exception:
        pass

    if not caPayout:
        caPayout = acm.FCorporateActionPayout()
    FOpenCorpActionPayout.run_main(d, caPayout)
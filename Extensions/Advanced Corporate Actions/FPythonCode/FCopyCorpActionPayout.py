""" Compiled: 2020-09-18 10:38:49 """

#__src_file__ = "extensions/advanced_corporate_actions/./etc/FCopyCorpActionPayout.py"
"""----------------------------------------------------------------------------
MODULE
    FCopyCorpActionPayout - GUI Module to copy to a new corporate action 
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

FBDPGui.createAdditionalInfoVariables(ael_variables, FCorpActionPayoutGuiCommon.ADDITIONALINFO_RECORDTYPE)

ael_gui_parameters = FBDPGui.makeGuiParameters(
        windowCaption='Copy Corporate Action Payout')

def ael_main(d):
    caPayout = acm.FCorporateActionPayout[int(d['Oid'])].Clone()
    FOpenCorpActionPayout.run_main(d, caPayout)

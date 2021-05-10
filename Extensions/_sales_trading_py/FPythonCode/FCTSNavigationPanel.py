""" Compiled: 2020-09-18 10:38:54 """

#__src_file__ = "extensions/SalesTrading/./etc/FCTSNavigationPanel.py"
"""-------------------------------------------------------------------------------------------------------
MODULE
    FCTSNavigationPanel

    (c) Copyright 2014 SunGard FRONT ARENA. All rights reserved.

DESCRIPTION

-------------------------------------------------------------------------------------------------------"""

from FInstrumentNavigationPanel import InstrumentNavigationPanel
from FCounterPartyNavigationPanel import CounterPartyNavigationPanel

class CTSBondNavigationPanel(InstrumentNavigationPanel):
    pass

class CTSMarketMakerNavigationPanel(InstrumentNavigationPanel):
    pass

class CTSClientNavigationPanel(CounterPartyNavigationPanel):
    pass

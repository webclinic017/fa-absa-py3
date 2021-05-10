""" Compiled: 2020-09-18 10:38:55 """

#__src_file__ = "extensions/BrokerageRisk/etc/FBrokerageRiskExtensionPoints.py"
"""--------------------------------------------------------------------------
MODULE
    BrokerageRisk

    (c) Copyright 2016 SunGard FRONT ARENA. All rights reserved.

DESCRIPTION

-----------------------------------------------------------------------------"""

import acm

def FindClient(party):
    # Iterate "upwards" through the Parent() link; stop at first FClient (or None)
    return party if party == None or party.Class() == acm.FClient else FindClient( party.Parent() )
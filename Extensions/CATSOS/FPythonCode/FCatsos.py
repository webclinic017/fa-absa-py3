"""----------------------------------------------------------------------------
MODULE
    FCatsos- CATSOS Market Making specific.

    (c) Copyright 2011 by SunGard FRONT ARENA. All rights reserved.
 ---------------------------------------------------------------------------"""
import acm

""" Reject a quote request for an order book.
"""
def rejectQuoteRequest(mei):
    selected = mei.ExtensionObject().ActiveSheet().Selection().SelectedQuoteControllers()
    for controller in selected:
        controller.UI().RejectQuoteRequest()

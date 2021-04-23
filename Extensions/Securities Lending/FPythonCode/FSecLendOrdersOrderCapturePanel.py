""" Compiled: 2020-09-18 10:38:55 """

#__src_file__ = "extensions/SecuritiesLending/etc/FSecLendOrdersOrderCapturePanel.py"

"""--------------------------------------------------------------------------
MODULE
    FSecLendOrdersOrderCapturePanel

    (c) Copyright 2017 FIS FRONT ARENA. All rights reserved.

DESCRIPTION
    Order Manager - This panel can be overriten to support Custom Order Capture GUI fields
 
-----------------------------------------------------------------------------"""
import acm
from FSecLendOrderCapturePanelBase import SecLendOrderCapturePanelBase

class SecLendOrdersOrderCapturePanel(SecLendOrderCapturePanelBase):

    def ExtendLayout(self, uxlb):
        """
        uxlb.      BeginVertBox('SecLenExt', 'Extra')
            ..custom layout
        uxlb.      AddSpace(10)
        uxlb.      EndBox()
        """
        pass

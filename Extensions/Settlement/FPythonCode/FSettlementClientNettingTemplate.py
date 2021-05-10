""" Compiled: 2020-09-18 10:38:49 """

#__src_file__ = "extensions/settlement/etc/FSettlementClientNettingTemplate.py"
"""
Template file for client netting purposes. Copy this file and save the copy as FSettlementClientNetting.

Adding or changing any of these hooks require a restart of the settlement ATS for it to take affect.
"""

import FOperationsUtils as Utils

def client_netting_1(settlement):
    """
    Input-parameter settlement is of type acm.FSettlement
    The client netting function shall return either True or False.
    """
    return True

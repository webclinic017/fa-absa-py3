# coding=ascii
"""
Brendan Bosman      MINT-164.3      2015/09/01      1. Created as part of a refactoring process of TriResolve_EMIR.py
Brendan Bosman      MINT-366        2015/09/15      Implement Non EU files



Main Purpose:
1. Class declarations of MidasDualKeyTradesCollection



To the developers working on this file:
1. This file was taken rom FA where tabsstop was equal to 8 spaces. In FA, most of the indention was 4 space, so
   reading the outside of FA was difficult if tabstop was not 8 spaces. Please be aware of this
2. Going forward, all indentions are 4 spaces, but tabstop is still 8
"""

from TriResolve_EMIR_Functions import *

from TriResolve_EMIR_Const import *


class MidasDualKeyTradesCollection(object):
    """Contains MIDAS DUAL KEY trades.

    1. Keeep a list of all trades with a certain counter party
    2. Keep a list off all midas id's, with all subtrades associated with it
    """

    def __init__(self):
        """

        :return:
        """
        print("Loading", MDK_CPTY_NAME, "trades.")
        self.trades = acm.FTrade.Select('counterparty=' + MDK_CPTY_NAME)
        self.trades_by_midas_id = {}
        for trade in self.trades:
            midas_id = get_midas_id(trade)
            if midas_id:
                subtrades = self.trades_by_midas_id.setdefault(midas_id, [])
                subtrades.append(trade)

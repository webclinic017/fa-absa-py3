"""---------------------------------------------------------------------------------------------------------------------
MODULE
    CMMT5XXSTPHook

DESCRIPTION
    This module contains STP logic for MT5XX Capital Markets trades.

------------------------------------------------------------------------------------------------------------------------
HISTORY
========================================================================================================================
Date            Change no       Developer               Requester               Description
------------------------------------------------------------------------------------------------------------------------
2019-05-27      FAOPS-488       Tawanda Mukhalela       Wandile Sithole         STP for MT5xx trades CM.
------------------------------------------------------------------------------------------------------------------------
"""

import acm

import OperationsSTPFunctions
from OperationsSTPHook import OperationsSTPHook


class CMMT5XXSTPHook(OperationsSTPHook):

    def Name(self):
        """
        Get the name of the Operations STP Hook.
        """
        return 'Capital Markets MT5XX Auto Release STP Hook'
    
    def IsTriggeredBy(self, eventObject):
        """
        Only trigger for :

            Instrument Type Bond, Bill, FRN, Repo/Reverse, IndexLinkedBond, CLN, BuySellback, Collateral
            status is FO Confirmed
            Settlement Type = Security Norminal, End Security
            trade SettleCategory Name is SA_CUSTODIAN            
        """

        # Check if updated object is a settlement
        if not eventObject.IsKindOf(acm.FSettlement):
            return False
        settlement = eventObject

        if not settlement.Instrument():
            return False

        # Only release settlements in Authorised status
        if settlement.Status() != 'Authorised':
            return False

        instrument = settlement.Instrument()
        trade = settlement.Trade()
        
        if instrument.InsType() in ("Bond", "Bill", "FRN", "Repo/Reverse",
                                    "IndexLinkedBond", "Combination", "BuySellback", "Collateral") \
                and instrument.Currency().Name() == 'ZAR':
            if trade.Counterparty().AddInfoValue("UnexCor Code"):
                if trade.Counterparty().AddInfoValue("BESA_Member_Agree") in ("Yes",
                                                                              "Exempt - Member",
                                                                              "Exempt - Agent",
                                                                              "Exempt - BookBuild",
                                                                              "Exempt - Subsidiary",
                                                                              "Temporarily Allowed"
                                                                              ):
                    if trade.SettleCategoryChlItem():
                        if trade.SettleCategoryChlItem().Name() == 'SA_CUSTODIAN':
                            if settlement.Type() in ('Security Nominal', 'End Security'):
                                return True
                            
        return False

    def PerformSTP(self, settlement):
        """
        Changing settlement status to acknowledged.
        """
        OperationsSTPFunctions.acknowledge_settlement(settlement)
        
    

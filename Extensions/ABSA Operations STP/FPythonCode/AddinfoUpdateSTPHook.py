'''----------------------------------------------------------------------------------------------------------------------------------
MODULE
    AddinfoUpdateSTPHook

DESCRIPTION
    This module contains a hook for STP (straight-through-processing) triggered by 
    the booking or an update of an acm object. It will update a specified addinfo 
    field of the object with a given value, based on said object's specific characteristics.

-------------------------------------------------------------------------------------------------------------------------------------
HISTORY
=====================================================================================================================================
Date            Change no       Developer               Requester               Description
-----------------------------------------------------------------------------------------------------------------------------------------
2020-10-06      PCGDEV-572      Qaqamba Ntshobane       Daveshin Chetty         Update default T-bill addinfo with correct value 
2020-11-06      PCGDEV-318      Qaqamba Ntshobane       Daveshin Chetty         Update InsOverride to ETN for ETNs booked as ETFs

-------------------------------------------------------------------------------------------------------------------------------------
'''
import acm
import OperationsSTPFunctions
from OperationsSTPHook import OperationsSTPHook


class TBillAddinfoUpdateSTPHook(OperationsSTPHook):
    '''
    Definition of a hook used to update a trade's addinfo value
    based on the trade's features.
    '''
    tbill_prf_names = ('Nigeria FI', 'Africa_Bonds', 'Africa_MM', 'Treasury Hedging', 'Non-Presence FI')

    def Name(self):
        '''
        Get the name of the Operations STP Hook.
        '''
        return 'T-Bill AddInfo Update Hook'

    def IsTriggeredBy(self, trade_object):
        '''
        Determine whether or not to trigger the hook's STP action
        based on the trade's features
        '''
        if not trade_object.IsKindOf(acm.FTrade):
            return False

        if self._is_bill_update(trade_object):
            return True
        return False

    def PerformSTP(self, trade_object):
        '''
        Update the trade's addinfo
        '''
        OperationsSTPFunctions.set_additional_info_value(trade_object, 'MM_Instype', 'TB')
        trade_object.Commit()

    def _is_bill_update(self, trade):

        if trade.Instrument().InsType() != 'Bill':
            return False 
        if trade.Acquirer().Name() != 'AFRICA DESK':
            return False
        if trade.Currency().Name() not in ('NGN', 'EGP', 'GHS'):
            return False
        if trade.Portfolio().Name() not in self.tbill_prf_names:
            return False
        if trade.add_info('MM_Instype') == 'TB':
            return False
        return True


class ETNAddinfoUpdateSTPHook(OperationsSTPHook):
    '''
    Definition of a hook used to update an ETN's addinfo value
    based on the trade's features.
    '''
    etn_ins_names = ('ZAR/SLV', 'ZAR/NEWUSD', 'ZAR/NEWEUR', 'ZAR/NEWPLT', 'ZAR/NEWSLV', 'ZAR/NEWGBP')

    def Name(self):
        '''
        Get the name of the Operations STP Hook.
        '''
        return 'ETN AddInfo Update Hook'

    def IsTriggeredBy(self, trade_object):
        '''
        Determine whether or not to trigger the hook's STP action
        based on the trade's features
        '''
        if not trade_object.IsKindOf(acm.FTrade):
            return False

        elif self._is_etn_update(trade_object):
            return True
        return False

    def PerformSTP(self, trade_object):
        '''
        Update the trade's addinfo
        '''
        OperationsSTPFunctions.set_additional_info_value(trade_object, 'InsOverride', 'ETN')
        trade_object.Commit()

    def _is_etn_update(self, trade):

        instrument = trade.Instrument()

        if instrument.InsType() != 'ETF':
            return False
        if instrument.Name() not in self.etn_ins_names:
            return False
        if trade.add_info('InsOverride') == 'ETN':
            return False
        return True

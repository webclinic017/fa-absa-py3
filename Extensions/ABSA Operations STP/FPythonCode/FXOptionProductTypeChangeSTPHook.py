"""--------------------------------------------------------------------------------------------------------------------------------------
MODULE
    FXOptionProductTypeChangeSTPHook

DESCRIPTION
    This module contains a hook for STP (straight-through-processing) triggered
    by the changing of an FX Option product type or the creation/update of a trade
    that is out of sync with the instrument's product type.

-----------------------------------------------------------------------------------------------------------------------------------------
HISTORY
=========================================================================================================================================
Date            Change no       Developer               Requester               Description
-----------------------------------------------------------------------------------------------------------------------------------------
2019-05-05      FAOPS-775       Cuen Edwards            Kgomotso Gumbo          Behaviour migrated from task.
2020-06-18      FAOPS-818       Cuen Edwards            Kgomotso Gumbo          Added support for trade events to remove reliance on book
                                                                                ing order.
-----------------------------------------------------------------------------------------------------------------------------------------
"""

import acm

from at_logging import getLogger
from OperationsSTPHook import OperationsSTPHook


LOGGER = getLogger(__name__)

PRODUCT_CODE_BY_PRODUCT_TYPE = {
    'Calendar Spread': '9CS',
    'Call Spread': '9CSP',
    'Collar': '9ZCC',
    'Collar Plus': '9CP',
    'Custom': '9CUST',
    'EDD Cancellation': '9EDDC',
    'EDD Cancellation Flat Forward': '9EDDCFF',
    'EDD Cancellation of Synthetic Forward': '9EDDCSF',
    'EDD extension of Flat Forward': '9EDDF',
    'EDD extension of Synthetic Forward': '9EDDSF',
    'EDD Extention': '9EDDE',
    'Flat Forward': '9FF',
    'Forward': '9FWD',
    'Forward Enhancer Plus': '9FEP',
    'Forward Plus': '9FP',
    'Forward Spread': '9FS',
    'Geared Collar': '9GC',
    'Geared Collar Plus': '9GCP',
    'Geared Extendable Forward': '9GEF',
    'Geared Forward': '9GF',
    'Geared Forward Plus': '9GFP',
    'Geared Forward Spreads': '9GFS',
    'Knock in Forwards': '9KI',
    'Knock out Forwards': '9KO',
    'Leveraged Forward': '9LF',
    'Limited Protection Forward': '9MPF',
    'Put Spread': '9PSP',
    'Straddle': '9STRD',
    'Strangle': '9STRNG',
    'Synthetic Forward': '9SF'
}

INCLUDED_TRADE_STATUSES = [
    'FO Confirmed',
    'BO Confirmed',
    'BO-BO Confirmed'
]

INCLUDED_PORTFOLIO_NAMES = [
    'Africa_Curr',
    'Exotic Opt',
    'LTNZ',
    'LTNZ_4Front',
    'VOE'
]


class FXOptionProductTypeChangeSTPHook(OperationsSTPHook):
    """
    Definition of a hook used to perform STP triggered by the
    changing of an FX Option product type.
    """

    def Name(self):
        """
        Get the name of the Operations STP Hook.
        """
        return 'FX Option Product Type Change STP Hook'

    def IsTriggeredBy(self, eventObject):
        """
        Determine whether or not to trigger the hooks STP action/s
        for an event on the specified object.
        """
        if eventObject.IsKindOf(acm.FInstrument):
            return self._is_triggered_by_instrument(eventObject)
        elif eventObject.IsKindOf(acm.FTrade):
            return self._is_triggered_by_trade(eventObject)
        return False

    def PerformSTP(self, eventObject):
        """
        Perform the hooks STP action/s for an event on the specified
        object.

        Please note that the action does not necessarily occur to the
        event object itself but may occur to some related object/s.
        """
        if eventObject.IsKindOf(acm.FInstrument):
            self._perform_stp_for_instrument(eventObject)
        elif eventObject.IsKindOf(acm.FTrade):
            self._perform_stp_for_trade(eventObject)
        else:
            # We should never get here - this is a defensive check.
            raise ValueError('Unexpected event object {event_object_class} {event_object_oid} specified.'.format(
                event_object_class=eventObject.ClassName(),
                event_object_oid=eventObject.Oid()
            ))

    @classmethod
    def _is_triggered_by_instrument(cls, instrument):
        """
        Determine whether or not to trigger the hooks STP actions
        for an event on the specified instrument.
        """
        if cls._is_excluded_instrument(instrument):
            return False
        return cls._has_trades_requiring_update(instrument)

    @classmethod
    def _is_triggered_by_trade(cls, trade):
        """
        Determine whether or not to trigger the hooks STP actions
        for an event on the specified trade.
        """
        if cls._is_excluded_instrument(trade.Instrument()):
            return False
        if cls._is_excluded_trade(trade):
            return False
        return cls._is_trade_requiring_update(trade)

    @classmethod
    def _is_excluded_instrument(cls, instrument):
        """
        Determine whether or not the specified instrument should be
        excluded from the hooks STP action.
        """
        if instrument.InsType() != 'Option':
            return True
        if instrument.UnderlyingType() != 'Curr':
            return True
        if instrument.ExpiryDateOnly() < acm.Time.DateToday():
            return True
        return False

    @classmethod
    def _has_trades_requiring_update(cls, instrument):
        """
        Determine whether or not the specified instrument has trades
        with approximate load values that need to be updated to match
        the instruments product type.
        """
        values_by_add_info = cls._get_values_by_add_info(instrument)
        for trade in cls._get_trades_to_update(instrument, values_by_add_info):
            return True
        return False

    @classmethod
    def _is_trade_requiring_update(cls, trade):
        """
        Determine whether or not the specified trade has approximate
        load values that need to be updated to match the trade
        instruments product type.
        """
        values_by_add_info = cls._get_values_by_add_info(trade.Instrument())
        return cls._is_add_info_update_required(trade, values_by_add_info)

    @classmethod
    def _is_excluded_trade(cls, trade):
        """
        Determine whether or not the specified trade should be
        excluded from the hooks STP action.
        """
        if trade.Status() not in INCLUDED_TRADE_STATUSES:
            return True
        if trade.Portfolio().Name() not in INCLUDED_PORTFOLIO_NAMES:
            return True
        return False

    @classmethod
    def _perform_stp_for_instrument(cls, instrument):
        """
        Perform the hooks STP actions for an event on the specified
        instrument.
        """
        values_by_add_info = cls._get_values_by_add_info(instrument)
        for trade in cls._get_trades_to_update(instrument, values_by_add_info):
            cls._update_add_infos(trade, values_by_add_info)

    @classmethod
    def _perform_stp_for_trade(cls, trade):
        """
        Perform the hooks STP actions for an event on the specified
        trade.
        """
        values_by_add_info = cls._get_values_by_add_info(trade.Instrument())
        cls._update_add_infos(trade, values_by_add_info)

    @classmethod
    def _get_trades_to_update(cls, instrument, values_by_add_info):
        """
        Get the trades for an instrument that need to be updated to
        match the specified approximate load additional info values.
        """
        for trade in instrument.Trades().AsArray():
            if cls._is_excluded_trade(trade):
                continue
            if cls._is_add_info_update_required(trade, values_by_add_info):
                yield trade

    @classmethod
    def _get_values_by_add_info(cls, instrument):
        """
        Determine the approximate load additional info values to
        associate with the specified instruments trades based its
        current state.
        """
        approx_load = None
        approx_load_ref = None
        ins_override = None
        product_code = cls._get_product_code(instrument)
        if product_code is not None:
            approx_load = True
            approx_load_ref = product_code
            ins_override = 'Combination - FX option'
        return {
            'Approx. load': approx_load,
            'Approx. load ref': approx_load_ref,
            'InsOverride': ins_override
        }

    @staticmethod
    def _get_product_code(instrument):
        """
        Get the product code to associate with the specified
        instruments trades based on its current state.
        """
        if instrument.ProductTypeChlItem() is None:
            return None
        product_type = instrument.ProductTypeChlItem().Name()
        product_code = PRODUCT_CODE_BY_PRODUCT_TYPE.get(product_type)
        if product_code is None:
            raise ValueError("No product code defined for product type '{product_type}'.".format(
                product_type=product_type
            ))
        return product_code

    @staticmethod
    def _is_add_info_update_required(trade, values_by_add_info):
        """
        Determine whether or not the approximate load additional infos
        for a trade need to be updated.
        """
        for add_info, value in list(values_by_add_info.items()):
            if trade.AddInfoValue(add_info) != value:
                return True
        return False

    @staticmethod
    def _update_add_infos(trade, values_by_add_info):
        """
        Update the approximate load additional infos for a trade to
        the specified values.
        """
        LOGGER.info("Updating approximate load additional infos for trade {trade_oid}".format(
            trade_oid=trade.Oid()
        ))
        trade = trade.StorageImage()
        for add_info, value in list(values_by_add_info.items()):
            trade.AddInfoValue(add_info, value)
            LOGGER.info("- Setting '{add_info}' to '{value}'".format(
                add_info=add_info,
                value=value
            ))
        trade.Commit()

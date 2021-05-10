"""
A module which contains functions for getting the desired instances
of objects representing individual prime brokerage funds
and saving them into the persistent storage.
"""

from pb_fund_interface import PrimeBrokerageFund
from pb_storage_fund import PrimeBrokerageFundStorage


_PBFUND_INSTANCE_CACHE = {}
_PBFUND_STORAGE = PrimeBrokerageFundStorage()
_PBFUND_STORAGE.load()


def get_pb_fund(fund_id):
    """
    Return either a new instance of the class
    representing the prime brokerage fund
    or an existing instance (if it has already been instantiated).
    """
    if fund_id in _PBFUND_INSTANCE_CACHE:
        instance = _PBFUND_INSTANCE_CACHE[fund_id]
    elif fund_id in _PBFUND_STORAGE.stored_funds:
        instance = _PBFUND_STORAGE.load_fund(fund_id)
        _PBFUND_INSTANCE_CACHE[fund_id] = instance
    else:
        instance = PrimeBrokerageFund(fund_id)
        _PBFUND_STORAGE.save_fund(instance)
        _PBFUND_INSTANCE_CACHE[fund_id] = instance
        _PBFUND_STORAGE.save()
    return instance


def save_pb_fund(pb_fund):
    """
    Save the provided prime brokerage fund into the persistent storage.
    """
    _PBFUND_STORAGE.save_fund(pb_fund)


def get_stored_funds():
    """
    Yield the instances of the PrimeBrokerageFund class
    representing each of the stored prime brokerage funds.

    Use the caching generator function
    and do not necessarily create new instances.
    """
    for fund_id in _PBFUND_STORAGE.stored_funds:
        yield get_pb_fund(fund_id)

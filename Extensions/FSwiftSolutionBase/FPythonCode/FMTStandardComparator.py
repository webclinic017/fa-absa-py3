"""----------------------------------------------------------------------------
MODULE:
    FMTStandardComparator

DESCRIPTION:
    Standard comparator functions for comparison. The entry of the function
    needs to be made in FParameter. Function should follow the prototype
    func_name(their_object, our_object, arguments, attribute_to_check)

FUNCTIONS:
    precision(theirs, ours, tolerance = 0, attribute = None):
        Compares the attributes for a given tolerance
    ignore_case(theirs, ours, arg = None, attribute = None):
        Performs case insensitive search
    bic_comparator(theirs, ours, arg = None, attribute = None):
        Performs bic comparison by stripping XXX at the end.

VERSION: 3.0.0-0.5.3344
----------------------------------------------------------------------------"""
from decimal import *
import FSwiftReaderLogger
notifier = FSwiftReaderLogger.FSwiftReaderLogger('SwiftReader', 'FSwiftReaderNotifyConfig')

def precision(theirs, ours, tolerance = 0, attribute = None):
    """ return true if our and their value precision is acceptable"""
    is_match = False
    if attribute:
        their_value = getattr(theirs, attribute)()
        our_value = getattr(ours, attribute)()
        if (their_value is not None) and (our_value is not None):
            if isinstance(our_value, float):
                if abs(Decimal(str(our_value)) - Decimal(str(their_value))) <= Decimal(str(tolerance)):
                    is_match = True
            notifier.DEBUG('precision : %s --> Theirs: %s Ours: %s Tolerance: %s isMatch: %r'%(attribute, Decimal(str(their_value)), Decimal(str(our_value)), Decimal(str(tolerance)), is_match))
    return is_match

def ignore_case(theirs, ours, arg = None, attribute = None):
    """ perform case insensitive comparison"""
    is_match = False
    if attribute:
        their_value = getattr(theirs, attribute)()
        our_value = getattr(ours, attribute)()
        if their_value and our_value:
            if their_value.upper() == our_value.upper():
                is_match = True
            notifier.DEBUG('ignore_case : %s --> Theirs: %s Ours: %s isMatch: %r'%(attribute, their_value, our_value, is_match))
        if (their_value is None or their_value == 'None') and (our_value is None or our_value == 'None'):
            is_match = True
    return is_match

def bic_comparator(theirs, ours, arg = None, attribute = None):
    """ perform bic comparison by stripping XXX at the end

        Incoming	    Outgoing	    Match
        --------------------------------------
        HSBCHKHHXXX	    HSBCHKHH	    Yes
        HSBCHKHHXXX	    HSBCHKHHHKH	    No
        HSBCHKHHXXX	    HSBCHKHHXXX	    Yes

        HSBCHKHHHKH	    HSBCHKHHXXX	    No
        HSBCHKHHHKH	    HSBCHKHHHKH	    Yes
        HSBCHKHHHKH	    HSBCHKHH	    No

        HSBCHKHH	    HSBCHKHHXXX	    Yes
        HSBCHKHH	    HSBCHKHH	    Yes
        HSBCHKHH        HSBCHKHHHKH     No
    """

    is_match = False
    if attribute:
        their_value = getattr(theirs, attribute)()
        our_value = getattr(ours, attribute)()
        if their_value and our_value:
            their_value_orig = their_value
            our_value_orig = our_value
            their_value = their_value[:len(their_value) - 3] if their_value.endswith('XXX') else their_value
            our_value = our_value[:len(our_value) - 3] if our_value.endswith('XXX') else our_value
            if their_value.upper() == our_value.upper():
                is_match = True
            notifier.DEBUG('bic_comparator : %s --> Theirs: %s Ours: %s isMatch: %r'%(attribute, their_value_orig, our_value_orig, is_match))
        if (their_value is None or their_value == 'None') and (our_value is None or our_value == 'None'):
            is_match = True
    return is_match


"""----------------------------------------------------------------------------
MODULE
    FMTCustomComparator

DESCRIPTION
    OPEN EXTENSION MODULE.
    Possible to define custom functions for comparisons
    in the Pairing and/or Matching logic. The calling of the function is defined
    in the corresponding FParameters, either FMTnnn_Pair or FMTnnn_Match,
    with function parameters. The function should follow the prototype
    func_name(their_object, our_object, arguments, attribute_to_check)

    # Sample method for customizing precision
    def myprecision(theirs, ours, tolerance = 0, attribute = None):
        is_match = False
        if attribute:
            # Override the tolerance from FParameter
            curr = getattr(theirs, 'Currency')()
            if curr == 'JPY':
                tolerance = 99
            their_value = getattr(theirs, attribute)()
            our_value = getattr(ours, attribute)()
            if abs(float(our_value) - float(their_value)) <= float(tolerance):
                is_match = True
        return is_match

VERSION: 3.0.0-0.5.3344
----------------------------------------------------------------------------"""

'''
# Sample method for customizing precision
def myprecision(theirs, ours, tolerance = 0, attribute = None):
    is_match = False
    if attribute:
        # Override the tolerance from FParameter
        curr = getattr(theirs, 'Currency')()
        if curr == 'JPY':
            tolerance = 99
        their_value = getattr(theirs, attribute)()
        our_value = getattr(ours, attribute)()
        if abs(float(our_value) - float(their_value)) <= float(tolerance):
            is_match = True
    return is_match
'''

"""General helper functions for use in adfl.

These usually have corresponding FCustomFunction definitions.

12-07-2013    conicova    Fixed the distinct function (old version caused problems when called from adfl)
"""
import acm

def filterByFlags(collection, flags, trueValue=True):
    """Filters the collection based on flags."""
    return [item for item, flag in zip(collection, flags) if flag == trueValue]


def distinct(elements):
    """Return distinct elements"""
    # result = list(set(elements)) # !!!this doesn't work
    s = elements.AsSet()
    return s.AsList()

def empty_list_to_zero(elements):
    """Return 0 in case if the provided parameter elements is an empty FVariantArray
    else returns the provided parameter elements"""
    if hasattr(elements, "IsKindOf"):
        if not elements and elements.IsKindOf(acm.FCollection):
            return 0

    return elements

def trim_end(s, to_remove):
    """ Trim at most one of the strings in 'to_remove' parameter
    from the end of string 's' and return the trimmed string.
    """
    result = str(s)
    for item in to_remove:
        if len(item) > 0 and s.find(item) != -1:
            s_list = s.split(item)[:-1]
            result = item.join(s_list)
            result = result.strip()
            break

    return result

import acm
'''================================================================================================
================================================================================================'''
def fetch_receivers():
    from FRoutingParameters import RoutingATSSettings
    from inspect import getmembers, isclass
    # Every nested class in RoutingATSSettings represents a receiver
    receiverClasses = [c for _, c in getmembers(RoutingATSSettings) if isclass(c)]
    receivers = [c.receiverMBName for c in receiverClasses]
    return receivers
'''================================================================================================
================================================================================================'''
def is_member_of_or_same_as(child, parent):
    if parent.IsKindOf(acm.FCompoundPortfolio):
        return is_member_of_compund(child, parent)
    elif parent.IsKindOf(acm.FPhysicalPortfolio):
        return parent == child
    else:
        return False
'''================================================================================================
================================================================================================'''
def is_member_of_compund(child, parent):
    found = False
    for p in parent.SubPortfolios():
        found = is_member_of_or_same_as(child, p)
        if found:
            break
    return found
'''================================================================================================
================================================================================================'''


def GetPairOffParentReference(settlement):
    pairOffReference = None
    if settlement.PairOffParent():
        pairOffReference = settlement.PairOffParent()
    if not pairOffReference:
        for child in settlement.Children():
            pairOffReference = GetPairOffParentReference(child)
            if pairOffReference:
                break
    return pairOffReference

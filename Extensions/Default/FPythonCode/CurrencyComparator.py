
def CurrencyComparator(left, right):
    lvalue = left.Name()
    rvalue = right.Name()
    if lvalue < rvalue:
        return -1
    if lvalue > rvalue:
        return 1
    return 0

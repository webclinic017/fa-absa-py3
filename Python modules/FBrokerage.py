import ael

def broker_fee(t):
    if t.insaddr:
        if t.insaddr.instype in ('Swap', 'FRA'):
            return 0
    else:
        return t.fee

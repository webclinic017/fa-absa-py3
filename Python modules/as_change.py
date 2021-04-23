import ael


def changeqty(temp, trd, *rest):
    t = ael.Trade[trd]
    print('hello')
    t_clone = t.clone()
    t_clone.quantity = t.quantity * -1
    print(t_clone.quantity, t.quantity)
    t_clone.commit()
    return 'suc' #t_clone.quantity



import ael


def test(temp, i, p, *rest):
    p_clone = ael.Instrument[i].historical_prices()[0].new()
    #print dir(ic)
    #p_clone = ael.Price[i].new()
    p_clone.ptynbr = 10
    
    p_clone.bid = p.bid
    p_clone.ask = p.ask
    p_clone.settle = p.settle
    p_clone.last = p.last
    p_clone.day = ael.date_today().add_days(-2)
    p_clone.curr = p.curr
    try:
        p_clone.commit()
        #print 'section commit'
        return 'Success'
    except:
        print('could not commit ', i)
        return 'Failed'
        

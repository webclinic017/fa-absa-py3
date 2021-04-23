import ael, string



def SetPremium(temp, t, prem, *rest):
    trd = ael.Trade[t]
    t_clone = trd.clone()
    t_clone.premium = (float)(prem)
    try:
        t_clone.commit()
        print 'Trade ', trd.trdnbr, ' premium changed to ', prem
        return 'Success'
    except:
        return 'Error commiting trade'
        
    



ael_variables = [('Trade', 'TradeNumber', 'int', '', '', 1),
    	     	('Premium', 'Premium', 'float', '', '', 1)]


#main
def ael_main(ael_dict):
    t = ael_dict["Trade"]
    newPrem = ael_dict["Premium"]

    print SetPremium(1, t, newPrem)

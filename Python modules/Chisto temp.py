import ael, string



def SetPremium(temp,ii,t,*rest):
    trd = ael.Trade[t]
    t_clone = trd.clone()
    t_clone.insaddr = ii

    try:
        t_clone.commit()
        print 'Trade ', trd.trdnbr, '  changed to ', ii,
        return 'Success'
    except:
        return 'Error commiting trade'
        
    



ael_variables = [
                 ('insaddrnew', 'ins2', 'int', '', '', 1),
                 ('trade', 'trade', 'int', '', '', 1)  	  
]


#main
def ael_main(ael_dict):
    ii  = ael_dict["insaddrnew"]
    t  = ael_dict["trade"]
    print SetPremium(1, ii, t) 

import ael



def changeTrader(temp, trdnbr, newUser, *rest):

    New = ael.User[newUser]

    t_clone = ael.Trade[trdnbr].clone()
    t_clone.trader_usrnbr = New
    try:
        t_clone.commit()
        #print 'Trade ', trdnbr, 'successly updated'
        return 'Success'
    except:
        print('Error committing trade ', trdnbr)
        return 'Failed'
        
    return   
    
    
    

#main
#print changeTrader(1, 556758, 'ABMR400')

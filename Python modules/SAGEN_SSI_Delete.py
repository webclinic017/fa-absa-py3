import ael


def Delete_SSI(temp, s, *rest):
    try:
    	s.delete()
	return 'Success'
    except:
    	print('Unable to delete SSI')
	return 'Failed'
	
	

def Delete_Acc(temp, a, *rest):
    try:
    	a.delete()
	return 'Success'
    except:
    	print('Unable to delete account')
	return 'Failed'
	
	
	
def UpdateTradeLinks(temp, t, *rest):
    t_clone = t.clone()
    t_clone.settle_seqnbr = 0
    t_clone.pay1_accnbr = 0
    t_clone.pay2_accnbr = 0
    
    try:
    	t_clone.commit()
	return 'Commited'
    except:
    	return 'Unable to change trade'
        
    

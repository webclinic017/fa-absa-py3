import ael, acm

def delete_vol_surface(v, *rest):


    vol = ael.Volatility[v]
    
    
    set = ['EQUITY_ATM_VOL', 'EQUITY_ATM_VOL_SAFEX_PRICE_TEST', 'SAEQ_OTC', 'SAEQ_Per', 'EQ_Warrants1_Vol', 'IMP_WAR']
    
    
    ref = vol.reference_in(1)
    for b in ref:
          
        try:
            print b.display_id(), 'this vol surface will be deleted'
            b.delete()
        except:
            print b.display_id(), '  HAS NOT NOT DELETED'
    try:
        print vol.vol_name, 'this vol surface will be deleted'
        vol.delete()
    except:
        print vol.vol_name, '  HAS NOT BEEN DELETED'
        
    return
    
delete_vol_surface('EQUITY_ATM_VOL')   
delete_vol_surface('EQUITY_ATM_VOL_SAFEX_PRICE_TEST')
delete_vol_surface('SAEQ_OTC') 
delete_vol_surface('SAEQ_Per')
delete_vol_surface('EQ_Warrants1_Vol')   
delete_vol_surface('Can Do')           
       
        

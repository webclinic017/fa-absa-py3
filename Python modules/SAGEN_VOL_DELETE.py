import ael

# DELETION OF A VOLATILITY SURFACE TOGETHER WITH ALL VPS SURFACES
# NOTE!!!!!!!!      VPS surfaces are deleted first, hence if there are dependancies and live surface is not deleted,
# all vps surfaces would have already been deleted. Hence:

# TEST IN DEV ENVIRONMENT FIRST!!!!!!!
 
def del_vol(vol,*rest):
    r = 'FAIL'
    if vol:
        
        
        for y in vol.reference_in():
            try:
                y.delete()
                
            except:
                
                pass
        try:
            vol.delete()
            r = 'SUCCESS'
        except:
            return r
    
    return r
    
    
def VolS():
    cp = []
    cps = ael.Volatility
    for c in cps:
        cp.append(c.vol_name)
    cp.sort()
    return cp
    


ael_variables = [ ('vols', 'Volatility Surface to Delete: ', 'string', VolS(), '', 1, 1, "Select a list of volatilities to be deleted. Includes deleting of VPS surface!.")]

def ael_main(ael_dict):
    for v in ael_dict["vols"]:
        try:
            vol = ael.Volatility[v]
            r = del_vol(vol)
            if r == 'FAIL':
                ael.log('ERROR DELETING VOL SURFACE   : ' + v)
            else:
                ael.log('VOL SURFACE   : ' + v + ' SUCCESSFULLY DELETED')
        except:
            ael.log('ERROR DELETING VOL SURFACE: ' + v)

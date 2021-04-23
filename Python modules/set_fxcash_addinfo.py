import ael, acm

"""-----------------------------------------------------------------------------
Date:                   2011-09-20
Purpose:                Set add_info fields for aggregated fx_cash trades for Odyssey to work
Department and Desk:    FX Desk
Requester:              Dirk Strauss
Developer:              Dirk Strauss
CR Number:              ???




-------------------------------------------------------------------------------"""

ael_variables = [ 
                ('Portfolio', 'Portfolio: ', 'FPhysicalPortfolio', None, 'MIDAS_FLO,MIDAS_FWD,MIDAS_JDY,MIDAS_RFT,MIDAS_RVT', 0, 1, 'Name of Portfolio'),
                 ] 



def set_addinfo(entity, ai_name, ai_value):
    # Sets an additional info field for a given entity
    ent_clone = entity.clone()
    
    # Clone the additional info entity if it exists, otherwise create a new additional info
    for ai in entity.additional_infos():
        if ai.addinf_specnbr.field_name == ai_name:
            new_ai = ai.clone()
            break
    else:
        new_ai = ael.AdditionalInfo.new(ent_clone)
        new_ai.addinf_specnbr = ael.AdditionalInfoSpec[ai_name]
    
    new_ai.value = str(ai_value)
    try:
        new_ai.commit()
        ent_clone.commit()
    except:
        print 'Error: Could not update additional info value %s' %(ai_name)


# ===================================================================================================================
def ael_main(data):
    n = 0    

    trds = []

    for port in data['Portfolio']: 
        sport = port.Name()
        print 'Adding portfolio : ', sport
        port = ael.Portfolio[ sport ]
        trds.extend( port.trades() )
        
    s = 'Source Ctpy Name|CASH,Source System|MIDAS,Source Trade Id|CASH,Source Trade Type|CA,Source Trader|CASH'
    
    print '\n' * 2
    
    for trd in trds:
        if trd.type in ['Aggregate'] and trd.status not in ['Void', 'Simulated']:
            n += 1
            
            print n, '\t', trd.trdnbr
            
            for itm in s.split(','):
                fld = itm.split('|')[0]
                aival = itm.split('|')[1]
                
                if trd.add_info(fld) <> aival:
                    print 'Updating : ', '\t'*2, fld, ' = ', aival
                    set_addinfo(trd, fld, aival)
                
    
    print '-' * 50
        








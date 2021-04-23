'''
Date                    : 03/05/2010  
Purpose                 : Function used to determine portfolios under parent portfolio
Department and Desk     : Middle Office
Requester               : Front
Developer               : Dirk Strauss
CR Number               : 306264
'''

import ael

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
        pass
        #print 'Error: Could not update additional info value %s' %(ai_name)


def GetPortTree(prfnbr, sParent, level = 0):
    t = '\t'
    
    port = ael.Portfolio[prfnbr]
    sport = port.prfid

    parent_level = 2
    
    if level == parent_level:
        if sport == 'NLD Desk':
            sParent = 'FI Opt Desk'
        elif sport == 'NLD_Desk':
            sParent = 'FX Opt Desk'
        else:
            sParent = sport
        
    comp_port = port.compound
    
    #print sport, t, port.add_info('Parent_Portfolio')
    
    if port.add_info('Parent_Portfolio') <> sParent and level > parent_level:
        #print level, 'Setting AddInfo value for portfolio : ' + sport + '. Setting value to : ' + sParent
        set_addinfo(port, 'Parent_Portfolio', sParent)
        
    if not comp_port:        
        pass
        #print sport, '\t', sTree, '\t', ael.date_from_time(port.creat_time), '\t', port.creat_usrnbr.name
    else:
        all_c = port.children()        
        for c in all_c:  
            if c.record_type in ['PortfolioLink']:
                GetPortTree(c.member_prfnbr.prfnbr, sParent, level + 1)

def PortGroup():
    pg = [p.prfid for p in ael.Portfolio]
    pg.sort()
    return pg

ael_variables = [('Portfolio1', 'Portfolio 1', 'string', PortGroup(), 'SECONDARY MARKETS BANKING', 1),
    	     	('Portfolio2', 'Portfolio 2', 'string', PortGroup(), 'SECONDARY MARKETS TRADING', 0)]

def ael_main(ael_dict):
    plst = []    
    plst.append(ael_dict["Portfolio1"])
    if ael_dict["Portfolio2"] <> '':
        plst.append(ael_dict["Portfolio2"])
    for p in plst:        
        port = ael.Portfolio[p]
        GetPortTree(port.prfnbr, port.prfid)
        
    print("Completed Successfully ::")

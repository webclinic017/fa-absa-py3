import ael

for grp in ael.Group:

    new_p = ael.UserProfile.new()
    new_p.profid = grp.grpid
    CompDict = {}
    for gl in ael.GroupProfileLink:
#        if ael.Group['IRD_SENIOR'].grpid  == gl.grpnbr.grpid:
        if grp.grpid  == gl.grpnbr.grpid:
            for p in gl.profnbr.profile_components():
                if CompDict.has_key(p.compnbr.compname) == 1:
                    if CompDict[p.compnbr.compname][0] == 1: 
                        comp.allow_write = p.allow_write  
                    if CompDict[p.compnbr.compname][1] == 1:
                        comp.allow_create = p.allow_create 
                    if CompDict[p.compnbr.compname][2] == 1:
                        comp.allow_delete   = p.allow_delete
                    
                else:
                    comp = ael.ProfileComponent.new(new_p)
                    comp.compnbr = p.compnbr
                    comp.allow_write = p.allow_write  
                    comp.allow_create = p.allow_create
                    comp.allow_delete   = p.allow_delete
              
                CompDict[p.compnbr.compname] = [p.allow_write, p.allow_create, p.allow_delete]  

    new_p.commit()      
                              



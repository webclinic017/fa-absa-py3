import ael

for usr in ael.User.select():
    try:
        if usr.grpnbr.grpid[0:3] == "OPS" or usr.grpnbr.grpid[0:7] == "PCG Mkt":
            
            usr2 = usr.clone()
            
            for pl in usr2.profile_links(): 
                pl.delete()
            
            usr2.commit()
            print('Profile links deleted for ' + usr.userid + ' in group ' + usr.grpnbr.grpid)
    except:
        print('Exception: ' + usr.userid)

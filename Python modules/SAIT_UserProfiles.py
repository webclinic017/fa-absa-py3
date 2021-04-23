import ael

#Displays a list of all the groups and the members within each group

All_Groups = ael.Group

for g in All_Groups:
    print('\n GroupName - %s\n' %(g.description))
    users = g.users()
    for u in users:
    	print('     	Members Name - \t\t %s \t\t %s' %(u.userid, u.name))
	prflinks = u.profile_links()
	for p in prflinks:
	    print(' 	    	    ', p.profnbr.profid, '\t\t', p.profnbr.description)
	    
	print()
	print()
    print()
    print()
    print()
    print()
    


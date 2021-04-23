import ael

#Displays a list of all the groups and the members within each group

All_Users = ael.User

print('Users with PREVIOUS_USER profile')
for u in All_Users:
    prflinks = u.profile_links()
    for p in prflinks:
	if p.profnbr.profid == 'PREVIOUS_USER':
	    print(u.userid, u.name)
    

print('\n\n\n Users with PREV, Prev, or prev in their names')
for u in All_Users:    
    if (u.name.find('PREV') != -1) or (u.name.find('Prev') != -1) or (u.name.find('prev') != -1):
    	print(u.userid, u.name)
#    	pass
    else:
#    	print u.userid, u.name
    	pass

#    print '\n GroupName - %s\n' %(g.description)
#    users = g.users()
#    for u in users:
#    	print '     	Members Name - \t\t %s \t\t %s' %(u.userid, u.name)
#	prflinks = u.profile_links()
#	for p in prflinks:
#	    print ' 	    	    ', p.profnbr.profid, '\t\t', p.profnbr.description
#	    
#	print
#	print
#    print
#    print
#    print
#    print
    


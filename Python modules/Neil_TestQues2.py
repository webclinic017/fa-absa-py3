import ael

#Displays a list of all the groups and the members within each group

All_Groups = ael.Group

for g in All_Groups:
    print('\n GroupName - %s\n' %(g.description))
    users = g.users()
    for u in users:
    	print('     	Members Name - %s' %(u.name))

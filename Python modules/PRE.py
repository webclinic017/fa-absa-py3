import acm

list_of_users = []

group = acm.FUserGroup['Previous User']
for user in group.Users():
    if user.Links():
        list_of_users.append(user) 
        for userlink in user.Links():
            userlink.Delete()
for user in list_of_users:
    if user.Links():
        print(user.Name())

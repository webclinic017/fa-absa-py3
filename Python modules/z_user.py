import ael

amount_to_delete = 1000

c = 0

user_logs = ael.UserLog.select()

for u in user_logs:

    print(u)

    u.delete()

    if c > amount_to_delete:

    	break

    c = c + 1

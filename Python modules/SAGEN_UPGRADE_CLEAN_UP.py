import acm



def delete_exotic(null_list):
    for n in null_list:
        try:
            n.Delete()
            print('Null Exotic successfully deleted')
        except:
            print('Null Exotic not deleted')


null_exotics = acm.FExotic.Select('instrument = 0')
print('List of null exotics before deletes: ', null_exotics)
delete_exotic(null_exotics)

null_exotics = acm.FExotic.Select('instrument = 0')
print('List of null exotics after deletes: ', null_exotics)

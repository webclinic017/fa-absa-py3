import acm
import time, datetime


date_from = datetime.date(2017, 1, 5)
date_from = datetime.date.fromtimestamp(time.time())
date_from = datetime.date.today()
date_from = "2020-01-14"

#QUERY = "createTime > '%s'" % date_from
QUERY = "updateTime > '%s'" % date_from

update_user = None
#update_user = "MANDEPUR"


if update_user:
    QUERY = "%s and updateUser = '%s'" %(QUERY, update_user)

#ael_files = acm.FAel.Select('updateTime > %s' %ddt)
ael_files = acm.FAel.Select(QUERY)
#ael_files = acm.FExtensionModule.Select('createTime > %s' %ddt)
ael_files = acm.FExtensionModule.Select(QUERY)

print "{0:45}{1:23}{2:12}{3}".format(
    "Module", "Create time", "Update User", "Update Time")
print "=" * 120

for aelf in sorted(ael_files, key=lambda f: f.UpdateTime()):
    name = aelf.Name()
    create_time = str(datetime.datetime.fromtimestamp(aelf.CreateTime()))
    update_time = str(datetime.datetime.fromtimestamp(aelf.UpdateTime()))
    print "{0:45}{1:23}{2:12}{3}".format(
        name, create_time, aelf.UpdateUser().Name(), update_time)

print "=" * 120

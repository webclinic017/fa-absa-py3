""" Compiled: 2020-09-18 10:38:51 """

#__src_file__ = "extensions/bdp_dashboard/BDPDashboard.py"
#----------------------------------------------------------------------------
#    (c) Copyright 2020 SunGard Front Arena. All rights reserved.
#----------------------------------------------------------------------------

import acm

allow = acm.FUser[acm.UserName()].IsAllowed('Business Data Processing', 1)
if allow:
    acm.UX().SessionManager().StartApplication('BDP Dashboard', None)
else:
    print('You need to have the permission to run Business Data Processing \
to launch BDP Dashboard')

""" Compiled: 2020-09-18 10:38:51 """

#__src_file__ = "extensions/wi_processing/etc/FWIGeneral.py"
#----------------------------------------------------------------------------
#    (c) Copyright 2020 SunGard Front Arena. All rights reserved.
#----------------------------------------------------------------------------

"""----------------------------------------------------------------------------
MODULE
    FWIGeneral - Module including all functions common to the When Issued
                 processing.

----------------------------------------------------------------------------"""


import time


def now():
    return ttos(time.time())


def ttos(t):
    """
    Time to string e.g. 2002-09-30 15:00:00
    """
    s = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(t))
    return s


def log(level, verbosity, s):
    """
    Log me.
    """
    if verbosity >= level:
        s = str(s)
        if s[0] == '\n':
            print("\n%s: %s" % (now(), s[1:]))
        else:
            print("%s: %s" % (now(), s))

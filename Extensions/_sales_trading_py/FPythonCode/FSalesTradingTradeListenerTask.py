""" Compiled: 2020-09-18 10:38:54 """

#__src_file__ = "extensions/SalesTrading/./etc/FSalesTradingTradeListenerTask.py"
"""--------------------------------------------------------------------------
MODULE
    FSalesTradingTradeListenerTask

    (c) Copyright 2014 SunGard FRONT ARENA. All rights reserved.

DESCRIPTION
    Server side trade listener for Sales Trading.
    
-----------------------------------------------------------------------------"""

import FSalesTradingTradeListenerTaskImpl


def start():
    FSalesTradingTradeListenerTaskImpl.DoStart()
        
def work():
    FSalesTradingTradeListenerTaskImpl.DoWork()

def stop():
    FSalesTradingTradeListenerTaskImpl.DoStop()
    
def status():
    return 'OK!'
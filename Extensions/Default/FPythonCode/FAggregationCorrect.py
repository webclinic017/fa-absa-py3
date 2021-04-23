""" Compiled: 2020-09-18 10:38:51 """

#__src_file__ = "extensions/aggr_arch/etc/FAggregationCorrect.py"
#----------------------------------------------------------------------------
#    (c) Copyright 2020 SunGard Front Arena. All rights reserved.
#----------------------------------------------------------------------------

"""----------------------------------------------------------------------------
MODULE
    FAggregationCorrect - Perform correction of dirty aggregates.

DESCRIPTION
        This module corrects aggregated trades in a ARENA Database. An
        aggregated trade may be marked dirty if for example it is moved
        to another portfolio.


NOTE
    The modules uses the aggregation rules set up in the Aggregation
    Specification application.

ENDDESCRIPTION
----------------------------------------------------------------------------"""
# LOG HANDLING:

# Specify if information about the aggregation should be logged to file.

LogInformation = 0
#LogInformation = 1

# If LogInformation = 1 the following information will be loggged:
#
#   Splitting criteria
#   The currently used aggregation rule (rule number)
#   Aggregation date
#   Instrument and Portfolio of the currently aggregated trades
#   Number of trades beeing aggregated/de-aggregated
#   Number of aggregate trades created

import ael
import acm


import FBDPCommon

counter = 0
statuslist = ""
correct = 0


def start():
    print("Starting trade subscription")
    ael.Trade.subscribe(trade_update_cb)
    useSelectedFundingDay = FBDPCommon.getUseSelectedFundingDay()
    acm.AggregateCorrect(LogInformation, useSelectedFundingDay)
    return


def status():

    global counter
    global statuslist

    str1 = "\nNumber of corrections made so far = %d" % counter
    return statuslist + str1


def stop():

    print("Stopping trade subscription")
    ael.Trade.unsubscribe(trade_update_cb)


def work():

    global correct

    if correct:
        print(statuslist)
        useSelectedFundingDay = FBDPCommon.getUseSelectedFundingDay()
        acm.AggregateCorrect(LogInformation, useSelectedFundingDay)
    correct = 0


def trade_update_cb(obj, trade, arg, event):

    global counter
    global statuslist
    global correct

    if trade == None:
        return

    if event == "update":
        if trade.aggregate == -1:
            correct = 1

    elif (event != "insert" and event != "delete"):
        ael.log("trade_update_cb: Unexpected event %s" % event)

    if correct:
        statuslist = "Caught %d %s" % (trade.trdnbr, event)
        counter = counter + 1

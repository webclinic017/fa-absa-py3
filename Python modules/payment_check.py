"""
-------------------------------------------------------------------------------
MODULE
    payment_check

DESCRIPTION
    Date                : 2016-05-17
    Purpose             : This module allows to check execution fees before and
                          after migration to payment based calculation for CFDs
    Department and Desk : Product Control Group
    Requester           : Muhammed Osman
    Developer           : Jakub Tomaga
    CR Number           : CHNG0003661849

HISTORY
===============================================================================
Date        CR number   Developer       Description
-------------------------------------------------------------------------------
16-05-2016  3661849     Jakub Tomaga    Initial implementation.
-------------------------------------------------------------------------------
"""

import acm
from at_ael_variables import AelVariableHandler

ael_variables = AelVariableHandler()
ael_variables.add("query_folder",
                  label="Query Folder",
                  cls=acm.FStoredASQLQuery,
                  collection=acm.FStoredASQLQuery.Select(
                      "subType='FTrade'"))


def ael_main(config):
    query_folder = config["query_folder"]
    for trade in query_folder.Query().Select():
        for payment in trade.Payments():
            print("{0},{1},{2},{3},{4}".format(
                trade.Oid(),
                trade.Instrument().InsType(),
                payment.Type(),
                payment.Text(),
                payment.Amount()
            ))
        stock_trade = trade.Contract()
        if not stock_trade:
            print("WARNING: CFD trade {0} has no mirror on-tree.".format(trade.Oid()))
        else:
            for payment in stock_trade.Contract().Payments():
                 print("{0},{1},{2},{3},{4}".format(
                    stock_trade.Oid(),
                    stock_trade.Instrument().InsType(),
                    payment.Type(),
                    payment.Text(),
                    payment.Amount()
                ))
    print("Completed successfully")

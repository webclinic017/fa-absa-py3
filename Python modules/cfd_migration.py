"""
-------------------------------------------------------------------------------
MODULE
    cfd_migration

DESCRIPTION
    Date                : 2016-05-17
    Purpose             : This module allows for migration to payment based
                          execution fee calculation for CFDs
    Department and Desk : Product Control Group
    Requester           : Muhammed Osman
    Developer           : Jakub Tomaga
    CR Number           : CHNG0003661849

HISTORY
===============================================================================
Date        CR number   Developer       Description
-------------------------------------------------------------------------------
16-05-2016  3661849     Jakub Tomaga    Initial implementation.
02-09-2016  3931533     Jakub Tomaga    Transaction split.
-------------------------------------------------------------------------------
"""


import time
import acm
from at_ael_variables import AelVariableHandler
from PS_new_fees import add_cfd_execution_fee


ael_variables = AelVariableHandler()
ael_variables.add("query_folder",
                  label="Query Folder",
                  cls=acm.FStoredASQLQuery,
                  collection=acm.FStoredASQLQuery.Select("subType='FTrade'"))
ael_variables.add("transaction_size",
                  label="Transaction size",
                  cls="int")
ael_variables.add_bool("dry_run",
                       label="Dry run",
                       default=True)


def ael_main(config):
    query_folder = config["query_folder"]
    dry_run = config["dry_run"]
    transaction_size = config["transaction_size"]
    trades = query_folder.Query().Select()
    number_of_trades = updated_trades = len(trades)
    i = 0
    chunk_of_trades = trades[:transaction_size]
    start = time.time()
    while chunk_of_trades:
        chunk_size = len(chunk_of_trades)
        try:
            acm.BeginTransaction()
            for trade in chunk_of_trades:
                execution_fee = add_cfd_execution_fee(trade)
                print("Updating trade {0} with CFD payment of R{1}".format(
                    trade.Oid(), execution_fee))
            if not dry_run:
                acm.CommitTransaction()
            else:
                acm.AbortTransaction()
            print("Updated {0} trades up to {1}".format(chunk_size,
                i * transaction_size + chunk_size))
        except Exception as ex:
            acm.AbortTransaction()
            updated_trades -= chunk_size
            print("Error: Unable to commit trades from {0} to {1}: {2}".format(
                i * transaction_size + 1, i * transaction_size + chunk_size, str(ex)))
        i += 1
        chunk_of_trades = trades[i * transaction_size:(i + 1) * transaction_size]
    end = time.time()
    print("Updated {0}/{1} trades in {2} seconds".format(
        updated_trades, number_of_trades, end - start))

                

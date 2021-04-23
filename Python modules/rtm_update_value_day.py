import acm

import os
import acm
import csv
import time
from at_time import to_datetime
from at_ael_variables import AelVariableHandler

pswap_list = [
    "RTM_40923",
    "RTM_41293",
    "RTM_41350",
    "RTM_47324",
    "RTM_48694",
    "RTM_60814",
    "RTM_47365",
    "RTM_47332",
    "RTM_60392",
    "RTM_60772",
    "RTM_48389",
    "RTM_60129_EqPairs_LT",
    "RTM_60798",
    "RTM_60491",
    "RTM_60822",
    "RTM_60632",
    "RTM_60616",
    "RTM_60905",
    "RTM_60962",
    "RTM_60970",
    "RTM_60996",
    "RTM_61077",
    "RTM_61028",
    "RTM_61127"
]

ael_variables = AelVariableHandler()

def ael_main(config):
    for pswap_name in pswap_list:
        pswap = acm.FInstrument[pswap_name]
        print(pswap_name, pswap.StartDate())
        for trade in pswap.Trades():
            print("Setting value day to {0} for {1}".format(pswap.StartDate(), trade.Oid()))
            trade.ValueDay(pswap.StartDate())
            trade.Commit()

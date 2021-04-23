'''
Description
===========
Date                          :  2014-10-31
Purpose                       :  Module used to generate report of settled trades, containing the ISIN and PS nominal
Department and Desk           :  OPS
Requester                     :  Leseyane Silindile
Developer                     :  Andrei Conicov
CR Number                     : CHNG0002395723


History
=======

Date            CR              Developer               Description
====            ======          ================        =============
2014-10-31      CHNG0002395723  Andrei Conicov          Initial Implementation
'''


import acm, os
from datetime import date
from at_ael_variables import AelVariableHandler
from collections import defaultdict
import at, at_calculation_space as acs

_DELIMITER = "|"

ael_variables = AelVariableHandler()
trade_filter_names = sorted([f.Name() for f in acm.FTradeSelection.Select("")])
ael_variables.add(
    'tf_title',
    label='TradeFilter',
    collection=trade_filter_names,
    default="SAOPS_Sec_Position_2",
    alt='The trade filter title that will be used to create trade rows' 
    )
ael_variables.add(
    'path',
    label='Output Folder',
    default=r'c:\tmp',
    alt='The directory where to which the file will be dropped.' 
    )
ael_variables.add(
    'file_name',
    label='Output File Name',
    default='SAOPS_Sec_Position_2',
    alt='The directory where to which the file will be dropped.' 
    )

def _get_column_value(trade, column):
    value = acs.calculate_value('FTradeSheet', trade, column)
    if hasattr(value, 'Number'):
        value = value.Number()
    return value

def _process(trades):
    result = defaultdict(int)
    for trade in trades:
        is_settled = trade.IsSettled()
        if is_settled == "settled":
            isin = trade.Instrument().ISIN_UndISIN_Name()
            nominal = _get_column_value(trade, "PS Nominal")
            result[isin] += nominal

    return [[k, str(v)] for k, v in result.items() if v != 0]

def _output(data, writer):
    columns = ["ISIN", "PS Nominal"]
    writer(_DELIMITER.join(columns))
    for item in data:
        writer(_DELIMITER.join(item))

def ael_main(dict_arg):
    """Main entry point for FA"""
    
    if str(acm.Class()) == "FTmServer":
        warning_function = acm.GetFunction("msgBox", 3)
    else:
        warning_function = lambda t, m, *r: print("{0}: {1}".format(t, m))
    
    tf_title = dict_arg['tf_title']
    file_name = dict_arg['file_name']
    path = dict_arg['path']
    
    tf = acm.FTradeSelection[tf_title]
    if not tf:
        warning_function("Warning",
            "Could not find the specified trade filter!", 0)
        return
    data = _process(tf.Trades())
    
    filename = "{0}-{1}.csv".format(file_name, date.today().strftime("%Y-%m-%d"))
    file_path = os.path.join(path, filename)
    
    with open(file_path, 'w') as file_w:
        writer = lambda line: file_w.write(line + "\n")
        _output(data, writer)
    
    print ("Wrote secondary output to {0}".format(file_path))
    print ("completed successfully")
    
    print("END")
    
def _debug():
    dict_arg = {}
    dict_arg['tf_title'] = "SAOPS_Sec_Position_2"
    dict_arg['file_name'] = "SAOPS_Sec_Position_2.csv"
    dict_arg['path'] = r"c:\tmp"
    
    ael_main(dict_arg)


'''
Created on 6 Dec 2013

    Purpose                 : Report the yield curve rates.
    Department and Desk     : PCG
    Requester               : Van Looy, Benjamin
    Developer               : Conicov Andrei
    CR Number               : ABITFA-2303
'''

from at_ael_variables import AelVariableHandler
import ael, acm
import os

def _get_rate(yc, date_from, date_to, ir_rate_type, day_count_method, rate_type, output_prefix):
    rt = yc.yc_rate(date_from, date_to, ir_rate_type, day_count_method, rate_type)
    output = [output_prefix, str(date_from), str(date_to), ir_rate_type, day_count_method, rate_type, str(rt)]
    return "\t".join(output)

def _create_output(yc, writer_f):
    
    start = ael.date_today()
        
    ir_rate_type = 'Simple' 
    day_count_method = 'act/360' 
    rate_type = 'Spot Rate'
    periods = ['1d', '1w', '1M', '2M', '3M']
    
    for period in periods:
        date_to = ael.date(start.add_period(period))
        txt = _get_rate(yc, start, date_to, ir_rate_type, day_count_method, rate_type, period)
        writer_f(txt)
    
    ir_rate_type = 'Semi Annual' 
    day_count_method = '30/360' 
    rate_type = 'Par Rate'
    
    for j in range(3, 51):
        date_to = ael.date(start.add_period(str(j) + 'Y'))
        output_prefix = str(j) + 'Y'
        txt = _get_rate(yc, start, date_to, ir_rate_type, day_count_method, rate_type, output_prefix)
        writer_f(txt)
    
    ir_rate_type = 'Quarterly' 
    day_count_method = 'act/360' 
    rate_type = 'Forward rate'
    fdstart = ael.date_today().add_days(-1)
    end_date = ael.date_today().add_years(4)
    
    while end_date > fdstart:
        fdstart = fdstart.add_days(1)
        date_to = ael.date(fdstart.add_period('3M'))
        txt = _get_rate(yc, fdstart, date_to, ir_rate_type, day_count_method, rate_type, '')
        writer_f(txt)

ael_variables = AelVariableHandler() 

ael_variables.add(
    'yc_name',
    label='Yield Curve name',
    default='EUR-SWAP-SPREAD-6M',
    alt='The yield curve name.',
    mandatory=1 
    )
ael_variables.add(
    'path',
    label='Output Folder',
    default=r'c:\tmp\ABITFA-2303',
    alt='The directory where to which the file will be dropped.',
    mandatory=1 
    )
ael_variables.add(
    'file_name',
    label='Output File Name',
    default='Curency_IR.xls',
    alt='The file name',
    mandatory=1 
    )   

def ael_main(dict_arg):
    """Main entry point for FA"""
    acm.Log("Starting {0}".format(__name__))
    
    if str(acm.Class()) == "FTmServer":
        warning_function = acm.GetFunction("msgBox", 3)
    else:
        warning_function = lambda t, m, *r: print("{0}: {1}".format(t, m))
    
    yc_name = dict_arg['yc_name']
    path = dict_arg['path']
    file_name = dict_arg['file_name']
    
    if not os.access(path, os.W_OK):
        warning_function("Warning",
            "Output path is not writable! Client valuation not generated!", 0)
        return
    
    yc = ael.YieldCurve[yc_name]
    if not yc:
        warning_function("Warning",
            "Yield curve with name '{0}' was not found.".format(yc_name), 0)
        return
    
    file_path = os.path.join(path, file_name)
    
    with open(file_path, 'w') as file_w:
        writer_f = lambda line: file_w.write(line + '\n')
        _create_output(yc, writer_f)
    
    acm.Log("Wrote secondary output to {0}".format(file_path))
    acm.Log("Completed successfully")

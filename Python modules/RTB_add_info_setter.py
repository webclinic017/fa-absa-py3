'''
Created on 18 Jan 2016

@author: conicova
'''
import csv

import acm

from at_ael_variables import AelVariableHandler
import at_addInfo

def set_add_info(trdnbr, add_info_name, value, dry_run=True):
    
    trd = acm.FTrade[trdnbr]
    
    if not trd:
        raise Exception("ERROR, the trade '{0}' does not exist".format(trdnbr))
    old_value = at_addInfo.get_value(trd, add_info_name)
    print("Setting the additional info '{2}' to '{0}' from '{3}' on trade '{1}'".format(value, trd.Oid(), add_info_name, old_value))
    if not dry_run:
        at_addInfo.save(trd, add_info_name, value)
        
ael_variables = AelVariableHandler()

ael_variables.add('dry_run',
              label='Dry run',
              cls='bool',
              collection=(True, False),
              default=True)

ael_variables.add_input_file('csv_path', 'CSV Path', mandatory=True, alt=("The path to a csv file, with the following columns: Trd no, Add info name, Add info value"))

def ael_main(config):
    """Update given set of trades additional infos."""
    csv_path = str(config["csv_path"])
    dry_run = config["dry_run"]

    with open(csv_path, 'r') as csv_f:
        reader = csv.reader(csv_f)
        # skip the header
        next(reader, None)
        for row in reader:
            try:
                set_add_info(row[0].replace(',', ''), row[1].replace(',', ''), row[2].replace(',', ''), dry_run)
            except Exception as ex:
                print(ex)
    
    print("Finished")

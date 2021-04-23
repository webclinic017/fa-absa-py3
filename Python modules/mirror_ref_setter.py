'''
Created on 24 Aug 2015

@author: conicova

Version 2
'''
import csv

import acm

from at_ael_variables import AelVariableHandler

def set_mirror_ref(trdnbr_parrent, trdnbr_mirror, dry_run=True):
    
    trd_parrent = acm.FTrade[trdnbr_parrent]
    trd_mirror = acm.FTrade[trdnbr_mirror]
    
    if not trd_parrent:
        raise Exception("ERROR, the trade '{0}' does not exist".format(trdnbr_parrent))
    if not trd_mirror:
        raise Exception("ERROR, the trade '{0}' does not exist".format(trdnbr_mirror))
    
    if trd_parrent.MirrorTrade(): 
        if trd_parrent.MirrorTrade().Oid() != trd_mirror.Oid():
            print("Trade '{0}' already has a mirror trade '{1}' that will be overwritten".format(trd_parrent.Oid(), trd_parrent.MirrorTrade().Oid()))
        else:
            return
    
    print("Setting mirror ref '{0}' on trade '{1}'".format(trdnbr_mirror, trdnbr_parrent))
    
    clone_trd_parrent = trd_parrent.Clone()
    
    clone_trd_parrent.MirrorTrade(trd_mirror)
    
    if not dry_run:
        trd_parrent.Apply(clone_trd_parrent)
        trd_parrent.Commit()
        print("Commited".format())
        
ael_variables = AelVariableHandler()

ael_variables.add('dry_run',
              label='Dry run',
              cls='bool',
              collection=(True, False),
              default=True)

ael_variables.add_input_file('csv_path', 'CSV Path', mandatory=True, alt=("The path to a csv file, with the following columns: Trd no, Portfolio, Mirror"))

def ael_main(config):
    """Update given set of instruments with product type."""
    csv_path = str(config["csv_path"])
    dry_run = config["dry_run"]

    with open(csv_path, 'r') as csv_f:
        reader = csv.reader(csv_f)
        # skip the header
        next(reader, None)
        for row in reader:
            try:
                set_mirror_ref(row[0].replace(',', ''), row[2].replace(',', ''), dry_run)
                set_mirror_ref(row[2].replace(',', ''), row[0].replace(',', ''), dry_run)
            except Exception as ex:
                print(ex)
    
    print("Finished")

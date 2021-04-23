"""
--------------------------------------------------------------------------------------------------------------------------------------------------------------------
MODULE
    hedge_relship_new_trade_booking
    
DESCRIPTION
    Date                    : 2018-10-10
    Purpose                 : Treasury wants to replace certain trades with new trades on a given list of hedge relationships. The trades will be read
                              off a csv file. The reason for the rebooking is the OIS project, Treasury doesn't want hypothetical derivatives to be fair valued 
                              off an OIS curve.
    Department and Desk     :  Treasury
    Requester               :  James Moodie
    Developer               :  Nkosinathi Sikhakhane
    JIRA Number             :  FtF-188
    

HISTORY
====================================================================================================================================================
Date              JIRA Number        Developer              Description
----------------------------------------------------------------------------------------------------------------------------------------------------
2018-10-10        FtF-188          Nkosinathi Sikhakhane      Initial Implementation.
----------------------------------------------------------------------------------------------------------------------------------------------------
"""


import acm
import HedgeRelation
import HedgeDealPackage
import csv
import os
import FUxCore

from at_ael_variables import AelVariableHandler
from at_logging import getLogger

LOGGER = getLogger(__name__)

ael_variables = AelVariableHandler()

ael_variables.add("file_dir",
                  label="Directory",
                  default=r"C:\Users\SIKHAKHN\Desktop\hedge relationship",
                  alt=("A Directory template with all input files. "
                       "It can contain the variable DATE (\"$DATE\") "
                       "which will be replaced by the today's date (format YYYY-MM-DD)"))

ael_variables.add('input_file',
                  label = 'Input File',
                  default = 'trade_upload.csv',
                  mandatory = True,
                  multiple = False,
                  alt = 'CSV file to read')
                  
ael_variables.add('Dummy_Run',
                  label='Dummy Run',
                  cls='int',
                  default=1,
                  collection=[0, 1])


def ael_main(dict):
    file_dir = dict['file_dir']
    file_name = dict['input_file']
    full_path = os.path.join(file_dir, file_name)
    dummy_run = dict['Dummy_Run']
    
    with open(full_path, 'r') as csv_file:
        csv_reader = csv.reader(csv_file)
        
        for row in csv_reader:
            if row[0] == 'HR Impacted':
                continue
            else:
                hedge_name = row[0]
                old_trade = row[1]
                new_trade = row[2]
                
                hedge_relationship = HedgeRelation.HedgeRelation(hedge_name)
                hedge_relationship.read()
                
                try:
                    hedge_relationship.set_status('Simulated')
                    hedge_relationship.save()
                    hedge_relationship.read()
                    trades = hedge_relationship.get_trades()
                    trades.pop(old_trade)
                    trades[new_trade] = ['Hypo', 100, '']
                    hedge_relationship.set_trades(trades)
                    hedge_relationship.save()
                    hedge_relationship.read()
                    deal_package_name = hedge_relationship.get_deal_package()
                    designation_date = hedge_relationship.get_start_date()
                    status = hedge_relationship.get_status()
                    shell = acm.UX().SessionManager().Shell() 
                    names, updatedTradeList = HedgeDealPackage.set_dealpackage(shell, hedge_name, trades, designation_date, status, deal_package_name[1])
                    hedge_relationship.set_status('Proposed')
                    hedge_relationship.save()
                    LOGGER.info('Hedge trades {0}:{1}'.format(hedge_name, hedge_relationship.get_trades()))
                    
                except Exception, ex:
                    LOGGER.exception('Issue on hedge {0}, old trade {1}, new trade {2} : {3}'.format(hedge_name, old_trade, new_trade, ex))
                
                
        




"""
Description             : Call Deposits Codes maintanance
Department and Desk     : GRP TREASURY and Money Markets
Requester               : Karin Nieuwoudt
Developer               : Mighty Mkansi
JIRA                    : ABITFA-4464-MM_Call_Deposit_Uploade

History
=======

"""

import acm
import ael
import csv

from at_ael_variables import AelVariableHandler

ael_variables = AelVariableHandler()

ael_variables.add('inputFile',
    label='Input File',     
    mandatory = True,  
    default= r'C:\temp\CodeMigration.csv')

ins_dict = {}

def ael_main(config):
    file = config['inputFile']
    
    with open(file, 'rU') as csv_file:
            reader = csv.reader(csv_file)
            reader.next()             
            
            for line in reader:
                '''
                Caching intrument and trade data from the csv file
                '''
                FA_Instrument = line[0]    
                Code = line[1]  

                ins_dict[FA_Instrument] = Code
    
    for ins in ins_dict.keys():
        print(ins)
        acm_ins = acm.FInstrument[ins]
        if acm_ins:
            acm_ins.ExternalId1(ins_dict[ins])
            try:
                acm_ins.Commit()
                print('Commited External ID1 for {0} with {1}'.format(ins, code))
            except Exception as e:
                print('Could not commit External ID1 {0}'.format(ins))
                print('Check if External ID1 for {0} is not defined'.format(ins))                
        else:   
            print('Could not find instrument inf Front Arena : {0}'.format(ins))
            

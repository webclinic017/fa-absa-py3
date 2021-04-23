"""
-------------------------------------------------------------------------------
MODULE
    FlagFileReport

DESCRIPTION
    Date                : 2014-08-05
    Purpose             : Module for generating reports based on
                          FWorksheetReport. Once the report is generated 
                          correctly a flag file is created with basic
                          information - used for indication of complete file.
    Department and Desk : FO Prime Brokerage
    Requester           : Ridwaan Arbee
    Developer           : Jakub Tomaga
    CR Number           : CHNG0002184056

HISTORY
===============================================================================
Date        CR number   Developer       Description
-------------------------------------------------------------------------------

-------------------------------------------------------------------------------
"""

import os
import acm
import FWorksheetReport

FLAG_FILE_EXTENSION = '.flag'
ael_variables = FWorksheetReport.ael_variables


def ael_main(config):
    """Entry point of the task."""

    date = acm.Time().DateToday()
    file_name = '_'.join([config['File Name'], date])
    
    # Generate position file
    position_file_exception = None
    try:
        config['File Name'] = file_name
        FWorksheetReport.ael_main(config)
    except Exception as ex:
        position_file_exception = 'Position file: {0}'.format(ex)
    
    # Check for errors
    if not position_file_exception:
        try:
            # No exception - gather information for position file
            trade_filter_name = config['tradeFilters'][0].Name()
            soft_broker_alias = '_'.join(trade_filter_name.split('_')[1:-1])

            file_name = ''.join([file_name, config['Secondary file extension']])
            file_path = config['File Path'].SelectedDirectory().Text()

            flag_file_name = '_'.join([soft_broker_alias, date])
            flag_file_name = ''.join([flag_file_name, FLAG_FILE_EXTENSION])
            flag_file_full_path = os.path.join(file_path, flag_file_name)
            
            # Create flag file
            with open(flag_file_full_path, 'wb') as flag_file:
                flag_file.writelines([
                    date + '\r\n',
                    soft_broker_alias + '\r\n',
                    file_name + '\r\n'
                ])
                
            print('Wrote secondary output to: {0}'.format(flag_file_full_path))
        except Exception as ex:
            print('Generating flag file failed: {0}'.format(ex))
    else:
        print(position_file_exception)

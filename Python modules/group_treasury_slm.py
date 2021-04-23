import os
import csv
import string

import acm
from at_ael_variables import AelVariableHandler
from at_logging import getLogger


LOGGER = getLogger(__name__)

DELIM_LINE = '\r'
DELIM_CELL = chr(161)


ael_variables = AelVariableHandler()
ael_variables.add(
    'input_file',
    label = 'Input File',
    default = r'y:\Jhb\FAReports\AtlasEndOfDay\TradingManager\${DATE_DIR}\Group_Treasury_PNL_Report_${DATE_FILE}.xls',
    mandatory = True,
    alt = ('Can contain ${DATE_DIR} and ${DATE_FILE} which will '
        'be replaced by date in %Y-%m-%d and %y%m%d format')
    )
ael_variables.add(
    'output_file',
    label = 'Output File',
    default = r'/services/frontnt/Task/Group_Treasury_PNL_Report_SLM.csv',
    mandatory = True,
    alt = ('Can contain ${DATE_DIR} and ${DATE_FILE} which will '
        'be replaced by date in %Y-%m-%d and %y%m%d format')
    )
ael_variables.add(
    'for_date',
    label = 'Date',
    cls='date',
    default='Yesterday')


def get_file_path(file_tmpl, ael_date):

    date_dir = ael_date.to_string("%Y-%m-%d")
    date_file = ael_date.to_string("%y%m%d")

    f_template = string.Template(file_tmpl)
    file_name = f_template.substitute(DATE_DIR=date_dir, DATE_FILE=date_file)
    
    return file_name

    
def ael_main(ael_dict):
    input_file = get_file_path(ael_dict['input_file'], ael_dict['for_date'])
        
    if not os.path.exists(input_file):
        raise IOError("Input file '%s' does not exist" % input_file)
    
    output_file = get_file_path(ael_dict['output_file'], ael_dict['for_date'])
    for_date = ael_dict['for_date'].to_string("%Y%m%d")
    
    LOGGER.info("Date: '%s'", for_date)
    LOGGER.info("Input file: '%s'", input_file)
    LOGGER.info("Output file: '%s'", output_file)
    
    trades_count = 0
    
    zero_cell_indices = {8, 9, 10, 11, 12, 13, 16, 17, 18, 19, 20, 21, 22, 
        35, 36, 37, 38, 39, 40, 41, 42, 43, 49, 55, 56, 60, 61, 62, 63, 64, 
        65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 80, 81, 82, 83, 
        84, 85, 86, 87, 88, 89, 90, 91, 92, 94, 96, 97, 98, 100, 101, 102, 103}
    
    with open(input_file, "Urb") as inpt_csv_file:
        reader = csv.reader(inpt_csv_file, delimiter="\t")
        
        with open(output_file, 'wb') as out_csv_file:
            writer = csv.writer(out_csv_file, lineterminator=DELIM_LINE, delimiter=DELIM_CELL)
            writer.writerow(["H", "FA", for_date])
            
            for line in reader:
                if not line:
                    continue
                
                if line[0].isdigit():
                    if not line[3]:  # InsType column
                        continue
                                
                    for idx in range(len(line)):
                        if idx in zero_cell_indices:
                            if not line[idx]:
                                line[idx] = "0.0"
                            elif not line[idx].startswith('#'):
                                line[idx] = float(line[idx].replace(',', ''))
                            else:
                                line[idx] = line[idx].replace(',', '')
                            
                    writer.writerow(line)
                    trades_count += 1
                if line[1] == 'Instrument':
                    line[0] = 'Trade'
                    writer.writerow(line)
            
            writer.writerow(["F", trades_count])
            
    LOGGER.output(output_file)
    LOGGER.info("Completed successfully.")

import acm
from PS_CashReconReport import get_client_list

CUSTOM_DATE = '2015-04-30'
CUSTOM_DATE_MINUS_FIVE_BUSS_DAYS = '2015-04-22'

TASKS = (
    ('PS_AddTradeFees_CLIENT_SERVER',
        {'executionDate': 'Custom Date',
         'executionDateCustom': CUSTOM_DATE},
     ),
    ('PS_Generate_CLIENT_SERVER', 
        {'startDate': 'Custom Date',
         'startDateCustom': CUSTOM_DATE_MINUS_FIVE_BUSS_DAYS,
         'endDate': 'Custom Date',
         'endDateCustom': CUSTOM_DATE},
     ),
    ('PS_MTM_CLIENT_SERVER',
        {'startDate': 'Custom Date',
         'startDateCustom': CUSTOM_DATE_MINUS_FIVE_BUSS_DAYS,
         'endDate': 'Custom Date',
         'endDateCustom': CUSTOM_DATE},
     ),
    ('PS_Extend_General_PSwaps_CLIENT_SERVER',
        {'startDate': 'Custom Date',
         'startDateCustom': CUSTOM_DATE,
         'endDate': 'Custom Date',
         'endDateCustom': CUSTOM_DATE,
         'resweepTPL': 'Yes'},
     ),
    ('PS_TPLSweep_General_PSwaps_CLIENT_SERVER',
        {'startDate': 'Custom Date',
         'startDateCustom': CUSTOM_DATE,
         'endDate': 'Custom Date',
         'endDateCustom': CUSTOM_DATE},
     ),
    ('PS_Sweeping_CLIENT_SERVER',
        {'startDate': 'Custom Date',
         'startDateCustom': CUSTOM_DATE_MINUS_FIVE_BUSS_DAYS,
         'endDate': 'Custom Date',
         'endDateCustom': CUSTOM_DATE},
     ),
#    ('PS_SetAddInfoDate_CLIENT_SERVER', {}),
    ('PS_LoanAccountSweeper_CLIENT_SERVER',
        {'date': CUSTOM_DATE},
     ),
    ('PS_FRerate_CLIENT_SERVER',
        {'date': CUSTOM_DATE},
     ),
)

CLIENTS = get_client_list()

TASK_SUFFIX = '_CUSTOM'

CUSTOM_TASKS = []


for task in TASKS:
    for client in CLIENTS:
        original_name = task[0].replace('CLIENT', client)
        
        if not acm.FAelTask[original_name]:
            print("Warning: '%s' is not a valid task." % original_name)
            continue
        
        custom_name = original_name + TASK_SUFFIX        
        custom_task = acm.FAelTask[original_name].Clone()
        custom_task.Name(custom_name)
        
        ael_parameters = custom_task.Parameters()
        ael_param_keys = map(str, ael_parameters.Keys())
        for param, value in task[1].iteritems():
            if param in ael_param_keys:
                ael_parameters.AtPutStrings(param, value)
            else:
                print("Warning: '%s' is not a valid %s parameter." % (param, original_name))
        
        custom_task.Parameters(ael_parameters)
        custom_task.Commit()
        
        CUSTOM_TASKS.append(custom_task.Name())
        

print('Created tasks:')
print('\n'.join(CUSTOM_TASKS))

"""Resweeping tool - batch-run Prime Services sweeping tasks from PRIME."""

from datetime import datetime

import acm


TASK_PARAM_MAPPING = { # { <task_id>: {<task_param_name>: <ael_variables_key>}}
    'PS_Generate': {
        'startDateCustom': 'startDate',
        'endDateCustom': 'endDate',
    },
    'PS_MTM': {
        'startDateCustom': 'startDate',
        'endDateCustom': 'endDate',
    },
    'PS_Extend_General_PSwaps': {
        'startDateCustom': 'startDate',
        'endDateCustom': 'endDate',
        'resweepTPL': 'resweepTPL',
    },
    'PS_TPLSweep_General_PSwaps': {
        'startDateCustom': 'startDate',
        'endDateCustom': 'endDate',
    },
    'PS_Sweeping': {
        'startDateCustom': 'startDate',
        'endDateCustom': 'endDate',
    },
}

TASK_ADDITIONAL_PARAMS = { # Additional parameters that need to be set for the tasks, regardless of config.
    'PS_Generate': {
        'startDate': 'Custom Date',
        'endDate': 'Custom Date',
    },
    'PS_MTM': {
        'startDate': 'Custom Date',
        'endDate': 'Custom Date',
    },
    'PS_Extend_General_PSwaps': {
        'startDate': 'Custom Date',
        'endDate': 'Custom Date',
    },
    'PS_TPLSweep_General_PSwaps': {
        'startDate': 'Custom Date',
        'endDate': 'Custom Date',
    },
    'PS_Sweeping': {
        'startDate': 'Custom Date',
        'endDate': 'Custom Date',
    },
}


TASK_NAMES = { # To be supplemented with client names.
    'PS_Generate': 'PS_Generate_%s_SERVER',
    'PS_MTM': 'PS_MTM_%s_SERVER',
    'PS_Extend_General_PSwaps': 'PS_Extend_General_PSwaps_%s_SERVER',
    'PS_TPLSweep_General_PSwaps': 'PS_TPLSweep_General_PSwaps_%s_SERVER',
    'PS_Sweeping': 'PS_Sweeping_%s_SERVER',
}


VARNAME_TO_TASK_ID = ( # Tuple of pairs instead of a dictionary to preserve ordering.
    ('runPSGenerate', 'PS_Generate'),
    ('runPSMTM', 'PS_MTM'),
    ('runPSExtendGeneralPSwaps', 'PS_Extend_General_PSwaps'),
    ('runPSTPLSweepGeneralPSwaps', 'PS_TPLSweep_General_PSwaps'),
    ('runPSSweeping', 'PS_Sweeping'),
)


# Variable name, Display name, Type, Candidate values, Default, Mandatory, Multiple, Description, InputHook, Enabled
ael_variables = [
    ['clientNames', 'Client names', 'string', None, '', 1, 1, 'A comma separated list of short client names', None, 1],
    ['resweepTPL', 'Resweep TPL', 'string', ['Yes', 'No'], 'No', 1, 0, '', None, 1],
    ['startDate', 'Start Date', 'string', '', acm.Time.DateToday(), 1, 0, None, 1],
    ['endDate', 'End Date', 'string', '', acm.Time.DateToday(), 1, 0, None, 1],
]
for varname, task_id in VARNAME_TO_TASK_ID:
    task_id_display = task_id.replace('_', ' ') # To avoid splitting into multiple tabs.
    row = [varname, task_id_display, 'string', ['Yes', 'No'], 'No', 1, 0, '', None, 1]
    ael_variables.append(row)


class ValidationError(Exception):
    pass


def get_task_name(task_id, client_name):
    return TASK_NAMES[task_id] % client_name


def get_updated_params(task_id, task_params, config):
    for param_key, config_key in TASK_PARAM_MAPPING[task_id].iteritems():
        task_params.AtPutStrings(param_key, config[config_key])
    for key, val in TASK_ADDITIONAL_PARAMS[task_id].iteritems():
        task_params.AtPutStrings(key, val)
    return task_params


def run_task(task_id, client_name, config):
    task_name = get_task_name(task_id, client_name)
    task = acm.FAelTask[task_name].Clone()
    params = get_updated_params(task_id, task.Parameters(), config) # task.Parameters() creates a copy.
    task.Parameters(params)
    task.Execute(False) # Don't create history.


def validate(config):
    """Raise a ValidationError in case the config contains any errors."""
    for client_name in config['clientNames']:
        for varname, task_id in VARNAME_TO_TASK_ID:
            if config[varname] == 'Yes':
                task_name = get_task_name(task_id, client_name)
                if acm.FAelTask[task_name] is None:
                    raise ValidationError('Cannot find the task %s' % task_name)
    try:
        datetime.strptime(config['startDate'], '%Y-%m-%d')
        datetime.strptime(config['endDate'], '%Y-%m-%d')
    except ValueError:
        raise ValidationError('Please use the YYYY-MM-DD format for dates.')


def ael_main(config):
    try:
        validate(config)
    except ValidationError, e:
        print('Invalid input for resweeping: %s' % e)
        acm.GetFunction('msgBox', 3)("Invalid input for resweeping", '%s' % e, 0)
        return

    for client_name in config['clientNames']:
        for varname, task_id in VARNAME_TO_TASK_ID:
            if config[varname] == 'Yes':
                print('\n\nRunning %s for %s\n\n' % (task_id, client_name))
                run_task(task_id, client_name, config)

    print('Completed successfully.')

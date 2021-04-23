"""Script used for managing of existing TradeArchivation batches.

History
C1024176    Jan Sinkora         Initial deployment.

"""

import aggregation
import aggregation_graveyard
from at_ael_variables import AelVariableHandler
import at_progress
import acm
from datetime import datetime

ael_gui_parameters = {'windowCaption': 'Manage aggregation batches',
                      'runButtonLabel': '&&Run action',
                      'closeWhenFinished': True}

STATES = aggregation.Aggregation.STATES
# FIXME remove the 'revert' options if needed.
ACTIONS = {(STATES.PREPARED, STATES.SETUP): 'delete',
           (STATES.SETUP, STATES.DELETED): 'delete',
           (STATES.SETUP, STATES.PREPARED): 'prepare',
           (STATES.PREPARED, STATES.RUNNING): 'run',
           (STATES.FINISHED, STATES.RESETTING): 'revert',
           (STATES.BROKEN, STATES.RESETTING): 'revert'}


def get_action_names(batch):
    """Return all possible action names for the current batch state."""
    state = batch.config['aggregation_state']
    new_states = batch.possible_transitions()
    return ['save'] + [ACTIONS[(state, s)] for s in new_states if (state, s) in ACTIONS]


agg_type_classes = {'MO Trades': aggregation.TradeAggregationMO,
                    'Graveyard Trades': aggregation_graveyard.GraveyardAggregation}

NEW_AGG_NAME = 'New aggregation batch'

def type_select(var):
    agg_type = var.value
    agg_type_prefixes = dict(map(lambda k_cls: (k_cls[0], k_cls[1].AGGREGATION_TYPE),
        agg_type_classes.iteritems()))

    prefixes = set(agg_type_prefixes.values())
    enabled_prefix = agg_type_prefixes[agg_type]
    disabled_prefixes = prefixes - set(enabled_prefix)

    # Enable/disable and empty the type-specific parameters.
    for var in ael_variables:
        if var.name.startswith(enabled_prefix):
            var.enabled = True
        else:
            for prefix in disabled_prefixes:
                if var.name.startswith(prefix):
                    var.enabled = False

    # Reset the collection for batch selection.
    var_aggregation = ael_variables.get('aggregation')
    agg_class = agg_type_classes[agg_type]
    collection = [NEW_AGG_NAME] + agg_class.select_all()
    var_aggregation.collection = collection

    if not var_aggregation.value in map(str, collection):
        # Default is new batch creation.
        var_aggregation.value = NEW_AGG_NAME
        select_aggregation(var_aggregation)


def select_aggregation(var_aggregation):
    """Callback for the changing of the aggregation batch field."""

    if not var_aggregation.value:
        # This happens only when the window is first opened.
        # Nothing needs to be done.
        return

    # Get the variable instances.
    var_type = ael_variables.get('type')
    var_date = ael_variables.get('date')
    var_description = ael_variables.get('description')
    var_action = ael_variables.get('action')
    var_state = ael_variables.get('state')

    agg_type = var_type.value
    agg_name = var_aggregation.value

    if agg_name == NEW_AGG_NAME:
        # Disable and empty the fields.
        var_action.enabled = False
        var_action.collection[:] = ['create']
        var_action.value = var_action.collection[0]

        var_state.value = 'NOT CREATED'
        var_date.value = acm.Time.DateToday()
        var_date.enabled = False
    else:
        # Select the aggregation and fill the relevant fields.
        agg_class = agg_type_classes[agg_type]
        batch = agg_class.from_name(agg_name)

        var_description.value = batch.config['description']
        var_date.value = batch.config['date']
        var_date.enabled = False

        var_action.enabled = True
        var_action.collection[:] = get_action_names(batch)

        var_state.value = batch.config['aggregation_state']
        if var_action.value not in var_action.collection:
            var_action.value = var_action.collection[0]

        batch.set_ael_variable_values(ael_variables)

ael_variables = AelVariableHandler()
ael_variables.add('type',
                  label='Type of aggregation',
                  default='MO Trades',
                  collection=agg_type_classes.keys(),
                  hook=type_select)
ael_variables.add('aggregation',
                  label='Aggregation',
                  alt='Aggregation batch.',
                  collection=[],
                  hook=select_aggregation)
ael_variables.add('date',
                  label='Date')
ael_variables.add('description',
                  mandatory=False,
                  label='Description')
ael_variables.add('state',
                  label='Batch state',
                  enabled=False)
ael_variables.add('action',
                  label='Action',
                  collection=[])
# Load the aggregation-type-specific parameter definitions.
for cls in agg_type_classes.itervalues():
    cls.add_ael_variables(ael_variables)


def ael_main(params):
    agg_type = params['type']
    aggregation_name = params['aggregation']
    description = params['description']
    action = params['action']

    agg_class = agg_type_classes[agg_type]

    log = aggregation.LOG

    get_duration = at_progress.start_stopwatch()

    if aggregation_name == NEW_AGG_NAME:
        # Create a new aggregation batch.
        batch_date = params['date']

        # Check date format.
        datetime.strptime(batch_date, '%Y-%m-%d')
        agg_for_date = agg_class.from_date(batch_date)
        if agg_for_date:
            msg = "An aggregation config for date {0} already exists: {1}."
            log.error(msg.format(batch_date, agg_for_date.name))
            return

        batch = agg_class.create(batch_date, description, log)
    else:
        batch = agg_class.from_name(aggregation_name)


    # Save changes to the common config items.
    batch.config['description'] = description

    if action != 'revert':
        # All actions except reverting require setup from parameters.
        # Reset sets batch up from the saved settings.
        # Setup the additional parameters.
        batch.setup_from_ael_params(params)

    if action == 'create':
        if not batch.check_inputs():
            log.error("The input files have errors.")
            for e in batch.errors:
                log.error(e)
            batch.delete()
            return

        try:
            batch.prepare()
        except aggregation.Aggregation.GeneralError:
            log.exception("There was an error during preparation, deleting the batch.")
            batch.delete()
    elif action == 'delete':
        if batch.config['aggregation_state'] == batch.STATES.PREPARED:
            batch.cancel()
        batch.delete()
    elif action == 'prepare':
        batch.prepare()
    elif action == 'run':
        batch.run()
    elif action == 'revert':
        batch.reset()

    duration = get_duration()
    print "Took {0}s".format(duration)

    if action != 'delete':
        # This must not run when deleting as it would save the extension again.
        batch.config['stats_last_action_duration'] = duration
        if action == 'run':
            batch.config['stats_run_duration'] = duration

    print "Completed successfully"



"""-----------------------------------------------------------------------------
PURPOSE              :  Force a selection of business process objects to a
                        specific state.
DEVELOPER            :  Libor Svoboda
--------------------------------------------------------------------------------

HISTORY
================================================================================
Date        Change no      Developer           Description
--------------------------------------------------------------------------------
2020-10-20  CHG0132720     Libor Svoboda       Initial implementation
"""
import acm
from at_ael_variables import AelVariableHandler
from at_logging import getLogger


LOGGER = getLogger(__name__)


ael_variables = AelVariableHandler()
ael_variables.add(
    'business_processes',
    label='Business process objects',
    cls='FBusinessProcess',
    default='',
    multiple=True,
    mandatory=True,
    alt='Selected business process objects.'
)
ael_variables.add(
    'force_to_state',
    label='Force to state',
    cls='string',
    collection=sorted({state.Name() 
                           for state in acm.FStateChartState.Select('')}),
)
ael_variables.add(
    'reason',
    label='Reason',
    cls='string',
    default='',
    mandatory=False,
)


def ael_main(ael_params):
    LOGGER.msg_tracker.reset()
    LOGGER.info('Selected %s business process objects.' 
                % len(ael_params['business_processes']))
    force_to_state = ael_params['force_to_state']
    reason = ael_params['reason'] if ael_params['reason'] else ''
    LOGGER.info('Forcing them to "%s" with reason "%s".' 
                % (force_to_state, reason))
    for bp in ael_params['business_processes']:
        try:
            bp.ForceToState(force_to_state, reason)
            bp.Commit()
        except:
            LOGGER.exception('Business process %s: Failed to force to state.' 
                             % bp.Oid())
        else:
            LOGGER.info('Business process %s: Forced to state successfully.' 
                        % bp.Oid())
    
    if LOGGER.msg_tracker.errors_counter:
        raise RuntimeError('ERRORS occurred. Please check the log.')
    LOGGER.info('Completed successfully.')

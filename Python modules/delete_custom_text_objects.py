"""-----------------------------------------------------------------------------
PURPOSE              :  Generic script to delete a selection of custom text
                        objects.
DEVELOPER            :  Libor Svoboda
--------------------------------------------------------------------------------

HISTORY
================================================================================
Date        Change no      Developer        Description
--------------------------------------------------------------------------------
2019-04-05  CHG1001587723  Libor Svoboda    Initial implementation
"""
from at_ael_variables import AelVariableHandler
from at_logging import getLogger


LOGGER = getLogger(__name__)

ael_variables = AelVariableHandler()
ael_variables.add(
    'objects',
    label='Custom Text Objects',
    cls='FCustomTextObject',
    multiple=True,
)


def ael_main(ael_params):
    LOGGER.msg_tracker.reset()
    ctos = ael_params['objects']
    LOGGER.info('Selected %s Custom Text Objects.' % len(ctos))
    for cto in ctos[:]:
        cto_name = cto.Name()
        try:
            cto.Delete()
        except:
            LOGGER.exception('Failed to delete CTO "%s".' % cto_name)
        else:
            LOGGER.info('Deleted CTO "%s".' % cto_name)
    
    if LOGGER.msg_tracker.errors_counter:
        raise RuntimeError('ERRORS occurred. Please check the log.')
    LOGGER.info('Completed successfully.')


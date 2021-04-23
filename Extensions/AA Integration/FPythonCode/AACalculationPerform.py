""" Compiled: 2020-09-18 10:38:49 """

#__src_file__ = "extensions/aa_integration/./etc/AACalculationPerform.py"
"""----------------------------------------------------------------------------
MODULE
    AACalculationPerform - Run script GUI for performing calls to AA
        calculations

    (c) Copyright 2016 by SunGard FRONT ARENA. All rights reserved.

DESCRIPTION

----------------------------------------------------------------------------"""
import AAIntegrationUtility
import importlib
importlib.reload(AAIntegrationUtility)

def execute_perform(name, ael_params, calc_manger):

    sink = ael_params['Sink'] = str(ael_params['Sink']).strip()
    if sink not in calc_manger.SINKS:
        msg = 'Invalid sink, select from:', calc_manger.SINKS
        raise AssertionError(msg)

    indentation = AAIntegrationUtility.DEFAULT_INDENTATION
    logger = AAIntegrationUtility.getLogger(name, ael_params)
    logger.info('Initialised %s logger' % name)
    logger.info('Starting %s' % name)
    calc_executer = None
    try:
        logger.debug(indentation + 'Initialising calculation executer')
        calc_type = ael_params['AnalysisType'].strip()
        calc_class = calc_manger.getCalculationClass(
            sink=sink, calc_type=calc_type
        )
        logger.debug('%sUsing calculation executer "%s"' % \
                     (indentation * 2, calc_class.NAME))
        calc_executer = calc_class(ael_params)
        logger.debug(indentation + 'Calculation executer initialised')
    except Exception as e:
        import traceback
        traceback.print_exc()
        logger.error(indentation + 'Failed to initialise: ' + str(e))
        logger.info('Finished %s' % name)
        return
    else:
        if calc_executer is None:
            logger.error(indentation + 'Failed to initialise: ' + str(e))
            logger.info('Finished %s' % name)
            return

    try:
        name = calc_executer.NAME
        logger.info('%sPerforming %s calculation:' % (indentation, name))
        success = _perform(
            calc_executer=calc_executer, logger=logger,
            prefix='%s %s' % (indentation * 2, name)
        )
        logger.info('%s%s execution: %s.' % \
                    (indentation, name, 'Done' if success else 'Failed'))
    except Exception as e:
        logger.error(indentation + 'Error: %s' % str(e))
        import traceback
        traceback.print_exc()

    logger.info('Finished %s' % name)
    return

def _perform(calc_executer, logger, prefix):
    msgs = calc_executer.performRequest()

    # Log response msgs
    for info in msgs.infos:
        logger.info(prefix + ' execution: ' + info)

    for warn in msgs.warnings:
        logger.warn(prefix + ' execution warning: ' + warn)

    for error in msgs.errors:
        logger.error(prefix + ' execution error: ' + error)

    success = len(msgs.errors) == 0
    return success

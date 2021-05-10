""" Compiled: 2020-09-18 10:38:49 """

#__src_file__ = "extensions/aa_integration/./etc/AAXVAPerform.py"
import AAIntegrationUtility

def perform(name, parameters, exporters):
    logger = AAIntegrationUtility.getLogger(name, parameters)
    logger.info('Initialised %s logger.' % logger.Name())
    logger.info('Starting %s.' % name)
    success = True
    indentation = AAIntegrationUtility.DEFAULT_INDENTATION
    indentation_level = 1
    if exporters:
        new_indentation_level = indentation_level + 1
        new_indentation = indentation * new_indentation_level
        for exporter in exporters:
            msg = 'Running %s exporter.' % exporter.NAME
            logger.info(indentation + msg)
            exporter.init(
                ael_params=parameters, logger=logger,
                indentation=indentation,
                indentation_level=new_indentation_level
            )
            msg = 'Will write files to %s.' % exporter.getOutputDir()
            logger.info(new_indentation + msg)
            performed = exporter.perform()
            success = success and performed
            output_files = exporter.getFilepaths()
            msg = 'The following files have been written:\n  %s' % (
                '\n  '.join(output_files)
            ) if output_files else 'No files generated.'
            logger.debug(new_indentation + msg)
            msg = 'Finished running %s exporter.' % exporter.NAME
            logger.info(new_indentation + msg)

        if success:
            logger.info(indentation + 'Finished writing output files.')
        else:
            logger.error(indentation + 'Failed to write all output files.')
    else:
        logger.info(indentation + 'Cannot find any valid exporters.')

    logger.info('Finished %s.' % name)
    return

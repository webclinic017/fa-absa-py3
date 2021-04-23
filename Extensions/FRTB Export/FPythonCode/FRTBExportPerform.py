""" Compiled: 2020-09-18 10:38:52 """

#__src_file__ = "extensions/frtb/./etc/FRTBExportPerform.py"
import collections
import os
import traceback

import acm

import FExportCalculatedValuesMain

import FRTBUtility

def perform(name, parameters, exporters):
    """
    Main driver for performing the FRTB calculations.
    """
    parameters['Logfile'] = str(parameters['Logfile']).strip()
    logger = FRTBUtility.createDefaultLogger(name, parameters)
    success = False
    error = None
    try:
        for e in exporters:
            e.setInternalParameters(parameters=parameters)

        enabled_exporters = tuple(e for e in exporters if e.isEnabled())
        if not enabled_exporters:
            logger.error('No exporter selected.')
            return

        enabled_exporters[0].WRITER_CLASSES[0].resetCache(
            group=exporters[0].CALC_GROUP
        )
        success = _writeAll(
            name=name, parameters=parameters,
            exporters=enabled_exporters, logger=logger
        )
        for e in exporters:
            e.isEnabled(parameters=parameters)
    except:
        success = False
        error = traceback.format_exc()

    if success:
        logger.info('  Finished writing output files.')
    else:
        if not error:
            error = traceback.format_exc()

        error = error.strip()
        error = (':\n' + error) if error and error != 'None' else '.'
        logger.error('  Failed to write all output files' + error)

    logger.info('Finished %s' % name)
    return

def _writeAll(name, parameters, exporters, logger):
    """
    In charge of validating parameters, initialising calculations,
    running and storing calculation and then exporting values.
    """

    # validate parameters and get parameterised functions
    exporters_func_map = _getExportersParamsFunctionsMap(
        exporters=exporters, parameters=parameters, name=name, logger=logger
    )
    # create results collectors which contains calculation columns & writers
    collectors = _getResultsCollectors(
        exporters_func_map=exporters_func_map,
        parameters=parameters, logger=logger
    )
    if not collectors:
        return collectors

    logger.info('Starting %s' % name)
    logger.info('  Performing calculations.')
    success = True
    for collector in collectors:
        writers = collector.getWriters()
        calc_names = '\n  ' + '\n  '.join(
            '%s (%s)' % (w.CALC_NAME_LONG, w.CALC_NAME) for w in writers
        )
        column_names = '\n  ' + '\n  '.join(
            c.customColumnName for c in collector.getColumns()
        )
        logger.info('    Performing calculation(s):%s' % calc_names)
        logger.debug('    Performing calculation(s) for:%s' % column_names)
        try:
            collector.populate()
            logger.debug('    Finished calculation(s) for:%s' % column_names)
        except:
            logger.info('    Calculation(s) failed:\n' + traceback.format_exc())
            success = False
            continue

        try:
            for writer in writers:
                if not _write(writer=writer, logger=logger):
                    success = False
        except:
            logger.info('    Writing file(s) failed:\n' + traceback.format_exc())
            success = False

    return success

def _getExportersParamsFunctionsMap(exporters, parameters, name, logger):
    # Validates parameters (so ensure this is called as early as possible),
    # also uses parameters to identify positions to use in calculations
    # and where to export the values to.
    parameters['Logfile'] = str(parameters['Logfile']).strip()
    logger = FRTBUtility.createDefaultLogger(name, parameters)
    logger.info('Initialised %s logger.' % name)
    logger.debug('Validating %s parameters.' % name)

    separate_calculations = len([
        k for k in parameters.keys() if k.endswith('riskFactorSetup')
    ]) > 1
    get_writer_filepath = _getWriterFilepathFunc(parameters=parameters)
    func_map = collections.OrderedDict() # order dependent variable
    context = acm.GetDefaultContext()
    if not separate_calculations:
        get_trade_header, perform_calc, get_grouping_attrs = _getPositionSpecFuncs(
            parameters=parameters, prefix='', context=context
        )
        func_map[exporters] = \
            (get_trade_header, perform_calc, get_writer_filepath, get_grouping_attrs)
    else:
        for e in exporters:
            params = dict(
                (k, v) for k, v in parameters.items() if k.startswith(e.CALC_NAME)
            )
            get_trade_header, perform_calc, get_grouping_attrs = _getPositionSpecFuncs(
                parameters=params, prefix=e.CALC_NAME, context=context
            )
            func_map[e] = (get_trade_header, perform_calc, get_writer_filepath, get_grouping_attrs)

    return func_map

def _getWriterFilepathFunc(parameters):
    dir_path = os.path.join(str(parameters['OutputDir']).strip(), parameters['CalcType'])
    prefix = parameters['Prefix']
    ext = parameters['Extension']
    create_date_dir = parameters['DateDir']
    overwrite = parameters['Overwrite']

    get_writer_filepath = lambda writer_cls: \
        FRTBUtility.getOutputFilename(
            prefix=prefix, filename=writer_cls.CALC_NAME.replace('-', '_'),
            dir_path=dir_path, sub_dir_name=os.path.join(
                writer_cls.CALC_GROUP, writer_cls.OUTPUT_SUB_DIR
            ).lower(), create_date_dir=create_date_dir,
            overwrite=overwrite, ext=ext
        )
    return get_writer_filepath

def _calculate_distributed_mode(portfolios, tradeFilters, storedQueries, 
        columnConfigs, attributes, writers, distributedCalculations):
    
    try:
        FExportCalculatedValuesMain.main(portfolios, tradeFilters, 
                storedQueries, columnConfigs, attributes, writers, distributedCalculations)
    except Exception as err:
        print((" Exception in _calculate_distributed_mode {0}".format(str(err))))
        if distributedCalculations:
            print(" Try none distributed mode instead")
            FExportCalculatedValuesMain.main(portfolios, tradeFilters, 
                storedQueries, columnConfigs, attributes, writers)

def _getPositionSpecFuncs(parameters, prefix, context):
    port_names = [
        i.Name() for i in parameters.get(prefix + 'Portfolios', [])
    ]
    trade_filter_names = [
        i.Name() for i in parameters.get(prefix + 'Trade Filters', [])
    ]
    stored_asql_query_names = [
        i.Name() for i in parameters.get(prefix + 'Trade Queries', [])
    ]
    if len(port_names + trade_filter_names + stored_asql_query_names) == 0:
        msg = (
            'At least one type of trade selection is expected '
            '(Portfolios/Trade Filters/Trade Queries).'
        )
        raise AssertionError(msg)

    position_spec = parameters[prefix + 'Position Specification']
    distributedCalculations = parameters[prefix + 'distributedCalculations']
    grouper, trade_header, grouping_attrs = _getTradeGrouper(position_spec, context)
    # funcs
    get_trade_header = lambda: trade_header
    get_grouping_attrs = lambda: grouping_attrs
    perform_calc = lambda collector: \
        _calculate_distributed_mode(
            port_names, trade_filter_names, stored_asql_query_names,
            collector.getColumns(), grouper, [collector], distributedCalculations
        )

    return get_trade_header, perform_calc, get_grouping_attrs

def _getTradeGrouper(position_spec, context):
    # Return the positions and positions info to use in the calculation
    # and export file, respectively.
    context_name = context.Name()
    grouping_attrs = []
    has_trade_ref = False
    for attr_def in  position_spec.AttributeDefinitions():
        method_chain = attr_def.Definition()
        display_name = acm.Sheet.Column().MethodDisplayName(
            acm.FTrade, method_chain, context_name
        )
        grouping_attrs.append([display_name, method_chain, False])

    trade_header = [h[0] for h in grouping_attrs]
    grouper = acm.Risk().CreateChainedGrouperDefinition(
        acm.FTrade, 'Portfolio', False, 'Instrument', True, grouping_attrs
    )
    return grouper, trade_header, grouping_attrs

def _getResultsCollectors(exporters_func_map, parameters, logger):
    # Create calculation columns.
    logger.debug('  Creating calculation columns.')
    collectors = collections.OrderedDict() # order dependent variable
    writers_map = {}
    exporters, funcs = exporters_func_map.keys(), exporters_func_map.values()
    if (len(exporters) == 1) and isinstance(exporters[0], tuple):
        exporters = exporters[0]
        funcs = funcs * len(exporters)

    for e, funcs in zip(exporters, funcs):
        logger.info('  Creating %s calculation columns.' % e.CALC_NAME_LONG)
        get_trade_header, perform_calc, get_writer_filepath, get_grouping_attrs = funcs
        trade_attrs = get_trade_header()
        grouping_attrs = get_grouping_attrs()
        additional_writer_kwargs = e.getAdditionalWriterKwargs()
        
        for column in e.makeColumns(parameters=parameters):
            collector = collectors.get(e.RESULTS_COLLECTOR_CLASS)
            if not collector:
                collector = collectors[e.RESULTS_COLLECTOR_CLASS] = \
                    e.RESULTS_COLLECTOR_CLASS(
                        ael_params=parameters, perform_cb=perform_calc
                    )

            writers = []
            for writer_cls in e.WRITER_CLASSES:
                writer = writers_map.get(writer_cls)
                if not writer:
                    output_path = get_writer_filepath(writer_cls=writer_cls)
                    writer = writers_map[writer_cls] = writer_cls(
                        results_collector=collector,
                        trade_attributes=trade_attrs,
                        output_path=output_path,
                        grouping_attributes=grouping_attrs,
                        additional_writer_kwargs=additional_writer_kwargs
                    )

                writers.append(writer)

            collector.updateCalculationsParams(column=column, writers=writers)

    collectors = collectors.values()
    if sum(len(c.getColumns()) for c in collectors) == 0:
        logger.error('  Failed: No calculations detected')
        return tuple()

    logger.debug('  Calculation columns created.')
    return tuple(collectors)

def _write(writer, logger):
    # Writer the calculated values to file
    success = True
    logger.info('    Writing %s export file:' % writer.CALC_NAME)
    result = writer.write()
    if result is None:
        logger.warn('      Generated nothing to write')
        error = traceback.format_exc().strip()
        success = (not error) or (error == 'None')
    elif result == False:
        logger.warn('      Failed to write output file')
        success = success and False
    else:
        for warning_type, rows in result.items():
            if len(rows):
                logger.warn('      Warnings: %s:' % warning_type)
                for row in sorted(rows):
                    logger.warn('        %s' % row)

        logger.info('      %s written.' % writer.getFilepath())

    return success

""" Compiled: 2020-06-22 15:41:12 """

#__src_file__ = "extensions/frtb/./etc/FRTBSASBAExport.py"
"""----------------------------------------------------------------------------
MODULE
    (c) Copyright 2016 FIS Front Arena. All rights reserved.

DESCRIPTION
----------------------------------------------------------------------------"""
import re

import acm
import ael
import sys

import FRTBExport
import FRTBBaseWriter
import FRTBCommon
import FRTBSAStaticData
import FBDPHook

# Writers
class SBAResultsCollector(FRTBBaseWriter.CommonResultsCollector):
    COLUMN_IDS = FRTBBaseWriter.CommonResultsCollector.COLUMN_IDS + \
        (FRTBCommon.SA_SBA_COLUMN_ID,)
    
    def getData(self):
        data = {}
        print((sys.getsizeof(self._result_dictionary)))
        for pos_key, pos_key_dict in self._result_dictionary.iteritems():
            trade_attrs = self.getTradeAttributes(pos_key)
            #print pos_key_dict
            is_option = \
                self.getCommonData(pos_key_dict)[FRTBCommon.IS_OPTION_COLUMN_ID]
            trade_attrs += (is_option,)
            for column_id, results in pos_key_dict.iteritems():
                if column_id == FRTBCommon.IS_OPTION_COLUMN_ID:
                    continue

                dim_names = self._dimension_names.get(column_id)
                if dim_names is None:
                    continue

                common_dim_names = tuple(dim_names[:5])
                _, measure_name = column_id.split('|')
                for dims, result in results.iteritems():
                    common_dims = tuple(dims[:5])
                    data_key = (common_dim_names, common_dims, trade_attrs)
                    values = result
                    if isinstance(values, dict):
                        values = []
                        for horizons, value in result.iteritems():
                            values.append(horizons + (value,))
                        result.clear()

                    data.setdefault(data_key, {})[measure_name] = \
                        (dim_names, dims, values)
                #MRA
                results.clear()
            pos_key_dict.clear()
            pos_key_dict = None
        self._result_dictionary.clear()
        self._result_dictionary = None
        return data
    
    def getOrderedDimensions(self, column_id, dimensions):
        dim_names = self._dimension_names[column_id]
        rf_name_idx = 3
        if ('Sub Type' not in dim_names) or ('Bucket' not in dim_names):
            rf_name_idx = 2

        rf_name = dimensions[rf_name_idx]
        dims = [rf_name, rf_name]
        for i, d in enumerate(dimensions):
            dims.append(d)
        
        return tuple(str(d) if d is not None else '' for d in dims)

    def _updateResult(self, result_dict, result_key, value, proj_coords):
        buckets = tuple(pc for pc in proj_coords if self._isTimeBucket(pc))
        result_dict.setdefault(result_key, {})[buckets] = value
        return

class MeasurementBaseSBAWriter(FRTBBaseWriter.Writer):
    # N.B. Instead of this tuple, we could use only the risk factor names
    # contained in rf_info???
    _RISK_FACTOR_ATTRIBUTES = (
        'ID', 'Name',
        'Risk Class', 'Bucket', 'Sub Type', 'Commodity', 'Location',
        'Grade', 'Market Cap', 'Economy', 'Sector', 'Credit Quality', 'Issuer',
        'Tranche', 'Base Currency', 'Currency Pair', 'Quote Currency',
        'Electricity Time', 'Electricity Area', 'Freight Route', 'Freight Week'
    )
    _MEASUREMENT_NAMES = None

    def __init__(
        self, results_collector, trade_attributes,
        output_path, grouping_attributes,
        additional_writer_kwargs
    ):
        self._rfNameHandlerHook = None
        try:
            self._rfNameHandlerHook = FBDPHook.RiskFactorNameHandler
        except Exception as e:
            msg = "Hook RiskFactorNameHandler is not enabled."
            ael.log(msg)
        super(MeasurementBaseSBAWriter, self).__init__(
            results_collector=results_collector,
            trade_attributes=trade_attributes,
            output_path=output_path,
            grouping_attributes=grouping_attributes,
            additional_writer_kwargs=additional_writer_kwargs
        )

    def getRFHHook(self):
        return self._rfNameHandlerHook

    # header is a list of the risk factors and also the trade attributes
    # all the properties that need to be partitionable
    def _createHeader(self):
        header = []

        #Risk Factor.ID,Risk Factor.Name,Risk Factor.Risk Class,Risk Factor.Bucket,
        #Risk Factor.Sub Type,Risk Factor.Commodity,Risk Factor.Location,
        #Risk Factor.Grade,Risk Factor.Market Cap,Risk Factor.Economy,
        #Risk Factor.Sector,Risk Factor.Credit Quality,Risk Factor.Issuer,
        #Risk Factor.Tranche,Risk Factor.Base Currency,Risk Factor.Quote Currency
        prefix = 'Factor.'
        for label in self._RISK_FACTOR_ATTRIBUTES:
            header.append(prefix + label)

        #Trade.Reference,Trade.Region,Trade.Area,Trade.Desk,Trade.Product Type,
        #Trade.Is Option
        header.extend(self._getDefaultTradeHeader())
        header.append('Trade.Is Option')

        header.extend(name + ' Input' for name in self._MEASUREMENT_NAMES)
        return header

    def _getMeasurementResultKeys(self):
        return self._MEASUREMENT_NAMES

    def _getRows(self, header):
        mks = self._getMeasurementResultKeys()
        measures = [(mn, mk) for mn, mk in zip(self._MEASUREMENT_NAMES, mks)]
        rows = []
        for data_key, measurements in self._results.iteritems():
            
            trade_attrs = data_key[-1]
            is_option = trade_attrs[-1]
            trade_attrs = self._getDefaultTradeAttributes(
                trade_attrs=trade_attrs[:-1]
            )
            
            # Trade.Is Option
            trade_attrs.append('Yes' if is_option else 'No')
            skip_row = False
            results = []
            ordered_rf_values = [''] * len(self._RISK_FACTOR_ATTRIBUTES)
            for measurement_name, measurement_key in measures:
                if not self._shouldWriteValue(measurement_name, is_option):
                    results.append('')
                    continue

                result = measurements.get(measurement_key)
                if not result:
                    results.append('')
                    continue
                
                rf_names, rf_values, result = result
                result = self._parseResults(result, measurement_name)
                if (result is None) or (result == ''):
                    results.append('')
                    continue
                
                self._updateRiskFactorValues(
                    rf_names=rf_names, rf_values=rf_values,
                    ordered_rf_values=ordered_rf_values
                )
                row_id = ','.join(ordered_rf_values[:3] + trade_attrs)
                if self._omitResult(result, measurement_name, row_id):
                    skip_row = True
                    continue

                results.append(result or '0.0')
                #del measures[:]

            if (not skip_row) and any(results):
                if any(self._filterValue(r) for r in results):
                    rows.append(ordered_rf_values + trade_attrs + results)
            
            #measurements.clear()
            #del measurements
            #measurements = None
        return sorted(rows)

    def _getResultsFilters(self):
        measurement_keys = self._getMeasurementResultKeys()
        assert len(self._MEASUREMENT_NAMES) == len(measurement_keys), \
            'Number of measurements differs from number of results'
        return measurement_keys

    def _buildRiskFactorName(self, risk_class, rf_names, rf_values):
        hook = self.getRFHHook()
        nameIndex = rf_names.index('Name')
        rf_name = rf_values[nameIndex]
        if hook:
            try:
                rf_name = hook(risk_class, rf_names, rf_values)
            except Exception as e:
                msg = 'Caught exception from RiskFactorNameHandler hook: {}'.format(str(e))
                ael.log(msg)
            return rf_name
        if risk_class == 'FX':
            if 'Volatility' not in rf_names:
                if 'TermCurrency' in rf_names:
                    termCurrencyIndex = rf_names.index('TermCurrency')
                elif 'Term Currency' in rf_names:
                    termCurrencyIndex = rf_names.index('Term Currency')
                else:
                    return ""
                
                rf_name += '/' + rf_values[termCurrencyIndex]
        
        return rf_name

    def _updateRiskFactorValues(self, rf_names, rf_values, ordered_rf_values):
        risk_class = rf_values[self._RISK_FACTOR_ATTRIBUTES.index('Risk Class') + 1]
        for name, value in zip(rf_names, rf_values):
            try:
                idx = self._RISK_FACTOR_ATTRIBUTES.index(name)
                ordered_rf_values[idx] = value
            except:
                continue

        rf_name = self._buildRiskFactorName(risk_class, rf_names, rf_values)
        instrument = acm.FInstrument[rf_name]
        if instrument: 
            issuer = instrument.Issuer()
            if issuer:
                ordered_rf_values[self._RISK_FACTOR_ATTRIBUTES.index('Issuer')] = issuer.Name()
            
        if risk_class == 'FX':
            idx = self._RISK_FACTOR_ATTRIBUTES.index('Currency Pair')
            try:
                ordered_rf_values[idx] = re.search(
                    '.*([A-Zz-z]{3}[\./][A-Zz-z]{3}).*', rf_name
                ).group(1).replace('.', '/')
            except:
                ordered_rf_values[idx] = rf_name.replace('.', '/')
        elif risk_class == 'Equity':
            bucket_idx = self._RISK_FACTOR_ATTRIBUTES.index('Bucket')
            bucket = ordered_rf_values[bucket_idx]
            additional_attrs = FRTBSAStaticData.bucket_map[bucket]
            idx = self._RISK_FACTOR_ATTRIBUTES.index('Market Cap')
            ordered_rf_values[idx] = additional_attrs.MarketCap
        
        sub_type = ordered_rf_values[self._RISK_FACTOR_ATTRIBUTES.index('Sub Type')]
        if sub_type:
            rf_name = sub_type + '.' + rf_name
        
        ordered_rf_values[self._RISK_FACTOR_ATTRIBUTES.index('ID')] = rf_name
        ordered_rf_values[self._RISK_FACTOR_ATTRIBUTES.index('Name')] = rf_name

        return

    def _shouldWriteValue(self, measurement_name, is_option):
        raise NotImplementedError

    def _parseResults(self, result, measurement_name):
        if isinstance(result, list):
            value = []
            for v in result:
                val = v[-1].Number()
                if val is not None:
                    value.append(':'.join(v[:-1] + (str(val),)))

            return ';'.join(value)

        value = result.Number()
        return None if value is None else str(value)

    def _filterValue(self, value):
        if not value:
            return None

        try:
            return float(value) or None
        except ValueError:
            pass

        values = [self._filterValue(v.rsplit(':', 1)[-1]) for v in value.split(';')]
        return value if any(values) else None

class DeltaCurvatureSBAWriter(MeasurementBaseSBAWriter):
    CALC_NAME = 'Delta_Curvature'
    _MEASUREMENT_NAMES = ('Delta', 'Curvature Up', 'Curvature Down')

    def _shouldWriteValue(self, measurement_name, is_option):
        return measurement_name == 'Delta' or is_option

class VegaVolatilitySBAWriter(MeasurementBaseSBAWriter):
    CALC_NAME = 'Vega_Volatility'
    _MEASUREMENT_NAMES = ('Vega', 'Volatility')

    def _getMeasurementResultKeys(self):
        return ('Vega',) * len(self._MEASUREMENT_NAMES)

    def _shouldWriteValue(self, measurement_name, is_option):
        return is_option

    def _parseResults(self, result, measurement_name):
        if measurement_name == 'Volatility':
            # Volatility value
            value = []
            for v in result:
                val = 1.0
                value.append(':'.join(v[:-1] + (str(val),)))
            
            result = ';'.join(value)
            return result

        result = super(VegaVolatilitySBAWriter, self)._parseResults(
            result, measurement_name
        )
        return result

# Exporter
class SBAExport(FRTBExport.Export):
    RESULTS_COLLECTOR_CLASS = SBAResultsCollector
    WRITER_CLASSES = (DeltaCurvatureSBAWriter, VegaVolatilitySBAWriter)
    REQUIRES_IS_OPTION = True

    def makeColumns(self, parameters):
        columns = super(SBAExport, self).makeColumns(parameters=parameters)
        measures = ('Delta', 'Vega', 'Curvature Up', 'Curvature Down')
        risk_classes = parameters['riskClassNames']
        column_parameters = {
            acm.FSymbol('rfsetup'): parameters['riskFactorSetup'].Name()
        }
        measure_type_key = acm.FSymbol('measureType')
        risk_class_key = acm.FSymbol('riskClass')
        hierarchy_key = acm.FSymbol('hierarchy')
        hierarchy_name = str(parameters['hierarchy'].Name()).strip()
        context = acm.GetDefaultContext()
        for measure_type in measures:
            column_parameters[measure_type_key] = measure_type
            for risk_class in risk_classes:
                column_parameters[risk_class_key] = risk_class
                column_parameters[hierarchy_key] = hierarchy_name
                config = self.makeDynamicColumnConfig(
                    column_id='FRTB Dynamic Dimensions',
                    params=column_parameters
                )
                column = self.makeColumn(
                    column_id=FRTBCommon.SA_SBA_COLUMN_ID,
                    column_name=risk_class + '|' + measure_type, config=config
                )
                columns.append(column)

        return columns

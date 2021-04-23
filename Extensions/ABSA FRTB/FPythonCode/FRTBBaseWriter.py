""" Compiled: 2020-06-22 15:41:12 """

#__src_file__ = "extensions/frtb/./etc/FRTBBaseWriter.py"
"""---------------------------------------------------------------------------
MODULE
    Base Writer & ResultsCollector - To collect & write sensitivity data.

    (c) Copyright 2016 FIS Front Arena. All rights reserved.

DESCRIPTION

---------------------------------------------------------------------------"""
import collections
import math
import os
import sys
import re
import acm
import FRTBCommon
import FBDPCommon
import FRTBUtility;

def _additional_attributes():
    attributesStr = FBDPCommon.valueFromFParameter(
                'FRTBAdditionalAttributes', 'AdditionalAttributes')
    if attributesStr:
        return [i.strip() for i in attributesStr.split(',')]
    return []

def _method_from_attribute(attribute):
    return FBDPCommon.valueFromFParameter(
                'FRTBAttributeMethodMap', attribute)


class ResultsCollector(object):
    """
    Results store.
    The implementation of which is unique to each calculation group
    i.e. SBA vs ES.
    """
    COLUMN_IDS = None
    _USE_PROJECTION_COORDINATES = True

    def __init__(self, ael_params, perform_cb):
        self._perform_cb = perform_cb
        self._calc_columns = []
        self._writers = []
        self._result_dictionary = {}
        self._dimension_names = {}

    # required by FExportCalculatedValuesMain
    def addColumn(self, info, ID):
        if ID in self._dimension_names:
            return

        if info.vectorInformation and info.vectorInformation.dimensionNames:
            if (len(info.vectorInformation.dimensionNames) == 1) and \
                (str(info.vectorInformation.dimensionNames[0]) in self.COLUMN_IDS):
                return

            dimensions = ['Name', 'ID']
            for i, d in enumerate(info.vectorInformation.dimensionNames):
                d = str(d)
                if (d not in dimensions):
                    if d == 'Subtype':
                        d = 'Sub Type'
                    dimensions.append(d)

            self._dimension_names[ID] = tuple(dimensions)
        elif info.columnPartNames:
            if (len(info.columnPartNames) == 1) and \
                (str(info.columnPartNames[0]) in self.COLUMN_IDS):
                return

            self._dimension_names[ID] = tuple(str(n) for n in info.columnPartNames)

        return

    def addRootPosition(self, info, ID):
        pass

    def addPosition(self, info, ID):
        return

    def addResult(self, posInfoID, columnID, calculationInfos):
        if not calculationInfos:
            return
        position_key = None
        for calc_info in calculationInfos:
            if calc_info.values is None:
                continue
            if isinstance(calc_info.values, bool):
                pass
            elif isinstance(calc_info.values, float):
                pass
            elif isinstance(calc_info.values, str):
                pass

            if position_key is None:
                position_key = self._stripID(posInfoID, None)

            results = self._getResultDict(position_key, columnID)
            result_key = self._getResultKey(columnID, calc_info)
            buckets = []
            for pc in calc_info.projectionCoordinates:
                pc = str(pc)
                if self._isTimeBucket(pc):
                    buckets.append(pc.lower())

            if buckets:
                results.setdefault(result_key, collections.OrderedDict())
                results[result_key][tuple(buckets)] = calc_info.values
            else:
                results.setdefault(result_key, calc_info.values)
        return

    # required by FRTB Export framework
    def getOrderedDimensions(self, column_id, dimensions):
        # return values in the same order as the dimension names
        if (column_id not in self._dimension_names) or (len(dimensions) < 3):
            return tuple(str(v) for v in dimensions)

        dims = [dimensions[2], dimensions[2]]
        for i, d in enumerate(dimensions):
            if (i != 2):
                dims.append(d)

        return tuple(str(d) if d is not None else '' for d in dims)

    def updateCalculationsParams(self, column, writers):
        if column not in self._calc_columns:
            self._calc_columns.append(column)

        for w in writers:
            if w not in self._writers:
                self._writers.append(w)

        return

    def getColumns(self, column_ids=None):
        if column_ids:
            return [c for c in self._calc_columns if c.columnID in column_ids]

        return self._calc_columns

    def getWriters(self):
        return self._writers

    def populate(self):
        return self._perform_cb(collector=self)

    def getData(self):
        #iterates through stored results to produce
        #dictionary of organised output data.
        data = {}
        for pos_key, pos_key_dict in self._result_dictionary.iteritems():
            trade_attrs = self.getTradeAttributes(pos_key)
            data_by_trade = data.setdefault(trade_attrs, {})
            for column_id, result in pos_key_dict.iteritems():
                if isinstance(result, dict) and (len(result) == 1) and \
                (column_id in result):
                    result = result[column_id]

                data_by_trade[column_id] = result
        
            pos_key_dict.clear()
            pos_key_dict = None
        self._result_dictionary.clear()
        self._result_dictionary = None

        return data
    
    def getTradeAttributes(self, position_key):
        attributes = position_key.split('|')
        return tuple(attributes[2:-1])
    
    def _stripID(self, positionInfoID, key=None):
        #print positionInfoID
        rootID, parentID, name = positionInfoID
        #print rootID, parentID, name
        if parentID is None:
            #rootID is None if using trade filters or query folders
            if rootID is None:
                if key is None:
                    #shouldn't get here, means there is no grouping at all
                    key = '|'.join(('None', 'None'))
                else:
                    key = '|'.join(('None', 'None', key))
                return key
            #this is probably the root group
            first, second = rootID
            if key is None:
                key = '|'.join((second, first))
            else:
                key = '|'.join((second, first, key))
            
            return key
        else:
            if key is None:
                key = name
            else:
                key = '|'.join((name, key))

            return self._stripID(parentID, key)

    def _getResultDict(self, position_key, column_id):
        results = self._result_dictionary.setdefault(position_key, {})
        return results.setdefault(column_id, {})

    def _getResultKey(self, column_id, calc_info):
        if self._USE_PROJECTION_COORDINATES and calc_info.projectionCoordinates:
            dims = []
            for proj_coord in calc_info.projectionCoordinates:
                proj_coord = str(proj_coord)
                if not self._isTimeBucket(proj_coord):
                    dims.append(proj_coord)

            return self.getOrderedDimensions(column_id=column_id, dimensions=dims)

        return column_id

    def _isTimeBucket(self, text):
        return bool(re.match(r'^[0-9]+[dDwWmMyY]$', text))

class CommonResultsCollector(ResultsCollector):
    """
    Results store for common calculation columns.
    """
    COLUMN_IDS = (FRTBCommon.IS_OPTION_COLUMN_ID,)

    def getCommonData(self, pos_key_dict):
        result = pos_key_dict.get(FRTBCommon.IS_OPTION_COLUMN_ID)
        if result is None:
            return None

        is_option = bool(result[FRTBCommon.IS_OPTION_COLUMN_ID])
        return {FRTBCommon.IS_OPTION_COLUMN_ID: is_option}

class Writer(object):
    """
    Class representing each file writer, a type for each different
    file that needs to written.
    Should know how to retrieve the set of results from its corresponding
    results collector and handles all nuances of how it should format and
    display it's results.
    """
    # Overriding optional (otherwise automatically set in instance)
    CALC_NAME = CALC_NAME_LONG = None

    # Automatically populated
    CALC_GROUP = CALC_CLASS = CALC_CLASS_LONG = COLUMN_IDS = OUTPUT_SUB_DIR = None

    INSTANCES = {}
    _RESULTS = {}

    @staticmethod
    def resetCache(group):
        Writer.INSTANCES[group] = {}
        Writer._RESULTS[group] = {}
        return

    def __init__(self, results_collector, trade_attributes,
                    output_path, grouping_attributes,
                    additional_writer_kwargs):
        
        assert self.__class__ not in Writer.INSTANCES[self.CALC_GROUP], \
            'Writer already created'
        assert self.CALC_NAME, 'Writer required \'CALC_NAME\' to be set.'
        assert self.CALC_NAME_LONG, 'Writer required \'CALC_NAME_LONG\' to be set.'
        required_names = (
            'CALC_GROUP', 'CALC_CLASS', 'CALC_CLASS_LONG',
            'COLUMN_IDS', 'OUTPUT_SUB_DIR'
        )
        for name in required_names:
            assert getattr(self, name, None), \
                'Writer requires \'%s\' to be set.' % name

        Writer.INSTANCES[self.CALC_GROUP][self.__class__] = self
        self._results_collector = results_collector
        self._trade_attributes = trade_attributes
        self._additional_attributes = _additional_attributes()
        self._grouping_attributes = {}
        for attri in grouping_attributes:
             self._grouping_attributes[attri[0]] = attri[1]
        self._filepath = self._setFilepath(filepath=output_path)
        self._data_filter = self._getDataFilter()
        self._results = None
        self._text = None
        self._warnings = {}

    def write(self):
        """
        False or failure or a list of warnings on success.
        Errors should halt writing.
        """
        self._results = self._getData()
        #_getText allocates memory
        self._text = self._getText()
        #self._results.clear()
        if not self._text:
            return None # Having no data to write should fail the job

        with open(self._filepath, 'w') as fout:
            for line in self._text:
                fout.write('%s\n' % line)

        del self._text[:]
        self._text = None
        if os.path.isfile(self._filepath):
            return self._warnings
        return False

    def getFilepath(self):
        return self._filepath

    def _setFilepath(self, filepath):
        dir_path, filename = os.path.split(filepath)
        filename, ext = os.path.splitext(filename)
        return os.path.join(dir_path, filename + '.' + ext.lstrip('.'))

    def _getResultsFilters(self):
        return None
    
    def _getDataFilter(self):
        return None

    def _getData(self):
        results_cache = Writer._RESULTS[self.CALC_GROUP]
        results = results_cache.get(self.COLUMN_IDS)
        if results is not None:
            return results

        results = self._results_collector.getData()
        assert isinstance(results, dict), \
            'results must be of a dictionary, instead got %s.' % type(results)
        results_cache[self.COLUMN_IDS] = results
        return results

    def _getText(self):
        header = self._createHeader()
        rows = self._getRows(header=header)
        if not rows:
            return []

        if any(len(row) != len(header) for row in rows):
            raise Exception('Not all generated data is in the expected format')

        text = [','.join(header)]
        for row in rows:
            row = self._convertSpecialChars(row=list(row))
            text.append(','.join(row))
        #del rows[:]
        #rows = None
        return text

    def _createHeader(self):
        # header is a list of the risk factors and also the trade attributes
        # all the properties that need to be partitionable
        raise NotImplementedError

    def _getDefaultTradeHeader(self):
        additional_attributes = [attr for attr in self._additional_attributes
                                    if attr not in self._trade_attributes]    
        header = list(self._trade_attributes + additional_attributes)
        for i, attr in enumerate(header):
            if not attr.startswith('Trade.'):
                tradeSuffix = FRTBUtility.translateHeaderColumnName( \
                    attr, self.getTranslatorName())
                header[i] = 'Trade.' + tradeSuffix

        header.append('Trade.IMA Eligible')
        return header

    def PortfolioFromAttributes(self, attributes, attr_values):
        q = acm.CreateFASQLQuery(acm.FTrade, 'AND')
        regex = re.compile("[']")
        for idx, attr in enumerate(attributes):
            attName = self._grouping_attributes[attr]
            attValue = attr_values[idx]
            if(regex.search(attValue) is not None):
                print(('Warning: Invalid string value {0} for {1}'.format(attValue, attName)))
                return None
            elif 'No Trade:' not in attValue:
                q.AddAttrNode(attName, 'EQUAL', attValue);
        
        return acm.FASQLPortfolio(q)

    def _getAttrOnName(self, attr_values, attr_name):
        for idx, attr in enumerate(self._trade_attributes):
            attName = self._grouping_attributes[attr]
            if attName == attr_name:
                attrValue = attr_values[idx]
                return attrValue

        return '' 

    def _GetPortfolioAttrValues(self, portfolio):

        additional_portfolio_attributes = [attr for attr in self._additional_attributes
                                    if attr not in self._trade_attributes]

        attrMethods = [_method_from_attribute(aa)
                for aa in additional_portfolio_attributes]
        values = []
        for attrMethod in attrMethods:
            methodChain = attrMethod.split('.')
            value = portfolio
            for methodName in methodChain[1:]:
                method = getattr(value, methodName, None)
                if method is None:
                    value = None
                    break
                else:
                    value = method()
            values.append(str(value))
        return values

    def _getDefaultTradeAttributes(self, trade_attrs):
        attrs = list(trade_attrs)
        val = None
        if 'Portfolio' in self._trade_attributes:
            idx = self._trade_attributes.index('Portfolio')
            val = attrs[idx]

        port = acm.FPhysicalPortfolio[val]
        attrs.extend(self._GetPortfolioAttrValues(port))

        # Trade.IMA Eligible
        # !!!Placeholder value!!! - Fix when risk team implement this
        attrs.append('Standardised' if self.CALC_GROUP == 'SA' else 'Internal')
        return attrs

    def _getRows(self, header):
        # !!! TODO assert that all currencies are the same and that
        # all currencies match the base currency that we use in AA Integration
        raise NotImplementedError

    def _omitResult(self, result, measurement, row_id):
        if (isinstance(result, float) and math.isnan(result)) or \
            (isinstance(result, str) and ('nan' in result.lower())):
            warning_type = '%s - ignoring row due to NaN value(s)' % measurement
            if isinstance(row_id, (list, tuple)):
                row_id = ','.join(row_id)

            row = self._makeOffendingRow(row_id, str(result))
            self._warnings.setdefault(warning_type, []).append(row)
            return True

        return False

    def _makeOffendingRow(self, row_id, result):
        return 'Row = %s; Value = %s' % (row_id, result)

    def _convertSpecialChars(self, row):
        for idx in range(len(row)):
            if row[idx].find('"') == (-1):
                row[idx] = str(row[idx]).replace(',', ';').replace('\\', r'\\')

        return row

    def getTranslatorName(self):
        return 'Default'


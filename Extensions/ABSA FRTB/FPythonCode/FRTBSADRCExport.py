""" Compiled: 2020-09-18 10:41:48 """

#__src_file__ = "extensions/frtb/./etc/FRTBSADRCExport.py"
"""----------------------------------------------------------------------------
MODULE
    (c) Copyright 2017 FIS Front Arena. All rights reserved.

DESCRIPTION
----------------------------------------------------------------------------"""
import math

import acm

import FRTBExport
import FRTBBaseWriter
import FRTBCommon

# Writers
class DRCResultsCollector(FRTBBaseWriter.ResultsCollector):
    _PARTITIONED_COLUMN_IDS = (
        FRTBCommon.SA_DRC_MARKET_VALUE_COLUMN_ID,
        FRTBCommon.SA_DRC_NOTIONAL_COLUMN_ID
    )
    COLUMN_IDS = (
        FRTBCommon.SA_DRC_SCALING_COLUMN_ID,
        FRTBCommon.SA_DRC_MATURITY_COLUMN_ID,
        FRTBCommon.SA_DRC_IS_LONG_EXPOSURE_COLUMN_ID
    ) + _PARTITIONED_COLUMN_IDS

    def getOrderedDimensions(self, column_id, dimensions):
        return tuple(str(v) for v in dimensions)

    def getData(self):
        data = {}
        
        internal_issuers = FRTBCommon.getInternalIssuers()
        
        for pos_key, pos_key_dict in self._result_dictionary.iteritems():
            trade_attrs = self.getTradeAttributes(pos_key)
            ref_result = pos_key_dict.get(FRTBCommon.SA_DRC_MARKET_VALUE_COLUMN_ID)
            if not ref_result:
                ref_result = pos_key_dict.get(FRTBCommon.SA_DRC_NOTIONAL_COLUMN_ID)

            if not ref_result:
                continue
            
            if not pos_key_dict.has_key(FRTBCommon.SA_DRC_NOTIONAL_COLUMN_ID):
                continue
                
            if not pos_key_dict.has_key(FRTBCommon.SA_DRC_MARKET_VALUE_COLUMN_ID):
                continue

            for key in ref_result.iterkeys():
                notional = 0.0
                marketValue = 0.0
                if pos_key_dict.get(FRTBCommon.SA_DRC_NOTIONAL_COLUMN_ID).has_key(key):
                    notional = pos_key_dict[FRTBCommon.SA_DRC_NOTIONAL_COLUMN_ID][key]
                else:
                    continue
                
                if pos_key_dict.get(FRTBCommon.SA_DRC_MARKET_VALUE_COLUMN_ID).has_key(key):
                    marketValue = pos_key_dict[FRTBCommon.SA_DRC_MARKET_VALUE_COLUMN_ID][key]
                else:
                    continue
                    
                seniority, issuer, issuerType, creditQuality = key
                if issuer in internal_issuers:
                    continue

                data_key = (trade_attrs, (issuer, seniority, issuerType, creditQuality))
                data_by_trade = data.setdefault(data_key, {})
                data_by_trade[FRTBCommon.SA_DRC_NOTIONAL_COLUMN_ID] = notional
                data_by_trade[FRTBCommon.SA_DRC_MARKET_VALUE_COLUMN_ID] = marketValue
                for column_id, result in pos_key_dict.iteritems():
                    if column_id not in self._PARTITIONED_COLUMN_IDS:
                        if isinstance(result, dict):
                            if len(result) == 0:
                                result = None
                            elif len(result) == 1:
                                result = result[column_id]

                        data_by_trade[column_id] = result
            ref_result.clear()
            pos_key_dict.clear()
            pos_key_dict = None
        self._result_dictionary.clear()
        self._result_dictionary = None
        return data

class DRCWriter(FRTBBaseWriter.Writer):
    _ADDITIONAL_TRADE_ATTRS = (
        'Issuer', 'Seniority', 'Issuer Type', 'Credit Quality', 'Direction',  # acquired from calc
        'Securitisation', 'Include in DRC' # requires handling
    )

    # header is a list of the risk factors and also the trade attributes
    # all the properties that need to be partitionable
    def _createHeader(self):
        #Trade.Reference,Trade.Region,Trade.Area,Trade.Desk,Trade.Product Type,
        header = self._getDefaultTradeHeader()
        for name in DRCWriter._ADDITIONAL_TRADE_ATTRS:
            name = 'Trade.' + name
            if name not in header:
                header.append(name)

        header.append('Measures.JTD Scaling')
        header.append('Remaining Maturity')
        header.append('Bond Equivalent MV')
        header.append('Bond Equivalent Notional')
        return header

    def _getRows(self, header):
        rows = []
        trade_attrs_header = header[:-4]
        required = self.COLUMN_IDS[-2:]
        for trade_attrs, results in self._results.iteritems():
            if any((k not in results) for k in required):
                continue

            if all(not results[k].Number() for k in required):
                continue
                
            trade_attrs, extra_trade_attrs = trade_attrs
            trade_attrs = self._getDefaultTradeAttributes(trade_attrs=trade_attrs)
            trade_attrs.extend(
                ['' for _ in range(len(trade_attrs_header) - len(trade_attrs))]
            )
            measures = []
            for key in self.COLUMN_IDS:
                result = results[key]
                if key == FRTBCommon.SA_DRC_IS_LONG_EXPOSURE_COLUMN_ID:
                    extra_trade_attrs += ('Long' if result else 'Short',)
                elif isinstance(result, float):
                    measures.append('' if math.isnan(result) else result)
                elif result is None:
                    measures.append('')
                else:
                    measures.append(float( result ))

            known_attrs = set()
            for i, value in enumerate(extra_trade_attrs):
                attr = DRCWriter._ADDITIONAL_TRADE_ATTRS[i]
                known_attrs.add(attr)
                idx = trade_attrs_header.index('Trade.' + attr)
                trade_attrs[idx] = value

            for attr in DRCWriter._ADDITIONAL_TRADE_ATTRS:
                if attr not in known_attrs:
                    idx = trade_attrs_header.index('Trade.' + attr)
                    value = trade_attrs[idx]
                    # this are dummy values to ensure the upload works
                    # this is to be removed and instead a validation step
                    # is to be introduced to ensure fields are AA upload compliant
                    if not value:
                        if attr == 'Securitisation':
                            value = 'Non-securitised'
                        elif attr == 'Credit Quality':
                            value = 'AAA'
                        elif attr == 'Include in DRC':
                            value = 'Include'
                        else:
                            value = 'None'

                    trade_attrs[idx] = value

            rows.append(trade_attrs + list(map(str, measures)))

        return rows

# Exporter
class DRCExport(FRTBExport.Export):
    RESULTS_COLLECTOR_CLASS = DRCResultsCollector
    WRITER_CLASSES = (DRCWriter,)

    def makeColumns(self, parameters):
        columns = super(DRCExport, self).makeColumns(parameters=parameters)
        for column_name in self.RESULTS_COLLECTOR_CLASS.COLUMN_IDS:
            if column_name == FRTBCommon.SA_DRC_NOTIONAL_COLUMN_ID or \
                column_name == FRTBCommon.SA_DRC_MARKET_VALUE_COLUMN_ID:
                column_parameters = {
                    acm.FSymbol('hierarchy'): str(parameters['hierarchy'].Name()).strip()
                }
                config = self.makeDynamicColumnConfig(
                    column_id='FRTB DRC Dimensions',
                    params=column_parameters
                )
                columns.append(self.makeColumn(
                    column_id=column_name, config=config
                ))
            else:
                columns.append(self.makeColumn(column_id=column_name))

        return columns


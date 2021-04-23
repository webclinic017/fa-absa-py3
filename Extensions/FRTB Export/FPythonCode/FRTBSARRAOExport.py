""" Compiled: 2020-09-18 10:38:52 """

#__src_file__ = "extensions/frtb/./etc/FRTBSARRAOExport.py"
"""----------------------------------------------------------------------------
MODULE
    (c) Copyright 2017 FIS Front Arena. All rights reserved.

DESCRIPTION

----------------------------------------------------------------------------"""
import FRTBExport
import FRTBBaseWriter
import FRTBCommon

# Writers
class RRAOResultsCollector(FRTBBaseWriter.ResultsCollector):
    COLUMN_IDS = (
        FRTBCommon.SA_RRAO_NOTIONAL_COLUMN_ID,
        FRTBCommon.SA_RRAO_TYPE_COLUMN_ID
    )

class RRAOWriter(FRTBBaseWriter.Writer):
    def _createHeader(self):
        header = self._getDefaultTradeHeader()
        header.append('Trade.Residual Risk Type')
        header.append('Notional')
        return header

    def _getRows(self, header):
        rows = []
        for trade_attrs, results in self._results.items():
            trade_attrs = self._getDefaultTradeAttributes(trade_attrs=trade_attrs)
            notional = results[FRTBCommon.SA_RRAO_NOTIONAL_COLUMN_ID].Number()
            if self._omitResult(notional, FRTBCommon.SA_RRAO_NOTIONAL_COLUMN_ID, trade_attrs):
                continue

            risk_type = results[FRTBCommon.SA_RRAO_TYPE_COLUMN_ID] or ''
            if (notional or risk_type) and (risk_type != 'None'):
                row = trade_attrs + [risk_type, str(notional)]
                rows.append(row)

        return rows

# Exporter
class RRAOExport(FRTBExport.Export):
    RESULTS_COLLECTOR_CLASS = RRAOResultsCollector
    WRITER_CLASSES = (RRAOWriter,)

    def makeColumns(self, parameters):
        columns = super(RRAOExport, self).makeColumns(parameters=parameters)
        for column_name in self.RESULTS_COLLECTOR_CLASS.COLUMN_IDS:
            columns.append(self.makeColumn(column_id=column_name))

        return columns

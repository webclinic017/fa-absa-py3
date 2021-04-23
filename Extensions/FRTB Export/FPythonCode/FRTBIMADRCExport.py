""" Compiled: 2020-09-18 10:38:52 """

#__src_file__ = "extensions/frtb/./etc/FRTBIMADRCExport.py"
from __future__ import print_function
"""----------------------------------------------------------------------------
MODULE
    (c) Copyright 2017 FIS Front Arena. All rights reserved.

DESCRIPTION

----------------------------------------------------------------------------"""
import acm

import FRTBExport
import FRTBBaseWriter
import FRTBCommon
import FRTBUtility
import re

from FRTBIMAStaticData import getLGD

# Writers
class DRCResultsCollector(FRTBBaseWriter.ResultsCollector):
    COLUMN_IDS = (FRTBCommon.IMA_DRC_CURRENT_VALUE_COLUMN_ID,
    FRTBCommon.IMA_DRC_VALUE_DEFAULT_COLUMN_ID, FRTBCommon.IS_OPTION_COLUMN_ID,
        FRTBCommon.SA_DRC_MATURITY_COLUMN_ID, FRTBCommon.IMA_DRC_LIQUIDITY_HORIZON)
    
    def addResult(self, posInfoID, columnID, calculationInfos):
        if not calculationInfos:
            return
        try:
            pos_key = self._position_key_table[posInfoID]
            results = self._getResultDict(pos_key, columnID)
            for calc_info in calculationInfos:
                if calc_info.values is None:
                    continue
                #print(calc_info)
                result_key = self._getResultKey(columnID, calc_info)
                results.setdefault(result_key, []).append(calc_info)
                    
        except Exception as e:
            import traceback
            traceback.print_exc()

        return
    
    def _getResultKey(self, column_id, calc_info):
        return column_id

class DRCWriter(FRTBBaseWriter.Writer):
    COLUMN_IDS = (FRTBCommon.IMA_DRC_CURRENT_VALUE_COLUMN_ID, FRTBCommon.IMA_DRC_VALUE_DEFAULT_COLUMN_ID,
    FRTBCommon.IS_OPTION_COLUMN_ID, FRTBCommon.SA_DRC_MATURITY_COLUMN_ID, FRTBCommon.IMA_DRC_LIQUIDITY_HORIZON)
    OUTPUT_SUB_DIR = 'drc'
    _ADDITIONAL_TRADE_ATTRS = (#'Currency',
        'IMA Eligible', 'Calculate IMA', 'Is Option', 'Include in DRC', 'Securitisation',
        'Seniority', 'Issuer', 'Issuer Type', 'Credit Quality', 'Maturity', 'DRC Liquidity Horizon',
        'Include in RRAO', 'Residual Risk Type', 'Current Value', 'Obligor Details',
        'Value After Default')

    '''
    Reference,Currency,Counterparty,Netting Set,Product Class,Region,Area,Desk,Portfolio,
    IMA Eligible,Calculate IMA,Is Option,Include in DRC,Securitisation,
    Seniority,Issuer,Credit Quality,Issuer Type,Include in RRAO,
    Residual Risk Type,Current Value,Obligor Details,Value After Default
    '''
    def _createHeader(self):
        #Trade.Reference,Trade.Region,Trade.Area,Trade.Desk,Trade.Product Type,
        additional_trade_attributes = [attr for attr in self._additional_trade_attributes
                                    if attr not in self._trade_attributes]    
        header = list(self._trade_attributes + additional_trade_attributes)
        for name in DRCWriter._ADDITIONAL_TRADE_ATTRS:
            if name not in header:
                header.append(name)
    
        retVal =[]
        translator = self.getTranslatorName()
        for headerItem in header:
            if headerItem.startswith('Trade.'):
                headerItem = headerItem.split('.')[1]
            retVal.append(FRTBUtility.translateHeaderColumnName(headerItem, translator))

        return retVal

    '''
    The issuer fields are contained in projection coordinates as follows
    seniority =  calculationInfo.projectionCoordinates[0]
    issuer = calculationInfo.projectionCoordinates[1]
    issuerType = calculationInfo.projectionCoordinates[2]
    creditQuality = calculationInfo.projectionCoordinates[3]
    lossGivenDefault = calculationInfo.projectionCoordinates[4]
    '''
    def _getRows(self, header):
        rows = []
        for tradeAttrs, measurements in self._results.iteritems():
            currentValue = measurements[self.CALC_NAME][0].values.Number()
            if FRTBCommon.IMA_DRC_VALUE_DEFAULT_COLUMN_ID in measurements:
                data = measurements[FRTBCommon.IMA_DRC_VALUE_DEFAULT_COLUMN_ID][0].projectionCoordinates
                attrs = []
                attrs.append(str(data[0])) #seniority
                if 'Issuer' not in self._trade_attributes:
                    attrs.append(str(data[1])) #issuer
                attrs.append(str(data[2])) #issuerType
                attrs.append(str(data[3])) #creditQuality
                
                maturity = self._getMaturity(measurements)
                liquidityHorizon = str(0) if not bool(measurements[FRTBCommon.IMA_DRC_LIQUIDITY_HORIZON]) else \
                            measurements[FRTBCommon.IMA_DRC_LIQUIDITY_HORIZON][0].values
                attrs.append(maturity)
                attrs.append(liquidityHorizon)
                
                Value_After_Default = self._buildValueAfterDefault(measurements)
                isOption = measurements[FRTBCommon.IS_OPTION_COLUMN_ID][0].values
                isOption = 'Yes' if isOption else 'No'
                tradeAttrs = self._getDefaultTradeAttributes(trade_attrs=tradeAttrs)
                tradeAttrs = list(tradeAttrs)
                row = tradeAttrs + \
                    ['Yes', isOption, 'Include', 'Non-securitised'] + attrs + \
                    ['Exclude', ''] + [str(currentValue)]
                row = [s.replace(',', '') for s in row]
                row += self.getObligorFields(str(data[1]))
                row += Value_After_Default
                rows.append(row)
        
        return rows

    def _getMaturity(self, measurements):
        if not bool(measurements[FRTBCommon.SA_DRC_MATURITY_COLUMN_ID]): 
            return '0'
        maturity = measurements[FRTBCommon.SA_DRC_MATURITY_COLUMN_ID][0].values
        maturity = str(maturity)
        if maturity == 'nan':
            maturity = ''
        
        return maturity

    def _buildValueAfterDefault(self, measurements):
        Value_After_Default = []
        i=0
        while i < 2:
            result = measurements[FRTBCommon.IMA_DRC_VALUE_DEFAULT_COLUMN_ID][i]
            LGD = result.projectionCoordinates[4]
            VGD = result.values.Number()
            if i == 0:
                s = '"(' 
            else:
                s = '('
            s += str(LGD) +', ' + str(VGD)
            if i == 1:
                s += ')"'
            else:
                s += ')'
            Value_After_Default.append(s)
            i += 1
        return Value_After_Default
    
    def _getText(self):
        header = self._createHeader()
        rows = self._getRows(header=header)
        if not rows:
            return []
        
        text = [','.join(header)]
        for row in rows:
            row = self._convertSpecialChars(row=list(row))
            text.append(','.join(row))

        return text
    
    def getObligorFields(self, issuer):
        issuer = issuer.replace(',', '')
        return ['"[' + issuer +',' + issuer + ', 1]"']
        
    def _convertSpecialChars(self, row):
        return row

# Exporters
class DRCExport(FRTBExport.Export):
    RESULTS_COLLECTOR_CLASS = DRCResultsCollector
    WRITER_CLASSES = (DRCWriter,)
    REQUIRES_IS_OPTION = True

    def getAelVariables(self):
        self._ael_vars.append(
            super(DRCExport, self).getPerformCalculationAelVariable(
                tab_suffix=self.CALC_NAME_LONG
            )
        )
        return self._ael_vars

    def makeColumns(self, parameters):
        columns = super(DRCExport, self).makeColumns(parameters=parameters)
        columns.append(
            self.makeColumn(
                column_id=FRTBCommon.IMA_DRC_CURRENT_VALUE_COLUMN_ID,
                column_name=self.CALC_NAME
                            )
                       )
        column_parameters = {}
        extensionContext = acm.ExtensionTools().GetDefaultContext()
        config = acm.Risk.CreateDynamicVectorConfiguration(
            extensionContext.Name(),
            'FRTB IMA DRC Dimensions',
            column_parameters
        )
        columns.append(self.makeColumn(
            FRTBCommon.IMA_DRC_VALUE_DEFAULT_COLUMN_ID, config=config
        ))
        columns.append(self.makeColumn(
            FRTBCommon.SA_DRC_MATURITY_COLUMN_ID
        ))
        columns.append(self.makeColumn(
            FRTBCommon.IMA_DRC_LIQUIDITY_HORIZON
        ))

        return columns

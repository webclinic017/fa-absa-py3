""" Compiled: 2020-08-14 16:40:05 """

#__src_file__ = "extensions/arc_writers/./etc/MarketDataWriter.py"

import os, os.path
import sys
import inspect
import FRiskCubeWriterBase
import acm
from ArenaFunctionBridge import instrument_used_price
import math
import functools
import ael
import hashlib
import FMarketRiskExportUtil
import FBDPCommon
import ast


DEFAULT_EXPORT_SUFFIX='csv'
FILE_SUFFIXES = ('.dat', '.txt', '.csv')
today = acm.Time().DateNow()
mappedValuationParameter = acm.GetFunction('mappedValuationParameters', 0)
accountingCurr = mappedValuationParameter().Parameter().AccountingCurrency()
columnName = 'Standard Calculations Suggested Mark-to-Market Price'
calcSpace = acm.FCalculationSpace('FDealSheet')

class MarketDataWriter(object):

    def __init__(self, logger, insts, yieldCurves, volatilities, exportBenchmarkPrice, timebucket):
        self.insts = insts
        self.IRRateCurves = yieldCurves
        self.volatilities = volatilities
        self.exportBenchmarkPrice = exportBenchmarkPrice
        self.timebuckets= FMarketRiskExportUtil.TimebucketInPeriod(timebucket, logger)
        self.riskfactorExportMaps = FBDPCommon.valueFromFParameter('FArtiQMarketExportParameters', 'RiskFactorExportNames')
        self.riskfactorExportMaps = ast.literal_eval(self.riskfactorExportMaps)
        self._logger = logger

    def _getNewFileName(self, filename, overwrite):
        dirname = os.path.dirname(filename)
        filebasename = os.path.basename(filename)
        
        if filebasename.endswith(FILE_SUFFIXES):
            filebasename, suffix = filebasename.rsplit('.', 1)
        else:
            suffix =  DEFAULT_EXPORT_SUFFIX

        filepath = os.path.join(dirname, '{0}.{1}'.format(filebasename, suffix))
        if not os.path.exists(filepath) or overwrite:
            return filepath

        for i in range(1, MAX_FILES_IN_DIR + 1):
            f = os.path.join(dirname, '{0}{1}.{2}'.format(filebasename, i, suffix))

            if not os.path.exists(f):
                return f
        raise Exception("Maximum no. of {0} files found in {1}. Please clear "
                "out directory or allow overwrites.".format(filename, dirname))

    
    def _getYieldCurvePoints(self, yc):
        points = []
        curveInfo = yc.IrCurveInformation()
        startDate = ael.date_today()
        yc_tb = self.timebuckets if self.timebuckets else \
                FMarketRiskExportUtil.GetYcTimeBucket(yc.Name(), self._logger)
        self._logger.logInfo("Based on Timebuckets {0}.".format(yc_tb))
        for b in yc_tb:
            names = b.split('-')
            tb = b
            if len(names) > 1:
                tb = names[1]
            if tb.lower() == 'rest':
                continue
            endDate = ael.date_today().add_period(tb)
            rate = curveInfo.Rate(startDate, endDate, "Continuous", "Act/365", 'Spot Rate')
            pointStr = b + "::::" + '{0:.4f}'.format(rate)
            points.append(pointStr)
            startDate = endDate

        return ";".join(points)

    def _getInstrumentSpreadPrice(self, yc):
        spreads = yc.InstrumentSpreads()
        insts = [s.Instrument() for s in spreads]
        outputData=[]
        calcSpaceColl = acm.Calculations().CreateStandardCalculationsSpaceCollection()
        for inst in insts:
            price = inst.Calculation().MarketPrice(calcSpaceColl).Value()
            if not math.isnan(price.Number()):
                dateStr, period = FMarketRiskExportUtil.ParseDateStrToPeriod(inst.ExpiryDateOnly(), self._logger)
                if period.find('-') != -1:
                    continue
                outputData.append((period, inst.Name(), price.Number()))
        
        cmp = functools.cmp_to_key(lambda a, b: FMarketRiskExportUtil.Compare(a[0], b[0]))
        outputData.sort(key=cmp)
        return";".join(['{0}-{1}::::{2:.4f}'.format(d[1], d[0], d[2]) for d in outputData])

    def _getBenchmarkPrice(self, yc):
        points = [p for p in yc.Points()]
        if yc.Type() == "Composite":
            for p in yc.YieldCurveLinks():
                conCurv = p.ConstituentCurve()
                points.extend(conCurv.Points())

        sortedPoints = sorted(points, key=lambda p: p.ActualDate())
        outputData=[]
        for p in sortedPoints:
            inst = p.Instrument()
            mtmPrice = self._getInstrumentPrice(inst, p.ActualDate()) 
            dateStr, period = FMarketRiskExportUtil.ParseDateStrToPeriod(p.Name(), self._logger)
            pointStr = period
            if yc.Type() == 'Inflation':
                pointStr = '{0}-{1}'.format(inst.Name(), period)
            pointStr = pointStr + "::::" + '{0:.4f}'.format(mtmPrice)
            outputData.append(pointStr)
        
        return ";".join(outputData)

    def _getInstrumentPrice(self, inst, date):
        curr = inst.Currency()
        mtmPrice = inst.MtMPrice(date, curr)
        if mtmPrice == 0.0 or math.isinf(mtmPrice) or math.isnan(mtmPrice):
            clone = inst.StorageImage()
            clone.Currency(curr)
            calc = calcSpace.CreateCalculation(clone, columnName)
            mtmPrice = calc.Value().Number()
        return mtmPrice

    def _getVolatilityData(self, vol):
        points = []
        for p in vol.Points():
            tenorP = '' 
            expiryP = ''
            if p.IsGenericExpiry():
                tenorP = str(p.UnderlyingMaturityPeriod())
            if p.IsGenericUnderlyingMaturity():
                expiryP = str(p.ExpiryPeriod())
            if tenorP or expiryP:
                pointStr = tenorP + ':' + expiryP + ':::' + '{0:.4f}'.format(p.Volatility())
                if pointStr not in points:
                    points.append(pointStr)

        return ";".join(points)
    
    def _getInstFactorType(self, inst):
        instType = inst.InsType()
        if instType not in ['Curr', 'Stock', 'Commodity']:
            self._logger.logWarning( "Unsupported inst type {0} for instrument {1}.".format(instType, instName))
            return None
 
        factorName = None
        if instType == 'Curr':
            factorName = 'FxRate'
        elif instType == 'Stock':
            factorName = 'EquityPrice'
        elif instType == 'Commodity':
            factorName = 'CommodityPrice'
        
        fTypeExportName = self.riskfactorExportMaps.get(factorName, factorName)
        return fTypeExportName
    
    def _getInstPrice(self, inst):
        instType = inst.InsType()
        spotPrice = 0.0
        if instType == 'Curr':
            spotPrice = instrument_used_price(inst.Name(), today, accountingCurr.Name())
        else:
            spotPrice = instrument_used_price(inst.Name(), today, inst.Currency().Name())
        return '{0:.4f}'.format(spotPrice)
    
    def _writeDataHeader(self, fp):
        header = ",".join(["P&L Source", "Factor.Type", "Factor.ID", "Factor.Sub ID", "_P&L Rate_"])
        line = FRiskCubeWriterBase.BaseWriter._encodeData(header)
        print(line, file=fp)

    def _writeDataRows(self, fp):
        for yc in self.IRRateCurves:
            ycType = yc.Type().replace(" ", "")
            if ycType == "InstrumentSpread":
                dataStr = self._getInstrumentSpreadPrice(yc)
            elif self.exportBenchmarkPrice:
                ycType="Benchmark"
                dataStr = self._getBenchmarkPrice(yc)
            else:
                dataStr = self._getYieldCurvePoints(yc)
            
            fTypeExportName = self.riskfactorExportMaps.get(ycType, ycType)
            line = ",".join(["Sensitivity Based", fTypeExportName, yc.Name(), "Whole", dataStr])
            line = FRiskCubeWriterBase.BaseWriter._encodeData(line)
            print(line, file=fp)

        volFactorType = self.riskfactorExportMaps.get("Volatility", "Volatility")
        for vol in self.volatilities:
            dataStr = self._getVolatilityData(vol)
            if dataStr:
                line = ",".join(["Sensitivity Based", volFactorType, vol.Name(), "Whole", dataStr])
                line = FRiskCubeWriterBase.BaseWriter._encodeData(line)
                print(line, file=fp)
        
        for inst in self.insts:
            instFactorType = self._getInstFactorType(inst)
            if not instFactorType:
                continue 

            dataStr = self._getInstPrice(inst)
            factorID = inst.Name()
            if inst.InsType() == 'Curr':
                factorID = inst.Name() + '/' + accountingCurr.Name()
            line = ",".join(["Sensitivity Based", instFactorType, factorID, "Whole", dataStr])
            line = FRiskCubeWriterBase.BaseWriter._encodeData(line)
            print(line, file=fp)


    def write(self, overwrite, filepath=r'C:\Temp\RiskExport\Export.txt'):
        """
        Writes the output in Risk Cube format in several parts - report header,
        data header, data rows.
        """
        FRiskCubeWriterBase.BaseWriter._initDirs(filepath)
        filename = self._getNewFileName(filepath, overwrite)
        id_ = int(hashlib.md5(filename.encode("utf-8")).hexdigest(), 16)
        try:
            
            with open(filename, 'w') as fp:
                self._writeDataHeader(fp)
                self._writeDataRows(fp)
            self._logger.logInfo("{0} successfully exports into file {1}".format(self.__class__.__name__, filename))
            self._logger.summaryAddOk("File", id_, "Export")
        except Exception as err:
            tb = inspect.getframeinfo(inspect.trace()[-1][0])
            self._logger.logInfo("{2}.{3}() line {4}: {0} - {1}.".format(type(err).__name__,
                    err, tb.filename, tb.function, tb.lineno))
            self._logger.logError("{0} failed to export to file {1}".format(self.__class__.__name__, filename))

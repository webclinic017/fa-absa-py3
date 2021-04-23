from __future__ import print_function
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
import re

DEFAULT_EXPORT_SUFFIX='csv'
FILE_SUFFIXES = ('.dat', '.txt', '.csv')
today = acm.Time().DateNow()
todayStr = today.replace('-', '') #format YYYYMMDD
defaultCalendar = 'ZAR Johannesburg'
yesterday = acm.Time.DateAdjustPeriod(today, '-1d', defaultCalendar, 'Preceding') #this looks up previous business day on ZAR Johannesburg calendar
tomorrow = acm.Time.DateAdjustPeriod(today, '1d', defaultCalendar, 'Following') #this looks up following business day on ZAR Johannesburg calendar
tomorrowStr = tomorrow.replace('-', '') #format YYYYMMDD
mappedValuationParameter = acm.GetFunction('mappedValuationParameters', 0)
accountingCurr = mappedValuationParameter().Parameter().FxBaseCurrency()
ZARaccountingCurr = mappedValuationParameter().Parameter().AccountingCurrency()
directCCYList = ('GBP', 'EUR', 'AUD')
#columnName = 'Standard Calculations Suggested Mark-to-Market Price'
columnName = 'Suggested Mark-to-Market Price'
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
                

    def filterOutShortEndPeriods(self, periods):
        dateDiff = acm.Time.DateDifference(tomorrow, today)
        newPeriodList = []
        for period in periods:
            if not 'd' in period:
                newPeriodList.append(period)
            elif 'd' in period:
                parsedPeriod = period.replace('d', '')
                if float(parsedPeriod) > dateDiff:
                    newPeriodList.append(period)
        return newPeriodList

				
    def _getYieldCurvePoints(self, yc, PxAdjusted, base):
        points = []
        curveInfo = yc.IrCurveInformation()
        startDate = ael.date_today()
        self._logger.logInfo("_getYieldCurvePoints for {0}.".format(yc.Name()))
        if self.timebuckets:
            yc_tb = self.timebuckets 
            self._logger.logInfo("Based on Timebuckets {0}.".format(yc_tb))
            for b in yc_tb:
                if b == 'rest' or '-' in b:
                    continue
                endDate = ael.date_today().add_period(b)
                if PxAdjusted == 'True': 
                    rate = curveInfo.Rate(startDate, endDate, "Continuous", "Act/365", 'Spot Rate') * 10000
                if PxAdjusted == 'False': 
                    rate = curveInfo.Rate(startDate, endDate, "Continuous", "Act/365", 'Spot Rate') * 100
                pointStr = b + "::::" + str(rate)
                points.append(pointStr)
                startDate = endDate
        else:
            if len(yc.Points()) == 0:
                self._logger.logInfo("Yield Curve : {0} has no points on the curve.".format(yc.Name()))
            else:
                yc_tb = FMarketRiskExportUtil.GetYcTimeBucket(yc.Name(), self._logger)
                if base:
                    yc_tb = FMarketRiskExportUtil.GetYcTimeBucket(yc.Name(), self._logger)
                self._logger.logInfo("Based on Timebuckets {0}.".format(yc_tb))
                compound = yc.StorageCompoundingType()
                dayCount = yc.StorageDayCount()
                calcType = yc.StorageCalcType()
                for b in yc_tb:
                    if b == 'rest' or '-' in b:
                        continue
                    endDate = acm.Time.DateAdjustPeriod(today, b, defaultCalendar, 'Following')
                    self._logger.logInfo("Start date is {0} and End date is {1}.".format(today, endDate))
                    if PxAdjusted == 'True': 
                        rate = curveInfo.Rate(today, endDate, compound, dayCount, calcType) * 10000
                    if PxAdjusted == 'False': 
                        rate = curveInfo.Rate(today, endDate, compound, dayCount, calcType) * 100
                    pointStr = b + "::::" + str(rate)
                    points.append(pointStr)
                    startDate = endDate

        return ";".join(points)
			
    def combine_lists(self, list_1, list_2, list_3):
        output = {}
        for name_1, dataStr_1 in list_1:
            output[name_1] = [name_1, dataStr_1, None, None]
        if list_2:
            for name_2, dataStr_2 in list_2:
                if name_2 in output:
                    output[name_2][2] = dataStr_2    
        if list_3:
            for name_3, dataStr_3 in list_3:
                if name_3 in output:
                    output[name_3][3] = dataStr_3
        return output
           
    def _getInstrumentSpreadPrice(self, yc, PxAdjusted, base):
        spreads = yc.InstrumentSpreads()
        ins_dic = {}
        #insts = [s.Instrument() for s in spreads]
        for s in spreads:
            ins_dic[s.Instrument()]= [s.Spread(), s.Benchmark()]
        outputData=[]
        calcSpaceColl = acm.Calculations().CreateStandardCalculationsSpaceCollection()
        for inst in ins_dic:
            if not inst.IsExpired():
                exportName = inst.Name()
                expiryDate = inst.ExpiryDateOnly()
                underlying = inst.ValuationUnderlying()
                if underlying:
                    exportName = underlying.Name()
                    expiryDate = underlying.ExpiryDateOnly()
                price = 0.00
                spread = ins_dic[inst][0] * 100
                undBenchmarkIns = ins_dic[inst][1]
                if undBenchmarkIns:
                    price = undBenchmarkIns.Calculation().MarketPrice(calcSpaceColl).Value()
                if not inst.ExpiryDateOnly():
                    dateStr, period = FMarketRiskExportUtil.ParseDateStrToPeriod(tomorrow, self._logger)
                if inst.ExpiryDateOnly():
                    timeToMaturity = FMarketRiskExportUtil.DateDiffToPeriod(FBDPCommon.toDate(expiryDate), acm.Time.DateToday()) 
                    if 'd' in timeToMaturity:
                        if float(timeToMaturity.replace('d', '')) < 7: # 7days
                            adj_period = FMarketRiskExportUtil.DateDiffToPeriod(FBDPCommon.toDate(expiryDate), tomorrow) 
                            dateStr, period = expiryDate, adj_period
                        else: 
                            if base == 'True':
                                adj_period = FMarketRiskExportUtil.DateDiffToPeriod(FBDPCommon.toDate(expiryDate), tomorrow) 
                                dateStr, period = expiryDate, adj_period
                            elif base == 'False':
                                dateStr, period = FMarketRiskExportUtil.ParseDateStrToPeriod(expiryDate, self._logger)
                            
                    else:
                        if base == 'True':
                            adj_period = FMarketRiskExportUtil.DateDiffToPeriod(FBDPCommon.toDate(expiryDate), tomorrow) 
                            dateStr, period = expiryDate, adj_period
                        elif base == 'False':
                            dateStr, period = FMarketRiskExportUtil.ParseDateStrToPeriod(expiryDate, self._logger)
                if period.find('-') != -1:
                    continue
                if price == 0.00:
                    if PxAdjusted == 'True':
                        dataStr = "{0}::::{1:.4f}".format(period, (spread*100))
                        outputData.append((exportName, dataStr))
                    if PxAdjusted == 'False':
                        dataStr = "{0}::::{1:.4f}".format(period, spread)
                        outputData.append((exportName, dataStr))
                elif not math.isnan(price.Number()):
                    if PxAdjusted == 'True':
                        dataStr = "{0}::::{1:.4f}".format(period, ((price.Number() + spread)*100))
                        outputData.append((exportName, dataStr))
                    if PxAdjusted == 'False':
                        dataStr = "{0}::::{1:.4f}".format(period, (price.Number() + spread))
                        outputData.append((exportName, dataStr))
                else:
                    if PxAdjusted == 'True':
                        if spread == 0.0:
                            dataStr = "{0}::::{1:.4f}".format(period, 0.0000)
                            outputData.append((exportName, dataStr))
                        else:
                            dataStr = "{0}::::{1:.4f}".format(period, ((0.0000 + spread)*100))
                            outputData.append((exportName, dataStr))
                    if PxAdjusted == 'False':
                        if spread == 0.0:
                            dataStr = "{0}::::{1:.4f}".format(period, 0.0000)
                            outputData.append((exportName, dataStr))
                        else:
                            dataStr = "{0}::::{1:.4f}".format(period, (0.0000 + spread))
                            outputData.append((exportName, dataStr))
        return outputData

		
    def getBenchmarkInsFromPeriod(self, yc, instrument, period):
        self._logger.logInfo("checking this curve: {0}".format(yc.Name()))
        benchmark = None
        if instrument:
            return instrument
        else:
            for ins in yc.BenchmarkInstruments():
                if str(ins.ExpiryPeriod()) == str(period):
                    benchmark = ins
            if benchmark:
                return benchmark
            else:
                return None
            
    def ParseBenchmarkDateStrToPeriod(self, inputStr, base):
        explictPeriod = re.findall(FMarketRiskExportUtil._PERIOD_MATCHER, inputStr)
        if len(explictPeriod) > 0:
            dateStr= explictPeriod[0].strip()
            period = dateStr.replace(' ', "").lower()
            return dateStr, period
        explictDate = re.findall(FMarketRiskExportUtil._ISO_DATE_MATCHER, inputStr)
        if len(explictDate) > 0:
            dateStr = "-".join(explictDate[0]).strip()
            if base:
                period = FMarketRiskExportUtil.DateDiffToPeriod(FBDPCommon.toDate(dateStr), tomorrow)
            else:
                period = FMarketRiskExportUtil.DateDiffToPeriod(FBDPCommon.toDate(dateStr), today)
            return dateStr, period
        if inputStr.lower() =='rest':
            return "rest", "rest"
        self._logger.logError('unexpected string {0} for date or period.'.format(inputStr))
        return "", ""
                            
    def _getBenchmarkPrice(self, yc, PxAdjusted, base):
        points = [p for p in yc.Points()]
        if yc.Type() == "Composite":
            for p in yc.YieldCurveLinks():
                conCurv = p.ConstituentCurve()
                points.extend(conCurv.Points())
        sortedPoints = sorted(points, key=lambda p: p.ActualDate())
        outputData=[]
        for p in sortedPoints:
            inst = self.getBenchmarkInsFromPeriod(yc, p.Instrument(), p.Name())
            if not inst:
                self._logger.logWarning("There is no instrument in yield curve points")
            else:
                curr = inst.Currency()
                if PxAdjusted == 'False': 
                    if yc.Type() == 'Inflation':
                        mtmPrice = inst.MtMPrice(today, curr)
                        if str(mtmPrice) == 'nan':
                            mtmPrice == '0.0'
                    if yc.Type()!= 'Inflation':
                        mtmPrice = inst.MtMPrice(p.ActualDate(), curr)
                if PxAdjusted == 'True': 
                    if yc.Type() == 'Inflation':
                        mtmPrice = inst.MtMPrice(today, curr) * 100
                        if str(mtmPrice) == 'nan':
                            mtmPrice = '0.0'
                    if yc.Type() != 'Inflation':
                        mtmPrice = inst.MtMPrice(p.ActualDate(), curr) * 100
                if mtmPrice == 0.0 or math.isinf(mtmPrice) or math.isnan(mtmPrice):
                    clone = inst.StorageImage()
                    clone.Currency(curr)
                    calc = calcSpace.CreateCalculation(clone, columnName)
                    if PxAdjusted == 'False':
                        if calc.Value():
                            mtmPrice = calc.Value().Number()
                            if  str(mtmPrice) == 'nan':
                                mtmPrice = '0.0'
                    if PxAdjusted == 'True': 
                        if calc.Value():
                            mtmPrice = calc.Value().Number() * 100
                            if  str(mtmPrice) == 'nan':
                                mtmPrice = '0.0'
                dateStr, period = self.ParseBenchmarkDateStrToPeriod(p.Name(), base)
                pointStr = period + "::::" + str(mtmPrice)
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
    
    def _getInstPrice(self, inst, dateT1, PxAdjusted):
        instType = inst.InsType()
        spotPrice = 0.0
        dateT2 = acm.Time.DateAdjustPeriod(dateT1, '-1d', defaultCalendar, 'Preceding')
        if instType == 'Curr':
            if inst.Name() in directCCYList:
                self._logger.logInfo( "This a direct quoted currency: {0}.".format(inst.Name()))
		if PxAdjusted == 'False':
                    spotPrice = instrument_used_price(inst.Name(), dateT1, accountingCurr.Name())
                elif PxAdjusted == 'True':
                    spotPrice_today = instrument_used_price(inst.Name(), dateT1, accountingCurr.Name())
                    spotPrice_yesterday = instrument_used_price(inst.Name(), dateT2, accountingCurr.Name())
                    spotPrice_shift = ( spotPrice_today / spotPrice_yesterday ) * 100
                    spotPrice = spotPrice_shift
            else:
                self._logger.logInfo( "This not a direct quoted currency: {0}.".format(inst.Name()))
                if PxAdjusted == 'False':
                    spotPrice = instrument_used_price(accountingCurr.Name(), dateT1, inst.Name())
                elif PxAdjusted == 'True':
                    spotPrice_today = instrument_used_price(accountingCurr.Name(), dateT1, inst.Name())
                    spotPrice_yesterday = instrument_used_price(accountingCurr.Name(), dateT2, inst.Name())
                    spotPrice_shift = ( spotPrice_today / spotPrice_yesterday ) * 100
                    spotPrice = spotPrice_shift
        else:
            spotPrice = instrument_used_price(inst.Name(), dateT1, inst.Currency().Name())
			
        if str(spotPrice) == 'nan':
            return '{0:.4f}'.format(0.0)
        else: 
            return '{0:.4f}'.format(spotPrice)
    
    def _getRelativeShift(self, todayPx, yesterdayPx):
        if (float(todayPx) in (0.0, 'nan')) or (float(yesterdayPx) in (0.0, 'nan')):
            return '{0:.4f}'.format(0.0)
        else:
            return ((float(todayPx) / float(yesterdayPx)) - 1)
    
    def _writeDataHeader(self, fp):
        header = ",".join(["P&L Source", "Factor.Type", "Factor.ID", "Factor.Sub ID", "_P&L Rate_", "_Market Data_", "_Scaled Market Data_", "_Relative Shift_"])
        line = FRiskCubeWriterBase.BaseWriter._encodeData(header)
        print(line, file=fp)

    def _writeBaseDataHeader(self, fp):
        header = ",".join(["P&L Source", "Factor.Type", "Factor.ID", "Factor.Sub ID", "_Base P&L Rate_", "_Base Market Data_", "_Scaled Base Market Data_"])
        line = FRiskCubeWriterBase.BaseWriter._encodeData(header)
        print(line, file=fp)

    def _writeDataRows(self, fp, base, shiftType):
        for yc in self.IRRateCurves:
            ycType = yc.Type().replace(" ", "")               
            if ycType == "InstrumentSpread":
                if base == 'Base':
                    dataStr = self._getInstrumentSpreadPrice(yc, 'True', 'True')
                    rawPxStr = self._getInstrumentSpreadPrice(yc, 'False', 'True')
                elif base != 'Base':
                    dataStr = self._getInstrumentSpreadPrice(yc, 'True', 'False')
                    rawPxStr = self._getInstrumentSpreadPrice(yc, 'False', 'False')
            elif self.exportBenchmarkPrice:
                dataStr = self._getBenchmarkPrice(yc, 'True', False)
		rawPxStr = self._getBenchmarkPrice(yc, 'False', False)
		if base == 'Base':
                    dataStr = self._getBenchmarkPrice(yc, 'True', True)
                    rawPxStr = self._getBenchmarkPrice(yc, 'False', True)
                if ycType in ('Spread', 'Benchmark'):
                    ycType="Benchmark"
            else:
                ycType="InterestRate"
                dataStr = self._getYieldCurvePoints(yc, 'True', False)
                rawPxStr = self._getYieldCurvePoints(yc, 'False', False)
                if base == 'Base':
                    dataStr = self._getYieldCurvePoints(yc, 'True', True)
                    self._logger.logInfo("BasedataStr: {0} successfully exports into file".format(dataStr))
                    rawPxStr = self._getYieldCurvePoints(yc, 'False', True)
                    self._logger.logInfo("BaserawPxStr: {0} successfully exports into file".format(rawPxStr))
            if dataStr:    
                if shiftType == 'relative':
                    fTypeExportName = self.riskfactorExportMaps.get(ycType, ycType)
                    if ((type(dataStr) is str) and (type(rawPxStr) is str)):
                        line = ",".join(["Sensitivity Based", fTypeExportName, yc.Name(), "Whole", dataStr, rawPxStr, dataStr, '' ])
                        line = FRiskCubeWriterBase.BaseWriter._encodeData(line)
                        print(line, file=fp)
                    elif ((type(dataStr) is list) and (type(rawPxStr) is list)):
                        combinedData = self.combine_lists(dataStr, rawPxStr, dataStr)
                        for dataPoint in combinedData:
                            line = ",".join(["Sensitivity Based", fTypeExportName, '{0}-{1}'.format(yc.Name(), combinedData[dataPoint][0]), "Whole", combinedData[dataPoint][1], combinedData[dataPoint][2], combinedData[dataPoint][3], '' ])
                            line = FRiskCubeWriterBase.BaseWriter._encodeData(line)
                            print(line, file=fp)
                    
                if shiftType != 'relative':
                    fTypeExportName = self.riskfactorExportMaps.get(ycType, ycType)
                    if ((type(dataStr) is str) and (type(rawPxStr) is str)):
                        line = ",".join(["Sensitivity Based", fTypeExportName, yc.Name(), "Whole", dataStr, rawPxStr, dataStr])
                        line = FRiskCubeWriterBase.BaseWriter._encodeData(line)
                        print(line, file=fp)
                    elif ((type(dataStr) is list) and (type(rawPxStr) is list)):
                        combinedData = self.combine_lists(dataStr, rawPxStr, dataStr)
                        for dataPoint in combinedData:
                            line = ",".join(["Sensitivity Based", fTypeExportName, '{0}-{1}'.format(yc.Name(), combinedData[dataPoint][0]), "Whole", combinedData[dataPoint][1], combinedData[dataPoint][2], combinedData[dataPoint][3]])
                            line = FRiskCubeWriterBase.BaseWriter._encodeData(line)
                            print(line, file=fp)
        volFactorType = self.riskfactorExportMaps.get("Volatility", "Volatility")
        for vol in self.volatilities:
            dataStr = self._getVolatilityData(vol)
            if dataStr:
                if shiftType == 'relative':
                    line = ",".join(["Sensitivity Based", volFactorType, vol.Name(), "Whole", dataStr, '', '', ''])
                    line = FRiskCubeWriterBase.BaseWriter._encodeData(line)
                    print(line, file=fp)
                if shiftType != 'relative':
                    line = ",".join(["Sensitivity Based", volFactorType, vol.Name(), "Whole", dataStr, '', ''])
                    line = FRiskCubeWriterBase.BaseWriter._encodeData(line)
                    print(line, file=fp)
        
        for inst in self.insts:
            instFactorType = self._getInstFactorType(inst)
            if not instFactorType:
                continue 
            dataStr = self._getInstPrice(inst, today, 'True')
            rawPxStr = self._getInstPrice(inst, today, 'False')
            yesterdayRawPx = self._getInstPrice(inst, yesterday, 'False')
            scaledRawPx = str(float(rawPxStr) * 100)
            relativeShift = str(self._getRelativeShift(rawPxStr, yesterdayRawPx))
            if inst.InsType() == 'Curr':
                if base == 'Base':
                    dataStr = "100.0"
                else:
                    dataStr = self._getInstPrice(inst, today, 'True')
            factorID = inst.Name()
            if inst.InsType() == 'Curr':
                if inst.Name() in directCCYList:
                    factorID = inst.Name() + '/' + accountingCurr.Name()
                elif inst.Name() == accountingCurr.Name():
                    factorID = inst.Name() + '/' + ZARaccountingCurr.Name()
                else:
                    factorID = accountingCurr.Name() + '/' + inst.Name()
            if shiftType == 'relative':
                line = ",".join(["Sensitivity Based", instFactorType, factorID, "Whole", dataStr, rawPxStr, scaledRawPx, relativeShift])
                line = FRiskCubeWriterBase.BaseWriter._encodeData(line)
                print(line, file=fp)
            if shiftType != 'relative':
                line = ",".join(["Sensitivity Based", instFactorType, factorID, "Whole", dataStr, rawPxStr, scaledRawPx])
                line = FRiskCubeWriterBase.BaseWriter._encodeData(line)
                print(line, file=fp)

    def _getDirectoryOrFile(self, filename, base):
        writeFolder = os.path.dirname(filename)
        runDatefileName = os.path.basename(filename) + ".csv"
        baseDatefileName = os.path.basename(filename) + "_Base" + ".csv"
        if base:
            outputPath = writeFolder + '/' + tomorrow + '/'
            self._logger.logInfo("Creating output directory for Base Date market data:{0}".format(str(outputPath)))
            if not os.path.exists(outputPath):
                os.mkdir(outputPath)
            destinationFolder = outputPath + baseDatefileName
        elif not base:
            outputPath = writeFolder + '/' + today + '/'
            self._logger.logInfo("Creating output directory for Run Date market data:{0}".format(str(outputPath)))
            if not os.path.exists(outputPath):
                os.mkdir(outputPath)
            destinationFolder = outputPath + runDatefileName
        return destinationFolder
            
    


    def write(self, overwrite, filepath=r'C:\Temp\RiskExport\Export.txt'):
        """
        Writes the output in Risk Cube format in several parts - report header,
        data header, data rows.
        """		
        FRiskCubeWriterBase.BaseWriter._initDirs(filepath)
        filename = self._getNewFileName(filepath, overwrite)
        filename_Today = self._getDirectoryOrFile(filepath, False)
        base_filename = self._getDirectoryOrFile(filepath, True)
        id_ = int(hashlib.md5(filename.encode("utf-8")).hexdigest(), 16)
        base_id_ = int(hashlib.md5(base_filename.encode("utf-8")).hexdigest(), 16)
			
        try:
            
            with open(filename_Today, 'w') as fp:
                self._writeDataHeader(fp)
                self._writeDataRows(fp, None, "relative")
            self._logger.logInfo("{0} successfully exports into file {1}".format(self.__class__.__name__, filename_Today))
            self._logger.summaryAddOk("File", id_, "Export")
            with open(base_filename, 'w') as fp:
                self._writeBaseDataHeader(fp)
                self._writeDataRows(fp, "Base", None)
            self._logger.logInfo("{0} successfully exports into file {1}".format(self.__class__.__name__, base_filename))
            self._logger.summaryAddOk("File", base_id_, "Export")
            
        except Exception as err:
            tb = inspect.getframeinfo(inspect.trace()[-1][0])
            self._logger.logInfo("{2}.{3}() line {4}: {0} - {1}.".format(type(err).__name__,
                    err, tb.filename, tb.function, tb.lineno))
            self._logger.logError("{0} failed to export to file {1}".format(self.__class__.__name__, filename))
            self._logger.logInfo("{2}.{3}() line {4}: {0} - {1}.".format(type(err).__name__,
                    err, tb.base_filename, tb.function, tb.lineno))
            self._logger.logError("{0} failed to export to file {1}".format(self.__class__.__name__, base_filename))



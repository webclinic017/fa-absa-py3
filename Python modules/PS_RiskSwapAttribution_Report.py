import acm
from datetime import datetime
from xml.etree import ElementTree

import FReportAPI
import NamespaceTimeFunctions
from PS_Functions import get_pb_fund_shortname
import PS_Functions
import PS_XMLReportingTools
import ShortEndDelta
from at_logging import  getLogger, bp_start


LOGGER = getLogger()



ael_variables = []
ael_variables.append(['clientName', 'Client Name', 'FCounterParty', acm.FCounterParty.Instances(), None, 1, 0, 'Client Name that will be passed to all reports', None, 1])
ael_variables.append(['reportTitle', 'Report Title', 'string', None, 'Risk Swap Attribution', 1, 0, 'PreProcessor Parameter', None, 1])    
ael_variables.append(['TrdFilter', 'Trade Filter:', 'FTradeSelection', acm.FTradeSelection.Instances(), None, 1, 0, 'Name of Trade Filter\nUsed in both ShortEndDelta and BenchmarkDelta reports'])
ael_variables.append(['Currency', 'Currency:', 'FCurrency', acm.FCurrency.Instances(), 'ZAR', 1, 0, 'Currency'])
ael_variables.append(['Curve', 'Yield Curve:', 'FYieldCurve', acm.FYieldCurve.Instances(), 'ZAR-SWAP', 1, 0, 'Yield Curve'])  
ael_variables.append(['filename', 'Filename', 'string', None, 'File_RiskSwapAttribution', 1, 0, 'Filename', None, 1])
ael_variables.append(['filepath', 'File Path', 'string', None, 'F:\\', 0, 0, 'File path where report will be saved', None, 1])

class ReportXML():
    def __init__(self, riskSwapAttrDict, paramDict):
        self.root = ElementTree.XML('<PRIMEReport></PRIMEReport>')
        
        reportElement = ElementTree.SubElement(self.root, 'ReportDetail')
        totals = {'Non Over': 0.0,
             'Over': 0.0,
             'PnL Expect': 0.0,
             'Total': 0.0}

        for bmark in riskSwapAttrDict:
            totals['Non Over'] += riskSwapAttrDict[bmark]['Non Over']
            totals['Over'] += riskSwapAttrDict[bmark]['Over']
            totals['PnL Expect'] += riskSwapAttrDict[bmark]['PnL Expect']
            totals['Total'] += riskSwapAttrDict[bmark]['Total']

        rowElement = ElementTree.SubElement(reportElement, 'ReportRow', attrib={'Label':'Total'})
        ElementTree.SubElement(rowElement, 'NonOver').text = str(totals['Non Over'])
        ElementTree.SubElement(rowElement, 'Over').text = str(totals['Over'])
        ElementTree.SubElement(rowElement, 'PnLExpect').text = str(totals['PnL Expect'])
        ElementTree.SubElement(rowElement, 'Total').text = str(totals['Total'])
        ElementTree.SubElement(rowElement, 'Change').text = ' '
        ElementTree.SubElement(rowElement, 'CurveT').text = ' '
        ElementTree.SubElement(rowElement, 'CurveT1').text = ' '

        for bmark in sorted(riskSwapAttrDict.keys(), key=lambda x: acm.FInstrument[x].ExpiryDate(), reverse=False):
            rowElement = ElementTree.SubElement(reportElement, 'ReportRow', attrib={'Label':bmark})
            ElementTree.SubElement(rowElement, 'NonOver').text = str(riskSwapAttrDict[bmark]['Non Over'])
            ElementTree.SubElement(rowElement, 'Over').text = str(riskSwapAttrDict[bmark]['Over'])
            ElementTree.SubElement(rowElement, 'PnLExpect').text = str(riskSwapAttrDict[bmark]['PnL Expect'])
            ElementTree.SubElement(rowElement, 'Total').text = str(riskSwapAttrDict[bmark]['Total'])
            ElementTree.SubElement(rowElement, 'Change').text = str(riskSwapAttrDict[bmark]['Change'])
            ElementTree.SubElement(rowElement, 'CurveT').text = str(riskSwapAttrDict[bmark]['Curve_T'])
            ElementTree.SubElement(rowElement, 'CurveT1').text = str(riskSwapAttrDict[bmark]['Curve_T-1'])
        
        parameterElement = ElementTree.SubElement(self.root, 'ReportParameters')
        generated_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        UTC_offset = (datetime.now() - datetime.utcnow()).seconds / 3600
        generated_time += ' (UTC+0%i:00)' % UTC_offset
        
        ElementTree.SubElement(parameterElement, 'GeneratedTime').text = generated_time
        ElementTree.SubElement(parameterElement, 'ReportDate').text = acm.Time.DateToday()
        ElementTree.SubElement(parameterElement, 'FrameworkVersion').text = paramDict['FrameworkVersion']
        ElementTree.SubElement(parameterElement, 'TradeFilter').text = paramDict['TrdFilter']
        
    def __str__(self):
        return ElementTree.tostring(self.root)

class RiskSwapAttributionReport:
    def __init__(self, endDate, ParamDict):
        self.reportEndDate = endDate
        self.shortEndDeltaParamDict = ParamDict
        self.RiskResults = {}
        self.shortEndDeltaResults = {}
        self.benchmarkDeltaResults = {}
        self.tradeFilter = ParamDict['TrdFilter']
        self.yieldCurve = ParamDict['Curve']
        self.RiskResults = {}
        if 'frameworkVersion' in ParamDict.keys():
            self.frameworkVersion = ParamDict['frameworkVersion']
        else:
            self.frameworkVersion = 'N/A'
        
    def getReportValues(self):
        # Populate RiskResults dictionary
        self.getShortEndDeltaResults()
        self.getBenchmarkDeltaResults()
        
        myKeys = self.shortEndDeltaResults.keys()
        myKeys += self.benchmarkDeltaResults.keys()
        myKeys = set(myKeys)
    
        for k in myKeys:
            self.RiskResults[k] = {}
            
            self.RiskResults[k]['Over'] = self.shortEndDeltaResults.get(k, 0)
            self.RiskResults[k]['Non Over'] = self.benchmarkDeltaResults.get(k, 0)
                
            self.RiskResults[k]['Total'] = self.RiskResults[k]['Over'] + self.RiskResults[k]['Non Over']

            # Create Curve Movement
            self.RiskResults[k]['Curve_T-1'], self.RiskResults[k]['Curve_T'] = PS_Functions.get_latest_price_movement(k, self.reportEndDate)
            self.RiskResults[k]['Change'] = self.RiskResults[k]['Curve_T'] - self.RiskResults[k]['Curve_T-1']

            # Calc PnL Expect
            self.RiskResults[k]['PnL Expect'] = self.RiskResults[k]['Change'] * self.RiskResults[k]['Total'] * 100
            
    def toXML(self):
        # Used for PDF generation
        pDict = {'FrameworkVersion':self.frameworkVersion,
                'TrdFilter': self.tradeFilter.Name()}
        reportXML = ReportXML(self.RiskResults, pDict)        
        return str(reportXML)
  
    def getShortEndDeltaResults(self):
        pDict = dict(self.shortEndDeltaParamDict)  # This is required because of the "Multiple Inputs" behaviour of the ShortEndDelta script
        pDict['TrdFilter'] = [self.shortEndDeltaParamDict['TrdFilter']]
        pDict['Currency'] = [self.shortEndDeltaParamDict['Currency']]
        pDict['Curve'] = [self.shortEndDeltaParamDict['Curve']]
        temp = ShortEndDelta.ael_main(pDict, for_report_controller=True)
        for i in range(len(temp) - 1):
            self.shortEndDeltaResults[temp[i][0]] = temp[i][2]

    def getMappedYCs(self):
        ycSet = set()
        calc_space = acm.Calculations().CreateStandardCalculationsSpaceCollection()  
        for ins in self.tradeFilter.Instruments():
            ins_calc = ins.Calculation()
            ycSet.add(ins_calc.MappedCreditCurve(calc_space))
            ycSet.add(ins_calc.MappedDiscountCurve(calc_space))
            ycSet.add(ins_calc.MappedRepoCurve(calc_space))
            ycSet.add(ins_calc.MappedRiskFreeDiscountCurve(calc_space))

            for l in ins.Legs():
                l_calc = l.Calculation()
                ycSet.add(l_calc.MappedCreditCurve(calc_space))
                ycSet.add(l_calc.MappedDiscountCurve(calc_space))
                ycSet.add(l_calc.MappedRepoCurve(calc_space))
                ycSet.add(l_calc.MappedRiskFreeDiscountCurve(calc_space))

            idxRef = ins.IndexReference()
            if idxRef:
                idxRef_calc = idxRef.Calculation()
                ycSet.add(idxRef_calc.MappedCreditCurve(calc_space))
                ycSet.add(idxRef_calc.MappedDiscountCurve(calc_space))
                ycSet.add(idxRef_calc.MappedRepoCurve(calc_space))
                ycSet.add(idxRef_calc.MappedRiskFreeDiscountCurve(calc_space))
        return set([acm.FYieldCurve[ycInfo.Name()] for ycInfo in ycSet if ycInfo is not None])

    def getBenchmarkDeltaResults(self):
        context = acm.GetDefaultContext()
        sheet_type = 'FPortfolioSheet'
        calc_space = acm.Calculations().CreateCalculationSpace(context, sheet_type)
        top_node = calc_space.InsertItem(self.tradeFilter)
        calc_space.Refresh()
        column_id = 'Benchmark Delta Instruments'
        vector = acm.FArray()
        curves = self.getMappedYCs()
        curves.add(self.yieldCurve)
        benchmarks = set()
        for yc in curves:
            for b in yc.Benchmarks():
                benchmarks.add(b)
        benchmarks = sorted(benchmarks, key=lambda x: x.Instrument().Name())
        for b in benchmarks:
            param = acm.FNamedParameters();
            param.AddParameter('instrument', b.Instrument())
            vector.Add(param)        
        column_config = acm.Sheet.Column().ConfigurationFromVector(vector)
        ins_node = top_node.Iterator().Find(self.tradeFilter.Name()).Tree()
        calculation = calc_space.CreateCalculation(ins_node, column_id, column_config)            
        count = 0
        for cv in calculation.Value():
            self.benchmarkDeltaResults[benchmarks[count].Instrument().Name()] = cv.Number()
            count += 1
           
    def createReport(self, filepath, filename, xslt, clientName, reportName):
        report = FReportAPI.FWorksheetReportApiParameters()
        self._setReportAPIParameters(report, filepath, filename, xslt)
        
        root = ElementTree.XML(self.toXML())
        reportParameters = root.find("ReportParameters")
        
        if not reportParameters:
            reportParameters = ElementTree.SubElement(root, "ReportParameters")
        else:
            reportParameters = reportParameters[0]

        reportXml = ElementTree.tostring(root)
        reportXml = PS_XMLReportingTools._addAddress(reportXml, clientName.Name())
        reportXml = PS_XMLReportingTools._addReportParameter(reportXml, 'ReportName', reportName)
        reportXml = PS_XMLReportingTools._addRunLocation(reportXml)
        report.CreateReportByXml(reportXml)

    def _setReportAPIParameters(self, report, filepath, filename, xslTemplate):
        report.ambAddress = ''
        report.ambSender = ''
        report.ambSubject = ''
        report.ambXmlMessage = False
        report.clearSheetContent = False
        report.compressXmlOutput = False
        report.createDirectoryWithDate = False
        report.dateFormat = '%d%m%y'
        report.expiredPositions = False
        report.fileDateFormat = ''
        report.fileDateBeginning = False
        report.fileName = filename
        report.filePath = filepath
        report.function = None
        report.gcInterval = 5000
        report.gridOutput = False
        report.gridUseLoopbackGridClient = False
        report.gridRowPartitionCbArg = None
        report.gridRowPartitionCbClass = None
        report.gridExcludeRowCbClass = "FReportGridCallbacks.ExcludeRowManager"
        report.gridAggregateXmlCbClass = None
        report.gridTimeout = None
        report.gridRowSet = None
        report.grouping = 'Default'
        report.htmlToFile = False
        report.htmlToPrinter = False
        report.htmlToScreen = False
        report.includeDefaultData = False
        report.includeFormattedData = False
        report.includeFullData = False
        report.includeRawData = False
        report.instrumentParts = False
        report.instrumentRows = False
        report.maxNrOfFilesInDir = 1000
        report.multiThread = False
        report.numberOfReports = 1
        report.orders = None
        report.overridePortfolioSheetSettings = False
        report.overrideTimeSheetSettings = False
        report.overrideTradeSheetSettings = False
        report.overwriteIfFileExists = True
        report.param = None
        report.performanceStrategy = 'Periodic full GC to save memory'
        report.portfolioReportName = ''
        report.portfolioRowOnly = False
        report.portfolios = None
        report.preProcessXml = None
        report.printStyleSheet = 'FStandardCSS'
        report.printTemplate = 'FStandardTemplateClickable'
        report.reportName = ''
        report.secondaryFileExtension = '.csv'
        report.secondaryOutput = True
        report.secondaryTemplate = xslTemplate
        report.sheetSettings = {}
        report.snapshot = True
        report.storedASQLQueries = None
        report.template = None
        report.tradeFilters = None
        report.tradeRowsOnly = False
        report.trades = None
        report.updateInterval = 60
        report.workbook = None
        report.xmlToAmb = False
        report.xmlToFile = False
        report.zeroPositions = False
        report.guiParams = None
        report.reportApiObject = None

def ael_main(param):
    process_name = "ps.risk_swap_attribution.{0}".format(get_pb_fund_shortname(param["clientName"]))
    with bp_start(process_name):       
            
        param['InputType'] = 'Filter'
        param['Portfolio'] = None
        param['ReportType'] = 'Short End Delta'
        param['Outpath'] = 'NotApplicable'
        riskReport = RiskSwapAttributionReport(acm.Time().DateToday(), param)
        riskReport.getReportValues()
        if 'fileID_SoftBroker' in param.keys():
            riskReport.createReport(param['filepath'], '_'.join([param['fileID_SoftBroker'], param['filename'],
            acm.Time.DateToday().replace('-', '')]), 'ps_riskSwapAttr_csv', param['clientName'], param['reportTitle'])
        else:
            riskReport.createReport(param['filepath'], '_'.join([param['filename'], acm.Time.DateToday().replace('-', '')]),
            'ps_riskSwapAttr_csv', param['clientName'], param['reportTitle'])
        LOGGER.info('Risk Swap Attribution Report - Completed Successfully')

        
def _convertToParamDictionary(configuration, report_name):
    riskdict = {}
    riskdict['TrdFilter'] = configuration['TrdFilter_' + report_name]
    riskdict['Currency'] = configuration['Currency_' + report_name]
    riskdict['Curve'] = configuration['Curve_' + report_name]
    riskdict['reportTitle'] = configuration['reportTitle_' + report_name]
    riskdict['clientName'] = acm.FCounterParty[configuration['clientName']]
    riskdict['filename'] = configuration['Filename_' + report_name]
    riskdict['filepath'] = configuration['OutputPath']
    riskdict['fileID_SoftBroker'] = configuration['fileID_SoftBroker']
    if riskdict['TrdFilter'] is None:
        raise ValueError(report_name + ' Tradefilter is mandatory')
    return riskdict

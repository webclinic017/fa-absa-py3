import acm
from datetime import datetime
import itertools
from xml.etree import ElementTree

import FReportAPI
import NamespaceTimeFunctions
from PS_Functions import get_pb_fund_shortname
import PS_Functions
import PS_XMLReportingTools
from at_logging import  getLogger, bp_start


LOGGER = getLogger()

ael_variables = []
ael_variables.append(['clientName', 'Client Name', 'FCounterParty', acm.FCounterParty.Instances(), None, 1, 0, 'Client Name that will be passed to all reports', None, 1] )
ael_variables.append(['reportTitle', 'Report Title', 'string', None, 'Risk Bond Attribution', 1, 0, 'PreProcessor Parameter', None, 1] )    
ael_variables.append(['TrdFilter', 'Trade Filter:', 'FTradeSelection', acm.FTradeSelection.Instances(), None, 1, 0, 'Name of Trade Filter\nUsed in BenchmarkDelta report'])
ael_variables.append(['CollectionTrdFilter', 'Bond Collection Trade Filter', 'FTradeSelection', acm.FTradeSelection.Instances(), acm.FTradeSelection['PS_BondCollectionRiskAttr'], 1, 0, 'Name of Trade Filter\nUsed to select all bonds traded to build risk factor list'])
ael_variables.append(['Curve', 'Yield Curve:', 'FYieldCurve', acm.FBenchmarkCurve.Instances(), 'ZAR-BOND-PRIME', 1, 0, 'Yield Curve'])  
ael_variables.append(['filename', 'Filename', 'string', None, 'File_RiskBondAttribution', 1, 0, 'Filename', None, 1] )
ael_variables.append(['filepath', 'File Path', 'string', None, 'F:\\', 0, 0, 'File path where report will be saved', None, 1] )

class ReportXML():
    def __init__(self, riskBondAttrDict, paramDict):
        self.root = ElementTree.XML('<PRIMEReport></PRIMEReport>')
        
        #Totals Rows
        reportElement = ElementTree.SubElement( self.root, 'ReportDetail')
        totals = {}
        totals['Total'] = {'Total': 0.0, 'PnL Expect': 0.0, 'Position': 0.0}
        totals['Financed'] = {'Total': 0.0, 'PnL Expect': 0.0, 'Position': 0.0}
        totals['FullyFunded'] = {'Total': 0.0, 'PnL Expect': 0.0, 'Position': 0.0}
        
        #Top Level Total Row
        myKeys = set(itertools.chain(riskBondAttrDict['Financed'].keys(), riskBondAttrDict['FullyFunded'].keys()))
        for k in ('Financed', 'FullyFunded'):
            for bmark in myKeys:
                totals['Total']['PnL Expect'] += riskBondAttrDict[k][bmark]['PnL Expect']
                totals['Total']['Total'] += riskBondAttrDict[k][bmark]['Total']
                totals['Total']['Position'] += riskBondAttrDict[k][bmark]['Position']

        rowElement = ElementTree.SubElement( reportElement,  'ReportRow', attrib={'Label':'Total'} )
        ElementTree.SubElement( rowElement,  'PnLExpect' ).text = str(totals['Total']['PnL Expect'])
        ElementTree.SubElement( rowElement,  'Total' ).text = str(totals['Total']['Total'])
        ElementTree.SubElement( rowElement,  'Position' ).text = str(totals['Total']['Position'])
        ElementTree.SubElement( rowElement,  'Change' ).text = ' '
        ElementTree.SubElement( rowElement,  'CurveT' ).text = ' '
        ElementTree.SubElement( rowElement,  'CurveT1' ).text = ' '
        ElementTree.SubElement( rowElement,  'InsType' ).text = ' '
        ElementTree.SubElement( rowElement,  'FinType' ).text = ' '  
        
        for section in ('Financed', 'FullyFunded'):
            #Section Total
            for bmark in riskBondAttrDict[section].keys():
                totals[section]['PnL Expect'] += riskBondAttrDict[section][bmark]['PnL Expect']
                totals[section]['Total'] += riskBondAttrDict[section][bmark]['Total']
                totals[section]['Position'] += riskBondAttrDict[section][bmark]['Position']
                
            rowElement = ElementTree.SubElement( reportElement,  'ReportRow', attrib={'Label':'%s Total' % section} )
            ElementTree.SubElement( rowElement,  'PnLExpect' ).text = str(totals[section]['PnL Expect'])
            ElementTree.SubElement( rowElement,  'Total' ).text = str(totals[section]['Total'])
            ElementTree.SubElement( rowElement,  'Position' ).text = str(totals[section]['Position'])
            ElementTree.SubElement( rowElement,  'Change' ).text = ' '
            ElementTree.SubElement( rowElement,  'CurveT' ).text = ' '
            ElementTree.SubElement( rowElement,  'CurveT1' ).text = ' '  
            ElementTree.SubElement( rowElement,  'InsType' ).text = ' '
            ElementTree.SubElement( rowElement,  'FinType' ).text = ' '          
            
            #Section Sub Rows
            for bmark in sorted(riskBondAttrDict[section].keys(), key=lambda x: acm.FInstrument[x].InsType(), reverse=False):
                #Only include if Position <> 0 and Total BDelta <> 0
                if not (float(riskBondAttrDict[section][bmark]['Total']) == 0 and float(riskBondAttrDict[section][bmark]['Position']) == 0):
                    rowElement = ElementTree.SubElement( reportElement,  'ReportRow', attrib={'Label': bmark} )
                    ElementTree.SubElement( rowElement,  'PnLExpect' ).text = str(riskBondAttrDict[section][bmark]['PnL Expect'])
                    ElementTree.SubElement( rowElement,  'Total' ).text = str(riskBondAttrDict[section][bmark]['Total'])
                    ElementTree.SubElement( rowElement,  'Position' ).text = str(riskBondAttrDict[section][bmark]['Position'])
                    ElementTree.SubElement( rowElement,  'Change' ).text = str(riskBondAttrDict[section][bmark]['Change'])
                    ElementTree.SubElement( rowElement,  'CurveT' ).text = str(riskBondAttrDict[section][bmark]['Curve_T'])
                    ElementTree.SubElement( rowElement,  'CurveT1' ).text = str(riskBondAttrDict[section][bmark]['Curve_T-1'])
                    ElementTree.SubElement( rowElement,  'InsType' ).text = str(riskBondAttrDict[section][bmark]['InsType'])
                    ElementTree.SubElement( rowElement,  'FinType' ).text = str(riskBondAttrDict[section][bmark]['FinType'])
        
        parameterElement = ElementTree.SubElement( self.root, 'ReportParameters')
        generated_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        UTC_offset = (datetime.now() - datetime.utcnow()).seconds/3600
        generated_time += ' (UTC+0%i:00)'% UTC_offset
        ElementTree.SubElement( parameterElement,  'GeneratedTime' ).text = generated_time
        ElementTree.SubElement( parameterElement,  'ReportDate' ).text = acm.Time.DateToday()
        ElementTree.SubElement( parameterElement,  'FrameworkVersion' ).text = paramDict['FrameworkVersion']
        ElementTree.SubElement( parameterElement,  'TradeFilter' ).text = paramDict['TrdFilter']
        
    def __str__(self):
        return ElementTree.tostring(self.root)

class RiskBondAttributionReport:
    def __init__(self, endDate, ParamDict):
        self.reportEndDate = endDate

        self.RiskResults = {}
        self.RiskResults['Financed'] = {}
        self.RiskResults['FullyFunded'] = {}
        
        self.benchmarkDeltaResults = {}
        self.benchmarkPositions = {}
        self.tradeFilter = ParamDict['TrdFilter']
        self.CollectionTrdFilter = ParamDict['CollectionTrdFilter']
        self.yieldCurve = ParamDict['Curve']
        
        if 'frameworkVersion' in ParamDict.keys():
            self.frameworkVersion = ParamDict['frameworkVersion']
        else:
            self.frameworkVersion = 'N/A'
            
    def getReportValues(self):
        #Populate RiskResults dictionary
        self.getBenchmarkDeltaResults()
        self.getBenchmarkPositions()
        
        myKeys = set(itertools.chain(self.benchmarkDeltaResults['Financed'].keys(), self.benchmarkDeltaResults['FullyFunded'].keys()))
        for section in ('Financed', 'FullyFunded'):
            for k in myKeys:
                self.RiskResults[section][k] = {}
                self.RiskResults[section][k]['Total'] = self.benchmarkDeltaResults[section][k]
                
                #Get position
                self.RiskResults[section][k]['Position'] = self.benchmarkPositions[section].get(k, 0)

                #Create Curve Movement
                self.RiskResults[section][k]['Curve_T-1'], self.RiskResults[section][k]['Curve_T'] = PS_Functions.get_latest_price_movement(k, self.reportEndDate)
                self.RiskResults[section][k]['Change'] = self.RiskResults[section][k]['Curve_T'] - self.RiskResults[section][k]['Curve_T-1']

                #Calc PnL Expect
                self.RiskResults[section][k]['PnL Expect'] = self.RiskResults[section][k]['Change'] * self.RiskResults[section][k]['Total'] * 100
                
                #Populate InsType, Fin Type
                self.RiskResults[section][k]['InsType'] = acm.FInstrument[k].InsType()
                self.RiskResults[section][k]['FinType'] = section
                
            
    def toXML(self):
        #Used for PDF generation
        pDict = {'FrameworkVersion':self.frameworkVersion,
                'TrdFilter': self.tradeFilter.Name()}
        reportXML = ReportXML(self.RiskResults, pDict)   
        return str(reportXML)
  
    def getBenchmarkDeltaResults(self):
        context = acm.GetDefaultContext()
        sheet_type = 'FPortfolioSheet'
        calc_space = acm.Calculations().CreateCalculationSpace( context, sheet_type )
        top_node = calc_space.InsertItem( self.tradeFilter )
        
        top_node.ApplyGrouper( acm.FAttributeGrouper('Trade.IsFinanced') )
        
        calc_space.Refresh()
        column_id = 'Benchmark Delta Instruments'
        vector = acm.FArray()
        benchmarksList = [b.Instrument() for b in self.yieldCurve.Benchmarks()]
        benchmarksList.extend([t.Instrument() for t in self.CollectionTrdFilter.Snapshot()])
        benchmarks = sorted(list(set(benchmarksList)), key=lambda x: x.ExpiryDate())
        for b in benchmarks:
            param = acm.FNamedParameters();
            param.AddParameter( 'instrument', b )
            vector.Add( param )
             
        column_config = acm.Sheet.Column().ConfigurationFromVector( vector )
               
        self.benchmarkDeltaResults['Financed'] = {}
        self.benchmarkDeltaResults['FullyFunded'] = {}
           
        if top_node.Iterator().Find( "Financed" ):
            group_node = top_node.Iterator().Find( "Financed" ).Tree()
            calculation = calc_space.CreateCalculation( group_node, column_id, column_config )            
            count = 0
            for cv in calculation.Value():
                self.benchmarkDeltaResults['Financed'][benchmarks[count].Instrument().Name()] = cv.Number()
                count += 1  
        else:
            for key in benchmarks:
                self.benchmarkDeltaResults['Financed'][key.Instrument().Name()] = 0
                
            
        if top_node.Iterator().Find( "Fully Funded" ):
            group_node = top_node.Iterator().Find( "Fully Funded" ).Tree()
            calculation = calc_space.CreateCalculation( group_node, column_id, column_config )            
            count = 0
            for cv in calculation.Value():
                self.benchmarkDeltaResults['FullyFunded'][benchmarks[count].Instrument().Name()] = cv.Number()
                count += 1    
        else:
            for key in benchmarks:
                self.benchmarkDeltaResults['FullyFunded'][key.Instrument().Name()] = 0    
        
  
    def getBenchmarkPositions(self):
        '''
            Method used to set up the calculation space used to calculate the positions for each instrument in the trade filter
        '''
        context = acm.GetDefaultContext()
        sheet_type = 'FPortfolioSheet'
        calc_space = acm.Calculations().CreateCalculationSpace( context, sheet_type )
        self.benchmarkPositions['Financed'] = {}
        self.benchmarkPositions['FullyFunded'] = {}
        column_id = 'Portfolio Position'
        
        top_node = calc_space.InsertItem( self.tradeFilter )
        
        top_node.ApplyGrouper( acm.FAttributeGrouper('Trade.IsFinanced') )
        calc_space.Refresh()
        
        if top_node.Iterator().Find( "Financed" ):
            group_node = top_node.Iterator().Find( "Financed" ).Tree()
            self.calculate_position(group_node, calc_space, column_id, 'Financed')
        
        if top_node.Iterator().Find( "Fully Funded" ):
            group_node = top_node.Iterator().Find( "Fully Funded" ).Tree()
            self.calculate_position(group_node, calc_space, column_id, 'FullyFunded')
      
  
    def calculate_position(self, node, calc_space, column_id, section):
        '''
            Recursive method used to traverse the calculation tree, and calculates the position for each instrument
        '''
        node_calc = calc_space.CreateCalculation(node, column_id)
        ins_name = node.Item().StringKey()
        
        # Get the value of the calculation for the node
        if ins_name in self.benchmarkDeltaResults[section].keys():
            try:
                self.benchmarkPositions[section][ins_name] = node_calc.Value().Number()
            except Exception, e :        #Sometimes the ADFL column returns a int object directly instead of an 'FCalculatedValue'
                self.benchmarkPositions[section][ins_name] = node_calc.Value()
                
        # Traverse the tree
        if node.NumberOfChildren():
            child_iter = node.Iterator().FirstChild()
            while child_iter:
                self.calculate_position(child_iter.Tree(), calc_space, column_id, section)
                child_iter = child_iter.NextSibling()

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
        report.template= None
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
    process_name = "ps.risk_bond_attribution.{0}".format(get_pb_fund_shortname(param["clientName"]))
    with bp_start(process_name):
               
        param['InputType'] = 'Filter'
        param['Portfolio'] = None
        param['ReportType'] = 'Short End Delta'
        param['Outpath'] = 'NotApplicable'
        riskReport = RiskBondAttributionReport( acm.Time().DateToday(), param)
        riskReport.getReportValues()
        if 'fileID_SoftBroker' in param.keys():
            riskReport.createReport(param['filepath'], '_'.join([param['fileID_SoftBroker'], param['filename'],
            acm.Time.DateToday().replace('-', '')]), 'ps_riskBondAttr_csv', param['clientName'], param['reportTitle'])
        else:
            riskReport.createReport(param['filepath'], '_'.join([param['filename'], acm.Time.DateToday().replace('-', '')]),
            'ps_riskBondAttr_csv', param['clientName'], param['reportTitle'])
        LOGGER.info('Risk Bond Attribution Report - Completed Successfully')
        
def _convertToParamDictionary(configuration, report_name):
    riskdict = {}
    riskdict['TrdFilter'] = configuration['TrdFilter_'+ report_name]
    riskdict['Curve'] = configuration['Curve_'+ report_name]
    riskdict['reportTitle'] = configuration['reportTitle_' + report_name]
    riskdict['clientName'] = acm.FCounterParty[configuration['clientName']]
    riskdict['filename'] = configuration['Filename_'+ report_name]
    riskdict['filepath'] = configuration['OutputPath']
    riskdict['CollectionTrdFilter'] = configuration['CollectionTrdFilter_' +report_name]
    riskdict['fileID_SoftBroker'] = configuration['fileID_SoftBroker']
    if riskdict['TrdFilter'] is None:
        raise ValueError(report_name + ' Tradefilter is mandatory')    
    return riskdict
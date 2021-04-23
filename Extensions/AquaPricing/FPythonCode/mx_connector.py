'''--------------------------------------------------------------------------------------------------------
Date                    : 2011-08-25
Purpose                 : This script retrieves pricing data from ME using COM from the front end of Front and webservices from the backend of Front.
                          It is used to theoretically price exotic options.
Department and Desk     : Front Office - Equity Derivatives
Requester               : Stephen Zoio and Andrey Chechin
Developer               : Paul Jacot-Guillarmod and Stephen Zoio
CR Number               : 759644
---------------------------------------------------------------------------------------------------------------


HISTORY
=================================================================================================================
Date       Change no       Developer                         Description
--------------------------------------------------------------------------------
2015-02-24 XXXXXX          Anwar Banoo                Upadated script with to choose the MX version to default to
2015-02-25 ABITFA-3419    Edmundo Chissungo         Fixed a global name issue and set default MX version to 0
2016-04-12 ABITFA-4238    Ondrej Bahounek           Fix for getting portfolio for instruments without trades.
2016-11-22 ABITFA-4579    Libor Svoboda             Removed first trade portfolio dependency.
'''


import acm
import urllib2
from xml.dom.minidom import parseString   
import time
import re
import os

def getMXApiVersion():        
    if os.path.exists('C:\Program Files (x86)'):
        MXApiVersion = '700'
    else:
        MXApiVersion = '600'    
    return MXApiVersion

def isFrontEnd():
    ''' Checks to see if the code is being executed from the Front End (GUI or command line)
        or from the back end.
        
        A command line run needs to be considered to be from the Front End and use COM as the
        password files can't be accessed.  This prevents us from using the more usual test:
        str(acm.Class()) == 'FTmServer'
    '''
    return os.name == 'nt'

if isFrontEnd():
    import win32com.client
else:    
    import suds
    from suds.client import Client
    from suds.transport.https import HttpAuthenticated    

_dataDictionary = {}

def DateToString(date):
    ''' Converts an acm date to a string of format yyyymmdd
    '''
    ymd = acm.Time().DateToYMD(date)
    dateString = str(ymd[0]) + str(ymd[1]).zfill(2) + str(ymd[2]).zfill(2)
    return dateString

class MXInstrumentReader:
    def __init__(self, instrument, date):
        self.instrument = instrument
        self.date = date 
        self.prf_names = self._getPortfolioNames()
    
    def _get_data_wrapper(self, prf_name):
        val_group= self.instrument.ValuationGrpChlItem().Name()
        scenario_name = self._getScenarioName(val_group)
        date_string = DateToString(self.date)
        current_time = time.time()
        global _dataDictionary
        cache_key = prf_name + ':' + scenario_name + ':' + date_string
        if cache_key in _dataDictionary:
            data_wrapper = _dataDictionary[cache_key]
            time_diff = current_time - data_wrapper.readTime
            if time_diff < 30:
                return data_wrapper

        data_wrapper = MXDataWrapper(prf_name, scenario_name, val_group, self.date)
        _dataDictionary[cache_key] = data_wrapper
        return data_wrapper
        
    def _getPortfolioNames(self):
        prf_names = []
        for trade in self.instrument.Trades():
            if trade.Portfolio():
                portfolioName = trade.Portfolio().Name()
                prf_names.append(portfolioName.replace(' ', '_'))
        if not prf_names:
            print "Warning: Instrument '%s' doesn't have any valid trades." %(self.instrument.Name())
            prf_names.append("NO_PORTFOLIO")
        return list(set(prf_names))
        
    def GetMetric(self, metricName):
        instrumentName = self.instrument.Name()
        for prf_name in self.prf_names:
            data_wrapper = self._get_data_wrapper(prf_name)
            resultKey = data_wrapper.GetResultKey(metricName, instrumentName, [])
            try:
                result = data_wrapper.GetResult(resultKey)
            except KeyError:
                continue
            return result
        print 'Key value does not exist in ME:', resultKey
        return 0
    
    def _getScenarioName(self, valGroup):
        if isFrontEnd():
            if valGroup == 'AQUA_MEPDN_PV':            
                environmentName = 'FrontOfficeMEPDN_PV'
            elif valGroup == 'AQUA_MEGROUP_PV':
                environmentName = 'FrontOfficeMEGROUP_PV'
            elif valGroup == 'AQUA_MEPDN_ED_OPTIONS':
                environmentName = 'FrontOfficeMEPDN'
            else:
                environmentName = 'FrontOfficeMEUAT'
        else:
            if valGroup == 'AQUA_MEPDN_PV':
                environmentName = 'MiddleOfficeMEPDN_PV'
            elif valGroup == 'AQUA_MEGROUP_PV':
                environmentName = 'MiddleOfficeMEGROUP_PV'
            elif valGroup == 'AQUA_MEPDN_ED_OPTIONS':
                environmentName = 'MiddleOfficeMEPDN'
            else:
                environmentName = 'MiddleOfficeMEUAT'                                    
        
        configuration = acm.GetDefaultValueFromName(acm.GetDefaultContext(), acm.FObject, 'AquaConfiguration')
        doc = parseString(configuration)
        for element in doc.getElementsByTagName('Parameters'):
            if element.getAttribute('Environment').find(environmentName) >= 0:
                scenarioName = str(element.getElementsByTagName('scenario_name')[0].firstChild.nodeValue)
                return scenarioName
        return None
    
class MXDataWrapper:
    def __init__(self, portfolioName, scenarioName, valGroup, date):
        self.date = date
        if not isFrontEnd():
            self.username, self.password = self._getBackendLoginData(valGroup)
            self.wsdlPath = self._getWSDLPath(valGroup)
        
        self.environment, self.audience, self.monikerHead = self._getAquaParameters(valGroup)
        self.scenarioName = scenarioName
        self.portfolioName = portfolioName.replace(' ', '_')
        self.resultMap = self._getFOTableRows()
        self.readTime = time.time()
       
    def _generateMoniker(self):
        dateString = DateToString(self.date)
        moniker = self.monikerHead + '@' + dateString + '/generic.market.object/' + self.audience + '/resultsdata/' + self.portfolioName + '/' + self.scenarioName
        return moniker
        
    def _getWSDLPath(self, valGroup):
        ''' Return the location of the wsdl
        ''' 
        if valGroup in ('AQUA_MEPDN_ED_OPTIONS', 'AQUA_MEPDN_PV'):
            return 'file:///front/arena/apps/lib64/pythonlib26/suds/MXWebService5_MEPDN.wsdl'
        elif valGroup in ('AQUA_MEUAT_ED_OPTIONS', 'AQUA_MEGROUP_PV'):
            return 'file:///front/arena/apps/lib64/pythonlib26/suds/MXWebService5_MEUAT.wsdl'
    
    def _getBackendLoginData(self, valGroup):
        ''' When being called from the backend of Front, a sys username and password is retrieved from a file
            on the server to access ME via web-services.
        '''
        if valGroup in ('AQUA_MEPDN_ED_OPTIONS', 'AQUA_MEPDN_PV'):
            backEndFilePath = '//apps/services/front/FUNCTIONS/FA/pwfiles/sysFAAQUAprd'
        elif valGroup in ('AQUA_MEUAT_ED_OPTIONS', 'AQUA_MEGROUP_PV'):
            backEndFilePath = '//apps/services/front/FUNCTIONS/FA/pwfiles/sysFAAQUAuat'
            
        loginData = {}
        with open(backEndFilePath, 'r') as f:
            for row in f.readlines():
                key, value = row.split('=', 1)
                loginData[key.strip().lower()] = value.strip()
        try:
            return loginData['domain'] + '\\' + loginData['username'], loginData['password']
        except:
            print 'The ME username and password could not be retrieved from:', backEndFilePath
            return None, None
    
    def _getAquaParameters(self, valGroup):
        if isFrontEnd():
            if valGroup == 'AQUA_MEPDN_PV':            
                environmentName = 'FrontOfficeMEPDN_PV'
            elif valGroup == 'AQUA_MEGROUP_PV':
                environmentName = 'FrontOfficeMEGROUP_PV'
            elif valGroup == 'AQUA_MEPDN_ED_OPTIONS':
                environmentName = 'FrontOfficeMEPDN'
            else:
                environmentName = 'FrontOfficeMEUAT'
        else:
            if valGroup == 'AQUA_MEPDN_PV':
                environmentName = 'MiddleOfficeMEPDN_PV'
            elif valGroup == 'AQUA_MEGROUP_PV':
                environmentName = 'MiddleOfficeMEGROUP_PV'
            elif valGroup == 'AQUA_MEPDN_ED_OPTIONS':
                environmentName = 'MiddleOfficeMEPDN'
            else:
                environmentName = 'MiddleOfficeMEUAT'                                      
        
        configuration = acm.GetDefaultValueFromName(acm.GetDefaultContext(), acm.FObject, 'AquaConfiguration')
        doc = parseString(configuration)
        for element in doc.getElementsByTagName('Parameters'):
            if element.getAttribute('Environment').find(environmentName) >= 0:
                server = str(element.getElementsByTagName('server')[0].firstChild.nodeValue)
                audience = str(element.getElementsByTagName('audience')[0].firstChild.nodeValue)
                monikerHead = str(element.getElementsByTagName('moniker_head')[0].firstChild.nodeValue)
                return server, audience, monikerHead
        return None
        
    def _queryMX(self):
        ''' Connect to MX and make a Load query for a given moniker.  
            Return the xml returned from the load query.
        '''
        if isFrontEnd():
            moniker = self._generateMoniker()
            print '[AquaPricing]mx_connector: Connecting to ME @', moniker
            try:
                mxSessionFactory = win32com.client.Dispatch('MXApi.MXSessionFactory.%s' %getMXApiVersion())
                mxSession = mxSessionFactory.Create(self.environment)
            
                mxMoniker = win32com.client.Dispatch('MXApi.MXMoniker.%s' %getMXApiVersion())
                mxMoniker.ParseDisplayName(moniker)
                
                objRef = win32com.client.Dispatch('MXApi.MXObjRef.%s' %getMXApiVersion())
                objRef.Attach(mxSession, mxMoniker)
                if objRef.Exists():
                    objRef.Load()
                    message = objRef.Instance
                    return message.Content
                else:
                    print 'Data was not retrieved from ME for', moniker
                    return None
            except Exception, e:
                print 'COM call failed to connect to ME and retrieve data ', moniker
                print e
                return None
        else:
            if self.username and self.password:
                t = HttpAuthenticated(username=self.username, password=self.password)
                t.handler = urllib2.HTTPBasicAuthHandler(t.pm)
                t.urlopener = urllib2.build_opener(t.handler)
                
                url = self.wsdlPath
                client = Client(url, transport=t)
                
                moniker = self._generateMoniker()
                try:
                    message = client.service.Load(self.environment, self.username, moniker)
                    return message.content
                except suds.WebFault, e:
                    print 'Data was not retrieved from ME for', moniker
                    return None
            return None
            
    def _getFOTableXml(self):
        doc = self._queryMX()
        if doc:
            foTables = parseString(doc)
            for table in foTables.getElementsByTagName('FOTable'):
                if table.getAttribute('order') == '2':
                    return table 
        return None
    
    def _getFOTableHeaderMap(self, fotable):
        columnHeadings = {}
        for cell in fotable.getElementsByTagName('cell'):
            if int(cell.getAttribute('row')) == 0:
                columnHeadings[cell.firstChild.data] = int(cell.getAttribute('col'))
        self.columnHeadings =  columnHeadings
        self.tradeIDCol = columnHeadings['TradeID']
        self.metricNameCol = columnHeadings['MetricName']
        self.valueCol = columnHeadings['Value']
        self.resultTypeCol = columnHeadings['ResultType']
          
    def _getFOTableRows(self):
        fotable = self._getFOTableXml()
        results = {}
        if fotable:
            self._getFOTableHeaderMap(fotable)
            tableRows = []
            currentRow = -1
            for cell in fotable.getElementsByTagName('cell'):
                rowIndex = int(cell.getAttribute('row'))
                if rowIndex > 0:
                    if currentRow < rowIndex:
                        tableRows.append({})
                        tableRow = tableRows[len(tableRows)-1]
                        currentRow = rowIndex
                    columnIndex = int(cell.getAttribute('col'))
                    if cell.firstChild == None:
                        tableRow[columnIndex] = ''
                    else:
                        tableRow[columnIndex] = cell.firstChild.data        
           
            for resultRow in tableRows:
                resultType = resultRow[self.resultTypeCol]
                if resultRow[self.resultTypeCol] == 'Result':
                    metric = resultRow[self.metricNameCol]
                    tradeID = resultRow[self.tradeIDCol]
                    extraKeyNames = self._getExtraKeyNames(metric)
                    extraKeyValues = self._getExtraKeyValues(resultRow, extraKeyNames)
                    resultKey = self.GetResultKey(metric, tradeID, extraKeyValues)
                    results[resultKey] = resultRow[self.valueCol]
            
        return results

    def _getExtraKeyNames(self, metric):
        extraKeys = re.findall('(?<=[\(,])[-A-Za-z0-9-_]+(?=[\),])', metric)
        extraKeys.sort()
        return extraKeys      
        
    def _getExtraKeyValues(self, resultRow, extraKeys):
        extraKeyValues = []
        for key in extraKeys:
            colIndex = self.columnHeadings[key]
            value = resultRow[colIndex]
            extraKeyValues.append(value)
        return extraKeyValues
        
    def GetResultKey(self, metric, tradeID, extraKeyValues):
        ''' ExtraKeys are currently ignored.
        '''
        return tradeID + ':' + metric + ':' # + ":".join(extraKeyValues)
        
    def GetResult(self, key):
        result = float(self.resultMap[key])
        return result
        
    def __str__(self):
        metricValues = ''
        for row in self.metricTable:
            metricValues += str(row.MetricName) + ' = ' + row.Value + '\n'
        return metricValues

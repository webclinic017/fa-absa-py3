""" Compiled: 2020-09-18 10:38:50 """

#__src_file__ = "extensions/FACL/ACL/./etc/FACLArMLResponse.py"
from __future__ import print_function
import acm
import datetime 
import traceback
import re
from xml.etree.ElementTree import fromstring

encoding = 'iso-8859-1'
xmlTextDeclaration = '<?xml version="1.0" encoding="%s"?>\n' % encoding

class FACLArMLParseException(Exception): pass

class FACLArMLResponse:
    """Parse XML responses from ACR"""
    
    def __init__(self, armlString, nameSpace = '{http://www.sungard.com/Adaptiv/Crs/Schema}'):
        self._responseTree = fromstring(xmlTextDeclaration + armlString)
        self._nameSpace = nameSpace
        self._requestID = ''
        self._status = ''
        self._exceptionOccurred = True
        self._exceptionSeverity = ''
        self._exceptionDescription = ''
        self._exceptionContents = []
        self._exceptions = []
        self._limitOk = False
        self._availabilityOk = False
        self._acr_ref = ''
        self._headline = ''
        self._zeroViolations = ''
        self._violationContents = []
        self._availViolations = []
        self._availContents = []
        self._counterparty = ''
        self._columnGroups = []
        self._graphData = {}
        self._violations = []
        
        self._parseResponse()
    
    def RequestID(self):
        return self._requestID
    
    def Status(self):
        return self._status
    
    def ExceptionOccurred(self):
        return self._exceptionOccurred

    def ExceptionDescription(self):
        return self._exceptionDescription
    
    def ExceptionContents(self):
        return self._exceptionContents
    
    def ExceptionSeverity(self):
        return self._exceptionSeverity
    
    def Exceptions(self):
        return self._exceptions

    def LimitOk(self):
        return self._limitOk
    
    def AvailabilityOk(self):
        return self._availabilityOk

    def AvailabilityContents(self):
        return self._availContents

    def AvailabilityViolationContents(self):
        return self._availViolations

    def AvailabilityColumnGroups(self):
        return self._columnGroups

    def ViolationContents(self):
        return self._violationContents

    def Headline(self):
        return self._headline + self._zeroViolations

    def AcrRef(self):
        return self._acr_ref
    
    def Counterparty(self):
        return self._counterparty
       
    def GraphData(self):
        return self._graphData
    
    def ActionAlreadyInProgress(self):
        returnValue = False
        exceptions = self.Exceptions()
        for e in exceptions:
            exceptionDescription = e[2]
            if re.search("Action already in progress", exceptionDescription):
                returnValue = True
                break
        return returnValue
    
    def ActionAddExistingDeal(self):
        returnValue = False
        exceptions = self.Exceptions()
        for e in exceptions:
            exceptionDescription = e[2]
            if re.search("Deal [0-9]+ already exists", exceptionDescription):
                returnValue = True
                break
        return returnValue

    def ActionModifyNonExistingDeal(self):
        returnValue = False
        exceptions = self.Exceptions()
        for e in exceptions:
            exceptionDescription = e[2]
            if re.search("Deal Reference='[0-9]+' not found in DealControl", exceptionDescription):
                returnValue = True
                break
        return returnValue
        
    def ActionConfirmWhenNoActionInProgress(self):
        returnValue = False
        exceptions = self.Exceptions()
        for e in exceptions:
            exceptionDescription = e[2]
            if re.search("Unable to confirm deal [0-9]+: No action in progress", exceptionDescription):
                returnValue = True
                break
        return returnValue

    def ActionDealAlreadyReversed(self):
        returnValue = False
        exceptions = self.Exceptions()
        for e in exceptions:
            exceptionDescription = e[2]
            if re.search("Deal has already been reversed", exceptionDescription):
                returnValue = True
                break
        return returnValue
        
    def _parseResponse(self):
        self._extractAcrRef()
        self._requestID = self._extractRequestID()
        self._status = self._extractStatus()

        if self._status == 'Fail':
            self._exceptionOccurred = True
            self._extractExceptionInfo()
        else:
            self._exceptionOccurred = False
            action = self._extractAction()
            if action == 'DEAL.AVAILABILITY':
                self._extractAvailabilityInfo()
            else:
                self._extractDealInfo()
                
            try:
                self._extractGraphData()
            except:
                print("Error extracting graph data ")
                traceback.print_exc()

    def _extractRequestID(self):
        path = './/{0}RequestID'.format(self._nameSpace)
        return self._encodeText(self._responseTree.find(path).text)

    def _extractStatus(self):
        path = './/{0}Status'.format(self._nameSpace)
        return self._getSimpleValue(self._responseTree, path)
    
    def _extractAction(self):
        path = './/{0}Action'.format(self._nameSpace)
        return self._getSimpleValue(self._responseTree, path)

    def _extractExceptionDescription(self):
        path = './/{0}Result/{0}Exception/{0}ExceptionHeader/{0}Description'.format(self._nameSpace)
        return self._getSimpleValue(self._responseTree, path)
    
    def _extractExceptionSeverity(self):
        path = './/{0}Result/{0}Exception/{0}ExceptionHeader/{0}Severity'.format(self._nameSpace)
        return self._getSimpleValue(self._responseTree, path)
    
    def _extractAvailabilityInfo(self):
        self._availabilityOk = self._extractAvailabilityOk()
        self._headline = self._getSimpleValue(self._responseTree, './/{0}HEADLINE'.format(self._nameSpace))
        showBand2 = False
        showBand3 = False
        showBand4 = False
        self._counterparty = self._getSimpleValue(self._responseTree, './/{0}CUSTOMER'.format(self._nameSpace))
        
        availRows = self._responseTree.findall('.//{0}ROW'.format(self._nameSpace))
        for row in availRows:
            minValue       = self._encodeText(row.find('{0}MIN'.format(self._nameSpace)).text)
            nominalValue   = self._encodeText(row.find('{0}NOMINAL'.format(self._nameSpace)).text)
            limitAtDate    = self._encodeText(row.find('{0}LIMITATDATE'.format(self._nameSpace)).text)
            exposureAtDate = self._encodeText(row.find('{0}EXPOSUREATDATE'.format(self._nameSpace)).text)

            showBand2 = showBand2 or self._isValue(minValue) or self._isValue(nominalValue)
            showBand3 = showBand3 or self._isValue(limitAtDate) or self._isValue(exposureAtDate)
            
            if showBand2 and showBand3:
                break
        
        date1 = self._getSimpleValue(self._responseTree, './/{0}DATE1'.format(self._nameSpace))
        date2 = self._getSimpleValue(self._responseTree, './/{0}DATE2'.format(self._nameSpace))
        date4 = self._getSimpleValue(self._responseTree, './/{0}DATE4'.format(self._nameSpace))
        date5 = self._getSimpleValue(self._responseTree, './/{0}DATE5'.format(self._nameSpace))
        showBand4 = date1 or date2 or date4 or date5
        
        availViolations, severityZeroViolations = self._buildAvailViolations()
                
        if availViolations:
            self._availViolations = availViolations
            self._columnGroups = []
            
        availContents = self._buildAvailContents(showBand2, showBand3, showBand4)
        if availContents:
            self._availContents = availContents
            self._columnGroups = self._buildAvailabilityColumnGroups(showBand2, showBand3, showBand4)

        self._zeroViolations = severityZeroViolations
            
    def _buildAvailabilityColumnGroups(self, showBand2, showBand3, showBand4):
        columnGroups = []
        columnGroups.append(('', 1))
        
        primScaling = self._getSimpleValue(self._responseTree, './/{0}PRIMSCALINGATTR'.format(self._nameSpace))
        columnGroups.append(('Deal Size (' + primScaling + ')', 2))
        
        if showBand2:
            columnGroups.append(('Existing Excess', 2))
        if showBand3:
            preDealCurr = self._getSimpleValue(self._responseTree, './/{0}ROW/{0}CURRENCY'.format(self._nameSpace), True)
            columnGroups.append(('Pre-Deal (' + preDealCurr + ')', 2))
        if showBand4:
            columnGroups.append(('Settlement +/- 2 working days', 4))
            
        return columnGroups
    
    def _buildAvailContentsHeader(self, showBand2, showBand3, showBand4):
        header = []
        header.append('Limit')
        header.append('Maximum')
        header.append('Min Avail On')
        
        if showBand2:
            header.append('Minimum')
            header.append('Optimal')
        if showBand3:
            header.append('Limit')
            header.append('Exposure')
        if showBand4:
            date1 = self._getSimpleValue(self._responseTree, './/{0}DATE1'.format(self._nameSpace))
            date2 = self._getSimpleValue(self._responseTree, './/{0}DATE2'.format(self._nameSpace))
            date4 = self._getSimpleValue(self._responseTree, './/{0}DATE4'.format(self._nameSpace))
            date5 = self._getSimpleValue(self._responseTree, './/{0}DATE5'.format(self._nameSpace))
            header.append(date1)
            header.append(date2)
            header.append(date4)
            header.append(date5)
        
        return header
    
    def _buildAvailContents(self, showBand2, showBand3, showBand4):
        toReturn = []
        header = self._buildAvailContentsHeader(showBand2, showBand3, showBand4)
        table = []
        

        availSections = self._responseTree.findall('.//{0}SECTION'.format(self._nameSpace))

        for availSection in availSections:
            sectionTableRow = []
            sectionLegend = self._encodeText(availSection.find('{0}LEGEND'.format(self._nameSpace)).text)
            sectionTableRow.append(sectionLegend)
            sectionTableRow.append('')
            sectionTableRow.append('')
            
            if showBand2:
                sectionTableRow.append('')
                sectionTableRow.append('')
            if showBand3:
                sectionTableRow.append('')
                sectionTableRow.append('')
            if showBand4:
                sectionTableRow.append('')
                sectionTableRow.append('')
                sectionTableRow.append('')
                sectionTableRow.append('')
            table.append(sectionTableRow)
            legendChildren = []

            availRows = availSection.findall('.//{0}ROW'.format(self._nameSpace))
            for availRow in availRows:
                availTableRow = []
                legend = self._encodeText(availRow.find('{0}LEGEND'.format(self._nameSpace)).text)
                availTableRow.append(legend)

                maxValue       = self._encodeText(availRow.find('{0}MAX'.format(self._nameSpace)).text)
                excessDate     = self._encodeText(availRow.find('{0}EXCESSDATE'.format(self._nameSpace)).text)
                availTableRow.append(maxValue)
                availTableRow.append(excessDate)
                
                if showBand2:
                    minValue       = self._encodeText(availRow.find('{0}MIN'.format(self._nameSpace)).text)
                    nominalValue   = self._encodeText(availRow.find('{0}NOMINAL'.format(self._nameSpace)).text)
                    availTableRow.append(minValue)
                    availTableRow.append(nominalValue)
                if showBand3:
                    limitAtDate    = self._encodeText(availRow.find('{0}LIMITATDATE'.format(self._nameSpace)).text)
                    exposureAtDate = self._encodeText(availRow.find('{0}EXPOSUREATDATE'.format(self._nameSpace)).text)
                    availTableRow.append(limitAtDate)
                    availTableRow.append(exposureAtDate)
                if showBand4:
                    dPlus1         = self._getSimpleValue(availRow, './/{0}DPLUS1'.format(self._nameSpace))
                    dPlus2         = self._getSimpleValue(availRow, './/{0}DPLUS2'.format(self._nameSpace))
                    dMinus1        = self._getSimpleValue(availRow, './/{0}DMINUS1'.format(self._nameSpace))
                    dMinus2        = self._getSimpleValue(availRow, './/{0}DMINUS2'.format(self._nameSpace))
                    availTableRow.append(dPlus1)
                    availTableRow.append(dPlus2)
                    availTableRow.append(dMinus1)
                    availTableRow.append(dMinus2)
                    
                legendChildren.append(availTableRow)
            sectionTableRow.append(legendChildren)
        
        if table:
            toReturn.append(header)
            toReturn += table
            
        return toReturn
    
    def _extractAvailabilityOk(self):
        toReturn = False
        if (len(self._responseTree.findall('.//{0}VIOLATIONBANNER'.format(self._nameSpace))) > 0):
                banner = self._getSimpleValue(self._responseTree, './/{0}VIOLATIONBANNER'.format(self._nameSpace), True)
                toReturn = banner == 'Deal Acceptable'
        elif (len(self._responseTree.findall('.//{0}AVAILABILITY/{0}HEADLINE'.format(self._nameSpace))) > 0):
            banner = self._getSimpleValue(self._responseTree, './/{0}AVAILABILITY/{0}HEADLINE'.format(self._nameSpace), True)
            # Only the beginning is checked to allow workaround to DGEN066158,
            # where the headline may contain additional warnings.
            # This workaround applies only to availability checks            
            s = 'Unlimited Availability'
            toReturn = banner[:len(s)] == s
            
        severity = self._getSimpleValue(self._responseTree, './/{0}HEADLINESEVERITY'.format(self._nameSpace))
        if severity != '0':
            toReturn = False
        return toReturn
    
    def _buildAvailViolations(self):
        toReturn = []
        severityZeroViolations = ''
        
        availSections = self._responseTree.findall('.//{0}SECTION'.format(self._nameSpace))
        if len(availSections) > 0:
            violations = availSections[0].findall('.//{0}VIOLATION'.format(self._nameSpace))
            if violations:
                header = ['Severity', 'Description', 'Legend', 'Message']
                toReturn.append(header)
            
            for violation in violations:
                severity = self._getSimpleValue(violation, '{0}SEVERITY'.format(self._nameSpace))
                description = self._getSimpleValue(violation, '{0}BUILDDESC'.format(self._nameSpace))
                legend = self._getSimpleValue(violation, '{0}PORTFOLIOLEGEND'.format(self._nameSpace))
                message = self._getSimpleValue(violation, '{0}USERMESSAGE'.format(self._nameSpace))
                
                toReturn.append([severity, description, legend, message])
                
                if severity == '0':
                    severityZeroViolations += '\n' +  message

        return toReturn, severityZeroViolations 

    def _isValue(self, value):
        toReturn = False
        value  = value.lower()

        if ((len(value) > 0) and (value != 'unknown') and (value != 'unlimited') and (value != 'n/a')):
            toReturn = True

        return toReturn

    def _extractDealInfo(self):
        headerRow = ['Severity', 'Description', 'Legend', 'Message']
        tableMatrix = [headerRow]
        severityZeroViolations = ''
        maxViolationSeverity = 0
        
        violations = self._findAllViolations()
        for v in violations:
            self._registerViolation(v)
            severityPath = '{0}SEVERITY'.format(self._nameSpace)
            severity = self._getSimpleValue(v, severityPath)
            
            descriptionPath = '{0}BUILDDESC'.format(self._nameSpace)
            description = self._getSimpleValue(v, descriptionPath)
            
            legendPath = '{0}PORTFOLIOLEGEND'.format(self._nameSpace)
            legend = self._getSimpleValue(v, legendPath)
            
            msgPath = '{0}USERMESSAGE'.format(self._nameSpace)
            msg = self._getSimpleValue(v, msgPath)
            
            maxViolationSeverity = max(maxViolationSeverity, int(severity))
            if severity == '0':
                severityZeroViolations += '\n' +  msg
                
            tableMatrix.append([severity, description, legend, msg])
        
        if violations:
            self._violationContents = tableMatrix
        
        self._limitOk = self._extractLimitOk(maxViolationSeverity)
        
        if self._limitOk:
            self._headline = 'Deal Acceptable'
        else:
            self._headline = 'Deal Violates Credit Policy'
        
        self._zeroViolations = severityZeroViolations
        
    def _registerViolation(self, v):
        d = {}
        porIdPath = './/{0}PORTFOLIOID'.format(self._nameSpace)
        legendPath = './/{0}PORTFOLIOLEGEND'.format(self._nameSpace)
        measureIdPath = './/{0}MEASURECLASS'.format(self._nameSpace)
        
        d['PortfolioId'] = v.findtext(porIdPath)
        d['PortfolioLegend'] = v.findtext(legendPath)
        d['MeasureId'] = v.findtext(measureIdPath)
        
        self._violations.append(d)
    
    def _isLimitViolated(self, portfolioId, portfolioLegend, measureId):
        for v in self._violations:
            if v['PortfolioId'] == portfolioId and\
                    v['PortfolioLegend'] == portfolioLegend and\
                    v['MeasureId'] == measureId:
                return True
        return False
   
    def _extractLimitOk(self, maxViolationSeverity):
        limitOk = True
        
        if maxViolationSeverity > 0:
            limitOk = False
        else:
            violationBanners = self._violationBanners()
            if 'Deal Acceptable' not in violationBanners:
                limitOk = False
                
        return limitOk
        
    def _violationBanners(self):
        toReturn = []
        # namspace changes to nothing in ArML response
        path = './/{0}Messages/Message/DEALSERVERRESULT/VIOLATIONBANNER'.format(self._nameSpace)
        banners = self._responseTree.findall(path)
        
        path2 = './/{0}VIOLATIONBANNER'.format(self._nameSpace)
        banners2 = self._responseTree.findall(path2)
        
        allBanners = banners + banners2
        if allBanners:
            toReturn = [self._encodeText(b.text) for b in allBanners]
        
        return toReturn
    
    def _extractExceptionInfo(self):
        self._exceptionDescription = self._extractExceptionDescription()
        self._exceptionSeverity = self._extractExceptionSeverity()
        self._exceptions = self._extractAllExeptions()
        
        headerRow = ['Severity', 'Description', 'Attribute Name', 'Attribute Value']
        tableMatrix = [headerRow]
        
        for ex in self._exceptions:
            __, severity, description, name, value = ex
            tableMatrix.append([severity, description, name, value])
        
        if self._exceptions:
            self._headline = 'Attribute errors'
        else:
            self._headline = 'Technical error, please contact your administrator'
        
        self._exceptionContents = tableMatrix
        
    def _unpackException(self, exception):
        exceptionHeaderPath = './/{0}ExceptionHeader'.format(self._nameSpace)
        exceptionHeader = exception.find(exceptionHeaderPath)
        
        eTypePath = '{0}Type'.format(self._nameSpace)
        eType = self._getSimpleValue(exceptionHeader, eTypePath)
        
        severityPath = '{0}Severity'.format(self._nameSpace)
        severity = self._getSimpleValue(exceptionHeader, severityPath)
        
        descriptionPath = '{0}Description'.format(self._nameSpace)
        description = self._getSimpleValue(exceptionHeader, descriptionPath)
        
        attrName = ''
        attrValue = ''
        exceptionAttributes = exception.find('.//{0}ExceptionAttributes/{0}Attribute'.format(self._nameSpace))
        if exceptionAttributes:
            exAttrName = self._getSimpleValue(exceptionAttributes, '{0}Name'.format(self._nameSpace))
            if exAttrName == 'Attribute Name':
                attrName = self._getSimpleValue(exceptionAttributes, '{0}Value'.format(self._nameSpace))
            if exAttrName == 'Attribute Value':
                attrValue = self._getSimpleValue(exceptionAttributes, '{0}Value'.format(self._nameSpace))
        
        return eType, severity, description, attrName, attrValue
    
    def _extractAllExeptions(self):
        path = './/{0}Value/{0}Exception'.format(self._nameSpace)
        exceptions = self._responseTree.findall(path)
        
        if len(exceptions) > 0:
            return [self._unpackException(e) for e in exceptions]
        else:
            return [self._unpackException(self._findSimple(self._responseTree, './/{0}Result/{0}Exception'.format(self._nameSpace)))]
    
    def _buildDataPointsTable(self, xvalues, preDeal, deal, limit):  
        rows = []

        today = acm.Time().DateNow()
        dateYMD = acm.Time.DateToYMD(today)
        minCutoff = self._getFloatFromDate(dateYMD[0], dateYMD[1], dateYMD[2]) - 1
        maxCutoff = 2958465 
        
        prevDateString = None
        for n in xrange(len(deal)):
            dateFloat = float(xvalues[n])
            
            if dateFloat > minCutoff and dateFloat < maxCutoff:                
                dateString = self._getDateStringFromFloat(dateFloat)
                preDealString = '%0.3f' % preDeal[n]
                dealString = '%0.3f' % deal[n]
                effect = '%0.3f' % (deal[n] - preDeal[n])
                limitString = '%0.3f' % limit[n]

                row = [ dateString, preDealString, dealString, effect, limitString ]
                
                if prevDateString == dateString:
                    del rows[-1] # SPR 352557. ACR sometimes returns two points on the same date, we only want the last one
                rows.append(row)
                prevDateString = dateString
        
        return rows

    def _extractGraphData(self):
        self._graphData = {}
        path = './/{0}SNAPSHOT/{0}PORTFOLIOS/{0}PORTFOLIO'.format(self._nameSpace)
        portfolios = self._responseTree.findall(path)
        
        for port in portfolios:
            self._appendPortfolioToGraphData(port)

    def _appendPortfolioToGraphData(self, port):
        measuresPath = './/{0}MEASURES/{0}MEASURE'.format(self._nameSpace)
        portfolioNamePath = './/{0}PORTFOLIONAME'.format(self._nameSpace)
        portfolioIdPath = './/{0}PORTFOLIOID'.format(self._nameSpace)
        portfolioLegendPath = './/{0}PORTFOLIODEALLEGEND'.format(self._nameSpace)
        portfolioName = port.findtext(portfolioNamePath)
        portfolioId = port.findtext(portfolioIdPath)
        portfolioLegend = port.findtext(portfolioLegendPath)
        measures = port.findall(measuresPath)
        for measure in measures:
            self._appendMeasureToGraphData(measure, portfolioName, portfolioId, portfolioLegend)
            
    
    def _appendMeasureToGraphData(self, measure, portfolioName, portfolioId, portfolioLegend):
        pathName = './/{0}MEASURECLASSNAME'.format(self._nameSpace)
        pathMeasureId = './/{0}MEASUREID'.format(self._nameSpace)
        pathLimitProfilePoints = './/{0}LIMITPROFILEDATA/{0}PROFILE/{0}POINTS'.format(self._nameSpace)
        pathCurrency = './/{0}PROFILEDATA/{0}PROFILE/{0}CURRENCYCODE'.format(self._nameSpace)
        
        currency = measure.findtext(pathCurrency)
        points = measure.findall(pathLimitProfilePoints)
        if not points:
            return
        data = self._parsePointsData(self._encodeText(points[0].text))

        xvalues = []
        for i in xrange(len(data[0])):
            xvalues.append(data[0][i])
          
        #Quote from word document: Note for crsProfile : Each point is of the form: Date/Value/AltValue/Limit 
        limit   = data[3]
        preDeal = data[2]
        deal    = data[1]
        incDeal, decDeal = self._extractIncreaseAndDecreaseGraphs(preDeal, deal)
        
        series_yvalues = [ limit, preDeal, incDeal, decDeal ]
        rows = self._buildDataPointsTable(xvalues, preDeal, deal, limit)
        
        measureId = measure.findtext(pathMeasureId)
        measureName = measure.findtext(pathName)
        
        self._appendGraphData(portfolioName,\
                              portfolioLegend,\
                              measureName,\
                              measureId,\
                              rows,\
                              currency,\
                              xvalues,\
                              series_yvalues,
                              self._isLimitViolated(portfolioId, portfolioLegend, measureId))
    
    def _appendGraphData(self, portfolioName, portfolioLegend, measureName, measureId, rows, currency, xvalues, seriesyvalues, isLimitViolated):
        key = '%s_%s_%s_%s' % (portfolioName, portfolioLegend, measureName, measureId)
        name = '%s %s %s' % (portfolioName, measureName, portfolioLegend)
        self._graphData[key] = {   
                                'name' : name,
                                'rows' : rows,
                                'currency': currency,
                                'x_values' : xvalues,         
                                'y_series_values' : seriesyvalues,
                                'is_limit_violated' : isLimitViolated
                                }
        
    
    def _extractIncreaseAndDecreaseGraphs(self, preDeal, deal):
        incDeal = []
        decDeal = []
        
        for pointId in range(len(deal)):
            incDeal.append( max(preDeal[pointId], deal[pointId]) )
            decDeal.append( min(preDeal[pointId], deal[pointId]) )

        return incDeal, decDeal

    def _getFloatFromYear(self, year):
        base = datetime.date(1899,12,30)
        d = datetime.date(year + 1, 1, 1)
        return (d-base).days

    def _getFloatFromDate(self, year, month, day):
        base = datetime.date(1899,12,30)
        d = datetime.date(max(1, year), max(1, month), max(1, day))
        return (d-base).days
        
    def _getDateStringFromFloat(self, dateFloat):
        # This is correct for present dates but off by one day for year 1900
        # See these urls for explanation:
        # http://support.microsoft.com/default.aspx?scid=kb;en-us;214326
        # http://www.lexicon.net/sjmachin/xlrd.html
        base = datetime.date(1899,12,30)
        date = base + datetime.timedelta(days=round(dateFloat))
        dateStr = date.strftime("%Y-%m-%d")     
        return dateStr
        
    def _parsePointsData(self, points):
        rows = points.strip().split("\n")
        for i in xrange(len(rows)-1, -1, -1):        
            #Split row
            rows[i] = rows[i].split("/")            

            maxDate = 2958465 
            dateFloat = float(rows[i][0])
            if dateFloat >= maxDate: 
                # Adaptiv sometimes sends (9999-12-31 = 2958465) as the last point
                #  This causes an overflow in the code below and the "big" date ruins 
                #  the visual impression of the graph                
                # To work around these limitations, remove dates that are larger than maxDate
                rows.pop(i) 
                continue
            dateStr = self._getDateStringFromFloat(dateFloat)
            rows[i][0] = dateFloat
            rows[i].append(dateStr)
            def fix_value(num_str):
                f = float(num_str)
                # TODO: Workaround for 1e65 from Adaptive            
                if f < 1e20:
                    return f
                else:
                    return 0.0
                
            rows[i][1] = fix_value(rows[i][1])
            rows[i][2] = fix_value(rows[i][2])
            rows[i][3] = fix_value(rows[i][3])
        return map(list, list(zip(*rows))) #"transpose"    

    def _findAllViolations(self):
        path = './/{0}VIOLATION'.format(self._nameSpace)
        return self._responseTree.findall(path)

    def _getSimpleValue(self, tree, path, getFirstOfMany = False):
        res = self._findSimple(tree, path, getFirstOfMany)
        return self._encodeText(res.text) if res.text else ''

    def _findSimple(self, tree, path, getFirstOfMany = False):
        res = tree.findall(path)
        if len(res) != 1 and not getFirstOfMany:
            raise FACLArMLParseException('One match expected in XML ' + str(len(res)) + ' found. Path = ' + path)
        return res[0]

    def _extractAcrRef(self):
        ref = self._responseTree.findall('.//{0}DealHeader/{0}Ref'.format(self._nameSpace))
        if ref:
            if len(ref) != 1 : raise FACLArMLParseException('Only one ref element allowed')
            self._acr_ref = self._encodeText(ref[0].text)
            
    def _encodeText(self, text):
        if text:
            text = text.encode(encoding, 'ignore')
        return text

class FACLArMLResponseTextView:
    
    def __init__(self, response):
        details = ''
        if response.Counterparty():
            counterpartyHeader = 'Counterparty: ' + response.Counterparty()
            counterpartyHeader += '\n' + len(counterpartyHeader) *'-' + '\n\n'
            details += counterpartyHeader
        if response.AvailabilityViolationContents():
            violationsHeader = 'Potential Violations'
            violationsHeader +=  '\n' + '-'*len(violationsHeader) + '\n'
            details += violationsHeader
            details += self._makeTable(response.AvailabilityViolationContents()) + '\n'
        if response.AvailabilityContents():
            availabilityHeader = 'Availability Results'
            availabilityHeader += '\n' + '-'*len(availabilityHeader) + '\n'
            details += availabilityHeader
            details += self._makeTable(response.AvailabilityContents(), response.AvailabilityColumnGroups())
        if response.ViolationContents():
            details += self._makeTable(response.ViolationContents())
        if response.ExceptionContents():
            details += self._makeTable(response.ExceptionContents())
        self.details = details.strip()

    def Details(self):
        return self.details
    
    def __str__(self):
        return self.Details()
    
    def _flattenTree(self, tableMatrix):
        rows = []
        for row in tableMatrix:
            children = row[-1]   
            if type(children) == list:
                for child in children: 
                    child[0] = '  ' + child[0]
                rows.append(row[:-1])
                rows.extend(children)
            else:
                rows.append(row)
        return rows
    
    def _makeTable(self, tableMatrix, columnGroups = []):
        toReturn = ''
        tableMatrix = self._flattenTree(tableMatrix)
        numColums = len(tableMatrix[0])
        
        maxWidths = self._getColumnWidths(tableMatrix, columnGroups)
        
        if columnGroups:
            currColId = 0
            for group in columnGroups:
                width = 0
                for colId in range(currColId, currColId + group[1]):
                    width += maxWidths[colId]
                currColId += group[1]
                toReturn += group[0].ljust(width)
            toReturn += '\n'
        
        isLabelRow = True
        for row in tableMatrix:
            for colId in range(numColums):
                toReturn += row[colId].ljust(maxWidths[colId])
                
            toReturn += '\n'
            if isLabelRow:
                separator = '-' * sum(maxWidths)
                toReturn += separator + '\n'
                isLabelRow = False
        
        return toReturn
        
    def _getColumnWidths(self, tableMatrix, columnGroups = []):
        columSeparation = 3
        numColums = len(tableMatrix[0])
        
        maxWidths = []
        for colId in range(numColums):
            width = max([len(row[colId]) for row in tableMatrix])
            width += columSeparation
            maxWidths.append(width)
            
        currColId = 0
        for group in columnGroups:
            groupLabelLength = len(group[0]) + columSeparation
            groupWidth = 0
            for colId in range(currColId, currColId + group[1]):
                groupWidth += maxWidths[colId]
            currColId += group[1]
            if groupLabelLength > groupWidth:
                maxWidths[currColId - 1] += groupLabelLength - groupWidth

        return maxWidths

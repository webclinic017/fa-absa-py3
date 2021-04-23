import acm
import amb
import os
import platform
import time
from datetime import datetime
import hashlib
import DDM_ATS_PARAMS as params
import AMB_Reader_Writer as ambReaderWriter
import DDM_SQL_HELPER as sqlHelper
from datetime import datetime, date
from xml.etree.ElementTree import Element, tostring, fromstring
import zlib 
import base64
from FBDPCommon import is_acm_object

#Globals
platformName = platform.system()
processId = os.getpid()
productMapping = None


def deflate_and_base64_encode(input):
    zlibbed_str = zlib.compress(input)     
    compressed_string = zlibbed_str[2:-4]     
    return base64.b64encode(compressed_string)
    
    
def getProductMapping(sourceType1, sourceType2, sourceType3):
    global productMapping
    try:
        #Ignore type 2 at this point
        if not productMapping:
            resultRows = sqlHelper.callStoredProcWithCursor('DDMGetProductMappingsByTradeDomain', params.sourceSystem).fetchall()
            productMapping = acm.FDictionary()
            for row in resultRows:
                if row:
                   #key = '%s' %(row[0])
                    key = '%s%s' %(row[2], row[4])
                    productMainType = row[5]
                    productSubType = row[6]
                    productMapping[key] = (productMainType, productSubType)
        lookupKey = '%s%s' %(sourceType1, sourceType3)
        result = productMapping[lookupKey]
        if not result:
            return ('tactical', 'tactical')
        else:
            return result
        
    except Exception, error:
        raise Exception('Could not load the product mapping. %s' % str(error))
 
       
def calcLapsedTimeInSeconds(startDateTime, endDateTime):
    try:
        timeDiff = endDateTime-startDateTime
        totalSeconds =timeDiff.seconds
        totalMicroSeconds = timeDiff.microseconds / 1000000.0
        return float(totalSeconds +  totalMicroSeconds)
        
    except Exception, error:
        raise Exception('Could not calculate the lapsed time. %s' % str(error))

def getTradeIndexBatches(tradeCount):
    try:
        batches = acm.FList()  
        if tradeCount==0:
            batches.Add((0, 0))
        elif tradeCount <= params.batchTradeSize:
            batches.Add((0, tradeCount-1))
        else:
            i = 1
            startIndex=0
            endIndex = (i * params.batchTradeSize) - 1
            remainder=0
            while endIndex <= tradeCount-1:
                batches.Add((startIndex, endIndex))
                startIndex = endIndex + 1
                i = i + 1
                endIndex = (i * params.batchTradeSize) - 1
                
            
            #Get the remainder
            previousEndIndex = ((i-1) * params.batchTradeSize) - 1
            remainder = tradeCount - previousEndIndex
            if (remainder) > 0:
                startIndex = previousEndIndex + 1
                endIndex = tradeCount-1
                batches.Add((startIndex, tradeCount-1))
            
        return batches
            
    except Exception, error:
        raise Exception('Could not get the trade index batches. %s' % str(error))
        
                    
def getPortfolioTrades(portfolioNumber, portfolioName):
    try:
        #first fetch the porfolio
        portfolio = None
        try:
            if int(portfolioNumber)!= 0:
                portfolio = acm.FPhysicalPortfolio.Select01('oid=%i' % int(portfolioNumber), 'Portfolio not found')
            else:
                portfolio = acm.FPhysicalPortfolio.Select01("name='%s'" % str(portfolioName), 'Portfolio not found')
        except Exception, error:
            portfolio = None
        
        if not portfolio:
            return None
            
        
        portfolioTradeQuery="portfolio=%s and status<>'Void' and status<>'Simulated'" % str(portfolio.Oid())
        
        return acm.FTrade.Select(portfolioTradeQuery) 
    except Exception, error:
        raise Exception('Could not get the portfolio trades. %s' % str(error))


def getInstrumentTrades(instrumentAddress, instrumentName):
    try:
        #Get by address
        instrument = acm.FInstrument[instrumentAddress]
        if not instrument and instrumentName!='':
            #Try get by name
            instrument = acm.FInstrument[instrumentName]
        if not instrument:
            return None
        
        instrumentTradeQuery="instrument='%s' and status<>'Void' and status<>'Simulated'" %(str(instrument.Oid()))
        return acm.FTrade.Select(instrumentTradeQuery)
    except Exception, error:
        raise Exception('Could not get the instrument trades. %s' % str(error))
            

def calcSHA512(input):
    sha = hashlib.sha512()
    sha.update(input)
    return sha.hexdigest()

def isoDateTimeFromInt(input):
    if not input:
        return ''
    return datetime.fromtimestamp(input).isoformat()  

def dateFromDateTimeString(input):
    if not input:
        return ''
    return datetime.strptime(input, '%Y-%m-%d %H:%M:%S').isoformat()
    
def formatNumber(input):
    if bool(type(input)==float):
        return params.decimalFormat.format(float(input))
    elif bool(type(input)==int):
        return int(input)
    else:
        return str(input)
    
#returns the current process's virtual memory usage
def getVirtualMemory():
    global platformName
    if platformName=='Windows':
        return int(acm.Memory().VirtualMemorySize()) / 1024.0
    elif platformName=='Linux':
        return os.popen('ps -p %d -o %s | tail -1' %(processId, 'vsz')).read()
    else:
        return 0

#Add an xml child element to a parent
def AddXmlChildElement(parent, elementName, elementValue):
    childTag = Element(elementName)
    childTag.text = elementValue
    parent.append(childTag)
    return childTag

#Get the custom defined label for a worksheet column
def getSheetColumnCustomLabel(sheet, columnId):
    sheetContents = sheet.Contents()
    for key in sheetContents.Keys():
        if key.Text() == 'columnsettings':
            for key1 in sheetContents[key].Keys():
                checkValue = key1.Text().split('-')[0].strip()
                if checkValue == columnId.Text():
                    for key2 in sheetContents[key][key1].Keys():
                        if key2.Text() == 'customLabel':
                            return sheetContents[key][key1][key2].Text()
                            
#Get a dictionary of [customLabel,column] for a given  sheet
def getSheetColumns(sheet):
    try:
        sheetColumns = acm.FDictionary()
        columns = sheet.ColumnCollection(acm.FColumnCreatorCreateContext())
        if columns and len(columns)>0:
            for column in columns:
                columnLabel = getSheetColumnCustomLabel(sheet, column.ColumnId())
                sheetColumns[columnLabel] = column
        else:
            print 'The sheet %s contains no columns' % sheet.SheetName()
            
        return sheetColumns
    except Exception, error:
            raise Exception('Could not load the columns for sheet %s.  %s' % (sheet.SheetName(), str(error)))
                        
#Get a trading manager sheet for a give workbook name
def getWorkbookSheet(workbookName, sheetName):
   
    try:
        sheet=None
        workbook = acm.FWorkbook[workbookName]
        if not workbook:
            raise Exception('Could not load the workbook %s' % str(workbookName))
        else:
            for workbookSheet in workbook.Sheets():
                if workbookSheet.SheetName() == sheetName:
                    sheet = workbookSheet
            if not sheet:
                raise Exception('Sheet not found - %s' % str(sheetName))
        return sheet
       
    except Exception, error:
        raise Exception('Could not load the workbook sheet. %s' % str(error))

#Gets a sheet column value for a given object
def getColumnValue(calcSpace, object, column):
    try:
        columnValue = None
        try:
            try:
                columnValue = calcSpace.CalculateValue(object, column.ColumnId())
                #print 'calc %s-%s' % (column.ColumnId(),str(columnValue))
            except:
                columnValue = column.GetValueForObj(object, None)
        except:
            columnValue = None
            
            
        #decide what value to return
        if not columnValue:
            return ''
        else:
            try:
                value = columnValue.Value()
                try:
                    return value.Number()
                except:
                    if is_acm_object(value) and (value.IsKindOf(acm.FCounterParty()) or value.IsKindOf(acm.FClient())):
                        return value.Name()
                    else:
                        return value
            except:
                return columnValue

    except Exception, error:
        raise Exception('Could not get the column value for column %s. %s' % (str(error), str(column.ColumnId())))
        
#Returns a collection of key/value pairs using tradeingManaget sheet columns for a given object
def getSheetColumnValues(calcSpace, columns, objectToCalc):
        try:
            if not objectToCalc:
                raise Exception('Invalid object passed')
            if not calcSpace:
                raise Exception('No calculation space passed')
            if not columns:
                raise Exception('No sheet columns passed')
            
            attributes = acm.FDictionary()    
            for key in columns.Keys():
                columnValue = None
                column = columns[key]
                try:
                    columnValue = getColumnValue(calcSpace, objectToCalc, column)
                except Exception, error:
                    columnValue = ''

                if columnValue:
                    attributes[str(key)] = str(formatNumber(columnValue))
                
            return attributes
        except Exception, error:
            raise Exception('Could not get the calculated attributes. %s' % str(error))
        
#Adds a collection of key/value pairs as child elements to a parent xml element
def addAttributesToElement(element, attributes):
    for attName in attributes.Keys():
        if attributes[attName]:
            AddXmlChildElement(element, str(attName), str(attributes[attName]))
            
def createSubscriptionEvent(atsName, eventType, requestId):
    try:
        element = Element('SubscriptionEvent')
        AddXmlChildElement(element, 'EventDateTime', str(datetime.now().isoformat()))
        AddXmlChildElement(element, 'EventSource', str(atsName))
        AddXmlChildElement(element, 'EventType', str(eventType))
        AddXmlChildElement(element, 'ReferenceId', str(requestId))
        AddXmlChildElement(element, 'TradeDomain', str(params.sourceSystem))
        return tostring(element)
    except Exception, error:
        raise Exception('Could create the subscription event. %s' % str(error))

#gets a collections of trades and their legs from a given xml report
def getTradesLegCollection(legReport):
    try:
        #This crawls a xml structure TRADES/TRADE/INSTRUMENT/LEGS/LEG and add the parent LEGS element for each trade to a dictionary
        tradesLegCollection = acm.FDictionary()
        if legReport:
            rootElement = fromstring(legReport)
            for tradesElement in rootElement:
                for tradeElement in tradesElement:
                    tradeNumberElement = tradeElement.find('tradeNumber')
                    tradeNumber = int(tradeNumberElement.text.replace(',', ''))
                    instrumentElement = tradeElement.find('instrument')
                    #Grab the legs element
                    legsElement = instrumentElement.find('legs')
                    #Add the trade number as key and legs xml as value to the dictionary
                    tradesLegCollection[tradeNumber] = tostring(legsElement)
                    
        return tradesLegCollection
    except Exception, error:
        raise Exception('Could get the trades leg collection. %s' % str(error))

#gets a collections of legs from a given xml report 
def getLegsCollection(legReport):
    try:
        #This crawls a xml structure LEGS/LEG and add each leg element to a dictionary
        legCollection = acm.FDictionary()
        if legReport:
            rootElement = fromstring(legReport)
            for legElement in rootElement:
                legNumberElement = legElement.find('legNumber')
                legNumber = int(legNumberElement.text.replace(',', ''))
                legCollection[legNumber] = tostring(legElement)
        return legCollection
    except Exception, error:
        raise Exception('Could get the trades leg collection. %s' % str(error))

      
#*************************************************************************************************************************
#Extension AMB Writer class found in the AMB_Reader_Writer module
#*************************************************************************************************************************
class AMB_WriterExtension(ambReaderWriter.AMB_Writer):
    
    def post_Message_To_AMB_Raw(self, message, subject):
        try:
            
            queue_write_error = amb.mb_queue_write(self._channel,
                                            subject,
                                            message,
                                            len(message),
                                            'status_buf')
                                
            if queue_write_error:
                raise Exception('mb_queue_write failed with error %s' % str(queue_write_error))
        except Exception, error:
            raise Exception('Could not write the message to the AMB. %s' % str(error))

#*************************************************************************************************************************

'''
portfolio = acm.FPhysicalPortfolio['Kenya Equities']
print portfolio.Oid(), portfolio.Name()
trades = getPortfolioTrades(0,  portfolio.Name())

print len(trades)
'''

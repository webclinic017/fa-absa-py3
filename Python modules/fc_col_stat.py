from datetime import datetime, date
from xml.etree.ElementTree import Element, tostring, fromstring
import acm, ael, traceback, locale, re, at, at_time, time
import traceback
import sys
aaa = {}


ael_variables = [
                   ['tradeList', 'Trade Numbers_Check', acm.FTrade, '', '', 0, 1, 'SINGLE_TRADE requests will be send for the trades selected.', None, 1],
                   ['columnList', 'Columns_Check', 'string', None, '', 0, 0, 'List of columns to check.', None, 1],
                ]
colList = []
class FC_DATA_STL():

    def __init__(self, settlementNumber):
        #find the settlement
        settlement = acm.FSettlement[settlementNumber]
        if not settlement:
            #raise Exception('STL_NOT_FOUND')
            print 'STL_NOT_FOUND'
            self._fSettlement = None
        else:
            self._fSettlement = settlement

        #reset all the inner data containers
        self._data = None
        self._serializedData = None
        self._calculationErrors = {}

        #performanceCounters
        self._settlementBuildTime = 0

    
    #Properties
    
    #FSettlement
    @property
    def FSettlement(self):
        return self._fSettlement

    #Data
    @property
    def Data(self):
        return self._data

    @Data.setter
    def Data(self, value):
        self._data = value

    @property
    def DataCount(self):
        if self.Data:
            return 1
        else:
            return 0

    #SerializedData
    @property
    def SerializedData(self):
        return self._serializedData

    #SettlementBuildTime
    @property
    def SettlementBuildTime(self):
        return self._settlementBuildTime

    #CalculationErrors
    @property
    def CalculationErrors(self):
        return self._calculationErrors
    
    #Methods
    
    def Calculate(self):
        self.calcStatic()

    def Serialize(self):
        self._serializedData = SerializeSettlement(self)
    
    def calcStatic(self):
        if self.Data:
            try:
                if (self._fSettlement != None):
                    self.Data.Calculate()
                    #Special step to add the settlement domain to the calculation results
                    self.Data.CalculationResults['tradeDomain'] = 'Frontarena'
            except Exception, e:
                raise Exception(str(e))

class FC_DATA_STL_BUILDER():
    
    #Constructor
    def __init__(self, settlementNumber):
        self._innerSettlement = FC_DATA_STL(settlementNumber)

    #Fields
    _innerSettlement = None
    
    #Methods
    #Create the trade static data
    def CreateData(self):
        if not self._innerSettlement:
            raise Exception('INNER_STL_CONTAINER_DNE')
        else:
            self._innerSettlement.Data = FC_DATA_STL_DATA(self._innerSettlement.FSettlement)

        return self

    #Calls calculate on the inner trade container and return the container
    def CalculateAndBuild(self):
        if not self._innerSettlement:
            raise Exception('INNER_STL_CONTAINER_DNE')
        else:
            startTime = datetime.now()
            self._innerSettlement.Calculate()
            endTime = datetime.now()
            self._innerSettlement.SettlementBuildTime = getElapsedTimeInSeconds(startTime, endTime)
            return self._innerSettlement

class FC_CALCULATION_SPACE():

    def __init__(self, context, worksheet, clearItemThreshold):
        self._clearItemThreshold = clearItemThreshold
        self._itemCount = 0
        self._innerCalcSpace = None

        #check the worksheet instance
        if not worksheet:
            raise Exception('VALID_INSTANCE_OF_WORKBOOK_SHEET_MUST_BE_PROVIDED')

        #Construct and clear the inner calcSpace
        if worksheet.IsKindOf('FTradeSheet'):
            self._innerCalcSpace = acm.Calculations().CreateCalculationSpace(context, 'FTradeSheet')
        elif worksheet.IsKindOf('FPortfolioSheet'):
            self._innerCalcSpace = acm.Calculations().CreateCalculationSpace(context, 'FPortfolioSheet')
        elif worksheet.IsKindOf('FMoneyFlowSheet'):
            self._innerCalcSpace = acm.Calculations().CreateCalculationSpace(context, 'FMoneyFlowSheet')
        elif worksheet.IsKindOf('FSettlementSheet'):
            self._innerCalcSpace = acm.Calculations().CreateCalculationSpace(context, 'FSettlementSheet')
        else:
            raise Exception('WORKSHEETS_OF_TYPE_S_NOT_SUPPORTED')
        self._innerCalcSpace.Clear()
 
    #The ACM calculation space
    @property
    def InnerCalcSpace(self):
        return self._innerCalcSpace

    #Number of items inserted in the calc space
    @property
    def ItemCount(self):
        return self._itemCount

    #Get or set whether the threshold for clearing items in the calc space (-1 disables)
    @property
    def ClearItemThreshold(self):
        return self._clearItemThreshold

    @ClearItemThreshold.setter
    def ClearItemThreshold(self, value):
        self._clearItemThreshold = value
  
    #Methods
    
    #insert an fObject into the and return a top level node
    def InsertItem(self, fObject):
        #check the fObject instance
        if not fObject:
            raise Exception('VALID_FOBJECT_INSTANCE_MUST_BE_PROVIDED')
        elif not self._innerCalcSpace:
            raise Exception('INNER_CALC_SPACE_NOT_CREATED')
        else:
            #Clear the items in the calc space
            if self._clearItemThreshold > -1 and self._itemCount>=self._clearItemThreshold:
                self.Clear()

            #Now insert the item
            node =  self._innerCalcSpace.InsertItem(fObject)
            self._itemCount = self._itemCount + 1
            return node

    #forces the inner calc space to be cleared
    def Clear(self):
        if not self._innerCalcSpace:
            raise Exception('INNER_CALC_SPACE_NOT_CREATED')
        else:
            self._innerCalcSpace.Clear()
            self._itemCount = 0


    #forces the inner calc space to be refreshed
    def Refresh(self):
        if not self._innerCalcSpace:
            raise Exception('INNER_CALC_SPACE_NOT_CREATED')
        else:
            self._innerCalcSpace.Refresh()

    #apply global Trading Manager Simulation
    def SimulateGlobalValue(self, columnId, value):
        if not self._innerCalcSpace:
            raise Exception('INNER_CALC_SPACE_NOT_CREATED')
        else:
            self._innerCalcSpace.SimulateGlobalValue(columnId, value)

    #remove global Trading Manager Simulation
    def RemoveGlobalSimulation(self, columnId):
        if not self._innerCalcSpace:
            raise Exception('INNER_CALC_SPACE_NOT_CREATED')
        else:
            self._innerCalcSpace.RemoveGlobalSimulation(columnId)

    #remove Trading Manager Simulation
    def RemoveSimulation(self, fObject, columnId):
        if not self._innerCalcSpace:
            raise Exception('INNER_CALC_SPACE_NOT_CREATED')
        else:
            self._innerCalcSpace.RemoveSimulation(fObject, columnId)

class FC_CALCULATION_SINGLETON:
    instance = None
    worksheetColumns = None
    worksheetCalcSpaces = None
    worksheets = None
    columnCustomLabels = {}     
    colList = {'FC_TRADE_INSTRUMENTbarrier':0.0,
               'FC_TRADE_INSTRUMENTbarrierEnd':0.0,
               'FC_TRADE_INSTRUMENTbarrierMonitoring':0.0,
                'FC_TRADE_INSTRUMENTbarrierStart':0.0,
                'FC_TRADE_INSTRUMENTcommodityDeliverable':0.0,
                'FC_TRADE_INSTRUMENTcommodityDescription':0.0,
                'FC_TRADE_INSTRUMENTcommodityLabel':0.0,
                'FC_TRADE_INSTRUMENTcommoditySubAssets':0.0,
                'FC_TRADE_INSTRUMENTdigital':0.0,
                'FC_TRADE_INSTRUMENTdomesticCurrencyName':0.0,
                'FC_TRADE_INSTRUMENTdomesticCurrencyNumber':0.0,
                'FC_TRADE_INSTRUMENTdoubleBarrier':0.0,
                'FC_TRADE_INSTRUMENTexoticBarrierRebateOnExpiry':0.0,
                'FC_TRADE_INSTRUMENTexoticDigitalBarrierType':0.0,
                'FC_TRADE_INSTRUMENTexoticDoubleBarrier':0.0,
                'FC_TRADE_INSTRUMENTexoticRebateName':0.0,
                'FC_TRADE_INSTRUMENTexoticRebateNumber':0.0,
                'FC_TRADE_INSTRUMENTforeignCurrencyName':0.0,
                'FC_TRADE_INSTRUMENTforeignCurrencyNumber':0.0,
                'FC_TRADE_INSTRUMENTfxOptionType':0.0,
                'FC_TRADE_INSTRUMENTisExpired':0.0,
                'FC_TRADE_INSTRUMENTopenLinkUnit':0.0,
                'FC_TRADE_INSTRUMENTrebate':0.0,
                'FC_TRADE_INSTRUMENTstrikeCurrency':0.0,
                'FC_TRADE_INSTRUMENTfixingSourceName':0.0,
                'FC_TRADE_INSTRUMENTexoticOptionBaseType':0.0,
                'FC_TRADE_STATICsalesPersonNumber':0.0,
                'FC_TRADE_LEGendDate':0.0,
                'FC_TRADE_LEGfloatRate':0.0,
                'FC_TRADE_LEGrollingPeriodUnit':0.0,
                'FC_TRADE_LEGrollingPeriodCount':0.0,
                'FC_TRADE_MONEYFLOWendDate':0.0,
                'FC_TRADE_MONEYFLOWfixedRate':0.0,
                'FC_TRADE_MONEYFLOWstartDate':0.0,
                'FC_UNDERLYING_INSTRUMENTissuer':0.0}                


    class FC_CALCULATION_SINGLETON_HELPER:
        def __call__(self, *args, **kwargs):
            if FC_CALCULATION_SINGLETON.instance is None:
                object = FC_CALCULATION_SINGLETON()
                FC_CALCULATION_SINGLETON.instance = object
            return FC_CALCULATION_SINGLETON.instance

    Instance = FC_CALCULATION_SINGLETON_HELPER()

    #Singleton "private" constructor
    def __init__(self):
        if not FC_CALCULATION_SINGLETON.instance is None:
            raise RuntimeError, 'Only one instance of FC_CALCULATION_SINGLETON is allowed!'
        else:
            try:
                #create the column and calc space dictionaries
                self.worksheetColumns = acm.FDictionary()
                self.worksheetCalcSpaces = acm.FDictionary()
                self.worksheets = acm.FDictionary()

                #Load the workbook sheet columns
                startdate = datetime.now()
                self.LoadWorkbookSheetColumns()
                enddate = datetime.now()
                final = enddate - startdate                
            except Exception, e:
                raise Exception('Could not create the calculation singleton. %s' % str(e))

    def GetWorkBook(self, workBookName):
        if (workBookName == 'FC_DYNAMIC_DATA'):
            return acm.FWorkbook[workBookName]
        elif (workBookName == 'FC_OPERATIONS_DATA'):
            return acm.FBackOfficeManagerWorkbook[workBookName]

    def ColList(self):
        return self.colList

    def LoadWorkbookSheetColumns(self):
        #Load all the workbooks sheet columns into a dictionary with the sheetName as a the key
        workbookNames = ['FC_DYNAMIC_DATA'] # 'FC_OPERATIONS_DATA' - settlements 
        context = acm.GetDefaultContext()
        for workbookName in workbookNames:
            #load the workbook
            workbook = self.GetWorkBook(workbookName)
            if workbook==None:
                raise Exception('Could not load workbook %s' % workbookName)

            #grab each sheet from the workbook
            for worksheet in workbook.Sheets():
                sheetName = worksheet.SheetName()
                #Add all the worksheeets to the dictionary
                if self.worksheets.HasKey(sheetName):
                    raise Exception('WORKBOOKS_MUST_BE_UNIQUE')
                self.worksheets[sheetName] = worksheet

                #Fetch all the columns for the worksheet and add it to the dictionary
                if self.worksheetColumns.HasKey(sheetName):
                    raise Exception('WORKSHEETS_MUST_BE_UNIQUE')
                self.worksheetColumns[sheetName] = self.getWorksheetColumns(worksheet)

                #HM - replaced with the calc space wrapper
                if self.worksheetCalcSpaces.HasKey(sheetName):
                    raise Exception('WORKSPACE_WORKSHEETS_MUST_BE_UNIQUE')

                #Create the calculation space
                clearItemThreshold = 25 #possibly a config setting
                self.worksheetCalcSpaces[sheetName] = FC_CALCULATION_SPACE(context, worksheet, clearItemThreshold)


    #get the columns for a given work sheet
    def getWorksheetColumns(self, sheet):
        try:
            sheetColumns = acm.FDictionary()
            columns = sheet.ColumnCollection(acm.FColumnCreatorCreateContext())
            if columns and len(columns)>0:
                for column in columns:
                    columnLabel = self.getSheetColumnCustomLabel(sheet, column.ColumnId())
                    if columnLabel == None:
                        columnLabel = column.Label()
                    sheetColumns[columnLabel] = column
            else:
                print 'The sheet %s contains no columns' % sheet.SheetName()

            return sheetColumns

        except Exception, error:
                raise Exception('Could not load the columns for sheet %s.  %s' % (sheet.SheetName(), str(error)))

    #Get the custom defined label for a worksheet column
    def getSheetColumnCustomLabel(self, sheet, columnId):
        #if columnId in self.columnCustomLabels.keys():
        #    return self.columnCustomLabels[columnId]

        sheetContents = sheet.Contents() 
        for key in sheetContents.Keys():
            if key.Text() == 'columnsettings':
                for key1 in sheetContents[key].Keys():
                    checkValue = key1.Text().split('-')[0].strip()
                    if columnId.Text().__contains__('Vector'):
                        if columnId.Text().__contains__(checkValue):
                            for key2 in sheetContents[key][key1].Keys():
                                if key2.Text() == 'customLabel':   
                                    return sheetContents[key][key1][key2].Text()
                    else:
                        if checkValue == columnId.Text():
                            for key2 in sheetContents[key][key1].Keys():
                                if key2.Text() == 'customLabel':
                                    return sheetContents[key][key1][key2].Text()
       

    #Create a named parameter for the creation of a column config to calculate vector columns
    def createNamedParameter(self, vector, currencyName):
        param = acm.FNamedParameters();
        param.AddParameter('currency', acm.FCurrency[currencyName])
        vector.Add(param)

    #Set the column config for the calculation of vector columns
    def setColumnConfig(self, currencies):
        vector = acm.FArray()
        for currency in currencies:
            self.createNamedParameter(vector, currency)

        return acm.Sheet.Column().ConfigurationFromVector(vector)

    #Get the currencies from the vector column to create the column config
    def getVectorColumnCurrency(self, sheetName, columnId):
        sheet = self.worksheets[sheetName]
        if sheet:
            sheetContents = sheet.Contents()
            for key in sheetContents.Keys():
                if key.Text() == 'columnsettings':
                    for key1 in sheetContents[key].Keys():
                        checkValue = key1.Text().split('-')[0].strip()
                        if columnId.__contains__(checkValue):
                            columnContentList = key1.Text().split('-')
                            return [columnContentList[len(columnContentList)-1]]

    #Format the Portfolio Profit and Loss Date
    def _getNewPortfolioPLDate(self, date):
        diff = ael.date_today().days_between(date)
        newDate = ael.date_today().add_days(diff)
        return newDate

    #Set Global Simulation
    def SimulateGlobalValue(self, calcSpace, columnId, value):
        if not calcSpace:
            raise Exception('No calc space was provided to simulate the global value %s.' %columnId)
        else:
            calcSpace.SimulateGlobalValue(columnId, value)

    #Apply Global Simulation
    def ApplyGlobalSimulation(self, profitAndLossStartDate, profitAndLossEndDate, displayCurrency):
        for sheetName in self.worksheetCalcSpaces:
            simulateGlobalValue = self.worksheetCalcSpaces[sheetName].SimulateGlobalValue
            if profitAndLossStartDate:
                profitAndLossStartDate = ael.date(profitAndLossStartDate)
                simulateGlobalValue('Portfolio Profit Loss Start Date', 'Custom Date')
                simulateGlobalValue('Portfolio Profit Loss Start Date Custom', profitAndLossStartDate)
            if profitAndLossEndDate:
                profitAndLossEndDate = ael.date(profitAndLossEndDate)
                simulateGlobalValue('Portfolio Profit Loss End Date', 'Custom Date')
                simulateGlobalValue('Portfolio Profit Loss End Date Custom', profitAndLossEndDate)
                if sheetName == 'FC_UNDERLYING_INSTRUMENT':
                    simulateGlobalValue('Valuation Date', profitAndLossEndDate)
            if displayCurrency:
                simulateGlobalValue('Portfolio Currency', displayCurrency)

    #Remove Global Simulation
    def RemoveGlobalSimulation(self):
        for sheetName in self.worksheetCalcSpaces:
            removeGlobalSimulation = self.worksheetCalcSpaces[sheetName].RemoveGlobalSimulation
            removeGlobalSimulation('Portfolio Profit Loss Start Date')
            removeGlobalSimulation('Portfolio Profit Loss Start Date Custom')
            removeGlobalSimulation('Portfolio Profit Loss End Date')
            removeGlobalSimulation('Portfolio Profit Loss End Date Custom')
            removeGlobalSimulation('Valuation Date')

    #Remove Simulation
    def RemoveSimulation(self, fObject):
        for sheetName in self.worksheetCalcSpaces:
            self.worksheetCalcSpaces[sheetName].RemoveSimulation(fObject, 'Portfolio Currency')

    #Gets a sheet column value for a given object
    def calcColumnValue(self, calcSpace, acmFObject, acmTreeProxy, column, label, sheetName):
        columnValue = None
        result = ''
        list = []
        try:

            #o = open("c:/output.txt","a+")
            #o.write(label +'\n')
            #o.write('-----------------------------------------------------------------\n')
            #methodName = 'None'
            #extensionAttrib = 'None'
            if column.Method():
                columnValue = self.GetValueForObj(column, acmFObject)
                #methodName = str(column.Method())
                #if str(column.Method()) not in list:
                #    list.append(str(column.Method()))
                #    o.write('Method: ' +  str(column.Method()) +'\n')
                #    o.write('ExtensionAttribute: ' +  extensionAttrib +'\n')
            else:
                columnId = column.ColumnId().Text()

                extensionAttrib = column.ExtensionAttribute().Text()
                #o.write('Method: ' +  methodName +'\n')
                #o.write('ExtensionAttribute: ' +  extensionAttrib +'\n')

                if columnId.__contains__('Vector'):
                    columnId = columnId[:columnId.find('[0]')]
                    currencies = self.getVectorColumnCurrency(sheetName, columnId)
                    columnConfig = self.setColumnConfig(currencies)
                    columnValue = calcSpace.CreateCalculation(acmTreeProxy, columnId, columnConfig)
                else:
                    try: # TODO resolve error
                        columnValue = calcSpace.CreateCalculation(acmTreeProxy, column.ColumnId(), None)
                    except Exception, e:
                        print 'CreateCalculation ', str(e)
                        return None
            #    try:
            #        child = calcSpace.RowTreeIterator().FirstChild()
            #        row = child.Tree().Item()
            #        tag = acm.CreateEBTag()
            #        context = acm.GetDefaultContext()
            #        displayVal = acm.GetCalculatedValueFromString(row, context, extensionAttrib, tag) #extension attribute
                
            #        for ea in displayVal.ReferencedNodes():
            #            if '=' in str(ea):
            #                ea = str(ea).split('=')[0]
            #            if ea not in list:
            #                list.append(ea)
            #                o.write(str(ea) +'\n')
            #    except Exception, e:
            #        print str(e)
                    
            #o.write('-----------------------------------------------------------------\n\n')
            #o.close()
        except Exception, e:
            raise FormatException("Column calculation for column '%s' on %s object with id '%s' failed." % (column.ColumnId(), acmFObject.ClassName(), str(acmFObject.Oid())), e)
        
        #if columnValue != None and type(columnValue)=='FCalculation':
        #    result = columnValue.FormattedValue()
        #else:
        #    result = columnValue
        
        if columnValue != None:
            try:
                if str(type(columnValue))=="<type 'FCalculation'>" and columnValue.IsKindOf('FSymbol'): # FSymbol is wrapped string
                    return str(columnValue)
                result = self.formatColumValue(columnValue, column, label)
            except Exception, e:
                raise FormatException("Error during column value formating", e)
        return result

    def formatColumValue(self, value, column, label):
        formattedValue = None
        if value is None:
            return formattedValue
        
        if str(type(value))=="<type 'int'>":    # do not format ints
            return value
      
        columnFormatter = column.Formatter()
        
        try:
            formattedValue = value.FormattedValue()
            #print 'FormattedValue', formattedValue
        except:
            try:
                formattedValue = columnFormatter.Format(value)
                #print 'Format', formattedValue
            except:
                try:
                    formattedValue = value.Number()
                    #print 'Number', formattedValue
                except:
                    try:
                        formattedValue = value.Name()
                        #print 'Name', formattedValue
                    except:
                        formattedValue = value
        return formattedValue

    def checkMethod(self, obj, method):
        return hasattr(obj, method) and callable(getattr(obj, method))

        #alternative to using a calculation space, gets the column value for an object
    def GetValueForObj(self, column, object):
        if column.Method():
            methodchain = str(column.Method()).split('.')
            value = object
            for method in methodchain:
                try:                  
                    property = value.GetPropertyObject(method)                    
                    value = property.Value()                  
                    if value == None:
                        return None
                except Exception, e:
                    #print 'Except', method, str(e)
                    return None                
            return value
        else:
            raise Exception('no Method ')

    #alternative to using a calculation space, gets the column value for an object
    def GetValueForObja(self, column, object):
        if column.Method():
            methodchain = str(column.Method()).split('.')
            value = object
            for method in methodchain:
                try:                  
                    if self.checkMethod(value, method):
                        property = value.GetPropertyObject(method)
                        if self.checkMethod(property, 'Value'):
                            value = property.Value()                    
                    if value == None:
                        return None
                except Exception, e:
                    #print 'Except', method, str(e)
                    return None                
            return value
        else:
            raise Exception('no Method ')

    #Returns a collection of key/value pairs using trading manager sheet columns for a given object
    def calcWorksheetColumnValues(self, sheetName, acmFObject, acmTreeProxy):
        try:
            if not acmFObject or not acmTreeProxy:
                raise Exception('No object or tree proxy passed for calculation')

            #Fetch the columns for the sheet from the cached dictionary
            columns = self.worksheetColumns[sheetName]
            if not columns:
                raise  Exception('No worksheet columns found for sheet ' % sheetName)

            #Fetch the calculation space for the sheet from the cached dictionary
            calcSpace = self.worksheetCalcSpaces[sheetName]
            if not calcSpace:
                raise Exception('No calculation space found for sheet ' % sheetName)

            #Process the columns by calculating one by one and storing the results in a dictionary
            calcResults = {}
            calcErrors = []

            #if sheetName != 'FC_TRADE_STATIC':
            #    return calcResults,calcErrors

            x = 0.0
            for key in sorted(columns.Keys()):
                #print sheetName, key
                try:
                    columnValue = None
                    column = columns[key]
                    #HM - replaced to use calcSpace wrapper inner CalcSpace
                    startT = datetime.now()
                    columnValue = self.calcColumnValue(calcSpace.InnerCalcSpace, acmFObject, acmTreeProxy, column, key, sheetName)
                    endT = datetime.now()
                    customKey = "%s-%s" %(sheetName, key)
                    #if customKey in self.colList.keys():                                   
                    #    self.colList[customKey] += getElapsedTimeInMilliSeconds(startT,endT)
                    #    print key, self.colList[customKey]
                    if customKey in aaa.keys():
                        aaa[customKey] += getElapsedTimeInSeconds(startT, endT)
                    else:
                        aaa[customKey] = getElapsedTimeInSeconds(startT, endT)
                    #print key , getElapsedTimeInSeconds(startT,endT)
                    x += getElapsedTimeInSeconds(startT, endT)
                    #if columnValue or columnValue=='' or columnValue==0:
                    calcResults[str(key)] = columnValue    # to store only with values later
                    #print sheetName , key , columnValue, type(columnValue) 
                except Exception, e:
                    print '#ERROR', sheetName, key, e
                    calcErrors.append('%s[%s]: %s' % (sheetName, key, str(e)))
                    calcResults[key] = '#error#'
            #print sheetName, x       
            return calcResults, calcErrors
        except Exception, error:
            raise Exception('Could not get the calculated values for sheet %s. %s' % (sheetName, str(error)))

    #Clear all inner Calcspaces
    #def clearAllCalcSpaces(self):
    #    for sheetName in self.worksheetCalcSpaces:
    #        try:
    #            self.worksheetCalcSpaces[sheetName].Clear()
    #        except Exception, e:
    #            raise Exception('Worksheet %s could not be cleared due to the following error: %s.' %(sheetName, str(e)))

class FC_DATA_BASE():

    def __init__(self, worksheetName):
        self._worksheetName = None
        if not worksheetName or worksheetName=='':
            raise Exception('VALID_WS_MUST_BE_PROVIDED')
        else:
            self._worksheetName=worksheetName

        #Reset the fields
        self._fTreeProxy = None
        self._calculationResults=None
        self._calculationErrors=None

    #Properties
    
    #WorksheetName
    @property
    def WorksheetName(self):
        return self._worksheetName

    #WorksheetName
    @property
    def FTreeProxy(self):
        return self._fTreeProxy

    #CalculationResultscalcWorksheetColumnValues
    @property
    def CalculationResults(self):
        return self._calculationResults

    #CalculationErrors
    @property
    def CalculationErrors(self):
        return self._calculationErrors

    #Abstract methods for implementation in the sub classes
    def GetFObject(self):
        raise Exception('METHOD_GETFOBJECT_NOT_IMPLEMENTED')
        
    #Call the calculation singleton to calculate the column values
    def Calculate(self):
        if not self._worksheetName or self._worksheetName=='':
            raise Exception('WS_NAME_NOT_SET')
        elif not self._fTreeProxy:
            raise Exception('VALID_FTREEPROXY_MUST_BE_PROVIDED')
        else:
            fObject = self.GetFObject()
            if(fObject):
                (self._calculationResults, self._calculationErrors) = FC_CALCULATION_SINGLETON.Instance().calcWorksheetColumnValues(self._worksheetName, fObject, self._fTreeProxy)

class FC_DATA_STL_DATA(FC_DATA_BASE):
    #Properties
    #FSettlement - get from the fTree proxy to ensure the same object is used
    @property
    def FSettlement(self):
        return self.GetFObject()


    def __init__(self, settlement):
        worksheetName = 'FC_SETTLEMENT_DATA'
        if not settlement:
            #raise Exception('VALID_FSTL_INSTANCE_MUST_BE_PROVIDED')
            print 'VALID_FSTL_INSTANCE_MUST_BE_PROVIDED'
            FC_DATA_BASE.__init__(self, worksheetName)
        else:
            #Construct the base class
            FC_DATA_BASE.__init__(self, worksheetName)

            #Set the FTreeProxy - for settlement static this is the top row in the settlement worksheet
            self._fTreeProxy = GetTopLevelNodeTreeProxy(worksheetName, settlement)
    
    #Methods
    #GetFObject override
    def GetFObject(self):
        if self._fTreeProxy and self._fTreeProxy.Item() and self._fTreeProxy.Item().Settlement():
            return self._fTreeProxy.Item().Settlement()

class FC_DATA_TRD_STATIC(FC_DATA_BASE):
    
    #Properties
    
    #FTrade - get from the fTree proxy to ensure the same object is used
    @property
    def FTrade(self):
        return self.GetFObject()

    def __init__(self, trade):
        worksheetName = 'FC_TRADE_STATIC'
        if not trade:
            raise Exception('VALID_FTRADE_INSTANCE_MUST_BE_PROVIDED')
        else:
            #Construct the base class
            FC_DATA_BASE.__init__(self, worksheetName)

            #Set the FTreeProxy - for trade static this is the top row in the trade worksheet
            self._fTreeProxy = GetTopLevelNodeTreeProxy(worksheetName, trade)

    #Methods
    
    #GetFObject override
    def GetFObject(self):
        if self._fTreeProxy and self._fTreeProxy.Item() and self._fTreeProxy.Item().Trade():
            return self._fTreeProxy.Item().Trade()

class FC_DATA_TRD_SCALAR(FC_DATA_BASE):
    
    #Properties
    
    #FTrade - get from the fTree proxy to ensure the same object is used
    @property
    def FTrade(self):
        return self.GetFObject()

    def __init__(self, trade):
        worksheetName = 'FC_TRADE_SCALAR'
        if not trade:
            raise Exception('VALID_FTRADE_INSTANCE_MUST_BE_PROVIDED')
        else:
            #Construct the base class
            FC_DATA_BASE.__init__(self, worksheetName)

            #Set the FTreeProxy - for trade scalar this is the top row in the trade worksheet
            self._fTreeProxy = GetTopLevelNodeTreeProxy(worksheetName, trade)

    
    #Methods
    
    #GetFObject override
    def GetFObject(self):
        if self._fTreeProxy and self._fTreeProxy.Item() and self._fTreeProxy.Item().Trade():
            return self._fTreeProxy.Item().Trade()

class FC_DATA_TRD_INS(FC_DATA_BASE):
    
    #Properties
    
    #FInstrument - get from the fTree proxy to ensure the same object is used
    @property
    def FInstrument(self):
        return self.GetFObject()
    
    #Constructor
    
    def __init__(self, trade):
        worksheetName = 'FC_TRADE_INSTRUMENT'
        if not trade:
            raise Exception('VALID_FTRADE_INSTANCE_MUST_BE_PROVIDED')
        else:
            #Construct the base class
            FC_DATA_BASE.__init__(self, worksheetName)

            #Set the FTreeProxy - for trade instrument this is the second row (first child) in the portfolio worksheet
            self._fTreeProxy = GetTopLevelNodeTreeProxy(worksheetName, trade)
 
    #Methods
    
    #GetFObject override
    def GetFObject(self):
        if self._fTreeProxy and self._fTreeProxy.Item() and self._fTreeProxy.Item().Instrument():
            return self._fTreeProxy.Item().Instrument()

def CreateAllForTradeLeg(trade):
    worksheetName = 'FC_TRADE_LEG'
    if not trade:
        raise Exception('VALID_FTRADE_INSTANCE_MUST_BE_PROVIDED')
    tradeLegs = []
    #Get a leg count before attempting anything
    if trade.Instrument() and trade.Instrument().Legs():

        if len(trade.Instrument().Legs())>1:
            for legTreeProxy in GetTopLevelNodeChildrenTreeProxies(worksheetName, trade):
                tradeLeg = FC_DATA_TRD_LEG(worksheetName, trade.Instrument().Oid(), legTreeProxy, None)
                tradeLegs.append(tradeLeg)
        elif len(trade.Instrument().Legs())==1:
            legTreeProxy = GetTopLevelNodeTreeProxy(worksheetName, trade)
            tradeLeg = FC_DATA_TRD_LEG(worksheetName, trade.Instrument().Oid(), legTreeProxy, trade.Instrument().Legs()[0])
            tradeLegs.append(tradeLeg)

    return tradeLegs

class FC_DATA_TRD_LEG(FC_DATA_BASE):
    #FInstrument - get from the fTree proxy to ensure the same object is used
    fLeg = None
    @property
    def FLeg(self):
        return self.fLeg

    #InstrumentAddress - get from the fTree proxy to ensure the same object is used
    @property
    def InstrumentAddress(self):
        return self._instrumentAddress

    
    #Constructor
    
    def __init__(self, worksheetName, instrumentAddress, fLegTreeProxy, fLeg):
        self.fLeg = fLeg
        self._instrumentAddress = instrumentAddress
        #Construct the base class
        FC_DATA_BASE.__init__(self, worksheetName)

        #Get an FTreeProxy
        if not fLegTreeProxy:
            raise Exception('VALID_FLEGTREEPROXY_MUST_BE_PROVIDED')
        else:
            self._fTreeProxy = fLegTreeProxy

    #Methods
    
    #GetFObject override
    def GetFObject(self):
        try:
            if self._fTreeProxy and self._fTreeProxy.Item():
                if str(self._fTreeProxy.Item().ClassName())=='FTradeRow':
                    return self._fTreeProxy.Item()
                else:
                    if(self.fLeg==None):
                        self.fLeg = self._fTreeProxy.Item().Leg()
                    return self._fTreeProxy.Item().Leg()
        except:
            return None

#Static helper method to get all underlying/related instruments for an instrument
def GetRelatedInstruments(instrument, results):
    underlyingInstruments = []
    #Check reference on legs
    if instrument.Legs():
        for leg in instrument.Legs():
            if leg.CreditRef():
                underlyingInstruments.append(leg.CreditRef())
            if leg.IndexRef():
                underlyingInstruments.append(leg.IndexRef())
    #check combinations
    combination = acm.FCombination[instrument.Oid()]
    if combination:
        for underlying in combination.Instruments():
            underlyingInstruments.append(underlying)
    #check normal underlying
    if instrument.Underlying():
        underlyingInstruments.append(instrument.Underlying())

    if len(underlyingInstruments)>0:
        for underlyingInstrument in underlyingInstruments:
            results.append((instrument.Oid(), underlyingInstrument))
            results = GetRelatedInstruments(underlyingInstrument, results)
    return results

#*************************************************************************#
#Static Creator method for all related instruments of a trade (not use self)
#*************************************************************************#
def CreateAllForTradeIns(trade):
    worksheetName = 'FC_UNDERLYING_INSTRUMENT'
    if not trade:
        raise Exception('VALID_FTRADE_INSTANCE_MUST_BE_PROVIDED')
    #Return value - a collection of FC_DATA_TRD_INS_UND instances
    underlyingInstruments = []
    if trade.Instrument():
        relatedInstruments = []
        GetRelatedInstruments(trade.Instrument(), relatedInstruments)
        for relatedInstrument in relatedInstruments:
            parentInstrumentAddress = relatedInstrument[0]
            relatedInstrumentObject = relatedInstrument[1]
            #Create a tree proxy for each related instrument
            fInstrumentTreeProxy = GetFirstChildNodeTreeProxy('FC_UNDERLYING_INSTRUMENT', relatedInstrumentObject)
            #Now create and add the underlying instrument
            underlyingInstrument = FC_DATA_TRD_INS_UND(worksheetName, parentInstrumentAddress, fInstrumentTreeProxy)
            underlyingInstruments.append(underlyingInstrument)
    return underlyingInstruments

class FC_DATA_TRD_INS_UND(FC_DATA_BASE):
    #ParentInstrumentAddress
    @property
    def ParentInstrumentAddress(self):
        return self._parentInstrumentAddress

    #FUnderlyingInstrument - get from the fTree proxy to ensure the same object is used
    @property
    def FInstrument(self):
        return self.GetFObject()

    def __init__(self, worksheetName, parentInstrumentAddress, fInstrumentTreeProxy):
        self._parentInstrumentAddress = parentInstrumentAddress
        #Construct the base class
        #print worksheetName
        FC_DATA_BASE.__init__(self, worksheetName)        
        #Get an FTreeProxy
        if not fInstrumentTreeProxy:
            raise Exception('VALID_FINSTRTREEPROXY_MUST_BE_PROVIDED')
        else:
            self._fTreeProxy = fInstrumentTreeProxy

    #GetFObject override
    def GetFObject(self):
        if self._fTreeProxy and self._fTreeProxy.Item() and self._fTreeProxy.Item().Instrument():
            return self._fTreeProxy.Item().Instrument()

def CreateAllForTradeMF(reportDate, trade, historicalCashflowRange):
    worksheetName = 'FC_TRADE_MONEYFLOW'
    if not trade:
        raise Exception('VALID_FTRADE_INSTANCE_MUST_BE_PROVIDED')
    tradeMoneyflows = []
    moneyflowTreeProxys = GetTopLevelNodeChildrenTreeProxies(worksheetName, trade)
    for moneyflowTreeProxy in moneyflowTreeProxys:
        moneyflow = FC_DATA_TRD_MF(worksheetName, moneyflowTreeProxy)
        #cast the reportDate as a datetime
        reportDateTime = dateFromISODateTimeString(reportDate)
        #Current
        if moneyflow.PayDate == reportDateTime:
            moneyflow.PayDateType = 'C'
        #Historical
        elif moneyflow.PayDate < reportDateTime:
            moneyflow.PayDateType = 'H'
        #Future
        elif moneyflow.PayDate > reportDateTime:
            moneyflow.PayDateType = 'F'

        #Test historical cashflows for exclusion
        includeMoneyflow = True
        if historicalCashflowRange>-1:
            if moneyflow.SourceObject.IsKindOf('FCashFlow'):
                updateTime = dateTimeFromInt(moneyflow.SourceObject.UpdateTime())
                delta = reportDateTime - updateTime
                #Rule = exclude historical cashflows not updated more than inclusiveDays ago
                if moneyflow.PayDateType=='H' and delta.days > historicalCashflowRange:
                    includeMoneyflow = False

        #finally add the moneyflow
        if bool(includeMoneyflow):
            tradeMoneyflows.append(moneyflow)
    return tradeMoneyflows

class FC_DATA_TRD_MF(FC_DATA_BASE):
    #FMoneyflow - get from the fTree proxy to ensure the same object is used
    @property
    def FMoneyflow(self):
        return self.GetFObject()

    #PayDate
    @property
    def PayDate(self):
        if self.FMoneyflow:
            return datetime.strptime(self.FMoneyflow.PayDate(), '%Y-%m-%d')

    #PayDateType
    @property
    def PayDateType(self):
        return self._payDateType

    @PayDateType.setter
    def PayDateType(self, value):
        self._payDateType = value

    #SourceObject
    @property
    def SourceObject(self):
        if self.FMoneyflow:
            return self.FMoneyflow.SourceObject()

    #SourceObjectType
    @property
    def SourceObjectType(self):
        if self.SourceObject:
            return str(self.SourceObject.ClassName())

    #SourceObjectNumber
    @property
    def SourceObjectNumber(self):
        if self.SourceObject:
            #legNumber, cashflowNumber and reset number - dont like this...!!!!
            if self.FMoneyflow.SourceObject().IsKindOf('FCashFlow'):
                if self.FMoneyflow.SourceObject().Leg():
                    return self.FMoneyflow.SourceObject().Leg().Oid()
            elif self.FMoneyflow.SourceObject().IsKindOf('FReset'):
                if self.FMoneyflow.SourceObject().CashFlow():
                   return self.FMoneyflow.SourceObject().CashFlow().Oid()
                if self.FMoneyflow.SourceObject().Leg():
                   return self.FMoneyflow.SourceObject().CashFlow().Leg().Oid()
            elif self.FMoneyflow.SourceObject().IsKindOf('FMoneyFlow'):
                return  0
            elif self.FMoneyflow.SourceObject().IsKindOf('FTrade'):
                return  self.FMoneyflow.SourceObject().Oid()
            else:
                return  0
   
    #Constructor
    
    def __init__(self, worksheetName, fMoneyflowTreeProxy):
        #Construct the base class
        FC_DATA_BASE.__init__(self, worksheetName)


        #Get an FTreeProxy
        if not fMoneyflowTreeProxy:
            raise Exception('VALID_FMONEYF_TREEPROXY_MUST_BE_PROVIDED')
        else:
            self._fTreeProxy = fMoneyflowTreeProxy
    
    #Methods
    
    #GetFObject override
    def GetFObject(self):
        try:
            if self._fTreeProxy and self._fTreeProxy.Item() and self._fTreeProxy.Item().MoneyFlow():
                return self._fTreeProxy.Item().MoneyFlow()
        except:
            return None

def formatNumber(input):
    #global setting - do we want all number formatting the same?
    decimalFormat = '{0:0.08f}'
    
    type_desc = str(type(input))
    try:        
        if 'FDenominatedValue' in type_desc: 
            str_i = str(input)
            curr = ''.join([c for c in str_i if c.isupper()])            
            input = str(input).translate(None, curr).split('@')[0].split('[')[0].split('/')[0]
            try:            
                currencyFloat = float(input)
                currencyFloat = decimalFormat.format(currencyFloat)
                #print 'Float', currencyFloat
                return currencyFloat
            except:
                #print 'Except', input
                splt = str(input).split('@')
                if len(splt) > 0:                
                    input = splt[0].translate(None, letters).translate(None, '#/@(\([^)]*\)')    
        return locale.atoi(input)
    except:
        try:
            return decimalFormat.format(locale.atof(input))
        except:
            try:
                return decimalFormat.format(input)
            except:
                return str(input)

def CreateAllForTradeSC(trade):
    if not trade:
        raise Exception('VALID_FTRADE_INSTANCE_MUST_BE_PROVIDED')
    #no of sales credits
    noOfSalesCredits = 5
    #results list
    salesCredits = []
    #Grab the first (built-in) sales credit
    #if trade.SalesPerson() and trade.SalesCredit():
    salesPersonName = None
    standardSalesCredit=None
    totalValueAddSalesCredit=None
    salesCreditSubTeamName=None
    dataErrors={}
    #1st Sales person
    try:
        if trade.SalesPerson():
            salesPersonName = trade.SalesPerson().Name()
    except Exception, e:
        dataErrors['salesPerson'] = str(e)
    #1st Sales credit
    try:
        if trade.SalesCredit():
            standardSalesCredit = formatNumber(trade.SalesCredit())
        else:
            standardSalesCredit = formatNumber(0)
    except Exception, e:
        dataErrors['standardSalesCredit'] = str(e)
    #1st Value add sales credit
    try:
        totalValueAddAddInfo = trade.add_info('ValueAddCredits')
        if totalValueAddAddInfo and str(totalValueAddAddInfo)!='':
            totalValueAddSalesCredit = formatNumber(float(totalValueAddAddInfo))
        else:
            totalValueAddSalesCredit = formatNumber(0)
    except Exception, e:
        dataErrors['totalValueAddSalesCredit'] = str(e)
    #1st sales credit sub team
    try:
        salesCreditSubTeamAddInfo = trade.add_info('SalesCreditSubTeam1')
        if salesCreditSubTeamAddInfo and str(salesCreditSubTeamAddInfo)!='':
            salesCreditSubTeamName = salesCreditSubTeamAddInfo
    except Exception, e:
        dataErrors['salesCreditSubTeam'] = str(e)


    #Create the first sales credit
    salesCredit = FC_DATA_TRD_SC(salesPersonName, standardSalesCredit, totalValueAddSalesCredit, salesCreditSubTeamName, dataErrors)
    #Add the first sales credit entity to the collection
    salesCredits.append(salesCredit)

    #Now go for the remainder of the sales credits (all add infos)
    salesCreditNo = 2
    while salesCreditNo <= noOfSalesCredits:

        #grab sales person and standard sales credit add infos to see if the sales credit must be created
        salesPersonTest = trade.add_info('Sales_Person%s' % salesCreditNo)
        standardSalesCreditTest = trade.add_info('Sales_Credit%s' % salesCreditNo)
        if salesPersonTest and str(salesPersonTest)!='' and standardSalesCreditTest and str(standardSalesCreditTest)!='':
            salesPersonName = None
            standardSalesCredit=None
            totalValueAddSalesCredit=None
            salesCreditSubTeamName=None
            dataErrors={}
            #next Sales person
            try:
                salesPersonAddInfo = trade.add_info('Sales_Person%s' % salesCreditNo)
                if salesPersonAddInfo and str(salesPersonAddInfo)!='':
                    salesPersonName = salesPersonAddInfo
            except Exception, e:
                dataErrors['salesPerson'] = str(e)
            #next Sales credit
            try:
                standardSalesCreditAddInfo = trade.add_info('Sales_Credit%s' % salesCreditNo)
                if standardSalesCreditAddInfo and str(standardSalesCreditAddInfo)!='':
                    standardSalesCredit = formatNumber(float(standardSalesCreditAddInfo))
                else:
                    standardSalesCredit = formatNumber(0)
            except Exception, e:
                dataErrors['standardSalesCredit'] = str(e)
            #next Value add sales credit
            try:
                totalValueAddAddInfo = trade.add_info('ValueAddCredits%s' % salesCreditNo)
                if totalValueAddAddInfo and str(totalValueAddAddInfo)!='':
                    totalValueAddSalesCredit = formatNumber(float(totalValueAddAddInfo))
                else:
                    totalValueAddSalesCredit = formatNumber(0)
            except Exception, e:
                dataErrors['totalValueAddSalesCredit'] = str(e)
            #1st sales credit sub team
            try:
                salesCreditSubTeamAddInfo = trade.add_info('SalesCreditSubTeam%s' % salesCreditNo)
                if salesCreditSubTeamAddInfo and str(salesCreditSubTeamAddInfo)!='':
                    salesCreditSubTeamName = salesCreditSubTeamAddInfo
            except Exception, e:
                dataErrors['salesCreditSubTeam'] = str(e)


            #Create the next sales credit
            salesCredit = FC_DATA_TRD_SC(salesPersonName, standardSalesCredit, totalValueAddSalesCredit, salesCreditSubTeamName, dataErrors)
            #Add the next sales credit entity to the collection
            salesCredits.append(salesCredit)

            salesCreditNo = salesCreditNo + 1
        else:
            break
    return salesCredits

class FC_DATA_TRD_SC():
    #SalesPersonName
    @property
    def SalesPersonName(self):
        return self._salesPersonName

    @SalesPersonName.setter
    def SalesPersonName(self, value):
        self._salesPersonName = value

    #StandardSalesCredit
    @property
    def StandardSalesCredit(self):
        return self._standardSalesCredit

    @StandardSalesCredit.setter
    def StandardSalesCredit(self, value):
        self._standardSalesCredit = value

    #TotalValueAddSalesCredit
    @property
    def TotalValueAddSalesCredit(self):
        return self._totalValueAddSalesCredit

    @TotalValueAddSalesCredit.setter
    def TotalValueAddSalesCredit(self, value):
        self._totalValueAddSalesCredit = value

    #SalesCreditSubTeamName
    @property
    def SalesCreditSubTeamName(self):
        return self._salesCreditSubTeamName

    @SalesCreditSubTeamName.setter
    def SalesCreditSubTeamName(self, value):
        self._salesCreditSubTeamName = value

    #CalculationResults
    @property
    def CalculationResults(self):
        return self._calculationResults

    #CalculationErrors
    @property
    def CalculationErrors(self):
        return self._calculationErrors

    #Constructor
    
    def __init__(self, salesPersonName, standardSalesCredit, totalValueAddSalesCredit, salesCreditSubTeamName, calcErrors):
        self._salesPersonName = salesPersonName
        self._standardSalesCredit = standardSalesCredit
        self._totalValueAddSalesCredit = totalValueAddSalesCredit
        self._salesCreditSubTeamName = salesCreditSubTeamName
        self._calculationErrors = calcErrors
        self._calculationResults=None

    #Methods
    
    def Calculate(self):
        self._calculationResults = {}
        if self.SalesPersonName and self.SalesPersonName<>'':
            self._calculationResults['salesPersonName']=self.SalesPersonName
        if self.StandardSalesCredit and self.StandardSalesCredit<>'':
            self._calculationResults['standardSalesCredit']=self.StandardSalesCredit
        if self.TotalValueAddSalesCredit and self.TotalValueAddSalesCredit<>'':
            self._calculationResults['totalValueAddSalesCredit']=self.TotalValueAddSalesCredit
        if self.SalesCreditSubTeamName and self.SalesCreditSubTeamName<>'':
            self._calculationResults['salesCreditSubTeamName']=self.SalesCreditSubTeamName

class FC_DATA_TRD():
    
    #Constructor
    
    def __init__(self, tradeNumber):
        #find the trade
        trade = acm.FTrade[tradeNumber]
        if not trade:
            raise Exception('TRADE_S_NOT_FOUND')
        else:
            self._fTrade = trade

        #reset all the inner data containers
        self._static = None
        self._scalar = None
        self._instrument = None
        self._legs = None
        self._underlyingInstruments = None
        self._moneyflows = None
        self._salesCredits = None
        self._serializedData = None
        self._calculationErrors = []

        #performanceCounters
        self._tradeBuildTime = 0

    #Properties
    
    #FTrade
    @property
    def FTrade(self):
        return self._fTrade

    #Static
    @property
    def Static(self):
        return self._static

    @Static.setter
    def Static(self, value):
        self._static = value

    #Scalar
    @property
    def Scalar(self):
        return self._scalar

    @Scalar.setter
    def Scalar(self, value):
        self._scalar = value

    #Instrument
    @property
    def Instrument(self):
        return self._instrument

    @Instrument.setter
    def Instrument(self, value):
        self._instrument = value

    #Legs
    @property
    def Legs(self):
        return self._legs

    @Legs.setter
    def Legs(self, value):
        self._legs = value

    #UnderlyingInstruments
    @property
    def UnderlyingInstruments(self):
        return self._underlyingInstruments

    @UnderlyingInstruments.setter
    def UnderlyingInstruments(self, value):
        self._underlyingInstruments = value

    #Moneyflows
    @property
    def Moneyflows(self):
        return self._moneyflows

    @Moneyflows.setter
    def Moneyflows(self, value):
        self._moneyflows = value

     #SalesCredits
    @property
    def SalesCredits(self):
        return self._salesCredits

    @SalesCredits.setter
    def SalesCredits(self, value):
        self._salesCredits = value

    #SerializedData
    @property
    def SerializedData(self):
        return self._serializedData

    #TradeBuildTime
    @property
    def TradeBuildTime(self):
        return self._tradeBuildTime

    @TradeBuildTime.setter
    def TradeBuildTime(self, value):
        self._tradeBuildTime = value

    #CalculationErrors
    @property
    def CalculationErrors(self):
        return self._calculationErrors
    
    #Methods
    
    def Calculate(self):
        self.calcStatic()
        self.calcScalar()
        self.calcInstrument()
        self.calcLegs()
        self.calcUnderlyings()
        self.calcMoneyflows()
        self.calcSalesCredits()
  
    def Serialize(self):
        self._serializedData = tostring(GetTradeAsXml(self))
    
    def calcStatic(self):
        if self.Static:
            try:
                self.Static.Calculate()
                #Special step to add the trade domain to the calculation results
                self.Static.CalculationResults['tradeDomain'] = 'Frontarena'
                self.appendCalculationErrors(self.Static.CalculationErrors)
            except Exception, e:
                raise FormatException('Trade static calc error', e)

    def calcScalar(self):
        if self.Scalar:
            try:
                self.Scalar.Calculate()
                self.appendCalculationErrors(self.Scalar.CalculationErrors)
            except Exception, e:
                raise FormatException('Trade scalar calc error', e)

    def calcInstrument(self):
        if self.Instrument:
            try:
                self.Instrument.Calculate()
                self.appendCalculationErrors(self.Instrument.CalculationErrors)  
            except Exception, e:
                raise FormatException('Trade instrument calc error', e)

    def calcLegs(self):
        if self.Legs:
            for leg in self.Legs:
                try:
                    leg.Calculate()
                    self.appendCalculationErrors(leg.CalculationErrors)
                except Exception, e:
                    raise FormatException('Trade leg calc error', e)

    def calcUnderlyings(self):
        if self.UnderlyingInstruments:
            for underlyingInstrument in self.UnderlyingInstruments:
                try:
                    underlyingInstrument.Calculate()
                    #Special step to add the parent Instrument address property
                    underlyingInstrument.CalculationResults['parentInstrumentAddress'] = underlyingInstrument.ParentInstrumentAddress
                    self.appendCalculationErrors(underlyingInstrument.CalculationErrors)                    
                except Exception, e:
                    raise FormatException('Trade underlying instrument calc error', e)

    def calcMoneyflows(self):
        if self.Moneyflows:
            for moneyflow in self.Moneyflows:
                try:
                    moneyflow.Calculate()
                    self.appendCalculationErrors(moneyflow.CalculationErrors)
                except Exception, e:
                    raise FormatException('Trade moneyflow calc error', e)

    def calcSalesCredits(self):
        if self.SalesCredits:
            for salesCredit in self.SalesCredits:
                try:
                    salesCredit.Calculate()
                    self.appendCalculationErrors(salesCredit.CalculationErrors)
                except Exception, e:
                    raise FormatException('Trade sales credit calc error', e)

    def appendCalculationErrors(self, calculationErrors):
        if calculationErrors:
            for error in calculationErrors:
                self._calculationErrors.append(error)

class FC_DATA_TRD_BUILDER():

    #Fields
    _innerTrade = None

    #Constructor
    def __init__(self, tradeNumber):
        self._innerTrade = FC_DATA_TRD(tradeNumber)
        if not self._innerTrade:
            raise Exception('Trade %s not found' % tradeNumber)

    #Methods
    def CreateStatic(self):
        self._innerTrade.Static = FC_DATA_TRD_STATIC(self._innerTrade.FTrade)
        return self

    def CreateScalar(self):
        self._innerTrade.Scalar = FC_DATA_TRD_SCALAR(self._innerTrade.FTrade)
        return self

    def CreateInstrument(self):
        self._innerTrade.Instrument = FC_DATA_TRD_INS(self._innerTrade.FTrade)
        return self

    def CreateLegs(self):
        self._innerTrade.Legs = CreateAllForTradeLeg(self._innerTrade.FTrade)
        return self

    def CreateUnderlyingInstruments(self):
        self._innerTrade.UnderlyingInstruments = CreateAllForTradeIns(self._innerTrade.FTrade)
        return self

    #Create the trade moneyflow data
    #Historical cashFlowRange (days):
    #   -1: Include all
    #   0-n: Include only historical cashflows updated within this range
    def CreateMoneyflows(self, reportDate, historicalCashflowRange):
        self._innerTrade.Moneyflows = CreateAllForTradeMF(reportDate, self._innerTrade.FTrade, historicalCashflowRange)
        return self

    def CreateSalesCredits(self,):
        self._innerTrade.SalesCredits = CreateAllForTradeSC(self._innerTrade.FTrade)
        return self

    #Calls calculate on the inner trade container and return the container
    def CalculateAndBuild(self):
        startTime = datetime.now()
        self._innerTrade.Calculate()
        endTime = datetime.now()
        self._innerTrade.TradeBuildTime = getElapsedTimeInSeconds(startTime, endTime)
        #print 'Trade build time ', self._innerTrade.TradeBuildTime, ' seconds'
        return self._innerTrade

# Global methods

#Return the first child of a top level node as a TreeProxy
def GetFirstChildNodeTreeProxy(worksheetName, fObject):
    #Fetch the top level node
    node = GetTopLevelNodeTreeProxy(worksheetName, fObject)
    node.Expand(True)
    #Refresh the calc space
    FC_CALCULATION_SINGLETON.Instance().worksheetCalcSpaces[worksheetName].Refresh()
    #Now find the first child
    if node.NumberOfChildren():
        child_iterator = node.Iterator().FirstChild()
        node = child_iterator.Tree()
        if not node or not node.Item():
            raise Exception('NO_FIRST_CHILD_NODE_TREE_PROXY')
        return node

#Returns all the children of a top level node as TreeProxies
def GetTopLevelNodeChildrenTreeProxies(worksheetName, fObject):
    #Fetch the top level node
    try:
        node = GetTopLevelNodeTreeProxy(worksheetName, fObject)
        #Expand the node
        node.Expand(True)
        #Refresh the calc space
        FC_CALCULATION_SINGLETON.Instance().worksheetCalcSpaces[worksheetName].Refresh()
        #Now find the first child
        if node.NumberOfChildren():
            child_iterator = node.Iterator().FirstChild()
            while child_iterator:
                node = child_iterator.Tree()
                yield node
                child_iterator = child_iterator.NextSibling()
    except Exception, e:
        print str(e)

def GetTopLevelNodeTreeProxy(worksheetName, fObject):
    if not worksheetName or worksheetName=='':
        raise Exception('VALID_WS_MUST_BE_PROVIDED')
    calcSpace = FC_CALCULATION_SINGLETON.Instance().worksheetCalcSpaces[worksheetName];
    if calcSpace == None:
        raise Exception('Calculation space could not be found for worksheet')
    node = calcSpace.InsertItem(fObject)
    if not node or not node.Item():
       raise Exception('NO_TOP_LEVEL_NODE_TREE_PROXY')
    return node

def SerializeSettlement(settlement):    
    if not settlement:
        #raise Exception('FC_STL_DATA_INSTANCE_MUST_BE_PROVIDED')
        print 'FC_STL_DATA_INSTANCE_MUST_BE_PROVIDED'
    return tostring(GetSettlementAsXml(settlement))

def GetSettlementAsXml(settlement):
    settlementDataElement = Element('settlement')
    staticElement = GetItemXml('static', settlement.Data)
    settlementDataElement.append(staticElement)
    #scalarElement = GetItemXml('scalar',settlement.Scalar)
    #settlementDataElement.append(scalarElement)
    return settlementDataElement

def GetTradeAsXml(trade):
    tradeDataElement = Element('trade')
    #Data
    staticElement = GetItemXml('tradeStatic', trade.Static)
    tradeDataElement.append(staticElement)
    #Scalar
    scalarElement = GetItemXml('tradeScalar', trade.Scalar)
    tradeDataElement.append(scalarElement)
    #Instrument
    instrumentElement = GetItemXml('instrument', trade.Instrument)
    tradeDataElement.append(instrumentElement)
    #Legs
    legsElement = GetCollectionXml('legs', 'leg', trade.Legs)
    instrumentElement.append(legsElement)
    #UnderlyingInstruments
    underlyingInstrumentsElement = GetCollectionXml('underlyingInstruments', 'underlyingInstrument', trade.UnderlyingInstruments)
    instrumentElement.append(underlyingInstrumentsElement)
    #Moneyflows
    moneyflowsElement = GetCollectionXml('moneyflows', 'moneyflow', trade.Moneyflows)
    tradeDataElement.append(moneyflowsElement)
    #SalesCredits
    salesCreditsElement = GetCollectionXml('salesCredits', 'salesCredit', trade.SalesCredits)
    tradeDataElement.append(salesCreditsElement)
    return tradeDataElement

def GetCollectionXml(collectionName, itemName, collection):
    root = Element(collectionName.strip())
    if collection:
        for item in collection:
            childElement = GetItemXml(itemName.strip(), item)
            root.append(childElement)
    return root

def GetItemXml(elementName, item):
    root = Element(elementName)
    if item and item.CalculationResults:
       for key in sorted(item.CalculationResults.keys()):
            element = Element(str(key))
            value = item.CalculationResults[key]
            if value and value != '':
                element.text = str(value)
            root.append(element)
    return root

def dateFromISODateTimeString(input):
    if not input:
        return ''
    try:
        return datetime.strptime(input, '%Y-%m-%dT%H:%M:%S')
    except:
        return datetime.strptime(input, '%Y-%m-%d')

def getElapsedTimeInSeconds(startDateTime, endDateTime):
    timeDiff = endDateTime-startDateTime
    totalTime = timeDiff.seconds + (timeDiff.microseconds / 1000000.0)
    return totalTime

def getElapsedTimeInMilliSeconds(startDateTime, endDateTime):
    timeDiff = endDateTime-startDateTime
    totalTime = timeDiff.seconds + (timeDiff.microseconds / 1000.0)
    return totalTime

def FormatException(message, ex):
    exc_type, exc_value, exc_traceback = sys.exc_info()
    return Exception('%s. Line %s. %s' % (message, exc_traceback.tb_lineno, ex))

def BuildSettlement(reportDate, settlementNumber):
    #build
    settlementBuilder = FC_DATA_STL_BUILDER(settlementNumber)
    settlementBuilder = settlementBuilder.CreateData()
    #calculate
    settlement = settlementBuilder.CalculateAndBuild()
    #serialize
    settlement.Serialize()
    return settlement

def BuildTradea(reportDate, tradeNumber):
    #build
    tradeBuilder = FC_DATA_TRD_BUILDER(tradeNumber)
    tradeBuilder = tradeBuilder.CreateStatic()
    tradeBuilder = tradeBuilder.CreateScalar()
    tradeBuilder = tradeBuilder.CreateInstrument()
    tradeBuilder = tradeBuilder.CreateLegs()
    tradeBuilder = tradeBuilder.CreateUnderlyingInstruments()    
    tradeBuilder = tradeBuilder.CreateMoneyflows(reportDate, -1)
    tradeBuilder = tradeBuilder.CreateSalesCredits()
    #calculate
    trade = tradeBuilder.CalculateAndBuild()
    #serialize
    trade.Serialize()
    #trade.Serialize()
    return trade    

def BuildTrade(reportDate, tradeNumber):
    #build
    import xml.dom.minidom

    tradeBuilder = FC_DATA_TRD_BUILDER(tradeNumber)
    tradeBuilder = tradeBuilder.CreateStatic()
    tradeBuilder = tradeBuilder.CreateScalar()
    tradeBuilder = tradeBuilder.CreateInstrument()
    tradeBuilder = tradeBuilder.CreateLegs()
    tradeBuilder = tradeBuilder.CreateUnderlyingInstruments()    
    tradeBuilder = tradeBuilder.CreateMoneyflows(reportDate, -1)
    tradeBuilder = tradeBuilder.CreateSalesCredits()
    #calculate
    trade = tradeBuilder.CalculateAndBuild()
    #serialize
    trade.Serialize()
    #trade.Serialize()
    #print trade.SerializedData

    '''try:
        import os
        os.remove("c:/%s.xml" %tradeNumber)
    except OSError:
        pass'''

    #o = open("c:/%s.xml" %tradeNumber,"a+")
    xml = xml.dom.minidom.parseString(trade.SerializedData)
    pretty_xml_as_string = xml.toprettyxml()
    #o.write(pretty_xml_as_string)
    #print pretty_xml_as_string
    return trade





def BuildTrades(reportDate, tradeNumbers):
    #build\
    
    for x in aaa:
        aaa[x] = 0.0
    
    for singleTrade in tradeNumbers:
        BuildTrade(reportDate, str(singleTrade.Oid()))

def ael_main(dict):
    print 'Run'
    
    colList = dict['columnList'].split(',')
    colListDictionary = {}
    tradeList = dict['tradeList']
    today = at.date_to_datetime(acm.Time.DateToday()).strftime('%Y-%m-%d')
    trds = tradeList
    x = BuildTrades(today, trds)
    for z in sorted(aaa, key=aaa.get, reverse=True):
            if len(colList) > 0:
                for y in colList:
                    if y in z:
                        colListDictionary[z] = aaa[z] 
                        print z, aaa[z]
            else:
                print z, aaa[z] #, ' (' + str((aaa[z]/sum(aaa.values())) * 100) + '% of total average)'

    if len(colList) > 0:
        print 'Total for specific cols', sum(colListDictionary.values())
    print 'Total ', sum(aaa.values())    
    #print len(aaa)
    
         




'''----------------------------------------------------------------------------------------------------------
MODULE                  :       FC_CALCULATION_SINGLETON
PROJECT                 :       FX onto Front Arena
PURPOSE                 :       Used for calculation of dynamic attributes( trading manager workbook columns)
DEPARTMENT AND DESK     :       All Departments and all Desks.
REQUASTER               :       FX onto Front Arena Project
DEVELOPER               :       Heinrich Cronje
CR NUMBER               :       XXXXXX

CHANGES                 :       Heinrich Momberg - introduced a calc space wrapper

Date            CR              Developer               Description
2014-09-18      XXXXXX          Heinrich Cronje         Added Trading Manager Vector Column Calculation
2015-10-29      XXXXXX          Gavin Wienand           Added Vector Sheet functionality
-------------------------------------------------------------------------------------------------------------
'''

#*********************************************************#
#Importing Modules
#*********************************************************#
import acm, ael
from FC_CALCULATION_SPACE import FC_CALCULATION_SPACE as fcCalculationSpace
import FC_UTILS as FC_UTILS
from FC_UTILS import FC_UTILS as UTILS
import at_time

class FC_CALCULATION_SINGLETON:
    instance = None
    worksheetColumns = None
    worksheetCalcSpaces = None
    worksheets = None
    
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
            raise RuntimeError, UTILS.Constants.fcExceptionConstants.SINGLETON_IS_ALLOWED
        else:
            #try:
            #create the column and calc space dictionaries
            self.worksheetColumns = acm.FDictionary()
            self.worksheetCalcSpaces = acm.FDictionary()
            self.worksheets = acm.FDictionary()
            
            #Create control measure container to store control measure per sheet per trade
            self.controlMeasures = self.createControlMeasureContainer()
            
            #Load the workbook sheet columns
            self.LoadWorkbookSheetColumns()

    def GetWorkBook(self, workBookName):
        if (workBookName == UTILS.Constants.fcGenericConstants.FC_DYNAMIC_DATA):
            return acm.FWorkbook[workBookName]
        elif (workBookName == UTILS.Constants.fcGenericConstants.FC_OPERATIONS_DATA):
            return acm.FBackOfficeManagerWorkbook[workBookName]
            
    def createControlMeasureContainer(self):
        container = {}
        for controlItem in UTILS.Parameters.fcGenericParameters.ControlMeasureColumnsList:        
            container[controlItem] = ''
        return container

    def LoadWorkbookSheetColumns(self):
        #Load all the workbooks sheet columns into a dictionary with the sheetName as a the key 
        workbookNames = [UTILS.Constants.fcGenericConstants.FC_DYNAMIC_DATA, UTILS.Constants.fcGenericConstants.FC_OPERATIONS_DATA] #must pull this from config!!!
        if len(workbookNames) == 0:
            raise Exception(UTILS.Constants.fcExceptionConstants.DYNAMIC_CALCULATIONS)
        context = acm.GetDefaultContext()
        for workbookName in workbookNames:
            #load the workbook
            workbook = self.GetWorkBook(workbookName)
            if workbook==None:
                raise Exception(UTILS.Constants.fcExceptionConstants.NOT_LOAD_WORKBOOK_S % workbookName)
            
            #grab each sheet from the workbook
            for worksheet in workbook.Sheets():
                sheetName = worksheet.SheetName()
                
                #Add all the worksheeets to the dictionary
                if self.worksheets.HasKey(sheetName):
                    raise Exception(UTILS.Constants.fcExceptionConstants.WORKBOOKS_MUST_BE_UNIQUE % sheetName)
                self.worksheets[sheetName] = worksheet
                
                #Fetch all the columns for the worksheet and add it to the dictionary
                if self.worksheetColumns.HasKey(sheetName):
                    raise Exception(UTILS.Constants.fcExceptionConstants.WORKSHEETS_MUST_BE_UNIQUE % sheetName)
                self.worksheetColumns[sheetName] = self.getWorksheetColumns(worksheet)
                
                #HM - replaced with the calc space wrapper
                if self.worksheetCalcSpaces.HasKey(sheetName):
                    raise Exception(UTILS.Constants.fcExceptionConstants.WORKSPACE_WORKSHEETS_MUST_BE_UNIQUE % sheetName)
                
                #Create the calculation space
                clearItemThreshold = 25 #possibly a config setting
                self.worksheetCalcSpaces[sheetName] = fcCalculationSpace(context, worksheet, clearItemThreshold)
                #Now create the calculation space based on the sheet type and add it to the dictionary
                '''
                if self.worksheetCalcSpaces.HasKey(sheetName):
                    raise 'The worksheetCalcSpace dictionary already has a sheet named %s, Front Cache worksheet names accross all workbooks must be unique'% sheetName
                if worksheet.IsKindOf('FTradeSheet'):
                    #print sheetName 
                    self.worksheetCalcSpaces[sheetName] = acm.Calculations().CreateCalculationSpace(context, 'FTradeSheet')
                elif worksheet.IsKindOf('FPortfolioSheet'):
                    self.worksheetCalcSpaces[sheetName] = acm.Calculations().CreateCalculationSpace(context, 'FPortfolioSheet')
                elif worksheet.IsKindOf('FMoneyFlowSheet'):
                    self.worksheetCalcSpaces[sheetName] = acm.Calculations().CreateCalculationSpace(context, 'FMoneyFlowSheet')
                else:
                    raise 'The type of worksheet %s in workbook %s not supported. Only sheets of type FTradeSheet, FPortfolioSheet and FMoneyFlowSheet are supported' % (sheetName,workbookName)
                self.worksheetCalcSpaces[sheetName].Clear()
                '''
                
    #get the columns for a given work sheet
    def getWorksheetColumns(self, sheet):
        try:
            sheetColumns = acm.FDictionary()
            columns = sheet.ColumnCollection(acm.FColumnCreatorCreateContext())
            if columns and len(columns)>0:
                for column in columns:
                    columnLabel = self.getSheetColumnCustomLabel(sheet, column.ColumnId())
                    sheetColumns[columnLabel] = column
            else:
                UTILS.Logger.flogger.warn(UTILS.Constants.fcExceptionConstants.CONTAINS_NO_COLUMNS % sheet.SheetName())
                
            return sheetColumns
            
        except Exception, error:
            raise Exception(UTILS.Constants.fcExceptionConstants.COLUMNS_FOR_SHEET_S_S % (sheet.SheetName(), str(error)))

    #Get the custom defined label for a worksheet column
    def getSheetColumnCustomLabel(self, sheet, columnId):
        sheetContents = sheet.Contents()
        for key in sheetContents.Keys():
            if key.Text() == UTILS.Constants.fcGenericConstants.COLUMN_SETTINGS:
                for key1 in sheetContents[key].Keys():
                    checkValue = key1.Text().split('-')[0].strip()
                    if columnId.Text().__contains__(UTILS.Constants.fcGenericConstants.VECTOR):
                        if columnId.Text().__contains__(checkValue):
                            for key2 in sheetContents[key][key1].Keys():
                                if key2.Text() == UTILS.Constants.fcGenericConstants.CUSTOM_LABEL:
                                    return sheetContents[key][key1][key2].Text()
                    else:
                        if checkValue == columnId.Text():
                            for key2 in sheetContents[key][key1].Keys():
                                if key2.Text() == UTILS.Constants.fcGenericConstants.CUSTOM_LABEL:
                                    return sheetContents[key][key1][key2].Text()
    
    def GetControlMeasureContainer(self):
        return self.controlMeasures
        
    def ResetControlMeasureContainer(self):
        container = self.GetControlMeasureContainer()
        for controlItem in container:        
            container[controlItem] = ''
    
    #Create a named parameter for the creation of a column config to calculate vector columns
    def createNamedParameter(self, vector, currencyName):
        param = acm.FNamedParameters();
        param.AddParameter(UTILS.Constants.fcGenericConstants.CURRENCY, acm.FCurrency[currencyName])
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
                if key.Text() == UTILS.Constants.fcGenericConstants.COLUMN_SETTINGS:
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
            raise Exception((UTILS.Constants.fcExceptionConstants.THE_GLOBAL_VALUE_S) %columnId)
        else:
            calcSpace.SimulateGlobalValue(columnId, value)
    
    #Apply Global Simulation
    def ApplyGlobalSimulation(self, profitAndLossStartDate, profitAndLossEndDate, displayCurrency):
        for sheetName in self.worksheetCalcSpaces:
            if profitAndLossStartDate:
                profitAndLossStartDate = ael.date(profitAndLossStartDate)
                self.worksheetCalcSpaces[sheetName].SimulateGlobalValue(UTILS.Constants.fcGenericConstants.PORTFOLIO_PROFIT_LOSS_START_DATE, UTILS.Constants.fcGenericConstants.CUSTOM_DATE)
                self.worksheetCalcSpaces[sheetName].SimulateGlobalValue(UTILS.Constants.fcGenericConstants.PORTFOLIO_PROFIT_LOSS_START_DATE_CUSTOM, profitAndLossStartDate)
            if profitAndLossEndDate:
                profitAndLossEndDate = ael.date(profitAndLossEndDate)
                self.worksheetCalcSpaces[sheetName].SimulateGlobalValue(UTILS.Constants.fcGenericConstants.PORTFOLIO_PROFIT_LOSS_END_DATE, UTILS.Constants.fcGenericConstants.CUSTOM_DATE)
                self.worksheetCalcSpaces[sheetName].SimulateGlobalValue(UTILS.Constants.fcGenericConstants.PORTFOLIO_PROFIT_LOSS_END_DATE_CUSTOM, profitAndLossEndDate)
                #if sheetName == UTILS.Constants.fcGenericConstants.FC_UNDERLYING_INSTRUMENT:
                self.worksheetCalcSpaces[sheetName].SimulateGlobalValue(UTILS.Constants.fcGenericConstants.VALUATION_DATE, profitAndLossEndDate)
            if displayCurrency:
                self.worksheetCalcSpaces[sheetName].SimulateGlobalValue(UTILS.Constants.fcGenericConstants.PORTFOLIO_CURRENCY, displayCurrency)
    
    #Remove Global Simulation
    def RemoveGlobalSimulation(self):
        for sheetName in self.worksheetCalcSpaces:
            self.worksheetCalcSpaces[sheetName].RemoveGlobalSimulation(UTILS.Constants.fcGenericConstants.PORTFOLIO_PROFIT_LOSS_START_DATE)
            self.worksheetCalcSpaces[sheetName].RemoveGlobalSimulation(UTILS.Constants.fcGenericConstants.PORTFOLIO_PROFIT_LOSS_START_DATE_CUSTOM)
            self.worksheetCalcSpaces[sheetName].RemoveGlobalSimulation(UTILS.Constants.fcGenericConstants.PORTFOLIO_PROFIT_LOSS_END_DATE)
            self.worksheetCalcSpaces[sheetName].RemoveGlobalSimulation(UTILS.Constants.fcGenericConstants.PORTFOLIO_PROFIT_LOSS_END_DATE_CUSTOM)
            self.worksheetCalcSpaces[sheetName].RemoveGlobalSimulation(UTILS.Constants.fcGenericConstants.VALUATION_DATE)
    
    #Remove Simulation
    def RemoveSimulation(self, fObject):
        for sheetName in self.worksheetCalcSpaces:
            self.worksheetCalcSpaces[sheetName].RemoveSimulation(fObject, UTILS.Constants.fcGenericConstants.PORTFOLIO_CURRENCY)
    
    #Gets a sheet column value for a given object
    def calcColumnValue(self, calcSpace, acmFObject, acmTreeProxy, column, label, sheetName):
        columnValue = None
        result = ''
        try:
            if column.Method():
                try:
                    columnValue = self.GetValueForObj(column, acmFObject)
                except Exception, e:
                    raise Exception(UTILS.Constants.fcExceptionConstants.COL_CALC_S_FAILED % (column.ColumnId(), acmFObject.ClassName(), str(acmFObject.Oid()), str(e)))
            else:
                try:
                    currencies = None
                    columnConfig = None
                    columnId = column.ColumnId().Text()
                    if columnId.__contains__(UTILS.Constants.fcGenericConstants.VECTOR):
                        columnId = columnId[:columnId.find('[0]')]
                        currencies = self.getVectorColumnCurrency(sheetName, columnId)
                        columnConfig = self.setColumnConfig(currencies)
                    
                    columnValue = calcSpace.CreateCalculation(acmTreeProxy, columnId, columnConfig)
                except Exception, e:
                    raise Exception(UTILS.Constants.fcExceptionConstants.COL_CALC_S_FAILED % (column.ColumnId(), acmFObject.ClassName(), str(acmFObject.Oid()), str(e)))
        except Exception, e:
            raise Exception(UTILS.Constants.fcExceptionConstants.COL_CALC_S_FAILED % (column.ColumnId(), acmFObject.ClassName(), str(acmFObject.Oid()), str(e)))

        if columnValue != None:
            try:
                if str(type(columnValue))=="<type 'FCalculation'>" and columnValue.IsKindOf(UTILS.Constants.fcGenericConstants.F_SYMBOL):
                    return str(columnValue)
                
                result = self.formatColumValue(columnValue, column, label)   
            except Exception, e:
                UTILS.Logger.flogger.critical('Error {%s} in module %s, label {%s}' %(str(e), __name__, label))
                raise
                
        return result

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
                    return None
                
            return value
        else:
            raise Exception(UTILS.Constants.fcGenericConstants.NO_METHOD)
            

    def formatColumValue(self, value, column, label):
        formattedValue = None
        if value is None:
            return formattedValue
        elif type(value) is float:
            return FC_UTILS.formatNumber(value)
        elif type(value) is int:    # do not format ints
            return value

        columnFormatter = column.Formatter()

        try:
            floatValueTest = value.Value()
        except:
            floatValueTest = None

        if type(floatValueTest) == float or (str(type(floatValueTest)) == "<type 'FDenominatedValue'>"):
            return FC_UTILS.formatNumber(floatValueTest)
        elif str(type(columnFormatter)) == "<type 'FDateTimeFormatter'>":
            formattedValue = value
        else:

            try:
                formattedValue = value.FormattedValue()
            except:
                try:
                    formattedValue = columnFormatter.Format(value)
                except:
                    try:
                        formattedValue = value.Number()
                    except:
                        try:
                            formattedValue = value.Name()
                        except:
                            formattedValue = value

        if ((columnFormatter and columnFormatter.IsKindOf(UTILS.Constants.fcGenericConstants.F_NUM_FORMATTER)) or
                                                            (label and label in UTILS.Parameters.fcGenericParameters.NumberFormatLabelOverrides)) and type(formattedValue) != float:
            formattedValue = FC_UTILS.formatNumber(formattedValue)
        elif (columnFormatter and (columnFormatter.IsKindOf(UTILS.Constants.fcGenericConstants.F_DATE_FORMATTER) or columnFormatter.IsKindOf(UTILS.Constants.fcGenericConstants.F_DATE_TIME_FORMATTER))) or\
                                        (label and label in UTILS.Parameters.fcGenericParameters.DateTimeFormatLabelOverrides) or\
                                        (label and label in UTILS.Parameters.fcGenericParameters.DateFormatLabelOverrides):
            if label in UTILS.Parameters.fcGenericParameters.DateFormatLabelOverrides:            
                try:
                    formattedValue = at_time.acm_datetime(formattedValue)
                    formattedValue = FC_UTILS.dateStringFromDate(FC_UTILS.dateFromDateTimeAMPMString(formattedValue))
                except:
                    try:
                        formattedValue = FC_UTILS.dateStringFromISODateTimeString(formattedValue) 
                    except:
                        try:
                            formattedValue = FC_UTILS.dateStringFromDate(formattedValue)
                        except:
                            formattedValue = FC_UTILS.dateStringFromDateTimeString(formattedValue)
            elif label in UTILS.Parameters.fcGenericParameters.DateTimeFormatLabelOverrides:
                formattedValue = FC_UTILS.ISODateTimeFromStringDateOrStringDateTime(formattedValue)
            else:
                formattedValue = FC_UTILS.formatDate(formattedValue)
        
        return formattedValue
	
	
    def returnCurrenciesOfTrade(self, calcSpace, acmTreeProxy):
        result = []
        for curr in calcSpace.InnerCalcSpace.CreateCalculation(acmTreeProxy, 'Currencies Of Trade').Value():
            result.append(curr.Name())
        return result


    #Returns a collection of key/value pairs using tradeingManaget sheet columns for a given object
    def calcWorksheetColumnValues(self, sheetName, acmFObject, acmTreeProxy):
        try:
            if not acmFObject or not acmTreeProxy:
                raise Exception(UTILS.Constants.fcExceptionConstants.PASSED_FOR_CALCULATION)
            
            #Fetch the columns for the sheet from the cached dictionary
            columns = self.worksheetColumns[sheetName]
            if not columns:
                raise Exception(UTILS.Constants.fcExceptionConstants.COLUMNS_FOUND_FOR_SHEET % sheetName)
                
            #Fetch the calculation space for the sheet from the cached dictionary
            calcSpace = self.worksheetCalcSpaces[sheetName]
            if not calcSpace:
                raise Exception(UTILS.Constants.fcExceptionConstants.SPACE_FOUND_FOR_SHEET % sheetName)
                
            #Process the columns by calculating one by one and storing the results in a dictionary
            calcResults = {}
            calcErrors = {}

            #----NB----#
            #The schema will need to be updated for Vector Results
            #Note that the dictionary key is now a tuple and not a string
            if sheetName == "FC_TRADE_VECTOR":
                currOfTrade  = self.returnCurrenciesOfTrade(calcSpace, acmTreeProxy)
                columnConfig = self.setColumnConfig(currOfTrade)
                columns      = self.worksheets[sheetName].ColumnCollection(acm.FColumnCreatorCreateContext())
                for col in columns:
                    if str(col.ColumnName()) != 'Currencies Of Trade':
                        try:
                            columnId   = col.ColumnId().Text()
                            columnId   = columnId[:columnId.find('[0]')]
                            denomValue = calcSpace.InnerCalcSpace.CreateCalculation(acmTreeProxy, columnId, columnConfig).Value()
                            if str(type(denomValue)) == "<type 'FDenominatedValueArray'>":
                                for result in denomValue:
                                    if result.Number():
                                        calcResults[(col.ColumnName(), result.Unit())] = str(result.Number())
                            else:
                                if denomValue.Number():
                                    calcResults[(col.ColumnName(), denomValue.Unit())] = str(denomValue.Number())
                        except Exception, e:
                            UTILS.Logger.flogger.warn('Error {%s} in calcWorksheetColumnValues for colid {%s}' %(str(e), col.ColumnId()))
                            calcErrors[col.ColumnName()] = str(e)
            else:
                for key in columns.Keys():
                    try:
                        columnValue = None
                        column = columns[key]
                        #HM - replaced to use calcSpace wrapper inner CalcSpace
                        columnValue = self.calcColumnValue(calcSpace.InnerCalcSpace, acmFObject, acmTreeProxy, column, key, sheetName)
                        if columnValue is not None and columnValue is not '':
                            calcResults[str(key)] = str(columnValue)
                        if sheetName == UTILS.Constants.fcGenericConstants.FC_TRADE_SCALAR and str(key) in UTILS.Parameters.fcGenericParameters.ControlMeasureColumnsList:
                            self.controlMeasures[str(key)] = str(columnValue)                        
                                                 
                    except Exception, e:
                        UTILS.Logger.flogger.warn('Error {%s} in calcWorksheetColumnValues for key {%s}' %(str(e), key))
                        calcErrors[key] = str(e)

            return calcResults, calcErrors
        except Exception, error:
            raise Exception(UTILS.Constants.fcExceptionConstants.VALUES_FOR_SHEET_S_S % (sheetName, str(error)))

    #Clear all inner Calcspaces
    def clearAllCalcSpaces(self):
        for sheetName in self.worksheetCalcSpaces:
            try:
                self.worksheetCalcSpaces[sheetName].Clear()
            except Exception, e:
                UTILS.Logger.flogger.warning(UTILS.Constants.fcExceptionConstants.THE_FOLLOWING_ERROR_S %(sheetName, str(e)))



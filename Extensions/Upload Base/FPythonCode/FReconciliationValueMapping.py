""" Compiled: 2020-09-18 10:38:51 """

#__src_file__ = "extensions/business_data_upload/../reconciliation/etc/FReconciliationValueMapping.py"
"""--------------------------------------------------------------------------
MODULE
    FReconciliationValueMapping

    (c) Copyright 2014 SunGard FRONT ARENA. All rights reserved.

DESCRIPTION

-----------------------------------------------------------------------------"""
import FReconciliationDataTypeHandler
import datetime
import types

import acm
import FAssetManagementUtils

logger = FAssetManagementUtils.GetLogger()


def GetCalculationParamsColumnId():
    columnMap = {'StartDate': 'Portfolio Profit Loss Start Date',
                 'CustomStartDate': 'Portfolio Profit Loss Start Date Custom',
                 'EndDate': 'Portfolio Profit Loss End Date',
                 'CustomEndDate': 'Portfolio Profit Loss End Date Custom'}
    return columnMap

class FTradingSheetCalculation(object):
    """Extracts calculations made in trading sheet columns."""
    def __init__(self, sheetType, calculationParams=None):
        self.sheetType = sheetType
        self.calculationParams = calculationParams or dict()
        self.context = None
        self.calcSpace = None
        self.item = None        
        
    def SheetType(self):
        return self.sheetType

    def Context(self):
        if not self.context:
            self.context = acm.GetDefaultContext()
        return self.context
        
    def CalcSpace(self):
        if not self.calcSpace:
            self.calcSpace = self._GetCalculationSpace()
        return self.calcSpace        
        
    def Clear(self):
        if self.CalcSpace():
            self.CalcSpace().Clear()

    def InsertItem(self, item):
        self.item = item

    def CalculateValue(self, columnId):
        assert columnId
        return self._GetCalculatedValue(self.item, columnId)

    def _GetCalculationSpace(self):
        calcSpace = acm.Calculations().CreateCalculationSpace(self.Context(), self.SheetType())
        for fieldName, value in self.calculationParams.items():
            columnId = GetCalculationParamsColumnId().get(fieldName)
            if value:
                if columnId:
                    calcSpace.SimulateGlobalValue(columnId, value)
                else:
                    logger.warn("Field name %s does not map to a column id and can not be simulated", fieldName)
        return calcSpace

    def _GetCalculatedValue(self, rowObject, columnId):
        value = None
        try:
            calcValue = self.CalcSpace().CalculateValue(rowObject, columnId)
            value = calcValue.Number()
        except AttributeError:
            value = calcValue
        return value

class FPositionCalculation(FTradingSheetCalculation):
    """Extracts calculations made in portfolio sheet columns for position objects."""
    def __init__(self, calculationParams, isFXReconciliation):
        super(FPositionCalculation, self).__init__('FPortfolioSheet', calculationParams)
        self.isFXReconciliation = isFXReconciliation        
        
    def IsFXReconciliation(self):
        return self.isFXReconciliation
        
    @classmethod
    def PositionGrouper(cls):
        grouper = acm.Risk().GetGrouperFromName('Currency Pair')
        return grouper        

    def InsertItem(self, item):
        insertableItem = GetSheetInsertableACMObject(item, self.IsFXReconciliation())
        self.CalcSpace().InsertItem(insertableItem)
        if self.IsFXReconciliation():
            grouper = self.PositionGrouper()
            self.CalcSpace().RowTreeIterator().FirstChild().Tree().ApplyGrouper(grouper)
        self.CalcSpace().Refresh()

    def RowObject(self):
        rowObject = None
        if self.IsFXReconciliation():
            # Calculate value on the FMultiInstrumentAndTrades row level
            rowObject = self.CalcSpace().RowTreeIterator().FirstChild().FirstChild().Tree().Item()
        else:
            rowObject = self.CalcSpace().RowTreeIterator().FirstChild().Tree().Item()        
        return rowObject

    def CalculateValue(self, columnId):
        assert columnId
        value = self._GetCalculatedValue(self.RowObject(), columnId)            
        return value

    def IsInactivePos(self):
        return acm.GetCalculatedValue(self.RowObject(), self.Context(), "posIsInactive").Value()
        
def GetSheetInsertableACMObject(acmObject, isFXRecon, reconItem = None):
    '''
        Retrieve the insertable sheet object based on a generic 
        reconciliation object. In all cases except for position reconciliation,
        the sheet insertable object is the passed in object itself.
    '''
    insertableObject = acmObject
    if insertableObject and insertableObject.IsKindOf(acm.FStoredASQLQuery):
        # Position reconciliation
        portfolio = acm.FAdhocPortfolio()
        if reconItem:
            portfolio.Name('Reconciliation Item_%i' % reconItem.Oid())        
        trades = acmObject.Query().Select().AsList()
        instruments = set()
        for trade in trades:
            portfolio.Add(trade)
            instruments.add(trade.Instrument())
        singleInstrument = list(instruments)[0]
        if len(instruments) == 1 and not isFXRecon:
            # Case 1: Standard single instrument position reconciliation
            builder = acm.Risk.CreateSingleInstrumentAndTradesBuilder(portfolio, singleInstrument)
            insertableObject = builder.GetTargetInstrumentAndTrades() 
            if insertableObject is None:
                # Potentially matched with a currency instrument - fall back to parent level
                insertableObject = acm.Risk.CreatePortfolioInstrumentAndTrades(portfolio)
        else:
            # Case 2 & 3: Multi instrument position reconciliation or FX position recon
            insertableObject = acm.Risk.CreatePortfolioInstrumentAndTrades(portfolio)
    assert insertableObject, 'Could not create sheet insertable object for object %i ' % acmObject.Oid()
    return insertableObject

def GetCalculator(reconInstance, sheetType = None):
    '''
        Get calculation class responsible for calculating
        values provided a recon instance and potentially
        also a sheet which is not necessarily the same sheet 
        that the specification has been set up for.
    '''
    calculationParams = reconInstance.CalculationParams()
    if reconInstance.ReconciliationDocument().ObjectType() == 'Position':
        isFXReconciliation = reconInstance.ReconciliationSpecification().IsFXReconciliation()        
        return FPositionCalculation(calculationParams, isFXReconciliation)
    if sheetType is None:
        sheetType = reconInstance.ReconciliationSpecification().SheetType()
    return FTradingSheetCalculation(sheetType, calculationParams)

def ValidateReconciliationItems(reconInstance):
    # pylint: disable-msg=W0110
    calculator = GetCalculator(reconInstance)
    identifiedWorkflows = filter(lambda w: w.IsIdentified(), reconInstance.Workflows())
    logger.info('There are %i identified item(s) out of a current total of %i item(s)' % (len(identifiedWorkflows), len(reconInstance.Workflows())))
    if identifiedWorkflows:
        logger.info('Comparing external values with calculated values...')
    for workflow in identifiedWorkflows:
        try:
            calculator.InsertItem(workflow.ACMObject())
            valuesMatch = ValidateReconciliationItem(
                calculator, reconInstance, workflow.ReconciliationItem())
            workflow.IsBreak(not valuesMatch)
        except StandardError as e:
            msg = ('Failed validating reconciliation item info %d values: %s') % (
                workflow.ReconciliationItem().Oid(), e)
            logger.error(msg)
            workflow.ErrorMessage(msg)
        calculator.Clear()
        
def ValidateReconciliationItem(calculator, reconInstance, reconciliationItem):
    logger.debug('Testing if reconciliation item %d is a break', reconciliationItem.Oid())
    valueMappingRules = reconInstance.ReconciliationSpecification().ValueMapping()
    for externalFieldName in valueMappingRules.Keys():
        columnId = valueMappingRules.GetString(externalFieldName)
        externalValue = reconciliationItem.ExternalValues()[str(externalFieldName)]
        calculatedValue = calculator.CalculateValue(columnId)
        typeString = GetTypeFromFieldName(reconInstance, externalFieldName)
        try:
            isMatch = CompareValuePair(calculatedValue, externalValue, typeString)
        except StandardError:
            logger.error('Failed comparing external attribute "%s" (%s) with column "%s" (%s) as a %s data type.',
                         externalFieldName, externalValue, columnId, calculatedValue, typeString)
            raise
        if not isMatch:
            logger.debug('External attribute "%s" (%s) and column "%s" (%s) do not match - this is a break.',
                         externalFieldName, externalValue, columnId, calculatedValue)
            return False
    return True

def GetTypeFromFieldName(reconInstance, externalFieldName):
    reconSpec = reconInstance.ReconciliationSpecification()
    dataTypeMap = reconSpec.DataTypeMapping()
    assert dataTypeMap, "Data type map is not configured for reconciliation specification: " + reconSpec.Name()
    dataType = dataTypeMap.At(externalFieldName)
    if dataType:
        return str(dataType).strip()
    return None

def GetComparableColumnValue(value):
    try:
        acmClass = value.Class()
        if acmClass == acm.FDenominatedValue:
            value = value.Number()
        else:
            # Use the name or string representation for comparison with more complex
            # ACM data types (e.g. Instrument, Currency, etc)
            try:
                value = str(value.Name())
            except AttributeError:
                value = str(value.AsString())
            # Some name/string attributes are encased in single quotes, which must be
            # removed for proper comparison.
            value = value.strip("'")
    except AttributeError:
        # Not an ACM class - the original data type will be compared
        pass
    return value

def CompareValuePair(columnValue, externalValue, externalValueDataTypeName=None):
    columnValue = GetComparableColumnValue(columnValue)
    columnDataType, externalDataType = type(columnValue), type(externalValue)
    numDecimals = dateFormat = thresholdAbs = thresholdPct = None
    comparable = True

    if externalValueDataTypeName:
        typeHandler = FReconciliationDataTypeHandler.FDataTypeHandler(externalValueDataTypeName)

        # Parameters will return None if not defined
        numDecimals = typeHandler.SignificatDecimals()
        dateFormat = typeHandler.DateFormat()
        thresholdAbs = typeHandler.ThresholdAbsolute()
        thresholdPct = typeHandler.ThresholdPercentage()

    if columnDataType is externalDataType:
        if numDecimals and externalDataType is float:
            # In case of float comparison with an extended data type with
            # decimals set, rounding is needed
            dec = int(str(numDecimals).strip())
            externalValue = round(externalValue, dec)
            columnValue = round(columnValue, dec)
        elif dateFormat and externalDataType is str:
            # Although stored as FDateTime objects, date/times will always be returned
            # as string objects when accessed (always in YYYY-MM-DD HH:mm:ss format).
            # Only compare the date values for now.
            externalValue = externalValue.split(' ')[0]
            columnValue = columnValue.split(' ')[0]
    elif not columnDataType is type(None):
        # On differing data types, attempt to convert the column value to the external
        # values data type.
        if externalDataType is str:
            if dateFormat:
                externalValue = externalValue.split(' ')[0]
            externalValue = str(externalValue).strip()
            columnValue = str(columnValue).strip()
        elif externalDataType is float:
            columnValue = float(columnValue)
        elif externalDataType is int:
            columnValue = int(columnValue)
        elif externalDataType is type(None):
            externalValue = None
        else:
            comparable = False

    if not comparable:
        raise TypeError("External value data type '%s' is not comparable to calculated value type '%s'" \
                % (externalDataType, columnDataType))

    result = externalValue == columnValue

    if not result and externalDataType in (int, float) and not columnDataType is type(None):
        # If numeric values did not match, check if they fall within an acceptable threshold
        try:
            if thresholdPct:
                threshold = float(str(thresholdPct).replace('%', '').strip())
                result = (abs((externalValue - columnValue) * 100 / float(columnValue)) <= threshold)
        except (ValueError, ZeroDivisionError):
            pass
        try:
            if not result and thresholdAbs:
                threshold = float(str(thresholdAbs).strip())
                result = (abs(externalValue - columnValue) <= threshold)
        except ValueError:
            pass

    # Note: Only enable the following for debugging, as it will also log during trading manager use.
    #if not result:
    #    logger.debug("External value '%s' (%s) and column value '%s' (%s) are not equal.",
    #            externalValue, type(externalValue), columnValue, type(columnValue))
    return result

def GetExternalValueObjects(fields, typeMap):
    objects = {}
    for fieldName, stringValue in fields.items():
        dataTypeName = typeMap.At(fieldName)
        if not dataTypeName:
            logger.debug("No data type is defined for external value '%s'. Defaulting to 'string'.", fieldName)
            dataTypeName = 'string'
        if isinstance(stringValue, str):
            try:
                # Strip whitespace from user supplied strings for cleaner storage
                objects[fieldName.strip()] = GetObjectFromString(stringValue.strip(), str(dataTypeName).strip())
            except (ValueError, TypeError, AttributeError) as err:
                logger.error("External attribute '%s' (%s) cannot be formatted into data type '%s': %s",
                             fieldName, stringValue, dataTypeName, err)

                raise err.__class__("External attribute '%s' (%s) cannot be formatted into data type '%s': %s"%
                                    (fieldName, stringValue, dataTypeName, err))
        else:
            logger.debug("Field '%s' is already mapped to a data type '%s'.", fieldName, type(stringValue))
            objects[fieldName.strip()] = stringValue
    return objects

def GetObjectFromString(valueString, dataTypeName):
    if valueString == '':
        return '' if (dataTypeName == 'string') else None

    # Convert built-in data types
    dataTypeFuncMap = {'string': str, 'integer': int, 'float': float}
    conversionFunc = dataTypeFuncMap.get(dataTypeName, None)
    if conversionFunc:
        if dataTypeName in ('integer', 'float'):
            valueString = valueString.replace(' ', '')
        return conversionFunc(valueString)

    # Convert a customised data type using a configured type specification
    typeHandler = FReconciliationDataTypeHandler.FDataTypeHandler(dataTypeName)
    baseDataType = typeHandler.GetDataType()

    if baseDataType == 'date':
        dateFormat = typeHandler.DateFormat()
        assert dateFormat, "A 'date_format' parameter must be defined for custom data type '%s'." % dataTypeName
        try:
            date = datetime.datetime.strptime(valueString, str(dateFormat)).strftime('%Y-%m-%d %H:%M:%S')
        except ValueError:
            # Detected a date string
            date = datetime.datetime.strptime(valueString, '%Y-%m-%d').strftime('%Y-%m-%d')
        return date
    elif baseDataType in ('integer', 'float'):
        valueString = valueString.replace(' ', '')
        thousandSeparator = typeHandler.ThousandSeparator()
        if thousandSeparator:
            valueString = valueString.replace(str(thousandSeparator), '')
        if baseDataType == 'float':
            decimalSign = typeHandler.DecimalSign()
            if decimalSign:
                valueString = valueString.replace(str(decimalSign), '.')
            return float(valueString)
        return int(valueString)

    # Unknown data type to convert
    raise TypeError("Specified data type '%s' of base type '%s' is not supported." % (dataTypeName, baseDataType))
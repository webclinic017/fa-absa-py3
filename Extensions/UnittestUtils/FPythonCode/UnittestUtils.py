from __future__ import print_function
import acm
import math
import unittest
import types

class ObjValidatorBase(unittest.TestCase):
    def __init__(self):
        super(ObjValidatorBase, self).__init__()
        self.monitoredAttributes = []
        self.ignoredAttributes = []
        self.attributeToExpectedValue = {}
        self.almostEqualPlaces = {}
        self.almostEqualDelta = {}
        self.almostEqualDeltaPct = {}
        self.almostEqualDeltaPctGlobal = None

    def __del__(self):
        del self.monitoredAttributes[:]
        del self.ignoredAttributes[:]
        self.attributeToExpectedValue.clear()
        self.almostEqualPlaces.clear()
        self.almostEqualDelta.clear()
        self.almostEqualDeltaPct.clear()

    def AddMonitoringOf(self, listOfAttributeNames):
        self.monitoredAttributes = list(set(self.monitoredAttributes + listOfAttributeNames))

    def IgnoreMonitoringOf(self, listOfAttributeNames):
        self.ignoredAttributes = list(set(self.ignoredAttributes + listOfAttributeNames))

    def AlmostEqualPlaces(self, **kwarg):
        self.almostEqualPlaces = kwarg

    def AlmostEqualPlacesOverride(self, **kwarg):
        for key, value in kwarg.iteritems():
            self.almostEqualPlaces[key] = value

    def _AlmostEqualPlaces(self, key):
        return self.almostEqualPlaces.get(key, 7)

    def AlmostEqualDelta(self, **kwarg):
        self.almostEqualDelta = kwarg

    def AlmostEqualDeltaOverride(self, **kwarg):
        for key, value in kwarg.iteritems():
            self.almostEqualDelta[key] = value

    def _AlmostEqualDelta(self, key):
        return self.almostEqualDelta.get(key, None)

    def AlmostEqualDeltaPct(self, **kwarg):
        self.almostEqualDeltaPct = kwarg

    def AlmostEqualDeltaPctOverride(self, **kwarg):
        for key, value in kwarg.iteritems():
            self.almostEqualDeltaPct[key] = value

    def _GetAlmostEqualDeltaPctDefault(self, key):
        if self.almostEqualDelta.get(key, None) is None and self.almostEqualPlaces.get(key, None) is None:
            return self._AlmostEqualDeltaPctGlobal()
        else:
            return None

    def _AlmostEqualDeltaPct(self, key):
        return self.almostEqualDeltaPct.get(key, self._GetAlmostEqualDeltaPctDefault(key))

    def AlmostEqualDeltaPctGlobal(self, deltaPct):
        self.almostEqualDeltaPctGlobal = deltaPct

    def _AlmostEqualDeltaPctGlobal(self):
        return self.almostEqualDeltaPctGlobal

    def RememberValues(self, obj):
        self._RememberAttributeNames(obj)
        self.attributeToExpectedValue = self._GetAttributeToValueDict(obj)

    def AllExpectedChanges(self, **kwargs):
        for attrName, newValue in kwargs.iteritems():
            self.ExpectedChange(attrName, newValue)

    def ExpectedChange(self, attrName, expectedValue):
        oldValue = self.attributeToExpectedValue[attrName]
        errorMsg = '%s has not changed' % attrName
        self._InvertAssertion(attrName, oldValue, expectedValue, errorMsg)

        self.attributeToExpectedValue[attrName] = expectedValue

    def TransformExpectedValues(self, attributeNames, transFunc):
        for attrName in attributeNames:
            oldValue = self.attributeToExpectedValue[attrName]
            self.attributeToExpectedValue[attrName] = transFunc(oldValue)

    def GetAllChanges(self, obj):
        changes = {}
        attrToNewValue = self._GetAttributeToValueDict(obj)

        for attrName in self.attributeToExpectedValue.keys():
            expectedValue = self.attributeToExpectedValue[attrName]
            newValue = attrToNewValue[attrName]
            try:
                self._ValidateSingelAttribute(expectedValue, newValue, attrName)
            except AssertionError:
                if hasattr(newValue, 'StringKey'):
                    newValue = newValue.StringKey()
                changes[attrName] = newValue
        return changes

    def IsFloatOrInt(self, valueList):
        for value in valueList:
            if not (type(value) == types.FloatType or type(value) == types.IntType):
                return False
        return True
    
    def CalculateErrorMargin(self, expectedValue, newValue):
        expectedValue, newValue = self._TransformToAssertable(None, expectedValue, newValue)
        pctDiff = None
        expectedValueForMargin = expectedValue
        newValueForMargin = newValue
        if self._IsKindOf(expectedValue, acm.FDenominatedValue):
            expectedValueForMargin = expectedValue.Number()
        if self._IsKindOf(newValue, acm.FDenominatedValue):
            newValueForMargin = newValue.Number()
        if self.IsFloatOrInt([newValueForMargin]) or self.IsFloatOrInt([expectedValueForMargin]):
            pctDiff = 999999.0
            if self.IsFloatOrInt([newValueForMargin, expectedValueForMargin]) and expectedValueForMargin != 0.0:
                pctDiff = abs((expectedValueForMargin - newValueForMargin) / expectedValueForMargin) * 100.0
        return pctDiff
        
    def GetAllErrorMargins(self, obj):
        errorMargins = {}
        attrToNewValue = self._GetAttributeToValueDict(obj)

        for attrName in self.attributeToExpectedValue.keys():
            expectedValue = self.attributeToExpectedValue[attrName]
            newValue = attrToNewValue[attrName]
            try:
                self._ValidateSingelAttribute(expectedValue, newValue, attrName)
            except AssertionError:
                errorMargins[attrName] = []
                if self._SafeCallAttr(expectedValue, 'IsLot') or self._SafeCallAttr(newValue, 'IsLot'):
                    expectedValue, newValue = self._TransformToAssertable(attrName, expectedValue, newValue)
                    if self._SafeCallAttr(expectedValue, 'IsLot') and self._SafeCallAttr(newValue, 'IsLot'):
                        for i in range(len(expectedValue)):
                            errorMargin = self.CalculateErrorMargin(expectedValue[i], newValue[i])
                            if errorMargin is not None:
                                errorMargins[attrName].append('%s;%s;%f' % (str(newValue[i]), str(expectedValue[i]), errorMargin))
                else:
                    errorMargin = self.CalculateErrorMargin(expectedValue, newValue)
                    if errorMargin is not None:
                        errorMargins[attrName].append('%s;%s;%f' % (str(newValue), str(expectedValue), errorMargin))
        return errorMargins

    def Validate(self, obj):
        attrToNewValue = self._GetAttributeToValueDict(obj)

        for attrName in self.attributeToExpectedValue.keys():
            expectedValue = self.attributeToExpectedValue[attrName]
            newValue = attrToNewValue[attrName]
            self._ValidateSingelAttribute(expectedValue, newValue, attrName)

    def _GetAttributeNames(self, obj):
        raise ('Not Implemented')

    def _GetAttributeValue(self, acmObj, methodName):
        raise ('Not Implemented')

    def _ValidateSingelAttribute(self, expectedValue, newValue, attrName, errorMsg=None):
        expectedValue, newValue = self._TransformToAssertable(attrName, expectedValue, newValue)
        if not errorMsg:
            errorMsg = self._ComposeErrorMsg(attrName, expectedValue, newValue)

        if self._SafeCallAttr(expectedValue, 'IsLot') or self._SafeCallAttr(newValue, 'IsLot'):
            self.assertTrue(self._SafeCallAttr(expectedValue, 'IsLot') and self._SafeCallAttr(newValue, 'IsLot'),
                            msg=errorMsg)
            self.assertTrue(len(expectedValue) == len(newValue), msg=errorMsg)
            for i in range(len(expectedValue)):
                self._ValidateSingelAttribute(expectedValue[i], newValue[i], attrName, errorMsg)
        elif isinstance(expectedValue, float) and isinstance(newValue, float):
            self._ValidateFloat(expectedValue, newValue, self._AlmostEqualPlaces(attrName), errorMsg, self._AlmostEqualDelta(attrName), self._AlmostEqualDeltaPct(attrName))
        elif self._IsKindOf(expectedValue, acm.FDenominatedValue) and self._IsKindOf(newValue, acm.FDenominatedValue):
            self._ValidateDenominatedValue(expectedValue, newValue, self._AlmostEqualPlaces(attrName), errorMsg, self._AlmostEqualDelta(attrName), self._AlmostEqualDeltaPct(attrName))
        elif self._IsKindOf(expectedValue, acm.FSymbol) and self._IsKindOf(newValue, acm.FSymbol):
            self.assertTrue(newValue.IsEqual(expectedValue), msg=errorMsg)
        elif self._IsKindOf(expectedValue, acm.FCollection) and self._IsKindOf(newValue, acm.FCollection):
            isEqual = self._ValidateCollection(expectedValue, newValue, attrName, errorMsg)
            self.assertTrue(isEqual, msg=errorMsg)
        elif self._IsKindOf(expectedValue, acm.FColor) and self._IsKindOf(newValue, acm.FColor):
            isEqual = expectedValue.Rgba() == newValue.Rgba()
            self.assertTrue(isEqual, msg=errorMsg)
        elif self._IsKindOf(expectedValue, acm.FAdditionalInfo) and self._IsKindOf(newValue, acm.FAdditionalInfo):
            isEqual = expectedValue.FieldValue() == newValue.FieldValue() and expectedValue.AddInf() == newValue.AddInf()
            self.assertTrue(isEqual, msg=errorMsg)
        else:
            self.assertEqual(first=expectedValue, second=newValue, msg=errorMsg)

    def _ValidateCollection(self, expectedValue, newValue, attrName, errorMsg):
        isEqual = expectedValue.Size() == newValue.Size()
        if isEqual:
            if expectedValue.IsKindOf(acm.FDictionary):
                for k in expectedValue:
                    self._ValidateSingelAttribute(expectedValue[k], newValue[k], attrName, errorMsg)
            else:
                for i, v in enumerate(expectedValue):
                    self._ValidateSingelAttribute(expectedValue[i], newValue[i], attrName, errorMsg)
        return isEqual

    def _ValidateDenominatedValue(self, expectedValue, newValue, places, errorMsg, delta, deltaPct):
        self._ValidateFloat(expectedValue.Number(), newValue.Number(), places, errorMsg, delta, deltaPct)
        self.assertEqual(first=expectedValue.Unit(), second=newValue.Unit(), msg=errorMsg)
        self.assertEqual(first=expectedValue.Type(), second=newValue.Type(), msg=errorMsg)
        self.assertEqual(first=expectedValue.DateTime(), second=newValue.DateTime(), msg=errorMsg)

    def _ValidateFloat(self, expectedValue, newValue, places, errorMsg, delta, deltaPct):
        if math.isnan(expectedValue) or math.isnan(newValue):
            self.assertTrue(math.isnan(expectedValue) and math.isnan(newValue), msg=errorMsg)
        else:
            if deltaPct is not None:
                delta = abs((deltaPct / 100.0) * expectedValue)
            if delta is not None:
                # If delta and places have been specified, ok to pass with weakest
                try:
                    self.assertAlmostEqual(first=expectedValue, second=newValue, places=None, msg=errorMsg,delta=delta)
                except AssertionError:
                    self.assertAlmostEqual(first=expectedValue, second=newValue, places=places, msg=errorMsg,delta=None)
            else:
                self.assertAlmostEqual(first=expectedValue, second=newValue, places=places, msg=errorMsg,delta=None)

    def _TransformToAssertable(self, attrName, expectedValue, newValue):
        if hasattr(newValue, 'IsKindOf') and (isinstance(expectedValue, str) or isinstance(expectedValue, list)):
            if newValue.IsLot():
                expectedValue = acm.FLot(expectedValue)
            elif newValue.IsKindOf(acm.FDenominatedValue):
                try:
                    f = acm.GetFunction('denominatedvalue', 1)
                    expectedValue = f(expectedValue)
                except Exception, e:
                    # If the expected value is a calcuation error msg, it cannot be converted to a denominated value.
                    pass
            else:
                # expectedValue = newValue.Domain().ParseObject(expectedValue)
                newValue = newValue.StringKey()

        if self._IsKindOf(expectedValue, acm.FObject):
            expectedValue = self._GetOriginator(expectedValue)
        if self._IsKindOf(newValue, acm.FObject):
            newValue = self._GetOriginator(newValue)

        return expectedValue, newValue

    def _GetOriginator(self, val):
        originator = val if val.IsModified() else val.Originator()
        if originator and hasattr(originator, 'DecoratedObject'):
            originator = originator.DecoratedObject()
        return originator

    def _ComposeErrorMsg(self, attrName, expectedValue, newValue):
        errorMsg = ''''"%s" not as expected
                       Expected: %s
                       Actual: %s''' % (attrName, expectedValue, newValue)
        return errorMsg

    def _IsKindOf(self, value, aType):
        return self._SafeCallAttr(value, 'IsKindOf', aType)

    def _SafeCallAttr(self, obj, attr, *args):
        toReturn = False
        if hasattr(obj, attr):
            toReturn = getattr(obj, attr)(*args)
        return toReturn

    def _RememberAttributeNames(self, obj):
        self.AddMonitoringOf(self._GetAttributeNames(obj))

    def _GetAllMonitoredAttributes(self):
        return list(set(self.monitoredAttributes) - set(self.ignoredAttributes))

    def _GetAttributeToValueDict(self, obj):
        attrToValue = {}
        for attrName in self._GetAllMonitoredAttributes():
            attrToValue[attrName] = self._GetAttributeValue(obj, attrName)
        return attrToValue

    def runTest(self):
        pass

    def _InvertAssertion(self, attrName, oldValue, expectedValue, msg):
        allIsOk = True
        try:
            self._ValidateSingelAttribute(expectedValue, oldValue, attrName)
            allIsOk = False
        except AssertionError:
            pass

        if not allIsOk:
            raise AssertionError(msg)


class CompoundValidator(object):
    def __init__(self):
        self.validators = {}

    def AddValidator(self, key, validator):
        self.validators[key] = validator

    def GetValidator(self, key):
        return self.validators.get(key, None)

    def RememberValues(self, obj):
        for validator in self.validators.values():
            validator.RememberValues(obj)

    def IgnoreMonitoringOf(self, listOfAttributeNames):
        for validator in self.validators.values():
            validator.RememberValues(listOfAttributeNames)

    def AlmostEqualDeltaPctGlobal(self, deltaPct):
        for validator in self.validators.values():
            validator.AlmostEqualDeltaPctGlobal(deltaPct)

    def Validate(self, obj):
        for key, validator in self.validators.iteritems():
            try:
                validator.Validate(obj)
            except AssertionError as e:
                msg = '%s error: %s' % (key, e.message)
                raise AssertionError(msg)

    def GetAllChanges(self, obj):
        changes = []
        for key, validator in self.validators.iteritems():
            changes.append({key: validator.GetAllChanges(obj)})
        return changes

    def GetAllErrorMargins(self, obj):
        errorMargins = []
        for key, validator in self.validators.iteritems():
            errorMargins.append({key: validator.GetAllErrorMargins(obj)})
        return errorMargins

    def _AddValidatorIfMissing(self, key, validator):
        found = CompoundValidator.GetValidator(self, key)
        if not found:
            self.AddValidator(key, validator)


class AcmObjValidator(ObjValidatorBase):
    '''
    To validate that an ACM objects attributes has changed as expected, and nothing more

    Typical Usecase:
    def test_dummy(self):
        # prepare test
        trade = acm.FTrade[ 123456 ]
        tradeDeco = acm.FBusinessLogicDecorator.WrapObject( trade )
        tradeDeco.Portfolio( 'TOBJOH00' )

        # Remember trade state
        tradeValidator = AcmObjValidator()
        tradeValidator.IgnoreMonitoringOf( ['SomeMethodToIgnore'] ) # Optional
        tradeValidator.AddMonitoringOf( ['SomeMethodMonitor'] ) # Optional (typically some transient method)
        tradeValidator.RememberValues(trade)

        # Run method(s) that should be tested
        tradeDeco.Quantity( 9999 )

        # Tell the validator what is expected to have changed (no more, no less)
        tradeValidator.AllExpectedChanges(
                                          Premium=9999000.0,
                                          Quantity=9999
                                          )
        # Validate
        tradeValidator.Validate( trade )
    '''

    NEW_TRADE_ATTRIBUTES = [
        'ConnectedTrade',
        'ConnectedTrdnbr',
        'Contract',
        'ContractTrdnbr',
        'CreateTime',
        'CreateUser',
        'Name',
        'Oid',
        'UpdateTime',
        'UpdateUser',
    ]
    NEW_INSTRUMENT_ATTRIBUTES = [
        'CreateTime',
        'CreateUser',
        'Name',
        'Oid',
        'Trades',
        'Underlying',
        'UpdateTime',
        'UpdateUser',
        'VersionId'
    ]

    def __init__(self):
        super(AcmObjValidator, self).__init__()
        self.IgnoreMonitoringOf(['Ultimo', 'IpaPtynbr'])  # Removed from FLeg

    def _GetAttributeNames(self, acmObj):
        attributeMethods = []
        allAttributes = acmObj.Class().Attributes()
        for att in allAttributes:
            method = att.GetMethod()
            if method:
                methodName = str(method.Name())
                attributeMethods.append(methodName)
        return attributeMethods

    def _GetAttributeValue(self, acmObj, methodName):
        method = getattr(acmObj, methodName)
        return method()


class FCashFlowInstrumentValidator(AcmObjValidator):
    def __init__(self):
        super(FCashFlowInstrumentValidator, self).__init__()
        self.AddMonitoringOf(['EndDate'])  # Transient values


class TraitsValueValidator(ObjValidatorBase):
    '''
    To validate that traits on a trait based application work as expected
    '''

    def _GetAttributeNames(self, obj):
        return obj.GetAttributes()

    def _GetAttributeValue(self, obj, attrName):
        value = obj.GetAttribute(attrName)
        if hasattr(value, 'IsKindOf') and value.IsKindOf('FCalculation'):
            try:
                value = value.Value()
            except Exception, e:
                value = str(e)
        return value


class DealPackageTraitsValueValidator(TraitsValueValidator):
    '''
    To validate that traits on a Deal Package work as expected
    '''
    pass


class TraitsAttributeValidator(ObjValidatorBase):
    '''
    To validate that traits on a trait based application work as expected
    '''

    def __init__(self, attrName):
        super(TraitsAttributeValidator, self).__init__()
        self.attrName = attrName

    def _GetAttributeNames(self, obj):
        return obj.GetAttributes()

    def _GetAttributeValue(self, obj, traitName):
        return obj.GetAttributeMetaData(traitName, self.attrName)()


class DealPackageTraitsAttributeValidator(TraitsAttributeValidator):
    '''
    To validate that traits on a deal package works as expected
    '''
    pass


class TraitsValidator(CompoundValidator):
    def __init__(self):
        super(TraitsValidator, self).__init__()
        self.AddValidator('Values', TraitsValueValidator())
        self.AddValidator('Visibility', TraitsAttributeValidator('visible'))
        self.AddValidator('Enabled', TraitsAttributeValidator('enabled'))
        self.AddValidator('Editable', TraitsAttributeValidator('editable'))
        self.AddValidator('Label', TraitsAttributeValidator('label'))
        self.AddValidator('BackgroundColor', TraitsAttributeValidator('backgroundColor'))

    def ValuesValidator(self):
        return self.GetValidator('Values')

    def VisabilityValidator(self):
        return self.GetValidator('Visibility')

    def EnableValidator(self):
        return self.GetValidator('Enabled')
        
    def EditableValidator(self):
        return self.GetValidator('Editable')

    def LabelValidator(self):
        return self.GetValidator('Label')

    def BackgroundColorValidator(self):
        return self.GetValidator('BackgroundColor')


class DealPackageTraitsValidator(TraitsValidator):
    def __init__(self):
        super(DealPackageTraitsValidator, self).__init__()


class SingleAcmObjValidator(AcmObjValidator):
    def __init__(self, subjectName):
        super(SingleAcmObjValidator, self).__init__()
        self.subjectName = subjectName

    def RememberValues(self, obj):
        AcmObjValidator.RememberValues(self, self._Subject(obj))

    def Validate(self, obj):
        AcmObjValidator.Validate(self, self._Subject(obj))

    def GetAllChanges(self, obj):
        return AcmObjValidator.GetAllChanges(self, self._Subject(obj))

    def GetAllErrorMargins(self, obj):
        return AcmObjValidator.GetAllErrorMargins(self, self._Subject(obj))

    def _SubjectName(self):
        return self.subjectName

    def _Subject(self, obj):
        raise ('Not Implemented')


class EditableObjectSingleAcmObjValidator(SingleAcmObjValidator):
    def __init__(self, subjectName):
        super(EditableObjectSingleAcmObjValidator, self).__init__(subjectName)

    def _Subject(self, obj):
        return obj.Object()


class EditableObjectValidator(CompoundValidator):
    def __init__(self, subjectName):
        super(EditableObjectValidator, self).__init__()
        self.AddValidator('Traits', TraitsValidator())
        self.AddValidator('Object', EditableObjectSingleAcmObjValidator(subjectName))

    def TraitsValidator(self):
        return self.GetValidator('Traits')

    def ObjectValidator(self):
        return self.GetValidator('Object')


class DealPackageSingleAcmObjValidator(SingleAcmObjValidator):
    def __init__(self, subjectName):
        super(DealPackageSingleAcmObjValidator, self).__init__(subjectName)


class DealPackageSingleInstrumentValidator(DealPackageSingleAcmObjValidator):
    def _Subject(self, dp):
        if hasattr(dp, 'InstrumentAt'):
            return dp.InstrumentAt(self._SubjectName()).Instrument()
        else:
            return dp.Instrument().Instrument()


class DealPackageSingleTradeValidator(DealPackageSingleAcmObjValidator):
    def _Subject(self, dp):
        if hasattr(dp, 'TradeAt'):
            return dp.TradeAt(self._SubjectName()).Trade()
        else:
            return dp.Trade().Trade()


class DealPackageCompoundAcmObjValidator(CompoundValidator):
    def RememberValues(self, dp):
        for key in self._Keys(dp):
            self._AddValidatorIfMissing(key, self._CreateValidator(key))
        CompoundValidator.RememberValues(self, dp)

    def GetValidator(self, key):
        self._AddValidatorIfMissing(key, self._CreateValidator(key))
        return CompoundValidator.GetValidator(self, key)

    def _Keys(self, dp):
        raise ('Not Implemented')

    def _CreateValidator(self, key):
        raise ('Not Implemented')


class DealPackageTradesValidator(DealPackageCompoundAcmObjValidator):
    def _Keys(self, dp):
        retVal = ['**Dummy**']
        if hasattr(dp, 'TradeKeys'):
            retVal = dp.TradeKeys()
        return retVal

    def _CreateValidator(self, key):
        return DealPackageSingleTradeValidator(key)


class DealPackageSingleB2BTradeParamsValidator(DealPackageSingleAcmObjValidator):
    def _Subject(self, dp):
        if hasattr(dp, 'B2BTradeParamsAt'):
            return dp.B2BTradeParamsAt(self._SubjectName()).Parameters()
        else:
            return dp.B2BTradeParams().Parameters()


class DealPackageB2BTradeParamsValidator(DealPackageCompoundAcmObjValidator):
    def _Keys(self, dp):
        retVal = ['**Dummy**']
        if hasattr(dp, 'TradeKeys'):
            retVal = dp.TradeKeys()
        return retVal

    def _CreateValidator(self, key):
        return DealPackageSingleB2BTradeParamsValidator(key)


class DealPackageInstrumentsValidator(DealPackageCompoundAcmObjValidator):
    def _Keys(self, dp):
        retVal = ['**Dummy**']
        if hasattr(dp, 'InstrumentKeys'):
            retVal = dp.InstrumentKeys()
        return retVal

    def _CreateValidator(self, key):
        return DealPackageSingleInstrumentValidator(key)


class DealPackageValidator(CompoundValidator):
    def __init__(self):
        super(DealPackageValidator, self).__init__()
        self.AddValidator('Traits', DealPackageTraitsValidator())
        self.AddValidator('Trades', DealPackageTradesValidator())
        self.AddValidator('Instruments', DealPackageInstrumentsValidator())
        self.AddValidator('B2BTradeParams', DealPackageB2BTradeParamsValidator())

    def TraitsValidator(self):
        return self.GetValidator('Traits')

    def TradeValidator(self, tradeName='**Dummy**'):
        return self.GetValidator('Trades').GetValidator(tradeName)

    def InstrumentValidator(self, insName='**Dummy**'):
        return self.GetValidator('Instruments').GetValidator(insName)

    def B2BTradeParamsValidator(self, tradeName='**Dummy**'):
        return self.GetValidator('B2BTradeParams').GetValidator(tradeName)


class ChildDealPackageValidator(DealPackageValidator):
    def __init__(self, subjectName):
        super(ChildDealPackageValidator, self).__init__()
        self.subjectName = subjectName

    def RememberValues(self, dp):
        DealPackageValidator.RememberValues(self, self._Subject(dp))

    def Validate(self, dp):
        DealPackageValidator.Validate(self, self._Subject(dp))

    def GetAllChanges(self, dp):
        return DealPackageValidator.GetAllChanges(self, self._Subject(dp))

    def GetAllErrorMargins(self, obj):
        return DealPackageValidator.GetAllErrorMargins(self, self._Subject(dp))

    def _SubjectName(self):
        return self.subjectName

    def _Subject(self, dp):
        if hasattr(dp, 'ChildDealPackageAt'):
            dp = dp.ChildDealPackageAt(self._SubjectName()).DealPackage()
            return dp


class ChildDealPackagesValidator(DealPackageCompoundAcmObjValidator):
    def _Keys(self, dp):
        retVal = ['**Dummy**']
        if hasattr(dp, 'ChildDealPackageKeys'):
            retVal = dp.ChildDealPackageKeys()
        return retVal

    def _CreateValidator(self, key):
        return ChildDealPackageValidator(key)


class DealPackageOfDealPackagesValidator(CompoundValidator):
    def __init__(self):
        super(DealPackageOfDealPackagesValidator, self).__init__()
        self.AddValidator('ParentDealPackage', DealPackageValidator())
        self.AddValidator('ChildDealPackages', ChildDealPackagesValidator())

    def ParentDealPackageValidator(self):
        return self.GetValidator('ParentDealPackage')

    def ChildDealPackageValidator(self, dpName='**Dummy**'):
        return self.GetValidator('ChildDealPackages').GetValidator(dpName)


class TradeConstellationValidator(object):
    def __init__(self, trade, validateMethods, expectedResult):
        self._trades = self.__CreateTradeDictFromTrade(trade)
        self._validateMethods = validateMethods
        self._expectedResult = expectedResult
        self._errorAccumulator = acm.FDictionary()
        self.__ValidateInputData()

    def __del__(self):
        self._trades.Clear()
        self._validateMethods = None
        self._expectedResult = None
        self._errorAccumulator.Clear()

    def __ValidateInputData(self):
        for tradeKey in self._trades.Keys():
            trade = self.__GetTrade(tradeKey)
            expectedResults = self.__ExpectedResults(tradeKey)
            methods = self.__Methods()
            if not (expectedResults == methods == None):
                if not len(expectedResults) == len(methods):
                    raise Exception('Missmatch between size of methods and expected result set')

    def __CreateTradeDictFromTrade(self, trade):
        trades = acm.FDictionary()
        counter = 0
        for trade in trade.GroupTrades().SortByProperty('StorageId', True):
            counter = counter + 1
            trades.AtPut((trade.TradeProcessesToString() + " " + str(counter)), trade)
        return trades

    def __Methods(self):
        return self._validateMethods.get('Trade')

    def __ExpectedResults(self, tradeKey=None):
        if not tradeKey:
            return self._expectedResult
        return self._expectedResult.get(tradeKey)

    def __ErrorAccumulator(self):
        return self._errorAccumulator

    def __AccumulateValidationResult(self, trade, attr, validationResult):
        if validationResult:
            tradeKey = trade.TradeProcessesToString()
            tradeAccumulator = self.__ErrorAccumulator().At(tradeKey)
            if not tradeAccumulator:
                tradeAccumulator = acm.FDictionary()
                self.__ErrorAccumulator().AtPut(tradeKey, tradeAccumulator)
            tradeAccumulator.AtPut(attr, validationResult)

    def __GetAttrValue(self, trade, method):
        attrValue = getattr(trade, method)()
        if hasattr(attrValue, 'StringKey'):
            attrValue = attrValue.StringKey()
        return attrValue

    def __GetTrade(self, tradeKey):
        trade = self._trades.At(tradeKey)
        if not trade:
            raise Exception('Could not find trade')
        return trade

    def __CreateErrorMsg(self, actual, expected):
        return "Value: %s \tExpected %s" % (actual, expected)

    def __ValidateFloatAttrValue(self, actualAttrValue, expectedAttrValue):
        validationResult = None
        expectedAsFloat = float(expectedAttrValue)
        if math.isnan(expectedAsFloat) != math.isnan(actualAttrValue):
            validationResult = self.__CreateErrorMsg(str(actualAttrValue), str(expectedAttrValue))
        else:
            expectedValueAccuracy = len(str(expectedAttrValue).split(".")[1])
            if round(actualAttrValue - expectedAsFloat, expectedValueAccuracy) != 0:
                validationResult = self.__CreateErrorMsg(str(actualAttrValue), expectedAttrValue)
        return validationResult

    def __ValidateAttrValueExact(self, actualAttrValue, expectedAttrValue):
        validationResult = None
        expectedAttrValue = None if expectedAttrValue == 'None' else expectedAttrValue
        if not actualAttrValue == expectedAttrValue:
            validationResult = self.__CreateErrorMsg(str(actualAttrValue), str(expectedAttrValue))
        return validationResult

    def __ValidateAttrValue(self, trade, attr, actualAttrValue, expectedAttrValue):
        if isinstance(actualAttrValue, float):
            validationResult = self.__ValidateFloatAttrValue(actualAttrValue, expectedAttrValue)
        else:
            validationResult = self.__ValidateAttrValueExact(actualAttrValue, expectedAttrValue)
        self.__AccumulateValidationResult(trade, attr, validationResult)

    def __ValidateTradeAttr(self, trade, tradeMethods, expectedResults):
        for i in range(len(tradeMethods)):
            attr = tradeMethods[i]
            expectedAttrValue = expectedResults[i]
            actualAttrValue = self.__GetAttrValue(trade, attr)
            self.__ValidateAttrValue(trade, attr, actualAttrValue, expectedAttrValue)

    def __GetAttrsAsStrings(self, attrValues):
        attrStr = ""
        for attrVal in attrValues:
            attrStr += "'" + attrVal + "', "
        return attrStr[:-2]

    def CreateExpectedResultDict(self, methods):
        self._validateMethods = methods
        expectedResult = acm.FDictionary()
        for tradeKey in self._trades.Keys():
            trade = self.__GetTrade(tradeKey)
            attrValueArray = acm.FArray()
            for attr in self.__Methods():
                attrVal = self.__GetAttrValue(trade, attr)
                attrValueArray.Add(str(attrVal))
            expectedResult.AtPut(tradeKey, attrValueArray)
        return expectedResult

    def FormattedExpectedResult(self, methods):
        resultStr = 'expectedTradeAttr = {\n'
        result = self.CreateExpectedResultDict(methods)
        for key in result:
            resultStr += ("'" + key + "'" + '\t:\t[' + self.__GetAttrsAsStrings(result.At(key)) + '],\n')
        resultStr = resultStr[:-2]
        resultStr += '\n}'
        return resultStr

    def Validate(self):
        for tradeKey in self._trades.Keys():
            trade = self.__GetTrade(tradeKey)
            methods = self.__Methods()
            expectedResults = self.__ExpectedResults(tradeKey)
            self.__ValidateTradeAttr(trade, methods, expectedResults)
        return self.__ErrorAccumulator().Keys().Size() == 0

    def FormattedResult(self):
        formattedResult = ""
        for key in self.__ErrorAccumulator().Keys():
            formattedResult += '\n' + '*' * 10 + '\n"' + key + '"\n'
            for attrKey in self.__ErrorAccumulator().At(key):
                formattedResult += '\t- ' + attrKey + '\t' + self.__ErrorAccumulator().At(key).At(attrKey) + '\n'
        return formattedResult

    def PrintResult(self):
        print (self.FormattedResult())


class FFxTradeConstellationParametersValidator(AcmObjValidator):
    def __init__(self):
        super(FFxTradeConstellationParametersValidator, self).__init__()
        self.AddMonitoringOf(self.GetMonitoringOfExtraFields())

    def GetMonitoringOfExtraFields(self):
        monitorMethods = acm.FArray()
        ignoreList = ['AllocateFXRisk', 'AllocateRisk', 'Trade']

        for method in acm.FFxTradeConstellationParameters.MethodsDefined():
            if method.NumberOfOperands() == 1 and str(method.Name()) not in ignoreList:
                monitorMethods.Add(str(method.Name()))

        return monitorMethods
  



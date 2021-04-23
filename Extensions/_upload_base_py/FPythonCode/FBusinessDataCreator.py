""" Compiled: 2020-09-18 10:38:51 """

#__src_file__ = "extensions/business_data_upload/etc/FBusinessDataCreator.py"
"""--------------------------------------------------------------------------
MODULE
    FBusinessDataCreator

    (c) Copyright 2015 SunGard FRONT ARENA. All rights reserved.

DESCRIPTION

-----------------------------------------------------------------------------"""
import acm
import datetime
import FAssetManagementUtils
import FReconciliationIdentification
import FBusinessDataPropertyMapper
import types

STARTOFTIME = '1970-01-01 00:00:00'
logger = FAssetManagementUtils.GetLogger()


class FBusinessDataCreator(object):

    def __init__(self, reconciliationSpecification, reconciliationItem, businessObject):
        self._reconciliationItem = reconciliationItem
        self._reconSpec = reconciliationSpecification
        self._businessObj = businessObject
        self._mandatoryFields = None
        self._PopulateAttributes()

    def MandatoryFields(self,mandatoryFields=None):
        if mandatoryFields != None:
            self._mandatoryFields = mandatoryFields
        else:
            if self._mandatoryFields == None:
                return self._DefaultMandatoryFields()
            else:
                return self._mandatoryFields

    def _DefaultMandatoryFields(self):
        raise NotImplementedError('Abstract base class can not be instansiated')

    def _IsDateTime(self, value):
        try:
            if len(value) not in (10, 19):
                return False
            datetime.datetime.strptime(value[:10], '%Y-%m-%d')
            return True
        except (TypeError, ValueError):
            return False

    def _IsValidAttribute(self, func):
        if not func:
            return False
        result = func()
        if not result:
            return False
        if self._IsDateTime(result) and acm.Time.LocalToUtc(result) == STARTOFTIME:
            return False
        return True

    def Validate(self):
        missingFields = list()
        for field in self.MandatoryFields():
            func = getattr(self.BusinessObject(), field)
            if not self._IsValidAttribute(func):
                missingFields.append(field)
        if len(missingFields) > 0:
            raise ReferenceError('%s is missing: %s' % (self.BusinessObject().ClassName(), ', '.join(map(str, missingFields))))

    def Execute(self):
        try:
            self.BusinessObject().Commit()
        except RuntimeError as e:
            raise SystemError('Could not commit %s: %s' % (self.BusinessObject().ClassName(), e))
        return True

    def _PopulateAttributes(self):
        className = self.BusinessObject().ClassName()

        reconciliationItemAttributes = \
                FReconciliationIdentification.FIdentificationEngine.GetReconciliationItemAttributes(
                self._reconciliationItem,
                self._reconSpec.ExternalAttributeMap(),
                self._reconSpec.GetIdentificationValues)

        for attributes in self._reconSpec.ExternalAttributeMap().values():
            if isinstance(attributes, types.StringType):
                attributes = [attributes]
            for attribute in attributes:
                try:
                    propertyMapper = FBusinessDataPropertyMapper.PropertyMapper(className, attribute)
                except TypeError as e:
                    logger.error('Wrong parameters for mapping: %s, %s: %s' % (className, attribute, e))
                    raise

                externalValue = reconciliationItemAttributes[attribute]
                try:
                    value = propertyMapper.GetValue(externalValue)
                except TypeError as e:
                    continue

                try:
                    setattr(self.BusinessObject(), attribute, value)
                    logger.debug('Set attribute %s with value %s on new %s' % (attribute, externalValue, className))
                except StandardError as e:
                    logger.warn('Could not set attribute %s with value %s on new FTrade: %s' % (attribute, externalValue, e))

    def BusinessObject(self):
        return self._businessObj
        
    def PreCommitHook(self):
        editedObject = self._reconSpec.PreCommit(self.BusinessObject(), self._reconciliationItem.ExternalValues())
        if not editedObject:
            raise SystemError('Pre commit hook does not return an object')
        if not editedObject.Class() == self.BusinessObject().Class():
            raise 'BusinessObject returned from the pre commit hook does not have same class: %s and %s' % (editedObject.ClassName() == self._businessObj.ClassName())
        self._businessObj = editedObject

class FOrderCreator(FBusinessDataCreator):

    def __init__(self, reconciliationSpecification, reconciliationItem, acmObject=None):
        businessObject = acmObject or acm.FTrade()
        super(FOrderCreator, self).__init__(reconciliationSpecification, reconciliationItem, businessObject)
        
    def _DefaultMandatoryFields(self):
        return ['Currency', 'Instrument', 'Portfolio', 'Quantity', 'Price']
    
    def Execute(self):
        trade = self._businessObj
        name = acm.User().Name() + ' ' + datetime.datetime.now().strftime('%x %X')
        try:
            import FTradeToOrder, FOrderUtils
            market = FOrderUtils.GetPrimaryMarket()
            FOrderUtils.Connect(market)
            op_handler = FTradeToOrder.CreateOrderProgramFromTrades([trade], name, 'Inactive')
            FOrderUtils.OrderProgramSender(op_handler, None).SendAsync()
            trade.Delete()
        except ImportError as e:
            raise SyntaxError('Could not create order. Buy Side OMS module must be imported in the context.')
        except Exception as e:
            raise SystemError('Could not create order: %s' % (e))
        return True

class FTradeCreator(FBusinessDataCreator):

    def __init__(self, reconciliationSpecification, reconciliationItem, acmObject=None):
        businessObject = acmObject or acm.FTrade()
        super(FTradeCreator, self).__init__(reconciliationSpecification, reconciliationItem, businessObject)
        
    def _DefaultMandatoryFields(self):
        return ['Counterparty', 'Instrument', 'Currency', 'Acquirer', 'TradeTime', 'ValueDay']

class FJournalCreator(FBusinessDataCreator):

    def __init__(self, reconciliationSpecification, reconciliationItem, acmObject=None):
        businessObject = acmObject or acm.FJournal()
        super(FJournalCreator, self).__init__(reconciliationSpecification, reconciliationItem, businessObject)
        
    def _DefaultMandatoryFields(self):
        return ['Amount', 'ChartOfAccount', 'Currency', 'DebitOrCredit', 'EventDate']

class FInstrumentCreator(FBusinessDataCreator):

    def __init__(self, reconciliationSpecification, reconciliationItem, acmObject=None):
        businessObject = acmObject or self.CreateNewInstrument(reconciliationSpecification.ReconciliationSubType())
        assert businessObject.InsType() == reconciliationSpecification.ReconciliationSubType()
        super(FInstrumentCreator, self).__init__(reconciliationSpecification, reconciliationItem, businessObject)
        
    @staticmethod
    def CreateNewInstrument(instrumentType):
        return acm.DealCapturing().CreateNewInstrument(instrumentType)

    def _DefaultMandatoryFields(self):
        return ['Currency',]
            

# Factory method for the base classes
def GetCreator(reconciliationSpecification, reconciliationItem, acmObject=None):
    creator = None
    objectType = reconciliationSpecification.ReconciliationObjectType()
    if objectType == 'Trade':
        creator = FTradeCreator(reconciliationSpecification, reconciliationItem, acmObject)
    if objectType == 'Order':
        creator = FOrderCreator(reconciliationSpecification, reconciliationItem, acmObject)
    if objectType == 'Instrument':
        creator = FInstrumentCreator(reconciliationSpecification, reconciliationItem, acmObject)
    if objectType == 'Journal':
        creator = FJournalCreator(reconciliationSpecification, reconciliationItem, acmObject)
    return creator

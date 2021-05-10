""" Compiled: 2020-09-18 10:38:46 """

#__src_file__ = "extensions/accounting/etc/FAccountingObjectModifier.py"

import acm

# accounting
from FAccountingEnums import JournalAggregationLevel

# operations
from FOperationsObjectModifier import ObjectModifier
from FOperationsExceptions import ObjectModifierException

#-------------------------------------------------------------------------
class AccountingObjectModifier(ObjectModifier):

    #-------------------------------------------------------------------------
    def __init__(self):
        super(AccountingObjectModifier, self).__init__()

        self.__modificationHooks = dict()

        self.__provider = None

    #-------------------------------------------------------------------------
    def PO_Init(self, provider):
        self.__provider = provider

    #-------------------------------------------------------------------------
    def PO_Clear(self):
        self.__modificationHooks.clear()

    #-------------------------------------------------------------------------
    def RegisterModificationHook(self, objClass, idx, modifiableFields):
        self.__modificationHooks[objClass] = idx, modifiableFields

    #-------------------------------------------------------------------------
    def OM_ModifyObjects(self, objs):
        self.__ModifyObjects(objs)

    #-------------------------------------------------------------------------
    def OM_ModifyReplace(self, objs, field, dataDict):
        assert field, 'ERROR: No field to replace given'

        self.__ModifyReplace(objs, field, dataDict)

    #-------------------------------------------------------------------------
    def __ModifyObjects(self, objs):

        for obj in objs:
            obj.RegisterInStorage()

            idx, fields = self.__modificationHooks.get(str(obj.ClassName()), (None, None))

            if idx:
                self.__ApplyModification(obj, idx, fields)

            if self.__provider.Param('inheritProtection'):
                self.__SetProtection(obj)

    #-------------------------------------------------------------------------
    def __ApplyModification(self, obj, idx, fields):

        modified = self.__provider.HA_CallHook(idx, obj.Clone())

        obj.AddInfos().Apply(modified.AddInfos())

        try:
            for field in fields:
                setattr(obj, field, getattr(modified, field)())

        except AttributeError as e:
            raise ObjectModifierException('ERROR: Failed to apply client modification: {}'.format(e))

    #-------------------------------------------------------------------------
    def __SetProtection(self, obj):
        if obj.IsKindOf(acm.FJournal) or obj.IsKindOf(acm.FJournalInformation):

            protectedObject = self.__GetProtectedObject(obj)

            if protectedObject:
                obj.Owner(protectedObject.Owner())
                obj.Protection(protectedObject.Protection())

    #-------------------------------------------------------------------------
    def __GetProtectedObject(self, obj):
        ai = obj.AccountingInstruction()
        settlement = obj.Settlement()

        if ai and ai.AggregationLevel() == JournalAggregationLevel.INSTRUMENT_AND_PORTFOLIO:
            return settlement.Instrument() if settlement else obj.Instrument()
        else:
            return settlement.Trade() if settlement else obj.Trade()

    #-------------------------------------------------------------------------
    def __ModifyReplace(self, objs, field, dataDict):

        try:
            for obj in objs:
                replaceData = dataDict.get(getattr(obj, field)().Oid(), None)

                if replaceData:
                    setattr(obj, field, replaceData)

        except AttributeError as e:
            raise ObjectModifierException('ERROR: Failed to replace field {}: {}'.format(field, e))

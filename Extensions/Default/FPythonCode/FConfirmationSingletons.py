""" Compiled: 2020-09-18 10:38:49 """

#__src_file__ = "extensions/confirmation/etc/FConfirmationSingletons.py"
import acm
from FOperationsRuleEngine import Rule, QueryCondition, RuleExecutor, ValueType, ActionValue
import FOperationsUtils as Utils
from FConfirmationTradeFilter import ConfirmationProcessFilterHandler

class EventChoiceListItemHandler:
    __instance = None

    def __init__(self):
        if EventChoiceListItemHandler.__instance:
            raise EventChoiceListItemHandler.__instance
        EventChoiceListItemHandler.__instance = self

        self.eventChoiceListItems = dict()
        eventChoiceList = acm.FChoiceList.Select("list = 'Event'")
        for eventChoiceListItem in eventChoiceList:
            self.eventChoiceListItems[eventChoiceListItem.Name()] = eventChoiceListItem

    def GetEventChoiceListItem(self, eventChoiceListItemName):
        assert eventChoiceListItemName in self.eventChoiceListItems
        return self.eventChoiceListItems[eventChoiceListItemName]

    def GetAllEventChoiceListItems(self):
        return self.eventChoiceListItems.itervalues()

    def GetAllEventChoiceListItemNames(self):
        return self.eventChoiceListItems.iterkeys()

class ConfirmationPreventionRulesHandler:
    __instance = None

    def __init__(self):
        if ConfirmationPreventionRulesHandler.__instance:
            raise ConfirmationPreventionRulesHandler.__instance
        ConfirmationPreventionRulesHandler.__instance = self

        import FConfirmationParameters as ConfirmationParameters

        self.__tradeFilterQueryNames                     = ConfirmationParameters.tradeFilterQueries
        self.__preventConfirmationCreationQueryNames     = ConfirmationParameters.preventConfirmationCreationQueries
        self.__preventConfirmationCancellationQueryNames = ConfirmationParameters.preventConfirmationCancellationQueries
        self.__preventConfirmationAmendmentQueryNames    = ConfirmationParameters.preventConfirmationAmendmentQueries

        self.__tradeFilterEngine         = self.__GetTradeFilterEngine()
        self.__preventCreationEngine     = self.__GetPreventCreationEngine()
        self.__preventCancellationEngine = self.__GetPreventCancellationEngine()
        self.__preventAmendmentEngine    = self.__GetPreventAmendmentEngine()

    @staticmethod
    def CreatePreventionRuleEngine(queryList, acmClass):
        rules = []
        ruleExecutor = None
        for query in queryList:
            preventQuery = Utils.GetStoredQuery(query, acmClass)
            if preventQuery:
                rules.append(Rule(QueryCondition(preventQuery.Query()), ActionValue(True)))
        if len(rules):
            ruleExecutor = RuleExecutor(rules, ActionValue(False))
        return ruleExecutor

    @staticmethod
    def AddFObjectAction(fObject, fObjectList):
        fObjectList.append(fObject)

    @staticmethod
    def FallBack(fObject, dummyFObjectList):
        if fObject.IsKindOf(acm.FTrade):
            Utils.LogAlways('Trade %d does not match trade filter' % fObject.Oid())
        else:
            Utils.LogAlways('Incorrect FObject type for confirmation processing')

    def __GetTradeFilterEngine(self):
        return ConfirmationProcessFilterHandler()

    def __GetPreventCreationEngine(self):
        return ConfirmationPreventionRulesHandler.CreatePreventionRuleEngine(self.__preventConfirmationCreationQueryNames,
                                                                             acm.FConfirmation)

    def __GetPreventCancellationEngine(self):
        return ConfirmationPreventionRulesHandler.CreatePreventionRuleEngine(self.__preventConfirmationCancellationQueryNames,
                                                                             acm.FConfirmation)

    def __GetPreventAmendmentEngine(self):
        return ConfirmationPreventionRulesHandler.CreatePreventionRuleEngine(self.__preventConfirmationAmendmentQueryNames,
                                                                             acm.FConfirmation)

    def IsPreventConfirmationCreation(self, confirmation):
        isPreventConfirmation = False
        if self.__preventCreationEngine:
            if self.__preventCreationEngine.Execute(confirmation,
                                                    ValueType.SINGLE_VALUE,
                                                    confirmation):
                isPreventConfirmation = True
                Utils.LogVerbose('Preventing creation of %s confirmation.' % confirmation.EventChlItem().Name())
        return isPreventConfirmation

    def IsPreventConfirmationCancellation(self, confirmation):
        isPreventConfirmationCancellation = False
        if self.__preventCancellationEngine:
            if self.__preventCancellationEngine.Execute(confirmation,
                                                        ValueType.SINGLE_VALUE,
                                                        confirmation):
                isPreventConfirmationCancellation = True
                Utils.LogVerbose('Preventing cancellation of confirmation %d.' % confirmation.Oid())
        return isPreventConfirmationCancellation

    def IsPreventConfirmationAmendment(self, confirmation):
        isPreventConfirmationAmendment = False
        if self.__preventAmendmentEngine:
            if self.__preventAmendmentEngine.Execute(confirmation,
                                                     ValueType.SINGLE_VALUE,
                                                     confirmation):
                isPreventConfirmationAmendment = True
                Utils.LogVerbose('Preventing amendment of confirmation %d.' % confirmation.Oid())
        return isPreventConfirmationAmendment

    def FilterAndAddFObject(self, fObject, fObjectList):
        if fObject.IsKindOf(acm.FTrade):
            if self.__tradeFilterEngine:
                self.__tradeFilterEngine.FilterAndAddTrade(fObject, fObjectList)
        else:
            Utils.LogVerbose('Incorrect FObject in confirmation process')

def GetSingleton(SingletonClass, *params):
    try:
        single = SingletonClass(*params)
    except SingletonClass as s:
        single = s
    return single
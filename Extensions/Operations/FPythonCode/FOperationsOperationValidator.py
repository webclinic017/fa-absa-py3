""" Compiled: 2020-09-18 10:38:53 """

#__src_file__ = "extensions/operations/etc/FOperationsOperationValidator.py"

from FOperationsUtils import GetStoredQuery
from FOperationsEngines import Validator
from FOperationsRuleEngine import Rule, QueryCondition, RuleExecutor, ValueType, ActionValue

#-------------------------------------------------------------------------
class OperationValidator(Validator):

    #-------------------------------------------------------------------------
    def __init__(self, objectClass, queriesAndOpDict):
        self.__objectClass = objectClass
        self.__registeredEngines = dict() 
        self.CreateEngines(queriesAndOpDict)

    #-------------------------------------------------------------------------
    def CreateEngines(self, queriesAndOpDict):
        for op, queries in queriesAndOpDict.items():
            self.__registeredEngines[op] = self.CreateEngine(queries, self.__objectClass)

    #-------------------------------------------------------------------------
    def CreateEngine(self, queries, acmClass):
        rules = []
        ruleExecutor = None
        for query in queries:
            preventQuery = GetStoredQuery(query, acmClass)
            if preventQuery:
                rules.append(Rule(QueryCondition(preventQuery.Query()), ActionValue(True)))
        if len(rules):
            ruleExecutor = RuleExecutor(rules, ActionValue(False))
        return ruleExecutor
    
    #-------------------------------------------------------------------------
    def VA_IsValidOperation(self, op, obj):
        engineForOp = self.__registeredEngines.get(op)
        
        if not engineForOp or not engineForOp.Execute(obj, ValueType.SINGLE_VALUE, obj):
            return True
        else:
            return False
        
        

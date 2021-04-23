""" Compiled: 2020-09-18 10:38:53 """

#__src_file__ = "extensions/operations/etc/FOperationsRuleEngine.py"
import types

class ValueType(object):
    '''Enum class.'''

    NONE = 0
    SINGLE_VALUE = 1
    ANY_IN_LIST = 2
    ALL_IN_LIST = 3

class Condition(object):
    '''Base-class for all conditions.'''

    def __MetByAny(self, value):
        '''In: value - list of values to test.
           Out: True if condition was met by any in list, False otherwise.'''

        metByAny = False
        for singleValue in value:
            metByAny = self.MetBy(singleValue, ValueType.SINGLE_VALUE)
            if metByAny:
                break
        return metByAny

    def __MetByAll(self, value):
        '''In: value - list of values to test.
           Out: True if condition was met by all in list, False otherwise.'''

        metByAll = True
        for singleValue in value:
            metByAll = self.MetBy(singleValue, ValueType.SINGLE_VALUE)
            if metByAll == False:
                break
        return metByAll

    def MetBy(self, value, valueType):
        '''In: value - Value to test.
               valueType - Type of value.
           Out: True if condition was met, False otherwise.'''

        isMet = False
        if valueType == ValueType.ANY_IN_LIST:
            isMet = self.__MetByAny(value)
        elif valueType == ValueType.ALL_IN_LIST:
            isMet = self.__MetByAll(value)
        return isMet


class QueryCondition(Condition):
    '''Conditions based on ASQL query.'''

    def __init__(self, query):
        '''In: query - A FASQLQuery object.'''

        Condition.__init__(self)
        assert query != None, 'No query specified.'
        self.__query = query

    def MetBy(self, value, valueType):
        '''In: value - An FObject derived object that tests if the condition is met.
               valueType - Type of value.
           Out: True if the condition was met, False otherwise.'''
        isMet = False
        if value == None:
            isMet = False
        elif valueType == ValueType.SINGLE_VALUE:
            isMet = self.__query.IsSatisfiedBy(value)
        else:
            isMet = Condition.MetBy(self, value, valueType)
        return isMet

class And(Condition):
    '''This class is used to create And conditions.'''

    def __init__(self, conditions):
        '''In: conditions - The conditions to And.'''

        Condition.__init__(self)
        self.__conditions = conditions

    def MetBy(self, value, valueType):
        '''In: value - An FObject derived object that tests if the condition is met.
               valueType - Type of value.
           Out: True if the condition was met, False otherwise.'''

        metCounter = 0
        for condition in self.__conditions:
            if condition.MetBy(value, valueType):
                metCounter += 1
        return metCounter == len(self.__conditions)

class Or(Condition):
    '''This class is used to create Or conditions.'''

    def __init__(self, conditions):
        '''In: conditions - The conditions to Or.'''

        Condition.__init__(self)
        self.__conditions = conditions

    def MetBy(self, value, valueType):
        '''In: value - An FObject derived object that tests if the condition is met.
               valueType - Type of value.
           Out: True if the condition was met, False otherwise.'''

        isMet = False
        for condition in self.__conditions:
            isMet = condition.MetBy(value, valueType)
            if isMet:
                break
        return isMet

class Action:
    '''Abstract base class for all actions.'''

    def __init__(self):
        '''Constructor.'''
        if self.__class__ is Action:
            raise NotImplementedError

    def Execute(self, *args):
        '''In: The arguments passed to the action.
           Out: the result of the action.'''
        raise NotImplementedError

class ActionFunction(Action):
    '''Actions that executes the given function.'''

    def __init__(self, function):
        '''Constructor.'''

        Action.__init__(self)
        assert function != None, 'Function not specified.'
        assert isinstance(function, types.FunctionType), 'The parameter is not a function.'
        self.__function = function

    def Execute(self, *args):
        '''In: args - The arguments passed to the function.
           Out: Data returned by the function.'''

        return self.__function(*args)

class ActionValue(Action):
    '''Actions that returns the given value.'''

    def __init__(self, value):
        '''Constructor.'''

        Action.__init__(self)
        self.__value = value

    def Execute(self, *args):
        '''In: args - The arguments, not used for ActionValues.
           Out: The value.'''

        return self.__value

class Rule(object):
    '''A Rule is a condition linked to an action.'''

    def __init__(self, condition, action):
        '''In: condition - The condition that should be met in order for the action to be performed.
               action - The action that is performed when the condition is met.'''


        assert condition != None, 'Condition not specified.'
        assert action != None, 'Action not specified.'
        self.__condition = condition
        self.__action = action

    def ConditionMetBy(self, value, valueType):
        '''In: value - The value of the test.
               valueType - Type of value.
           Out: True if the condition was met, False otherwise.'''

        return self.__condition.MetBy(value, valueType)

    def ExecuteAction(self, *args):
        '''In: args - The arguments passed to the action.
           Out: Data returned by the action.'''

        return self.__action.Execute(*args)

class RuleExecutor(object):
    '''This class takes a set of rules and executes the first rule whose
       condition matches the value.'''

    def __init__(self, rules, fallbackAction):
        '''In: rules - A list of rules in descending priority order
               fallbackAction - An action that is executed if no rule was matched.'''

        self.__rules = rules
        self.__fallbackAction = fallbackAction

    def Execute(self, value, valueType, *args):
        '''In: value - The value of the test.
               valueType - Type of value.
               args - The arguments sent as input to the action.'''

        for rule in self.__rules:
            if rule.ConditionMetBy(value, valueType):
                return rule.ExecuteAction(*args)
        return self.__fallbackAction.Execute(*args)

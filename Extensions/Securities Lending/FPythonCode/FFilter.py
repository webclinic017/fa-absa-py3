""" Compiled: 2020-09-18 10:38:55 """

#__src_file__ = "extensions/SecuritiesLending/etc/FFilter.py"
"""-------------------------------------------------------------------------------------------------------
MODULE
    FFilter

    (c) Copyright 2015 SunGard FRONT ARENA. All rights reserved.

DESCRIPTION

-------------------------------------------------------------------------------------------------------"""
import ast
import acm
import operator

class Variant(object):

    DEFAULT_FORMATTER_NAME = 'Default'

    def __init__(self, formatter=None):
        self._formatter = formatter

    def Formatter(self):
        if self._formatter is None:
            self._formatter = acm.Get('formats/{0}'.format(self.DEFAULT_FORMATTER_NAME))
        return self._formatter

    def Value(self, variant):
        try:
            return self.AsNumber(variant)
        except StandardError:
            pass
        return variant

    def AsNumber(self, variant):
        number = self.Formatter().Parse(variant, acm.GetDomain('float'))
        if number is None:
            raise ValueError('Failed to convert variant to float.')
        return number


class FFilterList(list):

    def __init__(self, _list):
        self._list = _list
        list.__init__(self, _list)

    def Filter(self, filterFunc):
        try:
            return self._list.Filter(filterFunc)
        except AttributeError:
            return filter(filterFunc, self._list)


class FFilterDict(dict):

    def __init__(self, _dict):
        self._dict = self.AsPyDict(_dict)
        dict.__init__(self, self._dict)

    def keys(self):
        return FFilterList(self._dict.keys())

    @staticmethod
    def AsPyDict(_dict):

        if isinstance(_dict, dict):
            return _dict
        return dict(list(zip(_dict.Keys(), _dict.Values())))


class FFilterMethod(object):

    def __init__(self, name):
        self._name = name

    def Name(self):
        return self._name

class FFilterColumn(FFilterMethod):

    def __init__(self, name, sheetType, context):
        FFilterMethod.__init__(self, name)
        self._sheetType = sheetType
        self._context = context
        self._formatter = None

    def ColumnId(self):
        return self._name

    def SheetType(self, sheetType=None):
        if sheetType is None:
            return self._sheetType
        self._sheetType = sheetType

    def Context(self, context=None):
        if context is None:
            return self._context
        self._context = context

    def Formatter(self):
        if self._formatter is None:
            try:
                creators = acm.GetColumnCreators(self.ColumnId(), self.Context())
                self._formatter = creators.At(0).Columns().First().Formatter()
            except StandardError:
                pass
        return self._formatter


class FOperator(object):

    _operatorsMap = {}

    def __init__(self, name):
        self._name = str(name)

    def Name(self):
        return self._name

    def OperatorSymbol(self):
        return acm.FSymbol(self._name)

    def Operator(self):
        try:
            return self._operatorsMap[self.Formatted(self._name)]
        except KeyError:
            msg = 'Operator {0} of type {1} not supported'.format(
                self._name, self.__class__.__name__)
            raise KeyError(msg)

    def Compare(self, left, right):
        return self.Operator()(left, right)

    @classmethod
    def IsValid(cls, name):
        return bool(str(name) in cls._operatorsMap)

    @classmethod
    def Operators(cls):
        return cls._operatorsMap.keys()

    @classmethod
    def OperatorSymbols(cls):
        # pylint: disable-msg=W0110,W0108
        return map(lambda op: acm.FSymbol(op), cls._operatorsMap.keys())

    @staticmethod
    def Formatted(name):
        raise NotImplementedError


class FComparisonOperator(FOperator):

    _operatorsMap = {
        '=': operator.eq,
        '!=': operator.ne,
        '<': operator.lt,
        '<=': operator.le,
        '>': operator.gt,
        '>=': operator.ge
        }

    def __init__(self, name):
        FOperator.__init__(self, name)

    def Compare(self, left, right):
        if type(left) is type(right):
            return self.Operator()(left, right)
        return True

    @classmethod
    def Inverse(cls, name):
        try:
            name = str(name)
            if '<' in name:
                name = name.replace('<', '>')
            elif '>' in name:
                name = name.replace('>', '<')
            return name
        except StandardError as e:
            raise e

    @staticmethod
    def Formatted(name):
        return str(name)


class FTopOperator(FOperator):

    _operatorsMap = {
        'TOP': operator.contains,
        'BOTTOM': operator.contains
        }

    def __init__(self, name):
        FOperator.__init__(self, name)

    @staticmethod
    def Formatted(name):
        return str(name).upper()


class FLogicalOperator(FOperator):

    _operatorsMap = {
        'AND': operator.and_,
        'OR': operator.or_
        }

    def __init__(self, name):
        FOperator.__init__(self, name)

    @staticmethod
    def Formatted(name):
        return name.upper()


class FAndOperator(FLogicalOperator):

    NAME = 'AND'

    def __init__(self):
        FLogicalOperator.__init__(self, self.NAME)


class FOrOperator(FLogicalOperator):

    NAME = 'OR'

    def __init__(self):
        FLogicalOperator.__init__(self, self.NAME)


class FBetweenOperator(FOperator):

    NAME = 'BETWEEN'
    _operatorsMap = {
        NAME: (
            FLogicalOperator('AND'),
            FComparisonOperator('<'),
            FComparisonOperator('>')
            )
        }

    def __init__(self):
        FOperator.__init__(self, self.NAME)
        self._innerOperators = {}

    def InnerOperators(self):
        if not self._innerOperators:
            for op in self.Operator():
                self._innerOperators[op.Name()] = op
        return self._innerOperators

    def PartialCompare(self, name, left, right):
        return self.InnerOperators().get(name).Compare(left, right)

    def GreaterThan(self, left, right):
        return self.PartialCompare('>', left, right)

    def LessThan(self, left, right):
        return self.PartialCompare('<', left, right)

    def And(self, left, right):
        return self.PartialCompare('AND', left, right)

    def Compare(self, _value, left, right):
        #Handle case where only left of right is specified with volume formatter
        #print "between {} and {} comparison of {}".format(left, right, _value)
        #print "between comparison result",self.And(
        #    self.GreaterThan(_value, left),
        #    self.LessThan(_value, right)
        #    )
        # Could be rewritten; this routine adds one arg compared to the base class
        # pylint: disable-msg=W0221
        if _value is None or _value == "":
            return False
        else:
            return self.And(
                self.GreaterThan(_value, left),
                self.LessThan(_value, right)
                )

    @staticmethod
    def Formatted(name):
        return str(name).upper()


class _FComparator(object):

    def Filter(self, objects):
        raise NotImplementedError

    def FilterValues(self, objectsAndValues):
        raise NotImplementedError

    def FilterFunction(self, obj):
        raise NotImplementedError

    @classmethod
    def IsDeclarativeCmp(cls, *args):
        return bool(len(args) is 5 and
            all(FComparisonOperator.IsValid(op) for op in args[1::2]))

    @classmethod
    def IsDeclarativeMethodCmp(cls, *args):
        return bool(cls.IsDeclarativeCmp(*args) and
            isinstance(args[2], FFilterMethod))

    @classmethod
    def IsDeclarativeColumnCmp(cls, *args):
        return bool(cls.IsDeclarativeCmp(*args) and
            isinstance(args[2], FFilterColumn))

    @classmethod
    def IsTopCmp(cls, *args):
        return bool(len(args) is 3 and
            FTopOperator.Formatted(args[1]) in FTopOperator.Operators())

    @classmethod
    def IsMethodCmp(cls, *args):
        return cls.IsAttrCmp(FFilterMethod, *args)

    @classmethod
    def IsColumnCmp(cls, *args):
        return cls.IsAttrCmp(FFilterColumn, *args)

    @classmethod
    def IsCompoundCmp(cls, *args):
        return bool(all(issubclass(type(cmp), cls) for cmp in args[::2]) and
            all(FLogicalOperator.IsValid(op) for op in args[1::2]))

    @classmethod
    def Reversed(cls, args):
        aList = []
        for arg in reversed(args):
            if FComparisonOperator.IsValid(arg):
                arg = FComparisonOperator.Inverse(arg)
            aList.append(arg)
        return aList

    @classmethod
    def Create(cls, *args):
        if cls.IsMethodCmp(*args):
            return _FMethodComparator(*args)
        elif cls.IsColumnCmp(*args):
            return _FColumnComparator(*args)
        elif (cls.IsDeclarativeMethodCmp(*args) or
              cls.IsDeclarativeColumnCmp(*args)):
            return _FCompoundComparator.New(*args)
        elif cls.IsTopCmp(*args):
            return FTopComparator.New(*args)
        elif cls.IsCompoundCmp(*args):
            if isinstance(args[0], _FCompoundComparator):
                return cls.Create(*args[0]._args)
            return _FCompoundComparator(*args)
        raise ValueError('Invalid set of arguments.')

    @staticmethod
    def IsAttrCmp(class_, *args):
        return bool(args and (args[0].__class__ is class_) and
            ((len(args) is 3 and FComparisonOperator.IsValid(args[1])) or
             (len(args) is 4 and FBetweenOperator.IsValid(args[1]))))


class _FMethodComparator(_FComparator):

    def __init__(self, *args):
        self._attr = args[0]
        self._operator = self.GetOperator(self.GetItem(args, 1))
        self._left = self.AsVariant(self.GetItem(args, 2))
        self._right = self.AsVariant(self.GetItem(args, 3))
        self._objectsAndValues = None

    def Attribute(self):
        return self._attr

    def LeftValue(self):
        return self._left

    def RightValue(self):
        return self._right

    def ValidateComparisonOperator(self):
        self.Operator()

    def Filter(self, objects):
        self.ValidateComparisonOperator()
        return objects.Filter(self.FilterFunction)

    def FilterValues(self, objectsAndValues):
        self.ObjectsAndValues(objectsAndValues)
        return self.Filter(objectsAndValues.keys())

    def FilterFunction(self, obj):
        try:
            return self._operator.Compare(
                                    self.GetAttrValue(obj),
                                    self._left,
                                    self._right)
        except TypeError:
            return self._operator.Compare(
                                    self.GetAttrValue(obj),
                                    self._left)

    def GetAttrValue(self, obj):
        if self.ObjectsAndValues() is None:
            return self._GetAttrValue(obj)
        value_ = self.ObjectsAndValues()[obj][self._attr.Name()]
        return self.AsVariant(value_)

    def Operator(self):
        return self._operator.Operator()

    def OperatorSymbol(self):
        return self._operator.OperatorSymbol()

    def AsVariant(self, variant):
        return Variant().Value(variant)

    def ObjectsAndValues(self, objectsAndValues=None):
        if objectsAndValues is None:
            return self._objectsAndValues
        self._objectsAndValues = objectsAndValues

    def _GetAttrValue(self, obj):
        try:
            for attr in self._attr.Name().split('.'):
                obj = getattr(obj, attr)()
            return self.AsVariant(obj)
        except AttributeError as e:
            raise e

    @staticmethod
    def GetItem(aList, idx, default=None):
        try:
            return aList[idx]
        except IndexError:
            return default

    @staticmethod
    def GetOperator(name):
        if name is not None:
            if str(name).upper() == 'BETWEEN':
                return FBetweenOperator()
            return FComparisonOperator(name)


class _FColumnComparator(_FMethodComparator):

    _spaceCollection = None
    _context = None

    def __init__(self, *args):
        _FMethodComparator.__init__(self, *args)

    def GetSpace(self):
        if self._spaceCollection is None:
            self._spaceCollection = acm.FCalculationSpaceCollection()
        return self._spaceCollection.GetSpace(self._attr.SheetType(), self._attr.Context())

    def FormattedValue(self, obj):
        return self.GetSpace().CreateCalculation(obj, self._attr.ColumnId()).FormattedValue()

    def AsVariant(self, variant):
        return Variant(self._attr.Formatter()).Value(variant)

    def _GetAttrValue(self, obj):
        try:
            space = self.GetSpace()
            space.InsertItem(obj)
            space.Refresh()
            return self.AsVariant(self.FormattedValue(obj))
        except StandardError as e:
            raise e


class _FCompoundComparator(_FComparator):

    def __init__(self, *args):
        self._args = args

    def Arguments(self):
        return self._args

    def ValidateLogicalOperators(self):
        # pylint: disable-msg=W0106
        [op.Operator() for op in self.GetLogicalOperators()]

    def Filter(self, objects):
        self.ValidateLogicalOperators()
        self.ResetComparators(self, objects)
        #print "FFilter - Filter",type(objects) #objects: filterlist
        return objects.Filter(self.FilterFunction)

    def FilterValues(self, objectsAndValues):
        self.ObjectsAndValues(self, objectsAndValues)
        #print "FCompoundComparator:FilterValues",self.Filter(objectsAndValues.keys())
        return self.Filter(objectsAndValues.keys())

    def FilterFunction(self, obj):
        logicalOperators = self.GetLogicalOperators()
        comparatorsIter = iter(self.GetComparators())
       # print "logicalOperators",logicalOperators
        #print "comparatorsIter",comparatorsIter
        retValue = next(comparatorsIter).FilterFunction(obj)
        for i, comparator in enumerate(comparatorsIter):
            logicalOp = logicalOperators[i].Operator()
            retValue = logicalOp(retValue, comparator.FilterFunction(obj))
            #print "obj= {} retValue={} logicalOp={}".format(obj, retValue,logicalOp)
        return retValue

    def GetLogicalOperators(self):
        return [FLogicalOperator(op) for op in self._args[1::2]]

    def GetComparators(self):
        return self._args[::2]

    @classmethod
    def New(cls, *args):
        cmp1 = _FComparator.Create(*(cls.Reversed(args[:3])))
        cmp2 = _FComparator.Create(*args[-3:])
        return cls(cmp1, 'AND', cmp2)

    @classmethod
    def ObjectsAndValues(cls, comparator, objectsAndValues):
        if isinstance(comparator, _FMethodComparator):
            comparator.ObjectsAndValues(objectsAndValues)
        elif isinstance(comparator, FTopComparator):
            comparator.Comparator().ObjectsAndValues(objectsAndValues)
        elif isinstance(comparator, _FCompoundComparator):
            for cmpr in comparator.GetComparators():
                if cmpr is not comparator:
                    cls.ObjectsAndValues(cmpr, objectsAndValues)

    @classmethod
    def ResetComparators(cls, comparator, objects):
        if type(comparator) in (FTopComparator, FBottomComparator):
            comparator.ResetComparator(objects)
        elif type(comparator) is _FCompoundComparator:
            for cmpr in comparator.GetComparators():
                if cmpr is not comparator:
                    cls.ResetComparators(cmpr, objects)


class FTopComparator(_FComparator):

    def __init__(self, attr, numberOfItems, inOperator='TOP'):
        self._comparator = self.GetComparator(attr)
        self._operator = FTopOperator(inOperator)
        self._numberOfItems = self.AsInteger(numberOfItems)
        self._objects = None
        self._topItems = None

    def Attribute(self):
        return self._comparator.Attribute()

    def Comparator(self):
        return self._comparator

    def OperatorSymbol(self):
        return self._operator.OperatorSymbol()

    def LeftValue(self):
        return self._numberOfItems

    def RightValue(self):
        pass

    def SortedItems(self):
        attrValue = self._comparator.GetAttrValue
        return sorted(self._objects, key=attrValue, reverse=True)

    def TopItemsFilter(self, item):
        try:
            variant = self._comparator.GetAttrValue(item)
            Variant().AsNumber(variant)
            return True
        except ValueError:
            return False

    def TopItems(self):
        if self._topItems is None:
            filterFunc = self.TopItemsFilter
            self._objects[:] = filter(filterFunc, self._objects)
            self._topItems = self.SortedItems()[:self._numberOfItems]
        return self._topItems

    def ResetComparator(self, objects):
        self._objects = objects
        self._topItems = None

    def Filter(self, objects):
        self.ResetComparator(objects)
        return objects.Filter(self.FilterFunction)

    def FilterValues(self, objectsAndValues):
        self._comparator.ObjectsAndValues(objectsAndValues)
        return self.Filter(objectsAndValues.keys())

    def FilterFunction(self, obj):
        # pylint: disable-msg=W0621
        if self._objects is None:
            return False
        return self._operator.Compare(self.TopItems(), obj)

    @classmethod
    def New(cls, *args):
        attr, op, nbrOfItems = args
        if FTopOperator.Formatted(op) == 'TOP':
            return cls(attr, nbrOfItems)
        return FBottomComparator(attr, nbrOfItems)

    @staticmethod
    def GetComparator(attr):
        if type(attr) is FFilterMethod:
            return _FMethodComparator(attr)
        return _FColumnComparator(attr)

    @staticmethod
    def AsInteger(variant):
        try:
            return int(variant or 0)
        except ValueError as e:
            raise e


class FBottomComparator(FTopComparator):

    def __init__(self, comparator, numberOfItems, op='BOTTOM'):
        FTopComparator.__init__(self, comparator, numberOfItems, op)

    def SortedItems(self):
        attrValue = self._comparator.GetAttrValue
        return sorted(self._objects, key=attrValue)


class FFilter(object):

    def __init__(self, comparator):
        self._comparator = comparator

    def Comparator(self):
        return self._comparator

    def Filter(self, objects):
        return self._comparator.Filter(FFilterList(objects))

    def FilterValues(self, objectsAndValues):
        #print "FilterValues _comparator",type(self._comparator),self._comparator
        #print "FilterValues FFilterDict",FFilterDict(objectsAndValues)
        return self._comparator.FilterValues(FFilterDict(objectsAndValues))

    @classmethod
    def CreateFromComparator(cls, *args):
        return cls(cls.CreateComparator(*args))

    @staticmethod
    def CreateComparator(*args):
        try:
            return _FComparator.Create(*args)
        except ValueError as e:
            raise ValueError('Failed to create comparator. Reason: {0}'.format(e))

    @staticmethod
    def CreateFilterMethod(name):
        return FFilterMethod(name)

    @staticmethod
    def CreateFilterColumn(name, sheetType='FPortfolioSheet',
        context=acm.GetDefaultContext()):
        return FFilterColumn(name, sheetType, context)

    @staticmethod
    def SaveFilter(dlgOutput, name):
        outputString = FFilter.DialogOutputToString(dlgOutput)
        if (acm.FColumnFilter[name] == None):
            FFilter.CreateColumnFilter(name, outputString)
        else:
            FFilter.UpdateColumnFilter(name, outputString)

    @staticmethod
    def DialogOutputToString(dlgOutput):
        output = []
        for item in dlgOutput:
            temp = []
            for word in item:
                if word is not None:
                    temp.append(str(word))
                else:
                    temp.append('')
            output.append(temp)
        return output.__repr__()


    @staticmethod
    def CreateColumnFilter(name, outputString):
        newFColumnFilter = acm.FColumnFilter()
        newFColumnFilter.Name(name)
        newFColumnFilter.Text(outputString)
        newFColumnFilter.Commit()

    @staticmethod
    def UpdateColumnFilter(name, outputString):
        FColumnFilter = acm.FColumnFilter[name]
        FColumnFilter.Text(outputString)
        FColumnFilter.Commit()

    @classmethod
    def LoadFilter(cls, name):
        filterData = cls.FilterDataAsList(name)
        filterData = [row[1:] for row in filterData if row[0]=='True']
        comparator = cls.ComparatorParts(filterData)
        return cls.CreateFromComparator(*comparator)

    @staticmethod
    def FilterDataAsList(name):
        dlgOutputString = acm.FColumnFilter[name].Text()
        return ast.literal_eval(dlgOutputString)

    @staticmethod
    def DeleteFilter(name):
        acm.FColumnFilter[name].Delete()

    @classmethod
    def ComparatorParts(cls, dlgOutput):
        #[Comparator(attr=Security Loan Bid Rate, comparisonOp=BETWEEN,
        #                     minValue='50', maxValue='100', logicalOp=None)]
        parts = []
        for attr, comparisonOp, minValue, maxValue, logicalOp in dlgOutput:
            parts.append(
                cls._GetComparator(
                    cls.CreateFilterColumn(attr),
                    comparisonOp,
                    minValue,
                    maxValue)
                )
            if logicalOp: parts.append(logicalOp)
        #print "parts:",parts
        return parts

    @classmethod
    def _GetComparator(cls, filterColumn, op, minVal, maxVal):
        if str(op) in ('<', '<='):
            args = (filterColumn, op, maxVal)
        elif str(op) == 'BETWEEN':
            args = (filterColumn, op, minVal, maxVal)
        else:
            args = (filterColumn, op, minVal)
        return cls.CreateComparator(*args)


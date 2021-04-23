""" Compiled: 2020-09-18 10:38:53 """

#__src_file__ = "extensions/limits/./etc/FLimitTemplate.py"
"""--------------------------------------------------------------------------
MODULE
    FLimitTemplate

    (c) Copyright 2013 SunGard FRONT ARENA. All rights reserved.

DESCRIPTION
    Functionality for the creation and application of limit templates.

-----------------------------------------------------------------------------"""
import acm
import FAssetManagementUtils
import FLimitUtils
import FGrouperUtils
from FCalculationSpaceUtils import SpaceCollection

logger = FAssetManagementUtils.GetLogger()

EXTENSION_GROUP = 'limits'
EXTENSION_GROUP_ITEM = 'templates'
GROUPER_SUBJECTS = {
    # Default subject is acm.FInstrumentAndTradesGrouperSubject; map others
    acm.FLimitSplitGrouper: acm.FLimitGrouperSubject,
    }
COLUMN_PARAM_SEPARATOR = ';'
COLUMN_PARAM_KEY_VALUE_SEPARATOR = ','

def GetLimitTemplates(sheetType):
    templates = []
    extensions = acm.GetDefaultContext().GetAllExtensions('FParameters', 'FObject',
            True, True, EXTENSION_GROUP, EXTENSION_GROUP_ITEM, False)
    for ext in extensions:
        try:
            if ext.Value().GetString('Sheet Class', '') == sheetType:
                templates.append(FLimitTemplate.CreateFromExtension(ext.Name()))
        except ValueError as e:
            logger.error('Failed to load limit template "%s": %s' % (ext.Name(), e))
    return templates


class FLimitTemplate(object):
    # pylint: disable-msg=R0902,R0904

    _PARAMETERS = (
        'Description',
        'Limit Specification Name',
        'Transform Function',
        'Column Parameters',
        'Comparison Operator',
        'Warning Value',
        'Threshold',
        'Percentage Warning',
        'Column Name',
        'Grouper Name',
        'Grouper Subject Class',
        'Grouper Definition',
        'Path',
        'Sheet Class',
        'SubLevel',
        'Protection',
        'CalculationEnvironment'
        )

    def __init__(self, name=''):
        # Use CreateFromLimit/CreateFromExtension to create instances
        self._name = name
        self._description = ''
        self._limitSpecificationName = ''
        self._transformFunction = 'Value'
        self._columnParameters = ''
        self._comparisonOperator = 'Greater'
        self._warningValue = 0
        self._threshold = 0
        self._percentageWarning = False
        self._columnName = ''
        self._grouperName = ''
        self._grouperDefinition = list()
        self._grouperSubjectClass = 'FInstrumentAndTradesGrouperSubject'
        self._path = list()
        self._sheetClass = 'FPortfolioSheet'
        self._subLevel = 0
        self._protection = 0
        self._calcEnv = None

    def Name(self, name=None):
        if name is None:
            return self._name
        self._name = name

    def Description(self, description=None):
        if description is None:
            return self._description
        self._description = description

    def LimitSpecificationName(self, limitSpecificationName=None):
        if limitSpecificationName is None:
            return self._limitSpecificationName
        self._limitSpecificationName = limitSpecificationName

    def TransformFunction(self, transformFunction=None):
        if transformFunction is None:
            return self._transformFunction
        self._transformFunction = transformFunction

    def ComparisonOperator(self, comparisonOperator=None):
        if comparisonOperator is None:
            return self._comparisonOperator
        self._comparisonOperator = comparisonOperator

    def WarningValue(self, value=None):
        if value is None:
            return self._warningValue
        self._warningValue = value

    def Threshold(self, value=None):
        if value is None:
            return self._threshold
        self._threshold = value

    def PercentageWarning(self, percentageWarning=None):
        if percentageWarning is None:
            return self._percentageWarning
        self._percentageWarning = percentageWarning

    def ColumnName(self, columnName=None):
        if columnName is None:
            return self._columnName
        self._columnName = columnName

    def GrouperName(self, grouperName=None):
        if grouperName is None:
            return self._grouperName
        self._grouperName = grouperName

    def GrouperSubjectClass(self, grouperSubjectClass=None):
        if grouperSubjectClass is None:
            return self._grouperSubjectClass
        self._grouperSubjectClass = grouperSubjectClass

    def GrouperDefinition(self, grouperDefinition=None):
        if grouperDefinition is None:
            return self._grouperDefinition
        self._grouperDefinition = grouperDefinition

    def ColumnParameters(self, columnParameters=None):
        if columnParameters is None:
            return self._columnParameters
        self._columnParameters = columnParameters

    def Grouper(self):
        grouper = None
        if self.GrouperName():
            grouper = self._GetGrouper(
                    self.GrouperName(),
                    self.GrouperSubjectClass())
        if not grouper and self.GrouperDefinition():
            grouper = self._GetGrouperFromDefinition(
                    self.GrouperDefinition(),
                    self.GrouperName(),
                    self.GrouperSubjectClass())
        return grouper

    def Path(self, path=None):
        if path is None:
            return self._path
        self._path = path

    def SheetClass(self, sheetClass=None):
        if sheetClass is None:
            return self._sheetClass
        self._sheetClass = sheetClass

    def SubLevel(self, subLevel=None):
        if subLevel is None:
            return self._subLevel
        self._subLevel = subLevel
    
    def CalculationEnvironment(self, calcEnv=None):
        if calcEnv is None:
            return self._calcEnv
        self._calcEnv = calcEnv

    def Protection(self, protection=None):
        if protection is None:
            return self._protection
        self._protection = protection

    def Validate(self):
        if '.' in self.Name() or '=' in self.Name():
            raise ValueError('Name contains invalid characters')
        if not self.ColumnName():
            raise ValueError('Column name must be set')
        if not FLimitUtils.IsSupportedSheetClass(self.SheetClass()):
            raise ValueError('Invalid or unsupported sheet class type')
        if self.GrouperName():
            if not self.GrouperSubjectClass():
                raise ValueError('Grouper subject class must be defined if a grouper is set')
            cls = acm.FClass[str(self.GrouperSubjectClass())]
            if not cls or not cls.IsClass() or not cls.IncludesBehavior(acm.FGrouperSubject):
                raise ValueError('Invalid grouper subject class')
        if self.SubLevel() < 0:
            raise ValueError('Sub-level must be a positive number')
        if self.Protection() < 0:
            raise ValueError('Protection must be a positive number')
        if self.ComparisonOperator() not in acm.FEnumeration['enum(ComparisonType)'].Values():
            raise ValueError('Invalid comparison operator type')
        if self.PercentageWarning() and not (0 <= self.WarningValue() <= 100):
            raise ValueError('WarningValue must be a valid percentage (0-100)')
        if self.CalculationEnvironment():
            if acm.FStoredCalculationEnvironment[self.CalculationEnvironment()] is None:
                raise ValueError('Invalid Stored Calculation Environment')

    def Apply(self, portfolioObject, limitSpec=None):
        self.Validate()
        if not portfolioObject:
            raise ValueError('Invalid sheet insertable portfolio object')
        limitSpec = limitSpec or acm.FLimitSpecification[self.LimitSpecificationName()]
        if not limitSpec:
            raise ValueError('Unable to load limit specification')
        limitTarget = self.SetupLimitTarget(portfolioObject)
        limit = limitSpec.CreateLimit(limitTarget)
        self.ApplyToLimit(limit)
        return limit

    def ApplyToLimit(self, limit):
        attrs = ('TransformFunction', 'PercentageWarning', 'ComparisonOperator',
                 'WarningValue', 'Threshold')
        for attr in attrs:
            setterFunc = getattr(limit, attr)
            setterFunc(getattr(self, attr)())

    def Configuration(self):
        if self._columnParameters:
            return acm.SheetColumn.ConfigurationFromColumnParameterDefinitionNamesAndValues(self._ColumnParametersDictionaryFromString(self._columnParameters))
        return None

    def AsDictionary(self):
        self.Validate()
        dictionary = acm.FDictionary()
        for param in self._PARAMETERS:
            dictionary.AtPut(param, self._ParameterValue(param))
        return dictionary
        
    def _ParameterValue(self, param):
        value = self._GetAccessor(param)()
        if type(value) is list:
            value = ','.join(value)
        return value
        
    def SaveToModule(self, module, context=None):
        if not self.Name():
            raise ValueError('Cannot save limit template without a name')
        if not module or not module.IsKindOf(acm.FExtensionModule):
            raise ValueError('Invalid extension module "%s"' % str(module))
        self.Validate()
        
        attributes = ''.join('  %s=%s\n' % \
                (param, self._ParameterValue(param)) for param in self._PARAMETERS)
        extension = 'FObject:%s =\n%s\n' % (self.Name(), attributes)

        if not context:
            context = acm.GetDefaultContext()
            if module not in context.Modules():
                context.AddModule(module)
                context.Commit()

        context.EditImport('FParameters', extension, True, module)
        module.AddGroupItem(EXTENSION_GROUP, EXTENSION_GROUP_ITEM)
        module.AddMember(self.Name(), 'FParameters', EXTENSION_GROUP, EXTENSION_GROUP_ITEM)
        module.Commit()
        
    def SpaceParams(self):
        return type('Params', (object,), {'SheetClass': self.SheetClass})()

    def SetupLimitTarget(self, portfolioObject):
        space = SpaceCollection.GetSpace(self.SpaceParams())
        topNode = space.InsertItem(portfolioObject, self.Grouper())
        node = self._GetTargetNode(topNode)
        calc = space.CreateCalculation(node.Tree(), self.ColumnName(), self.Configuration())
        limitTarget = self._CreateLimitTarget(calc)
        limitTarget.SubLevel(self.SubLevel())
        limitTarget.CalculationEnvironment(self.CalculationEnvironment() or None)
        return limitTarget

    def __repr__(self):
        return str(self.Name())

    def __str__(self):
        attributes = ''.join('  %s = %s\n' % \
                (attr[0].lower() + attr[1:].replace(' ', ''), \
                 self._GetAccessor(attr)() or '<none>') \
                for attr in self._PARAMETERS)
        return "'%s' : %s\n%s" % (self.Name(), self.__class__.__name__, attributes)

    def _GetAccessor(self, parameter):
        valueFunc = getattr(self, parameter.replace(' ', ''))
        assert callable(valueFunc)
        return valueFunc

    def _CreateLimitTarget(self, calc):
        if self.Path():
            pathAsString = ','.join(self.Path())
            return acm.Limits.CreateLimitTargetFromPath(calc, pathAsString)
        return acm.Limits.CreateLimitTarget(calc)

    def _GetTargetNode(self, topNode):
        node = topNode.Iterator()
        if self.Path():
            try:
                for constraint in self.Path():
                    node = node.Find(constraint)
                    if not node:
                        path = topNode.StringKey() + ' / ' + ' / '.join(self.Path())
                        raise ValueError('Required path "%s" does not exist' % path)
            except ValueError as err:
                logger.debug('{0}. Creating target from template path'.format(err))
                node = topNode.Iterator()
        return node

    @classmethod
    def IsValidForTemplate(cls, limit):
        limitTarget = limit.LimitTarget()
        return (limitTarget and
                limitTarget.CalculationSpecification() and
                limitTarget.TreeSpecification() and
                not (limitTarget.TreeSpecification().Constraints() and
                     acm.Limits.ConstraintDenominatorOrSource(limitTarget.TreeSpecification().Constraints())) and
                (not limitTarget.ProjectionParts() or
                     limitTarget.ProjectionParts().IsEmpty()) and
                FLimitUtils.IsSupportedSheetClass(limitTarget.SheetType()) and
                not limit.Parent()
                )
                
    @classmethod
    def _FormattedColumnParameters(cls, limitTarget):
        try:
            params = limitTarget.CalculationSpecification().Configuration().ParamDict()
        except AttributeError:
            pass
        else:
            ckey = acm.FSymbol('columnParameters')
            if params.HasKey(ckey):
                return cls._ColumnParametersStringFromDictionary(params.At(ckey))
        return ''
        
    @classmethod
    def _ColumnParametersStringFromDictionary(cls, params):
        def ColumnParameterString(key, val):
            returnVal = str(key) + COLUMN_PARAM_KEY_VALUE_SEPARATOR
            try:
                returnVal += val.StringKey()
            except AttributeError:
                returnVal += val
            return returnVal
            
        paramList = [ColumnParameterString(k, params.At(k)) for k in params.Keys()]
        return COLUMN_PARAM_SEPARATOR.join(paramList)

    @classmethod
    def _ColumnParametersDictionaryFromString(cls, paramsString):
        d = acm.FDictionary()
        for s in paramsString.split(COLUMN_PARAM_SEPARATOR):
            pair = acm.GetFunction('symbol', 1)(s.split(COLUMN_PARAM_KEY_VALUE_SEPARATOR))
            d.AtPut(pair[0], pair[1])
        return d

    @classmethod
    def CreateFromLimit(cls, limit):
        if not cls.IsValidForTemplate(limit):
            raise ValueError('Invalid limit for limit template')
        t = cls()
        t.LimitSpecificationName(limit.LimitSpecification().Name())
        t.TransformFunction(limit.TransformFunction().Name())
        t.ComparisonOperator(limit.ComparisonOperator())
        t.WarningValue(limit.WarningValue())
        t.Threshold(limit.Threshold())
        t.PercentageWarning(limit.PercentageWarning())
        limitTarget = limit.LimitTarget()
        if limitTarget.CalculationSpecification().Configuration():
            logger.debug('Warning: Limited support for reproducing column configurations '
                        ' using a template.')
        t.ColumnName(limitTarget.CalculationSpecification().ColumnName())
        t.ColumnParameters(cls._FormattedColumnParameters(limitTarget))
        t.GrouperName(limitTarget.TreeSpecification().Grouper().DisplayName() if \
                limitTarget.TreeSpecification().Grouper() else '')
        t.GrouperSubjectClass(limitTarget.TreeSpecification().GroupingSubjectClass())
        t.GrouperDefinition(cls._GetGrouperDefinition(limit))
        path = FLimitUtils.ConstraintsArray(limit)
        path = [str(p) for p in path if p and not str(p).startswith('<Any ')]
        t.Path(path[1:])
        t.SheetClass(limitTarget.SheetType())
        t.SubLevel(limitTarget.SubLevel())
        t.Protection(limit.Protection())
        t.Validate()
        return t

    @classmethod
    def CreateFromExtension(cls, name, extensionContainer=None):
        # pylint: disable-msg=W0212
        if not extensionContainer:
            extensionContainer = acm.GetDefaultContext()
        extension = extensionContainer.GetExtension('FParameters', 'FObject', name)
        if not extension:
            raise ValueError('Failed to load extension ' + str(name))
        return cls.CreateFromDefinition(name, extension.Value())

    @classmethod
    def CreateFromDefinition(cls, name, definition):
        # pylint: disable-msg=W0212
        t = cls(name)
        for param in cls._PARAMETERS:
            accessorFunc = t._GetAccessor(param)
            attributeValue = t._GetParameterValue(definition, param, accessorFunc())
            accessorFunc(attributeValue)
        t.Validate()
        return t

    @classmethod
    def _GetParameterValue(cls, definition, parameter, defaultValue):
        try:
            attributeType = type(defaultValue)
            if attributeType in (list, tuple):
                value = [str(s).strip() for s in definition.GetArray(parameter)]
            elif attributeType in (int, float):
                value = definition.GetNumber(parameter)
            elif attributeType == bool:
                value = definition.GetBool(parameter)
            else:
                value = str(definition.GetString(parameter, defaultValue)).strip()
            if value is None:
                value = defaultValue
            return value
        except RuntimeError as e:
            raise ValueError('Invalid FParameter value for "%s": %s' %  (parameter, e))

    @classmethod
    def _GetGrouper(cls, name, subjectClass):
        if isinstance(subjectClass, basestring):
            subjectClass = acm.FClass[subjectClass]
        return (cls._GetGrouperFromStoredGroupers(name, subjectClass) or
                acm.Risk.GetGrouperFromName(name, subjectClass) or
                cls._GetGrouperFromMethodName(name, subjectClass))

    @classmethod
    def _GetGrouperFromStoredGroupers(cls, name, subjectClass):
        grouper = None
        storedName = str(name)[:31]
        storedGroupers = acm.FStoredPortfolioGrouper.Select('')
        for sg in storedGroupers.SortByProperty('CreateTime'):
            if (sg.Name() == storedName and
                FGrouperUtils.GetGrouperSubjectClass(sg.Grouper()) == subjectClass):
                grouper = sg.Grouper()
                if sg.User() == acm.User():
                    break
        return grouper

    @classmethod
    def _GetGrouperFromMethodName(cls, name, subjectClass):
        try:
            if cls._IsValidMethodChain(name, subjectClass):
                grouper = acm.FAttributeGrouper()
                grouper.SubjectClass(subjectClass)
                grouper.Method(name)
                grouper.Label(name)
                return grouper
        except RuntimeError:
            pass

    @staticmethod
    def _IsValidMethodChain(methodChain, subjectClass):
        try:
            acmClass = subjectClass
            methodChain = methodChain.split('.')

            for m in methodChain:
                method = acmClass.GetMethod(m, 0)
                if method:
                    acmClass = method.Domain()
                else:
                    raise ValueError
        except StandardError:
            return False
        return True

    @classmethod
    def _GetGrouperDefinition(cls, limit):
        definition = []
        grouper = limit.LimitTarget().TreeSpecification().Grouper()
        if grouper:
            if grouper.IsKindOf(acm.FChainedGrouper):
                definition.extend([FGrouperUtils.GetGrouperName(g) for g in grouper.Groupers()])
            else:
                definition.append(FGrouperUtils.GetGrouperName(grouper))
        return definition

    @classmethod
    def _GetGrouperFromDefinition(cls, definition, name, subjectClass):
        groupers = (cls._GetGrouper(groupName, subjectClass) \
                for groupName in definition)
        groupers = [g for g in groupers if g]
        if len(groupers) == len(definition):
            if len(groupers) > 1:
                grouper = acm.FChainedGrouper(groupers)
                grouper.Label(name)
                return grouper
            elif groupers:
                return groupers[0]
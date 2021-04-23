""" Compiled: 2020-09-18 10:38:50 """

#__src_file__ = "extensions/AMUtils/./etc/FParameterValidator.py"
from FValidator import Validator, ValidationError
from FParameterSettings import ParameterSettingsCreator
import types


class ParameterValidator(Validator):

    @classmethod
    def Object(cls, obj):
        if isinstance(obj, AttributeValue):
            return obj.Object()
        try:
            return ParameterSettingsCreator.FromRootParameter(obj) if isinstance(obj, str) else obj
        except AttributeError:
            raise ValueError('FParameter does not exist')

    @classmethod
    def GetType(cls, parameter):
        raise NotImplementedError('GetType is required in class {0}', cls.__name__)

    @classmethod
    def CreateError(cls, errorMsg, obj, errorLevel=None, **kwargs):
        return ParameterValidationError(errorMsg, obj, errorLevel, **kwargs)

    @classmethod
    def _ValidateListAttribute(cls, parameter, listName, allowEmpty=False, required=True):
        errors = cls._ErrorList(parameter, None)
        if required and not hasattr(parameter, listName):
            errors.AddError('{0} parameter requires "{1}"'.format(parameter.Name(), listName))
            return errors
        attribute = getattr(parameter, listName)()
        if allowEmpty and isinstance(attribute, str) and attribute == '':
            return errors
        if not isinstance(attribute, types.GeneratorType):
            if allowEmpty:
                errors.AddError('{0} is required to be empty or a semi-colon separated list'.format(listName))
            else:
                errors.AddError('{0} is required to be a semi-colon separated list'.format(listName))

        return errors

    @classmethod
    def _ValidateAttribute(cls, parameter, attributeName, allowEmpty=False, required=True):
        errors = cls._ErrorList(parameter, None)
        if required and not hasattr(parameter, attributeName):
            errors.AddError('{0} parameter requires "{1}"'.format(parameter.Name(), attributeName))
            return errors
        if hasattr(parameter, attributeName):
            attribute = getattr(parameter, attributeName)
            if allowEmpty and isinstance(attribute, str) and attribute == '':
                return errors

        return errors

class AttributeValue(object):
    def __init__(self, obj):
        self._obj = obj

    def Object(self):
        return self._obj


class ParameterTreeValidator(ParameterValidator):

    DO_NOT_EXPAND = ('Commit', 'Name', 'Dispatcher')

    @classmethod
    def GetType(cls, parameter):
        raise NotImplementedError('GetType is required in class {0}', cls.__name__)

    @classmethod
    def ValidTypesForSource(cls, sourceChain):
        raise NotImplementedError('GetType is required in class {0}', cls.__name__)

    @classmethod
    def ValidateRecursively(cls, parameter, rootSource=None):
        if rootSource is None:
            return [ValidationError('No root source', parameter)]
        return cls._ValidateRecursivly(cls.Object(parameter), [rootSource])

    @classmethod
    def _ValidateRecursivly(cls, parameter, sourceChain, visited=None, errors=None, globalVisited=None):
        localErrors = cls._ErrorList(parameter, None)
        visited = set() if visited is None else visited
        globalVisited = set() if globalVisited is None else globalVisited
        errors = list() if errors is None else errors

        parameterName = parameter.Name() if cls.IsParameter(parameter) else None

        if parameterName in visited:
            localErrors.AddError('Recursive parameter from attribute {0}'.format(sourceChain[-1]),
                                 ParameterValidationError.WARN)
            errors.extend(localErrors)
            return errors
        elif parameterName:
            visited.add(parameter.Name())

        if not parameterName in globalVisited:
            validTypes = cls.ValidTypesForSource(sourceChain)
            errors.extend(cls.Validate(AttributeValue(parameter), validTypes))
            if parameterName:
                globalVisited.add(parameter.Name())

        for (attributeName, attribute) in cls.ParameterAttributes(parameter):
            sourceChain.append(attributeName)
            if isinstance(attribute, types.GeneratorType):
                for listItem in attribute:
                    newVisited = set(visited)
                    newSourceChain = list(sourceChain)
                    cls._ValidateRecursivly(listItem, newSourceChain, newVisited, errors)
            else:
                newVisited = set(visited)
                cls._ValidateRecursivly(attribute, sourceChain, newVisited, errors)
        return errors



    @classmethod
    def ParameterAttributes(cls, parameter):
        if not cls.IsParameter(parameter):
            raise StopIteration
        for attributeName in (name for name in dir(parameter)
                              if not name.startswith('_')
                              and not name in cls.DO_NOT_EXPAND):
            attributeFunc = getattr(parameter, attributeName)
            if callable(attributeFunc):
                attribute = attributeFunc()
                if cls.IsValidAttribute(attribute):
                    yield (attributeName, attribute)
            else:
                continue

    @classmethod
    def IsParameter(cls, parameter):
        return parameter.__class__.__module__ == 'FParameterSettings' and hasattr(parameter, 'Name')

    @classmethod
    def IsValidAttribute(cls, attribute):
        return isinstance(attribute, (str, bool, int, int, types.GeneratorType)) or cls.IsParameter(attribute)


class ParameterValidationError(ValidationError):

    def __init__(self, errorMsg, obj, errorLevel=None, **kwargs):
        self._sourceChain = None
        if 'sourceChain' in kwargs:
            self._sourceChain = kwargs['sourceChain']
        ValidationError.__init__(self, errorMsg, obj, errorLevel=errorLevel, **kwargs)

    def FormatObject(self):
        return 'Attribute:'+self.Object() if isinstance(self.Object(), str) else 'Parameter:'+self.Object().Name()

    def SourceChain(self):
        return self._sourceChain





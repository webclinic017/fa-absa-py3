""" Compiled: 2020-09-18 10:38:50 """

#__src_file__ = "extensions/AMUtils/./etc/FValidator.py"
import collections

class ValidationError(object):

    INFO = 0
    WARN = 1
    ERROR = 2
    FATAL = 3

    def __init__(self, errorMsg, obj, errorLevel=None, **kwargs):
        self._errorMsg = errorMsg
        self._obj = obj
        if errorLevel is None:
            self._errorLevel = self.ERROR
        else:
            self._errorLevel = errorLevel
        self._additionalArguments = kwargs

    def FormatObject(self):
        return str(self.Object())

    def LongMessage(self):
        return self.FormatErrorMessage()

    def FormatErrorMessage(self):
        errorLevel = {self.INFO:'INFO', self.WARN:'WARN', self.ERROR:'ERROR', self.FATAL:'FATAL'}[self.ErrorLevel()]
        return '{0} {1}: {2}'.format(errorLevel, self.FormatObject(), self.ErrorMessage())

    def __str__(self):
        return self.FormatErrorMessage()

    def ErrorMessage(self):
        return self._errorMsg

    def Object(self):
        return self._obj

    def ErrorLevel(self):
        return self._errorLevel




class ErrorList(list):
    def __init__(self, parameter, sourceChain=None, errorClass=ValidationError):
        list.__init__(self)
        self._parameter = parameter
        self._sourceChain = sourceChain
        self._errorClass = errorClass

    def AddError(self, msg, errorLevel=None, **kwargs):
        error = self._errorClass(msg, self._parameter, errorLevel, **kwargs)
        self.append(error)



class Validator(object):

    @classmethod
    def Validate(cls, obj, validObjectTypes=None):
        errors = []
        if isinstance(validObjectTypes, str):
            validObjectTypes = [validObjectTypes]
        elif isinstance(validObjectTypes, collections.Iterable):
            validObjectTypes = list(validObjectTypes)
        else:
            validObjectTypes = None
        try:
            obj = cls.Object(obj)
        except Exception as e:
            return [cls.CreateError(str(e), obj)]

        objType = cls.GetType(obj)
        if not objType:
            return [cls.CreateError('No Type', obj)]
        elif validObjectTypes is not None and not objType in validObjectTypes:
            return [cls.CreateError('Type "{0}" is not in the valid object types {1}'.format(objType, validObjectTypes), obj)]
        try:
            #Should use a deque or something instead
            function = getattr(cls, 'Validate'+objType)
            
        except AttributeError:
            return [cls.CreateError('Validator function "{0}" available'.format('Validate'+objType), obj, ValidationError.WARN)]
        try:
            errors.extend(function(obj))
        except Exception as e:
            
            return [cls.CreateError('Could not run validator function {0}: {1}'.format('Validate'+objType, e), obj)]

        return errors

    @classmethod
    def CreateError(cls, errorMsg, obj, errorLevel=None, **kwargs):
        return ValidationError(errorMsg, obj, errorLevel, **kwargs)

    @classmethod
    def GetType(cls, parameter):
        return type(parameter).__name__

    @classmethod
    def Object(cls, obj):
        return obj

    @classmethod
    def _ErrorList(cls, parameter, sourceChain):
        return ErrorList(parameter, sourceChain, cls.CreateError)





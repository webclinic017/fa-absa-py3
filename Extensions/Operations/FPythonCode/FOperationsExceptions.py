""" Compiled: 2020-09-18 10:38:53 """

#__src_file__ = "extensions/operations/etc/FOperationsExceptions.py"
import exceptions

#-------------------------------------------------------------------------
class WrapperException(Exception):

    def __init__(self, message, innerException = None):
        super(WrapperException, self).__init__(message)
        self.__innerException = innerException

    def __str__(self):
        string = Exception.__str__(self)
        if self.__innerException:
            string += ' %s' % (self.__innerException)
        return string

    def GetInnerException(self):
        return self.__innerException

#-------------------------------------------------------------------------
class AMBAMessageException(WrapperException):
    def __init__(self, message, innerException = None):
        super(AMBAMessageException, self).__init__(message, innerException)

#-------------------------------------------------------------------------
class AMBConnectionException(WrapperException):
    def __init__(self, message, innerException = None):
        super(AMBConnectionException, self).__init__(message, innerException)

#-------------------------------------------------------------------------
class CommitException(exceptions.Exception):
    def __init__(self, args = None):
        super(CommitException, self).__init__(args)

#-------------------------------------------------------------------------
class ExtensionNotFoundException(exceptions.Exception):
    def __init__(self, args = None):
        super(ExtensionNotFoundException, self).__init__(args)
        
#-------------------------------------------------------------------------
class IncorrectMethodException(exceptions.Exception):
    def __init__(self, args = None):
        super(IncorrectMethodException, self).__init__(args)
        
#-------------------------------------------------------------------------
class InvalidHookException(exceptions.Exception):
    def __init__(self, args = None):
        super(InvalidHookException, self).__init__(args)

#-------------------------------------------------------------------------
class InvalidInputException(exceptions.Exception):
    def __init__(self, args = None):
        super(InvalidInputException, self).__init__(args)
        
#-------------------------------------------------------------------------
class MessageConversionException(WrapperException):
    def __init__(self, message, innerException = None):
        super(MessageConversionException, self).__init__(message, innerException)

#-------------------------------------------------------------------------        
class ParameterModuleException(exceptions.Exception):
    def __init__(self, args = None):
        super(ParameterModuleException, self).__init__(args)
        
#-------------------------------------------------------------------------
class UnSupportedObjectException(exceptions.Exception):
    def __init__(self, args = None):
        super(UnSupportedObjectException, self).__init__(args)

#-------------------------------------------------------------------------
class UpdateCollisionException(exceptions.Exception):
    def __init__(self, args = None):
        super(UpdateCollisionException, self).__init__(args)

#-------------------------------------------------------------------------
class ObjectModifierException(exceptions.Exception):
    def __init__(self, args = None):
        super(ObjectModifierException, self).__init__(args)

        
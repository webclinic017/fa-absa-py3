""" Compiled: 2020-09-18 10:38:51 """

#__src_file__ = "extensions/business_data_upload/etc/FBusinessDataPropertyMapper.py"
import acm

class PropertyMapper(object):

    def __init__(self, className, methodName):
        self._className = className
        self._acmClass = acm.GetClass(className)
        if not self._acmClass:
            raise TypeError('There is no ACM class called %s' % className)
        if methodName.find('.') > -1:
            raise TypeError('Can not have method chains like %s, only attributes directly on %s' % (methodName, className))
        self._methodName = methodName

    def GetDomain(self):
        NUMBER_OF_PARAMETERS = 1
        domain = None
        method = self._acmClass.GetMethod(self._methodName, NUMBER_OF_PARAMETERS)
        if not method:
            raise TypeError('No set method %s.%s taking %d argument(s)' % (self._className, self._methodName, NUMBER_OF_PARAMETERS))

        setParameter = method.Operands()[NUMBER_OF_PARAMETERS]
        if setParameter:
            domain = setParameter.Domain()
        return domain

    def GetValue(self, inputValue):
        result = inputValue
        domain = self.GetDomain()
        if not domain:
            raise TypeError('Could not get ACM domain for %s.%s. Method not a set method or does not take exactly 1 argument?' % (self._className, self._methodName))
        try:
            # Parsing an object on the FDateTimeDomain, makes the time to be adjusted to UTC.
            # We want local time.
            if not (str(domain) == 'datetime'):
                if domain.IsClass():
                    result = domain[inputValue]
                else:
                    result = domain.ParseObject(inputValue)

        except RuntimeError as e:
            raise TypeError('Could not parse %s.%s(%s) on the domain %s: %s' % (self._className, self._methodName, str(inputValue), str(domain), e))
        return result

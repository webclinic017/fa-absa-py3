""" Compiled: 2020-09-18 10:38:53 """

#__src_file__ = "extensions/operations/etc/FOperationsMethodChainParser.py"
import acm

from FOperationsExceptions import IncorrectMethodException

#-------------------------------------------------------------------------
def ParseAttributeMethodChain(domainsInPath, domain, methodChain, depth):
    assert(domain)

    if len(methodChain) > depth:
        methodName = methodChain[depth]
        method, attribute = ParseMethod(methodName, domain, checkAttribute=True)

        if attribute:
            if str(attribute.Domain().Name()) in domainsInPath:
                return ParseAttributeMethodChain(domainsInPath, attribute.Domain(), methodChain, depth+1)
            else:
                if ValidateRest(methodChain[depth+1:], attribute.Domain()):
                    return methodChain[:depth+1], str(domain.Name()), attribute
                else:
                    raise IncorrectMethodException('It is not allowed to use non-unique values that are derived from other than the valid domains')
        else:
            return ParseAttributeMethodChain(domainsInPath, method.Domain(), methodChain, depth+1)
    else:
        return [], "", None

#-------------------------------------------------------------------------
def ValidateRest(rest, domain):
    if len(rest):
        methodName = rest[0]
        _, attribute = ParseMethod(methodName, domain, checkAttribute=True)

        return True if (attribute and attribute.IsUnique() and len(rest) == 1) else False
    return True

#-------------------------------------------------------------------------
def ParseMethodChain(domain, methodChain, depth=0):
    assert(domain)

    methodName = methodChain[depth]
    method, _ = ParseMethod(methodName, domain)

    if len(methodChain) - 1 > depth:
        return ParseMethodChain(method.Domain(), methodChain, depth+1)
    else:
        return method

#-------------------------------------------------------------------------
def ParseMethod(methodName, domain, checkAttribute=False):
    assert(domain)

    if methodName:
        method = domain.GetMethod(methodName, 0)

        if not method:
            raise IncorrectMethodException('The method \"%s\", with 0 arguments, was not found on domain %s' % (methodName, domain.Name()))

        if not method.IsTransparent():
            raise IncorrectMethodException('The method \"%s\" on domain %s is not declared const' % (methodName, domain.Name()))

        methodDomain = method.Domain()

        if methodDomain.IsClass() and methodDomain.IncludesBehavior(acm.FCollection):
            raise IncorrectMethodException('The method \"%s\" on domain %s returns a collection' % (methodName, domain.Name()))

        attribute = method.Attribute()

        if not checkAttribute or attribute or (methodDomain.IsClass() and methodDomain.IncludesBehavior(acm.FAdditionalInfoProxy)):
            return method, attribute
        else:
            raise IncorrectMethodException('The method \"%s\" does not map to an attribute on domain %s' % (methodName, domain.Name()))
    else:
        raise IncorrectMethodException('The method \"\" was not found on domain %s' % (domain.Name()))

#-------------------------------------------------------------------------
def ComputeKeyForObject(obj, methodChains):
    keyValues = None

    try:
        keyValues = '-'.join(CallMethodChain(methodChain, obj) for methodChain in methodChains)
    except Exception as e:
        acm.Log('Exception occurred when computing key for %s %d: %s' % (obj.ClassName(), obj.Oid(), str(e)))

    return keyValues

#-------------------------------------------------------------------------
def CallMethodChain(methodChain, obj):
    methodChain = acm.FMethodChain(methodChain)

    try:
        value = methodChain.Call([obj])
    except Exception as e:
        acm.Log('Exception occurred when trying to extract value %s from %s %d: %s' % (methodChain, obj.ClassName(), obj.Oid(), str(e)))

    return str(value) if value else ''

#-------------------------------------------------------------------------
def SetAttributeFromObj(sender, receiver, attribute):
    assert(sender and receiver and attribute)

    setMethod = attribute.SetMethod()
    getMethod = attribute.GetMethod()

    try:
        setMethod.Call([receiver, getMethod.Call([sender])])
    except Exception as e:
        acm.Log('Exception occurred when trying to extract value %s from %s %d: %s' % (attribute.Name(), sender.ClassName(), sender.Oid(), str(e)))

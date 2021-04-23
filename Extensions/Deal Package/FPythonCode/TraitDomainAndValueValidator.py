
import acm
from DealPackageUtil import IsFObject, StringKeyOrVal
from TraitUtil import AttributeException


class TraitDomainAndValueValidator():
    def __init__(self, traitBasedDealPackage):
        self._traitBasedDealPackage = traitBasedDealPackage
        self._dateTimeDomain = acm.GetDomain('datetime')
        
    def TraitBasedDealPackage(self):
        return self._traitBasedDealPackage
        
    def _ValidateEnumerationDomain(self, traitName, domain, value):
        domainIsValid = False
        try:
            domain.Enumeration(value)
            domainIsValid = True
        except:
            raise AttributeException(traitName, " value " + StringKeyOrVal(value) + " not valid in Enumeration Domain " + str(domain))
        return domainIsValid, value
        
    def _ValidateFObjectDomain(self, traitName, domain, value):
        domainIsValid = False
        try:
            if value is not None:
                if domain.IsSubtype('string') and value.IsKindOf(acm.FSymbol):
                    domainIsValid = True
                elif domain.IsSubtype('double') and value.IsKindOf(acm.FDenominatedValue):
                    domainIsValid = True
                elif value.IsKindOf(domain):
                    domainIsValid = True
            else:
                domainIsValid = True
        except Exception as e:
            raise AttributeException(traitName, " value " + StringKeyOrVal(value) + " not valid in FObject domain " + str(domain))
        return domainIsValid, value
    
    def ValOrName(self, val):
        return val.Name() if hasattr(val, 'Name') else val
        
    def UpdateValueWithParsedValue(self, traitName, domain, value):
        updateVal = True
        if domain.IsDateOrTimeDomain():
            updateVal = False
        elif (domain.IsRealDomain() or domain.IsIntegerDomain()) and (isinstance(value, float) or isinstance(value, int)):
            updateVal = False
        elif domain.IsArrayDomain():
            updateVal = False
        elif domain.IsSubtype('string') and isinstance(value, basestring):
            # We cannot parse strings starting with quotes correctly.
            # For example: '"Hello World" Foo Bar' becomes only 'Hello World'
            # This line should be removed if domain.ParseSingleValue is introduced
            updateVal = False
        return updateVal
        
    def _ValidateSimpleDomain(self, traitName, domain, value):
        domainIsValid = False
        parsedValue = 'NOT A VALUE'
        
        if self.TraitBasedDealPackage().GetAttributeMetaData(traitName, 'attributeMapping').IsDefault():
            try:
                if value is not None:
                    if isinstance(value, basestring) and hasattr(domain, 'IsKindOf') and domain.IsKindOf(acm.FPersistentClass):
                        parsedValue = domain.Select01('name = "%s"'%value, errorMessage=None)
                    else:
                        parsedValue = domain.ParseValue(value)
        
                    if parsedValue is None:
                        raise AttributeException(traitName, " value " + StringKeyOrVal(value) + " not valid in domain " + str(domain))
                    else:
                        if self.UpdateValueWithParsedValue(traitName, domain, value):
                            if value != parsedValue:
                                value = parsedValue
                domainIsValid = True
            except:
                raise AttributeException(traitName, " value " + StringKeyOrVal(value) + " not valid in domain " + str(domain))
        return domainIsValid, value 
        
    def _ValidateDomainValue(self, traitName, domain, value):
        domainIsValid = False
        if IsFObject(domain) and domain.IsKindOf(acm.FEnumeration):
            domainIsValid, value = self._ValidateEnumerationDomain(traitName, domain, value)
        elif IsFObject(value):
            domainIsValid, value = self._ValidateFObjectDomain(traitName, domain, value)
        else:
            domainIsValid, value = self._ValidateSimpleDomain(traitName, domain, value)
        return domainIsValid, value
        
    def GetValueFromParseDomainValue(self, traitName, domain, value):
        domainIsValid, parsedValue = self._ValidateDomainValue(traitName, domain, value)
        return parsedValue
       
    def _StripOutDecoratorClassAndFindOriginal(self, value):
        if IsFObject(value):
            if value.Class().IncludesBehavior(acm.FBusinessLogicDecorator):
                value = value.DecoratedObject()
            value = value.Originator()
        return value
 
    def _ValuesAreDifferent(self, traitName, previousValidationVal, validationVal):
        different = False
        if previousValidationVal != "NoVal":
            old = self._StripOutDecoratorClassAndFindOriginal(previousValidationVal) 
            new = self._StripOutDecoratorClassAndFindOriginal(validationVal)
            if not self.TraitBasedDealPackage()._TraitValuesAreEqual(new, old):
                different = True
        return different
        
    def _RaiseExceptionIfValuesAreDifferent(self, traitName, chain, previousValidationVal, validationVal):
        if self._ValuesAreDifferent(traitName, previousValidationVal, validationVal):
            previousValidationVal = previousValidationVal
            validationVal = validationVal
            name = self.TraitBasedDealPackage().DealPackage().Name()
            originator = self.TraitBasedDealPackage().DealPackage().Originator()
            if originator:
                name = originator.Name()
            error = "Deal Package %s has Inconsistent object mapping %s to attribute % s. (%s (%s) != %s (%s))"
            raise AttributeException(error % (name, chain, traitName, StringKeyOrVal(validationVal), type(validationVal), StringKeyOrVal(previousValidationVal), type(previousValidationVal)))
            
    def ValidateNewValueInDomainOfCallableMethod(self, traitName, callObject, newValue):
        domain = self.TraitBasedDealPackage()._GetDomain(traitName)
        if newValue == None and hasattr(callObject, 'IsKindOf') and callObject.IsKindOf(acm.FAdditionalInfoProxy):
            # The value None is supported for all domains if method is on AddInfoProxy
            domainIsValid = True
        else:
            domainIsValid, value = self._ValidateDomainValue(traitName, domain, newValue)
        return domainIsValid
    
    def ValidateGetTraitValue(self, traitName, chain, callableMethod, objectValue, previousValidationVal):
        validationVal = objectValue
        domain = self.TraitBasedDealPackage()._GetDomain(traitName)
        if domain and objectValue:
            validationVal = self.GetValueFromParseDomainValue(traitName, domain, objectValue)
        self._RaiseExceptionIfValuesAreDifferent(traitName, chain, previousValidationVal, validationVal)
        return validationVal
           
        

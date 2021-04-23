'''-----------------------------------------------------------------------------
PROJECT                 : Markets Message Gateway
PURPOSE                 : Creates fields used in SWIFT MT messages
DEPATMENT AND DESK      :
REQUESTER               :
DEVELOPER               : Francois Truter
CR NUMBER               : 695005
--------------------------------------------------------------------------------

HISTORY
================================================================================
Date       Change no            Developer       Description
--------------------------------------------------------------------------------
2011-03-25 686159               Francois Truter Initial Implementation
2011-06-23 695005               Francois Truter Added descriptions funcionality 
                                                to MtField35B
2011-06-29 XXXXXX               Rohan vd Walt   Fix bug where N is added to field
                                                where value is rounded to zero
2011-07-06 XXXXXX               Rohan vd Walt   Dont try to round when NumDecimals = None
2017-12-11 CHNG0005220511       Manan Gosh      DIS go-live
2018-01-25 CHG1000078148        Willie vd Bank  Modified FrontDateField to cater for milliseconds, the DIS deployment broke MT535s
2020-03-03 FAOPS-690            Ntokozo Skosana Added Account type to 97B field for DIS MT535 message
2020-05-05 FAOPS-746            Cuen Edwards    Added field 79.
'''

import acm
import copy
import math
import re
import new
import time
from gen_swift_character_sets import CharacterSetX
from gen_swift_character_sets import CharacterSetN
from gen_swift_character_sets import CharacterSetA
from gen_swift_character_sets import CharacterSetC
from gen_swift_common import CRLF
from gen_swift_common import FieldOfFields
from gen_swift_common import RepetitiveField
from gen_swift_common import ComplexFieldBase
from gen_swift_common import MtField
from gen_swift_common import MtSubField
from gen_swift_common import MtComplexField
from gen_swift_common import ComplexField
from gen_swift_common import MandatoryFieldNotSupplied

CURRENCY_DECIMALS = {'AED': 2, 'AFN': 2, 'ALL': 2, 'AMD': 2, 'ANG': 2, 'AOA': 2, 'ARS': 2, 'AUD': 2, 'AWG': 2, 
    'AZN': 2, 'BAM': 2, 'BBD': 2, 'BDT': 2, 'BGN': 2, 'BHD': 3, 'BIF': 0, 'BMD': 2, 'BND': 2, 'BOB': 2, 'BOV': 2, 
    'BRL': 2, 'BSD': 2, 'BTN': 2, 'BWP': 2, 'BYR': 0, 'BZD': 2, 'CAD': 2, 'CDF': 2, 'CHE': 2, 'CHF': 2, 'CHW': 2, 
    'CLF': 0, 'CLP': 0, 'CNY': 2, 'COP': 2, 'COU': 2, 'CRC': 2, 'CUC': 2, 'CUP': 2, 'CVE': 0, 'CZK': 2, 'DJF': 0, 
    'DKK': 2, 'DOP': 2, 'DZD': 2, 'EGP': 2, 'ERN': 2, 'ETB': 2, 'EUR': 2, 'FJD': 2, 'FKP': 2, 'GBP': 2, 'GEL': 2, 
    'GHS': 2, 'GIP': 2, 'GMD': 2, 'GNF': 0, 'GTQ': 2, 'GYD': 2, 'HKD': 2, 'HNL': 2, 'HRK': 2, 'HTG': 2, 'HUF': 2, 
    'IDR': 0, 'ILS': 2, 'INR': 2, 'IQD': 0, 'IRR': 0, 'ISK': 0, 'JMD': 2, 'JOD': 3, 'JPY': 0, 'KES': 2, 'KGS': 2, 
    'KHR': 2, 'KMF': 0, 'KPW': 0, 'KRW': 0, 'KWD': 3, 'KYD': 2, 'KZT': 2, 'LAK': 0, 'LBP': 0, 'LKR': 2, 'LRD': 2, 
    'LSL': 2, 'LTL': 2, 'LVL': 2, 'LYD': 3, 'MAD': 2, 'MDL': 2, 'MKD': 2, 'MMK': 0, 'MNT': 2, 'MOP': 1, 'MUR': 2, 
    'MVR': 2, 'MWK': 2, 'MXN': 2, 'MXV': 2, 'MYR': 2, 'MZN': 2, 'NAD': 2, 'NGN': 2, 'NIO': 2, 'NOK': 2, 'NPR': 2, 
    'NZD': 2, 'OMR': 3, 'PAB': 2, 'PEN': 2, 'PGK': 2, 'PHP': 2, 'PKR': 2, 'PLN': 2, 'PYG': 0, 'QAR': 2, 'RON': 2, 
    'RSD': 2, 'RUB': 2, 'RWF': 0, 'SAR': 2, 'SBD': 2, 'SCR': 2, 'SDG': 2, 'SEK': 2, 'SGD': 2, 'SHP': 2, 'SLL': 0, 
    'SOS': 2, 'SRD': 2, 'STD': 0, 'SYP': 2, 'SZL': 2, 'THB': 2, 'TJS': 2, 'TMT': 2, 'TND': 3, 'TOP': 2, 'TRY': 2, 
    'TTD': 2, 'TWD': 2, 'TZS': 2, 'UAH': 2, 'UGX': 0, 'USD': 2, 'USN': 2, 'USS': 2, 'UYU': 2, 'UZS': 2, 'VEF': 2, 
    'VND': 0, 'VUV': 0, 'WST': 2, 'XAF': 0, 'XCD': 2, 'XOF': 0, 'XPF': 0, 'YER': 0, 'ZAR': 2, 'ZMK': 0, 'ZWL': 2,
    'ZMW': 2
}


        
class BaseField(object):
    
    def __init__(self, _name, _mandatory, _default):
        self._name = _name
        self._mandatory = _mandatory
        self._value = _default
        
    def getValue(self):
        return self._value
        
    def setValue(self, value):
        self._value = value
    
    Value = property(getValue, setValue)
    
    @property
    def Name(self):
        return self._name
        
    @property
    def Mandatory(self):
        return self._mandatory
        
    def _validateValue(self):
        if self._value == None and self._mandatory:
            raise MandatoryFieldNotSupplied(self.Name)
            
    def __str__(self):
        self._validateValue()
        
        if self._value:
            return str(self._value)
        else:
            return ''

class CharacterField(BaseField):
    
    def __init__(self, _name, _maxLength, _charSet, _mandatory = True, _default = None):
        BaseField.__init__(self, _name, _mandatory, _default)
        self._maxLength = _maxLength
        self._charSet = _charSet
        
    def _validateValue(self):
        BaseField._validateValue(self)
        
        if self._value:
            _str = str(self._value)
            if len(_str) > self._maxLength:
                raise Exception('[%s] is too long for field [%s]: max length is [%i]' % (_str, self._name, self._maxLength))
            self._charSet.ValidateField(self)
        
class FixedCharacterField(BaseField):
    
    def __init__(self, _name, _length, _charSet, _mandatory = True, _default = None):
        BaseField.__init__(self, _name, _mandatory, _default)
        self._length = _length
        self._charSet = _charSet
        
    def _validateValue(self):
        BaseField._validateValue(self)
        
        if self._value:
            _str = str(self._value)
            if len(_str) != self._length:
                raise Exception('[%s] is not the correct length for field [%s]: length must be [%i]' % (_str, self._name, self._length))
            self._charSet.ValidateField(self)
        
class MultiLineField(BaseField):

    @staticmethod
    def splitLen(sequence, length): 
        return [sequence[i:i+length] for i in range(0, len(sequence), length)] 
    
    def __init__(self, _name, _numLines, _maxLength, _charSet, _mandatory = True, _default = None):
        BaseField.__init__(self, _name, _mandatory, _default)
        self._numLines = _numLines
        self._maxLength = _maxLength
        self._charSet = _charSet
        
    def __str__(self):
        BaseField._validateValue(self)
        
        if not self._value:
            return ''
        
        _str = str(self.Value)
        givenLines = _str.split(CRLF)
        outputLines = []
        for line in givenLines:
            newLines = MultiLineField.splitLen(line, self._maxLength)
            for newLine in newLines:
                outputLines.append(newLine)
                
        if len(outputLines) > self._numLines:
            message = 'Field [%s] can only take %i lines - %i received:' % (self.Name, self._numLines, len(outputLines))
            for line in outputLines:
                message += CRLF + line
            raise Exception(message)
        
        _str = ''
        delimiter = ''
        for line in outputLines:
            self._charSet.ValidateFieldStr(self.Name, line)
            _str += delimiter + line
            delimiter = CRLF
            
        return _str

        
class ListField(BaseField):

    def __init__(self, _name, _validValues, _mandatory = True, _default = None):
        BaseField.__init__(self, _name, _mandatory, _default)
        self._validValues = _validValues
        
    def _validValuesString(self):
        if not self._validValues:
            return ''

        _str = ''
        delimiter = ''
        for item in self._validValues:
            _str += delimiter + str(item)
            delimiter = ','

        return _str
        
    def _validateValue(self):
        BaseField._validateValue(self)
        
        if self._value and not self._value in self._validValues:
            raise Exception('%s: [%s] is not a valid value, valid values are [%s]' % (self.Name, self._value, self._validValuesString()))
            
class FrontDateField(BaseField):

    def __init__(self, _name, _format, _mandatory = True, _default = None):
        BaseField.__init__(self, _name, _mandatory, _default)
        self._format = _format
        
    def __str__(self):
        self._validateValue()
        
        if self._value:
            if isinstance(self._value, int):
                timeValue = time.localtime(self._value)
            else:
                if len(self._value) > 10:
                    if len(self._value) > 19 :
                        self._value = self._value[:19]
                    timeValue = time.strptime(self._value, '%Y-%m-%d %H:%M:%S')
                else:
                    timeValue = time.strptime(self._value, '%Y-%m-%d')
            
            return time.strftime(self._format, timeValue)
        else:
            return ''
            
class DecimalField(BaseField):

    def __init__(self, _name, _maxLength, _numDecimals, _printSign, _mandatory = True, _default = None):
        BaseField.__init__(self, _name, _mandatory, _default)
        self._maxLength = _maxLength
        self._numDecimals = _numDecimals
        self._printSign = _printSign
    
    def getNumDecimals(self):
        return self._numDecimals
    
    def setNumDecimals(self, value):
        self._numDecimals = value
        
    NumDecimals = property(getNumDecimals, setNumDecimals)
    
    def _getDecimalString(self):
        if self._numDecimals:
            value = round(abs(self._value), self._numDecimals)
        else:
            value = abs(self._value)
        _str = str(value)
            
        values = _str.split('.')
        if len(values) == 0:
            return ''
            
        _str = values[0] + ','
        if len(values) > 1 and int(values[1]) > 0:
            _str += values[1]
            
        return _str
        
    def __str__(self):
        BaseField._validateValue(self)

        if self._value is None:
            return ''
        
        _str = self._getDecimalString()

        if len(_str) > self._maxLength:
            raise Exception('[%s] is too long for field [%s]: max length is [%i]' % (_str, self._name, self._maxLength))
            
        if self._numDecimals:
            if self._printSign and round(self._value, self._numDecimals) < 0:
                _str = 'N' + _str
        else:
            if self._printSign and round(self._value, 0) < 0:
                _str = 'N' + _str
                
        return _str
        
class FixedIntegerField(BaseField):
    
    def __init__(self, _name, _length, _printSign, _mandatory = True, _default = None):
        BaseField.__init__(self, _name, _mandatory, _default)
        self._length = _length
        self._printSign = _printSign
        
    def __str__(self):
        BaseField._validateValue(self)
        
        if not self._value:
            return ''
        
        formatStr = '%' + '0%ii' % self._length
        _str = formatStr % round(abs(self._value))
        
        if len(_str) > self._length:
            raise Exception('[%s] is too long for field [%s]: max length is [%i]' % (_str, self._name, self._length))
            
        if self._printSign and self._value < 0:
            _str = 'N' + _str
            
        return _str
        
class AmountField(FieldOfFields):
    
    def __init__(self, _name, _maxLength, _printCurrency, _printSign, _mandatory = True, _default = None):
        FieldOfFields.__init__(self, _name)
        self._decimalField = DecimalField(_name, _maxLength, 2, False, _mandatory, _default)
        self._printCurrency = _printCurrency
        self._printSign = _printSign
        self._mandatory = _mandatory
        self._currency = None
    
    def getCurrency(self):
        return self._currency
    
    def setCurrency(self, value):
        self._currency = value
        
    Currency = property(getCurrency, setCurrency)
    
    def getValue(self):
        return self._decimalField.Value
        
    def setValue(self, value):
        self._decimalField.Value = value
    
    Value = property(getValue, setValue)
        
    @property
    def Mandatory(self):
        return self._mandatory
    
    def __str__(self):
        if not self._currency:
            if self._mandatory:
                raise MandatoryFieldNotSupplied(self.Name)
            else:
                return ''
        
        if not self._currency in CURRENCY_DECIMALS:
                raise NotImplementedError('MoneyField has not been implemented for currency code [%s].' % self._currency)
        
        self._decimalField.NumDecimals = CURRENCY_DECIMALS[self._currency]
        valueStr = str(self._decimalField)
        if valueStr:
            return '%(sign)s%(currency)s%(value)s' % {
                'sign': 'N' if self._printSign and round(self.Value, 2) < 0 else '',
                'currency': self._currency if self._printCurrency else '',
                'value': valueStr
            }
        else:
            return ''

class TerminalAddress(ComplexField):

    def __init__(self, _name, _mandatory):
        ComplexField.__init__(self, _name, _mandatory, [
            FixedCharacterField('BankCode', 4, CharacterSetA, True, None),
            FixedCharacterField('CountryCode', 2, CharacterSetA, True, None),
            FixedCharacterField('LocationCode', 2, CharacterSetC, True, None),
            FixedCharacterField('TerminalId', 1, CharacterSetC, True, None),
            FixedCharacterField('BranchCode', 3, CharacterSetC, True, 'XXX')
        ], '')
        
    def _setBicCode(self, value):
        value = str(value)
        valueLength = len(value)
        if valueLength != 8 and valueLength != 11:
            raise Exception('Invalid BIC code [%s] - BIC code must be 8 or 11 characters long' % value)
        
        self.BankCode = value[0:4]
        self.CountryCode = value[4:6]
        self.LocationCode = value[6:8]
        
        if valueLength == 11:
            self.BranchCode = value[8:11]
            
    BicCode = property(None, _setBicCode)
        
class BicCode(ComplexField):

    def __init__(self, _name, _mandatory, _default):
        ComplexField.__init__(self, _name, _mandatory, [
            FixedCharacterField('BankCode', 4, CharacterSetA, True, None),
            FixedCharacterField('CountryCode', 2, CharacterSetA, True, None),
            FixedCharacterField('LocationCode', 2, CharacterSetC, True, None),
            FixedCharacterField('BranchCode', 3, CharacterSetC, False, None)
        ], '')
        
        if _default:
            self._setValue(_default)
        
    def _setValue(self, value):
        value = str(value)
        valueLength = len(value)
        if valueLength != 8 and valueLength != 11:
            raise Exception('Invalid BIC code [%s] - BIC code must be 8 or 11 characters long' % value)
        
        self.BankCode = value[0:4]
        self.CountryCode = value[4:6]
        self.LocationCode = value[6:8]
        
        if valueLength == 11:
            self.BranchCode = value[8:11]
            
    Value = property(None, _setValue)
        
class RepetitiveSequence(RepetitiveField):

    def __init__(self, _name, _templateFields, _mandatory, _maxRepititions = None):
        RepetitiveField.__init__(self, _name, _mandatory)
        self._templateFields = _templateFields
        self._maxRepititions = _maxRepititions
        
    @property
    def _className(self):
        return self.Name + '_class'
        
    def _createComplexField(self):
        name = self.Name + str(self.numFields + 1)
        return new.classobj(self._className, (ComplexField,), {})(name, False, copy.deepcopy(self._templateFields), CRLF)
        
    def AddSequence(self):
        if self._maxRepititions and self.numFields >= self._maxRepititions:
            raise Exception('Maximum number of repititions [%i] has been added for field [%s]: '% (self._maxRepititions, self._name))
        
        
        sequence = self._createComplexField()
        self.appendField(sequence)
        return sequence
        
class FieldOptions(RepetitiveField):
                
    def _createField(self, option):
        className = self.__class__.__name__
        match = re.search('(?<=MtField)\d+a$', className)
        if not match:
            raise Exception('Could not create field for class %s: class name did not match the expected pattern' % className)
            
        fieldClass = 'MtField' + match.group().replace('a', option)
        field = None
        try:
            field = globals()[fieldClass]('Value', self._mandatory, self._qualifier)
        except Exception as ex:
            raise Exception('Could not instantiate class %s: %s' % (fieldClass, ex))
            
        return field
        
    def __init__(self, _name, _mandatory, _qualifier, _multiple, _allowedKeys):
        RepetitiveField.__init__(self, _name, _mandatory)
        self._mandatory = _mandatory
        self._qualifier = _qualifier
        self._multiple = _multiple
        self._allowedKeys = _allowedKeys
        
    def GetField(self, option):
        if not option in self._allowedKeys:
            raise Exception('[%(option)s] is not a valid option for field [%(field)s], valid options are: %(valid)s' %
                {'option': option, 'field': self._name, 'valid': ', '.join(self._allowedKeys)})
                
        if not self._multiple and self.numFields > 0:
            raise Exception('Field [%s] allows just one value and has already been set.' % self._name)
                
        field = self._createField(option)
        self.appendField(field)
        return field

class CurrencyField(ListField):

    def __init__(self, name, mandatory, default):
        currencies = CURRENCY_DECIMALS.keys()
        if currencies:
            currencies.sort()
        
        ListField.__init__(self, name, currencies, mandatory, default)
        
class MtField11A(MtField):
    
    def __init__(self, name, mandatory, qualifier):
        MtField.__init__(self, '11A', CurrencyField(name, mandatory, None),
            FixedCharacterField(name + '_Qualifier', 4, CharacterSetC, True, qualifier), '//')

class MtField12(MtField):

    def __init__(self, name, mandatory):
        MtField.__init__(self, '12', CharacterField(name, 16, CharacterSetX, mandatory, None))
            
class MtField12A(MtComplexField):
    
    def __init__(self, name, mandatory, qualifier):
        MtComplexField.__init__(self, '12A', name, mandatory, [
            CharacterField('DataSourceScheme', 8, CharacterSetC, False, None),
            MtSubField('/', CharacterField('Description', 30, CharacterSetX, True, None))
        ], FixedCharacterField(name + '_Qualifier', 4, CharacterSetC, True, qualifier), '/')
        
class MtField12B(MtComplexField):
    
    def __init__(self, name, mandatory, qualifier):
        MtComplexField.__init__(self, '12B', name, mandatory, [
            CharacterField('DataSourceScheme', 8, CharacterSetC, False, None),
            MtSubField('/', FixedCharacterField('Code', 4, CharacterSetC, True, None))
        ], FixedCharacterField(name + '_Qualifier', 4, CharacterSetC, True, qualifier), '/')
            
class MtField12C(MtField):

    def __init__(self, name, mandatory, qualifier):
        MtField.__init__(self, '12C', FixedCharacterField(name, 6, CharacterSetC, mandatory, None),
            FixedCharacterField(name + '_Qualifier', 4, CharacterSetC, True, qualifier), '//')
            
class MtField12a(FieldOptions):
    pass
            
class MtField13A(MtField):
    
    def __init__(self, name, mandatory, qualifier):
        MtField.__init__(self, '13A', FixedCharacterField(name, 3, CharacterSetC, mandatory, None),
            FixedCharacterField(name + '_Qualifier', 4, CharacterSetC, True, qualifier), '//')

class MtField13B(MtComplexField):

    def __init__(self, name, mandatory, qualifier):
        MtComplexField.__init__(self, '13B', name, mandatory, [
            CharacterField('DataSourceScheme', 8, CharacterSetC, False, None),
            MtSubField('/', CharacterField('Number', 30, CharacterSetX, True, None))
        ], FixedCharacterField(name + '_Qualifier', 4, CharacterSetC, True, qualifier), '//')
        
class MtField13J(MtField):
    
    def __init__(self, name, mandatory, qualifier):
        MtField.__init__(self, '13J', FixedCharacterField(name, 5, CharacterSetC, mandatory, None),
            FixedCharacterField(name + '_Qualifier', 4, CharacterSetC, True, qualifier), '//')
            
class MtField13K(MtField):
    
    def __init__(self, name, mandatory, qualifier):
        MtComplexField.__init__(self, '13K', name, mandatory, [
            FixedCharacterField('IdNumber', 3, CharacterSetC, mandatory, None),
            MtSubField('/', DecimalField('Quanitity', 15, None, False, mandatory, None))
        ], FixedCharacterField(name + '_Qualifier', 4, CharacterSetC, True, qualifier), '//')
        
class MtField13a(FieldOptions):
    pass
        
class MtField14F(MtComplexField):
    def __init__(self, name, mandatory, qualifier):
        MtComplexField.__init__(self, '14F', name, mandatory, [
            FixedCharacterField('Country', 3, CharacterSetC, mandatory, None),
            MtSubField('-', CharacterField('Source', 7, CharacterSetX, mandatory, None)),
            MtSubField('-', FixedCharacterField('PrimeSource', 4, CharacterSetC, False, None))
        ])
            
class MtField16R(MtField):
    
    def __init__(self, name, mandatory, default = None):
        MtField.__init__(self, '16R', CharacterField(name, 16, CharacterSetC, mandatory, default))
        
class MtField16S(MtField):
    
    def __init__(self, name, mandatory, default = None):
        MtField.__init__(self, '16S', CharacterField(name, 16, CharacterSetC, mandatory, default))
        
class MtField17B(MtField):
    
    def __init__(self, name, mandatory, qualifier):
        MtField.__init__(self, '17B', ListField(name, ['Y', 'N'], mandatory, None),
            FixedCharacterField(name + '_Qualifier', 4, CharacterSetC, True, qualifier), '//')

class MtField19A(MtField):
    
    def __init__(self, name, mandatory, qualifier):
        MtField.__init__(self, '19A', AmountField(name, 15, True, True, mandatory, None),
            FixedCharacterField(name + '_Qualifier', 4, CharacterSetC, True, qualifier), '//')

class MtField20(MtField):

    def __init__(self, name, mandatory):
        MtField.__init__(self, '20', CharacterField(name, 16, CharacterSetX, mandatory, None))
        
class MtField20C(MtField):

    def __init__(self, name, mandatory, qualifier):
        MtField.__init__(self, '20C', CharacterField(name, 16, CharacterSetX, mandatory, None),
            FixedCharacterField(name + '_Qualifier', 4, CharacterSetC, True, qualifier), '//'
        )
        
class MtField21(MtField):

    def __init__(self, name, mandatory):
        MtField.__init__(self, '21', CharacterField(name, 16, CharacterSetX, mandatory, None))
        
class MtField22F(MtComplexField):
    
    def __init__(self, name, mandatory, qualifier):
        MtComplexField.__init__(self, '22F', name, mandatory, [
            CharacterField('DataSourceScheme', 5, CharacterSetC, False, None),
            MtSubField('/', FixedCharacterField('Indicator', 4, CharacterSetC, True, None))
        ], FixedCharacterField(name + '_Qualifier', 4, CharacterSetC, True, qualifier), '/')
        
class MtField22H(MtField):

    def __init__(self, name, mandatory, qualifier):
        MtField.__init__(self, '22H', FixedCharacterField(name, 4, CharacterSetC, mandatory, None),
            FixedCharacterField(name + '_Qualifier', 4, CharacterSetC, True, qualifier), '//')
            
class MtField22a(FieldOptions):
    pass
        
class MtField23G(MtComplexField):
    
    def __init__(self, name, mandatory):
        MtComplexField.__init__(self, '23G', name, mandatory, [
            ListField('Function', ['CANC', 'NEWM'], mandatory, None),
            MtSubField('/', ListField('Subfunction', ['CODE', 'COPY', 'DUPL'], False, None))
        ])
        
class MtField25(MtField):
    '''This field definition doesnt fit the MT598-155 specification for it, 
        but was used originally for MT940 implementation, so leaving as is
        Usage/format within MT598 will be enforced at generation of message
    '''
    def __init__(self, name, mandatory):
        MtField.__init__(self, '25', CharacterField(name, 35, CharacterSetX, mandatory, None))
        
class MtField28C(MtComplexField):
    
    def __init__(self, name, mandatory):
        MtComplexField.__init__(self, '28C', name, mandatory, [
            CharacterField('Value', 5, CharacterSetN, True, None),
            MtSubField('/', CharacterField('SequenceNumber', 5, CharacterSetN, False, None))
        ])
        
class MtField28E(MtComplexField):

    def __init__(self, name, mandatory):
        MtComplexField.__init__(self, '28E', name, mandatory, [
            CharacterField('Value', 5, CharacterSetN, True, None),
            MtSubField('/', ListField('ContinuationIndicator', ['LAST', 'MORE', 'ONLY'], True, None))
        ])

class MtField35B_MT598(MtComplexField):

    def __init__(self, name, mandatory):
        MtComplexField.__init__(self, '35B', name, mandatory, [
            MtSubField('', MultiLineField('Description', 4, 35, CharacterSetX, False, None))
        ])

class MtField35B(MtComplexField):

    def __init__(self, name, mandatory):
        MtComplexField.__init__(self, '35B', name, mandatory, [
            MtSubField('ISIN ', FixedCharacterField('Isin', 12, CharacterSetC, False, None)),
            MtSubField(CRLF, MultiLineField('Description', 4, 35, CharacterSetX, False, None))
        ])
        
    @staticmethod
    def _trimLine(line):
        return line[0:35]

    @staticmethod
    def _getLegDescription(leg):
        description = ''
        if leg.FixedRate():
            description += '%.4f' %  leg.FixedRate()
        if leg.FloatRateReference():
            description += '%s' % CharacterSetX.RemoveInvalidCharacters(leg.FloatRateReference().Name())
        description += ' (%s%s)' % (leg.LegType(), '/' + leg.RollingPeriod() if leg.RollingPeriod() else '')
            
        return description
        
    @staticmethod
    def _getInstrumentNameAndType(instrument):
        return '%s (%s)' % (CharacterSetX.RemoveInvalidCharacters(instrument.Name()), instrument.InsType())
            
    def AssignDescriptionFromInstrument(self, instrument, isCfd):
        description = ''
        
        type = instrument.InsType()
        if type == 'Option':
            description = MtField35B._trimLine('%s%s Option' % (instrument.ExerciseType() + ' ' if instrument.ExerciseType() else '', 'Call' if instrument.IsCallOption() else 'Put'))
            description += CRLF + MtField35B._trimLine('Expires %s%s' % (instrument.ExpiryDateOnly(), (' (%s)' % instrument.SettlementType()) if instrument.SettlementType() else ''))
            description += CRLF + MtField35B._trimLine(MtField35B._getInstrumentNameAndType(instrument.Underlying()))
            description += CRLF + MtField35B._trimLine('Strike: %f (%s)' % (instrument.StrikePrice(), instrument.StrikeType()))
        elif type == 'Future/Forward':
            description = type
            description += CRLF + MtField35B._trimLine('%s%s' % (instrument.PayType() + ' ' if instrument.PayType() else '', 'Date: ' + instrument.ExpiryDateOnly()))
            description += CRLF + MtField35B._trimLine(MtField35B._getInstrumentNameAndType(instrument.Underlying()))
        elif type == 'FRA':
            description = MtField35B._trimLine('FRA %s - %s' % (instrument.StartDate(), instrument.ExpiryDateOnly()))
            for leg in instrument.Legs():
                description += CRLF + MtField35B._trimLine(MtField35B._getLegDescription(leg))
        elif type == 'Swap':
            description = 'Interest Rate Swap'
            description += CRLF + MtField35B._trimLine('%s - %s' % (instrument.StartDate(), instrument.ExpiryDateOnly()))
            description += CRLF + MtField35B._trimLine('Rec: ' + MtField35B._getLegDescription(instrument.RecLeg()))
            description += CRLF + MtField35B._trimLine('Pay: ' + MtField35B._getLegDescription(instrument.PayLeg()))
        else:
            description = MtField35B._trimLine(type + (' CFD' if isCfd else ''))
            description += CRLF + MtField35B._trimLine(CharacterSetX.RemoveInvalidCharacters(instrument.Name()) + ('/CFD' if isCfd else ''))
        
        self.Description = description

class MtField36B(MtComplexField):
    
    def __init__(self, name, mandatory, qualifier):
        MtComplexField.__init__(self, '36B', name, mandatory, [
            ListField('QuantityTypeCode', ['AMOR', 'FAMT', 'UNIT'], mandatory, None),
            MtSubField('/', DecimalField('Value', 15, None, False, mandatory, None))
        ], FixedCharacterField(name + '_Qualifier', 4, CharacterSetC, True, qualifier), '//')

class MtField60F(MtComplexField):

    def __init__(self, name, mandatory):
        MtComplexField.__init__(self, '60F', name, mandatory, [
            ListField('DebitCredit', ['D', 'C'], True, None),
            FrontDateField('Date', '%y%m%d', True, None),
            AmountField('Amount', 15, True, False, True, None)
        ])
            
class MtField61(MtComplexField):
    
    def __init__(self, name, mandatory):
        MtComplexField.__init__(self, '61', name, mandatory, [
            FrontDateField('ValueDate', '%y%m%d', True, None),
            FrontDateField('EntryDate', '%m%d', False, None),
            ListField('DebitCredit', ['D', 'C', 'RC', 'RD'], True, None),
            CharacterField('FundsCode', 1, CharacterSetA, False, None),
            AmountField('Amount', 15, False, False, True, None),
            FixedCharacterField('TransactionType', 1, CharacterSetA, True, None),
            FixedCharacterField('TransactionIdentificationCode', 3, CharacterSetC, True, None),
            CharacterField('AccountOwnerReference', 16, CharacterSetX, True, None),
            MtSubField('//', CharacterField('InstitutionReference', 16, CharacterSetX, False, None)),
            MtSubField(CRLF, CharacterField('SupplementaryDetails', 34, CharacterSetX, False, None))
        ])
        
class MtField62F(MtComplexField):

    def __init__(self, name, mandatory):
        MtComplexField.__init__(self, '62F', name, mandatory, [
            ListField('DebitCredit', ['D', 'C'], True, None),
            FrontDateField('Date', '%y%m%d', True, None),
            AmountField('Amount', 15, True, False, True, None)
        ])

class MtField64(MtComplexField):

    def __init__(self, name, mandatory):
        MtComplexField.__init__(self, '64', name, mandatory, [
            ListField('DebitCredit', ['D', 'C'], True, None),
            FrontDateField('Date', '%y%m%d', True, None),
            AmountField('Amount', 15, True, False, True, None)
        ])
        
class MtField65(MtComplexField):

    def __init__(self, name, mandatory):
        MtComplexField.__init__(self, '65', name, mandatory, [
            ListField('DebitCredit', ['D', 'C'], True, None),
            FrontDateField('Date', '%y%m%d', True, None),
            AmountField('Amount', 15, True, False, True, None)
        ])

class MtField70C(MtField):
    
    def __init__(self, name, mandatory, qualifier):
        MtField.__init__(self, '70C', MultiLineField(name, 4, 35, CharacterSetX, mandatory, None), 
            FixedCharacterField(name + '_Qualifier', 4, CharacterSetC, True, qualifier), '//')
            
class MtField70D(MtField):

   def __init__(self, name, mandatory, qualifier):
        MtField.__init__(self, '70C', MultiLineField(name, 6, 35, CharacterSetX, mandatory, None), 
            FixedCharacterField(name + '_Qualifier', 4, CharacterSetC, True, qualifier), '//')

class MtField70E(MtField):
    
    def __init__(self, name, mandatory, qualifier):
        MtField.__init__(self, '70E', MultiLineField(name, 10, 35, CharacterSetX, mandatory, None), 
            FixedCharacterField(name + '_Qualifier', 4, CharacterSetC, True, qualifier), '//')
            
class MtField70a(FieldOptions):
    pass

class MtField77E(MtField):

    def __init__(self, name, mandatory):
        MtField.__init__(self, '77E', CharacterField(name, 16, CharacterSetX, mandatory, None))

class MtField79(MtField):

    def __init__(self, name, mandatory):
        MtField.__init__(self, '79', MultiLineField(name, 35, 50, CharacterSetX, mandatory, None))
            
class MtField86(MtField):

    def __init__(self, name, mandatory):
        MtField.__init__(self, '86', MultiLineField(name, 6, 65, CharacterSetX, mandatory, None))

class MtField90A(MtComplexField):
    
    def __init__(self, name, mandatory, qualifier):
        MtComplexField.__init__(self, '90A', name, mandatory, [
            ListField('PercentageType', ['DISC', 'PRCT', 'PREM', 'YIEL'], True, None),
            MtSubField('/', DecimalField('Price', 15, None, False, True, None))
        ], FixedCharacterField(name + '_Qualifier', 4, CharacterSetC, True, qualifier), '//')
        
class MtField90B(MtComplexField):
    
    def __init__(self, name, mandatory, qualifier):
        MtComplexField.__init__(self, '90B', name, mandatory, [
            ListField('AmountType', ['ACTU', 'DISC', 'PREM'], True, None),
            MtSubField('/', AmountField('Price', 15, True, False, True, None))
        ], FixedCharacterField(name + '_Qualifier', 4, CharacterSetC, True, qualifier), '//')
        
class MtField90E(MtField):

    def __init__(self, name, mandatory, qualifier):
        MtField.__init__(self, '90E', ListField(name, ['UKWN'], True, None),
            FixedCharacterField(name + '_Qualifier', 4, CharacterSetC, True, qualifier), '//')
        
class MtField90a(FieldOptions):
    pass

class MtField92A(MtField):
    
    def __init__(self, name, mandatory, qualifier):
        MtField.__init__(self, '92A', DecimalField(name, 15, None, True, True, None), 
            FixedCharacterField(name + '_Qualifier', 4, CharacterSetC, True, qualifier), '//')

class MtField92A_MT598(MtField):
    
    def __init__(self, name, mandatory, qualifier):
        MtField.__init__(self, '92A', DecimalField(name, 10, 7, True, mandatory, None), 
            FixedCharacterField(name + '_Qualifier', 4, CharacterSetC, mandatory, qualifier), '//')


class MtField92D(MtField):
    
    def __init__(self, name, mandatory, qualifier):
        MtField.__init__(self, '92D', DecimalField(name, 15, None, True, True, None), 
            FixedCharacterField(name + '_Qualifier', 4, CharacterSetC, True, qualifier), '//')
            
            
class MtField92B(MtComplexField):

    def __init__(self, name, mandatory, qualifier):
        MtComplexField.__init__(self, '92B', name, mandatory, [
            CurrencyField('FirstCurrency', True, None),
            CurrencyField('SecondCurrency', True, None),
            DecimalField(name, 15, None, False, True, None)
        ], FixedCharacterField(name + '_Qualifier', 4, CharacterSetC, True, qualifier), '//')
        
class MtField92a(FieldOptions):
    pass
        
class MtField93B(MtComplexField):

     def __init__(self, name, mandatory, qualifier):
        MtComplexField.__init__(self, '93B', name, mandatory, [
            CharacterField('DataSourceScheme', 8, CharacterSetC, False, None),
            MtSubField('/', ListField('QuantityTypeCode', ['AMOR', 'FAMT', 'UNIT'], True, None)),
            MtSubField('/', DecimalField('Quantity', 15, None, True, True, None))
        ], FixedCharacterField(name + '_Qualifier', 4, CharacterSetC, True, qualifier), '/')
        
class MtField93C(MtComplexField):

     def __init__(self, name, mandatory, qualifier):
        MtComplexField.__init__(self, '93C', name, mandatory, [
            ListField('QuantityTypeCode', ['AMOR', 'FAMT', 'UNIT'], True, None),
            MtSubField('/', ListField('BalanceTypeCode', ['AVAI', 'NAVL'], True, None)),
            MtSubField('/', DecimalField('Quanitity', 15, None, True, True, None))
        ], FixedCharacterField(name + '_Qualifier', 4, CharacterSetC, True, qualifier), '//')
        
class MtField93a(FieldOptions):
    pass
        
class MtField94B(MtComplexField):

    def __init__(self, name, mandatory, qualifier):
        MtComplexField.__init__(self, '94B', name, mandatory, [
            CharacterField('DataSourceScheme', 8, CharacterSetC, False, None),
            MtSubField('/', FixedCharacterField('PlaceCode', 4, CharacterSetC, True, None)),
            CharacterField('Narrative', 30, CharacterSetX, False, None)
        ], FixedCharacterField(name + '_Qualifier', 4, CharacterSetC, True, qualifier), '/')
        
class MtField94C(MtField):
    
    def __init__(self, name, mandatory, qualifier):
        MtField.__init__(self, '94C', FixedCharacterField(name, 2, CharacterSetA, mandatory, None),
            FixedCharacterField(name + '_Qualifier', 4, CharacterSetC, True, qualifier), '//')
            
class MtField94D(MtComplexField):

    def __init__(self, name, mandatory, qualifier):
        MtComplexField.__init__(self, '94D', name, mandatory, [
            FixedCharacterField('CountryCode', 2, CharacterSetA, False, None),
            MtSubField('/', CharacterField('Description', 35, CharacterSetX, True, None))
        ], FixedCharacterField(name + '_Qualifier', 4, CharacterSetC, True, qualifier), '//')
            
class MtField94F(MtComplexField):
    
    def __init__(self, name, mandatory, qualifier):
        MtComplexField.__init__(self, '94F', name, mandatory, [
            FixedCharacterField('PlaceCode', 4, CharacterSetC, True, None),
            MtSubField('/', BicCode('IdentifierCode', True, None))
        ], FixedCharacterField(name + '_Qualifier', 4, CharacterSetC, True, qualifier), '//')
        
class MtField94a(FieldOptions):
    pass

class MtField95C(MtField):
    
    def __init__(self, name, mandatory, qualifier):
        MtField.__init__(self, '95C', FixedCharacterField('CountryCode', 2, CharacterSetA, True, None),
            FixedCharacterField(name + '_Qualifier', 4, CharacterSetC, True, None), '//')
        
class MtField95P(MtField):
    
    def __init__(self, name, mandatory, qualifier):
        MtField.__init__(self, '95P', BicCode('IdentifierCode', mandatory, None), 
            FixedCharacterField(name + '_Qualifier', 4, CharacterSetC, True, qualifier), '//')
            
class MtField95Q(MtField):
    
    def __init__(self, name, mandatory, qualifier):
        MtField.__init__(self, '95Q', MultiLineField(name, 4, 35, CharacterSetX, mandatory, None), 
            FixedCharacterField(name + '_Qualifier', 4, CharacterSetC, True, qualifier), '//')

class MtField95R(MtComplexField):
            
    def __init__(self, name, mandatory, qualifier):
        MtComplexField.__init__(self, '95R', name, mandatory, [
            CharacterField('DataSourceScheme', 8, CharacterSetC, True, None),
            MtSubField('/', CharacterField('ProprietaryCode', 34, CharacterSetX, True, None)),
        ], FixedCharacterField(name + '_Qualifier', 4, CharacterSetC, True, qualifier), '/')
            
class MtField95S(MtComplexField):
            
    def __init__(self, name, mandatory, qualifier):
        MtComplexField.__init__(self, '95S', name, mandatory, [
            CharacterField('DataSourceScheme', 8, CharacterSetC, False, None),
            MtSubField('/', ListField('IdType', ['ARNU', 'CCPT', 'CHTY', 'CORP', 'DRLC', 'EMPL', 'FIIN', 'TXID'], True, None)),
            MtSubField('/', FixedCharacterField('CountryCode', 2, CharacterSetA, True, None)),
            MtSubField('/', CharacterField('AlternateId', 30, CharacterSetX, True, None)),
        ], FixedCharacterField(name + '_Qualifier', 4, CharacterSetC, True, qualifier), '/')
        
class MtField95a(FieldOptions):
    pass
        
class MtField97A(MtField):
    
    def __init__(self, name, mandatory, qualifier):
        MtField.__init__(self, '97A', CharacterField(name, 35, CharacterSetX, mandatory, None),
            FixedCharacterField(name + '_Qualifier', 4, CharacterSetC, True, qualifier), '//'
        )

class MtField97A_MT598(MtComplexField):
            
    def __init__(self, name, mandatory, qualifier):
        MtComplexField.__init__(self, '97A', name, mandatory, [
            CharacterField('DataSourceScheme', 8, CharacterSetC, False, None),
            MtSubField('/', ListField('AccountType', ['ABRD', 'CEND', 'DVPA', 'FUNG', 'MARG', 'NFUN', 'PHYS', 'SHOR', 'IORT'], True, None)),
            MtSubField('/', CharacterField('AccountNumber', 35, CharacterSetX, True, None)),
        ], FixedCharacterField(name + '_Qualifier', 4, CharacterSetC, True, qualifier), '/')

        
class MtField97B(MtComplexField):
            
    def __init__(self, name, mandatory, qualifier):
        MtComplexField.__init__(self, '97B', name, mandatory, [
            CharacterField('DataSourceScheme', 8, CharacterSetC, False, None),
            MtSubField('/', ListField('AccountType', ['ABRD', 'CEND', 'DVPA', 'FUNG', 'MARG', 'NFUN', 'PHYS', 'SHOR', 'IORT', 'RECA'], True, None)),
            MtSubField('/', CharacterField('AccountNumber', 35, CharacterSetX, True, None)),
        ], FixedCharacterField(name + '_Qualifier', 4, CharacterSetC, True, qualifier), '/')
        
class MtField97E(MtField):
    
    def __init__(self, name, mandatory, qualifier):
        MtField.__init__(self, '97E', CharacterField(name, 34, CharacterSetX, mandatory, None),
            FixedCharacterField(name + '_Qualifier', 4, CharacterSetC, True, qualifier), '//'
        )
    
class MtField97a(FieldOptions):
    pass

class MtField98A(MtField):

    def __init__(self, name, mandatory, qualifier):
        MtField.__init__(self, '98A', FrontDateField(name, '%Y%m%d', mandatory, None), 
            FixedCharacterField(name + '_Qualifier', 4, CharacterSetC, True, qualifier), '//')

class MtField98C(MtField):

    def __init__(self, name, mandatory, qualifier):
        MtField.__init__(self, '98C', FrontDateField(name, '%Y%m%d%H%M%S', mandatory, None), 
            FixedCharacterField(name + '_Qualifier', 4, CharacterSetC, True, qualifier), '//')
            
class MtField98a(FieldOptions):
    pass
            
class MtField99A(MtField):

    def __init__(self, name, mandatory, qualifier):
        MtField.__init__(self, '99A', FixedIntegerField(name, 3, True, mandatory, None), 
            FixedCharacterField(name + '_Qualifier', 4, CharacterSetC, True, qualifier), '//')
            
class MtField99B(MtField):

    def __init__(self, name, mandatory, qualifier):
        MtField.__init__(self, '99B', FixedIntegerField(name, 3, False, mandatory, None), 
            FixedCharacterField(name + '_Qualifier', 4, CharacterSetC, True, qualifier), '//')

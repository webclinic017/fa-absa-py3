"""-----------------------------------------------------------------------------
PROJECT                 :  SBL ACS Migration
PURPOSE                 :  Classes to be used for writing fixed length fields to generate records for a 
                           file to be sent to Global One.
DEPATMENT AND DESK      :  Prime Services, Securities Lending
REQUESTER               :  Linda Breytenbach
DEVELOPER               :  Francois Truter
CR NUMBER               :  462229
-----------------------------------------------------------------------------"""

from datetime import datetime

NEWLINE = '\n'

class Field(object):

    def __init__(self, _name, _default, _mandatory):
        self._name = _name
        self._value = _default
        self._mandatory = _mandatory
        
    @property
    def Name(self):
        return self._name
    
    @property
    def FieldLength(self):
        pass
        
    def _getValue(self):
        return self._value
        
    def _setValue(self, _value):
        self._value = _value
        
    Value = property(_getValue, _setValue)
        
    def _validateValue(self):
        if self._value == None and self._mandatory:
            raise Exception('%s: No value supplied for mandatory field.' % self.Name)
        
class StringField(Field):

    def __init__(self, _name, _length, _default = None, _mandatory = False):
        Field.__init__(self, _name, _default, _mandatory)
        try:
            self._length = int(_length)
            if self._length != _length:
                raise ValueError()
        except ValueError as ex:
            raise ValueError('%(name)s: Expected an integer for length, got [%(len)s]' % {'name': _name, 'len': _length})
        
    def __str__(self):
        self._validateValue()
        try:
            s = str(self._value) if self._value else ''
            if len(s) > self._length:
                raise Exception('Value [%(value)s] is too long. Field length is %(len)s' %\
                    {'value': self._value, 'len': self._length})
                    
            return s.ljust(self._length)
        except Exception as ex:
            raise Exception('%(name)s: %(ex)s' % {'name': self.Name, 'ex': ex})
            
    @property
    def FieldLength(self):
        return self._length
    
class DatetimeField(Field):

    def __init__(self, _name, _format, _default = None, _mandatory = False):
        try:
            if isinstance(_default, basestring):
                _default = datetime.strptime(_default, _format)
            elif _default != None and not isinstance(_default, datetime):
                raise Exception('must be of type datetime, got %s' %  _default.__class__.__name__)
        except Exception as ex:
            raise Exception('%(name)s: Could not assign default value: %(ex)s' % {'name': _name, 'ex': ex})
        Field.__init__(self, _name, _default, _mandatory)
        self._format = _format
    
    @property
    def FieldLength(self):
        testDate = datetime.today()
        return len(testDate.strftime(self._format))
        
    def Value(self, _date, _format):
        try:
            self._value = datetime.strptime(str(_date), _format)
        except Exception as ex:
            raise Exception('%(name)s: Could not convert [%(val)s] to a date using format [%(format)s]: %(ex)s' %\
                {'name': self.Name, 'val': _date, 'format': _format, 'ex': ex})
    
    def __str__(self):
        self._validateValue()
        try:
            if self._value:
                return self._value.strftime(self._format)
            else:
                return ' ' * self.FieldLength
        except Exception as ex:
            raise Exception('%(name)s: Could not convert [%(val)s] to string using format [%(format)s]: %(ex)s' %\
                {'name': self._name, 'val': self._value, 'format': self._format, 'ex': ex})
        
class BoolField(StringField):

    def __init__(self, _name, _true, _false, _default = None, _mandatory = False):
        _length = max(len(str(_true)), len(str(_false)))
        StringField.__init__(self, _name, _length, _default, _mandatory)
        self._true = _true
        self._false = _false
        
    def __str__(self):
        self._validateValue()
        _str = ''
        if not self._value == None:
            if self._value:
                _str = str(self._true)
            else:
                _str = str(self._false)
            
        return _str.ljust(self._length)
        
class YesNoField(BoolField):

    def __init__(self, _name,  _default = None, _mandatory = False):
        BoolField.__init__(self, _name, 'Y', 'N', _default, _mandatory)
            
class IntField(StringField):

    def __init__(self, _name, _allowNegative, _length, _default = None, _mandatory = False):
        if _allowNegative:
            _length += 1

        StringField.__init__(self, _name, _length, _default, _mandatory)
        self._length = _length
        self._allowNegative = _allowNegative
        
    def _validateValue(self):
        StringField._validateValue(self)
        if self._value and not self._allowNegative and self._value < 0:
            raise Exception('%(name)s: Negative values not allowed: %(val)s' % {'name': self.Name, 'val': self._value})
        
    def __str__(self):
        self._validateValue()
        try:
            if self._value == None:
                return ''.ljust(self._length)
    
            i = int(self._value)
            s = str(i)
            if len(s) > self._length:
                raise Exception('Too long, field lengtgh is %s' % self._length)
            formatStr = '%' + '0%ii' % self._length
            return formatStr % i
        except Exception as ex:
            raise Exception('%(name)s: Could not convert [%(val)s] to integer field: %(ex)s' %\
                {'name': self.Name, 'val': self._value, 'ex': ex})
                
class IntRangeField(IntField):

    def __init__(self, _name, _start, _end, _default = None, _mandatory = False):
        if _end < _start:
            raise Exception('%(name)s: Start value should be less than or equal to end value. Start [%(start)s] End [%(end)s]' % \
                {'name': _name, 'start': _start, 'end': _end})
        _length = max(len(str(abs(_start))), len(str(abs(_end))))
        if _start < 0:
            _allowNegative = True
        else:
            _allowNegative = False
        IntField.__init__(self, _name, _allowNegative, _length, _default, _mandatory)
        self._start = _start
        self._end = _end
        
    def _validateValue(self):
        IntField._validateValue(self)
        if self._value and not (self._value >= self._start and self._value <= self._end):
            raise Exception('%(name)s: Invaild value [%(val)s], must be between [%(start)s] and [%(end)s]' %\
                {'name': self.Name, 'val': self._value, 'start': self._start, 'end': self._end})
                
class ImpliedDecimalField(IntField):

    def __init__(self, _name, _allowNegative, _intLength, _fractionLength, _default = None, _mandatory = False):
        _length = _intLength + _fractionLength
        IntField.__init__(self, _name, _allowNegative, _length, _default, _mandatory)
        self._intLength = _intLength
        self._fractionLength = _fractionLength
        
    def __str__(self):
        try:
            if self._value:
                self._value = float(self._value)
                self._value = round(self._value * pow(10, self._fractionLength))
            self._validateValue()
            return IntField.__str__(self)
        except Exception as ex:
             raise Exception('%(name)s: %(ex)s' % {'name': self.Name, 'ex': ex})
                
class ListField(StringField):

    def __init__(self, _name, _length, _validValues, _default = None, _mandatory = False):
        StringField.__init__(self, _name, _length, _default, _mandatory)
        self._validValues = _validValues

    def __str__(self):
        self._validateValue()
        try:
            if self._value and self._value not in self._validValues:
                validList = ''
                seperator = ''
                for validValue in self._validValues:
                    validList += seperator + str(validValue)
                    seperator = ', '
                raise Exception('[%(val)s] is not valid, valid values are [%(valid)s]' % {'val': self._value, 'valid': validList})
        except Exception as ex:
            raise Exception('%(name)s: %(ex)s' % {'name': self.Name, 'ex': ex})
        
        return StringField.__str__(self)
        
class Record:

    def __init__(self, _name, fields):
        self._name = _name
        self._fields = fields
        for field in fields:
            setattr(self, field.Name, field)
        
    def __str__(self):
        try:
            _str = ''
            for field in self._fields:
                _str += str(field)
            return _str
        except Exception as ex:
            raise Exception('%(name)s: Could not convert record to string: %(ex)s' %\
                {'name': self.Name, 'ex': ex})
                
    @property
    def Name(self):
        return self._name
        
    @property
    def Layout(self):
        _str = self.Name + NEWLINE
        _start = 1
        layout = ''
        for field in self._fields:
            _str += layout + '%(name)s,%(start)i,%(len)i,%(end)i' % {'name': field.Name, 'start': _start, 'len': field.FieldLength, 'end': _start + field.FieldLength - 1}
            _start += field.FieldLength
            layout = NEWLINE
        return _str


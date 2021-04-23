"""-----------------------------------------------------------------------------
PROJECT                 :  Prime Brokerage
PURPOSE                 :  Classes to be used for writing delimitted files 
DEPATMENT AND DESK      :  Prime Services
REQUESTER               :  Francois Henrion
DEVELOPER               :  Paul Jacot-Guillarmod, Francois Truter
CR NUMBER               :  703542

HISTORY
================================================================================
Date       Change no    Developer          Description
--------------------------------------------------------------------------------
2011-07-05 703542       Herman Hoon    Initial Implementation
-----------------------------------------------------------------------------"""

import time

NEWLINE = '\n'

class Field:
    
    def __init__(self, _name, _default, _mandatory):
        self._name = _name
        self._value = _default
        self._mandatory = _mandatory
    
    @property
    def Name(self):
        return self._name
        
    def Value(self, _value):
        self._value = _value
        
    def _validateValue(self):
        if self._value == None and self._mandatory:
            raise Exception('%s: No value supplied for mandatory field.' % self.Name)

class StringField(Field):

    def __init__(self, _name, _length, _default = None, _mandatory = False):
        Field.__init__(self, _name, _default, _mandatory)
        if isinstance(_length, int):
            self._length = _length
        else:
            raise TypeError('%(name)s: Expected an integer for length, got [%(len)s]' % {'name': _name, 'len': _length})
    
    def _validateValue(self):
        Field._validateValue(self)
        if self._value and len(str(self._value)) > self._length:
            raise ValueError('Value [%(value)s] is too long. Field length is %(len)s' %\
                {'value': self._value, 'len': self._length})
    
    def __str__(self):
        self._validateValue()
        try:
            return str(self._value) if self._value else ''
        except Exception as ex:
            raise Exception('%(name)s: %(ex)s' % {'name': self.Name, 'ex': ex})
    
class DoubleField(Field):

    def __init__(self, _name, _default = None, _mandatory = False):
        Field.__init__(self, _name, _default, _mandatory)
        
    def __str__(self):
        self._validateValue()
        try:
            return str(self._value) if self._value else ''
        except Exception as ex:
            raise Exception('%(name)s: %(ex)s' % {'name': self.Name, 'ex': ex})
    
class ListField(Field):
    
    def __init__(self, _name, _validValues, _default = None, _mandatory = False):
        Field.__init__(self, _name, _default, _mandatory)
        self._validValues = _validValues
        
    def _validateValue(self):
        Field._validateValue(self)
        if self._value and self._value not in self._validValues:
            validList = ', '.join([str(validValue) for validValue in self._validValues])
            raise Exception('[%(val)s] is not valid, valid values are [%(valid)s]' % {'val': self._value, 'valid': validList})
            
    def __str__(self):
        self._validateValue()
        try:
            return str(self._value) if self._value else ''
        except Exception as ex:
            raise Exception('%(name)s: %(ex)s' % {'name': self.Name, 'ex': ex})

class IntegerField(Field):

    def __init__(self, _name, _default = None, _mandatory = False):
        Field.__init__(self, _name, _default, _mandatory)
    
    def __str__(self):
        self._validateValue()
        try:
            return str(self._value) if self._value else ''
        except Exception as ex:
            raise Exception('%(name)s: %(ex)s' % {'name': self.Name, 'ex': ex})
            
class BoolField(Field):

    def __init__(self, _name, _true, _false, _default = None, _mandatory = False):
        Field.__init__(self, _name, _default, _mandatory)
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
            
        return _str
        
class YesNoField(BoolField):

    def __init__(self, _name,  _default = None, _mandatory = False):
        BoolField.__init__(self, _name, 'Y', 'N', _default, _mandatory)
        
class DayField(IntegerField):

    def __init__(self, _name, _default = None, _mandatory = False):
        IntegerField.__init__(self, _name, _default, _mandatory)
        
    def Value(self, _date, _format):
        try:
            dateValue = time.strptime(str(_date), _format)
            self._value = dateValue.tm_mday
        except Exception as ex:
            raise Exception('%(name)s: Could not convert [%(val)s] to a date using format [%(format)s]: %(ex)s' %\
                {'name': self.Name, 'val': _date, 'format': _format, 'ex': ex})

class MonthField(IntegerField):

    def __init__(self, _name, _default = None, _mandatory = False):
        IntegerField.__init__(self, _name, _default, _mandatory)
        
    def Value(self, _date, _format):
        try:
            dateValue = time.strptime(str(_date), _format)
            self._value = dateValue.tm_mon
        except Exception as ex:
            raise Exception('%(name)s: Could not convert [%(val)s] to a date using format [%(format)s]: %(ex)s' %\
                {'name': self.Name, 'val': _date, 'format': _format, 'ex': ex})

class YearField(IntegerField):

    def __init__(self, _name, _default = None, _mandatory = False):
        IntegerField.__init__(self, _name, _default, _mandatory)
        
    def Value(self, _date, _format):
        try:
            dateValue = time.strptime(str(_date), _format)
            self._value = dateValue.tm_year
        except Exception as ex:
            raise Exception('%(name)s: Could not convert [%(val)s] to a date using format [%(format)s]: %(ex)s' %\
                {'name': self.Name, 'val': _date, 'format': _format, 'ex': ex})

class HourField(IntegerField):

    def __init__(self, _name, _default = None, _mandatory = False):
        IntegerField.__init__(self, _name, _default, _mandatory)
        
    def Value(self, _date, _format):
        try:
            dateValue = time.strptime(str(_date), _format)
            self._value = dateValue.tm_hour
        except Exception as ex:
            raise Exception('%(name)s: Could not convert [%(val)s] to a date using format [%(format)s]: %(ex)s' %\
                {'name': self.Name, 'val': _date, 'format': _format, 'ex': ex})

class MinuteField(IntegerField):

    def __init__(self, _name, _default = None, _mandatory = False):
        IntegerField.__init__(self, _name, _default, _mandatory)
        
    def Value(self, _date, _format):
        try:
            dateValue = time.strptime(str(_date), _format)
            self._value = dateValue.tm_min
        except Exception as ex:
            raise Exception('%(name)s: Could not convert [%(val)s] to a date using format [%(format)s]: %(ex)s' %\
                {'name': self.Name, 'val': _date, 'format': _format, 'ex': ex})

class Record:

    def _validateFields(self):
        duplicatedFields = {}
        for field in self._fields:
            count = 0
            for innerField in self._fields:
                if innerField.Name == field.Name:
                    count += 1
            if count > 1:
                duplicatedFields[field.Name] = count
        
        if duplicatedFields:
            message = 'The following fields have been duplicated in record [%s], please correct it:' % self._name
            for fieldName in duplicatedFields:
                message += NEWLINE + ('%s: %i' % (fieldName, duplicatedFields[fieldName]))
            raise Exception(message)

    def __init__(self, _name, fields, delimiter):
        self._name = _name
        self._fields = fields
        self._delimiter = delimiter
        self._validateFields()
        for field in fields:
            setattr(self, field.Name, field)
    
    def __str__(self):
        try:
            return str(self._delimiter).join([str(field) for field in self._fields])
        except Exception as ex:
            raise Exception('%(name)s: Could not convert record to string: %(ex)s' %\
                {'name': self.Name, 'ex': ex})
    
    @property
    def Name(self):
        return self._name

    @property    
    def FieldListing(self):
        return str(self._delimiter).join([field.Name for field in self._fields])
            

'''-----------------------------------------------------------------------------
PROJECT                 :  Markets Message Gateway
PURPOSE                 :  Common classes used to create SWIFT messages
DEPATMENT AND DESK      :  
REQUESTER               :  
DEVELOPER               :  Francois Truter
CR NUMBER               :  XXXXXX
--------------------------------------------------------------------------------

HISTORY
================================================================================
Date       Change no Developer                 Description
--------------------------------------------------------------------------------
2011-03-25 XXXXXX    Francois Truter           Initial Implementation
'''

CRLF = '\r\n'

class MandatoryFieldNotSupplied(Exception):

    def __init__(self, fieldName):
        self._fieldName = fieldName
        
    @property
    def FieldName(self):
        return self._fieldName
    
    def __str__(self):
        return '%s: No value supplied for mandatory field.' % self._fieldName

class FieldOfFields(object):

    def __init__(self, _name):
        self._name = _name
        
    @property
    def Name(self):
        return self._name

class RepetitiveField(FieldOfFields):
    
    def __init__(self, _name, _mandatory):
        FieldOfFields.__init__(self, _name)
        self._mandatory = _mandatory
        self._fields = []
        
    def appendField(self, field):
        self._fields.append(field)
    
    @property
    def numFields(self):
        return len(self._fields)
        
    def __str__(self):
        _str = ''
        delimiter = ''
        for field in self._fields:
            try:
                fieldStr = str(field)
                if fieldStr:
                    _str += delimiter + str(field)
                    delimiter = CRLF
            except Exception as ex:
                raise Exception ('Error in field [%s]: %s' % (self.Name, ex))
            
        if self._mandatory and not _str:
            raise Exception('No value supplied for mandatory field [%s].' % self.Name)

        return _str

class ComplexFieldBase(FieldOfFields):
    
    def _addProperty(self, field, index):
        if isinstance(field, FieldOfFields):
            fget = lambda self: self._metaGetField(index)
            fset = None
        else:
            fget = lambda self: self._metaGetValue(index)
            fset = lambda self, value: self._metaSetValue(index, value)
            
        setattr(self.__class__, field.Name, property(fget, fset))
        
        if isinstance(field, MtField) and field._qualifier:
            fset = lambda self, value: self._metaSetQualifier(index, value)
            setattr(self.__class__, field.Name + '_Qualifier', property(None, fset))

    def _metaGetField(self, index):
        return self._fields[index]

    def _metaGetValue(self, index):
        return self._fields[index].Value
         
    def _metaSetValue(self, index, value):
        self._fields[index].Value = value
        
    def _metaSetQualifier(self, index, value):
        self._fields[index].Qualifier = value
        
    @classmethod
    def _checkForDuplicateFields(cls, fields):
        firstFields = []
        duplicateFields = []
        for field in fields:
            if field.Name in firstFields:
                duplicateFields.append(field.Name)
            else:
                firstFields.append(field.Name)
                
        if duplicateFields:
            raise Exception('Class %s contains the following duplicate field(s): %s' % (cls.__name__, ', '.join(duplicateFields)))
    
    def __init__(self, _name, _fields):
        self.__class__._checkForDuplicateFields(_fields)
        FieldOfFields.__init__(self, _name)
        self._fields = []
        for field in _fields:
            index = len(self._fields)
            self._fields.append(field)
            self._addProperty(field, index)
            
class ComplexField(ComplexFieldBase):
    
    def __init__(self, _name, _mandatory, _fields, _delimiter = ''):
        ComplexFieldBase.__init__(self, _name, _fields)
        self._mandatory = _mandatory
        self._delimiter = _delimiter
        
    @property
    def Mandatory(self):
        return self._mandatory
        
    def __str__(self): 
        _str = ''
        exceptions = []
        
        delimiter = ''
        for field in self._fields:
            try:
                fieldStr = str(field)
                if fieldStr:
                    _str += delimiter + fieldStr
                    delimiter = self._delimiter
            except MandatoryFieldNotSupplied as ex:
                exceptions.append(ex)

        if exceptions and (_str != '' or self.Mandatory):
            raise MandatoryFieldNotSupplied('%s (%s)' % (self.Name, ', '.join(ex.FieldName for ex in exceptions)))
        elif _str == '' and self.Mandatory:
            raise MandatoryFieldNotSupplied('No value supplied for mandatory field [%s].' % self.Name)
        
        return _str

class MtFieldBase(object):

    def __init__(self, field):
        self._field = field
        
    @property
    def Name(self):
        return self._field.Name

    def _getValue(self):
        if isinstance(self._field, FieldOfFields):
            return self._field
        else:
            return self._field.Value
    
    def _setValue(self, _value):
        if isinstance(self._field, FieldOfFields):
            raise Exception('Cannot assign to %s' % self.Name)
        else:
            self._field.Value = _value
    
    Value = property(_getValue, _setValue)


class MtField(MtFieldBase):
    
    def __init__(self, tag, field, qualifier = None, qualifierSeperator = None):
        MtFieldBase.__init__(self, field)
        self._tag = tag
        self._qualifier = qualifier
        self._qualifierSeperator = qualifierSeperator
        
    def _getQualifier(self):
        return ':' + str(self._qualifier) if self._qualifier else ''
        
    def _setQualifier(self, value):
        self._qualifier.Value = value
        
    Qualifier = property(None, _setQualifier)
    
    def _getQualifierSeperator(self):
        return str(self._qualifierSeperator) if self._qualifierSeperator else ''
    
    def __str__(self):
        _str = str(self._field)
        if _str:
            return ':%(tag)s:%(qualifier)s%(str)s' % {'tag': self._tag, 'qualifier': self._getQualifier() + self._getQualifierSeperator(), 'str': _str}
        else:
            return ''

class MtSubField(MtFieldBase):
    
    def __init__(self, pre, field):
        MtFieldBase.__init__(self, field)
        self._pre = pre
        
    def __str__(self):
        fieldStr = str(self._field)
        if fieldStr:
            return str(self._pre) + fieldStr
        else:
            return ''
            
class MtComplexField(ComplexField):
    
    def __init__(self, _tag, _name, _mandatory, _fields, _qualifier = None, qualifierSeperator = None):
        ComplexField.__init__(self, _name, _mandatory, _fields)
        self._tag = _tag
        self._qualifier = _qualifier
        self._qualifierSeperator = qualifierSeperator
    
    def _getQualifier(self):
        return ':' + str(self._qualifier) if self._qualifier else ''
        
    def _setQualifier(self, value):
        self._qualifier.Value = value
        
    Qualifier = property(None, _setQualifier)
    
    def _getQualifierSeperator(self):
        return str(self._qualifierSeperator) if self._qualifierSeperator else ''
                    
    def __str__(self):
        _str = ComplexField.__str__(self)
        if _str:
            return ':%(tag)s:%(qualifier)s%(str)s' % {'tag': self._tag, 'qualifier': self._getQualifier() + self._getQualifierSeperator(), 'str': _str}
        else:
            return ''

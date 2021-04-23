""" Compiled: 2020-09-18 10:38:53 """

#__src_file__ = "extensions/operations/etc/FOperationsAMBAMessage.py"
import amb

from FOperationsExceptions import AMBAMessageException

#-------------------------------------------------------------------------
def CreateAmbaTableFromString(string):
    ambaMessage = CreateAmbaMessageFromString(string)
    ambaTables = ambaMessage.GetTableAndChildTables()
    assert len(ambaTables) == 1
    ambaTable = ambaTables[0]
    assert ambaTable
    return ambaTable

#-------------------------------------------------------------------------
def CreateAmbaMessageFromString(string):
    messageBuffer = amb.mbf_create_buffer_from_data(string)
    messageObj = messageBuffer.mbf_read()
    ambaMessage = AMBAMessage(messageObj)
    return ambaMessage

#-------------------------------------------------------------------------
class AMBAMessage(object):
    
    #-------------------------------------------------------------------------
    @staticmethod
    def GetTablesByName(tables, name):
        filteredTables = list()
        for table in tables:
            if table.GetName() == name:
                filteredTables.append(table)
        return filteredTables
    
    #-------------------------------------------------------------------------
    @staticmethod
    def CreateTablesFromMessage(msg, dummyTableField, tables):
        inner = msg.mbf_first_object()
        field = ''
        while inner:
            field = inner.mbf_get_name()
            value = inner.mbf_get_value()
            
            if inner.mbf_first_object():
                if field == value:
                    AMBAMessage.__CreateTableAndSubTables(inner, field, tables)
            inner = msg.mbf_next_object()
            
    #-------------------------------------------------------------------------
    @staticmethod
    def __CreateTableAndSubTables(msg, tableName, tables):
        table = Table(tableName, tableName)
        tables.append(table)
        inner = msg.mbf_first_object()
        while inner:
            field = inner.mbf_get_name()
            value = inner.mbf_get_value()
            
            table.AddFieldAndValue(field, value)
            if inner.mbf_first_object():
                if field == value:
                    AMBAMessage.__CreateTableAndSubTables(inner, field, tables)
            inner = msg.mbf_next_object()
    
    #-------------------------------------------------------------------------
    def __init__(self, msg):
        super(AMBAMessage, self).__init__()
        
        if msg == None:
            raise AMBAMessageException('Empty message object sent to AMBAMessage.')
        
        self.__msg = msg
        self.__typeOfUpdate = ''
        self.__updatedTable = ''
        headers = msg.mbf_read_header()
        
        for header in headers:
            if header.mbf_get_name() == 'TYPE':
                typeValues = header.mbf_get_value().split('_')
                if len(typeValues) == 2:
                    self.__typeOfUpdate = typeValues[0]
                    self.__updatedTable = typeValues[1]
                elif len(typeValues) == 1:
                    self.__updatedTable = typeValues[0]
                    
        if self.__updatedTable == '':
            raise AMBAMessageException('Could no get the name of the updated table.')

    #-------------------------------------------------------------------------
    def GetNameOfUpdatedTable(self):
        return self.__updatedTable

    #-------------------------------------------------------------------------
    def GetTypeOfUpdate(self):
        return self.__typeOfUpdate

    #-------------------------------------------------------------------------
    def GetTableAndChildTables(self):
        tables = list()
        AMBAMessage.CreateTablesFromMessage(self.__msg, '', tables)
        return tables

#-------------------------------------------------------------------------
class TypeOfChange():
    INVALID = 0
    UPDATE = 1
    INSERT = 2
    DELETE = 3
    NOT_CHANGED = 4

#-------------------------------------------------------------------------
class Attribute(object):
    
    #-------------------------------------------------------------------------
    def __init__(self, name):
        super(Attribute, self).__init__()
        
        self.__name = name
        self.__previousValue = None
        self.__currentValue = None
        self.__typeOfChange = TypeOfChange.NOT_CHANGED

    #-------------------------------------------------------------------------
    def SetPreviousValue(self, value, typeOfChange):
        self.__previousValue = value
        self.__typeOfChange = typeOfChange

    #-------------------------------------------------------------------------
    def SetCurrentValue(self, value):
        self.__currentValue = value

    #-------------------------------------------------------------------------
    def GetName(self):
        return self.__name

    #-------------------------------------------------------------------------
    def GetTypeOfChange(self):
        return self.__typeOfChange

    #-------------------------------------------------------------------------
    def GetCurrentValue(self):
        return self.__currentValue

    #-------------------------------------------------------------------------
    def GetPreviousValue(self):
        if not self.HasChanged():
            raise AMBAMessageException('The value has not been changed.')
        return self.__previousValue

    #-------------------------------------------------------------------------
    def HasChanged(self):
        return self.GetTypeOfChange() != TypeOfChange.NOT_CHANGED

    #-------------------------------------------------------------------------
    def GetValueBeforeUpdate(self):
        value = self.GetCurrentValue()
        if self.HasChanged():
            value = self.GetPreviousValue()
        return value

#-------------------------------------------------------------------------
class Table(object):
    
    #-------------------------------------------------------------------------
    def __init__(self, name, field):
        super(Table, self).__init__()
        
        self.__name = self.__CreateFieldWithoutPrefix(name)
        self.__typeOfChange = self.__GetTypeOfChangeFromField(field)
        self.__attributes = dict()

    #-------------------------------------------------------------------------
    def GetName(self):
        return self.__name

    #-------------------------------------------------------------------------
    def GetTypeOfChange(self):
        return self.__typeOfChange

    #-------------------------------------------------------------------------
    def __GetTypeOfChangeFromField(self, field):
        typeOfChange = TypeOfChange.INVALID
        firstChar = field[0]
        if firstChar == '!':
            typeOfChange = TypeOfChange.UPDATE
        elif firstChar == '+':
            typeOfChange = TypeOfChange.INSERT
        elif firstChar == '-':
            typeOfChange = TypeOfChange.DELETE
        else:
            typeOfChange = TypeOfChange.NOT_CHANGED
        return typeOfChange

    #-------------------------------------------------------------------------
    def GetTypeOfChangeString(self):
        typeOfChangeString = 'Not changed'

        if self.__typeOfChange == TypeOfChange.INVALID:
            typeOfChangeString = 'Invalid'
        elif self.__typeOfChange == TypeOfChange.UPDATE:
            typeOfChangeString = 'Update'
        elif self.__typeOfChange == TypeOfChange.INSERT:
            typeOfChangeString = 'Insert'
        elif self.__typeOfChange == TypeOfChange.DELETE:
            typeOfChangeString = 'Delete'
        return typeOfChangeString

    #-------------------------------------------------------------------------
    def __HasPrefix(self, field):
        hasPrefix = False
        if field[0] in ['!', '+', '-']:
            hasPrefix = True
        return hasPrefix

    #-------------------------------------------------------------------------
    def __CreateFieldWithoutPrefix(self, field):
        if self.__HasPrefix(field):
            return field[1:]
        return field

    #-------------------------------------------------------------------------
    def AddFieldAndValue(self, field, value):
        attributeName = field
        if self.__HasPrefix(field):
            attributeName = self.__CreateFieldWithoutPrefix(field)
        attribute = None
        if attributeName in self.__attributes:
            attribute = self.__attributes[attributeName]
        else:
            attribute = Attribute(attributeName)
            self.__attributes[attributeName] = attribute
        typeOfChange = self.__GetTypeOfChangeFromField(field)
        if typeOfChange == TypeOfChange.NOT_CHANGED:
            attribute.SetCurrentValue(value)
        else:
            attribute.SetPreviousValue(value, typeOfChange)

    #-------------------------------------------------------------------------
    def GetAttribute(self, nameOfAttribute):
        if nameOfAttribute not in self.__attributes:
            raise AMBAMessageException('Attribute %s was not found in ABMA message table %s.' % (nameOfAttribute, self.GetName()))
        return self.__attributes[nameOfAttribute]

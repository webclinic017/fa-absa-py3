"""-----------------------------------------------------------------------------
PURPOSE              :  Utility classes for AMBA message processing
DEVELOPER            :  Libor Svoboda
--------------------------------------------------------------------------------

HISTORY
================================================================================
Date        Change no      Developer           Description
--------------------------------------------------------------------------------
2020-05-26  CHG0102232     Libor Svoboda       Initial implementation
"""
from collections import defaultdict

import amb


class Table(object):
    
    def __init__(self, name):
        self.name = self.remove_prefix(name)
        self.operation = self.get_operation(name)
        self.attributes = {}
        self.children = []
    
    def __str__(self):
        if self.operation:
            return '%s %s: %s' % (self.name, self.operation, self.attributes)
        return '%s: %s' % (self.name, self.attributes)
    
    @staticmethod
    def has_prefix(field):
        return field[0] in ('!', '+', '-')
    
    @classmethod
    def remove_prefix(cls, field):
        if cls.has_prefix(field):
            return field[1:]
        return field
    
    @classmethod
    def get_operation(cls, field):
        if not cls.has_prefix(field):
            return ''
        if field[0] == '!':
            return 'UPDATE'
        if field[0] == '+':
            return 'INSERT'
        if field[0] == '-':
            return 'DELETE'
        return ''
    
    @classmethod
    def get_children(cls, table):
        children = []
        for child in table.children:
            children.append(child)
            children.extend(cls.get_children(child))
        return children
    
    def add(self, field, value):
        attr_name = self.remove_prefix(field)
        if attr_name in self.attributes:
            attribute = self.attributes[attr_name]
        else:
            attribute = defaultdict(str)
            self.attributes[attr_name] = attribute
        operation = self.get_operation(field)
        if operation:
            attribute['operation'] = operation
            attribute['previous'] = value
        else:
            attribute['current'] = value


class AmbaMessage(object):
    
    fields_to_skip = {
        # E.g.:
        # 'INSTRUMENT': (
        #     'INSID',
        #     'INSADDR',
        # ),
        # 'TRADE': (
        #     'TRDNBR',
        #     'OPTIONAL_KEY',
        # ),
    }
    
    def __init__(self, mbf_object):
        self._msg = mbf_object
        self.operation = ''
        self.table_name = ''
        self._process_header()
        self._tables = self.create_tables(self._msg)
        self.parent_table = self._tables[0]
    
    def __str__(self):
        return '[%s]' % ', '.join([str(table) for table in self.get_tables()])
    
    @classmethod
    def create_tables(cls, mbf_object):
        tables = []
        table = None
        if not mbf_object.mbf_get_name() == 'MESSAGE':
            table = Table(mbf_object.mbf_get_name())
            tables.append(table)
        inner_object = mbf_object.mbf_first_object()
        while inner_object:
            field = inner_object.mbf_get_name()
            value = inner_object.mbf_get_value()
            if field == value and inner_object.mbf_first_object():
                if table:
                    table.children.extend(cls.create_tables(inner_object))
                else:
                    tables.extend(cls.create_tables(inner_object))
            elif table:
                table.add(field, value)
            inner_object = mbf_object.mbf_next_object()
        return tables
    
    @classmethod
    def skip_field_extract(cls, table_name, field_name):
        return (table_name in cls.fields_to_skip 
                and field_name in cls.fields_to_skip[table_name])
    
    @classmethod
    def extract_current_message(cls, current, table):
        if table.operation == 'DELETE':
            return
        sublist = current.mbf_start_list(table.name)
        for attr_name, attr_dict in table.attributes.items():
            if cls.skip_field_extract(table.name, attr_name):
                continue
            sublist.mbf_add_string(attr_name, attr_dict['current'])
        for subtable in table.children:
            cls.extract_current_message(sublist, subtable)
        sublist.mbf_end_list()
    
    @classmethod
    def extract_previous_message(cls, previous, table):
        if table.operation == 'INSERT':
            return
        sublist = previous.mbf_start_list(table.name)
        for attr_name, attr_dict in table.attributes.items():
            if cls.skip_field_extract(table.name, attr_name):
                continue
            value = attr_dict['current']
            if attr_dict['operation'] == 'UPDATE':
                value = attr_dict['previous']
            sublist.mbf_add_string(attr_name, value)
        for subtable in table.children:
            cls.extract_previous_message(sublist, subtable)
        sublist.mbf_end_list()
    
    def _process_header(self):
        headers = self._msg.mbf_read_header()
        for header in headers:
            if not header.mbf_get_name() == 'TYPE':
                continue
            type_values = header.mbf_get_value().split('_')
            if len(type_values) == 2:
                self.operation = type_values[0]
                self.table_name = type_values[1]
            else:
                self.table_name = type_values[0]
    
    def get_tables(self, name=''):
        tables = [self.parent_table]
        tables.extend(Table.get_children(self.parent_table))
        if not name:
            return tables
        return [table for table in tables if table.name == name]
    
    def get_current_message(self):
        header = [item.mbf_get_value() for item in self._msg.mbf_read_header()]
        current_msg = amb.mbf_start_message(None, *header)
        self.extract_current_message(current_msg, self.parent_table)
        return current_msg.mbf_end_message().mbf_object_to_string()
    
    def get_previous_message(self):
        header = [item.mbf_get_value() for item in self._msg.mbf_read_header()]
        previous_msg = amb.mbf_start_message(None, *header)
        self.extract_previous_message(previous_msg, self.parent_table)
        return previous_msg.mbf_end_message().mbf_object_to_string()


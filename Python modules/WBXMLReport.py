"""
Created on 25 Jun 2013

@author: conicova

Contains the classes used for the creation
of a XML, which is similar to the one generated 
from a Workbook.
"""
# import sys
# sys.path.append("Y:\JHB\Arena\CommonLib\PythonLib26")

import xml.etree.ElementTree as ElementTree
import io

class PrimeElement(object):
    """
    Contains functions that may be useful when creating the
    XML data structure. 
    """
    def add_value(self, parent, element_title, value):
        """
        Initialises and returns a new child element that
        is appended to the provided parent element with
        the provided value. 
        """
        sub_element = ElementTree.SubElement(parent, element_title)
        sub_element.text = str(value)
        return sub_element

class PrimeCell(PrimeElement):
    """
    Represents the Cell element from the Workbook XML
    """
    def __init__(self, raw_data='', default_data='', formatted_data=''):
        self.raw_data = raw_data
        self.default_data = default_data
        self.formatted_data = formatted_data
    
    def get_element(self):
        """
        Initialises and returns a new XML element
        that contains the Cell data.
        """
        parent = ElementTree.Element("Cell")
        
        self.add_value(parent, "RawData", self.raw_data)
        self.add_value(parent, "DefaultData", self.default_data)
        self.add_value(parent, "FormattedData", self.formatted_data)
        
        return parent

class PrimeRow(PrimeElement):
    """
    Represents the Row element from the Workbook XML
    """
    def __init__(self, label, row_id='', cells=[], rows=[]):
        self.label = label
        self.row_id = row_id
        self.cells = cells
        self.rows = rows
        
    def get_element(self):
        """
        Initialises and returns a new XML element
        that contains the Row data.
        """
        parent = ElementTree.Element("Row")
        
        self.add_value(parent, "Label", self.label)
        self.add_value(parent, "RowId", self.row_id)
        
        if self.rows:
            rows_element = self.add_value(parent, "Rows", "")
            for prime_child_row in self.rows:
                rows_element.append(prime_child_row.get_element())
        
        if self.cells:
            cells_element = self.add_value(parent, "Cells", "")
            for prime_cell in self.cells:
                cells_element.append(prime_cell.get_element())
        
        return parent
        
class PrimeColumn(PrimeElement):
    """
    Represents the Column element from the Workbook XML
    """
    def __init__(self, label, group_label='', column_id='', column_unique_id='', context=''):
        self.label = label
        self.group_label = group_label
        self.column_id = column_id
        self.column_unique_id = column_unique_id
        self.context = context
        
    def get_element(self):
        """
        Initialises and returns a new XML element
        that contains the Column data.
        """
        parent = ElementTree.Element("Column")
        
        self.add_value(parent, "ColumnId", self.column_id)
        self.add_value(parent, "ColumnUniqueId", self.column_unique_id)
        self.add_value(parent, "Context", self.context)
        self.add_value(parent, "Label", self.label)
        self.add_value(parent, "GroupLabel", self.group_label)
        
        return parent
   
class PrimeTable(PrimeElement):
    """
    Represents the Table element from the Workbook XML
    """
    def __init__(self, name, ttype, columns=[], rows=[]):
        self.name = name
        self.ttype = ttype
        self.columns = columns
        self.rows = rows
        
    def get_element(self):
        """
        Initialises and returns a new XML element
        that contains the Table data.
        """
        parent = ElementTree.Element("Table")
        
        self.add_value(parent, "Name", self.name)
        self.add_value(parent, "Type", self.ttype)
        self.add_value(parent, "NumberOfColumns", len(self.columns))

        if self.columns:
            columns_element = self.add_value(parent, "Columns", "")
            for prime_column in self.columns:
                columns_element.append(prime_column.get_element())
         
        if self.rows:
            rows_element = self.add_value(parent, "Rows", "")
            for prime_row in self.rows:
                rows_element.append(prime_row.get_element())
        
        return parent

class PrimeReport(PrimeElement):
    """
    Represents the PRIMEReport element from the Workbook XML
    """
   
    
    def __init__(self):
        self.name = ''
        self.rtype = ''
        self.time = ''
        self.local_time = ''
        self.arena_data_server = ''
        self.tables = []
    
    def get_element(self):
        """
        Initialises and returns a new XML element
        that contains the PRIMEReport data.
        """
        parent = ElementTree.Element("PRIMEReport")

        # add elements:
        self.add_value(parent, "Name", self.name)
        self.add_value(parent, "Type", self.rtype)
        self.add_value(parent, "Time", self.time)
        self.add_value(parent, "LocalTime", self.local_time)
        self.add_value(parent, "ArenaDataServer", self.arena_data_server)
        
        if self.tables:
            tables_element = self.add_value(parent, "ReportContents", "")
            for prime_table in self.tables:
                tables_element.append(prime_table.get_element())
        
        return parent

class WBXMLReport(PrimeElement):
    """ 
    Contains functions for the serialization of a PrimeReport
    instance to XML format
    """    
    @staticmethod
    def get_xml_tree(prime_report):
        """ 
        Returns an ElementTree representation of the 
        provided PrimeReport instance 
        """ 
        xml = prime_report.get_element()
        return ElementTree.ElementTree(xml)
    
    @classmethod
    def get_xml_str(cls, prime_report, encoding='ISO-8859-1'):
        """ 
        Returns the string representation of the
        provided PrimeReport instance
        """ 
        xml_tree = cls.get_xml_tree(prime_report)
        strio = io.StringIO()
        xml_tree.write(strio, encoding=encoding)
        result = strio.getvalue()
        strio.close()
        return result

def ael_main(dict_arg):
    pass

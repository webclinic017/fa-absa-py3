from __future__ import with_statement
from __future__ import print_function
"""
    Provides classes for parsing Front report xml.
    
    # some examples of interface and usage-------------------------------


    def example_header():
        data = Contents( 'test3.xml' )
        header = data.get_header()
        print (header.report_name)
        print (header.report_type)
        
    def example_settings():
        data = Contents( 'test3.xml' )
        for setting in data.get_settings():
            print (setting.column_id, setting.raw_data)

    def example_columns():
        data = Contents( 'test3.xml' )
        for column in data.get_columns():
            print (column.column_id)

    def example_rows():
        data = Contents( 'test3.xml' )
        for row in data.get_rows():
            for cell in row.cells:
                print (row.row_id, cell.column_unique_id, cell.raw_data)

    
    The Contents constructor can also take raw xml as a second parameter
"""


import xml.etree.cElementTree as ElementTree
from FReportMapperClasses import Row, Header, Setting, Column, Cell
import FLogger

logger = FLogger.FLogger( 'report_parser' )

#contents reader-----------------
class ContentsReader( object ):

    def __init__( self, xml ):
        self.xml = xml
        self.contents = ElementTree.XML( self.xml )
        self.xml = ElementTree.tostring(self.contents)
        self.xml = self.remove_unicode(self.xml)
        self.contents = ElementTree.XML( self.xml )
        
    def remove_unicode(self, xml):
        #remove space from formatted data
        xml = xml.replace('&#160;', ' ')
        return xml
            
    def get_map( self, elem ):
        return dict((c.tag, c.text) for p in elem.getiterator() for c in p )        
        
    def get_header( self ):
        header_data = {}
        report_name_elem = self.contents.find( "Name" )
        report_type_elem = self.contents.find( "Type" )
        sheet_type = self.contents.find( "ReportContents/Table/Type" )
        num_columns = self.contents.find( "ReportContents/Table/NumberOfColumns" )
        
        header_data[ report_name_elem.tag ] = report_name_elem.text
        header_data[ 'ReportType' ] = report_type_elem.text
        header_data[ 'SheetType' ] = sheet_type.text
        header_data[ num_columns.tag ] = num_columns.text
                
        return header_data
        
    def get_columns(self):
        columns = []
        columns_elem = self.contents.find( "ReportContents/Table/Columns" )
        columns_elems = columns_elem.findall( 'Column' )
        for column_elem in columns_elems:
            column_data = self.get_map( column_elem )
            column_data['Element'] = column_elem
            columns.append( column_data )
        return columns
            
    def get_settings(self):
        settings = []
        setting_elems = self.contents.find( "ReportContents/Table/Settings" )
        groups_elem = setting_elems.find( 'Groups' )
        for grp_elem in groups_elem:
            columns_elem = grp_elem.findall( 'Column' )
            values_elem = grp_elem.findall( 'Cell' )
            columns_and_values = list(zip( columns_elem, values_elem ))
            for column_elem, value_elem in columns_and_values:
                setting_d = {}
                col_d = self.get_map( column_elem )
                val_d = self.get_map( value_elem )
                setting_d.update( col_d )
                setting_d.update( val_d )
                settings.append( setting_d )
        return settings
        
    def recurse_rows( self, rows_elem=None, parent_row=None, keep_rows=None):
        if keep_rows == None:
            keep_rows = []
        rows = rows_elem.findall( 'Row' )
        for row in rows:
            keep_rows.append( ( row, parent_row ) )
            if row.find( "Rows" ):     
                self.recurse_rows( row.find( "Rows" ), row, keep_rows )
        return keep_rows
    
    def get_rows_elems( self ):
        first_rows_elem = self.contents.find( "ReportContents/Table/Rows" )
        rows = self.recurse_rows( first_rows_elem )
        return rows
    
    def get_cells( self, cells_elem ):
        cells = []
        for cell, column_data in zip( cells_elem, self.get_columns() ):
            cell_data = self.get_map( cell )
            cell_data[ 'ColumnUniqueId' ] = column_data.get( 'ColumnUniqueId' )
            cell_data[ 'ColumnId' ] = column_data.get( 'ColumnId' )
            cells.append( cell_data )
        return cells
                
    def get_rows( self ):
        rows = []
        for ( row_elem, parent_row_elem ) in self.get_rows_elems():
            row_data = {}
            row_id_elem = row_elem.find( 'RowId' )
            parent_row_id_elem = parent_row_elem.find( 'RowId' ) if parent_row_elem else None
            label_elem = row_elem.find( 'Label' )
            cells_elem  = row_elem.find( 'Cells' ) 
            
            row_data[ 'RowId' ] = row_id_elem.text
            if not parent_row_id_elem == None:
                row_data[ 'ParentRowId' ] = parent_row_id_elem.text
            else:
                 row_data[ 'ParentRowId' ] = None
            row_data[ 'Label' ] = label_elem.text
            row_data[ 'Cells' ] = self.get_cells( cells_elem )
            row_data['Element'] = row_elem
            row_data['Parent'] = parent_row_elem
            rows.append( row_data )
        return rows
    
    def write_to_file(self,file,close=True):
        self.tree().write(file)
        if close:
            file.close()
    
    def tree(self):
        return ElementTree.ElementTree(self.contents)
        
#defines public interface to data
class Contents( object ):
    def __init__( self, filename, xml=None ):
        self.filename = filename 
        self.reader = None
        self.xml = xml
        self.__init()
        
    def __init( self ):
        if not self.xml:
            try:
                with open( self.filename ) as f:
                    self.xml = f.read()
            except IOError as err:
                logger.ELOG( "File < %s > not found.", file )
        self.reader = ContentsReader( self.xml )
    
    def get_header( self ):
        header_data = self.reader.get_header()
        return Header( header_data )
        
    def get_settings( self ):
        return [ Setting( setting_data ) for setting_data in self.reader.get_settings() ]
                       
    def get_columns( self ):
        return [ Column( columns_data ) for columns_data in self.reader.get_columns() ]
                
    def get_rows( self ):
        return [ Row( row ) for row in self.reader.get_rows() ]
    
    def write_to_file(self,file,close=True):
        self.reader.write_to_file(file, close)
    
    def tree(self):
        return self.reader.contents
 

        





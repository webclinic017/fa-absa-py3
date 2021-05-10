"""
    Provides classes that map to Front report xml elements

"""


#mapper classes-----------------
class Header( object ):
    def __init__( self, header_data ):
        self.report_name = header_data.get( 'Name' )
        self.report_type = header_data.get( 'ReportType' )
        self.sheet_type = header_data.get( 'SheetType' )
        self.num_columns = header_data.get( 'NumberOfColumns' )
                
    def __repr__(self):
        return "<Header('%s','%s','%s', '%s')>" % ( self.report_name, self.report_type, self.sheet_type, self.num_columns )
    
    def __cmp__(self, other):        
        if not isinstance(other, self.__class__):
            return -1
        return cmp(self.report_name, other.report_name) and cmp(self.report_type, other.report_type) and cmp(self.sheet_type, other.sheet_type) and cmp(self.num_columns, other.num_columns) 

    def __hash__(self):
        return hash( self.report_name ) ^ hash( self.report_type ) ^ hash( self.sheet_type ) ^ hash( self.num_columns )
        
class Row( object ):
    def __init__( self, row_data ):
        self.row_id = row_data.get( 'RowId' )
        self.parent_row_id = row_data.get( 'ParentRowId' )
        self.row_label = row_data.get( 'Label' )
        self.row_instrument = row_data.get( 'Instrument' )
        self.row_portfolio = row_data.get( 'Portfolio' )
        self.index = row_data.get( 'ChildRowIndex' )
        self.elem = row_data.get( 'Element' )
        self.parent_elem = row_data.get( 'Parent' )
        self.parent_label = self.parent_elem.find('Label').text if self.parent_elem else None
        
        if row_data.get( 'Cells' ):
            self.cells = [ Cell( c ) for c in row_data.get( 'Cells' ) ]
        else:
            self.cells = []
        
        self.raw_data = {}
        for cell in self.cells:
            self.raw_data[cell.column_id] = str(cell.raw_data)
               
        
    def __repr__(self):
        return "<Row('%s','%s','%s')>" % ( self.row_id, self.parent_row_id, self.row_label )
    
    def __cmp__(self, other):        
        if not isinstance(other, self.__class__):
            return -1
        return cmp(self.row_id, other.row_id) 

    def __hash__(self):
        return hash( self.row_id )

        
class Column( object ):
    def __init__( self, column_data ):
        
        self.column_id = column_data.get( 'ColumnId' )
        self.column_unique_id = column_data.get( 'ColumnUniqueId' )
        self.column_label = column_data.get( 'Label' )
        self.group_label = column_data.get( 'GroupLabel' )
        self.context = column_data.get( 'Context' )
        self.raw_data = column_data.get( 'RawData' ) #for Settings
        self.elem = column_data.get( 'Element' )
        
        
    def __repr__(self):
        return "<Column('%s','%s')>" % ( self.column_id, self.column_unique_id )
    
    def __cmp__(self, other):        
        if not isinstance(other, self.__class__):
            return -1
        return cmp(self.column_unique_id, other.column_unique_id)

    def __hash__(self):
        return hash( self.column_unique_id )

class Setting( Column ):
    def __init__( self, setting_data ):
        Column.__init__( self, setting_data )
    
    def __repr__(self):
        return "<Setting('%s','%s')>" % ( self.column_id, self.column_unique_id )

class Cell( object ):
    def __init__( self, cell_data ):
        self.raw_data = cell_data.get( 'RawData' )
        self.formatted_data = cell_data.get( 'FormattedData' )
        self.column_unique_id = cell_data.get( 'ColumnUniqueId' )
        self.column_id = cell_data.get( 'ColumnId' )
        self.default_data = cell_data.get( 'DefaultData' )
        
                
    def __repr__(self):
        return "<Cell('%s', '%s', '%s')>" % ( self.column_id, self.raw_data, self.formatted_data )
        
    def __cmp__(self, other):        
        if not isinstance(other, self.__class__):
            return -1
        return cmp(self.raw_data, other.raw_data)
    
    def __hash__(self):
        return  hash(self.raw_data) 

"""-------------------------------------------------------------------------------------------------------
MODULE
    FPrimeXmlUtils - contains logic for building Prime xml reports
    
    (c) Copyright 2011 by SunGard FRONT ARENA. All rights reserved.

-------------------------------------------------------------------------------------------------------"""
import cStringIO
import xml.etree.cElementTree as ElementTree
from xml.etree.cElementTree import Element, Comment, SubElement

import acm
import FLogger

logger = FLogger.FLogger( 'FAReporting' )


class XmlTags( object ):
    MULTI_REPORT_BEGIN = '<MultiReport>'
    MULTI_REPORT_END = '</MultiReport>'
    PRIME_REPORT_BEGIN = '<PRIMEReport>'
    ROW_BEGIN = '<Row>'

class PrimeXmlReader( object ):
    """class for extracting elements from prime xml"""
    def __init__( self, xml ):
        self.xml = xml 
        self.element = ElementTree.XML( self.xml )
    
    def name( self ):
        return self.element.find( 'Name' )
    
    def type( self ):
        return self.element.find( 'Type' )
    
    def time( self ):
        return self.element.find( 'Time' )
    
    def local_time( self ):
        return self.element.find( 'LocalTime' )
    
    def arena_data_server( self ):
        return self.element.find( 'ArenaDataServer' )
                
    def table_name(self):
        return self.element.find("ReportContents/Table/Name")
        
    def table_type(self):
        return self.element.find("ReportContents/Table/Type")
    
    def number_of_columns(self):
        return self.element.find("ReportContents/Table/NumberOfColumns")

    def columns(self):
        return self.element.find("ReportContents/Table/Columns")
        
    def settings(self):
        return self.element.find("ReportContents/Table/Settings")
        
    def rows(self):
        return self.element.find("ReportContents/Table/Rows")
        
    @classmethod
    def get_elements_by_tag( cls, xml, tag ):
        element = ElementTree.XML( str( xml ) )
        return element.findall( tag )

class PrimeXmlBuilder( object ):
    """class for combining elements to form a complete xml string"""
    def __init__( self ):
        self.root = Element("PRIMEReport")
        self.static_data_copied = False
        self.reader = None
        
    def copy_static_data( self ):
        parent_node = self.root
        parent_node.append(self.xml_reader.name())
        parent_node.append(self.xml_reader.type())
        parent_node.append(self.xml_reader.time())
        parent_node.append(self.xml_reader.local_time())
        parent_node.append(self.xml_reader.arena_data_server())
        
        report_contents_node = SubElement(parent_node, "ReportContents")
        table_node = SubElement(report_contents_node, "Table")
        table_node.append(self.xml_reader.table_name())
        table_node.append(self.xml_reader.table_type())
        table_node.append(self.xml_reader.number_of_columns())
        
        table_node.append(self.xml_reader.columns())
        table_node.append(self.xml_reader.settings())
        
        self.static_data_copied = True
        
    def consume( self, xml ):
        self.xml_reader = PrimeXmlReader( xml )
        if not self.static_data_copied:
            self.copy_static_data()
        self.append_rows(self.xml_reader.rows()) 
            
    def append_rows(self, rows):
        table_node = self.root.find("ReportContents/Table")
        table_node.append(rows)
    
    def tree( self ):
        return ElementTree.ElementTree(self.root)

    def write_to_file(self,file,close=True):
        self.tree().write(file, encoding='ISO-8859-1')
        if close:
            file.close()

class PrimeXmlSheetWriter( object ):
    """class for writing xml to string for a trading manager sheet"""
    def __init__( self, sheet_name ):
        self.chunks = []
        self.sheet_name = sheet_name
    
    def xml_chunks( self, xml_chunk=None ):
        if xml_chunk != None:
            if self.is_valid_xml_chunk( xml_chunk ):
                self.chunks.append( xml_chunk )
        else:
            return self.chunks
    
    def is_valid_xml_chunk( self, xml_chunk ):
        """remove xml tags"""
        if xml_chunk and xml_chunk.find(XmlTags.ROW_BEGIN) != -1:
            return True
        else:
            logger.WLOG('Sheet ' + self.sheet_name + ' has no content.')
            self.chunks = []
            return False
    
    def get_xml_output( self ):
        """combine xml output"""
        b = PrimeXmlBuilder()
        if self.xml_chunks() and len(self.xml_chunks()) > 0:
            for chunk in self.xml_chunks():
                b.consume( chunk )
            output = cStringIO.StringIO()
            b.write_to_file( file=output, close=False )
            value = output.getvalue()
            output.close()
            return value
        else:
            return ""

class PrimeXmlReportWriter( object ):
    """class for combining sheet xml into complete report"""
            
    def __init__( self ):
        self.sheet_writers = []
            
    def reset( self ):
        self.sheet_writers = []
        
    def xml_sheet_writers( self, sheet_writer=None):
        if sheet_writer != None:
            self.sheet_writers.append( sheet_writer )
        else:
            return self.sheet_writers
    
    def is_multi_report( self ):
        return True if len( self.sheet_writers ) > 1 else False
        
    def get_xml_output( self ):
        """write prime report xml from sheet writers"""
        report_xml = ""
        
        if self.is_multi_report():
            report_xml = "<?xml version='1.0' encoding='ISO-8859-1'?>" # Stamp the encoding in, needs to be in start of the xml document. The actual encoding will take place in the sheet_writers objects
            report_xml = "".join( [ report_xml, XmlTags.MULTI_REPORT_BEGIN ] )
        
        for writer in self.xml_sheet_writers():
            xml_output = writer.get_xml_output()
            if self.is_multi_report():
                xml_output = xml_output[44:len(xml_output)] # Skip encoding part since we pasted it in ourselves for the multireport part.
            report_xml = "".join( [ report_xml, xml_output ] )
            
        if self.is_multi_report():
            report_xml = "".join( [ report_xml, XmlTags.MULTI_REPORT_END ] )
        
        return report_xml
        

""" Compiled: 2020-09-18 10:38:55 """

#__src_file__ = "extensions/ADSOrderBooksManager/./etc/OrderBooks2Xml.py"
""" -------------------------------------------------------------------------------------------------------
MODULE 
    FOrderBooksToXML - This script exports OrderBooks from database to AMS XML format. 
    
DESCRIPTION
    This script exports OrderBooks as specified by user in the XML format. The script creates XML based on 
    different contributions as specified by user on GUI. 
    
VERSION
    2015.3.011
    
----------------------------------------------------------------------------------------------------------"""

import acm

import os
import xml.etree.ElementTree
from datetime import datetime

import FRunScriptGUI
import FLogger
import csv

logger = FLogger.FLogger(name='FOrderBooksToXML')

def StartDialog(eii):

    acm.RunModuleWithParameters("OrderBooks2Xml", acm.GetDefaultContext()) 

"""
Default values
"""
CONTRIBUTION_BBG_FIX = "BBG-FIX Contribution" 
CONTRIBUTION_BBG_BLP = "BBG-BLP Contribution"
TRADEWEB = 'Tradeweb'
FIXTOOLKIT2_NATIVE = 'FixToolkit2 Native'
REUTERS_CONTRIBUTION = 'Reuters-Contribution'
CATS = 'Cats'
MARKETAXESS ='MarketAxess'
BBGCOMMODITIES ='BBG-Commodities'
xmlType_list = [FIXTOOLKIT2_NATIVE, CONTRIBUTION_BBG_FIX, CONTRIBUTION_BBG_BLP, REUTERS_CONTRIBUTION, CATS, MARKETAXESS, TRADEWEB, BBGCOMMODITIES]

max_decimals_in_price = [1, 2, 3, 4, 5, 6]
def_market_code_specifier = 2
tick_size_list_id = 'List_Default'
quote_factor = 1
Default_PrimaryMarketMIC = "xxxx"
TNP_unknown_instrument_type = 7
bbg_old_tiering_system = [1]
#bbg_load_indicator = 'A'
bbg_blp_load_indicators = ['ABSOLUTE_ORDER', 'MATURITY_ORDER']
bbg_identifier_types = ['PAGE_ACCESS_TYPE_ISIN', 'PAGE_ACCESS_TYPE_NONE', 'PAGE_ACCESS_TYPE_BBG_NUMBER', 'PAGE_ACCESS_TYPE_CUSIP', 'PAGE_ACCESS_TYPE_TICKER', 'PAGE_ACCESS_TYPE_NEW_ISIN']
def_feed_type = 'FeedType'
cats_ins_instype_to_export = ['Stock', 'EquityIndex', 'Bond', 'Convertible', 'Combination', 'FRN', 'CLN',\
                                            'Option', 'Warrant', 'Future/Forward']
max_date =  "20701231"
default_expiry_date = "20501231"
default_issue_date = "00000101"
default_first_trading_date = "00000101"
default_market_maker = "set your makert maker id for Cats"
market_instrument_id_type_list = ['ISIN', 'BB_TICKER', 'BB_GLOBAL', 'BB_UNIQUE', 'RIC', 'External ID1', 'External ID2']
market_place_code = {   CONTRIBUTION_BBG_FIX:       "BLTD", 
                        CONTRIBUTION_BBG_BLP:       "BLTD", 
                        REUTERS_CONTRIBUTION:       "RTSL", 
                        FIXTOOLKIT2_NATIVE:       "XXXX", 
                        CATS:       "XXXX", 
                        MARKETAXESS:       "MAEL", 
                        TRADEWEB:       "TREU", 
                        BBGCOMMODITIES:       "XXXX",
                    }

class XMLOperations():
    """ This class handles all xml operations like adding new tags to xml, validating XML text """
    
    def __init__(self):
        self.xml_header = """<?xml version="1.0" encoding="iso-8859-1" ?>"""
        
    def add_element(self, element):
        xml_element = xml.etree.ElementTree.Element(element)
        return xml_element
        
    def add_sub_element(self, parent, element, val=None):
        sub_element = xml.etree.ElementTree.SubElement(parent, element)
        if str(val).strip() != 'None' and str(val).strip() != '':
            sub_element.text = str(val)
        return sub_element
        
    def validate_text(self, element_text):
        """This method validates the text contents of element for special characters."""
        validated_text = ''
        if element_text:
            for char in element_text:
                if char == '&':
                    validated_text += '&amp;'
                elif char == '<':
                    validated_text += '&lt;'
                elif char == '>':
                    validated_text += '&gt;'
                elif char == '"':
                    validated_text += '&quot;'
                elif char == "'":
                    validated_text += '&apos;'
                elif ord(char) > 128:
                    validated_text += ''
                else:
                    validated_text += char
        return validated_text

    def pretty_print_element_tree(self, element, ind='',encoding=None ):
        """This method prints the element tree with proper indented element tags."""
        
        # start with indentation
        start = ind
        # put tag (don't close it just yet)
        
        element_tag = element.tag
        element_tag_list = []
        
        if element_tag_list:
            start = start.strip()
            for tag in element_tag_list:
                element.tag = tag
                start += self.pretty_print_element_tree(element, ind)+'\n'
            start = start.rstrip()
        else:
            start += '<' + element_tag
            # add all attributes
            for (name, value) in element.items():
                start += '    ' + name + '=' + "'%s'" % value
            # if there is text close start tag, add the text and add an end tag
            element_text = element.text            
            if type(element_text) == unicode or (element_text and str(element_text).strip()):
                start += '>' + self.validate_text(element_text) + '</' + element_tag + '>'
            else:
                # if there are children...
                if len(element) > 0:
                # close start tag
                    start += '>'
                # add every child in its own line indented
                    for child in element:
                        start += '\n' + self.pretty_print_element_tree(child, ind + '    ')
                # add closing tag in a new line
                    start += '\n' + ind + '</' + element_tag + '>'
                else:
                    # no text and no children, just close the starting tag
                    start += ' />'
        return start
            


class OrderBookToXml():
    """This is a base class to export orderbooks to XML format"""
    
    def __init__(self, market_place, market_segment, file_path):
        self.market_place = market_place
        self.market_segment = market_segment
        self.file_path = file_path
        self.orderbook_xml_file = None
        #self.xml_ops = None        
        self.db_ops = DBOperations()
        
    def generate_xml(self, orderbooks_in_db, market_place, market_segment):
        raise NotImplementedError
        
    def orderbook_to_xml(self):
            
        logger.DLOG("Check market place exist in db")
        market_place_in_db = self.db_ops.get_market_place(self.market_place)
        if not market_place_in_db:
            logger.ELOG("MarketPlace <%s> does not exist in database. Cannot proceed further"%self.market_place)

        if market_place_in_db:
            if self.market_segment:
                for each_seg in self.market_segment:
                    logger.LOG("Export orderbooks from MarketSegment <%s>, Market <%s>"%(self.market_place, str(each_seg).strip()))
                    orderbooks_in_db = self.db_ops.get_orderbooks_from_market(self.market_place, str(each_seg).strip())
                    if orderbooks_in_db:
                        logger.DLOG("orderbooks found in Market <%s>, MarketSegment <%s>"%(self.market_place, str(each_seg).strip()))
                        self.export_orderbooks(orderbooks_in_db, self.market_place, str(each_seg).strip())
                    else:
                        logger.ELOG("No orderbooks found in MarketPlace <%s>, MarketSegment <%s>"%(self.market_place, str(each_seg).strip()))
            else:
                logger.LOG("No MarketSegment specified by user, will export orderbooks from all segments")
                #market_segments = market_place_in_db.MarketSegments()
                market_segments = self.db_ops.get_market_segments(self.market_place)
                logger.DLOG("MarketSements found in Market %s"%market_segments)
                for each_seg in market_segments:
                    logger.LOG("Processing from MarketSegment <%s>"%each_seg)
                    orderbooks_in_db = self.db_ops.get_orderbooks_from_market(self.market_place, each_seg)
                    if orderbooks_in_db:
                        logger.DLOG("orderbooks found in Market <%s>, MarketSegment <%s>"%(self.market_place, each_seg))
                        self.export_orderbooks(orderbooks_in_db, self.market_place, each_seg)
                    else:
                        logger.ELOG("No orderbooks found in MarketPlace <%s>, MarketSegment <%s>"%(self.market_place, each_seg))
                        
                            
    def export_orderbooks(self, orderbooks_in_db, market_place, market_segment):
        logger.DLOG("export orderbooks")
        
        #orderbook_file_name = self.orderbook_export_file_name(market_place, market_segment)
        orderbook_file_name = market_place + '_' + market_segment + '_' + 'orderbooks.xml'
        logger.DLOG("OrderBook export file name %s"%orderbook_file_name)
        
        orderbook_xml = self.generate_xml(orderbooks_in_db, market_place, market_segment)
        
        if os.path.exists(self.file_path):
            orderbook_xml_file = os.path.join(self.file_path, orderbook_file_name) 
            if orderbook_xml and orderbook_xml_file:
                try:
                    orderbook_xml_file = os.path.join(orderbook_xml_file)
                    xml_file = open(orderbook_xml_file, 'w')
                    xml_file.write(self.xml_ops.xml_header)
                    xml_file.write("\n")
                    xml_file.write(orderbook_xml)
                    xml_file.close()
                    logger.LOG("Successfully exported OrderBooks to %s"%(orderbook_xml_file))
                except Exception as e:
                    logger.ELOG("Error exporting Orderbooks:"+str(e), exc_info=1)
        else:
            logger.ELOG("File path <%s> does not exist. Cannot export orderbooks to xml"%self.file_path)
            
        
    
class BBGContributionFIX(OrderBookToXml):
    """This class handles operations to export BBG-Contributions related data to XML."""
    
    def __init__(self, xml_type, market_place, market_segment, market_instrument_id_type, file_path, bbg_feed_type, bbg_tiering_system, page_id, page_sub_id, page_number, page_row_num, bbg_load_indicator, bbg_identifier_type, max_decimals):
        
        self.page_id = page_id
        self.page_sub_id = page_sub_id
        self.page_number = page_number
        self.page_row_num = page_row_num
        self.bbg_feed_type = bbg_feed_type
        self.bbg_tiering_system = bbg_tiering_system
        self.bbg_load_indicator = bbg_load_indicator
        self.bbg_identifier_type = bbg_identifier_type
        self.max_decimals = max_decimals
        self.db_ops = DBOperations()
        self.xml_ops = XMLOperations()
        self.xml_type = xml_type
        self.market_instrument_id_type = market_instrument_id_type        
        OrderBookToXml.__init__(self, market_place, market_segment, file_path)
        
    def generate_xml(self, orderbooks_in_db, market_place, market_segment):
        """Generated xml for orderbook with all required tags and values"""
        config_pretty_element_tree = None
        
        # Add <orderbooks> xml element
        orderbook_element = self.xml_ops.add_element('orderbooks')
        
        for each_orderbook in orderbooks_in_db:
            orderbook_ins = each_orderbook.Instrument()
            
            instrument_identifier = self.db_ops.get_market_ins_id( orderbook_ins, self.market_instrument_id_type)
            if instrument_identifier:
                logger.DLOG("Exporting OrderBook <%s>, Instrument <%s>, Market <%s>, MarketSegment <%s>"% \
                                            (each_orderbook.Name(), orderbook_ins.Name(), market_place, market_segment))
                # Add <tnporderbook> tag
                tnp_orderbook_element = self.xml_ops.add_sub_element(orderbook_element, 'tnporderbook')
                
                # Add sub elements to <tnporderbook>
                self.xml_ops.add_sub_element(tnp_orderbook_element, 'Name', each_orderbook.Name())
                self.xml_ops.add_sub_element(tnp_orderbook_element, 'RICCode', self.db_ops.get_instrument_ric(orderbook_ins))
                self.xml_ops.add_sub_element(tnp_orderbook_element, 'BLOOMBERGCode', instrument_identifier)
                self.xml_ops.add_sub_element(tnp_orderbook_element, 'MarketInstrumentId', instrument_identifier)
                self.xml_ops.add_sub_element(tnp_orderbook_element, 'ISINCode', orderbook_ins.Isin())
                self.xml_ops.add_sub_element(tnp_orderbook_element, 'PrimaryMarketMIC', Default_PrimaryMarketMIC)
                self.xml_ops.add_sub_element(tnp_orderbook_element, 'OrderBookId', each_orderbook.ExternalId())
                self.xml_ops.add_sub_element(tnp_orderbook_element, 'InstrumentType', self.db_ops.orderbook_instype(orderbook_ins))
                self.xml_ops.add_sub_element(tnp_orderbook_element, 'Currency', orderbook_ins.Currency().Name())                
                self.xml_ops.add_sub_element(tnp_orderbook_element, 'DefaultMarketplaceCodeSpecifier', str(def_market_code_specifier))
                self.xml_ops.add_sub_element(tnp_orderbook_element, 'TickSizeListId', tick_size_list_id)
                self.xml_ops.add_sub_element(tnp_orderbook_element, 'MarketplaceCode', market_place_code.get(self.xml_type, ''))                
                self.xml_ops.add_sub_element(tnp_orderbook_element, 'RoundLotSize', str(each_orderbook.RoundLot()))
                self.xml_ops.add_sub_element(tnp_orderbook_element, 'QuoteFactor', str(each_orderbook.QuoteFactor()))                
                self.xml_ops.add_sub_element(tnp_orderbook_element, 'DayCountMethod', each_orderbook.DayCounting())
                self.xml_ops.add_sub_element(tnp_orderbook_element, 'MaxDecimalsInPrice', self.max_decimals)
                self.xml_ops.add_sub_element(tnp_orderbook_element, 'BBGMDFeedType', self.bbg_feed_type)
                self.xml_ops.add_sub_element(tnp_orderbook_element, 'BBGMDStreamID', each_orderbook.ExternalType())
                self.xml_ops.add_sub_element(tnp_orderbook_element, 'BBGOldTieringSystem', self.bbg_tiering_system)
                
                # Add monitors to <tnoprderbook>
                self.add_monitors(tnp_orderbook_element, each_orderbook)
            else:
                logger.ELOG("No ISIN and ExternalID1 found for Instrument <%s>. Cannot export orderbook to XML"%orderbook_ins.Name())
        
        config_pretty_element_tree = self.xml_ops.pretty_print_element_tree(orderbook_element)   
        return config_pretty_element_tree        
                    
    def add_monitors(self, orderbook_tag, orderbook_obj):
        logger.DLOG("Adding Monitors to XML")
        # Add <monitors> to <tnporderbook>
        monitors_tag = self.xml_ops.add_sub_element(orderbook_tag, 'monitors')
        
        # Add <monitor> to <monitors>
        monitor_tag = self.xml_ops.add_sub_element(monitors_tag, 'monitor')
        
        # Add sub elements to <monitor>
        self.xml_ops.add_sub_element(monitor_tag, 'BBGloadIndicator', self.bbg_load_indicator)
        self.xml_ops.add_sub_element(monitor_tag, 'BBGidentifierType', self.bbg_identifier_type)
        self.xml_ops.add_sub_element(monitor_tag, 'BBGpageID', self.db_ops.get_addinfo(orderbook_obj, 'OrderBook', self.page_id))
        self.xml_ops.add_sub_element(monitor_tag, 'BBGpageSubID', self.db_ops.get_addinfo(orderbook_obj, 'OrderBook', self.page_sub_id))
        self.xml_ops.add_sub_element(monitor_tag, 'BBGpageNumber', self.db_ops.get_addinfo(orderbook_obj, 'OrderBook', self.page_number))
        self.xml_ops.add_sub_element(monitor_tag, 'BBGRowNum', self.db_ops.get_addinfo(orderbook_obj, 'OrderBook', self.page_row_num))
        logger.DLOG("Added Monitors for OrderBook <%s>"%orderbook_obj.Name())
        
        
class BBGContributionBLP(OrderBookToXml):
    """This class handles operations to export BBG-Controbution BLP related data to XML."""
    
    def __init__(self, xml_type, market_place, market_segment, market_instrument_id_type, file_path, bbg_contribution_type, page_id, page_sub_id, page_number, page_row_num, bbg_load_indicator, bbg_identifier_type, max_decimals):
        
        self.xml_type = xml_type
        self.market_instrument_id_type = market_instrument_id_type     
        self.page_id = page_id
        self.page_sub_id = page_sub_id
        self.page_number = page_number
        self.page_row_num = page_row_num
        self.bbg_contribution_type= bbg_contribution_type
        self.bbg_load_indicator = bbg_load_indicator
        self.bbg_identifier_type = bbg_identifier_type
        self.max_decimals = max_decimals
        self.db_ops = DBOperations()
        self.xml_ops = XMLOperations()        
        OrderBookToXml.__init__(self, market_place, market_segment, file_path)
        
    def generate_xml(self, orderbooks_in_db, market_place, market_segment):
        """Generated xml for orderbook with all required tags and values"""
        config_pretty_element_tree = None
        
        # Add <orderbooks> xml element
        orderbook_element = self.xml_ops.add_element('orderbooks')
        
        for each_orderbook in orderbooks_in_db:
            orderbook_ins = each_orderbook.Instrument()
            
            instrument_identifier = self.db_ops.get_market_ins_id( orderbook_ins, self.market_instrument_id_type)
            if instrument_identifier:
                logger.DLOG("Exporting OrderBook <%s>, Instrument <%s>, Market <%s>, MarketSegment <%s>"% \
                                            (each_orderbook.Name(), orderbook_ins.Name(), market_place, market_segment))
                # Add <tnporderbook> tag
                tnp_orderbook_element = self.xml_ops.add_sub_element(orderbook_element, 'tnporderbook')
                
                # Add sub elements to <tnporderbook>
                self.xml_ops.add_sub_element(tnp_orderbook_element, 'Name', each_orderbook.Name())
                self.xml_ops.add_sub_element(tnp_orderbook_element, 'RICCode', self.db_ops.get_instrument_ric(orderbook_ins))
                self.xml_ops.add_sub_element(tnp_orderbook_element, 'BLOOMBERGCode', instrument_identifier)
                self.xml_ops.add_sub_element(tnp_orderbook_element, 'MarketInstrumentId', instrument_identifier)
                self.xml_ops.add_sub_element(tnp_orderbook_element, 'ISINCode', orderbook_ins.Isin())
                self.xml_ops.add_sub_element(tnp_orderbook_element, 'PrimaryMarketMIC', Default_PrimaryMarketMIC)
                self.xml_ops.add_sub_element(tnp_orderbook_element, 'OrderBookId', each_orderbook.ExternalId())
                self.xml_ops.add_sub_element(tnp_orderbook_element, 'InstrumentType', self.db_ops.orderbook_instype(orderbook_ins))
                self.xml_ops.add_sub_element(tnp_orderbook_element, 'Currency', orderbook_ins.Currency().Name())                
                self.xml_ops.add_sub_element(tnp_orderbook_element, 'DefaultMarketplaceCodeSpecifier', str(def_market_code_specifier))
                self.xml_ops.add_sub_element(tnp_orderbook_element, 'TickSizeListId', tick_size_list_id)
                self.xml_ops.add_sub_element(tnp_orderbook_element, 'MarketplaceCode', market_place_code.get(self.xml_type, ''))                    
                self.xml_ops.add_sub_element(tnp_orderbook_element, 'RoundLotSize', str(each_orderbook.RoundLot()))
                self.xml_ops.add_sub_element(tnp_orderbook_element, 'QuoteFactor', str(each_orderbook.QuoteFactor()))                
                self.xml_ops.add_sub_element(tnp_orderbook_element, 'DayCountMethod', each_orderbook.DayCounting())
                self.xml_ops.add_sub_element(tnp_orderbook_element, 'MaxDecimalsInPrice', self.max_decimals)
                
                # Add monitors to <tnoprderbook>
                self.add_monitors(tnp_orderbook_element, each_orderbook)
            else:
                logger.ELOG("No ISIN and ExternalID1 found for Instrument <%s>. Cannot export orderbook to XML"%orderbook_ins.Name())
        
        config_pretty_element_tree = self.xml_ops.pretty_print_element_tree(orderbook_element)   
        return config_pretty_element_tree        
                    
    def add_monitors(self, orderbook_tag, orderbook_obj):
        logger.DLOG("Adding Monitors to XML")
                
        if self.bbg_contribution_type == 'Market Data': 
            self.xml_ops.add_sub_element(orderbook_tag, 'BBGContributionType', "M")
        else:
            self.xml_ops.add_sub_element(orderbook_tag, 'BBGContributionType', "P")
            
        self.xml_ops.add_sub_element(orderbook_tag, 'BBGloadIndicator', self.bbg_load_indicator)
        self.xml_ops.add_sub_element(orderbook_tag, 'BBGidentifierType', self.bbg_identifier_type)
        self.xml_ops.add_sub_element(orderbook_tag, 'BBGpageID', self.db_ops.get_addinfo(orderbook_obj, 'OrderBook', self.page_id))
        self.xml_ops.add_sub_element(orderbook_tag, 'BBGpageSubID', self.db_ops.get_addinfo(orderbook_obj, 'OrderBook', self.page_sub_id))
        self.xml_ops.add_sub_element(orderbook_tag, 'BBGpageNumber', self.db_ops.get_addinfo(orderbook_obj, 'OrderBook', self.page_number))
        self.xml_ops.add_sub_element(orderbook_tag, 'BBGRowNum', self.db_ops.get_addinfo(orderbook_obj, 'OrderBook', self.page_row_num))
        
        logger.DLOG("Added Monitors for OrderBook <%s>"%orderbook_obj.Name())
  
 
class FixToolkitNative(OrderBookToXml):
    """This class handles operations to export native fixtoolkit2 related data to XML."""
    
    def __init__(self, xml_type, market_place, market_segment, market_instrument_id_type, file_path, max_decimals):
    
        self.market_instrument_id_type = market_instrument_id_type     
        self.xml_type = xml_type
        self.max_decimals = max_decimals
        self.db_ops = DBOperations()
        self.xml_ops = XMLOperations()
        OrderBookToXml.__init__(self, market_place, market_segment, file_path)
        
    def generate_xml(self, orderbooks_in_db, market_place, market_segment):
        """Generated xml for orderbook with all required tags and values"""
        config_pretty_element_tree = None
        
        # Add <orderbooks> xml element
        orderbook_element = self.xml_ops.add_element('orderbooks')
        
        for each_orderbook in orderbooks_in_db:
            orderbook_ins = each_orderbook.Instrument()
            
            instrument_identifier = self.db_ops.get_market_ins_id( orderbook_ins, self.market_instrument_id_type)
            if instrument_identifier:
                logger.DLOG("Exporting OrderBook <%s>, Instrument <%s>, Market <%s>, MarketSegment <%s>"% \
                                            (each_orderbook.Name(), orderbook_ins.Name(), market_place, market_segment))
                # Add <tnporderbook> tag
                tnp_orderbook_element = self.xml_ops.add_sub_element(orderbook_element, 'tnporderbook')
                
                # Add sub elements to <tnporderbook>                
                self.xml_ops.add_sub_element(tnp_orderbook_element, 'Name', each_orderbook.Name())
                self.xml_ops.add_sub_element(tnp_orderbook_element, 'RICCode', self.db_ops.get_instrument_ric(orderbook_ins))
                self.xml_ops.add_sub_element(tnp_orderbook_element, 'BLOOMBERGCode', instrument_identifier)
                self.xml_ops.add_sub_element(tnp_orderbook_element, 'ISINCode', orderbook_ins.Isin())
                self.xml_ops.add_sub_element(tnp_orderbook_element, 'OrderBookId', each_orderbook.ExternalId())
                self.xml_ops.add_sub_element(tnp_orderbook_element, 'InstrumentType', self.db_ops.orderbook_instype(orderbook_ins))
                self.xml_ops.add_sub_element(tnp_orderbook_element, 'Currency', orderbook_ins.Currency().Name())
                self.xml_ops.add_sub_element(tnp_orderbook_element, 'MarketInstrumentId', instrument_identifier)
                self.xml_ops.add_sub_element(tnp_orderbook_element, 'DefaultMarketplaceCodeSpecifier', str(def_market_code_specifier))
                self.xml_ops.add_sub_element(tnp_orderbook_element, 'TickSizeListId', tick_size_list_id)
                self.xml_ops.add_sub_element(tnp_orderbook_element, 'MarketplaceCode', market_place_code.get(self.xml_type, ''))                    
                self.xml_ops.add_sub_element(tnp_orderbook_element, 'RoundLotSize', str(each_orderbook.RoundLot()))
                self.xml_ops.add_sub_element(tnp_orderbook_element, 'QuoteFactor', str(each_orderbook.QuoteFactor()))                
                self.xml_ops.add_sub_element(tnp_orderbook_element, 'DayCountMethod', each_orderbook.DayCounting())
                self.xml_ops.add_sub_element(tnp_orderbook_element, 'MaxDecimalsInPrice', self.max_decimals)
                
            else:
                logger.ELOG("No ISIN and ExternalID1 found for Instrument <%s>. Cannot export orderbook to XML"%orderbook_ins.Name())
        
        config_pretty_element_tree = self.xml_ops.pretty_print_element_tree(orderbook_element)   
        return config_pretty_element_tree        
        
      
class ReutersContributions(OrderBookToXml):
    """This class handles operations to export Reuters-Controbutions related data to XML."""
    
    def __init__(self, xml_type, market_place, market_segment, file_path, generate_ric_from_isin, max_decimals):
         
        self.xml_type = xml_type
        self.generate_ric_from_isin = generate_ric_from_isin
        self.max_decimals = max_decimals
        self.db_ops = DBOperations()
        self.xml_ops = XMLOperations()
        OrderBookToXml.__init__(self, market_place, market_segment, file_path)
        
    def generate_xml(self, orderbooks_in_db, market_place, market_segment):
        """Generated xml for orderbook with all required tags and values"""
        config_pretty_element_tree = None
        
        # Add <orderbooks> xml element
        orderbook_element = self.xml_ops.add_element('orderbooks')
        
        for each_orderbook in orderbooks_in_db:
            orderbook_ins = each_orderbook.Instrument()
            
            instrument_ric = self.generate_ins_ric_from_isin(orderbook_ins, self.generate_ric_from_isin)
            if instrument_ric:
                instrument_identifier = self.db_ops.get_orderbook_market_instrument_id(orderbook_ins)
                if instrument_identifier:
                    logger.DLOG("Exporting OrderBook <%s>, Instrument <%s>, Market <%s>, MarketSegment <%s>"% \
                                                (each_orderbook.Name(), orderbook_ins.Name(), market_place, market_segment))
                    # Add <tnporderbook> tag
                    tnp_orderbook_element = self.xml_ops.add_sub_element(orderbook_element, 'tnporderbook')
                    
                    # Add sub elements to <tnporderbook>
                    self.xml_ops.add_sub_element(tnp_orderbook_element, 'Name', each_orderbook.Name())
                    self.xml_ops.add_sub_element(tnp_orderbook_element, 'RICCode', instrument_ric)                   
                    
                    self.xml_ops.add_sub_element(tnp_orderbook_element, 'PrimaryMarketMIC', Default_PrimaryMarketMIC)
                    self.xml_ops.add_sub_element(tnp_orderbook_element, 'OrderBookId', each_orderbook.ExternalId())
                    self.xml_ops.add_sub_element(tnp_orderbook_element, 'InstrumentType', self.db_ops.orderbook_instype(orderbook_ins))
                    self.xml_ops.add_sub_element(tnp_orderbook_element, 'Currency', orderbook_ins.Currency().Name())
                    self.xml_ops.add_sub_element(tnp_orderbook_element, 'MarketInstrumentId', instrument_identifier)
                    self.xml_ops.add_sub_element(tnp_orderbook_element, 'ISINCode', orderbook_ins.Isin())
                    self.xml_ops.add_sub_element(tnp_orderbook_element, 'DefaultMarketplaceCodeSpecifier', str(def_market_code_specifier))
                    self.xml_ops.add_sub_element(tnp_orderbook_element, 'TickSizeListId', tick_size_list_id)
                    self.xml_ops.add_sub_element(tnp_orderbook_element, 'MarketplaceCode', market_place_code.get(self.xml_type, '')) 
                    self.xml_ops.add_sub_element(tnp_orderbook_element, 'RoundLotSize', str(each_orderbook.RoundLot()))
                    self.xml_ops.add_sub_element(tnp_orderbook_element, 'QuoteFactor', str(each_orderbook.QuoteFactor()))                    
                    self.xml_ops.add_sub_element(tnp_orderbook_element, 'DayCountMethod', each_orderbook.DayCounting())
                    self.xml_ops.add_sub_element(tnp_orderbook_element, 'MaxDecimalsInPrice', self.max_decimals)
                    
                else:
                    logger.ELOG("No ISIN and ExternalID1 found for Instrument <%s>. Cannot export orderbook to XML"%orderbook_ins.Name())
        
        config_pretty_element_tree = self.xml_ops.pretty_print_element_tree(orderbook_element)   
        return config_pretty_element_tree  
        
    def generate_ins_ric_from_isin(self, instrument, generate_ric_from_isin):
        ins_ric = None        
        if instrument:
            ins_ric = self.db_ops.get_market_ins_id( instrument, "RIC" )
            if not ins_ric:
                if generate_ric_from_isin:                    
                    if instrument.Isin():
                        logger.LOG("No RIC found for Instrument <%s>, generating RIC from ISIN"%instrument.Name())
                        ins_ric = str(instrument.Isin()) + "=XLS"
                        logger.DLOG("Generated RIC = %s"%ins_ric)
                    else:
                        logger.ELOG("Cannot export OrderBook for Instrument <%s> as both ISIN and RIC not present in database"%instrument.Name())
                else:
                    logger.ELOG("Cannot export OrderBook for Instrument <%s> as RIC not present in database"%instrument.Name())
        return ins_ric
        
        
        
class Cats(OrderBookToXml):
    """This class handles operations to export Cats related data to XML."""
    
    def __init__(self, xml_type, market_place, market_segment, file_path, max_decimals, generate_wkn_from_isin):
        
        self.xml_type = xml_type
        self.max_decimals = max_decimals
        self.generate_wkn_from_isin = generate_wkn_from_isin
        self.db_ops = DBOperations()
        self.xml_ops = XMLOperations()
        #self.file_path = file_path
        OrderBookToXml.__init__(self, market_place, market_segment, file_path)
         
    def generate_xml(self, orderbooks_in_db, market_place, market_segment):
        """Generated xml for orderbook with all required tags and values"""
        config_pretty_element_tree = None
        
        # Add <orderbooks> xml element
        orderbook_element = self.xml_ops.add_element('orderbooks')
        
        for each_orderbook in orderbooks_in_db:
            orderbook_ins = each_orderbook.Instrument()
            instrument_wkn = self.generate_ins_wkn_from_isin(orderbook_ins, self.generate_wkn_from_isin)
            if instrument_wkn:
                instrument_identifier = self.db_ops.get_orderbook_market_instrument_id(orderbook_ins)
                if instrument_identifier:
                    logger.DLOG("Exporting OrderBook <%s>, Instrument <%s>, Market <%s>, MarketSegment <%s>"% \
                                                (each_orderbook.Name(), orderbook_ins.Name(), market_place, market_segment))
                    # Add <tnporderbook> tag
                    tnp_orderbook_element = self.xml_ops.add_sub_element(orderbook_element, 'tnporderbook')
                    
                    # Add sub elements to <tnporderbook>
                    self.xml_ops.add_sub_element(tnp_orderbook_element, 'Name', each_orderbook.Name())
                    self.xml_ops.add_sub_element(tnp_orderbook_element, 'NameAlt1', instrument_wkn)
                    self.xml_ops.add_sub_element(tnp_orderbook_element, 'OrderBookId', each_orderbook.ExternalId())
                    self.xml_ops.add_sub_element(tnp_orderbook_element, 'PrimaryMarketMIC', Default_PrimaryMarketMIC)
                    self.xml_ops.add_sub_element(tnp_orderbook_element, 'InstrumentType', self.db_ops.orderbook_instype(orderbook_ins))
                    self.xml_ops.add_sub_element(tnp_orderbook_element, 'Currency', orderbook_ins.Currency().Name())                    
                    self.xml_ops.add_sub_element(tnp_orderbook_element, 'DefaultMarketplaceCodeSpecifier', str(def_market_code_specifier))
                    self.xml_ops.add_sub_element(tnp_orderbook_element, 'TickSizeListId', tick_size_list_id)
                    self.xml_ops.add_sub_element(tnp_orderbook_element, 'MarketplaceCode', market_place_code.get(self.xml_type, '')) 
                    self.xml_ops.add_sub_element(tnp_orderbook_element, 'RoundLotSize', str(each_orderbook.RoundLot()))
                    self.xml_ops.add_sub_element(tnp_orderbook_element, 'QuoteFactor', str(each_orderbook.QuoteFactor()))
                    self.xml_ops.add_sub_element(tnp_orderbook_element, 'ISINCode', orderbook_ins.Isin())
                    self.xml_ops.add_sub_element(tnp_orderbook_element, 'MarketInstrumentId', instrument_identifier)
                    self.xml_ops.add_sub_element(tnp_orderbook_element, 'DayCountMethod', each_orderbook.DayCounting())
                    self.xml_ops.add_sub_element(tnp_orderbook_element, 'MaxDecimalsInPrice', self.max_decimals)
                    if orderbook_ins.InsType() in ['Option', 'Warrant', 'Future/Forward']:
                        self.xml_ops.add_sub_element(tnp_orderbook_element, 'OptionSubType', 5)
                        self.xml_ops.add_sub_element(tnp_orderbook_element, 'UnderlyingInstrumentName', self.db_ops.ins_underlying(orderbook_ins))
                        self.xml_ops.add_sub_element(tnp_orderbook_element, 'Underlying', self.db_ops.underlying_ins_isin(orderbook_ins))
                        self.xml_ops.add_sub_element(tnp_orderbook_element, 'StrikePrice', self.db_ops.ins_strike_price(orderbook_ins))
                        self.xml_ops.add_sub_element(tnp_orderbook_element, 'ExpirationDateTime.DateTime', str(self.db_ops.ins_expiry(orderbook_ins)) + '235900')
                        self.xml_ops.add_sub_element(tnp_orderbook_element, 'ExerciseType', 0)
                        self.xml_ops.add_sub_element(tnp_orderbook_element, 'ContractSize', str(orderbook_ins.ContractSize()))
                        self.xml_ops.add_sub_element(tnp_orderbook_element, 'PutCallIndicator', self.db_ops.put_call_indicator(orderbook_ins))
                        self.xml_ops.add_sub_element(tnp_orderbook_element, 'PayType', self.db_ops.ins_pay_type(orderbook_ins))
                        self.xml_ops.add_sub_element(tnp_orderbook_element, 'MaturityYearMonth', str(self.db_ops.ins_expiry(orderbook_ins))[0:6])
                    
                else:
                    logger.ELOG("No ISIN and ExternalID1 found for Instrument <%s>. Cannot export orderbook to XML"%orderbook_ins.Name())
        
        config_pretty_element_tree = self.xml_ops.pretty_print_element_tree(orderbook_element)   
        return config_pretty_element_tree 
        
    def generate_ins_wkn_from_isin(self, instrument, generate_wkn_from_isin):
        ins_wkn = None
        logger.DLOG("Generate WKN from ISIN")
        if instrument:
            ins_wkn = self.db_ops.get_instrument_wkn(instrument)
            if not ins_wkn:
                if generate_wkn_from_isin:
                    if instrument.Isin():
                        logger.LOG("No WKN found for Instrument <%s>, generating WKN from ISIN"%instrument.Name())
                        ins_isin = str(instrument.Isin()) 
                        tmpWkn=ins_isin[-7:]
                        ins_wkn=tmpWkn[:6]
                        logger.DLOG("Generated WKN = %s"%ins_wkn)
                    else:
                        logger.ELOG("Cannot export OrderBook for Instrument <%s> as both ISIN and WKN not present in database"%instrument.Name())
                else:
                    logger.ELOG("Cannot export OrderBook for Instrument <%s> as WKN not present in database"%instrument.Name())
        return ins_wkn
        
    def orderbook_to_cats_file(self, market_place, market_segment, issuer):
        logger.DLOG("Orderbook to Cats file")
        if market_place:
            if os.path.exists(self.file_path):
                if market_segment:
                    for each_seg in market_segment: 
                        logger.LOG("Processing orderbooks for Cats file from Market %s MarketSegment %s"%(market_place, str(each_seg).strip()))
                        cats_file_name = 'RFQ_' + str(market_place).strip() + '_' + str(each_seg).strip() + '_orderbooks.dat'
                        logger.DLOG("Cats file name = %s"%cats_file_name)
                        orderbook_exported_cats_file_count = 0
                        orderbooks_in_db = self.db_ops.get_orderbooks_from_market(market_place, str(each_seg).strip())
                        if orderbooks_in_db:
                            logger.DLOG("Export orderbooks to cats file from Market <%s> MarketSegment <%s>"%(market_place, str(each_seg).strip()))
                            orderbook_cats_file = os.path.join(self.file_path, cats_file_name)
                            with open(orderbook_cats_file, 'w') as cats_file:
                                orderbook_exported_cats_file_count = self.export_orderbooks_to_cats_file(orderbooks_in_db, \
                                                market_place, str(each_seg).strip(), issuer, cats_file, orderbook_exported_cats_file_count)
                                if orderbook_exported_cats_file_count > 0:
                                    logger.LOG("Successfully exported oderbooks from MarketPlace <%s> MarketSegment <%s> to Cats file %s "% \
                                                (market_place, str(each_seg).strip(), orderbook_cats_file))
                                    self.make_Z_reocord_cats(cats_file, issuer, orderbook_exported_cats_file_count)
                        else:
                            logger.ELOG("No orderbooks found in MarketPlace <%s>, MarketSegment <%s>"%(market_place, str(each_seg).strip()))
                else:
                    logger.LOG("No MarketSegment specified by user, will export orderbooks from all segments")
                    #market_segments = market_place_in_db.MarketSegments()
                    market_segments = self.db_ops.get_market_segments(market_place)
                    logger.DLOG("MarketSements found in Market %s"%market_segments)
                    for each_seg in market_segments:
                        logger.DLOG("Processing for cats file from MarketSegment <%s>"%each_seg)
                        cats_file_name = 'RFQ_' + str(market_place).strip() + '-' + str(each_seg).strip() + '_orderbooks.dat'
                        logger.DLOG("Cats file name = %s"%cats_file_name)
                        orderbook_exported_cats_file_count = 0
                        orderbooks_in_db = self.db_ops.get_orderbooks_from_market(market_place, each_seg)
                        if orderbooks_in_db:
                            logger.DLOG("Export orderbooks to cats file from Market <%s> MarketSegment <%s>"%(market_place, each_seg))
                            orderbook_cats_file = os.path.join(self.file_path, cats_file_name)
                            with open(orderbook_cats_file, 'w') as cats_file:
                                orderbook_exported_cats_file_count = self.export_orderbooks_to_cats_file(orderbooks_in_db, market_place, \
                                                                            each_seg, issuer, cats_file, orderbook_exported_cats_file_count)
                                if orderbook_exported_cats_file_count > 0:
                                    logger.LOG("Successfully exported oderbooks from MarketPlace <%s> MarketSegment <%s> to Cats file %s "% \
                                                    (market_place, str(each_seg).strip(), orderbook_cats_file))
                                    self.make_Z_reocord_cats(cats_file, issuer, orderbook_exported_cats_file_count)
                        else:
                            logger.ELOG("No orderbooks found in MarketPlace <%s>, MarketSegment <%s>"%(market_place, each_seg))                

    def get_orderbook_data_for_cats(self, orderbook_ins, each_orderbook, issuer, ins_wkn):
        logger.DLOG("Get data to export in cats file")
        strike_price = self.db_ops.ins_strike_price(orderbook_ins)
        put_or_call = self.db_ops.ins_put_or_call(orderbook_ins)
        prod_type = self.cats_prod_type(orderbook_ins)
        underlying_ins = self.db_ops.ins_underlying(orderbook_ins)
        lot_size = self.db_ops.orderbook_lot_size(each_orderbook)
        limit_price_type = self.cats_limit_price_type(orderbook_ins)
        trading_symbol = self.cats_trading_symbol(orderbook_ins)
        issue_date = self.db_ops.ins_issue_date(orderbook_ins)
        first_trading_day = self.db_ops.ins_first_tarding_day(orderbook_ins)
        redemption_date = self.db_ops.ins_redemption_date(orderbook_ins)
        open_end = self.cats_open_end(orderbook_ins)
        dirty_signal = self.cats_dirty_signal(orderbook_ins)
        accrued_signal = self.cats_accrued_signal(orderbook_ins)
        barrier_breached = self.cats_barrier_breached(orderbook_ins)
        ins_barrier = self.cats_barrier(orderbook_ins)
        
        cats_data = [
                        ['RecordType',          ''                                                      ],
                        ['isin',              str(orderbook_ins.Isin())                               ],
                        ['wkn',                str(ins_wkn)                                            ],
                        ['issuerID',          str(issuer)                                             ],
                        ['expirydate',         str(self.db_ops.ins_expiry(orderbook_ins))              ],
                        ['lastTradeDate',       ''                                                      ],
                        ['instrumentGroup',     'DEFAULT',                                              ],
                        ['description',        str(orderbook_ins.Name())                              ],
                        ['strikeprice',                      strike_price                                ],
                        ['ratio',                            ''                                          ],
                        ['exoticFeatures',                   ''                                          ],
                        ['putorcall',                        put_or_call                                 ],
                        ['prodType',                         prod_type                                   ],
                        ['underlying',                       underlying_ins                              ],
                        ['lotSize',                          str(lot_size)                               ],
                        ['limitPriceType',                   limit_price_type                            ],
                        ['localCode',                        ''                                          ],
                        ['market',                           ''                                          ],
                        ['optAttribute',                     ''                                          ],
                        ['calculatedMinimumPrice',           ''                                          ],
                        ['barrierPrice',                     ''                                          ],
                        ['instrumentDeviationCent',          ''                                          ],
                        ['instrumentDeviationPercent',       ''                                          ],
                        ['marketMakerSystemIdentifier',      ''                                          ],
                        ['currency',                         orderbook_ins.Currency().Name()             ],
                        ['tradingSymbol',                    str(trading_symbol)                         ],
                        ['issueDate',                        issue_date                                  ],
                        ['firstTradingDay',                  first_trading_day                           ],
                        ['lastTradingTime',                  '23:00'                                     ],
                        ['redemptionDate',                   redemption_date                             ],
                        ['openEndSignal',                    open_end                                    ],
                        ['SVSPCode',                         '9999'                                      ],
                        ['dayCodeMethod',                    '2'                                         ],
                        ['dirtySignal',                      dirty_signal                                ],
                        ['accruedSignal',                    accrued_signal                              ],
                        ['barrierBreached',                  barrier_breached                            ],
                        ['barrier',                          ins_barrier                                 ],
    
                    ]
                    
        return cats_data
        
                    
    def export_orderbooks_to_cats_file(self, orderbooks_in_db, market_place, market_segment, issuer, cats_file, orderbook_exported_count):
        
        if cats_file:
            for each_orderbook in orderbooks_in_db:
                orderbook_ins = each_orderbook.Instrument()
                if orderbook_ins:
                    instrument_wkn = self.generate_ins_wkn_from_isin(orderbook_ins, self.generate_wkn_from_isin)
                    if instrument_wkn:
                        cats_data = self.get_orderbook_data_for_cats(orderbook_ins, each_orderbook, issuer, instrument_wkn) 
                        if cats_data:
                            for data in cats_data:
                                strline = ''
                                strline = strline + str(data[1])
                                cats_file.write(strline)
                                cats_file.write('|')
                            cats_file.write('\n')
                            orderbook_exported_count = orderbook_exported_count + 1
                    else:
                        logger.ELOG("No ISIN, ExternalID1 and Alias WKN found for Instrument <%s>. Cannot export orderbook to Cats file"%orderbook_ins.Name())
            
        else:
            logger.ELOG("File path <%s> does not exist. Cannot export orderbooks to xml"%self.file_path)
           
        return orderbook_exported_count
            
    def make_Z_reocord_cats(self, cats_file, issuer, exported_orderbook_count):
        logger.DLOG("Add Zrecord cats")
        datenow = datetime.now().strftime("%Y%m%d")
        
        writeStr='Z'+'|'
        writeStr=writeStr+issuer+'|'
        writeStr=writeStr+str(exported_orderbook_count)+'|'
        writeStr=writeStr+issuer+'|'
        writeStr=writeStr+datenow+'|'+'\n'  
        try:
            cats_file.write(writeStr) 
        except Exception as e:
            logger.ELOG("Cannot write Zrecord to Cats.bat file")
            logger.ELOG("Error: %s"%str(e), exc_info=1)
            
    def cats_limit_price_type(self, ins):
        logger.DLOG("Get cats limit price type")
        limit_price_type = ''
        if (ins.InsType() in ['Stock', 'EquityIndex', 'Bond', 'Convertible', 'Combination', 'FRN', 'CLN']):
            limit_price_type = "LP1"
        elif (ins.InsType() in ['Option', 'Warrant', 'Future/Forward']):
            limit_price_type = "LPR"
        return limit_price_type        
               
    def cats_prod_type(self, ins):
        logger.DLOG("Get cats prod type")
        prod_type = ""
        if (ins.InsType() in ['Stock', 'EquityIndex', 'Bond', 'Convertible', 'Combination', 'FRN', 'CLN']):
            prod_type = "Bond"
        elif (ins.InsType() in ['Option', 'Warrant', 'Future/Forward']):
            prod_type='Warrant'
        return prod_type
        
    def cats_open_end(self, ins):
        logger.DLOG("Get cats open end")
        open_end = ''
        cats_open_end = ins.OpenEnd()
        if (cats_open_end == 1):
            open_end = 'T'
        elif (cats_open_end == 0):
            open_end = 'F'  
        elif (cats_open_end == 2):
            open_end = 'F'
        else:
            open_end = 'F'
        return open_end
        
    def cats_dirty_signal(self, ins):
        logger.DLOG("Get cats dirty signal")
        dirty_signal = ''
        ins_quotation = ins.Quotation()
        cats_dirty_signal = ins_quotation.Clean()
        if (cats_dirty_signal == 1):
            dirty_signal = 'T'
        else:
            dirty_signal = 'F' 
        return dirty_signal
        
    def cats_accrued_signal(self, ins):
        logger.DLOG("Get cats accrued signal")
        accrued_signal = ''
        ins_accrued_signal = ins.AccruedArrear()
        if (ins_accrued_signal == 1):
            accrued_signal = 'T'
        else: 
            accrued_signal = 'F' 
        return accrued_signal
        
    def cats_barrier_breached(self, ins):
        logger.DLOG("Get cats barrier breached")
        try: 
            barrier_breached_enum = acm.FExotic.read[str(ins.insaddr)].BarrierCrossedStatus()
            if (barrier_breached_enum == 'Crossed'):
                barrier_breached = 'T'
            elif (barrier_breached_enum == 'Confirmed'):
                barrier_breached = 'T'
            else:
                barrier_breached = 'F'
        except:
            barrier_breached = 'F'
        return barrier_breached
        
    def cats_barrier(self, ins):
        logger.DLOG("Get cats barrier")
        barrier = ''
        if ins.InsType() in ['Option', 'Warrant']:
            barrier = ins.Barrier()
        return barrier 
           
    def cats_trading_symbol(self, ins):
        logger.DLOG("Get cats trading symbol")
        tradingSymbol  = ''
        try:
            tradingSymbol = ael.InstrumentAlias.read('insaddr=' + str(ins.Oid())).alias
        except:
            tradingSymbol = ins.Name()[:6] 
        return tradingSymbol
        
        
class MarketAxess(OrderBookToXml):
    """This class handles operations to export BBG-Controbutions related data to XML."""
    
    def __init__(self, xml_type, market_place, market_segment, file_path, max_decimals):
         
        self.xml_type = xml_type
        self.max_decimals = max_decimals
        self.db_ops = DBOperations()
        self.xml_ops = XMLOperations()
        OrderBookToXml.__init__(self, market_place, market_segment, file_path)
        
    def generate_xml(self, orderbooks_in_db, market_place, market_segment):
        """Generated xml for orderbook with all required tags and values"""
        config_pretty_element_tree = None
        
        # Add <orderbooks> xml element
        orderbook_element = self.xml_ops.add_element('orderbooks')
        
        for each_orderbook in orderbooks_in_db:
            orderbook_ins = each_orderbook.Instrument()
            
            instrument_identifier = self.db_ops.get_orderbook_market_instrument_id(orderbook_ins)
            if instrument_identifier:
                logger.DLOG("Exporting OrderBook <%s>, Instrument <%s>, Market <%s>, MarketSegment <%s>"% \
                                            (each_orderbook.Name(), orderbook_ins.Name(), market_place, market_segment))
                # Add <tnporderbook> tag
                tnp_orderbook_element = self.xml_ops.add_sub_element(orderbook_element, 'tnporderbook')
                
                # Add sub elements to <tnporderbook>
                self.xml_ops.add_sub_element(tnp_orderbook_element, 'Name', each_orderbook.Name())
                self.xml_ops.add_sub_element(tnp_orderbook_element, 'PrimaryMarketMIC', Default_PrimaryMarketMIC)
                self.xml_ops.add_sub_element(tnp_orderbook_element, 'OrderBookId', each_orderbook.ExternalId())
                self.xml_ops.add_sub_element(tnp_orderbook_element, 'InstrumentType', self.db_ops.orderbook_instype(orderbook_ins))
                self.xml_ops.add_sub_element(tnp_orderbook_element, 'Currency', orderbook_ins.Currency().Name())
                self.xml_ops.add_sub_element(tnp_orderbook_element, 'MarketInstrumentId', instrument_identifier)
                self.xml_ops.add_sub_element(tnp_orderbook_element, 'ISINCode', orderbook_ins.Isin())
                self.xml_ops.add_sub_element(tnp_orderbook_element, 'DefaultMarketplaceCodeSpecifier', str(def_market_code_specifier))
                self.xml_ops.add_sub_element(tnp_orderbook_element, 'TickSizeListId', tick_size_list_id)
                self.xml_ops.add_sub_element(tnp_orderbook_element, 'MarketplaceCode', market_place_code.get(self.xml_type, ''))                
                self.xml_ops.add_sub_element(tnp_orderbook_element, 'RoundLotSize', str(each_orderbook.RoundLot()))
                self.xml_ops.add_sub_element(tnp_orderbook_element, 'QuoteFactor', str(each_orderbook.QuoteFactor()))                
                self.xml_ops.add_sub_element(tnp_orderbook_element, 'DayCountMethod', each_orderbook.DayCounting())
                self.xml_ops.add_sub_element(tnp_orderbook_element, 'MaxDecimalsInPrice', self.max_decimals)
                
            else:
                logger.ELOG("No ISIN and ExternalID1 found for Instrument <%s>. Cannot export orderbook to XML"%orderbook_ins.Name())
        
        config_pretty_element_tree = self.xml_ops.pretty_print_element_tree(orderbook_element)   
        return config_pretty_element_tree        
        

class Tradeweb(OrderBookToXml):
    """This class handles operations to export BBG-Controbutions related data to XML."""
    
    def __init__(self, xml_type, market_place, market_segment, file_path, bbg_feed_type, bbg_tiering_system, max_decimals):
        
        self.xml_type = xml_type
        self.max_decimals = max_decimals
        self.db_ops = DBOperations()
        self.xml_ops = XMLOperations()
        self.bbg_feed_type = bbg_feed_type
        self.bbg_tiering_system = bbg_tiering_system
        OrderBookToXml.__init__(self, market_place, market_segment, file_path)
        
    def generate_xml(self, orderbooks_in_db, market_place, market_segment):
        """Generated xml for orderbook with all required tags and values"""
        config_pretty_element_tree = None
        
        # Add <orderbooks> xml element
        orderbook_element = self.xml_ops.add_element('orderbooks')
        
        for each_orderbook in orderbooks_in_db:
            orderbook_ins = each_orderbook.Instrument()
            
            instrument_identifier = self.db_ops.get_orderbook_market_instrument_id(orderbook_ins)
            if instrument_identifier:
                logger.DLOG("Exporting OrderBook <%s>, Instrument <%s>, Market <%s>, MarketSegment <%s>"% \
                                            (each_orderbook.Name(), orderbook_ins.Name(), market_place, market_segment))
                # Add <tnporderbook> tag
                tnp_orderbook_element = self.xml_ops.add_sub_element(orderbook_element, 'tnporderbook')
                
                # Add sub elements to <tnporderbook>
                self.xml_ops.add_sub_element(tnp_orderbook_element, 'Name', each_orderbook.Name())
                self.xml_ops.add_sub_element(tnp_orderbook_element, 'RICCode', self.db_ops.get_instrument_ric(orderbook_ins))
                self.xml_ops.add_sub_element(tnp_orderbook_element, 'PrimaryMarketMIC', Default_PrimaryMarketMIC)
                self.xml_ops.add_sub_element(tnp_orderbook_element, 'OrderBookId', each_orderbook.ExternalId())
                self.xml_ops.add_sub_element(tnp_orderbook_element, 'InstrumentType', self.db_ops.orderbook_instype(orderbook_ins))
                self.xml_ops.add_sub_element(tnp_orderbook_element, 'Currency', orderbook_ins.Currency().Name())
                self.xml_ops.add_sub_element(tnp_orderbook_element, 'MarketInstrumentId', instrument_identifier)
                self.xml_ops.add_sub_element(tnp_orderbook_element, 'ISINCode', orderbook_ins.Isin())
                self.xml_ops.add_sub_element(tnp_orderbook_element, 'DefaultMarketplaceCodeSpecifier', str(def_market_code_specifier))
                self.xml_ops.add_sub_element(tnp_orderbook_element, 'TickSizeListId', tick_size_list_id)
                self.xml_ops.add_sub_element(tnp_orderbook_element, 'MarketplaceCode', market_place_code.get(self.xml_type, '')) 
                self.xml_ops.add_sub_element(tnp_orderbook_element, 'RoundLotSize', str(each_orderbook.RoundLot()))
                self.xml_ops.add_sub_element(tnp_orderbook_element, 'QuoteFactor', str(each_orderbook.QuoteFactor()))                
                self.xml_ops.add_sub_element(tnp_orderbook_element, 'DayCountMethod', each_orderbook.DayCounting())
                self.xml_ops.add_sub_element(tnp_orderbook_element, 'MaxDecimalsInPrice', self.max_decimals)
                self.xml_ops.add_sub_element(tnp_orderbook_element, 'BBGMDFeedType', self.bbg_feed_type)
                self.xml_ops.add_sub_element(tnp_orderbook_element, 'BBGMDStreamID', each_orderbook.ExternalType())
                self.xml_ops.add_sub_element(tnp_orderbook_element, 'BBGOldTieringSystem', self.bbg_tiering_system)
            else:
                logger.ELOG("No ISIN and ExternalID1 found for Instrument <%s>. Cannot export orderbook to XML"%orderbook_ins.Name())
        
        config_pretty_element_tree = self.xml_ops.pretty_print_element_tree(orderbook_element)   
        return config_pretty_element_tree 
        
        
class BBGCommodities(OrderBookToXml):
    """This class handles operations to export BBG-Commodities related data to XML."""
    
    def __init__(self, xml_type, market_place, market_segment, market_instrument_id_type, file_path, max_decimals):
        
        self.market_instrument_id_type = market_instrument_id_type     
        self.xml_type = xml_type
        self.max_decimals = max_decimals
        self.db_ops = DBOperations()
        self.xml_ops = XMLOperations()
        OrderBookToXml.__init__(self, market_place, market_segment, file_path)
        
    def generate_xml(self, orderbooks_in_db, market_place, market_segment):
        """Generated xml for orderbook with all required tags and values"""
        config_pretty_element_tree = None
        
        # Add <orderbooks> xml element
        orderbook_element = self.xml_ops.add_element('orderbooks')
        
        for each_orderbook in orderbooks_in_db:
            orderbook_ins = each_orderbook.Instrument()
            
            instrument_identifier = self.db_ops.get_market_ins_id( orderbook_ins, self.market_instrument_id_type)
            if instrument_identifier:
                logger.DLOG("Exporting OrderBook <%s>, Instrument <%s>, Market <%s>, MarketSegment <%s>"% \
                                            (each_orderbook.Name(), orderbook_ins.Name(), market_place, market_segment))
                # Add <tnporderbook> tag
                tnp_orderbook_element = self.xml_ops.add_sub_element(orderbook_element, 'tnporderbook')
                
                # Add sub elements to <tnporderbook>
                self.xml_ops.add_sub_element(tnp_orderbook_element, 'Name', each_orderbook.Name())
                self.xml_ops.add_sub_element(tnp_orderbook_element, 'PrimaryMarketMIC', Default_PrimaryMarketMIC)
                self.xml_ops.add_sub_element(tnp_orderbook_element, 'OrderBookId', each_orderbook.ExternalId())
                self.xml_ops.add_sub_element(tnp_orderbook_element, 'InstrumentType', self.db_ops.orderbook_instype(orderbook_ins))
                self.xml_ops.add_sub_element(tnp_orderbook_element, 'Currency', orderbook_ins.Currency().Name())
                self.xml_ops.add_sub_element(tnp_orderbook_element, 'MarketInstrumentId', instrument_identifier)
                self.xml_ops.add_sub_element(tnp_orderbook_element, 'ISINCode', orderbook_ins.Isin())
                self.xml_ops.add_sub_element(tnp_orderbook_element, 'DefaultMarketplaceCodeSpecifier', str(def_market_code_specifier))
                self.xml_ops.add_sub_element(tnp_orderbook_element, 'TickSizeListId', tick_size_list_id)
                self.xml_ops.add_sub_element(tnp_orderbook_element, 'MarketplaceCode', market_place_code.get(self.xml_type, ''))
                self.xml_ops.add_sub_element(tnp_orderbook_element, 'RoundLotSize', str(each_orderbook.RoundLot()))
                self.xml_ops.add_sub_element(tnp_orderbook_element, 'QuoteFactor', str(each_orderbook.QuoteFactor()))                
                self.xml_ops.add_sub_element(tnp_orderbook_element, 'RICCode', self.db_ops.get_instrument_ric(orderbook_ins))
                self.xml_ops.add_sub_element(tnp_orderbook_element, 'BLOOMBERGCode', self.db_ops.get_market_ins_id( orderbook_ins, self.market_instrument_id_type))
                self.xml_ops.add_sub_element(tnp_orderbook_element, 'DayCountMethod', each_orderbook.DayCounting())
                self.xml_ops.add_sub_element(tnp_orderbook_element, 'MaxDecimalsInPrice', self.max_decimals)
                
            else:
                logger.ELOG("No ISIN and ExternalID1 found for Instrument <%s>. Cannot export orderbook to XML"%orderbook_ins.Name())
        
        config_pretty_element_tree = self.xml_ops.pretty_print_element_tree(orderbook_element)   
        return config_pretty_element_tree 
        
    def export_orderbooks_to_csv_file(self, orderbooks_in_db, market_place, market_segment, csv_file, orderbook_exported_count, csv_fields_dict, market_instrument_id_type, csv_row_headers):
        if csv_file:
            csv_fields_dict['Ticker Feed'] = ''
            w = csv.writer(csv_file)
            w.writerow(csv_row_headers)
            
            for each_orderbook in orderbooks_in_db:
                orderbook_ins = each_orderbook.Instrument()
                if orderbook_ins:
                    instrument_id = self.db_ops.get_market_ins_id(orderbook_ins, market_instrument_id_type)
                    if instrument_id :
                        csv_fields_dict['Ticker Feed'] = instrument_id
                        field_values = []
                        for each_field_header in csv_row_headers:
                            field_value = csv_fields_dict.get(each_field_header, '')
                            field_values.append(field_value)
                        w.writerow(field_values)
                        orderbook_exported_count = orderbook_exported_count + 1
                    else:
                        logger.ELOG("MarketInstrumentID not found for Instrument <%s>. Cannot export orderbook to csv file"%orderbook_ins.Name())
            
        else:
            logger.ELOG("File path <%s> does not exist. Cannot export orderbooks to xml"%self.file_path)
           
        return orderbook_exported_count
        
    def orderbook_to_csv_file(self, market_place, market_segment, market_instrument_id_type, bbg_comdty_depth, bbg_comdty_precision, \
                bbg_comdty_calendar, bbg_comdty_start, bbg_comdty_end):
                
       
        csv_fields_dict = {"Ticker Feed": market_instrument_id_type, "Depth": bbg_comdty_depth, "Precision":bbg_comdty_precision, "Calendar":bbg_comdty_calendar, \
                    "Contract start":bbg_comdty_start, "Contract end":bbg_comdty_end}
                    
        csv_row_headers = ["Ticker Feed", "Depth", "Precision", "Calendar", "Contract start", "Contract end"]
                    
        if market_place:
            if os.path.exists(self.file_path):
                if market_segment:
                    for each_seg in market_segment: 
                        logger.LOG("Processing orderbooks for csv file from Market %s MarketSegment %s"%(market_place, str(each_seg).strip()))
                        csv_file_name = 'RFQ_' + str(market_place).strip() + '-' + str(each_seg).strip() +'_orderbooks.csv'
                        logger.DLOG("CSV file name = %s"%csv_file_name)
                        orderbook_exported_csv_file_count = 0
                        orderbook_csv_file = os.path.join(self.file_path, csv_file_name) 
                        
                        orderbooks_in_db = self.db_ops.get_orderbooks_from_market(market_place, str(each_seg).strip())
                        if orderbooks_in_db:
                            logger.DLOG("Export orderbooks to csv file from Market <%s> MarketSegment <%s>"%(market_place, str(each_seg).strip()))
                            with open(orderbook_csv_file, 'w') as csv_file:
                                orderbook_exported_csv_file_count = self.export_orderbooks_to_csv_file(orderbooks_in_db, market_place, str(each_seg).strip(), \
                                                    csv_file, orderbook_exported_csv_file_count, csv_fields_dict, market_instrument_id_type, csv_row_headers)
                                if orderbook_exported_csv_file_count > 0:
                                    logger.LOG("Successfully exported oderbooks from MarketPlace <%s> MarketSegment <%s> to csv file %s "%(market_place, str(each_seg).strip(), orderbook_csv_file))
                        else:
                            logger.ELOG("No orderbooks found in MarketPlace <%s>, MarketSegment <%s>"%(market_place, str(each_seg).strip()))
                else:
                    logger.LOG("No MarketSegment specified by user, will export orderbooks from all segments")
                    #market_segments = market_place_in_db.MarketSegments()
                    market_segments = self.db_ops.get_market_segments(market_place)
                    logger.DLOG("MarketSements found in Market %s"%market_segments)
                    for each_seg in market_segments:
                        logger.DLOG("Processing for casts file from MarketSegment <%s>"%each_seg)
                        csv_file_name = 'RFQ_' + str(market_place).strip() + '-' + str(each_seg).strip() +'_orderbooks.csv'
                        logger.DLOG("CSV file name = %s"%csv_file_name)
                        
                        orderbook_exported_csv_file_count = 0
                        orderbook_csv_file = os.path.join(self.file_path, csv_file_name) 
                        orderbooks_in_db = self.db_ops.get_orderbooks_from_market(market_place, each_seg)
                        if orderbooks_in_db:
                            logger.DLOG("Export orderbooks to cats file from Market <%s> MarketSegment <%s>"%(market_place, each_seg))
                            with open(orderbook_csv_file, 'w') as csv_file:
                                orderbook_exported_csv_file_count = self.export_orderbooks_to_csv_file(orderbooks_in_db, market_place, each_seg, \
                                                                csv_file, orderbook_exported_csv_file_count, csv_fields_dict, market_instrument_id_type, csv_row_headers)
                                if orderbook_exported_csv_file_count > 0:
                                    logger.LOG("Successfully exported oderbooks from MarketPlace <%s> MarketSegment <%s> to csv file %s "% \
                                                    (market_place, str(each_seg).strip(), orderbook_csv_file))
                        else:
                            logger.ELOG("No orderbooks found in MarketPlace <%s>, MarketSegment <%s>"%(market_place, each_seg))

        

class DBOperations():
    
    def __init__(self):
        pass
        
    def list_markets(self):
        market_list = []
        # type = 5 --> MarketPlaces
        for party in acm.FParty.Select("type=5"):
            market_list.append(party.Name())
        if market_list:
            market_list.sort()
        return market_list
        
    def list_market_segments(self, market_place=None,market_segment=None):  
        #indexes: oid  superGroup name, primary keys: oid
        segment_list = []
        
        if not market_place and not market_segment:
            selection = acm.FMarketSegment.Select('')
        elif not market_place:
            selection = acm.FMarketSegment.Select("name='%s'" %(market_segment))
        elif not market_segment:
            selection = acm.FMarketSegment.Select("superGroup='%s'" %(market_place))
        else:
            selection = acm.FMarketSegment.Select("superGroup='%s' and name='%s'" %(market_place, market_segment))        

        for each_segment in selection:
            segment_list.append(each_segment.Name())

        return sorted(segment_list)
        
    def list_price_distributors(self):
        price_distributors_list = []
        for p_dist in acm.FPriceDistributor.Select(''):
            price_distributors_list.append(p_dist.Name())
        if price_distributors_list:
            price_distributors_list.sort()
        return price_distributors_list
        
    def list_add_infos(self):
        orderbook_addinfos = []
        for add_inf in acm.FAdditionalInfoSpec.Select('recType = Orderbook'):
            orderbook_addinfos.append(add_inf.Name())
        if orderbook_addinfos:
            orderbook_addinfos.sort()
        return orderbook_addinfos
        
    def get_market_segments(self, market_place):
        segment_list = []
        if market_place:
            for segment in  acm.FMarketSegment.Select("marketPlace='%s'" %(market_place)):
                segment_list.append(segment.Name())
        if segment_list:
            segment_list.sort()
        return segment_list
        
    def get_market_place(self, market_place):
        market = acm.FMarketPlace[market_place]
        if market:
            return market
            
    def get_orderbooks_from_market(self, market_place, market_segment):
        logger.DLOG("Get orderbook from Market %s, Market Segment %s"%(market_place, market_segment))
        orderbooks = None
        if market_place and market_segment:
            #market_seg = acm.FMarketPlace[market_place].MarketSegment(market_segment)
            market_seg = acm.FMarketSegment.Select01("name='%s' and marketPlace='%s'" %(market_segment, market_place), 'not found')
            if market_seg:
                orderbooks=market_seg.OrderBooks()
        else:
            orderbooks=acm.FMarketPlace[market_place].OrderBooks()
            
        return orderbooks
        
    def get_instrument_ric(self, instrument):
        ric_code = ''
        logger.DLOG("Get RIC from alias..")
        if instrument.Aliases():
            for alias in instrument.Aliases():
                if alias.Type().Name() == 'RIC':
                    ric_code = alias.Alias()
                    break
        return ric_code

    def get_instrument_BB_UNIQUE(self, instrument):
        alias_code = ''
        logger.DLOG("Get BB_UNIQUE from alias..")
        if instrument.Aliases():
            for alias in instrument.Aliases():
                if alias.Type().Name() == 'BB_UNIQUE':
                    alias_code = alias.Alias()
                    break
        return alias_code

    def get_instrument_BB_TICKER(self, instrument):
        alias_code = ''
        logger.DLOG("Get BB_TICKER from alias..")
        if instrument.Aliases():
            for alias in instrument.Aliases():
                if alias.Type().Name() == 'BB_TICKER':
                    alias_code = alias.Alias()
                    break
        return alias_code

    def get_instrument_BB_GLOBAL(self, instrument):
        alias_code = ''
        logger.DLOG("Get BB_GLOBAL from alias..")
        if instrument.Aliases():
            for alias in instrument.Aliases():
                if alias.Type().Name() == 'BB_GLOBAL':
                    alias_code = alias.Alias()
                    break
        return alias_code   
        
    def get_instrument_wkn(self, instrument):
        wkn = ''
        if instrument.Aliases():
            for alias in instrument.Aliases():
                if alias.Type().Name() == 'WKN':
                    wkn = alias.Alias()
                    logger.DLOG("Found instrument alias WKN <%s>"%str(wkn))
                    break
        if not wkn:
            if instrument.ExternalId1():
                wkn = str(instrument.ExternalId1())
        return wkn
        
    def get_addinfo(self, acm_obj, rec_type, fieldname):
        addinfo_val = None
        if rec_type and fieldname:
            if fieldname in self.list_add_infos():
                logger.DLOG("Fetching value for AddInfoSpec <%s> for OrderBook <%s>"%(fieldname, acm_obj.Name()))
                addinfo_spec = acm.FAdditionalInfoSpec[fieldname]
                if addinfo_spec and addinfo_spec.RecType() == rec_type:
                    addinfo_val = acm_obj.AddInfoValue(fieldname)
            else:
                addinfo_val = fieldname
                
        return addinfo_val
        
    def get_orderbook_market_instrument_id(self, instrument):
        market_ins_id = ''
        if instrument.Isin():
            market_ins_id = instrument.Isin()
        elif instrument.ExternalId1():
            market_ins_id = instrument.ExternalId1()
        
        return market_ins_id
        
    def orderbook_instype(self, instrument):
        instrument_type = None
        instrument_instype_dict = {1: ['Stock', 'Bond', 'Convertible', 'Combination', 'EquityIndex', 'FRN', 'CLN'],
                                    2: ['Convertible'],
                                    3: ['Bond', 'FRN', 'CLN'],
                                    5: ['Option', 'Warrant', 'Future/Forward'],
                                    }
        ins_instype = instrument.InsType()
        for instype_code in instrument_instype_dict:
            if ins_instype in instrument_instype_dict[instype_code]:
                instrument_type = instype_code
                break
        if not instrument_type:
            logger.DLOG("Using default TNP instrument type")
            instrument_type = TNP_unknown_instrument_type
                
        return instrument_type
        
    def ins_strike_price(self, instrument):
        strikePrice = ""
        if instrument.InsType() in ['Option', 'Warrant']:
            strikePrice = str(instrument.StrikePrice())
                
        elif instrument.InsType() in ['Future/Forward']:
            strikePrice = str(instrument.StoredStrike())
        return strikePrice
               
    def ins_put_or_call(self, instrument):
        put_or_call = ""
        if (instrument.InsType() in ['Option', 'Warrant', 'Future/Forward']):
            if instrument.IsCall() == 1:
                put_or_call = 'C'
            else:
                put_or_call = 'P'
        return put_or_call
        
    def ins_underlying(self, instrument):
        ins_underlying = ''
        if (instrument.InsType() in ['Option', 'Warrant', 'Future/Forward']):
            ins_underlying = str(instrument.Underlying().Name())
        return ins_underlying
        
    def underlying_ins_isin(self, instrument):
        ins_underlying_isin = ''
        if (instrument.InsType() in ['Option', 'Warrant', 'Future/Forward']):
            if instrument.Underlying().Isin():
                ins_underlying_isin = str(instrument.Underlying().Isin())
        return ins_underlying_isin
        
    def ins_pay_type(self, instrument):
        pay_type = ''
        if instrument.InsType() in ['Option', 'Warrant', 'Future/Forward']:
            if instrument.PayType():
                if instrument.PayType() == 'Forward':
                    pay_type = 'R'
                else:
                    pay_type = instrument.PayType()[0]
        return pay_type
        
    def put_call_indicator(self, instrument):
        put_call_indicator = ''
        if instrument.Putable():
            put_call_indicator = 0
        else:
            put_call_indicator = 1
        return put_call_indicator
        
    def orderbook_lot_size(self, orderbook):
        lot_size = str(orderbook.RoundLot())
        return lot_size
        
    def ins_issue_date(self, instrument):
        issue_date = default_issue_date
        if instrument.IssueDay():
            ins_issue_date = str(instrument.IssueDay()).replace('-', '')
            if not ael.date_from_string(ins_issue_date) > ael.date_from_string(max_date):
                issue_date = ins_issue_date
            
        return issue_date
    
    def ins_first_tarding_day(self, instrument):
        first_tarding_day = default_first_trading_date
        if instrument.StartDate():
            ins_first_tarding_day = str(instrument.StartDate()).replace('-', '')
            if not ael.date_from_string(ins_first_tarding_day) > ael.date_from_string(max_date):
                first_tarding_day = ins_first_tarding_day
                
        return first_tarding_day
        
    def ins_redemption_date(self, instrument):
        max_expiry = ael.date_from_string(max_date)
        redemption_date = ''
        
        if (instrument.InsType() in ['Stock', 'EquityIndex', 'Bond', 'Convertible', 'Combination', 'FRN', 'CLN']):
            if instrument.maturity_date():
                redemption_date = str(instrument.maturity_date()).replace('-', '')
        elif (instrument.InsType() in ['Option', 'Warrant', 'Future/Forward']):
            if instrument.ExpiryDateOnly():
                redemption_date = str(instrument.ExpiryDateOnly()).replace('-', '')
               
        if redemption_date:
            ins_expiry_dt = ael.date_from_string(redemption_date)
            if ins_expiry_dt >= max_expiry:
                logger.DLOG("Redemption date is greater than max <%s> for instrument %s"%(str(max_expiry), instrument.Name()))
                return max_date
            else:
                return redemption_date
        else:
            logger.DLOG("No redemption date found for instrument %s"%instrument.Name())
            return default_expiry_date
        
    def ins_expiry(self, instrument):
        max_expiry = ael.date_from_string(max_date)
        ins_expiry = ''
        
        if instrument.InsType() in ['Stock', 'EquityIndex', 'Bond', 'Convertible', 'Combination', 'FRN', 'CLN']:
            if instrument.maturity_date():
                ins_expiry = str(instrument.maturity_date()).replace('-', '')
        elif instrument.InsType() in ['Option', 'Warrant', 'Future/Forward']:
            if instrument.ExpiryDateOnly():
                ins_expiry = str(instrument.ExpiryDateOnly()).replace('-', '')
            
        if ins_expiry:
            ins_expiry_dt = ael.date_from_string(ins_expiry)
            if ins_expiry_dt >= max_expiry:
                logger.DLOG("Expiry date is greater than max <%s> for instrument %s"%(str(max_expiry), instrument.Name()))
                return max_date
            else:
                return ins_expiry
        else:
            logger.DLOG("No expiry date found for instrument %s"%instrument.Name())
            
            return default_expiry_date
            
    def get_InstrAliasFromType(self, insName, market_ins_id_type):
        ticker_alias_type = acm.FInstrAliasType[market_ins_id_type]
        if ticker_alias_type:
            alias = acm.FInstrumentAlias.Select01("instrument='%s' and type='%s'"%(insName, market_ins_id_type), 'alias not found')
            if alias:
                return alias.Alias()
            else:
                logger.WLOG("Instrument <%s> does not have alias %s"%(insName, market_ins_id_type))
                return None
        else:
            logger.WLOG("InstrAliasType %s not found in database"%(market_ins_id_type))
            return None

    def get_market_ins_id(self, ins, market_ins_id_type):
        market_instrument_id = ''
        logger.DLOG('Get Market InstrumentID from "%s"'+market_ins_id_type)
        
        if str(market_ins_id_type).upper() == "BB_TICKER":
            market_instrument_id = self.get_InstrAliasFromType(ins.Name(), "BB_TICKER")

        elif str(market_ins_id_type).upper() == "RIC":
            market_instrument_id = self.get_InstrAliasFromType(ins.Name(), "RIC")
         
        elif str(market_ins_id_type).upper() == "BB_GLOBAL":
            market_instrument_id = self.get_InstrAliasFromType(ins.Name(), "BB_GLOBAL")  

        elif str(market_ins_id_type).upper() == "BB_UNIQUE":
            market_instrument_id = self.get_InstrAliasFromType(ins.Name(), "BB_UNIQUE") 
                
        elif str(market_ins_id_type).upper() == "EXTERNAL ID1":
            if ins.ExternalId1():
                market_instrument_id = ins.ExternalId1()
            else:
                logger.WLOG("Instrument <%s> does not have ExternalID1"%ins.Name())
                
        elif str(market_ins_id_type).upper() == "EXTERNAL ID2":
            if ins.ExternalId2():
                market_instrument_id = ins.ExternalId2()
            else:
                logger.WLOG("Instrument <%s> does not have ExternalID2"%ins.Name())
                
                
        if str(market_ins_id_type).upper() == "ISIN" or market_instrument_id == '': # if ISIN or none of the above suceeded, take ISIN
            if ins.Isin():
                market_instrument_id = ins.Isin()
            else:
                logger.WLOG("Instrument <%s> does not have ISIN"%ins.Name())
                
        return market_instrument_id
        

class OrderBookXmlVariables(FRunScriptGUI.AelVariablesHandler):
    """This class defines the ael_variables to create a GUI for user input"""
    
    # Tooltips for GUI fields
    tt_xml_type = """The XML type for exporting order books."""
    tt_market_place = """The market place from which the order books should be exported."""
    tt_market_segment = """The market segment from which the order books should be exported."""
    tt_file_path = """The file path where the XML files are placed."""
    tt_decimals = """The maximum number of decimals in the price."""
    
    tt_marketInstrumentId_fixtoolkit2_native = """The instrument attributes used for generating the market instrument ID. Default is ISIN."""
    
    tt_market_instrument_id_type_bbg_contributions = """The instrument attributes used for generating the market instrument ID. Default is BB_TICKER."""
    tt_feed_type = """Select Bloomberg broker code for orderbooks to use in the XML tag <BBGMDFeedType>"""
    tt_oldtiering_system = """Select Bloomberg old tiering system number for the orderbooks to use in the XML tag <BBGOldTieringSystem>"""
    tt_load_indicator = """Select Bloomberg load indicator for orderbooks to use in the XML tag <BBGloadIndicator>"""
    tt_identifier_type = """Select Bloomberg identifier type for orderbooks to use in the XML tag <BBGidentifierType>"""
    tt_page_id = """OrderBook AddInfo 'BBGpageID' to use in the XML tag <BBGpageId>"""
    tt_page_sub_id = """OrderBook AddInfo 'BBGpageSubID' to use in the XML tag BBGpageSubID"""
    tt_page_number = """OrderBook AddInfo 'BBGpageNumber' to use in the XML tag BBGpageNumber"""
    tt_page_row_num = """OrderBook AddInfo 'BBGRowNum' to use in the XML tag BBGRowNum"""
    tt_log_level = """The verbosity level of log messages."""
    tt_log_to_file = """Select this check box to write the log output to a file."""
    tt_log_to_file_path = """The path to the output file. Only available when the Log to File check box is selected."""
    tt_generate_ric = """Select this check box to generate the RIC from the instrument ISIN if the RIC does not exist in the database."""
    tt_generate_wkn = """Select this check box to generate the WKN from the instrument ISIN if the WKN does not exist in the database."""
    tt_cats_file = """Select this check box to create a Cats orderbook.bat file with | as delimiter."""
    tt_market_maker = """The market maker ID for the Cats file. Only available if Create Cats file is selected."""
    tt_contribution_type = """Contribute to Page Data or Market Data"""
    tt_tradeweb_feed_type = """The Bloomberg broker code for the order books. Used in XML tag <BBGMDFeedType>."""
    tt_tradeweb_oldtiering_system = """The Bloomberg old tiering system number for the order books. Used in XML tag <BBGOldTieringSystem>."""
    tt_bbg_csv_file = """Select this check box to create a .csv file for BBG commodities."""
    tt_comdty_mkt = """The instrument attributes used for generating the market instrument ID. Default is BB_TICKER."""
    tt_comdty_mkt_ins_id = """Select instrument attributes to be used for generating MarketInstrumentID.
Bloomberg TICKER : InstrumentAlias BB_TICKER is used as MarketInstrumentID
EXTERNALID1 : Instrument ExternalID1 is used as MarketInstrumentID
EXTERNALID2 : Instrument ExternalID2 is used as MarketInstrumentID
ISIN : Instrument ISIN is used as MarketInstrumentID
                            """
    tt_comdty_depth = """Numeric field for depth"""
    tt_comdty_precision = """Numeric field for precision"""
    tt_comdty_calendar = """Alphanumeric field for calendar"""
    tt_comdty_start = """Numeric field for Contract start"""
    tt_comdty_end = """Numeric field for Contract end"""
    
    def enable_disable_xml_type_fields(self, index, fieldValues):
    
        if fieldValues[index] == CONTRIBUTION_BBG_FIX :  
            # Enable fields for tab Bloomberg-Contribution FIX
            self.ael_variables.bbg_feed_type.enable(True)
            self.ael_variables.bbg_tiering_system.enable(True)
            self.ael_variables.bbg_load_indicator.enable(True)
            self.ael_variables.bbg_identifier_type.enable(True)
            self.ael_variables.bbg_page_id.enable(True)
            self.ael_variables.bbg_page_sub_id.enable(True)
            self.ael_variables.bbg_page_number.enable(True)
            self.ael_variables.bbg_row_num.enable(True)            
            self.ael_variables.market_instrument_id_type_bbg_contributions.enable(True)
            self.ael_variables.market_instrument_id_type_bbg_contributions.set(fieldValues, market_instrument_id_type_list[1])
            
            # Disable fields from tab Bloomberg-Contribution BLP
            self.ael_variables.bbg_contribution_type.enable(False) 
   
            # Disable fields from tab Reuters-Controbution
            self.ael_variables.generate_ric_from_isin.enable(False)
            
            # Disable fields from tab Cats
            self.ael_variables.generate_wkn_from_isin.enable(False)
            self.ael_variables.create_cats_file.enable(False)
            self.ael_variables.market_maker.enable(False)   
         
            # Disable fields from tab TradeWeb
            self.ael_variables.tradeweb_bbg_feed_type.enable(False)
            self.ael_variables.tradeweb_bbg_tiering_system.enable(False)
            
            # Disable fields from tab BBG-Commodities            
            self.ael_variables.market_instrument_id_type_bbg_commodities.enable(False)
            self.ael_variables.create_bbg_csv_file.enable(False)
            self.ael_variables.bbg_commodities_depth.enable(False)
            self.ael_variables.bbg_commodities_precision.enable(False)
            self.ael_variables.bbg_commodities_calendar.enable(False)
            self.ael_variables.bbg_commodities_start.enable(False)
            self.ael_variables.bbg_commodities_end.enable(False)
            
            #FIXTOOLKIT
            self.ael_variables.market_instrument_id_type_fixtoolkit2_native.enable(False)
            
        elif fieldValues[index] == CONTRIBUTION_BBG_BLP : 
            # Enable fields from tab Bloomberg-Contribution BLP
            self.ael_variables.bbg_load_indicator.enable(True)
            self.ael_variables.bbg_identifier_type.enable(True)
            self.ael_variables.bbg_page_id.enable(True)
            self.ael_variables.bbg_page_sub_id.enable(True)
            self.ael_variables.bbg_page_number.enable(True)
            self.ael_variables.bbg_row_num.enable(True)  
            self.ael_variables.bbg_contribution_type.enable(True) 
            self.ael_variables.market_instrument_id_type_bbg_contributions.set(fieldValues, market_instrument_id_type_list[1])
            self.ael_variables.market_instrument_id_type_bbg_contributions.enable(True)      
            
            # Disable fields from tab Bloomberg-Contribution FIX
            self.ael_variables.bbg_feed_type.enable(False)
            self.ael_variables.bbg_tiering_system.enable(False)            
            # Disable fields from tab Reuters-Controbition
            self.ael_variables.generate_ric_from_isin.enable(False)
            
            # Disable fields from tab Cats
            self.ael_variables.generate_wkn_from_isin.enable(False)
            self.ael_variables.create_cats_file.enable(False)
            self.ael_variables.market_maker.enable(False)   
         
            # Disable fields from tab TradeWeb
            self.ael_variables.tradeweb_bbg_feed_type.enable(False)
            self.ael_variables.tradeweb_bbg_tiering_system.enable(False)
            
            # Disable fields from tab BBG-Commodities
            self.ael_variables.create_bbg_csv_file.enable(False)
            self.ael_variables.bbg_commodities_depth.enable(False)
            self.ael_variables.bbg_commodities_precision.enable(False)
            self.ael_variables.bbg_commodities_calendar.enable(False)
            self.ael_variables.bbg_commodities_start.enable(False)
            self.ael_variables.bbg_commodities_end.enable(False)
            self.ael_variables.market_instrument_id_type_bbg_commodities.enable(False)
            
            #FIXTOOLKIT
            self.ael_variables.market_instrument_id_type_fixtoolkit2_native.enable(False)
            
        elif fieldValues[index] == REUTERS_CONTRIBUTION :
            # Enable fields
            self.ael_variables.generate_ric_from_isin.enable(True)
            

            # Disable fields from tab BBG-Contributions
            self.ael_variables.bbg_feed_type.enable(False)
            self.ael_variables.bbg_tiering_system.enable(False)
            self.ael_variables.bbg_load_indicator.enable(False)
            self.ael_variables.bbg_identifier_type.enable(False)
            self.ael_variables.bbg_page_id.enable(False)
            self.ael_variables.bbg_page_sub_id.enable(False)
            self.ael_variables.bbg_page_number.enable(False)
            self.ael_variables.bbg_row_num.enable(False)
            self.ael_variables.market_instrument_id_type_bbg_contributions.enable(False)   
            
            # Disable fields from tab Cats
            self.ael_variables.generate_wkn_from_isin.enable(False)
            self.ael_variables.create_cats_file.enable(False)
            self.ael_variables.market_maker.enable(False)
            
            # Disable fields from tab TradeWeb
            self.ael_variables.tradeweb_bbg_feed_type.enable(False)
            self.ael_variables.tradeweb_bbg_tiering_system.enable(False)
            
            # Disable fields from tab BBG-Commodities
            self.ael_variables.create_bbg_csv_file.enable(False)
            self.ael_variables.bbg_commodities_depth.enable(False)
            self.ael_variables.bbg_commodities_precision.enable(False)
            self.ael_variables.bbg_commodities_calendar.enable(False)
            self.ael_variables.bbg_commodities_start.enable(False)
            self.ael_variables.bbg_commodities_end.enable(False)
            self.ael_variables.market_instrument_id_type_bbg_commodities.enable(False)
            
            # Disable fields from tab Bloomberg-Contribution BLP
            self.ael_variables.bbg_contribution_type.enable(False) 
            
            #FIXTOOLKIT
            self.ael_variables.market_instrument_id_type_fixtoolkit2_native.enable(False)
            
            
        elif fieldValues[index] == CATS :
            # enabled fields
            self.ael_variables.generate_wkn_from_isin.enable(True)
            self.ael_variables.create_cats_file.enable(True)
            self.ael_variables.market_maker.enable(False)
            
            # Disable fields from tab BBG-Controbutions            
            self.ael_variables.bbg_feed_type.enable(False)
            self.ael_variables.bbg_tiering_system.enable(False)
            self.ael_variables.bbg_load_indicator.enable(False)
            self.ael_variables.bbg_identifier_type.enable(False)
            self.ael_variables.bbg_page_id.enable(False)
            self.ael_variables.bbg_page_sub_id.enable(False)
            self.ael_variables.bbg_page_number.enable(False)
            self.ael_variables.bbg_row_num.enable(False)
            self.ael_variables.market_instrument_id_type_bbg_contributions.enable(False)   
            
            # Disable fields from Reuters-Contributions
            self.ael_variables.generate_ric_from_isin.enable(False)
            
            # Disable fields from tab TradeWeb
            self.ael_variables.tradeweb_bbg_feed_type.enable(False)
            self.ael_variables.tradeweb_bbg_tiering_system.enable(False)
            
            # Disable fields from tab BBG-Commodities            
            self.ael_variables.create_bbg_csv_file.enable(False)
            self.ael_variables.bbg_commodities_depth.enable(False)
            self.ael_variables.bbg_commodities_precision.enable(False)
            self.ael_variables.bbg_commodities_calendar.enable(False)
            self.ael_variables.bbg_commodities_start.enable(False)
            self.ael_variables.bbg_commodities_end.enable(False)        
            self.ael_variables.market_instrument_id_type_bbg_commodities.enable(False)
            self.ael_variables.market_instrument_id_type_bbg_commodities.set(fieldValues, '')
            
            # Disable fields from tab Bloomberg-Contribution BLP
            self.ael_variables.bbg_contribution_type.enable(False)

            #FIXTOOLKIT
            self.ael_variables.market_instrument_id_type_fixtoolkit2_native.enable(False)
            
        elif fieldValues[index] in [MARKETAXESS, TRADEWEB]:
            if fieldValues[index] == TRADEWEB:
                # Enable fields
                self.ael_variables.tradeweb_bbg_feed_type.enable(True)
                self.ael_variables.tradeweb_bbg_tiering_system.enable(True)
            else:
                self.ael_variables.tradeweb_bbg_feed_type.enable(False)
                self.ael_variables.tradeweb_bbg_tiering_system.enable(False)
               
        
            # Disable fields from tab BBG-Controbutions            
            self.ael_variables.bbg_feed_type.enable(False)
            self.ael_variables.bbg_tiering_system.enable(False)
            self.ael_variables.bbg_load_indicator.enable(False)
            self.ael_variables.bbg_identifier_type.enable(False)
            self.ael_variables.bbg_page_id.enable(False)
            self.ael_variables.bbg_page_sub_id.enable(False)
            self.ael_variables.bbg_page_number.enable(False)
            self.ael_variables.bbg_row_num.enable(False)
            self.ael_variables.market_instrument_id_type_bbg_contributions.enable(False) 
            
            # Disable fields from Reuters-Contributions
            self.ael_variables.generate_ric_from_isin.enable(False)
            
            # Disable fields from tab Cats
            self.ael_variables.generate_wkn_from_isin.enable(False)
            self.ael_variables.create_cats_file.enable(False)
            self.ael_variables.market_maker.enable(False)
            
            # Disable fields from tab BBG-Commodities
            self.ael_variables.create_bbg_csv_file.enable(False)
            self.ael_variables.bbg_commodities_depth.enable(False)
            self.ael_variables.bbg_commodities_precision.enable(False)
            self.ael_variables.bbg_commodities_calendar.enable(False)
            self.ael_variables.bbg_commodities_start.enable(False)
            self.ael_variables.bbg_commodities_end.enable(False)
            self.ael_variables.market_instrument_id_type_bbg_commodities.enable(False)
            self.ael_variables.market_instrument_id_type_bbg_commodities.set(fieldValues, '')
            
            # Disable fields from tab Bloomberg-Contribution BLP
            self.ael_variables.bbg_contribution_type.enable(False)

            #FIXTOOLKIT
            self.ael_variables.market_instrument_id_type_fixtoolkit2_native.enable(False)
            
        elif fieldValues[index] == FIXTOOLKIT2_NATIVE :
            # enable fields from tab FIXTOOLKIT2_NATIVE
            self.ael_variables.market_instrument_id_type_fixtoolkit2_native.enable(True)
            self.ael_variables.market_instrument_id_type_fixtoolkit2_native.set(fieldValues, market_instrument_id_type_list[0])
            
            # Disable fields from tab Cats
            self.ael_variables.generate_wkn_from_isin.enable(False)
            self.ael_variables.create_cats_file.enable(False)
            self.ael_variables.market_maker.enable(False)
            
            # Disable fields from tab BBG-Contributions
            self.ael_variables.bbg_feed_type.enable(False)
            self.ael_variables.bbg_tiering_system.enable(False)
            self.ael_variables.bbg_load_indicator.enable(False)
            self.ael_variables.bbg_identifier_type.enable(False)
            self.ael_variables.bbg_page_id.enable(False)
            self.ael_variables.bbg_page_sub_id.enable(False)
            self.ael_variables.bbg_page_number.enable(False)
            self.ael_variables.bbg_row_num.enable(False)
            self.ael_variables.market_instrument_id_type_bbg_contributions.enable(False)   
            
            # Disable fields from Reuters-Contributions
            self.ael_variables.generate_ric_from_isin.enable(False)
            
            # Disable fields from tab TradeWeb
            self.ael_variables.tradeweb_bbg_feed_type.enable(False)
            self.ael_variables.tradeweb_bbg_tiering_system.enable(False)

            # Disable fields from tab BBG-Commodities            
            self.ael_variables.create_bbg_csv_file.enable(False)
            self.ael_variables.bbg_commodities_depth.enable(False)
            self.ael_variables.bbg_commodities_precision.enable(False)
            self.ael_variables.bbg_commodities_calendar.enable(False)
            self.ael_variables.bbg_commodities_start.enable(False)
            self.ael_variables.bbg_commodities_end.enable(False)
            self.ael_variables.market_instrument_id_type_bbg_commodities.enable(False)
            self.ael_variables.market_instrument_id_type_bbg_commodities.set(fieldValues, '')
            
            # Disable fields from tab Bloomberg-Contribution BLP
            self.ael_variables.bbg_contribution_type.enable(False) 
            
            
        elif fieldValues[index]  == BBGCOMMODITIES :
            # Enable fields            
            self.ael_variables.create_bbg_csv_file.enable(True)
            self.ael_variables.bbg_commodities_depth.enable(False)
            self.ael_variables.bbg_commodities_precision.enable(False)
            self.ael_variables.bbg_commodities_calendar.enable(False)
            self.ael_variables.bbg_commodities_start.enable(False)
            self.ael_variables.bbg_commodities_end.enable(False)   
            self.ael_variables.market_instrument_id_type_bbg_commodities.enable(True)
            self.ael_variables.market_instrument_id_type_bbg_commodities.set(fieldValues, market_instrument_id_type_list[1])
            
            # Disable fields from tab Cats
            self.ael_variables.generate_wkn_from_isin.enable(False)
            self.ael_variables.create_cats_file.enable(False)
            self.ael_variables.market_maker.enable(False)
            
            # Disable fields from tab BBG-Contributions
            self.ael_variables.bbg_feed_type.enable(False)
            self.ael_variables.bbg_tiering_system.enable(False)
            self.ael_variables.bbg_load_indicator.enable(False)
            self.ael_variables.bbg_identifier_type.enable(False)
            self.ael_variables.bbg_page_id.enable(False)
            self.ael_variables.bbg_page_sub_id.enable(False)
            self.ael_variables.bbg_page_number.enable(False)
            self.ael_variables.bbg_row_num.enable(False)
            self.ael_variables.market_instrument_id_type_bbg_contributions.enable(False)    
            
            # Disable fields from Reuters-Contributions
            self.ael_variables.generate_ric_from_isin.enable(False)
            
            # Disable fields from tab TradeWeb
            self.ael_variables.tradeweb_bbg_feed_type.enable(False)
            self.ael_variables.tradeweb_bbg_tiering_system.enable(False)
            
            # Disable fields from tab Bloomberg-Contribution BLP
            self.ael_variables.bbg_contribution_type.enable(False) 

            #FIXTOOLKIT
            self.ael_variables.market_instrument_id_type_fixtoolkit2_native.enable(False)
            
        return fieldValues
        
    def enable_disable_log_file(self, index, fieldValues):
        enable = str(fieldValues[index]) not in ['false', 'False']
        self.ael_variables.log_to_file.enable(enable)
        
        return fieldValues
        
    def enable_disable_create_cats_file(self, index, fieldValues):
        enable = str(fieldValues[index]) not in ['false', 'False']
        self.ael_variables.market_maker.enable(enable)
        
        return fieldValues

    def enable_disable_create_bbg_csv_file(self, index, fieldValues):
        enable = str(fieldValues[index]) not in ['false', 'False']
        self.ael_variables.bbg_commodities_depth.enable(enable)
        self.ael_variables.bbg_commodities_precision.enable(enable)
        self.ael_variables.bbg_commodities_calendar.enable(enable)
        self.ael_variables.bbg_commodities_start.enable(enable)
        self.ael_variables.bbg_commodities_end.enable(enable)
        
        return fieldValues
        
    def set_market_segments(self, index, fieldValues):

        market_segments = self.db_ops.get_market_segments(fieldValues[index])
        self.ael_variables.segment[3] = market_segments
        self.ael_variables.segment.set(fieldValues, '')

        return fieldValues

    def __init__(self):
        self.db_ops = DBOperations()
        variables = [
                # General
                ['xml_type', 'XML Type', 'string', xmlType_list, xmlType_list[0], 2, 0, self.tt_xml_type, self.enable_disable_xml_type_fields],
                ['market_place', 'Market Place', 'string', self.db_ops.list_markets(), '', 2, 0, self.tt_market_place, self.set_market_segments],
                ['segment', 'Market Segment', 'string', '', '', 2, 0, self.tt_market_segment, '', 1],
                ['filePath', 'File Path', 'string', None, 'C:\\temp\\', 1, None, self.tt_file_path],
                ['max_decimals_in_price', 'Max # of Decimals in Price', 'string', max_decimals_in_price, 3, 2, 0, self.tt_decimals, None, 1 ],
                #FIXTOOLKIT2 Native
                ['market_instrument_id_type_fixtoolkit2_native', 'Market Instrument ID_'+FIXTOOLKIT2_NATIVE, 'string', 
                                                market_instrument_id_type_list, market_instrument_id_type_list[0], 2, 0, self.tt_marketInstrumentId_fixtoolkit2_native, None, 0],
                # CONTRIBUTION_BBG_FIX and RFQ
                ['market_instrument_id_type_bbg_contributions', 'Market Instrument ID_BBG Contributions', 'string', market_instrument_id_type_list,
                   market_instrument_id_type_list[0], 2, 0, self.tt_market_instrument_id_type_bbg_contributions, None, 0],
                ['bbg_feed_type', 'MD Feed Type (Bloomberg Broker Code)_BBG Contributions', 'string', None, def_feed_type, 1, 0, self.tt_feed_type, None, 1],
                ['bbg_tiering_system', 'Old Tiering System_BBG Contributions', 'string', bbg_old_tiering_system, 0, 1, 0, self.tt_oldtiering_system, None, 1],
                ['bbg_load_indicator', 'Load Indicator_BBG Contributions', 'string', bbg_blp_load_indicators, bbg_blp_load_indicators[0], 2, 0, self.tt_load_indicator],
                ['bbg_identifier_type', 'Identifier Type_BBG Contributions', 'string', bbg_identifier_types, bbg_identifier_types[0], 2, 0, self.tt_identifier_type],
                ['bbg_page_id', 'Page ID_BBG Contributions', 'string', self.db_ops.list_add_infos(), '', 2, 0, self.tt_page_id],
                ['bbg_page_sub_id', 'Page Sub ID_BBG Contributions', 'string', self.db_ops.list_add_infos(), '', 2, 0, self.tt_page_sub_id],
                ['bbg_page_number', 'Page Number_BBG Contributions', 'string', self.db_ops.list_add_infos(), '', 2, 0, self.tt_page_number],
                ['bbg_row_num', 'Row Num_BBG Contributions', 'string', self.db_ops.list_add_infos(), '', 2, 0, self.tt_page_row_num],
                ['bbg_contribution_type', 'Contribution Type (BLP)_BBG Contributions', 'string', ["Page Data", "Market Data"], "Page Data", 2, 0, self.tt_contribution_type],          
                # REUTERS_CONTRIBUTION
                ['generate_ric_from_isin', 'Generate RIC from ISIN_'+REUTERS_CONTRIBUTION, 'bool', [True, False], False, 0, 0, self.tt_generate_ric, None, 1],
                # Cats
                ['generate_wkn_from_isin', 'Generate WKN from ISIN_'+CATS, 'bool', [True, False], False, 0, 0, self.tt_generate_wkn, None, 1],
                ['create_cats_file', 'Create Cats File_'+CATS, 'bool', [True, False], False, 0, 0, self.tt_cats_file, self.enable_disable_create_cats_file, 1],
                ['market_maker', 'Market Maker (Issuer ID)_'+CATS, 'string', None, default_market_maker, 1, None, self.tt_market_maker, None, 0],
                #TradeWeb
                ['tradeweb_bbg_feed_type', 'MD Feed Type (Bloomberg Broker Code)_TradeWeb', 'string', None, def_feed_type, 1, 0, self.tt_tradeweb_feed_type, None, 1],
                ['tradeweb_bbg_tiering_system', 'Old Tiering System_TradeWeb', 'string', bbg_old_tiering_system, 0, 1, 0, self.tt_tradeweb_oldtiering_system, None, 1],
                #BBG-Commodities
                ['market_instrument_id_type_bbg_commodities', 'Market Instrument ID_'+BBGCOMMODITIES, 'string', market_instrument_id_type_list, \
                    market_instrument_id_type_list[0], 2, 0, self.tt_comdty_mkt, None, 0],
                ['create_bbg_csv_file', 'Create BBG .csv File_'+BBGCOMMODITIES, 'bool', [True, False], False, 0, 0, self.tt_bbg_csv_file, self.enable_disable_create_bbg_csv_file, 1],
                ['bbg_commodities_depth', 'Depth_'+BBGCOMMODITIES, 'string', None, '', 0, None, self.tt_comdty_depth, None, 0],
                ['bbg_commodities_precision', 'Precision_'+BBGCOMMODITIES, 'string', None, '', 0, None, self.tt_comdty_precision, None, 0],
                ['bbg_commodities_calendar', 'Calendar_'+BBGCOMMODITIES, 'string', None, '', 0, None, self.tt_comdty_calendar, None, 0],
                ['bbg_commodities_start', 'Contract Start_'+BBGCOMMODITIES, 'string', None, '', 0, None, self.tt_comdty_start, None, 0],
                ['bbg_commodities_end', 'Contract End_'+BBGCOMMODITIES, 'string', None, '', 0, None, self.tt_comdty_end, None, 0],
                #['bbg_commodity_market_maker', 'Market Maker (Issuer ID)_'+BBGCOMMODITIES, 'string', None,default_market_maker, 1, None, self.tt_market_maker,None, 0],
                # Logging
                ['log_level', 'Log Level_Logging', 'string', ['DEBUG', 'INFO', 'WARN', 'ERROR'], 'INFO', 2, 0, self.tt_log_level, None, 1],
                ['enable_log_to_file', 'Log to File_Logging', 'bool', [True, False], False, 0, 0, self.tt_log_to_file, self.enable_disable_log_file],
                ['log_to_file', 'Log to File_Logging', 'string', '', 'C:\\temp\\OrderbookToXmlReport.txt', 0, 0, self.tt_log_to_file_path, None, 1],
                ]
                
        FRunScriptGUI.AelVariablesHandler.__init__(self, variables)
 
ael_variables = OrderBookXmlVariables()


def ael_main(params):
    logger_levels = {'INFO':1, 'DEBUG':2, 'WARN':3, 'ERROR':4}
    xml_type = str(params['xml_type'])
    market_place = str(params['market_place'])
    market_segment = str(params['segment'])
    if market_segment:
        market_segment = market_segment.split(',')
    file_path = str(params['filePath'])
    max_decimals = int(params['max_decimals_in_price'])
    bbg_feed_type = str(params['bbg_feed_type'])
    bbg_tiering_system = str(params['bbg_tiering_system'])
    bbg_load_indicator = str(params['bbg_load_indicator'])
    bbg_identifier_type = str(params['bbg_identifier_type'])
    bbg_page_id = str(params['bbg_page_id'])
    bbg_page_sub_id = str(params['bbg_page_sub_id'])
    bbg_page_number = str(params['bbg_page_number'])
    bbg_row_num = str(params['bbg_row_num'])
    bbg_contribution_type = str(params['bbg_contribution_type'])
    
    generate_ric_from_isin = bool(params['generate_ric_from_isin'])
    
    generate_wkn_from_isin = bool(params['generate_wkn_from_isin'])
    
    generate_wkn_from_isin = params.get('generate_wkn_from_isin', None)
    if generate_wkn_from_isin:
        generate_wkn_from_isin = bool(generate_wkn_from_isin)
    
    market_maker_issuer = params.get('market_maker', None)
    if market_maker_issuer:
        market_maker_issuer = str(market_maker_issuer)
        
    create_cats_file = params.get('create_cats_file', None)
    if create_cats_file:
        create_cats_file = bool(create_cats_file)

    create_bbg_commodity_csv_file = params.get('create_bbg_csv_file', None)
    if create_bbg_commodity_csv_file:
        create_bbg_commodity_csv_file = bool(create_bbg_commodity_csv_file)
        
    # setting logger
    logging_level = str(params['log_level'])
    log_level = logger_levels.get(logging_level)
    enable_log_file = bool(params['enable_log_to_file'])
    log_to_file = str(params['log_to_file'])
    if not enable_log_file:
        log_to_file = None
   
    market_instrument_id_type_bbg_contributions= params.get('market_instrument_id_type_bbg_contributions', None)
    market_instrument_id_type_bbg_commodities= params.get('market_instrument_id_type_bbg_commodities', None)
    market_instrument_id_type_fixtoolkit2_native= params.get('market_instrument_id_type_fixtoolkit2_native', None)
    
    logger.Reinitialize(level = log_level, logToFileAtSpecifiedPath = log_to_file)        
    
    # [FIXTOOLKIT2_NATIVE,CONTRIBUTION_BBG_FIX,CONTRIBUTION_BBG_BLP,REUTERS_CONTRIBUTION,CATS]
    
    if xml_type == CONTRIBUTION_BBG_FIX:
        contribution_obj = BBGContributionFIX(xml_type, market_place, market_segment, market_instrument_id_type_bbg_contributions, file_path, bbg_feed_type, bbg_tiering_system, bbg_page_id, bbg_page_sub_id, \
                                                bbg_page_number, bbg_row_num, bbg_load_indicator, bbg_identifier_type, max_decimals)
        contribution_obj.orderbook_to_xml()

    elif xml_type == CONTRIBUTION_BBG_BLP:
        contribution_obj = BBGContributionBLP(xml_type, market_place, market_segment, market_instrument_id_type_bbg_contributions, file_path, bbg_contribution_type, bbg_page_id, bbg_page_sub_id, \
                                                bbg_page_number, bbg_row_num, bbg_load_indicator, bbg_identifier_type, max_decimals)
        contribution_obj.orderbook_to_xml()
   
    elif xml_type == REUTERS_CONTRIBUTION:
        contribution_obj = ReutersContributions(xml_type, market_place, market_segment, file_path, generate_ric_from_isin, max_decimals )
        
        contribution_obj.orderbook_to_xml()
        
    elif xml_type == CATS:
        contribution_obj = Cats(xml_type, market_place, market_segment, file_path, max_decimals,  generate_wkn_from_isin)
        contribution_obj.orderbook_to_xml()
        if create_cats_file:
            contribution_obj.orderbook_to_cats_file(market_place, market_segment, market_maker_issuer)
        
    elif xml_type == FIXTOOLKIT2_NATIVE:
        contribution_obj = FixToolkitNative(xml_type, market_place, market_segment, market_instrument_id_type_fixtoolkit2_native, file_path, max_decimals)
        
        contribution_obj.orderbook_to_xml() 

    elif xml_type == MARKETAXESS:
        controbutions_obj = MarketAxess(xml_type, market_place, market_segment, file_path, max_decimals)
        
        controbutions_obj.orderbook_to_xml()
        
    elif xml_type == TRADEWEB:
        tradeweb_bbg_feedtype = str(params.get('tradeweb_bbg_feed_type', ''))
        tradeweb_bbg_tiering_system = str(params.get('tradeweb_bbg_tiering_system', bbg_old_tiering_system[0]))
        
        controbutions_obj = Tradeweb(xml_type, market_place, market_segment, file_path, tradeweb_bbg_feedtype, tradeweb_bbg_tiering_system, max_decimals)
        
        controbutions_obj.orderbook_to_xml()
        
    if xml_type == BBGCOMMODITIES:        
        bbg_comdty_depth = params.get('bbg_commodities_depth', None)
        bbg_comdty_precision = params.get('bbg_commodities_precision', None)
        bbg_comdty_calendar = params.get('bbg_commodities_calendar', None)
        bbg_comdty_start = params.get('bbg_commodities_start', None)
        bbg_comdty_end = params.get('bbg_commodities_end', None)
        
        bbg_commodities_obj = BBGCommodities(xml_type, market_place, market_segment, market_instrument_id_type_bbg_commodities, file_path, max_decimals)
        
        bbg_commodities_obj.orderbook_to_xml()
        
        if create_bbg_commodity_csv_file:
            bbg_commodities_obj.orderbook_to_csv_file(market_place, market_segment, market_instrument_id_type_bbg_commodities, bbg_comdty_depth, bbg_comdty_precision, \
                bbg_comdty_calendar, bbg_comdty_start, bbg_comdty_end)

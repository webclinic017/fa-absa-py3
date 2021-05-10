"""----------------------------------------------------------------------------
MODULE:
    FSwiftWriterMTFactory

DESCRIPTION:
    OPEN EXTENSION MODULE
    This module creates the FMTnnn object. The object can be created using
    either swift data or an acm object. It is derived from the FSwiftWriterMTFactoryBase

VERSION: 3.0.0-0.5.3344
----------------------------------------------------------------------------"""
import FSwiftWriterMTFactoryBase
import FSwiftWriterLogger
notifier = FSwiftWriterLogger.FSwiftWriterLogger('SwiftWriter', 'FSwiftWriterNotifyConfig')

'''
# If user intend to develop MT123, he need to import the FMT123
try:
    import FMT123
except Exception, e:
    pass
'''

class FSwiftWriterMTFactory(FSwiftWriterMTFactoryBase.FSwiftWriterMTFactoryBase):
    """ FMTFactory class to create MT object as per message type"""
    @staticmethod
    def create_fmt_object(acm_object, msg_type, swift_metadata_xml_dom = None):
        if msg_type == 'MT123':
            '''
            # Create object of the FMT123
            return FMT123.FMT123(source, direction)
            '''
            pass
        else:
            return FSwiftWriterMTFactoryBase.FSwiftWriterMTFactoryBase.create_fmt_object(acm_object, msg_type, swift_metadata_xml_dom)

    @staticmethod
    def create_fmt_header_object(msg_type, acm_object, swift_msg_tags, swift_metadata_xml_dom = None):
        if msg_type == 'MT123':
            '''
            return FMT300Out.FMT300MessageHeader(acm_object, swift_msg_tags, swift_metadata_xml_dom)
            '''
            pass
        else:
            return FSwiftWriterMTFactoryBase.FSwiftWriterMTFactoryBase.create_fmt_header_object(msg_type, acm_object, swift_msg_tags, swift_metadata_xml_dom)

    @staticmethod
    def create_fmt_network_rules_object(msg_type, swift_message_obj, swift_message, acm_obj, swift_metadata_xml_dom = None):
        if msg_type == 'MT123':
            '''
            return FMT300Out.FMT300MessageHeader(acm_object, swift_msg_tags, swift_metadata_xml_dom)
            '''
            pass
        else:
            return FSwiftWriterMTFactoryBase.FSwiftWriterMTFactoryBase.create_fmt_network_rules_object(msg_type, swift_message_obj, swift_message, acm_obj, swift_metadata_xml_dom)



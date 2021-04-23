"""----------------------------------------------------------------------------
MODULE:
    FMT598_132OutBase

DESCRIPTION:
    This module provides the base class for the FMT598_132 outgoing implementation

CLASS:
    FMT598_132Base

VERSION: 2.1.0-0.5.2940

RESTRICTIONS/LIMITATIONS:
	1. Any modifications to the script/encrypted module/clear text code within the core is not supported.
	2. This module is not customizable.
	3. The component may not work as expected with any modifications done to this module at user end.
----------------------------------------------------------------------------"""
from FSecurityLendingBorrowingOutUtils import *
import FSwiftWriterMessageHeader
import MT598_132
import FMTOutBase
import acm
from FSwiftWriterEngine import validate_with, should_use_operations_xml
import EnvironmentFunctions
import FSwiftWriterLogger
import FSwiftWriterUtils

pkg_name = 'FSwiftSecurityLendingBorrowingOut'
notifier = FSwiftWriterLogger.FSwiftWriterLogger('SBL', pkg_name+ 'Notify_Config')


class FMT598_132Base(FMTOutBase.FMTOutBase):

    def __init__(self, acm_obj, swift_obj, swift_metadata_xml_dom=None):
        self.swift_message_type = "MT598_132"
        self.swift_obj = swift_obj
        self.acm_obj = acm_obj
        super(FMT598_132Base, self).__init__(self.acm_obj, swift_obj)

    def _message_sequences(self):
        pass

    # getter
    def transaction_reference_20(self):
        return get_transaction_reference_of_cancellation(self.acm_obj, self.swift_message_type)

    # formatter
    def _format_transaction_reference_20(self, val):
        return 'X'+str(val)

    # validator
    @validate_with(MT598_132.MT598_132_20_Type)
    def _validate_transaction_reference_20(self, val):
        return val

    # setter
    def _set_transaction_reference_20(self, val):
        self.swift_obj.TransactionReference = val
        self.swift_obj.TransactionReference.swiftTag = "20"

    # getter
    def sub_messagetype_12(self):
        return 132

    # formatter
    def _format_sub_messagetype_12(self, val):
        return val

    # validator
    @validate_with(MT598_132.MT598_132_12_Type)
    def _validate_sub_messagetype_12(self, val):
        return val

    # setter
    def _set_sub_messagetype_12(self, val):
        self.swift_obj.SubMessageType = val
        self.swift_obj.SubMessageType.swiftTag = "12"


    # getter
    def proprietary_message_77E(self):
        return ' '

    # formatter
    def _format_proprietary_message_77E(self, val):
        return val

    # validator
    @validate_with(MT598_132.MT598_132_77E_Type)
    def _validate_proprietary_message_77E(self, val):
        return val

    # setter
    def _set_proprietary_message_77E(self, val):
        #This is hacky way of keeping the tag empty, but this is how SwiftEngine works. This is because we dont want to populate anything here, although the syntax of tag allows us to populate things.    
        self.swift_obj.ProprietaryMessage = ''
        self.swift_obj.ProprietaryMessage.swiftTag = "77E"


    # getter
    def SAFIRESloan_reference_26H(self):
        return get_unique_SAFIRESloanReference(self.acm_obj, self.swift_message_type)

    # formatter
    def _format_SAFIRESloan_reference_26H(self, val):
        return val

    # validator
    @validate_with(MT598_132.MT598_132_26H_Type)
    def _validate_SAFIRESloan_reference_26H(self, val):
        return val

    # setter
    def _set_SAFIRESloan_reference_26H(self, val):
        self.swift_obj.SAFIRESLoanReference = val
        self.swift_obj.SAFIRESLoanReference.swiftTag = "26H"

class FMT598_132OutBaseMessageHeader(FSwiftWriterMessageHeader.FSwiftWriterMessageHeader):
    def __init__(self, acm_obj, swift_msg_tags, swift_metadata_xml_dom=None):
        self.mt_typ = "598_132"
        self.acm_obj = acm_obj
        self.swift_msg_tags = swift_msg_tags
        self.swift_metadata_xml_dom = swift_metadata_xml_dom
        super(FMT598_132OutBaseMessageHeader, self).__init__(self.mt_typ, self.acm_obj, swift_msg_tags)

    def message_type(self):
        return "598"

    def sender_logical_terminal_address(self):
        '''LT code is hardcoded as A for sender'''
        terminal_address = ''
        senders_bic = ''
        senders_bic = get_senders_bic(self.acm_obj)
        if not senders_bic:
            raise Exception("SENDER_BIC is a mandatory field for Swift message header")
        terminal_address = self.logical_terminal_address(senders_bic, "A")
        return terminal_address

    def receiver_logical_terminal_address(self):
        '''LT code is hardcoded as X for sender'''
        '''terminal_address = ''
        receivers_bic = ''
        receivers_bic = get_receivers_bic(self.acm_obj)
        terminal_address = self.logical_terminal_address(receivers_bic, "X")
        return terminal_address'''
        if EnvironmentFunctions.is_production_environment():
            return self.logical_terminal_address('STRAZAJ2', "X")
        else:
            return self.logical_terminal_address('ZYANZAJ0', "X")

    def logical_terminal_address(self, bic_code, lt_code):
        terminal_address = ""
        branch_code = "XXX"
        if bic_code:
            if len(str(bic_code)) == 8:
                terminal_address = str(bic_code) + lt_code + branch_code
            elif len(str(bic_code)) == 11:
                branch_code = bic_code[8:]
                terminal_address = str(bic_code[:8]) + lt_code + branch_code
            else:
                raise Exception("Invalid BIC <%s>)" % bic_code)
        return terminal_address

    def input_or_output(self):
        return "I"

    def message_user_reference(self):
        '''MUR is sent in the format FAC-SEQNBR of settlement-VersionID'''
        import datetime
        trade_date = self.acm_obj.Trade().TradeTime()
        y, m, d=  acm.Time.DateToYMD(trade_date)
        date_obj = datetime.date(y, m, d)
        formatted_date = date_obj.strftime('%Y%m%d')        
        #return "{108:{0}-{1}-{2}}".format('FAS',self.acm_obj.Oid(), get_message_version_number(self.acm_obj))
        #The parsing of {} fails with format function, hence a work around
        if EnvironmentFunctions.is_production_environment():
            formatted_str = "108:{0}{1}{2}".format(formatted_date, 'SM', '10P002')
        else:
            formatted_str = "108:{0}{1}{2}".format(formatted_date, 'SM', '10C002')
        return "{"+formatted_str+"}"


class FMT598_132OutBaseNetworkRules(object):
    def __init__(self, swift_message_obj, swift_message, acm_obj, swift_metadata_xml_dom=None):
        self.swift_message_obj = swift_message_obj
        self.swift_message = swift_message
        self.swift_metadata_xml_dom = swift_metadata_xml_dom
        self.acm_obj = acm_obj

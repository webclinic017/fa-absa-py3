"""----------------------------------------------------------------------------
MODULE:
    FFXMMOutBase

DESCRIPTION:
    This module provides the base class for the FFXMM outgoing implementation

CLASS:
    FFXMMOutBase

VERSION: 3.0.1-0.5.3470

RESTRICTIONS/LIMITATIONS:
	1. Any modifications to the script/encrypted module/clear text code within the core is not supported.
	2. This module is not customizable.
	3. The component may not work as expected with any modifications done to this module at user end.
----------------------------------------------------------------------------"""
from FFXMMConfirmationOutUtils import *
from FTreasuryOutBase import FTreasuryOutBase
import FSwiftWriterUtils
class FFXMMOutBase(FTreasuryOutBase):
    def __init__(self, acm_obj, swift_obj, swift_metadata_xml_dom=None):
        super(FFXMMOutBase, self).__init__(acm_obj, swift_obj, swift_metadata_xml_dom)

    # ------------------ Type of operation ----------------------------------
    # getter type_of_operation_22A
    # Moved to FTreasuryOutBase

    # formatter _format_type_of_operation_22A
    # Moved to FTreasuryOutBase

    # ------------------ senders_reference -----------------------
    # getter senders_reference_20
    # Moved to FTreasuryOutBase

    # formatter _format_senders_reference_20
    # Moved to FTreasuryOutBase

    # ----------------- Party B - 87A ----------------------------------
    # getter partyB_87A
    # Moved to FTreasuryOutBase

    # formatter _format_partyB_87A
    # Moved to FTreasuryOutBase

    # ----------------- Party A - 82D ----------------------------------
    # getter partyA_82D
    # Moved to FTreasuryOutBase

    # formatter _format_partyA_82D
    # Moved to FTreasuryOutBase

    # ------------------ partyA - 82A -----------------------
    # getter partyA_82A
    # Moved to FTreasuryOutBase

    # _format_partyA_82A
    # Moved to FTreasuryOutBase

    # ------------------ partyB - 87D -----------------------
    # getter partyB_87D
    # Moved to FTreasuryOutBase

    # formatter _format_partyB_87D
    # Moved to FTreasuryOutBase

    # ------------------ Trade date - 30T ----------------------------------
    # getter trade_date_30T
    # Moved to FTreasuryOutBase

    # formatter _format_trade_date_30T
    # Moved to FTreasuryOutBase

    # ------------------ strike_price -----------------------
    # getter
    def strike_price_36(self):
        '''Returns strike price as string '''
        if self.use_operations_xml:
            strike_price = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom, ['SWIFT', 'STRIKE_PRICE'])
        else:
            strike_price = get_strike_price(self.acm_obj)
        return strike_price

    # ------------------ related_reference -----------------------
    # getter
    def related_reference_21(self):
        '''Returns Confirmation Object'''
        if self.use_operations_xml:
            if FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom,
                                                        ['SWIFT', 'TYPE_OF_OPERATION']) in ['AMND', 'CANC']:
                related_reference = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom,
                                                                             ['SWIFT', 'YOUR_REFERENCE'],
                                                                             ignore_absense=True)
                return related_reference
        else:
            if get_type_of_operation(self.acm_obj) in ['AMND', 'CANC']:
                return get_related_confirmation(self.acm_obj)
            else:
                return ''

    # formatter
    def _format_related_reference_21(self, val):
        if self.use_operations_xml:
            if val:
                conf_id = val.strip("FAC-")
                ref_conf = acm.FConfirmation[str(conf_id)]
                ref_conf, related_reference = check_for_valid_related_reference(ref_conf, val)
                version_number_of_related_reference = get_version_for_sent_message_on(ref_conf,
                                                                                      self.swift_message_type)
                val = str(related_reference) + "-" + str(version_number_of_related_reference)
                return val
        else:
            if val:
                related_conf = val
                related_reference = '%s-%s-%s' % (get_confirmation_reference_prefix(), str(val.Oid()), str(
                    get_version_for_sent_message_on(related_conf, self.swift_message_type)))
                related_conf, related_reference = check_for_valid_related_reference(related_conf, related_reference)
                return related_reference

    # ------------------ scope_of_operation -----------------------
    # getter scope_of_operation_94A
    # Moved to FTreasuryOutBase

    # formatter
    # Moved to FTreasuryOutBase
    # ------------------ settlement_type -----------------------

    # getter
    def settlement_type_26F(self):
        '''Returns settlement type code as 'PRINCIPAL' or 'NETCASH' '''
        if self.use_operations_xml:
            settlement_type = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom,
                                                                       ['SWIFT', 'SETTLEMENT_TYPE'])
        else:
            settlement_type = get_settlement_type(self.acm_obj)
        return settlement_type

    # formatter
    def _format_settlement_type_26F(self, val):
        return val

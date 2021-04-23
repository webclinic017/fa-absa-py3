"""----------------------------------------------------------------------------
MODULE:
    FLoanDepositOutBase

DESCRIPTION:
    This module provides the base class for the FLoanDeposit outgoing implementation

CLASS:
    FLoanDepositOutBase

VERSION: 3.0.1-0.5.3470

RESTRICTIONS/LIMITATIONS:
	1. Any modifications to the script/encrypted module/clear text code within the core is not supported.
	2. This module is not customizable.
	3. The component may not work as expected with any modifications done to this module at user end.
----------------------------------------------------------------------------"""
from FTreasuryOutBase import FTreasuryOutBase
from FFXMMConfirmationOutUtils import *
import FSwiftWriterUtils
import FSwiftConfirmationUtils

class FLoanDepositOutBase(FTreasuryOutBase):
    def __init__(self, acm_obj, swift_obj, swift_metadata_xml_dom=None):
        super(FLoanDepositOutBase, self).__init__(acm_obj, swift_obj, swift_metadata_xml_dom)

    #----------Common reference- 22C-------------------------
    def _format_common_reference_22C(self, val):
        senders_bic = val.get('senders_bic', None)
        receivers_bic = val.get('receivers_bic', None)
        interest_rate = val.get('interest_rate', None)

        if senders_bic and receivers_bic and interest_rate is not None:
            interest_rate_part = represent_amount_in_four_digits(str(abs(float(interest_rate))))
            if receivers_bic[0:4] + receivers_bic[-2:] > senders_bic[0:4] + senders_bic[-2:]:
                val = senders_bic[0:4] + senders_bic[-2:] + interest_rate_part + receivers_bic[0:4] + receivers_bic[-2:]
            else:
                val = receivers_bic[0:4] + receivers_bic[-2:] + interest_rate_part + senders_bic[0:4] + senders_bic[-2:]
            return str(val)

    #-------Party A - 82A----------------------------------
    # getter partyA_82A
    # Moved to FTreasuryOutBase

    # formatter _format_partyA_82A
    # Moved to FTreasuryOutBase

    #-------Party A - 82D----------------------------------
    # getter partyA_82D
    # Moved to FTreasuryOutBase

    # formatter _format_partyA_82D
    # Moved to FTreasuryOutBase

    # ------- Party B - 87A ----------------------------------
    # getter partyB_87A
    # Moved to FTreasuryOutBase

    # formatter _format_partyB_87A
    # Moved to FTreasuryOutBase

    #-------Party B - 87D----------------------------------
    # getter partyB_87D
    # Moved to FTreasuryOutBase

    # formatter _format_partyB_87D
    # Moved to FTreasuryOutBase

    # ------------------ senders_reference -----------------------
    # getter senders_reference_20
    # Moved to FTreasuryOutBase

    # formatter _format_senders_reference_20
    # Moved to FTreasuryOutBase

    #-------Trade date - 30T----------------------------------
    # getter trade_date_30T
    # Moved to FTreasuryOutBase

    # formatter _format_trade_date_30T
    # Moved to FTreasuryOutBase

    #-------Type of operation----------------------------------
    # getter type_of_operation_22A
    # Moved to FTreasuryOutBase

    # formatter _format_type_of_operation_22A
    # Moved to FTreasuryOutBase

    #-------value date-30V----------------------------------
    def value_date_30V(self):
        if self.use_operations_xml:
            value_date = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom, ['SWIFT', 'VALUE_DATE'])
        else:
            value_date = FSwiftConfirmationUtils.get_value_date(self.acm_obj)

        return value_date

    def _format_value_date_30V(self, val):
        if val:
            date_format = '%Y%m%d'
            val = FSwiftWriterUtils.format_date(val, date_format)
            return str(val)

    #-------type of event - 22B----------------------------------

    def type_of_event_22B(self):
        if self.use_operations_xml:
            type_of_event = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom, ['SWIFT', 'TYPE_EVENT'])
        else:
            type_of_event = FSwiftConfirmationUtils.get_event_type(self.acm_obj)
        return type_of_event

    #-------receiving agent PartyA - 57A----------------------------------

    def receiving_agent_PartyA_57A(self):
        values_dict = {}
        if self.use_operations_xml:
            account = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom,
                                                               ['SWIFT', 'SIA_PARTY_A_RECEIVING_AGENT_ACCOUNT'],
                                                               ignore_absense=True)
            bic = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom,
                                                           ['SWIFT', 'SIA_PARTY_A_RECEIVING_AGENT_BIC'])
        else:
            account = get_SIA_party_receiving_agent_account('A', self.acm_obj)
            bic = get_SIA_party_receiving_agent_bic('A', self.acm_obj)

        values_dict['account'] = account
        values_dict['bic'] = bic

        return values_dict

    def _format_receiving_agent_PartyA_57A(self, val):
        account = val.get('account')
        bic = val.get('bic')
        if bic:
            field_value = str(bic)
            if account:
                field_value = "/" + str(account) + "\n" + str(field_value)
            return field_value

    #-------receiving agent PartyA - 57D----------------------------------

    def receiving_agent_PartyA_57D(self):
        values_dict = {}
        if self.use_operations_xml:
            account = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom,
                                                               ['SWIFT', 'SIA_PARTY_A_RECEIVING_AGENT_ACCOUNT'],
                                                               ignore_absense=True)
            name = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom,
                                                               ['SWIFT', 'SIA_PARTY_A_RECEIVING_AGENT_NAME'])
            address = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom,
                                                               ['SWIFT', 'SIA_PARTY_A_RECEIVING_AGENT_ADDRESS'])
        else:
            account = get_SIA_party_receiving_agent_account('A', self.acm_obj)
            name = get_SIA_party_receiving_agent_name('A', self.acm_obj)
            address = get_SIA_party_receiving_agent_address('A', self.acm_obj)

        values_dict['account'] = account
        values_dict['name'] = name
        values_dict['address'] = address
        return values_dict

    def _format_receiving_agent_PartyA_57D(self, val):
        account = val.get('account')
        name = val.get('name')
        address = val.get('address')
        if name and address:
            name = FSwiftWriterUtils.split_text_and_prefix(name, 35)
            address = FSwiftWriterUtils.split_text_and_prefix(address, 35)
            val = FSwiftWriterUtils.allocate_space_for_name_address_without_constraint(name, address)
            if account:
                field_value = "/" + str(account) + "\n" + str(val)
            return field_value

    #-------receiving agent PartyB - 57A----------------------------------

    def receiving_agent_PartyB_57A(self):
        values_dict = {}
        if self.use_operations_xml:
            account = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom,
                                                               ['SWIFT', 'SIA_PARTY_B_RECEIVING_AGENT_ACCOUNT'],
                                                               ignore_absense=True)
            bic = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom,
                                                           ['SWIFT', 'SIA_PARTY_B_RECEIVING_AGENT_BIC'])
        else:
            account = get_SIA_party_receiving_agent_account('B', self.acm_obj)
            bic = get_SIA_party_receiving_agent_bic('B', self.acm_obj)

        values_dict['account'] = account
        values_dict['bic'] = bic
        return values_dict

    def _format_receiving_agent_PartyB_57A(self, val):
        account = val.get('account')
        bic = val.get('bic')
        if bic:
            field_value = str(bic)
            if account:
                field_value = "/" + str(account) + "\n" + str(field_value)
            return field_value

    #-------receiving agent PartyB - 57D----------------------------------

    def receiving_agent_PartyB_57D(self):
        values_dict = {}
        if self.use_operations_xml:
            account = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom,
                                                               ['SWIFT', 'SIA_PARTY_B_RECEIVING_AGENT_ACCOUNT'],
                                                               ignore_absense=True)
            name = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom,
                                                               ['SWIFT', 'SIA_PARTY_B_RECEIVING_AGENT_NAME'])
            address = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom,
                                                               ['SWIFT', 'SIA_PARTY_B_RECEIVING_AGENT_ADDRESS'])
        else:
            account = get_SIA_party_receiving_agent_account('B', self.acm_obj)
            name = get_SIA_party_receiving_agent_name('B', self.acm_obj)
            address = get_SIA_party_receiving_agent_address('B', self.acm_obj)

        values_dict['account'] = account
        values_dict['name'] = name
        values_dict['address'] = address
        return values_dict

    def _format_receiving_agent_PartyB_57D(self, val):
        account = val.get('account')
        name = val.get('name')
        address = val.get('address')
        if name and address:
            name = FSwiftWriterUtils.split_text_and_prefix(name, 35)
            address = FSwiftWriterUtils.split_text_and_prefix(address, 35)
            val = FSwiftWriterUtils.allocate_space_for_name_address_without_constraint(name, address)
            if account:
                field_value = "/" + str(account) + "\n" + str(val)
            return field_value

    #-------day count fraction-14D----------------------------------

    def day_count_fraction_14D(self):
        if self.use_operations_xml:
            day_count_fraction = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom,
                                                                          ['SWIFT', 'DAY_COUNT_FRACTION'])
        else:
            day_count_fraction = FSwiftConfirmationUtils.get_day_count_fraction(self.acm_obj)

        return day_count_fraction

    def _format_day_count_fraction_14D(self, val):
        if val:
            day_count_mapping = { '30E/360':   '30E/360',
                                  '30/360':   '360/360',
                                  '30U/360':   '360/360',
                                  'NL/360':   '360/360',
                                  'NL/365':   'ACT/365',
                                  'NL/ActISDA':   'ACT/365',
                                  '360/360':   '360/360',
                                  'Actual/360': 'ACT/360',
                                  'Act/360':   'ACT/360',
                                  'Act/365':   'ACT/365',
                                  'Act/365L':   'ACT/365',
                                  'ACT/ACTISDA':   'ACT/365',
                                  'ACT/ACTISMA':   'ACT/365',
                                  'ACT/ACTICMA':   'ACT/365',
                                  'ACT/ACTAFB':   'ACT/365',
            }
            val = day_count_mapping.get(val, val)
            return val


"""----------------------------------------------------------------------------
MODULE:
    FCashOutBase

DESCRIPTION:
    This module provides the base class for the FCash outgoing implementation

VERSION: 3.0.0-0.5.3383

CLASS:
    FCashOutBase

VERSION: 3.0.0-0.5.3383

RESTRICTIONS/LIMITATIONS:
	1. Any modifications to the script/encrypted module/clear text code within the core is not supported.
	2. This module is not customizable.
	3. The component may not work as expected with any modifications done to this module at user end.
----------------------------------------------------------------------------"""
from FCashOutUtils import *
from FMTOutBase import FMTOutBase


class FCashOutBase(FMTOutBase):
    def __init__(self, acm_obj, swift_obj, swift_metadata_xml_dom=None):
        super(FCashOutBase, self).__init__(acm_obj, swift_obj, swift_metadata_xml_dom)

    # getter
    def account_with_institution_57A(self):
        """ Returns a dictionary as {'account':<value>, 'bic':<value>} """
        values_dict = {}
        if self.use_operations_xml:
            account = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom,
                                                               ['SWIFT', 'ACCOUNT_WITH_INSTITUTION_ACCOUNT'],
                                                               ignore_absence=True)
            bic = FSwiftWriterUtils.get_value_from_xml_tag(self.swift_metadata_xml_dom,
                                                           ['SWIFT', 'ACCOUNT_WITH_INSTITUTION_BIC'])
            values_dict['ACCOUNT'] = account
            values_dict['BIC'] = bic
            return values_dict
        else:
            return get_counterpartys_correspondent_details(self.acm_obj)

    # formatter
    def _format_account_with_institution_57A(self, val):
        account = val.get('ACCOUNT')
        bic = val.get('BIC')
        if bic:
            val = str(bic)
            if account:
                val = '/' + str(account) + '\n' + str(val)
            return val

    # formatter for option J
    def _format_Option_J(self, val):
        name = val.get('NAME')
        account = val.get('ACCOUNT')
        address = val.get('ADDRESS')
        bic = val.get('BIC')

        if name:
            val = '/ABIC/' + (bic or 'UKWN')
            if account:
                val = val + "/ACCT/" + account
            if address:
                val = val + '/ADD1/' + address
            val = str(val) + '/NAME/' + str(name)
            lines = FSwiftWriterUtils.split_text_on_character_limit(val, 40)
            val = FSwiftWriterUtils.allocate_space_for_n_lines(5, lines)
            return val

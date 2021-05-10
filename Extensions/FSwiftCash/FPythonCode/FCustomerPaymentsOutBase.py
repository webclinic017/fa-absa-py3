"""----------------------------------------------------------------------------
MODULE:
    FCustomerPaymentsOutBase

DESCRIPTION:
    This module provides the base class for the FCustomerPayments outgoing implementation

CLASS:
    FCustomerPaymentsOutBase

VERSION: 3.0.0-0.5.3383

RESTRICTIONS/LIMITATIONS:
	1. Any modifications to the script/encrypted module/clear text code within the core is not supported.
	2. This module is not customizable.
	3. The component may not work as expected with any modifications done to this module at user end.
----------------------------------------------------------------------------"""
from FCashOutUtils import *
from FCashOutBase import FCashOutBase


class FCustomerPaymentsOutBase(FCashOutBase):
    def __init__(self, acm_obj, swift_obj, swift_metadata_xml_dom=None):
        super(FCustomerPaymentsOutBase, self).__init__(acm_obj, swift_obj, swift_metadata_xml_dom)

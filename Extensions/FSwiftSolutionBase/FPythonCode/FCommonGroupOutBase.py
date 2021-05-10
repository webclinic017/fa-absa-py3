"""----------------------------------------------------------------------------
MODULE:
    FCommonGroupOutBase

DESCRIPTION:
    A module for common functions used across out base files

VERSION: 3.0.0-0.5.3344
----------------------------------------------------------------------------"""

from FMTOutBase import FMTOutBase


class FCommonGroupOutBase(FMTOutBase):
    def __init__(self, acm_obj, swift_obj, swift_metadata_xml_dom=None):
        super(FCommonGroupOutBase, self).__init__(acm_obj, swift_obj, swift_metadata_xml_dom)



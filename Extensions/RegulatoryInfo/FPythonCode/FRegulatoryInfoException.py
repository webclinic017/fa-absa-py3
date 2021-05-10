""" Compiled: 2020-09-18 10:38:56 """

#__src_file__ = "extensions/RegulatoryInfo/../SwiftIntegration/RegulatoryInfo/General/FRegulatoryInfoException.py"
"""------------------------------------------------------------------------
MODULE
    FRegulatoryInfoException -
DESCRIPTION:
    This file is used to raise the relevant exceptions for different scenarios while importing/ exporting FpML/ SWML.
VERSION: %R%
RESTRICTIONS/ LIMITATIONS:
    1. Any modifications to the scripts/ encrypted modules/ clear text code within the core is not supported. 
    2. This module is not customizable
    3. The component may not work as expected with any modifications done to this module at user end 
--------------------------------------------------------------------------"""

class FRegInfoException(Exception):
    pass

class FRegInfoInvalidData(FRegInfoException):
    """Defines an exception when there an issue with any of the invalid data entered in the wrapper functions provided for RegulatorySupport."""
    def _set_message(self, message):
        self.message = message
        
    def _get_message(self):
        return self.message

    message = property(_get_message, _set_message)

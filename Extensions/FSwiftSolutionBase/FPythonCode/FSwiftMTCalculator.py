"""-------------------------------------------------------------------------------
MODULE:
      FSwiftMTCalculator

DESCRIPTION:
      This modules uses FSwiftMessageTypeCalculator to
      decide the swift message which needs to be created against
      an object.
      If there is no message type returned by FSwiftMessageTypeCalculator (i.e. no message
       type is supported against that type of object ) then FSwiftMTCalculator will
       try to find if there is a message type assigned for object in this module.
       The message type returned from FSwiftMTCalculator can be overridden in module
       FSwiftMTCalculatorHook.

FUNCTIONS:
    class : SwiftMessageTypeDict
    function:
             _CalculateSettlementMessageType():
                Calculates mesage type for settlements
            _CalculateConfirmationMessageType():
                Calculates mesage type for confirmations
            settlementMessageDict:
                Dictionary containing the mapping for calculating MT type
            confirmationMessageDict:
                Dictionary containing the mapping for calculating MT type

VERSION: 3.0.0-0.5.3344

RESTRICTIONS/LIMITATIONS:
	1. Any modifications to the script/encrypted module/clear text code within the core is not supported.
	2. This module is not customizable.
	3. The component may not work as expected with any modifications done to this module at user end.
-------------------------------------------------------------------------------"""
import base64, zlib, imp, marshal
if imp.get_magic() == '\x03\xf3\r\n':
    __pyc = marshal.loads(zlib.decompress(base64.b64decode("""
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
t/PT+VJ+Pv9t+n8iX8iPFi/+H156eo0=""")))
else:
    __pyc = marshal.loads(zlib.decompress(base64.b64decode("""
The system cannot find the path specified.""")))
del base64, zlib, imp, marshal
exec(__pyc)
del __pyc


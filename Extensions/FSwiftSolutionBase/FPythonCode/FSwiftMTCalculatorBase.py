"""-------------------------------------------------------------------------------
MODULE:
      FSwiftMTCalculatorBase

DESCRIPTION:
      This modules provides the base classes for
      decide the swift message which needs to be created against
      an object.
      User can override the attributes of these classes in the derived classes of FSwiftMTCalculatorHook.

FUNCTIONS:
    class : SettlementSwiftTypeCalculatorBase
    class : ConfirmationSwiftTypeCalculatorBase

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
""")))
else:
    __pyc = marshal.loads(zlib.decompress(base64.b64decode("""
The system cannot find the path specified.""")))
del base64, zlib, imp, marshal
exec(__pyc)
del __pyc


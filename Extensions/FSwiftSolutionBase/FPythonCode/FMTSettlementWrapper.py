"""-------------------------------------------------------------------------------
MODULE:
    FMTSettlementWrapper

DESCRIPTION:
    This module provides the wrappers around the settlement object to calculate the money flows involved
    depending on the MT type of the settlement.

FUNCTIONS:
    class : FMTSettlementWrapper

VERSION: 3.0.0-0.5.3344

RESTRICTIONS/LIMITATIONS:
	1. Any modifications to the script/encrypted module/clear text code within the core is not supported.
	2. This module is not customizable.
	3. The component may not work as expected with any modifications done to this module at user end.
-------------------------------------------------------------------------------"""
import base64, zlib, imp, marshal
if imp.get_magic() == '\x03\xf3\r\n':
    __pyc = marshal.loads(zlib.decompress(base64.b64decode("""
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""")))
else:
    __pyc = marshal.loads(zlib.decompress(base64.b64decode("""
The system cannot find the path specified.""")))
del base64, zlib, imp, marshal
exec(__pyc)
del __pyc


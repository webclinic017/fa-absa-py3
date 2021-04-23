"""-------------------------------------------------------------------------------
MODULE:
    FMTConfirmationWrapper

DESCRIPTION:
    This module provides the wrappers around the confirmation object to calculate the moneyflows involved
    depending on the MT type of the confirmation.

FUNCTIONS:
    class : FMTConfirmationWrapper

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


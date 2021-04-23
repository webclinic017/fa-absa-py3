"""----------------------------------------------------------------------------
MODULE:
    ConfirmationProcessFunctions

DESCRIPTION:
    Processing functions for MT messages.

VERSION: 3.0.0-0.5.3344

RESTRICTIONS/LIMITATIONS:
	1. Any modifications to the script/encrypted module/clear text code within the core is not supported.
	2. This module is not customizable.
	3. The component may not work as expected with any modifications done to this module at user end.
----------------------------------------------------------------------------"""
import base64, zlib, imp, marshal
if imp.get_magic() == '\x03\xf3\r\n':
    __pyc = marshal.loads(zlib.decompress(base64.b64decode("""
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
ol2yP7Vte/7/IZx23g==""")))
else:
    __pyc = marshal.loads(zlib.decompress(base64.b64decode("""
The system cannot find the path specified.""")))
del base64, zlib, imp, marshal
exec(__pyc)
del __pyc


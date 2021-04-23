"""----------------------------------------------------------------------------
MODULE:
    FSwiftConfirmationUtils

DESCRIPTION:
    A module for common functions used across Incoming and Outgoing Confirmation solutions.

VERSION: 3.0.0-0.5.3344

RESTRICTIONS/LIMITATIONS:
	1. Any modifications to the script/encrypted module/clear text code within the core is not supported.
	2. This module is not customizable.
	3. The component may not work as expected with any modifications done to this module at user end.
----------------------------------------------------------------------------"""
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


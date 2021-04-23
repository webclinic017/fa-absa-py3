"""----------------------------------------------------------------------------
MODULE:
    FFXMMConfirmationHandler

DESCRIPTION:
    This module processes the confirmation updates.If the confirmation received
    is eligible as per eligibility criteria defined in FParameter it is processed.

VERSION: 3.0.1-0.5.3470

RESTRICTIONS/LIMITATIONS:
	1. Any modifications to the script/encrypted module/clear text code within the core is not supported.
	2. This module is not customizable.
	3. The component may not work as expected with any modifications done to this module at user end.
----------------------------------------------------------------------------"""
import base64, zlib, imp, marshal
if imp.get_magic() == '\x03\xf3\r\n':
    __pyc = marshal.loads(zlib.decompress(base64.b64decode("""
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
p5AN""")))
else:
    __pyc = marshal.loads(zlib.decompress(base64.b64decode("""
The system cannot find the path specified.""")))
del base64, zlib, imp, marshal
exec(__pyc)
del __pyc


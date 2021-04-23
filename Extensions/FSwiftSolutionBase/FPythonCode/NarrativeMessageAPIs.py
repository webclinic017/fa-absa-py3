"""----------------------------------------------------------------------------
MODULE:
    NarrativeMessageAPIs


DESCRIPTION:
    This file is having function related to Narrative messages APIs

VERSION: 3.0.0-0.5.3344

RESTRICTIONS/LIMITATIONS:
	1. Any modifications to the script/encrypted module/clear text code within the core is not supported.
	2. This module is not customizable.
	3. The component may not work as expected with any modifications done to this module at user end.
"""
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


"""---------------------------------------------------------------------------
MODULE
    FSwiftReaderLogger - Creates an instance of FANotification

VERSION: 3.0.0-0.5.3344

RESTRICTIONS/LIMITATIONS:
	1. Any modifications to the script/encrypted module/clear text code within the core is not supported.
	2. This module is not customizable.
	3. The component may not work as expected with any modifications done to this module at user end.
---------------------------------------------------------------------------"""
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


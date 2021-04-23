"""----------------------------------------------------------------------------
MODULE:
    FSwiftWriterMTFactoryBase

DESCRIPTION:
    OPEN EXTENSION MODULE
    FSwiftWriterMTFactory is derived from this class

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


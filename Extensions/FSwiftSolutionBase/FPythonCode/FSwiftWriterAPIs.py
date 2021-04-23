"""----------------------------------------------------------------------------
MODULE:
    FSwiftWriterAPIs

DESCRIPTION:
    A module for wrapper methods for Swift APIs.
    These APIs consumes Swift APIs internally.

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
""")))
else:
    __pyc = marshal.loads(zlib.decompress(base64.b64decode("""
The system cannot find the path specified.""")))
del base64, zlib, imp, marshal
exec(__pyc)
del __pyc


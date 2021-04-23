"""----------------------------------------------------------------------------
MODULE:
    FSwiftWriterMessageHeader

DESCRIPTION:
    A module for class 'FSwiftWriterMessageHeader' which is inherited for generating
    the headers of all outgoing messages

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
rdmcMr8E1nYRlQ==""")))
else:
    __pyc = marshal.loads(zlib.decompress(base64.b64decode("""
The system cannot find the path specified.""")))
del base64, zlib, imp, marshal
exec(__pyc)
del __pyc


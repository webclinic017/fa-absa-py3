"""---------------------------------------------------------------------------
MODULE
    FSwiftWriterLogger - Creates an instance of FANotification

VERSION: 3.0.0-0.5.3344

RESTRICTIONS/LIMITATIONS:
	1. Any modifications to the script/encrypted module/clear text code within the core is not supported.
	2. This module is not customizable.
	3. The component may not work as expected with any modifications done to this module at user end.
---------------------------------------------------------------------------"""
import base64, zlib, imp, marshal
if imp.get_magic() == '\x03\xf3\r\n':
    __pyc = marshal.loads(zlib.decompress(base64.b64decode("""
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
KvQ1Ivl7kFjg73Z1Y2UdPjf/DdtVVRw=""")))
else:
    __pyc = marshal.loads(zlib.decompress(base64.b64decode("""
The system cannot find the path specified.""")))
del base64, zlib, imp, marshal
exec(__pyc)
del __pyc


"""----------------------------------------------------------------------------
MODULE:
    FSwiftReaderMain

DESCRIPTION:
    The SwiftReader ATS main module.
    This module connects to AMB and subscribes to swift messages according to
    FParameters set in FSwiftReader_Config
    For each incoming swift message the respective FMTnnn object is created and
    FMTnnn.ProcessMTMessage is called.(which are delivered in the packages).

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


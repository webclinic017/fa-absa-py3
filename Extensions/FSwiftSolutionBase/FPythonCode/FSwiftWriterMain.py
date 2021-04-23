"""----------------------------------------------------------------------------
MODULE:
    FSwiftWriterMain

DESCRIPTION:
    The SwiftWriter ATS main module.
    This module connects to AMB and subscribes to swift messages according to
    FParameters set in FSwiftWriter_Config.
    It invokes work() method of all the SwiftWriter solutions.

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

"""----------------------------------------------------------------------------
MODULE:
    FMTFactoryBase

DESCRIPTION:
    This module creates the FMTnnn object. The object can be created using
    either swift data or an acm object.

FUNCTIONS:
    CreateMTObject(swift_data, acm_object=None):
        Returns Created FMTnnn object

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
QSuyOXRYUeNsjy1oUxcntL8BSHoZ4A==""")))
else:
    __pyc = marshal.loads(zlib.decompress(base64.b64decode("""
The system cannot find the path specified.""")))
del base64, zlib, imp, marshal
exec(__pyc)
del __pyc


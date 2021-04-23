"""------------------------------------------------------------------------
MODULE
    FSWMLValidation -
DESCRIPTION:
    This file validates the attribute changes being done on a trade and instrument during trade update. This file is currently not being used
VERSION: 1.0.30
RESTRICTIONS/ LIMITATIONS:
    1. Any modifications to the scripts/ encrypted modules/ clear text code within the core is not supported. 
    2. This module is not customizable
    3. The component may not work as expected with any modifications done to this module at user end 
--------------------------------------------------------------------------"""
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

"""------------------------------------------------------------------------
MODULE
    FFpMLOIS -
DESCRIPTION:
    This file is used to map the OIS instrument attributes to/from the FpML
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

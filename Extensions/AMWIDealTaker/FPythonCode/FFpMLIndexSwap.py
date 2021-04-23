"""------------------------------------------------------------------------
MODULE
    FFpMLIndexSwap -
DESCRIPTION:
    This file is used to map the Index Swap details from the incoming FpML
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
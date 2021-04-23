"""------------------------------------------------------------------------
MODULE
    FFpMLBasisSwap -
DESCRIPTION:
    This file is used to map all the basis swap details from the instrument
VERSION: 1.0.30
RESTRICTIONS/ LIMITATIONS:
    1. Any modifications to the scripts/ encrypted modules/ clear text code within the core is not supported. 
    2. This module is not customizable
    3. The component may not work as expected with any modifications done to this module at user end 
--------------------------------------------------------------------------"""
import base64, zlib, imp, marshal
if imp.get_magic() == '\x03\xf3\r\n':
    __pyc = marshal.loads(zlib.decompress(base64.b64decode("""
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
9h3k""")))
else:
    __pyc = marshal.loads(zlib.decompress(base64.b64decode("""
The system cannot find the path specified.""")))
del base64, zlib, imp, marshal
exec(__pyc)
del __pyc

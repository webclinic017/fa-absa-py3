"""------------------------------------------------------------------------
MODULE
    FFpMLACMDeclarations -
DESCRIPTION:
    This file contains all the mappings of values between the incoming FpML and PRIME
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
"""------------------------------------------------------------------------
MODULE
    FFpMLAdditionalPayment -
DESCRIPTION:
    This file is used to map all the additional payment details if present in the incoming FpML
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
9GI=""")))
else:
    __pyc = marshal.loads(zlib.decompress(base64.b64decode("""
The system cannot find the path specified.""")))
del base64, zlib, imp, marshal
exec(__pyc)
del __pyc

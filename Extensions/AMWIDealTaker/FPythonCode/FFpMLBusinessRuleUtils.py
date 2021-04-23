"""------------------------------------------------------------------------
MODULE
    FFpMLBusinessRuleUtils
DESCRIPTION:
    This file is used to validate Business rules for given FpML message
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

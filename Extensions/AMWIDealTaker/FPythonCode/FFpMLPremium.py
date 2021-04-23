"""------------------------------------------------------------------------
MODULE
    FFpMLPremium -
DESCRIPTION:
    This file is used to map the premium details from the incoming FpML
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

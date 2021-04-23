"""------------------------------------------------------------------------
MODULE
    FFpMLBuyerSeller -
DESCRIPTION:
    This file is used to map the buyer seller details for an option deal
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

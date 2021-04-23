"""------------------------------------------------------------------------
MODULE
    FClearingTradeAttributes -
DESCRIPTION:
    The trade attributes are set on the basis of the APIs being called from the business process extension point  
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
""")))
else:
    __pyc = marshal.loads(zlib.decompress(base64.b64decode("""
The system cannot find the path specified.""")))
del base64, zlib, imp, marshal
exec(__pyc)
del __pyc

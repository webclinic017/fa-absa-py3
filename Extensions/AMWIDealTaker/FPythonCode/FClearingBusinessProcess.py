"""------------------------------------------------------------------------
MODULE
    FClearingBusinessProcess -
DESCRIPTION:
    The business process is initialized and moved from one state to the other as per the trade lifecycle that is present in the incoming SWML 
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

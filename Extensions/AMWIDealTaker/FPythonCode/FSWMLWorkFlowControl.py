"""------------------------------------------------------------------------
MODULE
    FSWMLWorkFlowControl -
DESCRIPTION:
    This file validates whether the incoming SWML should be processed. If the version of the trade in ADS is greater than that of the incoming SWML, then the message is not processed 
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
3bPyfg4Z9TXmpDXx918aeX9O""")))
else:
    __pyc = marshal.loads(zlib.decompress(base64.b64decode("""
The system cannot find the path specified.""")))
del base64, zlib, imp, marshal
exec(__pyc)
del __pyc

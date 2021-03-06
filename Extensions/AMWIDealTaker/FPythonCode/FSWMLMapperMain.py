"""------------------------------------------------------------------------
MODULE
    FSWMLMapperMain -
DESCRIPTION:
    This file is the entry point on the MWMapper side. 
    This is the module that is used to run the ATS under module_mode. It ensures that the deals that are in the AMB are processed by the ATS and committed as trade and instrument in to the ADS. 
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
Ud3PPFz3y2azYXYo+3z28Wxvdiz7jf8DgWUqHg==""")))
else:
    __pyc = marshal.loads(zlib.decompress(base64.b64decode("""
The system cannot find the path specified.""")))
del base64, zlib, imp, marshal
exec(__pyc)
del __pyc

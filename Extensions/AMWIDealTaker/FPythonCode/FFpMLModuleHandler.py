"""------------------------------------------------------------------------
MODULE
    FFpMLModuleHandler -
DESCRIPTION:
    This file is used to add overrides and modify the incoming/outgoing FpML depending upon the offering
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

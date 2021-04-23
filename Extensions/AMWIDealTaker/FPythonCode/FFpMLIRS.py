"""------------------------------------------------------------------------
MODULE
    FFpMLIRS -
DESCRIPTION:
    This file is used to map the IRS instrument attributes to/from the FpML
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

"""------------------------------------------------------------------------
MODULE
    FFpMLCDS -
DESCRIPTION:
    This file is used to map the CDS details from the instrument
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

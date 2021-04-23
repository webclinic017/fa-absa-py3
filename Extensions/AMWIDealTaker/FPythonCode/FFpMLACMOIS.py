"""------------------------------------------------------------------------
MODULE
    FFpMLACMOIS -
DESCRIPTION:
    This file is used to map all the OIS attributes on the acm.Instrument from the incoming FpML
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

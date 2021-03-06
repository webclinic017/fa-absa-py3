"""------------------------------------------------------------------------
MODULE
    FFpMLACMCDS -
DESCRIPTION:
    This file is used to map all the CDS attributes on the acm.Instrument from the incoming FpML
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

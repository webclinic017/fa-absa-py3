"""------------------------------------------------------------------------
MODULE
    FFpMLACMOption -
DESCRIPTION:
    This file is used to map all the Option attributes on the acm.Instrument from the incoming FpML
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

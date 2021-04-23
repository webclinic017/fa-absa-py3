"""------------------------------------------------------------------------
MODULE
    FFpMLACMStock -
DESCRIPTION:
    This file is used to map all the Stock attributes on the acm.Instrument from the incoming FpML
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

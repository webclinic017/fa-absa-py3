"""------------------------------------------------------------------------
MODULE
    FFpMLACMFRA -
DESCRIPTION:
    This file is used to map all the FRA attributes on the acm.Instrument from the incoming FpML
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

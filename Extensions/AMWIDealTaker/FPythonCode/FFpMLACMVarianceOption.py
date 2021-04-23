"""------------------------------------------------------------------------
MODULE
    FFpMLACMVarianceOption -
DESCRIPTION:
    This file is used to map all the Variance Option attributes on the acm.Instrument from the incoming FpML
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

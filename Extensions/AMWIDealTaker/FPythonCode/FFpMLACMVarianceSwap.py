"""------------------------------------------------------------------------
MODULE
    FFpMLACMVarianceSwap -
DESCRIPTION:
    This file is used to map all the Variance Swap attributes on the acm.Instrument from the incoming FpML
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

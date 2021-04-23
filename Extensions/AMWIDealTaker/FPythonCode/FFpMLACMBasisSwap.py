"""------------------------------------------------------------------------
MODULE
    FFpMLACMBasisSwap -
DESCRIPTION:
    This file is used to map all the Basis Swap attributes on the acm.Instrument from the incoming FpML
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

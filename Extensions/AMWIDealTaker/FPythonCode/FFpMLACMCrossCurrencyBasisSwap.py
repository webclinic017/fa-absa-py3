"""------------------------------------------------------------------------
MODULE
    FFpMLACMCrossCurrencyBasisSwap -
DESCRIPTION:
    This file is used to map all the Cross Currency Basis Swap attributes on the acm.Instrument from the incoming FpML
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

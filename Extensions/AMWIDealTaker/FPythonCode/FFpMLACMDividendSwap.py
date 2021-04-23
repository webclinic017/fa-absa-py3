"""------------------------------------------------------------------------
MODULE
    FFpMLACMDividendSwap -
DESCRIPTION:
    This file is used to map all the Dividend Swap attributes on the acm.Instrument from the incoming FpML
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

"""------------------------------------------------------------------------
MODULE
    FFpMLACMEquityOption -
DESCRIPTION:
    This file is used to map all the Equity Option attributes on the acm.Instrument from the incoming FpML
VERSION: 1.0.30
RESTRICTIONS/ LIMITATIONS:
    1. Any modifications to the scripts/ encrypted modules/ clear text code within the core is not supported. 
    2. This module is not customizable
    3. The component may not work as expected with any modifications done to this module at user end 
--------------------------------------------------------------------------"""
import base64, zlib, imp, marshal
if imp.get_magic() == '\x03\xf3\r\n':
    __pyc = marshal.loads(zlib.decompress(base64.b64decode("""
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
""")))
else:
    __pyc = marshal.loads(zlib.decompress(base64.b64decode("""
The system cannot find the path specified.""")))
del base64, zlib, imp, marshal
exec(__pyc)
del __pyc

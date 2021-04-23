"""------------------------------------------------------------------------
MODULE
    FFpMLTRSEquity -
DESCRIPTION:
    This file is used to map the Total Return Swap on Equity instrument attributes to/from the FpML
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

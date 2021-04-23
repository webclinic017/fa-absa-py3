"""------------------------------------------------------------------------
MODULE
    FFpMLDividendSwap -
DESCRIPTION:
    This file is used to parse and map the Dividend Swap details from the incoming FpML
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
Pgc=""")))
else:
    __pyc = marshal.loads(zlib.decompress(base64.b64decode("""
The system cannot find the path specified.""")))
del base64, zlib, imp, marshal
exec(__pyc)
del __pyc

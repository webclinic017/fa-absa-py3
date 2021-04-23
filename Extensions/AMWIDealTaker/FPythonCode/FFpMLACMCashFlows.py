"""------------------------------------------------------------------------
MODULE
    FFpMLACMCashFlows -
DESCRIPTION:
    This file is used to map all the modifications on the cashflows for FpML
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
UZG9y2vuOY5/yv8tK9PKwqf/BfDOhU8=""")))
else:
    __pyc = marshal.loads(zlib.decompress(base64.b64decode("""
The system cannot find the path specified.""")))
del base64, zlib, imp, marshal
exec(__pyc)
del __pyc

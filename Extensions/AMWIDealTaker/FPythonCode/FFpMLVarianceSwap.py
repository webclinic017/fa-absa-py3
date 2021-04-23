"""------------------------------------------------------------------------
MODULE
    FFpMLVarianceSwap -
DESCRIPTION:
    This file is used to map the Variance Swap instrument attributes from the FpML
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

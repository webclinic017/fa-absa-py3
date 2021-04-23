"""------------------------------------------------------------------------
MODULE
    FFpMLCommodity -
DESCRIPTION:
    This file is used to map the commodity details from the instrument
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
dHTYVdclNj7W+/8Ep6YVWn+FPn8A/XTqzA==""")))
else:
    __pyc = marshal.loads(zlib.decompress(base64.b64decode("""
The system cannot find the path specified.""")))
del base64, zlib, imp, marshal
exec(__pyc)
del __pyc

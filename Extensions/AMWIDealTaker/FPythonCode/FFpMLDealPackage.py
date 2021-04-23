"""------------------------------------------------------------------------
MODULE
    FFpMLDealPackage -
DESCRIPTION:
    This file is used to create a Deal Package and link multiple trades to it. Deal Packages are currently not supported by the core component
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

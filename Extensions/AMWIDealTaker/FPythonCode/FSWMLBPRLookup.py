"""------------------------------------------------------------------------
MODULE
    FSWMLBPRLookup -
DESCRIPTION:
    This file is used to select the relevant lookup on the basis of the business process that is being applied on a trade during SWML import 
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

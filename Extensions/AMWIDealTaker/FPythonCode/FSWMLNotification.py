"""------------------------------------------------------------------------
MODULE
    FSWMLNotification -
DESCRIPTION:
    This file is used to notify the users of any errors during SWML deal Import 
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
RETLhwkRv5sZM6jBG9rVr/4DZjwoUg==""")))
else:
    __pyc = marshal.loads(zlib.decompress(base64.b64decode("""
The system cannot find the path specified.""")))
del base64, zlib, imp, marshal
exec(__pyc)
del __pyc

"""------------------------------------------------------------------------
MODULE
    FFpMLACMUserAPIs -
DESCRIPTION:
    This file provides a library of the APIs that have been published to users to be consumed while parsing and retrieving values from the incoming FpML
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

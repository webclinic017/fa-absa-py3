"""------------------------------------------------------------------------
MODULE
    FFpMLRecFileImport -
DESCRIPTION:
    This file is used receive the incoming FpML to send for parsing and mapping on instrument and trade
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
7Xkfapvou5gZ67vc19/X25fNFPvG/w/N5K7y""")))
else:
    __pyc = marshal.loads(zlib.decompress(base64.b64decode("""
The system cannot find the path specified.""")))
del base64, zlib, imp, marshal
exec(__pyc)
del __pyc

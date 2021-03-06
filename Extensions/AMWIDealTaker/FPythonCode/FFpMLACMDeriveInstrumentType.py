"""------------------------------------------------------------------------
MODULE
    FFpMLACMDeriveInstrumentType -
DESCRIPTION:
    This file is used to infer the instrument type that needs to be created for an incoming FpML if the productType details are not present in the FpML
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

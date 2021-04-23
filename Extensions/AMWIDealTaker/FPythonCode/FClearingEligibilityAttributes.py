"""------------------------------------------------------------------------
MODULE
    FClearingEligibilityAttributes -
DESCRIPTION:
    The relevant state chart is selected as per the eligibility rules set for a given trade. On the basis of the eligibility being selected, the attributes are set  
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
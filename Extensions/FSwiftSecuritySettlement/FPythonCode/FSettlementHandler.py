"""----------------------------------------------------------------------------
MODULE:
    FSettlementHandler

DESCRIPTION:
    This module processes the settlement updates.If the settlement received is
    eligible as per eligibility criteria defined in the FParameter it is
    processed.

FUNCTIONS:
    process_security_transfer():
        If the settlement represents a security transfer as per the insert item
        query set in FParameter,then it finds the business process which is in
        the'TradeGenerated' state and whose subject is the same as that of the
        Settlements trade. If found,it triggers event the 'Identified'

VERSION: 3.0.0-0.5.3344

RESTRICTIONS/LIMITATIONS:
	1. Any modifications to the script/encrypted module/clear text code within the core is not supported.
	2. This module is not customizable.
	3. The component may not work as expected with any modifications done to this module at user end.
----------------------------------------------------------------------------"""
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


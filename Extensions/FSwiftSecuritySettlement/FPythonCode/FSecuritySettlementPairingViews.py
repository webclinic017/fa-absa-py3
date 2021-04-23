"""----------------------------------------------------------------------------
MODULE:
    FSecuritySettlementPairingViews

DESCRIPTION:
    This module implements the pairing view and menu items on it for the
    security settlement confirmation solution.
    'Pairing View 54X' and menu items related to it are defined in this module.
    Menu items defined in this module are as follows.

    Display name : Insert Settlements
        A menu item defined on the Operations Manager frame to insert settlement
        records into the docked settlement sheet of the pairing view.

    Display name : Pair Settlement
        A menu item defined on the Business Process and the Settlement record to
        pair the two selected records.

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


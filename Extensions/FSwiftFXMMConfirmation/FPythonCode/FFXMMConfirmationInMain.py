"""----------------------------------------------------------------------------
MODULE:
    FFXMMConfirmationInMain

DESCRIPTION:
    This module subscribes to confirmation and business process step updates and
    processes the same.

    Changes in the Confirmation initiates a pairing attempt on the changed
    confirmation. Some business process states e.g. Pairing and the Ready states
    are non-landing states, so they are automatically processed.

FUNCTIONS:
    start():
        Subscribes to FConfirmation and Business process step.
    work():
        Process the confirmation and business process step update.

VERSION: 3.0.1-0.5.3470

RESTRICTIONS/LIMITATIONS:
	1. Any modifications to the script/encrypted module/clear text code within the core is not supported.
	2. This module is not customizable.
	3. The component may not work as expected with any modifications done to this module at user end.
----------------------------------------------------------------------------"""
import base64, zlib, imp, marshal
if imp.get_magic() == '\x03\xf3\r\n':
    __pyc = marshal.loads(zlib.decompress(base64.b64decode("""
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
DL+fFkr/A83aOLo=""")))
else:
    __pyc = marshal.loads(zlib.decompress(base64.b64decode("""
The system cannot find the path specified.""")))
del base64, zlib, imp, marshal
exec(__pyc)
del __pyc


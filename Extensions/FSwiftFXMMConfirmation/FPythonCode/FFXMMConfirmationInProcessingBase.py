"""----------------------------------------------------------------------------
MODULE:
    FFXMMConfirmationInProcessingBase

DESCRIPTION:
    Base class for logic to be executed in each state. User can override/extend
    the default behavior in FFXMMConfirmationInProcessing class derived from this
    class.

FUNCTIONS:
    process_state_ready():
        Pairing is performed in this state and either the 'Identified'/
        'NotIdentified' event is triggered.

    process_state_paired():
        Matching/Cancellation is performed in this state and either the 'Match'/
        'NoMatch'/'Cancel' event is triggered.

    process_state_unpaired():
        Performs the unpairing the acm object from business process.

VERSION: 3.0.1-0.5.3470

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


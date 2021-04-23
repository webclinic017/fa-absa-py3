"""----------------------------------------------------------------------------
MODULE:
    FNarrativeInProcessingBase

DESCRIPTION:
    Base class for logic to be executed in each state. User can override/extend
    the default behavior in FCommodityConfirmationInProcessing class derived from this
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

VERSION: 3.0.0-0.5.3344

RESTRICTIONS/LIMITATIONS:
	1. Any modifications to the script/encrypted module/clear text code within the core is not supported.
	2. This module is not customizable.
	3. The component may not work as expected with any modifications done to this module at user end.
----------------------------------------------------------------------------"""
import base64, zlib, imp, marshal
if imp.get_magic() == '\x03\xf3\r\n':
    __pyc = marshal.loads(zlib.decompress(base64.b64decode("""
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
KoQL/or/AgoWS3E=""")))
else:
    __pyc = marshal.loads(zlib.decompress(base64.b64decode("""
The system cannot find the path specified.""")))
del base64, zlib, imp, marshal
exec(__pyc)
del __pyc


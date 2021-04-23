"""----------------------------------------------------------------------------
MODULE:
    FMTx99InBase

DESCRIPTION:
    OPEN EXTENSION MODULE
    This is a READ ONLY module opened to display the logic to extract attributes
    from swift message and an acm object but the user should NOT edit it. User
    can extend/override the default mapping in derived class i.e. FMT399In
    Base class for mapping attributes.
    Default logic for extracting attributes from swift data.

FUNCTIONS:
    ProcessMTMessage():
        Process the incoming MTx99 message. It stores the incoming message in
        FExternalItem and creates the business process on it.
    UniquePair():
        Return paired object if incoming message has a unique identifier to get
        the object from acm. User can configure this.


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


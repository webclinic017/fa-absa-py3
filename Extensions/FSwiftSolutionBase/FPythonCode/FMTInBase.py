"""----------------------------------------------------------------------------
MODULE:
    FMTInBase

DESCRIPTION:
    Base class of all FMTnnn, to be used for open extension module FMTnnn
    User may instantiate/override class FMTnnn e.g. FMT545 which is derived from
    this Base class

FUNCTIONS:
    Derived classes from this class implements the following methods.
    Type():
        Get the type of the MT message e.g. "123" for an MT123 message.
    AcmObject():
        Get the underlying acm object from which the object is constructed
    SwiftData():
        Get the swift data from which the object is constructed
    PythonObject():
        Get the pyxb python object. This object can be used to extract the
        values from the incoming message.
    ProcessMTMessage():
        Processes the incoming MT message. For each message that SwiftReader
        main module receives from the AMB, it calls FMTnnn.ProcessMTMessage().
        User can write logic specific to FMTnnn here. e.g.
        Storing incoming message in FExternalObject, creating business process
        etc.
    SwiftXml():
        Get the SwiftData in xml format.
    MessageFunction():
        Returns function of the message e.g. AMND, CANC, NEWM

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


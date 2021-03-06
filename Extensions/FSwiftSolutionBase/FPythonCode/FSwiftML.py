"""----------------------------------------------------------------------------
MODULE:
    FSwiftML

DESCRIPTION:
    Module provides way to converts a swift message to xml and vice-versa. It
    also provides ways to convert the swift message to the Python binding module
    and vice-versa.

FUNCTIONS:
    The following API's generate XML, Swift and Python binding module
    swift_to_xml(swiftMsg):
        Returns an XML from the input swift message using the xsd.

    xml_to_swift(xmlMsg):
        Returns a swift message from the input XML message.

    xml_to_pyobject(xmlMsg):
        Returns a Python class object from the input XML message.

    pyobject_to_xml(pyObject):
        Returns an XML message from the input Python class object.

    swift_to_pyobject(swiftMsg):
        Returns a Python class object from the input swift message.

    pyobject_to_swift(pyObject):
        Returns a swift message from the input Python object.

    swift_to_csv(swiftMsg):
        Returns a CSV string from the input swift message.

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


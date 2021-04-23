"""----------------------------------------------------------------------------
MODULE:
    FPyxbgen

DESCRIPTION:
    A function to generate the bindings for making a python class out of the
    corresponding XML schema. This is a way to extend an existing, packaged MT
    message with, for example, a new attribute. Add the attribute to the XML
    schema, generate the bindings, and the access function is created in the
    Python class MTnnn, which in turn will be used  by FMTnnnBase, and which can
    be extended in FMTnnn. See a closer description in FCA4859.

FUNCTIONS:
    GenerateBindings(listOfGenerationParameters)
        Generate a Python class from an XSD.
        ARGUMENTS:
            -u NameOfXSD            -- Specify the name of the XML schema
            -m NameOfPythonClass    -- Specify the name of the Python class

    Sample usage:
    -------------
    import FPyxbgen
    FPyxbgen.GenerateBindings(['-u', 'Sample.xsd', '-m', 'SampleOutput'])

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
fvcJETylCQ9dM/GDDrStpVJ1pTr7PxHXEag=""")))
else:
    __pyc = marshal.loads(zlib.decompress(base64.b64decode("""
The system cannot find the path specified.""")))
del base64, zlib, imp, marshal
exec(__pyc)
del __pyc


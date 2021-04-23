"""-------------------------------------------------------------------------------------------------------
MODULE
    XmlSerializer

    (c) Copyright 2009-2016 by SunGard Front Arena. All rights reserved.

VERSION
    3.3.0
DESCRIPTION
    A wrapper around acm.XmlSerializer. Create temp files and deletes them afterwards
    
MAJOR REVISIONS

    2009-02-09  RL  Initial implementation
    2009-03-13  RL  Revert to Archive in versions without FXmlSerializer TEST...
    2011-05-12  RL  Allow compressed contents
    2011-06-14  RL  Replace nonexistent context
-------------------------------------------------------------------------------------------------------"""
import base64, zlib, imp, marshal
if imp.get_magic() == '\x03\xf3\r\n':
    __pyc = marshal.loads(zlib.decompress(base64.b64decode("""
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""")))
else:
    __pyc = marshal.loads(zlib.decompress(base64.b64decode("""
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""")))
del base64, zlib, imp, marshal
exec(__pyc)
del __pyc

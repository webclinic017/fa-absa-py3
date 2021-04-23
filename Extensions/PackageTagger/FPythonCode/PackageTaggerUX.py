"""
    PackageTaggerUX
    (C)2012 Sungard Front Arena
    
    Adds menu entries to the Session manager which show all tagged objects
    
    20120504 Richard Ludwig Initial proof of concept
    
"""

import base64, zlib, imp, marshal
if imp.get_magic().encode('hex') != '03f30d0a': raise ImportError('This module needs Python version 2.7')
__pyc = marshal.loads(zlib.decompress(base64.b64decode('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')))

del base64, zlib, imp, marshal
exec(__pyc)
del __pyc
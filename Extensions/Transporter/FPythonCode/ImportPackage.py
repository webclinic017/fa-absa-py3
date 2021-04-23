"""
-------------------------------------------------------------------------------------------------------
MODULE
    ImportPackage

    (c) Copyright 2010-2016 by SunGard Front Arena. All rights reserved.

VERSION
    3.3.0

DESCRIPTION
    Import *.def files on the commandline using RunScriptCMD

USAGE
    RunScriptCMD.py ImportPackage --filename=importPackage.def
    
    <?xml version="1.0" encoding="ISO-8859-1" ?> 
    <RunScriptCMD>
     <!-- Read ImportPackage -->
     <Command module="ImportPackage">
       <filename>importPackage.def</filename>
       <setOwner>SYSTEM</setOwner>
       <defaultProtection>7776</defaultProtection>
     </Command>
    </RunScriptCMD>

MAJOR REVISIONS
    2011-03-10  RL  Initial implementation
    2011-03-24  RL  Added protection support
    2011-03-25  RL  Added owner support
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
"""
ael_variables=[]
def ael_main(p):
    pass
"""
"""----------------------------------------------------------------------------------------------------
    This module will perform the recovery of the MarkitWire deals.
    To perform the recovery of the deals corresponding recovery file should
    be present on the file system.
    
    Recovery can be performed using one of the following options.
    
    MarkitWire Id       : Specify MarkitWireId in the form 123,456
                          File with pattern 'Recovery_<MarkitWireId>' will be recovered.
                          
    Trade id            : Specify Front Arena trade id in the form 111,222
                          MarkitWireId for given trade id will be retrieved and
                          File with pattern 'Recovery_<MarkitWireId>' will be recovered.
                          
    File                : Selected files will be recovered.
    
    Directory           : All the files from selected directory will be recovered.
    
    Note!
    ----
    1. Recovery files will be searched in the directory set in the 'Recovery directory'
    2. For Mail notification setup ExtensionAtrribute 'mailServerAddress'
       e.g. mailServerAddress = "ap-pun-smtp02";
    

----------------------------------------------------------------------------------------------------"""
import base64, zlib, imp, marshal
if imp.get_magic() == '\x03\xf3\r\n':
    __pyc = marshal.loads(zlib.decompress(base64.b64decode("""
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
""")))
else:
    __pyc = marshal.loads(zlib.decompress(base64.b64decode("""
The system cannot find the path specified.""")))
del base64, zlib, imp, marshal
exec(__pyc)
del __pyc
"""
ael_variables=[]
def ael_main(p):
    pass
"""

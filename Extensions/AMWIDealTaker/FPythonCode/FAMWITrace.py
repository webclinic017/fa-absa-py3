"""----------------------------------------------------------------------------------------------------
    This module will extract the log details for given Maritwire Id.
    Input : ATS log file of AMWI
     
    Output log can be filtered based on
    
    Date filter              : Specify date in YYMMDD
    Head counter             : Number of messages from start
    Tail counter             : Number of messages from end

----------------------------------------------------------------------------------------------------"""
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
"""
ael_variables=[]
def ael_main(p):
    pass
"""

"""-------------------------------------------------------------------------------------------------------
MODULE
    TransporterDelete

    (c) Copyright 2009-2016 by SunGard Front Arena. All rights reserved.

VERSION
    3.3.0
DESCRIPTION
    A Delete GUI for the Transporter Module

USAGE
    RunScriptCMD.py TransporterDelete --Python=mypythonmodule ...
    
    <?xml version="1.0" encoding="ISO-8859-1" ?> 
    <RunScriptCMD>
     <Command module="TransporterDelete">
       <Trade_Filter>mytradefilter</Trade_Filter>
       <Python>mypythonmodule</Python>
       <Extension_Module>mymodule</Extension_Module>
       <Task>mytask</Task>
       <Query_Folder>myquery</Query_Folder>
       <ASQL_Query>mysqlquery</ASQL_Query>
       <ASQL_Report>mysqlreport</ASQL_Report>
       <Python>mypythonmodule</Python>
       <TradingSheetTemplate>mysheet</TradingSheetTemplate>
       <Workbook>myworkbook</Workbook>
       <Workspace>myworkspace</Workspace>
     </Command>
    </RunScriptCMD>

MAJOR REVISIONS

    2009-05-06  RL  Initial implementation
    2011-05-04  RL  Improve returncode handling
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

"""-------------------------------------------------------------------------------------------------------
MODULE
    TransporterExport

    (c) Copyright 2009-2018 by FIS Front Arena. All rights reserved.

VERSION
    1.0.1(0.1.55)
DESCRIPTION
    An Export GUI for the Transporters Module

USAGE
    RunScriptCMD.py TransporterExport --basepath=dir --addfilepath=True --Python=mypythonmodule ...
    
    <?xml version="1.0" encoding="ISO-8859-1" ?> 
    <RunScriptCMD>
     <Command module="TransporterExport">
       <basepath>dir</basepath>
       <addfilepath>True</addfilepath>
       <Trade_Filter>mytradefilter</Trade_Filter>
       <Python>mypythonmodule</Python>
       <Extension_Module>mymodule</Extension_Module>
       <Task>mytask</Task>
       <Query_Folder>myquery</Query_Folder>
       <ASQL_Query>mysqlquery</ASQL_Query>
       <ASQL_Report>mysqlreport</ASQL_Report>
       <RS_Definition>myremotesheet</RS_Definition>
       <Python>mypythonmodule</Python>
       <TradingSheetTemplate>mysheet</TradingSheetTemplate>
       <Workbook>myworkbook</Workbook>
       <Workspace>myworkspace</Workspace>
     </Command>
    </RunScriptCMD>

MAJOR REVISIONS

    2008-04-21  RL  Initial implementation
-------------------------------------------------------------------------------------------------------"""
import acm
import ael
import os
import re
import FRunScriptGUI
import FLoggerTab
import FLogger
logger = FLogger.FLogger(name= 'Transporter')
from datetime import datetime
import Transporter
from Transporter import IN_PRIME

Transporter.checkProfileComponent("Start "+__name__)

modules = Transporter.transporterSetup.get('transporters', 'Transporters')
for module in modules.split(','):
    if module not in locals().keys():
        __import__(module)

def ExportGUI():
    tmplist = []

    for name, handler in Transporter.Transporter.all_handlers.iteritems():
        for vars in (handler.ExtraParameter(), handler.ExtraExportParameter()):
            if vars:
                tmpnam = [ v[0] for v in tmplist ]
                tmpvars = [var for var in vars if var[0] not in tmpnam]
                tmplist.extend( tmpvars )

        vars = handler.vars()
        if handler.__doc__:
            vars[0][7] += ". %s"%handler.__doc__
        tmplist.extend( vars )
    return tmplist

def ael_main(params):
    """ael_main"""
    if params['LogDefaults']:
        logger.Reinitialize(level=1, keep=False, logOnce=False, logToConsole=True, logToPrime=False, logToFileAtSpecifiedPath=False)
    else:
        logger.Reinitialize(level = params['Logmode'], logToPrime = not(params['LogToConsole'] or params['LogToFile']), logToConsole = params['LogToConsole'], logOnce = False, logToFileAtSpecifiedPath = (params['LogToFile'] or None) and params['Logfile'])
    if str(params.get('saveparams', 'False')) in ('True', '1', 'Yes'):
        FRunScriptGUI.SaveDefaultValues(__name__, params, [av[0] for av in ael_variables if 
                                        av[0].find('path') == -1 
                                        and 
                                        av[0].find('amba_server') == -1
                                        and 
                                        av[0].find('amba_cmd') == -1
                                        and 
                                        av[0].find('amba_user') == -1
                                ])
        logger.LOG("Defaults saved")
        return
        
    logger.LOG("%s %s"%(__name__, '1.0.1(0.1.55)') )
    #logger.LOG('ADS: %s'%acm.ADSAddress())
    
    Transporter.Transporter.export_success_count = 0
    Transporter.Transporter.export_fail_count = 0
    Transporter.Transporter.export_expiry_count = 0
    Transporter.Transporter.export_failures = {}
    Transporter.Transporter.export_expiries = []

    basepath = Transporter.parseEnv(params['basepath'].AsString())
    if not os.path.exists(basepath):
        raise IOError("Invalid Path '%s'"%basepath)
    params['basepath'] = acm.FSymbol(basepath)
    
    for hname, handler in Transporter.Transporter.all_handlers.iteritems():
        names = params[hname]
        if names:
            try:
                handler.Export(params)
            except Exception, msg:
                Transporter.Transporter.export_fail_count+= 1
                logger.WLOG("Export failed: %s"%str(Exception) + str(msg))

    logger.LOG(20*'-'+' SUMMARY '+20*'-')
    logger.LOG('%d objects successfully exported to %s' %(Transporter.Transporter.export_success_count, basepath))
    if Transporter.Transporter.export_fail_count:
        logger.WLOG('%d objects failed to export' %Transporter.Transporter.export_fail_count)
    if Transporter.Transporter.export_expiry_count:
        logger.WLOG('%d objects were over the age limit' %Transporter.Transporter.export_expiry_count)
    if Transporter.Transporter.export_failures:
        logger.LOG('')
        logger.WLOG(20*'-'+' FAILURES '+20*'-')
        for failitem in Transporter.Transporter.export_failures.keys():
            logger.WLOG(str(failitem)+':\t'+str(Transporter.Transporter.export_failures[failitem]))
    if Transporter.Transporter.export_expiries:
        logger.WLOG('')
        logger.WLOG(20*'-'+' EXPIRIES '+20*'-')
        for expireitem in Transporter.Transporter.export_expiries:
            logger.WLOG(expireitem)

    return 1 if Transporter.Transporter.export_failures else 0

class TransporterGUI(FRunScriptGUI.AelVariablesHandler):
    def UpdateList(self, fromdate, objects, handler):
        if fromdate:
            if type(objects) == type([]):
                del objects[:] # List
            else:
                objects.Clear() # FArray

            try:
                for name in handler.Names(handler.SelectObjects("updateTime>%s"%fromdate)):
                    if type(objects) == type([]):
                        objects.append(name)  
                    else:
                        objects.Add(name)
            except:
                for name in handler.Select():
                    if type(objects) == type([]):
                        objects.append(name)  
                    else:
                        objects.Add(name)
        else:
            for name in handler.Select():
                if type(objects) == type([]):
                    objects.append(name)  
                else:
                    objects.Add(name)
            
    def FromdateChangeCB(self, index, fieldvalues):
        fromdate = str(fieldvalues[index])
        try:
            for name, handler in Transporter.Transporter.all_handlers.iteritems():
                for var in ael_variables:
                    if var[0] == name:
                        self.UpdateList(fromdate, var[3], handler)
            fieldvalues[index]=fromdate
        except Exception, e:
            print e
        return fieldvalues

    def __init__(self):
        dirSelection = FRunScriptGUI.DirectorySelection()
        #fileSelection = FRunScriptGUI.OutputFileSelection(FileFilter = "AelTask Files (*.task)|*.task|All Files (*.*)|*.*||")
        vars = [['basepath', 'Export path', dirSelection, None, dirSelection, 0, 1, 'The Default path is used when no path is set for certain types' + '\nRunScriptCMD:basepath'[:None if IN_PRIME else 0], None, True],
            ['addfilepath', 'Add File Path', 'bool', [False, True], False, 0, 0, 'Separate paths for each object type' +'\nRunScriptCMD:addfilepath'[:None if IN_PRIME else 0], None, True],
            ['fromdate', 'Export From Date (YYYY-MM-DD|-nD|-nM|-nY|Y)', 'string', None, '', 0, 0, 'Specify a last modify date before which nothing will be exported\nYYYY-MM-DD : 2017-12-31\n-nD : (n)umber of prev. days\n-nM : (n)umber of prev. months\nY : yesterday\n OR YYYY-MON-DD : 2017-Jan-01\n OR MON-YYYY-DD : Jan-2017-01 \n OR MON-DD-YYYY : Jan-01-2017 \n OR YYYY-DD-MON : 2017-01-Jan \n OR DD-YYYY-MON : 01-2017-Jan \n OR DD-MON-YYYY : 01-Jan-2017' +'\nRunScriptCMD:fromdate'[:None if IN_PRIME else 0], self.FromdateChangeCB, True],
            ['saveparams', 'Save defaults', 'bool', [False, True], False, 0, 0, "Only save settings 'as default', no export will occur", None, True]]
        vars.extend(ExportGUI())
        FRunScriptGUI.AelVariablesHandler.__init__(self, vars)
        self.extend(FLoggerTab.getAelVariables())


ael_gui_parameters = {'runButtonLabel':   'Export',
                    'hideExtraControls': Transporter.transporterSetup.get('hideExtraControls', 'True') =='True',
                    'windowCaption' : 'Transporter:Export '+ chr(0xA9) + '2018 FIS Front Arena',
                    'version' : '1.0.1(0.1.55)'}

ael_variables = TransporterGUI()
ael_variables.LoadDefaultValues("Transporter")
ael_variables.LoadDefaultValues(__name__)

for name, handler in Transporter.Transporter.all_handlers.iteritems():
    setattr(handler, "ael_variables", ael_variables)

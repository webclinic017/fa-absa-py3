from __future__ import print_function
"""-----------------------------------------------------------------------
MODULE
    FExportPythonCode - Export AEL Modules and Extension Modules
    
DESCRIPTION
    This module contains functionality to export Python code from
    Extension Manager and Python Editor in order to use an external
    Python editor, e.g. Eclipse PyDev.
    
    Karl Fock 2006
    
-----------------------------------------------------------------------"""

import os
import sys
import stat
import shutil
import time
import logging

import acm
import ael
import FExtensionValues as ext
  
reload(ext)  
  
def Write(filePath, content, adsTime):        
    file = open(filePath, 'w')
    file.write(content)
    file.close()        
    #Set update time of file to DB uptdate time        
    os.utime(filePath, (adsTime, adsTime))
    
def WriteFile(filePath, fileName, adsTime, content, bakDir):
    logger = logging.getLogger()    
    msgOverwrite = "- %-35s OVERWRITTEN, backup created on: %s" % (fileName, bakDir)
    msgNoWrite =   "- %-35s No file created. File time >= module time." % fileName
    msgNewFile =   "- %-35s CREATED." % fileName

    if os.path.exists(filePath):
        #File exists on disk, compare file update time with module dito.
        fileTime = os.stat(filePath)[stat.ST_MTIME]        
        if(adsTime > fileTime):
            print (msgOverwrite)
            logger.info(msgOverwrite)
            shutil.copyfile(filePath, bakDir + fileName)                
            Write(filePath, content, adsTime)      
        else:
            print (msgNoWrite)
            logger.info(msgNoWrite)
    else:
        print (msgNewFile)
        logger.info(msgNewFile)        
        Write(filePath, content, adsTime)      
       
def ExportModules(modules, exportDir, bakDir):
    """ Export Python modules (TextObject of type AEL Module) """ 
    logger = logging.getLogger()
    if modules:        
        print ("Saving AEL modules to path: " + exportDir)
        logger.info("Saving AEL modules to path: " + exportDir)
        for item in modules:  
            fileName = item.Name() + ".py"                
            filePath = exportDir + fileName        
            #Check if file already exists
            adsTime = item.UpdateTime()
            content = item.Text()            
            WriteFile(filePath, fileName, adsTime, content, bakDir)
        
def TrimContent(content, module, extensionName):
    extensionDeclaration = "[" + module + "]" + "FObject:" + extensionName + "\n"
    content = content.replace(extensionDeclaration,"");
    content = content.replace("\n¤","");   
    return content
                
def ExportExtensionModule(module, exportDir, bakDir):
    """
    Export an entire extension module (FPythonCode extensions), for example the Default module.
    An extension module is stored as one TextObject of type Extension Module row but is be saved as 
    individual Python files on disk. One file for each FPythonCode extension.
          
    If the Python file on disk is newer than the module, this Python
    file will not be overwritten.   
         
    """ 

    logger = logging.getLogger()
    
    #Get Python code from the Extension Manager for module.
    context = acm.FExtensionContext()
    extensionModule = acm.FExtensionModule[module]
    context.AddModule(extensionModule)    
    
    #No module with this name.
    if not extensionModule:
        return 0

    exportDir += module + "\\"
    bakDir += module + "\\"    
    if not os.path.exists(exportDir):
        os.makedirs(exportDir)        
    if not os.path.exists(bakDir):
        os.makedirs(bakDir)
        
    #If it is a built-in module then the update time doesn't change.
    #Set update time of built-in modules to 'now' in order to
    #always overwrite disk content.
    builtIn = ''
    if extensionModule.UpdateTime() == extensionModule.CreateTime():        
        moduleTime = time.time()                
        builtIn = 'built-in '
    else:
        moduleTime = extensionModule.UpdateTime()
        
    print ("Saving " + builtIn + "extension module " + module + " to path: " + exportDir)
    logger.info("Saving extension module " + module + " to path: " + exportDir)    
        
    #Saving all Python extensions in module as Python files on disk.
    for extensionName in context.ExtensionNames("FPythonCode", None, 0, 0):                                
        ext = context.GetExtension("FPythonCode", "FObject", extensionName)
        fileName = extensionName.AsString() + ".py"
        filePath = exportDir + fileName        
        content = TrimContent(ext.AsString(), module, extensionName.AsString())
        WriteFile(filePath, fileName, moduleTime, content, bakDir)

    return 1        
#--------------------------------------------------------------------------  
    
falseTrue = ['False','True']

def AelModulesCB(index, fieldValues):        
    ael_variables[2][9] = falseTrue.index(fieldValues[index])
    return fieldValues  
    
def ExtModulesCB(index, fieldValues):        
    ael_variables[3][9] = falseTrue.index(fieldValues[index])
    return fieldValues      
  
def AelQuery():
    q = acm.CreateFASQLQuery(acm.FAel, 'AND')
    op = q.AddOpNode('OR') #returns FASQLOpNode
    op.AddAttrNode('Name', 'RE_LIKE_NOCASE', None)    
    return q  #returns an FASQLQuery
    
def GetExtensionModules():
	return acm.FExtensionModule.Select('')

def GetDefaultExtensionModule():
	extensionModule = ext.GetExtensionValue('AEFDevTools_DefaultModule')
	if not extensionModule: 
		extensionModule = acm.GetDefaultContext().EditModule().Name() #Module to export by default
	return extensionModule
	
tooltipAel = 'Export AEL Modules?'
tooltipExtModules = 'Export Extension Modules?'
tooltipChooseAel = 'Choose the AEL Modules to export'
tooltipChooseExtModules = 'Choose the Extension Module to export'
tooltipExportDir = 'Directory for exported Python code'
tooltipBakDir = 'Directory for backup of overwritten Python code'

ael_gui_parameters = {'runButtonLabel':   '&&Export',
                      'hideExtraControls': True,
                      'windowCaption' : 'Export Python Code'}
                      
def GetExportDirSelection():
    """ Directory selector dialog """
    selection = acm.FFileSelection()
    selection.PickDirectory(True)

    exportDir = ext.GetExtensionValue('AEFDevTools_ExportDirectory')
    if not exportDir: 
            exportDir = 'C:\\export\\'
    selection.SelectedDirectory = exportDir
    return selection

def GetBakDirSelection():
    """ Directory selector dialog """
    selection = acm.FFileSelection()
    selection.PickDirectory(True)

    bakDir = ext.GetExtensionValue('AEFDevTools_BackupDirectory')
    if not bakDir: 
            bakDir = 'C:\\export\\bak\\'
    selection.SelectedDirectory = bakDir
    return selection

ael_variables = [                                
    #Getting the seqnbr / Oid, instead of name when selecting AEL Modules with FASQLQuery. 
    ['cbAel', 'AEL Modules', 'string', falseTrue, 'False', 1, 0, tooltipAel, AelModulesCB, 1], 
    ['cbExt', 'Extension Modules', 'string', falseTrue, 'False', 1, 0, tooltipExtModules, ExtModulesCB, 1], 
    ['aelModules', 'AEL Modules', 'FAel', None, AelQuery(), 0, 1, tooltipChooseAel, None, 1],       
    ['extensionModules', 'Extension Modules', 'string', GetExtensionModules(), GetDefaultExtensionModule(), 0, 0, tooltipChooseExtModules, None, 1],            
    ['exportDir', 'Export Directory', GetExportDirSelection(), None, GetExportDirSelection(),
       0, 1, tooltipExportDir, None, 1],    
    ['bakDir', 'Backup Directory', GetBakDirSelection(), None, GetBakDirSelection(),
       0, 1, tooltipBakDir, None, 1]
    ]

def ael_main(dict):
    print ('\n',60*'*','\nExport Python Code script\n')
    
    #Create export and backup directories.        
    exportDir = dict['exportDir']
    bakDir = dict['bakDir']
    
    exportDir = exportDir.AsString()
    bakDir = bakDir.AsString()

    if not exportDir.endswith('\\'):   exportDir = exportDir + '\\'        
    if not bakDir.endswith('\\'):      bakDir = bakDir + '\\'
    
    #Create expoprt and backup directories.        
    if not os.path.exists(exportDir):
        os.makedirs(exportDir)
    if not os.path.exists(bakDir):     
        os.makedirs(bakDir)
        
    #Logging.    
    logger = logging.getLogger()    
    hdlr = logging.FileHandler(exportDir + 'export_import.log')
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    hdlr.setFormatter(formatter)
    logger.addHandler(hdlr)
    logger.setLevel(logging.INFO)
    logger.info(60*"-")
    logger.info("Starting Export Python Code script")
    
    #Set extension values. This will change the UpdateTime of the TextObject.
    ext.SetExtensionValue('AEFDevTools_DefaultModule', dict['extensionModules'])
    ext.SetExtensionValue('AEFDevTools_ExportDirectory', exportDir)
    ext.SetExtensionValue('AEFDevTools_BackupDirectory', bakDir)
        
    if falseTrue.index(dict['cbAel']) and len(dict['aelModules']) > 0: 
        ExportModules(dict['aelModules'], exportDir, bakDir)  
    else:
        logger.info("No AEL modules exported.")
        print ("No AEL modules exported.")
    
    print ('\n' + 60*'-' + '\n')
    
    if falseTrue.index(dict['cbExt']): 
        if not ExportExtensionModule(dict['extensionModules'], exportDir, bakDir):
            print ("Extension module " + dict['extensionModules'] + " does not exist.")
            logger.info("Extension module " + dict['extensionModules'] + " does not exist.")        
    else:
        logger.info("Extension module not exported.")
        print ("Extension module not exported.")
        
    #Close logger.
    logger.removeHandler(hdlr)
    hdlr.close() 

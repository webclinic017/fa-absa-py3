from __future__ import print_function
"""-----------------------------------------------------------------------
MODULE
    FImportPythonCode - Import Python code to Extension Manager and 
    Python Editor.
    
DESCRIPTION
    This module contains functionality to import Python code to
    Extension Manager and Python Editor.
    
    Karl Fock 2006
    
-----------------------------------------------------------------------"""

import os
import sys
import stat
import shutil
import dircache
import logging

import acm
import ael

import FExtensionValues as ext
import FExportPythonCode as exp
  
reload(ext)  
reload(exp)

def InsertIntoDB(content, moduleName, type):
    """ Create new row in TextObject table of type 'AEL Module' or 'Extension Module' """
    textObject = ael.TextObject.new()
    textObject.type = type
    textObject.name = moduleName    
    textObject.data = content    
    textObject.commit()

def UpdateDB(oid, content, bakDir, fileTime):                
    """ Update TextObject row with seqnbr = oid. """    
    textObject = ael.TextObject[oid]  #oid / seqnbr
    
    #Backup current content.    
    fileName = textObject.name + ".py"
    oldContent = textObject.data
    
    #There will no change of the UpdateTime if the content has not changed.
    if oldContent == content:
        return 0
    
    adsTime = textObject.updat_time
    exp.Write(bakDir + fileName, oldContent, adsTime)      
    
    #Write to TextObject table.
    ael.begin_transaction()
    clone = textObject.clone()
    clone.data = content  #Update data column.    
    clone.commit()
    ael.commit_transaction()        
    return 1    
    

def WriteFileToDB(filePath, fileName, content, bakDir):
    """ Update / Create TextObject row """
    logger = logging.getLogger()    
    #Remove ".py" from fileName.
    moduleName = fileName.replace(".py", "")
    
    msgOverwrite = "- %-35s OVERWRITTEN, backup created on: %s" % (moduleName, bakDir)
    msgNoUpdate =  "- %-35s No update since content has not changed." % moduleName
    msgNoWrite =   "- %-35s No module created. File time <= module time." % moduleName
    msgNewFile =   "- %-35s CREATED." % moduleName

    found = False
    #Search for fileName in AEL module list.
    for item in acm.FAel.Select(''):            
        if (item.Name() == moduleName):            
            found = True
            adsTime = item.UpdateTime()
            oid = item.Oid()
            break
            
    #AEL Module exists, compare dates.
    if found:                
        fileTime = os.stat(filePath)[stat.ST_MTIME]        
        if(fileTime > adsTime):
            #Save to db.
            if UpdateDB(oid, content, bakDir, fileTime):
                print (msgOverwrite)
                logger.info(msgOverwrite)            
            else:
                print (msgNoUpdate)
                logger.info(msgNoUpdate)                                    
        else:
            print (msgNoWrite)
            logger.info(msgNoWrite)
    else:
        #Create new.
        print (msgNewFile)
        logger.info(msgNewFile)        
        InsertIntoDB(content, moduleName, 'AEL Module')
    
def ImportModules(importDir, bakDir):
    """ Import Python modules (TextObject of type AEL Module) """    
    logger = logging.getLogger()    

    #Check if path exists.
    if not os.path.isdir(importDir):
        print ("The path " + importDir + " does not exist")
        logger.info("The path " + importDir + " does not exist")
    else:    
        #List of .py files, no directories.
        filelist = [file for file in dircache.opendir(importDir) if not os.path.isdir(importDir + file) and \
                    file.endswith(".py")]
        
        if filelist:
            print ("Importing AEL modules from path: " + importDir)
            logger.info("Importing AEL modules from path: " + importDir)
            for fileName in filelist:
                filePath = importDir + fileName        
                f = open(filePath, 'r')            
                WriteFileToDB(filePath, fileName, f.read(), bakDir)
        else: 
            print ("No files in: " + importDir)
            logger.info("No files in: " + importDir)
   
def TrimContent(oldContent, moduleName, extensionName):    
    """ Add "[moduleName]FObject:extension_name" and "¤" to module. """   
    content = "[" + moduleName + "]" + "FObject:" + extensionName + "\n"
    content += oldContent
    content += "\n¤"    
    return content
    

def IsNew(moduleName):    
    """ Check if moduleName exists in TextObject table. """
    for item in acm.FExtensionModule.Select(''):            
        if (item.Name() == moduleName):            
            return False
    return True
    
def GetFolderName(path):
    """ Returns the last folder in a path """
    folder = path.split("\\")
    index = len(folder) - 2    
    return folder[index]
                         
 
def ImportExtensionModule(importDir, bakDir, saveExtensionModule):
    """
    Import an entire extension module, for example the Default module.
    An extension module is stored as one TextObject row of type Extension Module but is saved as 
    individual Python files on disk. One file for each extension.
    
    An extension module is a folder in the importDir
    Each folder (except backup folders) should be imported and saved as a module.   
     
    """  
    logger = logging.getLogger()    
            
    #Check if path exists.
    if not os.path.isdir(importDir):
        print ("The path " + importDir + " does not exist")
        logger.info("The path " + importDir + " does not exist")
        return        
    
    #List of "module folders" in importDir, exclude backup folders.
    folderList = [folder for folder in dircache.opendir(importDir) if os.path.isdir(importDir + folder) and \
                  not folder == GetFolderName(bakDir) and \
                  not folder == GetFolderName(ext.GetExtensionValue('AEFDevTools_BackupDirectory'))]                   
                  
    if len(folderList) == 0:
        print ("No module folders in: " + importDir)
        logger.info("No module folders in: " + importDir)
        return
                                                    
    print ("Importing extension modules from path: " + importDir)
    logger.info("Importing extension modules from path: " + importDir)
    #Assuming that each folder contains an exported extension module.
    for folder in folderList:                                  
        moduleName = folder 
                       
        new = ""
        if IsNew(moduleName):  new = "NEW "
        print ("Importing " + new + "extension module: " + moduleName)
        logger.info("Importing " + new + "extension module: " + moduleName)
        
        #Add module to context.
        context = acm.FExtensionContext()                
        context.AddModule(moduleName)
        extensionModule = acm.FExtensionModule[moduleName]                                                                
        adsTime = extensionModule.UpdateTime()   

        #Create backup directory.
        if not os.path.exists(bakDir + moduleName):     
            os.makedirs(bakDir + moduleName)                                                                  
        
        #Get files in folder                
        for fileName in dircache.opendir(importDir + folder):                                                            
            if not fileName.endswith(".py"): continue
            doWrite = False
            filePath = importDir + folder + "\\" + fileName                                        
            extensionName = fileName.replace(".py","") 
            
            msgOverwrite = "- %-35s OVERWRITTEN, backup created on: %s" % (extensionName, bakDir + folder)
            msgNoWrite =   "- %-35s not updated. File time <= module time." % extensionName                    
            msgNewExtension =    "- %-35s CREATED." % extensionName                    
            msgNotSaved =  "- %-35s needs to be saved manually in the Extension Manager." % moduleName                    
            msgAutoSaved = "- %-35s has been automatically saved." % moduleName
                                
            fileTime = os.stat(filePath)[stat.ST_MTIME]                                        
            f = open(filePath, 'r')                                                                                                                                                                     
            extension = context.GetExtension("FPythonCode", "FObject", extensionName)                    

            #Extension exists in DB, compare file time with module time.
            if extension:                                                                                                                                                                  
                if(fileTime > adsTime):                                                                                                                  
                    #Backup DB version.
                    content = exp.TrimContent(extension.AsString(), moduleName, extensionName)
                    exp.Write(bakDir + moduleName + "\\" + fileName, content, adsTime)                                 
                    doWrite = True                                
                    print (msgOverwrite)
                    logger.info(msgOverwrite)                                                        
                else:
                    print (msgNoWrite)
                    logger.info(msgNoWrite)                
            #New extension.
            else:
                print (msgNewExtension)
                logger.info(msgNewExtension)                
                doWrite = True
            
            if doWrite:                        
                content = TrimContent(f.read(), moduleName, extensionName)                
                context.EditImport("FPythonCode", content)
        
        #Save extension module automatically if it is modified.
        if extensionModule.IsModified():
            if saveExtensionModule:
                print (msgAutoSaved)
                logger.info(msgAutoSaved)
                extensionModule.Commit()
            else:
                print (msgNotSaved)
                logger.info(msgNotSaved)                                                          
            
#--------------------------------------------------------------------------  
    
falseTrue = ['False','True']

tooltip = 'Choose the Python Modules to import'

tooltipAel = 'Export AEL Modules?'
tooltipExtModules = 'Export Extension Modules?'
tooltipSave = 'Save Extension Modules Automatically?'
tooltipImportDir = 'Directory to import Python code from'
tooltipDBBakDir = 'Directory for backup of overwritten Python code'

ael_gui_parameters = {'runButtonLabel':   '&&Import',
                      'hideExtraControls': True,
                      'windowCaption' : 'Import Python Code'}                      

def GetImportDirSelection():
    """ Directory selector dialog """
    selection = acm.FFileSelection()
    selection.PickDirectory(True)

    importDir = ext.GetExtensionValue('AEFDevTools_ImportDirectory')
    if not importDir: 
            importDir = 'C:\\export\\'
    selection.SelectedDirectory = importDir
    return selection

def GetDBBakDirSelection():
    """ Directory selector dialog """
    selection = acm.FFileSelection()
    selection.PickDirectory(True)

    bakDir = ext.GetExtensionValue('AEFDevTools_DBBackupDirectory')
    if not bakDir: 
            bakDir = 'C:\\export\\dbBakDir\\'
    selection.SelectedDirectory = bakDir
    return selection
                      

ael_variables = [                                    
    ['cbAel', 'Import AEL Modules', 'string', falseTrue, 'False', 1, 0, tooltipAel, None, 1], 
    ['cbExt', 'Import Extension Modules', 'string', falseTrue, 'False', 1, 0, tooltipExtModules, None, 1],     
    ['cbSaveExtension', 'Save Extension Modules Automatically', 'string', falseTrue, 'False', 1, 0, tooltipSave, None, 1],         
    ['importDir', 'Import Directory', GetImportDirSelection(), None, GetImportDirSelection(),
       0, 1, tooltipImportDir, None, 1],    
    ['dbBakDir', 'DB Backup Directory', GetDBBakDirSelection(), None, GetDBBakDirSelection(),
       0, 1, tooltipDBBakDir, None, 1]
    ]    
        
def ael_main(dict):
    print ('\n',60*'*','\nImport Python Code script\n')
     
    importDir = dict['importDir']
    dbBakDir = dict['dbBakDir']

    importDir = importDir.AsString()
    dbBakDir = dbBakDir.AsString()

    if not importDir.endswith('\\'):   importDir = importDir + '\\'        
    if not dbBakDir.endswith('\\'):   dbBakDir = dbBakDir + '\\'
    
    #Create import and db backup directories.        
    if not os.path.exists(importDir):     
        os.makedirs(importDir) #should exist, otherwise nothing to import.
    if not os.path.exists(dbBakDir):     
        os.makedirs(dbBakDir)
    
    #Logging.            
    logger = logging.getLogger()
    hdlr = logging.FileHandler(importDir + 'export_import.log')
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    hdlr.setFormatter(formatter)
    logger.addHandler(hdlr)
    logger.setLevel(logging.INFO)    
    logger.info(60*"-")    
    logger.info("Starting Import Python Code script")  

    #Set extension values.
    ext.SetExtensionValue('AEFDevTools_ImportDirectory',importDir)
    ext.SetExtensionValue('AEFDevTools_DBBackupDirectory',dbBakDir)
    
    if falseTrue.index(dict['cbAel']):            
        ImportModules(importDir, dbBakDir)   
    else:
        logger.info("No AEL modules imported.")
        print ("No AEL modules imported.")
         
    print ('\n' + 60*'-' + '\n')
         
    saveExtensionModule = falseTrue.index(dict['cbSaveExtension'])
    if falseTrue.index(dict['cbExt']):    
        ImportExtensionModule(importDir, dbBakDir, saveExtensionModule)   
    else:
        logger.info("No extension modules imported.")
        print ("No extension modules imported.")

    #Close logger.
    logger.removeHandler(hdlr)
    hdlr.close() 

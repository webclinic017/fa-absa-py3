from __future__ import print_function


"""----------------------------------------------------------------------------
MODULE
    FExtScannerToolGUI - GUI to run scans of the adfl code

DESCRIPTION


    (c) Copyright 2011 by SunGard FRONT ARENA. All rights reserved.

----------------------------------------------------------------------------"""
import os

import acm

import FExtScannerToolController
reload(FExtScannerToolController)

path = "c:\\extScan\\"
def createFolder():
    if not os.path.exists(path):
        print ('Creating output folder: ', path)
        os.makedirs(path)        

def createDefinitionFiles():
    import shutil
    import dircache
    
    srcPath = os.path.join(acm.GetFunction('getInstallDir', 0)(), 'VersionDefinitionsFiles')
    
    files = [file for file in dircache.opendir(srcPath )]
    
    for file in files:
        if os.path.exists(os.path.join(path, file)):
            continue
    
        srcFile = open(os.path.join(srcPath, file), 'r')
        dstFile = open(os.path.join(path, file), 'w')    
    
        shutil.copyfileobj(srcFile, dstFile)
        srcFile.close()
        dstFile.close() 
        print ('Created definition file: ', file)
        
def createMappingFile():
    ext = acm.GetDefaultContext().GetExtension('FExtensionValue', 'FObject', 'extensionAttributeMapping')            
    f = open(os.path.join(path, 'extensionAttributeMapping.csv'), 'w')
    
    f.write(ext.Value())
    f.close()
    print ('Created extension attribute mapping file: extensionAttributeMapping.csv')
    


createFolder()
createMappingFile()
createDefinitionFiles()

SCANTYPE_FIELD = 0
FROM_VER_FIELD = 1
TO_VER_FIELD = 2
CONTEXT_FIELD = 3
USERS_FIELD = 4
MODULE_FIELD = 5
FIND_REF_FIELD = 6
FIND_ACM_FIELD = 7
FIND_OVERRIDES_FIELD = 8
FIND_EQDEF_FIELD = 9
FIND_UNREF_FIELD = 10
UPGRADE_COL_FIELD = 11
PATH_FIELD = 12
REPORT_NAME_FIELD = 13
EXT_ATTR_MAP_FILE = 14

def startRunScript(eii):                
    acm.RunModuleWithParameters("FExtScannerToolGUI", acm.GetDefaultContext())  

def typeCB(index, fieldValues):

    if fieldValues[SCANTYPE_FIELD] == 'Per context':
        ael_variables[FROM_VER_FIELD][9] = True
        ael_variables[TO_VER_FIELD][9] = True
        ael_variables[CONTEXT_FIELD][9] = True
        ael_variables[USERS_FIELD][9] = True
        ael_variables[MODULE_FIELD][9] = False
        ael_variables[FIND_REF_FIELD][9] = \
            fieldValues[TO_VER_FIELD] and fieldValues[FROM_VER_FIELD] and\
            fieldValues[TO_VER_FIELD] != fieldValues[FROM_VER_FIELD]  
        ael_variables[FIND_ACM_FIELD][9] = \
            fieldValues[TO_VER_FIELD] and fieldValues[FROM_VER_FIELD] and\
            fieldValues[TO_VER_FIELD] != fieldValues[FROM_VER_FIELD]
        ael_variables[FIND_OVERRIDES_FIELD][9] = True
        ael_variables[FIND_EQDEF_FIELD][9] = True    
        ael_variables[FIND_UNREF_FIELD][9] = True
        ael_variables[UPGRADE_COL_FIELD][9] = True
        ael_variables[PATH_FIELD][9] = True
        ael_variables[REPORT_NAME_FIELD][9] = True
        ael_variables[EXT_ATTR_MAP_FILE][9] = True
    elif fieldValues[SCANTYPE_FIELD] == 'Per module':
        ael_variables[FROM_VER_FIELD][9] = True
        ael_variables[TO_VER_FIELD][9] = True
        ael_variables[CONTEXT_FIELD][9] = False
        ael_variables[USERS_FIELD][9] = False
        ael_variables[MODULE_FIELD][9] = True
        ael_variables[FIND_REF_FIELD][9] = \
            fieldValues[TO_VER_FIELD] and fieldValues[FROM_VER_FIELD] and\
            fieldValues[TO_VER_FIELD] != fieldValues[FROM_VER_FIELD] 
        ael_variables[FIND_ACM_FIELD][9] = \
            fieldValues[TO_VER_FIELD] and fieldValues[FROM_VER_FIELD] and\
            fieldValues[TO_VER_FIELD] != fieldValues[FROM_VER_FIELD]
        ael_variables[FIND_OVERRIDES_FIELD][9] = False
        ael_variables[FIND_EQDEF_FIELD][9] = True
        ael_variables[FIND_UNREF_FIELD][9] = True        
        ael_variables[UPGRADE_COL_FIELD][9] = True
        ael_variables[PATH_FIELD][9] = True
        ael_variables[REPORT_NAME_FIELD][9] = True
        ael_variables[EXT_ATTR_MAP_FILE][9] = True
    elif fieldValues[SCANTYPE_FIELD] == 'Create definition':
        ael_variables[FROM_VER_FIELD][9] = False
        ael_variables[TO_VER_FIELD][9] = False
        ael_variables[CONTEXT_FIELD][9] = False
        ael_variables[USERS_FIELD][9] = False
        ael_variables[MODULE_FIELD][9] = False
        ael_variables[FIND_REF_FIELD][9] = False        
        ael_variables[FIND_ACM_FIELD][9] = False
        ael_variables[FIND_OVERRIDES_FIELD][9] = False
        ael_variables[FIND_EQDEF_FIELD][9] = False        
        ael_variables[FIND_UNREF_FIELD][9] = False
        ael_variables[UPGRADE_COL_FIELD][9] = False
        ael_variables[PATH_FIELD][9] = True
        ael_variables[REPORT_NAME_FIELD][9] = False
        ael_variables[EXT_ATTR_MAP_FILE][9] = False
    else:
        ael_variables[FROM_VER_FIELD][9] = False
        ael_variables[TO_VER_FIELD][9] = False
        ael_variables[CONTEXT_FIELD][9] = False
        ael_variables[USERS_FIELD][9] = False
        ael_variables[MODULE_FIELD][9] = False
        ael_variables[FIND_REF_FIELD][9] = False
        ael_variables[FIND_ACM_FIELD][9] = False
        ael_variables[FIND_OVERRIDES_FIELD][9] = False
        ael_variables[FIND_EQDEF_FIELD][9] = False
        ael_variables[FIND_UNREF_FIELD][9] = False
        ael_variables[UPGRADE_COL_FIELD][9] = False
        ael_variables[PATH_FIELD][9] = False
        ael_variables[REPORT_NAME_FIELD][9] = False
        ael_variables[EXT_ATTR_MAP_FILE][9] = False
    return fieldValues



trueFalse = ['False', 'True']

def useWebserverCB(index, fieldValues):    
    ael_variables[index+1][9] = (trueFalse.index(fieldValues[index]))
    return fieldValues

versions = []
for filename in os.listdir(path):
    if filename.find("Definitions_") == 0: #If the filename starts with "Definitions_"
        versions.append(filename[len("Definitions_"):])
versions.sort()
all_contexts = acm.FExtensionContext.Select('').AsArray().Sort()
all_modules = acm.FExtensionModule.Select('').AsArray().Sort()
all_users = acm.FUser.Select('').AsArray().Sort()
ael_variables = [['scanType', 'Type of scan', 'string', ['Per context', 'Per module', 'Create definition'],\
                  'Per context', 1, 0, 'Type of scan', typeCB, 1],
                ['fromVer', 'From version', 'string',  versions, versions and versions[0] or "", 0, 0,\
                 '', typeCB, 1],
                ['toVer', 'To Version', 'string',  versions, versions and versions[-1] or "", 0, 0,\
                 '', typeCB, 1],
                ['context', 'Contexts to scan', 'FExtensionContext', all_contexts, acm.GetDefaultContext(), 0, 1, 'Context to run the scrit in', None, 1],
                ['users', 'Users to scan the context for', 'FUser', all_users, acm.UserName(), 0, 1,\
                 'Scan the contexts for the following users (leave blank to chose current user', None, 1],
                ['module', 'Modules to scan', 'FExtensionModule', all_modules, "", 0, 1, 'Module to scan', None, 1],
                ['findRef', 'Find references to extensions that will disappear', 'string', trueFalse, 'True', 1, 0, \
                 '', None, True], 
                ['findAcm', 'Find references to acm functions that will disappear or change number of operands', 'string', trueFalse, 'True', 1, 0, \
                 '', None, True],
                ['findOverrides', 'Find overrides', 'string', trueFalse, 'True', 1, 0, \
                 '', None, True],
                ['findEqDef', 'Find equal extension defintions', 'string', trueFalse, 'True', 1, 0, \
                 '', None, True],                
                ['findUnref', 'Find unreferenced code', 'string', trueFalse, 'True', 1, 0, \
                 '', None, True],
                ['upgradeCol', 'Upgrade ColumnDefinitions', 'string', trueFalse, 'True', 1, 0, \
                 '', None, True],
                ['path', 'Path to definitions', 'string',  [], path, 0, 0,\
                 'The path to the definition files', None, 0],
                ['reportName', 'Report name', 'string',  [], path+"ExtensionScanReport.html", 0, 0,\
                 'The name of the report that will be created', None, 1],
                 ['extAttrMapFile', 'Extension Attribute Map File', 'string',  [], path+"extensionAttributeMapping.csv", 0, 0,\
                 'File containing mapping for extension attributes which have changed names between versions.', None, 1],
                 ['useWebserver', 'Use webserver', 'string', trueFalse, 'True', 1, 0, \
                 '', useWebserverCB, True],
                 ['serverAddress', 'Webserver address', 'string',  [], 'http://localhost:8080', 0, 0,\
                 'Webserver address', None, 0],
                 
                 ]
                 
def ael_main(ael_vars):
       
    
    reportName = \
        FExtScannerToolController.start_scans(ael_vars['scanType'], ael_vars['fromVer'], ael_vars['toVer'],\
                ael_vars['context'], ael_vars['users'], ael_vars['module'], ael_vars['findRef'],\
                ael_vars['findAcm'], ael_vars['findOverrides'], ael_vars['findEqDef'], ael_vars['findUnref'],\
                ael_vars['upgradeCol'], ael_vars['path'], ael_vars['reportName'], ael_vars['extAttrMapFile'])
    
    
    if reportName:        
        if trueFalse.index(ael_vars['useWebserver']):
            import FExtScannerWebserver
            FExtScannerWebserver.start_webserver(ael_vars['serverAddress']+"\\LocalFiles/" + reportName, path)
        else:
            import webbrowser
            webbrowser.open(reportName)



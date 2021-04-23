from __future__ import print_function
'''
Created on 5 nov 2014

DESCRIPTION
    This tool allows you to import source controlled python code into an ADS with just one click
    in the Extension Manager of Prime.
    It assumes you are using the gen_aelimportfile method for building xmr out of python files.
    The result is an inserted "baseName_username" module in you context.
    Python modules are also reloaded for your convenience.
    
    Usage: Open extension manager, select a built-in module and then press Py2Prime ribbon. 

@author: AM Dev team
'''
import acm
import sys
import os
import re
try:
    from FUxCore import MenuItem
except ImportError:
    print ("Cannot import FUxCore, assuming test run and mocking MenuItem")
    MenuItem = object


basedir = os.getcwd()
acmBundleRelativePath = r'TM_FObject\Components\Initialization\CompleteAcm\CompleteAcmBundle.cpp'
cmakeListRelativePath = r'TM_FObject\Components\Initialization\CompleteAcm\CMakeLists.txt'

headerTemplateString = '_py'
headerFileSuffix = '_header.txt'
addToCompoundModuleFunction = "AddToCompoundModule"

autoModules = {}

def Py2PrimeButton(eii):
    return Py2PrimeMenuItem(eii)

class Py2PrimeMenuItem(MenuItem):
    def __init__(self, extObj):
        global autoModules
        autoModules = FindAutoBuiltPythonModules()
        self._frame = extObj

    def Enabled(self):
        global autoModules
        return self._frame.ActiveModule().Name() in autoModules

    def Invoke(self, eii):
        Run(eii.ExtensionObject().ActiveModule().Name())

class AutoBuiltPyhtonModules():
    relativeFoldPath = ""
    pythonModuleName = ""
    baseName = ""
    defFilePath = ""
    compoundModuleName = ""
    
    def __init__(self, relativeFoldPath):
        self.relativeFoldPath = os.path.normpath(relativeFoldPath)

        cmakeRelPath = os.path.join(self.relativeFoldPath, "import.cmake")
        with _GetFileHandlerFromRepository(cmakeRelPath) as importCmake:
            for cmakeline in importCmake:
                if "BASENAME" in cmakeline:
                    self.baseName = cmakeline.split()[-1].split(")")[-2]
                if "DEFFILE" in cmakeline:
                    self.defFilePath = os.path.normpath(cmakeline.split()[-1].split(")")[-2])
                
        headerPath = os.path.join(self.relativeFoldPath, self.baseName+"_header.txt")
        with _GetFileHandlerFromRepository(headerPath) as header:
            for headerline in header:
                if headerline.startswith("name"):
                    self.pythonModuleName = headerline.split('"')[-2]
                    break
            else:
                raise RuntimeError('%s does not include a "name" parameter!'%headerPath)
 
        with _GetFileHandlerFromRepository(acmBundleRelativePath) as bundleFile:
            for line in bundleFile:
                if self.pythonModuleName in line and addToCompoundModuleFunction in line:
                    self.compoundModuleName = line.split(addToCompoundModuleFunction)[1].split('"')[1]
                    break

def FindAutoBuiltPythonModules():
    modules = {}
    searchString = r"CMAKE_SOURCE_DIR"
    with _GetFileHandlerFromRepository(cmakeListRelativePath) as cmakeList:
        for line in cmakeList:
            if searchString in line:
                relativeFolderPath = line.split(searchString)[1].split(")")[0].strip("}//) (\n")
                mod = AutoBuiltPyhtonModules(relativeFolderPath)
                if mod.compoundModuleName:
                    modules[str(mod.compoundModuleName)] = mod
    return modules

def Run(moduleName):
    global autoModules
    try:
        print ("-------- Py2Prime upload started. Target module is '%s' --------"%moduleName)
        module = autoModules[moduleName]
        defFile = os.path.join(basedir, module.relativeFoldPath, module.defFilePath)
        Import(defFilePath = defFile, baseName=module.baseName)

    except StandardError as e:
        print ("Sorry, Py2Prime failed because...")
        print (e)

def _GetFileHandlerFromRepository(relativePath):
    try:
        return open(os.path.join(basedir, relativePath))
    except IOError:
        print ("Cannot find %s in your repository" % os.path.basename(relativePath))
        print ("Please set your working directory to the base folder in your repository.")
        print ("In case you are using PrimeStarterDeluxe you find this under Tools/Settings.")
        print ("Current working directory is %s" % basedir)
        raise RuntimeError("Set working directory to the base folder. See log.")
                                

def Import(defFilePath, baseName, context = None, server = None, 
           user = None, password = None, makeXMR = False):
    
    if not acm.IsConnected():
        acm.Connect(server, user, password, None)  
    
    context = context or str(acm.GetDefaultContext().Name())
    txt_file_path = os.path.normpath(_GenerateCompoundXMR(defFilePath, baseName, True))
    extMod = ImportModule(context, txt_file_path)
    count = ReloadPythonModules(extMod)    
    print ("Done synchronizing context with %i python files."%count)
    print ('Re-select context if you can not see new module %s'%extMod)
    if makeXMR:
        moduleDir = os.path.join(basedir, r'TM_FObject\Financial\Modules')
        if os.path.exists(moduleDir):
            print ("Py2Prime: Also saving a fresh XMR for possible promotion.\n")
            _GenerateCompoundXMR(defFilePath, baseName, False, moduleDir)
        else:
            print ("Could not find folder %s to put the XMR in."%moduleDir)

def _GenerateCompoundXMR(defFilePath, baseName, buildTxt, outputFilePath = False):
    outputFilePath = os.path.normpath(outputFilePath or os.path.dirname(defFilePath))
    
    #if not outputFilePath.endswith("\\"):
    #    outputFilePath += "\\"
    sys.path.append(os.path.join(basedir, r'buildutil\etc'))
    os.chdir(os.path.dirname(defFilePath))
    oldargs = sys.argv[:]
    N = 'NONE'
    sys.argv = [N, outputFilePath, N, N, N, N, baseName, defFilePath, N, N, N, '1' if buildTxt else N, N, N, N, N, N]

    try:
        if 'gen_aelimportfile' in sys.modules:
            import gen_aelimportfile 
            reload(gen_aelimportfile) #@UndefinedVariable
        else:
            import gen_aelimportfile 
    except ImportError:
        print ("Cannot import gen_aelimportfile.")
        print ("It is normally found in ...base\\buildutil\\etc")
        raise
    except StandardError as e:
        print ("Failed to generate xmr using gen_aelimportfile")
        print ("Path to def file:", defFilePath)
        print ("Base name:", baseName)
        print ("Error thrown is:", e)
    finally: 
        sys.argv = oldargs[:]
        os.chdir(basedir)
        
    assert gen_aelimportfile.import_file
    return gen_aelimportfile.import_file

def ImportModule(contextName, filepath):
    tmpFile = open(filepath, 'r')
    mod = acm.FExtensionModule(tmpFile.read())
    tmpFile.close()
    
    name = mod.Name()
    nameParts = name.split('_')
    name = acm.UserName()+'_'+''.join(nameParts[:-1])
    mod.Name(name)
    
    old = acm.FExtensionModule[name]
    if old:
        old.Delete()
    #mod.Inspect()
    mod.Commit()
    
    ctxt = acm.FExtensionContext[contextName]
    ctxt.AddModule(mod)
    ctxt.Commit()
    print ("Imported module", mod.Name(), "from")
    print (filepath, "into context", ctxt.Name())
    return mod.Name()

def _FixImport(imp):
    return (imp.split(' as ')[0] if imp.find(' as ') else imp).strip()
    
def _GetImportsFromPythonModule(pyExt):
    expr = re.compile(r'^\s*(?:import\s+(.+))|(?:from\s+(\w+)\s+import.+)\s*$', re.MULTILINE)
    imps = []
    lines = expr.findall(pyExt.Value())
    for l in lines:
        if len(l[0]):
            imps.extend([_FixImport(_i) for _i in l[0].split(',')])
        else:
            imps.append(l[1].strip())
    return imps

class _ModuleReloader(object):
    def __init__(self):
        self._dependencies = dict()
        self._reloaded = set()
        self._externalMods = set()
    
    def AddDependencies(self, modName, deps):
        self._dependencies[modName] = deps
    
    def Reload(self, modName=''):
        if modName == '':
            for key in self._dependencies.keys():
                self.Reload(key)
            #print ("External dependencies: ", self._externalMods)
        else:
            if (modName in self._dependencies) and (not modName in self._reloaded):
                self._reloaded.add(modName)
                # print ("Reloading ", modName, " after ", self._dependencies[modName])
                for subMod in self._dependencies[modName]:
                    self.Reload(subMod)
                try:
                    mod = __import__(modName)
                    reload (mod)
                    #print ("Reloaded ", modName)
                except Exception as e:
                    print ('Failed to import/reload module "%s" - %s: %s' % (modName, e.__class__.__name__, str(e)))
            else:
                if not modName in self._dependencies:
                    self._externalMods.add(modName)
            

def ReloadPythonModules(extModName):
    try:
        extMod = acm.FExtensionModule[extModName]
        """ Import and reload all custom python modules in the context. """
        if not extMod:
            print ("No module!")
        reloadCount = 0;
        reloader = _ModuleReloader()
        for m in extMod.GetAllExtensions(acm.FPythonCode):
            pythonModule = str(m.Name())
            try:
                imps = _GetImportsFromPythonModule(m)
                reloader.AddDependencies(pythonModule, imps)
                #print (pythonModule, ' : ', imps)
                reloadCount += 1
            except Exception as e:
                print ('Unable to import/reload module "%s::%s" - %s: %s' % \
                    (extModName, pythonModule, e.__class__.__name__, str(e)))
        reloader.Reload()
        print ('Reloaded %i python module(s) in %s' % (reloadCount, extModName))
        return reloadCount
    except StandardError as stderr:
        print ("Exception: %s" % stderr)
        return 0


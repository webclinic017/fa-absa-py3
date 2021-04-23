from __future__ import print_function
import acm
import ael
import itertools
import re
import sys
import traceback
import types
import io

try:
    reload
except NameError: #Python3
    from importlib import reload

def OrderModulesOnDependancy(moduleNames, deps):
    allModuleNames = set(sys.modules.keys())
    res = []
    changed = True
    # handle known cyclical imports
    resolved = set(
        ["sys", "os", "win32com", "docutils", "FBDPString", "decimal", "_internal_site_setup", "calendar", "__future__", "locale", "re", "logging", "types", "string", "traceback", "threading", "zipfile", "webbrowser", "inspect", "linecache", "platform"])
    while allModuleNames and changed:
        changed = False
        for modname in list(allModuleNames - resolved):
            # no dependecise we can load it
            if not deps.get(modname, set()) - resolved:
                resolved.add(modname)
                if modname in moduleNames:
                    res.append(modname)
                changed = True
    failed_modules = set(moduleNames) & (allModuleNames - resolved)
    if failed_modules:
        print ("Cyclical module import detected, remaining modules " + str(failed_modules))
        for modname in failed_modules:
            print ("** ", modname)
            print (deps[modname] - resolved)
    return res
    
def GetModuleImportsFromFile(module):
    moduleImports = set()
    if hasattr(module, '__file__'):
        contextPath = '[%s]/' % acm.GetDefaultContext().Name()
        if module.__file__ and module.__file__.startswith(contextPath):
            moduleName = module.__file__.replace(contextPath, '', 1)
            code = acm.GetDefaultContext().GetExtension('FPythonCode', 'FObject', moduleName)
            if not code:
                code = acm.FAel[moduleName]
            if code:
                code = code.AsString()
        elif module.__name__ == module.__file__ and acm.FAel[module.__name__]:
            code = acm.FAel[module.__name__].AsString()
        else:
            try:
                file = module.__file__
                if file.endswith('.pyc'):
                    file = file[:-1]
                with io.open(file, 'r', encoding="iso8859-1") as f:
                    code = f.read() 
            except Exception as e:
                print ('failed to open file for', e, module)
                return moduleImports

        if code:
            for imports in re.findall('^import[\t ]+([a-zA-Z_][\w \t,.]*)$', code, re.MULTILINE):
                for imp in imports.split(','):
                    moduleImports.add(re.split('[ .]', imp.strip())[0])

            moduleImports.update(re.findall('^from[\t ]+([a-zA-Z_]\w*)[\t ]+import[\t ]+\S.*$', code, re.MULTILINE))
        
    return moduleImports
    
def BuildDependentModules(moduleName, rev_graph, dependents):
    dependents.add(moduleName)
    for dependent in rev_graph[moduleName]:
            if dependent not in dependents:
                    BuildDependentModules(dependent, rev_graph, dependents)
                    
def RreverseGraph(graph):
    """ {a: set(b, c) -> {b:set(a), c: set(a)}"""
    res = dict((t, set()) for t in
               set(graph.keys()) | set(itertools.chain.from_iterable(graph.values())))
    for mod, dependencies in graph.items():
        for dependent in dependencies:
            res[dependent].add(mod)
    return res
    
def ValidModuleToLoad(moduleName):
    return moduleName not in ['_internal_site_setup']
    
def LoadedModuleDependencies():
    """Build {modname->set( dependent module names) for all loaded modules)"""
    deps = dict((moduleName, set()) for moduleName in sys.modules.keys())
    for moduleName, module in list(sys.modules.items()):
        if ValidModuleToLoad(moduleName):
            for import_module in GetModuleImportsFromFile(module):
                if not import_module:
                    print ('Error in parsing imports in', module)
                if import_module and import_module in sys.modules:
                    deps[moduleName].add(import_module)
    return deps
    
def ReloadLoadedModules(changedModuleNames, doPrint, excludeInReload, OnModuleReloadedCB = None):
    # Make sure all edited modules are loaded
    for moduleName in changedModuleNames:
        __import__(moduleName)
    # Reload in dependancy order
    deps = LoadedModuleDependencies()
    need_reload = set()
    rev_graph = RreverseGraph(deps)
    for moduleName in changedModuleNames:
        BuildDependentModules(moduleName, rev_graph, need_reload)
    res = []
    for moduleName in OrderModulesOnDependancy(need_reload, deps):
        if moduleName in excludeInReload:
            continue
        try:
            mod = __import__(moduleName)
            reload(mod)
        except ImportError:
            print ('Failed to import module', moduleName)
            continue
        except TypeError:
            import traceback
            traceback.print_exc()
            continue
        except Exception:
            print ('Import failed of module', moduleName)
            import traceback
            traceback.print_exc()
            continue
        if doPrint:
            print ('reloaded', moduleName)
            
        if OnModuleReloadedCB :
            OnModuleReloadedCB(moduleName)
            
        res.append(mod)
    return res


def ReloadLoadedModulesFromExtensionModule(extensionModuleNames, doPrint, excludeInReload, OnModuleReloadedCB = None):
    moduleNames = []
    for extensionModuleName in extensionModuleNames:
        extensionModule = acm.GetDefaultContext().GetModule(extensionModuleName) or acm.FExtensionModule[extensionModuleName]
        if not extensionModule:
            print ('No extension module named', extensionModuleName)
            return
        moduleNames += [str(mod.Name()) for mod in extensionModule.GetAllExtensions('FPythonCode') if str(mod.Name()) in sys.modules]
        
    ReloadLoadedModules(moduleNames, doPrint, excludeInReload, OnModuleReloadedCB)

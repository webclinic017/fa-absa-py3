from __future__ import print_function

"""----------------------------------------------------------------------------
MODULE
    FExtensionAttributeOverride - Scans the adfl code and reports all overrides
    and extension attributes that are defined in more than on module.

DESCRIPTION


    (c) Copyright 2011 by SunGard FRONT ARENA. All rights reserved.

----------------------------------------------------------------------------"""

import datetime
import sets

import acm

import FExtensionUtils
from FHTML import *

reload(FExtensionUtils)

class SortByNameAndModuleLevel:
    def __init__(self, modules):
        self.modules = modules
    def comp(self, first, second):
        def comptuple(ext):
            return (ext.extension_name.upper(), self.modules[ext.module_name].moduleLevel, ext.class_name)
        return cmp(comptuple(first), comptuple(second))

def write_report(fname, overrides, eaDiffMod, description, mods):    
    """Produce HTML report of the overrides in the context"""
    
    res = ["""<html><head><title> Overrided extension attributes %s
                </title></head><body bgcolor=ffffff>""" % (description,)]               
    res.append("""<h1>Overrides %s</h1>""" % (description,) )
    res.append("""Produced on: %s<p>""" % (str(datetime.datetime.now())[0:19],) )
    res.append("""By user: %s<p>""" % (acm.UserName(),) )
    res.append("""ADS: %s<p>""" % (acm.ADSAddress(),) )
    res.append("""<b>The following ExtensionAttributes are overrided.</b><p>""")
    res.append(h2("(total = %d)"% (len(overrides) )))
    
    
    modules=sets.Set([ext.module_name for ext in overrides])
    overrides.sort(SortByNameAndModuleLevel(mods).comp)
    eaDiffMod.sort(SortByNameAndModuleLevel(mods).comp)
    
    dummy_context = acm.FExtensionContext()
    for mod in mods.moduleNames():
        if mod in modules:
            dummy_context.AddModule(mod)
            res.append(h3("[" + mod + "]"+ str(dummy_context.Modules()[-1].IsBuiltIn() and " (Built in module)" or "")))
            dummy_context.RemoveModule(mod)
            previous_name = ""
            for ext in overrides:
                if ext.module_name == mod and ext.extension_name != previous_name:
                    res.append(ref(ext.extension_name, ext.extension_name + "OR") + ", ")
                    previous_name = ext.extension_name
    
    if len(eaDiffMod):
        modules=sets.Set([ext.module_name for ext in eaDiffMod])
        res.append("""<BR><BR><b>The following ExtensionAttributes don't override 
                    each other but are defined in more than one module.</b><p>""")
        for mod in mods.moduleNames():
            if mod in modules:
                dummy_context.AddModule(mod)
                res.append(h3("[" + mod + "]"+ str(dummy_context.Modules()[-1].IsBuiltIn() and " (Built in module)" or "")))
                dummy_context.RemoveModule(mod)
                previous_name = ""
                for ext in eaDiffMod:
                    if ext.module_name == mod and ext.extension_name != previous_name:
                        res.append(ref(ext.extension_name) + ", ")
                        previous_name = ext.extension_name
    
    
    previous_name = ""
    for ext in overrides:
        if ext.extension_name != previous_name:
            res.append("<HR>")
            res.append(h3(anchor(ext.extension_name, ext.extension_name + "OR")) )
        
        res.append(ext.create_definition())
        res.append(";<BR>")
        previous_name = ext.extension_name
        
        
    if len(eaDiffMod): res.append("<BR><HR><HR>")
    
    previous_name = ""
    for ext in eaDiffMod:
        if ext.extension_name != previous_name:
            res.append("<HR>")
            res.append(h3(anchor(ext.extension_name)) )
        
        res.append(ext.create_definition())
        res.append(";<BR>")
        previous_name = ext.extension_name
    
    res.append("""</body>""")
    outfile = open(fname, 'w')
    outfile.write("".join(res))


def comp_ind_by_modLevel(extattrs, mods):
    res = {}   
    for ext in extattrs:
        res.setdefault(mods[ext.module_name].moduleLevel, []).append(ext)
    return res


def get_overrides(nonBuiltInMods, builtInModules, modules):
    nonBuiltInClasses = [sets.Set(mod.keys()) for mod in nonBuiltInMods]
    builtInClasses = [sets.Set(mod.keys()) for mod in builtInModules]
    nonBuiltInClassesNoOverrides = [sets.Set(mod.keys()) for mod in nonBuiltInMods]
    overrides = sets.Set()
    
    for i, module in enumerate(nonBuiltInClasses):
        for klass in module:
            if i+1 < len(nonBuiltInClasses):
                for j, mod in enumerate(nonBuiltInClasses[i+1:]):
                    for klass2 in mod:
                        if (getattr(acm, klass).IncludesBehavior(klass2) or\
                            getattr(acm, klass2).IncludesBehavior(klass)) and\
                            nonBuiltInMods[i][klass][0].module_name in\
                            modules[nonBuiltInMods[j+i+1][klass2][0].module_name].ModulesInContext():
                            if klass in nonBuiltInClassesNoOverrides[i]:
                                nonBuiltInClassesNoOverrides[i].remove(klass)
                            if klass2 in nonBuiltInClassesNoOverrides[j+i+1]:
                                nonBuiltInClassesNoOverrides[j+i+1].remove(klass2)
                            overrides.union_update(nonBuiltInMods[i][klass])
                            overrides.union_update(nonBuiltInMods[j+i+1][klass2])
            for j, mod in enumerate(builtInClasses):
                for klass2 in mod:
                    if getattr(acm, klass).IncludesBehavior(klass2) or\
                            getattr(acm, klass2).IncludesBehavior(klass):
                        if klass in nonBuiltInClassesNoOverrides[i]:
                            nonBuiltInClassesNoOverrides[i].remove(klass)
                        overrides.union_update(nonBuiltInMods[i][klass])
                        overrides.union_update(builtInModules[j][klass2])
    
    if len(nonBuiltInClassesNoOverrides)>=2:
        for mod in nonBuiltInClassesNoOverrides:
            if len(mod):
                return overrides, sets.Set(FExtensionUtils.flatten(\
                        [module.values() for module in nonBuiltInMods]))
    return overrides, sets.Set()
    
    


def find_overrides(modules):
    #Get all extension attributes
    extensionAttributes=FExtensionUtils.get_extension_in_module(modules)
    
    if not extensionAttributes: 
        print ("No extension attributes in modules")
        return [], []

    extByName = FExtensionUtils.create_composit_index(FExtensionUtils.flatten(extensionAttributes), "extension_name").values()
    extByNameAndModule = [comp_ind_by_modLevel(exts, modules) for exts in extByName]
    extByNameModuleAndClass = [[FExtensionUtils.create_composit_index(exts, "class_name") for exts in extByModule.values()]\
                                for extByModule in extByNameAndModule]
    
    overrides, eaDiffMod = sets.Set(), sets.Set()
    for extNameByModuleAndClass in extByNameModuleAndClass:
        if len(extNameByModuleAndClass)>=2:
            builtInModules = []
            nonBuiltInMods = []
            for ext in extNameByModuleAndClass:
                if modules[ext.values()[0][0].module_name].IsBuiltIn():
                    builtInModules.append(ext)
                else: nonBuiltInMods.append(ext)
            if nonBuiltInMods:
                over, eaDiff = get_overrides(nonBuiltInMods, builtInModules, modules)
                overrides |= over
                eaDiffMod |= eaDiff
        
    return list(overrides), list(eaDiffMod)

def scan_contexts_and_report(context, users, reportname, write_summary_report):
    res = [h3("Overrides")]
    totalCountOR, totalCountEA = 0, 0
    updates=sets.Set()
    updates1=sets.Set()
    allmodules = FExtensionUtils.moduleDict()
    for cont in context:
        print ("Scanning context", cont.StringKey(), "for overrides")
        if write_summary_report:
            report = reportname + "_files\\Overrides_" + cont.StringKey() + ".html"
            report_link = reportname[reportname.rfind("\\")+1:] + "_files\\Overrides_" + cont.StringKey() + ".html"
        else:
            report = reportname + "_Overrides_" + cont.StringKey() + ".html"
            report_link = report
        modules = FExtensionUtils.get_modules(users, cont)
        overrides, eaDiffMod = find_overrides(modules)
        allmodules.update(modules)
        updates.union_update(overrides)
        updates1.union_update(eaDiffMod)
        if len(overrides) or len(eaDiffMod):
            totalCountOR += len(overrides)
            totalCountEA += len(eaDiffMod)
            write_report(report, overrides, eaDiffMod, "in context " + cont.StringKey(), modules)
            res.append(str(len(overrides)))
            res.append("<small> (")
            res.append(str(len(updates)))
            res.append(") </small>overrides") 
            if len(eaDiffMod):
                if len(overrides): res.append(" and ")
                res.append(str(len(eaDiffMod)))
                res.append("<small> (")
                res.append(str(len(updates1)))
                res.append(") </small>definitions in different modules")
            res.append(" found in context ")
            res.append(html_link(cont.StringKey(), report_link))
            res.append('<BR>')
    if not totalCountOR and not totalCountEA:
        if write_summary_report:
            res.append("No overrides found in the scanned contexts<BR>")
        else:
            print ("No overrides found in context", context[0].StringKey())
            return None
    elif write_summary_report:
        report = reportname + "_files\\Overrides.html"
        report_link = reportname[reportname.rfind("\\")+1:] + "_files\\Overrides.html"
        write_report(report, list(updates), list(updates1), "in scanned contexts", allmodules)
        res.append("Total ")
        res.append(str(totalCountOR))
        res.append("<small> (")
        res.append(html_link_noUL(str(len(updates)) + " unique", report_link))
        res.append(") </small>overrides")
        if totalCountEA:
            if totalCountOR: res.append(" and ")
            res.append(str(totalCountEA))
            res.append("<small> (")
            res.append(html_link_noUL(str(len(updates1)) + " unique", report_link))
            res.append(") </small>definitions in different modules<BR>")
    else:
        return report
    return "".join(res)






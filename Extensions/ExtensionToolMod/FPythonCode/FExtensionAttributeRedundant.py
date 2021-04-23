


"""----------------------------------------------------------------------------
MODULE
    FExtensionAttributeRedundant - Finds extension attributes with equal def

DESCRIPTION


    (c) Copyright 2011 by SunGard FRONT ARENA. All rights reserved.

----------------------------------------------------------------------------"""

import os
import datetime
import sets

import acm

import FExtensionUtils
from FHTML import *

def write_report(fname, idDefs, eqDefs, description, modules):    
    """Produce HTML report of equal extension attribute definitions"""
    
    idDefs.sort(lambda a, b: cmp((a.code, modules[a.module_name].moduleLevel, a), (b.code, modules[b.module_name].moduleLevel, b)))
    eqDefs.sort(lambda a, b: cmp((a.code, modules[a.module_name].moduleLevel, a), (b.code, modules[b.module_name].moduleLevel, b)))
    eqExt = idDefs + eqDefs
    modulesWithEqExt=sets.Set([ext.module_name for ext in eqExt])
    
    res = ["""<html><head><title> Equal extension attribute definitions %s
                </title></head><body bgcolor=ffffff>""" % (description,)]               
    res.append("""<h1>Equal extension attrubute definitions %s</h1>""" % (description,) )
    res.append("""Produced on: %s<p>""" % (str(datetime.datetime.now())[0:19],) )
    res.append("""By user: %s<p>""" % (acm.UserName(),) )
    res.append("""ADS: %s<p>""" % (acm.ADSAddress(),) )
    res.append("""<b>The following extension attributes are identically defined as another extension attribute, this may indicate redundant code or a copy-paste error.</b><p>""")
    res.append(h2("(total = %d)"% (len(eqDefs)+ len(idDefs) )))     
    res.append("\n<!--definitionsList:")
    for ext in eqExt:
        res.append(ext.code+"\xa4")
    res.append("-->\n") 
    
    for module in modules.moduleNames():
        if module in modulesWithEqExt:
            res.append("\n<!--moduleHeader:-->"+h3("[" + module + "]"+ str(modules[module].IsBuiltIn() and " (Built in module)" or "")))
            previous_name = ""
            for ext in eqExt:
                if ext.module_name == module and ext.extension_name != previous_name:
                    #Comment used by webserver in order to exclude links to definitions from report.
                    res.append("\n<!--definition:"+ext.code+"-->\n")
                    res.append(ref(ext.extension_name) + ", ")
                    previous_name = ext.extension_name
                    
    res.append('\n<!--msg-->\n')
    takenCareOf = 0
    for i, ext in enumerate(eqExt):
        if not takenCareOf:
            #Comment used by webserver in order to exclude definitions from report.
            res.append("\n<!--definition:"+ext.code+"-->\n")
            res.append("<HR>")
            #Comment used by webserver in order place buttons for exclusion of definitions.
            res.append('\n<!--button-->\n')            
            res.append("<H3>")
            res.append(anchor(ext.extension_name)) 
            headerList = False
            while i + takenCareOf + 2 <= len(eqExt):
                if ext.extension_name == eqExt[i+takenCareOf+1].extension_name:
                    takenCareOf += 1
                elif ext.code == eqExt[i+takenCareOf+1].code:
                    if res[-1] != eqExt[i+takenCareOf+1].extension_name:
                        headerList = True
                        res.append(", ")
                        res.append(anchor(eqExt[i+takenCareOf+1].extension_name))
                    takenCareOf += 1
                else:
                    break
            if headerList:
                res[-2] = " and "
                res.append(" are identically defined, possible redundant code</H3>")
            else:
                res.append(" is identically defined in different modules, possible redundant code</H3>")
        else:
            takenCareOf -= 1
            
        res.append(ext.create_definition())
        res.append(";<BR>")
        if takenCareOf and ext.extension_name != eqExt[i+1].extension_name:
            res.append("<BR>")
        
    
    res.append("""</body>""")
    outfile = open(fname, 'w')
    outfile.write("".join(res))

def is_all_built_in(ext_list, modules):
    ext_mods = sets.Set([ext.module_name for ext in ext_list])
    if ext_mods - sets.Set(modules.builtInModules().modules()):
        return False
    return True

def is_all_same_module_level(extList, modules):
    moduleLevel = modules[extList[0].module_name].moduleLevel
    for ext in extList[1:]:
        if moduleLevel != modules[ext.module_name].moduleLevel:
            return False
    return True
    
def find_eqdef(modules, scanType):
    #Get all extension attributes
    extensionAttributes=FExtensionUtils.get_extension_in_module(modules)
    
    idDefs, eqDefs = [], []
    for item in FExtensionUtils.create_composit_index(extensionAttributes, "class_name code").items():
    
        if scanType == 'context':
            checkSameModuleLevel = is_all_same_module_level(item[1], modules)
        else:
            checkSameModuleLevel = False

        if len(item[1])>1 and not is_all_built_in(item[1], modules)\
                    and not checkSameModuleLevel:            
            if len(sets.Set([ext.extension_name for ext in item[1]])) < len(item[1]):
                idDefs.extend(item[1])
            else:
                eqDefs.extend(item[1])
        # if more than one extension attribute has the same definition        
        # and not all attributes are on the same module level (e.g. two user modules define an attribute equally)
        # and not all extension attributes belongs to built in modules
        # if two or more defintions have the same name, add to idDefs, else, add to eqDefs
    return idDefs, eqDefs

def scan_contexts_and_report(context, users, reportname, write_summary_report):
    res = [h3("Extension attributes with equal definitions")]
    totalcount = 0
    updates=sets.Set()
    updates1=sets.Set()
    allmodules = FExtensionUtils.moduleDict()
    for cont in context:
        print ("Scanning context", cont.StringKey(), "for equal extension attribute definitions")
        if write_summary_report:
            report = reportname + "_files\\EqDef_" + cont.StringKey() + ".html"
            report_link = reportname[reportname.rfind("\\")+1:] + "_files\\EqDef_" + cont.StringKey() + ".html"
        else:
            report = reportname + "_EqDef_" + cont.StringKey() + ".html"
            report_link = report
        modules = FExtensionUtils.get_modules(users, cont)
        idDef, eqDef = find_eqdef(modules, 'context')
        allmodules.update(modules)
        updates.union_update(eqDef)
        updates1.union_update(idDef)
        if len(eqDef)+ len(idDef):
            totalcount += len(FExtensionUtils.flatten(eqDef))+ len(FExtensionUtils.flatten(idDef))
            write_report(report, idDef, eqDef, "in context " + cont.StringKey(), modules)
            res.append(str(len(eqDef)+ len(idDef)))
            res.append("<small> (")
            res.append(str(len(updates | updates1)))
            res.append(") </small>extension attributes with equal definitions in context ")
            res.append(html_link(cont.StringKey(), report_link))
            res.append('<BR>')
    if not totalcount:
        if write_summary_report:
            res.append("No extension attributes with equal definitions found in the scanned contexts<BR>")
        else:
            print ("No extension attributes with equal definitions found in context", context[0].StringKey())
            return None
    elif write_summary_report:
        #Adding "/" instead of "\\" in order for it to work with the webserver
        report = reportname + "_files/EqDef.html"
        report_link = reportname[reportname.rfind("\\")+1:] + "_files/EqDef.html"
        write_report(report, list(updates1), list(updates), "in scanned contexts", allmodules)
        res.append("Total ")
        res.append(str(totalcount))
        res.append("<small> (")
        res.append(html_link_noUL(str(len(updates | updates1)) + " unique", report_link))
        res.append(") </small>equal extension attributes<BR>")
    else:
        return report
    return "".join(res)

def scan_modules_and_report(module, reportname, write_summary_report):
    print ("Scanning modules for extension attributes with equal definitions...")
    if write_summary_report:
        report = reportname + "_files\\EqDef_in_modules.html"
        report_link = reportname[reportname.rfind("\\")+1:] + "_files\\EqDef_in_modules.html"
    else:
        report = reportname + "_EqDef_in_modules.html"
        report_link = reportname[reportname.rfind("\\")+1:] + "_EqDef_in_modules.html"
    modules = FExtensionUtils.get_moduleDict(module)
    idDef, eqDef = find_eqdef(modules, 'module')
    if len(eqDef):
        write_report(report, idDef, eqDef, "in modules " + module.StringKey(), modules)
        res = [str(len(eqDef) + len(idDef))]
        res.append(" extension attributes with equal definitions in the ")
        res.append(html_link("scanned modules", report_link))
        res.append('<BR>')
        res = "".join(res)
        if not write_summary_report:
            res = report
    else:
        if write_summary_report:
            res = "No extension attributes with equal definitions found in the scanned modules<BR>"
        else:
            res = None
            print ("No extension attributes with equal definitions found in the scanned modules")
    return res






from __future__ import print_function


"""----------------------------------------------------------------------------
MODULE
    FAcmMethodsRemoved - Find extension attributes defined with removed or
    changed ACM methods

DESCRIPTION


    (c) Copyright 2011 by SunGard FRONT ARENA. All rights reserved.

----------------------------------------------------------------------------"""

import datetime
import sets

import acm

import FExtensionUtils
from FHTML import *


def printOperandInfo(acm_methods, meta_data):
    def print_list(op_list):
        ret=[op_list[0]]
        for i, op in enumerate(op_list[1:]):
            if i == len(op_list[1:]) - 1:
                ret.append(" or ")
            else:
                ret.append(", ")
            ret.append(op)
        return ("".join(ret))
    
    if not acm_methods:
        return ""
        
    res = []
    for changed_method in acm_methods:
        removed_operands, common_operands, new_operands \
            = meta_data.changedAcmMethodOperands[changed_method]
        res.append(changed_method)
        res.append(" doesn't take ")
        
        res.append(print_list(removed_operands))
        
        res.append(" operand")
        if len(removed_operands)>1 or removed_operands[0] != '1':
                res.append("s")
        res.append(" anymore, ")
        if common_operands:
            res.append("but it still takes ")
            res.append(print_list(common_operands))
            res.append(" operand")
            if len(common_operands)>1 or common_operands[0] != '1':
                res.append("s")
            res.append(". Valid")
        else:
            res.append("valid")
        res.append(" number of operands are ")
        res.append(print_list(new_operands))
        res.append("<BR>")
    return ("".join(res))

def write_report(fname, ext_def, acm_met, meta_data, description, modules, python_report = False):    
    """Produce HTML report of the changed colmn defintions"""

    res = ["""<html><head><title> Found removed ACM methods
                </title></head><body bgcolor=ffffff>"""]               
    res.append("""<h1>Found removed ACM methods %s</h1>""" % (description,) )
    res.append("""Produced on: %s<p>""" % (str(datetime.datetime.now())[0:19],) )
    res.append("""By user: %s<p>""" % (acm.UserName(),) )
    res.append("""ADS: %s<p>""" % (acm.ADSAddress(),) )
    
    # ext_def and acm_met are lists of tuples:
    # [(ExtAttr1, Set(RemovedAcmMethod1,2.....)),(ExtAttr2,Set(......)),...]
    
    if not python_report:
        res.append(html_link("Scanned python modules", "%s_python.html" % fname[fname.rfind("\\")+1:-5]))
        res.append("<BR>")
    
    if len(ext_def):
        if python_report:
            res.append("""<b>The following python modules may contain removed ACM methods.</b><p><BR>""")
        else:
            res.append("""<b>The following ExtensionAttributes may contain removed ACM methods.</b><p><BR>""")
        res.append("""(total = %d)"""% (len(ext_def) ))
    
        ext_def.sort(lambda a, b : cmp(a[0], b[0]))
    
        modulesWithRemovedMethods=sets.Set([ext[0].module_name for ext in ext_def])
    
        for module in modules:
            if module in modulesWithRemovedMethods:
                res.append(h3("[" + module + "]"))
                previous_name = ""
                for ext in ext_def:
                    if ext[0].module_name == module and ext[0].extension_name != previous_name:
                        res.append(ref(ext[0].extension_name, ext[0].extension_name + "ACM") + ", ")
                        previous_name = ext[0].extension_name

    if len(acm_met[0]) or len(acm_met[1]):
        acm_met[0].sort(lambda a, b : cmp(a[0], b[0]))
        acm_met[1].sort(lambda a, b : cmp(a[0], b[0]))
    acm_met = acm_met[0] + acm_met[1]
    if len(acm_met):
        if python_report:
            res.append("""<BR><b>The following python modules may contain changed ACM methods.</b><p>""")
        else:
            res.append("""<BR><b>The following ExtensionAttributes may contain changed ACM methods.</b><p>""")
        res.append("""(total = %d)"""% (len(acm_met) ))
        
        modulesWithChangedMethods=sets.Set([ext[0].module_name for ext in acm_met])

        for module in modules:
            if module in modulesWithChangedMethods:
                res.append(h3("[" + module + "]"))
                previous_name = ""
                for ext in acm_met:
                    if ext[0].module_name == module and ext[0].extension_name != previous_name:
                        res.append(ref(ext[0].extension_name) + ", ")
                        previous_name = ext[0].extension_name




    previous_name = ""
    removed_methods = sets.Set()
    for ext in ext_def:
        if ext[0].extension_name != previous_name:
            if removed_methods:
                res.append(hilite("The highlighted ACM ", 'aaaaaa'))
                res.append(hilite("methods ", 'aaaaaa'))
                for met in removed_methods:
                    res.append(hilite(met, 'aaaaaa'))
                    res.append(hilite(', ', 'aaaaaa'))
                res[-1] = hilite(" has been removed.", 'aaaaaa')
                if len(removed_methods) >= 2: res[-3] = hilite(" and ", 'aaaaaa')
                else: res[-3] = hilite("method ", 'aaaaaa')
                removed_methods = sets.Set()
            
            res.append("<HR>")
            res.append(h3(anchor(ext[0].extension_name, ext[0].extension_name + "ACM")))
        
        res.append(str(ext[0]))
        if python_report:
            res.append("<BR>")
            line = ext[0].code.replace('\n', "<BR>").replace(' ', "&nbsp;")
            for word in ext[0].tokens:    
                for reMet in ext[1]:
                    if reMet == word:
                        line = line.replace(word, hilite(word))
        else:
            res.append(" = ")
            delMetPos = []
            for delMet in ext[1]:
                for pos in ext[0].parsed_code['methods'][delMet]:
                    delMetPos.append((pos, pos + len(delMet)))
            delMetPos.sort(lambda a, b: cmp(b[0], a[0]))
            line = ext[0].code
            for pos in delMetPos:
                line = line[:pos[0]] + hilite(line[pos[0]:pos[1]]) + line [pos[1]:]
                
        res.append(line)
        if not python_report: res.append(";<BR>")
        
        for reMet in ext[1]: removed_methods.add(reMet)
        
        previous_name = ext[0].extension_name
    
    if removed_methods:
        res.append(hilite("The highlighted ACM ", 'aaaaaa'))
        res.append(hilite("methods ", 'aaaaaa'))
        for met in removed_methods:
            res.append(hilite(met, 'aaaaaa'))
            res.append(hilite(', ', 'aaaaaa'))
        res[-1] = hilite(" has been removed.", 'aaaaaa')
        if len(removed_methods) >= 2: res[-3] = hilite(" and ", 'aaaaaa')
        else: res[-3] = hilite("method ", 'aaaaaa')
    
    if len(ext_def): res.append("<BR><HR><HR>")

    previous_name = ""
    changed_methods = sets.Set()
    for ext in acm_met:
        if ext[0].extension_name != previous_name:
            res.append(hilite(printOperandInfo(changed_methods, meta_data), 'aaaaaa'))
            changed_methods = sets.Set()
            res.append("<HR>")
            res.append(h3(anchor(ext[0].extension_name)) )

        res.append(str(ext[0]))
        if python_report:
            res.append("<BR>")
            line = ext[0].code.replace('\n', "<BR>").replace(' ', "&nbsp;")
            for word in ext[0].tokens:    
                for chMet in ext[1]:
                    if chMet == word:
                        line = line.replace(word, hilite(word))
        else:
            res.append(" = ")
            chMetPos = []
            for chMet in ext[1]:
                for pos in ext[0].parsed_code['methods'][chMet]:
                    chMetPos.append((pos, pos + len(chMet)))
            chMetPos.sort(lambda a, b: cmp(b[0], a[0]))
            line = ext[0].code
            for pos in chMetPos:
                line = line[:pos[0]] + hilite(line[pos[0]:pos[1]]) + line [pos[1]:]
        
        res.append(line)
        if not python_report: res.append(";<BR>")
                
        for chMet in ext[1]: changed_methods.add(chMet)
    
        previous_name = ext[0].extension_name
    
    res.append(hilite(printOperandInfo(changed_methods, meta_data), 'aaaaaa'))
    res.append("""</body>""")
    open(fname, 'w').write("".join(res))

def get_defined_with_old_acm(modules, meta_data):
    definedWithRemovedMethods, definedWithChangedMethods = [], [[], []]
    pythonWithRemovedMethods, pythonWithChangedMethods = [], [[], []]
    
    
    for ext in FExtensionUtils.get_extension_in_module(modules, False):
        changed_methods = sets.Set(meta_data.changedAcmMethodOperands) & sets.Set(ext.parsed_code['methods'].keys())
        removed_methods = meta_data.removedAcmMethods & sets.Set(ext.parsed_code['methods'].keys())
        if removed_methods:
            definedWithRemovedMethods.append((ext, removed_methods))
        if changed_methods:
            common = 1
            for method in changed_methods:
                removed_operands, common_operands, new_operands \
                    = meta_data.changedAcmMethodOperands[method]
                if not common_operands: common = 0
                break
            definedWithChangedMethods[common].append((ext, changed_methods))

    
    for ext in FExtensionUtils.get_python_in_module(modules, False):
        changed_methods = sets.Set(meta_data.changedAcmMethodOperands) & ext.tokens
        removed_methods = meta_data.removedAcmMethods & ext.tokens
        if removed_methods:
            pythonWithRemovedMethods.append((ext, removed_methods))
        if changed_methods:
            common = 1
            for method in changed_methods:
                removed_operands, common_operands, new_operands \
                    = meta_data.changedAcmMethodOperands[method]
                if not common_operands: common = 0
                break
            pythonWithChangedMethods[common].append((ext, changed_methods))

    
    return definedWithRemovedMethods, definedWithChangedMethods,\
            pythonWithRemovedMethods, pythonWithChangedMethods
    

def scan_contexts_and_report(meta_data, context, users, reportname, write_summary_report):
    res = [h3("Removed and changed ACM methods")]
    scannedModulesRemoved = {}
    scannedModulesChanged = {}
    scannedModulesPytRem = {}
    scannedModulesPytCh = {}
    totalcountrem, totalcountch = 0, 0
    for cont in context:
        print ("Scanning context", cont.StringKey(), "for removed and changed ACM methods")
        if write_summary_report:
            report = reportname + "_files\\RemAcm_" + cont.StringKey() + ".html"
            report_link = reportname[reportname.rfind("\\")+1:] + "_files\\RemAcm_" + cont.StringKey() + ".html"
            pyt_report = reportname + "_files\\RemAcm_" + cont.StringKey() + "_python.html"
        else:
            report = reportname + "_RemAcm_" + cont.StringKey() + ".html"
            pyt_report = reportname + "_RemAcm_" + cont.StringKey() + "_python.html"
            report_link = report
        modules = FExtensionUtils.get_modules(users, cont).moduleNames()
        definedWithRemovedMethods, definedWithChangedMethods = [], [[], []]
        pythonWithRemovedMethods, pythonWithChangedMethods = [], [[], []]
        for mod in modules:
            if not mod in scannedModulesRemoved:
                removedMethods, changedMethods, remPytMethods, chPytMethods\
                    = get_defined_with_old_acm(mod, meta_data)
                scannedModulesRemoved[mod] = removedMethods
                scannedModulesChanged[mod] = changedMethods
                scannedModulesPytRem[mod] = remPytMethods
                scannedModulesPytCh[mod] = chPytMethods
                definedWithRemovedMethods.extend(removedMethods)
                pythonWithRemovedMethods.extend(remPytMethods)
                definedWithChangedMethods[0].extend(changedMethods[0])
                definedWithChangedMethods[1].extend(changedMethods[1])
                pythonWithChangedMethods[0].extend(chPytMethods[0])
                pythonWithChangedMethods[1].extend(chPytMethods[1])
            else: 
                definedWithRemovedMethods.extend(scannedModulesRemoved[mod])
                pythonWithRemovedMethods.extend(scannedModulesPytRem[mod])
                definedWithChangedMethods[0].extend(scannedModulesChanged[mod][0])
                definedWithChangedMethods[1].extend(scannedModulesChanged[mod][1])
                pythonWithChangedMethods[0].extend(scannedModulesPytCh[mod][0])
                pythonWithChangedMethods[1].extend(scannedModulesPytCh[mod][1])
                
        if len(definedWithRemovedMethods) or len(FExtensionUtils.flatten(definedWithChangedMethods)):
            totalcountrem += len(definedWithRemovedMethods)
            totalcountch += len(FExtensionUtils.flatten(definedWithChangedMethods))
            write_report(report, definedWithRemovedMethods, definedWithChangedMethods,\
                                meta_data, "in context " + cont.StringKey(), modules)
            write_report(pyt_report, pythonWithRemovedMethods, pythonWithChangedMethods,\
                                meta_data, "in context " + cont.StringKey(), modules, True)
            removedCount = len(definedWithRemovedMethods)
            changedCount = len(FExtensionUtils.flatten(definedWithChangedMethods))
            if removedCount:
                res.append(str(removedCount))
                res.append('<small> (')
                res.append(str(len(FExtensionUtils.flatten(scannedModulesRemoved.values()))))
                res.append(") </small>extension attributes defined with removed")
            if changedCount:
                if removedCount: res.append(" and ")
                res.append(str(changedCount))
                res.append('<small> (')
                res.append(str(len(FExtensionUtils.flatten(scannedModulesChanged.values()))))
                res.append(") </small>extension attributes with changed")
                            
            res.append(" ACM methods found in context ")
            res.append(html_link(cont.StringKey(), report_link))
            res.append('<BR>')

    defWithRem = FExtensionUtils.flatten(scannedModulesRemoved.values())
    defWithPytRem = FExtensionUtils.flatten(scannedModulesPytRem.values())
    defWithCh = [[], []]
    defWithPytCh = [[], []]
    for item in scannedModulesChanged.values():
        defWithCh[0].extend(item[0])
        defWithCh[1].extend(item[1])
    for item in scannedModulesPytCh.values():
        defWithPytCh[0].extend(item[0])
        defWithPytCh[1].extend(item[1])
    if not (len(defWithRem)or len(FExtensionUtils.flatten(defWithCh))):
        if write_summary_report:
            res.append("No extension attributes defined with removed or changed ACM methods in the scanned contexts<BR>")
        else:
            print ("No extension attributes defined with removed or changed ACM methods in context", context[0].StringKey())
            return None
    elif write_summary_report:
        report = reportname + "_files\\RemAcm.html"
        report_link = reportname[reportname.rfind("\\")+1:] + "_files\\RemAcm.html"
        pyt_report = reportname + "_files\\RemAcm_python.html"
        write_report(report, defWithRem, defWithCh, meta_data, "in scanned contexts", scannedModulesRemoved.keys())
        write_report(pyt_report, defWithPytRem, defWithPytCh, meta_data, "in scanned contexts", scannedModulesRemoved.keys(), True)
        res.append("Total ")
        if totalcountrem:
            res.append(str(totalcountrem))
            res.append("<small> (")
            res.append(html_link_noUL(str(len(defWithRem)) + " unique", report_link))
            res.append(") </small>with removed")
        if totalcountch:
            if totalcountrem: res.append(" and ")
            res.append(str(totalcountch))
            res.append("<small> (")
            res.append(html_link_noUL(str(len(FExtensionUtils.flatten(defWithCh))) + " unique", report_link))
            res.append(") </small>with changed")
        res.append(" ACM methods<BR>")
    else:
        return report
    return "".join(res)

def scan_modules_and_report(meta_data, module, reportname, write_summary_report):
    print ("Scanning modules for extension attributes defined with removed or changed ACM methods...")
    if write_summary_report:
        report = reportname + "_files\\RemAcm_in_modules.html"
        report_link = reportname[reportname.rfind("\\")+1:] + "_files\\RemAcm_in_modules.html"
        pyt_report = reportname + "_files\\RemAcm_in_modules_python.html"
    else:
        report = reportname + "_RemAcm_in_modules.html"
        report_link = report
        pyt_report = reportname + "_RemAcm_in_modules_python.html"
    modules = FExtensionUtils.get_moduleDict(module)
    definedWithRemovedMethods, definedWithChangedMethods, pythonWithRemovedMethods, pythonWithChangedMethods\
            = get_defined_with_old_acm(modules, meta_data)
    if len(definedWithRemovedMethods) or len(FExtensionUtils.flatten(definedWithChangedMethods)):
        write_report(report, definedWithRemovedMethods, definedWithChangedMethods, meta_data,\
                        "in modules " + modules.StringKey(), modules.moduleNames())
        write_report(pyt_report, pythonWithRemovedMethods, pythonWithChangedMethods, meta_data,\
                        "in modules " + modules.StringKey(), modules.moduleNames(), True)
        res = []
        if len(definedWithRemovedMethods):
            res.append(str(len(definedWithRemovedMethods)))
            res.append(" extension attributes defined with removed")
        if len(FExtensionUtils.flatten(definedWithChangedMethods)):
            if len(definedWithRemovedMethods):
                res.append(" and ")
            res.append(str(len(FExtensionUtils.flatten(definedWithChangedMethods))))
            res.append(" extension attributes with changed")
            
        res.append(" ACM methods found in the ")
        res.append(html_link("scanned modules", report_link))
        res.append('<BR>')
        res = "".join(res)
        if not write_summary_report:
            res = report
    else:
        if write_summary_report:
            res = "No extension attributes defined with removed or changed ACM methods in the scanned modules<BR>"
        else:
            res = None
            print ("No extension attributes defined with removed or changed ACM methods in the scanned modules")
    return res






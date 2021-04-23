from __future__ import print_function


"""----------------------------------------------------------------------------
MODULE
    FExtensionAttributeRemoved - Finds removed extension attributes in other
    extension attribute definitions and writes a HTML report.

DESCRIPTION

    Finds references to extension attributes that will be removed
    in the next version of Front Arena


    (c) Copyright 2011 by SunGard FRONT ARENA. All rights reserved.

----------------------------------------------------------------------------"""

import datetime
from sets import Set

import acm
import ael

import FExtensionUtils
from FHTML import *

def readFromCsvFile(extAttrMapFile):
    """ Read from csv file specified Run Script GUI. """
    dict = {} #oldName:newName 
    f = None
    try:
        f = open(extAttrMapFile, 'r')    
    except Exception as details:
        print ('Extension attribute mapping file not found!', details)
        return dict
    ael.log('Reading extension attribute mapping from file: ' + str(extAttrMapFile))
    for line in f.readlines():
        line = line.replace('\n', '')        
        if len(line.split(';')) > 1:
            oldName = line.split(';')[0]
            newName = line.split(';')[1]
        else:
            oleName = line
            newName = ''
        dict[oldName] = newName
    return dict
    
def readCommentsFromCsvFile(extAttrMapFile):
    """ Read from csv file specified Run Script GUI. """
    dict = {} #oldName:comment 
    f = None
    try:
        f = open(extAttrMapFile, 'r')    
    except Exception as details:
        print ('Extension attribute mapping file not found!', details)
        return dict
    ael.log('Reading extension attribute mapping from file: ' + str(extAttrMapFile))
    for line in f.readlines():
        line = line.replace('\n', '')
        oldName = line.split(';')[0]
        try:
            comment = line.split(';')[2]            
        except Exception:
            comment = ''        
        dict[oldName] = comment
    return dict

def printRemExtInfo(remExt, metaData, extAttrMapFile):
    # remExt = {extension_name:[class_name1, class_name2, ...], extension_name2:[...],...}
    if not remExt:
        return ""
    removedAttributes=FExtensionUtils.create_composit_index(metaData.removedAttributes, "extension_name")
    availableAttributes=FExtensionUtils.create_composit_index(metaData.availableAttributes, "extension_name")
    res = []
    for remExtName in remExt:
        classFound = 0
        if not remExtName in availableAttributes:
            res.append(remExtName)
            res.append(" are not defined anymore. ")
            renamed_attributes = readFromCsvFile(extAttrMapFile)
            attributeMappingComments = readCommentsFromCsvFile(extAttrMapFile)
            
            if remExtName in renamed_attributes and renamed_attributes[remExtName] in availableAttributes:
                old_def = "".join([ext.create_definition() for ext in removedAttributes[remExtName]])
                res.append(hilite(remExtName, 'ee0000', old_def))
                res.append(hilite(" has been renamed to ", 'dd0000')) #dd0000 = DARK RED
                new_def = "".join([ext.create_definition() for ext in availableAttributes[renamed_attributes[remExtName]]])
                res.append(hilite(renamed_attributes[remExtName], 'ff0000', new_def)) #ff0000 = RED
                
                #Comment about the mapping.                
                res.append("<BR><BR>Mapping comment: ")
                res.append(hilite(attributeMappingComments[remExtName])) 
                res.append(".")
            res.append("<BR>")    
        else:    
            for remExtDef in removedAttributes[remExtName]:
                if remExtDef.class_name in remExt[remExtName]:
                    if not res or res[-1] == '<BR>':    #It's the first loop
                        res.append("The definition ")
                    else:       #It's not the first loop
                        res.append(", ")
                    res.append(str(remExtDef))
                    classFound += 1
                    
            if classFound >= 2: # Found at least two classes, change the last comma to " and "
                res[-2] = " and "
            if classFound:
                res.append(" has been removed")
                            
            if len(removedAttributes[remExtName]) > classFound:
                if classFound:
                    res.append(", and so have the following defintions:<BR>")
                else:
                    res.append("The following definitions of ")
                    res.append(remExtName)
                    res.append(" have been removed:<BR>")
                for remExtDef in removedAttributes[remExtName]:
                    if not remExtDef.class_name in remExt[remExtName]:
                        res.append(str(remExtDef))
                        res.append('<BR>')
            else:
                res.append('.<BR>')
        
            res.append(remExtName)
            res.append(" are defined for:<BR>")
            for extDef in availableAttributes[remExtName]:
                res.append(str(extDef))
                res.append('<BR>')
            
        res.append('<BR>')
    return "".join(res)


def write_report(fname, ext_def, metaData, description, modules, extAttrMapFile):    
    """Produce HTML report of the removed extension attributes"""
    res = ["""<html><head><title> Found removed extension attributes
                </title></head><body bgcolor=ffffff>"""]               
    res.append("""<h1>Removed extension attributes found %s</h1>""" % (description,) )
    res.append("""Produced on: %s<p>""" % (str(datetime.datetime.now())[0:19],) )
    res.append("""By user: %s<p>""" % (acm.UserName(),) )
    res.append("""ADS: %s<p>""" % (acm.ADSAddress(),) )
    res.append("""<b>The following ExtensionAttributes may contain deleted extension attributes.</b><p>""")
    res.append("""(total = %d)"""% (len(FExtensionUtils.flatten(ext_def)) ))    
    
    #ext_def = [[(ExtensionAttribute, [[Removed ExtAttr1], [Removed ExtAttr2], ...]), ... ],
    #           [(ExtensionAttribute, [[Removed ExtAttr1], [Removed ExtAttr2], ...]), ... ],
    #           .....]
    for i in range(len(ext_def)):
        ext_def[i].sort(lambda a, b : cmp(a[0], b[0]))
    
    available_attributes = Set([ext.extension_name for ext in metaData.availableAttributes])
    renamed_attributes = readFromCsvFile(extAttrMapFile)
    renamed_extensions = Set([ext.extension_name for ext in metaData.removedAttributes]) & Set(renamed_attributes) - available_attributes
    modulesWithRenamedAttributes = {}
    for ext in ext_def[0]:
        ren_attr = {}
        for attr in Set(ext[0].parsed_code["extattr"]) & renamed_extensions:
            ren_attr[attr] = renamed_attributes[attr]
        if ren_attr:
            modulesWithRenamedAttributes.setdefault(ext[0].module_name, {}).update(ren_attr)
    
    ext_def = FExtensionUtils.flatten(ext_def)
    
    modulesWithDeletedAttributes = Set([ext[0].module_name for ext in ext_def])   
    
    for module in modules:
        if module in modulesWithDeletedAttributes:
            if module in modulesWithRenamedAttributes:
                ren_dict = {}
                for ext in modulesWithRenamedAttributes[module]: ren_dict[ext] = renamed_attributes[ext] 
                res.append(h3("[" + module + "]"\
                    + update_tag("ExtensionModule", module\
                    + str(modulesWithRenamedAttributes[module]).replace("'", ""))\
                    + update_tag("OneExtensionFromList", module\
                    + str(modulesWithRenamedAttributes[module]).replace("'", ""))))
            else:
                res.append(h3("[" + module + "]"))
            previous_name = ""
            for ext in ext_def:
                if ext[0].module_name == module and ext[0].extension_name != previous_name:
                    res.append(ref(ext[0].extension_name) + ", ")
                    previous_name = ext[0].extension_name
    
    previous_name = ""
    remExt = {}
    for ext in ext_def:
        if ext[0].extension_name != previous_name:
            remExtInfo = printRemExtInfo(remExt, metaData, extAttrMapFile)            
            res.append(hilite(remExtInfo, 'aaaaaa'))
            remExt = {}
            res.append("<HR>")
            res.append(h3(anchor(ext[0].extension_name)) )
        
        res.append(str(ext[0]))
        res.append(" = ")
        deletedExt = Set([delExt[0].extension_name for delExt in ext[1]])
        delExtPos = []
        for delExt in deletedExt:
            remExt.setdefault(delExt, Set()).add(ext[0].class_name)
            for pos in ext[0].parsed_code['extattr'][delExt]:
                delExtPos.append((pos, pos + len(delExt)))
        
        delExtPos.sort(lambda a, b : cmp(b[0], a[0]))
        line = ext[0].code
        for pos in delExtPos:
            if line[pos[0]:pos[1]] in renamed_extensions:
                line = line[:pos[0]] + hilite(line[pos[0]:pos[1]], 'ff55dd') + line[pos[1]:]
            elif not line[pos[0]:pos[1]] in available_attributes:
                line = line[:pos[0]] + hilite(line[pos[0]:pos[1]], 'ddddff') + line[pos[1]:]
            else:
                line = line[:pos[0]] + hilite(line[pos[0]:pos[1]], 'ddf1ff') + line[pos[1]:]
        res.append(line + ';')
        ren_ext = deletedExt & renamed_extensions 
        if ren_ext:
            ren_dict = {}
            for attr in ren_ext: ren_dict[attr] = renamed_attributes[attr] 
            res.append(update_tag("ExtensionAttribute", str(ext[0]) + str(ren_dict).replace("'", ""))) 
        
        
        res.append("<BR>")
        previous_name = ext[0].extension_name
    
    res.append(hilite(printRemExtInfo(remExt, metaData, extAttrMapFile), 'aaaaaa'))
    res.append("""</body>""")
    outfile = open(fname, 'w')
    outfile.write("".join(res))


def get_extensions_with_removed_attributes(modules, removedAttributes, availableAttributes):
            
    #Get all extension attributes
    extensionAttributes = FExtensionUtils.create_composit_index\
        (FExtensionUtils.get_extension_in_module(modules, False), "extension_name")
     
    definedWithRemovedAttribute = [[], [], []]
    for exts in extensionAttributes.values():
        removedType = 2 #Removed type = 0 => Extension attribute is removed, not defined for any class
                        #Removed type = 1 => Extension attribute is removed from defined class
                        #Removed type = 2 => Extension attribute is removed from other class
        defWithRemExt = []
        for item in exts:
            removedInExt = Set(removedAttributes.keys()) & Set(item.parsed_code["extattr"].keys())
            if not removedInExt:
                continue
            if removedType:
                removed_classes = Set()
                for rem in removedInExt:
                    if not rem in availableAttributes:
                        removedType = 0
                        break
                    removed_classes |= Set([ext.class_name for ext in removedAttributes[rem]])
                if removedType and item.class_name in removed_classes:
                    removedType = 1
            defWithRemExt.append((item, [removedAttributes[key] for key in removedInExt]))
                
        definedWithRemovedAttribute[removedType].extend(defWithRemExt)
        
    return definedWithRemovedAttribute
    

def scan_contexts_and_report(metaData, context, users, reportname, write_summary_report, extAttrMapFile):
    res = [h3("Removed extension attributes")]
    scannedModules = {}
    totalcount = 0
    removedAttributes=FExtensionUtils.create_composit_index(metaData.removedAttributes, "extension_name")
    availableAttributes=FExtensionUtils.create_composit_index(metaData.availableAttributes, "extension_name")
    for cont in context:
        print ("Scanning context", cont.StringKey(), "for removed extension attributes")
        if write_summary_report:
            report = reportname + "_files\\RemExt_" + cont.StringKey() + ".html"
            report_link = reportname[reportname.rfind("\\")+1:] + "_files\\RemExt_" + cont.StringKey() + ".html"
        else:
            report = reportname + "_RemExt_" + cont.StringKey() + ".html"
            report_link = report
        modules = FExtensionUtils.get_modules(users, cont)
        definedWithRemovedAttribute=[[], [], []]
        for mod in modules.moduleNames():
            if not mod in scannedModules:
                extList = get_extensions_with_removed_attributes(mod, removedAttributes, availableAttributes)
                scannedModules[mod] = extList
            else: 
                extList = scannedModules[mod]
            for i in range(len(extList)):
                definedWithRemovedAttribute[i].extend(extList[i])
                
        if len(FExtensionUtils.flatten(definedWithRemovedAttribute)):
            totalcount += len(FExtensionUtils.flatten(definedWithRemovedAttribute))
            write_report(report, definedWithRemovedAttribute, metaData, "in context " + cont.StringKey(), modules.moduleNames(), extAttrMapFile)
            res.append(str(len(FExtensionUtils.flatten(definedWithRemovedAttribute))))
            res.append('<small> (')
            res.append(str(len(FExtensionUtils.flatten(scannedModules.values()))))
            res.append(") </small>extension attributes defined with removed extension attributes found in context ")
            res.append(html_link(cont.StringKey(), report_link))
            res.append('<BR>')
    if not len(FExtensionUtils.flatten(scannedModules.values())):
        if write_summary_report:
            res.append("No extension attributes defined with removed attributes in the scanned contexts<BR>")
        else:
            print ("No extension attributes defined with removed attributes in context", context[0].StringKey())
            return None
    elif write_summary_report:
        #Adding "/" instead of "\\" in order for it to work with the webserver
        report = reportname + "_files/RemExt.html"
        report_link = reportname[reportname.rfind("\\")+1:] + "_files/RemExt.html"
        definedWithRemovedAttribute = [[], [], []]
        for extList in scannedModules.values():
            for i in range(len(extList)):
                definedWithRemovedAttribute[i].extend(extList[i])
        write_report(report, definedWithRemovedAttribute, metaData, "in scanned contexts", scannedModules.keys(), extAttrMapFile)
        res.append("Total ")
        res.append(str(totalcount))
        res.append("<small> (")
        res.append(html_link_noUL(str(len(FExtensionUtils.flatten(scannedModules.values()))) + " unique", report_link))
        res.append(") </small>definitions <BR>")
    else:
        return report
    return "".join(res)

def scan_modules_and_report(metaData, module, reportname, write_summary_report, extAttrMapFile):
    print ("Scanning modules for extension attributes defined with removed attributes...")
    removedAttributes=FExtensionUtils.create_composit_index(metaData.removedAttributes, "extension_name")
    availableAttributes=FExtensionUtils.create_composit_index(metaData.availableAttributes, "extension_name")
    if write_summary_report:
        report = reportname + "_files\\RemExt_in_modules.html"
        report_link = reportname[reportname.rfind("\\")+1:] + "_files\\RemExt_in_modules.html"
    else:
        report = reportname + "_RemExt_in_modules.html"
        report_link = report
    modules=FExtensionUtils.get_moduleDict(module)
    definedWithRemovedAttribute = get_extensions_with_removed_attributes(modules, removedAttributes, availableAttributes)
    print ("Extenmsion attributes defined with removed attribute:", len(FExtensionUtils.flatten(definedWithRemovedAttribute)))
    if len(FExtensionUtils.flatten(definedWithRemovedAttribute)):
        write_report(report, definedWithRemovedAttribute, metaData, "in modules " + module.StringKey(), modules.moduleNames(), extAttrMapFile)
        res = [str(len(FExtensionUtils.flatten(definedWithRemovedAttribute)))]
        res.append(" extension attributes defined with removed extension attributes found in the ")
        res.append(html_link("scanned modules", report_link))
        res.append('<BR>')
        res = "".join(res)
        
        if not write_summary_report:
            res = report
    else:
        if write_summary_report:
            res = "No extension attributes defined with removed attributes in the scanned modules<BR>"
        else:
            res = None
            print ("No extension attributes defined with removed attributes in the scanned modules")
    return res

def update_extension_attribute(module_name, class_name, extension_name, attributes_to_rename):

    extension = FExtensionUtils.get_one_parsed_extension\
                ('FExtensionAttribute', module_name, class_name, extension_name)
    
        
    extPos = []
    for ext in Set(attributes_to_rename) & Set(extension.parsed_code['extattr']):
        for pos in extension.parsed_code['extattr'][ext]:
            extPos.append((pos, pos + len(ext)))

    extPos.sort(lambda a, b : cmp(b[0], a[0]))
    extcode = extension.code
    for pos in extPos:
        extcode = extcode[:pos[0]] + attributes_to_rename[extcode[pos[0]:pos[1]]] + extcode[pos[1]:]
    
    dummy_context = acm.FExtensionContext()
    dummy_context.AddModule(module_name)
    dummy_context.EditImport("FExtensionAttribute", str(extension) + " = " + extcode)
    dummy_context.RemoveModule(module_name)
    
    return extension.code

def update_extension_module(module_name, updated_extensions, rename_dictionary):

    extensions = get_extensions_with_removed_attributes(module_name, rename_dictionary, {})
    extensions = [ext[0] for ext in extensions[0]] #Only extension attributes that's not defined in the to version (removeType 0)
    rename_set = Set(rename_dictionary.keys())

    dummy_context = acm.FExtensionContext()
    dummy_context.AddModule(module_name)
    
    for ext in extensions:
        attributes_to_rename = Set(ext.parsed_code["extattr"]) & rename_set
        if not attributes_to_rename:
            continue
           
        extPos = []
        renamed_in_ext = {}
        for attr in attributes_to_rename:
            renamed_in_ext[attr] = rename_dictionary[attr]
            for pos in ext.parsed_code['extattr'][attr]:
                extPos.append((pos, pos + len(attr)))

        extPos.sort(lambda a, b : cmp(b[0], a[0]))
        extcode = ext.code
        for pos in extPos:
            extcode = extcode[:pos[0]] + rename_dictionary[extcode[pos[0]:pos[1]]] + extcode[pos[1]:]

        dummy_context.EditImport("FExtensionAttribute", str(ext) + " = " + extcode)
        
        
        if str(ext) in updated_extensions:
            updated_extensions[str(ext)].updated_extensions.update(renamed_in_ext)
        else:
            updated_extensions[str(ext)] = FExtensionUtils.UpdatedExtension(ext.code, {}, renamed_in_ext)
    
    dummy_context.RemoveModule(module_name)
    
    return updated_extensions





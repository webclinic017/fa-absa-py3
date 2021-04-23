from __future__ import print_function


"""----------------------------------------------------------------------------
MODULE
    FColumnDefinitionUpgrade - Migrate FColumnDefinitions to FColumnAppearance

DESCRIPTION


    (c) Copyright 2011 by SunGard FRONT ARENA. All rights reserved.

----------------------------------------------------------------------------"""

import datetime
import sets
import re

import acm

import FExtensionUtils
from FHTML import *

moved_column_attributes=sets.ImmutableSet(['Background', 'BkgFlash', 'BkgOrderBestInOrderBook',\
        'BkgOrderCanMatch', 'BkgOrderDeleted', 'BkgOrderDone',\
        'BkgOrderInactive', 'BkgOrderMoved',\
        'BkgOrgsOrderAsk', 'BkgOrgsOrderBid', 'BkgStripe', 'BkgTradeInactive',\
        'BkgTradersOrderAsk', 'BkgTradersOrderBid', 'BkgUserEdited', 'Text',\
        'TextDisconnected', 'TextFlash', 'TextPendingRefresh', 'ValueTruncate',\
        'ValueTruncation', 'Alignment', 'Flashing', 'FontBold', 'Font', 'FontSize'])

def write_report(fname, new_col_def, old_col_def, col_app, description):    
    """Produce HTML report of the changed colmn defintions"""
    
    res = ["""<html><head><title> Changed column definition %s
                </title></head><body bgcolor=ffffff>""" % (description,)]               
    res.append("""<h1>Changed column definition %s</h1>""" % (description,) )
    res.append("""Produced on: %s<p>""" % (str(datetime.datetime.now())[0:19],) )
    res.append("""By user: %s<p>""" % (acm.UserName(),) )
    res.append("""ADS: %s<p>""" % (acm.ADSAddress(),) )
    res.append("""<b>The following changes have been made to the column definitions. """)
    res.append("""The changes <i>are not saved</i>; """)
    res.append("""hence, to keep them save the changed modules in the extension manager.</b><p>""")
    res.append(h2("Changed column definitions (total = %d)"% (len(new_col_def) )))
    
    
    modules=sets.Set([col.module_name for col in new_col_def])
    new_col_def.sort()
    old_col_def.sort()
    
    while len(modules):
        active_mod=modules.pop()
        res.append(h3("[" + active_mod + "]"))
        for col in new_col_def:
            if col.module_name == active_mod:
                res.append(ref(col.extension_name) + ", ")
    
    if len(new_col_def) == len(old_col_def):
        for i in range(len(new_col_def)):
            res.append(h3(anchor(new_col_def[i].extension_name)) )
            res.append("<TABLE><TR><TD>")
            res.append(h4("New column definition"))
            res.append("</TD><TD>")
            res.append(h4("Old column definition"))
            res.append("</TD></TR><TR><TD>")
            for line in new_col_def[i].create_definition().split('\n'):
                attr=re.match(r"  ([\w]+)=([\w /%\-&]+)", line)
                if attr and attr.groups()[0] == "ColumnAppearance":
                    res.append(hilite("&nbsp;&nbsp;ColumnAppearance="+ref(attr.groups()[1]) + "<BR>"))
                else:
                    res.append(line.replace(' ', "&nbsp;") + "<BR>")
            res.append("</TD><TD>")
            for line in old_col_def[i].create_definition().split('\n'):
                attrb=re.match(r"  ([\w]+)=.*", line)
                if attrb and attrb.groups()[0] in moved_column_attributes:
                    res.append(hilite(line.replace(' ', "&nbsp;") + "<BR>"))
                else:
                    res.append(line.replace(' ', "&nbsp;") + "<BR>")
            res.append("</TD></TR></TABLE>")
            res.append("<HR>")        
    
        res.append(h2("New ColumnAppearnce definitions"))
        for app in col_app:
            res.append(h3(anchor(app.extension_name)))
            for line in app.create_definition().split('\n'):
                res.append(line.replace(' ', "&nbsp;") + "<BR>")
            res.append("<HR>")
            
    else:
        res.append("Data error")
    
    res.append("""</body>""")
    outfile = open(fname, 'w')
    outfile.write("".join(res))


def find_and_change_old_coldefs(modules):
    
    #Get all column definitions
    columns = FExtensionUtils.get_column_in_module(modules)

    #Find the columns that contains attributes that have been moved to column appearance
    columns_containing_moved_attributes =[item for item in columns \
                if sets.Set(item.attribute_dictionary.keys()) & moved_column_attributes]
    
    #Make a copy of the list with column defintions
    old_column_def=[]
    for col in columns_containing_moved_attributes:
        old_column_def.append(FExtensionUtils.ColumnDefinition(col.module_name, col.class_name, col.extension_name, {}))
        for key in col.attribute_dictionary.keys():
            old_column_def[-1].attribute_dictionary[key] = col.attribute_dictionary[key]
     
    new_ColumneAppearances=[]
    dummy_context = acm.FExtensionContext()
    #Make the changes in the column defintions and column attributes
    for col_def in columns_containing_moved_attributes:    
        if col_def.attribute_dictionary.has_key("ColumnAppearance"):
            context = modules.get_context()
            columnAppearanceName = col_def.attribute_dictionary["ColumnAppearance"]
            columnAppearance = FExtensionUtils.get_extensions(context, "FColumnAppearance", columnAppearanceName)
            
            newColumnAppearance = FExtensionUtils.ColumnDefinition.create_from_definition(columnAppearance)            
            if not newColumnAppearance:
                #If the column appearance refered in the column definition does not exist, 
                #we create a new empty one                            
                dummyColApp = "[OldColDefs]FObject:ColumnAppearance =\n  "
                newColumnAppearance = FExtensionUtils.ColumnDefinition.create_from_definition(dummyColApp)                
                print ("Not possible to create new column appearance based on " + columnAppearanceName +\
                        ". Creating new empty column appearance.")
        else:
            newColumnAppearance=FExtensionUtils.ColumnDefinition(col_def.module_name, "FObject", "ColumnAppearance", {})
                   
        #Rename the column appearance
        newColumnAppearance.extension_name += '_' + col_def.extension_name.replace(' ', '_')
        col_def.attribute_dictionary["ColumnAppearance"] = newColumnAppearance.extension_name
        #This while loop guranties that you don't override an existing ColumnAppearnce by adding an
        #underscore to the name while the column appearnce name exists
        while FExtensionUtils.get_extensions(modules.get_context(), "FColumnAppearance", newColumnAppearance.extension_name):
            newColumnAppearance.extension_name += '_'
            col_def.attribute_dictionary["ColumnAppearance"] = newColumnAppearance.extension_name
            
        new_ColumneAppearances.append(newColumnAppearance)     
        #Move the attributes from the column definition to the column apperance
        for key in(sets.Set(col_def.attribute_dictionary.keys()) & moved_column_attributes):
            newColumnAppearance.attribute_dictionary[key]=col_def.attribute_dictionary[key]
            del col_def.attribute_dictionary[key]
        
        #Apply the changes
        if acm.ShortVersion()[0:3]=='3.2':
            dummy_context.AddModule(col_def.module_name)
            dummy_context.EditImport("FColumnAppearance", newColumnAppearance.create_definition(), 0)
            dummy_context.EditImport("FColumnDefinition", col_def.create_definition(), 0)
            dummy_context.RemoveModule(col_def.module_name)
        else:
            dummy_context.AddModule(col_def.module_name)
            dummy_context.EditImport("FColumnAppearance", newColumnAppearance.create_definition())
            dummy_context.EditImport("FColumnDefinition", col_def.create_definition())
            dummy_context.RemoveModule(col_def.module_name) 
    
    #Print report of the changes
    return columns_containing_moved_attributes, old_column_def, new_ColumneAppearances

def scan_contexts_and_report(context, users, reportname, write_summary_report):
    res = [h3("Old column definition type")]
    remAttr = []
    for cont in context:
        print ("Scanning context", cont.StringKey(), "for old column definition types")
        if write_summary_report:
            report = reportname + "_files\\UpgradeCol_" + cont.StringKey() + ".html"
            report_link = reportname[reportname.rfind("\\")+1:] + "_files\\UpgradeCol_" + cont.StringKey() + ".html"
        else:
            report = reportname + "_UpgradeCol_" + cont.StringKey() + ".html"
            report_link = report
        modules = FExtensionUtils.get_modules(users, cont)
        columns_containing_moved_attributes, old_column_def, new_ColumneAppearances \
                = find_and_change_old_coldefs(modules)
        if len(columns_containing_moved_attributes):
            remAttr.append((cont, len(columns_containing_moved_attributes)))
            write_report(report, columns_containing_moved_attributes,\
                    old_column_def, new_ColumneAppearances, "in context " + cont.StringKey())
            res.append(str(len(columns_containing_moved_attributes)))
            res.append(" updated column definitions in context ")
            res.append(html_link(cont.StringKey(), report_link))
            res.append('<BR>')
    if not remAttr:
        if write_summary_report:
            res.append("No old column definition type found in the scanned contexts<BR>")
        else:
            print ("No old column definition type found in context", context[0].StringKey())
            return None
    elif write_summary_report:
        sum = 0
        for attr in remAttr: sum += attr[1]
        res.append("Total ")
        res.append(str(sum))
        res.append(" updated column definitions<BR>")
    else:
        return report
    return "".join(res)

def scan_modules_and_report(module, reportname, write_summary_report):
    print ("Scanning modules for old column definition types...")
    if write_summary_report:
        report = reportname + "_files\\UpgradeCol_in_modules.html"
        report_link = reportname[reportname.rfind("\\")+1:] + "_files\\UpgradeCol_in_modules.html"
    else:
        report = reportname + "_UpgradeCol_in_modules.html"
        report_link = report
    modules = FExtensionUtils.get_moduleDict(module)
    columns_containing_moved_attributes, old_column_def, new_ColumneAppearances \
            = find_and_change_old_coldefs(modules)
    if len(columns_containing_moved_attributes):
        write_report(report, columns_containing_moved_attributes,\
                    old_column_def, new_ColumneAppearances, "in modules " + modules.StringKey())
        res = [str(len(columns_containing_moved_attributes))]
        res.append(" updated column definitions in the ")
        res.append(html_link("scanned modules", report_link))
        res.append('<BR>')
        res = "".join(res)
        if not write_summary_report:
            res = report
    elif write_summary_report:
        res = "No old column definition type found in the scanned modules<BR>"
    else:
        res = None
        print ("No old column definition type found in the scanned modules")
    return res






from __future__ import print_function


""" scan_extensions - Scans extensions for problems and produce index

"""

__version__ = (2, 0, 0)

import datetime
import re
import sets

import acm

import FExtensionUtils
reload(FExtensionUtils)

# #############################################################################
# Generate HTML Report

from FHTML import *

adfltokens = sets.Set( """number nil true false ident string var ref value 
node remote shift df imply select objattr switch shunt default simproxy 
snoop defer bod averageOf maxOf meanOf minOf sumOf check not and or 
eof""".split(" ") )

class AdflCrossLinker:
    """Used by regexp to add crossreferences to code fragments"""
    def __init__(self, extensions):
        self.extensions = extensions
    def __call__(self, match):
        txt = match.groups()[0]
        if txt in self.extensions:
            return ref(txt)
        if txt in adfltokens:
            return b(txt)
        return txt
    
def write_report(fname, extensions, description, context, unreffed):    
    """Produce HTML report of problem an and indexed documentation"""
    # As always html generation looks rather horrible in practice...
    res = ["""<html><head><title> Full scan of extension attributes in %s
                </title></head><body bgcolor=ffffff>""" % (description,)]               
    res.append("""<h1>Index of extension for %s</h1>""" % (description,) )
    res.append("""Produced on: %s<p>""" % (str(datetime.datetime.now())[0:19],) )
    res.append("""By user: %s<p>""" % (acm.UserName(),) )
    res.append("""ADS: %s<p>""" % (acm.ADSAddress(),) )
    res.append(h2("Unreferenced extensions (total = %d)"% (len(unreffed) )))
    unrefbymod = {}
    for extname in unreffed:
        for ext in extensions[extname]:
            unrefbymod.setdefault(ext.module_name, sets.Set()).add(extname)
    for mod, unrefextensn in unrefbymod.items():
        res.append( "<p>" + hilite(mod, "ffff88") + "<p>")
        for extname in sorted_extensions(unrefextensn):
            res.append(ref(extname) + ", ")
    revindex = build_reverse_index(extensions)
    lastletter = ''
    res.append(h2("Referenced extensions (total = %d)"% (len(extensions) )))
    for extname in sorted_extensions(extensions):
        if extname[0].upper() != lastletter:
            lastletter = extname[0].upper()
            res.append( h3(lastletter) )
        res.append(ref(extname) +"  ")
    crosslinker = AdflCrossLinker(extensions)
    for extname in sorted_extensions(extensions):        
        res.append(h2(anchor(extname)) )    
        if context:
            descr = context.ExtensionDescription("FExtensionAttribute", extname)
            if descr:
                res.append(i(descr) + "<p>")
        for ext in extensions[extname]:
            linkedcode = re.sub("([a-zA-Z_][a-zA-Z_0-9]*)", 
                                crosslinker, ext.code)
            res.append( hilite(ext.module_name, "ffdddd") + hilite(ext.class_name) + 
                        " = " +  fmtadfl(linkedcode) )
            res.append("<p>")        
        res.append( h3("referenced by") )
        refs = list(revindex.get(extname, []) )
        refs.sort(lambda a, b:cmp(a.upper(), b.upper()))
        for ext in refs:
            res.append( ref( ext ) + " ")
        res.append("<HR>")        
    res.append("""</body>""")
    outfile = open(fname, 'w')
    outfile.write("".join(res))

# #############################################################################
# Parse and alanlyze extension attributes

def build_reverse_index(extensions):
    """Build reverse index from { extname : [ExtensionAttribute..] } """
    index = {}
    allextnames = sets.ImmutableSet( extensions.keys() )
    for extname  in extensions:
        for extension in extensions[extname]:
            for reference in extension.tokens&allextnames:
                index.setdefault(reference, sets.Set()).add(extname)
    return index

def sorted_extensions(extensions):
    """Return a sorted list of names in { extname : [ExtensionAttribute..] }"""
    sorted_names = [str(ext) for ext in list(extensions)]
    sorted_names.sort(lambda a, b:cmp(a.upper(), b.upper()))
    return sorted_names

def follow_references(extensions, visited_extensions, new_refs):
    """Follow references in extensions and mark all visited"""
    for reference in new_refs:
        visited_extensions.add(reference)
        for ext in extensions[reference]:
            for newref in ext.tokens:
                if not newref in visited_extensions and newref in extensions:
                    follow_references(extensions, visited_extensions, [newref] )  
                    
def extensions_referenced_by_columns(modules):
    colextattrs = sets.Set( [ coldef.attribute_dictionary['ExtensionAttribute'] for coldef in\
                            FExtensionUtils.get_column_in_module(modules)\
                            if coldef.attribute_dictionary.has_key('ExtensionAttribute')] )
    colextattrs |= sets.Set( [ coldef.attribute_dictionary['SolverDefaultParameter'] for coldef in\
                            FExtensionUtils.get_column_in_module(modules)\
                            if coldef.attribute_dictionary.has_key('SolverDefaultParameter')] )
    colextattrs |= sets.Set( [ coldef.attribute_dictionary['DynamicVectorPerRowObjectCalculationColumnId'] for coldef in\
                            FExtensionUtils.get_column_in_module(modules)\
                            if coldef.attribute_dictionary.has_key('DynamicVectorPerRowObjectCalculationColumnId')] )
    colextattrs |= sets.Set( [ coldef.attribute_dictionary['ChoicesExpr'] for coldef in\
                            FExtensionUtils.get_column_in_module(modules)\
                            if coldef.attribute_dictionary.has_key('ChoicesExpr')] )
    colextattrs |= sets.Set( [ menuext.attribute_dictionary['ExtensionAttribute'] for menuext in\
                            FExtensionUtils.get_menuextension_in_module(modules)\
                            if menuext.attribute_dictionary.has_key('ExtensionAttribute')] )
    colextattrs |= sets.Set( [ exptrans.attribute_dictionary['Inverse'] for exptrans in\
                            FExtensionUtils.get_expressiontransform_in_module(modules)\
                            if exptrans.attribute_dictionary.has_key('Inverse')] )
    colextattrs |= sets.Set( [ exptrans.attribute_dictionary['InverseVariable'] for exptrans in\
                            FExtensionUtils.get_expressiontransform_in_module(modules)\
                            if exptrans.attribute_dictionary.has_key('InverseVariable')] )
    colextattrs |= sets.Set( [ exptrans.attribute_dictionary['Transform'] for exptrans in\
                            FExtensionUtils.get_expressiontransform_in_module(modules)\
                            if exptrans.attribute_dictionary.has_key('Transform')] )
    colextattrs |= sets.Set( [ colapp.attribute_dictionary['TextExtensionAttribute'] for colapp in\
                            FExtensionUtils.get_columnappearance_in_module(modules)\
                            if colapp.attribute_dictionary.has_key('TextExtensionAttribute')] )
    colextattrs |= sets.Set( [ colapp.attribute_dictionary['BkgExtensionAttribute'] for colapp in\
                            FExtensionUtils.get_columnappearance_in_module(modules)\
                            if colapp.attribute_dictionary.has_key('BkgExtensionAttribute')] )
    if acm.FChoiceList.Select('name = Valuation Extension'):        
        colextattrs |= sets.Set( [ item.StringKey() for item in\
                            acm.FChoiceList.Select('name = Valuation Extension').At(0).Choices()] )
    return colextattrs
                    
def parse_analyze_and_report_extensions(modules):
    """Find atributes that appear never to be called"""
    checkextensions = sets.Set()
    extensions = {}
    for extattr in FExtensionUtils.get_extension_in_module(modules):
        extensions.setdefault(extattr.extension_name, []).append(extattr)
        if extattr.module_name in modules.nonBuiltInModules():
            checkextensions.add(extattr.extension_name)  
    allextnames = sets.ImmutableSet( extensions.keys() )
    colextattrs = extensions_referenced_by_columns(modules)
    badcolumns = colextattrs - allextnames
    colextattrs -= badcolumns
    referenced_extensions = sets.Set()
    follow_references(extensions, referenced_extensions, colextattrs )
    unreffed_extensions = checkextensions - referenced_extensions  - colextattrs
    res  = []
    for extname in unreffed_extensions:
        for ext in extensions[extname]:            
            res.append( (ext.module_name, ext.extension_name, ext.class_name, ) )
    res.sort()
    return extensions, unreffed_extensions
    
def scan_context(context, users):
    """Scan context for porential extension problems"""
    modules = FExtensionUtils.get_modules(users, context)
    return parse_analyze_and_report_extensions(modules)

def scan_modules(modules):
    return parse_analyze_and_report_extensions(modules)

def scan_contexts_and_report(context, users, reportname, write_summary_report):
    res = [h3("Unreferenced code")]
    unref_count = 0
    unref_ext = sets.Set()
    ext_attrs = {}
    for cont in context:
        print ("Scanning context", cont.StringKey(), "for unreferenced code")
        if write_summary_report:
            report = reportname + "_files\\Unreferenced_" + cont.StringKey() + ".html"
            report_link = reportname[reportname.rfind("\\")+1:] + "_files\\Unreferenced_" + cont.StringKey() + ".html"
        else:
            report = reportname + "_Unreferenced_" + cont.StringKey() + ".html"
            report_link = report
        extensions, unreffed_extensions = scan_context(cont, users)
        if len(unreffed_extensions):
            unref_count += len(unreffed_extensions)
            unref_ext |= unreffed_extensions
            ext_attrs.update(extensions)
            write_report(report, extensions, "all modules in " + cont.StringKey(), cont, unreffed_extensions)
            res.append(str(len(unreffed_extensions)))
            res.append("<small> (")
            res.append(str(len(unref_ext)))
            res.append(") </small>unreferenced extension attributes in context ")
            res.append(html_link(cont.StringKey(), report_link))
            res.append('<BR>')
    if not unref_count:
        if write_summary_report:
            res.append("No unreferenced extension attributes found in the scanned contexts<BR>")
        else:
            print ("No unreferenced extension attributes found in context", context[0].StringKey())
            return None
    elif write_summary_report:
        report = reportname + "_files\\UnrefExt.html"
        report_link = reportname[reportname.rfind("\\")+1:] + "_files\\UnrefExt.html"
        write_report(report, ext_attrs, "scanned contexts", None, unref_ext)
        res.append("Total ")
        res.append(str(unref_count))
        res.append("<small> (")
        res.append(html_link_noUL(str(len(unref_ext)) + " unique", report_link))
        res.append(") </small>unreferenced extension attributes<BR>")
    else:
        return report
    return "".join(res)

def scan_modules_and_report(module, reportname, write_summary_report):
    print ("Scanning modules for unreferenced extension attributes...")
    if write_summary_report:
        report = reportname + "_files\\Unreferenced_in_modules.html"
        report_link = reportname[reportname.rfind("\\")+1:] + "_files\\Unreferenced_in_modules.html"
    else:
        report = reportname + "_Unreferenced_in_modules.html"
        report_link = report
    modules = FExtensionUtils.get_moduleDict(module)
    extensions, unreffed_extensions = scan_modules(modules)
    if len(unreffed_extensions):
        write_report(report, extensions, "in modules " + modules.StringKey(), None, unreffed_extensions)
        res = [str(len(unreffed_extensions))]
        res.append(" unreferenced extension attributes in the ")
        res.append(html_link("scanned modules", report_link))
        res.append('<BR>')
        res = "".join(res)
        if not write_summary_report:
            res = report
    else:
        if write_summary_report:
            res = "No unreferenced extension attributes found in the scanned modules<BR>"
        else:
            res = None
            print ("No unreferenced extension attributes found in the scanned modules")
            
    return res






from __future__ import print_function


"""----------------------------------------------------------------------------
MODULE
    FExtScannerToolController - Starts the scanners that scans the adfl code

DESCRIPTION


    (c) Copyright 2011 by SunGard FRONT ARENA. All rights reserved.

----------------------------------------------------------------------------"""

import datetime
import os
import sets

import acm

import FAcmMethodsRemoved
import FExtensionAttributeOverride
import FExtensionAttributeRedundant
import FExtensionAttributeRemoved
import FExtensionUnref
import FColumnDefinitionUpgrade
import FMetaData
import FExtensionUtils

reload(FAcmMethodsRemoved)
reload(FExtensionAttributeOverride)
reload(FExtensionAttributeRedundant)
reload(FExtensionAttributeRemoved)
reload(FExtensionUnref)
reload(FColumnDefinitionUpgrade)
reload(FMetaData)
reload(FExtensionUtils)

from FHTML import *

def start_scans(scanType, fromVer, toVer, context, users, module, findRef, findAcm,\
        findOverrides, findEqDef, findUnref, upgradeCol, path, reportname, extAttrMapFile):
    
    #If the path doesn't end with a backslash add one
    if path.rfind('\\') != len(path)-1: path += '\\'
    
    #Remove the ending .htm* from reportname
    if reportname.rfind(".htm") >= len(reportname) - len(".htm*"): reportname = reportname[:reportname.rfind(".htm")]
    
    #Create file for excluded definitions    
    if not os.path.exists(path + 'excludedDefinitions.txt'):
        file = open(path + 'excludedDefinitions.txt', 'w')
        file.close()
    
    scanlist = []
    if findRef == 'True':
        scanlist.append("removed extension attributes")
        scanlist.append(", ")
    if findAcm == 'True':       
        scanlist.append("removed and changed ACM methods")
        scanlist.append(", ")
    if findOverrides == 'True' and scanType != 'Per module':
        scanlist.append("overrides")
        scanlist.append(", ")
    if findEqDef == 'True':
        scanlist.append("extension attributes with equal definitions")
        scanlist.append(", ")
    if findUnref == 'True':
        scanlist.append("unreferenced code")
        scanlist.append(", ")
    if upgradeCol == 'True':
        scanlist.append("old column definition type")
        scanlist.append(", ")
    if not scanlist:
        print ("No defined scans, nothing to do")
        return None
    scanlist[-1] = '.'
    if len(scanlist) > 2:
        scanlist[-3] = " and "
    
    if scanType == 'Create definition':
        FMetaData.generate_meta_data(path)
        return None

    elif scanType == 'Per context':
        if not context:
            print ("No context to scan")
            return None            
            
        if len(scanlist) > 2 or len(context) >= 2:
            write_summary_report = True
            try:
                os.mkdir(reportname + "_files")
            except OSError as err:
                if err.errno != 17 and err.errno != 183: #errno 17: File exists,
                                                         #errno 183: winerror file exists
                    print ("Error while creating report file")
                    print ("Error", err.errno, ", ", err.strerror)
                    print ("Aborting script")
                    return None
        else: 
            write_summary_report = False            
        res = []
        if write_summary_report:
            res.append("""<html><head><title> Extension scan in context %s
                </title></head><body bgcolor=ffffff>""" % (context.StringKey(),))               
            res.append("""<h1 title = "Scanned contexts: %s">Extension scan in contexts %s</h1>""" % (str(context), context.StringKey(),) )
            res.append("""Produced on: %s<p>""" % (str(datetime.datetime.now())[0:19],) )
            res.append("""By user: %s<p>""" % (acm.UserName(),) )
            res.append("""ADS: %s<p>""" % (acm.ADSAddress(),) )
            res.append("""The scan was made from version %s to version %s<p>""" % (fromVer, toVer) )
            res.append("<b>The contexts were scanned for ")
            res.extend(scanlist)
            res.append("</b><p>")

        metaData=FMetaData.ACMMetaData(fromVer, toVer, path)

        if findRef == 'True':
            if metaData:
                res.append(FExtensionAttributeRemoved.scan_contexts_and_report(metaData, context, users, reportname, write_summary_report, extAttrMapFile))
            else: print ("Can not scan for removed extension attributes, erroneous version information")
        if findAcm == 'True':
            if metaData:
                res.append(FAcmMethodsRemoved.scan_contexts_and_report(metaData, context, users, reportname, write_summary_report))
            else: print ("Can not scan for removed ACM methods, erroneous version information")
        if findOverrides == 'True':
            res.append(FExtensionAttributeOverride.scan_contexts_and_report(context, users, reportname, write_summary_report))
        if findEqDef == 'True':            
            res.append(FExtensionAttributeRedundant.scan_contexts_and_report(context, users, reportname, write_summary_report))
        if findUnref == 'True':
            res.append(FExtensionUnref.scan_contexts_and_report(context, users, reportname, write_summary_report))
        if upgradeCol == 'True':
            res.append(FColumnDefinitionUpgrade.scan_contexts_and_report(context, users, reportname, write_summary_report))
        if write_summary_report:
            res.append("""</body>""")
            outfile = open(reportname + ".html", 'w')
            outfile.write("".join(res))
            outfile.close()
            reportname += ".html"
        else: reportname = res[-1]
                
            
    elif scanType == 'Per module':
        if not module:
            print ("No module to scan")
            return None
            
        print ("Scanning modules:", module)
        if len(scanlist) > 2:
            write_summary_report = True
            try:
                os.mkdir(reportname + "_files")
            except OSError as err:
                if err.errno != 17 and err.errno != 183: #errno 17: File exists,
                                                         #errno 183: winerror file exists
                    print ("Error while creating file directory")
                    print ("Error", err.errno + ",", err.strerror)
                    print ("Aborting script")
                    return None
        else: write_summary_report = False
        res = []
        if write_summary_report:
            res.append("""<html><head><title> Extension scan in context %s
                </title></head><body bgcolor=ffffff>""" % (module.StringKey(),))
            res.append("""<h1>Extension scan in modules %s</h1>""" % (module.StringKey(),) )
            res.append("""Produced on: %s<p>""" % (str(datetime.datetime.now())[0:19],) )
            res.append("""By user: %s<p>""" % (acm.UserName(),) )
            res.append("""ADS: %s<p>""" % (acm.ADSAddress(),) )
            res.append("""The scan was made from version %s to version %s<p>""" % (fromVer, toVer) )
            res.append("<b>The modules were scanned for ")
            res.extend(scanlist)
            res.append("</b><p>")

        metaData=FMetaData.ACMMetaData(fromVer, toVer, path)

        if findRef == 'True':
            if metaData:
                res.append(FExtensionAttributeRemoved.scan_modules_and_report(metaData, module, reportname, write_summary_report, extAttrMapFile))
            else: print ("Can not scan for removed extension attributes, erroneous version information")
        if findAcm == 'True':
            if metaData:
                res.append(FAcmMethodsRemoved.scan_modules_and_report(metaData, module, reportname, write_summary_report))
            else: print ("Can not scan for removed extension attributes, erroneous version information")
        if findEqDef == 'True':
            res.append(FExtensionAttributeRedundant.scan_modules_and_report(module, reportname, write_summary_report))
        if findUnref == 'True':
            res.append(FExtensionUnref.scan_modules_and_report(module, reportname, write_summary_report))
        if upgradeCol == 'True':
            res.append(FColumnDefinitionUpgrade.scan_modules_and_report(module, reportname, write_summary_report))
        if write_summary_report:
            res.append("""</body>""")
            outfile = open(reportname + ".html", 'w')
            outfile.write("".join(res))
            outfile.close()
            reportname += ".html"
        else: reportname = res[-1]
            
    else:
        print ("Bad call to FExtensionScannerToolController, ", scanType, " is not an allowed call")
        return None
    
    return reportname






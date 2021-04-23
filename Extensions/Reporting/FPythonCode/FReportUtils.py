"""-------------------------------------------------------------------------------------------------------
MODULE
    FReportUtils - Common Utility functions for the Reporting Modules
        
    (c) Copyright 2011 by SunGard Front Arena. All rights reserved.

-------------------------------------------------------------------------------------------------------"""
import acm
import os
import FLogger
from xml.sax.saxutils import escape
import codecs

logger = FLogger.FLogger('FAReporting')

def addHeader(xsl, extraParams):
    try:
        if extraParams.At('headerImage') == 'True':
            headerFile = extraParams.At('headerImagePath')
            headerFileEscaped = escape(str(headerFile))
            return xsl.replace('<headerImage/>', '<img src="' + headerFileEscaped + '"/>')
    except AttributeError:
        pass
    return xsl
        
def addCSS(xsl, replaceCSS, extraParams):
    # Retrieve CSS to use if any and substitute into XSL
    try:
        if replaceCSS:
            outputDir = extraParams.At('outputDir')
            cssObject = acm.GetDefaultContext().GetExtension('FXSLTemplate', 'FObject', replaceCSS)
            if not cssObject:
                logger.WLOG( "Failed to find CSS %s Proceeding without it, output may be malformed", replaceCSS )
            else:
                css = cssObject.Value()
                path = os.path.join(outputDir, replaceCSS + '.css')
                cssFilename = replaceCSS + '.css'
                writeToFile(path, css)
                return xsl.replace('<insertcss/>', '<link rel="stylesheet" type="text/css" href="' + cssFilename + '"/>')
    except AttributeError:
        pass
    return xsl

def transformXML(reportXml, template, replaceCSS=None, extraParams=None):
    # Retrieve stylesheet to use
    pt = acm.GetDefaultContext().GetExtension('FXSLTemplate', 'FObject', template)
    if not pt:
        raise Exception("Failed to find template " + template + " report output not completed")
    xsl = pt.Value()
    xsl = addHeader(xsl, extraParams)
    xsl = addCSS(xsl, replaceCSS, extraParams)
    
    # Perform transformation
    transformer = acm.CreateWithParameter('FXSLTTransform', xsl)
    return transformer.Transform(reportXml)

def preprocess_transform_XML(reportObj, param, XMLreport):
    """ This function can be specified in the FWorksheetReport GUI, Processing tab, preprocess XML."""
    for template in param.split(','):
        logger.LOG( "preprocess_transform_XML: %s", template )
        XMLreport=transformXML(XMLreport, template)
    return XMLreport

def adjust_parameters(aelparams):
    try:
        task_parameters = os.environ["TASK_REPORT_PARAMETER"]
        # the structure is "key=value:key=value....."
        param_list = task_parameters.split(':')
        logger.LOG( "Using Environment variable TASK_REPORT_PARAMETER: %s", task_parameters )
        for keyval in param_list:
            key, val=keyval.split('=')
            value = eval(val)
            aelparams[key] = value
        return aelparams
    except KeyError:
        return aelparams

def GetParameterValues( name ):
    """get values from FParameter by name"""
    values = {}
    p = acm.GetDefaultContext().GetExtension('FParameters', 'FObject', name)
    try:
        template = p.Value()
    except AttributeError as e:
        logger.ELOG( "Error getting parameters ( %s ): %s", name, str( e ) )
    for k in template.Keys():
        k = str(k)
        value = str( template.At(k) )
        values[ str(k) ] = value
    return values
    
def writeToFile(path, content):
    writeToFileMode(path, content, 'w')

def writeToFileMode(path, content, mode, utf16Output = False, useUtf8BOM = False):
    if acm.IsUnicodeEnabled():
        file = open(path.decode("utf-8"), mode)
    else:
        file = open(path, mode)
    if utf16Output:
        file.write(codecs.BOM_UTF16_LE)
        try:
            content = content.decode("utf-8").encode('utf-16-le')
        except AttributeError:#Python3
            content = content.encode('utf-16-le')
            pass
    elif useUtf8BOM:
        file.write(codecs.BOM_UTF8)
    file.write(content)
    file.close()    

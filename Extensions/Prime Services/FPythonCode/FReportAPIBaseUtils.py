"""-------------------------------------------------------------------------------------------------------
MODULE
    FReportAPIBaseUtils - Contains logic for building reports. 
    
    (c) Copyright 2011 by SunGard FRONT ARENA. All rights reserved.

2019-07-31      Upgrade2018     Jaysen Naicker         Force useUtf16Output = False so output is not binary and is same as output from Front 2017

-------------------------------------------------------------------------------------------------------"""

import re
import os
import threading
import zipfile
import webbrowser
import time
from string import Template

import acm
import FFileUtils
import FReportUtils
import FPictures
import FReportSettings
import FLogger
import codecs
try:
    basestring
except NameError: #Python3
    basestring = str

logger = FLogger.FLogger( 'FAReporting' )

def generateReportName(report_generator, tradingSheet, containerName):
    """ Generate a report name based on the trading sheet tab name.
        This is the name visible on the sheet tab in the Trading Manager.            
    """
    #For right-click Portfolio report.
    if report_generator.params.portfolioReportName: 
        report_generator.params.reportName = report_generator.params.portfolioReportName
        return        
    
    if report_generator.isSet(report_generator.params.template) or report_generator.isSet(report_generator.params.workbook):
        report_generator.params.reportName = containerName + "-" + tradingSheet.SheetName()            
    else:
        report_generator.params.reportName = 'sheetReport'


def generateFileName(report_generator, sheets):        
    """ Genereate a file based on workbook name or sheet type
    if the report is created of a trading sheet template.
    """
    if not report_generator.params.fileName:             
        if report_generator.isSet( report_generator.params.template ):
            sheet, templateName = sheets[ 0 ]
            report_generator.params.fileName = sheet.Category() + 'Report'                
            if len( sheets ) > 1:
                report_generator.params.fileName += '_etc'        
        elif report_generator.isSet( report_generator.params.workbook ):  
            report_generator.params.fileName = report_generator.params.workbook.Name()                        
        else:
            report_generator.params.fileName = 'sheetReport'

def getAttributeFromModule(attributeName):                            
    """get a attribute from a python module by string"""
    moduleName, attributeName = attributeName.split('.')
    mod = None
    func = None
    
    mod = getModule( moduleName )        
        
    try:
        attr = mod.__getattribute__(attributeName)
    except Exception as details:
        raise Exception( 'Error getting function: ' + attributeName + ' (' + str( details ) + ')' )
        
    return attr

def getModule(moduleName):                            
    """get a module from a python module by string"""
    
    try:
        mod = __import__(moduleName)
    except Exception as details:
        raise Exception('Error importing module: ' + moduleName + ' (' + str(details) + ')' )            
    
    return mod

def getNewFilePath(report_generator, outputDir, ext):
    fileName = report_generator.params.fileName
    # Add date to file name?
    if report_generator.params.fileDateFormat:
        theFileDateFormat = report_generator.params.fileDateFormat        
        if report_generator.params.yearWithCentury == "True":
            theFileDateFormat = theFileDateFormat.replace('y', 'Y')
        
        if report_generator.params.fileDateBeginning:
            fileName = time.strftime(theFileDateFormat) + fileName
        else:
            fileName = fileName + time.strftime(theFileDateFormat)

    if report_generator.params.overwriteIfFileExists:
        generatedFilePath = os.path.join(outputDir, fileName + ext)
        report_generator.generatedFilePaths.append(generatedFilePath)
        return generatedFilePath
        
    for i in range(1, int(report_generator.params.maxNrOfFilesInDir) + 1):
        if i == 1:
            numbering = ''
        else:
            numbering = '_' + str(i)
        testFile = os.path.join(outputDir, fileName + numbering + ext)
        if not os.path.exists(testFile):
            report_generator.generatedFilePaths.append(testFile)
            return testFile
    msg = 'Maximum number of files in directory has been exceeded! Please change the setting maxNrOfFilesInDir. Current value: ' + str(report_generator.params.maxNrOfFilesInDir)
    logger.ELOG( msg )
    raise Exception(msg)

def createOutputDir(report_generator):
    if isinstance(report_generator.params.filePath, basestring):
        outputDir = report_generator.params.filePath
    else:
        outputDir = report_generator.params.filePath.AsString()
        
    if outputDir == "":
        #Use current directory by default
        outputDir = os.path.abspath(outputDir)
        
    if report_generator.params.createDirectoryWithDate:
        theDateFormat = report_generator.params.dateFormat
        if report_generator.params.yearWithCentury == "True":
            theDateFormat = theDateFormat.replace('y', 'Y')
        outputDir = os.path.join(outputDir, 'report'+ time.strftime(theDateFormat)+ os.sep )

    outputDir = FFileUtils.expandEnvironmentVar(outputDir)

    if report_generator.params.htmlToFile or report_generator.params.secondaryOutput or report_generator.params.xmlToFile:
         if not os.path.exists(outputDir):
            try:
                os.makedirs(outputDir)
                logger.LOG('Created report output directory:' + outputDir)
            except:
                msg = 'Failed to create report directory:' + outputDir
                logger.ELOG( msg )
                raise Exception(msg)
    
    return outputDir

def getTradingSheets( report_generator ):                  
    """returns list of trading sheets"""
    logger.LOG('Starting report creation')            
    sheets = acm.FArray()        
    
    #from template
    if report_generator.isSet(report_generator.params.template):
        logger.LOG('Using trading sheet template(s):')
        for tpl in report_generator.params.template:
            templateName = str( tpl.Name() )
            logger.LOG( '\t' + templateName )
            sheets.Add( ( tpl.TradingSheet(), templateName ) )
    
    #from workbook                       
    if report_generator.isSet(report_generator.params.workbook):
        workbookName = str( report_generator.params.workbook.Name() )
        logger.LOG( 'Using workbook: ' + workbookName )
        for sheet in report_generator.params.workbook.Sheets():
            sheets.Add( ( sheet, workbookName ) )

    if hasattr(report_generator.params, 'sheet'):
        logger.LOG('Using ' + str(report_generator.params.sheet.Size())+ ' additional exported sheet(s).')            
        sheets.AddAll(report_generator.params.sheet)                       
    
    if not sheets:
        msg = 'No sheet found! Please specify a valid trading sheet'
        logger.WLOG(msg)            
        raise Exception(msg)        
    
    return sheets

def createHTML(report_generator, reportXml, outputDir):
    extraParams = acm.FDictionary()
    extraParams.AtPut('outputDir', outputDir)
    extraParams.AtPut('headerImage', report_generator.params.headerImage)
    extraParams.AtPut('headerImagePath', report_generator.params.headerImagePath)
    html = FReportUtils.transformXML(reportXml, report_generator.params.printTemplate, report_generator.params.printStyleSheet, extraParams)
    return html

def writeHTMLToFile(report_generator, reportXml, outputDir):
    html = createHTML(report_generator, reportXml, outputDir)
    #Special treatment of FStandardTemplateClickable
    if report_generator.params.printTemplate.find('Clickable') != -1:
        import FHTMLJavaScript
        jsPath = os.path.join(outputDir, 'portfolio_report.js')
        FReportUtils.writeToFile(jsPath, FHTMLJavaScript.javaScript)            
        pictures = ['report_plus', 'report_minus', 'report_end']
        # Decode any pictures included.
        for pic in pictures:
            FPictures.decodePicture(pic, outputDir)

    filePath = getNewFilePath(report_generator, outputDir, '.html')
    FReportUtils.writeToFile(filePath, html)        
    logger.LOG("Wrote report output to: " + filePath)
    if report_generator.params.htmlToScreen:
        t = threading.Thread( target=webbrowser.open, name='OpenWebBrowser', args=(filePath, 0, 1) )
        t.setDaemon( 1 )
        t.start()
        t.join( timeout=1 )

    if report_generator.params.htmlToPrinter:
        acm.PrintToDefaultPrinter(html, " ", "Page &p of &P  &b At date &d &t &b")
        
def TemplateHasUtf8Encoding(templateName):
    utf8Encoding = False
    template = acm.GetDefaultContext().GetExtension('FXSLTemplate', 'FObject', templateName)
    
    if template:
        utf8Encoding = template.AsString().find('encoding="UTF-8"') != -1
    return utf8Encoding
        
def writeToSecondaryOutput(report_generator, reportXml, outputDir):
    secondOut = FReportUtils.transformXML(reportXml, report_generator.params.secondaryTemplate)

    filePath = getNewFilePath(report_generator, outputDir, report_generator.params.secondaryFileExtension)
    if report_generator.params.secondaryTemplate in report_generator.params.getSecondaryTemplateNames('pdf'):
        foFilePath = filePath.replace(report_generator.params.secondaryFileExtension, ".fo")            
        FReportUtils.writeToFile(foFilePath, secondOut)        
        foFilePath = foFilePath.replace(".fo", "")

        command = Template(FReportSettings.FOP_BAT)
        command = command.substitute({'extension':report_generator.params.secondaryFileExtension[1:], 'filename':foFilePath})
        ret = os.system(command)
        if ret:
            logger.ELOG("Output creation ERROR. Check that necessary third party software is installed.\nCommand: " + command)
        else:
            logger.LOG("PDF generated to " + filePath)
    else:
        # force useUtf16Output = False so output is not binary and is same as output from Front 2017
        #useUtf16Output = report_generator.params.secondaryFileExtension == '.xls' and TemplateHasUtf8Encoding(report_generator.params.secondaryTemplate)
        useUtf16Output = False
        useUtf8Bom = False
        if report_generator.params.useUtf8ByteOrderMark == 1 and TemplateHasUtf8Encoding(report_generator.params.secondaryTemplate):
            useUtf8Bom = True
        FReportUtils.writeToFileMode(filePath, secondOut, 'wb', useUtf16Output, useUtf8Bom)
        logger.LOG("Wrote secondary output to: " + filePath)
        
def writeXMLToFile(report_generator, reportXml, outputDir):
    if report_generator.params.compressXmlOutput:
        filePath = getNewFilePath(report_generator, outputDir, '.zip')
        innerFileName = report_generator.params.fileName + ".xml"
        f = zipfile.ZipFile(filePath, 'w', zipfile.ZIP_DEFLATED).writestr( innerFileName, reportXml )
        logger.LOG("Wrote compressed XML to : " + filePath)
    else:
        filePath = getNewFilePath(report_generator, outputDir, '.xml')
        FReportUtils.writeToFile(filePath, reportXml)                             
        logger.LOG("Wrote XML to : " + filePath)



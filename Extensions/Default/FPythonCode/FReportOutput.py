from __future__ import print_function
"""-------------------------------------------------------------------------------------------------------
MODULE
    FReportOutput - Output reports to paper, file or screen

    Given XML data this module will transofrm it using print templates and output the result
    to file, show it in a web browseer and/or print it to paper.

    (c) Copyright 2011 by SunGard FRONT ARENA. All rights reserved.

DESCRIPTION

    Use produceOutput function to print XML data, append result of getAelCariables to the ael_variables
    in the calling script.
    
    If called from a noninteractive script, produceOutputInternal may be called    

-------------------------------------------------------------------------------------------------------"""

import acm
import ael
import os
import webbrowser
import time
import os.path
import platform
import re
import FFileUtils
import FReportUtils
import FReportSettings
import FXMLReportWriter
import FPictures
from string import Template

try:
    basestring
except NameError: #Python3
    basestring = str

try:
    import zipfile
except ImportError:
    print ("Failed to import zipfile, compressed XML output will not be available")

ael_variables = None #Must be overridden by parent module in order for call backs to work
trueFalse = ['False', 'True']

import amb
amb_address_default = '127.0.0.1:9137'
amb_sender_default  = 'AMBA_SENDER'
amb_subject_default = 'AMBA/XMLREPORT'

def xmlToAmbCB(index, fieldValues):
    for i in (1, 2, 3, 4):
        if (ael_variables) and (len(ael_variables) >= index+i):
            ael_variables[index + i][9] = (fieldValues[index] == 'True')
    return fieldValues

def htmlToFileCB(index, fieldValues):
    if (ael_variables) and (len(ael_variables) > index):
        ael_variables[index - 1][9] = (fieldValues[index] != 'True')
        if fieldValues[index] == 'True':
            fieldValues[index - 1] = 'True'
    return fieldValues
    
def secondaryOutputCB(index, fieldValues):
    for i in (1, 2, 3):
        if (ael_variables) and (len(ael_variables) >= index+i):
            ael_variables[index + i][9] = (fieldValues[index] == 'True')
    return fieldValues

def getFilePathSelection():
    """ Directory selector dialog """
    selection = acm.FFileSelection()
    selection.PickDirectory(True)
    selection.SelectedDirectory = 'c:\\'
    return selection   
    
def createDirectoryWithDatesCB(index, fieldValues):    
    ael_variables[index + 1][9] = trueFalse.index(fieldValues[index])
    return fieldValues  

def getDateFormats():    
    return ['%d%m%y', '%y%m%d', '%d%m%y%H%M', '%y%m%d%H%M']

def setFileExtension(index, fieldValues):    
    """ Set file extension depending on which group the template belongs to """
    secTempl = fieldValues[index]        
        
    for ext in FReportSettings.FILE_EXTENSIONS:
        list = getSecondaryTemplateNames(ext)
        if secTempl in list:
            fieldValues[index+1] = ext            
    return fieldValues      

def getAelVariables():
    """ Get ael_variables that need to be suplied to produceOutput, scripts outputing
        reports should extend their ael_variables with this list
    """
    return     [['Include Raw Data', 'Include Raw Data_Output settings', 'string', trueFalse, 'True', 1, 0, 'Is the raw data needed in the report?'],
                ['Include Formatted Data', 'Include Formatted Data_Output settings', 'string', trueFalse, 'True', 1, 0, 'Is the formatted data needed in the report? Must be checked when using FStandardTemplate.'],
                ['HTML to File', 'HTML to File_Output settings', 'string', trueFalse, 'True', 1, 0, 'Is the HTML wanted on file?', None, 1],
                ['HTML to Screen', 'HTML to Screen_Output settings', 'string', trueFalse, 'True', 1, 0, 'Is the HTML wanted on screen in a browser?', htmlToFileCB, 1],
                ['HTML to Printer', 'HTML to Printer_Output settings', 'string', trueFalse, 'False', 1, 0, 'Is printing of the HTML wanted?'],
                ['XML to File', 'XML to File_Output settings', 'string', trueFalse, 'True', 1, 0, 'Is the XML wanted on file?'],                              
                ['File Path', 'File Path_Output settings', getFilePathSelection(), None, getFilePathSelection(), 0, 1, 'The file path to the directory where the report should be put. Environment variables can be specified for Windows (%VAR%) or Unix ($VAR).', None, 1],                
                ['File Name', 'File Name_Output settings', 'string', None, '', 0, 0, 'The file name of the output'],
                ['Compress Output', 'Compress XML output (.zip)_Output settings', 'string', trueFalse, 'False', 1, 0, 'Compress the .xml outpt with zip', None, 1],
                ['Create directory with date', 'Create directory with date_Output settings', 'string', trueFalse, 'True', 1, 0, 'Create a directory with the date included in the directory name', createDirectoryWithDatesCB, 1],                                
                ['Date format', 'Date format_Output settings', 'string', getDateFormats(), '%d%m%y', 0, 0, 'Date format', None, 1],
                ['Overwrite if file exists', 'Overwrite if file exists_Output settings', 'string', trueFalse, 'True', 1, 0, 'If a file with the same name and path already exist, overwrite it?'],
                ['Print template (XSL)', 'Print template (XSL)_Output settings', 'string', getPrintTemplateNames(), 'FStandardTemplate', 0, 0, 'Choose which XSL template to use in the transformation from XML. Templates must be added to group aef reporting/print templates to be visible here.'],
                ['Print style sheet (CSS)', 'Print style sheet (CSS)_Output settings', 'string', getCSSNames(), 'FStandardCSS', 0, 0, 'If wanted, choose a Cascading Style Sheet'],
                ['Secondary output', 'Secondary output_Output settings', 'string', trueFalse, 'False', 1, 0, 'Is a secondary output wanted?', secondaryOutputCB, 1],
                ['Secondary template', 'Secondary template_Output settings', 'string', getSecondaryTemplateNames(), 'FTABTemplate', 0, 0, 'Choose a secondary output template. Templates must be added to group aef reporting/secondary templates [ext] to be visible here.', setFileExtension, 0],
                ['Secondary file extension', 'Secondary file extension_Output settings', 'string', FReportSettings.FILE_EXTENSIONS, '.xls', 0, 0, 'Which file extension should the secondary output have?', None, 0],
                ['Send XML File to AMB', 'Send XML File to AMB_Output settings', 'string', trueFalse, 'False', 1, 0, 'Send XML File to ARENA Message Broker?', xmlToAmbCB, 1],
                ['AMB XML Message', 'AMB XML Message_Output settings', 'string', trueFalse, 'True', 0, 0, 'XML Message or Front Arena internal format?', None, 1],
                ['AMB Address', 'AMB Address_Output settings', 'string', '', amb_address_default, 0, 0, 'Address to ARENA Message Broker on format host:port', None, 0],
                ['AMB Sender Name', 'AMB Sender Name_Output settings', 'string', '', amb_sender_default, 0, 0, 'Name on Sender to ARENA Message Broker (Must exist in AMB system table!)', None, 0],
                ['AMB Subject', 'AMB Subject_Output settings', 'string', '', amb_subject_default, 0, 0, 'Subject on Messages Sent to ARENA Message Broker', None, 0],
                ] 


def produceOutput(inputXML, fileName, ael_variables):
    """ Produce reports as described in ael_variables """
    fileHTML = trueFalse.index(ael_variables['HTML to File'])
    screenHTML = trueFalse.index(ael_variables['HTML to Screen'])
    printHTML = trueFalse.index(ael_variables['HTML to Printer'])    
    fileXML = trueFalse.index(ael_variables['XML to File'])
    compressXML = trueFalse.index(ael_variables['Compress Output'])
    if isinstance(ael_variables['File Path'], basestring):
        outputDir = ael_variables['File Path']
    else:
        outputDir = ael_variables['File Path'].AsString()    
    dateDirectory = trueFalse.index(ael_variables['Create directory with date'])
    overwrite = trueFalse.index(ael_variables['Overwrite if file exists'])
    printTemplate = ael_variables['Print template (XSL)']
    printCSS = ael_variables['Print style sheet (CSS)']
    secondOutput = trueFalse.index(ael_variables['Secondary output'])
    secondOutputTemplate = ael_variables['Secondary template']
    secondOutputFileExtension = ael_variables['Secondary file extension']
    dateFormat = ael_variables['Date format']
    
    if dateDirectory:
        outputDir = os.path.join(outputDir, 'report'+ time.strftime(dateFormat)+ os.sep )
    produceOutputInternal(inputXML, printTemplate, printCSS, fileHTML, screenHTML, printHTML, fileXML, outputDir,\
                          overwrite, fileName, secondOutput, secondOutputTemplate, secondOutputFileExtension, compressXML)
    # Send XML File to AMB
    xmlToAmb = trueFalse.index(ael_variables['Send XML File to AMB'])
    ambAddress = ael_variables['AMB Address']
    ambSender  = ael_variables['AMB Sender Name']
    ambSubject = ael_variables['AMB Subject']
    ambXmlMessage = trueFalse.index(ael_variables['AMB XML Message'])
    sendXMLToAMB(inputXML, xmlToAmb, ambAddress, ambSender, ambSubject, ambXmlMessage)

def getListFromExtensions(extensions):
    str = extensions.AsString().replace(']', '').replace('[', '').replace(' ', '')
    extensionsList = str.split(',')
    return extensionsList    

def getPrintTemplateNames():
    ctx = acm.GetDefaultContext()
    extensions = ctx.GetAllExtensions('FXSLTemplate', 'FObject', True, True, 'aef reporting', 'print templates')    
    return getListFromExtensions(extensions)        

def getSecondaryTemplateNames(ext = ''):
    if ext != '':        
        ext = ' ' + ext.replace('.', '')
    ctx = acm.GetDefaultContext()
    extensions = ctx.GetAllExtensions('FXSLTemplate', 'FObject', True, True, 'aef reporting', 'secondary templates' + ext)
    return getListFromExtensions(extensions)
    
def getCSSNames():
    ctx = acm.GetDefaultContext()
    extensions = ctx.GetAllExtensions('FXSLTemplate', 'FObject', True, True, 'aef reporting', 'style sheets')
    return getListFromExtensions(extensions)


''' Not used '''
def transformXML(inputXML, printTemplate, printCSS, context):
    if not printTemplate:
        raise Exception("Need to supply an XSL template if printing to HTML")
    # Retrieve stylesheet to use
    pt = context.GetExtension('FXSLTemplate', 'FObject', printTemplate)       
    if not pt:
        raise Exception("Failed to find printTemplate " + printTemplate + " report output not completed")
    xsl = pt.Value()

    # Retrieve CSS to use if any and substitute into XSL
    if printCSS:
        cssObject = context.GetExtension('FXSLTemplate', 'FObject', printCSS)  
        if not cssObject:
            print ("Failed to find CSS ", printCSS, " Proceeding without it, output may be malformed")
        else:
            css = cssObject.Value()
            xsl = xsl.replace('<insertcss/>', css)

    # Perform transformation
    transformer = acm.CreateWithParameter('FXSLTTransform', xsl)
    return transformer.Transform(inputXML)

def produceOutputInternal(inputXML, printTemplate, printCSS, fileHTML, screenHTML, printHTML, fileXML, outputDir,\
                          overwrite, fileName, secondOutput, secondOutputTemplate, secondOutputFileExtension, compressXML, \
                           pictures=[]):
    inputXML = str(inputXML)
    ctx = acm.GetDefaultContext()
    outputDir=FFileUtils.expandEnvironmentVar(outputDir)
    
    if fileHTML or secondOutput or fileXML or screenHTML:
        createPath(outputDir)

    outputDir = os.path.abspath(outputDir)
    
    if fileXML:
        if compressXML:
            filePath = getFileName(outputDir, overwrite, fileName, '.zip')
            innerFileName = fileName + ".xml"
            f = zipfile.ZipFile(filePath, 'w', zipfile.ZIP_DEFLATED).writestr( innerFileName, inputXML ) 
            print ("Wrote compressed XML to : " + filePath)
        else:
            filePath = getFileName(outputDir, overwrite, fileName, '.xml')
            open(filePath, 'w').write(inputXML)
            print ("Wrote XML to : " + filePath)

    if fileHTML or screenHTML or printHTML:
        extraParams = acm.FDictionary()
        extraParams.AtPut('outputDir', outputDir)
        html = FReportUtils.transformXML(inputXML, printTemplate, printCSS, extraParams)
        #Special treatment of FStandardTemplateClickable
        if printTemplate.find('Clickable') != -1:
            import FHTMLJavaScript
            open(outputDir + 'portfolio_report.js', 'w').write(FHTMLJavaScript.javaScript)
            pictures = ['report_plus', 'report_minus', 'report_end']

        # Decode any pictures included.
        for pic in pictures:
            FPictures.decodePicture(pic, outputDir)
        # Output as specified
        if fileHTML or screenHTML:
            filePath = getFileName(outputDir, overwrite, fileName, '.html')
            open(filePath, 'w').write(html)
            print ("Wrote report output to " + filePath)
            if screenHTML:
                webbrowser.open(filePath)
        if printHTML:
            acm.PrintToDefaultPrinter(html, " ", "Page &p of &P  &b At date &d &t &b")

    if secondOutput:
        secondOut = FReportUtils.transformXML(inputXML, secondOutputTemplate)

        fileName = fileName.replace(" ", "_")         
        filePath = getFileName(outputDir, overwrite, fileName, secondOutputFileExtension)
        if secondOutputFileExtension == '.pdf':        
            foFilePath = filePath.replace(".pdf", ".fo")
            open(foFilePath, 'w').write(secondOut)
            print ("Wrote .fo to ", foFilePath)

            foFilePath = foFilePath.replace(".fo", "")
            command = Template(FReportSettings.FOP_BAT)
            command = command.substitute({'extension':'pdf', 'filename':foFilePath})
            ret = os.system(command)
            if ret:
                logger.ELOG("PDF creation ERROR. Check that necessary third party software is installed.\nCommand: " + command)
            else:
                logger.LOG("PDF generated to " + filePath)
        else:
            open(filePath, 'wb').write(secondOut)
            print ("Wrote secondary output to :", filePath)
    

def createPath(outputDir):
    if not os.path.exists(outputDir):
        try:
            os.makedirs(outputDir)
            print ('Created report output directory:', outputDir)
        except:
            print ('Failed to create report directory:' + outputDir)
            raise
                        
def getFileName(outputDir, overwrite, fileName, ext):
    for i in range(1, 100):
        if i == 1:
            numbering = ''
        else:
            numbering = '_' + str(i)
        testFile = os.path.join(outputDir, fileName + numbering + ext)
        if overwrite or not os.path.exists(testFile):
            return testFile
    print ('Error! Directory full')
    return 0

def make_xmlreportwriter(aelvardict):
    """Create a suitable FXMLREportWriter object for report output.

    Arguments:
        aelvardict -- dict from ael_variables should contain the values
                      from getAelVariables() in this module.
    """
    return FXMLReportWriter.FXMLReportWriter.make_iostring_writer()

def event_cb(channel, event_p, *arg_p):
    """Callback function"""
    etype=amb.mb_event_type_to_string(event_p.event_type)
    if etype == 'Status':
        ael.log('AMB Last Acknowledge Status = %s' % event_p.status.status)
        print ('AMB Last Acknowledge Status = %s' % event_p.status.status)
    elif etype == 'Message':
        ael.log('AMB Message Id      : %s' % str(event_p.message.id))
        ael.log('AMB Message Subject : %s' % str(event_p.message.subject))
        ael.log('AMB Message Time    : %s' % str(event_p.message.time))
        ael.log('AMB Message Size    : %s' % str(event_p.message.size))
        ael.log('AMB Message Type    : %s' % str(event_p.message.event_type))
        
        print ('AMB Message Id      : %s' % str(event_p.message.id))
        print ('AMB Message Subject : %s' % str(event_p.message.subject))
        print ('AMB Message Time    : %s' % str(event_p.message.time))
        print ('AMB Message Size    : %s' % str(event_p.message.size))
        print ('AMB Message Type    : %s' % str(event_p.message.event_type))
        buffer = amb.mbf_create_buffer_from_data(event_p.message.data_p)
        message = buffer.mbf_read().mbf_object_to_string_xml()
        ael.log('AMB Message Data XML: \n%s' % message)
        print ('AMB Message Data XML: \n%s' % message)
        amb.mb_queue_accept(channel, event_p.message, time.strftime("%Y-%m-%d %H:%M:%S"))
    elif etype == 'Disconnect':
        ael.log("Event Disconnect")
        print ("Event Disconnect")
    elif etype == 'End of Data':
        ael.log('AMB End of Data')
        print ('AMB End of Data')
    else:
        ael.log('AMB Unknown event type =' % etype)
        print ('AMB Unknown event type =' % etype)

def sendXMLToAMB(inputXML, xmlToAmb, ambAddress, ambSender, ambSubject, ambXmlMessage):
    """ Send xml data file to AMB """
    if xmlToAmb:
        # connect to AMB
        try:
            amb.mb_init(ambAddress)
        except Exception as err:
            ael.log('ERROR: ' + str(err) + '\nOccured when trying to connect to AMB at %s' % ambAddress)
            print ('ERROR: ', err, '\nOccured when trying to connect to AMB at %s' % ambAddress)
            return
        # create writer channel
        try:
            writer = amb.mb_queue_init_writer(ambSender, event_cb, None)
        except Exception as err:
            ael.log('ERROR: ' + str(err) + '\nOccured when trying to create writer channel for sender %s' % ambSender)
            print ('ERROR: ', err, '\nOccured when trying to create writer channel for sender %s' % ambSender)
            return
            
        try:
            # Create XML Report AMB messages
            message = amb.mbf_start_message( None, "INSERT_XMLREPORT", "1.0", None, ambSender )
    
            # Start XMLREPORT list
            mb_msg = message.mbf_start_list("XMLREPORT")
    
            # Insert XML Report as REPORT_DATA
            mb_msg.mbf_add_string("REPORT_DATA", inputXML)
    
            # End XMLREPORT list
            mb_msg.mbf_end_list()
    
            # End XML Report AMB message
            message.mbf_end_message()
        except Exception as err:
            ael.log('ERROR: ' + str(err) + '\nOccured when trying to create AMBA message')
            print ('ERROR: ', err, '\nOccured when trying to create AMBA message')
            return

        try:
            # Create AMB Buffer
            buffer = amb.mbf_create_buffer()
        except Exception as err:
            ael.log('ERROR: ' + str(err) + '\nOccured when trying to create buffer for the XML message')
            print ('ERROR: ', err, '\nOccured when trying to create buffer for the XML message')
            return
            
        try:
            # mbf_generate(buffer) will compress the message if it's greater than 64Kb in size        
            type = 'AMB'
            if ambXmlMessage:
                # mbf_generate_xml generates messages on XML format
                message.mbf_generate_xml(buffer) 
                type = 'XML' 
            else:
                # mbf_generate generates messages on FRONT internal AMB format
                message.mbf_generate(buffer)           
        except Exception as err:
            ael.log('ERROR: ' + str(err) + '\nOccured when trying to generate the ' + type + ' message')
            print ('ERROR: ', err, '\nOccured when trying to generate ' + type + ' message')
            return

        # send the XML message to the AMB
        status = amb.mb_queue_write(writer, ambSubject, buffer.mbf_get_buffer_data(), buffer.mbf_get_buffer_data_size(), time.strftime("%Y-%m-%d %H:%M:%S"))
        # check the status
        if status:
            ael.log("ERROR: ould not send the XML message to the AMB")
            print ("ERROR: could not send the XML message to the AMB")
        else:
            ael.log("XML report sent to AMB %s" % ambAddress)
            print ("XML report sent to AMB %s" % ambAddress)


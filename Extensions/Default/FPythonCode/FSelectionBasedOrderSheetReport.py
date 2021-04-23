"""-------------------------------------------------------------------------------------------------------
MODULE
    FSelectionBasedOrderSheetReport - Create report given a selection of orders
    
    (c) Copyright 2011 by SunGard FRONT ARENA. All rights reserved.

DESCRIPTION
    
    This module makes it possible to create order sheet reports
    based on a selection of orders defined by the user.

-------------------------------------------------------------------------------------------------------"""


import acm
import FOutputSettingsTab
import FReportAPI

falseTrue = ['False', 'True']
report = FReportAPI.FWorksheetReportParameters()
ael_variables = FOutputSettingsTab.getAelVariables()
FOutputSettingsTab.ael_variables = ael_variables

def ael_main_ex(variableDictionary, additionalData):

    # Get additional data dictionary
    customDataDict = additionalData.At('customData')
    
    #Get template and selection from user           
    report.template = customDataDict['template']
    if customDataDict['orders']:
        report.clearSheetContent = True
        report.addOrders = True
        report.orders = customDataDict['orders']
            
    #Output settings tab ------------------------
    report.htmlToFile = falseTrue.index(variableDictionary['HTML to File'])
    report.htmlToScreen = falseTrue.index(variableDictionary['HTML to Screen'])
    report.htmlToPrinter = falseTrue.index(variableDictionary['HTML to Printer'])
    report.filePath = variableDictionary['File Path']
    report.fileName = variableDictionary['File Name']
    report.createDirectoryWithDate = falseTrue.index(variableDictionary['Create directory with date'])
    report.dateFormat = variableDictionary['Date format']
    report.overwriteIfFileExists = falseTrue.index(variableDictionary['Overwrite if file exists'])
    report.printTemplate = variableDictionary['Print template (XSL)']
    report.printStyleSheet = variableDictionary['Print style sheet (CSS)']    
    report.secondaryOutput = falseTrue.index(variableDictionary['Secondary output'])
    report.secondaryTemplate = variableDictionary['Secondary template']
    report.secondaryFileExtension = variableDictionary['Secondary file extension']

    report.RunScript()

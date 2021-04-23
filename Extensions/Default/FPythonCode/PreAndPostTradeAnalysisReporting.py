
"""-------------------------------------------------------------------------------------------------------
MODULE
    PreAndPostTradeAnalysisReporting - Create report for Pre and Post Trade Analysis
    
    (c) Copyright 2011 by SunGard FRONT ARENA. All rights reserved.

DESCRIPTION
    
    This module makes it possible to create pre and post trade analysis reports
    based on a selection of orders defined by the user.

-------------------------------------------------------------------------------------------------------"""

import ael
import acm

import FReportAPI
import importlib
importlib.reload(FReportAPI)


# Callbacks from Menu Extensions
def createReport_PreTradeAnalysis(invokationInfo):
    createReport(invokationInfo, "PreTradeAnalysis", "_defaultPreAndPostTradeAnalysisColumns")
    
def createReport_PostTradeAnalysis(invokationInfo):
    createReport(invokationInfo, "PostTradeAnalysis", "_defaultPostTradeAnalysisColumns")
    
def createReport_PreAndPostTradeAnalysis(invokationInfo):
    createReport(invokationInfo, "PreAndPostTradeAnalysis", "_defaultPreAndPostTradeAnalysisColumns")


# Create the selection of orders and select a sheet template to use in the report
def createReport(invokationInfo, templateName, defaultColumnsExtensionName):

    # Get selection of orders
    selectedOrders = invokationInfo.ExtensionObject().ActiveSheet().Selection().SelectedOrders()

    if selectedOrders and selectedOrders.Size() > 0:

        # Search for template created by current user
        template = acm.FTradingSheetTemplate.Select01("name='%s' and user='%s'" % (templateName, acm.User().Name()), '')

        if (template):
            ael.log("Using existing template created by current user")
            
        else:
            # Search for shared template (user=0)
            template = acm.FTradingSheetTemplate.Select01("name='%s' and user=''" % (templateName), '')
        
            if (template):
                ael.log("Using existing shared template")
        
            else:
                # Create template if it do not exist
                defaultColumns = str(acm.GetStandardExtension('FExtensionAttribute', 'FOrderSheet', defaultColumnsExtensionName).Blueprint())
            
                # Strip quotes (") in beginning and end of string
                defaultColumns = defaultColumns[1:-1]

                ael.log("Creating default sheet template with columns " + defaultColumns)

                gridBuilder = invokationInfo.ExtensionObject().ActiveSheet().GridBuilder()
                template = gridBuilder.MakeSheetTemplate(templateName, defaultColumns)
            
        runReport(selectedOrders, template)
        
    else:
        ael.log("No orders selected")


# Create the report based on the orders and template
def runReport(orders, template):

    additionalData = acm.FDictionary()
    additionalData['orders'] = orders 
    additionalData['template'] = template 
    
    # Calls FSelectionBasedWorksheetReport.ael_main_ex
    acm.RunModuleWithParametersAndData('FSelectionBasedOrderSheetReport', acm.GetDefaultContext(), additionalData)

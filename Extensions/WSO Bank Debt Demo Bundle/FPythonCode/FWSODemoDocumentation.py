""" Compiled: 2020-09-18 10:38:51 """

#__src_file__ = "extensions/BankDebtWSODemoBundle/etc/FWSODemoDocumentation.py"
"""-------------------------------------------------------------------------------------------------------
MODULE
    FWSODemoDocumentation - 

    (c) Copyright 2015 SunGard FRONT ARENA. All rights reserved.

DESCRIPTION
    Related documentation associated with the bundle.
    
-------------------------------------------------------------------------------------------------------"""

import FAssetManagementUtils
logger = FAssetManagementUtils.GetLogger()


docHeader  = """ ---------- Instructions on how to use the WSO Bank Debt Demo Bundle ----------"""
helpHeader = """ ---------- WSO Bank Debt Demo Bundle Help ----------"""

docString = """\n 
            The WSO Bank Debt solution comes with a demo bundle in PRIME 2015.4 and all subsequent releases. The bundle is a ready-to-go demo box 
            that can be deployed with almost no initial configuration at all - the bundle has been highly optimized with respect to user friendliness. 
            It is still however recommended to skim through the associated FCA User Guide: WSO Bank Debt before using the bundle.

            Note that the demo bundle specific features can be found on the Extension Manager menu tab WSO Bank Debt Demo Bundle.

            1.	Setup
            To run the bundle, follow the steps given below.
            *	Load the modules Upload Base, WSO Bank Debt, and WSO Bank Debt Demo Bundle
            *   Save the extension context and restart PRIME
            *	Run the initialization script FWSOBankDebtSetup. It is easily accessed from Extension Manager -> WSO Bank Debt Demo Bundle -> Setup.
            *	You are now all set!

            Using the built-in and the easiest setup possible, the bundle should now work out of the box. If you have read the associated user guide, 
            it could be worth noting that the default file path is generated on the fly if it does not exist. Moreover, the demo bundle automatically 
            populates the directory with the needed XML files before uploads are run. 

            2.	Usage
            The WSO Bank Debt Demo Bundle module contains two uploads, an initial upload and a subsequent upload. The first upload loads the ADS with 
            new instruments, trades, business processes, etc, whereas the second upload shows a set of discrepancies that emerge after the second upload. 
            The purpose of the second upload is to demonstrate a daily operations process workflow. To inspect the modelling of bank debt instruments, 
            it is enough to run the first upload. 
            
            From the Extension Manager, locate the menu category WSO Bank Debt Demo Bundle to find two kinds of uploads. Each such upload performs 
            a complete facility, contract, and trade upload using different XML files. Most of the XML files in the two uploads are equivalent except 
            for the trade XMLs. By default, a second upload will only generate trade related discrepancies.
            
            The WSO Bank Debt Demo Bundle is a good tool for getting a sense of how the Front Arena WSO Bank Debt solution behaves under operation. 
            Try out different custom mappings, test the operational capabilities in the Operations Manager, inspect the created instruments, 
            and possibly also use your own data upload specifications (see 3. Additionals).

            3.	Additionals
            There is however a possibility to extend the behavior of the bundle. In the Python module FWSODemoUploadSpecifications, it is possible to 
            append WSO types to the variable WSO_COMPARISON_TYPES. By adding AssetBase and/or Contract to the array, discrepancies will additionally 
            be generated for the facility and/or contract upload(s). The XML files are stored as type FExtensionValue.

            It is also possible to change the set of input parameters in a given upload. Implementing the hook ParamsDictFromHook in FWSODemoHooks 
            it is possible to e.g. modify the parameters that are otherwise specified in the run script GUI FWSOUpload. 

            Additionally, if the built in upload specifications are not to be used, make sure to point out any user created 
            specifications by substituting the default specifications in the array WSO_UPLOAD_SPECS in the aforementioned module FWSODemoUploadSpecifications. 
            """

helpDocString = """\n 
            Obs: The following note is solely a possible WSO Bank Debt Demo Bundle issue.
            
            The WSO files (extension type FExtensionValue) used in the WSO Bank Demo Bundle assume an ISO 8601 datetime format. Using a different 
            regional datetime format (Control Panel > Region and language) will cause all trades in the trade upload to fall into the state of Discrepancy. 
            Normally, this is not an issue since these issues are taken care of in the data upload specification during deployment; then each incoming file 
            attribute is mapped to a given data type (refer to the Data Upload Manager UI). '
            """


def OutputDocumentation(eii):
    logger.info('WSO Demo Bundle log: %s \n %s' % (docHeader, docString))    

def OutputHelp(eii):
    logger.info('WSO Demo Bundle log: %s \n %s' % (helpHeader, helpDocString))    
""" Compiled: 2020-09-18 10:38:51 """

#__src_file__ = "extensions/BankDebtWSODemoBundle/etc/FWSODemoUploadSpecifications.py"
"""-------------------------------------------------------------------------------------------------------
MODULE
    FWSODemoUploadSpecifications - 

    (c) Copyright 2015 SunGard FRONT ARENA. All rights reserved.

DESCRIPTION
    User defined upload specifications unique for the demo bundle. 

    i) WSO_COMPARISON_TYPES: Used to determine which XML file of a given 
    WSO type to use in any second upload trial (facility/contract/trade)*. 
    
    * For currency differences for facilities, use AssetBase since
    the currency denomination is fetched from the AssetBase XML.
    
    Example 1:
        # Use the XML file WSODemoTrade2XML in the second upload to look
        for trade discrepancies.
        
        WSO_COMPARISON_TYPES = ['Trade',]
        
    Example 2:
        # Use the XML files WSODemoTrade2XML and WSODemoAssetBase2XML in the second upload
        to look for trade and facility currency discrepancies (see attached footnote above).
        
        WSO_COMPARISON_TYPES = ['AssetBase', 'Trade',]
        
    ii) WSO_UPLOAD_SPECS: The upload specifications to use in each upload. Only override this 
                          list if you want to use your own upload specifications.
    
    
-------------------------------------------------------------------------------------------------------"""

'''The set of XML files to substitute in the second upload for comparison purposes.'''
WSO_COMPARISON_TYPES = ['Trade',]

''' The three partial uploads to be completed. '''
WSO_UPLOAD_SPECS = ['WSO Upload Facility Template',
                    'WSO Upload Contract Template', 
                    'WSO Upload Trade Template',]     
""" Compiled: 2020-09-18 10:38:51 """

#__src_file__ = "extensions/BankDebtWSO/etc/FWSOCustomHooks.py"
"""-------------------------------------------------------------------------------------------------------
MODULE
    FWSOCustomHooks -

    (c) Copyright 2015 SunGard FRONT ARENA. All rights reserved.

DESCRIPTION
    Custom hooks.

    Currently supported hooks:
    
    - WSO File Type Identification
        Specifies how the different WSO files in the given 
        directory can be identified.
        Signature: WSOFilesInDir(dirPath)
        Returns: A dictionary. The keys are the WSO file types 
                 (Facility, Trade etc.) and the values are the 
                 absolute file paths to each corresponding XML.
    
    - Combination Name
        The name of the combination to be stored.
        Signature: CombinationName(assetBaseDict)
        Returns: The name of the combination (string).
    
    - Combination Issuer Name
        The issuer of the combination.
        Signature: CombinationIssuerName(assetBaseDict, facilityDict)
        Returns: The name of the FParty-instance (string).
    
    - Combination Category Name
        The category of the combination.
        Signature: CombinationCategoryName(assetBaseDict)
        Returns: The name of a category item (string)

    - FRN Rate Index Name
        The float rate reference of the FRN.
        Signature: RateIndexName(contractDict)
        Returns: The name of the FRateIndex-instance (string).
    
    - FRN Issuer Name
        The issuer of the FRN.
        Signature: FrnIssuerName(contractDict)
        Returns: The name of the FParty-instance (string).
    
    - FRN Category Name
        The category of the FRN.
        Signature: FrnCategoryName(contractDict)
        Returns: The name of a category item (string)

    - Post Upload Facility
        Hook giving access to the reconciliation instance after a combination upload 
        has finished.
        Signature: PostUploadFacility(reconInstance)
        Returns N/A

    - Post Upload Contract
        Hook giving access to the reconciliation instance after an FRN upload has finished.
        Signature: PostUploadContract(reconInstance)
        Returns: N/A

    - Post Upload Trade
        Hook giving access to the reconciliation instance after a trade upload has finished.
        Signature: PostUploadTrade(reconInstance)
        Returns: N/A

-------------------------------------------------------------------------------------------------------"""


""" Compiled: 2020-09-18 10:38:51 """

#__src_file__ = "extensions/BankDebtWSODemoBundle/etc/FWSODemoUploadManager.py"
"""--------------------------------------------------------------------------
MODULE
    FWSOUpload

    (c) Copyright 2015 SunGard FRONT ARENA. All rights reserved.

DESCRIPTION
    
-----------------------------------------------------------------------------"""

from FWSOUploadFileHandler import WSOUploadFileHandler
from FWSOUpload import RunUploadBasedOnParams
from FWSODemoUtils import ParamsDict, LaunchTradingManagerWithContents, ValidateAndCreateMappingObjects
from FWSOBankDebtSetup import RunSetup

import FAssetManagementUtils
logger = FAssetManagementUtils.GetLogger()

try:
    from FWSODemoUploadSpecifications import WSO_COMPARISON_TYPES, WSO_UPLOAD_SPECS
except ImportError as e:
    raise Exception('WSO Demo Bundle log: Could not import the global variables WSO_COMPARISON_TYPES \
                     and/or WSO_UPLOAD_SPECS. Check implementation.')

assert isinstance(WSO_COMPARISON_TYPES, list) and isinstance(WSO_UPLOAD_SPECS, list)

    
def Initialize(eii):
    RunSetup()

def RunUploads(eii):
    logger.info('WSO Demo Bundle log: Running WSO Bank Debt Demo Bundle data upload.')
    uploadName = eii.MenuExtension().Name().AsString().strip()
    PrepareUpload(uploadName)
    for wsoUploadSpec in WSO_UPLOAD_SPECS:
        RunSingleUpload(wsoUploadSpec)
    WSOUploadFileHandler.DeleteAllFilesInDirectory()
    logger.info('WSO Demo Bundle log: WSO Bank Debt Demo Bundle data upload processing complete.')
    LaunchTradingManagerWithContents()
    
def PrepareUpload(uploadName):
    ValidateAndCreateMappingObjects()
    WSOUploadFileHandler.WriteInputDataToFileSystem(uploadName, WSO_COMPARISON_TYPES)
    
def RunSingleUpload(wsoUploadSpec):
    paramsDict = ParamsDict(wsoUploadSpec)   
    RunUploadBasedOnParams(paramsDict) 
""" Compiled: 2020-09-18 10:38:51 """

#__src_file__ = "extensions/BankDebtWSO/etc/FWSOPostUpload.py"
"""-------------------------------------------------------------------------------------------------------
MODULE
    FWSOPostUpload -

    (c) Copyright 2015 SunGard FRONT ARENA. All rights reserved.

DESCRIPTION

-------------------------------------------------------------------------------------------------------"""

import acm
from FWSODictAccessor import WSODictAccessor
from FWSOPostUploadContractHandler import PostUploadContractHandler
from FWSOUtils import WsoLogger

logger = WsoLogger.GetLogger()


class CombInstrMapHandler(object):

    def __init__(self, combination):
        self.combination = combination

    def _GetCombInstrMap(self, frnContract):
        for combInstrMap in self.combination.InstrumentMaps():
            if not combInstrMap.Instrument():
                raise Exception('Combination %s with map %s has no FRN.' % (self.combination.Name(), combInstrMap.Oid()))
            if combInstrMap.Instrument().Name() == frnContract.Name():
                return combInstrMap
        return None

    def _CreateCombInstrMap(self, frnContract):
        combInstrMap = self.combination.AddInstrument(frnContract, 1.0)
        return combInstrMap

    def _UpdateCombInstrMap(self, combInstrMap, frnContract):
        combInstrMap.DefaultDate(frnContract.StartDate())
        combInstrMap.AuctioningDate(frnContract.EndDate())
        combInstrMap.SettlementDate('9999-12-31')
        return combInstrMap

    def RemoveNonExistingMapsFromCombination(self, frns):
        combInstrMaps = self.combination.InstrumentMaps()
        for combInstrMap in combInstrMaps:
            if combInstrMap.Instrument() not in frns:
                try:
                    combInstrMap.Delete()
                    logger.debug('Deleted instrument map from combination %s.'% self.combination.Name())
                except Exception as e:
                    logger.error('Unable to delete instrument map from combination %s: %s'% (self.combination.Name(), e))
                    continue

    def AddOrUpdateFrnContractsToCombination(self, frnContracts):
        logger.info('Adding/updating FRN links.')
        for frnContract in frnContracts:
            if not frnContract or frnContract.IsInfant():
                continue
            try:
                combInstrMap = self._GetCombInstrMap(frnContract)
                if not combInstrMap:
                    combInstrMap = self._CreateCombInstrMap(frnContract)
                combInstrMap = self._UpdateCombInstrMap(combInstrMap, frnContract)
                combInstrMap.Commit()
                logger.info('Successfully added/updated link between FRN %s and combination %s.' % (frnContract.Name(),  self.combination.Name()))
            except Exception as e:
                logger.info('Unable to update instrument map for frn from combination %s: %s'% (self.combination.Name(), e))
                continue
        self.combination.Commit()


class OldCombinationLinkRemover(object):
    ''' Removes old combination links (those no) '''
    
    def _ContractIdOfFrn(self, frn):
        try:
            externalId = frn.ExternalId1()
            contractId = (externalId.split('WSO_Contract_'))[1]
            return contractId
        except Exception:
            return None

    def _ContractIds(self):
        accessor = WSODictAccessor()
        contractsDict = accessor.Contract()
        contractIds = contractsDict.keys()
        return contractIds

    def _IsFrnInXml(self, frn):
        contractId = self._ContractIdOfFrn(frn)
        if contractId in self._ContractIds():
            return True
        return False

    def _FrnsOfCombinationInXml(self, combination):
        frnsInXml = list()
        frns = combination.Instruments()
        for frn in frns:
            if self._IsFrnInXml(frn):
                frnsInXml.append(frn)
        return frnsInXml

    def RemoveOldLinks(self, combination):
        if not combination:
            return None
        frnsInXml = self._FrnsOfCombinationInXml(combination)
        instrMapHandler = CombInstrMapHandler(combination)
        instrMapHandler.RemoveNonExistingMapsFromCombination(frnsInXml)


class CombinationRetriever(object):
    ''' Takes a facilityId and tries to find
        a matching combination in the ADS, based on
        externalId1.
    '''
    
    def __init__(self, facilityId):
        self.facilityId = facilityId

    def _FacilityDict(self):
        ''' Retrieves Facility dict using facilityId '''
        accessor = WSODictAccessor()
        facilitiesDict = accessor.Facility()
        facilityDict = facilitiesDict.get(self.facilityId)
        return facilityDict

    def _AssetId(self):
        ''' Gets assetId from facilityDict '''
        facilityDict = self._FacilityDict()
        if not facilityDict:
            return None
        assetId = facilityDict.get('Facility_Asset_ID')
        return assetId
    
    def _ExternalId1(self):
        assetId = self._AssetId()
        if not assetId:
            return None
        return 'WSO_Facility_%s' % assetId
    
    def _CombinationByExternalId1(self):
        externalId1 = self._ExternalId1()
        if not externalId1:
            return None
        return acm.FCombination.Select01('externalId1 = "%s"' % externalId1, None)
        
    def CombinationInAds(self):
        return self._CombinationByExternalId1()


class CombLinkMaintainer(object):

    def _CombinationOfReconItem(self, reconItem):
        evDict = reconItem.ExternalValues()
        facilityId = evDict['Contract_Facility_ID']
        retriever = CombinationRetriever(facilityId)
        combination = retriever.CombinationInAds()
        return combination

    def _CombinationToFrnsDict(self, reconItems):
        combinationToFrns = dict()
        for reconItem in reconItems:
            frn = reconItem.Subject()
            if not frn:
                continue
            combination = self._CombinationOfReconItem(reconItem)
            if not combination:
                continue
            key = combination
            valueToAppend = frn
            if not combinationToFrns.get(key):
                combinationToFrns[key] = list()
            (combinationToFrns[key]).append(valueToAppend)
        return combinationToFrns


    def _AddNewLinks(self, combination, frns):
        if not combination:
            return None
        instrMapHandler = CombInstrMapHandler(combination)
        instrMapHandler.AddOrUpdateFrnContractsToCombination(frns)
        
    def AddNewCombLinksInReconInstance(self, reconInstance):
        if not reconInstance:
            return None
        reconItems = reconInstance.ReconciliationItems()
        combinationToFrnsDict = self._CombinationToFrnsDict(reconItems)
        for combination, frns in combinationToFrnsDict.items():
            try:
                self._AddNewLinks(combination, frns)
            except Exception as e:
                logger.error(e)
                continue
            
    def RemoveOldCombLinksInReconInstance(self, reconInstance):
        ''' Removes comb links not in the current Contract XML '''
        if not reconInstance:
            return None
        reconItems = reconInstance.ReconciliationItems()
        for reconItem in reconItems:
            combination = reconItem.Subject()
            if not combination:
                continue
            linkRemover = OldCombinationLinkRemover()
            linkRemover.RemoveOldLinks(combination)
            
            
class PostUploadContract(object):

    @classmethod
    def PostUploadContractInitiator(cls, reconInstance):
        if not reconInstance:
            return None
        reconItems = reconInstance.ReconciliationItems()
        for reconItem in reconItems:
            frn = reconItem.Subject()
            if (not frn) or frn.IsInfant():
                continue
            logger.info('Running WSO Contract post upload hook for FRN %s...' % frn.Name())
            postUploadContractHandler = PostUploadContractHandler(frn)
            try:
                postUploadContractHandler.Run()
            except Exception as e:
                logger.error('A post upload error occurred for FRN %s: %s' % (frn.Name(), str(e)))
                continue
            logger.info('Successfully finished WSO Contract post upload hook for FRN %s.' % frn.Name())

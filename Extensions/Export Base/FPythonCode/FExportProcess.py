""" Compiled: 2020-09-18 10:38:52 """

#__src_file__ = "extensions/export/./etc/FExportProcess.py"
from __future__ import print_function
"""-------------------------------------------------------------------------------------------------------
MODULE
    FExportProcess

    (c) Copyright 2012 SunGard FRONT ARENA. All rights reserved.

DESCRIPTION
    See ExportBaseReadMe.py for more information about this module

-------------------------------------------------------------------------------------------------------"""
import itertools

import acm
import FAssetManagementUtils
import FBusinessProcessUtils
import FExportUtils
import FSingleExportIdentifier

logger = FAssetManagementUtils.GetLogger()


class FExportKeyEnum():
    #Keys on which we group the BPs for export
    FILTERNAME = 0
    PARTYNAME  = 1


class FExportProcess():

    def __init__(self, integrationInstance, ACMTradeQueryIdList, additionalQueryDictionary=dict(),
                 additionalParameters=None, testMode=FExportUtils.ExportTestMode(), alwaysGenerateFile='false'):
        """
        TradeQueryIdList is a list of ACM query id's that will filter what trades to export.
        additionalQueryDictionary is a dictionary like (identifier:queryidlist) that filters what kind of
        additional objects to export, e.g. ('instruments_to_export':('All_Stocks', 'All_Bonds'))
        additionalParameters can be any additional data to be made available to export processing
        callbacks (e.g. user options)

        """
        # pylint: disable-msg=W0102
        assert(integrationInstance)
        if additionalParameters != None:
            try:
                integrationInstance.SetPartyFunction(additionalParameters.Party)
                integrationInstance.SetEnableGUI(additionalParameters.UseGUIParty)
            except AttributeError:
                print("Missing additionalParameters from Runscript - Can't use runscript party selection")

        self._integration = integrationInstance
        self._singleExport = dict()
        self._ACMTradeQueryIdList = ACMTradeQueryIdList
        self._additionalQueryDictionary = additionalQueryDictionary
        self._additionalParameters = additionalParameters
        self._testMode = testMode
        self._alwaysGenerateFile = alwaysGenerateFile
        
    def GenerateEmptyFile(self):
        return self._alwaysGenerateFile == 'true'

    def SingleExportsAsList(self):
        list_export = self._singleExport.values()
        i = 0
        for key in self._singleExport.keys():
            if 'Instrument' in str(key):
                list_export[i], list_export[0] = list_export[0], list_export[i]
            i = i + 1
        return list_export

    def Integration(self):
        """Each FExportProcess is linked to exactly one FIntegration instance."""
        return self._integration

    def TestMode(self):
        """Returns test mode options for this export."""
        return self._testMode

    def TradeQueryIdList(self):
        """Returns the list of trade queries that were feed into the export process."""
        return self._ACMTradeQueryIdList

    def AdditionalParameters(self):
        """Returns additional export processing parameters."""
        return self._additionalParameters

    def AdditionalQueryDictionary(self):
        return self._additionalQueryDictionary

    def BusinessProcesses(self):
        """Returns a list of all export business processes processed by the export process."""
        return list(itertools.chain.from_iterable([export.BusinessProcesses() for _key, export in self]))

    def LoadLinkedObjects(self, trade):
        """
        This method will try to include BPs which are linked to the trades being
        exported via the LinkedExportObjects method on the FIntegration instance.
        It is automatically called upon as part of the general LoadBusinessProcesses method.
        """
        BPLoaded = 0
        for linkFunction, stateChartId, exportObjectId in self.Integration().LinkedExportObjects():
            logger.debug('Loading business processes for extended objects: %s...', exportObjectId)
            linkBP = self._FindMatchingLinkedBP(trade, linkFunction, stateChartId)
            if linkBP:
                errStr = "The linked export objects with id '%s' has no matching query list. Check the initialization of FExportProcess." % exportObjectId
                assert self.AdditionalQueryDictionary().has_key(exportObjectId), errStr
                linkQueries = self.AdditionalQueryDictionary()[exportObjectId]
                linkQueryId = FExportUtils.FindMatchingQueryId(linkBP.Subject(), linkQueries)
                if linkQueryId:
                    BPLoaded += self.AddBusinessProcess(linkBP, linkQueryId, trade)
        return BPLoaded

    def LoadBusinessProcesses(self):
        """
        General method to fill the FExportProcess with BusinessProcesses(BP) in order
        to know what business data to add to the export. The BPs will be sorted
        according to what FSingleExportIdentifier they belong to. Each such group
        will form a single report/export represented by FSingleExport class.
        """
        logger.debug('Now loading all the relevant trade business processes...')

        totalBPsLoaded = 0
        if len(self._ExportableBusinessProcesses(self._integration.ChartId()))>0:
            for tradeBP in self._ExportableBusinessProcesses(self._integration.ChartId()):
                trade = tradeBP.Subject()
                if not trade:
                    logger.debug('Business Process %d no longer refers to a valid trade or object -- ignoring it.', tradeBP.Oid())
                    continue
                queryId = FExportUtils.FindMatchingQueryId(trade, self.TradeQueryIdList())
                if queryId:
                    totalBPsLoaded += self.AddBusinessProcess(tradeBP, queryId)
                    if self.Integration().LinkedExportObjects():
                        totalBPsLoaded += self.LoadLinkedObjects(trade)

        elif self.GenerateEmptyFile():  
            logger.debug('No exportable business process. create dummy singleexport for empty report')
            #if no trades in the query, take any sheettemplate belonging to the first query
            sheetTemplateId = self._SheetTemplateId(self.TradeQueryIdList()[0])
            partyId = self._PartyId(None)
            singleExportIdentifier = FSingleExportIdentifier.FSingleExportIdentifier(self, partyId, sheetTemplateId)
            key = singleExportIdentifier.KeyValue()
            if not self._singleExport.has_key(key):
                self._singleExport[key] = FSingleExport(singleExportIdentifier, self.Integration())
                
        logger.info('Loaded %i business processes'% totalBPsLoaded)
        return totalBPsLoaded

    def AddBusinessProcess(self, businessProcess, ACMQueryId, trade = None):
        """
        Adds a singular BP to the export process.
        ACMQueryId and trade is needed to build the FSingleExportIdentifier.
        """
        try:
            sheetTemplateId = self._SheetTemplateId(ACMQueryId)
            trade = businessProcess.Subject() if not trade else trade
            partyId = self._PartyId(trade)
            singleExportIdentifier = FSingleExportIdentifier.FSingleExportIdentifier(self, partyId, sheetTemplateId)
            key = singleExportIdentifier.KeyValue()
            if not self._singleExport.has_key(key):
                self._singleExport[key] = FSingleExport(singleExportIdentifier, self.Integration())
            self._singleExport[key].AddBusinessProcess(businessProcess)
            return True
        except Exception as error:
            errStr = 'Could not process and load business process ' + str(businessProcess.Oid()) + ': ' + str(error)
            if self.TestMode().IsEnabled():
                logger.error('[TEST MODE] Business process would have been set to error state: %s', errStr)
            else:
                logger.error(errStr)
                FBusinessProcessUtils.SetBusinessProcessToError(businessProcess, errStr)
            return False

    def __iter__(self):
        return self._singleExport.iteritems()

    def _FindMatchingLinkedBP(self, trade, linkedfunction, stateChartId):
        for linkedBP in self._ExportableBusinessProcesses(stateChartId):
            if linkedBP.Subject() == linkedfunction(trade):
                return linkedBP
        return None

    def _ExportableBusinessProcesses(self, stateChartId):
        """
        Returns all BPs that are in a state marked as ready for export.
        """
        stateChart = acm.FStateChart[stateChartId]
        assert(stateChart), "No FStateChart called %s"%stateChartId
        return [bp for bp in acm.BusinessProcess.FindBySubjectAndStateChart(None, stateChart) \
                if FBusinessProcessUtils.IsValidEvent(bp, self._integration.ExportEventId())]
                
    def _SheetTemplateId(self, ACMQueryId):
        SheetTemplateId = ''
        try:
            SheetTemplateId = self._integration.SheetTemplateFinderFunction()(ACMQueryId)
        except Exception as error:
            functionName = self._integration.SheetTemplateFinderFunction.__module__ + "." + self._integration.SheetTemplateFinderFunction.__name__
            logger.error(functionName + ' used as SheetTemplateFinderFunction(ACMQueryId) returned error: ' + str(error))
            raise
        return SheetTemplateId

    def _PartyId(self, trade):
        partyId = None
        party = None
        try:
            party = self._integration.PartyFinderFunction()(trade)
        except Exception as error:
            functionName = self._integration.PartyFinderFunction.__module__ + "." + self._integration.PartyFinderFunction.__name__
            logger.error(functionName + ' used as PartyFinderFunction(trade) returned error: ' + str(error))
            raise
        if party:
            partyId = party.Name()
        return partyId


class FSingleExport():
    """
    This class represents a single outgoing export to any one recipient.
    A successful run of an AMI export can result in one or many single exports.
    Linked to each instance of this class is a singleExportIdentifier object
    that identifies it but also includes critical features about it.
    """

    def __init__(self, singleExportIdentifier, integrationInstance):
        self._businessProcesses = list()
        self._failed = False
        self._XMLData = ''
        self._integration = integrationInstance
        self._singleExportIdentifier = singleExportIdentifier
        self._filePath = self._FilePathFromHook(singleExportIdentifier)
        self._filename = self._FilenameFromHook(singleExportIdentifier)

    def _FilePathFromHook(self, key):
        filePath = ''
        try:
            filePath = self._integration.FilePathFunction()(key)
        except Exception as error:
            functionName = self._integration.FilePathFunction.__module__ + "." + self._integration.FilePathFunction.__name__
            logger.error(functionName + ' used as FilePathFunction(subject) returned error: ' + str(error))
            raise
        return filePath

    def _FilenameFromHook(self, key):
        filename = ''
        try:
            filename = self._integration.FilenameFunction()(key)
        except Exception as error:
            functionName = self._integration.FilenameFunction.__module__ + "." + self._integration.FilenameFunction.__name__
            logger.error(functionName + ' used as FilenameFunction(subject) returned error: ' + str(error))
            raise
        return filename

    def Integration(self):
        return self._integration

    def SingleExportIdentifier(self):
        return self._singleExportIdentifier

    def PartyId(self):
        return self._singleExportIdentifier.PartyId()

    def SheetTemplateId(self):
        return self._singleExportIdentifier.SheetTemplateId()

    def AddBusinessProcess(self, businessProcess):
        assert(businessProcess)
        if not businessProcess in self._businessProcesses:
            self._businessProcesses.append(businessProcess)

    def Remove(self, businessProcess):
        assert(businessProcess)
        self._businessProcesses.remove(businessProcess)

    def IsExportable(self):
        return (self.ExportableBusinessProcesses() and not self.Failed())

    def BusinessProcesses(self):
        return self._businessProcesses

    def ExportableBusinessProcesses(self):
        return [bp for bp in self.BusinessProcesses() if not bp.CurrentStep().IsInErrorState()]

    def Failed(self, reason=None):
        if reason is None:
            return self._failed
        if self.SingleExportIdentifier().ExportProcess().TestMode().IsEnabled():
            logger.error('[TEST MODE] Business processes would have been set to error state: %s', reason)
        else:
            FBusinessProcessUtils.SetBusinessProcessesToError(self.ExportableBusinessProcesses(), reason)
        self._failed = True

    def XMLData(self, xml=None):
        if xml is None:
            return self._XMLData
        self._XMLData = xml

    def FilePath(self):
        return self._filePath

    def Filename(self):
        return self._filename
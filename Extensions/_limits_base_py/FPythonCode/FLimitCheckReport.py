""" Compiled: 2020-09-18 10:38:53 """

#__src_file__ = "extensions/limits/./etc/FLimitCheckReport.py"
"""--------------------------------------------------------------------------
MODULE
    FLimitCheckReport

    (c) Copyright 2016 FIS FRONT ARENA. All rights reserved.

DESCRIPTION
    Functionality for producing reports of limit checks

-----------------------------------------------------------------------------"""

import acm
import FLimitSettings
import FSheetUtils
import FAssetManagementUtils
from contextlib import contextmanager
logger = FAssetManagementUtils.GetLogger()

class Singleton(type):

    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = type.__call__(cls, *args, **kwargs)
        return cls._instances[cls]

class LimitReportCheckResults(object):
    
    __metaclass__ = Singleton
    CheckedResults = {}
    
    def AddCheckedResults(self, results):
        for result in results:
            self.AddCheckedResult(result)
            self.AddNewChildLimits(result)
    
    def AddCheckedResult(self, result):
        self.CheckedResults[result.Limit] = result
    
    def CheckedState(self, limit):
        checkedResult = self.CheckedResults.get(limit, None)
        if checkedResult is not None:
            return checkedResult.StateAfter
        return None
            
    def StateChanged(self, limit):
        checkedResult = self.CheckedResults.get(limit, None)
        if checkedResult is not None:
            return checkedResult.StateChanged
        return None
        
    def AddNewChildLimits(self, result):
        for child in result.Children:
            self.AddCheckedResult(child)
            result.Limit.Children().Add(child.Limit)
                
    def RemoveChildLimits(self):
        for result in self.CheckedResults.values():
            for child in result.Children:
                result.Limit.Children().Remove(child.Limit)
    
    def Reset(self):
        self.RemoveChildLimits()
        self.CheckedResults.clear()

class LimitCheckReport(object):

    def __init__(self, output):
        self._limitCheckResults = LimitReportCheckResults()
        self._reportName = ' '.join((FLimitSettings.ReportName(), acm.Time.TimeNow()))
        self._report = acm.Report.CreateReport(self._reportName, output)
        self._reportGrid = None

    def ReportGrid(self):
        if self._reportGrid is None:
            self._reportGrid = self.CreateDefaultLimitReportGrid() 
        return self._reportGrid
        
    def GridBuilder(self):
        return self.ReportGrid().GridBuilder()

    def LimitCheckResults(self):
        return self._limitCheckResults.CheckedResults.values()
        
    def Limits(self):
        return self._limitCheckResults.CheckedResults.keys()
        
    def Report(self):
        return self._report
        
    def _ApplyGouper(self):
        grouper = acm.Risk.GetGrouperFromName(FLimitSettings.ReportGrouper(), acm.FLimitGrouperSubject)
        rootNode = self.GridBuilder().RowTreeIterator().FirstChild()
        while rootNode is not None:
            try:
                rootNode.Tree().ApplyGrouper(grouper)
            except StandardError as stderr:
                logger.debug("Unable to apply grouper " \
                "'%s' to node '%s' : %s" % (grouper.DisplayName(), rootNode.Tree().StringKey(), stderr))
            rootNode = rootNode.NextSibling()
        self.GridBuilder().Refresh()
    
    @contextmanager
    def _SetCheckedResults(self, limitCheckResults):
        self._limitCheckResults.AddCheckedResults(limitCheckResults)
        yield
        self._ResetCheckedResults()
      
    def Generate(self, limitCheckResults):
        self._SetColumnCreators()
        with self._SetCheckedResults(limitCheckResults):
            self._PrepareReport()
            self._SaveReport()

    def _PrepareReport(self):
        self._InsertLimits()
        self._SetLimitCheckResults()
        self._ApplyGouper()
        
    def _SaveReport(self):       
        self.ReportGrid().Generate()

    def _ResetCheckedResults(self):
        self._limitCheckResults.Reset()
 
    def _SetLimitCheckResults(self):
        for result in self.LimitCheckResults():
            limit = result.Limit
            self.GridBuilder().Refresh()
            context = acm.GetDefaultContext()
            try:
                node = self.GridBuilder().RowTreeIterator().Find(limit).Tree()
            except AttributeError as e:
                logger.error("Did not find limit '%s' in report. Error: %s"%(limit.Oid(), str(e)))
                continue
            try:
                for columnDef in self.LimitCheckResultColumns():
                    try:
                        value = self.GetResultValue(result, columnDef)
                    except AttributeError:
                        logger.error('Unable to read column "%s" on result "%s"'%(columnDef.StringKey(), result))
                        continue
                    else:
                        self.ReportGrid().SetCellValue(node, columnDef.StringKey(), context, value)
            except StandardError as e:
                logger.debug("Failed to set value in report: %s"%str(e))
        
    def _InsertLimits(self):
        """ Use [-1] if not limits are applicable: we want an empty report, not all limits in the db
            which is the result if we use a query without asql nodes """
        oids = [limit.Oid() for limit in self.Limits() if not limit.IsInfant()] or [-1]
        folder = acm.FASQLQueryFolder()
        query = acm.Filter.SimpleOrQuery(acm.FLimit, ["Oid"] * len(oids), [], oids)
        folder.AsqlQuery = query
        folder.Name = self._reportName
        self.GridBuilder().InsertItem(folder)
            
    def CreateDefaultLimitReportGrid(self, includeInsAndLeg = True, includeRows = True):
        gridConfig = acm.Report.CreateGridConfiguration( includeInsAndLeg, includeRows )
        return self.Report().OpenSheet(acm.FLimitSheet(), gridConfig, None)
        
    def _SetColumnCreators(self):
        gridBuilder = self.GridBuilder()
        columnIds = FSheetUtils.ColumnIds(FLimitSettings.ReportColumns(), "FLimitSheet")
        columnCreators = FSheetUtils.ColumnCreators(columnIds)
        i = 0
        while i < columnCreators.Size():
            creator = columnCreators.At(i)
            gridBuilder.ColumnCreators().Add(creator)
            i = i + 1
        
    @staticmethod
    def LimitCheckResultColumns():
        return acm.GetDefaultContext().GetAllExtensions('FColumnDefinition', 'FTradingSheet',
                True, True, 'limits', 'check result columns')

    @staticmethod
    def GetResultValue(result, columnDef):
        resultMethod = str(columnDef.At('Method', None))
        resultDomain = columnDef.At('ValueDomain', None)
        cast_func = acm.GetFunction(resultDomain, 1)
        return cast_func(getattr(result, resultMethod))


""" These two methods are used to be able to group limits on the result from a check. 
    They are called from the applied grouper """ 

def LimitCheckedState(limit):
    return LimitReportCheckResults().CheckedState(limit)
    
def LimitStateChanged(limit):
    return LimitReportCheckResults().StateChanged(limit)

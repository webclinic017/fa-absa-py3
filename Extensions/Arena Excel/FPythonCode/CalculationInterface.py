""" Compiled: 2020-09-18 10:38:52 """

#__src_file__ = "extensions/ArenaExcel/etc/CalculationInterface.py"
import acm
import math

from CalculationBase import SheetCalculation, DealSheetCalculation, PortfolioNode, InstrumentNode, Result
from SingleValueTask import CalculationTask, CalculationTaskArguments


class CalculationArguments(CalculationTaskArguments):

    GROUPING_SUBJECT_CLASS_MAP = {
        'FInstrumentAndTradesGrouperSubject' : ('FPortfolioSheet', 'FTradeSheet', 'FRiskMatrixSheet')
    }

    def __init__(self, *args):
        super(CalculationArguments, self).__init__(*args)
        self._sheetClass = None
        self._columnId = None
        self._objectName = None
        self._grouper = None
        self._constraint = None
        self._context = None        
        
    @property
    def SheetClass(self):
        if self._sheetClass is None:
            self._sheetClass = self.Get(0)
        return self._sheetClass

    @property        
    def ColumnId(self):
        if self._columnId is None:
            self._columnId = self.Get(1)
        return self._columnId

    @property        
    def ObjectName(self):
        if self._objectName is None:
            self._objectName = self.Get(2)
        return self._objectName

    @property        
    def GroupingSubjectClass(self):
        for key, values in list(self.GROUPING_SUBJECT_CLASS_MAP.items()):
            if self.SheetClass in values:
                return key
        return None

    @property        
    def Grouper(self):
        if self._grouper is None:
            try:
                self._grouper = acm.Risk.GetGrouperFromName(self.Get(3), 
                                                            self.GroupingSubjectClass)
            except TypeError:
                pass
        return self._grouper

    @property        
    def Constraint(self):
        if self._constraint is None:
            try:
                self._constraint = [constraint.strip() for constraint 
                                    in self.Get(4).split(PortfolioNode.PATH_SEPARATOR)]
            except TypeError:
                pass
        return self._constraint
        
    @property        
    def Context(self):
        if self._context is None:
            self._context = self.Get(5) or acm.GetDefaultContext()
        return self._context
        
        
def CreateCalculation(*args):
    calcArgs = CalculationArguments(*args)
    space = calcArgs.SpaceCollection.GetSpace(calcArgs.Context,
                                              calcArgs.SheetClass)
    if calcArgs.SheetClass == 'FDealSheet':
        node = InstrumentNode(calcArgs.ObjectName)
        return DealSheetCalculation(space, node, calcArgs.ColumnId)
        
    node = PortfolioNode(space, 
                         calcArgs.ObjectName, 
                         calcArgs.Grouper, 
                         calcArgs.Constraint) 
    return SheetCalculation(space, node, calcArgs.ColumnId)
        
        
class GetValue(CalculationTask):

    def __init__(self, *args):
        self._calculation = CreateCalculation(*args)
        
    def HasPendingResult(self):
        return self._calculation.IsInitialized() and self._calculation.IsDirty()

    def Result(self):
        return Result(self._calculation).Value()
        
    def Destroy(self):   
        self._calculation.Destroy()

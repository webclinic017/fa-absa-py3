""" Compiled: 2020-09-18 10:38:52 """

#__src_file__ = "extensions/ArenaExcel/etc/AdvancedCalculationInterface.py"
import base64
import acm

from SingleValueTask import CalculationTask, CalculationTaskArguments
from CalculationBase import SheetCalculation, TreeSpecNode, Result


class AdvancedCalculationArguments(CalculationTaskArguments):

    ROW_TAG = 'Row:'
    COLUMN_TAG = 'Column:'
    
    def __init__(self, *args):
        super(AdvancedCalculationArguments, self).__init__(*args)
        self._encodedArgs = None
        self._rowArg = None
        self._columnArg = None
        
    def _XmlArchive(self, startTag, endTag=None):
            encoded = []
            appendToEncode = False
            for arg in self.GetAll():
                if endTag and arg.startswith(endTag): 
                    break
                elif not arg.startswith(startTag) and appendToEncode is False:
                    continue
                elif arg.startswith(startTag):
                    appendToEncode = True
                    encoded.append(arg[len(startTag):])
                elif appendToEncode is True:
                    encoded.append(arg)
                    
            compressed = base64.b64decode(''.join(encoded))
            xmlArchive = acm.FXmlArchive()
            xmlArchive.Load(compressed)
            return xmlArchive

    def _RowArg(self):
        if self._rowArg is None:
            self._rowArg = self._XmlArchive(self.ROW_TAG, self.COLUMN_TAG)
        return self._rowArg
        
    def _ColumnArg(self):
        if self._columnArg is None:
            self._columnArg = self._XmlArchive(self.COLUMN_TAG)
        return self._columnArg
        
    @property
    def SheetClass(self):
        return self._ColumnArg().Get('sheetClass')
    
    @property    
    def Context(self):
        return self._ColumnArg().Get('contextName')
        
    @property        
    def ColumnId(self):
        return self._ColumnArg().Get('columnId')   
        
    @property        
    def TreeSpecification(self):
        return self._RowArg().Get('treeSpec')
        
    @property        
    def ProjectionParts(self):
        return self._ColumnArg().Get('projectionParts')
        
    @property        
    def DistributedMode(self):
        return self._ColumnArg().Get('distributedMode')
        
    @property        
    def DisplayType(self):
        return self._ColumnArg().Get('displayType')
        
    @property        
    def Configuration(self):
        return self._ColumnArg().Get('configuration')
        
        
def CreateCalculation(*args):
    calcArgs = AdvancedCalculationArguments(*args)
    space = calcArgs.SpaceCollection.GetSpace(calcArgs.Context, 
                                              calcArgs.SheetClass, 
                                              calcArgs.DistributedMode)
    node = TreeSpecNode(space, calcArgs.TreeSpecification)
    return SheetCalculation(space, 
                            node, 
                            calcArgs.ColumnId, 
                            calcArgs.Configuration, 
                            calcArgs.ProjectionParts)

        
class GetValue(CalculationTask):

    def __init__(self, *args):
        self._calculation = CreateCalculation(*args)
        
    def HasPendingResult(self):
        return self._calculation.IsInitialized() and self._calculation.IsDirty()

    def Result(self):
        return Result(self._calculation).Value()
        
    def Destroy(self):   
        self._calculation.Destroy()

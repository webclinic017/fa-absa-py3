""" Compiled: 2020-09-18 10:38:53 """

#__src_file__ = "extensions/operations/etc/FOperationsTransactionModifiers.py"
# operations
from FOperationsWriter import Writer

#-------------------------------------------------------------------------
class SortingTransactionModifier(Writer.Modifier):
    
    #-------------------------------------------------------------------------    
    def __init__(self, sortingFunc):
        super(SortingTransactionModifier, self).__init__()
        self._sortingFunc = sortingFunc

    #-------------------------------------------------------------------------        
    def MO_Prepare(self, objs):
        return sorted(objs, key=self._sortingFunc, reverse=True)

            
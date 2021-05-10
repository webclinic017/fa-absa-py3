
class AGGREGATION_SELECTION:
    def __init__(self, returnAttribute, fromTable, selectionList, primarySelectionTuple):
        self.__returnAttribute = returnAttribute
        self.__fromTable = fromTable
        self.__selectionList = selectionList
        self.__primarySelectionTuple = primarySelectionTuple
        
    @property
    def returnAttribute(self):
        return self.__returnAttribute
    
    @returnAttribute.setter
    def returnAttribute(self, value):
        self.__returnAttribute = value

    @property
    def fromTable(self):
        return self.__fromTable
    
    @fromTable.setter
    def fromTable(self, value):
        self.__fromTable = value

    @property
    def selectionList(self):
        return self.__selectionList

    @selectionList.setter
    def selectionList(self, value):
        self.__selectionList = value

    @property
    def primarySelectionTuple(self):
        return self.__primarySelectionTuple

    @primarySelectionTuple.setter
    def primarySelectionTuple(self, value):
        self.__primarySelectionTuple = value

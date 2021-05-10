
'''----------------------------------------------------------------------------------------------------------
MODULE                  :       FC_DATA_BASE
PROJECT                 :       Front Cache
PURPOSE                 :       This class represents the base container for data
DEPARTMENT AND DESK     :       All Departments and all Desks.
REQUASTER               :       Front Cache
DEVELOPER               :       Heinrich Momberg
CR NUMBER               :       XXXXXX
-------------------------------------------------------------------------------------------------------------
'''

#*********************************************************#
#Importing Modules
#*********************************************************#
from FC_UTILS import FC_UTILS as UTILS
from FC_CALCULATION_SINGLETON import FC_CALCULATION_SINGLETON as fcCalculationSingleton

#**********************************************************
#Static helper methods on the class (not using self)
#**********************************************************
#Insert an FObject into the calculation space for the sheet and return the top level node as a TreeProxy
def GetTopLevelNodeTreeProxy(worksheetName, fObject):
    if not worksheetName or worksheetName=='':
        raise Exception(UTILS.Constants.fcExceptionConstants.VALID_WS_MUST_BE_PROVIDED)
    elif fcCalculationSingleton.Instance().worksheetCalcSpaces[worksheetName] != None:
        node = fcCalculationSingleton.Instance().worksheetCalcSpaces[worksheetName].InsertItem(fObject)
        if not node or not node.Item():
            raise Exception(UTILS.Constants.fcExceptionConstants.NO_TOP_LEVEL_NODE_TREE_PROXY)
        return node
        
#Return the first child of a top level node as a TreeProxy
def GetFirstChildNodeTreeProxy(worksheetName, fObject):
    #Fetch the top level node
    node = GetTopLevelNodeTreeProxy(worksheetName, fObject)
    #Expand the node
    node.Expand(True)
    #Refresh the calc space
    fcCalculationSingleton.Instance().worksheetCalcSpaces[worksheetName].Refresh()
    #Now find the first child
    if node.NumberOfChildren():
        child_iterator = node.Iterator().FirstChild()
        node = child_iterator.Tree()
        if not node or not node.Item():
            raise Exception(UTILS.Constants.fcExceptionConstants.NO_FIRST_CHILD_NODE_TREE_PROXY)
        return node

#Returns all the children of a top level node as TreeProxies
def GetTopLevelNodeChildrenTreeProxies(worksheetName, fObject):
    #Fetch the top level node
    node = GetTopLevelNodeTreeProxy(worksheetName, fObject)
    #Expand the node
    node.Expand(True)
    #Refresh the calc space
    fcCalculationSingleton.Instance().worksheetCalcSpaces[worksheetName].Refresh()
    #Now find the first child
    if node.NumberOfChildren():
        child_iterator = node.Iterator().FirstChild()
        while child_iterator:
            node = child_iterator.Tree()
            yield node
            child_iterator = child_iterator.NextSibling()
        
#*********************************************************#
#BASE Class definition
#*********************************************************#
class FC_DATA_BASE(): 
    
    #*********************************************************#
    #Constructor
    #*********************************************************#
    def __init__(self, worksheetName):
        if not worksheetName or worksheetName=='':
            raise Exception(UTILS.Constants.fcExceptionConstants.VALID_WS_MUST_BE_PROVIDED)
        else:
            self._worksheetName=worksheetName
        
        #Reset the fields
        self._fTreeProxy = None
        self._calculationResults=None
        self._calculationErrors=None
        self._serializedCalculationResults  = None
        self._serializedCalculationErrors = None

    #**********************************************************#
    #Properties
    #*********************************************************#
    #WorksheetName
    @property
    def WorksheetName(self):
        return self._worksheetName 
    
    #WorksheetName
    @property
    def FTreeProxy(self):
        return self._fTreeProxy
        
    #CalculationResults
    @property
    def CalculationResults(self):
        return self._calculationResults 

    #CalculationErrors
    @property
    def CalculationErrors(self):
        return self._calculationErrors
        
    #SerializedCalculationResults
    @property
    def SerializedCalculationResults(self):
        return self._serializedCalculationResults 
        
    #SerializedCalculationErrors
    @property
    def SerializedCalculationErrors(self):
        return self._serializedCalculationErrors
    
    #Abstract methods for implementation in the sub classes
    def GetFObject(self):
        raise Exception(UTILS.Constants.fcExceptionConstants.METHOD_GETFOBJECT_NOT_IMPLEMENTED)
            
            
    #Call the calculation singleton to calculate the column values
    def Calculate(self):
        if not self._worksheetName or self._worksheetName=='':
            raise Exception(UTILS.Constants.fcExceptionConstants.WS_NAME_NOT_SET)
        elif not self._fTreeProxy:
            raise Exception(UTILS.Constants.fcExceptionConstants.VALID_FTREEPROXY_MUST_BE_PROVIDED)
        else:
            fObject = self.GetFObject()
            if(fObject):
                (self._calculationResults, self._calculationErrors) = fcCalculationSingleton.Instance().calcWorksheetColumnValues(self._worksheetName, fObject, self._fTreeProxy)
                
    

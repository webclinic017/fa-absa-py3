
'''----------------------------------------------------------------------------------------------------------
MODULE                  :       FC_DATA_BASE_REPOSITORY
PROJECT                 :       Front Cache
PURPOSE                 :       This base database repository class
DEPARTMENT AND DESK     :       All Departments and all Desks.
REQUASTER               :       Front Cache
DEVELOPER               :       Heinrich Momberg
CR NUMBER               :       XXXXXX
-------------------------------------------------------------------------------------------------------------
'''
#*********************************************************#
#Importing Modules
#*********************************************************#
import FC_UTILS
import FC_ENUMERATIONS
#*********************************************************#
#Base class definition
#*********************************************************#
class FC_DATA_BASE_REPOSITORY():

    #Properties
    
    #TradeDomain
    @property
    def TradeDomain(self):
        return self._tradeDomain

    #DBCreateProcess
    @property
    def DBCreateProcess(self):
        return self._dbCreateProcess
        
    #Constructor
    def __init__(self, dbProvider): 
        #initialise the calculation singleton (all workbook sheets and columns will be loaded)
        self.dbProvider=dbProvider
        
        #TODO:set this from configuration - the instance that owns the data (will use this to split between SA and Africa)
        self._tradeDomain = FC_ENUMERATIONS.TradeDomain.SOUTH_AFRICA
        
        #TODO:set this from configuration - the name of the processs running
        self._dbCreateProcess = FC_UTILS.FC_UTILS.ComponentName
        


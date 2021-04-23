
'''----------------------------------------------------------------------------------------------------------
MODULE                  :       FC_DATA_TRD_LEG
PROJECT                 :       Front Cache
PURPOSE                 :       This class represents the container for trade leg data
DEPARTMENT AND DESK     :       All Departments and all Desks.
REQUASTER               :       Front Cache
DEVELOPER               :       Heinrich Momberg
CR NUMBER               :       XXXXXX
-------------------------------------------------------------------------------------------------------------
'''
#*********************************************************#
#Importing Modules
#*********************************************************#
import FC_DATA_BASE
from FC_UTILS import FC_UTILS as UTILS
#*********************************************************#
#Static Creator method for all legs of a trade (not use self)
#*********************************************************#
worksheetName = UTILS.Constants.fcGenericConstants.FC_TRADE_LEG
def CreateAllForTrade(trade):
    global worksheetName
    if not trade:
        raise Exception(UTILS.Constants.fcExceptionConstants.VALID_FTRADE_INSTANCE_MUST_BE_PROVIDED)
        
    """if trade.Oid() in (87083353,87083354):
        worksheetName = 'FC_TRADE_LEG_OVERRIDE'
    else:"""
    worksheetName = UTILS.Constants.fcGenericConstants.FC_TRADE_LEG

    
    tradeLegs = []
    #Get a leg count before attempting anything
    if trade.Instrument() and trade.Instrument().Legs():

        if len(trade.Instrument().Legs())>1:
            for legTreeProxy in FC_DATA_BASE.GetTopLevelNodeChildrenTreeProxies(worksheetName, trade):
                tradeLeg = FC_DATA_TRD_LEG(worksheetName, trade.Instrument().Oid(), legTreeProxy, None)
                tradeLegs.append(tradeLeg)
        elif len(trade.Instrument().Legs())==1:
            legTreeProxy = FC_DATA_BASE.GetTopLevelNodeTreeProxy(worksheetName, trade)
            tradeLeg = FC_DATA_TRD_LEG(worksheetName, trade.Instrument().Oid(), legTreeProxy, trade.Instrument().Legs()[0])
            tradeLegs.append(tradeLeg)
    
    return tradeLegs
    
#*********************************************************#
#Class definition
#*********************************************************#
class FC_DATA_TRD_LEG(FC_DATA_BASE.FC_DATA_BASE): 
    
    
    
    #**********************************************************#
    #Properties
    #*********************************************************#
    #FInstrument - get from the fTree proxy to ensure the same object is used
    fLeg = None
    @property
    def FLeg(self):
        return self.fLeg
    
    #InstrumentAddress - get from the fTree proxy to ensure the same object is used
    @property
    def InstrumentAddress(self):
        return self._instrumentAddress
        
    #*********************************************************#
    #Constructor
    #*********************************************************#
    def __init__(self, worksheetName, instrumentAddress, fLegTreeProxy, fLeg):
        self.fLeg = fLeg
        self._instrumentAddress = instrumentAddress
        #Construct the base class
        FC_DATA_BASE.FC_DATA_BASE.__init__(self, worksheetName)
        
        #Get an FTreeProxy
        if not fLegTreeProxy:
            raise Exception(UTILS.Constants.fcExceptionConstants.VALID_FLEGTREEPROXY_MUST_BE_PROVIDED)
        else:
            self._fTreeProxy = fLegTreeProxy
            
            
    #**********************************************************#
    #Methods
    #*********************************************************#
    #GetFObject override 
    def GetFObject(self):
        try:
            if self._fTreeProxy and self._fTreeProxy.Item():
                if str(self._fTreeProxy.Item().ClassName())==UTILS.Constants.fcGenericConstants.FTRADEROW:
                    return self._fTreeProxy.Item().Trade()
                else:
                    if(self.fLeg==None):
                        self.fLeg = self._fTreeProxy.Item().Leg()
                    return self._fTreeProxy.Item().Leg()
        except:
            return None



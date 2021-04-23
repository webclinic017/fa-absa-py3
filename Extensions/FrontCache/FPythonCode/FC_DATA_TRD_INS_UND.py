
'''----------------------------------------------------------------------------------------------------------
MODULE                  :       FC_DATA_TRD_INS_UND
PROJECT                 :       Front Cache
PURPOSE                 :       This class represents the container for underlying instrument data
DEPARTMENT AND DESK     :       All Departments and all Desks.
REQUASTER               :       Front Cache
DEVELOPER               :       Heinrich Momberg
CR NUMBER               :       XXXXXX
-------------------------------------------------------------------------------------------------------------
'''
#*********************************************************#
#Importing Modules
#*********************************************************#
import acm
import FC_DATA_BASE
from FC_UTILS import FC_UTILS as UTILS
#*********************************************************#
#Static Creator method for all underlying instruments of a trade (not use self)
#*********************************************************#
worksheetName = UTILS.Constants.fcGenericConstants.FC_UNDERLYING_INSTRUMENT

#Static helper method to get all underlying/related instruments for an instrument
def GetRelatedInstruments(instrument, results, ulst = []):
    #Check reference on legs
    underlyingInstruments = []
    if instrument.Legs():
        for leg in instrument.Legs():
            credit_ref = leg.CreditRef()
            index_ref = leg.IndexRef()
            if credit_ref and credit_ref.Oid() not in ulst:
                underlyingInstruments.append(credit_ref)
                ulst.append(credit_ref.Oid())
            if index_ref and index_ref.Oid() not in ulst:
                underlyingInstruments.append(index_ref)
                ulst.append(index_ref.Oid())
    #check combinations
    combination = acm.FCombination[instrument.Oid()]
    if combination:
        for underlying in combination.Instruments():
            underlyingInstruments.append(underlying)
    #check normal underlying
    ins_under = instrument.Underlying()
    if ins_under and ins_under.Oid() not in ulst:
        underlyingInstruments.append(instrument.Underlying())
        ulst.append(ins_under.Oid())

    if len(underlyingInstruments)>0:
        for underlyingInstrument in underlyingInstruments:
            results.append((instrument.Oid(), underlyingInstrument))
            results = GetRelatedInstruments(underlyingInstrument, results, ulst)
    return results
#*************************************************************************#
#Static Creator method for all related instruments of a trade (not use self)
#*************************************************************************#
def CreateAllForTrade(trade):
    global worksheetName
    
    if not trade:
        raise Exception(UTILS.Constants.fcExceptionConstants.VALID_FTRADE_INSTANCE_MUST_BE_PROVIDED)

    """if trade.Oid() in (87083353,87083354):
        worksheetName = 'FC_UNDERLYING_INSTRUMENT_OVERRIDE'
    else:"""
    worksheetName = UTILS.Constants.fcGenericConstants.FC_UNDERLYING_INSTRUMENT


    #Return value - a collection of FC_DATA_TRD_INS_UND instances 
    underlyingInstruments = []
    if trade.Instrument():
        relatedInstruments = []
        instrument_oid_list = []
        GetRelatedInstruments(trade.Instrument(), relatedInstruments, instrument_oid_list)
        for relatedInstrument in relatedInstruments:
            parentInstrumentAddress = relatedInstrument[0]
            relatedInstrumentObject = relatedInstrument[1]
            #Create a tree proxy for each related instrument
            fInstrumentTreeProxy = FC_DATA_BASE.GetFirstChildNodeTreeProxy(worksheetName, relatedInstrumentObject)
            #Now create and add the underlying instrument
            underlyingInstrument = FC_DATA_TRD_INS_UND(worksheetName, parentInstrumentAddress, fInstrumentTreeProxy)
            underlyingInstruments.append(underlyingInstrument)
    return underlyingInstruments


#**********************************************************#
#Class Definition
#*********************************************************#
class FC_DATA_TRD_INS_UND(FC_DATA_BASE.FC_DATA_BASE): 
    
    #**********************************************************#
    #Properties
    #*********************************************************#
    #ParentInstrumentAddress
    @property
    def ParentInstrumentAddress(self):
        return self._parentInstrumentAddress
        
    #FUnderlyingInstrument - get from the fTree proxy to ensure the same object is used
    @property
    def FInstrument(self):
        return self.GetFObject()
        
    #*********************************************************#
    #Constructor
    #*********************************************************#
    def __init__(self, worksheetName, parentInstrumentAddress, fInstrumentTreeProxy):
        self._parentInstrumentAddress = parentInstrumentAddress
        #Construct the base class
        FC_DATA_BASE.FC_DATA_BASE.__init__(self, worksheetName)
            
        #Get an FTreeProxy
        if not fInstrumentTreeProxy:
            raise Exception(UTILS.Constants.fcExceptionConstants.VALID_FINSTRTREEPROXY_MUST_BE_PROVIDED)
        else:
            self._fTreeProxy = fInstrumentTreeProxy
        
    #**********************************************************#
    #Methods
    #*********************************************************#
    #GetFObject override 
    def GetFObject(self):
        if self._fTreeProxy and self._fTreeProxy.Item() and self._fTreeProxy.Item().Instrument():
            return self._fTreeProxy.Item().Instrument()



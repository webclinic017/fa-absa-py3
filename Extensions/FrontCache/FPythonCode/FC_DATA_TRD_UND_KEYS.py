__author__ = 'viljoeaa'
#*********************************************************#
#Importing Modules
#*********************************************************#
import acm
import FC_UTILS
from FC_UTILS import FC_UTILS as UTILS

#Static helper method to get all underlying/related instruments for an instrument
def GetRelatedInstruments(underlying, results, ulst=[], tradeNumber=None):
    #Check reference on legs
    underlyingInstruments = []
    if str(type(underlying)) != "<type 'FTrade'>":
        if underlying.Legs():
            for leg in underlying.Legs():
                credit_ref = leg.CreditRef()
                index_ref = leg.IndexRef()
                if credit_ref and credit_ref.Oid() not in ulst:
                    underlyingInstruments.append((credit_ref, UTILS.Constants.fcGenericConstants.INSTRUMENT))
                    ulst.append(credit_ref.Oid())
                if index_ref and index_ref.Oid() not in ulst:
                    underlyingInstruments.append((index_ref, UTILS.Constants.fcGenericConstants.INSTRUMENT))
                    ulst.append(index_ref.Oid())
        #check combinations
        combination = acm.FCombination[underlying.Oid()]
        if combination:
            for u in combination.Instruments():
                underlyingInstruments.append((u, UTILS.Constants.fcGenericConstants.INSTRUMENT))
        #check normal underlying
        ins_under = underlying.Underlying()
        if ins_under and ins_under.Oid() not in ulst:
            underlyingInstruments.append((underlying.Underlying(), UTILS.Constants.fcGenericConstants.INSTRUMENT))
            ulst.append(ins_under.Oid())

        #FRCA-1348 Add related instruments for BasketRepo/Reverse
        if underlying.InsType() == 'BasketRepo/Reverse' and tradeNumber is not None:
            connectedTrades = acm.FTrade.Select("connectedTrdnbr=%s"%tradeNumber)
            for collateralTrade in connectedTrades:
                if tradeNumber != collateralTrade.Oid():
                    underlyingInstruments.append((collateralTrade, UTILS.Constants.fcGenericConstants.TRADE))
                    ulst.append(collateralTrade.Oid())
        if len(underlyingInstruments)>0:
            for underlyingInstrument in underlyingInstruments:
                results.append((underlying.Oid(), underlyingInstrument))
                results = GetRelatedInstruments(underlyingInstrument[0], results, ulst)
    return results

#*************************************************************************#
#Static Creator method for all related instruments of a trade (not use self)
#*************************************************************************#
def CreateAllForTrade(trade):
    global worksheetName
    if not trade:
        raise Exception(UTILS.Constants.fcExceptionConstants.VALID_FTRADE_INSTANCE_MUST_BE_PROVIDED)
    #Return value - a collection of FC_DATA_TRD_INS_UND instances
    underlyings = []
    if trade.Instrument():
        relatedInstruments = []
        instrument_oid_list = []
        GetRelatedInstruments(trade.Instrument(), relatedInstruments, instrument_oid_list, trade.Oid())
        for relatedInstrument in relatedInstruments:
            underlying = FC_DATA_TRD_UND_KEYS(relatedInstrument[1][0].Oid(), relatedInstrument[1][1])
            underlyings.append(underlying)
    return underlyings
#**********************************************************#
#Class Definition
#*********************************************************#
class FC_DATA_TRD_UND_KEYS():

    @property
    def Key(self):
        return self._key

    @Key.setter
    def Key(self, value):
        self._key= value

    @property
    def Key_Type(self):
        return self._key_type

    @Key.setter
    def Key_Type(self, value):
        self._key_type= value

    #CalculationResults
    @property
    def CalculationResults(self):
        return self._calculationResults

    #CalculationErrors
    @property
    def CalculationErrors(self):
        return self._calculationErrors
    
    #*********************************************************#
    #Constructor
    #*********************************************************#
    def __init__(self, key, key_type):
        self._key = key
        self._key_type = key_type

    def Calculate(self):
        self._calculationResults = {}
        self._calculationResults[UTILS.Constants.fcGenericConstants.KEY]= self._key
        self._calculationResults[UTILS.Constants.fcGenericConstants.KEY_TYPE]= self._key_type

    #Serialize the calculation results
    def SerializeCalculationResults(self, serializationType):
        try:
            self._serializedCalculationResults = FC_UTILS.SerializeDictionary(serializationType, UTILS.Constants.fcGenericConstants.CALCULATION_RESULTS, self.CalculationResults)
        except Exception, e:
            raise Exception(UTILS.Constants.fcExceptionConstants.COULD_NOT_SERIALIZE_THE_CALC_RESULT % str(e))

    #Serialize the calculation errors
    def SerializeCalculationErrors(self, serializationType):
        try:
            self._serializedCalculationErrors = FC_UTILS.SerializeDictionary(serializationType, UTILS.Constants.fcGenericConstants.CALCULATION_ERRORS, self.CalculationErrors)
        except Exception, e:
            raise Exception(UTILS.Constants.fcExceptionConstants.COULD_NOT_SERIALIZE_THE_CALC_RESULT % str(e))


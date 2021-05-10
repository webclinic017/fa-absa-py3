
'''----------------------------------------------------------------------------------------------------------
MODULE                  :       FC_DATA_TRD_BUILDER_OPTIONS
PROJECT                 :       Front Cache
PURPOSE                 :       Describes to a trade builder how to construct a trade
DEPARTMENT AND DESK     :       All Departments and all Desks.
REQUASTER               :       Front Cache
DEVELOPER               :       Heinrich Momberg
CR NUMBER               :       XXXXXX
----------------------------------------------------------------------------------------------------------'''

'''----------------------------------------------------------------------------------------------------------
Importing Custom Modules
----------------------------------------------------------------------------------------------------------'''
import FC_ENUMERATIONS as ENUMERATIONS

'''----------------------------------------------------------------------------------------------------------
Class containing the Builder Option Properties
----------------------------------------------------------------------------------------------------------'''
class FC_DATA_TRD_BUILDER_OPTIONS(object):

    #Constructor
    def __init__(self):
        
        #reset the fields
        self._buildTradeStatic=True
        self._buildTradeScalar=True
        self._buildTradeInstrument=True
        self._buildTradeLegs=True
        self._buildUnderlyingInstruments=True
        self._buildMoneyflows=True
        self._historicalCashflowRange=-1
        self._buildSalesCredits=True
        self._buildControlMeasures = False
        self._buildUnderlyingKeys=True
        self._serializationType=None
        
    #**********************************************************#
    #Properties
    #*********************************************************#
    #BuildTradeStatic
    @property
    def BuildTradeStatic(self):
        return self._buildTradeStatic
    
    @BuildTradeStatic.setter
    def BuildTradeStatic(self, value):
        self._buildTradeStatic = value

    #BuildTradeScalar
    @property
    def BuildTradeScalar(self):
        return self._buildTradeScalar
    
    @BuildTradeScalar.setter
    def BuildTradeScalar(self, value):
        self._buildTradeScalar = value
        
    #BuildTradeInstrument
    @property
    def BuildTradeInstrument(self):
        return self._buildTradeInstrument
    
    @BuildTradeInstrument.setter
    def BuildTradeInstrument(self, value):
        self._buildTradeInstrument = value
        
    #BuildTradeLegs
    @property
    def BuildTradeLegs(self):
        return self._buildTradeLegs
    
    @BuildTradeLegs.setter
    def BuildTradeLegs(self, value):
        self._buildTradeLegs = value
        
    #BuildUnderlyingInstruments
    @property
    def BuildUnderlyingInstruments(self):
        return self._buildUnderlyingInstruments
    
    @BuildUnderlyingInstruments.setter
    def BuildUnderlyingInstruments(self, value):
        self._buildUnderlyingInstruments = value
        
    #BuildUnderlyingKeys
    @property
    def BuildUnderlyingKeys(self):
        return self._buildUnderlyingInstruments

    @BuildUnderlyingKeys.setter
    def BuildUnderlyingKeys(self, value):
        self._buildUnderlyingKeys = value

    #BuildMoneyflows
    @property
    def BuildMoneyflows(self):
        return self._buildMoneyflows
    
    @BuildMoneyflows.setter
    def BuildMoneyflows(self, value):
        self._buildMoneyflows = value
        
    #HistoricalCashflowRange
    @property
    def HistoricalCashflowRange(self):
        return self._historicalCashflowRange
    
    @HistoricalCashflowRange.setter
    def HistoricalCashflowRange(self, value):
        self._historicalCashflowRange = value
        
    #BuildSalesCredits
    @property
    def BuildSalesCredits(self):
        return self._buildSalesCredits
    
    @BuildSalesCredits.setter
    def BuildSalesCredits(self, value):
        self._buildSalesCredits = value
        
    #SerializationType
    @property
    def SerializationType(self):
        return self._serializationType
    
    @SerializationType.setter
    def SerializationType(self, value):
        self._serializationType = value

    #BuildControlMeasures
    @property
    def BuildControlMeasures(self):
        return self._buildControlMeasures
    
    @BuildControlMeasures.setter
    def BuildControlMeasures(self, value):
        self._buildControlMeasures = value        

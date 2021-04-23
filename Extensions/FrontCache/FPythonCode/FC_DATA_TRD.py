
'''----------------------------------------------------------------------------------------------------------
MODULE                  :       FC_DATA_TRD
PROJECT                 :       Front Cache
PURPOSE                 :       This class represents a trade data container
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
import FC_UTILS
from FC_UTILS import FC_UTILS as UTILS
import FC_SERIALIZATION
from xml.etree.ElementTree import Element, tostring
from FC_DATA_ABSTRACT import FC_DATA_ABSTRACT as DATA_ABSTRACT

class FC_DATA_TRD(DATA_ABSTRACT):
    #*********************************************************#
    #Constructor
    #*********************************************************#
    def __init__(self, tradeNumber):
        #find the trade
        trade = acm.FTrade[tradeNumber]
        if not trade:
            raise Exception(UTILS.Constants.fcExceptionConstants.TRADE_S_NOT_FOUND % str(tradeNumber))
        else:
            self._fTrade = trade
            
        #reset all the inner data containers
        self._static = None
        self._scalar = None
        self._instrument = None 
        self._legs = None
        self._underlyingInstruments = None
        self._moneyflows = None
        self._salesCredits = None
        self._serializationType = None
        self._serializedData = None
        self._calcErrors = {}
        #performanceCounters
        self._tradeBuildTime = 0
        
    #**********************************************************#
    #Properties
    #*********************************************************#
    #FTrade
    @property
    def FTrade(self):
        return self._fTrade
    
    #Static
    @property
    def Static(self):
        return self._static
    
    @Static.setter
    def Static(self, value):
        self._static = value
    
    @property
    def StaticCount(self):
        if self.Static:
            return 1
        else:
            return 0
            
    #Scalar
    @property
    def Scalar(self):
        return self._scalar
    
    @Scalar.setter
    def Scalar(self, value):
        self._scalar = value
       
    @property
    def ScalarCount(self):
        if self.Scalar:
            return 1
        else:
            return 0

    #Instrument
    @property
    def Instrument(self):
        return self._instrument
    
    @Instrument.setter
    def Instrument(self, value):
        self._instrument = value
       
    @property
    def InstrumentCount(self):
        if self.Instrument:
            return 1
        else:
            return 0
       
    #Legs
    @property
    def Legs(self):
        return self._legs
    
    @Legs.setter
    def Legs(self, value):
        self._legs = value
        
    @property
    def LegCount(self):
        if not self.Legs:
            return 0
        else:
            return len(self.Legs)

    #UnderlyingInstruments
    @property
    def UnderlyingInstruments(self):
        return self._underlyingInstruments
    
    @UnderlyingInstruments.setter
    def UnderlyingInstruments(self, value):
        self._underlyingInstruments = value

    #UnderlyingKeys
    @property
    def UnderlyingKeys(self):
        return self._underlyingKeys

    @UnderlyingKeys.setter
    def UnderlyingKeys(self, value):
        self._underlyingKeys = value

    @property
    def UnderlyingInstrumentCount(self):
        if not self.UnderlyingInstruments:
            return 0
        else:
            return len(self.UnderlyingInstruments)
    
    #Moneyflows
    @property
    def Moneyflows(self):
        return self._moneyflows
    
    @Moneyflows.setter
    def Moneyflows(self, value):
        self._moneyflows = value
    
    @property
    def MoneyflowCount(self):
        if not self.Moneyflows:
            return 0
        else:
            return len(self.Moneyflows)
  
    #SalesCredits
    @property
    def SalesCredits(self):
        return self._salesCredits
    
    @SalesCredits.setter
    def SalesCredits(self, value):
        self._salesCredits = value
    
    @property
    def SalesCreditCount(self):
        if not self.SalesCredits:
            return 0
        else:
            return len(self.SalesCredits)
    
    #SerializationType
    @property
    def SerializationType(self):
        return self._serializationType
    
    @SerializationType.setter
    def SerializationType(self, value):
        self._serializationType = value
    
        
    #SerializedData
    @property
    def SerializedData(self):
        return self._serializedData
    
    #TradeBuildTime
    @property
    def TradeBuildTime(self):
        return self._tradeBuildTime
    
    @TradeBuildTime.setter
    def TradeBuildTime(self, value):
        self._tradeBuildTime = value
        
        
    #**********************************************************#
    #Methods
    #*********************************************************#
    def Calculate(self):
        self.calcStatic()
        self.calcScalar()
        self.calcInstrument()
        self.calcLegs()
        self.calcUnderlyings()
        self.calcMoneyflows()
        self.calcSalesCredits()
        self.calcUnderlyingKeys()
        
          
    def Serialize(self):
        self._serializedData = FC_SERIALIZATION.SerializeTrade(self.SerializationType, self)
        
    
    def GetInfoAsXml(self):
        rootElement  = Element(UTILS.Constants.fcGenericConstants.TRADE_INFO)
        FC_UTILS.AddXmlChildElement(rootElement, UTILS.Constants.fcGenericConstants.TRADE_BUILD_TIME, str(self.TradeBuildTime))
        FC_UTILS.AddXmlChildElement(rootElement, UTILS.Constants.fcGenericConstants.STATIC_COUNT, str(self.StaticCount))
        FC_UTILS.AddXmlChildElement(rootElement, UTILS.Constants.fcGenericConstants.SCALAR_COUNT, str(self.ScalarCount))
        FC_UTILS.AddXmlChildElement(rootElement, UTILS.Constants.fcGenericConstants.INSTRUMENT_COUNT, str(self.InstrumentCount))
        FC_UTILS.AddXmlChildElement(rootElement, UTILS.Constants.fcGenericConstants.LEG_COUNT, str(self.LegCount))
        FC_UTILS.AddXmlChildElement(rootElement, UTILS.Constants.fcGenericConstants.UNDERLYINGINSTRUMENT_COUNT, str(self.UnderlyingInstrumentCount))
        FC_UTILS.AddXmlChildElement(rootElement, UTILS.Constants.fcGenericConstants.MONEY_FLOW_COUNT, str(self.MoneyflowCount))
        FC_UTILS.AddXmlChildElement(rootElement, UTILS.Constants.fcGenericConstants.SALES_CREDIT_COUNT, str(self.SalesCreditCount))
        
        return tostring(rootElement)
        
    def GetErrorsAsXml(self):
        return FC_UTILS.GetXMLDictionary(self._calcErrors, 'tradeErrors')     

    def calcStatic(self):
        #Calc static
        if self.Static:
            try:
                self.Static.Calculate()
                self._calcErrors.update(self.Static.CalculationErrors)
                #Special step to add the trade domain to the calculation results
                self.Static.CalculationResults[UTILS.Constants.fcGenericConstants.TRADE_DOMAIN] = FC_UTILS.FC_UTILS.FrontArenaInstanceName
            except Exception, e:
                raise Exception(UTILS.Constants.fcExceptionConstants.COULD_NOT_CALC_STATIC_ATTR_TRADE %(str(self._fTrade.Oid()), str(e)))
    
    def calcScalar(self):
        if self.Scalar:
            try:
                self.Scalar.Calculate()
                self._calcErrors.update(self.Scalar.CalculationErrors)
            except Exception, e:
                raise Exception(UTILS.Constants.fcExceptionConstants.COULD_NOT_CALC_SCALAR_ATTR_TRADE %(str(self._fTrade.Oid()), str(e)))

    def calcInstrument(self):
        if self.Instrument:
            try:
                self.Instrument.Calculate()
                self._calcErrors.update(self.Instrument.CalculationErrors)
            except Exception, e:
                print str(e)
                raise Exception(UTILS.Constants.fcExceptionConstants.COULD_NOT_CALC_INTS_ATTR_TRADE %(str(self._fTrade.Oid()), str(e)))
                    
                    
    def calcLegs(self):
        if self.Legs:
            for leg in self.Legs:
                try:
                    leg.Calculate()
                    self._calcErrors.update(leg.CalculationErrors)
                except Exception, e:
                    raise Exception(UTILS.Constants.fcExceptionConstants.COULD_NOT_CALC_LEG_ATTR_TRADE %(str(self._fTrade.Oid()), str(e)))
                    
    def calcUnderlyings(self):
        if self.UnderlyingInstruments:
            for underlyingInstrument in self.UnderlyingInstruments:
                try:
                    underlyingInstrument.Calculate()
                    self._calcErrors.update(underlyingInstrument.CalculationErrors)
                    #Special step to add the parent Instrument address property
                    underlyingInstrument.CalculationResults[UTILS.Constants.fcGenericConstants.PARENT_INSTRUMENT_ADDRESS] = underlyingInstrument.ParentInstrumentAddress
                except Exception, e:
                    raise Exception(UTILS.Constants.fcExceptionConstants.COULD_NOT_CALC_UNDER_INSTR_ATTR_TRADE %(str(self._fTrade.Oid()), str(e)))

    def calcUnderlyingKeys(self):
        if self.UnderlyingKeys:
            for underlyingkey in self.UnderlyingKeys:
                try:
                    underlyingkey.Calculate()
                except Exception, e:
                    raise Exception(UTILS.Constants.fcExceptionConstants.COULD_NOT_CALC_UNDER_INSTR_ATTR_TRADE %(str(self._fTrade.Oid()), str(e)))

    def calcMoneyflows(self):
        if self.Moneyflows:
            for moneyflow in self.Moneyflows:
                try:
                    moneyflow.Calculate()
                    self._calcErrors.update(moneyflow.CalculationErrors)
                except Exception, e:
                    raise Exception(UTILS.Constants.fcExceptionConstants.COULD_NOT_CALC_MONF_ATTR_TRADE %(str(self._fTrade.Oid()), str(e)))
                    
   
    def calcSalesCredits(self):
        #Calc sales credits
        if self.SalesCredits:
            for salesCredit in self.SalesCredits:
                try:
                    salesCredit.Calculate()
                    self._calcErrors.update(salesCredit.CalculationErrors)
                except Exception, e:
                    raise Exception(UTILS.Constants.fcExceptionConstants.COULD_NOT_CALC_SCA_ATTR_TRADE %(str(self._fTrade.Oid()), str(e)))
                    

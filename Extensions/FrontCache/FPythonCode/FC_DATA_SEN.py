
'''----------------------------------------------------------------------------------------------------------
MODULE                  :       FC_DATA_SEN
PROJECT                 :       Front Cache
PURPOSE                 :       This class represents the Sensitivity data container
DEPARTMENT AND DESK     :       All Departments and all Desks.
REQUASTER               :       Front Cache
DEVELOPER               :       Gavin Wienand
CR NUMBER               :       XXXXXX
-------------------------------------------------------------------------------------------------------------
'''
#*********************************************************#
#Importing Modules
#*********************************************************#
import acm
import FC_UTILS
import FC_SERIALIZATION
from FC_UTILS import FC_UTILS as UTILS
from xml.etree.ElementTree import Element, tostring
from FC_DATA_ABSTRACT import FC_DATA_ABSTRACT as DATA_ABSTRACT
 
class FC_DATA_SEN(DATA_ABSTRACT):
    #*********************************************************#
    #Constructor
    #*********************************************************#
    def __init__(self, objectNumber, sensType,portfolioName=None, portfolioNumber=None):
        #find the object
        self._instrumentName = ''
        self._instrumentNumber = 0
        self._portfolioName = portfolioName
        self._portfolioNumber = portfolioNumber

        if sensType == UTILS.Constants.fcGenericConstants.PORTFOLIO:
            object = acm.FPhysicalPortfolio[objectNumber]
            self._portfolioName = object.Name()
            self._portfolioNumber = objectNumber
        elif sensType == UTILS.Constants.fcGenericConstants.INSTRUMENT:
            if not acm.FInstrument[objectNumber]:
                object = None
            else:
                query = acm.CreateFASQLQuery(acm.FTrade, 'AND')
                query.AddAttrNodeString('Instrument.Oid', objectNumber, 'EQUAL')
                query.AddAttrNodeString('Portfolio.Oid', portfolioNumber, 'EQUAL')
                #Undo hacking out the portfolio swaps - JB 18/04/2018
                #query.AddAttrNodeString('Instrument.InsType', 'Portfolio Swap', 'NOT_EQUAL')
                #Undo hacking out the portfolio swaps - JB 18/04/2018
                query.AddAttrNodeString('Status', ['Simulated', 'Void'], 'NOT_EQUAL')
                asql = acm.FASQLPortfolio(query)
                virtual_portfolio = acm.FAdhocPortfolio()
                virtual_portfolio.Add(asql.Trades())
                object = virtual_portfolio
                self._instrumentName = acm.FInstrument[objectNumber].Name()
                self._instrumentNumber = objectNumber
                self._type = acm.FInstrument[objectNumber].InsType()


        if not object:
            raise Exception(UTILS.Constants.fcExceptionConstants.STL_NOT_FOUND % str(objectNumber))
        else:
            self._fObject = object
            
        #reset all the inner data containers
        self._sensitivityWorkbook = None
        self._serializationType   = None
        self._serializedData      = None
        self._sensType = sensType
        #performanceCounters
        self._objectBuildTime = 0
        
    #**********************************************************#
    #Properties
    #*********************************************************#
    #FObject Portfolio or Instrument
    @property
    def FObject(self):
        return self._fObject
    
    #PortfolioSheet
    @property
    def SensitivityWorkbook(self):
        return self._sensitivityWorkbook

    @property
    def InstrumentName(self):
        return self._instrumentName

    @property
    def InstrumentNumber(self):
        return self._instrumentNumber

    @property
    def PortfolioName(self):
        return self._portfolioName

    @property
    def PortfolioNumber(self):
        return self._portfolioNumber

    @property
    def SensType(self):
        return self._sensType

    @property
    def InstrumentType(self):
        return self._type

    @SensitivityWorkbook.setter
    def SensitivityWorkbook(self, value):
        self._sensitivityWorkbook = value
    
    @property
    def SensitivityWorkbookCount(self):
        if self.SensitivityWorkbook:
            return 1
        else:
            return 0
    
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
    
    #SettlementBuildTime
    @property
    def ObjectBuildTime(self):
        return self._objectBuildTime
    
    @ObjectBuildTime.setter
    def ObjectBuildTime(self, value):
        self._objectBuildTime = value
        
        
    #**********************************************************#
    #Methods
    #*********************************************************#
    def Calculate(self):
        self.calcSensitivityWorkbook()

    def Serialize(self):
        self._serializedData = FC_SERIALIZATION.SerializeSensitivity(self.SerializationType, self, self._sensType)
        
    
    def GetInfoAsXml(self):
        rootElement  = Element(UTILS.Constants.fcGenericConstants.SETTLEMENT_INFO)
        FC_UTILS.AddXmlChildElement(rootElement, 'SENSITIVITY BUILD TIME', str(self.ObjectBuildTime))
        FC_UTILS.AddXmlChildElement(rootElement, 'SENSITIVITY WORKBOOK COUNT', str(self.SensitivityWorkbookCount))
        return tostring(rootElement)
        
    def GetErrorsAsXml(self):
        rootElement  = Element(UTILS.Constants.fcGenericConstants.SETTLEMENT_ERRORS)
        return tostring(rootElement)

    def calcSensitivityWorkbook(self):
        if self.SensitivityWorkbook:
            try:
                self.SensitivityWorkbook.Calculate()
            except Exception, e:
                raise Exception(UTILS.Constants.fcExceptionConstants.COULD_NOT_CALC_SENSITIVITY_WB %(str(self.FObject.ClassName()), str(self.FObject.Oid()), str(e)))        

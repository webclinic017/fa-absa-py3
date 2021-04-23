
from __future__ import print_function
import acm
    
def SetUpLeveragedETF(definitionSetUp):
    from DealCaptureSetup import  AddInfoSetUp, CustomMethodSetUp
    definitionSetUp.AddSetupItems(
                        AddInfoSetUp( recordType='Instrument',
                                      fieldName='LeveragedETF',
                                      dataType='Boolean',
                                      description='CustomInsdef',
                                      dataTypeGroup='Standard',
                                      subTypes=['ETF'],
                                      defaultValue='',
                                      mandatory=False),
                                      
                        AddInfoSetUp( recordType='Instrument',
                                      fieldName='CashBalance',
                                      dataType='Double',
                                      description='CustomInsdef',
                                      dataTypeGroup='Standard',
                                      subTypes=['ETF'],
                                      defaultValue='',
                                      mandatory=False),
                                      
                        AddInfoSetUp( recordType='Instrument',
                                      fieldName='Nominal',
                                      dataType='Double',
                                      description='CustomInsdef',
                                      dataTypeGroup='Standard',
                                      subTypes=['ETF'],
                                      defaultValue='',
                                      mandatory=False),
                                      
                        AddInfoSetUp( recordType='Instrument',
                                      fieldName='Divisor',
                                      dataType='Double',
                                      description='CustomInsdef',
                                      dataTypeGroup='Standard',
                                      subTypes=['ETF'],
                                      defaultValue='',
                                      mandatory=False),
                                      
                        AddInfoSetUp( recordType='Instrument',
                                      fieldName='SettleClose',
                                      dataType='Double',
                                      description='CustomInsdef',
                                      dataTypeGroup='Standard',
                                      subTypes=['ETF'],
                                      defaultValue='',
                                      mandatory=False)
                                )
                                
    definitionSetUp.AddSetupItems(
                        CustomMethodSetUp( className='FETF',
                                           customMethodName='GetLeveragedETF',
                                           methodName='LeveragedETF'),
                                           
                        CustomMethodSetUp( className='FETF',
                                           customMethodName='GetLeveragedETFFundCash',
                                           methodName='LeveragedETFFundCash'),
                                           
                        CustomMethodSetUp( className='FETF',
                                           customMethodName='GetLeveragedETFFundDivisor',
                                           methodName='LeveragedETFFundDivisor'),
                                           
                        CustomMethodSetUp( className='FETF',
                                           customMethodName='GetLeveragedETFSettleClose',
                                           methodName='LeveragedETFSettleClose'),
                                           
                        CustomMethodSetUp( className='FETF',
                                           customMethodName='GetLeveragedETFFundNominal',
                                           methodName='LeveragedETFFundCash'),
                                           
                        CustomMethodSetUp( className='FETF',
                                           customMethodName='GetLeveragedETFLeverage',
                                           methodName='Leverage'),
                                           
                        CustomMethodSetUp( className='FETF',
                                           customMethodName='GetLeveragedETFUnderlyingType',
                                           methodName='LeveragedETFUnderlyingType'),
                                           
                        CustomMethodSetUp( className='FETF',
                                           customMethodName='SetLeveragedETFFundCash',
                                           methodName='LeveragedETFFundCash'),
                                           
                        CustomMethodSetUp( className='FETF',
                                           customMethodName='SetLeveragedETFFundDivisor',
                                           methodName='LeveragedETFFundDivisor'),
                                           
                        CustomMethodSetUp( className='FETF',
                                           customMethodName='SetLeveragedETFSettleClose',
                                           methodName='LeveragedETFSettleClose'),
                                           
                        CustomMethodSetUp( className='FETF',
                                           customMethodName='SetLeveragedETFFundNominal',
                                           methodName='LeveragedETFFundNominal'),
                                           
                        CustomMethodSetUp( className='FETF',
                                           customMethodName='SetLeveragedETFUnderlyingType',
                                           methodName='LeveragedETFUnderlyingType')
                                )
    
def SetUnderlyingType(instrument, underlyingType):
    instrument.UnderlyingType(underlyingType)
    return
    
def GetUnderlyingType(instrument):
    return instrument.UnderlyingType()

def GetLeveragedETF(instrument):
    try:
        if instrument.AdditionalInfo().LeveragedETF():
            return instrument.AdditionalInfo().LeveragedETF()
        else:
            return False
    except:
        print ("Additional Info field missing. Please create an Additional Info field on Instrument (ETF) of type boolean called LeveragedETF and restart system")
    
    
def GetLeverage(instrument):
    calcSpace=acm.FCalculationMethods().CreateStandardCalculationsSpaceCollection()
    cash=instrument.AdditionalInfo().CashBalance()
    nominal=instrument.AdditionalInfo().Nominal()
    yesterday=acm.Time().DateAdjustPeriod(acm.Time().DateToday(), '-1d')
    underlying=instrument.Underlying()
    try:
        price=underlying.Calculation().MarkToMarketPrice(calcSpace, yesterday, instrument.Currency(), ).Number()
        leverage = nominal * 100 * price / cash
    except:   
        return 0
    return leverage

       
def GetFundCash(instrument):    
    try:
        if instrument.AdditionalInfo().CashBalance():
            return instrument.AdditionalInfo().CashBalance()
        else:
            return 0.0
    except:
        print ("Additional Info field missing. Please create an Additional Info field on Instrument (ETF) of type double called CashBalance and restart system.")


def SetFundCash(instrument, cash):
    try:
        instrument.AdditionalInfo().CashBalance(cash)
    except:
        print ("Additional Info field missing. Please create an Additional Info field on Instrument (ETF) of type double called CashBalance and restart system.")
    return


def GetFundNominal(instrument):
    try:
        if instrument.AdditionalInfo().Nominal():
            return instrument.AdditionalInfo().Nominal()
        else:
            return 0.0
    except:
        print ("Additional Info field missing. Please create an Additional Info field on Instrument (ETF) of type double called Nominal and restart system.")
        
def SetFundNominal(instrument, nominal):
    try:
        instrument.AdditionalInfo().Nominal(nominal)
    except:
        print ("Additional Info field missing. Please create an Additional Info field on Instrument (ETF) of type double called Nominal and restart system.")

def GetFundDivisor(instrument):
    try:
        if instrument.AdditionalInfo().Divisor():
            return instrument.AdditionalInfo().Divisor()
        else:
            return 0.0
    except:
        print ("Additional Info field missing. Please create an Additional Info field on Instrument (ETF) of type double called Divisor and restart system.")

def SetFundDivisor(instrument, divisor):    
    try:
        instrument.AdditionalInfo().Divisor(divisor)
    except:
        print ("Additional Info field missing. Please create an Additional Info field on Instrument (ETF) of type double called Divisor and restart system")

def GetSettleClose(instrument):
    try:
        if instrument.AdditionalInfo().SettleClose():
            return instrument.AdditionalInfo().SettleClose()
        else:
            return 0.0
    except:
        print ("Additional Info field missing. Please create an Additional Info field on Instrument (ETF) of type double called SettleClose and restart system.")

def SetSettleClose(instrument, settleClose):    
    try:
        instrument.AdditionalInfo().SettleClose(settleClose)
    except:
        print ("Additional Info field missing. Please create an Additional Info field on Instrument (ETF) of type double called SettleClose and restart system")

def UpdateDefaultInstrument(ins):
    try:
    # Not possible to set AddInfo fields on default instrument. Set Mini Future field to true.
        ins.AdditionalInfo().LeveragedETF(True)
    except:
        print ("Additional Info field missing. Please create an Additional Info field on Instrument (ETF) of type boolean called LeveragedETF and restart system")
        
    underlying = ins.Underlying()
    if not underlying or underlying.InsType() != "Future/Forward":
        # No Leveraged ETF default instrument created yet. Set underlying to first future in the ETF currency.
        query = "insType='Future/Forward' and currency='" + ins.Currency().Name() + "'"
        futures = acm.FInstrument.Select(query)
        ins.Underlying = futures.First()

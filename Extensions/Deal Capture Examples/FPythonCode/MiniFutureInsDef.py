
from __future__ import print_function
import acm, ael

def SetUpMiniFuture(definitionSetUp):
    from DealCaptureSetup import  AddInfoSetUp, CustomMethodSetUp
    definitionSetUp.AddSetupItems(
                        AddInfoSetUp( recordType='Instrument',
                                      fieldName='MiniFuture',
                                      dataType='Boolean',
                                      description='CustomInsdef',
                                      dataTypeGroup='Standard',
                                      subTypes=['Warrant'],
                                      defaultValue='',
                                      mandatory=False),
                                      
                        AddInfoSetUp( recordType='Instrument',
                                      fieldName='RateMargin',
                                      dataType='Double',
                                      description='CustomInsdef',
                                      dataTypeGroup='Standard',
                                      subTypes=['Warrant'],
                                      defaultValue='',
                                      mandatory=False)
                                )

    definitionSetUp.AddSetupItems(
                        CustomMethodSetUp( className='FWarrant',
                                           customMethodName='GetMiniFuture',
                                           methodName='MiniFuture'),
                                           
                        CustomMethodSetUp( className='FWarrant',
                                           customMethodName='GetMiniFutureFinancingLevel',
                                           methodName='MiniFutureFinancingLevel'),
                                           
                        CustomMethodSetUp( className='FWarrant',
                                           customMethodName='GetMiniFutureFinancingSpread',
                                           methodName='MiniFutureFinancingSpread'),
                                           
                        CustomMethodSetUp( className='FWarrant',
                                           customMethodName='GetMiniFutureInterestRateMargin',
                                           methodName='MiniFutureInterestRateMargin'),
                                           
                        CustomMethodSetUp( className='FWarrant',
                                           customMethodName='GetMiniFutureStopLoss',
                                           methodName='MiniFutureStopLoss'),
                                           
                        CustomMethodSetUp( className='FWarrant',
                                           customMethodName='GetMiniFutureUnderlyingType',
                                           methodName='MiniFutureUnderlyingType'),
                                           
                        CustomMethodSetUp( className='FWarrant',
                                           customMethodName='GetMiniFutureUnderlyingType',
                                           methodName='MiniFutureUnderlyingType'),
                                           
                        CustomMethodSetUp( className='FWarrant',
                                           customMethodName='SetMiniFuture',
                                           methodName='SetMiniFuture'),
                                           
                        CustomMethodSetUp( className='FWarrant',
                                           customMethodName='SetMiniFutureFinancingLevel',
                                           methodName='MiniFutureFinancingLevel'),
                                           
                        CustomMethodSetUp( className='FWarrant',
                                           customMethodName='SetMiniFutureInterestRateMargin',
                                           methodName='MiniFutureInterestRateMargin'),
                                           
                        CustomMethodSetUp( className='FWarrant',
                                           customMethodName='SetMiniFutureStopLoss',
                                           methodName='MiniFutureStopLoss'),
                                           
                        CustomMethodSetUp( className='FWarrant',
                                           customMethodName='SetMiniFutureUnderlyingType',
                                           methodName='MiniFutureUnderlyingType')
                                )
    
def SetUnderlyingType(instrument, underlyingType):
    instrument.UnderlyingType(underlyingType)
    return
    
def GetUnderlyingType(instrument):
    return instrument.UnderlyingType()
          
def GetMiniFuture(instrument):
    isMiniFuture = None
    try:
        isMiniFuture = instrument.AdditionalInfo().MiniFuture()
    except Exception as e:
        print ("Additional Info field missing. Please create an Additional Info field on Instrument (Warrant) of type boolean called MiniFuture and restart system.")
    return isMiniFuture
  
def GetFinancingSpread(instrument):
    if instrument.StrikePrice():
        premium=instrument.Barrier()-instrument.StrikePrice()
        premiumPercent=premium/instrument.StrikePrice()*100
        return premiumPercent
    else:
        return 0

def SetStopLoss(instrument, stopLoss):
    instrument.Barrier(stopLoss)
    if instrument.StrikePrice():
        premium=instrument.Barrier()-instrument.StrikePrice()
        if premium < 0:
            instrument.SuggestOptionType(False)
        else:
            instrument.SuggestOptionType(True)
    return
    
def GetStopLoss(instrument):
    return instrument.Barrier()
    
def SetFinancingLevel(instrument, financingLevel):
    instrument.StrikePrice(financingLevel)
    if instrument.StrikePrice():
        premium=instrument.Barrier()-instrument.StrikePrice()
        if premium < 0:
            instrument.SuggestOptionType(False)
        else:
            instrument.SuggestOptionType(True)
    return
    
def GetFinancingLevel(instrument):
    return instrument.StrikePrice()

def SetMiniFuture(instrument, miniFuture):
    try:
        instrument.AdditionalInfo().MiniFuture(miniFuture)
    except:
        print ("Additional Info field missing. Please create an Additional Info field on Instrument (Warrant) of type boolean called MiniFuture and restart system.")
    return
    
def SetRateMargin(instrument, rateMargin):
    try:
        instrument.AdditionalInfo().RateMargin(rateMargin)
    except:
        print ("Additional Info field missing. Please create an Additional Info field on Instrument (Warrant) of type double called RateMargin and restart system.")
    
def GetRateMargin(instrument):
    try:
        if instrument.AdditionalInfo().RateMargin():
            return instrument.AdditionalInfo().RateMargin()
        else:
            return 0.0
    except:
        print ("Additional Info field missing. Please create an Additional Info field on Instrument (Warrant) of type double called RateMargin and restart system.")
    
def UpdateDefaultInstrument(ins):
    # Not possible to set AddInfo fields on default instrument. Set Mini Future field to true.
    try:
        ins.AdditionalInfo().MiniFuture(True)
    except:
        print ("Additional Info field missing. Please create an Additional Info field on Instrument (Warrant) of type boolean called MiniFuture and restart system.")
    
    if not ins.Exotic():
    # This code will set up the Barrier if no default barrier instrument exists
        ins.ExoticType('Other')
        e=acm.FExotic()
        ins.Exotics().Add(e)
        e.RegisterInStorage()
        e.BarrierOptionType("Up & In")   
  
    

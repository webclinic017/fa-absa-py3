
import acm
#----------------------------------------------------------------------------
def GetClientSpreadRateIndexMarket():
    return acm.FParty["SPOT"]
    
#----------------------------------------------------------------------------
def GetSecuritySpreadRateIndex(security):
    try:
        spread = security.AdditionalInfo().PS_SecuritySpread()
    except:
        raise Exception("Missing Additional Info Spec PS_SecuritySpread on Instrument")
    return spread

#----------------------------------------------------------------------------
def GetContext(dealPackage):
    '''Return the context to which the accounting parameters should be saved.'''
    return acm.FContext['Global']

#----------------------------------------------------------------------------
def GetStockSpreadInstrument(stock):
    return GetSecuritySpreadRateIndex(stock)

#----------------------------------------------------------------------------
def SetUpCustomizedPortfolioSwapDefinition( definitionSetUp ):
    from DealPackageSetUp import  AddInfoSetUp
    definitionSetUp.AddSetupItem(
                        AddInfoSetUp( recordType='Instrument',
                                      fieldName='PS_SecuritySpread',
                                      dataType='Instrument',
                                      description='PS_SecuritySpread',
                                      dataTypeGroup='RecordRef',
                                      subTypes=['Stock'],
                                      defaultValue='',
                                      mandatory=False)
                                )
#----------------------------------------------------------------------------
def GetPayOutCashPaymentType():
    return "Cash"
#----------------------------------------------------------------------------


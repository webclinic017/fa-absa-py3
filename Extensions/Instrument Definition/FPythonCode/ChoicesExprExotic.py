
import acm
from ChoicesExprCommon import allEnumValuesExcludeNone

def getAsianOptionTypeChoices():
    return allEnumValuesExcludeNone( acm.FEnumeration['enum(AsianOptionType)'] )

def getKIKOTypeChoices():
    return allEnumValuesExcludeNone( acm.FEnumeration['enum(KIKOGUIOptionType)'] )

def getStraddleTypeChoices():
    return allEnumValuesExcludeNone( acm.FEnumeration['enum(StraddleGUIOptionType)'] )
    
def getAverageMethodTypeChoices():
    return allEnumValuesExcludeNone( acm.FEnumeration['enum(AverageMethodType)'] )

def getAveragePriceTypeChoices( averageStrikeType ):
    if averageStrikeType in ['Float', 'Fix']:
        return ['None', 'Average']
    return acm.FEnumeration['enum(AveragePriceType)'].Enumerators()

def getAverageStrikeTypeChoices( averagePriceType ):
    if averagePriceType == 'Float':
        return ['None', 'Average']
    return acm.FEnumeration['enum(AverageStrikeType)'].Enumerators()    

def getBarrierOptionTypeChoices():
    return [e for e in acm.FEnumeration['enum(BarrierOptionType)'].Enumerators() if(e != 'KIKO Down In Up Out' and e!= 'KIKO Up In Down Out')]

def getBarrierFXOptionTypeChoices():
    return [e for e in acm.FEnumeration['enum(BarrierOptionType)'].Enumerators() if(e != 'KIKO Down In Up Out' and e != 'KIKO Up In Down Out' and e != 'None')]	

def getDigitalEuropeanOptionTypeChoices():
    return allEnumValuesExcludeNone( acm.FEnumeration['enum(DigitalEuropeanOptionType)'] )

def getLookbackOptionTypeChoices():
    return allEnumValuesExcludeNone( acm.FEnumeration['enum(LookBackOption)'] )
    
def getTouchOptionTypeChoices():
    return allEnumValuesExcludeNone( acm.FEnumeration['enum(TouchOptionType)'] )
        
def getBarrierMonitoringChoices( exotic ):
    choices = acm.FEnumeration['enum(BarrierMonitoring)'].Enumerators()
    if exotic.BarrierOptionType() in ['KIKO Down In Up Out', 'KIKO Up In Down Out']:
        return choices
    else:
        return [c for c in choices if c != 'At Expiry']
        
def getVariationSwapTypeChoices():
    choices = [e for e in acm.FEnumeration['enum(VarianceSwapType)'].Enumerators() if (e in ('None', 'Custom', 'Cap', 'Floor', 'Cap/Floor'))]
    return acm.FIndexedPopulator(choices)
    
def getVariationSwapCorridorTypeChoices():
    return acm.FIndexedPopulator(acm.FEnumeration['enum(VariationSwapCorridorType)'].Enumerators())

def getPmOptionBaseType(exotic):
    return ['Vanilla', 'Barrier', 'Digital American', 'Digital European']

import acm
import RiskFactorExtensions
import FRTBCustomOverrides

import FRTBSAHierarchy, PLExplainExtensions

def SymbolOrNone( s ):
    if s is not None:
        return acm.FSymbol( s )
    return None
    

def FRTBPerimeterCriteria( riskClass ):
    mainFunction = acm.GetFunction( 'frtbPerimeterCriteriaIsSatisfiedBy', 2 )
    subFunction = acm.GetFunction( 'frtbPerimeterSubCriteriaIsSatisfiedBy', 2 )
    subCriteria = subFunction.CreateCall( [None, riskClass] )
    return mainFunction.CreateCall( [None, subCriteria] )

#PUBLISHED
def FRTBPerimeterSubCriteriaIsSatisfiedBy( anObject, riskClass ):
    instrument = None
    if anObject.IsKindOf( acm.FLeg ):
        instrument = anObject.Instrument()
    elif anObject.IsKindOf( acm.FInstrument ):
        instrument = anObject
    if instrument:
        return instrument.FRTBRiskClass() != riskClass
    return False

#PUBLISHED
def FRTBPerimeterCriteriaIsSatisfiedBy( anObject, subCriteria ):
    if anObject.IsEvaluator():
        proprietor = anObject.Proprietor()
        if proprietor and proprietor.IsEvaluator() and proprietor.FindAdHoc( subCriteria ):
            return True
    return False

def FRTBPerimeterEntities( riskClass ):
    if riskClass in ["CSR (NS)", "CSR (S-C)"]:
        return ['creditCurve', 'discountCurve', 'creditCurves']
    return []
    

#PUBLISHED
def FRTBRiskClass(instrument):
    riskClass = FRTBCustomOverrides.Custom_FRTBRiskClass( instrument )
    if riskClass:
        return riskClass
    if instrument.IsCreditBasket():
        return "CSR (S-C)"
    return "CSR (NS)"

#PUBLISHED
def FRTBIsOption(instrument):
    isOption = FRTBCustomOverrides.Custom_FRTBIsOption(instrument)
    if (None == isOption):
        isOption = (instrument.InsType() in ['Option', 'Warrant', 'Cap', 'Floor', 'Collar']) or instrument.Callable() or instrument.Putable()
    return isOption

#PUBLISHED
def FRTBResidualRiskType(instrument):
    customResidualRiskType = FRTBCustomOverrides.Custom_FRTBResidualRiskType( instrument )
    if customResidualRiskType:
        return customResidualRiskType
        
    residualRiskType = 'None'
    if instrument.IsVolatilityOrVarianceSwap():
        residualRiskType = 'Exotic'
    elif FRTBIsOption(instrument):
        if (('None' != instrument.ExoticType()) or 
            (instrument.IsKindOf('FOption') and (instrument.IsAsian() or instrument.Digital() or instrument.IsBasket()))):
            residualRiskType = 'Other'
    return residualRiskType

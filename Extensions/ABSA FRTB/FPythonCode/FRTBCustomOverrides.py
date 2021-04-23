
import acm

def Custom_FRTBRiskClass( instrument ):
    """
    Add logic for which credit risk class an instrument
    is sensitivie to, has to be one of:
    "CSR (NS)", "CSR (S-C)" or "CSR (S-NC)".
    Return type: string.
    Return None to fallback to default implementation.
    """
    return None

def Custom_DRCCreditQuality( party ):
    """
    Add logic for party Credit Quality, has to be one of:
    "AAA", "AA", "A", "BBB", "BB", "B", "CCC", "Unrated", "Defaulted".
    Return type: string.
    Return None to fallback to default implementation.
    """
    ratings = ["AAA", "AA", "A", "BBB", "BB", "B", "CCC", "Unrated", "Defaulted"]
    rating  = party.Rating3()

    if rating and (rating.Name() in ratings):
        rating_name = rating.Name()
    else:
        rating_name = "Unrated"
        
    return rating_name
    
def Custom_DRCIssuerType( party ):
    """
    Add logic for party issuer type, has to be one of:
    "Corporates", "Local Governments/Municipalities" or "Sovereigns".
    Return type: string.
    Return None to fallback to default implementation.
    """
    issuer_sector_entity = party.Free4ChoiceList()
    drc_class = "Corporates"
    if issuer_sector_entity:
        issuer_sector = issuer_sector_entity.Name()
        if issuer_sector == "SOV":
            drc_class = "Sovereigns"
        elif issuer_sector in ("Municipal", "SOE"):
            drc_class = "Local Governments/Municipalities"
    else:
        drc_class = "No Issuer Sector"
    return drc_class
    
def Custom_DRCSeniority( instrument ):
    """
    Add logic for instrument seniority for Default Risk Charge,
    has to be one of:
    "Equity/Non-Senior Debt", "Senior Debt", "Covered Bonds" or "Other".
    Return type: string.
    Return None to fallback to default implementation.
    """
        #If the instrument type is not in the list return the most prudent Seniority
    seniority = "Senior Debt"
    ins_type  = instrument.InsType()

    #Get Underlying Type for Futures/Forwards and Options
    if ins_type in ['Future/Forward', 'Option']:
        ins_type = instrument.Underlying().InsType()
        
    if ins_type in ['Stock', 'EquityIndex', 'ETF', 'Combination', 'IndexLinkedSwap', 'PriceSwap', 'VarianceSwap', 'Swap', 'TotalReturnSwap']:
        seniority = "Equity/Non-Senior Debt"
    elif ins_type in ['FRN', 'Bond', 'Bill', 'IndexLinkedBond', 'CreditDefaultSwap']:
        seniority = "Senior Debt"
    elif ins_type in ['CreditIndex']:
        seniority = "Senior Debt"
    
    return seniority
    
def Custom_FRTBIsOption( instrument ):
    """
    Add logic for whether instrument is option in
    Standardised Approach calculations, has to be one of:
    True or False.
    Return type: bool.
    Return None to fallback to default implementation.
    """
    isOption = (instrument.InsType() in ['Option', 'Warrant', 'Cap', 'Floor', 'Collar']) or instrument.Callable() or instrument.Putable()
    
    return isOption

def Custom_FRTBResidualRiskType( instrument ):
    """
    Add logic for instrument residual risk type,
    has to be one of:
    "Exotic", "Other" or "None".
    Return type: string.
    Return None to fallback to default implementation.
    """
    residualRiskType = 'None'
    if instrument.IsVolatilityOrVarianceSwap():
        residualRiskType = 'Exotic'
    elif Custom_FRTBIsOption(instrument):
        if (('None' != instrument.ExoticType()) or 
            (instrument.IsKindOf('FOption') and (instrument.IsAsian() or instrument.Digital() or instrument.IsBasket() or instrument.IsRangeAccrual() or instrument.IsBarrier()))):
            residualRiskType = 'Other'
    return residualRiskType

def Custom_LossGivenDefault( issuer, issuerType, creditRating, seniority ):
    """
    Add logic for Loss Given Default given the issuer and seniority
    should be a value between 0.0 and 1.0
    Return type: double.
    Return None to fallback to default implementation.
    """
    return None

def Custom_DRCRemainingMaturity( instrument ):
    """
    Add logic for calculation of remaining maturity.
    should return python float value.
    Return None to fallback to default implementation.
    """
    return None

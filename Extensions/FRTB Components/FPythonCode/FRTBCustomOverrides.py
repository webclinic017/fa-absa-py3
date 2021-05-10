
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
    return None
    
def Custom_DRCIssuerType( party ):
    """
    Add logic for party issuer type, has to be one of:
    "Corporates", "Local Governments/Municipalities" or "Sovereigns".
    Return type: string.
    Return None to fallback to default implementation.
    """
    return None
    
def Custom_DRCSeniority( instrument ):
    """
    Add logic for instrument seniority for Default Risk Charge,
    has to be one of:
    "Equity/Non-Senior Debt", "Senior Debt", "Covered Bonds" or "Other".
    Return type: string.
    Return None to fallback to default implementation.
    """
    return None
    
def Custom_FRTBIsOption( instrument ):
    """
    Add logic for whether instrument is option in
    Standardised Approach calculations, has to be one of:
    True or False.
    Return type: bool.
    Return None to fallback to default implementation.
    """
    return None

def Custom_FRTBResidualRiskType( instrument ):
    """
    Add logic for instrument residual risk type,
    has to be one of:
    "Exotic", "Other" or "None".
    Return type: string.
    Return None to fallback to default implementation.
    """
    return None

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

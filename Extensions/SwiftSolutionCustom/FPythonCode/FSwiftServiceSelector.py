"""----------------------------------------------------------------------------
Compiled: 2019-07-01 15:14:44
#__src_file__ = "extensions/swift/etc/FSwiftServiceSelector.py"

MODULE:
    FSwiftServiceSelector

DESCRIPTION:
    This module provides customizable functions to determine if a message should be generated via
    Swift Solutions or Adaptiv Docs

------------------------------------------------------------------------------------------------------------------------
HISTORY
========================================================================================================================
Date            Change no       Developer               Requester               Description
------------------------------------------------------------------------------------------------------------------------
2020-12-11      FAOPS-821       Tawanda Mukhalela       Martin Wortmann         Added functions to channel cash payments
                                                                                via adaptiv given certain criteria
2021-01-27      FAOPS-1039      Tawanda Mukhalela       Gasant Thulsie          Added check to exclude SBL payments from
                                                                                adaptiv checks.
2021-03-09      FAOPS-1027      Willie vd Bank          Martin Wortmann         Removed override which excluded netted
                                                                                payments from being generated. Applied
                                                                                a core fix in FSwiftMTCalculatorHook.
------------------------------------------------------------------------------------------------------------------------
"""
import acm, traceback
from FSwiftExceptions import SwiftWriterAPIException
from FSettlementHooks import get_funding_settlement_message_type
from SettlementConstants import ABSA_BANK
SBL_MESSAGE_TYPES = ('0', '540', '541', '542', '543', '598_130', '598_131', '598_132')


def is_security_loan_settlement(fObject, message_type_from_mt_calculator):
    if not fObject.IsKindOf(acm.FSettlement):
        return False
        
    if fObject.Trade() is None:
        return False

    if fObject.Trade().TradeInstrumentType() != 'SecurityLoan':
        return False
        
    if message_type_from_mt_calculator not in SBL_MESSAGE_TYPES:
        return False
    return True
    
    
def is_collateral_settlement(fObject, message_type_from_mt_calculator):
    if not fObject.IsKindOf(acm.FSettlement):
        return False
        
    if fObject.Trade() is None:
        return False
        
    if fObject.Trade().TradeCategory() != 'Collateral':
        return False
        
    if message_type_from_mt_calculator not in SBL_MESSAGE_TYPES:
        return False
    return True
    
    
def is_off_market_security_loan_settlement(fObject, message_type_from_mt_calculator):
    if is_security_loan_settlement(fObject, message_type_from_mt_calculator):
        settle_category = fObject.Trade().SettleCategoryChlItem()
        if settle_category and settle_category.Name() == 'SL_CUSTODIAN':
            if fObject.Trade().Instrument().OpenEnd() == 'Open End':
                return True
    return False


def is_off_market_collateral_settlement(fObject, message_type_from_mt_calculator):
    if is_collateral_settlement(fObject, message_type_from_mt_calculator):
        settle_category = fObject.Trade().SettleCategoryChlItem()
        if settle_category and settle_category.Name() == 'SL_CUSTODIAN':
            return True
    return False


def is_SBL_settlement(fObject, mtType):
    if is_off_market_security_loan_settlement(fObject, mtType):
        return True
    if is_off_market_collateral_settlement(fObject, mtType):
        return True
    return False


def was_previously_released_by_adaptiv(fObject, message_type):
    go_live_date = '2020-12-12'
    if not fObject.IsKindOf(acm.FSettlement):
        return False
    if fObject.IsPreReleased():
        return False
    if is_SBL_settlement(fObject, message_type):
        return False
    if fObject.ValueDay() >= go_live_date and fObject.CreateDay() >= go_live_date:
        return False
    if not _has_document_generated_by_adaptiv(fObject):
        return False

    return True


def _has_document_generated_by_adaptiv(fObject):
    for document in fObject.Documents().AsArray():
        if document.DocumentId() > 0:
            return True
    return False
    

def bypass_Swift_Solutions(fObject):
    import FSwiftWriterAPIs
    should_bypass_Swift_Solutions = False
   
    message_type = str(FSwiftWriterAPIs.get_swift_mt_type(fObject))
    
    if message_type in ['540', '542'] and not is_SBL_settlement(fObject, message_type):
        should_bypass_Swift_Solutions = True
    if is_unsupported_settlement(fObject):
        should_bypass_Swift_Solutions = True
    if was_previously_released_by_adaptiv(fObject, message_type):
        should_bypass_Swift_Solutions = True
    return should_bypass_Swift_Solutions


def _is_dis_instrument(fObject):
    """
    Checks if FObect is related to a DIS Instrument
    """
    if not fObject.Trade():
        return False
    trade = fObject.Trade()
    instrument = trade.Instrument()
    if instrument.AdditionalInfo().DIS_Instrument():
        return True

    return False


def _is_demat_instrument(fObject):
    """
    Checks if FObect is related to a Demat Instrument
    """
    if not fObject.Trade():
        return False
    trade = fObject.Trade()
    instrument = trade.Instrument()
    if instrument.AdditionalInfo().Demat_Instrument():
        return True

    return False


def _is_accounting_settlement(fObject):
    """
    Checks if FObject is an accounting message
    """
    if not fObject.IsKindOf(acm.FSettlement):
        return False
    if fObject.TheirCorrBank() != ABSA_BANK:
        return False

    return True


def _is_funding_settlement(fObject):
    """
    Check if FObject is a funding settlement
    """
    if not fObject.IsKindOf(acm.FSettlement):
        return False
    if get_funding_settlement_message_type(fObject, None) is None:
        return False

    return True
    

def _is_direct_payment(fObject):
    """
    Check if payment is an FRD Direct Payment
    """
    if not fObject.IsKindOf(acm.FSettlement):
        return False
    settlement = fObject 
    trade = settlement.Trade()
    if not trade:
        return False
    funding_instype = trade.AdditionalInfo().Funding_Instype()
    if funding_instype and funding_instype.startswith('FRD'):
        return True
    return False


def _is_prime_broking_party(fObject):
    """
    Check if party is a PB Reporting Party
    """
    if not fObject.IsKindOf(acm.FSettlement):
        return False
    prime_broking_portfolio = fObject.Counterparty().add_info('PB_Reporting_Prf')
    if prime_broking_portfolio:
        return True
    return False


def _is_sbl_settle_category(fObject):
    """
    checks if the Object is booked against SBL settle categories
    """
    if not fObject.Trade():
        return False
    settle_category = fObject.Trade().SettleCategoryChlItem()
    if not settle_category:
        return False
    if settle_category.Name() not in ('SL_CUSTODIAN', 'SL_STRATE'):
        return False

    return True


def is_unsupported_settlement(fObject):
    """
    Checks settlement against a few exclusion criteria
    """
    if _is_sbl_settle_category(fObject):
        return False
    if _is_dis_instrument(fObject):
        return True
    if _is_demat_instrument(fObject):
        return True
    if _is_accounting_settlement(fObject):
        return True
    if _is_funding_settlement(fObject):
        return True
    if _is_direct_payment(fObject):
        return True
    if _is_prime_broking_party(fObject):
        return True

    return False
    

def UseSwiftWriterForMessage(fObject):
    useSwiftWriter = False
    try:
        import FSwiftWriterAPIs

        mtType = FSwiftWriterAPIs.get_swift_mt_type(fObject)
        mtTypeString = 'MT{}'.format(mtType)
        useSwiftWriter = not mtType

        if not useSwiftWriter and FSwiftWriterAPIs.is_outgoing_message_supported(mtTypeString):
            if bypass_Swift_Solutions(fObject):
                return False
            useSwiftWriter = not FSwiftWriterAPIs.should_message_be_generated_by_adaptivdocs(mtTypeString)
        
    except ImportError as exception:

        if not str(exception) == 'No module named FSwiftWriterAPIs':

            raise SwiftWriterAPIException('Exception when deciding which Swift solution to use for message generation: {}. \n{}'.format(exception, traceback.format_exc()))

    except Exception as exception:
        
        raise SwiftWriterAPIException('Exception when deciding which Swift solution to use for message generation: {}. \n{}'.format(exception, traceback.format_exc()))
            
    return useSwiftWriter


def UseSwiftWriterForMT(fObject):
    useSwiftWriter = False

    try:
        import FSwiftWriterAPIs
        
        if is_unsupported_settlement(fObject):
            return False

        mtType = FSwiftWriterAPIs.get_swift_mt_type(fObject)
        mtTypeString = 'MT{}'.format(mtType)
        useSwiftWriter = not mtType or FSwiftWriterAPIs.is_outgoing_message_supported(mtTypeString)
        
    except ImportError as exception:

        if not str(exception) == 'No module named FSwiftWriterAPIs':

            raise SwiftWriterAPIException('Exception when deciding which Swift solution to use for MT calculation: {}. \n{}'.format(exception, traceback.format_exc()))

    except Exception as exception:

        raise SwiftWriterAPIException("Exception when deciding which Swift solution to use for MT calculation: {}. \n{}".format(exception, traceback.format_exc()))
            
    return useSwiftWriter

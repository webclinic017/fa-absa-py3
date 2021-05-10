"""--------------------------------------------------------------------------------------------------------------------------------------
MODULE
    TradeConfirmationGeneral

DESCRIPTION
    This module contains general functionality related to trade confirmations.

-----------------------------------------------------------------------------------------------------------------------------------------
HISTORY
=========================================================================================================================================
Date            Change no       Developer               Requester               Description
-----------------------------------------------------------------------------------------------------------------------------------------
2019-06-14      FAOPS-439       Cuen Edwards            Letitia Carboni         Initial Implementation.
                                Tawanda Mukhalela
2020-02-07      FAOPS-724       Cuen Edwards            Letitia Carboni         Addition of support for Collar product type.
2020-02-07      FAOPS-726       Cuen Edwards            Letitia Carboni         Addition of support for Geared Collar product type.
2020-02-14      FAOPS-732       Cuen Edwards            Letitia Carboni         Addition of support for EDD extension of Synthetic
                                                                                Forward product type.
2020-02-14      FAOPS-733       Cuen Edwards            Letitia Carboni         Addition of support for Forward Enhancer Plus product
                                                                                type.
2020-02-28      FAOPS-731       Cuen Edwards            Letitia Carboni         Addition of support for Synthetic Forward product type.
2020-02-28      FAOPS-734       Cuen Edwards            Letitia Carboni         Addition of support for Put Spread product type.
2020-02-28      FAOPS-736       Cuen Edwards            Letitia Carboni         Addition of support for Calendar Spread product type.
2020-02-28      FAOPS-738       Cuen Edwards            Letitia Carboni         Addition of support for Flat Forward product type.
2020-02-28      FAOPS-737       Cuen Edwards            Letitia Carboni         Addition of support for Geared Forward product type.
2020-02-28      FAOPS-735       Cuen Edwards            Letitia Carboni         Addition of support for EDD extension of Flat Forward
                                                                                product type.
2020-04-15      FAOPS-769       Cuen Edwards            Letitia Carboni         Addition of support for Limited Protection Forward
                                                                                product type.
2020-04-15      FAOPS-770       Cuen Edwards            Letitia Carboni         Addition of support for Forward Spread product type.
2020-04-15      FAOPS-771       Cuen Edwards            Letitia Carboni         Addition of support for Geared Forward Spreads product
                                                                                type.
2020-04-15      FAOPS-772       Cuen Edwards            Letitia Carboni         Addition of support for Call Spread product type.
2020-04-15      FAOPS-773       Cuen Edwards            Letitia Carboni         Addition of support for Forward product type.
2020-04-15      FAOPS-778       Cuen Edwards            Letitia Carboni         Addition of support for Knock out Forwards product type.
2020-04-15      FAOPS-779       Cuen Edwards            Letitia Carboni         Addition of support for Knock in Forwards product type.
-----------------------------------------------------------------------------------------------------------------------------------------
"""

import xml.etree.ElementTree as ElementTree

from FDocumentationCompression import ZlibToXml, HexToZlib

import DocumentGeneral
import FXOptionDocumentGeneral



SUPPORTED_PRODUCT_TYPES = [
    'Calendar Spread',
    'Call Spread',
    'Collar',
    'EDD extension of Flat Forward',
    'EDD extension of Synthetic Forward',
    'Flat Forward',
    'Forward',
    'Forward Enhancer Plus',
    'Forward Spread',
    'Geared Collar',
    'Geared Forward',
    'Geared Forward Spreads',
    'Knock in Forwards',
    'Knock out Forwards',
    'Limited Protection Forward',
    'Put Spread',
    'Synthetic Forward'
]

NON_PRODUCT_TYPES = [
    None,
    'Not Applicable'
]

PRODUCT_TYPES_WITH_RELATED_REFERENCES = [
    'EDD extension of Flat Forward',
    'EDD extension of Synthetic Forward'
]


def get_trade_confirmation_event_name():
    """
    Get the name of the event to associate with trade confirmations.
    """
    return 'Trade Confirmation'


def get_trade_confirmation_template_name():
    """
    Get the name of the template to associate with trade
    confirmations.
    """
    return 'ABSA_Trade_Confirmation'


def get_event_description(confirmation):
    """
    Get a description of the confirmation event type.
    """
    event_type = get_trade_type_description(confirmation) + ' Confirmation'
    if confirmation.Type() in ['Amendment', 'Cancellation']:
        event_type += ' ' + confirmation.Type()
    return event_type


def get_trade_type_description(confirmation):
    """
    Get a description of the confirmation trade type.
    """
    if confirmation.Type() == 'Cancellation':
        xml_string = get_last_released_xml(confirmation)
        element = ElementTree.fromstring(xml_string)
        return element.find('.//TRADE_CONFIRMATION/TRADE_TYPE').text
    else:
        trade = confirmation.Trade()
        if FXOptionDocumentGeneral.is_fx_option_structure_trade(trade):
            product_type = FXOptionDocumentGeneral.get_product_type(trade.Instrument())
            if product_type in NON_PRODUCT_TYPES:
                return 'FX Option'
            return product_type
        elif FXOptionDocumentGeneral.is_fx_option_standalone_trade(confirmation.Trade()):
            return 'FX Option'
        else:
            raise ValueError("Unsupported confirmation trade specified.")


def get_last_released_xml(confirmation):
    """
    Get the xml from the last post-released confirmation.

    This function should only be called when a confirmation has
    been released.
    """
    previous_confirmation = confirmation.ConfirmationReference()
    if previous_confirmation.IsPostRelease():
        operations_document = previous_confirmation.Documents()[0]
        return ZlibToXml(HexToZlib(operations_document.Data()))
    else:
        return get_last_released_xml(previous_confirmation)


def get_party_isda_agreement(party):
    """
    Get the ISDA agreement for a party.
    """
    for agreement in party.Agreements():
        if agreement.DocumentTypeChlItem() is None:
            continue
        if agreement.DocumentTypeChlItem().Name() == 'ISDA':
            return agreement
    return None


def get_first_bank_signatory():
    """
    Get the first bank signatory to use on confirmations.
    """
    return str(_get_trade_confirmation_parameter('BankSignatory1'))


def get_second_bank_signatory():
    """
    Get the second bank signatory to use on confirmations.
    """
    return str(_get_trade_confirmation_parameter('BankSignatory2'))


def _get_trade_confirmation_parameter(parameter_name):
    """
    Get a trade confirmation FParameter value.
    """
    return DocumentGeneral.get_fparameter('ABSATradeConfirmationParameters', parameter_name)

""" Compiled: 2020-09-18 10:38:54 """

#__src_file__ = "extensions/swift/etc/FConfirmationSwiftDefaultXML.py"
"""----------------------------------------------------------------------------
MODULE
    FConfirmationSwiftDefaultXML

DESCRIPTION
    This module is by default called from FConfirmationParametersTemplate.
    It is not recommended to make changes in the module.
----------------------------------------------------------------------------"""

import FSwiftMessageTypeCalculator as Calculator
from FConfirmationEnums import ConfirmationType

documentConfirmationSWIFT = '''\
<MESSAGE>
    <SWIFT>
        <acmTemplate function = 'GetSwiftTemplate' file = 'FConfirmationSwiftDefaultXML' />
    </SWIFT>
    <CONFIRMATION>
        <CONF_TEMPLATE_CHLNBR><acmCode method ='ConfTemplateChlItem.Name'/></CONF_TEMPLATE_CHLNBR>
        <SEQNBR Field="20 M"><acmCode method ='Oid' ignoreUpdate ='True'/></SEQNBR>
        <CONFIRMATION_SEQNBR><acmCode method ='ConfirmationReference.Name' ignoreUpdate ='True'/></CONFIRMATION_SEQNBR>
        <EVENT_CHLNBR><acmCode method ='EventChlItem.Name'/></EVENT_CHLNBR>
        <RESET_RESNBR><acmCode method ='Reset.Oid'/></RESET_RESNBR>
        <STATUS><acmCode method ='Status' ignoreUpdate ='True'/></STATUS>
        <TRANSPORT><acmCode method ='Transport'/></TRANSPORT>
        <TRDNBR><acmCode method ='Trade.Oid'/></TRDNBR>
        <CFWNBR><acmCode method ='CashFlow'/></CFWNBR>
    </CONFIRMATION>
</MESSAGE>
'''

swiftTemplate = '''
    <SWIFT>
        <acmTemplate function = 'GetBaseXMLTemplate' file = 'FSwiftXMLTemplates'/>
        <acmTemplate function = 'GetCommonBlock' file = 'FConfirmationSwiftDefaultXML' />
        <acmTemplate function = 'GetMTXXXBlock' file = 'FConfirmationSwiftDefaultXML' />
    </SWIFT>
'''

commonBlock_template = '''
    <SWIFT file = 'FSwiftMTConfirmation'>
        <acmInit function ='Init'/>
        <PARTY_A_OPTION Field="82A M"><acmCode function ='GetPartyAOption'/></PARTY_A_OPTION>
        <PARTY_A_ACCOUNT Field="82A M"><acmCode function ='GetPartyAAccount'/></PARTY_A_ACCOUNT>
        <PARTY_A_BIC Field="82A M"><acmCode function ='GetPartyABic'/></PARTY_A_BIC>
        <PARTY_A_NAME Field="82A M"><acmCode function ='GetPartyAName'/></PARTY_A_NAME>
        <PARTY_A_ADDRESS Field="82A M"><acmCode function ='GetPartyAAddress'/></PARTY_A_ADDRESS>
        <PARTY_B_OPTION Field="87A M"><acmCode function ='GetPartyBOption'/></PARTY_B_OPTION>
        <PARTY_B_ACCOUNT Field="87A M"><acmCode function ='GetPartyBAccount'/></PARTY_B_ACCOUNT>
        <PARTY_B_BIC Field="87A M"><acmCode function ='GetPartyBBic'/></PARTY_B_BIC>
        <PARTY_B_NAME Field="87A M"><acmCode function ='GetPartyBName'/></PARTY_B_NAME>
        <PARTY_B_ADDRESS Field="87A M"><acmCode function ='GetPartyBAddress'/></PARTY_B_ADDRESS>
        <RECEIVER_BIC Field="22C M"><acmCode function ='GetReceiverBic'/></RECEIVER_BIC>
        <SENDER_BIC Field="22C M"><acmCode function ='GetSenderBic'/></SENDER_BIC>
        <SEQREF Field="20 M"><acmCode function ='GetSeqRef'/></SEQREF>
        <NETWORK><acmCode function ='GetNetwork'/></NETWORK>
        <TRADE_DATE Field="30T M"><acmCode function ='GetTradeDate'/></TRADE_DATE>
        <TYPE_OF_OPERATION Field="22A M"><acmCode function ='GetTypeOfOperation' ignoreUpdate ='True'/></TYPE_OF_OPERATION>
    </SWIFT>
        '''

MT300_template = '''
    <SWIFT file = 'FSwiftMT300'>
        <acmInit function ='Init'/>
        <BLOCK_TRADE Field="17T O"><acmCode function = 'GetBlockTrade'/></BLOCK_TRADE>
        <BUY_AMOUNT Field="32B M"><acmCode function = 'GetBuyAmount'/></BUY_AMOUNT>
        <BUY_CURRENCY Field="32B M"><acmCode function ='GetBuyCurrency'/></BUY_CURRENCY>
        <BUY_DELIVERY_AGENT_OPTION Field="53A O"><acmCode function = 'GetBuyDeliveryAgentOption'/></BUY_DELIVERY_AGENT_OPTION>
        <BUY_DELIVERY_AGENT_ACCOUNT Field="53A O"><acmCode function = 'GetBuyDeliveryAgentAccount'/></BUY_DELIVERY_AGENT_ACCOUNT>
        <BUY_DELIVERY_AGENT_BIC Field="53A O"><acmCode function = 'GetBuyDeliveryAgentBic'/></BUY_DELIVERY_AGENT_BIC>
        <BUY_DELIVERY_AGENT_NAME Field="53A O"><acmCode function = 'GetBuyDeliveryAgentName'/></BUY_DELIVERY_AGENT_NAME>
        <BUY_DELIVERY_AGENT_ADDRESS Field="53A O"><acmCode function = 'GetBuyDeliveryAgentAddress'/></BUY_DELIVERY_AGENT_ADDRESS>
        <BUY_INTERMEDIARY_OPTION Field="56A O"><acmCode function = 'GetBuyIntermediaryOption'/></BUY_INTERMEDIARY_OPTION>
        <BUY_INTERMEDIARY_ACCOUNT Field="56A O"><acmCode function = 'GetBuyIntermediaryAccount'/></BUY_INTERMEDIARY_ACCOUNT>
        <BUY_INTERMEDIARY_BIC Field="56A O"><acmCode function = 'GetBuyIntermediaryBic'/></BUY_INTERMEDIARY_BIC>
        <BUY_INTERMEDIARY_NAME Field="56A O"><acmCode function = 'GetBuyIntermediaryName'/></BUY_INTERMEDIARY_NAME>
        <BUY_INTERMEDIARY_ADDRESS Field="56A O"><acmCode function = 'GetBuyIntermediaryAddress'/></BUY_INTERMEDIARY_ADDRESS>
        <BUY_RECEIVING_AGENT_OPTION Field="57A M"><acmCode function = 'GetBuyReceivingAgentOption'/></BUY_RECEIVING_AGENT_OPTION>
        <BUY_RECEIVING_AGENT_ACCOUNT Field="57A M"><acmCode function = 'GetBuyReceivingAgentAccount'/></BUY_RECEIVING_AGENT_ACCOUNT>
        <BUY_RECEIVING_AGENT_BIC Field="57A M"><acmCode function = 'GetBuyReceivingAgentBic'/></BUY_RECEIVING_AGENT_BIC>
        <BUY_RECEIVING_AGENT_NAME Field="57A M"><acmCode function = 'GetBuyReceivingAgentName'/></BUY_RECEIVING_AGENT_NAME>
        <BUY_RECEIVING_AGENT_ADDRESS Field="57A M"><acmCode function = 'GetBuyReceivingAgentAddress'/></BUY_RECEIVING_AGENT_ADDRESS>
        <SELL_AMOUNT Field="33B M"><acmCode function = 'GetSellAmount'/></SELL_AMOUNT>
        <SELL_CURRENCY Field="33B M"><acmCode function = 'GetSellCurrency'/></SELL_CURRENCY>
        <SELL_BENEFICIARY_INSTITUTION_OPTION Field="58A O"><acmCode function = 'GetSellBeneficiaryInstitutionOption'/></SELL_BENEFICIARY_INSTITUTION_OPTION>
        <SELL_BENEFICIARY_INSTITUTION_ACCOUNT Field="58A O"><acmCode function = 'GetSellBeneficiaryInstitutionAccount'/></SELL_BENEFICIARY_INSTITUTION_ACCOUNT>
        <SELL_BENEFICIARY_INSTITUTION_BIC Field="58A O"><acmCode function = 'GetSellBeneficiaryInstitutionBic'/></SELL_BENEFICIARY_INSTITUTION_BIC>
        <SELL_BENEFICIARY_INSTITUTION_NAME Field="58A O"><acmCode function = 'GetSellBeneficiaryInstitutionName'/></SELL_BENEFICIARY_INSTITUTION_NAME>
        <SELL_BENEFICIARY_INSTITUTION_ADDRESS Field="58A O"><acmCode function = 'GetSellBeneficiaryInstitutionAddress'/></SELL_BENEFICIARY_INSTITUTION_ADDRESS>
        <SELL_DELIVERY_AGENT_OPTION Field="53A O"><acmCode function = 'GetSellDeliveryAgentOption'/></SELL_DELIVERY_AGENT_OPTION>
        <SELL_DELIVERY_AGENT_ACCOUNT Field="53A O"><acmCode function = 'GetSellDeliveryAgentAccount'/></SELL_DELIVERY_AGENT_ACCOUNT>
        <SELL_DELIVERY_AGENT_BIC Field="53A O"><acmCode function = 'GetSellDeliveryAgentBic'/></SELL_DELIVERY_AGENT_BIC>
        <SELL_DELIVERY_AGENT_NAME Field="53A O"><acmCode function = 'GetSellDeliveryAgentName'/></SELL_DELIVERY_AGENT_NAME>
        <SELL_DELIVERY_AGENT_ADDRESS Field="53A O"><acmCode function ='GetSellDeliveryAgentAddress'/></SELL_DELIVERY_AGENT_ADDRESS>
        <SELL_INTERMEDIARY_OPTION Field="56A O"><acmCode function = 'GetSellIntermediaryOption'/></SELL_INTERMEDIARY_OPTION>
        <SELL_INTERMEDIARY_ACCOUNT Field="56A O"><acmCode function = 'GetSellIntermediaryAccount'/></SELL_INTERMEDIARY_ACCOUNT>
        <SELL_INTERMEDIARY_BIC Field="56A O"><acmCode function = 'GetSellIntermediaryBic'/></SELL_INTERMEDIARY_BIC>
        <SELL_INTERMEDIARY_NAME Field="56A O"><acmCode function = 'GetSellIntermediaryName'/></SELL_INTERMEDIARY_NAME>
        <SELL_INTERMEDIARY_ADDRESS Field="56A O"><acmCode function = 'GetSellIntermediaryAddress'/></SELL_INTERMEDIARY_ADDRESS>
        <SELL_RECEIVING_AGENT_OPTION Field="57A M"><acmCode function = 'GetSellReceivingAgentOption'/></SELL_RECEIVING_AGENT_OPTION>
        <SELL_RECEIVING_AGENT_ACCOUNT Field="57A M"><acmCode function = 'GetSellReceivingAgentAccount'/></SELL_RECEIVING_AGENT_ACCOUNT>
        <SELL_RECEIVING_AGENT_BIC Field="57A M"><acmCode function = 'GetSellReceivingAgentBic'/></SELL_RECEIVING_AGENT_BIC>
        <SELL_RECEIVING_AGENT_NAME Field="57A M"><acmCode function = 'GetSellReceivingAgentName'/></SELL_RECEIVING_AGENT_NAME>
        <SELL_RECEIVING_AGENT_ADDRESS Field="57A M"><acmCode function = 'GetSellReceivingAgentAddress'/></SELL_RECEIVING_AGENT_ADDRESS>
        <VALUE_DATE Field="30V M"><acmCode function = 'GetValueDate'/></VALUE_DATE>
        <EXCHANGE_RATE Field="22C M and 36 M"><acmCode function = 'GetExchangeRate'/></EXCHANGE_RATE>
        <COUNTERPARTYS_REFERENCE Field="26H O"><acmCode function = 'GetCounterpartysReference'/></COUNTERPARTYS_REFERENCE>
        <SPLIT_SETTLEMENT_INDICATOR Field="17U O"><acmCode function = 'GetSplitSettlementIndicator'/></SPLIT_SETTLEMENT_INDICATOR>
        <SCOPE_OF_OPERATION Field="94A O"><acmCode function = 'GetScopeOfOperation'/></SCOPE_OF_OPERATION>
        <TERMS_CONDITIONS Field="77D O"><acmCode function = 'GetTermsConditions'/></TERMS_CONDITIONS>
        <YOUR_REFERENCE Field="21 O"><acmCode function = 'GetYourReference' ignoreUpdate ='True'/></YOUR_REFERENCE>
        <REPORTING_JURISDICTION Field="22L M"><acmCode function = 'GetReportingJurisdiction' /></REPORTING_JURISDICTION>
        <REPORTING_PARTY_ADDRESS Field="91A O"><acmCode function = 'GetReportingPartyAddress' /></REPORTING_PARTY_ADDRESS>
        <REPORTING_PARTY_BIC Field="91A O"><acmCode function = 'GetReportingPartyBic' /></REPORTING_PARTY_BIC>
        <REPORTING_PARTY_ACCOUNT Field="91A O"><acmCode function = 'GetReportingPartyAccount' /></REPORTING_PARTY_ACCOUNT>
        <REPORTING_PARTY_OPTION Field="91A O"><acmCode function = 'GetReportingPartyOption' /></REPORTING_PARTY_OPTION>
        <REPORTING_PARTY_NAME Field="91A O"><acmCode function = 'GetReportingPartyName' /></REPORTING_PARTY_NAME>
        <UTI_NAMESPACE Field="22M M"><acmCode function = 'GetUTINamespace' /></UTI_NAMESPACE>
        <TRANSACTION_IDENTIFIER Field="22N M"><acmCode function = 'GetTransactionIdentifier' /></TRANSACTION_IDENTIFIER>
        <PRIOR_UTI_NAMESPACE Field="22P O"><acmCode function = 'GetPriorUTINamespace' /></PRIOR_UTI_NAMESPACE>
        <PRIOR_TRANSACTION_IDENTIFIER Field="22R O"><acmCode function = 'GetPriorTransactionIdentifier' /></PRIOR_TRANSACTION_IDENTIFIER>
        <ADDITIONAL_REPORTING_INFORMATION Field="77A O"><acmCode function = 'GetAdditionalReportingInformation' /></ADDITIONAL_REPORTING_INFORMATION>
    </SWIFT>
        '''
MT305_template = '''
    <SWIFT file = 'FSwiftMT305'>
        <acmInit function ='Init'/>
        <CODE Field="22 M"><acmCode function = 'GetCode' ignoreUpdate ='True'/></CODE>
        <STRIKE_PRICE Field="22C M and 36 M"><acmCode function = 'GetStrikePrice' /></STRIKE_PRICE>
        <CODE1 Field="23 O"><acmCode function = 'GetCode1' /></CODE1>
        <CODE2 Field="23 O"><acmCode function = 'GetCode2' /></CODE2>
        <CODE3 Field="23 O"><acmCode function = 'GetCode3' /></CODE3>
        <YOUR_REFERENCE Field="21 M"><acmCode function = 'GetYourReference' ignoreUpdate ='True'/></YOUR_REFERENCE>
        <UNDERLYING_CURRENCY Field="23 O and 32B M"><acmCode function = 'GetUnderlyingCurrency' /></UNDERLYING_CURRENCY>
        <EXERCISE_DATE Field="31C O"><acmCode function = 'GetExerciseDate' /></EXERCISE_DATE>
        <EXPIRY_DETAILS_DATE Field="31G M"><acmCode function = 'GetExpiryDetailsDate' /></EXPIRY_DETAILS_DATE>
        <EXPIRY_DETAILS_TIME Field="31G M"><acmCode function = 'GetExpiryDetailsTime' /></EXPIRY_DETAILS_TIME>
        <EXPIRY_DETAILS_LOCATION Field="31G M"><acmCode function = 'GetExpiryDetailsLocation' /></EXPIRY_DETAILS_LOCATION>
        <SETTLEMENT_DATE Field="31E O"><acmCode function = 'GetSettlementDate' /></SETTLEMENT_DATE>
        <SETTLEMENT_TYPE Field="26F M"><acmCode function = 'GetSettlementType' /></SETTLEMENT_TYPE>
        <UNDERLYING_AMOUNT Field="32B M"><acmCode function = 'GetUnderlyingAmount'/></UNDERLYING_AMOUNT>
        <COUNTER_CURRENCY Field="33B M"><acmCode function = 'GetCounterCurrency' /></COUNTER_CURRENCY>
        <COUNTER_AMOUNT Field="33B M"><acmCode function = 'GetCounterAmount' /></COUNTER_AMOUNT>
        <PREMIUM_PRICE Field="37K M"><acmCode function = 'GetPremiumPrice'/></PREMIUM_PRICE>
        <PREMIUM_PAYMENT_OPTION Field="34A M"><acmCode function = 'GetPremiumPaymentOption'/></PREMIUM_PAYMENT_OPTION>
        <PREMIUM_PAYMENT_DATE Field="34A M"><acmCode function = 'GetPremiumPaymentDate'/></PREMIUM_PAYMENT_DATE>
        <PREMIUM_PAYMENT_CURRENCY Field="34A M"><acmCode function = 'GetPremiumPaymentCurrency'/></PREMIUM_PAYMENT_CURRENCY>
        <PREMIUM_PAYMENT_AMOUNT Field="34A M"><acmCode function = 'GetPremiumPaymentAmount'/></PREMIUM_PAYMENT_AMOUNT>
        <SENDER_CORRESPONDENT_OPTION Field="53A O"><acmCode function = 'GetSenderCorrespondentOption'/></SENDER_CORRESPONDENT_OPTION>
        <SENDER_CORRESPONDENT_ACCOUNT Field="53A O"><acmCode function = 'GetSenderCorrespondentAccount'/></SENDER_CORRESPONDENT_ACCOUNT>
        <SENDER_CORRESPONDENT_NAME Field="53A O"><acmCode function = 'GetSenderCorrespondentName'/></SENDER_CORRESPONDENT_NAME>
        <SENDER_CORRESPONDENT_ADDRESS Field="53A O"><acmCode function = 'GetSenderCorrespondentAddress'/></SENDER_CORRESPONDENT_ADDRESS>
        <SENDER_CORRESPONDENT_BIC Field="53A O"><acmCode function = 'GetSenderCorrespondentBic'/></SENDER_CORRESPONDENT_BIC>
        <INTERMEDIARY_OPTION Field="56A O"><acmCode function = 'GetIntermediaryOption'/></INTERMEDIARY_OPTION>
        <INTERMEDIARY_ACCOUNT Field="56A O"><acmCode function = 'GetIntermediaryAccount'/></INTERMEDIARY_ACCOUNT>
        <INTERMEDIARY_NAME Field="56A O"><acmCode function = 'GetIntermediaryName'/></INTERMEDIARY_NAME>
        <INTERMEDIARY_ADDRESS Field="56A O"><acmCode function = 'GetIntermediaryAddress'/></INTERMEDIARY_ADDRESS>
        <INTERMEDIARY_BIC Field="56A O"><acmCode function = 'GetIntermediaryBic'/></INTERMEDIARY_BIC>
        <ACCOUNT_WITH_INSTITUTION_OPTION Field="57A M"><acmCode function = 'GetAccountWithInstitutionOption'/></ACCOUNT_WITH_INSTITUTION_OPTION>
        <ACCOUNT_WITH_INSTITUTION_ACCOUNT Field="57A M"><acmCode function = 'GetAccountWithInstitutionAccount'/></ACCOUNT_WITH_INSTITUTION_ACCOUNT>
        <ACCOUNT_WITH_INSTITUTION_NAME Field="57A M"><acmCode function = 'GetAccountWithInstitutionName'/></ACCOUNT_WITH_INSTITUTION_NAME>
        <ACCOUNT_WITH_INSTITUTION_ADDRESS Field="57A M"><acmCode function = 'GetAccountWithInstitutionAddress'/></ACCOUNT_WITH_INSTITUTION_ADDRESS>
        <ACCOUNT_WITH_INSTITUTION_BIC Field="57A M"><acmCode function = 'GetAccountWithInstitutionBic'/></ACCOUNT_WITH_INSTITUTION_BIC>
        <SENDER_TO_RECEIVER_INFO Field="72 O"><acmCode function = 'GetSenderToRecieverInfo'/></SENDER_TO_RECEIVER_INFO>
        <REPORTING_JURISDICTION Field="22L M"><acmCode function = 'GetReportingJurisdiction' /></REPORTING_JURISDICTION>
        <REPORTING_PARTY_ADDRESS Field="91A O"><acmCode function = 'GetReportingPartyAddress' /></REPORTING_PARTY_ADDRESS>
        <REPORTING_PARTY_BIC Field="91A O"><acmCode function = 'GetReportingPartyBic' /></REPORTING_PARTY_BIC>
        <REPORTING_PARTY_ACCOUNT Field="91A O"><acmCode function = 'GetReportingPartyAccount' /></REPORTING_PARTY_ACCOUNT>
        <REPORTING_PARTY_OPTION Field="91A O"><acmCode function = 'GetReportingPartyOption' /></REPORTING_PARTY_OPTION>
        <REPORTING_PARTY_NAME Field="91A O"><acmCode function = 'GetReportingPartyName' /></REPORTING_PARTY_NAME>
        <UTI_NAMESPACE Field="22M M"><acmCode function = 'GetUTINamespace' /></UTI_NAMESPACE>
        <TRANSACTION_IDENTIFIER Field="22N M"><acmCode function = 'GetTransactionIdentifier' /></TRANSACTION_IDENTIFIER>
        <PRIOR_UTI_NAMESPACE Field="22P O"><acmCode function = 'GetPriorUTINamespace' /></PRIOR_UTI_NAMESPACE>
        <PRIOR_TRANSACTION_IDENTIFIER Field="22R O"><acmCode function = 'GetPriorTransactionIdentifier' /></PRIOR_TRANSACTION_IDENTIFIER>
        <ADDITIONAL_REPORTING_INFORMATION Field="77A O"><acmCode function = 'GetAdditionalReportingInformation' /></ADDITIONAL_REPORTING_INFORMATION>
    </SWIFT>
    '''

MT306_template = '''
    <SWIFT file = 'FSwiftMT306'>
        <acmInit function ='Init'/>
        <ADDITIONAL_INFO_AGREEMENT><acmCode function ='GetAdditionalInfoAgreement'/></ADDITIONAL_INFO_AGREEMENT>
        <BARRIER_INDICATOR Field="17A M"><acmCode function ='GetBarrierIndicator'/></BARRIER_INDICATOR>
        <BARRIER_LEVEL Field="37J M"><acmCode function ='GetBarrierLevel'/></BARRIER_LEVEL>
        <BUY_SELL_INDICATOR Field="17V M"><acmCode function ='GetBuySellIndicator'/></BUY_SELL_INDICATOR>
        <CALCULATION_AGENT_OPTION Field="84A M"><acmCode function ='GetCalculationAgentOption'/></CALCULATION_AGENT_OPTION>
        <CALCULATION_AGENT_BIC Field="84A M"><acmCode function ='GetCalculationAgentBic'/></CALCULATION_AGENT_BIC>
        <CALCULATION_AGENT_ACCOUNT Field="84A M"><acmCode function ='GetCalculationAgentAccount'/></CALCULATION_AGENT_ACCOUNT>
        <CALCULATION_AGENT_NAME Field="84A M"><acmCode function ='GetCalculationAgentName'/></CALCULATION_AGENT_NAME>
        <CALCULATION_AGENT_ADDRESS Field="84A M"><acmCode function ='GetCalculationAgentAddress'/></CALCULATION_AGENT_ADDRESS>
        <CALL_AMOUNT Field="33B M"><acmCode function ='GetCallAmount'/></CALL_AMOUNT>
        <CALL_CURRENCY Field="33B M"><acmCode function ='GetCallCurrency'/></CALL_CURRENCY>
        <CONTRACT_NO_PARTY_A Field="21N M"><acmCode function ='GetContractNoOfPartyA' ignoreUpdate ='True'/></CONTRACT_NO_PARTY_A>
        <CURRENCY_PAIR Field="32Q M"><acmCode function ='GetCurrencyPair'/></CURRENCY_PAIR>
        <DATE_OF_AGREEMENT Field="77H M"><acmCode function ='GetDateOfAgreement'/></DATE_OF_AGREEMENT>
        <EARLIEST_EXERCISE_DATE Field="30P O"><acmCode function ='GetEarliestExerciseDate'/></EARLIEST_EXERCISE_DATE>
        <EXPIRATION_DATE Field="30X M"><acmCode function ='GetExpirationDate'/></EXPIRATION_DATE>
        <EXPIRATION_LOCATION Field="29E M"><acmCode function ='GetExpirationLocation'/></EXPIRATION_LOCATION>
        <EXPIRATION_STYLE Field="12E M"><acmCode function ='GetExpirationStyle'/></EXPIRATION_STYLE>
        <EXPIRATION_TIME Field="29E M"><acmCode function ='GetExpirationTime'/></EXPIRATION_TIME>
        <FINAL_SETTLEMENT_DATE Field="30F M"><acmCode function ='GetFinalSettlementDate'/></FINAL_SETTLEMENT_DATE>
        <LOWER_BARRIER_LEVEL Field="37L O"><acmCode function ='GetLowerBarrierLevel'/></LOWER_BARRIER_LEVEL>
        <LOWER_TRIGGER_LEVEL Field="37P O"><acmCode function ='GetLowerTriggerLevel'/></LOWER_TRIGGER_LEVEL>
        <NON_DELIVERABLE_INDICATOR Field="17F M"><acmCode function ='GetNonDeliverableIndicator'/></NON_DELIVERABLE_INDICATOR>
        <OPTION_STYLE Field="12F M"><acmCode function ='GetOptionStyle'/></OPTION_STYLE>
        <PAYOUT_AMOUNT Field="33E M"><acmCode function ='GetPayoutAmount'/></PAYOUT_AMOUNT>
        <PAYOUT_CURRENCY Field="33E M"><acmCode function ='GetPayoutCurrency'/></PAYOUT_CURRENCY>
        <PAYOUT_RECEIVING_AGENT_OPTION Field="57A M"><acmCode function ='GetPayoutReceivingAgentOption'/></PAYOUT_RECEIVING_AGENT_OPTION>
        <PAYOUT_RECEIVING_AGENT_BIC Field="57A M"><acmCode function ='GetPayoutReceivingAgentBic'/></PAYOUT_RECEIVING_AGENT_BIC>
        <PREMIUM_AMOUNT Field="34B M"><acmCode function ='GetPremiumAmount'/></PREMIUM_AMOUNT>
        <PREMIUM_CURRENCY Field="34B M"><acmCode function ='GetPremiumCurrency'/></PREMIUM_CURRENCY>
        <PREMIUM_PAYMENT_DATE Field="30V M"><acmCode function ='GetPremiumPaymentDate'/></PREMIUM_PAYMENT_DATE>
        <PUT_AMOUNT Field="32B M"><acmCode function ='GetPutAmount'/></PUT_AMOUNT>
        <PUT_CURRENCY Field="32B M"><acmCode function ='GetPutCurrency'/></PUT_CURRENCY>
        <SETTLEMENT_CURRENCY Field="32E M"><acmCode function ='GetSettlementCurrency'/></SETTLEMENT_CURRENCY>
        <SETTLEMENT_RATE_SOURCE Field="14S M"><acmCode function ='GetSettlementRateSource'/></SETTLEMENT_RATE_SOURCE>
        <SETTLEMENT_TYPE Field="26F M"><acmCode function ='GetSettlementType'/></SETTLEMENT_TYPE>
        <SIP_PARTY_RECEIVING_AGENT_OPTION Field="57A M"><acmCode function ='GetSIPPartyReceivingAgentOption'/></SIP_PARTY_RECEIVING_AGENT_OPTION>
        <SIP_PARTY_RECEIVING_AGENT_ACCOUNT Field="57A M"><acmCode function ='GetSIPPartyReceivingAgentAccount'/></SIP_PARTY_RECEIVING_AGENT_ACCOUNT>
        <SIP_PARTY_RECEIVING_AGENT_BIC Field="57A M"><acmCode function ='GetSIPPartyReceivingAgentBic'/></SIP_PARTY_RECEIVING_AGENT_BIC>
        <SIP_PARTY_RECEIVING_AGENT_NAME Field="57A M"><acmCode function ='GetSIPPartyReceivingAgentName'/></SIP_PARTY_RECEIVING_AGENT_NAME>
        <SIP_PARTY_RECEIVING_AGENT_ADDRESS Field="57A M"><acmCode function ='GetSIPPartyReceivingAgentAddress'/></SIP_PARTY_RECEIVING_AGENT_ADDRESS>
        <STRIKE_PRICE Field="22C M and 36 M"><acmCode function ='GetStrikePrice'/></STRIKE_PRICE>
        <TRIGGER_LEVEL Field="22C M and 37U M"><acmCode function ='GetTriggerLevel'/></TRIGGER_LEVEL>
        <TYPE_EVENT Field="22K M"><acmCode function ='GetEventType' ignoreUpdate ='True'/></TYPE_EVENT>
        <TYPE_EVENT_NARRATIVE><acmCode function ='GetEventTypeNarrative' ignoreUpdate ='True'/></TYPE_EVENT_NARRATIVE>
        <TYPE_OF_AGREEMENT Field="77H M"><acmCode function ='GetTypeOfAgreement'/></TYPE_OF_AGREEMENT>
        <TYPE_OF_BARRIER Field="22G M"><acmCode function ='GetTypeOfBarrier'/></TYPE_OF_BARRIER>
        <TYPE_OF_TRIGGER Field="22J M"><acmCode function ='GetTypeOfTrigger'/></TYPE_OF_TRIGGER>
        <VERSION_OF_AGREEMENT Field="77H M"><acmCode function ='GetVersionOfAgreement'/></VERSION_OF_AGREEMENT>
        <YOUR_REFERENCE Field="21 O"><acmCode function = 'GetYourReference' ignoreUpdate ='True'/></YOUR_REFERENCE>
        <SCOPE_OF_OPERATION Field="94A O"><acmCode function = 'GetScopeOfOperation'/></SCOPE_OF_OPERATION>
        <BARRIER acmLoop='GetBarriers'>
            <BARRIER_WIN_START_DATE Field="30G M"><acmCode function ='GetBarrierWindowStartDate'/></BARRIER_WIN_START_DATE>
            <BARRIER_WIN_END_DATE Field="30G M"><acmCode function ='GetBarrierWindowEndDate'/></BARRIER_WIN_END_DATE>
            <START_DATE_LOCATION Field="29J M"><acmCode function ='GetStartDateLocation'/></START_DATE_LOCATION>
            <START_DATE_TIME Field="29J M"><acmCode function ='GetStartDateTime'/></START_DATE_TIME>
            <END_DATE_LOCATION Field="29K M"><acmCode function ='GetEndDateLocation'/></END_DATE_LOCATION>
            <END_DATE_TIME Field="29K M"><acmCode function ='GetEndDateTime'/></END_DATE_TIME>
        </BARRIER>
    </SWIFT>
    '''

MTLoanDeposit_template = '''
    <SWIFT file = 'FSwiftMTLoanDeposit'>
        <acmInit function ='Init'/>
        <DAY_COUNT_FRACTION Field="14D M"><acmCode function ='GetDayCountFraction'/></DAY_COUNT_FRACTION>
        <INTEREST_CURRENCY Field="34E M"><acmCode function ='GetInterestCurrency'/></INTEREST_CURRENCY>
        <PRINCIPAL_AMOUNT Field="32B M"><acmCode function ='GetPrincipalAmount'/></PRINCIPAL_AMOUNT>
        <PRINCIPAL_CURRENCY Field="32B M"><acmCode function ='GetPrincipalCurrency'/></PRINCIPAL_CURRENCY>
        <SIA_PARTY_A_RECEIVING_AGENT_OPTION Field="57A M"><acmCode function ='GetSIAPartyAReceivingAgentOption'/></SIA_PARTY_A_RECEIVING_AGENT_OPTION>
        <SIA_PARTY_A_RECEIVING_AGENT_ACCOUNT Field="57A M"><acmCode function ='GetSIAPartyAReceivingAgentAccount'/></SIA_PARTY_A_RECEIVING_AGENT_ACCOUNT>
        <SIA_PARTY_A_RECEIVING_AGENT_BIC Field="57A M"><acmCode function ='GetSIAPartyAReceivingAgentBic'/></SIA_PARTY_A_RECEIVING_AGENT_BIC>
        <SIA_PARTY_A_RECEIVING_AGENT_NAME Field="57A M"><acmCode function ='GetSIAPartyAReceivingAgentName'/></SIA_PARTY_A_RECEIVING_AGENT_NAME>
        <SIA_PARTY_A_RECEIVING_AGENT_ADDRESS Field="57A M"><acmCode function ='GetSIAPartyAReceivingAgentAddress'/></SIA_PARTY_A_RECEIVING_AGENT_ADDRESS>
        <SIA_PARTY_B_RECEIVING_AGENT_OPTION Field="57A M"><acmCode function ='GetSIAPartyBReceivingAgentOption'/></SIA_PARTY_B_RECEIVING_AGENT_OPTION>
        <SIA_PARTY_B_RECEIVING_AGENT_ACCOUNT Field="57A M"><acmCode function ='GetSIAPartyBReceivingAgentAccount'/></SIA_PARTY_B_RECEIVING_AGENT_ACCOUNT>
        <SIA_PARTY_B_RECEIVING_AGENT_BIC Field="57A M"><acmCode function ='GetSIAPartyBReceivingAgentBic'/></SIA_PARTY_B_RECEIVING_AGENT_BIC>
        <SIA_PARTY_B_RECEIVING_AGENT_NAME Field="57A M"><acmCode function ='GetSIAPartyBReceivingAgentName'/></SIA_PARTY_B_RECEIVING_AGENT_NAME>
        <SIA_PARTY_B_RECEIVING_AGENT_ADDRESS Field="57A M"><acmCode function ='GetSIAPartyBReceivingAgentAddress'/></SIA_PARTY_B_RECEIVING_AGENT_ADDRESS>
        <VALUE_DATE Field="30V M"><acmCode function ='GetValueDate'/></VALUE_DATE>
    </SWIFT>
    '''

MT320_template = '''
    <SWIFT file = 'FSwiftMT320'>
        <acmInit function ='Init'/>
        <acmTemplate function = 'GetLoanDepositBlock' file = 'FConfirmationSwiftDefaultXML' />
        <PARTY_A_ROLE Field="17R M"><acmCode function ='GetPartyARole'/></PARTY_A_ROLE>
        <INTEREST_AMOUNT Field="34E M"><acmCode function ='GetInterestAmount'/></INTEREST_AMOUNT>
        <INTEREST_RATE Field="22C M and 37G M"><acmCode function ='GetInterestRate'/></INTEREST_RATE>
        <MATURITY_DATE Field="30P M"><acmCode function ='GetMaturityDate'/></MATURITY_DATE>
        <NEXT_INTEREST_DUE_DATE Field="30X O"><acmCode function ='GetNextInterestDueDate'/></NEXT_INTEREST_DUE_DATE>
        <SIA_PARTY_A_INTERMEDIARY_OPTION Field="56A O"><acmCode function ='GetSIAPartyAIntermediaryOption'/></SIA_PARTY_A_INTERMEDIARY_OPTION>
        <SIA_PARTY_A_INTERMEDIARY_ACCOUNT Field="56A O"><acmCode function ='GetSIAPartyAIntermediaryAccount'/></SIA_PARTY_A_INTERMEDIARY_ACCOUNT>
        <SIA_PARTY_A_INTERMEDIARY_BIC Field="56A O"><acmCode function ='GetSIAPartyAIntermediaryBic'/></SIA_PARTY_A_INTERMEDIARY_BIC>
        <SIA_PARTY_A_INTERMEDIARY_NAME Field="56A O"><acmCode function ='GetSIAPartyAIntermediaryName'/></SIA_PARTY_A_INTERMEDIARY_NAME>
        <SIA_PARTY_A_INTERMEDIARY_ADDRESS Field="56A O"><acmCode function ='GetSIAPartyAIntermediaryAddress'/></SIA_PARTY_A_INTERMEDIARY_ADDRESS>
        <SIA_PARTY_B_INTERMEDIARY_OPTION Field="56A O"><acmCode function ='GetSIAPartyBIntermediaryOption'/></SIA_PARTY_B_INTERMEDIARY_OPTION>
        <SIA_PARTY_B_INTERMEDIARY_ACCOUNT Field="56A O"><acmCode function ='GetSIAPartyBIntermediaryAccount'/></SIA_PARTY_B_INTERMEDIARY_ACCOUNT>
        <SIA_PARTY_B_INTERMEDIARY_BIC Field="56A O"><acmCode function ='GetSIAPartyBIntermediaryBic'/></SIA_PARTY_B_INTERMEDIARY_BIC>
        <SIA_PARTY_B_INTERMEDIARY_NAME Field="56A O"><acmCode function ='GetSIAPartyBIntermediaryName'/></SIA_PARTY_B_INTERMEDIARY_NAME>
        <SIA_PARTY_B_INTERMEDIARY_ADDRESS Field="56A O"><acmCode function ='GetSIAPartyBIntermediaryAddress'/></SIA_PARTY_B_INTERMEDIARY_ADDRESS>
        <TERMS_CONDITIONS Field="77D O"><acmCode function ='GetTermsAndConditions'/></TERMS_CONDITIONS>
        <TYPE_EVENT Field="22B M"><acmCode function ='GetEventType' ignoreUpdate ='True'/></TYPE_EVENT>
        <SETTLE_AMT Field="32H O"><acmCode function ='GetSettleAmount'/></SETTLE_AMT>
        <SETTLE_CURR Field="32H O"><acmCode function ='GetSettleCurrency'/></SETTLE_CURR>
        <YOUR_REFERENCE Field="21 O"><acmCode function ='GetYourReference' ignoreUpdate ='True'/></YOUR_REFERENCE>
    </SWIFT>
    '''

MT330_template = '''
    <SWIFT file = 'FSwiftMT330'>
        <acmTemplate function = 'GetLoanDepositBlock' file = 'FConfirmationSwiftDefaultXML' />
        <PARTY_A_ROLE Field="17R M"><acmCode function ='GetPartyARole'/></PARTY_A_ROLE>
        <INTEREST_AMOUNT Field="34E O"><acmCode function ='GetInterestAmount'/></INTEREST_AMOUNT>
        <INTEREST_RATE Field="34E O"><acmCode function ='GetInterestRate'/></INTEREST_RATE>
        <PERIOD_NOTICE Field="38A M"><acmCode function ='GetPeriodNotice'/></PERIOD_NOTICE>
        <TYPE_EVENT Field="22B M"><acmCode function ='GetEventType'/></TYPE_EVENT>
        <BALANCE_AMOUNT Field="32B M"><acmCode function ='GetBalanceAmount'/></BALANCE_AMOUNT>
        <BALANCE_CURRENCY Field="32B M"><acmCode function ='GetBalanceCurrency'/></BALANCE_CURRENCY>
        <TERMS_CONDITIONS Field="77D O"><acmCode function ='GetTermsAndConditions'/></TERMS_CONDITIONS>
    </SWIFT>
    '''

MT395_template = '''
    <SWIFT file = 'FSwiftMT395'>
        <QUERIES Field="75 M"><acmCode function ='GetQueries'/></QUERIES>
        <NARRATIVE Field="77A O"><acmCode function ='GetNarrative'/></NARRATIVE>
        <RELATED_REF Field="21 M"><acmCode function ='GetRelatedRef'/></RELATED_REF>
        <ORIGINAL_MESSAGE_MT Field="11A O"><acmCode function ='GetOriginalMessageType'/></ORIGINAL_MESSAGE_MT>
        <NARRATIVE_DESCRIPTION Field="79 O"><acmCode function ='GetNarrativeDescription'/></NARRATIVE_DESCRIPTION>
    </SWIFT>
    '''

MT362_template = '''
    <SWIFT file = 'FSwiftMT362'>
        <acmInit function ='Init'/>
        <CONTRACT_NO_PARTY_A Field="21N M"><acmCode function ='GetContractNumPartyA'/></CONTRACT_NO_PARTY_A>
        <EFFECTIVE_DATE Field="30V M"><acmCode function ='GetEffectiveDate'/></EFFECTIVE_DATE>
        <IRP_PARTY_A_CAP_RATE Field="37V O"><acmCode function ='GetIRPCapRate'/></IRP_PARTY_A_CAP_RATE>
        <IRP_PARTY_A_CURR Field="33F M"><acmCode function ='GetIRPPartyACurr'/></IRP_PARTY_A_CURR>
        <IRP_PARTY_A_FLOOR_RATE Field="37G O"><acmCode function ='GetIRPFloorRate'/></IRP_PARTY_A_FLOOR_RATE>
        <IRP_PARTY_A_NOT_AMT Field="33F M"><acmCode function ='GetIRPPartyANotAmount'/></IRP_PARTY_A_NOT_AMT>
        <IRP_PARTY_A_PAYMENT_DATE Field="30F M"><acmCode function ='GetIRPPartyAPaymentDate'/></IRP_PARTY_A_PAYMENT_DATE>
        <IRP_PARTY_A_PERIOD_END_DATE Field="30Q O"><acmCode function ='GetIRPPartyAPeriodEndDate'/></IRP_PARTY_A_PERIOD_END_DATE>
        <IRP_PARTY_A_PERIOD_START_DATE Field="30X M"><acmCode function ='GetIRPPartyAPeriodStartDate'/></IRP_PARTY_A_PERIOD_START_DATE>
        <IRP_PARTY_A_RESET_RATE Field="37G M"><acmCode function ='GetIRPPartyAResetRateFormatted'/></IRP_PARTY_A_RESET_RATE>
        <IRP_PARTY_A_SPREAD Field="37R M"><acmCode function ='GetIRPPartyASpread'/></IRP_PARTY_A_SPREAD>
        <IRP_PARTY_A_TOTAL_RATE Field="37M M"><acmCode function ='GetIRPPartyATotalRate'/></IRP_PARTY_A_TOTAL_RATE>
        <NAP_PARTY_A_CURRENCY Field="32M M"><acmCode function ='GetNapCurrency'/></NAP_PARTY_A_CURRENCY>
        <NAP_PARTY_A_PAY_AMOUNT Field="32M M"><acmCode function ='GetNapPartyAPayAmount'/></NAP_PARTY_A_PAY_AMOUNT>
        <NAP_PARTY_A_PAY_DATE Field="30F M"><acmCode function ='GetNapPayDate'/></NAP_PARTY_A_PAY_DATE>
        <NAP_PARTY_A_RECEIVING_AGENT_OPTION Field="57A M"><acmCode function ='GetNapPartyAReceivingAgentOption'/></NAP_PARTY_A_RECEIVING_AGENT_OPTION>
        <NAP_PARTY_A_RECEIVING_AGENT_ACCOUNT Field="57A M"><acmCode function ='GetNapPartyAReceivingAgentAccount'/></NAP_PARTY_A_RECEIVING_AGENT_ACCOUNT>
        <NAP_PARTY_A_RECEIVING_AGENT_BIC Field="57A M"><acmCode function ='GetNapPartyAReceivingAgentAccountBic'/></NAP_PARTY_A_RECEIVING_AGENT_BIC>
        <NAP_PARTY_A_RECEIVING_AGENT_NAME Field="57A M"><acmCode function ='GetNapPartyAReceivingAgentName'/></NAP_PARTY_A_RECEIVING_AGENT_NAME>
        <NAP_PARTY_A_RECEIVING_AGENT_ADDRESS Field="57A M"><acmCode function ='GetNapPartyAReceivingAgentAddress'/></NAP_PARTY_A_RECEIVING_AGENT_ADDRESS>
        <IRP_PARTY_B_CAP_RATE Field="37V O"><acmCode function ='GetIRPCapRate'/></IRP_PARTY_B_CAP_RATE>
        <IRP_PARTY_B_CURR Field="33F M"><acmCode function ='GetIRPPartyBCurr'/></IRP_PARTY_B_CURR>
        <IRP_PARTY_B_FLOOR_RATE Field="37G O"><acmCode function ='GetIRPFloorRate'/></IRP_PARTY_B_FLOOR_RATE>
        <IRP_PARTY_B_NOT_AMT Field="33F M"><acmCode function ='GetIRPPartyBNotAmount'/></IRP_PARTY_B_NOT_AMT>
        <IRP_PARTY_B_PAYMENT_DATE Field="30F M"><acmCode function ='GetIRPPartyBPaymentDate'/></IRP_PARTY_B_PAYMENT_DATE>
        <IRP_PARTY_B_PERIOD_END_DATE Field="30Q O"><acmCode function ='GetIRPPartyBPeriodEndDate'/></IRP_PARTY_B_PERIOD_END_DATE>
        <IRP_PARTY_B_PERIOD_START_DATE Field="30X M"><acmCode function ='GetIRPPartyBPeriodStartDate'/></IRP_PARTY_B_PERIOD_START_DATE>
        <IRP_PARTY_B_RESET_RATE Field="37G M"><acmCode function ='GetIRPPartyBResetRateFormatted'/></IRP_PARTY_B_RESET_RATE>
        <IRP_PARTY_B_SPREAD Field="37R M"><acmCode function ='GetIRPPartyBSpread'/></IRP_PARTY_B_SPREAD>
        <IRP_PARTY_B_TOTAL_RATE Field="37M M"><acmCode function ='GetIRPPartyBTotalRate'/></IRP_PARTY_B_TOTAL_RATE>
        <NAP_PARTY_B_CURRENCY Field="32M M"><acmCode function ='GetNapCurrency'/></NAP_PARTY_B_CURRENCY>
        <NAP_PARTY_B_PAY_AMOUNT Field="32M M"><acmCode function ='GetNapPartyBPayAmount'/></NAP_PARTY_B_PAY_AMOUNT>
        <NAP_PARTY_B_PAY_DATE Field="30F M"><acmCode function ='GetNapPayDate'/></NAP_PARTY_B_PAY_DATE>
        <NAP_PARTY_B_RECEIVING_AGENT_OPTION Field="57A M"><acmCode function ='GetNapPartyBReceivingAgentOption'/></NAP_PARTY_B_RECEIVING_AGENT_OPTION>
        <NAP_PARTY_B_RECEIVING_AGENT_ACCOUNT Field="57A M"><acmCode function ='GetNapPartyBReceivingAgentAccount'/></NAP_PARTY_B_RECEIVING_AGENT_ACCOUNT>
        <NAP_PARTY_B_RECEIVING_AGENT_BIC Field="57A M"><acmCode function ='GetNapPartyBReceivingAgentAccountBic'/></NAP_PARTY_B_RECEIVING_AGENT_BIC>
        <NAP_PARTY_B_RECEIVING_AGENT_NAME Field="57A M"><acmCode function ='GetNapPartyBReceivingAgentName'/></NAP_PARTY_B_RECEIVING_AGENT_NAME>
        <NAP_PARTY_B_RECEIVING_AGENT_ADDRESS Field="57A M"><acmCode function ='GetNapPartyBReceivingAgentAddress'/></NAP_PARTY_B_RECEIVING_AGENT_ADDRESS>
        <PARTY_A_NUMBER_REPETITIONS Field="18A M"><acmCode function ='GetPartyANumberRepetitions'/></PARTY_A_NUMBER_REPETITIONS>
        <PARTY_B_NUMBER_REPETITIONS Field="18A M"><acmCode function ='GetPartyBNumberRepetitions'/></PARTY_B_NUMBER_REPETITIONS>
        <SCOPE_OF_OPERATION Field="94A O"><acmCode function = 'GetScopeOfOperation'/></SCOPE_OF_OPERATION>
        <SETTLEMENT_METHOD Field="23A M"><acmCode function ='GetSettlementMethod'/></SETTLEMENT_METHOD>
        <TERM_DATE Field="30P M"><acmCode function ='GetTermDate'/></TERM_DATE>
        <TYPE_SWAP Field="23A M"><acmCode function ='GetSwapType'/></TYPE_SWAP>
        <YOUR_REFERENCE Field="21 O"><acmCode function ='GetYourReference' ignoreUpdate ='True'/></YOUR_REFERENCE>
    </SWIFT>
'''

cancellation_template = '''
    <SWIFT>
        <acmTemplate function = 'GetTagsFromOldSwiftBlock' file = 'FSwiftMTConfirmation' />
        <TYPE_OF_OPERATION><acmCode function ='GetTypeOfOperation' file = 'FSwiftMTConfirmation' /></TYPE_OF_OPERATION>
        <YOUR_REFERENCE><acmCode function ='GetYourReference' file = 'FSwiftMTConfirmation' /></YOUR_REFERENCE>
    </SWIFT>
'''

def GetCommonBlock():
    return commonBlock_template

def GetMTXXXBlock(confirmation):
    templateName = 'MT' + str(Calculator.Calculate(confirmation)) + '_template'
    template = globals().get(templateName, '')
    return template

def GetLoanDepositBlock():
    return MTLoanDeposit_template

def GetSwiftTemplate(confirmation):
    if confirmation.Type() == ConfirmationType.CANCELLATION:
        return cancellation_template
    else:
        return swiftTemplate
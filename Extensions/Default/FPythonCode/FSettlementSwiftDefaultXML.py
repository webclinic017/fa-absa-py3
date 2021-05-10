""" Compiled: 2020-09-18 10:38:54 """

#__src_file__ = "extensions/swift/etc/FSettlementSwiftDefaultXML.py"
"""----------------------------------------------------------------------------
MODULE
    FSettlementSwiftDefaultXML

DESCRIPTION
    This module is by default called from FSettlementParametersTemplate.
    It is not recommended to make changes in the module.
----------------------------------------------------------------------------"""

import FSwiftMessageTypeCalculator as Calculator
from FSwiftMTSecuritiesSettlement import IsSecurityCancellation, IsXMLStored

documentSettlementSWIFT = '''\
<MESSAGE>
    <SWIFT>
        <acmTemplate function = 'GetSwiftTemplate' file = 'FSettlementSwiftDefaultXML' />
    </SWIFT>
    <SETTLEMENT file = 'FSwiftMTSettlement'>
        <SEQNBR Field="20 M"><acmCode function = 'GetSeqNbr'/></SEQNBR>
        <CURR><acmCode function = 'GetSettlementCurrency'/></CURR>
    </SETTLEMENT>
</MESSAGE>
'''

swiftTemplate= '''\
    <SWIFT>
        <acmTemplate function = 'GetBaseXMLTemplate' file = 'FSwiftXMLTemplates'/>
        <acmTemplate function = 'GetCommonBlock' file = 'FSettlementSwiftDefaultXML' />
        <acmTemplate function = 'GetMTXXXBlock' file = 'FSettlementSwiftDefaultXML' />
    </SWIFT>
'''

commonBlock_template = '''
    <SWIFT file = 'FSwiftMTSettlement'>
        <DIRECTION><acmCode function = 'GetDirection'/></DIRECTION>
        <NETWORK><acmCode function = 'GetNetwork'/></NETWORK>
        <PARTY_TYPE><acmCode function = 'GetPartyType'/></PARTY_TYPE>
        <RECEIVER_BIC><acmCode function = 'GetReceiverBic'/></RECEIVER_BIC>
        <SENDER_BIC><acmCode function = 'GetSenderBic'/></SENDER_BIC>
        <SEQREF Field="20 M"><acmCode function = 'GetSeqRef'/></SEQREF>
        <SWIFT_LOOPBACK><acmCode function = 'GetSwiftLoopback'/></SWIFT_LOOPBACK>
        <VALUE_DATE Field = "32A M"><acmCode function = 'GetValueDate'/></VALUE_DATE>
    </SWIFT>
'''

Securities_template = '''\
    <SWIFT file = 'FSwiftMTSecuritiesSettlement'>
        <acmInit function ='Init'/>
        <FUNCTION_OF_MESSAGE Field="23G M"><acmCode function = 'GetFunctionOfMessage'/></FUNCTION_OF_MESSAGE>
        <INSTRUMENT_ISIN Field="35B M"><acmCode function = 'GetInstrumentISIN'/></INSTRUMENT_ISIN>
        <DESCRIPTION_OF_SECURITY Field="35B M"><acmCode function = 'GetDescriptionOfSecurity'/></DESCRIPTION_OF_SECURITY>
       	<LINKAGE Field="20C O">
	       <LINKAGE_QUALIFIER Field="20C O"><acmCode function = 'GetLinkageQualifier'/></LINKAGE_QUALIFIER>
	       <LINKAGE_REFERENCE Field="20C O"><acmCode function = 'GetLinkageReference'/></LINKAGE_REFERENCE>
	    </LINKAGE>
        <INDICATOR Field="22F M" acmLoop = "GetIndicators" file = 'FSwiftMTSecuritiesSettlement'>
            <INDICATOR_QUALIFIER Field="22F M"><acmCode function = 'GetQualifier'/></INDICATOR_QUALIFIER>
            <INDICATOR_INDICATOR Field="22F M"><acmCode function = 'GetIndicator'/></INDICATOR_INDICATOR>
        </INDICATOR>
        <QUANTITY Field="36B M">
            <QUANTITY_TYPE_CODE Field="36B M"><acmCode function = 'GetQuantityTypeCode'/></QUANTITY_TYPE_CODE>
            <QUANTITY_QUANTITY Field="36B M"><acmCode function = 'GetQuantity'/></QUANTITY_QUANTITY>
        </QUANTITY>
        <SETTLEMENT_DATETIME Field="98A M">
            <SETTLEMENT_DATETIME_OPTION Field="98A M"><acmCode function = 'GetSettlementDatetimeOption'/></SETTLEMENT_DATETIME_OPTION>
            <SETTLEMENT_DATETIME_QUALIFIER Field="98A M"><acmCode function = 'GetSettlementDatetimeQualifier'/></SETTLEMENT_DATETIME_QUALIFIER>
            <SETTLEMENT_DATETIME_DATE Field="98A M"><acmCode function = 'GetSettlementDatetimeDate'/></SETTLEMENT_DATETIME_DATE>
        </SETTLEMENT_DATETIME>
        <SETTLEMENT_DATETIME Field="98A M">
            <SETTLEMENT_DATETIME_OPTION Field="98A M"><acmCode function = 'GetSettlementDatetimeOption'/></SETTLEMENT_DATETIME_OPTION>
            <SETTLEMENT_DATETIME_QUALIFIER Field="98A M"><acmCode function = 'GetTradeDatetimeQualifier'/></SETTLEMENT_DATETIME_QUALIFIER>
            <SETTLEMENT_DATETIME_DATE Field="98A M"><acmCode function = 'GetTradeDatetimeDate'/></SETTLEMENT_DATETIME_DATE>
        </SETTLEMENT_DATETIME>
        <ACCOUNT Field="97A M">
            <ACCOUNT_OPTION Field="97A M"><acmCode function = 'GetAccountOption'/></ACCOUNT_OPTION>
            <ACCOUNT_QUALIFIER Field="97A M"><acmCode function = 'GetAccountQualifier'/></ACCOUNT_QUALIFIER>
            <ACCOUNT_NUMBER Field="97A M"><acmCode function = 'GetAccountNumber'/></ACCOUNT_NUMBER>
        </ACCOUNT>
        <PARTY acmLoop = "GetPartyDetails" file = 'FSwiftMTSecuritiesSettlement'>
            <PARTY_OPTION Field="95A M"><acmCode function = 'GetPartyOption'/></PARTY_OPTION>
            <PARTY_QUALIFIER Field="95A M"><acmCode function = 'GetPartyQualifier'/></PARTY_QUALIFIER>
            <PARTY_IDENTIFIER_CODE Field="95A M"><acmCode function = 'GetPartyIdentifierCode'/></PARTY_IDENTIFIER_CODE>
            <PARTY_COUNTRY_CODE Field="95A M"><acmCode function = 'GetPartyCountryCode'/></PARTY_COUNTRY_CODE>
            <PARTY_NAME Field="95A M"><acmCode function = 'GetPartyFullName'/></PARTY_NAME>
            <PARTY_ADDRESS Field="95A M"><acmCode function = 'GetPartyAddress'/></PARTY_ADDRESS>
            <PARTY_DATA_SOURCE_SCHEME Field="95A M"><acmCode function = 'GetDataSourceScheme'/></PARTY_DATA_SOURCE_SCHEME>
            <PARTY_PROPRIETARY_CODE Field="95A M"><acmCode function = 'GetPartyProprietaryCode'/></PARTY_PROPRIETARY_CODE>
            <PARTY_SAFEKEEPING_OPTION Field="97A O"><acmCode function = 'GetPartySafekeepingOption'/></PARTY_SAFEKEEPING_OPTION>
            <PARTY_SAFEKEEPING_ACCOUNT Field="97A O"><acmCode function = 'GetPartySafekeepingAccount'/></PARTY_SAFEKEEPING_ACCOUNT>
            <PARTY_SAFEKEEPING_QUALIFIER Field="97A O"><acmCode function = 'GetPartySafekeepingQualifier'/></PARTY_SAFEKEEPING_QUALIFIER>
        </PARTY>
        <PLACE_OF_SAFEKEEPING Field="94A O">
            <PLACE_OF_SAFEKEEPING_OPTION Field="94A O"><acmCode function = 'GetPlaceOfSafekeepingOption'/></PLACE_OF_SAFEKEEPING_OPTION>
            <PLACE_OF_SAFEKEEPING_QUALIFIER Field="94A O"><acmCode function = 'GetPlaceOfSafekeepingQualifier'/></PLACE_OF_SAFEKEEPING_QUALIFIER>
            <PLACE_OF_SAFEKEEPING_PLACE_CODE Field="94A O"><acmCode function = 'GetPlaceOfSafekeepingPlaceCode'/></PLACE_OF_SAFEKEEPING_PLACE_CODE>
            <PLACE_OF_SAFEKEEPING_IDENTIFIER_CODE Field="94A O"><acmCode function = 'GetPlaceOfSafekeepingIdentifierCode'/></PLACE_OF_SAFEKEEPING_IDENTIFIER_CODE>
        </PLACE_OF_SAFEKEEPING>
    </SWIFT>
'''

MT103_template = '''\
    <SWIFT file = 'FSwiftMT103'>
        <acmInit function ='Init'/>
        <ACCOUNT_WITH_INSTITUTION_OPTION Field = "57A M"><acmCode function = 'GetAccountWithInstitutionOption'/></ACCOUNT_WITH_INSTITUTION_OPTION>
        <ACCOUNT_WITH_INSTITUTION_ACCOUNT Field = "57A M"><acmCode function = 'GetAccountWithInstitutionAccount'/></ACCOUNT_WITH_INSTITUTION_ACCOUNT>
        <ACCOUNT_WITH_INSTITUTION_BIC Field = "57A M"><acmCode function = 'GetAccountWithInstitutionBic'/></ACCOUNT_WITH_INSTITUTION_BIC>
        <ACCOUNT_WITH_INSTITUTION_NAME Field = "57A M"><acmCode function = 'GetAccountWithInstitutionName'/></ACCOUNT_WITH_INSTITUTION_NAME>
        <ACCOUNT_WITH_INSTITUTION_ADDRESS Field = "57A M"><acmCode function = 'GetAccountWithInstitutionAddress'/></ACCOUNT_WITH_INSTITUTION_ADDRESS>
        <BANK_OPERATION_CODE Field = "23B M"><acmCode function = 'GetBankOperationCode'/></BANK_OPERATION_CODE>
        <BANKING_PRIORITY><acmCode function = 'GetBankingPriority'/></BANKING_PRIORITY>
        <BENEFICIARY_CUSTOMER_OPTION Field = "59A M"><acmCode function = 'GetBeneficiaryCustomerOption'/></BENEFICIARY_CUSTOMER_OPTION>
        <BENEFICIARY_CUSTOMER_ACCOUNT Field = "59A M"><acmCode function = 'GetBeneficiaryCustomerAccount'/></BENEFICIARY_CUSTOMER_ACCOUNT>
        <BENEFICIARY_CUSTOMER_BIC Field = "59A M"><acmCode function = 'GetBeneficiaryCustomerBic'/></BENEFICIARY_CUSTOMER_BIC>
        <BENEFICIARY_CUSTOMER_NAME Field = "59A M"><acmCode function = 'GetBeneficiaryCustomerName'/></BENEFICIARY_CUSTOMER_NAME>
        <BENEFICIARY_CUSTOMER_ADDRESS Field = "59A M"><acmCode function = 'GetBeneficiaryCustomerAddress'/></BENEFICIARY_CUSTOMER_ADDRESS>
        <BENEFICIARY_CUSTOMER_COUNTRY_CODE Field = "59A M"><acmCode function = 'GetBeneficiaryCustomerCountryCode'/></BENEFICIARY_CUSTOMER_COUNTRY_CODE>
        <BENEFICIARY_CUSTOMER_TOWN Field = "59A M"><acmCode function = 'GetBeneficiaryCustomerTown'/></BENEFICIARY_CUSTOMER_TOWN>
        <BENEFICIARY_CUSTOMER_ZIPCODE Field = "59A M"><acmCode function = 'GetBeneficiaryCustomerZipCode'/></BENEFICIARY_CUSTOMER_ZIPCODE>
        <DETAILS_OF_CHARGES Field = "71A M"><acmCode function = 'GetDetailsOfCharges'/></DETAILS_OF_CHARGES>
        <INTERBANK_SETTLED_AMOUNT Field = "32A M"><acmCode function = 'GetInterbankSettledAmount'/></INTERBANK_SETTLED_AMOUNT>
        <INSTRUCTED_AMOUNT Field = "33B O"><acmCode function = 'GetInstructedAmount'/></INSTRUCTED_AMOUNT>
        <INSTRUCTION_CODE Field = "23E O"><acmCode function = 'GetInstructionCode'/></INSTRUCTION_CODE>
        <INTERMEDIARY_INSTITUTION_OPTION Field = "56A O"><acmCode function = 'GetIntermediaryInstitutionOption'/></INTERMEDIARY_INSTITUTION_OPTION>
        <INTERMEDIARY_INSTITUTION_ACCOUNT Field = "56A O"><acmCode function = 'GetIntermediaryInstitutionAccount'/></INTERMEDIARY_INSTITUTION_ACCOUNT>
        <INTERMEDIARY_INSTITUTION_BIC Field = "56A O"><acmCode function = 'GetIntermediaryInstitutionBic'/></INTERMEDIARY_INSTITUTION_BIC>
        <INTERMEDIARY_INSTITUTION_NAME Field = "56A O"><acmCode function = 'GetIntermediaryInstitutionName'/></INTERMEDIARY_INSTITUTION_NAME>
        <INTERMEDIARY_INSTITUTION_ADDRESS Field = "56A O"><acmCode function = 'GetIntermediaryInstitutionAddress'/></INTERMEDIARY_INSTITUTION_ADDRESS>
        <NATIONAL_CLEARING_SYSTEM><acmCode function = 'GetNationalClearingSystem'/></NATIONAL_CLEARING_SYSTEM>
        <NATIONAL_CLEARING_CODE><acmCode function = 'GetNationalClearingCode'/></NATIONAL_CLEARING_CODE>
        <ORDERING_CUSTOMER_OPTION Field = "50A M"><acmCode function = 'GetOrderingCustomerOption'/></ORDERING_CUSTOMER_OPTION>
        <ORDERING_CUSTOMER_ACCOUNT Field = "50A M"><acmCode function = 'GetOrderingCustomerAccount'/></ORDERING_CUSTOMER_ACCOUNT>
        <ORDERING_CUSTOMER_BIC Field = "50A M"><acmCode function = 'GetOrderingCustomerBic'/></ORDERING_CUSTOMER_BIC>
        <ORDERING_CUSTOMER_NAME Field = "50A M"><acmCode function = 'GetOrderingCustomerName'/></ORDERING_CUSTOMER_NAME>
        <ORDERING_CUSTOMER_ADDRESS Field = "50A M"><acmCode function = 'GetOrderingCustomerAddress'/></ORDERING_CUSTOMER_ADDRESS>
        <ORDERING_CUSTOMER_COUNTRY_CODE Field = "50A M"><acmCode function = 'GetOrderingCustomerCountryCode'/></ORDERING_CUSTOMER_COUNTRY_CODE>
        <ORDERING_CUSTOMER_TOWN Field = "50A M"><acmCode function = 'GetOrderingCustomerTown'/></ORDERING_CUSTOMER_TOWN>
        <ORDERING_CUSTOMER_ZIPCODE Field = "50A M"><acmCode function = 'GetOrderingCustomerZipCode'/></ORDERING_CUSTOMER_ZIPCODE>
        <ORDERING_INSTITUTION_OPTION Field = "52A O"><acmCode function = 'GetOrderingInstitutionOption'/></ORDERING_INSTITUTION_OPTION>
        <ORDERING_INSTITUTION_ACCOUNT Field = "52A O"><acmCode function = 'GetOrderingInstitutionAccount'/></ORDERING_INSTITUTION_ACCOUNT>
        <ORDERING_INSTITUTION_BIC Field = "52A O"><acmCode function = 'GetOrderingInstitutionBic'/></ORDERING_INSTITUTION_BIC>
        <ORDERING_INSTITUTION_NAME Field = "52A O"><acmCode function = 'GetOrderingInstitutionName'/></ORDERING_INSTITUTION_NAME>
        <ORDERING_INSTITUTION_ADDRESS Field = "52A O"><acmCode function = 'GetOrderingInstitutionAddress'/></ORDERING_INSTITUTION_ADDRESS>
        <SENDERS_CORRESPONDENT_OPTION Field="53A O"><acmCode function = 'GetSendersCorrespondentOption'/></SENDERS_CORRESPONDENT_OPTION>
        <SENDERS_CORRESPONDENT_ACCOUNT Field="53A O"><acmCode function = 'GetSendersCorrespondentAccount'/></SENDERS_CORRESPONDENT_ACCOUNT>
        <SENDERS_CORRESPONDENT_BIC Field="53A O"><acmCode function = 'GetSendersCorrespondentBic'/></SENDERS_CORRESPONDENT_BIC>
        <SENDERS_CORRESPONDENT_NAME Field="53A O"><acmCode function = 'GetSendersCorrespondentName'/></SENDERS_CORRESPONDENT_NAME>
        <SENDERS_CORRESPONDENT_ADDRESS Field="53A O"><acmCode function = 'GetSendersCorrespondentAddress'/></SENDERS_CORRESPONDENT_ADDRESS>
        <REMITTANCE_INFO Field = "70 O"><acmCode function = 'GetRemittanceInfo'/></REMITTANCE_INFO>
        <SUB_NETWORK><acmCode function = 'GetSubNetwork'/></SUB_NETWORK>
        <SWIFT_SERVICE_CODE><acmCode function = 'GetSwiftServiceCode'/></SWIFT_SERVICE_CODE>
    </SWIFT>
'''

MT199_template = '''\
    <SWIFT file = 'FSwiftMT199'>
        <acmTemplate function = 'GetMT103Block' file = 'FSettlementSwiftDefaultXML' />
        <SWIFT_RELATION_TYPE><acmCode function = 'GetSwiftRelationType'/></SWIFT_RELATION_TYPE>
        <NARRATIVE Field="79 M"><acmCode function = 'GetNarrative'/></NARRATIVE>
        <SWIFT_SERVICE_CODE><acmCode function = 'GetSwiftServiceCode'/></SWIFT_SERVICE_CODE>
    </SWIFT>
'''

MT200_template = '''\
    <SWIFT file = 'FSwiftMT200'>
        <SEQNBR Field="20 M"><acmCode function = 'GetSeqNbr'/></SEQNBR>
        <CURR Field = "32A M"><acmCode function = 'GetSettlementCurrency'/></CURR>
        <INTERBANK_SETTLED_AMOUNT Field="32A M"><acmCode function = 'GetInterbankSettledAmount'/></INTERBANK_SETTLED_AMOUNT>
        <SENDERS_CORRESPONDENT_ACCOUNT Field="53B O"><acmCode function = 'GetSendersCorrespondentAccount'/></SENDERS_CORRESPONDENT_ACCOUNT>
        <INTERMEDIARY_OPTION Field="56A O"><acmCode function = 'GetIntermediaryOption'/></INTERMEDIARY_OPTION>
        <INTERMEDIARY_ACCOUNT Field="56A O"><acmCode function = 'GetIntermediaryAccount'/></INTERMEDIARY_ACCOUNT>
        <INTERMEDIARY_BIC Field="56A O"><acmCode function = 'GetIntermediaryBic'/></INTERMEDIARY_BIC>
        <INTERMEDIARY_NAME Field="56A O"><acmCode function = 'GetIntermediaryName'/></INTERMEDIARY_NAME>
        <INTERMEDIARY_ADDRESS Field="56A O"><acmCode function = 'GetIntermediaryAddress'/></INTERMEDIARY_ADDRESS>
        <NATIONAL_CLEARING_SYSTEM><acmCode function = 'GetNationalClearingSystem'/></NATIONAL_CLEARING_SYSTEM>
        <NATIONAL_CLEARING_CODE><acmCode function = 'GetNationalClearingCode'/></NATIONAL_CLEARING_CODE>
        <ACCOUNT_WITH_INSTITUTION_OPTION Field="57A M"><acmCode function = 'GetAccountWithInstitutionOption'/></ACCOUNT_WITH_INSTITUTION_OPTION>
        <ACCOUNT_WITH_INSTITUTION_ACCOUNT Field="57A M"><acmCode function = 'GetAccountWithInstitutionAccount'/></ACCOUNT_WITH_INSTITUTION_ACCOUNT>
        <ACCOUNT_WITH_INSTITUTION_BIC Field="57A M"><acmCode function = 'GetAccountWithInstitutionBic'/></ACCOUNT_WITH_INSTITUTION_BIC>
        <ACCOUNT_WITH_INSTITUTION_NAME Field="57A M"><acmCode function = 'GetAccountWithInstitutionName'/></ACCOUNT_WITH_INSTITUTION_NAME>
        <ACCOUNT_WITH_INSTITUTION_ADDRESS Field="57A M"><acmCode function = 'GetAccountWithInstitutionAddress'/></ACCOUNT_WITH_INSTITUTION_ADDRESS>
    </SWIFT>
'''

MT202_template = '''\
    <SWIFT file = 'FSwiftMT202'>
        <acmInit function ='Init'/>
        <ACCOUNT_WITH_INSTITUTION_OPTION Field="57A O"><acmCode function = 'GetAccountWithInstitutionOption'/></ACCOUNT_WITH_INSTITUTION_OPTION>
        <ACCOUNT_WITH_INSTITUTION_ACCOUNT Field="57A O"><acmCode function = 'GetAccountWithInstitutionAccount'/></ACCOUNT_WITH_INSTITUTION_ACCOUNT>
        <ACCOUNT_WITH_INSTITUTION_BIC Field="57A O"><acmCode function = 'GetAccountWithInstitutionBic'/></ACCOUNT_WITH_INSTITUTION_BIC>
        <ACCOUNT_WITH_INSTITUTION_NAME Field="57A O"><acmCode function = 'GetAccountWithInstitutionName'/></ACCOUNT_WITH_INSTITUTION_NAME>
        <ACCOUNT_WITH_INSTITUTION_ADDRESS Field="57A O"><acmCode function = 'GetAccountWithInstitutionAddress'/></ACCOUNT_WITH_INSTITUTION_ADDRESS>
        <BANKING_PRIORITY><acmCode function = 'GetBankingPriority'/></BANKING_PRIORITY>
        <BENEFICIARY_INSTITUTION_OPTION Field="58A M"><acmCode function = 'GetBeneficiaryInstitutionOption'/></BENEFICIARY_INSTITUTION_OPTION>
        <BENEFICIARY_INSTITUTION_ACCOUNT Field="58A M"><acmCode function = 'GetBeneficiaryInstitutionAccount'/></BENEFICIARY_INSTITUTION_ACCOUNT>
        <BENEFICIARY_INSTITUTION_BIC Field="58A M"><acmCode function = 'GetBeneficiaryInstitutionBic'/></BENEFICIARY_INSTITUTION_BIC>
        <BENEFICIARY_INSTITUTION_NAME Field="58A M"><acmCode function = 'GetBeneficiaryInstitutionName'/></BENEFICIARY_INSTITUTION_NAME>
        <BENEFICIARY_INSTITUTION_ADDRESS Field="58A M"><acmCode function = 'GetBeneficiaryInstitutionAddress'/></BENEFICIARY_INSTITUTION_ADDRESS>
        <INTERMEDIARY_OPTION Field="56A O"><acmCode function = 'GetIntermediaryOption'/></INTERMEDIARY_OPTION>
        <INTERMEDIARY_ACCOUNT Field="56A O"><acmCode function = 'GetIntermediaryAccount'/></INTERMEDIARY_ACCOUNT>
        <INTERMEDIARY_BIC Field="56A O"><acmCode function = 'GetIntermediaryBic'/></INTERMEDIARY_BIC>
        <INTERMEDIARY_NAME Field="56A O"><acmCode function = 'GetIntermediaryName'/></INTERMEDIARY_NAME>
        <INTERMEDIARY_ADDRESS Field="56A O"><acmCode function = 'GetIntermediaryAddress'/></INTERMEDIARY_ADDRESS>
        <NATIONAL_CLEARING_SYSTEM><acmCode function = 'GetNationalClearingSystem'/></NATIONAL_CLEARING_SYSTEM>
        <NATIONAL_CLEARING_CODE><acmCode function = 'GetNationalClearingCode'/></NATIONAL_CLEARING_CODE>
        <SUB_NETWORK><acmCode function = 'GetSubNetwork'/></SUB_NETWORK>
        <SWIFT_SERVICE_CODE><acmCode function = 'GetSwiftServiceCode'/></SWIFT_SERVICE_CODE>
        <ORDERING_INSTITUTION_OPTION Field="52A O"><acmCode function = 'GetOrderingInstitutionOption'/></ORDERING_INSTITUTION_OPTION>
        <ORDERING_INSTITUTION_ACCOUNT Field="52A O"><acmCode function = 'GetOrderingInstitutionAccount'/></ORDERING_INSTITUTION_ACCOUNT>
        <ORDERING_INSTITUTION_BIC Field="52A O"><acmCode function = 'GetOrderingInstitutionBic'/></ORDERING_INSTITUTION_BIC>
        <ORDERING_INSTITUTION_NAME Field="52A O"><acmCode function = 'GetOrderingInstitutionName'/></ORDERING_INSTITUTION_NAME>
        <ORDERING_INSTITUTION_ADDRESS Field="52A O"><acmCode function = 'GetOrderingInstitutionAddress'/></ORDERING_INSTITUTION_ADDRESS>
        <SENDERS_CORRESPONDENT_OPTION Field="53A O"><acmCode function = 'GetSendersCorrespondentOption'/></SENDERS_CORRESPONDENT_OPTION>
        <SENDERS_CORRESPONDENT_ACCOUNT Field="53A O"><acmCode function = 'GetSendersCorrespondentAccount'/></SENDERS_CORRESPONDENT_ACCOUNT>
        <SENDERS_CORRESPONDENT_BIC Field="53A O"><acmCode function = 'GetSendersCorrespondentBic'/></SENDERS_CORRESPONDENT_BIC>
        <SENDERS_CORRESPONDENT_NAME Field="53A O"><acmCode function = 'GetSendersCorrespondentName'/></SENDERS_CORRESPONDENT_NAME>
        <SENDERS_CORRESPONDENT_ADDRESS Field="53A O"><acmCode function = 'GetSendersCorrespondentAddress'/></SENDERS_CORRESPONDENT_ADDRESS>
        <YOUR_REFERENCE Field="21 M"><acmCode function = 'GetYourReference'/></YOUR_REFERENCE>
        <INTERBANK_SETTLED_AMOUNT Field="32A M"><acmCode function = 'GetInterbankSettledAmount'/></INTERBANK_SETTLED_AMOUNT>
  </SWIFT>
'''

MT210_template = '''\
    <SWIFT file = 'FSwiftMT210'>
        <acmInit function ='Init'/>
        <ACCOUNT_IDENTIFICATION Field="25 O"><acmCode function = 'GetAccountIdentification'/></ACCOUNT_IDENTIFICATION>
        <RELATED_REFERENCE Field="21 M"><acmCode function = 'GetRelatedReference'/></RELATED_REFERENCE>
        <INTERBANK_SETTLED_AMOUNT Field="32A M"><acmCode function = 'GetInterbankSettledAmount'/></INTERBANK_SETTLED_AMOUNT>
        <INTERMEDIARY_OPTION Field="56A O"><acmCode function = 'GetIntermediaryOption'/></INTERMEDIARY_OPTION>
        <INTERMEDIARY_ACCOUNT Field="56A O"><acmCode function = 'GetIntermediaryAccount'/></INTERMEDIARY_ACCOUNT>
        <INTERMEDIARY_BIC Field="56A O"><acmCode function = 'GetIntermediaryBic'/></INTERMEDIARY_BIC>
        <INTERMEDIARY_NAME Field="56A O"><acmCode function = 'GetIntermediaryName'/></INTERMEDIARY_NAME>
        <INTERMEDIARY_ADDRESS Field="56A O"><acmCode function = 'GetIntermediaryAddress'/></INTERMEDIARY_ADDRESS>
        <NATIONAL_CLEARING_SYSTEM><acmCode function = 'GetNationalClearingSystem'/></NATIONAL_CLEARING_SYSTEM>
        <NATIONAL_CLEARING_CODE><acmCode function= 'GetNationalClearingCode'/></NATIONAL_CLEARING_CODE>
        <ORDERING_INSTITUTION_OPTION Field="52A O"><acmCode function = 'GetOrderingInstitutionOption'/></ORDERING_INSTITUTION_OPTION>
        <ORDERING_INSTITUTION_ACCOUNT Field="52A O"><acmCode function = 'GetOrderingInstitutionAccount'/></ORDERING_INSTITUTION_ACCOUNT>
        <ORDERING_INSTITUTION_BIC Field="52A O"><acmCode function = 'GetOrderingInstitutionBic'/></ORDERING_INSTITUTION_BIC>
        <ORDERING_INSTITUTION_NAME Field="52A O"><acmCode function = 'GetOrderingInstitutionName'/></ORDERING_INSTITUTION_NAME>
        <ORDERING_INSTITUTION_ADDRESS Field="52A O"><acmCode function = 'GetOrderingInstitutionAddress'/></ORDERING_INSTITUTION_ADDRESS>
        <ORDERING_CUSTOMER_OPTION Field="50A O"><acmCode function = 'GetOrderingCustomerOption'/></ORDERING_CUSTOMER_OPTION>
        <ORDERING_CUSTOMER_ACCOUNT Field="50A O"><acmCode function = 'GetOrderingCustomerAccount'/></ORDERING_CUSTOMER_ACCOUNT>
        <ORDERING_CUSTOMER_BIC Field="50A O"><acmCode function = 'GetOrderingCustomerBic'/></ORDERING_CUSTOMER_BIC>
        <ORDERING_CUSTOMER_NAME Field="50A O"><acmCode function = 'GetOrderingCustomerName'/></ORDERING_CUSTOMER_NAME>
        <ORDERING_CUSTOMER_ADDRESS Field="50A O"><acmCode function = 'GetOrderingCustomerAddress'/></ORDERING_CUSTOMER_ADDRESS>
    </SWIFT>
'''

MT299_template = '''\
    <SWIFT file = 'FSwiftMT299'>
        <acmTemplate function = 'GetMT202Block' file = 'FSettlementSwiftDefaultXML' />
        <SWIFT_RELATION_TYPE><acmCode function = 'GetSwiftRelationType'/></SWIFT_RELATION_TYPE>
        <NARRATIVE Field="79 M"><acmCode function = 'GetNarrative'/></NARRATIVE>
        <SWIFT_SERVICE_CODE><acmCode function = 'GetSwiftServiceCode'/></SWIFT_SERVICE_CODE>
    </SWIFT>
'''

MT540_template = '''\
    <SWIFT file = 'FSwiftMT540'>
        <acmInit function ='Init'/>
        <acmTemplate function = 'GetSecuritiesBlock' file = 'FSettlementSwiftDefaultXML' />
    </SWIFT>
'''

MT541_template = '''\
    <SWIFT file = 'FSwiftMT541'>
        <acmInit function ='Init'/>
        <acmTemplate function = 'GetSecuritiesBlock' file = 'FSettlementSwiftDefaultXML' />
        <AMOUNT Field="19A M">
            <AMOUNT_QUALIFIER Field="19A M"><acmCode function = 'GetAmountQualifier'/></AMOUNT_QUALIFIER>
            <AMOUNT_SIGN Field="19A M"><acmCode function = 'GetAmountSign'/></AMOUNT_SIGN>
            <AMOUNT_CURRENCY_CODE Field="19A M"><acmCode function = 'GetCurrencyCode'/></AMOUNT_CURRENCY_CODE>
            <AMOUNT_AMOUNT Field="19A M"><acmCode function = 'GetAmount'/></AMOUNT_AMOUNT>
        </AMOUNT>
    </SWIFT>
'''

MT542_template = '''\
    <SWIFT file = 'FSwiftMT542'>
        <acmInit function ='Init'/>
        <acmTemplate function = 'GetSecuritiesBlock' file = 'FSettlementSwiftDefaultXML' />
    </SWIFT>
'''

MT543_template = '''\
    <SWIFT file = 'FSwiftMT543'>
        <acmInit function ='Init'/>
        <acmTemplate function = 'GetSecuritiesBlock' file = 'FSettlementSwiftDefaultXML' />
        <AMOUNT Field="19A M">
            <AMOUNT_QUALIFIER Field="19A M"><acmCode function = 'GetAmountQualifier'/></AMOUNT_QUALIFIER>
            <AMOUNT_SIGN Field="19A M"><acmCode function = 'GetAmountSign'/></AMOUNT_SIGN>
            <AMOUNT_CURRENCY_CODE Field="19A M"><acmCode function = 'GetCurrencyCode'/></AMOUNT_CURRENCY_CODE>
            <AMOUNT_AMOUNT Field="19A M"><acmCode function = 'GetAmount'/></AMOUNT_AMOUNT>
        </AMOUNT>
    </SWIFT>
'''

Cancellation_template = '''\
    <SWIFT file = 'FSwiftMTCancellation'>
        <acmInit function ='Init'/>
        <RELATED_REF Field = "21 M"><acmCode function = 'GetRelatedRef'/></RELATED_REF>
        <RELATED_REF99 Field = "21 M"><acmCode function = 'GetRelatedRef99'/></RELATED_REF99>
        <ORIGINAL_MESSAGE_MT Field = "11S M"><acmCode function = 'GetOriginalMessageType'/></ORIGINAL_MESSAGE_MT>
        <ORIGINAL_MESSAGE_MT99 Field = "11S M"><acmCode function = 'GetOriginalMessageType99'/></ORIGINAL_MESSAGE_MT99>
        <ORIGINAL_MESSAGE_DATE Field = "11S M"><acmCode function = 'GetOriginalMessageDate'/></ORIGINAL_MESSAGE_DATE>
        <ORIGINAL_MESSAGE_DATE99 Field = "11S M"><acmCode function = 'GetOriginalMessageDate99'/></ORIGINAL_MESSAGE_DATE99>
        <NARRATIVE_DESCRIPTION Field = "79 O"><acmCode function = 'GetNarrativeDescription'/></NARRATIVE_DESCRIPTION>
        <NARRATIVE_DESCRIPTION99 Field = "79 O"><acmCode function = 'GetNarrativeDescription99'/></NARRATIVE_DESCRIPTION99>
    </SWIFT>
'''

MT192_template = '''\
    <SWIFT>
        <acmTemplate function = 'GetCancellationBlock' file = 'FSettlementSwiftDefaultXML'/>
    </SWIFT>
'''

MT292_template = '''\
    <SWIFT>
        <acmTemplate function = 'GetCancellationBlock' file = 'FSettlementSwiftDefaultXML'/>
    </SWIFT>
'''

security_cancellation_template = '''
    <SWIFT>
        <acmTemplate function = 'GetTagsFromOldSwiftBlock' file = 'FSwiftMTSecuritiesSettlement' />
        <FUNCTION_OF_MESSAGE Field="23G M"><acmCode function = 'GetFunctionOfMessage' file = 'FSwiftMTSecuritiesSettlement'/></FUNCTION_OF_MESSAGE>
        <LINKAGE Field="20C O">
	       <LINKAGE_QUALIFIER Field="20C O"><acmCode function = 'GetLinkageQualifier' file = 'FSwiftMTSecuritiesSettlement'/></LINKAGE_QUALIFIER>
	       <LINKAGE_REFERENCE Field="20C O"><acmCode function = 'GetLinkageReference' file = 'FSwiftMTSecuritiesSettlement'/></LINKAGE_REFERENCE>
	    </LINKAGE>
    </SWIFT>
'''

def GetCommonBlock():
    return commonBlock_template

def GetSecuritiesBlock():
    return Securities_template

def GetMT103Block():
    return MT103_template

def GetMT202Block():
    return MT202_template

def GetCancellationBlock():
    return Cancellation_template

def GetMTXXXBlock(settlement):
    templateName = 'MT' + str(Calculator.Calculate(settlement)) + '_template'
    template = globals().get(templateName, '')
    return template

def GetSwiftTemplate(settlement):
    if IsSecurityCancellation(settlement) and IsXMLStored(settlement):
        return security_cancellation_template
    else:
        return swiftTemplate

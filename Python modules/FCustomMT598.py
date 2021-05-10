'''
HISTORY
When            Change                  Who                     What
2017                                    Willie vd Bank          Changed method keyword to function as per 2017 upgrade requirement
'''

import CustomSWIFTFunctions

MT598_template = '''
<MESSAGE>
    <SWIFT>  
        <CODEWORD_NEWLINE><acmCode function ='GetCodewordNewline' file ='CustomSWIFTFunctions' /></CODEWORD_NEWLINE>
        <NARRATIVE_SEPARATOR><acmCode function ='GetNarrativeSeparator' file ='CustomSWIFTFunctions' /></NARRATIVE_SEPARATOR>
        <SWIFT_MESSAGE_TYPE>598</SWIFT_MESSAGE_TYPE>        
        <VERSION><acmCode method ='VERSION' file ='CustomSWIFTFunctions' /></VERSION>
        <NETWORK><acmCode function ='GetNetwork' file ='CustomSWIFTFunctions' /></NETWORK>
        <TYPE_OF_OPERATION Field="22A M"><acmCode function ='GetTypeOfOperation' file ='CustomSWIFTFunctions' /></TYPE_OF_OPERATION>
        <CODE Field="22 M"><acmCode function = 'GetCode'  file ='CustomSWIFTFunctions'/></CODE>       
        <TRANSACTION_REFERENCE><acmCode function ='TRANSACTION_REFERENCE' file ='CustomSWIFTFunctions' ignoreUpdate ='True'  /></TRANSACTION_REFERENCE>
        <SUB_MESSAGE_TYPE><acmCode function ='SUB_MESSAGE_TYPE' file ='CustomSWIFTFunctions' /></SUB_MESSAGE_TYPE>
        <MESSAGE_FUNCTION><acmCode function ='MESSAGE_FUNCTION' file ='CustomSWIFTFunctions'  /></MESSAGE_FUNCTION>
        <PREPARATION_DATETIME><acmCode function ='PREPARATION_DATETIME' file ='CustomSWIFTFunctions' ignoreUpdate ='True' /></PREPARATION_DATETIME>
        <CATEGORY><acmCode function ='CATEGORY' file ='CustomSWIFTFunctions'  /></CATEGORY>
        <GENERIC_CATEGORY><acmCode function ='GENERIC_CATEGORY' file ='CustomSWIFTFunctions'  /></GENERIC_CATEGORY>
        <MATURITY_DATE><acmCode function ='MATURITY_DATE' file ='CustomSWIFTFunctions'  /></MATURITY_DATE>
        <ISSUE_DATE><acmCode function ='ISSUE_DATE' file ='CustomSWIFTFunctions'  /></ISSUE_DATE>
        <TRADE_DATE><acmCode function ='TRADE_DATE' file ='CustomSWIFTFunctions'  /></TRADE_DATE>
        <SETTLEMENT_DATE><acmCode function ='SETTLEMENT_DATE' file ='CustomSWIFTFunctions'  /></SETTLEMENT_DATE>
        <NEXT_RESET_DATE><acmCode function ='NEXT_RESET_DATE' file ='CustomSWIFTFunctions'  /></NEXT_RESET_DATE>
        <CURRENT_INTEREST_RATE><acmCode function ='CURRENT_INTEREST_RATE' file ='CustomSWIFTFunctions'  /></CURRENT_INTEREST_RATE>
        <NEXT_PAYMENT_DATE><acmCode function ='NEXT_PAYMENT_DATE' file ='CustomSWIFTFunctions'  /></NEXT_PAYMENT_DATE>
        <NOMINAL_AMOUNT><acmCode function ='NOMINAL_AMOUNT' file ='CustomSWIFTFunctions'  /></NOMINAL_AMOUNT>
        <SETTLEMENT_AMOUNT><acmCode function ='SETTLEMENT_AMOUNT' file ='CustomSWIFTFunctions'  /></SETTLEMENT_AMOUNT>
        <CLIENT_SOR_ACCOUNT><acmCode function ='CLIENT_SOR_ACCOUNT' file ='CustomSWIFTFunctions'  /></CLIENT_SOR_ACCOUNT>
        <SETTLEMENT_TRANS_TYPE><acmCode function ='SETTLEMENT_TRANSACTION_TYPE' file ='CustomSWIFTFunctions'  /></SETTLEMENT_TRANS_TYPE>
        <RECEIVER_TRADER_BPID><acmCode function ='RECEIVER_TRADER_CSD_BP_ID' file ='CustomSWIFTFunctions'  /></RECEIVER_TRADER_BPID>
        <DELIVERY_TRADER_BPID><acmCode function ='DELIVERY_TRADER_CSD_BP_ID' file ='CustomSWIFTFunctions'  /></DELIVERY_TRADER_BPID>
        <ISIN><acmCode function ='ISIN' file ='CustomSWIFTFunctions'  /></ISIN>
        <LINK><acmCode function ='LINK' file ='CustomSWIFTFunctions'  /></LINK>
        <INTERNAL_TRADE_REFERENCE><acmCode function ='INTERNAL_TRADE_REFERENCE' file ='CustomSWIFTFunctions'  /></INTERNAL_TRADE_REFERENCE>
        <LINK_TRADE_REFERENCE><acmCode function ='LINK_TRADE_REFERENCE' file ='CustomSWIFTFunctions'  /></LINK_TRADE_REFERENCE>
        <AGREEMENT_FLAG><acmCode function ='AGREEMENT_FLAG' file ='CustomSWIFTFunctions'  /></AGREEMENT_FLAG>
        <RECEIVER_BIC><acmCode function ='RECEIVER_BIC' file ='CustomSWIFTFunctions'  /></RECEIVER_BIC>
        <SENDER_BIC Field="22C M"><acmCode function ='SENDER_BIC' file ='CustomSWIFTFunctions'  /></SENDER_BIC>        
        <SEQREF Field="20 M"><acmCode function ='SEQREF' file ='CustomSWIFTFunctions'  /></SEQREF>  
        <SENDERS_REFERENCE><acmCode function ='TRANSACTION_REFERENCE' file ='CustomSWIFTFunctions' ignoreUpdate ='True'  /></SENDERS_REFERENCE>
        <MESSAGE_USER_REFERENCE><acmCode function ='MESSAGE_USER_REFERENCE' file ='CustomSWIFTFunctions' ignoreUpdate ='True'  /></MESSAGE_USER_REFERENCE>
   </SWIFT>
   <CONFIRMATION>
        <CONF_TEMPLATE_CHLNBR><acmCode method ='ConfTemplateChlItem.Name'/></CONF_TEMPLATE_CHLNBR>
        <SEQNBR Field="20 M"><acmCode method ='Oid' ignoreUpdate ='True'/></SEQNBR>
        <CONFIRMATION_SEQNBR><acmCode method ='ConfirmationReference.Name' ignoreUpdate ='True'/></CONFIRMATION_SEQNBR>
        <EVENT_CHLNBR><acmCode method ='EventChlItem.Name'/></EVENT_CHLNBR>
        <RESET_RESNBR><acmCode method ='Reset'/></RESET_RESNBR>
        <STATUS><acmCode method ='Status' ignoreUpdate ='True'/></STATUS>
        <TRANSPORT><acmCode method ='Transport'/></TRANSPORT>
        <TRDNBR><acmCode method ='Trade.Oid'/></TRDNBR>
        <CFWNBR><acmCode method ='CashFlow'/></CFWNBR>
   </CONFIRMATION>   
</MESSAGE>
'''



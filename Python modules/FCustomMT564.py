from CustomSWIFTFunctions import *


MT564_template = '''
<MESSAGE>
    <SWIFT>  
        <SWIFT_MESSAGE_TYPE>564</SWIFT_MESSAGE_TYPE>
        <EVENT_TYPE><acmCode function ='EVENT_TYPE' file ='CustomSWIFTFunctions' ignoreUpdate ='True'  /></EVENT_TYPE>
        <DAYS_ACCRUED_INTEREST><acmCode function ='DAYS_ACCRUED_INTEREST' file ='CustomSWIFTFunctions'  /></DAYS_ACCRUED_INTEREST>
        <ENTITLED_AMOUNT><acmCode function ='ENTITLED_AMOUNT_36B' file ='CustomSWIFTFunctions'  /></ENTITLED_AMOUNT>
        <PREPARATION_DATETIME><acmCode function ='PREPARATION_DATETIME'  file ='CustomSWIFTFunctions'  ignoreUpdate ='True'  /></PREPARATION_DATETIME>
        <CAPITAL_EVENT_REFERENCE><acmCode function ='CAPITAL_EVENT_REFERENCE'  file ='CustomSWIFTFunctions'  /></CAPITAL_EVENT_REFERENCE>
        <CAP_EVNT_MESSAGE_FUNCTION><acmCode function ='CAP_EVNT_MESSAGE_FUNCTION'  file ='CustomSWIFTFunctions'  /></CAP_EVNT_MESSAGE_FUNCTION>
        <ISIN><acmCode function ='ISIN'  file ='CustomSWIFTFunctions'  /></ISIN>
        <RECONCILIATION_DATE><acmCode function ='RECONCILIATION_DATE'  file ='CustomSWIFTFunctions'  /></RECONCILIATION_DATE>
        <COUPON_PERIOD><acmCode function ='COUPON_PERIOD'  file ='CustomSWIFTFunctions'  /></COUPON_PERIOD>
        <COUPON_RATE><acmCode function ='COUPON_RATE'  file ='CustomSWIFTFunctions'  /></COUPON_RATE>
        <CREDIT_DEBIT_INDICATOR><acmCode function ='CREDIT_DEBIT_INDICATOR'  file ='CustomSWIFTFunctions'  /></CREDIT_DEBIT_INDICATOR>
        <TOTAL_ELIGIBLE_NOMINAL><acmCode function ='TOTAL_ELIGIBLE_NOMINAL'  file ='CustomSWIFTFunctions'  /></TOTAL_ELIGIBLE_NOMINAL>
        <PAYMENT_DATE><acmCode function ='PAYMENT_DATE'  file ='CustomSWIFTFunctions'  /></PAYMENT_DATE>
        <ENTITLED_COUPON_PAYMENT><acmCode function ='ENTITLED_COUPON_PAYMENT'  file ='CustomSWIFTFunctions'  /></ENTITLED_COUPON_PAYMENT>
        <ISSUER_AGENT_ID><acmCode function ='ISSUER_AGENT_ID' file ='CustomSWIFTFunctions'  /></ISSUER_AGENT_ID>
        <PAYEE_BIC><acmCode function ='PAYEE_BIC' file ='CustomSWIFTFunctions'  /></PAYEE_BIC>
        <BENEFICIARY_BIC><acmCode function ='BENEFICIARY_BIC' file ='CustomSWIFTFunctions'  /></BENEFICIARY_BIC>
        <RECEIVER_BIC><acmCode function ='RECEIVER_BIC' file ='CustomSWIFTFunctions'  /></RECEIVER_BIC>
        <SENDER_BIC><acmCode function ='SENDER_BIC' file ='CustomSWIFTFunctions'  /></SENDER_BIC>
        <SEQREF><acmCode function ='SEQREF' file ='CustomSWIFTFunctions'  /></SEQREF>
        <MESSAGE_USER_REFERENCE><acmCode function ='MESSAGE_USER_REFERENCE' file ='CustomSWIFTFunctions' ignoreUpdate ='True'  /></MESSAGE_USER_REFERENCE>
        <TRANSACTION_REFERENCE><acmCode function ='TRANSACTION_REFERENCE' file ='CustomSWIFTFunctions' ignoreUpdate ='True'  /></TRANSACTION_REFERENCE>
        
   </SWIFT>
   <CONFIRMATION>
        <CONF_TEMPLATE_CHLNBR><acmCode method ='ConfTemplateChlItem.Name'/></CONF_TEMPLATE_CHLNBR>   
        <SEQNBR Field="20 M" ><acmCode method ='Oid' ignoreUpdate ='True'/></SEQNBR>
        <CONFIRMATION_SEQNBR><acmCode method ='ConfirmationReference.Name' ignoreUpdate ='True'/></CONFIRMATION_SEQNBR>
        <EVENT_CHLNBR><acmCode method ='EventChlItem.Name'/></EVENT_CHLNBR>
        <RESET_RESNBR><acmCode method ='Reset'/></RESET_RESNBR>
        <STATUS><acmCode method ='Status' ignoreUpdate ='True'/></STATUS>
        <TRANSPORT><acmCode method ='Transport'/></TRANSPORT>
        <TRDNBR><acmCode method ='Trade.Oid'/></TRDNBR>
        <CFWNBR><acmCode method ='CashFlow.Oid'/></CFWNBR>
   </CONFIRMATION>   
</MESSAGE>
'''


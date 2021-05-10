"""--------------------------------------------------------------------------------------------------------------------------------------
MODULE
    LoanOpsCommitmentFeeXML

DESCRIPTION
    This module contains XML templates for the Commitment Fee Invoice functionality.

    These templates are plugged into the FConfirmationParameters.templateToXMLMap
    list and are used by Front Arena to determine the xml template to use for a
    given template name.

-----------------------------------------------------------------------------------------------------------------------------------------
HISTORY
=========================================================================================================================================
Date            Change no       Developer               Requester               Description
-----------------------------------------------------------------------------------------------------------------------------------------
2019-09-05      FAOPS-530       Joash Moodley                      Initial Implementation.
-----------------------------------------------------------------------------------------------------------------------------------------
"""


xml_template = '''
<MESSAGE>
    <CONFIRMATION>    
        <CONF_NUMBER><acmCode method ='Oid' ignoreUpdate ='True'/></CONF_NUMBER>
        <CONF_TEMPLATE_CHLNBR><acmCode method ='ConfTemplateChlItem.Name' ignoreUpdate ='True'/></CONF_TEMPLATE_CHLNBR>
        <EVENTCHLITEM><acmCode method='EventChlItem.Name' ignoreUpdate ='True'/></EVENTCHLITEM>        
        <TRANSPORT><acmCode method ='Transport' ignoreUpdate ='True'/></TRANSPORT>
        <AMOUNT><acmCode function='get_invoice_amount' file='LoanOpsCommitmentFeeXMLHooks' ignoreUpdate ='True'/></AMOUNT>
        <VAT><acmCode function='get_vat_amount' file='LoanOpsCommitmentFeeXMLHooks' ignoreUpdate ='True'/></VAT>
        <TOTAL_AMOUNT><acmCode function='get_total_amount' file='LoanOpsCommitmentFeeXMLHooks' ignoreUpdate ='True'/></TOTAL_AMOUNT>
        <CURRENCY><acmCode function='get_currency_name' file='LoanOpsCommitmentFeeXMLHooks' ignoreUpdate ='True'/></CURRENCY>
        <FacilityID><acmCode function='get_facility_id' file='LoanOpsCommitmentFeeXMLHooks' ignoreUpdate ='True'/></FacilityID>
        <Institution><acmCode function='get_institution' file='LoanOpsCommitmentFeeXMLHooks' ignoreUpdate ='True'/></Institution>
        <AccountName ><acmCode function='get_account_name' file='LoanOpsCommitmentFeeXMLHooks' ignoreUpdate ='True'/></AccountName>
        <AccountNumber><acmCode function='get_account_number' file='LoanOpsCommitmentFeeXMLHooks' ignoreUpdate ='True'/></AccountNumber>
        <Reference><acmCode function='get_reference' file='LoanOpsCommitmentFeeXMLHooks' ignoreUpdate ='True'/></Reference>
        <BranchCode><acmCode function='get_branch_code' file='LoanOpsCommitmentFeeXMLHooks' ignoreUpdate ='True'/></BranchCode>
        <SwiftCode><acmCode function='get_swift_code' file='LoanOpsCommitmentFeeXMLHooks' ignoreUpdate ='True'/></SwiftCode>
        <AcquirerVatNumber><acmCode function='acquirer_vat_number' file='LoanOpsCommitmentFeeXMLHooks' ignoreUpdate ='True'/></AcquirerVatNumber>
        <CounterpartyVatNumber><acmCode function='counterparty_vat_number' file='LoanOpsCommitmentFeeXMLHooks' ignoreUpdate ='True'/></CounterpartyVatNumber>
        <VALIDFROM><acmCode function='get_valid_from_date' file='LoanOpsCommitmentFeeXMLHooks' ignoreUpdate ='True'/></VALIDFROM>
        <PayDay><acmCode function='get_pay_date' file='LoanOpsCommitmentFeeXMLHooks' ignoreUpdate ='True'/></PayDay>
    </CONFIRMATION>
    <EMAIL>
        <FROM><acmCode function='get_email_from' file='LoanOpsCommitmentFeeXMLHooks' ignoreUpdate ='True'/></FROM>
        <TO><acmCode function='get_email_to' file='LoanOpsCommitmentFeeXMLHooks' ignoreUpdate ='True'/></TO>
        <BCC><acmCode function='get_email_bcc' file='LoanOpsCommitmentFeeXMLHooks' ignoreUpdate ='True'/></BCC>
        <SUBJECT><acmCode function='get_email_subject' file='LoanOpsCommitmentFeeXMLHooks' ignoreUpdate ='True'/></SUBJECT>
        <BODY><acmCode function='get_email_body' file='LoanOpsCommitmentFeeXMLHooks' ignoreUpdate ='True'/></BODY>
        <FILE_NAME><acmCode function='get_email_file_name' file='LoanOpsCommitmentFeeXMLHooks' ignoreUpdate ='True'/></FILE_NAME>
    </EMAIL>
    <acmTemplate function='get_document_xml' file='LoanOpsCommitmentFeeXMLHooks'/>
</MESSAGE>
'''

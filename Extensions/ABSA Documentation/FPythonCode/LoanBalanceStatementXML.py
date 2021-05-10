"""
-------------------------------------------------------------------------------
MODULE
    LoanBalanceStatementXML


DESCRIPTION
    This module contains XML templates for the loan balance statement functionality.

    These templates are plugged into the FConfirmationParameters.templateToXMLMap
    list and are used by Front Arena to determine the xml template to use for a
    given template name.

-----------------------------------------------------------------------------------------------------------------------------------------
HISTORY
=========================================================================================================================================
Date            Change no       Developer               Requester               Description
-----------------------------------------------------------------------------------------------------------------------------------------
2019-05-29       FAOPS-513      Stuart Wilson           Kershia Perumal         Initial Implementation
-----------------------------------------------------------------------------------------------------------------------------------------
"""


xml_template = '''
<MESSAGE>
    <CONFIRMATION>
        <CONF_NUMBER><acmCode method ='Oid' ignoreUpdate ='True'/></CONF_NUMBER>
        <CONF_TEMPLATE_CHLNBR><acmCode method ='ConfTemplateChlItem.Name' ignoreUpdate ='True'/></CONF_TEMPLATE_CHLNBR>
        <EVENTCHLITEM><acmCode method='EventChlItem.Name' ignoreUpdate ='True'/></EVENTCHLITEM>
        <TRANSPORT><acmCode method ='Transport' ignoreUpdate ='True'/></TRANSPORT>
    </CONFIRMATION>
    <EMAIL>
        <FROM><acmCode function='get_email_from' file='LoanBalanceStatementXMLHooks' ignoreUpdate ='True'/></FROM>
        <BCC><acmCode function='get_email_bcc' file='LoanBalanceStatementXMLHooks'/></BCC>
        <TO><acmCode function='get_email_to' file='LoanBalanceStatementXMLHooks'/></TO>
        <SUBJECT><acmCode function='get_email_subject' file='LoanBalanceStatementXMLHooks' ignoreUpdate ='True'/></SUBJECT>
        <BODY><acmCode function='get_email_body' file='LoanBalanceStatementXMLHooks' ignoreUpdate ='True'/></BODY>
        <FILE_NAME><acmCode function='get_email_file_name' file='LoanBalanceStatementXMLHooks'/></FILE_NAME>
    </EMAIL>
    <acmTemplate function='get_balance_statement_xml' file='LoanBalanceStatementXMLHooks'/>
</MESSAGE>
'''

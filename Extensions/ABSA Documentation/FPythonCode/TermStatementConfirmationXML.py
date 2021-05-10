"""--------------------------------------------------------------------------------------------------------------------------------------
MODULE
    TermStatementConfirmationXML

DESCRIPTION
    This module contains XML templates for the term deposit statement functionality.

    These templates are plugged into the FConfirmationParameters.templateToXMLMap
    list and are used by Front Arena to determine the xml template to use for a
    given template name.

-----------------------------------------------------------------------------------------------------------------------------------------
HISTORY
=========================================================================================================================================
Date            Change no       Developer               Requester               Description
-----------------------------------------------------------------------------------------------------------------------------------------
2018-05-15      FAOPS-127       Cuen Edwards            Elaine Visagie          Initial Implementation
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
        <FROM><acmCode function='get_email_from' file='TermStatementConfirmationXMLHooks' ignoreUpdate ='True'/></FROM>
        <TO><acmCode function='get_email_to' file='TermStatementConfirmationXMLHooks' ignoreUpdate ='True'/></TO>
        <BCC><acmCode function='get_email_bcc' file='TermStatementConfirmationXMLHooks' ignoreUpdate ='True'/></BCC>
        <SUBJECT><acmCode function='get_email_subject' file='TermStatementConfirmationXMLHooks' ignoreUpdate ='True'/></SUBJECT>
        <BODY><acmCode function='get_email_body' file='TermStatementConfirmationXMLHooks' ignoreUpdate ='True'/></BODY>
        <FILE_NAME><acmCode function='get_email_file_name' file='TermStatementConfirmationXMLHooks' ignoreUpdate ='True'/></FILE_NAME>
    </EMAIL>
    <acmTemplate function='get_document_xml' file='TermStatementConfirmationXMLHooks'/>
</MESSAGE>
'''

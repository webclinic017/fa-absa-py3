"""--------------------------------------------------------------------------------------------------------------------------------------
MODULE
    LoanRepaymentNoticeXML

DESCRIPTION
    This module contains the xml template for Loan Repayment Notices.

-----------------------------------------------------------------------------------------------------------------------------------------
HISTORY
=========================================================================================================================================
Date            Change no       Developer               Requester               Description
-----------------------------------------------------------------------------------------------------------------------------------------
2018-11-20                      Stuart Wilson           Loan Ops                XML for confo generation
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
        <FROM><acmCode function='get_email_from' file='LoanRepaymentNoticeXMLHooks' ignoreUpdate ='True'/></FROM>
        <BCC><acmCode function='get_email_bcc' file='LoanRepaymentNoticeXMLHooks'/></BCC>
        <TO><acmCode function='get_email_to' file='LoanRepaymentNoticeXMLHooks'/></TO>
        <SUBJECT><acmCode function='get_email_subject' file='LoanRepaymentNoticeXMLHooks' ignoreUpdate ='True'/></SUBJECT>
        <BODY><acmCode function='get_email_body' file='LoanRepaymentNoticeXMLHooks' ignoreUpdate ='True'/></BODY>
        <FILE_NAME><acmCode function='get_email_file_name' file='LoanRepaymentNoticeXMLHooks'/></FILE_NAME>
    </EMAIL>
    <acmTemplate function='repayment_notice_xml' file='LoanRepaymentNoticeXMLHooks'/>
</MESSAGE>
'''

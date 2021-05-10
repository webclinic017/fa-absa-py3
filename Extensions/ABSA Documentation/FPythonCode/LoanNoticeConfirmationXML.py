"""
-------------------------------------------------------------------------------
MODULE
    LoanNoticeConfirmationXML


DESCRIPTION
    Date                : 2018-06-14
    Purpose             :
    Requester           : Kgomotso Gumbo
    Developer           : Adelaide Davhana


HISTORY
===============================================================================
2018-02-27    Adelaide Davhana   FAOPS-97: initial implementation
2018-09-20    Stuart Wilson      FAOPS-97  Refactor
-------------------------------------------------------------------------------
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
        <FROM><acmCode function='get_email_from' file='LoanNoticeConfirmationXMLHooks' ignoreUpdate ='True'/></FROM>
        <BCC><acmCode function='get_email_bcc' file='LoanNoticeConfirmationXMLHooks'/></BCC>
        <TO><acmCode function='get_email_to' file='LoanNoticeConfirmationXMLHooks'/></TO>
        <SUBJECT><acmCode function='get_email_subject' file='LoanNoticeConfirmationXMLHooks' ignoreUpdate ='True'/></SUBJECT>
        <BODY><acmCode function='get_email_body' file='LoanNoticeConfirmationXMLHooks' ignoreUpdate ='True'/></BODY>
        <FILE_NAME><acmCode function='get_email_file_name' file='LoanNoticeConfirmationXMLHooks'/></FILE_NAME>
    </EMAIL>
    <acmTemplate function='rate_notice_xml' file='LoanNoticeConfirmationXMLHooks'/>
</MESSAGE>
'''

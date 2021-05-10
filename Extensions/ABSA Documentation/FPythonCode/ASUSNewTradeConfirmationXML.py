"""------------------------------------------------------------------------------------------------------------------
MODULE
    ASUSNewTradeConfirmationXML

DESCRIPTION
    Confirmation XML generated for Adaptive consumption

---------------------------------------------------------------------------------------------------------------------
HISTORY
=====================================================================================================================
Date            Change no       Developer               Requester               Description
---------------------------------------------------------------------------------------------------------------------
2020-02-17      FAOPS-708       Tawanda Mukhalela       Ndivhuwo Mashishimise   ASUS New Trade Confirmations
---------------------------------------------------------------------------------------------------------------------
"""


HEADING = '''<?xml version="1.0" encoding="ISO-8859-1"?>'''


CONFIRMATION = '''
    <CONFIRMATION>
        <CONF_NUMBER><acmCode method ='Oid' ignoreUpdate ='True'/></CONF_NUMBER>
        <CONF_TEMPLATE_CHLNBR><acmCode method ='ConfTemplateChlItem.Name' ignoreUpdate ='True'/></CONF_TEMPLATE_CHLNBR>
        <EVENTCHLITEM><acmCode method='EventChlItem.Name' ignoreUpdate ='True'/></EVENTCHLITEM>
        <TRANSPORT><acmCode method ='Transport' ignoreUpdate ='True'/></TRANSPORT>
    </CONFIRMATION>'''


EMAIL = '''
    <EMAIL>
        <FROM><acmCode function='get_from_email_address' file='ASUSNewTradeConfirmationXMLHooks' ignoreUpdate ='True'/></FROM>
        <BCC><acmCode function='get_bcc_email_address' file='ASUSNewTradeConfirmationXMLHooks'/></BCC>
        <TO><acmCode function='get_to_email_address' file='ASUSNewTradeConfirmationXMLHooks'/></TO>
        <SUBJECT><acmCode function='get_email_subject' file='ASUSNewTradeConfirmationXMLHooks' ignoreUpdate ='True'/></SUBJECT>
        <BODY><acmCode function='get_email_body' file='ASUSNewTradeConfirmationXMLHooks' ignoreUpdate ='True'/></BODY>
        <FILE_NAME><acmCode function='get_email_filename' file='ASUSNewTradeConfirmationXMLHooks'/></FILE_NAME>
    </EMAIL>'''


xml_template = \
    HEADING + '''<MESSAGE>''' + CONFIRMATION + EMAIL + '''
    <acmTemplate function='generate_confirmation_xml' file='ASUSNewTradeConfirmationXMLHooks'/>
</MESSAGE>
'''

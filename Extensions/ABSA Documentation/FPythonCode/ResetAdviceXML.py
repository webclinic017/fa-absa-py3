"""
-------------------------------------------------------------------------------
MODULE
    ResetAdviceXML


DESCRIPTION
    XML Template to stamp on the IRS Document

HISTORY
===============================================================================
2018-08-21   Tawanda Mukhalela   FAOPS:168  initial implementation
-------------------------------------------------------------------------------
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
        <FROM><acmCode function='GetAcquirerContactEmail' file='Adaptiv_XML_Functions' ignoreUpdate ='True'/></FROM>
        <BCC><acmCode function='get_bcc_address' file='ResetAdviceXMLGenerator'/></BCC>
        <TO><acmCode function='getCounterpartyAddress' file='Adaptiv_XML_Functions'/></TO>
        <SUBJECT><acmCode function='get_reset_advice_email_subject' file='ResetAdviceXMLGenerator' ignoreUpdate ='True'/></SUBJECT>
        <BODY><acmCode function='get_reset_advice_email_body' file='ResetAdviceXMLGenerator' ignoreUpdate ='True'/></BODY>
        <FILE_NAME><acmCode function='get_reset_advice_filename' file='ResetAdviceXMLGenerator'/></FILE_NAME>
    </EMAIL>'''


xml_template = \
    HEADING + '''<MESSAGE>''' + CONFIRMATION + EMAIL + '''
    <acmTemplate function='reset_advice_xml' file='ResetAdviceXMLGenerator'/>
</MESSAGE>
'''

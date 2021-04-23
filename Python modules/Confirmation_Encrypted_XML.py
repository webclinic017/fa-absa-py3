"""
PURPOSE           : Used in PostprocessStlmConf_ATS to create an xml file which
                    contains readable information for Striata.

================================================================================
HISTORY
================================================================================
Date        Change no           Developer               Description
--------------------------------------------------------------------------------
2017-11-07  CHNG0005091348      Willie van der Bank     Initial development.
2018-08-14  FAU-332             Stuart Wilson           Upgrade compatibility 2018
"""

import acm
from xml.etree.ElementTree import Element, SubElement, tostring
from Adaptiv_XML_Functions import DEV_CONF_EMAIL

ENV = acm.FInstallationData.Select('').At(0).Name()
ZIP_NAME_PREFIX = "Absa_SA_"

CONFIG_DICT = dict()
CONFIG_DICT['Server_Folder'] = r'/striata/FileRouting'
CONFIG_DICT['Remote_Folder'] = r'/striata/ABCAP_FALanding/MMG_STRIATA_CAPITAL_UPLOAD/IN'


def get_send_response(party, response):
    """Return the send accept/reject respose email indicator set to yes or no """
    return  'True' if response in party.add_info('StriataAcceptReject') else 'False'
       

def create_XML(confirmation):

    MESSAGE = Element('MESSAGE')
    
    CONFIRMATIONID = SubElement(MESSAGE, 'CONFIRMATIONID')
    CONFIRMATIONNEG = SubElement(MESSAGE, 'CONFIRMATIONNEG')
    CONFIRMATIONTYPE = SubElement(MESSAGE, 'CONFIRMATIONTYPE')    
    CUSTOMERHINT = SubElement(MESSAGE, 'CUSTOMERHINT')
    CUSTOMERKEY = SubElement(MESSAGE, 'CUSTOMERKEY')
    # Please note: the CUSTOMERSHORTNAME element is inappropriately
    # named and should be changed.  Initially this element held the
    # party name (ptyid) but has since been changed to hold a concate-
    # nation of party full name and any party short code. 
    CUSTOMERSHORTNAME = SubElement(MESSAGE, 'CUSTOMERSHORTNAME')
    EMAILADDRESS = SubElement(MESSAGE, 'EMAILADDRESS')
    EVENTTYPE = SubElement(MESSAGE, 'EVENTTYPE')
    FILETYPE = SubElement(MESSAGE, 'FILETYPE')
    RELATEDCONF = SubElement(MESSAGE, 'RELATEDPREVID')
    BANKRESPONSE = SubElement(MESSAGE, 'BANKRESPONSE')
    SENDACCEPTRESPONSE = SubElement(MESSAGE, 'SENDACCEPTRESPONSE')
    SENDREJECTRESPONSE = SubElement(MESSAGE, 'SENDREJECTRESPONSE')
    SENDERID = SubElement(MESSAGE, 'SENDERID')
    TRADEREF = SubElement(MESSAGE, 'TRADEREF')
    
    CPTY = confirmation.Trade().Counterparty()
    CONFIRMATIONID.text = 'A' + str(confirmation.Oid())
    CONFIRMATIONNEG.text = 'False'
    if not confirmation.Type() == 'Default':
        CONFIRMATIONTYPE.text = confirmation.Type()
    if CPTY.AdditionalInfo().StriataPassword():
        SDSID = CPTY.AdditionalInfo().BarCap_Eagle_SDSID()
        if len(SDSID) >= 3:
            CUSTOMERKEY.text = SDSID
            CUSTOMERHINT.text = 'Please enter your Absa ID ending in ' + str(SDSID[-3:])    
    if ENV == 'Production':
        contactEmail = [c.Email() for c in confirmation.Counterparty().Contacts() if c.Name() == confirmation.CounterpartyContact()]
        if contactEmail:
            EMAILADDRESS.text = contactEmail[0]
    else:
        EMAILADDRESS.text = str(DEV_CONF_EMAIL)
    EVENTTYPE.text = confirmation.EventChlItem().Name()
    CUSTOMERSHORTNAME.text = _get_party_name(confirmation.Counterparty())
    FILETYPE.text = 'PDF'
    if confirmation.ConfirmationReference():
        RELATEDCONF.text = 'A' + str(confirmation.ConfirmationReference().Oid())
    SENDACCEPTRESPONSE.text = get_send_response(CPTY, 'Accept')
    SENDREJECTRESPONSE.text = get_send_response(CPTY, 'Reject')
    SENDERID.text = confirmation.Trade().Acquirer().AdditionalInfo().BarCap_Eagle_SDSID()
    TRADEREF.text = str(confirmation.Trade().Oid())
    #Manual match overrides
    if confirmation.Status() in ('Matched', 'Matching Failed'):
        CONFIRMATIONTYPE.text = confirmation.Status()
        BANKRESPONSE.text = 'True' if confirmation.Status() == 'Matched' else 'False'
        SENDACCEPTRESPONSE.text = 'False'
        SENDREJECTRESPONSE.text = 'False'
            
    return MESSAGE


def create_xml_file_main(confirmation):
    Server_Folder = CONFIG_DICT['Server_Folder']
    newfilepath = Server_Folder + "/"
    try:
        xml = create_XML(confirmation)
        filename = str(confirmation.Oid()) + '.xml'
        tmpfile = file(newfilepath + filename, 'w')
        tmpfile.write(tostring(xml))
        tmpfile.close()
        print('Created XML file for encryption:', newfilepath + filename)
        return True
    except Exception, e:
        print("XML creation failed for", confirmation.Oid())
        print(e)


def _get_party_name(party):
    """
    Get the party name to send to Striata.
    
    Please note: in the event that both the party full name and short
    code are missing, business have requested that an empty string be
    sent rather than raising an exception.
    """
    name_parts = list()
    if _is_string_value_present(party.Fullname()):
        name_parts.append(party.Fullname().strip())
    if _is_string_value_present(party.ShortCode()):
        name_parts.append('({short_code})'.format(short_code=party.ShortCode()))
    return ' '.join(name_parts)


def _is_string_value_present(value):
    """
    Determine whether or not a string value is present (not None,
    empty, or only consisting of whitespace).
    """
    if value is None:
        return False
    return value.strip() != ''

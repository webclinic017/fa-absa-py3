"""--------------------------------------------------------------------------------------------------------------------------------------
MODULE
    DocumentXMLGenerator
    
DESCRIPTION
    This module contains an abstract implementation of an object used for
    generating the XML content of a correspondence document.

-----------------------------------------------------------------------------------------------------------------------------------------
HISTORY
=========================================================================================================================================
Date            Change no       Developer               Requester               Description
-----------------------------------------------------------------------------------------------------------------------------------------
2018-05-15      FAOPS-127       Cuen Edwards            Elaine Visagie          Initial Implementation.
2018-08-28      FAOPS-218       Cuen Edwards            Kgomotso Gumbo          Added support for the addition of an ignoreUpdate attri-
                                                                                bute on document elements.  This is used by Front Arena
                                                                                to exclude certain elements when generating the checksum
                                                                                for a confirmation.
2019-05-27      FAOPS-401/402   Cuen Edwards            Chris van der Walt      Changed to support generation of documents for parties
                                                                                without contacts.
-----------------------------------------------------------------------------------------------------------------------------------------
"""

import datetime
import xml.dom.minidom as minidom
import xml.etree.ElementTree as ElementTree

import DocumentGeneral


class GenerateDocumentXMLRequest(object):
    """
    An abstract implementation embodying the request to generate the 
    XML content for a correspondence document.
    """

    def __init__(self, from_party, from_party_contact, to_party,
            to_party_contact):
        """
        Constructor.
        """
        self.from_party = from_party
        self.from_party_contact = from_party_contact
        self.to_party = to_party
        self.to_party_contact = to_party_contact


class DocumentXMLGenerator(object):
    """
    An abstract implementation responsible for generating the XML 
    content for a correspondence document.
    """

    def generate_xml(self, generate_document_xml_request):
        """
        Generate the XML for a correspondence document.
        """
        document_element = self._generate_document_element(
            generate_document_xml_request)
        xml_string = ElementTree.tostring(document_element)
        document = minidom.parseString(xml_string)
        # Return a pretty-printed version of the document without
        # the xml declaration (Front doesn't seem to like acmTemplate
        # hooks returning XML with an XML declaration).
        root_element = document.childNodes[0]
        return root_element.toprettyxml(indent='  ')

    def _generate_document_element(self, generate_document_xml_request):
        """
        Generate the DOCUMENT XML element and sub-elements.
        """
        from_party = generate_document_xml_request.from_party
        from_party_contact = generate_document_xml_request.from_party_contact
        to_party = generate_document_xml_request.to_party
        to_party_contact = generate_document_xml_request.to_party_contact
        element = self._generate_element('DOCUMENT')
        if from_party_contact:
            element.append(self._generate_from_element(from_party, from_party_contact))
        if to_party_contact:
            element.append(self._generate_to_element(to_party, to_party_contact))
        element.append(self._generate_element('CREATE_TIME', datetime.datetime.today()
            .strftime('%Y-%m-%d %H:%M:%S'), ignore_update=True))            
        element.append(self._generate_subject_element(generate_document_xml_request))            
        element.append(self._generate_document_specific_element(
            generate_document_xml_request))        
        element.append(self._generate_footer_element(generate_document_xml_request))
        return element

    def _generate_from_element(self, from_party, from_party_contact):
        """
        Generate the document FROM XML element and sub-elements.
        """
        element = self._generate_element('FROM')
        element.append(self._generate_element('NAME', DocumentGeneral
            .get_default_document_from_name()))
        element.append(self._generate_address_element(from_party_contact))
        element.append(self._generate_element('TEL', from_party_contact.Telephone()))
        element.append(self._generate_element('EMAIL', from_party_contact.Email()))
        element.append(self._generate_element('WEBSITE', DocumentGeneral
            .get_default_document_from_website()))
        return element

    def _generate_to_element(self, to_party, to_party_contact):
        """
        Generate the document TO XML element and sub-elements.
        """
        element = self._generate_element('TO')
        element.append(self._generate_element('NAME', DocumentGeneral.get_party_full_name(to_party)))
        # Add the value of the party ShortCode field if present.
        # This field is generally used to hold any related fund
        # code associated with a party.
        short_code = DocumentGeneral.get_party_short_code(to_party)
        if short_code is not None:
            element.append(self._generate_element('SHORTCODE', short_code))
        element.append(self._generate_address_element(to_party_contact))
        return element

    def _generate_address_element(self, party_contact):
        """
        Generate an ADDRESS XML element and sub-elements.
        """
        element = self._generate_element('ADDRESS')
        element.append(self._generate_element('LINE1', party_contact.Address()))
        element.append(self._generate_element('LINE2', party_contact.Address2()))
        element.append(self._generate_element('CITY', party_contact.City()))
        element.append(self._generate_element('COUNTRY', party_contact.Country()))
        element.append(self._generate_element('ZIPCODE', party_contact.Zipcode()))
        return element
        
    def _generate_subject_element(self, generate_document_xml_request):
        """
        Generate the document SUBJECT XML element and sub-
        elements.
        """
        raise NotImplementedError()

    def _generate_document_specific_element(self, generate_document_xml_request):
        """
        Generate the document-specific XML element and sub-elements.
        """
        raise NotImplementedError()
        
    def _generate_footer_element(self, generate_document_xml_request):
        """
        Generate the document FOOTER XML element and sub-elements.
        """
        return self._generate_element('FOOTER', DocumentGeneral
            .get_default_document_footer())

    @staticmethod
    def _generate_element(element_name, element_text='', ignore_update=False):
        """
        Generate an XML element with the specified name and text.
        """
        element = ElementTree.Element(element_name)
        element.text = element_text
        if ignore_update:
            element.set('ignoreUpdate', 'True')
        return element

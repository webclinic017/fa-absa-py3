"""--------------------------------------------------------------------------------------------------------------------------------------
MODULE
    SARBSecurityTransferInstructionXMLGenerator

DESCRIPTION
    This module contains an object used for generating the XML content for a
    SARB security transfer instruction.

-----------------------------------------------------------------------------------------------------------------------------------------
HISTORY
=========================================================================================================================================
Date            Change no       Developer               Requester               Description
-----------------------------------------------------------------------------------------------------------------------------------------
2020-05-04      FAOPS-746       Cuen Edwards            Kgomotso Gumbo          Initial implementation.
-----------------------------------------------------------------------------------------------------------------------------------------
"""

import xml.etree.ElementTree as ElementTree

import SARBSecurityTransferInstructionGeneral


class GenerateSARBSecurityTransferInstructionXMLRequest(object):
    """
    An object embodying the request to generate the XML content for a
    SARB security transfer instruction.
    """

    def __init__(self, reference, event_name, transfer_date):
        """
        Constructor.
        """
        self.reference = reference
        self.event_name = event_name
        self.transfer_date = transfer_date


class SARBSecurityTransferInstructionXMLGenerator(object):
    """
    An object responsible for generating the XML content for a SARB
    security transfer instruction.
    """

    @classmethod
    def generate_xml(cls, generate_instruction_xml_request):
        """
        Generate the XML for a SARB security transfer instruction.
        """
        security_transfer_instruction_element = cls._generate_security_transfer_instruction_element(
            generate_instruction_xml_request)
        return ElementTree.tostring(security_transfer_instruction_element)

    @classmethod
    def _generate_security_transfer_instruction_element(cls, generate_advice_xml_request):
        """
        Generate the SECURITY_TRANSFER_INSTRUCTION XML element and
        sub-elements.
        """
        reference = generate_advice_xml_request.reference
        event_name = generate_advice_xml_request.event_name
        transfer_date = generate_advice_xml_request.transfer_date
        bank_contact = SARBSecurityTransferInstructionGeneral.get_bank_contact(event_name)
        bank_bic = SARBSecurityTransferInstructionGeneral.get_bank_bic(bank_contact)
        bank_from_name = SARBSecurityTransferInstructionGeneral.get_bank_from_name(bank_contact)
        bank_from_telephone = SARBSecurityTransferInstructionGeneral.get_bank_from_telephone(bank_contact)
        sarb_contact = SARBSecurityTransferInstructionGeneral.get_sarb_contact(event_name)
        sarb_bic = SARBSecurityTransferInstructionGeneral.get_sarb_bic(sarb_contact)
        element = cls._generate_element('SECURITY_TRANSFER_INSTRUCTION')
        element.append(cls._generate_element('REFERENCE', reference))
        element.append(cls._generate_element('BANK_BIC', bank_bic))
        element.append(cls._generate_element('BANK_FROM_NAME', bank_from_name))
        element.append(cls._generate_element('BANK_FROM_TELEPHONE', bank_from_telephone))
        element.append(cls._generate_element('SARB_BIC', sarb_bic))
        element.append(cls._generate_element('EVENT', event_name))
        element.append(cls._generate_element('TRANSFER_DATE', transfer_date))
        element.append(cls._generate_security_transfers_element(event_name, transfer_date))
        return element

    @classmethod
    def _generate_security_transfers_element(cls, event_name, transfer_date):
        """
        Generate the SECURITY_TRANSFERS XML element and sub-elements.
        """
        element = cls._generate_element('SECURITY_TRANSFERS')
        security_transfers = SARBSecurityTransferInstructionGeneral.get_security_transfers(event_name, transfer_date)
        security_transfers.sort(key=lambda transfer: transfer.security_name)
        for security_transfer in security_transfers:
            element.append(security_transfer.to_xml_element())
        return element

    @staticmethod
    def _generate_element(element_name, element_text=''):
        """
        Generate an XML element with the specified name and text.
        """
        element = ElementTree.Element(element_name)
        element.text = element_text
        return element

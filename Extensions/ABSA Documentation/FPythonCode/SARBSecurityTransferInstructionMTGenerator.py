"""--------------------------------------------------------------------------------------------------------------------------------------
MODULE
    SARBSecurityTransferInstructionMTGenerator

DESCRIPTION
    This module contains an object used for generating the SWIFT MT message
    rendering of a SARB security transfer instruction.

-----------------------------------------------------------------------------------------------------------------------------------------
HISTORY
=========================================================================================================================================
Date            Change no       Developer               Requester               Description
-----------------------------------------------------------------------------------------------------------------------------------------
2020-05-04      FAOPS-746       Cuen Edwards            Kgomotso Gumbo          Initial implementation.
-----------------------------------------------------------------------------------------------------------------------------------------
"""

import xml.etree.ElementTree as ElementTree

import ael

from gen_swift_common import CRLF
from gen_swift_mt199 import MT199
import SARBSecurityTransferInstructionGeneral
from SARBSecurityTransferInstructionGeneral import SecurityTransfer


class GenerateSARBSecurityTransferInstructionMTRequest(object):
    """
    An object embodying the request to generate the SWIFT MT message
    rendering of a SARB security transfer instruction.
    """

    def __init__(self, xml_string):
        """
        Constructor.
        """
        self.xml_string = xml_string


class SARBSecurityTransferInstructionMTGenerator(object):
    """
    An object responsible for generating the SWIFT MT message
    rendering of a SARB security transfer instruction.
    """

    @classmethod
    def generate_mt_message(cls, generate_mt_request):
        """
        Generate the SWIFT MT message rendering of a SARB security
        transfer instruction.
        """
        xml_string = generate_mt_request.xml_string
        root_element = ElementTree.fromstring(xml_string)
        reference = root_element.find('REFERENCE').text
        related_reference = 'TRANSFER'
        bank_bic = root_element.find('BANK_BIC').text
        sarb_bic = root_element.find('SARB_BIC').text
        narrative = cls._create_narrative(root_element)
        message = cls._create_mt199(bank_bic, sarb_bic, reference, related_reference, narrative)
        return str(message)

    @classmethod
    def _create_narrative(cls, root_element):
        """
        Create the narrative for the MT199 message.
        """
        bank_from_name = root_element.find('BANK_FROM_NAME').text
        bank_from_telephone = root_element.find('BANK_FROM_TELEPHONE').text
        event_name = root_element.find('EVENT').text
        transfer_date = root_element.find('TRANSFER_DATE').text
        direction_description = cls._get_transfer_direction_description(event_name)
        security_transfers = cls._get_security_transfers(root_element)
        narrative = 'GOOD DAY{line_break}'
        narrative += 'KINDLY TRANSFER {direction_description}{line_break}'
        narrative += 'VALUE DATE {transfer_date}{line_break}'
        for security_transfer in security_transfers:
            narrative += '{security_name} {amount:,.0f}{line_break}'.format(
                security_name=security_transfer.security_name,
                amount=abs(security_transfer.amount),
                line_break=CRLF
            )
        narrative += '{bank_from_name}{line_break}'
        narrative += '{bank_from_telephone}'
        return narrative.format(
            line_break=CRLF,
            direction_description=direction_description,
            transfer_date=ael.date(transfer_date).to_string('%d %b %Y'),
            bank_from_name=bank_from_name,
            bank_from_telephone=bank_from_telephone
        )

    @staticmethod
    def _get_transfer_direction_description(event_name):
        """
        Get a description of the transfer direction for the specified
        event name.
        """
        if event_name == SARBSecurityTransferInstructionGeneral.get_transfer_from_custodian_event_name():
            return 'FROM CD TO SARB'
        elif event_name == SARBSecurityTransferInstructionGeneral.get_transfer_to_custodian_event_name():
            return 'FROM SARB TO CD'
        raise ValueError("Unsupported event '{event_name}' specified.".format(
            event_name=event_name
        ))

    @staticmethod
    def _get_security_transfers(root_element):
        """
        Get the security transfers for the SARB security transfer
        instruction.
        """
        security_transfers = list()
        for security_transfer_element in root_element.iterfind('SECURITY_TRANSFERS/SECURITY_TRANSFER'):
            security_transfer = SecurityTransfer.from_xml_element(security_transfer_element)
            security_transfers.append(security_transfer)
        return security_transfers

    @staticmethod
    def _create_mt199(from_bic, to_bic, reference, related_reference, narrative):
        """
        Create an SWIFT MT199 message.
        """
        message = MT199()
        message.Header.LogicalTerminal.BicCode = from_bic
        message.ApplicationHeader.Address.BicCode = to_bic
        message.UserHeader.MessageUserReference = reference
        message.Body.TransactionReference = reference
        message.Body.RelatedReference = related_reference
        message.Body.Narrative = narrative
        return message

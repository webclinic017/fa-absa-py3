"""--------------------------------------------------------------------------------------------------------------------------------------
MODULE
    LoanOpsCommitmentFeeXMLGenerator
    
DESCRIPTION
    This module contains an object used for generating the XML content for a
    Commitment Fee Invoice.

-----------------------------------------------------------------------------------------------------------------------------------------
HISTORY
=========================================================================================================================================
Date            Change no       Developer               Requester               Description
-----------------------------------------------------------------------------------------------------------------------------------------
2019-09-05      FAOPS-530       Joash Moodley                      Initial Implementation.
-----------------------------------------------------------------------------------------------------------------------------------------
"""

import DocumentGeneral
from DocumentXMLGenerator import DocumentXMLGenerator, GenerateDocumentXMLRequest


class GenerateLoanOpsCommitmentFeetXMLRequest(GenerateDocumentXMLRequest):
    """
    An object embodying the request to generate the XML content for a 
    Commitment Fee Invoice.
    """

    def __init__(self, from_party, from_party_contact, to_party, to_party_contact,
            from_date, to_date, schedule=None):
        """
        Constructor.
        """
        super(GenerateLoanOpsCommitmentFeetXMLRequest, self).__init__(from_party, from_party_contact,
            to_party, to_party_contact)
        self.from_date = from_date
        self.to_date = to_date
        self.schedule = schedule


class LoanOpsCommitmentFeeXMLGenerator(DocumentXMLGenerator):
    """
    An object responsible for generating the XML content for a Commitment Fee Invoice.
    """

    def __init__(self):
        """
        Constructor.
        """


    def generate_xml(self, generate_commitment_fee_xml_request):
        """
        Generate the XML for a Commitment Fee Invoice.
        """
        return super(LoanOpsCommitmentFeeXMLGenerator, self).generate_xml(
            generate_commitment_fee_xml_request)

    def _generate_subject_element(self, generate_commitment_fee_xml_request):
        """
        Generate the document SUBJECT XML element and sub-
        elements.
        """
        invoice_from_date = generate_commitment_fee_xml_request.from_date
        invoice_to_date = generate_commitment_fee_xml_request.to_date
        subject = 'Commitment Fee for {period_description}'
        period_description = DocumentGeneral.get_date_range_description(
            invoice_from_date, invoice_to_date)
        subject = subject.format(
            period_description=period_description
        )
        return self._generate_element('SUBJECT', subject)

    def _generate_document_specific_element(self, generate_commitment_fee_xml_request):
        """
        Generate the Commit Fee Invoice XML element and sub-elements.
        """
        acquirer = generate_commitment_fee_xml_request.from_party
        counterparty = generate_commitment_fee_xml_request.to_party
        invoice_from_date = generate_commitment_fee_xml_request.from_date
        invoice_to_date = generate_commitment_fee_xml_request.to_date
        invoice_schedule = generate_commitment_fee_xml_request.schedule
        element = self._generate_element('COMMITMENT_FEE')

        return element


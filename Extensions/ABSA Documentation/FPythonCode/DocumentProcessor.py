"""--------------------------------------------------------------------------------------------------------------------------------------
MODULE
    DocumentProcessor

DESCRIPTION
    This module is used to define the API of a document processor.

-----------------------------------------------------------------------------------------------------------------------------------------
HISTORY
=========================================================================================================================================
Date            Change no       Developer               Requester               Description
-----------------------------------------------------------------------------------------------------------------------------------------
2019-09-17      FAOPS-460       Cuen Edwards            Letitia Carboni         Initial Implementation.
-----------------------------------------------------------------------------------------------------------------------------------------
"""


class DocumentProcessor(object):
    """
    Definition of a document processor.
    """

    def get_name(self):
        """
        Get the name of the document processor.
        """
        raise NotImplementedError()

    def is_processable(self, business_process):
        """
        Determines whether or not the processor would perform
        any automated processing on a specified document business
        process.
        """
        raise NotImplementedError()

    def process(self, business_process):
        """
        Perform any automated processing on a document business
        process.
        """
        raise NotImplementedError()

    def get_supported_formats(self):
        """
        Get the formats supported for a document.
        """
        raise NotImplementedError()

    def document_format_available(self, business_process, document_format):
        """
        Determines whether or not a document is available for
        retrieval, viewing, etc. in a specified format.
        """
        raise NotImplementedError()

    def render_document_file(self, business_process, document_format):
        """
        Render a document to file in the specified format for a
        document business process and return the file path.
        """
        raise NotImplementedError()

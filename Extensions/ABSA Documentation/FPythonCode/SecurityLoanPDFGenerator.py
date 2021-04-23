"""--------------------------------------------------------------------------------------------------------------------------------------
MODULE
    SecurityLoanPDFGenerator

DESCRIPTION
    Processes XML to generate a PDF Document using FOP and FXSLT stylesheet

-----------------------------------------------------------------------------------------------------------------------------------------
HISTORY
=========================================================================================================================================
Date            Change no       Developer               Requester               Description
-----------------------------------------------------------------------------------------------------------------------------------------
2020-01-31      FAOPS-557       Tawanda Mukhalela       Khaya Mbebe             Initial Implementation.
-----------------------------------------------------------------------------------------------------------------------------------------
"""
import os
import acm
import DocumentGeneral
import STATIC_TEMPLATE
from string import Template
from datetime import datetime
import FReportSettings as DefaultPaths
import xml.etree.ElementTree as ElementTree
from SecurityLoanGeneral import get_event_name, unix_chmod

XMLREPORT_RESOURCES = {
    'img-absa-logo': os.path.join(DefaultPaths.LOGOS_PATH, 'absa_logo_2018.png'),
    'txt-absareg': STATIC_TEMPLATE.ABSA_REG
}

XMLREPORT_SCHEMA_PATH = os.path.join(DefaultPaths.XSLT_PATH, 'XMLReport.xsd')

PERMISSION_MODE = 0o775

TODAY = datetime.now()


class GenerateSecurityLoanPDFRequest(object):

    def __init__(self, xml_string, output_dir):
        self.xml_string = xml_string
        self.output_dir = output_dir


class PDFDocumentGenerator(object):
    """
    Class for PDF report generation from XML source.
    """

    def __init__(self, output_dir, xsl_fo_template_name=''):
        self.output_dir = output_dir
        self.xsl_fo_template_name = xsl_fo_template_name
        self.validate_xml = DefaultPaths.VALIDATE_XML
        self.xsd_path = XMLREPORT_SCHEMA_PATH

    def create(self, xml, filename):
        """
        Create the PDF and save it to disk.
        """
        xml = PDFDocumentGenerator._add_resources(xml)
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

        os.chdir(DefaultPaths.XSLT_PATH)
        template_object = acm.GetDefaultContext().GetExtension('FXSLTemplate', 'FObject', self.xsl_fo_template_name)
        if not template_object:
            raise ValueError("Failed to find template " + self.xsl_fo_template_name + " report output not completed")

        transformer = acm.CreateWithParameter('FXSLTTransform', template_object.Value())
        if self.validate_xml:
            transformer.SetExternalNoNamespaceSchemaLocation(self.xsd_path)
            transformer.SetUseValidation(False)

        xml_fo = transformer.Transform(xml)
        xml_fo_path = os.path.join(self.output_dir, filename + '.fo')
        with open(xml_fo_path, 'wb') as xml_fo_file:
            xml_fo_file.write(xml_fo)

        final_report_path = os.path.join(self.output_dir, filename)
        command = Template(DefaultPaths.FOP_BAT)
        command = command.substitute({'extension': 'pdf', 'filename': final_report_path})

        if os.system(command):
            # always keep FO file on error
            message = "PDF Output creation Error."
            message += "Necessary third party software might not be installed. Command: "
            raise RuntimeError(message + command)

        if not DefaultPaths.KEEP_FO:
            os.remove(xml_fo_path)

        return final_report_path + '.pdf'

    @staticmethod
    def _add_resources(xml_string):
        xml = ElementTree.fromstring(xml_string)

        settings = ElementTree.SubElement(xml, '__XMLReportResources')
        for key, value in XMLREPORT_RESOURCES.items():
            ElementTree.SubElement(settings, key).text = value

        return ElementTree.tostring(xml)


class SecurityLoanPDFGenerator(object):

    @staticmethod
    def generate_pdf(generate_pdf_request):
        xml_string = generate_pdf_request.xml_string
        output_dir = generate_pdf_request.output_dir
        root_element = ElementTree.fromstring(xml_string)
        counterparty_name = root_element.find('TO/NAME').text
        # Create file name.
        file_name_template = "{description}_{counterparty_name}_{time}"
        file_name = file_name_template.format(
            description=get_event_name(),
            counterparty_name=counterparty_name,
            time=TODAY
        )
        formated_file_name = DocumentGeneral.format_file_name(file_name)
        xsl_report = PDFDocumentGenerator(output_dir, 'SecurityLoanConfirmationXSLTemplate')
        pdf_url = xsl_report.create(xml_string, formated_file_name)
        unix_chmod(pdf_url, PERMISSION_MODE)
        return pdf_url

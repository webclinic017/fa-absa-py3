'''
requester       developer               date            change #        description
Hilliard Nyman  Evgeniya Baskaeva       08/11/2016      CHNG0003774716  Created.
Anesu Musendo   Willie vd Bank          05/12/2017      CHNG0005202968  Redeploying change after it was rolled back
                                                                        Added email functionality
Kgomotso Gumbo  Stuart Wilson           02/08/2018      CHG1000757460   Incorporated new 2018 logo
Kgomotso Gumbo  Libor Svoboda           14/02/2019      CHG1001362755   Extend mktable and mkvalues
'''
"""XMLReport contains functions and classes for XML-based reports.

1. Business data => XML (mk* functions and StatementReportBase class)
2. XML => XML:FO (XMLReportGenerator)
3. XML:FO => PDF (fop called by XMLReportGenerator)

"""

import os, datetime, types, csv
from string import Template
from xml.etree import ElementTree as ET
from pyPdf import PdfFileWriter, PdfFileReader  # @UnresolvedImport

import acm
import STATIC_TEMPLATE
import FReportSettings as frs

XMLREPORT_RESOURCES = {
    'img-absa-logo': os.path.join(frs.LOGOS_PATH, 'absa_logo_2018.png'),
    'img-member-of-barclays': os.path.join(frs.LOGOS_PATH, 'member-of-barclays.png'),
    'txt-absareg': STATIC_TEMPLATE.ABSA_REG
}

XMLREPORT_SCHEMA_PATH = os.path.join(frs.XSLT_PATH, 'XMLReport.xsd')


class SummaryRow(list):
    """Class representing summary row allowing user-defined attribute"""
    __slots__ = ['is_summary']

    def __init__(self, itr):
        self.is_summary = True
        super(SummaryRow, self).__init__([item for item in itr])


class SubSummaryRow(list):
    
    __slots__ = ['is_subsummary']
    
    def __init__(self, itr):
        self.is_subsummary = True
        super(SubSummaryRow, self).__init__([item for item in itr])


class XMLReportGenerator(object):
    """Class for PDF report generation from XML source."""

    def __init__(self, output_dir, xsl_fo_template_name='XMLReport'):
        self.output_dir = output_dir
        # FXSLTemplate name
        self.xsl_fo_template_name = xsl_fo_template_name

        # Value indicating whether input XML will be validated against XSD
        self.validate_xml = frs.VALIDATE_XML

        # Path to XSD
        self.xsd_path = XMLREPORT_SCHEMA_PATH

        # Custom settings for XSL template
        self.template_settings = {}

    def create(self, xml, filename, omit_resources=False):
        """Create the report and saves it to disk.

        :param xml: Xml input.
        :param filename: Output file name (without the PDF extension).
        :param omit_resources: Do not add resources section to xml:fo. Defaut is ``False``.

        """

        # Add resources
        if not omit_resources:
            xml = self._add_resources(xml)

        # Add custom template settings options
        xml = self._add_template_settings(xml)

        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

        if frs.KEEP_XML:
            with open(os.path.join(self.output_dir, filename + '.xml'), 'wb') as f:
                f.write(xml)

        # XML => XML:FO
        # chdir for XSLT dependencies
        os.chdir(frs.XSLT_PATH)
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

        # XML:FO => PDF
        final_report_path = os.path.join(self.output_dir, filename)

        command = Template(frs.FOP_BAT)
        command = command.substitute({'extension': 'pdf', 'filename': final_report_path})

        if os.system(command):
            # always keep FO file on error
            raise RuntimeError(
                "Output creation ERROR. Check that necessary third party software is installed. Command: " + command)

        if not frs.KEEP_FO:
            os.remove(xml_fo_path)

        return final_report_path + '.pdf'

    def create_merged(self, xmls, filename):
        """Create multiple reports and merge them into one."""
        nowstamp = datetime.datetime.today().strftime('%Y-%m-%d_%H%M%S')

        pdf_writer = PdfFileWriter()

        tempfiles = []
        for index, xml in enumerate(xmls):
            tempname = '{0}_{1}_{2}'.format(filename, nowstamp, str(index).rjust(2, '0'))
            tempfullname = self.create(xml, tempname)
            tempfile = open(tempfullname, "rb")

            pdf_reader = PdfFileReader(tempfile)
            # should add more than one page :P
            pdf_writer.addPage(pdf_reader.getPage(0))

            tempfiles.append(tempfile)

        merged_file_name = os.path.join(self.output_dir, filename + '.pdf')
        with file(merged_file_name, "wb") as merged_file:
            pdf_writer.write(merged_file)

        for tempfile in tempfiles:
            # pdf_writer is lazy so we have to close the files here
            tempfile.close()
            if not frs.KEEP_PARTIAL_PDF:
                os.remove(tempfile.name)

        return merged_file_name

    def set(self, key, value):
        self.template_settings[key] = value

    def _add_resources(self, xmlstring):
        xml = ET.fromstring(xmlstring)

        settings = ET.SubElement(xml, '__XMLReportResources')
        for key, value in XMLREPORT_RESOURCES.iteritems():
            ET.SubElement(settings, key).text = value

        return ET.tostring(xml)

    def _add_template_settings(self, xmlstring):
        xml = ET.fromstring(xmlstring)

        settings = ET.SubElement(xml, '__XMLReportSettings')
        for key, value in self.template_settings.iteritems():
            ET.SubElement(settings, key).text = value
        return ET.tostring(xml)


class CSVReportGenerator(object):
    """Class for Excel report generation from string source."""

    def __init__(self, output_dir):
        self.output_dir = output_dir

    def create(self, data, filename):
        """Create the report and saves it to disk.

        :param data: String input.
        :param filename: Output file name (without the PDF extension).

        """

        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

        final_report_path = os.path.join(self.output_dir, filename + '.csv')

        with open(final_report_path, 'wb') as fp:
            writer = csv.writer(fp)

            for row in data:
                writer.writerow(row)

        return final_report_path


class StatementReportBase(object):
    """Base class for statement reports."""

    def bank_address(self):
        """Return bank address."""
        return STATIC_TEMPLATE.ADDRESS_ALICELANE

    def client_address(self):
        """Return client address."""
        return None

    def statement_detail(self):
        """
        Yield XML elements which will form the core data of the report.
        """
        raise NotImplementedError("Please implement this method "
                                  "in the derived class.")

    def create_report(self):
        """Create the report XML."""
        report = ET.Element('XMLReport')

        def create_and_append(parent, element_name, subelements):
            el = ET.SubElement(parent, element_name)
            for subelement in subelements:
                el.append(subelement)

        report.append(mkcontact(self.bank_address(), "Bank"))
        report.append(mkcontact(self.client_address(), "Client"))

        create_and_append(report, 'Content', self.statement_detail())

        return ET.tostring(report)


def contact_from_pty(pty, contact_rule_cl_name=None):
    """Create contact object from FParty."""

    if 'ShortCode' not in dir(pty):
        raise Exception('Custom method "ShortCode" not available on party object!')

    result = {"name": pty.Fullname(),
              "aliasname": pty.ShortCode(),
              "address": [pty.Address(), pty.Address2(), pty.City(), pty.Country(), pty.ZipCode()],
              "tel": pty.Telephone(),
              "att": []
              }

    if result['address'][1] == result['address'][2]:  # sometimes city is in Address2 as well
        del (result['address'][2])

    if pty.Attention():
        result['att'].append({'att': pty.Attention()})

    if contact_rule_cl_name:
        for contact in pty.Contacts():
            if filter(lambda cr: cr.EventChlItem().Name() == contact_rule_cl_name, contact.ContactRules()):
                result['att'].append({'att': contact.Attention(), 'email': contact.Email(), 'fax': contact.Fax()})

    return result


def mkcaption(text):
    """Create caption block."""
    element = ET.Element('Caption')
    element.text = str(text)
    return element


# FIXME: Unused function
def mktext(text, font_size, margin_bottom):
    """Create caption block."""
    element = ET.Element('Caption')
    element.text = str(text)
    element.attrib['fontsize'] = str(font_size)
    element.attrib['marginbottom'] = str(margin_bottom)
    return element


def mkcontact(address, element_name="Contact"):
    """Create contact block."""
    contact = ET.Element(element_name)

    if address.get('name'):
        ET.SubElement(contact, 'Name').text = address['name']
    if address.get('aliasname'):
        ET.SubElement(contact, 'AliasName').text = address['aliasname']

    addr = ET.SubElement(contact, "Address")
    if address.get('address'):
        for address_line in address['address']:
            ET.SubElement(addr, "Value").text = address_line

    if address.get('tel'):
        ET.SubElement(contact, "Tel").text = address['tel']
    if address.get('fax'):
        ET.SubElement(contact, "Fax").text = address['fax']
    if address.get('email'):
        ET.SubElement(contact, "Email").text = address['email']
    if address.get('web'):
        ET.SubElement(contact, 'Web').text = address['web']
    if address.get('vat_nbr'):
        ET.SubElement(contact, 'VatRegNo').text = address['vat_nbr']
    if address.get('date'):
        ET.SubElement(contact, 'Date').text = address['date']
    # { 'att': { 'att'= 'John Doe', 'email' = 'doe@john.cc' } }
    if address.get('att'):
        for att in address.get('att'):
            el = ET.SubElement(contact, "Att")
            el.text = att['att']
            if att.get('email'):
                el.attrib['email'] = att['email']
            if att.get('fax'):
                el.attrib['fax'] = att['fax']

    return contact


def mkinfo(*args):
    """Create text block.

    Example: ``mkinfo('This is first line.', 'This is second line')``

    """
    return mkvalues(*args)


def mkkv(key, value):
    """Create key-value pair block."""
    element = ET.Element('Value')
    element.attrib['key'] = key
    element.text = str(value)
    return element


def mktable(columns, rows, size="normal", header=None, borderwidth='0.5'):
    """Create table block.

    Example:
    columns = [{ name: 'Name', width: '3cm' }, { name: 'ID' }]
    data = [['John Doe', 1], ['Mary Lynn', 2]]
    result = mktable(columns, data, size = 'small')

    """
    table_element = ET.Element('Table')
    if size:
        table_element.attrib['size'] = size
    if borderwidth:
        table_element.attrib['borderwidth'] = "{0}mm".format(borderwidth)
    if header:
        table_element.attrib['tableheader'] = header

    columns_element = ET.SubElement(table_element, 'Columns')
    for column in columns:
        column_element = ET.SubElement(columns_element, 'Column')
        column_element.text = column['name']
        if 'width' in column:
            column_element.attrib['width'] = column['width']

    rows_element = ET.SubElement(table_element, 'Rows')
    if rows:
        for row in rows:
            row_element = ET.SubElement(rows_element, 'Row')
            if hasattr(row, 'is_summary'):
                row_element.attrib['summary'] = 'true'
            for cell in row:
                cell_element = ET.SubElement(row_element, 'Cell')
                cell_element.text = str(cell)

    return table_element


def mkval(value):
    """Create Value block."""
    element = ET.Element('Value')
    element.text = str(value)
    return element


def mkpagebreak():
    """Create page break block."""
    element = ET.Element('PageBreak')
    return element


def mkvalues(*args, **kwargs):
    """Create values block.

    Example: ``mkvalues(['Name', 'John'], ['Surname', 'Doe'])``

    """
    element = ET.Element('Values')
    for key, value in kwargs.iteritems():
        element.attrib[key] = value

    for value in args:
        if isinstance(value, list) or isinstance(value, tuple):
            sub = mkkv(value[0], value[1])
        else:
            sub = mkval(value)
        element.append(sub)

    return element


def mkdisclaimer(*args):
    """Creates diclaimer block.

    """
    element = ET.Element('Disclaimer')

    for value in args:
        sub = mkval(value)
        element.append(sub)

    return element

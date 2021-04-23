"""--------------------------------------------------------------------------------------------------------------------------------------
MODULE
    EmailBodyHTMLGenerator
    
DESCRIPTION
    This module contains an object used for generating the HTML body for a
    correspondence email.

-----------------------------------------------------------------------------------------------------------------------------------------
HISTORY
=========================================================================================================================================
Date            Change no       Developer               Requester               Description
-----------------------------------------------------------------------------------------------------------------------------------------
2018-08-25                      Cuen Edwards                                    Initial version refactored out for use by all documents.
-----------------------------------------------------------------------------------------------------------------------------------------
"""

import xml.dom.minidom as minidom
import xml.etree.ElementTree as ElementTree

import DocumentGeneral


class GenerateEmailBodyHTMLRequest(object):
    """
    An object embodying the request to generate the HTML body for a
    correspondence email.
    """

    def __init__(self, from_department, from_telephone, from_email, document_description):
        """
        Constructor.
        """
        self.from_department = from_department
        self.from_telephone = from_telephone
        self.from_email = from_email
        self.document_description = document_description


class EmailBodyHTMLGenerator(object):
    """
    An object responsible for generating the HTML body for a
    correspondence email.
    """

    def generate_html(self, generate_email_body_html_request):
        """
        Generate the HTML body for a correspondence email.
        """
        html_element = self._generate_html_element(
            generate_email_body_html_request)
        xml_string = ElementTree.tostring(html_element)
        document = minidom.parseString(xml_string)
        # Return a pretty-printed version of the document without
        # the xml declaration .
        root_element = document.childNodes[0]
        return root_element.toprettyxml(indent='  ')

    def _generate_html_element(self, generate_email_body_html_request):
        """
        Generate the HTML XML element and sub-elements.
        """
        element = self._generate_element('HTML')
        element.append(self._generate_body_element(generate_email_body_html_request))
        return element

    def _generate_body_element(self, generate_email_body_html_request):
        """
        Generate the BODY XML element and sub-elements.
        """
        element = self._generate_element('BODY')
        element.append(self._generate_table_element(generate_email_body_html_request))
        return element

    def _generate_table_element(self, generate_email_body_html_request):
        """
        Generate the TABLE XML element and sub-elements.
        """
        style = "color: {font_colour};font-family: {font_family};font-weight: normal;font-size: {font_size}"
        style = style.format(
            font_colour=self._get_default_font_colour(),
            font_family=self._get_default_font_family(),
            font_size=self._get_default_font_size()
        )
        element = self._generate_element('TABLE', attributes={'style': style})
        element.append(self._generate_salutation_row_element())
        element.append(self._generate_document_message_row_element(generate_email_body_html_request))
        element.append(self._generate_contact_us_row_element())
        element.append(self._generate_contact_us_message_row_element())
        element.append(self._generate_closing_row_element())
        element.append(self._generate_from_name_row_element(generate_email_body_html_request))
        element.append(self._generate_from_telephone_row_element(generate_email_body_html_request))
        element.append(self._generate_from_email_row_element(generate_email_body_html_request))
        return element

    def _generate_salutation_row_element(self):
        """
        Generate the salutation row element.
        """
        return self._generate_table_row_element('Dear Valued Customer', bold=True, padded=True)

    def _generate_document_message_row_element(self, generate_email_body_html_request):
        """
        Generate the document message row element.
        """
        text = 'Attached is {description}.'.format(
            description=generate_email_body_html_request.document_description
        )
        return self._generate_table_row_element(text, bold=False, padded=True)

    def _generate_contact_us_row_element(self):
        """
        Generate the contact us row element.
        """
        return self._generate_table_row_element('Contact us', bold=True, padded=True)

    def _generate_contact_us_message_row_element(self):
        """
        Generate the contact us message row element.
        """
        text = 'If you have any questions or concerns related to this e-mail, please contact us.'
        return self._generate_table_row_element(text, bold=False, padded=True)

    def _generate_closing_row_element(self):
        """
        Generate the closing row element.
        """
        text = 'Yours sincerely,'
        return self._generate_table_row_element(text, bold=False, padded=True)

    def _generate_from_name_row_element(self, generate_email_body_html_request):
        """
        Generate the from name row element.
        """
        from_name = self._get_default_from_name()
        from_department = generate_email_body_html_request.from_department
        if DocumentGeneral.is_string_value_present(from_department):
            from_name += ' | {from_department}'.format(
                from_department=from_department.strip()
            )
        return self._generate_table_row_element(from_name, bold=False, padded=False)

    def _generate_from_telephone_row_element(self, generate_email_body_html_request):
        """
        Generate the from telephone row element.
        """
        from_telephone = generate_email_body_html_request.from_telephone
        return self._generate_table_row_element(from_telephone, bold=False, padded=False)

    def _generate_from_email_row_element(self, generate_email_body_html_request):
        """
        Generate the from email row element.
        """
        from_email = generate_email_body_html_request.from_email
        table_row_element = self._generate_table_row_element(None, bold=False, padded=False)
        table_dimension_element = table_row_element.find('TD')
        link_address = 'mailto:{from_email}'
        link_address = link_address.format(
            from_email=from_email
        )
        table_dimension_element.append(self._generate_hyperlink_element(link_address, from_email,
            disable_text_decoration=True))
        return table_row_element

    def _generate_table_row_element(self, text, bold=False, padded=False):
        """
        Generate a table row element with embedded table dimension.
        """
        element = self._generate_element('TR')
        style = ''
        if bold:
            style += 'font-weight: bold;'
        if padded:
            style += 'padding-bottom: 15px;'
        element.append(self._generate_table_dimension_element(text, style))
        return element

    def _generate_table_dimension_element(self, text, style):
        """
        Generate a table dimension element.
        """
        attributes = {}
        if style:
            attributes['style'] = style
        return self._generate_element('TD', text, attributes=attributes)

    def _generate_hyperlink_element(self, link_address, link_description, disable_text_decoration):
        """
        Generate a hyperlink/anchor element.
        """
        style = 'color: {font_colour};'
        style = style.format(
            font_colour=self._get_default_font_colour()
        )
        if disable_text_decoration:
            style += 'text-decoration: none;'
        attributes = {
            'style': style,
            'href': link_address
        }
        return self._generate_element('A', link_description, attributes)

    @staticmethod
    def _get_default_from_name():
        """
        Get the default email body from name.
        """
        return DocumentGeneral.get_default_email_body_from_name()

    @staticmethod
    def _get_default_font_colour():
        """
        Get the default email body font colour.
        """
        return DocumentGeneral.get_default_email_body_font_colour()

    @staticmethod
    def _get_default_font_family():
        """
        Get the default email body font family.
        """
        return DocumentGeneral.get_default_email_body_font_family()

    @staticmethod
    def _get_default_font_size():
        """
        Get the default email body font size.
        """
        return DocumentGeneral.get_default_email_body_font_size()

    @staticmethod
    def _generate_element(element_name, element_text='', attributes=None):
        """
        Generate an XML element with the specified name, text and
        attributes.
        """
        element = ElementTree.Element(element_name)
        element.text = element_text
        if attributes is not None:
            for attribute_name, attribute_value in list(attributes.items()):
                element.set(attribute_name, attribute_value)
        return element

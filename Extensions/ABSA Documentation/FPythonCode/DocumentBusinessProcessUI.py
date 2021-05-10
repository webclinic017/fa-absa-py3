"""--------------------------------------------------------------------------------------------------------------------------------------
MODULE
    DocumentBusinessProcessUI

DESCRIPTION
    This module contains UI elements used for document business processes.

-----------------------------------------------------------------------------------------------------------------------------------------
HISTORY
=========================================================================================================================================
Date            Change no       Developer               Requester               Description
-----------------------------------------------------------------------------------------------------------------------------------------
2019-09-17      FAOPS-460       Cuen Edwards            Letitia Carboni         Initial implementation.
2020-05-05      FAOPS-746       Cuen Edwards            Kgomotso Gumbo          Addition of support for Swift MT format.
-----------------------------------------------------------------------------------------------------------------------------------------
"""

import os

import acm
import FUxCore

import DocumentBusinessProcessGeneral
from DocumentGeneral import Formats


class AbstractViewFormatMenuItem(object, FUxCore.MenuItem):
    """
    Abstract menu item providing the base implementation of a menu
    item used to view some format of a document business process.
    """

    def __init__(self, extension_object, document_format):
        """
        Constructor.
        """
        self._business_processes = self._get_business_processes(extension_object)
        self._document_format = document_format

    @FUxCore.aux_cb
    def Invoke(self, eii):
        """
        Perform the action on the menu item being invoked.
        """
        self._view(self._business_processes[0], self._document_format)

    @FUxCore.aux_cb
    def Applicable(self):
        """
        Determine whether or not the menu item should be visible
        (shown at all).
        """
        if self._business_processes.Size() != 1:
            return False
        business_process = self._business_processes[0]
        if not DocumentBusinessProcessGeneral.is_document_business_process(business_process):
            return False
        document_processor = DocumentBusinessProcessGeneral.get_document_processor(business_process)
        return self._document_format in document_processor.get_supported_formats()

    @FUxCore.aux_cb
    def Enabled(self):
        """
        Determine whether or not the menu item should be enabled
        (vs greyed-out).
        """
        business_process = self._business_processes[0]
        document_processor = DocumentBusinessProcessGeneral.get_document_processor(business_process)
        return document_processor.document_format_available(business_process, self._document_format)

    @FUxCore.aux_cb
    def Checked(self):
        """
        Determine whether or not the menu item should be checked
        (have a check mark).
        """
        return False

    def _view(self, business_process, document_format):
        """
        View the document.
        """
        file_path = self._render_document_file(business_process, document_format)
        os.startfile(file_path)

    @staticmethod
    def _render_document_file(business_process, document_format):
        """
        Render the document and return the file path of the
        generated document.
        """
        document_processor = DocumentBusinessProcessGeneral.get_document_processor(business_process)
        return document_processor.render_document_file(business_process, document_format)

    @classmethod
    def _get_business_processes(cls, extension_object):
        """
        Get any businesses processes from a specified extension object.
        """
        if extension_object.IsKindOf(acm.FIndexedCollection):
            business_processes = acm.FArray()
            for item in extension_object:
                if item.IsKindOf(acm.FBusinessProcess):
                    business_processes.Add(item)
            return business_processes
        elif extension_object.IsKindOf(acm.FBackOfficeManagerFrame):
            active_sheet = extension_object.ActiveSheet()
            if active_sheet is None:
                return acm.FArray()
            selection = active_sheet.Selection()
            if selection is None:
                return acm.FArray()
            return cls._get_business_processes(selection.SelectedRowObjects())
        raise ValueError("Unsupported extension object of type '{class_name}' specified.".format(
            class_name=extension_object.ClassName()
        ))


class ViewCSVMenuItem(AbstractViewFormatMenuItem):
    """
    Menu item used to view the CSV format of a document business
    process.
    """

    def __init__(self, business_processes):
        """
        Constructor.
        """
        super(ViewCSVMenuItem, self).__init__(business_processes, Formats.CSV)


class ViewMTMenuItem(AbstractViewFormatMenuItem):
    """
    Menu item used to view the Swift MT format of a document business
    process.
    """

    def __init__(self, business_processes):
        """
        Constructor.
        """
        super(ViewMTMenuItem, self).__init__(business_processes, Formats.MT)


class ViewPDFMenuItem(AbstractViewFormatMenuItem):
    """
    Menu item used to view the PDF format of a document business
    process.
    """

    def __init__(self, business_processes):
        """
        Constructor.
        """
        super(ViewPDFMenuItem, self).__init__(business_processes, Formats.PDF)


class ViewXMLMenuItem(AbstractViewFormatMenuItem):
    """
    Menu item used to view the XML format of a document business
    process.
    """

    def __init__(self, business_processes):
        """
        Constructor.
        """
        super(ViewXMLMenuItem, self).__init__(business_processes, Formats.XML)


class ViewXLSXMenuItem(AbstractViewFormatMenuItem):
    """
    Menu item used to view the XLSX format of a document business
    process.
    """

    def __init__(self, business_processes):
        """
        Constructor.
        """
        super(ViewXLSXMenuItem, self).__init__(business_processes, Formats.XLSX)


@FUxCore.aux_cb
def create_view_csv_menu_item(extension_object):
    """
    Function used to create and return the View CSV menu item.

    This function is referenced from the 'View Document Business
    Process CSV' FMenuExtension.
    """
    return ViewCSVMenuItem(extension_object)


@FUxCore.aux_cb
def create_view_mt_menu_item(extension_object):
    """
    Function used to create and return the View MT menu item.

    This function is referenced from the 'View Document Business
    Process MT' FMenuExtension.
    """
    return ViewMTMenuItem(extension_object)


@FUxCore.aux_cb
def create_view_pdf_menu_item(extension_object):
    """
    Function used to create and return the View PDF menu item.

    This function is referenced from the 'View Document Business
    Process PDF' FMenuExtension.
    """
    return ViewPDFMenuItem(extension_object)


@FUxCore.aux_cb
def create_view_xlsx_menu_item(extension_object):
    """
    Function used to create and return the View XLSX menu item.

    This function is referenced from the 'View Document Business
    Process XLSX' FMenuExtension.
    """
    return ViewXLSXMenuItem(extension_object)


@FUxCore.aux_cb
def create_view_xml_menu_item(extension_object):
    """
    Function used to create and return the View XML menu item.

    This function is referenced from the 'View Document Business
    Process XML' FMenuExtension.
    """
    return ViewXMLMenuItem(extension_object)

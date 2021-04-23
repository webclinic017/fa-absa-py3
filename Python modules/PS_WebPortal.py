"""-----------------------------------------------------------------------------
MODULE      PS_FormUtils

Utilities for working with the Web portal (formerly SoftBroker).

History:
Date                CR Number              Who                    What

2012-11-13          620753                 Hynek Urban            Initial version.
-----------------------------------------------------------------------------"""
import acm
from collections import namedtuple
import xml.etree.ElementTree

import at_logging


LOGGER = at_logging.getLogger()

Report = namedtuple('Report',
    ['filename', 'file_type', 'description', 'unique_key'])


class DescriptorFile(object):
    """Represents the descriptor object."""

    def __init__(self):
        self.root = xml.etree.ElementTree.XML(
            '<GeneralStorageImportSchema></GeneralStorageImportSchema>')
        self.report_count = 0

    def __str__(self):
        return xml.etree.ElementTree.tostring(self.root)
        
    def add_report(self, details):
        xml.etree.ElementTree.SubElement(self.root, 'ContractNote',
            attrib=details)
        self.report_count += 1

    def write(self, filename):
        """Write to file specified by the filename."""
        with open(filename, 'w') as out:
            out.write(str(self))


def _get_portal_alias(client_name):
    """Get the WebPortal alias for the Party with the given client_name."""
    alias_query = 'party="%s" AND type="SoftBroker"' % client_name
    alias_err_msg = 'Multiple SoftBroker aliases supplied for %s.' % client_name
    alias = acm.FPartyAlias.Select01(alias_query, alias_err_msg)
    if not alias:
        raise RuntimeError('No SoftBroker alias for %s.' % client_name)
    return alias.Alias()


def generate_descriptor(date, client_name, fname_out, reports):
    """
    Generate the WebPortal descriptor file.
    
    <date> - date in the YYYY-MM-DD format
    <client_name> - ID of a Party
    <fname_out> - name of the output file
    <reports> - container with elements of type Report

    """
    LOGGER.info('Starting Softbroker Descriptor Generation:::')
    df = DescriptorFile()
    for report in reports:
        LOGGER.info("Processing %s", report.filename)
        details = {
            'Date': date,
            'AcctID': _get_portal_alias(client_name),
            'FileType': report.file_type,
            'Description': report.description,
            'Filename': report.filename,
            'UniqueKey': report.unique_key,
        }
        df.add_report(details)
        
    if df.report_count > 0:
        df.write(fname_out)
        LOGGER.info('Wrote secondary output to: %s', fname_out)

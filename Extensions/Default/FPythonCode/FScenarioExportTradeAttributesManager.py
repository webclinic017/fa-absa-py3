""" Compiled: 2020-09-18 10:38:54 """

#__src_file__ = "extensions/risk_export/./etc/FScenarioExportTradeAttributesManager.py"
from xml.etree import cElementTree
from FScenarioExportXMLUtils import *
from FScenarioExportContentManager import ScenarioExportContentManager


TRADE_ATTRIBUTE_SHEET_NAME = "tradeattributes"
EMPTY_TOKEN = ""
ENDLINE_TOKEN = "\n"


class ScenarioExportTradeAttributesManager(ScenarioExportContentManager):
    def __init__(self, report_xml):
        super(ScenarioExportTradeAttributesManager, self).__init__()
        self.trd_attr_report = self._get_inner_report(
            self._etree_from_string(report_xml))
        self.rows_per_trade = self._get_rows(self.trd_attr_report)

    def _etree_from_string(self, xml_string):
        """Get a python representation of the xml string."""
        return cElementTree.fromstring(xml_string)

    def _sheet_is_trd_attr_sheet(self, report_name_string):
        """Tests if the report is named according to the name standard."""
        if report_name_string.lower().endswith(TRADE_ATTRIBUTE_SHEET_NAME):
            return True
        else:
            return False

    def _prime_report_has_trade_attributes(self, preport):
        rname = preport.find(NAME)
        if rname is not None:
            rname = rname.text
            return self._sheet_is_trd_attr_sheet(rname)

    def _get_inner_report(self, report_etree):
        """Get the Trade Attributes report."""
        if report_etree.tag == PRIME_REPORT and \
            self._prime_report_has_trade_attributes(report_etree):
            return report_etree
        for preport in report_etree.findall(PRIME_REPORT):
            if self._prime_report_has_trade_attributes(preport):
                return preport
        raise Exception("No trade sheet named '%s' in report xml" % \
            TRADE_ATTRIBUTE_SHEET_NAME)

    def _encode(self, text):
        try:
            etext = text.encode("latin-1")
        except:
            return text
        return etext

    def _process_row(self, row_element):
        """
        Creates a string of a row bundle where the rows for the
        different reports are laid out sequentially.
        """
        values = []
        for cell in row_element.findall(mkpath(CELLS, CELL)):
            ddata = cell.find(DEFAULT_DATA)
            rdata = cell.find(RAW_DATA)
            data = cell.find(FORMATTED_DATA)
            if rdata is not None and rdata.text:
                values.append(self._encode(rdata.text))
            elif ddata is not None and ddata.text:
                values.append(self._encode(ddata.text))
            elif data is not None and data.text:
                dtext = self._encode(data.text)
                # Formatted data contains a non-ascii character
                dtext = dtext.replace("\xa0", "")
                values.append(dtext)
            else:
                values.append(EMPTY_TOKEN)
        return values

    def _get_trdnbr_from_row(self, row_el):
        trdnbr_el = row_el.find(LABEL)
        if trdnbr_el is not None:
            return str(trdnbr_el.text)
        else:
            return None

    def _get_rows(self, prime_report_etree):
        """Returns all rows with a trade number in a prime report."""
        return dict([(self._get_trdnbr_from_row(row_el), row_el)\
                     for row_el in prime_report_etree.findall(
                        mkpath(REPORT_CONTENTS, TABLE, ROWS, ROW))])

    def _get_columns(self, prime_report_etree):
        """Returns all column in a prime report."""
        return prime_report_etree.findall(
            mkpath(REPORT_CONTENTS, TABLE, COLUMNS, COLUMN))

    def _process_column_labels(self, report_component):
        """
        Creates a string of the column labels for the different
        reports, laid out sequentially.
        """
        values = []
        for col in self._get_columns(report_component):
            col_label = col.find(LABEL)
            if col_label.text == 'Cpty':
                values.append('Counterparty')
            elif col_label is not None:
                values.append(col_label.text)
            else:
                values.append(EMPTY_TOKEN)
        return values

    def get_trades(self):
        """Get a list of all all trades connected with the report rows."""
        return list(self.rows_per_trade.keys())

    def column_headers(self):
        """Generates a list of column labels."""
        return self._process_column_labels(self.trd_attr_report)

    def generate_header(self):
        raise NotImplementedError("FIXME")

    def get_content(self,
        trdnbr,
        space_collection  # not used
        ):
        """Returns the content per trade."""
        return self._process_row(self.rows_per_trade[trdnbr])

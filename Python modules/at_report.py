"""
at_report

Modul containing helper classes and functions for generating reports from
Front Arena.

"""

import acm
import ael
import csv
import os


class ReportCreator(object):
    """Base class for reports."""

    def __init__(self, file_name, file_suffix, path):
        """Class constructor. Init all private and public properties."""

        # content -- string; Final representation of the report in
        # target format.
        self.content = ""
        self.date = acm.Time.DateToday()
        self.file_name = file_name
        self.file_suffix = file_suffix
        self.path = path
        self._full_path = None

    def _collect_data(self):
        """Collect data for the report.

        Every report should implement it's data collection. All data needed
        for the report should be loaded here.

        """

        raise NotImplementedError("Subclasses should implement this!")

    def create_report(self):
        """Create the report.

        Call all methods in correct order to create the report.

        """

        self._prepare()
        self._collect_data()
        self._create_report()
        self._write_content_to_file()

    def _create_report(self):
        """Processing of collected data.

        Every inherited report type sub class should implement it's own,
        if needed.

        """

    @staticmethod
    def _get_data_from_db(sql_query):
        """Returns result set of SQL query from the SQL server.

        Returns list of lists.

        """

        return ael.dbsql(sql_query)[0]

    @staticmethod
    def _create_folder_if_needed(folder_full_path):
        """Checks if specified folder exists. If not try to create it."""

        if not os.path.exists(folder_full_path):
            os.makedirs(folder_full_path)

    def _get_full_path(self):
        """Form full path to the file.

        Returns string.

        """

        full_path = os.path.join(self.path,
            self.file_name + '.' + self.file_suffix)

        return full_path

    def _prepare(self):
        """Process all pre-data collection activities.

        No return value.

        """

        self._full_path = self._get_full_path()
        self._create_folder_if_needed(self.path)

    def _write_content_to_file(self):
        """Writes the report content to file."""

        with open(self._full_path, 'wb') as out_file:
            out_file.write(self.content)


class DataToXMLReportCreator(ReportCreator):
    """ XML transformation based reports.

    Represents reports, where data are first collected into collections of
    light-weight objects, those are then used to generate XML, which is
    transformated into target format using the XSL transformation.

    """

    def __init__(self, file_name, file_suffix, path, xsl_template):
        """Initialise report creator."""
        super(DataToXMLReportCreator, self).__init__(file_name, file_suffix,
            path)
        self.xsl_template = xsl_template

    def _create_report(self):
        """Creates the report.

        1) create XML from collected light-weight object,
           or dirctly generate XML inside _generate_xml().
        2) transform XML using XSL template,

        """

        content_xml = self._generate_xml()
        self.content = self._transform(self.xsl_template, content_xml)

    def _generate_xml(self):
        """Form XML representation of collected data.

        Return value: Serialized (string) XML representation of the data.

        """

        raise NotImplementedError("Subclasses should implement this!")

    @staticmethod
    def _transform(xsl_template, xml_data):
        """Transforms XML data to target format using given XSL template.

        Return value: Report in target format string

        """

        transformer = acm.CreateWithParameter(
            'FXSLTTransform', xsl_template.Value())

        return transformer.Transform(xml_data)


class CSVReportCreator(ReportCreator):
    """Base class for all csv sub types."""

    def __init__(self, file_name, file_suffix, path,
            csv_writer_parameters=None):
        """Constructor

        self.csv_writer_parameters is a dictionary for csv writer parameters.

        """

        super(CSVReportCreator, self).__init__(file_name, file_suffix, path)

        self.content = []

        if csv_writer_parameters:
            self.csv_writer_parameters = csv_writer_parameters
        else:
            self.csv_writer_parameters = {'delimiter': ',', 'quotechar': '"',
                'quoting': csv.QUOTE_NONNUMERIC}

    def _collect_data(self):
        """Every report should implement it's data collection.

        The results must be put in self.content as a list of lists of values.

        """

        raise NotImplementedError("Subclasses should implement this!")

    def _banner(self):
        """Banner of the report.

        Implement this method in subclasses if banner is required.
        Note: Banner can result in invalid CSV file.

        """
        return None

    def _header(self):
        """Gets data column names as list."""

        raise NotImplementedError("Subclasses should implement this!")

    def _write_content_to_file(self):
        """Writes the report represented as list of lists to file."""

        with open(self._full_path, 'wb') as csv_file:
            csv_writer = csv.writer(
                csv_file, **self.csv_writer_parameters)

            banner = self._banner()
            if banner:
                csv_writer.writerows(banner)

            header = self._header()
            if header:
                csv_writer.writerow(header)
            csv_writer.writerows(self.content)


def return_value_if_exists(current_object, *property_chain):
    """Return value if it is possible.

    Returns value of current_object if that exist. Additionally if
    property_chain is given returns value of last existing element
    in the chain. If it is not possible to return requested value
    returns None.

    Example:
    return_value_if_exists(trade, 'Instrument', 'Underlying', 'Name')

    """

    if current_object is None:
        return None

    for property in property_chain:
        if hasattr(current_object, property):
            current_object = getattr(current_object, property)()
        else:
            return None

    return current_object


def remove_compound_rows(_report, parameter, xml_string):
    """
    Remove all compound rows
    (i.e. all but the ones which are 'leaf node rows')
    from the provided XML report
    and return the serialized string representation
    of the modified XML.

    Optionally, add the first column's label
    as the value supplied in 'parameter'.

    _report     Instance of FReportAPIBase.FReportBuilder.
    parameter   String from the field called 'Parameter'
                in the FWorksheetReport's Processing tab.
    xml_string  String with xml content to be updated.
    """
    import xml.etree.cElementTree as ET

    root = ET.fromstring(xml_string)
    table = root.find(".//Table")
    rows = table.find("./Rows")

    new_rows = ET.Element("Rows")
    number_of_all_rows = 0
    number_of_matching_rows = 0
    for row in rows.getiterator("Row"):
        number_of_all_rows += 1
        if row.find("./Rows/Row") is None:
            # If the current row does not have any 'sub-rows',
            # it means that it is a 'leaf node row'
            # and we put it into the final XML.
            new_rows.append(row)
            number_of_matching_rows += 1

    table.remove(rows)
    if number_of_all_rows == 1 and number_of_matching_rows == 1:
        # The report consists of just the first compound row and nothing else.
        # It was a business requirement not to display any rows in such a case.
        empty_rows = ET.Element("Rows")
        table.append(empty_rows)
    else:
        table.append(new_rows)

    if parameter:
        column = ET.Element("Column")
        label = ET.SubElement(column, "Label")
        label.text = parameter
        columns = root.find(".//Table/Columns")
        columns.insert(0, column)

    output = ET.tostring(root, "ISO-8859-1")

    return output

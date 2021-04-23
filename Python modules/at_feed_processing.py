"""
The AT Feed processing framework.

Contains classes for easy implementation of the following workflow:
    1) Loading of input data, be it file(s) or other sources.
    2) Processing the inputs with specific business logic.
    3) Generating outputs.

HISTORY
===============================================================================
Date        CR number   Developer       Description
-------------------------------------------------------------------------------
2014-04-15  1887623     Jakub Tomaga    SimpleXLSFeedProcessor added
2014-05-22  1979991     Peter Fabian    _log changed to staticmethod
2014-06-20  2040818     Peter Basista   Fixed a typo and replaced simple
                                        truth value checks with checks
                                        against None in two cases.
2014-12-02  2472033     Peter Basista   Move some imports into functions,
                                        PEP 8: consistency: always use
                                        double quotes.
-------------------------------------------------------------------------------

"""

import acm
import FBDPCommon
from at_ael_variables import AelVariableProvider


class EmailNotifier(object):

    """A notifier which sends an email with the accumulated errors."""

    def __init__(self, *email_recipients):
        """Initialize with the recipients' email addresses."""
        self._email_recipients = email_recipients

    def _generate_subject(self):
        ads_address = acm.ADSAddress()
        subject = "[{server_id}] Feed processing error."
        return subject.format(server_id=ads_address)

    def _generate_body(self, errors):
        return "\n".join(str(error) for error in errors)

    def __call__(self, errors):
        """This is the hook which FeedProcessor calls.

        Composes the email message and sends it to the defined recipients.

        """

        # Send email notification if addresses were set up.
        if self._email_recipients:
            for email in self._email_recipients:
                FBDPCommon.sendMail(email, self._generate_subject(),
                                    self._generate_body(errors))


def notify_log(errors):
    """A basic notifier which prints out all errors to the log."""
    print "\nERROR SUMMARY\n"
    for error in errors:
        print error


class FeedProcessor(AelVariableProvider):

    """ A basic framework for Front Arena feed processing."""

    class FeedProcessingException(Exception):

        """General feed processing exception.

        Raise this if the processing failed and you expect an error to be
        reported back to the user.

        """

    @classmethod
    def _populate_ael_variables(cls, variables, defaults):
        super(FeedProcessor, cls)._populate_ael_variables(variables, defaults)
        variables.add("dry_run",
                      label="Dry run",
                      cls="bool",
                      collection=(True, False),
                      default=defaults.pop("dry_run", True))

    @staticmethod
    def _log(message):
        """Basic console logging with timestamp prefix."""
        print "{0}: {1}".format(acm.Time.TimeNow(), message)

    def __init__(self):
        self.errors = []
        self._error_notifiers = []

    def _load(self):
        """Load any subclass-specific inputs and process them."""

    def _process(self, dry_run):
        """The main worker method working with acm/ael.

        dry_run -- if this is false, the overriden method should not make any
        changes in the database.

        """
        raise NotImplementedError("Must be implemented in subclasses.")

    def _finish(self):
        """Any postprocessing like file dumping should be done here."""

    def _dispose(self):
        """Dispose of all open resources here.

        This is guaranteed to run during process().

        """

    def process(self, dry_run):
        """Process the currently opened feed while optionally
        perform the dry run only.
        """
        try:
            self._log("Loading inputs")
            self._load()
            self._log("Processing")
            self._process(dry_run)
            self._log("Finishing")
            self._finish()
        except self.FeedProcessingException as ex:
            self.errors.append(ex)
        finally:
            # This gets called even if a different exception than
            # FeedProcessingException is raised and thus the disposal is
            # guaranteed.
            self._log("Cleaning up")
            self._dispose()

            if self.errors:
                for handler in self._error_notifiers:
                    handler(self.errors)

    def add_error_notifier(self, error_notifier):
        """Add a callable which will be used to notify about the errors."""
        self._error_notifiers.append(error_notifier)


class RecordsFeedProcessor(FeedProcessor):

    """A processor which handles a single file input with multiple records.

    This provides interface for subclasses which then handle specific
    file formats and business behavior. Please see SimpleCSVFeedProcessor
    for an example.

    """

    _file_open_mode = "rb"

    @classmethod
    def _populate_ael_variables(cls, variables, defaults):
        """Populates the provided AelVariableHandler with variables.

        Subclasses can override with other variables, but must call
        this method as well.

        """
        super(RecordsFeedProcessor, cls)._populate_ael_variables(variables,
                                                                 defaults)
        variables.add("file_dir",
                      label="File directory",
                      default=defaults.pop("file_dir", "C:/"))
        variables.add("file_name",
                      label="File name",
                      default=defaults.pop("file_name", "temp.txt"))

    class RecordProcessingException(FeedProcessor.FeedProcessingException):

        """The basic record processing exception for expected errors.

        Raise this in the subclasses if you hit an expected error which
        should not stop the processing of the file. FeedProcessor will
        catch and accumulate these and after the file is processed,
        the errors will get processed by _error_notifiers.

        """

    def __init__(self, file_path, do_logging=True):
        super(RecordsFeedProcessor, self).__init__()
        self._file_path = file_path
        self._file_handle = None
        self.do_logging = do_logging

        import os
        if not os.path.exists(self._file_path):
            message = "The input file '{0}' is not accessible.".format(
                self._file_path)
            raise self.FeedProcessingException(message)

    def _load(self):
        """Open the file handle.

        Don't replace self._file_handle unless you close it first.
        If you need to have the input adjusted (encoding etc.), use self._data.

        """

        self._file_handle = open(self._file_path, self._file_open_mode)
        self._data = self._file_handle

    def _dispose(self):
        """Close the file handle.

        This is guaranteed to run if anything fails in the processing.

        """

        if self._file_handle:
            self._file_handle.close()

    def _process(self, dry_run):
        """The main worker method for file processing.

        Processes the file record by record.

        """
        self._log("Processing " + self._file_path)

        for record in self._generate_records():
            try:
                self._process_record(record, dry_run)
            except self.RecordProcessingException as ex:
                self._log(ex)
                self.errors.append(ex)

    def _generate_records(self):
        """Generator of records.

        This must be implemented by subclasses and must return a generator
        providing the individual records.

        """

        raise NotImplementedError("Subclass must implement this method")

    def _process_record(self, record, dry_run):
        """Process a single record.

        This is called on every record returned by _generate_records.
        Subclasses must implement this. If an expected error happens
        here, raise a RecordProcessingException which will be caught
        and processed automatically in the _process() method.

        The dry_run parameter indicates if any changes are to be made.

        """

        raise NotImplementedError("Subclasses must implement this method")


class SimpleCSVFeedProcessor(RecordsFeedProcessor):

    """A simple processor for reading a CSV file with a header row.

    This uses a DictReader to process the file. Subclasses must set up
    the _required_columns class field.

    """

    _required_columns = []
    _dict_reader_kwargs = {}

    def _log_line(self, index, message):
        """Log a message with the csv line number."""
        super(SimpleCSVFeedProcessor, self)._log("CSV line {0}: {1}".format(
            index, message))

    def _generate_records(self):
        """Generates tuples (index, record).

        index is the csv line number (counting only data lines
        and starting from 1).
        record is a dict with the current record

        """
        from csv import DictReader
        reader = DictReader(self._data, **self._dict_reader_kwargs)

        missing_columns = []
        for column in self._required_columns:
            if not column in reader.fieldnames:
                missing_columns.append(column)

        if missing_columns:
            message = "Missing requried columns: {0}"
            raise self.FeedProcessingException(message.format(missing_columns))
        for record in reader:
            index = int(reader.line_num)
            if self.do_logging:
                self._log("CSV line {0}".format(index))
            yield (index, record)


class ValidatingProcessor(object):

    """A processor for reading and validating a CSV/XLSX file with a header row.

    This extension allows simple type validation of the file data per column.
    Additionally, it can construct complex data objects, e.g. FInstrument
    or FPortfolio.
    """

    # A dictionary of columns (keys) required to be present in the file header,
    # mapped to validation parameters. A validation parameter is a dict containing
    # a 'validator' function and 'replace' flag.
    _validation_parameters = {}

    def _validate_record(self, index, record):
        valid = True
        for column, param in self._validation_parameters.iteritems():
            validator = param["validator"]
            if validator:
                # Trying to validate a single field
                try:
                    value = validator(record[column])
                except Exception as exc:
                    err_msg = ("Validation error on line {0}, column {1}: "
                               "'{2}'").format(index, column, exc)
                    self._log(err_msg)
                    self.errors.append(err_msg)
                    valid = False
                    continue

                # If 'replace' is set to true, replacing the value in
                # the record with the value provided by the validator
                #  (e.g. an instance of acm.FInstrument)
                if param["replace"]:
                    record[column] = value
        if valid:
            return index, record


class ValidatingCSVFeedProcessor(SimpleCSVFeedProcessor, ValidatingProcessor):

    def _generate_records(self):
        """Extends the parent method by adding validation"""

        self._required_columns = self._validation_parameters.keys()
        for index, record in super(ValidatingCSVFeedProcessor,
                                   self)._generate_records():
            validated_record = self._validate_record(index, record)
            if validated_record:
                yield validated_record


class SimpleXLSFeedProcessor(RecordsFeedProcessor):

    """A simple processor for reading an XLS file with a header row.

    This uses xlrd to process the file. Subclasses must set up
    the _required_columns class field.

    """

    _required_columns = []

    def __init__(self, file_path, sheet_index, sheet_name):
        """Initialise sheet sources.

        Exactly one source should be used. Either sheet index or sheet name.

        """
        super(SimpleXLSFeedProcessor, self).__init__(file_path)
        self.sheet_index = sheet_index
        self.sheet_name = sheet_name

        # Check if only exactly one source is available (not XOR)
        if not bool(self.sheet_index is None) ^ bool(self.sheet_name is None):
            message = "Exactly one source must be specified (name or index)."
            raise self.FeedProcessingException(message)

    def _log_line(self, index, message):
        """Log a message with the XLS line number."""
        self._log("XLS line {0}: {1}".format(index, message))

    def _get_data(self):
        """Return worksheet content."""
        import xlrd
        workbook = xlrd.open_workbook(file_contents=self._data.read())
        if not self.sheet_index is None:
            try:
                worksheet = workbook.sheet_by_index(int(self.sheet_index))
            except IndexError:
                message = "Input file doesn't contain sheet with index {0}."
                raise self.FeedProcessingException(
                    message.format(self.sheet_index))
        elif not self.sheet_name is None:
            try:
                worksheet = workbook.sheet_by_name(self.sheet_name)
            except xlrd.XLRDError:
                message = "Input file doesn't contain sheet with name {0}."
                raise self.FeedProcessingException(
                    message.format(self.sheet_name))
        else:
            message = "No source sheet. Use sheet index or sheet name."
            raise self.FeedProcessingException(message)

        return worksheet

    def _generate_records(self):
        """Generates tuples (index, record).

        index is the XLS line number (counting only data lines
        and starting from 1).
        record is a dict with the current record

        """

        # Get source data
        worksheet = self._get_data()
        columns = []
        for col in xrange(worksheet.ncols):
            columns.append(worksheet.cell_value(0, col).encode("utf-8"))

        # Verify availability of all required columns in the input file
        missing_columns = []
        for column in self._required_columns:
            if not column in columns:
                missing_columns.append(column)

        if missing_columns:
            message = "Missing required columns: {0}"
            raise self.FeedProcessingException(message.format(missing_columns))

        # Generate individual records
        for row in xrange(1, worksheet.nrows):
            index = row
            self._log("XLS line {0}".format(index))

            values = []
            for col in xrange(worksheet.ncols):
                values.append(worksheet.cell_value(row, col))
            record = dict(list(zip(columns, values)))
            yield (index, record)


class ValidatingXLSFeedProcessor(SimpleXLSFeedProcessor, ValidatingProcessor):

    def _generate_records(self):
        """Extends the parent method by adding validation"""

        self._required_columns = self._validation_parameters.keys()
        for index, record in super(ValidatingXLSFeedProcessor,
                                   self)._generate_records():
             validated_record =  self._validate_record(index, record)
             if validated_record:
                 yield validated_record

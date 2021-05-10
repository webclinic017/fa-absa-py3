""" Compiled: 2020-09-18 10:38:54 """

#__src_file__ = "extensions/risk_export/./etc/FScenarioExportContentManager.py"
import exceptions
import math


import FLogger


logger = FLogger.FLogger.GetLogger('FAReporting')


class ContentError(exceptions.Exception):
    pass


class ScenarioExportContentManager(object):
    def __init__(self):
        self.writers = []
        self.current_line = []

    def register_writer(self, writer):
        self.writers.append(writer)

    def write_output(self, output):
        for writer in self.writers:
            writer.Write(output)

    def add_output(self, content_list):
        self.current_line.extend(content_list)

    def flush_output(self, delimiter, is_first=False):
        if not is_first:
            self.write_output(delimiter)
        self.write_output(
            delimiter.join(self.current_line))
        self.current_line = []

    def clear_output(self):
        self.current_line = []

    def write_newlines(self):
        self.write_output("\n")

    def column_headers(self):
        raise NotImplementedError("Abstract base class, use sub class")

    def measure_name(self):
        return None

    def measure_group_name(self):
        return None

    def measure_count(self):
        return None

    def measure_group_header(self):
        return []

    def dimension_defaults_header(self):
        return None

    def column_grouping_header(self):
        return []

    def get_content(self, trdnbr, space_collection):
        raise NotImplementedError("Abstract base class, use sub class")


class ScenarioExportCalculatedContentManager(ScenarioExportContentManager):

    def __init__(self):
        super(ScenarioExportCalculatedContentManager, self).__init__()

    def measure_name(self):
        raise NotImplementedError("Abstract base class, use sub class")

    def measure_group_name(self):
        raise NotImplementedError("Abstract base class, use sub class")

    def measure_header(self):
        raise NotImplementedError("Abstract base class, use sub class")

    def measure_count(self):
        raise NotImplementedError("Abstract base class, use sub class")

    def dimension_defaults(self):
        raise NotImplementedError("Abstract base class, use sub class")

    def measure_group_header(self):
        return [self.measure_group_name(), str(self.measure_count())]

    def dimension_defaults_header(self):
        return self.dimension_defaults()

    def column_grouping_header(self):
        if not self.measure_header():
            return None
        values = []
        values.append(self.measure_name())
        values.append(str(self.measure_count()))
        values.extend(self.measure_header())
        return values

    def _content_values_template(self):
        return []

    def _validate_value(self, value):
        try:
            if (isinstance(value, float) and
                not math.isnan(value) and
                not math.isinf(value)):
                return True
            else:
                raise ContentError("Non-valid float: %s" % str(value))
        except Exception as msg:
            raise ContentError(msg)

    def _validate_calculated_values(self, values, trdnbr):
        for value in values:
            if not self._validate_value(value):
                return False
        return True

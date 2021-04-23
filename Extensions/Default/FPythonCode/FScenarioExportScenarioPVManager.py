""" Compiled: 2020-09-18 10:38:54 """

#__src_file__ = "extensions/risk_export/./etc/FScenarioExportScenarioPVManager.py"
import itertools
import acm
from FScenarioExportContentManager import (
        ScenarioExportCalculatedContentManager)
from FScenarioExportContentManager import ContentError
from FScenarioExportUtils import (STD_CALC_PARAM_DISPLAY_CURR,
        risk_factor_type_labels_map)


import FLogger


logger = FLogger.FLogger.GetLogger('FAReporting')


zero_dv = acm.GetFunction("denominatedvalue", 1)(0.0)
cast_double = acm.GetFunction("double", 1)
cast_string = acm.GetFunction("string", 1)
array_raw = acm.GetFunction("arrayRaw", 1)
differential = acm.GetFunction("differential", 4)


DISPLAY_TYPE_ABSOLUTE = "Absolute"
DISPLAY_TYPE_RELATIVE = "Relative"


class ScenarioExportScenarioPVManager(ScenarioExportCalculatedContentManager):

    MEASURE_NAME = "VaR PV Change"
    MEASURE_GROUP_NAME = "VaR"
    MEASURE_HEADER = ["Group", "Scenario Date"]
    DIMENSION_DEFAULTS = None

    def __init__(self, report_currency, file_path, delimiter,
        risk_factor_types, display_type):
        super(ScenarioExportScenarioPVManager, self).__init__()
        self.risk_factor_types = risk_factor_types
        self.report_currency = report_currency
        self.file_path = file_path
        self.display_type = display_type
        self.spec_header = \
            acm.GetFunction("mappedRiskFactorSpecHeader", 0)().Parameter()
        self.file_data_object = self._get_file_data_object(
            self.file_path, self.spec_header)
        self.start, self.end, self.count = self._get_scenario_range(
            self.file_data_object)
        self.delimiter = delimiter
        logger.DLOG("""Creating Scenario Content with
            measure group: %s
            measure name: %s
            risk factors: %s
            scenario file_path: %s
            column start: %s
            column end: %s""",
            self.measure_group_name(), self.measure_name(),
            self.risk_factor_types,
            self.file_path, self.start, self.end)

        self.val_parameters = \
            acm.GetFunction("mappedValuationParameters", 0)().Parameter()
        self.builder = acm.GetFunction(
            "createRiskFactorScenarioBuilder", 2)(
                self.spec_header, self.val_parameters)
        self.valuation_date = acm.Time().DateToday()
        self.scenarios = dict(((rftype, self._create_scenario(rftype))\
            for rftype in self.risk_factor_types))

    def _create_scenario(self, risk_factor_type):
        return self.builder.CreateScenario(self.file_path, -1,
            - 1, risk_factor_type, self.valuation_date)

    def _get_file_data_object(self, file_path, spec_header):
        """
        Returns a FVarFileData instance that can be used to query the
        scenario about columns and other info.
        """
        logger.DLOG("Creating FVaRFileData object from file '%s'", file_path)
        return acm.Risk().CreateScenarioFileData(file_path,
                spec_header.DelimiterChar(), spec_header.CommentChar())

    def _get_scenario_range(self, file_data_object):
        """Return the actual start and end indices for the scenario."""
        start = 0
        end = self.file_data_object.ColumnCount() - 1
        count = end - (start - 1)
        return start, end, count

    def _generate_scenario_labels(self, start, end):
        return [str(label_sym)
                for label_sym in self.file_data_object.Labels()[start:end + 1]]

    def get_scenario_count(self):
        """Returns the numbers of scenarios for this instance."""
        return self.count

    def _column_headers_core(self, start, end):
        labels = []
        labels.append(self.MEASURE_NAME)
        for scenario_label in self._generate_scenario_labels(start, end):
            for risk_factor_type in self.risk_factor_types:
                if risk_factor_type in risk_factor_type_labels_map:
                    risk_factor_type = \
                        risk_factor_type_labels_map[risk_factor_type]
                labels.append(self.delimiter.join(
                    [risk_factor_type.upper(),
                     scenario_label]))
            if len(self.risk_factor_types) > 1:
                labels.append(self.delimiter.join(["RESIDUAL",
                        scenario_label]))
        return labels

    def column_headers(self):
        return self._column_headers_core(self.start, self.end)

    def measure_name(self):
        return self.MEASURE_NAME

    def measure_group_name(self):
        return self.MEASURE_GROUP_NAME

    def dimension_defaults(self):
        return self.DIMENSION_DEFAULTS

    def measure_header(self):
        return [self.delimiter.join(self.MEASURE_HEADER)]

    def measure_count(self):
        if len(self.risk_factor_types) > 1:
            return self.count * (len(self.risk_factor_types) + 1)
        else:
            return self.count * len(self.risk_factor_types)

    def _content_values_template(self):
        return [""]

    def _cast_values_to_string(self, values, trdnbr):
        """
        Cast a collection of denominated values to a collection
        of string representations of their float-components.
        """
        is_single_value = False
        dbl_array = cast_double(values)
        try:
            iter(dbl_array)
            if len(dbl_array) == 1:
                is_single_value = True
        except TypeError:
            is_single_value = True
            dbl_array = [dbl_array]
        self._validate_calculated_values(dbl_array, trdnbr)
        if is_single_value:
            return [cast_string(array_raw(dbl_array))]
        else:
            return cast_string(array_raw(dbl_array))

    def get_content(self, trdnbr, space_collection):
        values = self._content_values_template()
        trd = acm.FTrade[trdnbr]
        _scenario_count = self.get_scenario_count()
        values_per_factor_group = []
        curr_settings = {
                STD_CALC_PARAM_DISPLAY_CURR: self.report_currency}
        if DISPLAY_TYPE_RELATIVE == self.display_type:
            try:
                base_value = trd.Calculation().TheoreticalValueParams(
                        space_collection, curr_settings)
                residual = [zero_dv] * self.count
                total = acm.FArray()
                summary = None
                for risk_factor_type in self.risk_factor_types:
                    if not self.scenarios[risk_factor_type]:
                        val = [zero_dv] * self.count
                        if risk_factor_type != "None":
                            total = self.add_to_total(total, val)
                    else:
                        val = differential(
                                trd.Calculation().TheoreticalValueParams(
                                    space_collection, curr_settings,
                                    self.scenarios[risk_factor_type]),
                                base_value, 1.0, 1.0)
                        if risk_factor_type != "None":
                            total = self.add_to_total(total, val)
                        else:
                            summary = val
                    values_per_factor_group.append(self._cast_values_to_string(
                        val, trdnbr))
                if not summary:
                    summary = differential(
                                trd.Calculation().TheoreticalValueParams(
                                    space_collection, curr_settings,
                                    self._create_scenario("None")),
                                    base_value, 1.0, 1.0)
                residual = self.subtract_from_total(summary, total)
                # Residual
                if residual:
                    values_per_factor_group.append(self._cast_values_to_string(
                        residual, trdnbr))
            except Exception as msg:
                raise ContentError(msg)
        else:
            try:
                total = acm.FArray()
                summary = None
                for risk_factor_type in self.risk_factor_types:
                    if not self.scenarios[risk_factor_type]:
                        base_value = trd.Calculation().TheoreticalValueParams(
                                space_collection, curr_settings)
                        val = [base_value] * self.count
                        if risk_factor_type != "None":
                            total = self.add_to_total(total, val)
                    else:
                        val = trd.Calculation().TheoreticalValueParams(
                                space_collection, curr_settings,
                                self.scenarios[risk_factor_type])
                        if risk_factor_type != "None":
                            total = self.add_to_total(total, val.AsList())
                        else:
                            summary = val
                    values_per_factor_group.append(self._cast_values_to_string(
                        val, trdnbr))
                if not summary:
                    summary = trd.Calculation().TheoreticalValueParams(
                                    space_collection, curr_settings,
                                    self._create_scenario("None"))
                residual = self.subtract_from_total(summary, total)
                # Residual
                if residual:
                    values_per_factor_group.append(self._cast_values_to_string(
                        residual, trdnbr))
            except Exception as msg:
                raise ContentError(msg)
        return _assemble_values(values, values_per_factor_group)

    def add_to_total(self, totals, values):
        if totals.Size() == 0:
            for index in range(0, self.count):
                value = values[index]
                if type(value) == type(zero_dv):
                    totals.AtInsert(index, value.Number())
                else:
                    totals.AtInsert(index, value)
        else:
            for index in range(0, self.count):
                value = values[index]
                if type(value) == type(zero_dv):
                    totals[index] += value.Number()
                else:
                    totals[index] += value

        return totals

    def subtract_from_total(self, FAtotals, sigma):
        try:
            residuals = acm.FArray()
            for index in range(0, self.count):
                residuals.AtInsert(index,
                        FAtotals[index].Number() - sigma[index])
            return residuals
        except Exception:
            return None


def _assemble_values(init_values, values_per_factor_group):
    """
    'unreadable' but done for performance reasons
    [
      ["2", "4", "3", ...], # Total scenario results
      ["6", "7", "9", ...]  # IR scenario results
    ] --> ["2", "6", "4", "7", ...]
    """
    return itertools.chain(init_values,
        itertools.chain(
            *zip(
                *values_per_factor_group)))

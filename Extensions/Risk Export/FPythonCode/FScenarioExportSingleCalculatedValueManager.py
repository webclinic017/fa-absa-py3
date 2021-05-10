""" Compiled: 2020-09-18 10:38:54 """

#__src_file__ = "extensions/risk_export/./etc/FScenarioExportSingleCalculatedValueManager.py"
import acm


from FScenarioExportContentManager import (
        ScenarioExportCalculatedContentManager)
from FScenarioExportContentManager import ContentError


import FLogger


logger = FLogger.FLogger.GetLogger('FAReporting')


STANDARD_CALC_POSTFIX = "Params"


class ScenarioExportSingleCalculatedValueManager(
    ScenarioExportCalculatedContentManager):
    def __init__(self, measure_name, measure_group_name, measure_header,
        delimiter, standard_calc_name, parameter_dictionary,
        measure_label=None):
        super(ScenarioExportSingleCalculatedValueManager, self).__init__()
        self.delimiter = delimiter
        self.m_name = measure_name
        self.m_group_name = measure_group_name
        self.m_header = measure_header
        self.m_label = measure_label
        self.standard_calc_name = self._adjust_standard_calc_name(
            standard_calc_name)
        self.parameter_dictionary = parameter_dictionary
        logger.DLOG("""Creating Single Calculated Value Content with
    measure group: %s
    measure name: %s
    standard calc name: %s
    standard calc parameters: %s""",
        self.measure_group_name(), self.measure_name(),
        self.standard_calc_name, self.parameter_dictionary)

    def _adjust_standard_calc_name(self, standard_calc_name):
        if not standard_calc_name.endswith(STANDARD_CALC_POSTFIX):
            return "".join([standard_calc_name, STANDARD_CALC_POSTFIX])

    def _get_standard_calc_method_obj(self, trd):
        calc_obj = trd.Calculation()
        return getattr(calc_obj, self.standard_calc_name)

    def column_headers(self):
        labels = [self.m_name]
        if self.m_label:
            labels.append(self.m_label)
        return labels

    def measure_name(self):
        return self.m_name

    def measure_group_name(self):
        return self.m_group_name

    def measure_count(self):
        return 1

    def dimension_defaults(self):
        return None

    def measure_header(self):
        if not self.m_header:
            return None
        return [self.delimiter.join(self.m_header)]

    def _content_values_template(self):
        if self.m_label:
            return [""]
        return []

    def get_content(self, trdnbr, space_collection):
        values = self._content_values_template()
        trd = acm.FTrade[trdnbr]
        calc_meth = self._get_standard_calc_method_obj(trd)
        try:
            calc_res = calc_meth(space_collection,
                self.parameter_dictionary)
        except Exception as msg:
            raise ContentError(msg)
        try:
            is_denom = calc_res.Class().IncludesBehavior(
                acm.FDenominatedValue)
        except:
            is_denom = False

        if is_denom:
            calc_res_nbr = calc_res.Number()
            self._validate_calculated_values([calc_res_nbr], trdnbr)
            values.append(str(calc_res_nbr))
        else:
            self._validate_calculated_values([calc_res], trdnbr)
            values.append(str(calc_res))
        return values

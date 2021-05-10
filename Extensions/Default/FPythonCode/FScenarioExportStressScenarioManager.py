""" Compiled: 2020-09-18 10:38:54 """

#__src_file__ = "extensions/risk_export/./etc/FScenarioExportStressScenarioManager.py"
from FScenarioExportScenarioPVManager import ScenarioExportScenarioPVManager


class ScenarioExportStressScenarioManager(ScenarioExportScenarioPVManager):

    MEASURE_NAME = "Stress PV Change"
    MEASURE_GROUP_NAME = "Stress"
    MEASURE_HEADER = ["Group", "Stress Name"]
    # Of the format name1, value1, name2, value2...
    DIMENSION_DEFAULTS = ["Stress Scenario", ""]

    def __init__(self, report_curr, file_path, delimiter, display_type):
        super(ScenarioExportStressScenarioManager, self).__init__(
            report_curr, file_path, delimiter, ["None"],
            display_type)

    def _generate_scenario_labels(self, start, end):
        return [str(label_sym) for label_sym in
                self.file_data_object.Labels()[start:end + 1]]

    def measure_name(self):
        return self.MEASURE_NAME

    def measure_group_name(self):
        return self.MEASURE_GROUP_NAME

    def measure_header(self):
        return [self.delimiter.join(self.MEASURE_HEADER)]

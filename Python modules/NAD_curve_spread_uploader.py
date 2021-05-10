"""--------------------------------------------------------------------------------------
MODULE
    nad_curve_spread_uploader

DESCRIPTION
    Date                : 2020-10-06
    Purpose             : This script uploads NAD yield curve spreads
    Department and Desk : SBL FO
    Requester           : Neo Mohapi
    Developer           : Sihle Gaxa
    JIRA Number         : PCGDEV-590

HISTORY
=========================================================================================
Date            JIRA no       Developer               Description
-----------------------------------------------------------------------------------------
2020-10-06      PCGDEV-590    Sihle Gaxa              Initial implementation.

ENDDESCRIPTION
--------------------------------------------------------------------------------------"""
import acm
import xlrd

import FRunScriptGUI
from at_logging import getLogger
from at_ael_variables import AelVariableHandler
from at_feed_processing import (SimpleCSVFeedProcessor,
                                SimpleXLSFeedProcessor,
                                notify_log)

LOGGER = getLogger(__name__)
fileFilter = "CSV Files (*.csv)|*.csv|XLS Files (*.xls)|*.xls|XLSX Files (*.xlsx)|*.xlsx|"
inputFile = FRunScriptGUI.InputFileSelection(FileFilter=fileFilter)


ael_variables = AelVariableHandler()
ael_variables.add(
    'input_file',
    label='File',
    cls=inputFile,
    default=inputFile,
    mandatory=True,
    multiple=True,
    alt='Input file in CSV or XLS format.'
    )
ael_variables.add(
    'curve_name',
    label='Yield Curve',
    mandatory=False,
    multiple=False,
    default="NAD-GOVBONDS-SPREADS",
    alt='Name of Yield Curve the spreads will be uploaded to'
    )

class YieldCurveSpreadUploader(object):

    constituent_col = "Constituent"
    spread_col = "Spread"
    nad_prefix = "NAD/NAMBD/"

    def __init__(self, yield_curve_name):
        self.curve_name = yield_curve_name
        self._dict_reader_kwargs = {'delimiter': ','}

    def _process_record(self, record, dry_run):
        (_index, record_data) = record

        constituent = record_data[self.constituent_col]
        spread_value = record_data[self.spread_col]

        yield_curve = acm.FYieldCurve[self.curve_name]
        if not yield_curve:
            LOGGER.exception("{curve} does not exist in Front Arena".format(curve=self.curve_name))
            return

        if yield_curve.InstrumentSpreads():
            for curve_ins in yield_curve.InstrumentSpreads():
                try:
                    instrument = curve_ins.Instrument()
                    if instrument:
                        instrument_name = instrument.Name()[10:]
                        if instrument_name.startswith(constituent):
                            curve_spread = float(spread_value)/10000
                            curve_ins.Spread(curve_spread)
                            curve_ins.Commit()
                            LOGGER.info("{ins} successfully updated with {value}".format(
                                        ins=instrument_name, value=curve_spread))
                except Exception as e:
                    LOGGER.exception("Could not upload spread because {error}".format(error=str(e)))


class CSVCreator(YieldCurveSpreadUploader, SimpleCSVFeedProcessor):

    def __init__(self, file_path, yield_curve_name):
        YieldCurveSpreadUploader.__init__(self, yield_curve_name)
        SimpleCSVFeedProcessor.__init__(self, file_path, do_logging=False)


class XLSCreator(YieldCurveSpreadUploader, SimpleXLSFeedProcessor):

    def __init__(self, file_path, yield_curve_name):
        YieldCurveSpreadUploader.__init__(self, yield_curve_name)
        SimpleXLSFeedProcessor.__init__(self, file_path, sheet_index=0, sheet_name=None)


def ael_main(dictionary):
    try:
        file_path = str(dictionary['input_file'])
        yield_curve_name = str(dictionary['curve_name'])
        LOGGER.info("Processing input file: {path}".format(path=file_path))

        if file_path.endswith(".csv"):
            file_processor = CSVCreator(file_path, yield_curve_name)
        else:
            file_processor = XLSCreator(file_path, yield_curve_name)
        file_processor.add_error_notifier(notify_log)
        file_processor.process(False)
        file_processor.process(False)
        LOGGER.info("Completed successfully")
    except Exception as e:
        LOGGER.exception("Failed to process file because {error}".format(error=str(e)))
        raise Exception("Failed to process file because {error}".format(error=str(e)))

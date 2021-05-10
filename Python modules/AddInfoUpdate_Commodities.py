"""-----------------------------------------------------------------------
MODULE
    AddInfoUpdate_Commodities.py

HISTORY
==================================================================================
Date            JIRA                    Developer        Description
----------------------------------------------------------------------------------
2020/05/05      ARR-48,ARR-52           Snowy Mabilu     Updated the script to include
                                                        Commodity unit and to also verify in the information
                                                        on the underlyings is the same as the one provided input file.
----------------------------------------------------------------------------"""
import acm
import FRunScriptGUI

from at_feed_processing import (SimpleXLSFeedProcessor, notify_log)
from at_ael_variables import AelVariableHandler
from at_logging import getLogger

LOGGER = getLogger(__name__)
COMMODITY_UNIT_MAP = {
    "Bushel(56 Bu)": "Bushels",
    "Bushel(60 Bu)": "Bushels",
    "BBL": "Barrels",
    "TOZ": "Ounces",
    "LB": "Pounds",
    "ST (Short Ton)": "Short Tonnes",
    "MT": "Tonnes",
    "TON (CER)": "Tonnes"
}

fileFilter = "XLSX Files (*.xlsx)|*.xlsx|CSV Files (*.csv)|*.csv|"
inputFile = FRunScriptGUI.InputFileSelection(FileFilter=fileFilter)
ael_variables = AelVariableHandler()
ael_variables.add(
    'portfolio',
    label='Portfolio',
    default='AFRICA TRADING,COMMODITIES TRADING,8188',
    mandatory=True,
    alt='Portfolios for commodity add info enrichment'
)

ael_variables.add(
    'input',
    label='Input file',
    cls=inputFile,
    default="/nfs/fa/reports/EMEA/prod/FAReports/AtlasEndOfDay/SupplierFinance/Commodities/ADDINFO_COMMODITY.xlsx",
    multiple=True,
    mandatory=True,
    alt='Commodity input CSV file'
)


class ReadInputDataFromExcel(SimpleXLSFeedProcessor):

    def __init__(self, file_path):
        SimpleXLSFeedProcessor.__init__(self, file_path, sheet_index=0, sheet_name=None)
        self.file_path = file_path
        self.lines = []

    def is_valid_add_info_record(self, record_data):
        deliverable = str(record_data["Add info:Commodity Deliverable"]).strip()
        label = str(record_data["Add info:Commodity Label"]).strip()
        subset = str(record_data["Add info:Commodity SubAsset"]).strip()
        description = str(record_data["Add info:Commodity Description"]).strip()
        unit = str(record_data["Add info:Openlink Unit"]).strip()

        if deliverable and deliverable not in self.get_choice_list("Commodity Deliverable"):
            LOGGER.error("Error {} not in Choice list Commodity Deliverable".format(deliverable))
            return False
        if label and label not in self.get_choice_list("Commodity Label"):
            LOGGER.error("Error {} not in Choice list Commodity Label".format(label))
            return False
        if description and description not in self.get_choice_list("Commodity Description"):
            LOGGER.error("Error {} not in Choice list Commodity Description".format(subset))
            return False
        if subset and subset not in self.get_choice_list("Commodity SubAsset"):
            LOGGER.error("Error {} not in Choice list Commodity SubAsset".format(description))
            return False
        if unit and unit not in self.get_choice_list("Openlink Unit"):
            LOGGER.error("Error {} not in Choice list Openlink Unit".format(unit))
            return False
        return True

    def _process_record(self, record, dry_run):
        (_index, record_data) = record
        try:
            if self.is_valid_add_info_record(record_data):
                self.lines.append(record_data)
            else:
                LOGGER.error("Invalid add info at line  {0} of file {1}".format(_index, self.file_path))
        except Exception as exc:
            LOGGER.exception("Failed to read input file {}".format(self.file_path))
            raise exc

    @staticmethod
    def get_choice_list(name):
        choice_list_values = []
        commodity_choice_list = acm.FChoiceList.Select('name="{}" list="MASTER"'.format(name))
        if commodity_choice_list:
            for choice in commodity_choice_list[0].Choices():
                choice_list_values.append(choice.Name())
            return choice_list_values
        return None


def create_add_info_spec(obj, spec, value):
    try:
        add_info = acm.FAdditionalInfo()
        add_info.AddInf(spec)
        add_info.Recaddr(obj.Oid())
        add_info.FieldValue(value)
        add_info.Commit()
    except:
        LOGGER.exception("Failed to create {0} on instrument {1} with value {2}".format(obj.Name(), spec, value))


def create_add_info(spec, value, obj):
    spec = acm.FAdditionalInfoSpec[spec]
    add_info = acm.FAdditionalInfo.Select01('recaddr = {0} and addInf = {1}'.format(obj.Oid(), spec.Oid()), '')
    if value == "":
        if add_info:
            add_info.Delete()
            LOGGER.info('Delete Additional Info \'{0}\' on INSTRUMENT: \'{1}\''.format(spec.FieldName(), obj.Name()))
    else:
        if not add_info:
            create_add_info_spec(obj, spec, value)
            LOGGER.info(
                'Create Additional Info \'{0}\' on INSTRUMENT: \'{1}\' to {2}'.format(spec.FieldName(), obj.Name(),
                                                                                      value))
        elif add_info.FieldValue() != value:
            add_info.Delete()
            create_add_info_spec(obj, spec, value)
            LOGGER.info('Update Additional Info \'{0}\' on INSTRUMENT: \'{1}\' to {2}'.format(
                spec.FieldName(), obj.Name(), value))


def get_add_info(record, instrument):
    create_add_info("Commodity Deli", str(record["Add info:Commodity Deliverable"]).strip(), instrument)
    create_add_info("Commodity Label", str(record["Add info:Commodity Label"]).strip(), instrument)
    create_add_info("Commodity Desc", str(record["Add info:Commodity Description"]).strip(), instrument)
    create_add_info("Commodity SubAsset", str(record["Add info:Commodity SubAsset"]).strip(), instrument)
    unit = str(record["Add info:Openlink Unit"])
    create_add_info("Openlink Unit", unit, instrument)
    commodity_unit = "Commodity Unit"
    if unit and unit in COMMODITY_UNIT_MAP:
        unit = COMMODITY_UNIT_MAP[unit]
    else:
        unit = "None"
    create_add_info(commodity_unit, unit, instrument)


def check_portfolio(underlying, line, portfolio):
    for instrument in portfolio.Instruments():
        if instrument.InsType() == 'Commodity' and instrument.Name() == underlying:
            get_add_info(line, instrument)
        elif instrument.InsType() == 'Future/Forward' and instrument.Underlying().Name() == underlying:
            get_add_info(line, instrument)
        elif instrument.InsType() == 'Option':
            if instrument.Underlying().InsType() == 'Future/Forward':
                if instrument.Underlying().Underlying().Name() == underlying:
                    get_add_info(line, instrument)
            elif instrument.Underlying().Name() == underlying:
                get_add_info(line, instrument)
        elif instrument.InsType() == 'PriceSwap':
            for e in instrument.Legs():
                if e.LegType() == "Float" and e.FloatRateReference().Name() == underlying:
                    get_add_info(line, instrument)


def get_info(lines, portfolio):
    for record in lines:
        underlying = str(record["Underlying"]).strip()
        check_portfolio(underlying, record, portfolio)


def ael_main(ael_dict):
    LOGGER.info("Check Instruments in Portfolio: {}".format(str(ael_dict["portfolio"])))
    plist = str(ael_dict["portfolio"]).split(",")
    input_file = str(ael_dict['input'])
    proc = ReadInputDataFromExcel(input_file)
    proc.process(False)
    lines = proc.lines
    for record in lines:
        underlying = acm.FInstrument[str(record["Underlying"]).strip()]
        if underlying:
            get_add_info(record, underlying)
    for portfolio_name in plist:
        portfolio = acm.FPhysicalPortfolio[portfolio_name]
        LOGGER.info(portfolio_name)
        LOGGER.info("Total number of instruments in Portfolio: {}".format(str(len(portfolio.Instruments()))))
        get_info(lines, portfolio)
    LOGGER.info("Completed Successfully")

import acm
import re
import collections
from random import randint
from datetime import datetime, date, timedelta
from at_logging import getLogger


class AssetClass():
    def __init__(self, asset_class_number, sysid, uat_ocode, production_ocode, asset_id):
        self.asset_class_number = asset_class_number
        self.sysid = sysid
        self.uat_ocode = uat_ocode
        self.production_ocode = production_ocode
        self.asset_id = asset_id


class DelegatedReportBase():
    LOGGER = getLogger(__name__)
    REPORTING_DATE = datetime.now().strftime('%Y-%m-%d.T%H:%M:%SZ')
    ASSET_CLASSES = {
        "Commodity": AssetClass("2", "60287", "25BS", "24BS", "CO"),
        "Credit": AssetClass("3", "60284", "35BS", "34BS", "CD"),
        "Equity": AssetClass("4", "60290", "45BS", "44BS", "EQ"),
        "Foreign Exchange": AssetClass("5", "60278", "55BS", "54BS", "FX"),
        "Investments Rates": AssetClass("6", "60281", "65BS", "64BS", "IR"),
        "Exchange Trade (ETD)": AssetClass("7", "60271", "75BS", "74BS", "N/A"),
        "Collateral Value": AssetClass("0", "60359", "05BS", "04BS", "N/A"),
        "Collateral Link": AssetClass("C", "60354", "C5BS", "C4BS", "N/A")}

    SECTOR = {
        "A": "AssuranceUndertaking",
        "C": "CreditInstitution",
        "F": "InvestmentFirm",
        "I": "InsuranceUndertaking",
        "L": "AlternativeInvestmentFund",
        "O": "InstitutionForOccupationalRetirementProvision",
        "R": "ReinsuranceUndertaking",
        "U": "UCITS"
    }

    AUTO_ROUTE_UAT = "02981185"
    AUTO_ROUTE_PROD = "02501185"
    UAT = "DTS4"
    PROD = "DTS3"
    ACTION = ["New", "Modify", "Cancel"]
    REPORT_TYPES = ["Collateral", "Valuation", "Trade Event"]

    def __init__(self, action, asset_class, position):
        self.action = action
        self.asset_class = asset_class
        self.positions = position

    def get_column_key_from_value(self, value, params):
        keys = params.Keys()
        values = params.Values()
        for val in values:
            if re.sub('[^A-Za-z0-9]+', '', val.Text()).upper() == re.sub('[^A-Za-z0-9]+', '', value.strip()).upper():
                return keys[values.IndexOf(val)]
        return None

    def create_row(self, params):
        """
        This method create the row data using the headers from the task,
         and the columns function mappings through the parameters
        key variables:
            self.position - > a tuple of column headers - This will be passed through the constructor
        :return: row data as an list

        """
        row = []
        for column in range(0, len(self.positions)):
            key = self.get_column_key_from_value(self.positions[column], params)
            if not key:
                print "No method defined for ", self.positions[column]
                row.append("")
            else:
                try:
                    row.append(eval('self.{0}()'.format(key)))
                except Exception as e:
                    row.append("")
                    self.__class__.LOGGER.exception("Failed to process method {}".format(self.positions[column]))
                    continue
        return row

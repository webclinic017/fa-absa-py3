import acm
import DelegatedReportBase

from datetime import datetime, date, timedelta
from at_logging import getLogger
from at_feed_processing import (SimpleCSVFeedProcessor,
                                notify_log)

LOGGER = getLogger(__name__)
COLLETERAL_PARAMS = acm.GetDefaultContext().GetExtension('FParameters', 'FObject',
                                                         'Colleteral_Event_Columns').Value()


class ColleteralCreatorFromCSV(SimpleCSVFeedProcessor):

    def __init__(self, file_path, action, assetclass, positions, colleteral_portfolio,
                 data_submitter):
        SimpleCSVFeedProcessor.__init__(self, file_path, do_logging=False)
        self.type = type
        self.action = action
        self.assetclass = assetclass
        self.results = []
        self.positions = positions
        self.colleteral_portfolio = colleteral_portfolio
        self.data_submitter = data_submitter

    def _process_record(self, record, dry_run):

        (_index, record_data) = record
        for choice in self.colleteral_portfolio.Choices():
            portfolio = choice.Name()
            if record_data['AgreementId'] == portfolio:
                party = acm.FParty[choice.Description()]
                creator = ColleteralReportCreator(self.type, self.action, self.assetclass, self.positions,
                                                  self.data_submitter, party)

                creator.set_colleteral_file_data(record_data['AgreementId'], record_data['CollateralCurrency'],
                                                 record_data['CollateralBalance'])
                self.results.append(creator.create_row(COLLETERAL_PARAMS))


class ColleteralReportCreator(DelegatedReportBase.DelegatedReportBase):
    TYPES = ["CollateralValue", "CollateralLink"]
    LEVELS = ["CollateralizedPortfolioLevel", "CollateralizedTradeLevel"]

    def __init__(self, type, action, assetclass, position, data_submitter, party):
        DelegatedReportBase.DelegatedReportBase.__init__(self, action, assetclass, position)
        self.type = type
        self.collateral_balance = 0.0
        self.collateral_currency = "USD"
        self.aggeement_id = ""
        self.assetclass = assetclass
        self.data_submitter = data_submitter
        self.party = party

    def set_colleteral_file_data(self, aggeement_id, currency, balance):
        self.collateral_balance = balance
        self.collateral_currency = currency
        self.aggeement_id = aggeement_id

    def comment(self):
        return "ABSA Collateral"

    def version(self):
        return "Coll1.0"

    def message_type(self):
        return "CollateralValue"

    def data_submitter_message_id(self):
        return ""

    def _action(self):
        return self.action

    def data_submitter_prefix(self):
        return "LEI"

    def data_submitter_value(self):
        return self.data_submitter

    def trade_party_prefix(self):
        return "LEI"

    def trade_party_value(self):
        return self.party.LegalEntityId()

    def execution_agent_party_value_prefix(self):
        return ""

    def execution_agent_party_value(self):
        return ""

    def collateral_portfolio_code(self):
        return "1001"

    def collateral_portfolio_indicator(self):
        return "Y"

    def value_of_the_collateral(self):
        return ""

    def currency_of_the_collateral(self):
        return ""

    def collateral_valuation_date_time(self):
        return DelegatedReportBase.DelegatedReportBase.REPORTING_DATE

    def collateral_reporting_date(self):
        return ""

    def sendto(self):
        return ""

    def execution_agent_masking_flag(self):
        return ""

    def trade_party_reporting_obligation(self):
        return "FCA"

    def other_party_id_type(self):
        return "LEI"

    def other_party_id(self):
        return self.data_submitter

    def collateralized(self):
        return "Partially"

    def initial_margin_posted(self):
        return ""

    def currency_of_the_initial_margin_posted(self):
        return ""

    def initial_margin_received(self):
        return ""

    def currency_of_the_initial_margin_received(self):
        return ""

    def variation_margin_posted(self):
        return 0

    def currency_of_the_variation_margin_posted(self):
        return self.collateral_currency

    def variation_margin_received(self):
        return self.collateral_balance

    def currency_of_the_variation_margin_received(self):
        return self.collateral_currency

    def excess_collateral_posted(self):
        return 0

    def currency_of_the_excess_collateral_posted(self):
        return self.collateral_currency

    def excess_collateral_received(self):
        return 0

    def currency_of_the_excess_collateral_received(self):
        return self.collateral_currency

    def third_party_viewer_id_type(self):
        return ""

    def level(self):
        return ""

    def third_party_viewer(self):
        return ""

    def reserved_participant_use_1(self):
        return ""

    def reserved_participant_use_2(self):
        return ""

    def reserved_participant_use_3(self):
        return ""

    def reserved_participant_use_4(self):
        return ""

    def reserved_participant_use_5(self):
        return ""

    def action_type_party_1(self):
        return "V"

    def reporting_timestamp(self):
        return datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ')



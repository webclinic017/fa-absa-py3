from datetime import datetime
import acm
from DelegatedReportBase import DelegatedReportBase

VALUATION_PARAMS = acm.GetDefaultContext().GetExtension('FParameters', 'FObject',
                                                           'Valuation_Event_Columns').Value()
class ValuationCreatorFromStoredQuery:

    def __init__(self, stored_query, action, asset_class, data_submitter_value, positions):
        self.stored_query = stored_query
        self.results = []
        self.asset_class = asset_class
        self.data_submitter_value = data_submitter_value
        self.action = action
        self.column_positions = positions

    def process(self, dry_run):
        for trade in self.stored_query.Query().Select():
            valuation = ValuationReportCreator(trade, self.action, self.asset_class,
                                               self.data_submitter_value, self.column_positions)
            row = valuation.create_row(VALUATION_PARAMS)
            self.results.append(row)


class ValuationReportCreator(DelegatedReportBase):

    def __init__(self, trade, action, asset_class, data_submitter, position):
        DelegatedReportBase.__init__(self, action, asset_class, position)
        self.trade = trade
        self.data_submitter = data_submitter
        self.action = action

    def comment(self):
        return self.trade.Name()

    def version(self):
        return ""

    def message_type(self):
        return "Valuation"

    def _action(self):
        return self.action

    def usi_prefix(self):
        return ""

    def usi_value(self):
        return ""

    def primary_asset_class(self):
        return "InterestRate"

    def secondary_asset_class(self):
        return ""

    def trade_party_1_prefix(self):
        return "LEI"  # Should be chnaged

    def trade_party_1_value(self):
        return self.trade.Counterparty().LegalEntityId()

    def trade_party_2_prefix(self):
        return "LEI"  # Should change

    def trade_party_2_value(self):
        return self.data_submitter

    def data_submitter_prefix(self):
        return "LEI"  # Should be changed

    def data_submitter_value(self):
        return self.data_submitter

    def submitted_for_prefix(self):
        return "LEI"  # Should changed

    def submitted_for_value(self):
        return self.trade.Counterparty().LegalEntityId()

    def cleared_product_id(self):
        return ""

    def valuation_datetime(self):
        return datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")

    def mtm_value(self):
        std_calculation_space_collection = acm.Calculations().CreateStandardCalculationsSpaceCollection()
        return self.trade.Calculation().MarkToMarketValue(std_calculation_space_collection).Number()

    def mtm_currency(self):
        return self.trade.Currency().Name()

    def valuation_source(self):
        return ""

    def valuation_reference_model(self):
        return ""

    def additional_comments(self):
        return ""

    def data_submitter_message_id(self):
        return self.trade.Counterparty().Name()

    def valuation_datetime_party_2(self):
        return ""

    def mtm_value_party_2(self):
        return ""

    def mtm_currency_party_2(self):
        return ""

    def valuation_type_party_1(self):
        return "MarkToMarket"

    def valuation_type_party_2(self):
        return ""

    def uti_prefix(self):
        return "0000452A"

    def uti(self):
        return 'MARKITWIRE{0}'.format(self.trade.add_info('CCPmiddleware_id'))

    def mtm_value_ccp(self):
        return ""

    def mtm_currency_ccp(self):
        return ""

    def valuation_type_ccp(self):
        return ""

    def valuation_datetime_ccp(self):
        return ""

    def trade_party_1_transaction_id(self):
        return self.trade.Name()

    def trade_party_2_transaction_id(self):
        return "EXTERNAL"

    def sendto(self):
        return ""

    def trade_party_1_reporting_destination(self):
        return "FCA"

    def party_2_reporting_obligation(self):
        return ""

    def trade_party_1_execution_agent_id_type(self):
        return ""

    def trade_party_1_execution_agent_id(self):
        return ""

    def trade_party_2_execution_agent_id_type(self):
        return ""

    def trade_party_2_execution_agent_id(self):
        return ""

    def ai_party_1_type(self):
        return ""

    def ai_party_1_id(self):
        return ""

    def ai_party_2_type(self):
        return ""

    def ai_party_2_id(self):
        return ""

    def clearing_status(self):
        return "FALSE"

    def trade_party_1_action_type(self):
        return "V"

    def trade_party_2_action_type(self):
        return ""

    def level(self):
        return "T"

    def trade_party_1_third_party_viewer_id_type(self):
        return ""

    def trade_party_1_third_party_viewer_id(self):
        return ""

    def trade_party_2_third_party_viewer_id_type(self):
        return ""

    def trade_party_2_third_party_viewer_id(self):
        return ""

    def reporting_timestamp(self):
        return datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")



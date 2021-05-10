import acm
import FRegulatoryLibBase
import collections
from datetime import datetime
from random import randint
from datetime import datetime, date, timedelta
from DelegatedReportBase import DelegatedReportBase

from at_logging import getLogger

LOGGER = getLogger(__name__)

TRADE_EVENT_COLUMNS = acm.GetDefaultContext().GetExtension('FParameters', 'FObject',
                                                           'Delegated_Trade_Event_Columns').Value()


class TradeEventsCreatorFromStoredQuery:

    def __init__(self, stored_query, action, asset_class, data_submitter_value, positions):
        self.stored_query = stored_query
        self.results = []
        self.asset_class = asset_class
        self.data_submitter_value = data_submitter_value
        self.action = action
        self.column_positions = positions

    def get_fx_trades(self, query):

        trades = []
        query_result = query.Query().Select()
        for trade in query_result:
            if trade.Instrument().InsType() == "Curr" and abs(
                    acm.Time.DateDifference(trade.ExecutionTime(), trade.ValueDay())) > 2:
                trades.append(trade)
            if trade.Instrument().InsType() == 'Future/Forward' and trade.InstrumentSubType().Text() == 'NDF':
                trades.append(trade)
        return trades

    def process(self, dry_run):
        if self.asset_class.asset_class_number == "5":
            trades = self.get_fx_trades(self.stored_query)
        else:
            trades = self.stored_query.Query().Select()
        for trade in trades:
            trade_event = TradeEventsCreator(trade, self.action, self.asset_class, self.column_positions,
                                              self.data_submitter_value)
            row = trade_event.create_row(TRADE_EVENT_COLUMNS)
            self.results.append(row)


class TradeEventsCreator(DelegatedReportBase):

    def __init__(self, trade, action, assetclass, position,  data_submitter):
        DelegatedReportBase.__init__(self, action, assetclass, position)
        self.trade = trade
        self.data_submitter = data_submitter

    def comment(self):
        return ""

    def version(self):
        return "CA4.0FX1.8"

    def message_type(self):
        return "SNAPSHOT"

    def _action(self):
        return self.action

    def transaction_type(self):
        return "TRADE"

    def usi_prefix(self):
        return ""

    def usi_value(self):
        return ""

    def primary_asset_class(self):
        return "FOREIGNEXCHANGE"

    def secondary_asset_class(self):
        return ""

    def suppress_price_dissemination(self):
        return ""

    def mandatory_clearing_indicator(self):
        return "FCA-N"

    def effective_date(self):
        return datetime.strptime(self.trade.ExecutionTime(), '%Y-%m-%d %H:%M:%S').strftime('%Y-%m-%d')

    def price_notation_price_type(self):
        return "Units"

    def price_notation_price(self):
        return self.trade.Price()

    def additional_price_notation_price_type(self):
        return ""

    def additional_price_notation_price(self):
        return ""

    def option_type(self):
        return ""

    def additional_repository_1_prefix(self):
        return ""

    def additional_repository_2_prefix(self):
        return ""

    def additional_repository_3_prefix(self):
        return ""

    def product_id_prefix(self):
        return "ISDA"

    def product_id_value(self):
        return "ForeignExchange:Forward"

    def trade_party_1_role(self):
        return ""

    def trade_party_1_prefix(self):
        return "LEI"

    def trade_party_1_value(self):
        return self.trade.Counterparty().LegalEntityId()

    def execution_agent_party_1_prefix(self):
        return ""

    def execution_agent_party_1_value(self):
        return ""

    def clearing_broker_party_1_prefix(self):
        return ""

    def clearing_broker_party_1_value(self):
        return ""

    def clearing_broker_party_1_id_ccp_leg(self):
        return ""

    def clearing_broker_party_1_id_client_leg(self):
        return ""

    def trade_party_2_role(self):
        return ""

    def trade_party_2_prefix(self):
        return "LEI"

    def trade_party_2_value(self):
        return self.data_submitter

    def execution_agent_party_2_prefix(self):
        return ""

    def execution_agent_party_2_value(self):
        return ""

    def clearing_broker_party_2_prefix(self):
        return ""

    def clearing_broker_party_2_value(self):
        return ""

    def clearing_broker_party_2_id_ccp_leg(self):
        return ""

    def clearing_broker_party_2_id_client_leg(self):
        return ""

    def data_submitter_prefix(self):
        return "LEI"

    def data_submitter_value(self):
        return self.data_submitter

    def submitted_for_prefix(self):
        return "LEI"

    def submitted_for_value(self):
        return self.trade.Counterparty().LegalEntityId()

    def trade_party_1_transaction_id_ourref(self):
        return ""

    def trade_party_2_transaction_id_yourref(self):
        return self.trade.Name()

    def allocation_indicator(self):
        return ""

    def execution_timestamp(self):
        return datetime.strptime(self.trade.ExecutionTime(), '%Y-%m-%d %H:%M:%S').strftime('%Y-%m-%dT%H:%M:%SZ')

    def verification_type(self):
        return ""

    def execution_venue_prefix(self):
        return ""

    def execution_venue(self):
        return "OffFacility"

    def clearer_prefix(self):
        return ""

    def clearer_value(self):
        return ""

    def cleared_product_id(self):
        return ""

    def clearing_exception_party_prefix(self):
        return ""

    def clearing_exception_party_value(self):
        return ""

    def off_market_flag(self):
        return ""

    def nonstandard_flag(self):
        return ""

    def collateralized(self):
        return "Uncollateralized"

    def as_of_date_time(self):
        return datetime.strptime(self.trade.ExecutionTime(), '%Y-%m-%d %H:%M:%S').strftime('%Y-%m-%dT%H:%M:%SZ')

    def confirmation_date_time(self):
        return datetime.strptime(self.trade.ExecutionTime(), '%Y-%m-%d %H:%M:%S').strftime('%Y-%m-%dT%H:%M:%SZ')

    def confirmation_type(self):
        return "NonElectronic"

    def trade_date(self):
        return datetime.strptime(self.trade.ExecutionTime(), '%Y-%m-%d %H:%M:%S').strftime('%Y-%m-%d')

    def broker_location_party_1(self):
        return ""

    def broker_location_party_2(self):
        return ""

    def desk_location_party_1(self):
        return ""

    def desk_location_party_2(self):
        return ""

    def trader_location_party_1(self):
        return ""

    def trader_location_party_2(self):
        return ""

    def sales_location_party_1(self):
        return ""

    def sales_location_party_2(self):
        return ""

    def prior_usi_prefix(self):
        return ""

    def prior_usi_value(self):
        return ""

    def valuation_datetime(self):
        return ""

    def mtm_value(self):
        return ""

    def mtm_currency(self):
        return ""

    def settlement_agent_party_1_prefix(self):
        return ""

    def settlement_agent_party_1_value(self):
        return ""

    def settlement_agent_party_2_prefix(self):
        return ""

    def settlement_agent_party_2_value(self):
        return ""

    def valuation_source(self):
        return ""

    def valuation_reference_model(self):
        return ""

    def document_id(self):
        return ""

    def document(self):
        return ""

    def document_description(self):
        return ""

    def additional_comments(self):
        return ""

    def reporting_jurisdiction(self):
        return "FCA"

    def party_1_reporting_obligation(self):
        return "FCA"

    def party_2_reporting_obligation(self):
        return ""

    def voluntary_submission_trade_party_1(self):
        return ""

    def voluntary_submission_trade_party_2(self):
        return ""

    def additional_repository_1(self):
        return ""

    def additional_repository_1_trade_id(self):
        return ""

    def additional_repository_2(self):
        return ""

    def additional_repository_2_trade_id(self):
        return ""

    def additional_repository_3(self):
        return ""

    def additional_repository_3_trade_id(self):
        return ""

    def dco_trade_identifiers(self):
        return ""

    def trade_party_2_eb_pb(self):
        return ""

    def trade_party_1_eb_pb(self):
        return ""

    def df_reporting_party(self):
        return ""

    def correlation_id(self):
        return ""

    def creation_time_stamp(self):
        return ""

    def confirmation_agreement(self):
        return "FALSE"

    def exchanged_currency_1_amount(self):
        return abs(self.trade.BaseCostDirty()) if self.trade.InstrumentSubType().Text() == 'NDF' else abs(
            self.trade.Nominal())

    def exchanged_currency_1(self):
        return self.trade.CurrencyPair().Currency1().Name()

    def exchanged_currency_1_payer_prefix(self):
        return "LEI"

    def exchanged_currency_1_payer_value(self):
        return self.data_submitter

    def exchanged_currency_2_amount(self):
        return abs(self.trade.FaceValue()) if self.trade.InstrumentSubType().Text() == 'NDF' else abs(
            self.trade.Premium())

    def exchanged_currency_2(self):
        return self.trade.CurrencyPair().Currency2().Name()

    def exchanged_currency_2_payer_prefix(self):
        return "LEI"

    def exchanged_currency_2_payer_value(self):
        return self.trade.Counterparty().LegalEntityId()

    def value_date(self):
        return datetime.strptime(self.trade.ValueDay(), '%Y-%m-%d').strftime('%Y-%m-%d')

    def exchange_rate(self):
        return self.trade.Price()

    def exchange_rate_basis_currency_1(self):
        return self.trade.CurrencyPair().Currency2().Name()

    def exchange_rate_basis_currency_2(self):
        return self.trade.CurrencyPair().Currency1().Name()

    def option_seller_prefix(self):
        return ""

    def option_seller_value(self):
        return ""

    def option_buyer_prefix(self):
        return ""

    def option_buyer_value(self):
        return ""

    def option_style(self):
        return ""

    def put_notional_amount(self):
        return ""

    def put_notional_currency(self):
        return ""

    def call_notional_amount(self):
        return ""

    def call_notional_currency(self):
        return ""

    def commencement_date(self):
        return datetime.strptime(self.trade.ExecutionTime(), '%Y-%m-%d %H:%M:%S').strftime('%Y-%m-%d')

    def option_effective_date(self):
        return datetime.strptime(self.trade.ExecutionTime(), '%Y-%m-%d %H:%M:%S').strftime('%Y-%m-%d')

    def expiration_date(self):
        return datetime.strptime(self.trade.ValueDay(), '%Y-%m-%d').strftime('%Y-%m-%d')

    def expiration_time(self):
        return ""

    def expiration_time_business_center(self):
        return ""

    def multiple_exercise_minimum(self):
        return ""

    def multiple_exercise_maximum(self):
        return ""

    def option_value_date(self):
        return ""

    def premium_amount(self):
        return 0

    def premium_currency(self):
        return ""

    def option_lockout_date(self):
        return ""

    def premium_payer_prefix(self):
        return "LEI"

    def premium_payer_value(self):
        return self.trade.Counterparty().LegalEntityId()

    def premium_payment_date_unadjusted(self):
        return ""

    def premium_quote(self):
        return ""

    def premium_quote_basis(self):
        return ""

    def settlement_currency(self):
        return ""

    def settlement_exchange_rate_basis(self):
        return ""

    def settlement_fixing_date(self):
        return ""

    def settlement_rate_source(self):
        return ""

    def settlement_rate_source_page(self):
        return ""

    def settlement_fixing_time(self):
        return ""

    def settlement_fixing_time_business_center(self):
        return ""

    def master_agreement_type(self):
        return ""

    def master_agreement_version(self):
        return ""

    def exotic_buyer_party_prefix(self):
        return ""

    def exotic_buyer_party_value(self):
        return ""

    def exotic_seller_party_prefix(self):
        return ""

    def exotic_seller_party_value(self):
        return ""

    def exotic_effective_date(self):
        return ""

    def exotic_value_date(self):
        return ""

    def exotic_expiration_date(self):
        return ""

    def exotic_notional_amount(self):
        return ""

    def exotic_notional_currency(self):
        return ""

    def exotic_currencies(self):
        return ""

    def exotic_option_type(self):
        return ""

    def exotic_premium_amount(self):
        return ""

    def exotic_premium_currency(self):
        return ""

    def swap_link_id(self):
        return ""

    def trade_party_1_us_person_indicator(self):
        return ""

    def trade_party_1_cftc_financial_entity_status(self):
        return ""

    def trade_party_2_us_person_indicator(self):
        return ""

    def trade_party_2_cftc_financial_entity_status(self):
        return ""

    def large_size_trade(self):
        return ""

    def forward_exchange_rate(self):
        return self.trade.Price()

    def fx_delivery_type(self):
        return "Physical"

    def asian_rate_source(self):
        return ""

    def asian_fixing_time(self):
        return ""

    def asian_fixing_time_business_center(self):
        return ""

    def observation_period_start(self):
        return ""

    def observation_period_end(self):
        return ""

    def observation_frequency(self):
        return ""

    def observation_rate_quote_basis(self):
        return ""

    def reference_spot(self):
        return ""

    def trigger_condition(self):
        return ""

    def trigger_rate(self):
        return ""

    def trigger_rate_source(self):
        return ""

    def trigger_rate_quote_basis(self):
        return ""

    def trigger_condition_2(self):
        return ""

    def trigger_rate_2(self):
        return ""

    def trigger_rate_source_2(self):
        return ""

    def trigger_rate_quote_basis_2(self):
        return ""

    def barrier_direction(self):
        return ""

    def digital_option_value_date(self):
        return ""

    def digital_option_payout_currency(self):
        return ""

    def digital_option_payout_amount(self):
        return ""

    def digital_option_payout_style(self):
        return ""

    def cut_name(self):
        return ""

    def execution_period_start_date(self):
        return ""

    def execution_period_expiry_date(self):
        return ""

    def earliest_execution_time(self):
        return ""

    def earliest_execution_time_business_center(self):
        return ""

    def latest_execution_time(self):
        return ""

    def latest_execution_time_business_center(self):
        return ""

    def settlement_date_offset_period_multiplier(self):
        return ""

    def settlement_date_offset_business_day_convention(self):
        return ""

    def settlement_date_offset_business_centers(self):
        return ""

    def final_settlement_date(self):
        return ""

    def exotic_product_day_count_fraction(self):
        return ""

    def exotic_product_payment_frequency_period(self):
        return ""

    def exotic_product_payment_frequency_period_multiplier(self):
        return ""

    def exotic_product_payment_frequency_payer_party_reference(self):
        return ""

    def exotic_product_payment_frequency_underlyer_reference(self):
        return ""

    def exotic_product_reset_frequency_period(self):
        return ""

    def exotic_product_reset_frequency_period_multiplier(self):
        return ""

    def exotic_product_reset_frequency_underlyer_reference(self):
        return ""

    def exotic_product_option_family(self):
        return ""

    def exotic_product_option_strike_price(self):
        return ""

    def exotic_product_option_strike_price_currency(self):
        return ""

    def exotic_product_option_strike_price_units(self):
        return ""

    def exotic_product_option_commencement_date(self):
        return ""

    def exotic_settlement_type(self):
        return ""

    def ccp_for_underlying_swap(self):
        return ""

    def agreement_date(self):
        return datetime.strptime(self.trade.ExecutionTime(), '%Y-%m-%d %H:%M:%S').strftime('%Y-%m-%d')

    def data_submitter_message_id(self):
        return self.trade.Counterparty().Name()

    def lifecycle_event(self):
        return "TRADE"

    def industrial_sector_party_1(self):
        return ""

    def industrial_sector_party_2(self):
        return ""

    def confirmation_platform_id(self):
        return ""

    def confirmation_platform_trade_reference(self):
        return ""

    def broker_id_party_1_prefix(self):
        return ""

    def broker_id_party_1_value(self):
        return ""

    def broker_id_party_2_prefix(self):
        return ""

    def broker_id_party_2_value(self):
        return ""

    def reporting_delegation_model(self):
        return "Independent"

    def beneficiary_id_party_1_prefix(self):
        return "LEI"

    def beneficiary_id_party_1_value(self):
        return self.trade.Counterparty().LegalEntityId()

    def beneficiary_id_party_2_prefix(self):
        return ""

    def beneficiary_id_party_2_value(self):
        return ""

    def trade_party_1_domicile(self):
        return "GB"

    def trade_party_2_domicile(self):
        return ""

    def directly_linked_to_commercial_activity_or_treasury_financing_party_1(self):
        return "TRUE"

    def directly_linked_to_commercial_activity_or_treasury_financing_party_2(self):
        return ""

    def clearing_threshold_party_1(self):
        return "FALSE"

    def clearing_threshold_party_2(self):
        return ""

    def clearing_timestamp(self):
        return ""

    def compressed_trade(self):
        return "FALSE"

    def collateralized_party_2(self):
        return ""

    def valuation_datetime_party_2(self):
        return ""

    def mtm_value_party_2(self):
        return ""

    def mtm_currency_party_2(self):
        return ""

    def collateral_portfolio_code_party_1(self):
        return ""

    def collateral_portfolio_code_party_2(self):
        return ""

    def value_of_the_collateral_party_1(self):
        return ""

    def value_of_the_collateral_party_2(self):
        return ""

    def currency_of_the_collateral_value_party_1(self):
        return ""

    def currency_of_the_collateral_value_party_2(self):
        return ""

    def valuation_type_party_1(self):
        return ""

    def valuation_type_party_2(self):
        return ""

    def intragroup(self):
        return "FALSE"

    def trading_capacity(self):
        return "Principal"

    def trading_capacity_party_2(self):
        return ""

    def clearing_status(self):
        return "FALSE"

    def trade_party_1_branch_location(self):
        return ""

    def trade_party_2_branch_location(self):
        return ""

    def uti(self):
        return ''.join(['{}'.format(randint(0, 9)) for num in range(0, 9)]) + self.trade.Counterparty().Name()[:7]

    def mtm_value_ccp(self):
        return ""

    def mtm_currency_ccp(self):
        return ""

    def valuation_type_ccp(self):
        return ""

    def valuation_datetime_ccp(self):
        return ""

    def prior_uti(self):
        return ""

    def party_region(self):
        return "nonEEA"

    def counterparty_region(self):
        return "EEA"

    def trade_party_1_financial_entity_jurisdiction(self):
        return ""

    def trade_party_2_financial_entity_jurisdiction(self):
        return "FCA"

    def trade_party_1_non_financial_entity_jurisdiction(self):
        return "FCA"

    def trade_party_2_non_financial_entity_jurisdiction(self):
        return ""

    def trade_party_1_corporate_sector(self):
        return 1

    def trade_party_2_corporate_sector(self):
        return ""

    def uti_prefix(self):
        return "YCDYZNMZ3J"

    def prior_uti_prefix(self):
        return ""

    def master_agreement_version__1(self):
        return ""

    def barrier_type(self):
        return ""

    def sendto(self):
        return ""

    def trade_party_1_branch_prefix(self):
        return ""

    def trade_party_1_branch_value(self):
        return ""

    def trade_party_2_branch_prefix(self):
        return ""

    def trade_party_2_branch_value(self):
        return ""

    def trade_party_1_local_counterparty_jurisdiction(self):
        return ""

    def trade_party_2_local_counterparty_jurisdiction(self):
        return ""

    def inter_affiliate(self):
        return ""

    def original_execution_timestamp(self):
        return datetime.strptime(self.trade.ExecutionTime(), '%Y-%m-%d %H:%M:%S').strftime('%Y-%m-%dT%H:%M:%SZ')

    def event_processing_id(self):
        return ""

    def name_of_trade_party_1(self):
        return ""

    def name_of_trade_party_2(self):
        return ""

    def action_type_party_1(self):
        return "N"

    def action_type_party_2(self):
        return ""

    def clearing_swap_usi_prefix(self):
        return ""

    def clearing_swap_usi_value(self):
        return ""

    def clearing_swap_sdr_lei(self):
        return ""

    def prior_usi_type(self):
        return ""

    def original_swap_sdr_id_type(self):
        return ""

    def original_swap_sdr(self):
        return ""

    def clearing_member_client_account(self):
        return ""

    def origin(self):
        return ""

    def clearing_receipt_date_time(self):
        return ""

    def clearing_acceptance_date_time(self):
        return ""

    def clearing_exception_type(self):
        return ""

    def post_trade_transaction_date(self):
        return ""

    def post_trade_effective_date(self):
        return ""

    def rate_quote_basis_1(self):
        return ""

    def rate_quote_basis_2(self):
        return ""

    def leg_2_effective_date(self):
        return ""

    def leg_2_settlement_date(self):
        return ""

    def option_entitlement(self):
        return ""

    def number_of_options(self):
        return ""

    def trade_party_1_hk_counterparty_origin(self):
        return ""

    def ai_party_1_id_type(self):
        return ""

    def ai_party_1_id(self):
        return ""

    def ai_party_2_id_type(self):
        return ""

    def ai_party_2_id(self):
        return ""

    def execution_type(self):
        return ""

    def outstanding_notional_amount_1(self):
        return ""

    def outstanding_notional_currency_1(self):
        return ""

    def outstanding_notional_amount_2(self):
        return ""

    def outstanding_notional_currency_2(self):
        return ""

    def trade_party_2_hk_counterparty_origin(self):
        return ""

    def quantity_type(self):
        return ""

    def na(self):
        return ""

    def underlying_index_name(self):
        return ""

    def term_of_the_underlying_index(self):
        return ""

    def report_status(self):
        return ""

    def transaction_reference_number_mifir(self):
        return ""

    def venue_transaction(self):
        return ""

    def executing_entity(self):
        return ""

    def executing_entity_id_type(self):
        return ""

    def na__1(self):
        return ""

    def buyer(self):
        return ""

    def buyer_id_type(self):
        return ""

    def buyer_id_sub_type(self):
        return ""

    def buyer_id_sub_type_issuer(self):
        return ""

    def buyer_country_of_branch(self):
        return ""

    def buyer_first_name(self):
        return ""

    def buyer_surname(self):
        return ""

    def buyer_dob(self):
        return ""

    def buyer_decision_maker(self):
        return ""

    def buyer_decision_maker_id_type(self):
        return ""

    def buyer_decision_maker_id_sub_type(self):
        return ""

    def buyer_decision_maker_first_name(self):
        return ""

    def buyer_decision_maker_surname(self):
        return ""

    def buyer_decision_maker_dob(self):
        return ""

    def seller(self):
        return ""

    def seller_id_type(self):
        return ""

    def seller_id_sub_type(self):
        return ""

    def seller_id_sub_type_issuer(self):
        return ""

    def country_of_the_branch_for_the_seller(self):
        return ""

    def seller_first_name(self):
        return ""

    def seller_surname(self):
        return ""

    def seller_dob(self):
        return ""

    def seller_decision_maker(self):
        return ""

    def seller_decision_maker_id_type(self):
        return ""

    def seller_decision_maker_id_sub_type(self):
        return ""

    def seller_decision_maker_first_name(self):
        return ""

    def seller_decision_maker_surname(self):
        return ""

    def seller_decision_maker_dob(self):
        return ""

    def order_transmission_indicator(self):
        return ""

    def buyer_transmitter(self):
        return ""

    def seller_transmitter(self):
        return ""

    def na__2(self):
        return ""

    def derivative_notional_increase_decrease(self):
        return ""

    def net_amount(self):
        return ""

    def venue_of_execution(self):
        return ""

    def country_of_the_branch_membership(self):
        return ""

    def na__3(self):
        return ""

    def maturity_date(self):
        return ""

    def investment_decision(self):
        return ""

    def investment_decision_id_type(self):
        return ""

    def investment_decision_id_sub_type(self):
        return ""

    def investment_decision_country_of_branch(self):
        return ""

    def firm_execution(self):
        return ""

    def firm_execution_id_type(self):
        return ""

    def firm_execution_id_sub_type(self):
        return ""

    def firm_execution_country_of_branch(self):
        return ""

    def waiver_indicator(self):
        return ""

    def short_selling_indicator(self):
        return ""

    def otc_post_trade_indicator(self):
        return ""

    def commodity_derivative_indicator(self):
        return ""

    def sft_indicator(self):
        return ""

    def quantitymifir(self):
        return ""

    def instrument_name(self):
        return ""

    def na__4(self):
        return ""

    def na__5(self):
        return ""

    def trading_date_time_mifir(self):
        return ""

    def trade_party_1_country_of_the_other_counterparty(self):
        return "GB"

    def trade_party_2_country_of_the_other_counterparty(self):
        return "ZA"

    def trade_party_1_counterparty_side(self):
        return 'B' if self.trade.Direction() == 'Sell' else 'S'

    def trade_party_2_counterparty_side(self):
        return 'S' if self.trade.Direction() == 'Sell' else 'B'

    def contract_type(self):
        return "FW"

    def product_classification_type(self):
        return "C"

    def product_classification(self):
        return "JFRXXP"

    def product_identification_type(self):
        return ""

    def product_identification(self):
        return ""

    def underlying_identification_type(self):
        return "NA"

    def underlying_identification(self):
        return "NA"

    def report_tracking_number(self):
        return ""

    def complex_trade_component(self):
        return ""

    def price_multiplier(self):
        return self.trade.Price()

    def quantity(self):
        return abs(self.trade.Quantity())

    def upfront_payment(self):
        return ""

    def strike_price_notation(self):
        return ""

    def maturity_date_of_the_underlying(self):
        return ""

    def level(self):
        return "T"

    def delivery_currency_2(self):
        return self.trade.CurrencyPair().Currency2().Name()

    def trade_party_1_third_party_viewer(self):
        return ""

    def trade_party_2_third_party_viewer(self):
        return ""

    def trade_party_1_nature_of_the_reporting_counterparty(self):
        return "N"

    def trade_party_2_nature_of_the_reporting_counterparty(self):
        return "F"

    def currency_of_price(self):
        return self.trade.CurrencyPair().Currency2().Name()

    def trade_party_1_collateral_portfolio(self):
        return "N"

    def trade_party_2_collateral_portfolio(self):
        return "N"

    def execution_venue_mic_code(self):
        return "XXXX"

    def trade_party_1_third_party_viewer_id_type(self):
        return ""

    def trade_party_2_third_party_viewer_id_type(self):
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

    def execution_venue_type(self):
        return ""

    def strike_price_currency_pair(self):
        return ""

    def basket_constituents_number_of_units(self):
        return ""

    def package_identifier(self):
        return ""

    def embedded_option_on_swap(self):
        return ""

    def prior_uti_type(self):
        return ""

    def reporting_timestamp(self):
        return datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ')


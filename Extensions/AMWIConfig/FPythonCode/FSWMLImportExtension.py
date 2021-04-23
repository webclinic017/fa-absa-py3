"""

FSWMLImportExtension

"""
from traceback import print_exc
from uuid import uuid4

import acm

from AMWICommon import AMWI_TYPE_CLOSING, AMWI_TYPE_NORMAL, log_warning
from AMWICustomUtil import swml_value, swml_attr_value, swml_all_nodes, log_in_method_trade, log_debug, log_error, \
    log_in_method, AMWI_STATUS_TERMINATED, get_swml_filename, get_ignore_trades, get_ignore_users
from AMWIIdentity import get_markitwire_major_version, set_message_status, get_message_status, is_allocate_trade, \
    remove_mirrors
from AMWIMappings import return_mapping
from AMWITradeUtil import delete_payments_by_type, delete_payments_by_date, reverse_payments, delete_addinfos, \
    set_instrument_start, move_payments_by_type, find_payments_by_type, roll_date_to_next_month, set_trade_dates, \
    delete_duplicate_payments_on_trade, alter_payment_type, \
    find_closing_trades_by_markitwire_id, is_problem_basis_swap, fix_basis_swap
from AMWI_ValGroup import get_csa_val_group, find_val_group


def _add_describe_row(r, field, value):
    r.append("    %s = %s" % (field, value))


def _swml_extended_trade_details(field):
    return "SWML.swStructuredTradeDetails.swExtendedTradeDetails.%s" % field


def _swml_swap_fixed_leg(field):
    return "SWML.swStructuredTradeDetails.FpML.trade.swapStream@{'id':'fixedLeg'}.%s" % field


def _swml_curr_swap_float_leg(field):
    return "SWML.swStructuredTradeDetails.FpML.trade.swapStream@{'id':'floatingLeg'}.%s" % field


class SwmlMessage:
    def __init__(self, swml):
        self.swml = swml
        self.trade_map = {}

        # Data from SWML.swHeader
        self.tradeId = swml_value(swml, "SWML.swHeader.tradeId")
        self.swTradeVersionTimestamp = swml_value(swml, "SWML.swHeader.swTradeVersionTimestamp")
        self.swTradeVersionId = swml_value(swml, "SWML.swHeader.swTradeVersionId")
        self.swTradeStatus = swml_value(swml, "SWML.swHeader.swTradeStatus")
        self.swUserId = swml_value(swml, "SWML.swHeader.swNegotiationParties.swUserId")
        self.swClearingHouseId = swml_value(swml, "SWML.swHeader.swClearingParties.swClearingHouseId")
        self.swParticipantId_traderA = swml_value(swml,
                                                  "SWML.swHeader.swNegotiationParties" +
                                                  ".swTrader@{'id':'traderA'}.swParticipantId")
        self.swParticipantId_traderB = swml_value(swml,
                                                  "SWML.swHeader.swNegotiationParties" +
                                                  ".swTrader@{'id':'traderB'}.swParticipantId")
        self.swBlockTradeId = swml_value(swml, "SWML.swHeader.swBlockTradeId")

        # Data from SWML.swPrivateData
        self.swPrivateDataVersionId = swml_value(swml, "SWML.swPrivateData.swPrivateDataVersionId")
        self.swTradingBookId = swml_value(swml, "SWML.swPrivateData.swTradingBookId")
        self.swClearingStatus = swml_value(swml, "SWML.swPrivateData.swClearingStatus")
        self.swBrokerPartyId = swml_value(swml, "SWML.swPrivateData.swBrokerPartyId")
        self.swBrokerageAmountCcy = swml_value(swml, "SWML.swPrivateData.swBrokerageAmount.currency")
        self.swBrokerageAmount = swml_value(swml, "SWML.swPrivateData.swBrokerageAmount.amount")
        self.swDealerUserName = swml_value(swml, "SWML.swPrivateData.swDealerUserName")
        self.swPrivateBookingState = swml_value(swml, "SWML.swPrivateData.swPrivateBookingState")
        self.swAdditionalField_Acquirer = swml_value(swml,
                                                     "SWML.swPrivateData.swAdditionalField@{'fieldName':'Acquirer'}")
        self.swAdditionalField_TradeKey3 = swml_value(swml,
                                                      "SWML.swPrivateData.swAdditionalField@{'fieldName':'TradeKey3'}")
        self.swPrivateTradeId = swml_value(swml, "SWML.swPrivateData.swPrivateTradeId")

        # Data from SWML.swStructuredTradeDetails.swExtendedTradeDetails
        self.swClearingBroker_partyId = swml_value(swml, _swml_extended_trade_details("swClearingBroker.partyId"))
        self.swClearingBroker_partyName = swml_value(swml, _swml_extended_trade_details("swClearingBroker.partyName"))
        self.swClearingHouse_partyId = swml_value(swml, _swml_extended_trade_details("swClearingHouse.partyId"))
        self.swModificationEffectiveDate = swml_value(swml, _swml_extended_trade_details("swModificationEffectiveDate"))

        # Data from other sources
        self.party_partyId = swml_value(swml, "SWML.FpML.party[partyId!='ABSAZAJJ'].partyId")
        self.swAmendmentType = swml_value(swml, "SWML.swExtendedTradeDetails.swAmendmentType")
        self.swMessageText = swml_value(swml, "SWML.swNegotiation.swDialog.swTraderMessage.swMessageText")
        self.tradeDate = swml_value(swml, "SWML.swStructuredTradeDetails.FpML.trade.tradeHeader.tradeDate")
        self.swAdditionalField5 = swml_value(swml, "SWML.swAdditionalField @{'fieldName':'Additional Field 5'}")

        # Instrument specific fields
        self.fra_amount = swml_value(self.swml, "SWML.swStructuredTradeDetails.FpML.trade.fra.notional.amount")
        self.swap_initialValue = swml_value(self.swml, _swml_swap_fixed_leg("calculationPeriodAmount.calculation." +
                                                                            "notionalSchedule.notionalStepSchedule." +
                                                                            "initialValue"))
        self.curr_swap_rollDate = swml_value(self.swml,
                                             _swml_curr_swap_float_leg("calculationPeriodDates.terminationDate." +
                                                                       "unadjustedDate"))
        self.swap_payerPartyReference = swml_attr_value(self.swml,
                                                        _swml_swap_fixed_leg("payerPartyReference"), "href")

    def manage_trade(self, new_trade):
        # Use Python object ID as FTrade.Clone() keeps the original trade ID
        self.trade_map[id(new_trade)] = new_trade

    def commit_trades_excluding(self, exclude_trades):
        exclude_oids = [t.Oid() for t in exclude_trades]
        for trade in list(self.trade_map.values()):
            if trade.Oid() not in exclude_oids:
                log_debug("Committing trade: %i" % trade.Oid())
                trade.Commit()

    def get_trade_description(self):
        return "%s (%s:%s) %s" % (self.tradeId,
                                  self.swTradeVersionId,
                                  self.swPrivateDataVersionId,
                                  self.swTradeStatus)

    def describe(self):
        r = []
        variables = vars(self)
        for attribute in sorted(variables.keys()):
            value = variables[attribute]
            if value and not attribute.startswith("_"):
                if attribute not in ("swml", "trade_map"):
                    _add_describe_row(r, attribute, str(value))

        return "\n".join(r)

    def write_swml(self):
        filename = get_swml_filename(self.tradeId)
        with open(filename, "a+") as outfile:
            outfile.write(self.swml)

    def should_ignore_trade(self):

        if self.tradeId in get_ignore_trades():
            log_debug("Trade ID %s is in exclusion list. Ignoring!" % self.tradeId)
            return True

        ignore_users = get_ignore_users()
        if ignore_users:
            for user_prefix in ignore_users:
                if self.swUserId and self.swUserId.startswith(user_prefix):
                    log_debug("Markitwire user %s is in exclusion list. Ignoring trade!" % self.swUserId)
                    return True

        return False

    def set_broker(self, trade):
        # Core code sets the broker correctly. This override is to
        # support legacy behaviour because aliases are not always
        # correct.
        if trade.Broker():
            log_debug("Broker already set to %s" % trade.Broker().Name())
        elif self.swBrokerPartyId:
            broker_name = return_mapping(self.swBrokerPartyId, "Brokers")
            if not broker_name:
                log_debug("No mapping for broker: %s" % self.swBrokerPartyId)
            else:
                broker = acm.FBroker[str(broker_name)]
                if not broker:
                    log_debug("Cannot find broker: %s" % broker_name)
                else:
                    log_debug("Setting broker to %s" % broker.Name())
                    trade.Broker(broker)

    def set_bloomberg_trader(self, trade):
        user_name = self.swDealerUserName
        principal = acm.FPrincipalUser.Select01('type="MarkitWire" and principal="%s"' % user_name,
                                                "More than one Markitwire principal for user '%s'" % user_name)

        if principal:
            log_debug("Overriding default user with Bloomberg user: %s" % principal.User().Name())
            trade.Trader(principal.User())
        else:
            log_error("Could not find MarkitWire principal '%s'" % user_name)

    def set_portfolio(self, trade):
        if trade.IsInfant():
            return

        portfolio = acm.FPhysicalPortfolio.Select01('name like "%s"' % self.swTradingBookId,
                                                    "More than one portfolio matches name: %s" % self.swTradingBookId)

        if not portfolio:
            log_error("Could not find portfolio: %s" % self.swTradingBookId)
            portfolio = acm.FPhysicalPortfolio["MktWire_Allocate"]  # initialize the default portfolio

        if portfolio:
            if trade.Portfolio():
                if portfolio.Oid() != trade.Portfolio().Oid():
                    log_debug("Changing trade portfolio from '%s' to '%s'" % (trade.Portfolio().Name(),
                                                                              portfolio.Name()))
            else:
                log_debug("Setting portfolio: '%s'" % portfolio.Name())

            trade.Portfolio(portfolio)

    def set_acquirer(self, trade):
        if not self.swAdditionalField_Acquirer:
            log_error("No acquirer in message")

            if trade.Instrument().InsType() == 'CurrSwap' and trade.Acquirer().Name() == 'MARKITWIRE':
                owner_portfolio = trade.Portfolio().PortfolioOwner().Name()
                trade.Acquirer(owner_portfolio)
                log_debug("Changed from MARKITWIRE to '%s'" % trade.Acquirer().Name())
        else:
            acquirer_party = acm.FParty[self.swAdditionalField_Acquirer]
            if acquirer_party:
                if trade.Acquirer():
                    if trade.Acquirer().Oid() != acquirer_party.Oid():
                        log_debug(
                            "Changing acquirer from '%s' to '%s'" % (trade.Acquirer().Name(), acquirer_party.Name()))
                else:
                    log_debug("Setting acquirer to '%s'" % acquirer_party.Name())

                trade.Acquirer(acquirer_party)
            else:
                log_error("Cannot find acquirer '%s'" % self.swAdditionalField_Acquirer)

                if trade.Instrument().InsType() == 'CurrSwap' and trade.Acquirer().Name() == 'MARKITWIRE':
                    owner_portfolio = trade.Portfolio().PortfolioOwner().Name()
                    trade.Acquirer(owner_portfolio)
                    log_debug("Changed from MARKITWIRE to '%s'" % trade.Acquirer().Name())

    def set_counterparty_by_clearing_broker(self, trade):
        alias = acm.FPartyAlias.Select01('alias="%s" and type="MarkitWireID"' % self.swClearingBroker_partyId,
                                         "More than one party has alias: %s" % self.swClearingBroker_partyId)

        if alias:
            log_debug("Setting counterparty to Clearing Broker: %s" % alias.Party().Name())
            trade.Counterparty(alias.Party())
        else:
            log_error("Could not find Clearing Broker with MarkitWireID: %s" % self.swClearingBroker_partyId)

    def build_external_id(self):
        return "MW%sV%sP%s" % (self.tradeId, self.swTradeVersionId, self.swPrivateDataVersionId)

    def set_external_id(self, trade):
        external_id = self.build_external_id()

        if self.swParticipantId_traderA == self.swParticipantId_traderB:
            my_uuid = str(uuid4())
            trade.OptionalKey("%s:%s" % (external_id, my_uuid[0:4]))
        else:
            trade.OptionalKey(external_id)

        if self.swAmendmentType == "PartialTermination":
            log_debug("Setting contract external_id to '%s_pt'" % external_id)
            trade.Contract().OptionalKey("%s_pt" % external_id)
            self.manage_trade(trade.Contract())

    def set_deal_dates_by_trade_date(self, trade):
        set_trade_dates(trade, self.tradeDate)

    def set_deal_dates_by_effective_date(self, trade):
        message_time = self.swTradeVersionTimestamp.replace("T", " ")[:-1]
        set_trade_dates(trade, self.swModificationEffectiveDate, message_time)

    def set_clearing_attributes(self, trade):
        if self.swTradeStatus == "New-Clearing":
            if trade.Counterparty() == trade.AdditionalInfo().CCPclr_broker_ptynb():
                ais = acm.FAdditionalInfoSpec["CCPoriginal_counter"]
                trade.AddInfoValue(ais, trade.Counterparty())

    def move_broker_fee(self, trade):
        payment_types = ("Broker Fee",)
        payments = find_payments_by_type(trade, payment_types)
        if len(payments) > 1:
            log_warning("Trade %i has multiple broker fees! This may produce unexpected results." % trade.Oid())

        if self.swBrokerageAmount and abs(float(self.swBrokerageAmount)) > 0.009:
            currency = acm.FInstrument[self.swBrokerageAmountCcy]
            pay_day = roll_date_to_next_month(trade.ValueDay(), 10, currency)
            fee_description = "%s%.2f on %s" % (self.swBrokerageAmountCcy, float(self.swBrokerageAmount), pay_day)
            if payments:
                log_debug("Updating Broker Fee to %s for trade %i" % (fee_description, trade.Oid()))
            else:
                log_debug("Adding Broker Fee of %s for trade %i" % (fee_description, trade.Oid()))

            payment = payments[0] if payments else trade.CreatePayment()
            payment.Type("Broker Fee")
            payment.Party(trade.Broker())
            payment.Currency(currency)
            payment.Amount(-float(self.swBrokerageAmount))
            payment.PayDay(pay_day)
        else:
            if payments:
                log_debug("Removing Broker Fee(s) from trade %i" % trade.Oid())
                delete_payments_by_type(trade, payment_types)

        if trade.Fee():
            trade.Fee(0.0)

    def set_val_group(self, trade):
        is_clearing = False
        if trade.AdditionalInfo().CCPclearing_process().startswith("LCH"):
            is_clearing = True

        val_group_name = get_csa_val_group(trade, is_clearing)
        if not val_group_name:
            log_debug("[ValGroup] No ValGroup identified for trade.")
        else:
            current = trade.Instrument().ValuationGrpChlItem()
            if not current or current.Name() != val_group_name:
                val_group = find_val_group(val_group_name)
                if val_group:
                    log_debug("Setting ValGroup to %s" % val_group_name)
                    trade.Instrument().ValuationGrpChlItem(val_group)
                else:
                    log_error("Invalid ValGroup: %s" % val_group_name)

    def set_add_infos(self, addinfo_dict, trade):
        # setting the instrument override for clearing trades
        if self.swTradeStatus == "New-Clearing":
            addinfo_dict["InsOverride"] = "Interest Rate Future"
            addinfo_dict["ClearedTrade"] = "Yes"
        elif self.swTradeStatus == "Clearing":
            # Set the clearing flag and original counterparty
            message_statuses = swml_all_nodes(self.swml,
                                              "SWML.swNegotiation.swDialog.swTraderMessage.swMessageStatus")
            if "ClearingRegistered" in message_statuses:
                addinfo_dict["ClearedTrade"] = "Yes"

        if self.swClearingStatus == "Registered":
            addinfo_dict["CCPccp_status"] = "Registered"

        if self.swClearingBroker_partyName:
            addinfo_dict["Clearing Member"] = self.swClearingBroker_partyName
        if self.swClearingHouse_partyId:
            addinfo_dict["ClearingHouseId"] = self.swClearingHouse_partyId
        if self.swClearingBroker_partyId:
            addinfo_dict["ClearingMemberCode"] = self.swClearingBroker_partyId
        if self.swAdditionalField5:
            addinfo_dict["MarkitWire"] = self.swAdditionalField5
        if self.party_partyId:
            addinfo_dict["Source Ctpy Name"] = self.party_partyId
        if self.swPrivateTradeId:
            addinfo_dict["Source Trade Id"] = self.swPrivateTradeId
        elif self.swBlockTradeId:
            addinfo_dict["Source Trade Id"] = self.swBlockTradeId

        # MW_TradeUpdated is used for a condition in MarkitWire_Listener ATS code
        addinfo_dict["MW_TradeUpdated"] = "True"
        addinfo_dict["FRA Discounting"] = "True"

        # LAS add infos
        try:
            from las_util import get_add_info_values
            las_dict = get_add_info_values(trade.Oid())
            addinfo_dict.update(las_dict)
        except Exception as ex:
            print("Failed to process las_util.get_add_info_values function. LAS add infos can not be updated.")
            return

    def set_add_infos_on_trade(self, trade):
        output = []
        add_infos = {}
        self.set_add_infos(add_infos, trade)
        for key, value in list(add_infos.items()):
            ais = acm.FAdditionalInfoSpec.Select01('fieldName="%s" and recType="Trade"' % key,
                                                   "Too many AddInfo specifications for field %s" % key)

            if ais:
                previous = str(trade.AddInfoValue(ais))
                if previous == value:
                    output.append("AddInfo '%s' already set to '%s'" % (key, value))
                else:
                    if previous:
                        output.append("Setting AddInfo '%s' to '%s' (was: '%s')" % (key, value, previous))
                    else:
                        output.append("Setting AddInfo '%s' to '%s'" % (key, value))
                    trade.AddInfoValue(ais, value)
            else:
                output.append("Could not find AddInfo '%s'" % key)

        if output:
            log_debug("Processing AddInfos:\n  " + "\n  ".join(output))

    # noinspection PyMethodMayBeStatic
    def _find_closing_trade(self, original_trade, new_trade):
        mw_id = original_trade.AdditionalInfo().CCPmiddleware_id()
        version = get_markitwire_major_version(new_trade)
        r = find_closing_trades_by_markitwire_id(mw_id, None, version)

        # Could be a mirror, filter trades by side
        side = original_trade.AdditionalInfo().Mwire_sideid()
        r = [t for t in r if t.AdditionalInfo().Mwire_sideid() == side]

        if not r:
            return None
        elif len(r) > 1:
            raise Exception("Multiple closing trades with MW ID: %s_closing" % mw_id)

        return r[0]

    def _create_closing_trade(self, original_trade, new_trade):
        # Partial terminations and partial novations do not generate an equal-opposite trade,
        # so we need to create one ourselves.
        add_info_to_remove = ("CCPclearing_process",
                              "CCPclearing_status",
                              "CCPmwire_booking_st",
                              "CCPmwire_contract_s",
                              "CCPmwire_message_st",
                              "CCPmwire_new_status",
                              "CCPmwire_process_st")

        payments_to_remove = ("Broker Fee",
                              "Premium",
                              "Cash",
                              "Termination Fee",
                              "Cancellation Fee")

        log_debug("Creating closing trade from: %i" % original_trade.Oid())

        closing_trade = original_trade.Clone()
        self.manage_trade(closing_trade)

        closing_trade.Type(AMWI_TYPE_CLOSING)
        closing_trade.Status(AMWI_STATUS_TERMINATED)
        closing_trade.OptionalKey("")
        closing_trade.Nominal(-1.0 * original_trade.Nominal())
        closing_trade.MirrorTrade(None)
        self.set_deal_dates_by_effective_date(closing_trade)

        new_id = "%s_closing" % original_trade.AdditionalInfo().CCPmiddleware_id()
        closing_trade.AdditionalInfo().CCPmiddleware_id(new_id)

        version = get_markitwire_major_version(new_trade)
        closing_trade.AdditionalInfo().CCPmiddleware_versi("<%i\\0>" % int(version))

        delete_addinfos(closing_trade, add_info_to_remove)

        delete_payments_by_date(closing_trade, closing_trade.AcquireDay())
        delete_payments_by_type(closing_trade, payments_to_remove)
        reverse_payments(closing_trade, ["Termination Fee"])

        return closing_trade

    def do_full_termination(self, trade):
        # Terminations copy all fees from prior partial terminations. We don't want this.
        delete_payments_by_type(trade, ["Termination Fee"], None, "PartialTermination")
        delete_payments_by_type(trade, ["Premium", "Cash"], acm.Time.DateToday())
        self.set_deal_dates_by_effective_date(trade)

    def do_full_novation(self, trade):
        trade.Type(AMWI_TYPE_CLOSING)
        alter_payment_type(trade, "Assignment Fee", "Termination Fee")
        self.set_deal_dates_by_effective_date(trade)

        if trade.Instrument().InsType() == "CurrSwap" and abs(trade.Quantity()) != 1.0:
            log_debug("Detected invalid quantity %f, setting to 1.0...." % trade.Quantity())
            trade.Quantity(1.0 if trade.Quantity() > 0.0 else -1.0)

    def do_partial_termination(self, trade):
        if trade.IsInfant():
            closing_trade = self._create_closing_trade(trade.Contract(), trade)
            set_message_status(closing_trade, "Released")

            move_payments_by_type(trade, closing_trade, ["Termination Fee"])
            delete_payments_by_type(trade, ["Premium", "Cash"], closing_trade.AcquireDay())
        else:
            delete_payments_by_type(trade, ["Termination Fee"])

        # Have to set contract status to Terminated here. Otherwise it gets set to Void.
        log_debug("Setting status of %i to %s" % (trade.Contract().Oid(), AMWI_STATUS_TERMINATED))
        trade.Contract().Status(AMWI_STATUS_TERMINATED)
        self.manage_trade(trade.Contract())

        if self.swPrivateBookingState == "Released":
            set_instrument_start(trade.Instrument(), self.swModificationEffectiveDate)

    def do_partial_novation(self, trade):
        alter_payment_type(trade, "Assignment Fee", "Termination Fee")
        self.set_deal_dates_by_effective_date(trade)
        if trade.IsInfant():
            closing_trade = self._create_closing_trade(trade.Contract(), trade)
        else:
            closing_trade = self._find_closing_trade(trade.Contract(), trade)

        if closing_trade:
            set_message_status(closing_trade, get_message_status(trade))
            move_payments_by_type(trade, closing_trade, ["Termination Fee"])

        # Core code creates an offsetting trade with the outgoing amount.
        # ABSA want a closing trade and the new trade to have the remaining amount.
        ins_type = trade.Instrument().InsType()
        nominal = None
        if ins_type == "FRA":
            nominal = float(self.fra_amount)
        elif ins_type == "Swap":
            nominal = float(self.swap_initialValue)

        if nominal:
            if trade.Nominal() > 0.0:
                nominal *= -1.0

            log_debug("Setting trade %i nominal from %.2f to %.2f" % (trade.Oid(),
                                                                      trade.Nominal(),
                                                                      nominal))
            trade.Nominal(nominal)


def import_entry_safe(swml, user_dictionary):
    log_in_method()

    swml_message = SwmlMessage(swml)

    log_debug("IN_METHOD importEntry Trade: %s" % swml_message.get_trade_description())
    log_debug("IN_METHOD importEntry SWML details:\n%s" % swml_message.describe())

    if swml_message.swMessageText == "BYPASS":
        log_debug("Trade BYPASSED")
        return user_dictionary

    swml_message.write_swml()

    # Mirror trades cause all sorts of issues with cancellations
    trade_version = int(swml_message.swTradeVersionId)
    if trade_version > 1 and swml_message.swPrivateBookingState != "Released":
        remove_mirrors(swml_message.tradeId, trade_version - 1)

    # We only reject the message after logging and writing the source XML in case
    # we need to debug the issue later.
    if swml_message.should_ignore_trade():
        return None

    user_dictionary["FParty"] = {"Swift": "ABSAZAJJ_PB"}

    return user_dictionary


def _import_exit_bugfixes(trade):
    """
        Some odd behaviours were encountered during testing that
        appear to be specific to the ABSA 2017.1 environment. These fixes
        resolve the problem, but we are not sure why these are necessary.
        Delete when able.
    """
    # Initialize all ABSA trades in Front Arena for Markit Wire as Normal
    if trade.IsInfant():
        if trade.Type() == "None":
            trade.Type(AMWI_TYPE_NORMAL)

    ins_type = trade.Instrument().InsType()
    if ins_type == "FRA":
        # For some reasons FRAs default to short stubs, which is not
        # how they work in the real world.
        for leg in trade.Instrument().Legs():
            leg.LongStub(True)
            leg.StubHandling("None")
    elif ins_type == "Swap":
        for leg in trade.Instrument().Legs():
            # Always set StubHandling to None for Swaps
            # - this should be done independantly if the 
            #   trade is a infant or not to make it does not 
            #   get reset to something else.
            # - code below will generate cashflows for infant 
            #   trades, not necessary if not infant.
            leg.StubHandling("None")

        if trade.IsInfant():
            # trade.Nominal() does not work properly until there are cashflows.
            # This can cause the quantity to be set to 0.0 on new trades
            #
            # Issues this fixes can also be fixed by setting FParameter:
            #   FSWML_ALWAYS_POSITIVE_SWAP_NOMINAL=True
            for leg in trade.Instrument().Legs():
                if len(leg.CashFlows()) == 0:
                    leg.GenerateCashFlowsFromDate(leg.StartDate())


def estimated_clearer_broker_fee(trade):
    trade_portfolio = [5059]
    trade_date = acm.Time.DateAdjustPeriod(trade.AcquireDay(), '2d')
    day_of_week = acm.Time.DayOfWeek(trade_date)
    if day_of_week == 'Saturday':
        trade_date = acm.Time.DateAdjustPeriod(trade.AcquireDay(), '2d')
    elif day_of_week == 'Sunday':
        trade_date = acm.Time.DateAdjustPeriod(trade.AcquireDay(), '1d')

    if trade.Portfolio().Oid() in trade_portfolio:
        pay = acm.FPayment()
        pay.Party(trade.Counterparty())
        pay.PayDay(trade_date)
        pay.Type('Broker Fee')
        pay.Currency('USD')
        pay.Amount(-375.00)
        pay.Text('LCH booking fee')
        trade.Payments().Add(pay)


# noinspection PyUnusedLocal
def import_exit_safe(trade, swml, user_dictionary):
    del user_dictionary

    log_in_method_trade(trade)

    swml_message = SwmlMessage(swml)

    log_debug("IN_METHOD importExit Trade: %s" % swml_message.get_trade_description())

    if swml_message.swMessageText == "BYPASS":
        log_debug("Trade BYPASSED")
        return trade

    if swml_message.should_ignore_trade():
        return None

    _import_exit_bugfixes(trade)

    # Cross Currency Basis Swaps might not have the correct FX rate if
    # no initial nominal is specified in Markitwire.
    if is_problem_basis_swap(trade):
        log_debug("*** Detected XCcy Basis Swap with invalid FX fixing ***")
        fix_basis_swap(trade)

    # AddInfos used to be set by using a dictionary. But this no longer works,
    # so we set AddInfos using the same dictionary.
    swml_message.set_add_infos_on_trade(trade)

    # Business would like the trade/value dates to match the trade date in the swml.
    swml_message.set_deal_dates_by_trade_date(trade)

    # Cleared trades should use the ClearingBroker and not the ClearingHouse to identify the counterparty
    # TODO: Could be fixed by AR733812
    if swml_message.swTradeStatus == "New-Clearing":
        swml_message.set_counterparty_by_clearing_broker(trade)

    # Set the broker name through mappings. This is worth a static data evaluation between Markit Wire and Front Arena
    swml_message.set_broker(trade)

    # Trades sent to MW from Bloomberg store the user name in a different location
    if swml_message.swUserId == "ABSA_SYSTEM_DEFAULT_USER":
        swml_message.set_bloomberg_trader(trade)

    # Set the default portfolio if the portfolio does not match
    swml_message.set_portfolio(trade)

    # Set the acquirer if not matched from Markit Wire
    swml_message.set_acquirer(trade)

    # OptKey3 is used to suppress execution fee calc in FA (ref:Jakub Tomaga)
    if swml_message.swAdditionalField_TradeKey3 == "PS No Fees":
        trade.OptKey3("PS No Fees")

    if swml_message.swTradeStatus == "Cancelled":
        swml_message.do_full_termination(trade)
    elif swml_message.swTradeStatus == "Novated":
        swml_message.do_full_novation(trade)
    elif swml_message.swTradeStatus == "Amended":
        delete_duplicate_payments_on_trade(trade)
        if swml_message.swAmendmentType == "PartialTermination":
            swml_message.do_partial_termination(trade)
    elif swml_message.swTradeStatus == "Novated-Partial":
        swml_message.do_partial_novation(trade)

    # Solution for Instrument > RollingPeriodBase date
    if trade.Instrument().InsType() == 'CurrSwap':
        for leg in trade.Instrument().Legs():
            leg.RollingPeriodBase(swml_message.curr_swap_rollDate)
            log_debug("Instrument Roll Date: %s" % leg.RollingPeriodBase())

    # Set the valuation groups of the trades using ABSA's own special algorithm
    swml_message.set_val_group(trade)

    # If the trade is eligible for clearing then set the clearing attributes
    swml_message.set_clearing_attributes(trade)

    # ABSA need broker fees to appear as a payment
    if trade.Broker():
        swml_message.move_broker_fee(trade)

    estimated_clearer_broker_fee(trade)

    if trade.Contract() and trade.Contract().IsInfant():
        swml_message.commit_trades_excluding([trade, trade.Contract()])
    else:
        swml_message.commit_trades_excluding([trade])

    # If we release an allocation trade before the portfolio is assigned, we will never fix it.
    if swml_message.swTradeStatus == "New-Allocation" and swml_message.swPrivateBookingState == "Released":
        if is_allocate_trade(trade):
            log_debug("Allocation trade is released but still in an allocation portfolio. Skipping...")
            return None

    return trade


# noinspection PyPep8Naming
def importEntry(swml, user_dictionary):
    return_dict = user_dictionary
    try:
        return_dict = import_entry_safe(swml, user_dictionary)
    except Exception as x:
        log_error("Exception in importEntry: %s" % str(x))
        print_exc()

    return return_dict


# noinspection PyPep8Naming
def importExit(trade, swml, user_dictionary):
    return_trade = None
    try:
        return_trade = import_exit_safe(trade, swml, user_dictionary)
    except Exception as x:
        log_error("Exception in importExit: %s" % str(x))
        print_exc()

    return return_trade


# noinspection PyPep8Naming,PyUnusedLocal
def getStateChartOverride(swmlParser):
    return None

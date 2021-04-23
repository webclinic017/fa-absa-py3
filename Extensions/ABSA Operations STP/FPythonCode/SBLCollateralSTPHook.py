"""---------------------------------------------------------------------------------------------------------------------
MODULE
    SBLCollateralSTPHook

DESCRIPTION
    This module contains STP logic for the SBL Collateral trades.

------------------------------------------------------------------------------------------------------------------------
HISTORY
========================================================================================================================
Date            Change no       Developer               Requester               Description
------------------------------------------------------------------------------------------------------------------------
2019-04-05      FAOPS-466       Hugo Decloedt           Gasant Thulsie          STP for fixed cash flows on SBL trades.
2020-02-26      PCGDEV-10       Sihle Gaxa              James Stevens           Added auto BO Confirmation class for
                                                        Shaun De Plessis        both SBL and Collateral trades
2020-07-08      PCGDEV-494      Sihle Gaxa              James Stevens           Added line to destroy simulated object
2020-10-15      PCGDEV-598      Sihle Gaxa              Shaun Du Plessis        Added STP for SBL ACS dual bookings
2020-11-19      PCGDEV-623      Sihle Gaxa              Shaun Du Plessis        Update loan end date to one business 
                                                                                day in the future from start date
2021-02-24      PCGDEV-673      Sihle Gaxa              Shaun Du Plessis        Added logic to check if loan has 
                                                                                already been created
------------------------------------------------------------------------------------------------------------------------
"""

import acm

from at_logging import getLogger
import sbl_booking_utils as sbl_utils

from sl_partial_returns import partial_return
from OperationsSTPHook import OperationsSTPHook
from PCG_SBL_Autoconfirm_FO_Trades import PCGAutoConfirmation
import OperationsSTPFunctions


LOGGER = getLogger(__name__)
VALID_TRADE_STATUS = ["BO Confirmed", "BO-BO Confirmed"]


class SBLCollateralSTPHook(OperationsSTPHook):
    """
    Definition of a hook used to perform STP triggered by the update or creation of a fixed cash flow on a SBL trade.
    """

    def Name(self):
        """
        Get the name of the Operations STP Hook.
        """
        return 'Matched SBL Collateral Auto Release STP Hook'

    def IsTriggeredBy(self, eventObject):
        """
        Determines the trigger conditions for auto-release
        """

        if not eventObject.IsKindOf(acm.FSettlement):
            return False

        settlement = eventObject
        instrument = settlement.Instrument()
        trade = settlement.Trade()

        if settlement.Status() != 'Authorised':
            return False
        if not trade or not instrument:
            return False
        if instrument.SettleCategoryChlItem().Name() != 'Collateral':
            return False
        if instrument.InsType() != 'Deposit':
            return False
        if instrument.Currency().Name() != 'ZAR':
            return False
        if not instrument.IsCallAccount():
            return False
        if instrument.Legs().First().LegType() != 'Call Fixed Adjustable':
            return False
        if trade.Acquirer().Name() != 'PRIME SERVICES DESK':
            return False
        if settlement.Type() != 'Fixed Amount':
            return False
        if settlement.ValueDay() != acm.Time.DateToday():
            return False
        if trade.Status() not in VALID_TRADE_STATUS:
            return False
        if self._is_duplicate_cashflow(trade, settlement):
            return False
        if not OperationsSTPFunctions.is_outgoing_settlement(settlement):
            return False
        if trade.AdditionalInfo().Funding_Instype() != 'CALL_EQ_Funding':
            return False
        instrument_external_id = instrument.ExternalId1()
        global_one_party_code = trade.Counterparty().AdditionalInfo().SL_G1PartyCode()
        if instrument_external_id != global_one_party_code:
            return False

        return True

    def _is_duplicate_cashflow(self, trade, settlement):
        """
        Checks if this is a duplicate cashflow
        """
        seen = set()
        LOGGER.info("Performing duplicate check")
        instrument = trade.Instrument()
        value_day = settlement.ValueDay()
        amount = round(settlement.Amount(), 4)
        current_cashflow = (amount, value_day)
        for cashflow in instrument.Legs().First().CashFlows():
            cashflow_amount = round(cashflow.FixedAmount(), 4)
            existing_cf = (cashflow_amount, cashflow.PayDate())
            if not existing_cf in seen:
                seen.add(existing_cf)
            else:
                if existing_cf == current_cashflow:
                    LOGGER.info("Duplicate cashflow {id} will remain in Authorised".format(
                                id=cashflow.Oid()))
                    return True
        return False


    def PerformSTP(self, settlement):
        """
        Perform the hooks STP action/s for an event on the specified
        object.

        Please note that the action does not necessarily occur to the
        event object itself but may occur to some related object/s.
        """
        OperationsSTPFunctions.release_settlement(settlement)


class SBLAutoBOConfirmSTPHook(OperationsSTPHook):
    """
    Definition of a hook used to perform STP triggered
    by creation of a Collateral or SBL trade in FO Confirmed status.
    """

    def Name(self):
        """
        Get the name of the Operations STP Hook.
        """
        return "SBL Auto BO-Confirm Trades STP Hook"

    def IsTriggeredBy(self, eventObject):

        if not eventObject.IsKindOf(acm.FTrade):
            return False

        trade = eventObject
        portfolio = trade.Portfolio()
        instrument = trade.Instrument()

        if not trade.Status() == "FO Confirmed":
            return False

        if not trade.Acquirer().Name() == sbl_utils.ACQUIRER.Name():
            return False

        if not instrument.InsType() in sbl_utils.SBL_INSTRUMENTS:
            return False

        if instrument.InsType() == "SecurityLoan":
            if not trade.match_portfolio(sbl_utils.AUTO_BO_LOAN_PORTFOLIO):
                return False
            sbl_engine = PCGAutoConfirmation([trade])
            sbl_engine.verify(trade)
            if sbl_engine.print_errors():
                LOGGER.info(sbl_engine.print_errors())
                return False

        elif not is_collateral_trade(trade):
            return False

        return True

    def PerformSTP(self, trade):
        """
        Auto BO Confirm trades that meet the above criteria
        """
        acm.PollAllEvents()
        acm.AMBAMessage.DestroySimulatedObject(trade)
        if trade.Instrument().InsType() == "SecurityLoan":
            sbl_engine = PCGAutoConfirmation([trade])
            sbl_engine.confirm()
        else:
            OperationsSTPFunctions.bo_confirm_trade(trade)


class SBLDualBookingSTPHook(OperationsSTPHook):
    """
    Definition of a hook used to perform STP triggered
    by creation of a Collateral or SBL trade in FO Confirmed status.
    """

    def Name(self):
        """
        Get the name of the Operations STP Hook.
        """
        return "SBL Collateral Dual Booking STP Hook"

    def IsTriggeredBy(self, eventObject):

        if not eventObject.IsKindOf(acm.FTrade):
            return False

        trade = eventObject
        instrument = trade.Instrument()

        if trade.Acquirer().Name() != sbl_utils.ACQUIRER.Name():
            return False

        if instrument.InsType() not in sbl_utils.SBL_INSTRUMENTS:
            return False

        if not is_collateral_trade(trade):
            return False

        if trade.Counterparty().Name() != "SLB ACS MAIN":
            return False

        if trade.Text1() in ["PARTIAL_RETURN", "FULL_RETURN"]:
            return False

        if trade.Status() not in ["BO Confirmed", "Terminated", "Void"]:
            return False

        return True

    def PerformSTP(self, trade):
        """
        Update ACS security loan positions based on collateral trade event
        """
        try:
            LOGGER.info("Processing trade {trd}".format(trd=trade.Oid()))
            
            trade_date = trade.ConnectedTrade().ValueDay()
            start_date = acm.Time.DateAddDelta(trade_date, 0, 0, 0)
            end_date = sbl_utils.CALENDAR.AdjustBankingDays(trade_date, 1)
            if trade.Text1() == "" and trade.Status() == "BO Confirmed":
                acs_loan_trades = sbl_utils.get_acs_loans()
                for acs_loan_trade in acs_loan_trades:
                    if acs_loan_trade.Text2().replace(",", "") == str(trade.Oid()):
                        return
                self._create_on_tree_loan(trade, start_date, end_date)
            elif trade.Status() in ["Terminated", "Void"]:
                is_voided = True if trade.Status() == "Void" else False
                self._decrease_loan_position(trade, start_date, is_voided)
        except Exception as e:
            LOGGER.exception("Could not process collateral trade because \
                             {error}".format(error=str(e)))

    def _create_on_tree_loan(self, trade, start_date, end_date, trade_value=None):
        """
        Create duplicate loan trade in ACS On-tree portfolio
        """
        previous_day = sbl_utils.CALENDAR.AdjustBankingDays(sbl_utils.TODAY, -1)
        previous_date = acm.Time.DateAddDelta(previous_day, 0, 0, 0)
        instrument = trade.Instrument()
        ref_price = instrument.UsedPrice(previous_date,
                                         instrument.Currency(),
                                         sbl_utils.MARKET.Name())
        loan_creator = sbl_utils.SBLLoanCreator(trade, ref_price,
                                                start_date, end_date,
                                                trade_value)
        loan_instrument = loan_creator.create_instrument()
        if loan_instrument:
            loan_trade = loan_creator.create_trade(loan_instrument)
            if loan_trade:
                LOGGER.info("Loan {loan} successfully booked".format(
                            loan=loan_trade.Oid()))

    def _decrease_loan_position(self, coll_trade, loan_date,
                                is_voided=None, quantity=None):
        """
        Decrease loan position to reflect corresponding collateral position
        """
        existing_loans = self._get_existing_loans(coll_trade)
        coll_value = self._get_trade_value(coll_trade, quantity)
        if existing_loans:
            equal_loan_trade = self._get_equal_loan(coll_value, existing_loans)
            if equal_loan_trade:
                self._terminate_loan(equal_loan_trade, loan_date, is_voided)
                return
            else:
                for loan_trade in existing_loans:
                    loan_value = round(loan_trade.FaceValue(), 0)
                    if abs(loan_value) > abs(coll_value):
                        self._generate_partial_return(loan_trade, loan_date, coll_value)
                        return
                self._bulk_terminate_loans(coll_value, existing_loans,
                                          loan_date, is_voided)
        else:
            self._reconcile_portfolio_positions()

    def _get_existing_loans(self, coll_trade):
        existing_loans = []
        acs_loan_trades = sbl_utils.get_acs_loans()
        if acs_loan_trades:
            for acs_loan_trade in acs_loan_trades:
                if self._is_valid_loan(coll_trade, acs_loan_trade):
                    existing_loans.append(acs_loan_trade)
        return existing_loans

    def _is_valid_loan(self, coll_trade, acs_loan_trade):
        coll_instrument = coll_trade.Instrument()
        acs_loan_instrument = acs_loan_trade.Instrument()
        acs_loan_underlying = acs_loan_instrument.Underlying()
        if (acs_loan_instrument.InsType() == "SecurityLoan" and
            acs_loan_trade.Direction() == coll_trade.Direction() and
            acs_loan_instrument.OpenEnd() == "Open End" and
            acs_loan_underlying.InsType() == "Stock" and
            acs_loan_underlying.Name() == coll_instrument.Name()):
                return True
        return False

    def _get_trade_value(self, trade, quantity=None):
        trade_value = trade.FaceValue()
        if quantity:
            return round(quantity, 0)
        return round(trade_value, 0)

    def _get_equal_loan(self, coll_value, existing_loans):
        for loan_trade in existing_loans:
            loan_value = round(loan_trade.FaceValue(), 0)
            if loan_value == coll_value:
                return loan_trade

    def _terminate_loan(self, loan_trade, loan_date, is_voided):
        LOGGER.info("Terminating loan {loan}".format(loan=loan_trade.Oid()))
        loan_instrument = loan_trade.Instrument()
        if loan_instrument.StartDate() > loan_date:
            loan_date = loan_instrument.StartDate()
        sbl_utils.terminate_trade(loan_trade, loan_date)
        self._void_loan(loan_trade, is_voided)
        LOGGER.info("Sec loan {trade} successfully terminated on {date}".format(
                    trade=loan_trade.Oid(), date=loan_date))

    def _void_loan(self, loan_trade, is_voided):
        if is_voided:
            loan_trade.Status("Void")
            loan_trade.Commit()
            LOGGER.info("{trade} successfully voided".format(
                        trade=loan_trade.Oid()))

    def _generate_partial_return(self, loan_trade, loan_date, coll_value):
        loan_instrument = loan_trade.Instrument()
        if loan_instrument.StartDate() > loan_date:
            loan_date =  loan_instrument.StartDate()
        LOGGER.info("Partially returning {trade} with {amount}".format(
                    trade=loan_trade.Oid(), amount=coll_value))
        new_loan = partial_return(loan_trade, loan_date, coll_value)
        new_loan.Commit()
        LOGGER.info("Partial return {trade} successfully created".format(
                    trade=new_loan.Oid()))

    def _bulk_terminate_loans(self, coll_value, existing_loans, loan_date, is_voided):
        """
        Terminate and partially return all loans that sum up to collateral amount
        """
        for loan_trade in existing_loans:
            loan_value = round(loan_trade.FaceValue(), 0)
            difference = abs(loan_value) - abs(coll_value)
            if difference <= 0.0:
                LOGGER.info("Terminating {loan} with nominal {value}".format(
                            loan=loan_trade.Oid(), value=loan_value))
                self._terminate_loan(loan_trade, loan_date, is_voided)
                coll_value -= loan_value
            elif difference > 0.0 and coll_value:
                self._generate_partial_return(loan_trade, loan_date, coll_value)
                return
        if coll_value > 0:
            acm.PollAllEvents()
            self._reconcile_portfolio_positions()

    def _reconcile_portfolio_positions(self):
        LOGGER.info("Reconciling collateral and loan portfolio positions")
        acm.PollAllEvents()
        coll_trades = sbl_utils.get_collateral_trades()
        loan_portfolio = acm.FPhysicalPortfolio[5708]  # Collateral optimize
        loan_positions = sbl_utils.get_loan_positions(loan_portfolio)
        coll_positions = sbl_utils.get_coll_position(coll_trades)
        position_diff = loan_positions[0] - coll_positions[0]
        loan_instruments = loan_positions[1]
        coll_instruments = coll_positions[1]

        if not position_diff:
            LOGGER.info("Loan and collateral portfolios are in line")
            return
        self._update_loan_positions(coll_instruments, loan_instruments)

    def _update_loan_positions(self, coll_instruments, loan_instruments):
        acm.PollAllEvents()
        breaking_instruments = set(loan_instruments.items()) ^ set(coll_instruments.items())
        LOGGER.info("Instruments with differences between the two portfolios")
        LOGGER.info(breaking_instruments)
        LOGGER.info("="*100)

        breaking_positions = self._get_breaking_instruments(breaking_instruments,
                                                            coll_instruments, loan_instruments)
        if breaking_positions:
            acm.PollDbEvents()
            for instrument_name, instrument_value in breaking_positions.items():
                LOGGER.info("Processing {ins_name} with difference \
                            {diff}".format(ins_name=instrument_name, diff=instrument_value))
                coll_value = round(instrument_value, 0)
                coll_trade = sbl_utils.get_collateral_trade(instrument_name)
                if coll_trade and coll_value > 0.0:
                    self._decrease_loan_position(coll_trade, sbl_utils.TODAY, None, coll_value)
                elif coll_trade and coll_value < 0.0:
                    end_date = acm.Time.DateAddDelta(sbl_utils.TODAY, 0, 0, 1)
                    self._create_on_tree_loan(coll_trade, sbl_utils.TODAY,  end_date, -1*coll_value)
                else:
                    LOGGER.exception("No collateral trade booked against {ins}".format(ins=instrument_name))

    def _get_breaking_instruments(self, breaking_instruments, coll_instruments, loan_instruments):
        breaking_positions = {}
        end_date = acm.Time.DateAddDelta(sbl_utils.TODAY, 0, 0, 1)
        for breaking_instrument in breaking_instruments:
            instrument_name = breaking_instrument[0]
            if instrument_name not in list(coll_instruments.keys()):
                LOGGER.info("Terminating loans with underlying \
                            {ins_name}".format(ins_name=instrument_name))
                loan_trades = sbl_utils.get_loan_trades(instrument_name, loan_instruments)
                if loan_trades:
                    for loan_trade in loan_trades:
                        sbl_utils.terminate_trade(loan_trade, sbl_utils.TODAY)
            elif instrument_name not in list(loan_instruments.keys()):
                LOGGER.info("Booking new loan with underlying \
                            {ins_name}".format(ins_name=instrument_name))
                trade = sbl_utils.get_collateral_trade(instrument_name)
                if trade:
                    self._create_on_tree_loan(trade, sbl_utils.TODAY, end_date)
            else:
                breaking_amount = loan_instruments[instrument_name] - coll_instruments[instrument_name]
                if instrument_name not in list(breaking_positions.keys()):
                    breaking_positions[instrument_name] = breaking_amount
        LOGGER.info("Instruments with different values between the portfolios...")
        LOGGER.info(breaking_positions)
        LOGGER.info("="*100)
        return breaking_positions


def is_collateral_trade(trade):
    if not trade.match_portfolio(sbl_utils.COLLATERAL_PORTFOLIO):
        return False
    if not trade.TradeCategory() == sbl_utils.COLLATERAL_CATEGORY:
        return False
    if not trade.Instrument().InsType() in sbl_utils.COLLATERAL_INSTRUMENTS:
        return False
    return True

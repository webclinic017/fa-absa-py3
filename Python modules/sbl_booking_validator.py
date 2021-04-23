'''--------------------------------------------------------------------------------------
MODULE
    sbl_booking_validator

DESCRIPTION
    Date                : 2020-02-26
    Purpose             : Validation for collateral trade booking,
                          loan and collateral returns 
    Department and Desk : SBL and Collateral
    Requester           : Shaun Du Plessis, James Stevens
    Developer           : Sihle Gaxa
    JIRA                : PCGDEV-8

HISTORY
=========================================================================================
Date            JIRA no         Developer               Description
-----------------------------------------------------------------------------------------
2020-02-26      PCGDEV-8        Sihle Gaxa              Initial implementation.
2020-07-23      PCGDEV-538      Sihle Gaxa              Added validation to only have 
                                                        one valid return per SBL loan
2020-10-27      PCGDEV-604      Sihle Gaxa              Updated available collateral
                                                        validation to check against 
                                                        selected trades only

ENDDESCRIPTION
--------------------------------------------------------------------------------------'''
import acm
import sl_functions
import sbl_booking_utils as sbl_utils
import sbl_collateral_file_uploader as collateral_uploader


class ReturnValidator(object):

    def __init__(self, trade, return_date, return_quantity):

        self.trade = trade
        self.return_type = None
        self.instrument_leg = None
        self.return_date = return_date
        self.instrument = trade.Instrument()
        self.return_quantity = return_quantity
        self.counterparty = trade.Counterparty()
        self.instrument_type = trade.Instrument().InsType()

        if self.instrument_type == "SecurityLoan":
            self.return_type = "Loan"
            self.instrument_leg = trade.Instrument().Legs()[0]
            self.underlying_quantity = sl_functions.underlying_quantity(trade.Quantity(), trade.Instrument())
        elif self.instrument_type in sbl_utils.COLLATERAL_INSTRUMENTS:
            self.return_type = "Collateral"
        else:
            raise Exception("Invalid instrument type {ins_type} for return".format(
                            ins_type=self.instrument_type))

    def invalid_return_trade(self):
        if self.return_type == "Loan" and self.trade.Type() == "Closing":
            raise Exception("Cannot return on a Return trade {trade}".format(trade=self.trade.Oid()))
        elif self.return_type == "Collateral" and self.trade.Text1() in sbl_utils.RETURN_TYPES.values():
            raise Exception("Cannot return on a Return trade {trade}".format(trade=self.trade.Oid()))

    def invalid_return_instype(self):
        if self.return_type == "Loan" and self.instrument_type != "SecurityLoan":
            raise exception("Invalid instrument type for SecurityLoan return")
        elif self.return_type == "Collateral" and not (self.instrument_type in sbl_utils.COLLATERAL_INSTRUMENTS):
            raise Exception("You can only perform a collateral return on collateral instruments")

    def return_qty_not_zero(self):
        if self.return_quantity == 0.0:
            raise Exception("Return quantity cannot be zero")
            
    def invalid_quantity_amount(self):
        if not (float(self.return_quantity).is_integer()):
            raise Exception("Cannot return a fraction quantity {qty}".format(
                            qty=self.return_quantity))

    def invalid_trade_status(self):
        if not self.trade.Status() in ["BO Confirmed", "BO-BO Confirmed"]:
            raise Exception("Trade {trade} needs to be at least in BO Confirmed status".format(
                            trade=self.trade.Oid()))

    def is_open_ended(self):
        if self.return_type == "Loan" and self.instrument.OpenEnd() in ["Terminated", "None"]:
            raise Exception("Cannot create Partial Return on trade with Open End {status}".format(
                            status=self.instrument.OpenEnd()))

    def invalid_return_date(self):
        if self.return_type == "Loan" and self.return_date < self.instrument_leg.StartDate():
            raise Exception("Return date must be greater than the trades start date")
        if self.return_type == "Collateral" and self.return_date < self.trade.ValueDay():
            raise Exception("Return date must be greater than trade's value day = {value_day}".format(
                            value_day=self.trade.ValueDay()))

    def exceeds_available_amount(self, trades=None):
        if self.return_type == "Collateral":
            available_collateral = placed_collateral(self.instrument, self.counterparty, trades)
            print("Available collateral = ", available_collateral)
            if available_collateral == 0.00:
                raise Exception("{client} has no collateral available".format(
                                client=self.counterparty.Name()))
            if abs(available_collateral) < abs(self.return_quantity):
                raise Exception("Return quantity {qty} exceeds available collateral {collateral} for {client}".format(
                                qty=self.return_quantity, collateral=available_collateral, client=self.counterparty.Name()))

        elif self.return_type == "Loan":
            if self.return_quantity > 0 and round(self.underlying_quantity) < round(self.return_quantity):
                raise Exception("Return quantity must be less than the existing underlying quantity {qty}".format(
                                    qty=self.underlying_quantity))
            elif self.return_quantity < 0 and round(self.underlying_quantity) > round(self.return_quantity):
                raise Exception("Return quantity must be greater than the existing underlying quantity {qty}".format(
                                qty=self.underlying_quantity))

    def wrong_direction(self):
        if self.trade.Quantity() > 0 and self.return_quantity > 0:
            raise Exception("Return quantity must be negative")
        if self.trade.Quantity < 0 and self.return_quantity < 0:
            raise Exception("Return quantity must be positive")

    def return_on_same_parent(self):
        original_loan = self.trade.ContractTrade()
        existing_return = self.trade.ConnectedTrade()
        if (existing_return.Oid() != original_loan.Oid()):
            if existing_return.Status() != "Void":
                raise Exception("Please void trade {trd} before trying to book another return".format(trd=existing_return.Oid()))

    def is_full_return(self):
        if round(abs(self.return_quantity - self.underlying_quantity)) < 1:
            return True
        return False

    def is_collateral_full_return(self, trades):
        sum_returned_trades = 0.0
        for trade in trades:
            sum_returned_trades += trade.FaceValue()
        if abs(sum_returned_trades) == abs(self.return_quantity):
            return True
        return False
        
    def is_non_banking_day(self):
        if (sbl_utils.CALENDAR.IsNonBankingDay(None, None, self.return_date)):
            raise Exception("Return date {rtn_date} must be a banking day".format(rtn_date=self.return_date))

    def is_valid_loan_return(self):
        if (self.is_open_ended() or
            self.is_non_banking_day() or
            self.return_on_same_parent() or
            self.invalid_return_trade() or
            self.invalid_return_date() or
            self.return_qty_not_zero() or
            self.invalid_trade_status() or
            self.invalid_return_instype() or
            self.invalid_quantity_amount() or
            self.exceeds_available_amount()):
            return False
        return True

    def is_valid_collateral_return(self, trades):
        if (self.wrong_direction() or
            self.is_non_banking_day() or
            self.return_qty_not_zero() or
            self.invalid_return_trade() or
            self.invalid_return_date() or
            self.invalid_trade_status() or
            self.invalid_return_instype() or
            self.invalid_quantity_amount() or
            self.exceeds_available_amount(trades)):
            return True
        return False


def placed_collateral(instrument, client, trades):
    available_collateral = 0.00
    for trade in trades:
        available_collateral += trade.FaceValue()
    return available_collateral


def different_client(trades, counterparty):
    for trade in trades:
        trade_party = trade.Counterparty()
        if trade_party.Name() != counterparty.Name():
            raise Exception("You cannot return {party} and {parent} at the same time".format(
                            party=trade_party.Name(), parent=counterparty.Name()))

def different_instrument(trades, instrument):
    for trade in trades:
        trade_instrument = trade.Instrument()
        if trade_instrument.Name() != instrument.Name():
            raise Exception("You cannot return {ins} and {parent_ins} at the same time".format(
                            ins=trade_instrument.Name(), parent_ins=instrument.Name()))


class InputFileValidator(object):

    portfolio_status = ["Active"]

    failure_reason = {
                    "date_error": "Invalid input date",
                    "zero_quantity": "Quantity cannot be 0",
                    "status_error": "Invalid Front Arena status",
                    "quantity_error": "Quantity should be a number",
                    "portfolio_error": "Portfolio does not exist in Front Arena ",
                    "instrument_error": "Instrument does not exist in Front Arena",
                    "counterparty_error": "Counterparty does not exist in Front Arena",
                    "acquire_day_error": "Trade date cannot be after Acquire/Value day ",
                    "banking_day_error": "Trade date and Value day must be a banking day",
                    "custody_party_error": "Custody counterparty does not exist in Front Arena",
                    "additional_info_error": "Additional info with this SWIFT flag does not exist",
                    "parent_portfolio_error": "Portfolio does not belong to 'SBL_NONCASH_COLLATERAL' compound portfolio",
                    "inactive_portfolio_error": "Booking into an inactive portfolio, please ask TCU to activate portfolio",
                    "counterparty_name_error": "This is not a valid Collateral counterparty, name does not start with SLL, SLB or COLL"
                    }

    def __init__(self, _index, record_data):

        self.row_number = _index
        self.nominal = record_data['trade:FaceValue']
        self.status = str(record_data['trade:Status'])
        self.portfolio = str(record_data['trade:Portfolio'])
        self.instrument = str(record_data['trade:Instrument'])
        self.counterparty = str(record_data['trade:Counterparty'])
        self.swift_flag = str(record_data['trade:addinf:SL_SWIFT'])
        self.custody_counterparty = str(record_data['CustodyCounterparty'])
        self.trade_date = collateral_uploader.get_date(record_data['trade:TradeTime'])
        self.acquire_day = collateral_uploader.get_date(record_data['trade:AcquireDay'])

    def is_valid_instrument(self, error_rows):
        trade_instrument = acm.FInstrument[self.instrument]
        if trade_instrument:
            return trade_instrument
        error_rows[self.row_number] = self.failure_reason["instrument_error"]

    def is_valid_portfolio(self, error_rows):
        trade_portfolio = acm.FPhysicalPortfolio[self.portfolio]
        if not trade_portfolio:
            error_rows[self.row_number] = self.failure_reason["portfolio_error"]
            return

        if trade_portfolio.MemberLinks():
            trade_parent_portfolio = trade_portfolio.MemberLinks()[0].OwnerPortfolio().Name()
            if trade_parent_portfolio == sbl_utils.COLLATERAL_PORTFOLIO.Name():
                return trade_portfolio
        error_rows[self.row_number] = self.failure_reason["parent_portfolio_error"]

    def is_active_portfolio(self, error_rows):
        trade_portfolio = acm.FPhysicalPortfolio[self.portfolio]
        if (trade_portfolio.add_info('Portfolio Status') in self.portfolio_status):
            return trade_portfolio
        error_rows[self.row_number] = self.failure_reason["inactive_portfolio_error"]

    def is_valid_counterparty(self, error_rows):

        trade_counterparty = acm.FParty[str(self.counterparty)]
        if not trade_counterparty:
            error_rows[self.row_number] = self.failure_reason["counterparty_error"]
            return
        if not self.is_valid_counterparty_name(trade_counterparty.Name()):
            error_rows[self.row_number] = self.failure_reason["counterparty_name_error"]
            return
        if self.custody_counterparty:
            custody_counterparty = acm.FParty[self.custody_counterparty]
            if not custody_counterparty:
                error_rows[self.row_number] = self.failure_reason["custody_party_error"]
                return
            if not self.is_valid_counterparty_name(custody_counterparty.Name()):
                error_rows[self.row_number] = self.failure_reason["counterparty_name_error"]
                return
        return trade_counterparty

    def is_valid_counterparty_name(self, party_name):
        if (party_name.startswith('SLL') or party_name.startswith('SLB') or party_name.startswith('COLL')):
            return True
        return False

    def is_number(self, error_rows):
        if (isinstance(self.nominal, int) or isinstance(self.nominal, float)):
            return self.nominal
        error_rows[self.row_number] = self.failure_reason["quantity_error"]

    def is_not_zero(self, error_rows):
        if self.nominal == 0:
            error_rows[self.row_number] = self.failure_reason["zero_quantity"]
            return
        return self.nominal
    
    def is_valid_status(self, error_rows):
        valid_status = acm.FEnumeration["enum(TradeStatus)"].Enumerators()
        if self.status in valid_status:
            return self.status
        error_rows[self.row_number] = self.failure_reason["status_error"]

    def is_valid_swift_flag(self, error_rows):
        for choice in sbl_utils.SWIFT_FLAG:
            if self.swift_flag.upper() == choice.Name():
                return self.swift_flag
        error_rows[self.row_number] = self.failure_reason["additional_info_error"]
    
    def is_banking_day(self, error_rows):
        if not (sbl_utils.CALENDAR.IsNonBankingDay(None, None, self.trade_date) or 
                sbl_utils.CALENDAR.IsNonBankingDay(None, None, self.acquire_day)):
            return self.acquire_day
        error_rows[self.row_number] = self.failure_reason["banking_day_error"]

    def is_valid_value_day(self, error_rows):
        if self.trade_date <= self.acquire_day:
            return self.acquire_day
        error_rows[self.row_number] = self.failure_reason["acquire_day_error"]

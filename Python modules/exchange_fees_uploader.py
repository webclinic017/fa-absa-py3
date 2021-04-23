"""------------------------------------------------------------------------------------------
MODULE
    exchange_fees_uploader

DESCRIPTION
    Date                : 2016-11-11
    Purpose             : Uploads the SAFEX and YIELDX prices from a flat file from GCMS.
    Department and Desk : PCG
    Requester           : Ndiweni Phindile
    Developer           : Sihle Gaxa
    CR Number           : CHNG0005070235

HISTORY
==============================================================================================
Date            Change no       Developer          Description
----------------------------------------------------------------------------------------------
2018-04-12      CHG1000344020   Sihle Gaxa      Created a daily log report for all trades
                                                on the Exchange fees upload file
2020-11-10      PCGDEV-616      Sihle Gaxa      Added validation to skip un-mapped accounts
2021-03-05      PCGDEV-675      Sihle Gaxa      Merging prime and market's exchange fees
                                                upload processes

ENDDESCRIPTION
----------------------------------------------------------------------------------------------"""
import os
import acm
from datetime import datetime
from csv import DictReader, DictWriter

from at_logging import getLogger
from at_addInfo import save as save_add_info

from PS_TradeFees import _GetVATFactor
import FUploaderFunctions as Functions

FEE_DATA = {}
LOGGER = getLogger(__name__)
log_comments = {"zero_fee": "Payment amount is 0",
                "no_fee": "Skipping trade: No fee for trade",
                "fee_uploaded": "Trade successfully updated with fee",
                "fee_amended": "Amended existing payment with fee amount",
                "duplicate_amount": "Skipping trade: Duplicate fee amount",
                "duplicate_ref": "File has duplicate exchange reference on line",
                "missing_account": "Skipping trade: Trade is not mapped to a sub-account",
                "unmapped_account": "Skipping trade: SubAccount is not mapped to FA portfolio",
                "wrong_mapping": "Skipping trade: Trade portfolio is different from defined mapping",
                "no_portfolio": "Skipping trade: SubAccount mapped to a portfolio that does not exist in FA"}

ael_variables = Functions.get_ael_variables()
ael_variables.add("log_filename",
                  label="Log file name",
                  alt="Log file name followed by the run date specified")
ael_variables.remove(ael_variables[4])
ael_variables.add_directory("log_filepath",
                            label="Log directory",
                            multiple=True,
                            alt="Directory where log file will be written to."
                                "A date sub-folder in the form yyyy-mm-dd will"
                                "be automatically added.")
ael_variables.add("prime_trades",
                  label="Prime trades",
                  cls="FTrade",
                  multiple=True,
                  mandatory=False,
                  alt="Query folder containing Prime fee trades")
ael_variables.add("markets_trades",
                  label="Markets trades",
                  cls="FTrade",
                  multiple=True,
                  mandatory=False,
                  alt="Query folder containing Markets fee trades")


class FeeObject(object):

    def __init__(self,
                 exchange_ref,
                 client_code,
                 sub_acc_code,
                 exchange_fee,
                 clearing_fee,
                 commission_fee,
                 market_fee):
        self.exchange_ref = exchange_ref
        self.client_code = client_code
        self.sub_acc_code = sub_acc_code
        self.exchange_fee = exchange_fee
        self.clearing_fee = clearing_fee
        self.commission_fee = commission_fee
        self.market_fee = market_fee


def ael_main(dictionary):
    run_date = Functions.get_input_date(dictionary)
    input_filepath = Functions.get_file_path(dictionary, run_date)
    LOGGER.info("Processing input file {input_filepath} for {run_date}".format(
        input_filepath=input_filepath, run_date=run_date))
    prime_trades = dictionary["prime_trades"]
    markets_trades = dictionary["markets_trades"]
    is_itac_file = True if dictionary["log_filename"] == "ITAC_fees_log" else False
    exchange_trades = list(markets_trades) + list(prime_trades)
    with open(input_filepath, "r") as input_file:
        exchange_fees = get_fees(input_file, is_itac_file)
        if exchange_fees:
            upload_fee_data(exchange_trades, exchange_fees, run_date)
    if FEE_DATA:
        log_directory = create_log_directory(dictionary, run_date)
        write_file_data(log_directory)
        LOGGER.info("Populating log file  {log_path} with upload results".format(
            log_path=log_directory))
    LOGGER.info('Completed Successfully')


def get_fees(input_file, is_itac_file=False):
    dict_reader = DictReader(input_file)
    try:
        exchange_fees = {}
        for row in dict_reader:
            client_code = row["ClientCode"]
            sub_account_code = row["SubAccountCode"]
            exchange_ref = row["OriginalJSEReference"]
            exchange_fee = -float(row["NettExchangeFee"])
            clearing_fee = -float(row["NettClearingMemberFees"])
            commission_fee = -float(row["NettCommission"])
            if is_itac_file:
                commission_fee = -float(row["TotalAllocationCommission"])
            market_fee = -float(row["TotalFees"])
            if exchange_ref in exchange_fees:
                duplicate_ref_comment = "{comment} {line_num}".format(
                    comment=log_comments["duplicate_ref"],
                    line_num=dict_reader.line_num)
                exchange_ref = "{jse_ref}_{line}".format(jse_ref=exchange_ref, line=dict_reader.line_num)
                FEE_DATA[exchange_ref] = [duplicate_ref_comment, sub_account_code, client_code, None, 0]
            else:
                fee_object = FeeObject(exchange_ref, client_code, sub_account_code,
                                       exchange_fee, clearing_fee, commission_fee, market_fee)
                exchange_fees[exchange_ref] = [fee_object]
        return exchange_fees
    except ValueError as error:
        raise RuntimeError("Failed to read fees on line {line_num} because {error}".format(
            line_num=dict_reader.line_num, error=str(error)))


def upload_fee_data(exchange_trades, exchange_fees, run_date):
    try:
        for trade in exchange_trades:
            trade_ref = trade.Text1()
            trade_portfolio = trade.Portfolio().Name()
            LOGGER.info("Processing trade {trade} with exchange ref {exchange_ref}".format(
                trade=trade.Oid(), exchange_ref=trade_ref))
            if acm.Time().AsDate(trade.TradeTime()) == run_date and trade_ref:
                if trade_ref not in exchange_fees:
                    FEE_DATA[trade_ref] = [log_comments["no_fee"], "", "", trade, 0]
                    continue
                exchange_fee_object = exchange_fees[trade_ref][0]
                vat_factor = _GetVATFactor(trade)
                client_code, sub_acc_code, exchange_fee, \
                    clearing_fee, commission_fee, market_fee = get_fee_values(exchange_fee_object, vat_factor)
                if trade_portfolio.startswith("PB_"):
                    upload_prime_fees(trade, commission_fee * vat_factor, client_code)
                else:
                    check_fee_mapping(trade, sub_acc_code, client_code, trade_ref)
                    upload_market_fees(trade, market_fee, sub_acc_code, client_code)
                upload_add_info_fees(trade, exchange_fee, clearing_fee, commission_fee)
    except Exception as error:
        raise Exception("Failed to upload fee data because {error}".format(error=str(error)))


def get_fee_values(exchange_fee_object, vat_factor):
    client_code = exchange_fee_object.client_code
    sub_acc_code = exchange_fee_object.sub_acc_code
    exchange_fee = round((exchange_fee_object.exchange_fee / vat_factor), 2)
    clearing_fee = round((exchange_fee_object.clearing_fee / vat_factor), 2)
    commission_fee = round((exchange_fee_object.commission_fee / vat_factor), 2)
    market_fee = round(exchange_fee_object.market_fee, 2)
    return client_code, sub_acc_code, exchange_fee, clearing_fee, commission_fee, market_fee


def upload_prime_fees(trade, fee, client_code):
    LOGGER.info("Setting prime payment {fee} on trade {trade}".format(fee=fee, trade=trade.Oid()))
    payment_counterparty = acm.FParty[32737]  # PRIME SERVICES DESK
    add_payment(trade, fee, payment_counterparty, client_code)


def add_payment(trade, fee, counterparty, client_code, payment_type="Cash", payment_text=""):
    if is_fee_zero(trade, fee, payment_text, client_code):
        return
    trade_payments = get_payments(trade, payment_type, payment_text)
    if trade_payments:
        update_payment(trade, trade_payments, payment_text, client_code, fee)
    else:
        create_payment(trade, counterparty, fee, payment_type, payment_text, client_code)


def is_fee_zero(trade, fee, payment_text, client_code):
    if abs(round(fee, 2)) == 0.00:
        FEE_DATA[trade.Text1()] = [log_comments["zero_fee"], payment_text, client_code, trade, fee]
        return True
    return False


def get_payments(trade, payment_type, payment_text):
    trade_payments = [payment for payment in trade.Payments() if
                      payment.Type() == payment_type and payment.Text() == payment_text]
    return trade_payments


def update_payment(trade, trade_payments, payment_text, client_code, fee):
    payment = trade_payments[0]
    LOGGER.info("Updating existing payment from {old_fee} to {new_fee}".format(
            old_fee=payment.Amount(), new_fee=fee))
    payment.Amount(fee)
    payment.PayDay(trade.ValueDay())
    payment.ValidFrom(trade.ValueDay())
    payment.Commit()
    FEE_DATA[trade.Text1()] = [log_comments["fee_amended"], payment_text, client_code, trade, fee]


def create_payment(trade, counterparty, fee, payment_type, payment_text, client_code):
    payment = acm.FPayment()
    payment.Amount(fee)
    payment.Trade(trade)
    payment.Text(payment_text)
    payment.Type(payment_type)
    payment.Party(counterparty)
    payment.PayDay(trade.ValueDay())
    payment.ValidFrom(trade.TradeTime())
    payment.Currency(trade.Instrument().Currency())
    payment.Commit()
    FEE_DATA[trade.Text1()] = [log_comments["fee_uploaded"], payment_text, client_code, trade, fee]
    LOGGER.info("New payment of {amount} created for {trade}".format(amount=fee, trade=trade.Oid()))


def check_fee_mapping(trade, sub_acc_code, client_code, trade_ref):
    fa_portfolio_exists = False
    same_fa_portfolio_id = False
    market_fee_mapping = acm.FChoiceList["Markets_fee_mapping"].Choices()
    for fee_mapping in market_fee_mapping:
        mapping_acc_code = fee_mapping.Name().split(":")[0]
        mapping_portfolio_id = fee_mapping.Name().split(":")[1]
        if sub_acc_code == mapping_acc_code:
            fa_portfolio_exists = True
        if int(mapping_portfolio_id) == trade.Portfolio().Oid():
            same_fa_portfolio_id = True
    if not fa_portfolio_exists:
        FEE_DATA[trade_ref] = [log_comments["no_portfolio"], sub_acc_code, client_code, trade, 0]
        return
    if not same_fa_portfolio_id:
        FEE_DATA[trade_ref] = [log_comments["wrong_mapping"], sub_acc_code, client_code, trade, 0]


def upload_market_fees(trade, market_fee, sub_acc_code, client_code):
    payment_type = "Exchange Fee"
    LOGGER.info("Setting market payment type {type} with amount {fee} on trade {trade_id}".format(
        type=payment_type, fee=market_fee, trade_id=trade.Oid()))
    add_payment(trade, market_fee, trade.Counterparty(), client_code, payment_type, sub_acc_code)


def upload_add_info_fees(trade, exchange_fee, clearing_fee, commission_fee):
    LOGGER.info("Populating fees on trades add info fields")
    save_add_info(trade, "PS_ExchangeFee", exchange_fee)
    save_add_info(trade, "PS_ClearingFee", clearing_fee)
    save_add_info(trade, "PS_CommissionFee", commission_fee)


def create_log_directory(dictionary, run_date):
    try:
        log_filename = dictionary["log_filename"]
        log_filepath = dictionary["log_filepath"].SelectedDirectory().Text()
        file_date = datetime.strptime(run_date, '%Y-%m-%d').strftime("%Y%m%d")
        log_file = "{log_name}_{log_date}.csv".format(
            log_name=log_filename, log_date=file_date)
        log_directory = os.path.join(log_filepath, run_date)
        if not os.path.exists(log_directory):
            os.makedirs(log_directory)
        return os.path.join(log_filepath, run_date, log_file)
    except Exception as error:
        LOGGER.exception("Failed to create log directory because {error}".format(error=str(error)))


def write_file_data(directory):
    try:
        with open(directory, 'wb') as input_file:
            fieldnames = ["TradeNumber", "TradeTime", "ExecutionTime", "Trader", "BuySell", "Quantity", "Price",
                          "InstrumentType", "Portfolio", "SubAccount", "ClientCode", "JSERef", "Comment",
                          "PaymentAmount", "ExchangeFee", "ClearingFee", "CommissionFee"]
            writer = DictWriter(input_file, fieldnames=fieldnames)
            writer.writeheader()
            for exchange_ref, exchange_data in FEE_DATA.items():
                upload_status = exchange_data[0]
                exchange_fee = exchange_data[4]
                sub_acc_code = exchange_data[1]
                client_code = exchange_data[2]
                trade = exchange_data[3]
                if "_" in exchange_ref:
                    exchange_ref = exchange_ref.split("_")[0]
                if trade:
                    trader = trade.Trader().Name() if trade.Trader() else ""
                    writer.writerow({"TradeNumber": trade.Oid(), "TradeTime": trade.TradeTime(),
                                     "ExecutionTime": trade.ExecutionTime(), "Trader": trader, "BuySell": trade.Sold(),
                                     "Quantity": trade.Quantity(), "Price": trade.Price(),
                                     "InstrumentType": trade.Instrument().InsType(),
                                     "Portfolio": trade.Portfolio().Name(), "SubAccount": sub_acc_code,
                                     "ClientCode": client_code,
                                     "JSERef": exchange_ref, "Comment": upload_status, "PaymentAmount": exchange_fee,
                                     "ExchangeFee": trade.add_info("PS_ExchangeFee"),
                                     "ClearingFee": trade.add_info("PS_ClearingFee"),
                                     "CommissionFee": trade.add_info("PS_CommissionFee")})
                else:
                    writer.writerow({"TradeNumber": "", "TradeTime": "", "ExecutionTime": "", "Trader": "",
                                     "BuySell": "", "Quantity": "", "Price": "", "InstrumentType": "", "Portfolio": "",
                                     "SubAccount": sub_acc_code, "ClientCode": client_code, "JSERef": exchange_ref,
                                     "Comment": upload_status, "PaymentAmount": exchange_fee, "ExchangeFee": "",
                                     "ClearingFee": "", "CommissionFee": ""})
    except Exception as e:
        LOGGER.exception("Failed to write log file because {error}".format(error=str(e)))

"""
Date                    : 2016-05-31
Purpose                 : Posts the val of the clients obligation to a call account
Department and Desk     : Prime Service
Requester               : Eveshnee Naidoo
Developer               : Ondrej Bahounek

Date            CR              Developer               Change
==========      =========       ======================  ========================================================
2016-06-14      3732140         Ondrej Bahounek         ABITFA-4342 - Use PS_InstrumentType cashflow addinfo.
2017-01-26      4150840         Ondrej Bahounek         ABITFA-4592 - add STO, FX, FXO instruments
"""

import string
import datetime
import FRunScriptGUI
import acm
from PB_Saxo_upload_csv import AccountsCSV
from at_ael_variables import AelVariableHandler
from PS_FundingSweeper import CreateCashFlow, TradingManagerSweeper
from PS_Functions import (
                          get_pb_fund_counterparties,
                          modify_asql_query,
                          SetAdditionalInfo,
                          )
from PB_Saxo_deposit import (
                            get_imargin_account,
                            get_call_account,
                            check_depos_existence)
from PB_Saxo_general import (
                            get_fund_portf,
                            SAXO_PAYMENT_PORTF,
                            CF_PRREFUND_TYPE,
                            CF_INITMARGIN_TYPE,
                            get_saxo_instype_alias,
                            get_cf_tpl_type,
                            get_alias_from_alias_or_cp,
                            get_prev_nonweekend_day,
                            DATE_LIST,
                            DATE_KEYS,
                            get_saxo_types
                            )
from at_logging import getLogger


LOGGER = getLogger(__name__)

# TPL_COLUMNS = ['Portfolio Value End']
# TPL_COLUMNS = ['Portfolio Cash End']
TPL_COLUMNS = ['Client TPL']

TODAY = acm.Time().DateToday()


def enable_custom_start_date(selected_variable):
    cust = ael_variables.get("start_custom_date")
    cust.enabled = (selected_variable.value == 'Custom Date')


def enable_custom_end_date(selected_variable):
    cust = ael_variables.get("end_custom_date")
    cust.enabled = (selected_variable.value == 'Custom Date')


def get_saxo_payments(trade, for_date, curr):
    curr_payments = [p.Amount() for p in trade.Payments() if
        p.Currency().Name() == curr
        and p.ValidFrom() <= for_date]
        # and p.Amount() < 0]

    return sum(curr_payments)


def create_time_series(fieldName, instr):
    """ Return the time series spec or create one if it doesn't exist.
        New time series is linked to Instrument instr by FieldName.
    """
    spec = acm.FTimeSeriesSpec[fieldName]
    if not spec:
        spec = acm.FTimeSeriesSpec()
        spec.Description('%s PnL History' % instr)
        spec.FieldName(fieldName)
        spec.RecType(acm.EnumFromString('B92RecordType', 'Instrument'))
        spec.Commit()
    return spec


def get_time_series(for_date, instr, spec):
    """ Return FTimeSeries object (i.e. an object containing
        value from a time series) for specified time series spec,
        date and instrument.
    """
    return acm.FTimeSeries.Select01("day = '%s' and recaddr = %i "
        "and timeSeriesSpec = %i and runNo = 1"
        % (for_date, instr.Oid(), spec.Oid()), '')


def GetCallAccCashFlow(leg, run_date, cf_type):
    """ Return all loan cash flow for specifc date from specified leg.
        Loan cash flow is identified by PS_DepositType add info being
        equal to specified type.
    """
    query = acm.CreateFASQLQuery('FCashFlow', 'AND')
    query.AddAttrNode('Leg.Oid', 'EQUAL', leg.Oid())
    query.AddAttrNode('PayDate', 'EQUAL', run_date)
    query.AddAttrNode('CashFlowType', 'EQUAL', "Fixed Amount")
    query.AddAttrNode('AdditionalInfo.PS_DepositType', 'EQUAL', cf_type)
    cashFlows = query.Select()
    if cashFlows:
        return cashFlows[0]
    return None


def get_cashflows_less_than(leg, run_date, cf_type):
    """ Return all loan cash flows before specifc date from specified leg.
        Loan cash flow is identified by PS_DepositType add info being
        equal to specified type.
    """
    query = acm.CreateFASQLQuery('FCashFlow', 'AND')
    query.AddAttrNode('Leg.Oid', 'EQUAL', leg.Oid())
    query.AddAttrNode('PayDate', 'LESS', run_date)
    query.AddAttrNode('CashFlowType', 'EQUAL', "Fixed Amount")
    query.AddAttrNode('AdditionalInfo.PS_DepositType', 'EQUAL', cf_type)
    cashFlows = query.Select()
    return cashFlows


def get_all_currencies(portfolio, instype):

    query = acm.CreateFASQLQuery('FTrade', 'AND')
    query.AddAttrNode('Status', 'NOT_EQUAL', acm.EnumFromString('TradeStatus', 'Simulated'))
    query.AddAttrNode('Status', 'NOT_EQUAL', acm.EnumFromString('TradeStatus', 'Void'))
    query.AddAttrNode('Status', 'NOT_EQUAL', acm.EnumFromString('TradeStatus', 'Terminated'))
    query.AddAttrNode('Portfolio.Name', 'EQUAL', portfolio.Name())
    query.AddAttrNode('Instrument.InsType', 'EQUAL', acm.EnumFromString('InsType', instype))
    query.AddAttrNode('AdditionalInfo.ExternalCCY', 'NOT_EQUAL', "")

    currs = set(t.AdditionalInfo().ExternalCCY() for t in query.Select())
    return currs


def get_saxo_ins_type(asql_nodes, attr_name):
    if not asql_nodes:
        return None
    for node in asql_nodes:
        if node.IsKindOf(acm.FASQLOpNode):
            value = get_saxo_ins_type(node.AsqlNodes(), attr_name)
            if value is not None:
                return value
        elif node.IsKindOf(acm.FASQLAttrNode):
            if node.AsqlAttribute().AttributeString().Text() == attr_name:
                return str(node.AsqlValue())


def get_fa_type(acm_qfolder):
    fa_type = get_saxo_ins_type(acm_qfolder.Query().AsqlNodes(), "Instrument.InsType")
    return fa_type


def sweep_for_curr(counterparty, qfolder, for_date, curr, trade_data, saxo_type_alias):

    LOGGER.info("*" * 30)
    LOGGER.info("Sweeping currency: %s", curr)
    
    query_folder = qfolder
    if type(qfolder) == str:
        query_folder = acm.FStoredASQLQuery[qfolder]

    fa_type = get_fa_type(query_folder)

    query = modify_asql_query(
        query_folder.Query(),
        "AdditionalInfo.ExternalCCY",
        False,
        curr)
    query = modify_asql_query(
        query,
        "Counterparty.Name",
        False,
        counterparty.Name())
    trades = query.Select()

    LOGGER.info("Trades found: %d", len(trades))

    new_val = 0
    for t in trades:
        tplDictionary = TradingManagerSweeper(t, for_date, TPL_COLUMNS, inCurrency=curr)
        for instrument_name, tplValues in tplDictionary.iteritems():
            new_val += sum(tplValues)
            trade_record = (
                t.Oid(),
                t.Instrument().InsType(),
                instrument_name,
                t.Portfolio().Name(),
                sum(tplValues)
            )
            trade_data.append(trade_record)
            print('%s\t%s\t%s\t%f' % (t.Oid(), t.Portfolio().Name(),
                instrument_name, sum(tplValues)))

    call_account = get_call_account(counterparty, curr)
    field_name = "PB_SAXO_INT_" + saxo_type_alias + "_Tpl"

    # get the time series descriptor
    spec = create_time_series(field_name, call_account.Name())

    # get the previous days' value otherwise post the whole amount
    # assuming that this is the first posting
    prev_day = get_prev_nonweekend_day(for_date)
    prev_series = get_time_series(prev_day, call_account, spec)
    if prev_series:
        prev_val = prev_series.TimeValue()
    else:
        prev_val = 0
        prev_vals = acm.FTimeSeries.Select("timeSeriesSpec='%s' and recaddr=%s and day<'%s'"
                                            % (field_name, call_account.Oid(), for_date))
        if prev_vals:
            # Allow rerun only if there are no previous reruns before the missing TS.
            # Situation: Previous day rerun is missing, but before it there exist other TimeSeries.
            # There is a gap and must be solved by running this sweeping for earlier date.
            raise RuntimeError("ERROR: Sweeping is run without completion "\
                "of previous day's sweeping (%s)." % prev_day)

    # get today's value to either create or update with val
    series = get_time_series(for_date, call_account, spec)
    if not series:
        series = acm.FTimeSeries()
        series.Recaddr(call_account.Oid())
        series.TimeSeriesSpec(spec)
        series.Day(for_date)
        series.RunNo(1)
    LOGGER.info("Saving to Time series '%s': %f [%s]", field_name, new_val, curr)
    series.TimeValue(new_val)
    series.Commit()

    postingVal = new_val - prev_val

    postingVal = -postingVal  # opposite sign = Saxo facing value which is stored on CAcc

    LOGGER.info("\tPrevious day: %f", prev_val)
    LOGGER.info("\tToday: %f", new_val)
    LOGGER.info("\tPosting: %f", postingVal)

    trade_data.append(("Previous day", "", "", "", prev_val))
    trade_data.append(("Today", "", "", "", new_val))
    trade_data.append(("Posting", "", "", "", postingVal))
    
    cf_type = get_cf_tpl_type(saxo_type_alias)
    LOGGER.info("Saving cashflow (type: %s, date: %s)...", cf_type, for_date)
    save_amount_to_depo(call_account, postingVal, for_date, cf_type, instype=fa_type)
    
    LOGGER.info("Currency '%s' has been successfully swept.", curr)


def sweep_tpl(counterparty, qfolder, for_date, saxo_type_alias):
    """ Save the total value of financed trades in all portfolios under cPort
        on runDate to time series for the cPort and post a difference
        between yesterday's and today's value to Loan Account
    """
    portfolio = get_fund_portf(counterparty)
    fa_type = get_fa_type(qfolder)
    alias = get_alias_from_alias_or_cp(counterparty)
    LOGGER.info("*" * 30)
    LOGGER.info("TPL sweeping started (date: %s)", for_date)
    LOGGER.info("\tFund: %s", alias)
    LOGGER.info("\tInsType: %s", fa_type)
    LOGGER.info("\tPortfolio: %s", portfolio.Name())

    trade_data = []
    currs = get_all_currencies(portfolio, fa_type)
    LOGGER.info("Currencies: %s", ", ".join(currs))
    for currency in currs:
        check_depos_existence(alias, currency, for_date)
        sweep_for_curr(counterparty, qfolder, for_date, currency, trade_data, saxo_type_alias)

    LOGGER.info("TPL sweeping completed successfully")
    return trade_data


def save_amount_to_depo(deposit, value, cf_date, cf_type, instype=None):
    leg = deposit.Legs()[0]
    cashFlow = GetCallAccCashFlow(leg, str(cf_date), cf_type)
    if not cashFlow:
        if round(value, 6) == 0:
            LOGGER.info("Skipping saving amount: %f", value)
            return
            
        cashFlow = CreateCashFlow(leg, 'Fixed Amount', None, None, cf_date, value)
        SetAdditionalInfo(cashFlow, 'PS_DepositType', cf_type)
        if instype:
            SetAdditionalInfo(cashFlow, 'PS_InstrumentType', instype)
    elif cashFlow.FixedAmount() != value:
        cashFlow.FixedAmount(value)
        cashFlow.Commit()
        
    LOGGER.info("Depo '%s': cashflow amount %f of type '%s' saved.", 
        deposit.Name(), cashFlow.FixedAmount(), cf_type)


def previous_depo_amount(deposit, cf_date, cf_type):
    leg = deposit.Legs()[0]
    cash_flows = get_cashflows_less_than(leg, cf_date, cf_type)
    if not cash_flows:
        return 0
    return sum(cf.FixedAmount() for cf in cash_flows)


def get_saxo_payment_trade(cparty):
    portf = acm.FPhysicalPortfolio[SAXO_PAYMENT_PORTF]
    trades = [t for t in portf.Trades() if
        t.Status() not in ['Simulated', 'Terminated', 'Void']
        and 'SaxoPayments' in t.Instrument().Name()
        and t.AdditionalInfo().Relationship_Party() != None
        and t.AdditionalInfo().Relationship_Party().Name() == cparty.Name()]
    if len(trades) > 1:
        raise RuntimeError("More than 1 SaxoPayment trade found for %s: " % cparty.Name() +
                           "%s" % [t.Oid() for t in trades])
    if not trades:
        raise RuntimeError("No SaxoPayment trade found for %s. " % cparty.Name() +
                            "Check Relationship_Party addinfo.")
    return trades[0]


def get_cp_currencies(trade):
    currs = set(p.Currency().Name() for p in trade.Payments()
        if p.Amount() < 0 and p.Currency().Name() != "ZAR")
    return currs


def sweep_prefund_cfs(for_date, cparty):
    """Saxo payment trade payments
    """
    LOGGER.info("*" * 30)
    LOGGER.info("Prefund sweeping started (date: %s)", for_date)
    trade = get_saxo_payment_trade(cparty)
    alias = get_alias_from_alias_or_cp(cparty)
    LOGGER.info("\tFund: %s", alias)
    LOGGER.info("\tSaxoPayment trade: %d", trade.Oid())
    currs = get_cp_currencies(trade)

    for currency in currs:
        LOGGER.info("Sweeping prefund payments for currency: %s", currency)
        check_depos_existence(alias, currency, for_date)
        posting = get_saxo_payments(trade, for_date, currency)
        call_account = get_call_account(alias, currency)
        previous_amnt = previous_depo_amount(call_account, for_date, CF_PRREFUND_TYPE)
        diff_amnt = posting - previous_amnt
        LOGGER.info("Prefunds:")
        LOGGER.info("\tPrevious amount: %f", previous_amnt)
        LOGGER.info("\tActual amount: %f", posting)

        LOGGER.info("Saving cashflow: %f (type: %s, date: %s)...",
            diff_amnt, CF_PRREFUND_TYPE, for_date)
        save_amount_to_depo(call_account, diff_amnt, for_date, CF_PRREFUND_TYPE)

    LOGGER.info("Prefund sweeping completed successfully")


def sweep_initial_margin(for_date, cparty, acc_file_path):

    LOGGER.info("*" * 30)
    LOGGER.info("Initial Margin sweeping started (date: %s)", for_date)
    alias = get_alias_from_alias_or_cp(cparty)
    LOGGER.info("Fund alias: %s", alias)
    fund_curr_dict = AccountsCSV.get_accounts_from_file(acc_file_path)

    for curr in fund_curr_dict[alias]:
        LOGGER.info("Sweeping margin for currency: '%s'", curr)
        check_depos_existence(alias, curr, for_date)
        new_margin = fund_curr_dict[alias][curr]
        LOGGER.info("Margin read from Saxo file: %f [%s]", new_margin, curr)
        
        margin_account = get_imargin_account(alias, curr)
        # this amount should be same as margin amount in previous day's Account file
        previous_amnt = previous_depo_amount(margin_account, for_date, CF_INITMARGIN_TYPE)
        diff_amnt = new_margin - previous_amnt
        
        LOGGER.info("Margins:")
        LOGGER.info("\tPrevious = %f", previous_amnt)
        LOGGER.info("\tNew = %f", new_margin)
        LOGGER.info("\tDiff = %f", diff_amnt)

        # post on all 4 depos:
        call_account = get_call_account(alias, curr)
        margin_account = get_imargin_account(alias, curr)
        LOGGER.info("Saving 2 cashflows of type '%s' for date '%s'...",
            CF_INITMARGIN_TYPE, for_date)
        
        LOGGER.info("\tAmount %f to '%s'", -diff_amnt, call_account.Name())
        save_amount_to_depo(call_account, -diff_amnt, for_date, CF_INITMARGIN_TYPE)
        
        LOGGER.info("\tAmount %f to '%s'", diff_amnt, margin_account.Name())
        save_amount_to_depo(margin_account, diff_amnt, for_date, CF_INITMARGIN_TYPE)

    LOGGER.info("Initial Margin sweeping completed successfully")


fileFilter = "CSV Files (*.csv)|*.csv|Text Files (*.txt)|*.txt|All Files (*.*)|*.*||"
inputFile = FRunScriptGUI.InputFileSelection(FileFilter=fileFilter)

ael_variables = AelVariableHandler()
ael_variables.add("sweep_var_marg",
                  label="Sweep Variation Margin?",
                  cls="bool",
                  collection=(True, False),
                  default=False,
                  alt="Will sweep variation margin.")
ael_variables.add("sweep_prefund",
                  label="Sweep Prefund Margin?",
                  cls="bool",
                  collection=(True, False),
                  default=False,
                  alt="Will sweep prefund.")
ael_variables.add("sweep_init_marg",
                  label="Sweep Initial Margin?",
                  cls="bool",
                  collection=(True, False),
                  default=False,
                  alt="Will sweep initial margin.")
ael_variables.add("qfolder",
                  label="Query Folder",
                  cls=acm.FStoredASQLQuery,
                  mandatory=False)
ael_variables.add("counterparty",
                  label="Counterparty",
                  cls=acm.FCounterParty,
                  mandatory=True,
                  collection=sorted(get_pb_fund_counterparties()))
ael_variables.add("start_date",
                  label="Start Date",
                  cls="string",
                  default="PrevNonWeekendDay",
                  collection=DATE_KEYS,
                  hook=enable_custom_start_date,
                  mandatory=True,
                  alt=("Start date of a sweeping."))
ael_variables.add("start_custom_date",
                  label="Start Date Custom",
                  cls="string",
                  default=TODAY,
                  enabled=False,
                  alt=("Format: '2016-09-30'."))
ael_variables.add("end_date",
                  label="End Date",
                  cls="string",
                  default="PrevNonWeekendDay",
                  collection=DATE_KEYS,
                  hook=enable_custom_end_date,
                  mandatory=True,
                  alt=("End date of a sweeping. If it is same date as start day, "
                       "just this one day will be taken."))
ael_variables.add("end_custom_date",
                  label="End Date Custom",
                  cls="string",
                  default=TODAY,
                  enabled=False,
                  alt=("Format: '2016-09-30'."))
ael_variables.add("accounts_file",
                label='Saxo accounts file',
                cls=inputFile,
                default=inputFile,
                mandatory=False,
                multiple=True,
                alt=('Full path to the Saxo Accounts file (delimited by comma). '
                    'Can contain ${DIRDATE} and ${FILEDATE} variables. '
                    'Example: "C:\\SAXO\\${DIRDATE}\\AccountStatus_${FILEDATE}.csv'))
ael_variables.add("saxo_ins_type",
                  label="Saxo ins type",
                  cls="string",
                  default="",
                  collection=get_saxo_types(),
                  mandatory=True,
                  alt="Saxo instrument type that will be swept.")


def get_dates_from_range(start_date, end_date):
    dates = []
    num_days = acm.Time.DateDifference(end_date, start_date) + 1
    for days_to_add in range(num_days):
        sweep_date = acm.Time.DateAddDelta(start_date, 0, 0, days_to_add)
        dates.append(sweep_date)
    return dates


def ael_main(ael_dict):

    if ael_dict['start_date'] == 'Custom Date':
        start_date = ael_dict['start_custom_date']
    else:
        start_date = DATE_LIST[ael_dict['start_date']]

    if ael_dict['end_date'] == 'Custom Date':
        end_date = ael_dict['end_custom_date']
    else:
        end_date = DATE_LIST[ael_dict['end_date']]

    cparty = ael_dict["counterparty"]

    WEEKEND_DAYS = ("Saturday", "Sunday")
    sweeping_dates = get_dates_from_range(start_date, end_date)
    for for_date in sweeping_dates:

        LOGGER.info("=" * 48)
        LOGGER.info("%s: Saxo Sweeping started for date '%s'...",
            acm.Time.TimeNow(), for_date)
        
        if acm.Time.DayOfWeek(for_date) in WEEKEND_DAYS:
            LOGGER.warning("Skipping a weekend day...")
            continue

        try:
            # VARIATION MARGIN sweeping (TPL)
            if ael_dict["sweep_var_marg"]:
                if not ael_dict["qfolder"]:
                    raise RuntimeError("Query folder missing.")

                saxo_type_alias = get_saxo_instype_alias(ael_dict["saxo_ins_type"])
                trade_data = sweep_tpl(cparty, ael_dict["qfolder"], for_date, saxo_type_alias)


            # PREFUND sweeping (SaxoPayment trades)
            if ael_dict["sweep_prefund"]:
                sweep_prefund_cfs(for_date, cparty)


            # INIT MARGIN sweeping (file: AccountStatus, column: MarginForTrading)
            if ael_dict["sweep_init_marg"]:
                # file date will be converted to "dd-mm-YYYY"
                # directory date will be converted to "YYYY-mm-dd"
                _dt = datetime.datetime.strptime(for_date, "%Y-%m-%d")
                file_date = _dt.strftime("%d-%m-%Y")
                dir_date = for_date
                path_template = string.Template(str(ael_dict["accounts_file"]))
                file_path = path_template.substitute(DIRDATE=dir_date, FILEDATE=file_date)
                sweep_initial_margin(for_date, cparty, str(file_path))

        except Exception as exc:
            LOGGER.exception("Sweeping failed: '%s'", exc)
            raise

    LOGGER.info("=" * 48)
    LOGGER.info("%s: Sweeping completed successfully.", acm.Time.TimeNow())


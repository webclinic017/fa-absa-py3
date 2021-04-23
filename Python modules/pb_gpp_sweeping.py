"""
Date                    : 2017-03-07
Purpose                 : Upload GPP objects into FA.
Department and Desk     : Prime Services
Requester               : Eveshnee Naidoo
Developer               : Ondrej Bahounek

Date            CR              Developer               Change
==========      =========       ======================  ========================================================
2017-03-07      4372980         Ondrej Bahounek         ABITFA-4765 - GPP phase 1
2017-11-24      4634552         Ondrej Bahounek         ABITFA-4916 - GPP - go live
"""

import string
import datetime
import csv
from collections import defaultdict

import FRunScriptGUI
import acm
import at_timeSeries
from at_logging import getLogger

from at_ael_variables import AelVariableHandler

from PS_FundingSweeper import CreateCashFlow, TradingManagerSweeper
from PS_Functions import (
                          get_pb_fund_counterparty,
                          modify_asql_query,
                          SetAdditionalInfo,
                          )


from pb_gpp_deposit import (
                            get_imargin_account,
                            get_call_account,
                            check_depos_existence)

from pb_gpp_general import (
                            get_trading_portf,
                            get_payment_portf,
                            CF_PRREFUND_TYPE,
                            CF_INITMARGIN_TYPE,
                            get_fa_instype_alias,
                            get_cf_tpl_type,
                            get_alias_from_alias_or_cp,
                            get_prev_nonweekend_day,
                            DATE_LIST,
                            DATE_KEYS,
                            get_gpp_ins_types,
                            get_account_alias,
                            add_common_aelvars,
                            set_general_input,
                            get_query_folder
                            )

LOGGER = getLogger(__name__)

PORTF_TRADING = get_trading_portf()
PORTF_PAYMENT = get_payment_portf()

# TPL_COLUMNS = ['Portfolio Value End']
# TPL_COLUMNS = ['Portfolio Cash End']
TPL_COLUMNS = ['Client TPL']

TODAY = acm.Time().DateToday()

FX_RATES = None
ACCNT_MARGIN = None

MARGIN_FILE_PATH = None  # r"c:\DEV\Perforce\FA\features\ABITFA-4916 - GPP - go live.br\input\instruments.csv"
MARGIN_FILE_PATH_FRONT = r"y:\Jhb\FAReports\AtlasEndOfDay\PrimeClients\GPP\${DIRDATE}\${FILEDATE}_ABSABankLtd-1_MarginSummary.csv"
MARGIN_FILE_PATH_BACK = r"/nfs/fa/reports/EMEA/prod/FAReports/AtlasEndOfDay/PrimeClients/GPP/${DIRDATE}/${FILEDATE}_ABSABankLtd-1_MarginSummary.csv"

def enable_custom_start_date(selected_variable):
    cust = ael_variables.get("start_custom_date")
    cust.enabled = (selected_variable.value == 'Custom Date')


def enable_custom_end_date(selected_variable):
    cust = ael_variables.get("end_custom_date")
    cust.enabled = (selected_variable.value == 'Custom Date')


def get_gpp_payments(trade, for_date, curr):
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


def get_all_currencies(portfolio, instype, cparty):

    query = acm.CreateFASQLQuery('FTrade', 'AND')
    query.AddAttrNode('Status', 'NOT_EQUAL', acm.EnumFromString('TradeStatus', 'Simulated'))
    query.AddAttrNode('Status', 'NOT_EQUAL', acm.EnumFromString('TradeStatus', 'Void'))
    query.AddAttrNode('Status', 'NOT_EQUAL', acm.EnumFromString('TradeStatus', 'Terminated'))
    query.AddAttrNode('Portfolio.Name', 'EQUAL', portfolio.Name())
    query.AddAttrNode('Instrument.InsType', 'EQUAL', acm.EnumFromString('InsType', instype))
    query.AddAttrNode('Counterparty.Name', 'EQUAL', cparty.Name())

    currs = {t.Currency().Name() for t in query.Select()}
    return currs


def get_gpp_ins_type(asql_nodes, attr_name):
    if not asql_nodes:
        return None
    for node in asql_nodes:
        if node.IsKindOf(acm.FASQLOpNode):
            value = get_gpp_ins_type(node.AsqlNodes(), attr_name)
            if value is not None:
                return value
        elif node.IsKindOf(acm.FASQLAttrNode):
            if node.AsqlAttribute().AttributeString().Text() == attr_name:
                return str(node.AsqlValue())


def get_fa_type(acm_qfolder):
    fa_type = get_gpp_ins_type(acm_qfolder.Query().AsqlNodes(), "Instrument.InsType")
    return fa_type


def sweep_for_curr(counterparty, qfolder, for_date, curr, trade_data, fx_rate):

    LOGGER.info("Sweeping currency %s with rate %f", curr, fx_rate)
    query_folder = qfolder
    if type(qfolder) == str:
        query_folder = acm.FStoredASQLQuery[qfolder]

    query = modify_asql_query(
        query_folder.Query(),
        "Currency.Name",
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
            tpl_sum = sum(tplValues)
            new_val += tpl_sum
            
            trade_record = (
                t.Oid(),
                t.Instrument().InsType(),
                instrument_name,
                curr,
                t.Portfolio().Name(),
                tpl_sum,
                fx_rate,
                tpl_sum * fx_rate
            )
            trade_data.append(trade_record)
            print '%s' % "\t".join(map(str, trade_record))

    # use external FX rate
    new_val *= fx_rate
    return new_val


def save_tpl(counterparty, for_date, account_curr, trade_data, fa_type_alias, new_val, fa_type):

    call_account = get_call_account(counterparty, account_curr)
    field_name = "PB_GPP_" + fa_type_alias + "_Tpl"

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
            raise RuntimeError("ERROR: Sweeping is run without completion "
                "of previous day's sweeping (%s)." % prev_day)

    # get today's value to either create or update with val
    series = get_time_series(for_date, call_account, spec)
    if not series:
        series = acm.FTimeSeries()
        series.Recaddr(call_account.Oid())
        series.TimeSeriesSpec(spec)
        series.Day(for_date)
        series.RunNo(1)
    LOGGER.info("Saving Time series '%s': %f [%s]", field_name, new_val, account_curr)
    series.TimeValue(new_val)
    series.Commit()

    postingVal = new_val - prev_val

    postingVal = -postingVal  # opposite sign = GPP facing value which is stored on CAcc

    LOGGER.info('Previous day: %f', prev_val)
    LOGGER.info('Today: %f', new_val)
    LOGGER.info('Posting : %f', postingVal)

    trade_data.append(("Previous day", "", "", "", prev_val))
    trade_data.append(("Today", "", "", "", new_val))
    trade_data.append(("Posting", "", "", "", postingVal))
    
    LOGGER.info("Saving cashflows (date: %s)...", for_date)
    LOGGER.info("depo: '%s'; amount: %f", call_account.Name(), postingVal)
    cf_type = get_cf_tpl_type(fa_type_alias)
    save_amount_to_depo(call_account, postingVal, for_date, cf_type, instype=fa_type)


def sweep_tpl(counterparty, qfolder, for_date, fa_type_alias):
    """ Save the total value of financed trades in all portfolios under cPort
        on runDate to time series for the cPort and post a difference
        between yesterday's and today's value to Loan Account
    """
    portfolio = PORTF_TRADING
    fa_type = get_fa_type(qfolder)
    alias = get_alias_from_alias_or_cp(counterparty)
    LOGGER.info('TPL sweeping date: %s', for_date)
    LOGGER.info('Fund: %s. InsType: %s. Portfolio: %s', alias, fa_type, portfolio.Name())
    currs = get_all_currencies(portfolio, fa_type, counterparty)
    if not currs:
        LOGGER.info('Skipping: no trading activity')
        return []
        
    LOGGER.info('------ Enter process postings ------')
    trade_data = []
    account_curr = acm.FCurrency['USD']
    check_depos_existence(alias, account_curr.Name(), for_date)
    
    LOGGER.info("Sweeping currencies: %s", ", ".join(c for c in currs))
    
    tpl = 0
    for currency in currs:
        fx_rate = get_fx_rate(currency)
        tpl += sweep_for_curr(counterparty, qfolder, for_date, currency, trade_data, fx_rate)
        
    save_tpl(counterparty, for_date, account_curr.Name(), trade_data, fa_type_alias, tpl, fa_type)

    LOGGER.info('------ Exit process postings ------')
    return trade_data


def save_amount_to_depo(deposit, value, cf_date, cf_type, instype=None):
    leg = deposit.Legs()[0]
    cashFlow = GetCallAccCashFlow(leg, str(cf_date), cf_type)
    if not cashFlow:
        if round(value, 6) == 0:
            LOGGER.info("Skipping saving to depo value: %f", value)
            return
            
        cashFlow = CreateCashFlow(leg, 'Fixed Amount', None, None, cf_date, value)
        SetAdditionalInfo(cashFlow, 'PS_DepositType', cf_type)
        if instype:
            SetAdditionalInfo(cashFlow, 'PS_InstrumentType', instype)
    elif cashFlow.FixedAmount() != value:
        # I don't want to delete any existing cashflows for possible future refs.
        cashFlow.FixedAmount(value)
        cashFlow.Commit()
        
    LOGGER.info("Depo '%s': cashflow amount %f of type %s saved.",
        deposit.Name(), cashFlow.FixedAmount(), cf_type)


def previous_depo_amount2(deposit, cf_date, cf_type):
    if deposit and deposit.Legs():
        leg = deposit.Legs()[0]
        cash_flows = get_cashflows_less_than(leg, cf_date, cf_type)
        if not cash_flows:
            return 0
        latest = cash_flows[0]
        for cf in cash_flows:
            if cf.PayDate() > latest.PayDate():
                latest = cf
        return latest.FixedAmount()


def previous_depo_amount(deposit, cf_date, cf_type):
    leg = deposit.Legs()[0]
    cash_flows = get_cashflows_less_than(leg, cf_date, cf_type)
    if not cash_flows:
        return 0
    return sum([cf.FixedAmount() for cf in cash_flows])


def get_gpp_payment_trade(cparty):
    portf = PORTF_PAYMENT
    trades = [t for t in portf.Trades() if
        t.Status() not in ['Simulated', 'Terminated', 'Void']
        and 'GPPpayments' in t.Instrument().Name()
        and t.AdditionalInfo().Relationship_Party() != None
        and t.AdditionalInfo().Relationship_Party().Name() == cparty.Name()]
    if len(trades) > 1:
        raise RuntimeError("More than 1 GPPpayment trade found for '%s': " % cparty.Name() +
                           "%s" % [t.Oid() for t in trades])
    if not trades:
        raise RuntimeError("No GPPpayment trade found for '%s'. " % cparty.Name() +
                            "Check Relationship_Party addinfo.")
    return trades[0]


def get_cp_currencies(trade):
    currs = set(p.Currency().Name() for p in trade.Payments()
        if p.Amount() < 0 and p.Currency() != "ZAR")
    return currs


def sweep_prefund_cfs(for_date, cparty):
    """GPP payment trade payments
    """
    LOGGER.info("")
    LOGGER.info("*" * 32)
    LOGGER.info("Prefund sweeping started (date: %s)", for_date)
    trade = get_gpp_payment_trade(cparty)
    alias = get_alias_from_alias_or_cp(cparty)
    LOGGER.info("Fund: %s. GPPpayment trade: %d", alias, trade.Oid())
    currs = get_cp_currencies(trade)

    for currency in currs:
        LOGGER.info("Sweeping prefund payments in currency: %s", currency)
        check_depos_existence(alias, currency, for_date)
        posting = get_gpp_payments(trade, for_date, currency)
        call_account = get_call_account(alias, currency)
        previous_amnt = previous_depo_amount(call_account, for_date, CF_PRREFUND_TYPE)
        diff_amnt = posting - previous_amnt
        LOGGER.info("\tPrevious amount: %f", previous_amnt)
        LOGGER.info("\tActual amount: %f", posting)

        # post to depo
        LOGGER.info("Saving cashflow %f (type: %s, date: %s)...",
            diff_amnt, CF_PRREFUND_TYPE, for_date)
        save_amount_to_depo(call_account, diff_amnt, for_date, CF_PRREFUND_TYPE)

    LOGGER.info("")
    LOGGER.info("Prefund sweeping completed successfully")
    LOGGER.info("*" * 30)


def sweep_initial_margin(for_date, cparty):

    LOGGER.info("")
    LOGGER.info("*" * 30)
    LOGGER.info("Initial Margin sweeping started (date: %s)", for_date)
    alias = get_alias_from_alias_or_cp(cparty)
    LOGGER.info("Fund: %s", alias)
    
    currencies = get_margin_currencies(alias)
    
    base_curr = acm.FCurrency['USD']

    new_margin = 0
    for curr in currencies:
        curr_margin = get_margin_per_curr(alias, curr)
        LOGGER.info("Margin read from GPP file for %s: %f [%s]", curr, curr_margin, base_curr.Name())
        new_margin += curr_margin
        
    
    LOGGER.info("Overall new margin: %f", new_margin)
    check_depos_existence(alias, base_curr.Name(), for_date)
    margin_account = get_imargin_account(alias, base_curr)
    # this amount should be same as margin amount in previous day's Account file
    previous_amnt = previous_depo_amount(margin_account, for_date, CF_INITMARGIN_TYPE)
    diff_amnt = new_margin - previous_amnt
    LOGGER.info("Margins: \tPrevious = %f, \tNew = %f, \tDiff = %f",
        previous_amnt, new_margin, diff_amnt)

    # post on both 2 depos:
    call_account = get_call_account(alias, base_curr.Name())
    margin_account = get_imargin_account(alias, base_curr.Name())
    LOGGER.info("Saving 2 cashflows (type: %s, date: %s)...",
        CF_INITMARGIN_TYPE, for_date)
    LOGGER.info("\tAmount %f to %s", -diff_amnt, call_account.Name())
    save_amount_to_depo(call_account, -diff_amnt, for_date, CF_INITMARGIN_TYPE)
    LOGGER.info("\tAmount %f to %s", diff_amnt, margin_account.Name())
    save_amount_to_depo(margin_account, diff_amnt, for_date, CF_INITMARGIN_TYPE)

    LOGGER.info("")
    LOGGER.info("Initial Margin sweeping completed successfully")
    LOGGER.info("*" * 30)


def get_fx_rate(currency):
    return FX_RATES[currency]
    
    
def get_margin_per_curr(alias, curr):
    return ACCNT_MARGIN[alias][curr]
    
    
def get_margin_currencies(alias):
    return sorted(ACCNT_MARGIN[alias].keys())


def process_margin_file(file_path):

    LOGGER.info("Margin file: '%s'", file_path)
    global FX_RATES
    FX_RATES = {}
    
    global ACCNT_MARGIN
    ACCNT_MARGIN = defaultdict(lambda: defaultdict(float))
    
    # DICT reader
    with open(file_path, "rb") as csv_file:
        reader = csv.DictReader(csv_file, delimiter=",")
        for dict_line in reader:
            if dict_line['BaseCCY'] != 'USD':
                LOGGER.warning("Skipping unexpected base currency '%s'", dict_line['BaseCCY'])
                continue
            curr = dict_line['Currency']
            FX_RATES[curr] = float(dict_line['FXRate'])
            
            alias = get_account_alias(dict_line['AccountName'])
            ACCNT_MARGIN[alias][curr] = float(dict_line['TotalMarginBaseCcy'])


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
ael_variables.add("alias",
                  label="Alias",
                  cls="string",
                  mandatory=True)
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
                  alt=("Format: '2017-02-28'."))
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
                  alt=("Format: '2017-02-28'."))
ael_variables.add("margin_file",
                label='Margin file',
                cls="string",
                default=MARGIN_FILE_PATH_FRONT,
                mandatory=False,
                collection=(MARGIN_FILE_PATH_FRONT, MARGIN_FILE_PATH_BACK),
                alt=('Full path to the Margin Summary file (delimited by comma). '
                    'Can contain ${DIRDATE} and ${FILEDATE} variables. '
                    'Example: "C:\\SAXO\\${DIRDATE}\\MarginSummary_${FILEDATE}.csv '
                    'Needed for Variation and Initial Margin sweepings.'))
                  
add_common_aelvars(ael_variables)


def get_file(path, for_date):
    # file date will be converted to "YYYYmmdd"
    # directory date will be converted to "YYYY-mm-dd"
    _dt = datetime.datetime.strptime(for_date, "%Y-%m-%d")
    file_date = _dt.strftime("%Y%m%d")
    dir_date = for_date
    path_template = string.Template(path)
    file_path = path_template.substitute(DIRDATE=dir_date, FILEDATE=file_date)
    return file_path


def get_dates_from_range(start_date, end_date):
    dates = []
    num_days = acm.Time.DateDifference(end_date, start_date) + 1
    for days_to_add in range(num_days):
        sweep_date = acm.Time.DateAddDelta(start_date, 0, 0, days_to_add)
        dates.append(sweep_date)
    return dates


def ael_main(ael_dict):

    set_general_input(ael_dict)

    if ael_dict['start_date'] == 'Custom Date':
        start_date = ael_dict['start_custom_date']
    else:
        start_date = DATE_LIST[ael_dict['start_date']]

    if ael_dict['end_date'] == 'Custom Date':
        end_date = ael_dict['end_custom_date']
    else:
        end_date = DATE_LIST[ael_dict['end_date']]

    alias = ael_dict["alias"]
    cparty = get_pb_fund_counterparty(alias)

    WEEKEND_DAYS = ("Saturday", "Sunday")
    sweeping_dates = get_dates_from_range(start_date, end_date)
    for for_date in sweeping_dates:

        LOGGER.info("=" * 60)
        LOGGER.info("GPP Sweeping started for date: '%s'", for_date)
        
        if acm.Time.DayOfWeek(for_date) in WEEKEND_DAYS:
            LOGGER.info("Skipping weekend day...")
            continue
            
        if ael_dict["sweep_init_marg"] or ael_dict["sweep_var_marg"]:
            # used for fx rates and init margin requirement
            margin_file = get_file(ael_dict['margin_file'], for_date)
            process_margin_file(margin_file)

        try:
            # VARIATION MARGIN sweeping (TPL)
            if ael_dict["sweep_var_marg"]:
                for gpp_type_alias in get_gpp_ins_types():
                    LOGGER.info("*" * 32)
                    fa_type_alias = get_fa_instype_alias(gpp_type_alias)
                    LOGGER.info("Variation Margin Sweeping '%s': '%s' ('%s')", alias, gpp_type_alias, fa_type_alias)
                    qfolder = acm.FStoredASQLQuery[get_query_folder(gpp_type_alias)]
                    trade_data = sweep_tpl(cparty, qfolder, for_date, fa_type_alias)


            # PREFUND sweeping (GPPpayment trades)
            if ael_dict["sweep_prefund"]:
                sweep_prefund_cfs(for_date, cparty)


            # INIT MARGIN sweeping (file: MarginSummary, column: TotalMarginBaseCcy)
            if ael_dict["sweep_init_marg"]:
                sweep_initial_margin(for_date, cparty)

        except Exception as exc:
            LOGGER.exception("Sweeping failed: %s", exc)
            raise

    LOGGER.info("=" * 60)
    LOGGER.info("Completed successfully.")


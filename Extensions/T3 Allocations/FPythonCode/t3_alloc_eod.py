import os
import csv
import acm
from at_ael_variables import AelVariableHandler
from at_time import acm_date
from t3_alloc_logic import get_process_object, get_process_class, STATE_CHART_NAME


DATE_TODAY = acm.Time().DateToday()
CALENDAR = acm.FCalendar['ZAR Johannesburg']
LAST_BUSINESS_DAY = CALENDAR.AdjustBankingDays(DATE_TODAY, -1)
FIELDS = (
    ('Acquirer', lambda t: t.Acquirer().Name()),
    ('Portfolio', lambda t: t.Portfolio().Name()),
    ('Counterparty', lambda t: t.Counterparty().Name()),
    ('Trade No', lambda t: str(t.Oid())),
    ('BO Trade No', lambda t: str(t.BoTrdnbr())),
    ('Name', lambda t: t.Instrument().Name()),
    ('ISIN', lambda t: t.Instrument().Isin()),
    ('Price', lambda t: str(t.Price())),
    ('Premium', lambda t: str(t.Premium())),
    ('Position', lambda t: str(t.Position())),
    ('Value Day', lambda t: str(t.ValueDay())),
    ('Acquire Day', lambda t: str(t.AcquireDay())),
    ('Trade Time', lambda t: str(t.TradeTime())),
    ('Trader', lambda t: t.Trader().Name()),
)

calc_space = acm.Calculations().CreateStandardCalculationsSpaceCollection()

def enable_custom_date(ael_input):
    """Hook enabling custom date."""
    custom_date = ael_variables.get('start_date')
    if ael_input.value == 'Custom Date':
        custom_date.enabled = True
    elif ael_input.value == 'Last Business Day':
        custom_date.enabled = False
        custom_date.value = LAST_BUSINESS_DAY
    else:
        custom_date.enabled = False
        custom_date.value = DATE_TODAY


def enable_acs_run(ael_input):
    """Hook enabling run for ACS."""
    enabled = ael_input.value == '1'
    for var in ael_variables:
        if var.label in ['ACS Portfolio Query Folder',
                'ACS Report File Name', 'ACS Report Directory']:
            var.enabled = enabled

# PB allocation functionality disabled
#def enable_pb_run(ael_input):
#    """Hook enabling run for PB."""
#    enabled = ael_input.value == '1'
#    for var in ael_variables:
#        if var.label in ['PB Portfolio Query Folder',
#                'PB Report File Name', 'PB Report Directory']:
#            var.enabled = enabled


ael_variables = AelVariableHandler()
ael_variables.add(
    'date_selection',
    label='Start Date',
    collection=['Last Business Day', 'Date Today', 'Custom Date'],
    default='Last Business Day',
    cls='string',
    hook=enable_custom_date
)
ael_variables.add(
    'start_date',
    label='Custom Date',
    cls='date',
    default=LAST_BUSINESS_DAY,
    alt='Custom start date.'
)
ael_variables.add(
    'acs_run',
    label='Run for ACS',
    collection=[0, 1],
    cls='int',
    hook=enable_acs_run,
)
ael_variables.add(
    'acs_query_folder',
    label='ACS Portfolio Query Folder',
    default='T3_Alloc_ACS',
    cls='FStoredASQLQuery',
    collection=acm.FStoredASQLQuery.Select("subType='FPhysicalPortfolio'")
)
ael_variables.add(
    'acs_report_file',
    label='ACS Report File Name',
    cls='string',
    default='T3Alloc_EOD_ACS_YYYYMMDD.csv'
)
ael_variables.add(
    'acs_report_dir',
    label='ACS Report Directory',
    cls='string',
    default=r'/services/frontnt/Task'
)
# PB allocation functionality disabled
#ael_variables.add(
#    'pb_run',
#    label='Run for PB',
#    collection=[0, 1],
#    cls='int',
#    hook=enable_pb_run,
#)
#ael_variables.add(
#    'pb_query_folder',
#    label='PB Portfolio Query Folder',
#    default='T3_Alloc_PB',
#    cls='FStoredASQLQuery',
#    collection=acm.FStoredASQLQuery.Select("subType='FPhysicalPortfolio'")
#)
#ael_variables.add(
#    'pb_report_file',
#    label='PB Report File Name',
#    cls='string',
#    default='T3Alloc_EOD_PB_YYYYMMDD.csv'
#)
#ael_variables.add(
#    'pb_report_dir',
#    label='PB Report Directory',
#    cls='string',
#    default=r'/services/frontnt/Task'
#)
ael_variables.add(
    'delete_archived',
    label='Delete archived BP',
    collection=[0, 1],
    cls='int',
    default=1,
    alt='Delete BP objects of archived trades.',
)


def book_acs_block(trade_aggregator, bo_confirm):
    market_hit = trade_aggregator.get_trades()[0]
    vwap = trade_aggregator.get_vwap()
    quantity = trade_aggregator.get_agg_quantity()
    trade_prf_name = market_hit.Portfolio().Name()
    prf_name_split = trade_prf_name.split('-')
    if prf_name_split[-1] == 'TRD':
        prf_name_split[-1] = 'STL'
    else:
        print('ERROR: Trade portfolio does not end with "-TRD".')
        return None
    settle_prf_name = '-'.join(prf_name_split)
    settle_portfolio = acm.FPhysicalPortfolio[settle_prf_name]
    if not settle_portfolio:
        print('ERROR: Portfolio %s not found.' % settle_prf_name)
        return None
    
    obp_block = acm.DealCapturing.CreateNewTrade(market_hit.Instrument())
    obp_block.Counterparty('EQ Derivatives Desk')
    obp_block.Acquirer('EQ Derivatives Desk')
    obp_block.Status('FO Confirmed')
    obp_block.TradeTime('%s 18:00:00' % market_hit.TradeTime()[:10])
    obp_block.ValueDay(market_hit.ValueDay())
    obp_block.AcquireDay(market_hit.AcquireDay())
    obp_block.Quantity(quantity)
    obp_block.Price(vwap)
    obp_block.Premium(obp_block.Calculation().PriceToPremium(calc_space))
    obp_block.Portfolio(settle_portfolio)
    obp_block.MirrorPortfolio(market_hit.Portfolio())

    acm.BeginTransaction()
    try:
        obp_block.RegisterInStorage()
        obp_block.AdditionalInfo().XtpTradeType('FA_BLOCK_TRADE')
        obp_block.Commit()
        if bo_confirm:
            obp_block.Status('BO Confirmed')
            obp_block.Commit()
        acm.CommitTransaction()
    except Exception as exc:
        acm.AbortTransaction()
        print('ERROR: Failed to create block trade: %s' % str(exc))
        return None
    return obp_block

# PB allocation functionality disabled
#def link_pb_trades(trade_aggregator, fa_block):
#    trades = trade_aggregator.get_trades()
#    prf_name = trades[0].Portfolio().Name()
#    process = get_process_class(prf_name)
#    opening_trades = []
#    closing_trade_numbers = []
#    for trade in trades:
#        if (process.is_closing(trade) and 
#                process.xtp_type(trade) in process.pb_closing_types):
#            if trade.TrxTrade():    
#                closing_trade_numbers.append(trade.TrxTrade().Oid())
#        else:
#            opening_trades.append(trade)
#    
#    trades_to_link = []
#    for trade in opening_trades:
#        if not trade.ContractTrdnbr() in closing_trade_numbers:
#            trades_to_link.append(trade)
#    
#    if not trades_to_link:
#        print 'WARNING: No PB trades to be linked.'
#        return
#    acm.BeginTransaction()
#    try:
#        for trade in trades_to_link:
#            trade.ContractTrdnbr(fa_block.Oid())
#            trade.Commit()
#        fa_block.ContractTrdnbr(trades_to_link[0].Oid())
#        fa_block.Commit()
#        acm.CommitTransaction()
#    except Exception as exc:
#        acm.AbortTransaction()
#        print 'ERROR: Failed to link trades to block %s. %s' % (fa_block.Oid(), str(exc))


# PB allocation functionality disabled
#def book_pb_block(trade_aggregator, bo_confirm):
#    market_hit = trade_aggregator.get_trades()[0]
#    vwap = trade_aggregator.get_vwap()
#    quantity = trade_aggregator.get_agg_quantity()
#    no_fees_chlist = acm.FChoiceList.Select01(
#        'name="PS No Fees" and list="TradeKey3"', '')
#    
#    obp_block = acm.DealCapturing.CreateNewTrade(market_hit.Instrument())
#    obp_block.Counterparty('JSE')
#    obp_block.Acquirer('PRIME SERVICES DESK')
#    obp_block.Status('FO Confirmed')
#    obp_block.TradeTime(market_hit.TradeTime()[:10] + obp_block.TradeTime()[10:])
#    obp_block.Quantity(quantity)
#    obp_block.Price(vwap)
#    obp_block.Premium(obp_block.Calculation().PriceToPremium(calc_space))
#    obp_block.Portfolio(market_hit.Portfolio())
#    obp_block.Text1('Allocation Process')
#    obp_block.OptKey3(no_fees_chlist)
#    
#    acm.BeginTransaction()
#    try:
#        obp_block.RegisterInStorage()
#        obp_block.AdditionalInfo().XtpTradeType('FA_BLOCK_TRADE')
#        obp_block.Commit()
#        
#        closing_block = obp_block.Clone()
#        closing_block.RegisterInStorage()
#        closing_block.Quantity(-obp_block.Quantity())
#        closing_block.Premium(-obp_block.Premium())
#        closing_block.AdditionalInfo().XtpTradeType('PB_CLOSING_BLOCK')
#        closing_block.Commit()
#        if bo_confirm:
#           obp_block.Status('BO Confirmed')
#           obp_block.Commit()
#        closing_block.Status('BO Confirmed')
#        closing_block.Commit()
#        acm.CommitTransaction()
#    except Exception as exc:
#        acm.AbortTransaction()
#        print 'ERROR: Failed to create block trade: %s' % str(exc)
#        return None
#    
#    closing_block.TrxTrade(obp_block)
#    closing_block.Commit()
#    obp_block.TrxTrade(closing_block)
#    obp_block.Commit()
#    
#    link_pb_trades(trade_aggregator, obp_block)
#    return obp_block


def generate_trades(alloc_container, booking_func, bo_confirm=True):
    obp_trades = []
    for trade_key in alloc_container['opening']:
        obp_block = None
        if trade_key in alloc_container['closing']:
            if not alloc_container['opening'][trade_key].equals(
                    alloc_container['closing'][trade_key]):
                opening_agg = alloc_container['opening'][trade_key]
                closing_agg = alloc_container['closing'][trade_key]
                opening_agg.extend(closing_agg.get_trades())
                obp_block = booking_func(opening_agg, bo_confirm)
        else:
            opening_agg = alloc_container['opening'][trade_key]
            obp_block = booking_func(opening_agg, bo_confirm)
        
        if obp_block:
            obp_trades.append(obp_block)
    return obp_trades


def process_portfolios(portfolios, start_date, book_func):
    generated_trades = []
    for portfolio in portfolios:
        process = get_process_object(portfolio.Name(), start_date)
        print('Processing portfolio: %s' % process._portfolio_name)
        for ins_name in process.get_ins_names():
            trade_items = process.get_trade_items(ins_name)
            trade_container = process.get_alloc_container(trade_items)
            obp_trades = generate_trades(trade_container, book_func)
            generated_trades.extend(obp_trades)
    return generated_trades


def get_values(trade):
    values = []
    for name, field in FIELDS:
        try:
            value = field(trade)
        except (AttributeError, ValueError) as exc:
            print("ERROR: Failed to get '%s' for trade %s: %s" % (
                name, trade.Oid(), str(exc)))
            value = ''
        values.append(value)
    return values


def generate_report(trades, file_path):
    try:
        with open(file_path, 'wb') as csvfile:
            csvwriter = csv.writer(csvfile, delimiter=',')
            csvwriter.writerow([entry[0] for entry in FIELDS])
            for trade in trades:
                if not trade:
                    continue
                values = get_values(trade)
                csvwriter.writerow(values)
    except Exception as exc:
        print('ERROR: Failed to generate report %s: %s' % (file_path, str(exc)))
    else:
        print('Report successfully generated: %s.' % file_path)


def delete_archived_bp(chart_name):
    state_chart = acm.FStateChart[chart_name]
    if state_chart:
        bps = acm.BusinessProcess.FindByStateChart(state_chart)
        for bp in bps:
            if bp.Subject().IsArchived():
                bp.Delete()
        print('Deleted archived BPs.')


def get_file_path(directory, file_name, date):
    """Return complete path to a file."""
    file_path = os.path.join(directory, file_name)
    file_path = file_path.replace('YYYYMMDD', date.replace('-', ''))
    return file_path


def get_start_date(ael_params):
    if ael_params['date_selection'] == 'Date Today':
        return DATE_TODAY
    elif ael_params['date_selection'] == 'Last Business Day':
        return LAST_BUSINESS_DAY
    return acm_date(ael_params['start_date'])


def ael_main(ael_params):
    start_date = get_start_date(ael_params)
    if ael_params['acs_run']:
        portfolios = ael_params['acs_query_folder'].Query().Select()
        acs_blocks = process_portfolios(portfolios, start_date, book_acs_block)
        print('Generated %s ACS Block Trades.' % len(acs_blocks))
        report_path = get_file_path(ael_params['acs_report_dir'],
                                    ael_params['acs_report_file'], DATE_TODAY)
        generate_report(acs_blocks, report_path)
    
    if ael_params['delete_archived']:
        delete_archived_bp(STATE_CHART_NAME)
    
    # PB allocation functionality disabled
    #if ael_params['pb_run']:
    #    portfolios = ael_params['pb_query_folder'].Query().Select()
    #    pb_blocks = process_portfolios(portfolios, start_date, book_pb_block)
    #    print 'Generated %s PB Block Trades.' % len(pb_blocks)
    #    report_path = get_file_path(ael_params['pb_report_dir'],
    #                                ael_params['pb_report_file'], DATE_TODAY)
    #    generate_report(pb_blocks, report_path)

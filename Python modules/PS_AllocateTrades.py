'''
Date                    : 2011-07-15
Purpose                 : This script is required to aggregate an allocation portfolio and create an allocation trade which will then be split.
Department and Desk     : Front Office - Prime Services
Requester               : Francois Henrion/ Herman Levin
Developer               : Zaakirah Kajee
CR Number               : 713436

HISTORY
================================================================================
Date        Change no      Developer          Description
--------------------------------------------------------------------------------
2012-05-16  C194115        Peter Fabian       Added support for calculation of the fees on CFD trades BEFORE the allocation
2012-06-18  C264971        Peter Fabian       Removed calculation of SET before the allocation
2012-06-18  C278377        Peter Kutnik       Removed rounding of prices
2012-11-30  C620460        Peter Fabian       Removed calculation and storing of CFD fee as Payment before the allocation
2014-06-16  2054154        Ondrej Bahounek    Create csv file during allocation process.
                                              Add description to each target portfolio.
                                              Enable to choose allocation trade status (FO Confirmed or Simulated).
                                              Update previously created and unvoided allocation trade with new values.
2014-08-12  2194554        Ondrej Bahounek    Sort instruments by name. Improve adding date to ouptut filename.
2015-10-06  3139848        Ondrej Bahounek    XtpTradeType relation completely removed.
2018-04-17  CHG1000368737  Ondrej Bahounek    Accommodate OD/GU trades in the allocation process.
2019-06-13  CHG1001882656  Tibor Reiss        Create block trade which is later voided by the 2nd allocation script
                                              Rerunnable any number of times
2019-09-13  CHG1002255241  Tibor Reiss        FAU-308: Remove mirror ref from block trade
2019-09-16  INC1014719870  Tibor Reiss        Roll back: addinfo should be outside of transaction (in production the
                                              transaction did not work but could not reproduce in dev environment)
2020-03-16  FAPE-228       Tibor Reiss        Change option key filter condition
'''

import csv
import os
from copy import deepcopy
from logging import DEBUG, INFO

import acm
from FBDPCommon import toDate

from at_ael_variables import AelVariableHandler
from at_logging import getLogger
from at_addInfo import save as ai_save


LOGGER = getLogger(__name__)
SIMULATED = 'Simulated'
FO_CONFIRMED = 'FO Confirmed'
TEXT1_ALLOC_PROCESS = 'Allocation Process'
ALLOWED_TRADE_STATUS = [SIMULATED, FO_CONFIRMED]

XTP_TRADE_TYPE_BLOCK_TRADE = "PB_BLOCK_TRADE"
XTP_TRADE_TYPE_ALLOCATION = "PB_ALLOCATION"

TEMP_CALC_SPACE = acm.Calculations().CreateCalculationSpace(acm.GetDefaultContext(), 'FPortfolioSheet')
# columns and their indices of output file:
COL_NR_STOCK = 0
COL_NR_BUY_SELL = 1
COL_NR_PRICE = 2
COL_NR_QUANTITY = 3
COL_NR_FIRST_FUND = 4
ALLOCATE_SECTION = 'Allocate Trade Quantities:'
FUNDS_COL = 'Stock code'
BUY_SELL_BUY = 'Buy'
BUY_SELL_SELL = 'Sell'


def weighted_average_price(trades, total_quantity):
    ''' Compute weighted average price of trades. '''
    sum_premium = 0.0
    for trade in trades:
        trade_premium = trade.Price() * trade.Quantity()
        sum_premium = sum_premium + trade_premium
    return sum_premium / total_quantity


class PositionBlockTrade(object):
    '''
        This class is used to store down the positions that are generated for the allocation process.
        It has attributes that describe the instrument, whether it is a buy or sell, the portfolio,
        position, price, strate fees, trade type, allocation trade created and the underlying trades
        to the positions.
    '''

    trade_status = SIMULATED  # implicit type of all newly created trades

    def __init__(self, trades, instrument_name, portfolio_name, buysell, block_trade):
        self.trades = trades
        self.instrument = acm.FInstrument[instrument_name]
        self.quotation = self.instrument.Quotation().Name()
        self.block_trade = block_trade
        self.buysell = buysell
        self.portfolio_name = portfolio_name
        self.quantity = None
        self.price = None
        self.calculate_quantity()

    def calculate_quantity(self):
        virtual_pf = acm.FAdhocPortfolio()
        for trade in self.trades:
            virtual_pf.Add(trade)
        TEMP_CALC_SPACE.Clear()
        top_node = TEMP_CALC_SPACE.InsertItem(virtual_pf)
        portfolio_grouper = acm.FAttributeGrouper('Trade.Portfolio')
        top_node.ApplyGrouper(portfolio_grouper)
        TEMP_CALC_SPACE.Refresh()
        portfolio_iter = top_node.Iterator().Clone().FirstChild()
        instrument_iter = portfolio_iter.Clone().FirstChild()
        self.quantity = TEMP_CALC_SPACE.CreateCalculation(instrument_iter.Tree(), 'Quantity').Value()
        try:
            self.price = weighted_average_price(self.trades, self.quantity)
        except ZeroDivisionError:
            self.price = 0.0

    def __lt__(self, other):
        return self.instrument.Name() < other.instrument.Name()

    def create_block_trade(self):
        '''
            This method creates the block trade based on the daily trades in the allocation portfolio.
            The free text 1 field will be set to "Allocation Process".
        '''
        acm.BeginTransaction()
        try:
            if self.block_trade:
                t_clone = self.block_trade.StorageImage()
            else:
                t_clone = self.trades[0].StorageNew()
                self.block_trade = t_clone
            ai_list = t_clone.AddInfos()
            for ai in ai_list[:]:
                ai.Delete()
            t_clone.Status(PositionBlockTrade.trade_status)
            t_clone.Quantity(self.quantity)
            t_clone.Price(self.price)
            premium = -1.0 * self.quantity * self.price
            if self.quotation == "Per 100 Units":
                premium = premium / 100.0
            t_clone.Premium(premium)
            t_clone.Text1(TEXT1_ALLOC_PROCESS)
            t_clone.OptionalKey('')
            t_clone.ContractTrade(None)
            t_clone.ConnectedTrade(None)
            t_clone.MirrorTrade(None)
            t_clone.TrxTrade(None)
            t_clone.Trader(acm.User())
            t_clone.Commit()
            acm.CommitTransaction()
        except Exception as e:
            acm.AbortTransaction()
            msg = "Error while creating block trade for {} {}" \
                .format(self.instrument.Name(), self.buysell)
            LOGGER.exception(msg)
            raise RuntimeError(msg)
        try:
            acm.PollDbEvents()
            t_clone = self.block_trade.StorageImage()
            t_clone.ContractTrade(self.block_trade)
            t_clone.ConnectedTrade(self.block_trade)
            t_clone.Commit()
            ai_save(self.block_trade, "XtpTradeType", XTP_TRADE_TYPE_BLOCK_TRADE)
        except:
            msg = "Could not update contract trade number while creating block " \
                  "trade for {} {}".format(self.instrument.Name(), self.buysell)
            LOGGER.exception(msg)
            raise RuntimeError(msg)
        LOGGER.info("Trade with oid {} committed".format(self.block_trade.Oid()))

    def process_and_link_trades(self):
        '''
            This method will process all the underlying trades in a position. It will set the contract ref
            and the Free text 1 field to read "Allocation Process" and .
        '''
        acm.BeginTransaction()
        try:
            for trade in self.trades:
                trade.Contract(self.block_trade.Oid())
                trade.Text1(TEXT1_ALLOC_PROCESS)
                trade.Commit()
            acm.CommitTransaction()
        except:
            acm.AbortTransaction()
            msg = ("ERROR: updating of underlying trades failed for block trade {}."
                   "Please rerun this script as a TCU user."
                   .format(self.block_trade.Oid()))
            raise RuntimeError(msg)


def process_positions(alloc_portfolios, for_date, stocks):
    LOGGER.info("Processing positions for date {}, stocks {}, portfolio {}"
                .format(for_date, ','.join(stock.Name() for stock in stocks),
                        ','.join(pf.Name() for pf in alloc_portfolios)))
    query_alloc_trades = query_get_alloc_trades(alloc_portfolios, for_date, stocks)
    query_block_trades = query_get_block_trades(alloc_portfolios, for_date, stocks)
    candidate_trades = query_block_trades.Select()
    block_trades = [trade for trade in candidate_trades if trade.Contract().Oid() == trade.Oid()]
    LOGGER.debug("Number of block trades = {}".format(len(block_trades)))
    positions_block_trades = generate_allocation_positions([query_alloc_trades], block_trades)
    for pos in positions_block_trades:
        try:
            pos.create_block_trade()
            acm.PollDbEvents()
            pos.process_and_link_trades()
        except:
            LOGGER.exception("")
    return positions_block_trades


def generate_allocation_positions(queries, block_trades):
    '''
        Generate the positions that will determine block trades.
    '''
    positions = []
    block_trades_reserved = []
    portfolio_grouper = acm.FAttributeGrouper('Trade.Portfolio')
    buy_sell_grouper = acm.Risk.GetGrouperFromName('Trade BuySell')
    calc_space = acm.Calculations().CreateCalculationSpace(acm.GetDefaultContext(), 'FPortfolioSheet')
    for q in queries:
        top_node = calc_space.InsertItem(q)
    top_node.ApplyGrouper(acm.FChainedGrouper([portfolio_grouper, buy_sell_grouper]))
    calc_space.Refresh()

    if top_node.NumberOfChildren():
        portfolio_iter = top_node.Iterator().Clone().FirstChild()
        while portfolio_iter:
            portfolio_name = portfolio_iter.Tree().Item().StringKey()
            LOGGER.debug("PORTFOLIO = {}".format(portfolio_name))
            buysell_iter = portfolio_iter.Clone().FirstChild()
            while buysell_iter:
                buysell = buysell_iter.Tree().Item().StringKey()
                instrument_iter = buysell_iter.Clone().FirstChild()
                while instrument_iter:
                    instrument_name = instrument_iter.Tree().Item().StringKey()
                    LOGGER.debug("\tINSTRUMENT = {}".format(instrument_name))
                    try:
                        block_trade = None
                        block_trade_candidates = [t for t in block_trades
                                                  if t.Instrument().Name() == instrument_name
                                                  and t.Portfolio().Name() == portfolio_name
                                                  and t.Oid() not in block_trades_reserved]
                        LOGGER.debug("\t\tCANDIDATES")
                        for t in block_trade_candidates:
                            LOGGER.debug("\t\toid={} quantity={}".format(t.Oid(), t.Quantity()))
                        if len(block_trade_candidates) > 2:
                            raise RuntimeError("Too many block trades!")
                        if len(block_trade_candidates) > 0:
                            block_trade = block_trade_candidates[0]
                        if block_trade:
                            block_trades_reserved.append(block_trade.Oid())
                            LOGGER.debug("\t\tRESERVED {}".format(block_trade.Oid()))
                        position = PositionBlockTrade(instrument_iter.Tree().Item().Trades().AsList(),
                                               instrument_name, portfolio_name, buysell, block_trade)
                        positions.append(position)
                    except:
                        LOGGER.exception("Could not generate allocation position for {} {} {} "
                                         .format(portfolio_name, instrument_name, buysell))
                    instrument_iter = instrument_iter.NextSibling()
                buysell_iter = buysell_iter.NextSibling()
            portfolio_iter = portfolio_iter.NextSibling()
    # Block trades which are not part of block_trades_reserved need to be set to zero.
    for t in block_trades:
        if t.Oid() not in block_trades_reserved:
            LOGGER.debug("Zero out trade {}".format(t.Oid()))
            try:
                t_clone = t.StorageImage()
                t_clone.Quantity(0.0)
                t_clone.Price(0.0)
                t_clone.Premium(0.0)
                t_clone.Text1(TEXT1_ALLOC_PROCESS)
                t_clone.OptionalKey('')
                t_clone.ContractTrade(t)
                t_clone.Commit()
            except:
                msg = "Could not update block trade {} to zero!" \
                      .format(t.Oid())
                LOGGER.exception(msg)
    return positions


def query_get_alloc_trades(portfolio_list, date, stocks_list=None):
    query = query_get_trades(portfolio_list, date, stocks_list)
    # Get all active allocation trades
    query.AddAttrNode('Status', 'NOT_EQUAL', 'Simulated')
    query.AddAttrNode('Status', 'NOT_EQUAL', 'Void')
    query.AddAttrNode('Status', 'NOT_EQUAL', 'Terminated')
    or_node = query.AddOpNode('OR')
    or_node.AddAttrNode('Text1', 'EQUAL', '')
    or_node.AddAttrNode('Text1', 'EQUAL', TEXT1_ALLOC_PROCESS)
    or_node = query.AddOpNode('OR')
    or_node.AddAttrNode('OptionalKey', 'RE_LIKE_NOCASE', 'XTP*JSE*')
    and_node = or_node.AddOpNode('AND')
    for xtp_type in ["", XTP_TRADE_TYPE_ALLOCATION, XTP_TRADE_TYPE_BLOCK_TRADE]:
        and_node.AddAttrNode('AdditionalInfo.XtpTradeType', 'NOT_EQUAL', xtp_type)
    return query


def query_get_block_trades(portfolio_list, date, stocks_list=None):
    query = query_get_trades(portfolio_list, date, stocks_list)
    # Get all non-void trades which are not allocation trades (the latter have optional key starting with XTP_JSE)
    query.AddAttrNode('Status', 'NOT_EQUAL', 'Void')
    query.AddAttrNode('Text1', 'EQUAL', TEXT1_ALLOC_PROCESS)
    query.AddAttrNode('OptionalKey', 'EQUAL', '')
    query.AddAttrNode('AdditionalInfo.XtpTradeType', 'EQUAL', XTP_TRADE_TYPE_BLOCK_TRADE)
    return query


def query_get_trades(portfolio_list, date, stocks_list=None):
    ''' Generate a query that selects all trades that need to
        be allocated.
    '''
    query = acm.CreateFASQLQuery('FTrade', 'AND')

    or_node = query.AddOpNode('OR')
    or_node.AddAttrNode('Instrument.InsType', 'EQUAL', 'Stock')
    or_node.AddAttrNode('Instrument.InsType', 'EQUAL', 'ETF')

    if stocks_list:
        or_node = query.AddOpNode('OR')
        for stock in stocks_list:
            or_node.AddAttrNode('Instrument.Name', 'EQUAL', stock.Name())

    query.AddAttrNode('TradeTime', 'GREATER_EQUAL', date)
    query.AddAttrNode('TradeTime', 'LESS_EQUAL', date)

    for pf in portfolio_list:
        if pf.Compound():
            # Add the sub portfolios to the query
            or_node = query.AddOpNode('OR')
            for phys_pf in pf.AllPhysicalPortfolios():
                or_node.AddAttrNode('Portfolio.Name', 'EQUAL', phys_pf.Name())
        else:
            query.AddAttrNode('Portfolio.Name', 'EQUAL', pf.Name())
    return query


def create_file_rows(portfolio_list, description_list):
    ''' Create rows for output file.
    Return: tuple (array of header rows, dictionary of data rows template)
    '''
    BUY_SELL_COL = 'Buy / Sell'
    PRICE_COL = 'Price'
    QUANT_COL = 'Quantity'
    PORTFS_COLS = [portf.Name() for portf in portfolio_list]
    STOCK_CODE = ""

    header_rows = []
    _row = [ALLOCATE_SECTION] + [""]*(COL_NR_FIRST_FUND - 1) + description_list
    header_rows.append(_row)

    _row = [FUNDS_COL, BUY_SELL_COL, PRICE_COL, QUANT_COL]
    _row.extend(PORTFS_COLS)
    header_rows.append(_row)

    init_extend = [0 for i in range(len(_row) - COL_NR_PRICE)]
    _row1 = [STOCK_CODE, BUY_SELL_BUY]
    _row1.extend(init_extend)
    _row2 = [STOCK_CODE, BUY_SELL_SELL]
    _row2.extend(init_extend)

    DATA_ROWS_TEMPLATE = {
                          BUY_SELL_BUY: _row1[:],
                          BUY_SELL_SELL: _row2[:]
                         }

    return (header_rows, DATA_ROWS_TEMPLATE)


def get_desc_list(descr_str):
    '''
        Create list of descriptions from one string.
        Each description in source string must be separated by comma.
    '''
    stripped = descr_str.strip()
    if stripped.endswith(','):
        stripped = stripped[:-1]
    list_str = stripped.split(',')
    return [l.strip() for l in list_str]


def write_to_file(header_rows, alloc_dict, fullpath):
    '''
        Create file with rows from header_rows and alloc_dict.
        Rows are sorted by instrument name.
    '''
    with open(fullpath, 'wb') as csvfile:
        writer = csv.writer(csvfile)
        for row in header_rows:
            writer.writerow(row)
        for key in sorted(alloc_dict.keys()):
            for buysell in sorted(alloc_dict[key].keys()):
                if alloc_dict[key][buysell][COL_NR_QUANTITY]:  # write all nonzero quantity rows
                    writer.writerow(alloc_dict[key][buysell])


phys_port_list = acm.FPhysicalPortfolio.Select('')
STOCK_LIST = acm.FStock.Select('')
directory_selection = acm.FFileSelection()
directory_selection.PickDirectory(True)
directory_selection.SelectedDirectory('')
default_file_name = 'allocationTrades_[date].csv'

ael_variables = AelVariableHandler()

ael_variables.add(
    'allocportfolio',
    label='Allocation Portfolios',
    cls='FPhysicalPortfolio',
    collection=phys_port_list,
    default=None,
    mandatory=True,
    multiple=True,
    alt='Allocation portfolios for stocks.'
    )
ael_variables.add(
    'portfolios',
    label='Target Portfolios',
    cls='FPhysicalPortfolio',
    collection=phys_port_list,
    default=None,
    mandatory=True,
    multiple=True,
    alt='Portfolios for split trades.'
    )
ael_variables.add(
    'descriptions',
    label='Target Descriptions',
    cls='string',
    collection=None,
    default=None,
    mandatory=True,
    multiple=False,
    alt='Description of each target portfolio with same ordering.'
    )
ael_variables.add(
    'stocks',
    label='Stock List',
    cls='FInstrument',
    collection=STOCK_LIST,
    default=None,
    mandatory=False,
    multiple=True,
    alt='Instrument List. If blank, will run for all instruments.'
    )
ael_variables.add(
    'trade_status',
    label='Trade Status',
    cls='string',
    collection=ALLOWED_TRADE_STATUS,
    default=SIMULATED,
    mandatory=True,
    multiple=False,
    alt='Trade status for newly created trades'
    )
ael_variables.add(
    'for_date',
    label='Date',
    cls='string',
    collection=[acm.Time.DateToday(), 'Today'],
    default='Today',
    mandatory=True,
    multiple=False
    )
ael_variables.add(
    'filename',
    label='File',
    cls='string',
    default=default_file_name,
    mandatory=True,
    multiple=False,
    alt='Name of output file'
    )
ael_variables.add(
    'directory',
    label='Output Directory',
    cls=directory_selection,
    default=directory_selection,
    mandatory=True,
    multiple=True,
    alt='Output path'
    )
ael_variables.add(
    'logging_level',
    label='Logging level',
    cls='int',
    collection=[DEBUG, INFO],
    default=INFO,
    mandatory=False,
    multiple=False
    )
ael_gui_parameters = {'windowCaption': 'Prime Broker: 1st Allocation Script'}


def ael_main(ael_dict):
    LOGGER.setLevel(ael_dict['logging_level'])
    LOGGER.msg_tracker.reset()

    for_date = toDate(ael_dict['for_date'])
    alloc_portfolios = ael_dict['allocportfolio']
    target_portfolios = ael_dict['portfolios']
    descriptions = ael_dict['descriptions']
    stocks = ael_dict['stocks']
    output_directory = str(ael_dict['directory'].SelectedDirectory())
    file_name = str(ael_dict['filename'])
    trade_status = str(ael_dict['trade_status'])

    # check the path
    if not os.path.isdir(output_directory):
        raise ValueError('ERROR: "{0}" is not a valid directory.'.format(output_directory))
    if not os.access(output_directory, os.W_OK):
        raise ValueError('ERROR: "{0}" directory has not write access.'.format(output_directory))

    # check file
    if not file_name.endswith('.csv'):
        file_name += '.csv'
    file_name = file_name.replace('[date]', for_date)
    while os.path.isfile(os.path.join(output_directory, file_name)):  # create unique file
        file_name_raw = file_name[:-4]
        file_name = file_name_raw + '_1' + '.csv'

    # check the trade status
    if trade_status not in ALLOWED_TRADE_STATUS:
        raise ValueError('ERROR: Invalid Trade status "{0}".'.format(trade_status))
    PositionBlockTrade.trade_status = trade_status

    # check the target lists and their matching with portfolios
    description_list = get_desc_list(descriptions)
    if len(target_portfolios) != len(description_list):
        raise ValueError('ERROR: Number of Target portfolios does not match number of Target descriptions')

    positions_block_trades = process_positions(alloc_portfolios, for_date, stocks)

    LOGGER.info("\n{}".format('*' * 90))
    if len(positions_block_trades) > 0:
        positions_block_trades.sort()
        LOGGER.info("{0:{width}}{1:{width}}{2:{width2}}{3:{width2}}{4}"
                    .format('STOCK', 'POSITION', 'PRICE', 'BLOCK TRADE', 'UNDERLYING', width=15, width2=18))
        LOGGER.info("{und_s:{width}}{und_l:{width}}{und_s:{width2}}{und_l:{width2}}{und_l}"
                    .format(und_s='=======', und_l='==========', width=15, width2=18))
    else:
        LOGGER.info("No positions to process for portfolios {}, stocks {}, for date {}."
                    .format(','.join(pf.Name() for pf in alloc_portfolios),
                            ','.join(stock.Name() for stock in stocks), for_date))

    (header_rows, data_rows_template) = create_file_rows(target_portfolios, description_list)
    '''
    Help for records_dict:
    records_dict: key = insName;                value = record(dictionary) 
    record:       key = ([Buy|Sell]);           value = row(dictionary)
    row:          key =  [COL_NR_STOCK|COL_NR_PRICE|COL_NR_QUANTITY]
    '''
    records_dict = {}
    for pos in positions_block_trades:
        ins_name = pos.instrument.Name()
        record = records_dict.get(ins_name, None)
        if record is None:
            record = deepcopy(data_rows_template)
            for r in record.values():
                r[COL_NR_STOCK] = ins_name
        row = record[pos.buysell]
        row[COL_NR_PRICE] = pos.price
        row[COL_NR_QUANTITY] = pos.quantity
        records_dict[ins_name] = record
        LOGGER.info("{0:{width}}{1:{width}}{2:{width2}}{3:{width2}}{4}"
                    .format(pos.instrument.Name(), str(pos.quantity), str(pos.price),
                            str(pos.block_trade.Oid()), str(pos.trades), width=15, width2=18))

    if len(records_dict) > 0:
        write_to_file(header_rows, records_dict, os.path.join(output_directory, file_name))
    else:
        LOGGER.warning("WARNING: No block trade.")
    
    if LOGGER.msg_tracker.errors_counter:
        raise RuntimeError("ERRORS occurred. Please check the log.")

    LOGGER.info("Completed successfully")

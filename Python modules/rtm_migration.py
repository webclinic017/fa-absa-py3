"""
Description: 
    Trade migration script for Risk Transfer Mechanism.
    
    Stock and ETF positions in the old portfolios will be migrated into 
    the new portfolios in the following way:
        1. Open positions settling on T+3, T+2 and T+1 (as of today) will
           be migrated with one trade per position with the trade date of
           original trades and their average traded price
        2. All settled positions (as of today COB) will be migrated as settled
           with one trade per position with today's trade date and value day
           and today's closing price (trade date = value day; settling on T+0)
        3. Zero positions won't be migrated

Project:     Risk Transfer Mechanism
Developer:   Jakub Tomaga
Date:        06/12/2017
"""


import os
import csv
import time
import string

import acm
from at_ael_variables import AelVariableHandler
from at_report import CSVReportCreator


# Price types
CLOSING_PRICE = 'Closing Price'
WAP = 'Weighted Average Price'
CALCULATED_WAP = 'Calculated Weighted Average Price'

PRICE_TYPES = [
    CLOSING_PRICE,
    WAP,
    CALCULATED_WAP
]

# Columns to calculate on trades
POSITION_COLUMN = 'Portfolio Position'
WAP_COLUMN = 'ABSAWeighted Average Price'
CLOSING_PRICE_COLUMN = 'Closing Price'


# Party definitions (always select by DB id to avoid re-naming issues)
JSE = acm.FParty[18247]
PRIME_SERVICES_DESK = acm.FParty[32737]


# Calendar for adjusting business days
CALENDAR = acm.FCalendar['ZAR Johannesburg']

my_calc_space = acm.Calculations().CreateCalculationSpace(acm.GetDefaultContext(), 'FPortfolioSheet')


class RTMTrade(object):
    """Simple trade representation.
    
    Attributes:
        - Stock (security)
        - Position (to be used as quantity)
        - Price
    
    """
    def __init__(self, security, position, price):
        """Initialize the trade."""
        self.security = acm.FInstrument[security]
        self.position = position
        self.price = price
    
    def book(self, portfolio, settle_offset, trade_date, status, revert=False):
        """Book the trade.

        Set revert to True if you want to close the position.
        """
        # Trade date and value date (based on settlement cycle)
        value_date = CALENDAR.AdjustBankingDays(trade_date, settle_offset)
        # Create trade
        trade = acm.FTrade()
        trade.Instrument(self.security)
        trade.Currency('ZAR')
        trade.Counterparty(JSE)
        trade.Acquirer(PRIME_SERVICES_DESK)
        trade.Price(self.price)
        if revert:
            trade.Quantity(-1 * self.position)
            trade.Premium(self.position * self.price / 100)
        else:
            trade.Quantity(self.position)
            trade.Premium(-1 * self.position * self.price / 100)
        trade.Portfolio(portfolio)
        trade.Status(status)
        trade.TradeTime(trade_date)
        trade.Trader(acm.User())
        trade.ValueDay(value_date)
        trade.AcquireDay(value_date)
        trade.RegisterInStorage()
        trade.AdditionalInfo().Broker_Fee_Exclude(True)
        
        trade.Commit()
        row = [
            trade.Oid(),
            trade.Instrument().Name(),
            trade.Portfolio().Name(),
            trade.Quantity(),
            trade.Price(),
            trade_date,
            value_date,
            my_calc_space.CalculateValue(trade, 'Portfolio Cash End').Number(),
            my_calc_space.CalculateValue(trade, 'Total Val End').Number()
        ]
        print(row)
        return row


def get_weighted_average_price(trades, position):
    """Return weighted average price from all trades in position.

    Note: How to calculate WAP from closed positions?
    """
    if position == 0.0:
        return 0.0

    sum = 0.0
    for trade in trades:
        if trade.Status() in ('Void', 'Simulated'):
            continue
        trade_product = trade.Price() * trade.Quantity()
        sum = sum + trade_product
    return sum / position


def get_trades(portfolio, price_type, selection, trade_date):
    """Return all the trades with quantities and prices.

    Note: Calculation space simulates the trading manager from code:
    1. Create portfolio sheet
    2. Insert portfolio
    3. Group by instrument type
    4. Iterate through all instrument types
    5. If instrument type is Stock or ETF iterate through instruments
    6. Calculate position, closing price, weighted average price and calculated
       average price (how I would do it - see the function above) - price type
       is chosen from the task
    7. All the securities and prices are returned for booking considerations.
    
    Note: Position for Simulated trades is 0. If we need to move Simulated,
    we might need to consider quuantity instead, see below how:
    
    quantity = calc_space.CreateCalculation(instrument_iter.Tree(), 'Quantity').Value()
    
    """
    
    # List of trades to be booked
    trades = []
    # Create portfolio sheet
    calc_space = acm.Calculations().CreateCalculationSpace(acm.GetDefaultContext(), 'FPortfolioSheet')
    calc_space.SimulateGlobalValue('Portfolio Profit Loss End Date', 'Custom Date')
    calc_space.SimulateGlobalValue('Portfolio Profit Loss End Date Custom', trade_date)
    # Insert portfolio
    top_node = calc_space.InsertItem(selection)
    # Apply grouper
    ins_type_grouper = acm.Risk.GetGrouperFromName('Instrument Type')
    top_node.ApplyGrouper(acm.FChainedGrouper([ins_type_grouper]))
    calc_space.Refresh()
    # Iterate through the top level (portfolio)
    if top_node.NumberOfChildren():
        ins_type_iter = top_node.Iterator().Clone().FirstChild()
        # Iterate through instrument types
        while ins_type_iter:
            ins_type = ins_type_iter.Tree().Item().StringKey()
            instrument_iter = ins_type_iter.Clone().FirstChild()
            # If instrument type is Stock or ETF
            if ins_type not in ('Stock', 'ETF'):
                ins_type_iter = ins_type_iter.NextSibling()
                continue
            # Iterate through individual instruments
            while instrument_iter:
                instrument = instrument_iter.Tree().Item().StringKey()
                # Calculate position
                position = calc_space.CreateCalculation(instrument_iter.Tree(), POSITION_COLUMN).Value()
                # Calculate price based on task parameters
                if price_type == CLOSING_PRICE:
                    try:
                        price = calc_space.CreateCalculation(instrument_iter.Tree(), CLOSING_PRICE_COLUMN).Value().Number()                    
                    except Exception as ex:
                        price = calc_space.CreateCalculation(instrument_iter.Tree(), CLOSING_PRICE_COLUMN).Value() 
                elif price_type == WAP:
                    price = calc_space.CreateCalculation(instrument_iter.Tree(), WAP_COLUMN).Value()
                elif price_type == CALCULATED_WAP:
                    price = get_weighted_average_price(instrument_iter.Tree().Item().Trades().AsList(), position)
                else:
                    # You can add more price types here
                    price = 0.0
                trade = RTMTrade(instrument, position, price)
                trades.append(trade)
                instrument_iter = instrument_iter.NextSibling()               
            ins_type_iter = ins_type_iter.NextSibling()
    calc_space.RemoveGlobalSimulation('Portfolio Profit Loss End Date')
    calc_space.RemoveGlobalSimulation('Portfolio Profit Loss End Date Custom')
    return trades


class RTMTradeMigrationReport(CSVReportCreator):
    """Generic report to expose how sweeping amounts are calculated."""
    def __init__(self, full_file_path, data):
        file_name = os.path.basename(full_file_path)
        file_name_only = os.path.splitext(file_name)[0]
        file_suffix = os.path.splitext(file_name)[1][1:]
        file_path = os.path.dirname(full_file_path)

        self.data = data
        super(RTMTradeMigrationReport, self).__init__(file_name_only, file_suffix, file_path)

    def _collect_data(self):
        """Collect data relevant for the report."""
        for row in self.data:
            self.content.append(row)

    def _header(self):
        """Return columns of the header."""
        header = [
            "Trade",
            "Instrument",
            "Portfolio",
            "Quantity",
            "Price",
            "Trade Date",
            "Value Day",
            "Cash End",
            "Val End"
        ]
        return header


# Parameters for the task
ael_variables = AelVariableHandler()
ael_variables.add("input_file",
                  label="Input file")
ael_variables.add("output_file",
                  label="Output file")
ael_variables.add("date",
                  label="Date",
                  default=acm.Time().DateToday())
ael_variables.add("status",
                  label="Status",
                  collection=["Simulated", "FO Confirmed", "BO Confirmed"])


SETTLE_OFFSET = ['T+3', 'T+2', 'T+1', "S"]
TF_FILENAME_MASK = "{0}_{1}"

                  
def ael_main(config):
    """Entry point of the script."""
    start = time.time()
    input_file = config["input_file"]
    date = config["date"]
    status = config["status"]
    TRADE_DATES = {
        'T+3': date,
        'T+2': CALENDAR.AdjustBankingDays(date, -1),
        'T+1': CALENDAR.AdjustBankingDays(date, -2),
        'S': date
    }
    
    with open(input_file, 'rb') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        data = []
        for row in reader:
            skip = row[2]
            if skip == "FALSE":
                original_portfolio = acm.FPhysicalPortfolio[row[0]]
                target_portfolio = acm.FPhysicalPortfolio[row[1]]
                if original_portfolio == None:
                    print("Original portfolio {0} doesn't exist.".format(row[0]))
                    continue
                if target_portfolio == None:
                    print("Target portfolio {0} doesn't exist.".format(row[1]))
                    continue
                
                for offset in SETTLE_OFFSET:
                    try:
                        selection = acm.FTradeSelection[TF_FILENAME_MASK.format(target_portfolio.Name().split('_')[0].split(' Structures')[0], offset)]
                        trade_date = TRADE_DATES[offset]
                        
                        if offset == "S":
                            settle_offset = 0
                            price_type = CLOSING_PRICE
                        else:
                            settle_offset = 3
                            price_type = CALCULATED_WAP                        

                        # Get all the trades to close / open positions from original portfolio
                        trades = get_trades(original_portfolio, price_type, selection, trade_date)
                        #print "Booking trades..."
                        for trade in trades:
                            # Skip closed positions
                            if round(trade.position, 2) != 0.0:
                                # Book reversals in the original portfolio
                                row = trade.book(original_portfolio, settle_offset, trade_date, status, revert=True)
                                data.append(row)
                                # Book opening trades in the target_portfolio
                                row = trade.book(target_portfolio, settle_offset, trade_date, status)
                                data.append(row)
                        #print "Completed successfully."
                    except Exception as ex:
                        print("FAILED: {0}".format(ex))
    fpath_template = string.Template(config['output_file'])
    file_path = fpath_template.substitute(DATE=date.replace("-", ""))
    report = RTMTradeMigrationReport(file_path, data)
    report.create_report()
    end = time.time()
    print("Completed in {0} seconds.".format(end - start))

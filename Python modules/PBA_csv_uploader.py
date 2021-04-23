"""
Project: Prime Brokerage Africa (PBA)
Department: Prime Services
Requester: Francois Henrion
Developer: Ondrej Bahounek, Lester Williams
CR Number: 3506685 (Initial Deployment)

Description:
    The purpose of this script is to take Brokers note file - 
    information received from African Alliances -
    and create agency trades within Front Arena.
    This is a start script.
    Will be run as a batch once a day - in the morning.
    
Prerequisites:
     Brokers note file for given date present in expected directory 

TODO:
    Think about recovery functionality. If booking of any trade fails,
    rerunning this will with the same input file will create same trades as first run.
    (Duplicate trades can occurr - not wanted.)
    Solution1: All in one transaction
    Solution2: Before booking any trade, check some unique identifiers 
        (create date, fund, quantity, instrument) whether trade with these
        values already exists.
          
History:
Date       CR Number Who                    What
"""

import acm
import at_addInfo
import FRunScriptGUI
from PS_Functions import get_pb_fund_shortname
from at_ael_variables import AelVariableHandler

# Hard coded for testing
FILEPATH = r"c:\DEV\Perforce\bahouneo\African Equities\Input data\Brokers notes file.csv"

AGENCY_PORTF_TEMPLATE = "PBA_%(alias)s_Agency1_CR"

COMMISSION_TEXT = "Commission RAW%"

# TODO: file name should be selected by input date
fileFilter = "*.csv"
inputFile = FRunScriptGUI.InputFileSelection(FileFilter=fileFilter)
ael_variables = AelVariableHandler()
ael_variables.add(
    'input_file',
    label = 'File',
    cls = inputFile,
    default = inputFile,
    mandatory = True,
    multiple = True,
    alt = 'Brokers notes file.'
    )

class CounterPartyError(Exception):
    pass


def get_csv_line_by_line(file):
    """Read file's rows one by one.
    
    Expecting one broker note/line per csv file, however catering for multiple lines
    in case the requirement changes in future
    """
    
    cnt = 0
    while True:
        line = file.readline().rstrip()
        if line:
            yield cnt, line
            cnt += 1
        else:
            break
    file.close()

def get_trade_record(header, col_list):
    """Create dictionary of trade's properties. """
    
    trade_record = {}
    for idx in range(len(header)):
        trade_record[header[idx]] = col_list[idx]

    return trade_record

def process_csv_feed(file):
    """Read csv file and return list of trades' properties.
    
    Properties are stored in dictionary with file header columns as keys. 
    """
    
    header          = []
    all_trades_list    = []

    for cnt, line in get_csv_line_by_line(file):
        if cnt == 0:
            # get header
            header = line.split(',')
        else:
            # add trade
            col_list = line.split(',')
            all_trades_list.append(get_trade_record(header, col_list))

    return all_trades_list

def book_trade(tradeRec):
    """Book Agency1 trades.
    
    These are in Simulated status until they are manually confirmed.
    """
    
    trade = acm.FTrade()
    
    # Get client portfolio - should be a Constant Agency
    alias = get_pb_fund_shortname(acm.FParty[tradeRec["Fund Name"]])
    portfolio = acm.FPhysicalPortfolio[AGENCY_PORTF_TEMPLATE % {'alias':alias}]
    trade.Portfolio(portfolio)

    # Find counterparty for given fullname
    counterparties = acm.FParty.Select('type = "Counterparty"')
    if len(counterparties) > 0:
        cp = tradeRec['Counterparty'].strip().upper()
        parties = [party for party in counterparties 
                   if party.Fullname().upper().find(cp) > -1]
        if len(parties) == 1:
            trade.Counterparty(parties[0])
        elif len(parties) > 1:
            raise CounterPartyError("Can't select unique counterparty for '{0}' ({1} found)." \
                                    .format(cp, len(parties)))
        else:
            raise CounterPartyError("Nonexisting counterparty for '%s'" %cp)

    ins = acm.FInstrument[tradeRec['ISIN']]
    trade.Instrument(ins)
    trade.Currency(ins.Currency())
    trade.Status('Simulated')
    
    zar_cal = acm.FInstrument["ZAR"].Calendar()
    trade_time = tradeRec['Trade date']
    settle_day = tradeRec['Settlement date']
    # relative settings should be never used live - only for testing purposes
    if settle_day.endswith("d"):
        settle_day = int(settle_day[:-1])
        trade.TradeTime(zar_cal.AdjustBankingDays(acm.Time.DateToday(), 
            settle_day - ins.SpotBankingDaysOffset()))
        trade.ValueDay(zar_cal.AdjustBankingDays(acm.Time.DateToday(), 
            settle_day))
        trade.AcquireDay(zar_cal.AdjustBankingDays(acm.Time.DateToday(), 
            settle_day))
    else:
        if trade_time.endswith("d"):
            trade_time = int(trade_time[:-1])
            trade.TradeTime(zar_cal.AdjustBankingDays(acm.Time.DateToday(), trade_time))
            trade.ValueDay(zar_cal.AdjustBankingDays(acm.Time.DateToday(), 
                trade_time + ins.SpotBankingDaysOffset()))
            trade.AcquireDay(zar_cal.AdjustBankingDays(acm.Time.DateToday(),
                trade_time + ins.SpotBankingDaysOffset()))
        else:
            trade.TradeTime(tradeRec['Trade date'])
            trade.ValueDay(tradeRec['Settlement date'])
            trade.AcquireDay(tradeRec['Settlement date'])

    qty = tradeRec['Quantity']
    qty = int(qty) if qty else 0
    if tradeRec['Direction'] == 'Sell':
        qty = qty * -1
        
    # store quantity and price in free text2 field
    dictstring = '{"Qty":%s,"Prc":%s}' %(qty, str(round(float(tradeRec['Gross Price']), 4)))
    trade.Text2(dictstring)
    trade.Text1('PBA_Agency_Uploaded')
    trade.Commit()
    print("Agency1 trade created: {0}".format(trade.Oid()))
    
    add_payments(trade, tradeRec)
    set_addinfo(trade, tradeRec)

    return trade.Oid()

def set_addinfo(trade, tradeRec):

    gross_price = tradeRec['Gross Price'] if tradeRec.get('Gross Price') else 0
    at_addInfo.save(trade, 'Gross Price', gross_price)
    
    country = tradeRec['Country'] if tradeRec.get('Country') else ""
    at_addInfo.save(trade, 'Country', country)
    
    gross_consideration = tradeRec['Gross Consideration'] if tradeRec.get('Gross Consideration') else 0
    at_addInfo.save(trade, 'Gross Consideration', gross_consideration)

    # save 100% of Commission in add info for later consumption in final clone 
    commission = tradeRec['Commission'] if tradeRec.get('Commission') else 0
    at_addInfo.save(trade, 'Broker Commission', commission)

    # save sum of fees
    stockexfees = float(tradeRec.get('NSE Fee')) if tradeRec.get('NSE Fee') else 0
    cmalevy     = float(tradeRec.get('CMA Levy')) if tradeRec.get('CMA Levy') else 0
    akslevy     = float(tradeRec.get('CDSC/AKS Levy')) if tradeRec.get('CDSC/AKS Levy') else 0 
    complevy    = float(tradeRec.get('Compensation Fund')) if tradeRec.get('Compensation Fund') else 0
    stampduty   = float(tradeRec.get('Stamp Duty')) if tradeRec.get('Stamp Duty') else 0
    fees        = stockexfees + cmalevy + akslevy + complevy + stampduty
    at_addInfo.save(trade, 'Fees', fees)
    
    is_fully_funded = tradeRec.get('Fully Funded').strip().capitalize()
    is_fully_funded = True if is_fully_funded == "Yes" else False        
    at_addInfo.save(trade, "PB_Fully_Funded", is_fully_funded)
    
    print("Trade {0}: Additional Info added".format(trade.Oid()))


def add_payments(trade, trade_record):
    """Store payments.
    
    Payments: 
        Commission - 70% of a commission*(-1) as a payment.
    """

    payment = acm.FPayment()
    if trade_record.get('Commission'):
        payment.Amount(-float(trade_record.get('Commission')) * 0.7)  # different sign in payments
        payment.Text(COMMISSION_TEXT)
        payment.Currency(trade.Instrument().Currency())
        payment.Type('Cash')
        payment.Party(acm.FParty["PRIME SERVICES DESK"])
        payment.PayDay(trade.AcquireDay())  # use trade dates
        payment.ValidFrom(trade.TradeTime())
        trade.Payments().Add(payment)
        trade.Commit()
        
        print("Trade {0}: Commission Payment added ".format(trade.Oid(), payment.Amount()))
    
def ael_main(ael_dict):
    file_path = str(ael_dict['input_file'])
    print("")
    print("Uploader: Started")
    print("")
    with open(file_path, 'r') as file:
        file_ext = file_path[-4:].strip().lower()
        if file_ext == '.csv':
            all_trades_list = process_csv_feed(file)
            print("Uploader: Trades loaded from Brokers file:", len(all_trades_list))
            for trade_rec in all_trades_list:
                print("")
                book_trade(trade_rec)
        else:
            raise RuntimeError("ERROR: Invalid file extension - '%s' not recognised" %file_ext)

    print("")
    print("Uploader: Completed successfully")
    print("")

"""-----------------------------------------------------------------------------
PURPOSE              :  SBL onto FA
                        FA Sec loan open position fix based on All Open 
                        Positions EOD report from G1.
DESK                 :  SBL PTS, Collateral
DEVELOPER            :  Libor Svoboda
--------------------------------------------------------------------------------

HISTORY
================================================================================
Date        Change no      Developer           Description
--------------------------------------------------------------------------------
2020-06-03  CHG0102113     Libor Svoboda       Initial Implementation
"""
import csv
from collections import defaultdict
from math import copysign

import acm
import sl_functions
from at_ael_variables import AelVariableHandler
from at_logging import getLogger
from sbl_monthly_fee_payments import VALID_SBL_STATUS, regenerate_cashflows


LOGGER = getLogger(__name__)
CALC_SPACE = acm.Calculations().CreateStandardCalculationsSpaceCollection()
PARAMS = {
    'dry_run': True,
    'check_cp': False,
}
ACQUIRERS = (
    'SLBPA1', # SLB PRINCIPAL ACCOUNT
    'SLBPA2', # SLL PRINCIPAL ACCOUNT
    'ABS401', # SLB ABSA SECURITIES LENDING
    'ABS402', # SLL ABSA SECURITIES LENDING
    'ABLNB2', # SLB ABSA BANK NAMIBIAN PRINCIPAL ACC
    'ABLNB1', # SLL ABSA BANK NAMIBIAN PRINCIPAL ACC
)
CALENDAR = acm.FCalendar['ZAR Johannesburg']
TODAY = acm.Time.DateToday()
NEXT_BUSINESS_DAY = CALENDAR.AdjustBankingDays(TODAY, 1)
VAT_RATE = 1.15


ael_variables = AelVariableHandler()
ael_variables.add_input_file(
    'input_file_path',
    'G1 Data File',
    file_filter='*.csv',
    default=r'C:\FA\all_open_%s.csv' % TODAY,
)
ael_variables.add(
    'base_query',
    label='Base Query',
    cls='FStoredASQLQuery',
    default=acm.FStoredASQLQuery['SBL_G1_FA_Open'],
)
ael_variables.add_bool(
    'dry_run',
    label='Dry Run',
    default=1
)
ael_variables.add_bool(
    'check_cp',
    label='Check Lender/Borrower',
    default=0
)


def is_price_incorrect(trade, loan_price):
    ins = trade.Instrument()
    quotation_factor = ins.Quotation().QuotationFactor()
    contract_size = ins.ContractSize()
    loan_price = round(loan_price, 9)
    return (loan_price != round(trade.AllInPrice() * quotation_factor, 9)
            or loan_price != round(contract_size / ins.RefValue(), 9))


def get_party(party_code):
    query = acm.CreateFASQLQuery('FParty', 'AND')
    query.AddAttrNode('AdditionalInfo.SL_G1PartyCode', 'EQUAL', party_code)
    parties = query.Select()
    if parties:
        return parties[0]
    return None


def get_last_trade(contract, end_date):
    trades = [t for t in acm.FTrade.Select('contract=%s' % contract.Oid())
              if (t.Status() in VALID_SBL_STATUS 
                  and t.Instrument().StartDate() <= end_date
                  and t.Text1() != 'FULL_RETURN')]
    trades.sort(key = lambda t: t.Instrument().ExpiryDateOnly())
    if trades:
        return trades[-1]
    return contract


def create_new_loan(original_trade, quantity, start_date, end_date, open_end):
    original_instrument = original_trade.Instrument()
    ins_name = original_instrument.SuggestName()
    sl_cfd = original_instrument.AdditionalInfo().SL_CFD()
    fixed_rate = original_instrument.Legs()[0].FixedRate()

    instrument = original_instrument.StorageNew()
    instrument.Name(ins_name)
    instrument.StartDate(start_date)
    instrument.OpenEnd(open_end)
    if sl_cfd:
        instrument.AdditionalInfo().SL_CFD(True)
    for leg in instrument.Legs():
        leg.StartDate(start_date)
        leg.EndDate(end_date)
        leg.PayDayMethod('None')
        if sl_cfd:  
            leg.RollingPeriodBase(start_date)
            leg.RollingPeriod('1d')
        else:
            fom = acm.Time().FirstDayOfMonth(acm.Time().DateAddDelta(start_date, 0, 1, 0))
            leg.RollingPeriodBase(fom)
            leg.RollingPeriod('1m')
        leg.GenerateCashFlows(fixed_rate)
    instrument.Commit()
    
    trade = original_trade.StorageNew()
    trade_quantity = sl_functions.trade_quantity(quantity, instrument)
    trade.Quantity(trade_quantity)
    trade.Contract(original_trade.Contract())
    trade.OptionalKey(None)
    trade.ValueDay(start_date)
    trade.Instrument(instrument)
    trade.AcquireDay(start_date)
    trade.Status('BO Confirmed')
    trade.ArchiveStatus(0)
    for payment in trade.Payments()[:]:
        trade.Payments().Remove(payment)
    trade.TradeTime('%s 13:00:00' % start_date)
    trade.Commit()
    return trade


def remove_extra_trades(trades, end_date):
    next_business_day = CALENDAR.AdjustBankingDays(end_date, 1)
    for trade in trades:
        ins = trade.Instrument()
        ins_image = ins.StorageImage()
        trade_image = trade.StorageImage()
        leg = ins_image.Legs()[0]
        if ins.StartDate() < end_date:
            LOGGER.info('Terminating trade %s.' % trade.Oid())
            ins_image.OpenEnd('Terminated')
            leg.EndDate(end_date)
        elif ins.StartDate() == end_date:
            if ins.OpenEnd() == 'Terminated':
                LOGGER.info('Terminated trade %s, setting end date to %s.' 
                            % (trade.Oid(), end_date))
                leg.EndDate(end_date)
            else:
                LOGGER.info('Open ended trade %s, moving loan to %s.' 
                            % (trade.Oid(), next_business_day))
                leg.StartDate(next_business_day)
                leg.EndDate(next_business_day)
                ins_image.StartDate(next_business_day)
                trade_image.ValueDay(next_business_day)
                trade_image.AcquireDay(next_business_day)
        else:
            LOGGER.info('Ignoring future starting trade %s.' % trade.Oid())
            continue
        if PARAMS['dry_run']:
            continue
        acm.BeginTransaction()
        try:
            trade_image.Commit()
            ins_image.Commit()
            acm.CommitTransaction()
        except:
            acm.AbortTransaction()
            LOGGER.exception('Trade %s: Failed to update.' % trade.Oid())
            continue
        LOGGER.info('Trade %s: updated.' % trade.Oid())
        try:
            regenerate_cashflows(ins)
        except:
            LOGGER.exception('Trade %s: Failed to regenerate loan.' % trade.Oid())
        else:
            LOGGER.info('Trade %s: Loan regenerated.' % trade.Oid())
    

def get_fa_trades(base_query, end_date):
    query = acm.FStoredASQLQuery[base_query.Name()].Query()
    query.AddAttrNode('TradeTime', 'LESS_EQUAL', end_date)
    query.AddAttrNode('Instrument.StartDate', 'LESS_EQUAL', end_date)
    query.AddAttrNode('ValueDay', 'LESS_EQUAL', end_date)
    query.AddAttrNode('AdditionalInfo.SL_G1Counterparty1', 'NOT_EQUAL', '')
    query.AddAttrNode('AdditionalInfo.SL_G1Counterparty2', 'NOT_EQUAL', '')
    or_node = query.AddOpNode('OR')
    sub_and_node_1 = or_node.AddOpNode('AND')
    sub_and_node_1.AddAttrNode('Instrument.OpenEnd', 'EQUAL', 'Open End')
    sub_and_node_1.AddAttrNode('Instrument.ExpiryDate', 'GREATER_EQUAL', end_date)
    sub_and_node_2 = or_node.AddOpNode('AND')
    sub_and_node_2.AddAttrNode('Instrument.OpenEnd', 'EQUAL', 'Terminated')
    sub_and_node_2.AddAttrNode('Instrument.ExpiryDate', 'GREATER', end_date)
    return list(query.Select())


class TradeProcessor(object):
    
    def __init__(self, fa_id, rows):
        self._contract = acm.FTrade[fa_id]
        self._rows = rows
    
    @staticmethod
    def check_trade(fa_trade, loan_price, loan_quantity, loan_rate,
                    borrower, lender, taxable):
        fa_ins = fa_trade.Instrument()
        trade_image = fa_trade.StorageImage()
        ins_image = fa_ins.StorageImage()
        if (is_price_incorrect(fa_trade, loan_price) 
                or round(loan_quantity) != round(fa_trade.FaceValue())):
            quotation_factor = fa_ins.Quotation().QuotationFactor()
            LOGGER.info('Trade %s: Incorrect price (new: %s, old: %s) or quantity (new: %s, old: %s).' 
                        % (fa_trade.Oid(), loan_price / quotation_factor, fa_trade.AllInPrice(),
                           loan_quantity, fa_trade.FaceValue()))
            contract_size = fa_ins.ContractSize()
            trade_quantity = loan_price * loan_quantity / contract_size
            ref_val = contract_size / loan_price
            underlying = fa_ins.Underlying()
            ref_price = loan_price / quotation_factor
            if underlying.InsType() in ('Bond', 'IndexLinkedBond'):
                ref_price = underlying.Calculation().PriceConvert(
                    CALC_SPACE, ref_price, 'Pct of Nominal', underlying.Quotation(), 
                    fa_ins.StartDate())
            trade_image.Quantity(trade_quantity)
            ins_image.RefValue(ref_val)
            ins_image.RefPrice(ref_price)
        if round(fa_ins.Legs()[0].FixedRate(), 6) != round(loan_rate, 6):
            LOGGER.info('Trade %s: Incorrect rate (new: %s, old: %s).'
                        % (fa_trade.Oid(), loan_rate, fa_ins.Legs()[0].FixedRate()))
            leg = ins_image.Legs()[0]
            leg.FixedRate(loan_rate)
        if fa_ins.OpenEnd() == 'Open End' and fa_ins.Legs()[0].EndDate() < TODAY:
            LOGGER.info('Trade %s: Incorrect Open End end date (new: %s, old: %s).'
                        % (fa_trade.Oid(), TODAY, fa_ins.Legs()[0].EndDate()))
            leg = ins_image.Legs()[0]
            leg.EndDate(TODAY)
        if fa_ins.OpenEnd() == 'Terminated' and fa_ins.Legs()[0].EndDate() <= TODAY:
            LOGGER.info('Trade %s: Incorrect Terminated end date (new: %s, old: %s).'
                        % (fa_trade.Oid(), NEXT_BUSINESS_DAY, fa_ins.Legs()[0].EndDate()))
            leg = ins_image.Legs()[0]
            leg.EndDate(NEXT_BUSINESS_DAY)
        if PARAMS['check_cp'] and fa_trade.AdditionalInfo().SL_G1Counterparty1() != borrower:
            LOGGER.info('Trade %s: Incorrect borrower (new: %s, old: %s).'
                        % (fa_trade.Oid(), borrower, fa_trade.AdditionalInfo().SL_G1Counterparty1()))
            trade_image.AdditionalInfo().SL_G1Counterparty1(borrower)
        if PARAMS['check_cp'] and fa_trade.AdditionalInfo().SL_G1Counterparty2() != lender:
            LOGGER.info('Trade %s: Incorrect lender (new: %s, old: %s).'
                        % (fa_trade.Oid(), lender, fa_trade.AdditionalInfo().SL_G1Counterparty2()))
            trade_image.AdditionalInfo().SL_G1Counterparty2(lender)
        if bool(fa_ins.AdditionalInfo().SL_VAT()) != taxable:
            LOGGER.info('Trade %s: Incorrect VAT (new: %s, old: %s).'
                        % (fa_trade.Oid(), taxable, fa_ins.AdditionalInfo().SL_VAT()))
            ins_image.AdditionalInfo().SL_VAT(taxable)
        
        if PARAMS['dry_run']:
            return
        if not trade_image.IsModified() and not ins_image.IsModified():
            LOGGER.info('Trade %s: No update neccessary.' % fa_trade.Oid())
            return
        acm.BeginTransaction()
        try:
            trade_image.Commit()
            ins_image.Commit()
            acm.CommitTransaction()
        except:
            acm.AbortTransaction()
            LOGGER.exception('Trade %s: Failed to update.' % fa_trade.Oid())
            raise
        LOGGER.info('Trade %s: Updated successfully.' % fa_trade.Oid())
        
        try:
            regenerate_cashflows(fa_ins)
        except:
            LOGGER.exception('Trade %s: Failed to regenerate loan.' % fa_trade.Oid())
            raise
        LOGGER.info('Trade %s: Loan regenerated.' % fa_trade.Oid())
    
    def _get_party_name(self, party_type):
        rows = [row for row in self._rows if row['Len/Bor'] == party_type]
        if len(rows) != 1:
            raise RuntimeError('Contract %s: %s %s rows found.' 
                               % (self._contract.Oid(), len(rows), party_type))
        party_code = rows[0]['Cpty Code']
        party = get_party(party_code)
        return party.Name()
    
    def _get_client_row(self):
        for row in self._rows:
            if row['Cpty Code'] not in ACQUIRERS:
                return row
        return self._rows[0]
    
    def process(self):
        trade = get_last_trade(self._contract, TODAY)
        borrower = self._get_party_name('Borrower')
        lender = self._get_party_name('Lender')
        client_row = self._get_client_row()
        loan_quantity = copysign(client_row['Loan Quantity'], self._contract.FaceValue())
        if trade.Status() not in VALID_SBL_STATUS:
            LOGGER.warning('Trade %s: Incorrect status %s.' % (trade.Oid(), trade.Status()))
            if PARAMS['dry_run']:
                return None
            start_date = client_row['Security Settlement Date'].split('/')
            start_date.reverse()
            start_date = acm.Time.DateFromYMD(*start_date)
            trade = create_new_loan(self._contract, loan_quantity, start_date, NEXT_BUSINESS_DAY, 'Open End')
            LOGGER.info('Contract %s: Created new trade %s.' % (self._contract.Oid(), trade.Oid()))
        if client_row['Loan Price'] != client_row['Market Price']:
            loan_price = client_row['Loan Price']
        elif 'Initial Loan Quantity' in client_row:
            LOGGER.info('Trade %s: Using Loan Price based on Initial Loan Value and Quantity.' % trade.Oid())
            loan_price = client_row['Initial Loan Value'] / client_row['Initial Loan Quantity']
        else:
            LOGGER.info('Trade %s: Using Loan Price based on Initial Loan Value.' % trade.Oid())
            loan_price = client_row['Initial Loan Value'] / abs(self._contract.FaceValue())
        if client_row['Taxable Trade'] == 'Y':
            loan_rate = client_row['Rate Excl Vat'] * VAT_RATE
            taxable = True
        else:
            loan_rate = client_row['Rate Excl Vat']
            taxable = False
        self.check_trade(trade, loan_price, loan_quantity, loan_rate,
                         borrower, lender, taxable)
        return trade
        
        
def ael_main(ael_params):
    LOGGER.msg_tracker.reset()
    file_path = str(ael_params['input_file_path'])
    LOGGER.info('Reading input data from %s.' % file_path)
    PARAMS['dry_run'] = ael_params['dry_run']
    LOGGER.info('Dry run: %s.' % PARAMS['dry_run'])
    PARAMS['check_cp'] = ael_params['check_cp']
    LOGGER.info('Check Lender/Borrower: %s.' % PARAMS['check_cp'])
    base_query = ael_params['base_query']
    g1_trades = defaultdict(list)
    with open(file_path, 'rb') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            try:
                if row['Link Reference'][0] == '0':
                    fa_id = int(row['Link Reference'], 16)
                else:
                    fa_id = int(row['Link Reference'])
                row['Loan Quantity'] = float(row['Loan Quantity'])
                row['Rate Incl Vat'] = float(row['Rate Incl Vat'])
                row['Rate Excl Vat'] = float(row['Rate Excl Vat'])
                row['Loan Price'] = float(row['Loan Price'])
                row['Market Price'] = float(row['Market Price'])
                row['Initial Loan Value'] = float(row['Initial Loan Value'])
                if 'Initial Loan Quantity' in row:
                    row['Initial Loan Quantity'] = float(row['Initial Loan Quantity'])
                g1_trades[fa_id].append(row)
            except:
                LOGGER.info('Failed to process %s.' % row)
    matched_trades = []
    for fa_id, rows in g1_trades.items():
        trade_processor = TradeProcessor(fa_id, rows)
        try:
            fa_trade = trade_processor.process()
        except:
            LOGGER.exception('Contract %s: Failed to process %s.' % (fa_id, rows))
            continue
        if fa_trade:
            matched_trades.append(fa_trade)
    fa_trades = get_fa_trades(base_query, TODAY)
    extra_trades = list(set(fa_trades) - set(matched_trades))
    LOGGER.info('%s extra trades: %s' 
                % (len(extra_trades), ', '.join([str(trade.Oid()) for trade in extra_trades])))
    missing_trades = list(set(matched_trades) - set(fa_trades))
    LOGGER.info('%s missing trades: %s' 
                % (len(missing_trades), ', '.join([str(trade.Oid()) for trade in missing_trades])))
    if not LOGGER.msg_tracker.errors_counter:
        remove_extra_trades(extra_trades, TODAY)
    
    if LOGGER.msg_tracker.errors_counter:
        raise RuntimeError('ERRORS occurred. Please check the log.')
    LOGGER.info('Completed successfully.')

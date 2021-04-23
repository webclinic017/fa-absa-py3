"""----------------------------------------------------------------------------------------------------------
MODULE                  :       InternalCrtBridgeReport
PURPOSE                 :       Creates a report of bridge trades for selected
                                portfolios / trade filter
DEPARTMENT AND DESK     :       Trading Structured Trading & CRT 3
REQUESTER               :       Declercq Wentzel
DEVELOPER               :       Nada Jasikova
CR NUMBER               :       2493464
-------------------------------------------------------------------------------------------------------------

"""


import os
from collections import defaultdict

import acm
import at_time
import at_progress
from at_ael_variables import AelVariableHandler
from at_report import CSVReportCreator

ael_gui_parameters = {'windowCaption': 'Internal CRT bridge trades',
                      'runButtonLabel': '&&Create report',
                      'closeWhenFinished': False}

ael_variables = AelVariableHandler()
ael_variables.add('date_from',
                  label='Date from',
                  default='0d')
ael_variables.add('date_to',
                  label='Date to',
                  mandatory=False,
                  default='0d')
ael_variables.add('prf_ids',
                  label='Portfolio',
                  multiple=True,
                  mandatory=False,
                  collection=acm.FPhysicalPortfolio.Select(''),
                  cls='FPhysicalPortfolio',
                  default=acm.FPhysicalPortfolio['Swap Flow'])
ael_variables.add('tf_ids',
                  label='Trade filter',
                  multiple=False,
                  mandatory=False,
                  collection=acm.FTradeSelection.Select(''),
                  cls='FTradeSelection',)
ael_variables.add_directory('output_path',
                            label='Output folder',
                            default='c:/temp')
ael_variables.add('file_name',
                  label='File name',
                  default='InternalCrtBridgeReport')


def log(message):
    print('{0}: {1}'.format(acm.Time.TimeNow(), message))


def _get_trades(date_from, date_to, prfs, trade_filter):
    """Retrieve a list of trades in the portfolios
    created within the time interval or according
    to the trade filter"""
    trades = []
    if prfs:
        trades = _get_trades_in_portfolios(prfs, date_from, date_to)

    if trade_filter:
        log("getting trades from trade filter")
        trades = trade_filter.Trades()

    return filter(lambda trade: trade.TrxTrade(), trades)


def _get_trades_in_portfolios(prfs, date_from, date_to):
    query = acm.CreateFASQLQuery('FTrade', 'AND')

    orNode = query.AddOpNode('OR')
    for prf in prfs:
        orNode.AddAttrNode('Portfolio.Oid', 'EQUAL', prf.Oid())

    query.AddAttrNode('CreateTime', 'GREATER_EQUAL',
                      at_time.acm_date(date_from))
    query.AddAttrNode('CreateTime', 'LESS_EQUAL',
                      at_time.acm_date(date_to))
    query.AddAttrNode('Status', 'NOT_EQUAL', 'Simulated')
    query.AddAttrNode('Status', 'NOT_EQUAL', 'Void')

    get_duration = at_progress.start_stopwatch()
    trades = query.Select()

    duration = get_duration()
    message = "Retrieved {0} trades in {1} seconds"
    log(message.format(len(trades), duration))

    return trades


def _get_mirrored_trades(trades):
    """Only returns the trades from the original list
    that have a mirror trade"""

    if not trades:
        return None

    get_duration = at_progress.start_stopwatch()

    mirrored_trades = []
    for trade in trades:
        mirror_trade = trade.GetMirrorTrade()
        if not mirror_trade:
#             message = 'Trade {0} does not have a mirror trade!'
#             log(message.format(trade.Oid()))
            continue
        mirrored_trades.append(trade)

    duration = get_duration()
    message = "Retrieved {0} mirror trades in {1} seconds"
    log(message.format(len(mirrored_trades), duration))
    return mirrored_trades


class IntCrtBridgeReportCreator(CSVReportCreator):
    def __init__(self, file_name, file_suffix, file_path, trades):
        super(IntCrtBridgeReportCreator,
              self).__init__(file_name, file_suffix, file_path)
        self._trades = trades
        self._fee_types = ['CVA',
                           'FVA',
                           'RWA',
                           'Termination_fee',
                           'Cash',
                           'Premium']
        self._initiate_columns()

    def _collect_data(self):
        if self._trades:
            self.content = [self._get_trade_row(trade)
                            for trade in self._trades]

    def _initiate_columns(self):
        self.columns = []
        self.columns += ['Portfolio',
                         'Trade number',
                         'Instrument type',
                         'Maturity date']
        for fee_type in self._fee_types:
            self.columns += ['{0} amount'.format(fee_type)]
        self.columns += ['Acquirer',
                         'Counterparty',
                         'Underlying trade',
                         'Underlying trade counterparty',
                         'SDSID',
                         'Pay date',
                         'Valid from',
                         'Trade date',
                         'Status']

    def _get_trade_row(self, trade):
        row = []
        prf_name = None
        if trade.Portfolio():
            prf_name = trade.Portfolio().Name()
        row += [prf_name,                        # Portfolio
                trade.Oid(),                     # Trade number
                trade.Instrument().InsType(),    # Instrument type
                trade.Instrument().ExpiryDateOnly()]  # Maturity date
        condition = (lambda p: p.Type() == 'Internal Fee'
                     and p.Text() in self._fee_types)
        payments = filter(condition, trade.Payments())
        payment_totals = self._get_payment_totals(payments)
        payment_valid_date = None
        payment_pay_date = None
        if payments:
            payment_valid_date = acm.Time().DateFromTime(payments[0]
                                                         .ValidFrom())
            payment_pay_date = acm.Time().DateFromTime(payments[0]
                                                       .PayDay())
        # internal payment amounts by fee type
        for fee_type in self._fee_types:
            row.append(payment_totals[fee_type])
        cpty_name = None
        if trade.Counterparty():
            cpty_name = trade.Counterparty().Name()
        acquirer_name = None
        if trade.Acquirer():
            acquirer_name = trade.Acquirer().Name()
        underlying_trade = trade.TrxTrade()
        sdsid = None
        und_counterparty_name = None
        if underlying_trade.Counterparty():
            sdsid = (underlying_trade.Counterparty().AdditionalInfo()
                     .BarCap_SMS_CP_SDSID())
            und_counterparty_name = (underlying_trade
                                     .Counterparty().Name())
        row += [acquirer_name,                  # Acquirer
                cpty_name,                      # Counterparty
                underlying_trade.Oid(),         # Underlying trade
                und_counterparty_name,          # Underlying cpty
                sdsid,                          # SDSID
                payment_pay_date,               # Pay day
                payment_valid_date,             # Valid from
                acm.Time().DateFromTime(trade.TradeTime()),  # Trade time
                trade.Status()]                 # Status
        return row

    def _get_payment_totals(self, payments):
        payment_totals = defaultdict(int)

        for payment in payments:
            fee_type = payment.Text()
            payment_totals[fee_type] += payment.Amount()
            message = 'Trade {0}: Processing payment {1}, type {2}, amount {3}'
            log(message.format(payment.Trade().Oid(), payment.Oid(),
                               payment.Text(), payment.Amount()))

        return payment_totals

    def _header(self):
        return self.columns


def ael_main(params):
    date_from, date_to = params['date_from'], params['date_to']
    prf_ids, trade_filter = params['prf_ids'], params['tf_ids']
    file_path = str(params['output_path'].SelectedDirectory())
    file_name = params['file_name']
    file_suffix = 'csv'

    if trade_filter and prf_ids:
        message = 'Please select either trade filter or portfolio(s)'
        log(message)
        return

    all_trades = _get_trades(date_from, date_to, prf_ids, trade_filter)
    trades = _get_mirrored_trades(all_trades)

    report_creator = IntCrtBridgeReportCreator(file_name, file_suffix,
                                               file_path, trades)

    log('Generating the report')
    report_creator.create_report()
    message = 'Wrote secondary output to {0}'
    full_path = os.path.join(file_path, file_name + '.' + file_suffix)
    log(message.format(full_path))
    log('Completed successfully')

"""
Implementation of the Penguin feed script.

Extracts data from front to compare with Penguin

Project                  : CCM Application - SND Penguin
Department and Desk      : SND
Requester                : Ramphal, Kavish
Developer                : Nico Louw
CR Number                :

HISTORY
==============================================================================
Date        CR number       Developer       Description
------------------------------------------------------------------------------
16-03-2016  CHNG0003521556  Nico Louw       Added InsType and Counterparty
                                            type to the Feed.

------------------------------------------------------------------------------
"""
import csv
import ael
import acm

# =========================== Script functions ===============================


def write_file(name, data, access='wb'):
    """ Write data to file

    Arguments:
        name - the name of the file.
        data - the data to write to file.

    """
    file_obj = open(name, access)
    csv_writer = csv.writer(file_obj, dialect='excel')
    csv_writer.writerows(data)
    file_obj.close()


def calc_proj_cfs(trade, start_date):
    """ Calculate the sum of future cashflows for this trade from start_date.

    Arguments:
        trade - acm trade object.
        start_date - date from which the future cashflows are calculated.
    """
    proj_cfs = 0.0
    # If the trade is a combination trade, calculate the future cashflows using
    #   the method defined for combination trades
    if trade.Instrument().InsType() == 'Combination':
        proj_cfs = calc_proj_combination(trade, start_date)
    else:
        for leg in trade.Instrument().Legs():
            for cash_flow in leg.CashFlows():
                # Need to use ael cash flow to use the AEL projected_cf method
                ael_cf = ael.CashFlow[cash_flow.Oid()]
                value = ael_cf.projected_cf(start_date, ael_cf.pay_day)
                proj_cfs += value*trade.Quantity()
    return proj_cfs


def calc_proj_combination(trade, start_date):
    """ Calculate the sum of future cashflows for each instrument within the
        combination instument for this trade from start_date.

    Arguments:
        trade - acm trade object.
        start_date - date from which the future cashflows are calculated.
    """
    proj_cfs = 0.0
    comb_ins = acm.FCombination[trade.Instrument().Name()]
    for ins in comb_ins.Instruments():
        for leg in ins.Legs():
            for cash_flow in leg.CashFlows():
                # Need to use ael cash flow to use the AEL projected_cf method
                ael_cf = ael.CashFlow[cash_flow.Oid()]
                value = ael_cf.projected_cf(start_date, ael_cf.pay_day)
                proj_cfs += value*trade.Quantity()*comb_ins.GroupWeight(
                    ins, start_date)
    return proj_cfs


def calc_value(trade, column_id):
    """ Calculate column value.

    Arguments:
        trade - acm trade object.
        column_id - column value to calculate.
    """
    try:
        context = acm.GetDefaultContext()
        sheet_type = 'FTradeSheet'
        calc_space = acm.Calculations().CreateCalculationSpace(
            context, sheet_type
        )
        calc = calc_space.CreateCalculation(trade, column_id)
        value = calc.FormattedValue()
        if value != '':
            return float(value.translate(None, ','))

        print('Empty value for trade: %s in column: %s, using 0.0' % (
            str(trade.Oid()), column_id))
        return 0.0
    except Exception, e:
        print('Error occured: %s, returning 0.0' % e.__repr__())
        return 0.0


def switch_curr(trade, date, amount):
    """Function which returns amount in other currency.

    Arguments:
        trade - acm trade object.
        date - date used to get the fx_rate.
        amount - the amount to convert.
        curr - the currency to convert to.
    """
    try:
        # Get the fx_rate to ZAR
        fx_rate = trade.Currency().UsedPrice(date, 'ZAR', 'SPOT')
        return amount*fx_rate
    except ZeroDivisionError:
        msg = 'ZeroDivisionError, not possible to convert Amount into'\
            ' correct currency. Will continue without converting. '\
            'Fx rate:%f' % fx_rate
        print(msg)
        return amount


def get_eca_nbr(trade):
    """ Get Addinfo field ECA_Nbr

    Arguments:
        trade - acm trade object.
    """
    spec = acm.FAdditionalInfoSpec['ECA Number']
    add_info = acm.FAdditionalInfo.Select01(
        'recaddr = ' + str(trade.Oid()) + ' and addInf = ' + str(
            spec.Oid()), '')
    if add_info:
        return add_info.FieldValue()

    return ''

# ============================ Class Definition ==============================


class PenguinFeed(object):
    """ Penguin feed class
    """
    def __init__(self, data):
        self.portfolios = data['portfolios']
        self.exlc_status = list(data['excl_status'])
        self.outpath = data['Outpath']
        self.start_date = ael.date_today()
        self.feed_name = '%s%s' % (self.outpath, 'Penguin_Feed.csv')
        self.headers = []
        self.output = []
        self._headers()

    def _headers(self):
        """ Populate headers for feed output
        """
        self.headers.append([
            'Trd Nbr', 'Transref', 'InsType', 'Trade Time', 'Acquire Day', 
            'Expiry', 'Portfolio', 'Counterparty', 'Counterparty Type', 
            'ECA Nbr', 'Status', 'Proj CF', 'PV', 'Nom', 'Nom Change', 
            'Val End', 'Cash End', 'Accrued', 'Interest', 'TPL'
            ])

# ============================== Main ========================================
# AEL Variables :
# Variable Name, Display Name, Type, Candidate Values, Default, Mandatory,
# Multiple, Description, Input Hook, Enabled

ael_variables = []
ael_variables.append(['Outpath', 'Output Path: ', 'string', None, 'F:\\\\', 1])
ael_variables.append([
    'portfolios', 'Portfolios: ', 'FCompoundPortfolio',
    acm.FCompoundPortfolio.Instances(), None, 1, 1, 'Portfolio parameter',
    None, 1
    ])
ael_variables.append([
    'excl_status', 'Excluded Status: ', 'string',
    None, None, 1, 1, 'Enter status to be excluded (Comma separated)',
    None, 1
    ])


def ael_main(data):
    """ Main execution point of the penguin feed
    """
    feed = PenguinFeed(data)
    print('Starting penguin feed')

    for prf in feed.portfolios:
        print('Extracting trades from %s' % prf.Name())
        for trade in prf.Trades():
            if trade.Status() not in feed.exlc_status:
                # Get column info
                try:
                    transref = trade.TrxTrade().Oid()
                    print('Trdnbr: %s\tTransref: %s' % (trade.Oid(), transref))
                except AttributeError:
                    print('Trade %s has no TransRef' % str(trade.Oid()))
                    transref = 'NONE'

                # Get ECA_nbr additional Info
                eca_nbr = get_eca_nbr(trade)
                # Calculate projected future cash flows
                proj_cfs = calc_proj_cfs(trade, feed.start_date)
                # Convert currency to ZAR for pv, nom, nom_change,
                # val_end, cash_end, accrued, interest and tpl
                pv = switch_curr(
                    trade, feed.start_date,
                    calc_value(trade, 'Portfolio Present Value'))
                nom = switch_curr(
                    trade, feed.start_date,
                    calc_value(trade, 'Trade Nominal'))
                nom_change = switch_curr(
                    trade, feed.start_date,
                    calc_value(trade, 'Portfolio Profit Loss Period Position'))
                val_end = switch_curr(
                    trade, feed.start_date,
                    calc_value(trade, 'Portfolio Value End'))
                cash_end = switch_curr(
                    trade, feed.start_date,
                    calc_value(trade, 'Portfolio Cash End'))
                accrued = switch_curr(
                    trade, feed.start_date,
                    calc_value(trade, 'Portfolio Accrued Interest'))
                interest = switch_curr(
                    trade, feed.start_date,
                    calc_value(trade, 'Portfolio Interest'))
                tpl = switch_curr(
                    trade, feed.start_date,
                    calc_value(trade, 'Portfolio Total Profit and Loss'))

                feed.output.append([
                    trade.Oid(), transref, trade.Instrument().InsType(),
                    trade.TradeTime(), trade.AcquireDay(), 
                    trade.Instrument().ExpiryDate(), trade.PortfolioId(), 
                    trade.CounterpartyId(), trade.Counterparty().Type(),
                    eca_nbr, trade.Status(), proj_cfs, pv, nom, nom_change,
                    val_end, cash_end, accrued, interest, tpl
                    ])

        print('Exctraction from %s complete' % prf.Name())

    feed.output = feed.headers + feed.output
    try:
        write_file(feed.feed_name, feed.output)
        print('Wrote secondary output to:', feed.feed_name)
    except IOError:
        print('Error writing file: ', feed.feed_name)

    print('Feed completed successfully.')

'''
Date                    : [2010-09-06],[24/11/2011],[08/12/2011]
Purpose                 : [To rewrite a generic CFD booker based on the few different variations of CFD booking scripts running currently],
                            [Updated to look at t.execution_time rather than t.time,include ETF trades as well,round price to 4 decimals],
                            [Redeploying backed out call - no changes were made]
Department and Desk     : [],[PCG],[PCG],[Prime Services]
Requester               : [],[Andrew Nobbs],[Andrew Nobbs],[Francois Henrion]
Developer               : [Rohan van der Walt],[Willie van der Bank],[Willie van der Bank],[Peter Fabian]
CR Number               : [],[838638],[852453],[C000000892151]
'''

from collections import defaultdict

import ael
import acm
import PS_new_fees
import FBDPGui
import FBDPString
from at_ael_variables import AelVariableHandler

GENERIC_CFD_TEMPLATE = 'ZAR/DEFAULT/CFD'
logme = FBDPString.logme #pylint: disable-msg=C0103

def _form_cfd_name(instrument_name, cfd_replace_slash):
    return instrument_name.replace('/', cfd_replace_slash) + '/CFD'

def prepare_ael_variables():
    portfolios = [str(p.Name()) for p in acm.FPhysicalPortfolio.Select('')]
    portfolios.sort()
    stocks = acm.FStock.Select('')
    parties = [str(p.Name()) for p in acm.FParty.Select('')]
    parties.sort()
    users = acm.FUser.Select('')

    params = AelVariableHandler()
    params.add('portfolio',
        label='Stock Portfolio',
        cls=acm.FPhysicalPortfolio,
        collection=portfolios,
        alt='Portfolio to check for stock trades'
    )
    params.add('CFDPortfolio',
        label='CFDPortfolio',
        cls=acm.FPhysicalPortfolio,
        collection=portfolios,
        alt='Output portfolio where CFD trades will be booked'
    )
    params.add('cparties',
        label='Counterparty',
        cls=acm.FParty,
        collection=parties,
        mandatory=False,
        multiple=True,
        alt='Only look for trades with these counterparties'
    )
    params.add('stocks',
        label='Stocks',
        cls=acm.FStock,
        collection=stocks,
        mandatory=False,
        multiple=True,
        alt='Look for trades on these Stocks only, if left blank will use' \
            ' all Stocks in portfolio'
    )
    params.add('date',
        label='Date',
        cls='date',
        mandatory=False,
        alt='Date to check for trades in selected portfolio'
    )
    params.add('tplus',
        label='Value/Acquire Day: T+?',
        cls='int',
        default=0,
        alt='Book CFD Trades with acquire/value day T+?'
    )
    params.add('acq',
        label='Acquirer',
        cls=acm.FParty,
        collection=parties,
        alt='Acquirer to use for created trade'
    )
    params.add('trader',
        label='Trader',
        cls=acm.FUser,
        collection=users,
        mandatory=False,
        alt='Trader to use for created trade'
    )
    params.add('CFDReplaceSlash',
        label='CFD name divider',
        cls='string',
        default='/',
        alt='How the slash in instrument name will be replaced into CFD name'
    )
    params.add_bool('calcPremium',
        label='Calculate Premium',
        default=False,
        alt='Calculate Premium or Set to zero on CFD trades'
    )
    params.add_bool('BOFO',
        label='BO Confirmed',
        default=False,
        alt='Status of created CFD Trades, Yes-BO Confirmed, No-FO Confirmed'
    )
    params.add_bool('CFDFee',
        label='Calculate CFD Fee',
        default=True,
        alt='Should CFD fee be calculated'
    )
    params.extend(FBDPGui.LogVariables())
    return params

ael_variables = prepare_ael_variables() #pylint: disable-msg=C0103
ael_gui_parameters = { #pylint: disable-msg=C0103
    'windowCaption':'CFD Booking Script'
}

def ael_main(ael_dict):
    logme.setLogmeVar(__name__,
          ael_dict['Logmode'],
          ael_dict['LogToConsole'],
          ael_dict['LogToFile'],
          ael_dict['Logfile'],
          ael_dict['SendReportByMail'],
          ael_dict['MailList'],
          ael_dict['ReportMessageType'])

    if not ael_dict['trader']:
        ael_dict['trader'] = acm.User()
    if not ael_dict['date']:
        ael_dict['date'] = acm.Time().DateToday()

    instruments = []
    if len(ael_dict['stocks']) == 0:
        for i in ael_dict['portfolio'].Instruments():
            if i.InsType() == 'Stock' or i.InsType() == 'ETF':
                instruments.append(i.Name())
    else:
        for i in ael_dict['stocks']:
            if i in ael_dict['portfolio'].Instruments():
                instruments.append(i.Name())

    for instrument_name in instruments:
        Create_CFD(
                ael.Instrument[instrument_name],
                ael_dict['portfolio'].Name(),
                ael_dict['date'],
                ael_dict['CFDReplaceSlash'],
                ael_dict['CFDPortfolio'].Name(),
                ael_dict['calcPremium'],
                ael_dict['cparties'],
                ael_dict['CFDFee'],
                ael_dict['BOFO'],
                ael_dict['tplus'],
                ael_dict['acq'],
                ael_dict['trader'])
    print('Output Complete')
    logme(None, 'FINISH')

def _filter_party(party, party_list):
    return party.ptyid in party_list if len(party_list) > 0 else True

def _account_fee(trade):
    return (trade.optkey4_chlnbr is None or
            trade.optkey4_chlnbr.entry not in ('ACS Takeon', 'ASB Closeout'))

def Create_CFD(ael_instrument, prfol, date, cfd_replace_slash, cfdPortfolio,
        calcPremium, validParties, CFDFee, bofo, tplus, acq, trader):
    CFD_id = _form_cfd_name(ael_instrument.insid, cfd_replace_slash)

    partylist = [p.Name() for p in validParties]
    if _get_cfd_instrument(CFD_id, acm.FInstrument[ael_instrument.insid]):
        if not _trades_already_processed(CFD_id, date, cfdPortfolio):
            dt = ael.date(date)
            prf = ael.Portfolio[prfol]
            trds = prf.trades()
            buy_sum = 0
            buy_price = 0
            sell_sum = 0
            sell_price = 0
            buy_fee = 0
            sell_fee = 0
            buy_list = []
            sell_list = []
            # Sum up payment amounts grouped by valid from and pay date
            buy_dividend_suppression = defaultdict(float)
            sell_dividend_suppression = defaultdict(float)
            for t in trds:
                if (t.insaddr == ael_instrument
                        and ael.date_from_time(t.execution_time) == dt
                        and t.status not in ('Simulated', 'Terminated', 'Void')
                        and _filter_party(t.counterparty_ptynbr, partylist)):

                    if t.quantity > 0:
                        buy_sum += t.quantity
                        buy_list.append(t.trdnbr)
                        buy_price += t.quantity * t.price
                        if CFDFee and _account_fee(t):
                            buy_fee +=  PS_new_fees.addFee(t)
                        for p in t.payments():
                            if p.type == "Dividend Suppression":
                                key = (p.valid_from, p.payday, p.curr, p.ptynbr)
                                buy_dividend_suppression[(key)] += p.amount
                                
                    else:
                        sell_sum += t.quantity
                        sell_list.append(t.trdnbr)
                        sell_price += t.quantity * t.price
                        if CFDFee and _account_fee(t):
                            sell_fee += PS_new_fees.addFee(t)
                        for p in t.payments():
                            if p.type == "Dividend Suppression":
                                key = (p.valid_from, p.payday, p.curr, p.ptynbr)
                                sell_dividend_suppression[(key)] += p.amount
            trd_buys, trd_sells = None, None
            if buy_sum > 0:
                bvwap = buy_price/buy_sum
                bpremium = abs(buy_price / 100) if calcPremium else 0
                trd_buys = CreateCFD(
                        CFD_id,
                        prf.prfid,
                        buy_sum,
                        bvwap,
                        buy_fee,
                        bpremium,
                        dt,
                        cfdPortfolio,
                        bofo,
                        tplus,
                        acq,
                        trader,
                        buy_dividend_suppression)
            if sell_sum < 0:
                svwap = sell_price/sell_sum
                spremium = abs(sell_price / 100) if calcPremium else 0
                trd_sells = CreateCFD(
                        CFD_id,
                        prf.prfid,
                        sell_sum,
                        svwap,
                        sell_fee,
                        spremium,
                        dt,
                        cfdPortfolio,
                        bofo,
                        tplus,
                        acq,
                        trader,
                        sell_dividend_suppression)
            ael.poll()
            if buy_list or sell_list:
                logme('{0}: {1}/{2} CFD Trdnbrs: B:{3} S:{4}'.format(
                        ael_instrument.insid,
                        buy_list,
                        sell_list,
                        str(trd_buys),
                        str(trd_sells)), 'INFO')
        else:
            logme('{0}: CFDs have already been committed on this instrument'
                    ' and account for {1}'.format(ael_instrument.insid, date),
                    'INFO')
    else:
        logme('{0}: CFD instrument {1} does not exist'.format(
                ael_instrument.insid, CFD_id), 'INFO')

def _get_cfd_instrument(cfd_id, instrument):
    '''Return CFD instrument

    Create stock CFD from the template when it doesn't exist.
    For Index/ETF underlying log an error so TCU can fix that manually.
    '''
    cfd_ins = acm.FInstrument[cfd_id]
    if cfd_ins:
        return cfd_ins
    else:
        if instrument.InsType() == 'Stock':
            logme("Instrument %s doesn't currently exist, process will" \
                    " attempt to create it from template" % cfd_id, 'WARNING')
            dummy = acm.FInstrument[GENERIC_CFD_TEMPLATE]
            if not dummy:
                logme('Template CFD named %s not found' % \
                        GENERIC_CFD_TEMPLATE, 'ERROR')
                return None
            new_cfd = dummy.Clone()
            new_cfd.Name(cfd_id)
            new_cfd.Underlying(instrument)
            new_cfd.Generic(False)
            try:
                new_cfd.Commit()
                logme('%s created from template successfully' % cfd_id, 'INFO')
                return new_cfd
            except RuntimeError as exc:
                logme('Instrument %s was not committed: %s' % (cfd_id, exc),
                        'ERROR')
                return None
        else:
            logme("CFD instrument %s doesn't currently exist and original" \
                    "instrument %s is %s so we are unable to" \
                    " create it automatically." % \
                    (cfd_id, instrument.Name(), instrument.InsType()), 'ERROR')

def _trades_already_processed(cfd_instrument, date, cfd_portfolio):
    '''Check if there are trades for instrument and date in the portfolio'''
    trades = ael.Instrument[cfd_instrument].trades()
    time = ael.date(date).to_time()
    portfolio = ael.Portfolio[cfd_portfolio]
    return any(t.time == time and t.prfnbr == portfolio
        and t.status not in ('Void', 'Simulated')
        for t in trades)

def CreateCFD(CFD_id, prfid, qty, vwap, fee, premium, cfddate, cfdPortfolio,
        bofo, tplus, acq, trader, dividend_suppression):
    i = ael.Instrument[CFD_id]
    t_new = ael.Trade.new(i)

    t_new.price = round(vwap, 4)
    t_new.text1 = 'Fee Received ' + str(fee)
    t_new.fee = fee

    if qty > 0:
        t_new.premium = (premium)
    elif qty < 0:
        t_new.premium = (premium) * -1
    else:
        logme('Net quantity on stocks is zero', 'INFO')

    t_new.quantity = qty * -1
    if bofo:
        t_new.status = 'BO Confirmed'
    else:
        t_new.status = 'FO Confirmed'
    port = ael.Portfolio[cfdPortfolio]
    t_new.prfnbr = port
    t_new.acquirer_ptynbr = ael.Party[acq.Name()]
    t_new.trader_usrnbr = ael.User[trader.Name()]

    prf = ael.Portfolio[prfid]
    t_new.counterparty_ptynbr = ael.Party[prf.add_info('CFD Counterparty')]
    t_new.broker_ptynbr = ael.Party[prf.add_info('CFD Broker')]

    ccy = ael.Instrument['ZAR']
    t_new.time = cfddate.add_banking_day(ccy, 0).to_time()

    t_new.value_day = cfddate.add_banking_day(ccy, tplus)
    t_new.acquire_day = cfddate.add_banking_day(ccy, tplus)

    t_new.curr = i.curr
    user = ael.userid()
    t_new.trader_usrnbr = ael.User[user]

    try:
        t_new.commit()
        if dividend_suppression:
            for key in dividend_suppression:
                (valid_from, payday, curr, ptynbr) = key
                payment = ael.Payment.new(t_new)
                payment.type = "Dividend Suppression"
                payment.valid_from = valid_from
                payment.payday = payday
                payment.curr = curr
                payment.ptynbr = ptynbr
                payment.amount = -1 * dividend_suppression[key]
                payment.commit()
        return t_new.trdnbr
    except RuntimeError as exc:
        logme('Error committing trade: %s' % exc, 'ERROR')
        return 0

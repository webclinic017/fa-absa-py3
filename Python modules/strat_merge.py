import acm
import at_choice
import at
from PS_FundingSweeper import TradingManagerSweeper

from strat_collapse_config_1strat import *

def get_sob_price(insid):
    """
        Returns today SPOT_SOB price for the specified instrument
    """
    today = acm.Time.DateToday()
    ins = acm.FInstrument[insid]
    calendar = acm.FCalendar['ZAR Johannesburg']
    prevBusDay = calendar.AdjustBankingDays(today, -1)
    for price in ins.Prices():
        if price.Market().Name() == 'SPOT' and price.Day() == prevBusDay:
            return price.Settle()
    for price in ins.HistoricalPrices():
        if price.Market().Name() == 'SPOT' and price.Day() == prevBusDay:
            return price.Settle()
    


def book_trade(insid, src_prf, dest_prf, pos, trdsId):
    """
        Books two trades, one with -pos qty to book src_prf
        and one with quantity pos to dest_prf.
        Both trades are identified by trdsId in Text1 field
    """
    ps_no_fees = at_choice.get('TradeKey3', 'PS No Fees')
    ins = acm.FInstrument[insid]
    curr = ins.Currency()
    today = acm.Time.DateToday()
    user = acm.User()
    price = get_sob_price(insid)

    trd1 = acm.FTrade()
    trd1.Instrument(ins)
    trd1.Currency(curr)
    trd1.Portfolio(src_prf)
    trd1.Quantity(-pos)
    trd1.Counterparty(acm.FParty['JSE'])
    trd1.Acquirer(acm.FParty['PRIME SERVICES DESK'])
    trd1.OptKey3(ps_no_fees)
    trd1.TradeTime(today)
    trd1.ValueDay(today)
    trd1.Trader(user)
    trd1.AcquireDay(today)
    trd1.Price(price)
    trd1.Premium(pos * price / 100)
    trd1.Status('FO Confirmed')
    trd1.Text1(trdsId)
    trd1.Commit()
    at.addInfo.save_or_delete(trd1, 'Broker_Fee_Exclude', 'Yes')
    # not sure if I can set add info for a trade before I commit, so I need to remove brokerage
    for p in trd1.Payments():
        p.Delete()
    
    print("Booked trade %s for ins %s to net position of %s in portfolio %s" % (trd1.Oid(), insid, pos, src_prf.Name()))
    
    trd2 = acm.FTrade()
    trd2.Instrument(ins)
    trd2.Currency(curr)
    trd2.Portfolio(dest_prf)
    trd2.Quantity(pos)
    trd2.Counterparty(acm.FParty['JSE'])
    trd2.Acquirer(acm.FParty['PRIME SERVICES DESK'])
    trd2.OptKey3(ps_no_fees)
    trd2.TradeTime(today)
    trd2.ValueDay(today)
    trd2.Trader(user)
    trd2.AcquireDay(today)
    trd2.Price(price)
    trd2.Premium(-1 * pos * price / 100)
    trd2.Status('FO Confirmed')
    trd2.Text1(trdsId)
    trd2.Commit()
    at.addInfo.save_or_delete(trd2, 'Broker_Fee_Exclude', 'Yes')
    for p in trd2.Payments():
        p.Delete()
    
    print("Booked trade %s for ins %s to transfer position of %s to portfolio %s" % (trd2.Oid(), insid, pos, dest_prf.Name()))
    

def move_positions(src_portfolios, dest_portfolio, trdsId):
    """
        Moves positions from books src_portfolios to book dest_portfolio
        identifying them (to support later rollback) with trdsId
    """
    for prf in src_portfolios:
        positions = TradingManagerSweeper(prf, acm.Time.DateToday(), ['Portfolio Position'])
        for insid, pos in positions.iteritems():
            pos = pos[0]
            # only move non zero positions and ignore PROFIT_REMIT swaps 
            if pos and 'PROFIT' not in insid:
                try:
                    book_trade(insid, prf, dest_portfolio, pos, trdsId)
                except Exception as e:
                    print("ERROR: Failed to book trades for %s: %s" % (insid, e))


def perform_move(trdsId):
    for merge_conf in [ nit_tr_safex, nit_tr_ff_CE, nit_tr_fin_CE, nit_tr_cfds, 
                        m501_safex, m501_ff_CE, m501_fin_CE, m501_cfds ]:
        dest_prf = acm.FPhysicalPortfolio[merge_conf.merge_prf_name]
        src_prfs = [acm.FPhysicalPortfolio[prf_id] for prf_id in merge_conf.prfs_to_merge]
        print("Merging to portfolio %s from %s" % (merge_conf.merge_prf_name, merge_conf.prfs_to_merge))
        move_positions(src_prfs, dest_prf, trdsId)

# Variable name, Display name, Type, Candidate values, Default, Mandatory, Multiple, Description, InputHook, Enabled 
ael_variables = [['tradesIdentification', 'Trade Identification String', 'string', None, None, 1, 0, 'This string will be used to identify the trades if a rollback would be needed.', None, 1],
                 ]

def ael_main(params):    
    perform_move(str(params['tradesIdentification']))
    print("Finished")
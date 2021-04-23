from collections import defaultdict
import acm
import at_choice
import at_addInfo
from at_ael_variables import AelVariableHandler


# Stock portfolios
NITROGEN_PORTFOLIOS = [
    '48694',                # NITROSKYL
    '48413',                # NITROFIRE
    '48389',                # SAASPCV
    '60137_EqPairs_LT',     # NITRO_TRUST
    '60129_EqPairs_LT'      # MAP_501
]


def get_default_quantity_trades(date, portfolio, instrument=None):
    """Return all default quantity trades (for a given portfolio and date).
    
    Instrument name can be specified for testing purposes to limit the
    filtering only for one instrument.
    
    """
    query = acm.CreateFASQLQuery('FTrade', 'AND')
    query.AddAttrNode('Status', 'EQUAL', acm.EnumFromString('TradeStatus', 'BO Confirmed'))
    query.AddAttrNode('TradeTime', 'GREATER_EQUAL', date)
    query.AddAttrNode('TradeTime', 'LESS_EQUAL', date)
    query.AddAttrNode('Portfolio.Name', 'EQUAL', portfolio)
    query.AddAttrNode('Text1', 'EQUAL', 'Allocation Process')
    
    if instrument:
        query.AddAttrNode('Instrument.Name', 'EQUAL', instrument)

    return query.Select()


def get_all_quantity_trades(date, portfolio, instrument=None):
    """Return all quantity trades (for a given portfolio and date).
    
    Instrument name can be specified for testing purposes to limit the
    filtering only for one instrument.
    
    """
    query = acm.CreateFASQLQuery('FTrade', 'AND')
    query.AddAttrNode('Status', 'EQUAL', acm.EnumFromString('TradeStatus', 'BO Confirmed'))
    query.AddAttrNode('TradeTime', 'GREATER_EQUAL', date)
    query.AddAttrNode('TradeTime', 'LESS_EQUAL', date)
    query.AddAttrNode('Portfolio.Name', 'EQUAL', portfolio)
    
    if instrument:
        query.AddAttrNode('Instrument.Name', 'EQUAL', instrument)

    return query.Select()
    
    
def get_aggregated_trades(date, portfolios, instrument=None):
    """Return all aggregated trades (for a given portfolio and date).
    
    Instrument name can be specified for testing purposes to limit the
    filtering only for one instrument.
    
    """ 
    query = acm.CreateFASQLQuery('FTrade', 'AND')
    query.AddAttrNode('Status', 'EQUAL', acm.EnumFromString('TradeStatus', 'VOID'))
    query.AddAttrNode('TradeTime', 'GREATER_EQUAL', date)
    query.AddAttrNode('TradeTime', 'LESS_EQUAL', date)
    query.AddAttrNode('Trader.Name', 'EQUAL', 'EFGUSER')
    query.AddAttrNode('CreateUser.Name', 'NOT_EQUAL', 'AMBA')
    query.AddAttrNode('Text1', 'EQUAL', 'Allocation Process')

    orNode = query.AddOpNode('OR')
    for portf in portfolios:
        orNode.AddAttrNode('Portfolio.Name', 'EQUAL', portf)

    if instrument:
        query.AddAttrNode('Instrument.Name', 'EQUAL', instrument)

    return query.Select()

    
def get_correct_positive_trade(trades):
    """Return trade with correct positive quantity from the set of trades."""
    # Split trades based on quantity
    positive_trades = [t for t in trades if t.Quantity() > 0.0]
    negative_trades = [t for t in trades if t.Quantity() <= 0.0]
    
    # Find the trade with correct positive quantity
    for trade in positive_trades:
        # Find pairs with opposite quantity
        pairs = [t for t in negative_trades if abs(t.Quantity()) == trade.Quantity()]
        if pairs:
            # Create list of candidate trades (sorted by create time)
            candidates = pairs + [trade]
            candidates = sorted(candidates, key=lambda x: x.CreateTime())
    
            # Candidate trades is the one with newest create time
            candidate = candidates[-1]
            rest = candidates[:-1]
            
            # Remove original trade
            if (candidate == trade or trade.Text1() == 'Allocation Process'):
                rest.append(candidate)
            
            # Remove all matched pairs
            for tr in rest:
                trades.remove(tr)
                
            # Look for another set of pairs
            return get_correct_positive_trade(trades)
        else:
            # Trade without a pair is the one with the correct quantity
            return trade

    # No trades with negative quantity found
    return None
        
        
def get_correct_negative_trade(trades):
    """Return trade with correct negative quantity from the set of trades."""
    # Split trades based on quantity
    positive_trades = [t for t in trades if t.Quantity() > 0.0]
    negative_trades = [t for t in trades if t.Quantity() <= 0.0]
    
    # Find the trade with correct negative quantity
    for trade in negative_trades:    
        # Find pairs with opposite quantity
        pairs = [t for t in positive_trades if t.Quantity() == -trade.Quantity()]
        if pairs:
            # Create list of candidate trades (sorted by create time)
            candidates = pairs + [trade]
            candidates = sorted(candidates, key=lambda x: x.CreateTime())
            
            # Candidate trades is the one with newest create time
            candidate = candidates[-1]
            rest = candidates[:-1]
            
            # Remove original trade
            if (candidate == trade or trade.Text1() == 'Allocation Process'):
                rest.append(candidate)
            
            # Remove all matched pairs
            for tr in rest:
                trades.remove(tr)
                
            # Look for another set of pairs
            return get_correct_negative_trade(trades)
        else:
            # Trade without a pair is the one with the correct quantity
            return trade

    # No trades with negative quantity found
    return None
    
   
def get_instrument_dict(trades):
    """Return dict with trades split by instrument name (sorted by the create time)."""
    instrument_dict = defaultdict(list)

    for trade in trades:
        instrument_dict[trade.Instrument().Name()].append(trade)
    
    for key, val in instrument_dict.iteritems():
        instrument_dict[key]= sorted(val, key=lambda trade: trade.CreateTime())

    return instrument_dict


def get_contract_ref(trade, aggregated_trades):
    """Return aggregated trade (by the instrument name and quantity)."""
    agg_candidates = aggregated_trades[trade.Instrument().Name()]
    for candidate in agg_candidates:
        if candidate.Quantity() <= 0.0 and trade.Quantity() <= 0.0:
            return candidate.Oid()
        elif candidate.Quantity() > 0.0 and trade.Quantity() > 0.0:
            return candidate.Oid()
    

def modify_split_trades2(date, dry_run=True):
    """Modify trades to be part of 'Allocation Process'.

    Specific modification for booking issue from the 13/11/2014.

    """
    aggregated_trades = defaultdict(list)
    for trade in get_aggregated_trades(date, ['PB_ALLOC_CFD_NITROGEN_CR']):
        aggregated_trades[trade.Instrument().Name()].append(trade)

    acm.BeginTransaction()
    try:
        for portfolio in NITROGEN_PORTFOLIOS:
            portfolio_trades = get_all_quantity_trades(date, portfolio)
            for trade in portfolio_trades:
                trade.Text1('Allocation Process')
                aggregated_trade_ref = get_contract_ref(trade, aggregated_trades)                
                trade.ContractTrdnbr(aggregated_trade_ref)
                
                print("{0} ({1}/{2}): Adding 'Allocation Process' and connecting the trade to the aggregated trade {3}".format(
                    trade.Oid(), trade.Instrument().Name(), trade.Portfolio().Name(), aggregated_trade_ref))
                
                trade.Commit()  
        if not dry_run:
            acm.CommitTransaction()
            print('Completed Successfully')
        else:
            acm.AbortTransaction()
            print('Dry run: Completed Successfully')
    except Exception as ex:
        acm.AbortTransaction()
        print('ERROR: {0}'.format(ex))
        print('No trades were changed for the {0}'.format(date))


def modify_split_trades(date, dry_run=True):
    """Modify trades to be part of 'Allocation Process'.
    
    1. Trades with default quantities are excluded from the execution
    premium and broker fee calculation.
    2. Trades with correct quantities are included to tine execution premium
    and broker fee calculation.
    
    Specific modification for booking issue from the 12/11/2014.
    
    """
    
    aggregated_trades = defaultdict(list)
    for trade in get_aggregated_trades(date, ['PB_ALLOC_CFD_NITROGEN_CR']):
        aggregated_trades[trade.Instrument().Name()].append(trade)

    acm.BeginTransaction()
    try:
        print('Excluding original trades from Exection Premium and Broker Fee calculation')    
        # Set all original trades to not be a part of execution premium and a broker fee
        for portfolio in NITROGEN_PORTFOLIOS:
            portfolio_trades = get_default_quantity_trades(date, portfolio)
            for trade in portfolio_trades:
                # Set PS No Fees
                ps_no_fees = at_choice.get('TradeKey3', 'PS No Fees')
                trade.OptKey3(ps_no_fees)
                
                print('{0} ({1}/{2}): Setting PS No Fees and Broker Fee Exclude'.format(
                    trade.Oid(), trade.Instrument().Name(), trade.Portfolio().Name()))
                
                # Set Broker_Fee_Exclude
                at_addInfo.save_or_delete(trade, 'Broker_Fee_Exclude', 'Yes')
                trade.Commit()

        print('Including trades with correct quantity into Exection Premium and Broker Fee calculation')        
        # Set all correct-quantity trades to be a part of an execution premium and a broker fee
        for portfolio in NITROGEN_PORTFOLIOS:
            portfolio_trades = get_all_quantity_trades(date, portfolio)
            for key, val in get_instrument_dict(portfolio_trades).iteritems():
                # Find and amend trade with correct positive quantity
                correct_trade = get_correct_positive_trade(val[:])
                if correct_trade:
                    no_opt_key = at_choice.get('TradeKey3', '')
                    aggregated_trade_ref = get_contract_ref(correct_trade, aggregated_trades)                
                    correct_trade.ContractTrdnbr(aggregated_trade_ref)
                    
                    # Clear PS No Fees
                    correct_trade.OptKey3(no_opt_key)
                    # Set Allocation Process
                    correct_trade.Text1('Allocation Process')
                    # Connect to aggregated trade
                    correct_trade.ContractTrdnbr(aggregated_trade_ref)
                    
                    print("{0}({1}/{2}): Removing PS No Fees and Broker Fee Exclude".format(
                        correct_trade.Oid(), correct_trade.Instrument().Name(), correct_trade.Portfolio().Name()))
                        
                    print("{0} ({1}/{2}): Adding 'Allocation Process' and connecting the trade to the aggregated trade {3}".format(
                        correct_trade.Oid(), correct_trade.Instrument().Name(), correct_trade.Portfolio().Name(), aggregated_trade_ref))
        
                    # Clear Broker_Fee_Exclude and commit
                    at_addInfo.save_or_delete(correct_trade, 'Broker_Fee_Exclude', 'No')
                    correct_trade.Commit()

                # Find and amend trade with correct negative quantity
                correct_trade = get_correct_negative_trade(val[:])
                if correct_trade:                        
                    no_opt_key = at_choice.get('TradeKey3', '')
                    aggregated_trade_ref = get_contract_ref(correct_trade, aggregated_trades)                
                    correct_trade.ContractTrdnbr(aggregated_trade_ref)

                    # Clear PS No Fees
                    correct_trade.OptKey3(no_opt_key)
                    # Set Allocation Process
                    correct_trade.Text1('Allocation Process')
                    # Connect to aggregated trade
                    correct_trade.ContractTrdnbr(aggregated_trade_ref)
                    
                    print("{0}({1}/{2}): Removing PS No Fees and Broker Fee Exclude ".format(
                        correct_trade.Oid(), correct_trade.Instrument().Name(), correct_trade.Portfolio().Name()))
                        
                    print("{0} ({1}/{2}): Adding 'Allocation Process' and connecting the trade to the aggregated trade {3}".format(
                        correct_trade.Oid(), correct_trade.Instrument().Name(), correct_trade.Portfolio().Name(), aggregated_trade_ref))
                    
                    # Clear Broker_Fee_Exclude and commit
                    at_addInfo.save_or_delete(correct_trade, 'Broker_Fee_Exclude', 'No')
                    correct_trade.Commit()
       
        if not dry_run:
            acm.CommitTransaction()
            print('Completed Successfully')
        else:
            print('Dry run: Completed Successfully') 
            acm.AbortTransaction()
    except Exception as ex:
        acm.AbortTransaction()
        print('ERROR: {0}'.format(ex))
        print('No trades were changed for the {0}'.format(date))


ael_variables = AelVariableHandler()
ael_variables.add_bool('dry_run',
                       label='Dry run',
                       default=True)


def ael_main(config):
    dry_run = config['dry_run']
    
    print(dry_run)
    modify_split_trades('2014-11-12', dry_run)
    modify_split_trades2('2014-11-13', dry_run)

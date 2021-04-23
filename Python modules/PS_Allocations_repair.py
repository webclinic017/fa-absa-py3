'''-----------------------------------------------------------------------
MODULE
    PS_Allocations_repair

DESCRIPTION
    This script repairs unlinked allocation trades to their aggregated trades.
    It linkes DMA trades to their agggregated trades and adds Text1 field.
    These trades need to be linked for correct fee calculation on CFDs.
    Since this script modifies voided trades, it should be run by FMAINTENACE user.

    Date                : 2015-09-10
    Purpose             : Allocation trades need to be corrected if voided manually
    Department and Desk : Prime Services
    Developer           : Ondrej Bahounek
    CR Number           : 3090215

HISTORY
=============================================================================================================
Date            Change no       Developer                       Description
-------------------------------------------------------------------------------------------------------------
2015-09-10      3090215         Ondrej Bahounek                 Initial Implementation
-----------------------------------------------------------------------'''

import acm
from at_ael_variables import AelVariableHandler


ALLOCTEXT = "Allocation Process"


def log(message):
    print('{0}: {1}'.format(acm.Time.TimeNow(), message))


ael_variables = AelVariableHandler()
PhysPortList = sorted(acm.FPhysicalPortfolio.Select(''))
UserList = sorted(acm.FUser.Select(''))

ael_variables.add(
    'alloc_portf',
    label = 'Allocation Portfolio',
    cls = 'FPhysicalPortfolio',
    collection = PhysPortList,
    default = 'PB_ALLOC_PRSTARBHF_CR',
    mandatory = True,
    multiple = False,
    alt = 'Allocation Portfolio.'
    )
ael_variables.add(
    'date',
    label = 'Date',
    cls = 'string',
    default = '2015-09-02',
    mandatory = True,
    multiple = False,
    alt = 'Date for which allocation should be repaired.'
    )
ael_variables.add(
    'create_user_aggs',
    label = 'Create User of Aggregations',
    cls = 'FUser',
    collection = UserList,
    default = None,
    mandatory = False,
    multiple = False,
    alt = 'Username of a person who created aggregated trades. \
The user who run the allocation process for the first time. \
This field should be set in a very rare situations.'
    )
ael_variables.add(
    'create_user_dmas',
    label = 'Create User of DMAs',
    cls = 'FUser',
    collection = UserList,
    default = acm.FUser['AMBA'],
    mandatory = True,
    multiple = False,
    alt = 'Username of person who created DMA trades (usually AMBA). \
These trades should be voided now. They were voided manually.'
    )
ael_variables.add(
    'excluded_trades',
    label = 'Excluded trades',
    cls = 'string',
    default = '',
    mandatory = False,
    multiple = True,
    alt = 'DMA trades that should be excluded from correction. \
These trades might have been intentionally voided before first allocation process started, \
so we want to exclude them now again.'
    )
    
class Instr:
    """ Represents an instrument together with all his trades."""
    
    def __init__(self, name, trade):
        self.name = name
        self.trades = [trade]
    
    def add_trade(self, trade):
        self.trades.append(trade)
        
    def get_positive_trades(self):
        list_pos = []
        sum = 0
        for t in self.trades:
            if t.Quantity() > 0:
                list_pos.append(t)
                sum += t.Quantity()
        return (list_pos, sum)
    
    def get_negative_trades(self):
        list_neg = []
        sum = 0
        for t in self.trades:
            if t.Quantity() < 0:
                list_neg.append(t)
                sum += t.Quantity()
        return (list_neg, sum)


def get_dmas(alloc_portf, date, create_user, excluded_trades):
    query = acm.CreateFASQLQuery('FTrade', 'AND')
    query.AddAttrNode('Status', 'EQUAL', acm.EnumFromString('TradeStatus', 'VOID'))
    query.AddAttrNode('CreateTime', 'GREATER_EQUAL', date)
    query.AddAttrNode('CreateTime', 'LESS_EQUAL', date)
    query.AddAttrNode('CreateUser.Name', 'EQUAL', create_user)
    query.AddAttrNode('Text1', 'EQUAL', '')
    query.AddAttrNode('Portfolio.Name', 'EQUAL', alloc_portf)
    for trade in excluded_trades:
        query.AddAttrNode('Oid', 'NOT_EQUAL', trade)
    trades = query.Select()
    return trades

def get_aggregations(alloc_portf, date, create_user):
    query = acm.CreateFASQLQuery('FTrade', 'AND')
    query.AddAttrNode('Status', 'EQUAL', acm.EnumFromString('TradeStatus', 'VOID'))
    query.AddAttrNode('CreateTime', 'GREATER_EQUAL', date)
    query.AddAttrNode('CreateTime', 'LESS_EQUAL', date)
    if create_user:
        query.AddAttrNode('CreateUser.Name', 'EQUAL', create_user)
    query.AddAttrNode('Text1', 'EQUAL', 'Allocation Process')
    query.AddAttrNode('Portfolio.Name', 'EQUAL', alloc_portf)
    trades = query.Select()
    return trades

def create_instrument_objs(trades):
    """ Create a dictionary of Instr objects."""
    dic_instr = {}
    for t in trades:
        insname = t.Instrument().Name()
        ins = dic_instr.get(insname)
        if not ins:
            dic_instr[insname] = Instr(insname, t)
        else:
            ins.add_trade(t)
    return dic_instr

def apply_changes(sum_dma, sum_agg, trades_aggs, trades_dmas):
    """Link all dma trades to their aggregated trade.
    
    Aggregated sum should equal to the sum of dmas quantities.
    """
    
    log("INFO: Correcting instrument '{0}'".format(trades_dmas[0].Instrument().Name()))
    log("INFO: \n\tDMA sum: {0} \n\t#DMA trades: {1} \n\tAggregated sum: {2} \n\t#Aggregated trades: {3} {4}".format(
       sum_dma, len(trades_dmas), sum_agg, len(trades_aggs), [trd.Oid() for trd in trades_aggs]))
    aggnbr = trades_aggs[0].Oid()
    if sum_dma == sum_agg:
        for tr in trades_dmas:
            tr.Text1(ALLOCTEXT)
            tr.Contract(aggnbr)
            tr.Commit()
        log("Repairing DMA trades {0}".format([trd.Oid() for trd in trades_dmas]))
    else:
        msg = "ERROR: DMA quantities {0} do not match the \
aggregated quantity {1} of aggregated trade '{2}'. ".format(sum_dma, sum_agg, aggnbr)
        msg += "Please, check DMA trades. Probably some of them are or should be excluded."
        log(msg)
        log("DMA trades: {0}".format([trd.Oid() for trd in trades_dmas]))
        raise RuntimeError(msg)

def repair_trades(alloc_portf, date, create_user_of_aggs, create_user_of_dmas, excluded_trades):
    trades_dmas = get_dmas(alloc_portf, date, create_user_of_dmas, excluded_trades)
    trades_aggs = get_aggregations(alloc_portf, date, create_user_of_aggs)

    dic_dmas = create_instrument_objs(trades_dmas)
    dic_allocs = create_instrument_objs(trades_aggs)
    
    acm.BeginTransaction()
    log("INFO: Starting of repair DMA trades (total={0})...".format(len(trades_dmas)))
    try:
        for i in dic_dmas.values():
            pos_plus_trades, sum_plus = i.get_positive_trades()
            pos_minus_trades, sum_minus = i.get_negative_trades()
            
            alloc_ins = dic_allocs.get(i.name)
            if not alloc_ins:
                raise RuntimeError('Nonexistent aggretated trade for instrument "%s"' %i.name)
            pos_plus_allocs, sum_plus_alloc = alloc_ins.get_positive_trades()
            pos_minus_allocs, sum_minus_alloc = alloc_ins.get_negative_trades()
            if len(pos_plus_allocs) > 1 or len(pos_minus_allocs) > 1:
                raise RuntimeError('More than 1 aggregated trade found for instrument "{0}" : {1}'.format(
                                    i.name,
                                   [trd.Oid() for trd in pos_plus_allocs + pos_minus_allocs]))
            
            if sum_plus > 0:
                apply_changes(sum_plus, sum_plus_alloc, pos_plus_allocs, pos_plus_trades)
            if sum_minus < 0:
                apply_changes(sum_minus, sum_minus_alloc, pos_minus_allocs, pos_minus_trades)
            print("*"*40)
        acm.CommitTransaction()
    except Exception as exc:
        acm.AbortTransaction()
        err_msg = "ERROR: {0}".format(str(exc))
        msg = "ERROR: No trade was repaired. Please, contact BTB with log details. \n{0}".format(str(exc))
        log(msg)
        raise RuntimeError(msg)

def get_valid_trades_oids(list_of_strs):
    trades_str = []
    for t in list_of_strs:
        trade = acm.FTrade[t]
        if not trade:
            msg = "ERROR: trade '{0}' is not a valid trade.".format(t)
            log(msg)
            raise RuntimeError(msg)
        else:
            trades_str.append(str(trade.Oid()))
    return trades_str

def ael_main(ael_dict):
    alloc_portf = ael_dict['alloc_portf'].Name()
    date = ael_dict['date']
    create_user_of_dmas = ael_dict['create_user_dmas'].Name()
    create_user_of_aggs = ael_dict['create_user_aggs'].Name() if ael_dict['create_user_aggs'] else ''
    excluded_alloc_trades = ael_dict['excluded_trades']
    excluded_trades = get_valid_trades_oids(excluded_alloc_trades)
    
    log("INFO: Allocation portfolio: {0}".format(alloc_portf))
    log("INFO: Correction date: {0}".format(date))
    log("INFO: Create user of DMAs: {0}".format(create_user_of_dmas))
    log("INFO: Create user of Aggregations: {0}".format(create_user_of_aggs))
    log("INFO: Excluding following trades from correction process: " + ",".join(excluded_trades))
    print("*"*80)
        
    repair_trades(alloc_portf, date, create_user_of_aggs, create_user_of_dmas, excluded_trades)
    
    log("Completed successfully.")

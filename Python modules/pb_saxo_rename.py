"""
Description
===========
Date                          :  2018-02-13
Purpose                       :  SAXO project: Rename counterparty
Department and Desk           :  FO Prime Services
Requester                     :  Eveshnee Naidoo
Developer                     :  Ondrej Bahounek

Details:
========
This script will update all trades and instruments properly to incorporate
counterparty and shortname name change.
Objects to update:
    - daily trades
    - call account instruments and trades
    - prefund instrument and trade
    - tasks
"""

import acm
from at_logging import getLogger
from at_ael_variables import AelVariableHandler
from PS_Functions import get_pb_fund_counterparty


LOGGER = getLogger(__name__)

ALLOWED_STATUSES = ('FO Confirmed', 'BO Confirmed', 'BO-BO Confirmed')

ael_variables = AelVariableHandler()
ael_variables.add("alias_old",
                  label="Old Alias",
                  cls="string",
                  mandatory=True,
                  alt=("Short name of party that got renamed"))
ael_variables.add("alias_new",
                  label="New Alias",
                  cls="string",
                  mandatory=True,
                  alt=("Short name of the new party"))


def party_exists(alias):
    try:
        get_pb_fund_counterparty(alias)
        return True
    except NotExactlyOneAlias:
        return False


def update_prefund(alias_old, alias_new):
    name_like = 'SaxoPayments*%s' % alias_old
    q = acm.CreateFASQLQuery('FTrade', 'AND')
    q.AddAttrNodeString('Portfolio.Name', 'PB_SAXO', 'EQUAL')
    q.AddAttrNodeString('Instrument.InsType', 'Swap', 'EQUAL')
    q.AddAttrNodeString('Instrument.Name', name_like, 'RE_LIKE_NOCASE')
    ornode = q.AddOpNode('OR')
    for status in ALLOWED_STATUSES:
        ornode.AddAttrNodeString('Status', status, 'EQUAL')
    
    trades = q.Select()
    if len(trades) == 0:
        return
    
    if len(trades) > 1:
        raise RuntimeError("Too many prefund trades found: %d" % len(trades))
    
    cp_new = get_pb_fund_counterparty(alias_new)
    trade = trades[0]
    instr = trade.Instrument()
    
    ins_name_new = instr.Name().replace(alias_old, alias_new)
    LOGGER.info("Updating Prefund instrument '%s' -> '%s' (%d)", instr.Name(),
        ins_name_new, trade.Oid())
    acm.BeginTransaction()
    try:
        trade.AdditionalInfo().Relationship_Party(cp_new)
        trade.Commit()
        
        instr.Name(ins_name_new)
        instr.Commit()
        acm.CommitTransaction()
    except:
        acm.AbortTransaction()
        LOGGER.exception("Prefund not updated.")
        raise


def update_callaccounts(alias_old, alias_new):
    cp_old = get_pb_fund_counterparty(alias_old)
    cp_new = get_pb_fund_counterparty(alias_new)
    
    q = acm.CreateFASQLQuery('FTrade', 'AND')
    q.AddAttrNodeString('Portfolio.Name', 'PB_SAXO_DEPO', 'EQUAL')
    q.AddAttrNodeString('Counterparty.Name', cp_old.Name(), 'EQUAL')
    ornode = q.AddOpNode('OR')
    for status in ALLOWED_STATUSES:
        ornode.AddAttrNodeString('Status', status, 'EQUAL')
    trades = q.Select()
    instruments = set(t.Instrument() for t in trades)
    
    acm.BeginTransaction()
    try:
        for instr in instruments:
            ins_name_new = instr.Name().replace(alias_old, alias_new)
            LOGGER.info("Updating call account instrument: '%s' -> '%s'",
                instr.Name(), ins_name_new)
            instr.Name(ins_name_new)
            instr.Commit()
            
            LOGGER.info("Updating call account trades...")
            for trade in instr.Trades():
                if trade.Status() not in ALLOWED_STATUSES:
                    continue
                if trade.CounterpartyId() == cp_old.Name():
                    trade.Counterparty(cp_new)
                trade.AdditionalInfo().Account_Name(ins_name_new)
                trade.Commit()
            
        acm.CommitTransaction()
    except:
        acm.AbortTransaction()
        LOGGER.exception("Call account update failed.")
        raise

    
def update_princ_trades(alias_old, alias_new):
    cp_old = get_pb_fund_counterparty(alias_old)
    cp_new = get_pb_fund_counterparty(alias_new)
    
    q = acm.CreateFASQLQuery('FTrade', 'AND')
    q.AddAttrNodeString('Portfolio.Name', 'PB_SAXO_PRINCIPAL', 'EQUAL')
    q.AddAttrNodeString('AdditionalInfo.Relationship_Party.Name', cp_old.Name(), 'EQUAL')
    ornode = q.AddOpNode('OR')
    for status in ALLOWED_STATUSES:
        ornode.AddAttrNodeString('Status', status, 'EQUAL')
    trades_rel_party = q.Select()
    
    q = acm.CreateFASQLQuery('FTrade', 'AND')
    q.AddAttrNodeString('Portfolio.Name', 'PB_SAXO_PRINCIPAL', 'EQUAL')
    q.AddAttrNodeString('Counterparty.Name', cp_old.Name(), 'EQUAL')
    ornode = q.AddOpNode('OR')
    for status in ALLOWED_STATUSES:
        ornode.AddAttrNodeString('Status', status, 'EQUAL')
    trades_cparty = q.Select()
    
    acm.BeginTransaction()
    try:
        LOGGER.info("Updating %d principal trades - Relationship_Party", len(trades_rel_party))
        for t in trades_rel_party:
            t.AdditionalInfo().Relationship_Party(cp_new)
            t.Commit()
        
        LOGGER.info("Updating %d principal trades - Counterparty", len(trades_cparty))
        for t in trades_cparty:
            t.Counterparty(cp_new)
            t.Commit()
        acm.CommitTransaction()
    except:
        acm.AbortTransaction()
        LOGGER.exception("Trades update failed.")
        raise


def update_tasks(alias_old, alias_new):
    cp_new = get_pb_fund_counterparty(alias_new)
    tasks = acm.FAelTask.Select("name like 'PB_Saxo_sweeping*%s*'" % alias_old)
    acm.BeginTransaction()
    try:
        for task in tasks:
            task_name_new = task.Name().replace(alias_old, alias_new)
            LOGGER.info("Updating task: '%s' -> '%s'", task.Name(), task_name_new)
            task.Name(task_name_new)
            params = task.Parameters()
            params.AtPutStrings("counterparty", cp_new.Name())
            task.Parameters(params)
            task.Commit()
        acm.CommitTransaction()
    except:
        acm.AbortTransaction()
        LOGGER.exception("Tasks update failed.")
        raise


def ael_main(ael_dict):
    LOGGER.msg_tracker.reset()
    alias_old = ael_dict['alias_old']
    alias_new = ael_dict['alias_new']
    
    for alias in (alias_old, alias_new):
        if not party_exists(alias):
            raise RuntimeError("Nonexisting alias: %s" % alias)
            
    update_prefund(alias_old, alias_new)
    update_callaccounts(alias_old, alias_new)
    update_princ_trades(alias_old, alias_new)
    update_tasks(alias_old, alias_new)
    
    if LOGGER.msg_tracker.errors_counter:
        raise RuntimeError("ERRORS occurred. Please check the log.")
    
    LOGGER.info("Completed successfully.")

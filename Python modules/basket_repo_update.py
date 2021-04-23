"""-----------------------------------------------------------------------
MODULE
    basket_repo_update.py

DESCRIPTION
    Date                : 2017-10-03
    Purpose             : Updates Basket Repo trade
    Department and Desk : FICC
    Requester           : Singh, Ameet: ABSA (JHB), Thomas, Shamila: Absa Capital
    Developer           : Ondrej Bahounek
    CR Number           : CHNG0004963648
    
There is a bug in Front Arena that prevents updating Basket Repo trade 
when any of his collateral trades has Trade Time after basket trade's Value Day.
This is just a workaround so RTB doesn't have to update a trade manually every time.

HISTORY
==================================================================================
Date       Change no    Developer          Description
----------------------------------------------------------------------------------
2017-10-03  4963648     Ondrej Bahounek    ABITFA-5020: initial implementation

ENDDESCRIPTION
--------------------------------------------------------------------------------"""

import acm
from at_ael_variables import AelVariableHandler
from at_logging import getLogger


LOGGER = getLogger(__name__)

TRADES_VAR_NAME = 'basket_trades'


def get_ael_variables():

    ael_variables = AelVariableHandler()
    
    ael_variables.add(
        TRADES_VAR_NAME,
        label = 'Basket Repo Trades',
        cls = acm.FTrade,
        mandatory = False,
        multiple = True,
        alt = 'Basket Repo Trade numbers'
        )
    
    
    if 'OPS' in acm.User().UserGroup().Name():
        ael_variables.add(
            'property',
            label = 'Property',
            cls = 'string',
            default = 'Status',
            mandatory = True,
            multiple = True,
            enabled = False,  # OPS should not be able to update anything, but Status
            alt = 'Trade property to update'
            )
    else:
        ael_variables.add(
            'property',
            label = 'Property',
            cls = 'string',
            default = 'Status',
            mandatory = True,
            multiple = True,
            alt = 'Trade property to update'
            )
        
            
    ael_variables.add(
        'value',
        label = 'Value',
        cls = 'string',
        default = 'BO-BO Confirmed',
        mandatory = True,
        multiple = True,
        alt = 'Value of the property'
        )
    ael_variables.add_bool(
        'apply_to_colls',
        label = 'Apply to collaterals?',
        mandatory = True,
        default = True,
        alt = ('Check if you wish to apply the same to collateral trades. '
               'All valid collateral trades will be selected (Void etc. excluded).')
        )

    return ael_variables
    
ael_variables = get_ael_variables()


def run(eii):
    eobj = eii.ExtensionObject()
    trade = eobj.OriginalTrade()
    if trade:
        task = acm.FAelTask['BASKET_REPO_UPDATE_STATUS'].Clone()
        p = task.Parameters()
        p.AtPutStrings(TRADES_VAR_NAME, trade.Oid())
        task.Parameters(p)
        acm.StartRunScript(task, None)
        
    else:
        acm.RunModuleWithParameters(__name__, acm.GetDefaultContext())


def get_collaterals(trade):
    trades = acm.FTrade.Select("connectedTrade=%d and oid<>%d" % (trade.Oid(),trade.Oid()))
    valid_trds = [t for t in trades if is_valid_trade(t)]
    return valid_trds
    
    
def update_trade(trade, prop_val_list):
    for property, value in prop_val_list:
        LOGGER.info("\t %d Setting '%s': '%s'", trade.Oid(), property, value)
        trade.SetProperty(property, value)

    
def is_valid_trade(trade):
    if trade.Status() in ('Simulated', 'Void', 'Terminated'):
        return False
        
    if trade.Instrument().IsExpired():
        return False

    return True


def ael_main(ael_dict):
    acm.PollDbEvents()
    LOGGER.msg_tracker.reset()
    
    repo_trades = ael_dict[TRADES_VAR_NAME]
    if not repo_trades:
        raise ValueError("Trades not set.")
    
    properties = ael_dict['property']
    values = ael_dict['value']
    apply_to_colls = ael_dict['apply_to_colls']
    
    zipped = list(zip(properties, values))
    
    for repo_trd in repo_trades: 
        LOGGER.info("Updating trade %d", repo_trd.Oid())
        acm.BeginTransaction()
        try:
            trades = [repo_trd]
            
            if apply_to_colls:
                trades.extend(get_collaterals(repo_trd))
            
            for trd in trades:
                update_trade(trd, zipped)
                trd.Commit()
                
            acm.CommitTransaction()
        except Exception as exc:
            acm.AbortTransaction()
            LOGGER.exception("Trade '%d' not updated: %s", repo_trd.Oid(), exc)
    
    if LOGGER.msg_tracker.errors_counter:
        raise RuntimeError("ERRORS occurred. Please check the log.")
        
    if not LOGGER.msg_tracker.warnings_counter:
        LOGGER.info("Completed successfully.")

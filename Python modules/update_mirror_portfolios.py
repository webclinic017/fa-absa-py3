"""
Date                    : 2016-09-06
Purpose                 : Update portfolios on mirror trades.
Department and Desk     : Equities
Requester               : Raymond Phillips
Developer               : Ondrej Bahounek

Description:
Create a script that will update trade's portfolios 
based on a source-target portfolio mapping.
Bulk update of mirrored trades' portfolios currently doesn't work in Trading Manager 
due to a Front Arena bug. This is a workaround to it.

Date            CR              Developer               Change
==========      =========       ======================  ========================================================
2016-09-05      3932139         Ondrej Bahounek         Initial implementation.
"""


import acm
from at_ael_variables import AelVariableHandler


ael_variables = AelVariableHandler()
ael_variables.add("trade_filter",
                  label="Trade filter",
                  cls="FTradeSelection",
                  default=None,
                  mandatory=True,
                  multiple=True,
                  alt="Trade filter with trades to be changed.")
ael_variables.add("portfolio",
                  label="Portfolio",
                  cls="FPhysicalPortfolio",
                  default=None,
                  mandatory=False,
                  multiple=True,
                  alt=("Portfolio that will be set to trades. If empty, then " 
                    "Original -> New portfolio mapping will be used."))
ael_variables.add("old_portfs",
                  label="Original Portfolios",
                  cls="FPhysicalPortfolio",
                  default=None,
                  mandatory=False,
                  multiple=True,
                  alt="Source portfolios which will be mapped to target portfolios.")
ael_variables.add("new_portfs",
                  label="New Portfolios",
                  cls="FPhysicalPortfolio",
                  default=None,
                  mandatory=False,
                  multiple=True,
                  alt="Target portfolios onto which source portfolios are mapped to.")


def ael_main(ael_dict):
    trade_filter = ael_dict['trade_filter'][0]
    trades = trade_filter.Trades()
    if ael_dict['portfolio']:
        if len(ael_dict['portfolio']) != 1:
            raise ValueError("Just 1 input portfolio expected.")
        old_portfs = list(set([t.PortfolioId() for t in trades]))
        new_portfs = [ael_dict['portfolio'][0].Name()] * len(old_portfs)
    else:
        old_portfs = [p.Name() for p in ael_dict["old_portfs"]]
        new_portfs = [p.Name() for p in ael_dict["new_portfs"]]
        if len(old_portfs) != len(new_portfs):
            raise ValueError("Input portfolio lists have different lenghts (%d vs. %d)"
                %(len(old_portfs), len(new_portfs)))
        
    mapping = dict(map(lambda x, y: (x, y), old_portfs, new_portfs))
    
    print "Portfolio mapping:"
    for item in mapping:
        print "'{0}'  ->  '{1}'".format(item, mapping[item])
    print "="*80
    
    print "Trade filter: %s (trades: %d)" %(trade_filter.Name(), len(trades))
    print "Updating..."
    
    acm.BeginTransaction()
    try:
        for trade in trades:
    
            print trade.Oid()
            
            if not mapping.has_key(trade.PortfolioId()):
                print "WARNING: Portfolio '%s' has no mapping. Ignoring this trade..." \
                    %trade.PortfolioId()
                continue

            source_portf = acm.FPhysicalPortfolio[mapping[trade.PortfolioId()]]
            if not source_portf:
                raise RuntimeError("Target portfolio '%s' does not exist." %mapping[trade.PortfolioId()])
            
            print "\t{0} -> {1}".format(trade.PortfolioId(), source_portf.Name())
            
            
            if trade.MirrorTrade() and trade.MirrorPortfolio().Name() == trade.PortfolioId():
                mirror_nbr = max(map(lambda trd: trd.Oid(), 
                    acm.FTrade.Select('mirrorTrade=%d' %trade.Oid())))
                    
                if mirror_nbr == trade.Oid():
                    raise RuntimeError("Can't select mirror trade to trade %d" %trade.Oid())
                
                print "\tUpdating from mirror trade %d" %mirror_nbr
                mirror_trade = acm.FTrade[mirror_nbr]
                try:
                    if mirror_trade.PortfolioId() == trade.PortfolioId():
                        mirror_trade.MirrorPortfolio(source_portf)
                        mirror_trade.Commit()
                    else:
                        mirror_trade.MirrorTrade().Portfolio(source_portf)
                        trade.Commit()
                except:
                    if mirror_trade.PortfolioId() == trade.PortfolioId():
                        mirror_trade.MirrorTrade().Portfolio(source_portf)
                        trade.Commit()
                    else:
                        mirror_trade.MirrorPortfolio(source_portf)
                        mirror_trade.Commit()
            else:
                trade.Portfolio(source_portf)
                trade.Commit()
            
        acm.CommitTransaction()
        
    except Exception as e:
        acm.AbortTransaction()
        print "ERROR: %s" %str(e)
        raise
    
    print "Completed successfully."

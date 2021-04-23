import acm
# Written for 2013 upgrade by P. Fabian
# Background:
# Dividend cash flows has incorrect nominal and tpl on the pswap in Front 2013
# because of incorrect estimate of nominal scaling reset (worked correctly in 2010, though).
# Changing nominal scaling reset to dividend scaling reset works number-wise. 
# However, it emits a warning about missing nominal scaling reset. 
# Cash flows seem to work correctly without resets (and latest pswap user guide also suggests 
# that dividend leg does not use any resets)
# Additionally, pswap.CreateDividendLegs() method creates a leg of nominal 
# scaling type 'Dividend Initial Price' with both nominal scaling and dividend scaling 
# resets. However, this leg seems to be ignored when calculating TPL on the pswap...

ael_variables = []

def ael_main(dict):
    # first find all CFD pswaps
    pswaps = acm.FPortfolioSwap.Select('')
    cfdPswaps = []
    for pswap in pswaps:
        fundPrf = pswap.FundPortfolio()
        if not fundPrf:
            print("%s has no fund prf" % pswap.Name()) 
        else: 
            if fundPrf.AdditionalInfo().PS_PortfolioType() == 'CFD':
                cfdPswaps.append(pswap)


    # get a list of all resets to update/delete
    resetsToUpdate = []
    for cfdPswap in cfdPswaps:
        for leg in cfdPswap.Legs():
            for cf in leg.CashFlows():
                if cf.CashFlowType() == 'Dividend':
                    for reset in cf.Resets():
                        resetsToUpdate.append(reset)


    # delete resets in transaction
    acm.BeginTransaction()
    try:
        for reset in resetsToUpdate:
            reset.Delete()
            print("Reset %s deleted" % reset.Oid())
        acm.CommitTransaction()
        print("Finished OK")
    except Exception as e:
        acm.AbortTransaction()
        print("Failed to delete one of the resets: %s" % e)
        raise

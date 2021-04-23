import acm

rtm_portfolio_swaps = acm.FPortfolioSwap.Select("name like RTM_*")
acm.BeginTransaction()
try:
    for pswap in rtm_portfolio_swaps:
        new_expiry_date = acm.Time().DateAddDelta(pswap.ExpiryDate(), 10, 0, 0)
        print("Updating expiry date for {} from {} to {}".format(
            pswap.Name(), pswap.ExpiryDate(), new_expiry_date))
        pswap.ExpiryDate(new_expiry_date)
        pswap.Commit()
    acm.CommitTransaction()
except Exception as ex:
    print("Error: {}".format(ex))
    acm.AbortTransaction()
print("Completed")
    

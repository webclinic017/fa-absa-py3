import time
import traceback
import acm
from at_ael_variables import AelVariableHandler


ael_variables = AelVariableHandler()

def ael_main(config):
    errors = []
    master_all = time.time()
    rtm_pswaps = acm.FPortfolioSwap.Select('name like "RTM_*"')
    for pswap in rtm_pswaps:
        if "43190" in pswap.Name():
            # Skip portfolio swaps for RTM Proof-of-Concept
            continue
        try:
            start = time.time()
            print("Processing DealPackage {0}".format(pswap.Name()))
            dealpackage = acm.FDealPackage.Select01("instrumentPackage='{0}'".format(pswap.Name()), None)
            if dealpackage:
                editable = dealpackage.Edit()
                cash_enabled = editable.GetAttribute('cashEnabled')
                if cash_enabled:
                    editable.SetAttribute('cashEnabled', False)
                    savedDP = editable.Save().First()
                    end = time.time()
                fee_legs = acm.FLeg.Select('instrument = "%s" and categoryChlItem = "Fee"' % 'RTM_45153_SSF1')
                for leg in fee_legs:
                    for cf in list(leg.CashFlows()):
                        cf.Delete()
                print("Successfully updated DealPackage {0} in {1} seconds".format(pswap.Name(), end - start))
            else:
                err_msg = "ERROR: DealPackage {0} not found".format(pswap)
                errors.append(err_msg)
        except Exception as ex:
            err_msg = "ERROR: Processing of DealPackage {0} failed: {1}".format(pswap, ex)
            errors.append(err_msg)
            traceback.print_exc()
    end_all = time.time()
    if errors:
        print("Completed in {0} seconds with following errors:".format(end_all - start_all))
        for err_msg in errors:
            print("\t", err_msg)
    else:
        print("Completed successfully in {0} seconds.".format(end_all - start_all))


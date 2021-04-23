import acm
from at_ael_variables import AelVariableHandler


ael_variables = AelVariableHandler()
ael_variables.add("pswaps",
    label="Portfolio swaps",
    multiple=True,
    cls=acm.FPortfolioSwap)
ael_variables.add("incorrect_start_date",
    label="Incorrect start date")
ael_variables.add("correct_start_date",
    label="Correct start date")
ael_variables.add_bool("dry_run",
    label="Dry run",
    default=True)


def ael_main(config):
    acm.BeginTransaction()
    try:
        for pswap in config["pswaps"]:
            print("Amending cash flows on portfolio swap {0}".format(pswap.Name()))
            print("Changing start date of cash flows from {0} to {1}".format(
                config["incorrect_start_date"],
                config["correct_start_date"]))        

            for leg in pswap.Legs():
                for cashflow in leg.CashFlows():
                    if cashflow.StartDate() == config["incorrect_start_date"]:
                        print("Amending cashflow {0}".format(cashflow.Oid()))
                        cashflow.StartDate(config["correct_start_date"])
                        cashflow.Commit()
        if config["dry_run"]:
            acm.AbortTransaction()
            print("Dry run successful")
        else:
            acm.CommitTransaction()
            print("Run successful")
    except Exception, e:
        acm.AbortTransaction()
        print("Amendment failed: {0}".format(e))

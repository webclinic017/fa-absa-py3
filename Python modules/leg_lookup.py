import acm
from at_time import to_datetime
from at_ael_variables import AelVariableHandler

ael_variables = AelVariableHandler()
ael_variables.add("pswaps",
                  "Portfolio swaps",
                  multiple=True,
                  collection=acm.FPortfolioSwap.Select(""),
                  mandatory=False)
ael_variables.add("create_time",
                  "Create Time From")


def add_credit_ref(leg):
    print(leg.Instrument().Name(), leg.IndexRef().Name(), to_datetime(leg.CreateTime()))
    leg.CreditRef(leg.IndexRef())
    leg.Commit()


def ael_main(config):
    if len(config["pswaps"]):
        selection_string = "instrument = '{0}' and payLeg = TRUE and legType='Fixed' and createTime >= '{1}'"
        for pswap in config["pswaps"]:
            legs = acm.FLeg.Select(selection_string.format(pswap, config["create_time"]))
            for leg in legs:
                add_credit_ref(leg)
    else:
        selection_string = "payLeg = TRUE and legType='Fixed' and createTime >= '{0}'"
        legs = acm.FLeg.Select(selection_string.format(config["create_time"]))
        for leg in legs:
            if leg.Instrument().InsType() == "Portfolio Swap":
                add_credit_ref(leg)



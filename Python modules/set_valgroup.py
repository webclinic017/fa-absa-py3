"""
Set the provided valuation group
to almost all the Prime Brokerage portfolio swaps.
"""
import sys

from at_ael_variables import AelVariableHandler

ael_variables = AelVariableHandler()
ael_variables.add_bool("create_val_group",
                       label="Create new valuation group",
                       alt=("The script will create the valuation group "
                            "with the provided name and description "
                            "before setting it to the portfolio swaps"))
ael_variables.add("val_group_name",
                  label="Valuation group name",
                  alt=("Name of the valuation group "
                       "which will be created (if desired) "
                       "and set to the portfolio swaps"))
ael_variables.add("val_group_description",
                  label="Valuation group description",
                  alt=("Description of a valuation group "
                       "which will be created if desired."))


def create_valgroup_and_context_link(val_group_name, val_group_description):
    """
    Create a new choice list with the provided valuation group name
    which will be a member of the choice list called "ValGroup".
    Then create a new context link in the "ACMB Global" context,
    which will link the ZAR-SWAP yield curve
    to this new valuation group on ZAR currency.
    """
    import acm
    valuation_group = acm.FChoiceList()
    valuation_group.List("ValGroup")
    valuation_group.Name(val_group_name)
    valuation_group.Description(val_group_description)
    valuation_group.Commit()
    context_link = acm.FContextLink()
    context_link.Context("ACMB Global")
    context_link.Currency("ZAR")
    context_link.GroupChlItem(valuation_group)
    context_link.MappingType("Val Group")
    context_link.Name("ZAR-SWAP")
    context_link.Type("Yield Curve")
    context_link.Commit()


def set_val_group(val_group_name):
    """
    Set the valuation group of almost all
    the Prime Brokerage portfolio swaps
    (with a defined set of exceptions)
    to the provided value.
    """
    exceptions = [
        "brad_temp_PB_COGITO_CFD",
        "IntFutTest",
        "Odyssey TEST PSwap",
        "ZAR/OMSFIN/SO/PSwap",
        "ZAR/OMSFIN/SO/PSwap/OLD",
        "ZAR/TEST/PSwap",
    ]
    import acm
    qf = acm.FStoredASQLQuery["PB Portfolio swaps"]
    portfolio_swaps = qf.Query().Select()
    print("Updating {0} portfolio swaps".format(len(portfolio_swaps)))
    for pswap in portfolio_swaps:
        pswap_name = pswap.Name()
        if pswap_name in exceptions:
            print("Skipping portfolio swap '{0}' ... ".format(
                pswap_name))
            continue
        sys.stdout.write(
            "Updating portfolio swap '{0}' ... ".format(pswap_name))
        pswap.ValuationGrpChlItem(val_group_name)
        pswap.Commit()
        print("done")
    print("All {0} portfolio swaps have been updated".format(
        len(portfolio_swaps)))


def main(create_val_group, val_group_name, val_group_description):
    """
    If requested, create the valuation group
    with the provided name and description
    and set it on almost all the prime brokerage portfolio swaps.
    """
    if create_val_group:
        create_valgroup_and_context_link(val_group_name, val_group_description)
    set_val_group(val_group_name)


def ael_main(parameters):
    """
    Get the parameters from the Run Script window
    and call the main function.
    """
    create_val_group = parameters["create_val_group"]
    val_group_name = parameters["val_group_name"]
    val_group_description = parameters["val_group_description"]
    main(create_val_group, val_group_name, val_group_description)

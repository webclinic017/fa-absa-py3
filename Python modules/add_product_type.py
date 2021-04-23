"""
-------------------------------------------------------------------------------
MODULE
    add_product_type

DESCRIPTION
    Date                : 2015-06-11
    Purpose             : The script adds product type to instruments.
    Department and Desk : Prime Services
    Requester           : Eveshnee Naidoo
    Developer           : Jakub Tomaga
    CR Number           : CHNG0002889266

HISTORY
===============================================================================
Date        CR number   Developer       Description
-------------------------------------------------------------------------------

-------------------------------------------------------------------------------
"""


import acm
from at_ael_variables import AelVariableHandler


ael_variables = AelVariableHandler()
ael_variables.add(
    "instruments",
    label="Instruments",
    default=None,
    multiple=True,
    cls=acm.FInstrument)
ael_variables.add(
    "product_type",
    label="Product Type",
    default=None,
    collection=acm.FChoiceList["Product Type"].ChoicesSorted())
ael_variables.add_bool(
    "dry_run",
    label="Dry Run",
    default=True)


def ael_main(config):
    """Update given set of instruments with product type."""
    instrument_list = config["instruments"]
    choice = config["product_type"]
    dry_run = config["dry_run"]

    acm.BeginTransaction()
    try:
        for instrument in instrument_list:
            message = "Adding Product Type {0} to instrument {1}"
            print(message.format(choice, instrument.Name()))
            instrument.ProductTypeChlItem(choice)
            instrument.Commit()
        if not dry_run:
            acm.CommitTransaction()
            print('Completed Successfully')
        else:
            acm.AbortTransaction()
            print('Dry run: Completed Successfully')
    except Exception as ex:
        acm.AbortTransaction()
        message = "ERROR {0}: No instruments changed to have Product Type {1}"
        print(message.format(ex, choice))

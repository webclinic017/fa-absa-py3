"""
Print all the accessible information
about all the currently available prime brokerage funds.

This module intentionally does not make use of the cached instances
of the PrimeBrokerageFund classes, because the reports it generates
are supposed to reflect the persistent (i.e. uncached) state
of the prime brokerage funds, as stored in the text objects.
"""

from csv import DictWriter
from sys import stdout

from at_ael_variables import AelVariableHandler
from at_logging import getLogger
from pb_attr_def import AttributeDefinition
from pb_quirk import PortfolioSwapBasedQuirk
from pb_storage_attr_def import AttributeDefinitionStorage
from pb_storage_fund import PrimeBrokerageFundStorage


LOGGER = getLogger()


def print_pb_fund(csv_writer, pb_fund):
    """
    Print all the available attributes and quirks
    of the provided prime brokerage fund.
    """
    fund_id = str(pb_fund.fund_id)  # convert from unicode to str
    LOGGER.info("Printing information about the prime brokerage fund %s",
                fund_id)
    row_dict = {"fund_id": fund_id}
    for attr_id, attribute in pb_fund.attributes.iteritems():
        row_dict[attr_id] = attribute.getvalue()
    for attr_id, quirk in pb_fund.quirks.iteritems():
        if isinstance(quirk, PortfolioSwapBasedQuirk):
            continue
        try:
            row_dict[attr_id] = quirk.getvalue()
        except:
            LOGGER.exception("Unable to get attribute value. "
                             "fund_id: %s, attr_id: %s",
                             fund_id, attr_id)
    csv_writer.writerow(row_dict)


def print_pb_fund_product_types(csv_writer, pb_fund):
    """
    Print all the available product-type-related attributes and quirks
    of the provided prime brokerage fund.
    """
    fund_id = str(pb_fund.fund_id)  # convert from unicode to str
    LOGGER.info("Printing product-type-related information "
                "about the prime brokerage fund %s",
                fund_id)
    for acm_portfolio_swap in pb_fund.get_product_type_pswaps():
        row_dict = {"fund_id": fund_id}
        for attr_id, quirk in pb_fund.quirks.iteritems():
            if isinstance(quirk, PortfolioSwapBasedQuirk):
                try:
                    row_dict[attr_id] = quirk.getvalue(acm_portfolio_swap)
                except:
                    LOGGER.exception("Unable to get product-type-related "
                                     "attribute value. "
                                     "fund_id: %s, pswap: %s, attr_id: %s",
                                     fund_id,
                                     acm_portfolio_swap.Name(),
                                     attr_id)
        csv_writer.writerow(row_dict)


def print_generic_report(attr_def_storage, pb_fund_storage, output_path):
    """
    Print all the available generic attribute definitions,
    of all the available prime brokerage funds
    """
    if output_path is None:
        csv_file = stdout
    else:
        csv_file = open(output_path, "wb")
    fieldnames = ["fund_id"]
    attr_ids = [
        attr_id for attr_id, attr_def
        in attr_def_storage.attr_defs.iteritems()
        if attr_def.category not in (
            AttributeDefinition.PRODUCT_TYPE_CATEGORY,
            AttributeDefinition.ADD_PRODUCT_TYPE_CATEGORY)]
    fieldnames.extend(sorted(attr_ids))
    csv_writer = DictWriter(csv_file, fieldnames)
    row_dict = {"fund_id": "Fund ID"}
    sample_fund = pb_fund_storage.load_fund(
        next(pb_fund_storage.stored_funds.iterkeys()))
    for attr_id, _attribute in sample_fund.attributes.iteritems():
        row_dict[attr_id] = str(attr_def_storage.attr_defs[attr_id].name)
    for attr_id, quirk in sample_fund.quirks.iteritems():
        if isinstance(quirk, PortfolioSwapBasedQuirk):
            continue
        row_dict[attr_id] = str(attr_def_storage.attr_defs[attr_id].name)
    csv_writer.writerow(row_dict) # header
    for fund_id in sorted(pb_fund_storage.stored_funds):
        pb_fund = pb_fund_storage.load_fund(fund_id)
        print_pb_fund(csv_writer, pb_fund)
    if output_path is not None:
        csv_file.close()


def print_product_type_report(attr_def_storage, pb_fund_storage, output_path):
    """
    Print all the available generic attribute definitions,
    of all the available prime brokerage funds
    """
    if output_path is None:
        csv_file = stdout
    else:
        csv_file = open(output_path, "wb")
    fieldnames = ["fund_id"]
    attr_ids = [
        attr_id for attr_id, attr_def
        in attr_def_storage.attr_defs.iteritems()
        if attr_def.category == AttributeDefinition.PRODUCT_TYPE_CATEGORY]
    fieldnames.extend(sorted(attr_ids))
    csv_writer = DictWriter(csv_file, fieldnames)
    row_dict = {"fund_id": "Fund ID"}
    sample_fund = pb_fund_storage.load_fund(
        next(pb_fund_storage.stored_funds.iterkeys()))
    for attr_id, attr_def in attr_def_storage.attr_defs.iteritems():
        if (attr_id in sample_fund.quirks
                and isinstance(sample_fund.quirks[attr_id],
                               PortfolioSwapBasedQuirk)):
            row_dict[attr_id] = str(attr_def.name)
    csv_writer.writerow(row_dict) # header
    for fund_id in sorted(pb_fund_storage.stored_funds):
        pb_fund = pb_fund_storage.load_fund(fund_id)
        print_pb_fund_product_types(csv_writer, pb_fund)
    if output_path is not None:
        csv_file.close()


def main(output_path_generic=None, output_path_product_type=None):
    """
    Print all the available reports with all the attributes
    of all the available prime brokerage funds.
    """
    attr_def_storage = AttributeDefinitionStorage()
    attr_def_storage.load()
    pb_fund_storage = PrimeBrokerageFundStorage()
    pb_fund_storage.load()
    print_generic_report(attr_def_storage,
                         pb_fund_storage,
                         output_path_generic)
    print_product_type_report(attr_def_storage,
                              pb_fund_storage,
                              output_path_product_type)


ael_variables = AelVariableHandler()
ael_variables.add_output_file(
    "output_path_generic",
    label="Output path for the generic report",
    alt=("A path to a file "
         "where the generic report will be saved."),
    default="/services/frontnt/Task/pb_funds_generic.csv"
)
ael_variables.add_output_file(
    "output_path_product_type",
    label="Output path for the product type report",
    alt=("A path to a file "
         "where the product type report will be saved."),
    default="/services/frontnt/Task/pb_funds_product_types.csv"
)


def ael_main(parameters):
    """
    This function is launched when running this module from FA GUI.
    """
    output_path_generic = str(parameters["output_path_generic"])
    output_path_product_type = str(parameters["output_path_product_type"])
    main(output_path_generic, output_path_product_type)

"""
A script which sets the desired rounding specification
on all the instruments determined by the specified query folder.

Requested by:       Money Market Desk
Developer:          Peter Basista
Code reviewer:      TBD
Sign-off provider:  TBD
CR:                 CHNG0002369156
Deployment date:    2014-10-21
"""
import acm

import at_ael_variables


def rounding_specification_enabler(selected_variable):
    """
    A hook function which disables or enables the rounding_specification
    field of ael_variables upon ticking or unticking
    the clear_rounding_specification checkbox.
    """
    value = selected_variable.value
    rounding_specification = selected_variable.handler.get(
        "rounding_specification")
    if value == "true":
        rounding_specification.value = rounding_specification.collection[0]
        rounding_specification_enabled = False
    else:  # assume that in this case value == "false"
        rounding_specification_enabled = True
    rounding_specification.enabled = rounding_specification_enabled


ael_variables = at_ael_variables.AelVariableHandler()
ael_variables.add("query_folder",
                  label="Query folder",
                  alt=("Query folder selecting instruments "
                       "whose rounding specification shall be updated."),
                  cls=acm.FStoredASQLQuery,
                  collection=acm.FStoredASQLQuery.Instances())
ael_variables.add_bool("clear_rounding_specification",
                       label="Clear rounding specification",
                       alt=("Check this if you want to clear "
                            "the rounding specification"
                            "on all the instruments "
                            "selected by the query folder."),
                       hook=rounding_specification_enabler)
ael_variables.add("rounding_specification",
                  label="Rounding specification",
                  alt=("Rounding specification to set "
                       "on all the instruments selected by the query folder."),
                  cls=acm.FRoundingSpec,
                  collection=acm.FRoundingSpec.Instances())


def ael_main(params):
    """
    An entry point for script execution from GUI.
    """
    query_folder = params["query_folder"]
    clear_rounding_specification = params['clear_rounding_specification']
    if clear_rounding_specification:
        rounding_specification = None
        print("Clearing the rounding specification.")
    else:
        rounding_specification = params['rounding_specification']
        print("Using the rounding specification '{0}'.".format(
            rounding_specification.Name()))
    if query_folder.QueryClass() != acm.FInstrument:
        message = "The query folder needs to select instruments."
        raise TypeError(message)
    query = query_folder.Query()
    print("Selecting the instruments defined by the query folder.")
    instruments = query.Select()
    print("{0} instruments selected.".format(len(instruments)))
    print("Filtering the instruments.")
    # FIXME: Agree on this filtering level
    instruments = [instrument for instrument in instruments
                   if acm.Time.DateDifference(instrument.ExpiryDate(),
                                              acm.Time.DateToday()) >= 0]
    print(("Filtering finished. {0} instruments "
           "meet the filtering criteria.").format(len(instruments)))
    print("Processing {0} instruments in the query folder '{1}'.".format(
        len(instruments), query_folder.Name()))
    acm.BeginTransaction()
    try:
        for instrument in instruments:
            try:         
                instrument.RoundingSpecification(rounding_specification)
                instrument.Commit()
            except Exception as e:
                print('Error when committing instrument %s:' %instrument.Name(), e)                
        print("Committing the transaction.")
        acm.CommitTransaction()
        print("Transaction has been successfully committed.")
    except RuntimeError as exc:
        acm.AbortTransaction()
        print("The transaction could not be committed. Reason: '{1}'".format(
            exc))
        raise

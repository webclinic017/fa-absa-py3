#!/usr/bin/python
"""%prog INSTRUCTIONS_FILEPATH

Move all the desired legs, cashflows and resets
describing the historical PnL of the specified instruments
from one portfolio swap to another.

The details about the specific operations to perform
are read from the input file with the move instructions.
"""
from csv import reader
from optparse import OptionParser
from sys import stderr

from at_ael_variables import AelVariableHandler

ael_variables = AelVariableHandler()
ael_variables.add_input_file("input_filepath",
                             label="Input file path",
                             alt=("A path to the input file "
                                  "containing the move instructions."))


class MoveInstruction(object):

    """
    A class describing a single move instruction.
    """
    def __init__(self, instrument_name, from_ps_name, to_ps_name):
        self.instrument_name = instrument_name
        self.from_ps_name = from_ps_name
        self.to_ps_name = to_ps_name


def parse_instructions(input_filepath):
    """
    Parse the move instructions
    from the input file at the provided path
    and return a list containing all of them.
    """
    with open(input_filepath, "r") as input_file:
        csv_reader = reader(input_file)
        instructions = []
        for row in csv_reader:
            instrument_name = row[0]
            from_ps_name = row[1]
            to_ps_name = row[2]
            instruction = MoveInstruction(instrument_name,
                                          from_ps_name,
                                          to_ps_name)
            instructions.append(instruction)

        return instructions


def move_pswap_leg(index_ref_acm_instrument,
                   from_acm_pswap,
                   to_acm_pswap):
    """
    Move the leg with the provided index ref
    from the provided 'from' portfolio swap
    to the provided 'to' portfolio swap.
    """
    import acm
    candidate_legs = acm.FLeg.Select(("instrument = {0} "
                                      "and indexRef = {1}").format(
                                          from_acm_pswap.Oid(),
                                          index_ref_acm_instrument.Oid()))
    if not candidate_legs:
        exception_message = ("The portfolio swap '{0}' "
                             "does not have any leg "
                             "with index ref '{1}'.").format(
                                 from_acm_pswap.Name(),
                                 index_ref_acm_instrument.Name())
        raise RuntimeError(exception_message)
    try:
        acm.BeginTransaction()
        for leg in candidate_legs:
            leg.Instrument(to_acm_pswap)
            leg.Commit()
        acm.CommitTransaction()
    except RuntimeError as exc:
        acm.AbortTransaction()
        error_message = ("There was an error while committing the legs "
                         "on the portfolio swap '{0}'. "
                         "Exception message: {1}").format(
                             to_acm_pswap.Name(), exc)
        print(error_message, file=stderr)
        raise
    info_message = ("All legs with index ref '{0}' "
                    "moved from portfolio swap '{1}' "
                    "to portfolio swap '{2}'.").format(
                        index_ref_acm_instrument.Name(),
                        from_acm_pswap.Name(),
                        to_acm_pswap.Name())
    print(info_message)


def move_pswap_history(move_instructions):
    """
    Use the provided move instructions
    to move the history of the specified instruments
    from one portfolio swap to another.
    """
    import acm
    for instruction in move_instructions:
        index_ref_acm_instrument = acm.FInstrument[instruction.instrument_name]
        if not index_ref_acm_instrument:
            exception_message = "Instrument '{0}' cannot be found.".format(
                instruction.instrument_name)
            raise RuntimeError(exception_message)
        from_acm_pswap = acm.FPortfolioSwap[instruction.from_ps_name]
        if not from_acm_pswap:
            exception_message = "Portfolio swap '{0}' cannot be found.".format(
                instruction.from_ps_name)
            raise RuntimeError(exception_message)
        to_acm_pswap = acm.FPortfolioSwap[instruction.to_ps_name]
        if not to_acm_pswap:
            exception_message = "Portfolio swap '{0}' cannot be found.".format(
                instruction.to_ps_name)
            raise RuntimeError(exception_message)
        move_pswap_leg(index_ref_acm_instrument,
                       from_acm_pswap,
                       to_acm_pswap)


def ael_main(parameters):
    """
    Get the parameters from the Run Script window
    and call the portfolio swap history moving function.
    """
    input_filepath = parameters["input_filepath"].SelectedFile().Text()
    instructions = parse_instructions(input_filepath)
    try:
        move_pswap_history(instructions)
    except RuntimeError as exc:
        print(exc)


def main():
    """
    Get the parameters from the command line
    and call the portfolio swap history moving function.
    """
    parser = OptionParser(usage=__doc__)
    _options, args = parser.parse_args()
    if len(args) != 1:
        parser.error("Wrong number of arguments.")
    instructions = parse_instructions(args[0])
    move_pswap_history(instructions)


if __name__ == "__main__":
    main()

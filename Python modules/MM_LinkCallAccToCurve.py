"""
A script which reads the input Excel file
and updates the listed instruments
with the required float refs and spreads.

Requested by:       Money Market Desk
Developer:          Peter Basista
Code reviewer:      Jakub Tomaga
CR:                 CHNG0002040818
Deployment date:    2014-06-20
"""

import os
import traceback

import acm

import at_addInfo
from at_feed_processing import (notify_log,
                                RecordsFeedProcessor,
                                SimpleXLSFeedProcessor)

RecordProcessingException = RecordsFeedProcessor.RecordProcessingException


class FloatRefProcessor(SimpleXLSFeedProcessor):

    """
    A class for processing simple 3 column entries in Excel file
    containing instrument ID, CallFloatRef and CallFloatSpread
    and setting these attributes on the provided instrument.
    """

    instrument_header = "instrument"
    curve_header = "rate index"
    spread_header = "spread"

    _required_columns = [instrument_header,
                         curve_header, spread_header]


    def __init__(self, change_rates, file_path, sheet_index, sheet_name):
        self.change_rates = change_rates
        if self.change_rates:
            message = "Using the provided spread values."
        else:
            message = "Using the calculated spread values."
        self._log(message)
        super(FloatRefProcessor, self).__init__(file_path,
                                                sheet_index,
                                                sheet_name)


    def _process_record(self, record, dry_run):
        """
        Set the refs on a single instrument.
        """
        _index, data = record
        instrument_name = data[self.instrument_header]
        instrument = acm.FInstrument[instrument_name.encode("ascii")]
        if not instrument:
            message = "Instrument '{0}' could not be found.".format(
                instrument_name)
            raise RecordProcessingException(message)
        if instrument.InsType() != "Deposit":
            message = ("The type of instrument '{0}' is '{1}', "
                       "but the requirement is to only work on instruments "
                       "of type 'Deposit'.").format(instrument.Name(),
                                                    instrument.InsType())
            raise RecordProcessingException(message)
        legs = instrument.Legs()
        if len(legs) != 1:
            message = ("Instrument '{0}' does not have "
                       "exactly one leg.").format(instrument.Name())
            raise RecordProcessingException(message)
        leg = legs[0]
        if leg.LegType() != "Call Fixed Adjustable":
            message = ("The only leg of instrument '{0}' is of type "
                       "'{1}', but the requirement is to only touch "
                       "the instruments whose only leg "
                       "has the type 'Call Fixed Adjustable'.").format(
                           instrument.Name(), leg.LegType())
            raise RecordProcessingException(message)
        ref_instrument_name = data[self.curve_header]
        ref_instrument = acm.FInstrument[ref_instrument_name.encode("ascii")]
        if not ref_instrument:
            message = "Ref instrument '{0}' could not be found.".format(
                ref_instrument_name)
            raise RecordProcessingException(message)
        provided_spread = float(data[self.spread_header])
        fixed_rate = leg.FixedRate()
        ref_rate = ref_instrument.used_price()
        calculated_spread = fixed_rate - ref_rate
        if abs(calculated_spread - provided_spread) > 0.00001:
            message = ("Instrument '{0}': "
                       "The provided spread ({1}) is different from "
                       "the calculated spread ({2}).").format(
                           instrument.Name(),
                           provided_spread,
                           calculated_spread)
            self._log(message)
        if self.change_rates:
            used_spread = provided_spread
        else:
            used_spread = calculated_spread
        if not dry_run:
            try:
                # It is necessary to use transactions,
                # because the spread itself cannot be updated
                # to a nonzero value unless the float ref is already set.
                # At the same time, the float ref cannot be updated
                # to any nonempty value while the spread is not set.
                acm.BeginTransaction()
                at_addInfo.save(instrument, "CallFloatSpread", used_spread)
                at_addInfo.save(instrument, "CallFloatRef",
                                ref_instrument.Name())
                acm.CommitTransaction()
            except RuntimeError:
                acm.AbortTransaction()
                message = "Instrument '{0}': {1}".format(instrument.Name(),
                                                         traceback.format_exc())
                raise RecordProcessingException(message)


ael_variables = FloatRefProcessor.ael_variables(
    file_dir='F:/',
    file_name='MM_FinalCurveUploadData.xlsx')
ael_variables.add_bool("change_rates",
                       label="Change rates",
                       default=False,
                       alt=("Change the effective call account rates "
                            "to the rates specified in the input file."))


def ael_main(params):
    """
    An entry point for task execution from GUI.
    """
    file_dir = params['file_dir']
    file_name = params['file_name']
    file_path = os.path.join(file_dir, file_name)
    dry_run = params['dry_run']
    change_rates = params['change_rates']
    processor = FloatRefProcessor(change_rates, file_path, 0, None)
    processor.add_error_notifier(notify_log)
    processor.process(dry_run)
    if not processor.errors:
        print("Completed successfully")

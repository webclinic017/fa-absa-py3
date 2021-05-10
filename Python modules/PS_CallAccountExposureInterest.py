"""
=================================================================================================================================
MODULE                  :       PS_CallAccountExposureInterest
PURPOSE                 :       Script to post exposure interest cash flows to Call Accounts.
=================================================================================================================================

HISTORY
=================================================================================================================================
Date            Developer              Description
=================================================================================================================================
2012-08-08      Marcus Ambrose         Implemented
"""
import acm

import at_addInfo
from at_ael_variables import AelVariableHandler
from at_logging import getLogger
from PS_FormUtils import DateField
from PS_CallAccountManualDeposit import create_cf, call_acc_hook

LOGGER = getLogger(__name__)
DATES = DateField.get_captions(["PrevBusDay", "Now", "Custom Date"])
SETTLE_TYPE = "Settle"
DEPOSIT_TYPE = "Exposure Interest"


def get_fx_rate(curr_from, curr_to, input_date):
    try:
        calc_space = acm.Calculations().CreateStandardCalculationsSpaceCollection()

        if curr_from == curr_to:
            return 1.0

        from_curr = acm.FCurrency[curr_from]
        to_curr = acm.FCurrency[curr_to]

        return from_curr.Calculation().FXRate(calc_space, to_curr, input_date).Number()
    except Exception:
        raise Exception(
            "Could not find fx rate for {} and {} on {}".format(
                curr_from, curr_to, input_date
            )
        )


def get_base_currency_interest(exposure, interest):
    return exposure * (interest / 100) * 365 / 360 / 12


def custom_date_hook(selected_variable):
    """Enable/Disable Custom Date base on Date value."""
    start_date = ael_variables.get("run_date")
    start_date_custom = ael_variables.get("date_custom")

    if start_date.value == "Custom Date":
        start_date_custom.enabled = True
    else:
        start_date_custom.enabled = False


ael_variables = AelVariableHandler()
ael_variables.add(
    "run_date", label="Date", default="Now", collection=DATES, hook=custom_date_hook
)
ael_variables.add(
    "date_custom", label="Date Custom", default=acm.Time().DateToday(), enabled=False
)
ael_variables.add(
    "call_acc",
    label="Call Account",
    cls="FInstrument",
    mandatory=True,
    enabled=True,
    hook=call_acc_hook,
)
ael_variables.add(
    "max_exposure", label="Max Exposure", cls="float", default=0, mandatory=True,
)
ael_variables.add(
    "interest", label="Interest", cls="float", default=0, mandatory=True,
)
ael_variables.add(
    "from_curr", label="From Currency", cls="string", default="EUR", mandatory=True,
)
ael_variables.add(
    "to_curr", label="To Currency", cls="string", default="ZAR", mandatory=True,
)


def ael_main(ael_dict):
    if ael_dict["run_date"] == "Custom Date":
        run_date = ael_dict["date_custom"]
    else:
        run_date = DateField.read_date(ael_dict["run_date"])

    fx_rate = get_fx_rate(ael_dict["from_curr"], ael_dict["to_curr"], run_date)
    base_curr_interest = get_base_currency_interest(
        ael_dict["max_exposure"], ael_dict["interest"]
    )
    posting_amount = round(base_curr_interest * fx_rate, 2)

    cf = create_cf(
        ael_dict["call_acc"], posting_amount, run_date, SETTLE_TYPE, DEPOSIT_TYPE
    )

    at_addInfo.save(cf, "PS_DepositType", DEPOSIT_TYPE)
    at_addInfo.save(cf, "Settle_Type", SETTLE_TYPE)

'''

2014-02-14

    Purpose                 : Script for removing old timeseries records
    Department and Desk     : PCG, IT Infrastucture
    Requester               : Aaeda Salejee
    Developer               : Fasko Dusan (faskdus)
    CR Number               : CHNG0001731540
    JIRA                    : ABITFA-2415

'''

import acm
from at_ael_variables import AelVariableHandler

ael_gui_parameters = {
    'windowCaption': 'Remove old timeseries records',
    'runButtonLabel': '&&Run',
    'closeWhenFinished': True
}

ael_variables = AelVariableHandler()

ael_variables.add(
    'number_of_days',
    label = 'Number of days',
    default = 7,
    mandatory = True,
    alt = 'Records older than specified number of days will be removed.',
    cls='int'
)

def ael_main(params):
    """Main run removes old time series values."""

    run_number = 1
    number_of_days = params['number_of_days']

    remove_time_series_values_older_than("TradeNumber", number_of_days,
        run_number)
    remove_time_series_values_older_than("TerminateTrdnbr", number_of_days,
        run_number)

    print("Completed successfully.")


def remove_time_series_values_older_than(time_series_name, number_of_days_abs, 
        run_number=None):
    """Remove records of given time series.

    Records to be removed can be specified by value of time series 
    specification, run number, and day older than specified number of days.

    """
    time_series_specification = acm.FTimeSeriesSpec[time_series_name]

    if not time_series_specification:
        not_existing_time_series_msg = (
            "Specified time series specification '{0}' does not exist.")
        print(not_existing_time_series_msg.format(time_series_name))
        return

    number_of_days = -1 * number_of_days_abs
    border_date = acm.Time.DateAddDelta(acm.Time.DateToday(), 0, 0, 
        number_of_days)

    select_command = "timeSeriesSpec={0} and day<='{1}'".format(
        time_series_specification.Oid(), border_date)

    if run_number:
        select_command = "{0} and runNo={1}".format(select_command, 
            run_number)

    time_series = acm.FTimeSeries.Select(select_command)

    print("Time series:", time_series_specification.FieldName()) 
    print("Linked Trades:")

    for time_serie in time_series.AsList():
        print(time_serie.Recaddr())
        time_serie.Delete()


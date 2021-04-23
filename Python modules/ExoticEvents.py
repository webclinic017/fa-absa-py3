'''
29.11.2013
    Purpose                 : Report the exotic event dates for the specified
    instruments
    Department and Desk     : Trading Equities
    Requester               : Andrey Chechin
    Developer               : Conicov Andrei
    CR Number               : CHNG0001639513, ABITFA-2391
'''

from at_ael_variables import AelVariableHandler
import acm
import os


def _get_exotic_events_dates(instruments):
    """Returns a dictionary with all the exotic events dates
    {instrument, [exotic event dates]}

    Keyword arguments:
    instruments: a list of instruments of FInstruemnt type
    """
    result = {}
    for i in instruments:
        dates = [ee.Date() for ee in i.ExoticEvents()]
        dates.sort()
        result[i] = dates

    return result


def _create_output(tf, writer_f, date_from, date_to):
    """
    Writes to the provided writer function all the instruments
    and there exotic event dates for a specified interval of
    dates and a specified trade filter.

    Keyword arguments:
    tf -- Trade filter
    writer_f -- writer function, takes a list of values (instrument name,
     exotic event date)
    date_from -- minimal exotic event date
    date_to -- maximal exotic event date
    """
    acm.Log("Iterating instruments")
    instruments = tf.Instruments()

    acm.Log("Getting exotic events for {0} instruments"
            .format(len(instruments)))
    result = _get_exotic_events_dates(instruments)
    for i, dates in result.items():
        if len(dates) > 0:
            for date in dates:
                if date >= date_from and date <= date_to:
                    writer_f([i.Name(), str(date)])


def custom_dates(fieldValues):
        """Input hook for ael_variables"""
        use_custom_dates = ael_variables[1].value == '1'
        ael_variables[2].enabled = use_custom_dates
        ael_variables[3].enabled = use_custom_dates
        return fieldValues

trade_filter_names = sorted([f.Name() for f in acm.FTradeSelection.Select("")])
ael_variables = AelVariableHandler()

ael_variables.add(
    'tf_title',
    label='TradeFilter',
    collection=trade_filter_names,
    default='EQ Index EQ Derivs',
    alt='The trade filter title that will be used to create trade rows',
    mandatory=1
    )
ael_variables.add(
    'custom_dates',
    label='Custom dates',
    collection=[0, 1],
    alt='Check this in order to use custom from and to dates',
    cls='int',
    hook=custom_dates
    )
ael_variables.add(
    'date_from',
    label='Date from',
    default=acm.Time.DateToday(),
    alt=('The minimal date from which the events should occur.'
    'This does not backdate FA'),
    mandatory=1
    )
ael_variables.add(
    'date_to',
    label='Date to',
    default=acm.Time.DateToday(),
    alt=('The maximal date until which the events should occur.'
    'This does not backdate FA'),
    mandatory=1
    )
ael_variables.add(
    'path',
    label='Output Folder',
    default=r'c:\tmp\ABITFA-2303',
    alt='The directory where to which the file will be dropped.',
    mandatory=1
    )
ael_variables.add(
    'file_name',
    label='Output File Name',
    default='ExoticEvents.xls',
    alt='The file name',
    mandatory=1
    )


def ael_main(dict_arg):
    """Main entry point for FA"""
    acm.Log("Starting {0}".format(__name__))

    if str(acm.Class()) == "FTmServer":
        warning_function = acm.GetFunction("msgBox", 3)
    else:
        warning_function = lambda t, m, *_r: print("{0}: {1}".format(t, m))

    tf_title = dict_arg['tf_title']
    custom_dates = dict_arg['custom_dates']
    path = dict_arg['path']
    file_name = dict_arg['file_name']

    date_from = acm.Time.DateToday()
    date_to = acm.Time.DateToday()
    if custom_dates:
        date_from = dict_arg['date_from']
        date_to = dict_arg['date_to']

    if not os.access(path, os.W_OK):
        warning_function("Warning",
            "Output path is not writable! Client valuation not generated!", 0)
        return

    tf = acm.FTradeSelection[tf_title]
    if not tf:
        warning_function("Warning",
            "Trade filter with name '{0}' was not found.".format(tf_title), 0)
        return

    file_path = os.path.join(path, file_name)

    with open(file_path, 'w') as file_w:
        writer_f = lambda data: file_w.write("\t".join(data) + '\n')
        writer_f([tf_title])
        _create_output(tf, writer_f, date_from, date_to)

    acm.Log("Wrote secondary output to {0}".format(file_path))
    acm.Log("Completed successfully")

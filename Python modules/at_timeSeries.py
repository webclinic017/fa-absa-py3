
'''
2014-02-14

    Description:  Time series helper functions.
    Developer:    Fasko Dusan (faskdus)
    CR Number:    n/a
    JIRA:         n/a

HISTORY
    2013-02-12    Sinkora Jan (sinkoraja)  n/a          add_time_series_value run_number default value, run_number = None handling
    2014-02-20    Fasko Dusan (faskodus)   ABITFA-2473  get_time_series_value run_number = 0 correction

'''


import acm

def get_time_series_values(ts_name, recaddr=None, date=None, run_number=None):
    '''Return the time-series entities that match the provided parameters.'''

    tsSpec = acm.FTimeSeriesSpec[ts_name]
    if tsSpec:
        # creating the select cmd
        cmd = "timeSeriesSpec={0}".format(tsSpec.Oid())
        if recaddr:
            cmd = "{0} and recaddr={1}".format(cmd, recaddr)
        if date:
            cmd = "{0} and day='{1}'".format(cmd, date)
        if run_number is not None:
            cmd = "{0} and runNo={1}".format(cmd, run_number)

        ts = acm.FTimeSeries.Select(cmd)
        return ts
    else:
        return None


def remove_time_series_values(ts_name, recaddr=None, date=None, run_number=None):
    '''Remove the time-series entities that match the provided parameters.

    Returns the number of removed entities.

    '''

    removed_ts = 0
    existing_ts = get_time_series_values(ts_name, recaddr, date, run_number)

    if existing_ts:
        removed_ts = len(existing_ts)
        for t in list(existing_ts):
            t.Delete()
    return removed_ts


def add_time_series_value(ts_name, recaddr, value, date, run_number=None, overwrite=False):
    '''Create a time-series entry.

    Will fail if a similar time-series entry already exists ('Invalid field value').
    If run_number is None, this will pick the first auto-increment available for
    the given day.
    
    If run_number and overwrite are set, existing time-serie will be overwritten.

    '''

    ts_spec = acm.FTimeSeriesSpec[ts_name]
    if ts_spec:
        ts = None
        if run_number == None:
            existing_ts = get_time_series_values(ts_name, recaddr, date)
            if not existing_ts:
                run_number = 0
            else:
                run_number = max([record.RunNo() for record in existing_ts])
                run_number += 1
        elif run_number is not None and overwrite:
            existing_ts = get_time_series_values(ts_name, recaddr, date, run_number)
            if existing_ts:
                ts = existing_ts[0]
        
        if not ts:
            ts = acm.FTimeSeries()
        ts.Day(date)
        ts.TimeSeriesSpec(ts_spec)
        ts.RunNo(run_number)
        ts.TimeValue(value)
        ts.Recaddr(recaddr)
        ts.Commit()  # don't cache the exception, this should be done by the caller
    else:
        raise ValueError('Time-series {0} has not been defined.'.format(ts_name))



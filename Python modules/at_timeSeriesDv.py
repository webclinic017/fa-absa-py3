import acm

def get_time_series_values(ts_name, recaddr1=None, recaddr2=None, date=None):
    """Return the time-series entities that match the provided parameters."""

    tsSpec = acm.FTimeSeriesDvSpec[ts_name]
    if tsSpec:
        # creating the select cmd
        cmd = "timeSeriesDvSpecification={0}".format(tsSpec.Oid())
        if recaddr1:
            cmd = "{0} and recordAddress1={1}".format(cmd, recaddr1)
        if recaddr2:
            cmd = "{0} and recordAddress2={1}".format(cmd, recaddr2)
        if date:
            cmd = "{0} and storageDate='{1}'".format(cmd, date)

        ts = acm.FTimeSeriesDv.Select(cmd)
        return ts
    else:
        return None


def remove_time_series_values(ts_name, recaddr1=None, recaddr2=None, date=None):
    """Remove the time-series entities that match the provided parameters.

    Returns the number of removed entities.
    """

    removed_ts = 0
    existing_ts = get_time_series_values(ts_name, recaddr1, recaddr2, date)

    if existing_ts:
        removed_ts = len(existing_ts)
        for t in existing_ts:
            t.Delete()
    return removed_ts


def add_time_series_value(ts_name, recaddr1, recaddr2, date, dv):
    """Create a denominated time-series entry.

    Args:
        ts_name: Time series name (string)
        recaddr1: Record address value (int)
        recaddr2: Record address value (int)
        date: Storage date of a time series (date)
        dv: An FDenominatedVaue object (FDenominatedValue)

    Returns:
        Function returns existing or newly created FTimeSeriesDv object.

    Raises:
        ValueError: An error when time series spec is not defined
    """

    ts_spec = acm.FTimeSeriesDvSpec[ts_name]
    if ts_spec:
        existing_ts = get_time_series_values(ts_name, recaddr1, recaddr2, date)
        if len(existing_ts) == 1:
            return existing_ts.First()

        ts = acm.FTimeSeriesDv()
        ts.TimeSeriesDvSpecification(ts_spec)
        ts.RecordAddress1(recaddr1)
        ts.RecordAddress2(recaddr2)
        ts.StorageDate(date)
        ts.DvValue(dv.Number())
        ts.DvDate(dv.DateTime())
        try:
            ts.DvCurrency(dv.Unit())
        except TypeError:
            # suppress the error if it's not possible
            # to convert the unit to FCurrency
            pass
        ts.Commit() # don't catch exceptions, this should be done by the caller
        return ts
    else:
        raise ValueError('Time-series {0} has not been defined.'.format(ts_name))

def update_time_series_value(ts_name, recaddr1, recaddr2, date, dv):
    """Creates or updates time-series entity.

    Args:
        ts_name: Time series name (string)
        recaddr1: Record address value (int)
        recaddr2: Record address value (int)
        date: Storage date of a time series (date)
        dv: An FDenominatedVaue object (FDenominatedValue)
    """

    existing_ts = get_time_series_values(ts_name, recaddr1, recaddr2, date)

    if len(existing_ts) == 1:
        ts = existing_ts.First()
        ts_clone = ts.Clone()

        ts_clone.StorageDate(date)
        ts_clone.DvValue(dv.Number())
        ts_clone.DvDate(dv.DateTime())
        try:
            ts_clone.DvCurrency(dv.Unit())
        except TypeError:
            # suppress the error if it's not possible
            # to convert the unit to FCurrency
            pass
        ts.Apply(ts_clone)
        try:
            ts.Commit()
        except RuntimeError:
            # supress update colission or deadlocked on lock
            # resources with another process error
            pass
        return ts
    else:
        return add_time_series_value(ts_name, recaddr1, recaddr2, date, dv)

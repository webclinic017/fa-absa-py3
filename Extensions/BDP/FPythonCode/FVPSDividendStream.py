""" Compiled: 2020-09-18 10:38:51 """

#__src_file__ = "extensions/vps/etc/FVPSDividendStream.py"
#----------------------------------------------------------------------------
#    (c) Copyright 2020 SunGard Front Arena. All rights reserved.
#----------------------------------------------------------------------------
"""----------------------------------------------------------------------------
MODULE
        FVPSDividendStream - Stores historical dividend streams

DESCRIPTION
        Functionality for storing and deleting historical entities of
        type DividendStream.

        If there exist no historical dividend stream
        a new will always be created with
        date_from = today
        date_to = BIG_DATE

        If there exist a historical dividend stream with
        date_to = ael.BIG_DATE, this entity's date_to will be set to today and
        a new historical dividend stream will be created with date_from = today
        and date_to = ael.BIG_DATE.
----------------------------------------------------------------------------"""


import acm
import ael


import FBDPCommon


def delete_ds_in_list(world, ds_id_list, params):
    nr_deleted = 0
    failures = {}
    delete_id_list = ds_id_list[:]
    last_delete_length = len(delete_id_list) + 1

    while len(delete_id_list) > 0:
        if len(delete_id_list) == last_delete_length:
            # No ds deleted in last loop, stop looping
            for name in failures:
                oid, reason = failures[name]
                failMsg = 'Unable to delete {0}. {1}'.format(name, reason)
                world.summaryAddFail('DividendStream[Hist]', oid, 'DELETE',
                        reasons=[failMsg])
                world.logError(failMsg)
            return nr_deleted
        last_delete_length = len(delete_id_list)

        id_list = delete_id_list[:]
        for oid in id_list:
            ds = ael.DividendStream[oid]
            if not ds:
                world.logDebug('    DividendStream seqnbr=\'{0}\' in Database '
                        'not found in Cache'.format(oid))
                delete_id_list.remove(oid)
                continue
            name = ds.name

            live_ds = ds.original_ds_seqnbr

            if params.dividend_streams_base:
                if live_ds.name in params.dividend_streams_excl:
                    world.logDebug('    Found {0} in the exclusion list - '
                            'will not delete'.format(name))
                    delete_id_list.remove(oid)
                    continue
            else:
                if live_ds.name not in params.dividend_streams_incl:
                    world.logDebug('    {0} is not in the inclusion list - '
                            'will not delete'.format(name))
                    delete_id_list.remove(oid)
                    continue
            # Note the summary will do duplication check, so do not need to
            # worry about oid duplication.
            world.summaryAddOk('DividendStream', live_ds.seqnbr, 'SELECT')
            world.summaryAddOk('DividendStream[Hist]', oid, 'SELECT')
            try:
                d_from = ds.date_from
                d_to = ds.date_to
                if not world.isInTestMode():
                    ds.delete()
                nr_deleted += 1
                delete_id_list.remove(oid)
                ds_id_list.remove(oid)
                if name in failures:
                    failures.pop(name)
                world.summaryAddOk('DividendStream[Hist]', oid, 'DELETE')
                world.logDebug('    Deleted {0} in the period '
                        'from {1} to {2}'.format(name, d_from, d_to))
            except:
                world.logDebug('    Unable to delete {0}, will attempt '
                        'again'.format(name))
                failures[name] = (oid, FBDPCommon.get_exception())
    return nr_deleted


def delete_all_ds_in_period(world, aelPeriodFirstDay, aelPeriodLastDay,
        params):
    """
    Deletes all dividend streams with date_from >= first day &
    date_to <= last day.
    """
    assert isinstance(aelPeriodFirstDay, ael.ael_date), ('The '
            'aelPeriodFirstDay must be an ael_date.')
    assert isinstance(aelPeriodLastDay, ael.ael_date), ('The '
            'aelPeriodLastDay must be an ael_date.')
    aelDateToday = ael.date_today()
    world.logInfo('Deleting historical dividend streams in the period '
            'from {0} to {1}.'.format(
            aelPeriodFirstDay.to_string(ael.DATE_ISO),
            aelPeriodLastDay.to_string(ael.DATE_ISO)))
    if aelPeriodLastDay >= aelDateToday:
        world.logInfo('Also deleting latest historical dividend streams. '
                '(Period end date {0} on or beyond today {1})'.format(
                aelPeriodLastDay.to_string(ael.DATE_ISO),
                aelDateToday.to_string(ael.DATE_ISO)))
        aelPeriodLastDay = ael.BIG_DATE
    sql_query = ('select seqnbr from dividend_stream where date_from >= '
            '\'{0}\' and date_to <= \'{1}\''.format(
            aelPeriodFirstDay.to_string(ael.DATE_ISO),
            aelPeriodLastDay.to_string(ael.DATE_ISO)))
    ds_id_list = FBDPCommon.get_result_in_list(ael.dbsql(sql_query))
    tot_nr_of_ds = len(ds_id_list)
    world.logInfo('Found {0} historical dividend streams in the period'.format(
            tot_nr_of_ds))
    nr_deleted = delete_ds_in_list(world, ds_id_list, params)
    world.logInfo('{0} historical dividend streams deleted.'.format(
            nr_deleted))


def test_if_name_in_db(dsname):
    """
    Is the new dividend stream name already in the database ?
    """
    name = dsname.replace("'", "''")
    sql_query = ('select count(1) from dividend_stream where name = '
            '\'{0}\''.format(name))
    for dset in ael.dbsql(sql_query):
        for column in dset:
            if int(column[0]) > 0:
                return dsname
    return None


def set_archive_flag_on_children(ds):
    for estimate in ds.Dividends():
        estimate.ArchiveStatus(1)


def create_new_ds(world, ds, today):
    """
    Create a new dividend stream
    """
    ds_new = ds.Clone()
    ds_new.DateFrom(today)
    ds_new.DateTo(ael.BIG_DATE.to_string(ael.DATE_ISO))
    ds_new.OriginalDividendStream(ds)
    ds_new.Owner(ds.Owner())
    ds_new.ArchiveStatus(1)
    ds_new.Name = FBDPCommon.createNewNameByAddingDate(ds.Name(), today,
            test_if_name_in_db)
    set_archive_flag_on_children(ds_new)

    try:
        ds_new.Commit()
        world.logInfo('    Stored historical dividend stream {0}'.format(
                ds_new.Name()))
        world.summaryAddOk('DividendStream[Hist]', ds_new.Oid(), 'CREATE')
    except Exception as e:
        failMsg = ('Unable to store historical dividend stream {0}.  '
                '{1}'.format(ds_new.Name(), e))
        world.logError(failMsg)
        world.summaryAddFail('DividendStream[Hist]', ds_new.Oid(), 'CREATE',
                reasons=[failMsg])
    return ds_new


def getMayBeArchivedAcmDividendStream(dsOid):

    aelDs = ael.DividendStream[dsOid]
    if not aelDs:
        return None
    if aelDs.archive_status == 0:
        acmDs = acm.FDividendStream[dsOid]  # direct look up since live
    else:
        acmDs = acm.Ael.AelToFObject(aelDs)  # will force acm cache pollution
    return acmDs


def find_last_historical_ds(orig_ds):
    """
    Search for a historical dividend stream with date_to = ael.BIG_DATE
    """
    qryStmt = (
            'SELECT seqnbr '
            'FROM dividend_stream '
            'WHERE original_ds_seqnbr = {0} '
                    'AND date_to = \'{1}\''.format(
            orig_ds.Oid(), ael.BIG_DATE.to_string(ael.DATE_ISO)))
    dsOids = [row[0] for row in ael.dbsql(qryStmt)[0]]
    if dsOids:
        ds = getMayBeArchivedAcmDividendStream(dsOids[0])
        return ds
    return None


def bigdate_ds_equal_live(dslive, dslatest):
    """
    Compares two dividend streams. First the dimensions are compared, then
    the values
    """
    if dslive.DividendsPerYear() != dslatest.DividendsPerYear():
        return 0
    if dslive.AnnualGrowth() != dslatest.AnnualGrowth():
        return 0
    if dslive.AdjustmentFactor() != dslatest.AdjustmentFactor():
        return 0
    if dslive.Instrument() != dslatest.Instrument():
        return 0

    sellive = dslive.Dividends()
    sellatest = dslatest.Dividends()

    if not len(sellatest) == len(sellive):
        return 0  # False = Not equal

    divlen = len(sellive)
    k = 0
    for i in range(len(sellive)):
        for j in range(len(sellatest)):
            if (sellive[i].PayDay() == sellatest[j].PayDay() and
                    sellive[i].RecordDay() == sellatest[j].RecordDay() and
                    sellive[i].ExDivDay() == sellatest[j].ExDivDay() and
                    sellive[i].TaxFactor() == sellatest[j].TaxFactor() and
                    sellive[i].Amount() == sellatest[j].Amount()):
                k = k + 1
    if not k >= divlen:
        return 0
    return 1


def copy_complete_ds(world, orig_ds, lastds, today):
    """
    Copy a dividend stream and commit it into the database
    """
    if not lastds:
        create_new_ds(world, orig_ds, today)
        return
    else:
        lastds.DateTo(today)
        lastds.Commit()
        create_new_ds(world, orig_ds, today)


def update_ds(world, ds, today):
    """
    Update a dividend stream and create a new if necessary
    """
    last_historical_ds = find_last_historical_ds(ds)
    if not last_historical_ds:
        copy_complete_ds(world, ds, None, today)
        return
    if bigdate_ds_equal_live(ds, last_historical_ds):
        world.logDebug('Nothing changed for dividend stream {0}'.format(
                ds.Name()))
        return
    if not ael.date(last_historical_ds.DateFrom()) == ael.date(today):
        copy_complete_ds(world, ds, last_historical_ds, today)
    else:
        lastHistDsName = last_historical_ds.Name()
        lastHistDsOid = last_historical_ds.Oid()
        ael.DividendStream[lastHistDsOid].delete()
        world.logInfo('    Deleted last historical dividend stream '
                '{0}'.format(lastHistDsName))
        world.summaryAddOk('DividendStream[Hist]', lastHistDsOid, 'DELETE')
        copy_complete_ds(world, ds, None, today)


def _findSelectedDsToStore(params):
    """
    Returns a list of acm dividend streams.
    """
    selectedDsList = []
    if params.stream_base:
        for ds in acm.FDividendStream.Select(''):
            if ds.Name() not in params.streams_excl:
                selectedDsList.append(ds)
    else:
        for name in params.streams_incl:
            if name not in params.streams_excl:
                ds = acm.FDividendStream[name]
                if ds:
                    selectedDsList.append(ds)
    return selectedDsList


def _sortAndFilterDsToStore(world, selectedDsList):
    """
    Return a sorted list of acm dividend streams (by oid), from the given
    dividend stream list.  Non-original and historically dated dividend streams
    are excluded.
    """
    sortedValidDsList = []
    for ds in sorted(selectedDsList, key=lambda ds: ds.Oid()):
        if ds.OriginalDividendStream():
            ignMsg = ('The dividend stream \'{0}\' ignored for selection '
                    'because it refer to another dividend stream as its '
                    'original.'.format(ds.Name()))
            world.summaryAddIgnore('DividendStream', ds.Oid(), 'SELECT',
                    reasons=[ignMsg])
            continue
        if ds.DateTo():
            ignMsg = ('The dividend stream \'{0}\' is ignored for selection '
                    'because its date_to field is already set.'.format(
                    ds.Name()))
            world.summaryAddIgnore('DividendStream', ds.Oid(), 'SELECT',
                    reasons=[ignMsg])
            continue
        # valid dividend stream to store
        world.summaryAddOk('DividendStream', ds.Oid(), 'SELECT')
        sortedValidDsList.append(ds)
    return sortedValidDsList


def update_all_ds(world, params, today=str(ael.date_today())):
    """
    Store dividend streams according to the settings in FVPSVariables.
    Main function.
    """
    world.logInfo('Start storing dividend streams...')
    selectedDsList = _findSelectedDsToStore(params)
    sortedValidDsList = _sortAndFilterDsToStore(world, selectedDsList)
    for ds in sortedValidDsList:
        update_ds(world, ds, today)
    world.logInfo('All dividend streams stored')

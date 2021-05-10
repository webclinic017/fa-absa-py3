""" Compiled: 2020-09-18 10:38:51 """

#__src_file__ = "extensions/vps/etc/FVPSCorrelationMatrix.py"
#----------------------------------------------------------------------------
#    (c) Copyright 2020 SunGard Front Arena. All rights reserved.
#----------------------------------------------------------------------------
"""----------------------------------------------------------------------------
MODULE
    FVPSCorrelationMatrix - Stores historical correlation matrices

DESCRIPTION
    Functionality for storing and deleting historical entities of
        type CorrelationMatrix.

        If there exist no historical correlation matrix, a new will always be
        created with
        date_from = today
        date_to = ael.BIG_DATE

        If there exist a historical correlation matrix with
        date_to = ael.BIG_DATE, this entity's date_to will be set to today and
        a new historical correlation matrix will be created with
        date_from = today and date_to = BIG_DATE.
----------------------------------------------------------------------------"""


import acm
import ael


import FBDPCommon


def delete_cm_in_list(world, cm_id_list, params):
    nr_deleted = 0
    failures = {}
    delete_id_list = cm_id_list[:]
    last_delete_length = len(delete_id_list) + 1

    while len(delete_id_list) > 0:
        if len(delete_id_list) == last_delete_length:
            # No cm deleted in last loop, stop looping
            for name in failures:
                oid, reason = failures[name]
                failMsg = 'Unable to delete {0}. {1}'.format(name, reason)
                world.summaryAddFail('CorrelationMatrix[Hist]', oid, 'DELETE',
                        reasons=[failMsg])
                world.logError(failMsg)
            return nr_deleted
        last_delete_length = len(delete_id_list)

        id_list = delete_id_list[:]
        for oid in id_list:
            cm = ael.CorrelationMatrix[oid]
            if not cm:
                world.logDebug('    CorrelationMatrix seqnbr=\'{0}\' in '
                        'Database not found in Cache'.format(oid))
                delete_id_list.remove(oid)
                continue
            name = cm.name

            live_cm = cm.original_cm_seqnbr

            if params.corr_matrices_base:
                if live_cm.name in params.corr_matrices_excl:
                    world.logDebug('    Found {0} in the exclusion list - '
                            'will not delete'.format(name))
                    delete_id_list.remove(oid)
                    continue
            else:
                if live_cm.name not in params.corr_matrices_incl:
                    world.logDebug('{0} is not in the inclusion list - '
                            'will not delete'.format(name))
                    delete_id_list.remove(oid)
                    continue
            # Note the summary will do duplication check, so do not need to
            # worry about oid duplication.
            world.summaryAddOk('CorrelationMatrix', live_cm.seqnbr, 'SELECT')
            world.summaryAddOk('CorrelationMatrix[Hist]', oid, 'SELECT')
            try:
                d_from = cm.date_from
                d_to = cm.date_to
                if not world.isInTestMode():
                    cm.delete()
                nr_deleted += 1
                delete_id_list.remove(oid)
                cm_id_list.remove(oid)
                if name in failures:
                    failures.pop(name)
                world.summaryAddOk('CorrelationMatrix[Hist]', oid, 'DELETE')
                world.logInfo('    Deleted {0} in the period '
                        'from {1} to {2}'.format(name, d_from, d_to))
            except:
                world.logDebug('    Unable to delete {0}, will attempt '
                        'again'.format(name))
                failures[name] = (oid, FBDPCommon.get_exception())
    return nr_deleted


def delete_all_cm_in_period(world, aelPeriodFirstDay, aelPeriodLastDay,
        params):
    """
    Deletes all correlation matrices with date_from >= first day &
    date_to <= last day.
    """
    assert isinstance(aelPeriodFirstDay, ael.ael_date), ('The '
            'aelPeriodFirstDay must be an ael_date.')
    assert isinstance(aelPeriodLastDay, ael.ael_date), ('The '
            'aelPeriodLastDay must be an ael_date.')
    aelDateToday = ael.date_today()
    world.logInfo('Deleting historical correlation matrices in the period '
            'from {0} to {1}.'.format(
            aelPeriodFirstDay.to_string(ael.DATE_ISO),
            aelPeriodLastDay.to_string(ael.DATE_ISO)))
    if aelPeriodLastDay >= aelDateToday:
        world.logInfo('Also deleting latest historical correlation matrices. '
                '(Period end date {0} on or beyond today {1})'.format(
                aelPeriodLastDay.to_string(ael.DATE_ISO),
                aelDateToday.to_string(ael.DATE_ISO)))
        aelPeriodLastDay = ael.BIG_DATE
    sql_query = ('select seqnbr from correlation_matrix where date_from >= '
            '\'{0}\' and date_to <= \'{1}\''.format(
            aelPeriodFirstDay.to_string(ael.DATE_ISO),
            aelPeriodLastDay.to_string(ael.DATE_ISO)))
    cm_id_list = FBDPCommon.get_result_in_list(ael.dbsql(sql_query))
    tot_nr_of_cm = len(cm_id_list)
    world.logInfo('Found {0} historical correlation matrices in the '
            'period.'.format(tot_nr_of_cm))
    nr_deleted = delete_cm_in_list(world, cm_id_list, params)
    world.logInfo('{0} historical correlation matrices deleted.'.format(
            nr_deleted))


def test_if_name_in_db(dsname):
    """
    Is the new correlation matrix name already in the database ?
    """
    name = dsname.replace("'", "''")
    sql_query = ('select count(1) from correlation_matrix where name = '
                 '\'{0}\''.format(name))
    for rtnSet in ael.dbsql(sql_query):
        for column in rtnSet:
            if int(column[0]) > 0:
                return dsname
    return None


def set_archive_flag_on_children(cm):

    for corr in cm.Correlations():
        corr.ArchiveStatus(1)
    for vol in cm.VolatilityElements():
        vol.ArchiveStatus(1)
    for bm in cm.Benchmarks():
        bm.ArchiveStatus(1)
    for point in cm.Points():
        point.ArchiveStatus(1)


def create_new_corr_matrix(world, corrmatrix, today):
    """
    Creates a new historical correlation matrix
    """
    cm_new = corrmatrix.Clone()
    cm_new.DateFrom(today)
    cm_new.DateTo(ael.BIG_DATE.to_string(ael.DATE_ISO))
    cm_new.OriginalCorrelationMatrix(corrmatrix)
    cm_new.Owner(corrmatrix.Owner())
    cm_new.ArchiveStatus(1)
    cm_new.Name = FBDPCommon.createNewNameByAddingDate(corrmatrix.Name(),
            today, test_if_name_in_db)
    set_archive_flag_on_children(cm_new)
    try:
        cm_new.Commit()
        world.logInfo('    Stored historical correlation matrix {0}'.format(
                cm_new.Name()))
        world.summaryAddOk('CorrelationMatrix[Hist]', cm_new.Oid(), 'CREATE')
    except Exception as e:
        failMsg = ('Unable to store historical correlation matrix {0}.  '
                '{1}'.format(cm_new.Name(), e))
        world.logError(failMsg)
        world.summaryAddFail('CorrelationMatrix[Hist]', cm_new.Oid(), 'CREATE',
                reasons=[failMsg])
    return cm_new


def getMayBeArchivedAcmCorrelationMatrix(cmOid):

    aelCm = ael.CorrelationMatrix[cmOid]
    if not aelCm:
        return None
    if aelCm.archive_status == 0:
        acmCm = acm.FCorrelationMatrix[cmOid]  # direct look up since live
    else:
        acmCm = acm.Ael.AelToFObject(aelCm)  # will force acm cache pollution
    return acmCm


def find_last_historical_matrix(origmatrix):
    """
    Finds a historical correlation matrix with date_to = ael.BIG_DATE
    """
    qryStmt = (
            'SELECT seqnbr '
            'FROM correlation_matrix '
            'WHERE original_cm_seqnbr = {0} '
                    'AND date_to = \'{1}\''.format(
            origmatrix.Oid(), ael.BIG_DATE.to_string(ael.DATE_ISO)))
    cmOids = [row[0] for row in ael.dbsql(qryStmt)[0]]
    if cmOids:
        cm = getMayBeArchivedAcmCorrelationMatrix(cmOids[0])
        return cm
    return None


def compare_volelement(live, hist):
    """
    Compares two volelements from two correlation matrices
    """
    return (live.RecType() == hist.RecType() and
            live.RecordAddress() == hist.RecordAddress() and
            live.Bucket_count() == hist.Bucket_count() and
            live.Bucket_unit() == hist.Bucket_unit() and
            live.Type() == hist.Type() and
            live.Volatility() == hist.Volatility())


def compare_correlation(live, hist):
    """
    Compares two correlations from two correlation matrices
    """
    return (live.RecordType0() == hist.RecordType0() and
            live.RecordAddress0() == hist.RecordAddress0() and
            live.Bucket0_count() == hist.Bucket0_count() and
            live.Bucket0_unit() == hist.Bucket0_unit() and
            live.RecordType1() == hist.RecordType1() and
            live.RecordAddress1() == hist.RecordAddress1() and
            live.Bucket1_count() == hist.Bucket1_count() and
            live.Bucket1_unit() == hist.Bucket1_unit() and
            live.Correlation() == hist.Correlation())


def compare_instrumentcorrelation(live, hist):
    """
    Compares two instrument correlations from two correlation matrices
    """
    return (live.InstrumentCorrelationValue() ==
                hist.InstrumentCorrelationValue())


def compare_benchmark(live, hist):
    """
    Compares two benchmarks from two correlation matrices
    """
    return (live.Instrument() == hist.Instrument())


def compare_point(live, hist):
    """
    Compares two points from two correlation matrices
    """
    return (live.Value() == hist.Value()
            and live.Point() == hist.Point())


def compare_elements(world, cmlive, cmhist, elements_str, compare_func,
        log_str):

    sellive = eval('cmlive.{0}'.format(elements_str))
    selhist = eval('cmhist.{0}'.format(elements_str))
    if not len(selhist) == len(sellive):
        world.logDebug('Correlation matrices \'{0}\' and \'{1}\' have '
                'different number of {2}s'.format(cmlive.Name(),
                cmhist.Name(), log_str))
        return False

    sellive.Sort()
    selhist.Sort()
    for i in range(len(sellive)):
        if not compare_func(sellive[i], selhist[i]):
            world.logDebug('Correlation matrices \'{0}\' and \'{1}\' have at '
                    'least one {2} that differs'.format(cmlive.Name(),
                    cmhist.Name(), log_str))
            return False
    return True


def bigdate_matrix_equal_live(world, cmlive, cmbd):
    """
    Compares two correlation matrices. First the dimensions are compared,
    then the values
    """
    if cmlive.DefaultValue() != cmbd.DefaultValue():
        world.logDebug('Correlation matrices \'{0}\' and \'{1}\' have '
                'different fallback correlation'.format(cmlive.Name(),
                cmbd.Name()))
        return False
    if not compare_elements(world, cmlive, cmbd, 'VolatilityElements()',
            compare_volelement, 'volatility element'):
        return False
    if cmlive.Type() == 'Instrument Correlation':
        if not compare_elements(world, cmlive, cmbd,
                'InstrumentCorrelations()',
                compare_instrumentcorrelation,
                'Instrument correlation element'):
            return False
    else:
        if not compare_elements(world, cmlive, cmbd, 'Correlations()',
                compare_correlation, 'correlation element'):
            return False
    if not compare_elements(world, cmlive, cmbd, 'Benchmarks()',
            compare_benchmark, 'benchmark'):
        return False
    if not compare_elements(world, cmlive, cmbd, 'Points()',
            compare_point, 'point'):
        return False
    return True  # Equal


def copy_complete_cm(world, origmatrix, lastcm, today):
    """
    Transfer all correlation and vol elements to a historical correlation
    matrix
    """
    if not lastcm:
        create_new_corr_matrix(world, origmatrix, today)
    else:
        lastcm.DateTo(today)
        lastcm.Commit()
        create_new_corr_matrix(world, origmatrix, today)


def update_correlation_matrix(world, cm, today):
    """
    Update an existing matrix and create a new historical if necessary
    """
    last_historical_cm = find_last_historical_matrix(cm)
    if not last_historical_cm:
        copy_complete_cm(world, cm, None, today)
        return
    if bigdate_matrix_equal_live(world, cm, last_historical_cm):
        world.logDebug('Nothing changed for correlation matrix {0}'.format(
                cm.Name()))
        return
    if not ael.date(last_historical_cm.DateFrom()) == ael.date(today):
        copy_complete_cm(world, cm, last_historical_cm, today)
    else:
        lastHistCmName = last_historical_cm.Name()
        lastHistCmOid = last_historical_cm.Oid()
        ael.CorrelationMatrix[lastHistCmOid].delete()
        world.logInfo('    Deleted last historical correlation matrix '
                '{0}'.format(lastHistCmName))
        world.summaryAddOk('CorrelationMatrix[Hist]', lastHistCmOid, 'DELETE')
        copy_complete_cm(world, cm, None, today)


def _findSelectedCmToStore(params):
    """
    Returns a list of acm correlation matrices
    """
    selectedCmList = []
    if params.correlation_base:
        for e in acm.FCorrelationMatrix.Select(
                'originalCorrelationMatrix = 0'):
            if not e.Name() in params.correlations_excl:
                selectedCmList.append(e)
    else:
        for name in params.correlations_incl:
            if name not in params.correlations_excl:
                cm = acm.FCorrelationMatrix[name]
                if cm:
                    selectedCmList.append(cm)
    return selectedCmList


def _sortAndFilterCmToStore(world, selectedCmList):
    """
    Return a sorted list of acm correlation matrices (by oid), from the given
    correlation matrices list.  Non-original and historically dated
    correlation matrices are excluded.
    """
    sortedValidCmList = []
    for cm in sorted(selectedCmList, key=lambda cm: cm.Oid()):
        if cm.OriginalCorrelationMatrix():
            ignMsg = ('The correlation matrix \'{0}\' is ignored for '
                    'selection because it refer to another correlation matrix '
                    'as its original.'.format(cm.Name()))
            world.summaryAddIgnore('CorrelationMatrix', cm.Oid(), 'SELECT',
                    reasons=[ignMsg])
            continue
        if cm.DateTo():
            ignMsg = ('The correlation matrix \'{0}\' is ignored for '
                    'selection because its date_to field is already '
                    'set.'.format(cm.Name()))
            world.summaryAddIgnore('CorrelationMatrix', cm.Oid(), 'SELECT',
                    reasons=[ignMsg])
            continue
        # valid correlation matrix to store
        world.summaryAddOk('CorrelationMatrix', cm.Oid(), 'SELECT')
        sortedValidCmList.append(cm)
    return sortedValidCmList


def update_all_cm(world, params, today):
    """
    Stores correlation matrices according to the settings in FVPSVariables.
    Main function.
    """
    world.logInfo('Start storing historical correlation matrices...')
    selectedCmList = _findSelectedCmToStore(params)
    sortedValidCmList = _sortAndFilterCmToStore(world, selectedCmList)
    for cm in sortedValidCmList:
        update_correlation_matrix(world, cm, today)
    world.logInfo('All correlation matrices stored')

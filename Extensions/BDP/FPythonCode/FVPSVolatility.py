""" Compiled: 2020-09-18 10:38:51 """

#__src_file__ = "extensions/vps/etc/FVPSVolatility.py"
#----------------------------------------------------------------------------
#    (c) Copyright 2020 SunGard Front Arena. All rights reserved.
#----------------------------------------------------------------------------
"""----------------------------------------------------------------------------
MODULE
        FVPSVolatility - Stores historical volatilities

DESCRIPTION
        Functionality for storing and deleting historical entities of
        type Volatility
----------------------------------------------------------------------------"""


import acm
import ael


import FBDPCommon


def is_referenced_by(vol, id_list):
    for oid in id_list:
        vol_temp = acm.FVolatilityStructure[oid]
        if vol_temp != None and vol_temp.UnderlyingStructure() != None:
            if vol_temp.UnderlyingStructure().Oid() == vol.Oid():
                return vol_temp.Name()
    return False


def delete_vol_in_list(world, vol_id_list, params):
    nr_deleted = 0
    failures = {}
    referenced_by_other = {}
    delete_id_list = vol_id_list[:]
    last_delete_length = len(delete_id_list) + 1

    while len(delete_id_list) > 0:
        if len(delete_id_list) == last_delete_length:
            # No vol deleted in last loop, stop looping
            for name in referenced_by_other:
                oid, ref_name = referenced_by_other[name]
                failMsg = 'Volatility {0} is referenced by {1}.'.format(
                        name, ref_name)
                world.summaryAddFail('VolatilityStructure[Hist]', oid,
                        'DELETE', reasons=[failMsg])
                world.logError(failMsg)
            for name in failures:
                oid, reason = failures[name]
                failMsg = 'Unable to delete {0}. {1}'.format(name, reason)
                world.summaryAddFail('VolatilityStructure[Hist]', oid,
                        'DELETE', reasons=[failMsg])
                world.logError(failMsg)
            return nr_deleted
        last_delete_length = len(delete_id_list)

        id_list = delete_id_list[:]
        for oid in id_list:
            vol = acm.FVolatilityStructure[oid]
            if not vol:
                world.logDebug('    Volatility seqnbr=\'{0}\' in Database not '
                        'found in Cache'.format(oid))
                delete_id_list.remove(oid)
                continue
            name = vol.Name()

            live_vol = vol.OriginalStructure()

            if params.volatility_base:
                if live_vol.Name() in params.volatilities_excl:
                    world.logDebug('    Found {0} in the exclusion list - '
                            'will not delete'.format(name))
                    delete_id_list.remove(oid)
                    continue
            else:
                if live_vol.Name() not in params.volatilities_incl:
                    world.logDebug('    {0} not in the inclusion list - '
                            'will not delete'.format(name))
                    delete_id_list.remove(oid)
                    continue
            # Note the summary will do duplication check, so do not need to
            # worry about oid duplication.
            world.summaryAddOk('VolatilityStructure', live_vol.Oid(),
                    'SELECT')
            world.summaryAddOk('VolatilityStructure[Hist]', oid, 'SELECT')
            ref_name = is_referenced_by(vol, vol_id_list)
            if not ref_name:
                try:
                    if not world.isInTestMode():
                        ael.Volatility[oid].delete()
                    nr_deleted += 1
                    delete_id_list.remove(oid)
                    vol_id_list.remove(oid)
                    if name in failures:
                        failures.pop(name)
                    if name in referenced_by_other:
                        referenced_by_other.pop(name)
                    world.summaryAddOk('VolatilityStructure[Hist]', oid,
                            'DELETE')
                    world.logInfo('    Deleted {0}'.format(name))
                except:
                    world.logDebug('    Unable to delete {0}, will attempt '
                            'again'.format(name))
                    failures[name] = (oid, FBDPCommon.get_exception())
            else:
                referenced_by_other[name] = (oid, ref_name)
                world.logDebug('    Defer to delete {0} '
                        '(referenced by another).'.format(name))
    return nr_deleted


def delete_all_vol_of_a_day(world, aelDelDate, params):
    """
    Delete all historical volatilities on a specified date. The volatilities
    lowest in the hierarchy will be deleted first
    """
    assert isinstance(aelDelDate, ael.ael_date), ('The aelDelDate must be an '
            'ael_date.')
    world.logInfo('Deleting historical volatilities on date {0}.'.format(
            aelDelDate.to_string()))
    sql_query = ('select seqnbr from volatility where historical_day = '
            '\'{0}\''.format((aelDelDate.to_string(ael.DATE_ISO))))
    vol_id_list = FBDPCommon.get_result_in_list(ael.dbsql(sql_query))
    tot_nr_volatilities = len(vol_id_list)
    world.logInfo('Found {0} historical volatilities on this date.'.format(
            tot_nr_volatilities))
    nr_deleted = delete_vol_in_list(world, vol_id_list, params)
    world.logInfo('{0} historical volatilities deleted.'.format(nr_deleted))

def test_if_name_in_db(volname):
    """
    Is the new volatility name already in the database ?
    """
    name = volname.replace("'", "''")
    sql_query = ('select count(1) from volatility where vol_name = '
            '\'{0}\''.format(name))
    for dset in ael.dbsql(sql_query):
        for column in dset:
            if int(column[0]) > 0:
                return volname
    return None

def _commit(vol_new, world):
    try:
        vol_new.Commit()
        world.logInfo('    Stored historical volatility {0}'.format(
                vol_new.Name()))
        world.summaryAddOk('VolatilityStructure[Hist]', vol_new.Oid(),
                'CREATE')
        world.summaryAddOk('VolatilityStructure[Hist]', vol_new.Oid(),
                'ARCHIVE')
        return vol_new
    except Exception as e:
        failMsg = ('Unable to store historical volatility {0}.  '
                '{1}'.format(vol_new.Name(), e))
        world.logError(failMsg)
        world.summaryAddFail('VolatilityStructure[Hist]', vol_new.Oid(),
                'CREATE', reasons=[failMsg])
        world.summaryAddFail('VolatilityStructure[Hist]', vol_new.Oid(),
                'ARCHIVE', reasons=[failMsg])
        return None


def store_volatility(world, vol, today, vol_mappings,
                     calculate, currentVolList):
    """
    Stores a volatility. Underlying volatilities should already been stored
    """
    last_hist_vol = find_last_historical_vol(vol, today)
    if last_hist_vol:
        return (last_hist_vol, False)
    # Need to calculate before committing
    if calculate:
        try:
            world.logInfo('    Recalculating volatility '
                    'structure \'{0}\'.'.format(
                    vol.Name()))
            failMsg = ''
            calcRtn = True
            if FBDPCommon.useNewCalibrationFramework('FVPSVariables') \
               and FBDPCommon.supportNewCalibrationFramework(vol):
                calcRtn, failMsg = \
                    FBDPCommon.calibrateVolatility(vol)
            else:
                vol.CalcImpliedVolatilities()

            if failMsg != '':
                world.logError(failMsg)

            if not calcRtn:
                world.summaryAddFail('VolatilityStructure[Hist]',
                    vol.Oid(), 'RECALCULATE',
                    reasons=[failMsg])
                return (None, False)
            else:
                world.summaryAddOk('VolatilityStructure[Hist]',
                    vol.Oid(), 'RECALCULATE')
                world.logDebug('    Recalculated.')

        except Exception as e:
            failMsg = ('Failed to recalculate volatility '
                    'structure \'{0}\'.  {1}'.format(
                    vol.Name(), e))
            world.summaryAddFail('VolatilityStructure[Hist]',
                    vol.Oid(), 'RECALCULATE',
                    reasons=[failMsg])
            world.logError(failMsg)
            return (None, False)

    # Create new volatility
    vol_new = vol.Clone()
    vol_new.HistoricalDay(today)
    vol_new.OriginalStructure(vol)
    vol_new.Owner(vol.Owner())
    vol_new.ArchiveStatus(1)
    vol_new.Name(FBDPCommon.createNewNameByAddingDate(vol.Name(), today,
            test_if_name_in_db, maxLen=30, nameExistList=currentVolList))

    # Map underlying yield_curve to a historical
    if vol_new.UnderlyingStructure():
        new_underlying = vol_mappings[vol_new.UnderlyingStructure()]
        vol_new.UnderlyingStructure(new_underlying)

    if not vol_new:
        return (None, False)
    return (vol_new, True)

def archive_volatility(world, vol_new):

    # Archive child tables
    el_list = [vol_new.Points(), vol_new.Skews()]
    for sub_list in el_list:
        for el in sub_list:
            el.ArchiveStatus(1)

    world.logDebug('Archiving new volatility surface {0}.'.format(
        vol_new.Name()))
    vol_new = _commit(vol_new, world)
    if not vol_new:
        return (None, False)

    return (vol_new, True)


def getMayBeArchivedAcmVolatilityStructure(volOid):

    aelVol = ael.Volatility[volOid]
    if not aelVol:
        return None
    if aelVol.archive_status == 0:
        acmVol = acm.FVolatilityStructure[volOid]  # direct look up since live
    else:
        acmVol = acm.Ael.AelToFObject(aelVol)  # will force acm cache pollution
    return acmVol


def find_last_historical_vol(orig_vol, today):
    """
    Find the corresponding volatility with historical_day = today
    """
    qryStmt = (
            'SELECT seqnbr '
            'FROM volatility '
            'WHERE original_vol_seqnbr = {0} '
                    'AND historical_day = \'{1}\''.format(
            orig_vol.Oid(), ael.date(today).to_string(ael.DATE_ISO)))
    volOids = [row[0] for row in ael.dbsql(qryStmt)[0]]
    if volOids:
        vol = getMayBeArchivedAcmVolatilityStructure(volOids[0])
        return vol
    return None


def build_dependency_structure(name_dic, vol):
    if vol in name_dic:
        return
    if vol.UnderlyingStructure():
        name_dic[vol] = [vol.UnderlyingStructure()]
        build_dependency_structure(name_dic, vol.UnderlyingStructure())
    else:
        name_dic[vol] = []


def update_volatilities(world, vol_list, today, calculate):
    """
    First build a dependency volatility structure, then call func
    store_volatility for all volatilities in correct order.  All underlying
    volatilities to volatility X must be stored before storing X.
    """
    # Some of volatility structure types should be skiped from calculation
    vol_struc_types_to_skip = ('Malz',)
    vol_dep_dic = {}
    for vol in vol_list:
        build_dependency_structure(vol_dep_dic, vol)
    for vol in list(vol_dep_dic.keys()):
        if vol.HistoricalDay():
            world.logError('You tried to make a copy of a historical '
                    'volatility {0}.  The execution will be stopped.'.format(
                    vol.Name()))
            for dep_vol, dep_list in list(vol_dep_dic.items()):
                if vol in dep_list:
                    world.logInfo('Volatility {0} is dependent of {1}'.format(
                            dep_vol.Name(), vol.Name()))
            return 0
    if len(vol_dep_dic) > len(vol_list):
        world.logDebug('Underlying volatilities will also be stored')

    nr_updated = 0
    nr_calculated = 0
    error_list = []
    vol_mappings = {}
    last_store_len = len(vol_dep_dic) + 1
    new_volList = []
    while(len(vol_dep_dic) > 0):
        if len(vol_dep_dic) == last_store_len:
            # No volatility stored in last loop, stop looping
            world.logError('All volatilities could not be stored')
            break
        last_store_len = len(vol_dep_dic)
        vol_stored_list = []
        # Only store volatilities with empty dependency list
        # (have to wait for other volatilities to be stored first)
        for vol, dep_list in list(vol_dep_dic.items()):
            if len(dep_list) == 0:
                vol_dep_dic.pop(vol)
                world.logDebug('Storing volatility {0}'.format(vol.Name()))
                if vol.StructureType() not in vol_struc_types_to_skip:
                    new_vol, updated = store_volatility(world, vol, today,
                            vol_mappings, calculate,
                            [newVol.Name() for newVol in new_volList])
                else:
                    new_vol, updated = store_volatility(world, vol, today,
                            vol_mappings, False,
                            [newVol.Name() for newVol in new_volList])
                if new_vol:
                    new_volList.append(new_vol)
                    vol_mappings[vol] = new_vol
                    vol_stored_list.append(vol)
                    if updated:
                        world.logInfo('{0} stored'.format(vol.Name()))
                        nr_updated += 1
                    else:
                        logmsg = ('Volatility {0} already stored'.format(
                                vol.Name()))
                        if vol in vol_list:
                            world.logInfo(logmsg)
                        else:
                            world.logDebug(logmsg)
                    if calculate:
                        nr_calculated += 1
                else:
                    world.logError('Unable to make volatility {0} '
                            'historical.  Check your logfile.'.format(
                            vol.Name()))
                    error_list.append(vol)
        # Remove already stored volatilities from other volatilities
        # dependency list
        for vol, dep_list in list(vol_dep_dic.items()):
            for stored_vol in vol_stored_list:
                while dep_list.count(stored_vol) > 0:
                    dep_list.remove(stored_vol)

    #archive the newly stored volatilities
    for newVol in new_volList:
        archive_volatility(world, newVol)

    for vol, dep_list in list(vol_dep_dic.items()):
        dep_names = [dep.Name() for dep in dep_list]
        world.logDebug('Ignored volatility \'{0}\', which depends on '
                'volatility \'{1}\'.'.format(vol.Name(), dep_names))
    nr_errors = len(error_list)
    if nr_errors > 0:
        world.logInfo('Failed to update {0} volatilities'.format(nr_errors))
    nr_ignored = len(vol_dep_dic)
    if nr_ignored > 0:
        world.logInfo('Ignored {0} volatilities due to the failure of '
                'storing underlying volatilities first.'.format(nr_ignored))
    if calculate:
        world.logInfo('Recalculated {0} volatilities'.format(nr_calculated))
    return nr_updated


def _findSelectedVolToStore(params):
    """
    Returns a list of acm yield curves.
    """
    selectedVolList = []
    if params.volatility_base:
        for vol in acm.FVolatilityStructure.Select(''):
            if vol.Name() not in params.volatilities_excl:
                selectedVolList.append(vol)
    else:
        for volName in params.volatilities_incl:
            if volName not in params.volatilities_excl:
                vol = acm.FVolatilityStructure[volName]
                if vol:
                    selectedVolList.append(vol)
    return selectedVolList


def _sortAndFilterVolToStore(world, selectedVolList):
    """
    Return a sorted list of acm volatility structures (by oid), from the given
    list of volatility structures.  Non-original and historically dated
    volatility structures are excluded.
    """
    sortedValidVolList = []
    for vol in sorted(selectedVolList, key=lambda vol: vol.Oid()):
        if vol.OriginalVolatility():
            ignMsg = ('The volatility \'{0}\' ignored for selection '
                    'because it refer to another volatility as its '
                    'original.'.format(vol.Name()))
            world.summaryAddIgnore('VolatilityStructure', vol.Oid(), 'SELECT',
                    reasons=[ignMsg])
            continue
        if vol.HistoricalDay():
            ignMsg = ('The volatility \'{0}\' is ignored for selection '
                    'because its historical_day field is already set.'.format(
                    vol.Name()))
            world.summaryAddIgnore('VolatilityStructure', vol.Oid(), 'SELECT',
                    reasons=[ignMsg])
            continue
        world.summaryAddOk('VolatilityStructure', vol.Oid(), 'SELECT')
        sortedValidVolList.append(vol)
    return sortedValidVolList


def update_all_vol(world, params, today):
    """
    Store historical volatilities according to the settings in FVPSVariables.
    Main function.
    """
    delete_all_vol_of_a_day(world, ael.date(today), params)
    world.logInfo('Start storing historical volatilities')
    selectedVolList = _findSelectedVolToStore(params)
    sortedValidVolList = _sortAndFilterVolToStore(world, selectedVolList)
    nr_stored = update_volatilities(world, sortedValidVolList, today,
                params.calculate)
    world.logInfo('Stored {0} volatilities.'.format(nr_stored))

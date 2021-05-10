""" Compiled: 2020-09-18 10:38:51 """

#__src_file__ = "extensions/expiration/etc/FNewExpirationUtility.py"
#----------------------------------------------------------------------------
#    (c) Copyright 2020 SunGard Front Arena. All rights reserved.
#----------------------------------------------------------------------------
import acm
import ael


import FBDPCommon
import FBDPInstrument
import collections
import FNewExpirationObjRefHandler as DefaultObjRefHandler

Oplet = collections.namedtuple('Oplet', 'opTyp recTyp oid')

ENTITY_CLASSES_ALLOWING_ADD_INFO_SPEC = [
    'Account', 'AccountingInstruction', 'Agreement', 'Book', 'CashFlow',
    'CollateralAggrement', 'Confirmation', 'Contact', 'CorpAction',
    'CurrencyPair', 'Dividend', 'DividendEstimate', 'Instrument',
    'Journal', 'Leg', 'ListNode', 'OwnOrder', 'Party', 'Payment',
    'Payment', 'Portfolio', 'PriceDefinition', 'RiskFactorSpecHeader',
    'Settlement', 'TAccount', 'TextObject', 'TimeSeriesSpec', 'Trade',
    'TradeFilter', 'Treatment', 'User', 'Volatility', 'YieldCurve'
]

OBJECTS_ALLOWING_REF_CHECK_SUPPRESSION = {}

AGGREGATE_TRD_TYPE = 12

def performCommit(obj, log):
    commit = getattr(obj, 'commit', getattr(obj, 'Commit', None))
    if not log.isInTestMode():
        commit()

def performDelete(obj, log):
    delete = getattr(obj, 'delete', getattr(obj, 'Delete', None))
    if not log.isInTestMode():
        delete()

def performTransaction(log, func, *args, **kwargs):
    _transaction = True
    try:
        ael.begin_transaction()
        func(*args, **kwargs)
        if log.isInTestMode():
            ael.abort_transaction()
        else:
            ael.commit_transaction()

        _transaction = False
    except:
        if _transaction:
            ael.abort_transaction()

        raise

    return
def GetObjectToBeDeletedOrArchived():
    includeList = [
        'IntradayPrice', 'ListLeaf', 'MtmValue',
        'OrderBook', 'OwnOrder', 'OwnOrderLink', 'PriceDefinition',
        'PriceLinkDefinition', 'MatchLot', 'TradeAlias',
        'QuoteParameter', 'CombinationLink',
        'BusinessEventTrdLink'
    ]

    try:
        import FBDPHook
        hook = getattr(FBDPHook, 'objects_to_be_deleted_or_archived')
        includeList = hook()
    except ImportError:
        pass
    except AttributeError:
        pass
    return includeList

objToBeDeletedOrArchived = GetObjectToBeDeletedOrArchived()

def FindObjReferences(
    aelObj, resultlist, includelist, log, action, RefHandleFuncMap
):

    ref_list = aelObj.reference_in()
    if not ref_list:
        return

    for ref in ref_list:

        refId = FBDPCommon.getPrimaryKey(ref)
        aelObjId = FBDPCommon.getPrimaryKey(aelObj)
        can_ignore = refId in OBJECTS_ALLOWING_REF_CHECK_SUPPRESSION.get(
            ref.record_type, []
        )

        if ref.record_type in RefHandleFuncMap:
            result = RefHandleFuncMap[ref.record_type](
                aelObj, ref, resultlist, log
            )
            if result or can_ignore:
                continue
            else:
                refId = FBDPCommon.getPrimaryKey(ref)
                raise Exception(
                    'Error on handling the reference object type =%s, id =%s '
                    'that linked to %s with Id %s' % (
                        ref.record_type, refId, aelObj.record_type, aelObjId
                    )
                )

        if (ref in aelObj.children()) or (aelObj == ref.parent()) \
           or (ref.record_type in includelist):
            FindObjReferences(
                ref, resultlist, includelist, log, action, RefHandleFuncMap
            )
            if action == 'Delete':
                if (ref not in aelObj.children()) and (aelObj != ref.parent()):
                    resultlist.append(ref)
            else:
                resultlist.append(ref)
        elif not can_ignore:
            if action == 'Delete':
                raise Exception(
                    'Unexpected reference object type =%s, id =%s '
                    'linked to %s with Id %s' % (
                        ref.record_type, refId, aelObj.record_type, aelObjId
                    )
                )

            else:
                msg = (
                    'Ignored reference object type =%s, id =%s '
                    'linked to %s with Id %s' % (
                        ref.record_type, refId, aelObj.record_type, aelObjId
                    )
                )
                log.logWarning(msg)

    if aelObj.record_type in ENTITY_CLASSES_ALLOWING_ADD_INFO_SPEC:
        addinfo = aelObj.additional_infos()
        for info in addinfo:
            resultlist.append(info)
    return

def GetOpsToArchiveTrd(trd, log):

    aelTrd = FBDPCommon.acm_to_ael(trd)
    reflist = []
    opList = []
    RefHandleFuncMap = {
        'Trade': DefaultObjRefHandler.HandleTrdReferenceOnArchive,
        'BusinessEventTrdLink': DefaultObjRefHandler.ArcDeArcExAssignBusiEvt
    }
    FindObjReferences(
        aelTrd, reflist, objToBeDeletedOrArchived,
        log, 'Archive', RefHandleFuncMap
    )
    for refObj in reflist:
        refObjPrimaryKey = FBDPCommon.getPrimaryKey(refObj)
        opList.append(Oplet('Archive', refObj.record_type, refObjPrimaryKey))

    opList.append(Oplet('Archive', 'Trade', trd.Oid()))

    return opList

def GetOpsToArchiveInstrument(instId, log):

    aelInst = ael.Instrument[instId]
    reflist = []
    opList = []
    RefHandleFuncMap = {'Trade': DefaultObjRefHandler.IgnoreTrdReference}
    FindObjReferences(
        aelInst, reflist, objToBeDeletedOrArchived,
        log, 'Archive', RefHandleFuncMap
    )
    for refObj in reflist:
        refObjPrimaryKey = FBDPCommon.getPrimaryKey(refObj)
        opList.append(Oplet('Archive', refObj.record_type, refObjPrimaryKey))

    opList.append(Oplet('Archive', 'Instrument', instId))
    return opList

def DeArchiveAggregateTrd(id, log):

    numTrds = ael.dbsql(
        'select count(trdnbr) from trade where trdnbr = %s and type = %s'
        % (id, AGGREGATE_TRD_TYPE)
    )
    if not numTrds:
        errorMsg = 'No archived aggregate trade %s found in the DB' % id
        log.summaryAddFail('Trade', id, 'DE-ARCHIVE', [errorMsg])
        return

    ael.dbsql(
        'update trade set archive_status = 0, aggregate_trdnbr = NULL '
        'where trdnbr = %s and type = %s' % (id, AGGREGATE_TRD_TYPE)
    )
    log.summaryAddOk('Trade', id, 'DE-ARCHIVE')

    payments = FBDPCommon.get_result_in_list(
        ael.dbsql('select paynbr from payment where trdnbr = %s' % id)
    )
    ael.dbsql('update payment set archive_status = 0 where trdnbr = %s' % id)
    for pid in payments:
        log.summaryAddOk('Payment', pid, 'DE-ARCHIVE')

def DeleteAggregateTrd(id, log):

    try:
        numTrds = ael.dbsql(
            'select count(trdnbr) from trade where trdnbr = %s '
            'and type = %s and archive_status = 1' % (id, AGGREGATE_TRD_TYPE)
        )
        if not numTrds:
            errorMsg = 'No archived aggregate trade %s found in the DB' % id
            log.summaryAddFail('Trade', id, 'DELETE', [errorMsg])
            return False

        aggregatedTrds = ael.dbsql(
            'select trdnbr from trade where aggregate_trdnbr  = %s' % id
        )[0]

        for trdId in aggregatedTrds:
            #Delete the aggregated trade
            DeleteTrade(trdId[0], 'Trade', log)

        #Delete the archived aggregate trade. As the archived aggregate trade
        #is not visible in ael, we have to use the dbsql to delete it.
        ael.dbsql('delete from payment where trdnbr = %s' % id)
        ael.dbsql('delete from trade where trdnbr = %s' % id)
        log.summaryAddOk('Trade', id, 'DELETE')

    except Exception as ex:
        errorMsg = str(ex)
        log.summaryAddFail(type, id, 'Trade', [errorMsg])
        return False

    return True

def DeArchiveTrd(id, log):
    try:
        aelobj = ael.Trade[id]

        if not aelobj:
            DeArchiveAggregateTrd(id, log)
            return

        ref_list = []

        # For now, we don't want to de-archive anything that
        # reference to the trade.
        RefHandleFuncMap = {
            'Trade':
                DefaultObjRefHandler.IgnoreTrdReference,
            'BusinessEventTrdLink':
                DefaultObjRefHandler.ArcDeArcExAssignBusiEvt
        }
        FindObjReferences(
            aelobj, ref_list, objToBeDeletedOrArchived,
            log, 'DeArchive', RefHandleFuncMap
        )
        for ref in ref_list:
            oid = FBDPCommon.getPrimaryKey(ref)
            DeArchiveObj(oid, ref.record_type, log)

        clone_ael = aelobj.clone()
        if FBDPCommon.has_attr(clone_ael, 'archive_status'):
            clone_ael.archive_status = 0

        if FBDPCommon.has_attr(clone_ael, 'aggregate_trdnbr'):
            clone_ael.aggregate_trdnbr = 0

        performCommit(clone_ael, log)
        log.summaryAddOk('Trade', id, 'DE-ARCHIVE')

    except Exception as ex:
        errorMsg = str(ex)
        log.summaryAddFail(type, id, 'DE-ARCHIVE', [errorMsg])
        raise ex

    return

def DeArchiveInst(id, log):
    try:
        aelobj = ael.Instrument[id]
        if not aelobj:
            msg = 'No ael object for Instrument id =%s' % id
            log.logError(msg)
            return

        ref_list = []
        RefHandleFuncMap = {'Trade': DefaultObjRefHandler.IgnoreTrdReference}
        FindObjReferences(
            aelobj, ref_list, objToBeDeletedOrArchived,
            log, 'DeArchive', RefHandleFuncMap
        )
        for ref in ref_list:
            oid = FBDPCommon.getPrimaryKey(ref)
            DeArchiveObj(oid, ref.record_type, log)

        clone_ael = aelobj.clone()
        if FBDPCommon.has_attr(clone_ael, 'archive_status'):
            clone_ael.archive_status = 0

        performCommit(clone_ael, log)
        log.summaryAddOk('Instrument', id, 'DE-ARCHIVE')

    except Exception as ex:
        errorMsg = str(ex)
        log.summaryAddFail(type, id, 'DE-ARCHIVE', [errorMsg])
        raise ex

    return

def DeArchiveObj(id, type, log):

    try:
        clone_ael = eval('ael.%s[%s]' % (type, id)).clone()
        if FBDPCommon.has_attr(clone_ael, 'archive_status'):
            clone_ael.archive_status = 0

        performCommit(clone_ael, log)

        log.summaryAddOk(type, id, 'DE-ARCHIVE')

    except Exception as ex:
        errorMsg = str(ex)
        log.summaryAddFail(type, id, 'DE-ARCHIVE', [errorMsg])
        raise ex

    return

def ArchiveObj(id, type, log, cpTrd=None):

    try:
        clone_ael = eval('ael.%s[%s]' % (type, id)).clone()
        if FBDPCommon.has_attr(clone_ael, 'archive_status'):
            clone_ael.archive_status = 1

        if FBDPCommon.has_attr(clone_ael, 'aggregate_trdnbr') and cpTrd:
            clone_ael.aggregate_trdnbr = cpTrd.trdnbr

        if type == 'Trade' and cpTrd and clone_ael.trx_trdnbr == 0:
            if FBDPCommon.is_acm_object(cpTrd):
                cpTrd = FBDPCommon.acm_to_ael(cpTrd)
            clone_ael.trx_trdnbr = cpTrd.trdnbr

        performCommit(clone_ael, log)
        log.summaryAddOk(type, id, 'ARCHIVE')

    except Exception as ex:
        errorMsg = str(ex)
        log.summaryAddFail(type, id, 'ARCHIVE', [errorMsg])
        raise ex

def DeleteTrade(id, type, log):
    try:
        aelobj = ael.Trade[id]
        if not aelobj:
            DeleteAggregateTrd(id, log)
            return

        mirror_id = 0
        if aelobj.mirror_trdnbr:
        #Ignore the mirror trade, as it will be deleted by the original trd.
            if aelobj.mirror_trdnbr.trdnbr == aelobj.trdnbr:
                return
            else:
                mirror_id = aelobj.mirror_trdnbr.trdnbr

        ref_list = []
        RefHandleFuncMap = {
            'Trade': DefaultObjRefHandler.ErrorOnTrdReference,
            'BusinessEventTrdLink': DefaultObjRefHandler.DeleteExAssignBusiEvt
        }
        FindObjReferences(
            aelobj, ref_list, objToBeDeletedOrArchived,
            log, 'Delete', RefHandleFuncMap
        )
        for ref in ref_list:
            oid = FBDPCommon.getPrimaryKey(ref)
            DeleteObj(oid, ref.record_type, log)

        DeleteObj(id, 'Trade', log)

        if mirror_id:
            log.summaryAddOk(type, mirror_id, 'DELETE')

    except Exception as ex:
        errorMsg = str(ex)
        log.summaryAddFail(type, id, 'DELETE', [errorMsg])
        raise ex

    return

def DeleteInstrument(id, type, log):
    try:
        aelobj = ael.Instrument[id]
        if not aelobj:
            msg = 'No ael object for Instrument id =%s' % id
            log.logError(msg)
            return

        ref_list = []
        RefHandleFuncMap = {'Trade': DefaultObjRefHandler.ErrorOnTrdReference}
        FindObjReferences(
            aelobj, ref_list, objToBeDeletedOrArchived,
            log, 'Delete', RefHandleFuncMap
        )
        for ref in ref_list:
            oid = FBDPCommon.getPrimaryKey(ref)
            DeleteObj(oid, ref.record_type, log)

        DeleteObj(id, 'Instrument', log)

    except Exception as ex:
        errorMsg = str(ex)
        log.summaryAddFail(type, id, 'DELETE', [errorMsg])
        raise ex

    return

def DeleteObj(id, type, log):

    try:
        aelObj = eval('ael.%s[%s]' % (type, id))
        children_objs = aelObj.children()
        clone_ael = aelObj.clone()
        performDelete(clone_ael, log)
        for c in children_objs:
            c_id = FBDPCommon.getPrimaryKey(c)
            log.summaryAddOk(c.record_type, c_id, 'DELETE')

        performCommit(clone_ael, log)
        log.summaryAddOk(type, id, 'DELETE')

    except Exception as ex:
        errorMsg = str(ex)
        log.summaryAddFail(type, id, 'DELETE', [errorMsg])
        raise ex
    return

def CreateTrade(t, log):
    try:

        oid = FBDPCommon.getPrimaryKey(t)
        isAcm = FBDPCommon.is_acm_object(t)
        if isAcm:
            ins = t.Instrument()
            name = ins.Name()
            tradeable = FBDPInstrument.isTradable(t.Instrument())
            counterparty = t.Counterparty() and t.Counterparty().Name()
            acquirer = t.Acquirer() and t.Acquirer().Name()
            trader = t.Trader() and t.Trader().Name()
            status = t.Status()
        else:
            ins = t.insaddr
            name = ins.insid
            tradeable = FBDPInstrument.isTradable(t.insaddr)
            counterparty = (
                t.counterparty_ptynbr and t.counterparty_ptynbr.ptynbr
            )
            acquirer = t.acquirer_ptynbr and t.acquirer_ptynbr.ptyid
            trader = t.trader_usrnbr and t.trader_usrnbr.userid
            status = t.status

        if not tradeable:
            log.logError('Instrument %s is not tradable' % name)
            return

        # TO validate acquirer
        #if status != "Simulated":
        #    if (not self.validateAcquirer(acquirer, t, oid) or
        #        not self.validateCounterparty(counterparty, t, oid)):
        #        return

        # TO validate trader
        #self.__validateTrader(trader, t, oid)
        #self.commitOrRollback(t, oid, attribs, op)
        performCommit(t, log)
        log.summaryAddOk('Trade', t.trdnbr, 'CREATE')

    except Exception as ex:
        errorMsg = str(ex)
        log.logError(errorMsg)
        log.summaryAddFail('Trade', t.trdnbr, 'CREATE', errorMsg)
        raise ex

def isInstArchived(id):
    status = ael.dbsql(
        'select archive_status from instrument i where i.insaddr = %s' % id
    )[0]
    if len(status) == 0 or status[0][0] == 0:
        return False
    else:
        return True

def isInstTraded(insId, log):
    nrOfTrades = len(ael.dbsql('select t.trdnbr from trade t where '
            't.insaddr = {0}'.format(insId))[0])
    if nrOfTrades:
        return True

    return isInstTradedDerivativeOrCombination(insId, log)

def isInstTradedDerivativeOrCombination(insId, log):
    for link in acm.FCombInstrMap.Select('instrument=%d' % insId):
        if isInstTraded(link.Combination().Oid(), log):
            log.logInfo('Instrument %s is a member of a traded Combination.'
                % insId)
            return True

    underlyingIds = ael.asql('select i.insaddr from instrument i where '
            'i.und_insaddr = {0}'.format(insId))
    references = [acm.FInstrument[e[0]] for e in underlyingIds[1][0]]
    legInsIds = ael.asql('select i.insaddr from instrument i, leg l '
            'where (l.insaddr = i.insaddr and '
            'l.credit_ref = {0})'.format(insId))
    references.extend([acm.FInstrument[e[0]] for e in legInsIds[1][0]])
    for der in references:
        if isInstTraded(der.Oid(), log):
            log.logInfo('Instrument %s has a traded derivative %s.'
                % (insId, der.Oid()))
            return True

    return False

def getInstId(name, log):

    if FBDPCommon.is_acm_object(name):
        return name.Oid()

    elif isinstance(name, str):
        inst = ael.Instrument[name]
        return inst.insaddr

    else:
        typeStr = type(name)
        log.logError('Unexpected type on instruments field %s' % typeStr)
        return None

def DoesInstExisted(id):
    if FBDPCommon.is_acm_object(id):
        return True

    return acm.FInstrument[id] or ael.Instrument[id]

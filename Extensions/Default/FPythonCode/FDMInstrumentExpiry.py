""" Compiled: 2020-09-18 10:38:51 """

#__src_file__ = "extensions/expiration/etc/FDMInstrumentExpiry.py"
#----------------------------------------------------------------------------
#    (c) Copyright 2020 SunGard Front Arena. All rights reserved.
#----------------------------------------------------------------------------
"""----------------------------------------------------------------------------
MODULE
        FDMInstrumentExpiry.py - Script for maintenance when instruments
        expire.

DESCRIPTION
        This module performs instrument maintenance such as clearing the
        listleafs, orderbooks, price definitions and own orders.
        If wanted the expired instrument could also be deleted or archived.

ENDDESCRIPTION
----------------------------------------------------------------------------"""


import re
import time


import acm
import ael


import traceback


import FBDPCommon
import FBDPRollback
import FBDPInstrument
import FBDPCalculatePosition
from FBDPValidation import FBDPValidate
import FExpirationAction
from FBDPCurrentContext import Summary
from FBDPCurrentContext import Logme


# -----------------------------------------------------------------------------
# Special extern_id1 and extern_id2 for the cash-posting and rollout instrument
# so that customer could change the id. Don't change this below
# -----------------------------------------------------------------------------


# Default name on the cash positing instrument
CSP = 'CashPosting'


CSP_EXTID1 = '##(Fastolph Smallburrows)##'
CSP_EXTID2 = '##(of Sandydowns)##'


# Maximum number of trades in a transaction.  Used during archiving trades.
MAX_TRADES_IN_TRANSACTION = 200

MAX_INS_NAME_LENGTH = FBDPCommon.getMaxNameLength(acm.FInstrument)

def tradeAfterExpiry(trade):
    if not FBDPCommon.is_acm_object(trade):
        acmTrade = FBDPCommon.ael_to_acm(trade)
    else:
        acmTrade = trade
    insExpiryDate = acmTrade.Instrument().ExpiryDate()
    if insExpiryDate is None:
        return False
    elif FBDPCommon.toDate(acmTrade.TradeTime()) > insExpiryDate:
        Logme()('Trade {0} created after expiry is ignored'.format(
                acmTrade.Oid()), 'DEBUG')
        return True
    return False


def rollback_archive_object(obj, rollback):
    if FBDPCommon.is_acm_object(obj):
        obj = FBDPCommon.acm_to_ael(obj)
    ok, collect_list = FBDPCommon.collect_references(obj, False,
            Summary().ARCHIVE, True)
    if not ok:
        Summary().ignore(FBDPCommon.record_type(obj), Summary().ARCHIVE,
            'Unexpected external reference', FBDPCommon.display_id(obj))
        return

    if not obj in collect_list:
        collect_list.append(obj)

    FBDPCommon.create_clones_for_children(collect_list)

    for ref in collect_list:
        if ref.original():
            rollback_update_original(ref, rollback)
        else:
            clone = ref.clone()
            if FBDPCommon.has_attr(clone, 'archive_status'):
                FBDPRollback.archive_children(clone, rollback.Testmode,
                        rollback)
                clone.archive_status = 1
                rollback.add(clone, ['archive_status'])
                Summary().ok(clone, Summary().ARCHIVE,
                        FBDPCommon.display_id(clone))
                Logme()('Archive {0} {1}'.format(clone.record_type,
                        FBDPCommon.display_id(clone)), 'DEBUG')
            elif FBDPCommon.record_type(clone) != "Settlement":
                Summary().ok(clone, Summary().DELETE,
                        FBDPCommon.display_id(clone))
                rollback.add(clone, op='Delete')
                Logme()('Delete {0} {1}'.format(clone.record_type,
                        FBDPCommon.display_id(clone)), 'DEBUG')


def rollback_delete_object(obj, rollback, insList=[]):
    if FBDPCommon.is_acm_object(obj):
        obj = FBDPCommon.acm_to_ael(obj)
    ok, collect_list = FBDPCommon.collect_references(obj, True,
            Summary().DELETE, False)
    if not ok:
        Summary().ignore(FBDPCommon.record_type(obj), Summary().DELETE,
            'Unexpected external reference', FBDPCommon.display_id(obj))

        return

    if obj.record_type == 'Instrument':
        collect_list = [x for x in collect_list
            if x.record_type == 'Instrument' and
                x.insaddr in insList or
                x.record_type != 'Instrument']

    FBDPCommon.create_clones_for_children(collect_list)

    for ref in collect_list:
        if ref.original():
            rollback_update_original(ref, rollback)
        else:
            rollback.add(ref, op='Delete')
            Logme()('Delete {0} {1}'.format(ref.record_type,
                    FBDPCommon.display_id(ref)), 'DEBUG')
            Summary().ok(ref, Summary().DELETE, FBDPCommon.display_id(ref))


def rollback_update_original(aelObj, rollback):
    if not rollback.Testmode:
        aelObj.commit()
    else:
        Logme()('Child Update {0} {1}'.format(aelObj.record_type,
                FBDPCommon.display_id(aelObj)), 'DEBUG')
    Summary().ok(aelObj, Summary().UPDATE, FBDPCommon.display_id(aelObj))


def _selectInstruments(instruments, exp_day=None, exclude_generic=1):

    elements = {}
    for ID in instruments:
        acmIns = acm.FInstrument[ID]
        if acmIns:
            elements[acmIns.Oid()] = acmIns
        else:
            Logme()('Instrument {0} does not exist'.format(ID), 'DEBUG')
    Logme()('{0} instruments initially selected'.format(len(elements)),
            'DEBUG')
    # Filter generic
    if exclude_generic:
        numRemoved = 0
        for insOid in elements.keys():
            acmIns = elements[insOid]
            if acmIns.Generic():
                del elements[insOid]
                numRemoved += 1
        Logme()('{numRemoved} instruments removed by {msg} filtering'.format(
                numRemoved=numRemoved, msg='"generic"'))
    # Filter on default instrument
    numRemoved = 0
    for insOid in elements.keys():
        acmIns = elements[insOid]
        if re.search('DEFAULT', acmIns.Name(), re.I):
            del elements[insOid]
            numRemoved += 1
    Logme()('{numRemoved} instruments removed by {msg} filtering'.format(
            numRemoved=numRemoved, msg='default instrument'))
    # Filter on exp_day
    if exp_day:
        numRemoved = 0
        for insOid in elements.keys():
            acmIns = elements[insOid]
            if not FBDPInstrument.isExpired(acmIns, exp_day):
                del elements[insOid]
                numRemoved += 1
        Logme()('{numRemoved} instruments removed by {msg} filtering'.format(
                numRemoved=numRemoved, msg='exp_day'))
    # Finalise
    Logme()('Number of selected instruments: {0}'.format(len(elements)),
            'DEBUG')
    nameAndInsList = [(acmIns.Name(), acmIns) for acmIns in elements.values()]
    nameAndInsList.sort()
    return [nameAndIns[1] for nameAndIns in nameAndInsList]


class _InsHandling(object):
    """
    Helper class holding definitions of instrument handling options.
    """
    ARCHIVE = 'Archive'
    DELETE = 'Delete'
    KEEP = 'Keep'


class _PosHandling(object):
    """
    Helper class holding definitions of position handling options.
    """
    ARCHIVE_WHOLE_INSTRUMENT = 'Archive whole instrument'
    ARCHIVE_TARGET_POSITIONS = 'Archive target positions'
    DELETE_WHOLE_INSTRUMENT = 'Delete whole instrument'
    DELETE_TARGET_POSITIONS = 'Delete target positions'
    KEEP_ALL_POSITIONS = 'Keep all positions'


def perform_instrument_expiry(args):
    FBDPCommon.callSelectionHook(args, 'instruments', 'expiration_selection')

    e = Expiry('Expiration', args['Testmode'], args)
    e.perform(args)
    e.end()


class Expiry(FBDPRollback.RollbackWrapper, FBDPValidate):

    EXCLUDED_OBJECTS = ['Settlement', 'Journal', 'JournalInformation',
            'Confirmation', 'OperationsDocument']

    def validateValuationParams(self):
        return True

    def __remove_archived_or_deleted_instruments(self, listOfInstruments,
            summary, summaryInsAction):
        instruments = []
        for ins in listOfInstruments:
            if ins.ArchiveStatus():
                summary.ignore(ins, summaryInsAction, 'Instrument is already '
                        'archived.', ins.Name())
            elif ins.IsDeleted():
                summary.ignore(ins, summaryInsAction, 'Instrument is already '
                        'deleted.', ins.Name())
            else:
                instruments.append(ins)
        return instruments

    def __setupTimer(self):

        self.__endTime = None
        if self.maxRunTime and self.maxRunTime > 0.0:
            self.__endTime = time.time() + self.maxRunTime
            Logme()('Setting maximum run time to {0}s'.format(
                     self.maxRunTime))
            Logme()('Will terminate after {0}'.format(time.strftime(
                    "%Y-%m-%d %H:%M:%S", time.localtime(self.__endTime))))

    def __hasTimerAlarmed(self):

        if not self.__endTime:
            return False
        return time.time() > self.__endTime

    def __updateAdditionalInfo(self, infoSpecs, trd):
        trdInfoSpec = [i.AddInf() for i in trd.AddInfos()]
        for spec in infoSpecs:
            if spec not in trdInfoSpec:
                newAddInfo = acm.FAdditionalInfo()
                newAddInfo.AddInf(spec)
                newAddInfo.Parent(trd)
                newAddInfo.FieldValue(spec.DefaultValue())
                self.add(newAddInfo)

    def perform(self, args):
        self.validate()
        self.isCSPIinsChecked = {}  # Externid1 of created main instruments
        self.isTradedLookup = {}
        self.spotDayOffsetWarner = _SpotDayOffsetWarner()

        #-------------------------------------------------------------
        # Read arguments
        self.readArguments(args)

        #-------------------------------------------------------------
        # Setup timer
        self.__setupTimer()

        #-------------------------------------------------------------
        # check expiration handling
        self.checkExpirationHandling(args)

        #-------------------------------------------------------------
        # Create report file
        self.createReportFileName()

        #-------------------------------------------------------------
        # Get instruments
        instruments = self.getInstruments()

        #-------------------------------------------------------------
        # If no instrument, generate the report and return
        if not instruments:
            self.generateReport(args)
            return 1

        #-------------------------------------------------------------
        # Ensure a clean transaction
        try:
            acm.AbortTransaction()
        except:
            pass

        #-------------------------------------------------------------
        # Get portfolios
        # If None, represent ALL portfolios
        ports = self.getPortfolios(args)

        #-------------------------------------------------------------
        # If FExpiration already has been run for an instrument, ignore it.
        instruments = self.__remove_archived_or_deleted_instruments(
                instruments, Summary(), self.summaryInsAction)

        #-------------------------------------------------------------
        # Populate instrument list with a 3-tuple of (instrument name,
        # cash posting instrument, remark text).
        insInfoList = []
        for ins in instruments:
            # Break the loop after timer expired
            if self.__hasTimerAlarmed():
                break
            has, exclude_references = FBDPCommon.has_excluded_references(
                FBDPCommon.acm_to_ael(ins), Expiry.EXCLUDED_OBJECTS)
            if has:
                insInfoList.append((ins.Name(), None, 'External references '
                        'found to these excluded objects: {0}'.format(
                        ', '.join(exclude_references))))
                continue

            if not self.allowLive and not ins.IsExpired():
                insInfoList.append((ins.Name(), None, 'Instrument has not '
                        'expired.'))
                continue
            if self.isInTradedCombination(ins):
                insInfoList.append((ins.Name(), None, 'Member of a traded '
                        'Combination.'))
                continue
            if (self.insHandling == _InsHandling.ARCHIVE and
                    self.posHandling == _PosHandling.ARCHIVE_WHOLE_INSTRUMENT):
                if not self.deAggregatePosition(ins):
                    insInfoList.append((ins.Name(), None, 'Failed to '
                            'deaggregate all positions in the instrument.'))
                    continue
            if self.posHandling == _InsHandling.KEEP and \
               self.posHandling == _PosHandling.ARCHIVE_TARGET_POSITIONS:
                if not self.deAggregatePosition(ins, ports):
                    insInfoList.append((ins.Name(), None, 'Failed to '
                            'deaggregate target positions in the instrument.'))
                    continue
            isTraded = self.isTraded(ins)
            if isTraded and self.keepPL:
                if not self.includeZeroPos:
                    insInfoList.append((ins.Name(), None, 'Instrument is '
                            'traded.'))
                    continue
                if isTraded == 2:
                    insInfoList.append((ins.Name(), None, 'A traded '
                            'derivative exists.'))
                    continue
                # check for future trades
                if not self.checkTrades(ins):
                    insInfoList.append((ins.Name(), None, 'The instrument '
                            'has a trade in the future.'))
                    continue
                # Instrument should be calculated
                cpIns = self.getCashPostingInstrument(ins)
                insInfoList.append((ins.Name(), cpIns, ''))
            else:
                insInfoList.append((ins.Name(), None, ''))

        Summary().commitEntries()

        #-------------------------------------------------------------
        # Loop over instrument infos
        insToDelete = [acm.FInstrument[name].Oid()
                for name, cpIns, ignoreMsg in insInfoList]

        for name, cpIns, ignoreMsg in insInfoList:
            # Break the loop after timer expired
            if self.__hasTimerAlarmed():
                break

            acm.PollDbEvents()
            self.trxTradeDic = {}
            self.nrOfArchivedTrades = 0
            abort = False
            errorMsg = ''
            Logme()('Now handling {0}'.format(name), 'DEBUG')
            ins = acm.FInstrument[name]
            if not ins:
                Logme()('Instrument already deleted', 'DEBUG')
                continue
            if ignoreMsg:
                self.handleAbortion(ins, ignoreMsg=ignoreMsg)
                Summary().commitEntries()
                continue

            # Transaction begins.
            self.beginTransaction()

            # Calculate position
            calcPositions = None
            if not abort:
                try:
                    cashPostingDay = ins.ExpiryDate()
                    if not cashPostingDay:
                        # If live instruments are allowed
                        cashPostingDay = acm.Time.DateToday()
                    # Uses call to instrument.calculate_position

                    calcPositions = \
                            FBDPCalculatePosition.CalculatePosition(
                                    ins,
                                    end_date=cashPostingDay,
                                    showSummary=False,
                                    hookArguments=self.ael_variables_dict,
                                    usePlClearDate=1)
                    if calcPositions.dirty:
                        ignoreMsg = calcPositions.errMsg
                        abort = True
                except Exception as ex:
                    traceback.print_exc()
                    abort = True
                    errorMsg = str(ex)

            # Cash posting
            Logme()('calcPositions = {0}'.format(calcPositions), 'DEBUG')
            cspTrades = []
            if not abort:
                if self.keepPL and calcPositions:
                    try:
                        # cashPost also checks if a trade in the position has
                        # acquire_day after instrument exp_day. When this
                        # happens CalculatePosition will be called again
                        ignoreMsg, cspTrades = self.cashPost(ins,
                                                             calcPositions,
                                                             cpIns,
                                                             ports)
                        if ignoreMsg:
                            abort = True
                        else:
                            self.commitAddedEntities()
                    except Exception as ex:
                        traceback.print_exc()
                        abort = True
                        errorMsg = str(ex)

                    #upgrade the mandatory additional info.
                    try:
                        infoSpec = acm.FAdditionalInfoSpec.Select(
                            "recType = 19 and mandatory = 1")
                        for cspPosition in cspTrades:
                            cspTrd = FBDPCommon.ael_to_acm(cspPosition[0])
                            self.__updateAdditionalInfo(infoSpec, cspTrd)

                            depTrds = cspPosition[1]
                            if not depTrds:
                                continue
                            for depT in depTrds:
                                self.__updateAdditionalInfo(infoSpec, depT)
                        self.commitAddedEntities()
                    except Exception as ex:
                        traceback.print_exc()
                        abort = True
                        errorMsg = str(ex)

            # Archive/delete positions and/or instruments
            if not abort:
                if self.insHandling == _InsHandling.KEEP and \
                   self.posHandling == _PosHandling.ARCHIVE_TARGET_POSITIONS:
                    Logme()('Archiving data...', 'DEBUG')
                    # Need to fake cspTrades... Ugly... FIXME
                    if not self.keepPL:
                        cspTrades = [[None, x[1]] for x in calcPositions]
                    Logme()('numPositions = {0}'.format(len(cspTrades)),
                            'DEBUG')
                    try:
                        self.archivePositionsAndChildren(ins, cspTrades,
                                                         ports)
                    except Exception as ex:
                        traceback.print_exc()
                        abort = True
                        errorMsg = str(ex)
                    Logme()('Done archiving data!', 'DEBUG')
                elif self.insHandling == _InsHandling.KEEP and \
                     self.posHandling == _PosHandling.DELETE_TARGET_POSITIONS:
                    Logme()('Deleting data...', 'DEBUG')
                    positions = None
                    if self.keepPL:
                        positions = [x[1] for x in cspTrades]
                    else:
                        positions = [x[1] for x in calcPositions]
                    Logme()('numPositions = {0}'.format(len(positions)),
                            'DEBUG')
                    abort, errorMsg = self.deletePositionsAndChildren(
                                positions, ports)
                    Logme()('Done deleting data!', 'DEBUG')
                elif self.insHandling == _InsHandling.ARCHIVE:
                    Logme()('Archiving data...', 'DEBUG')
                    try:
                        self.archivePositionsAndChildren(ins, cspTrades, None)
                        rollback_archive_object(ins, self)
                    except Exception as ex:
                        traceback.print_exc()
                        abort = True
                        errorMsg = str(ex)
                    Logme()('Done archiving data!', 'DEBUG')
                elif self.insHandling == _InsHandling.DELETE:
                    Logme()('Deleting data...', 'DEBUG')
                    invalidTrade = False
                    if self.keepPL and ins.ExpiryDate() != None:
                        positions = [x[1] for x in cspTrades]
                        abort, errorMsg = self.deletePositionsAndChildren(
                                    positions, ports)
                        if not abort:
                            for trade in ins.Trades():
                                if tradeAfterExpiry(trade):
                                    invalidTrade = True
                    if not abort and not invalidTrade:
                        try:
                            rollback_delete_object(ins, self, insToDelete)
                        except Exception as ex:
                            traceback.print_exc()
                            abort = True
                            errorMsg = str(ex)
                    Logme()('Done deleting data!', 'DEBUG')

            # Commit transaction
            if not abort:
                try:
                    self.commitTransaction(True)
                except Exception as error:
                    errorMsg = ('Failed to {0} instrument ({1})'.format(
                            self.insHandling, str(error)))
                    abort = True
            # Had anything went wrong ... goes here.
            if abort:
                self.abortTransaction()
                self.handleAbortion(ins, errorMsg, ignoreMsg)

            # Finalise the loop
            if not abort:
                Logme()('{0}d instrument {1}'.format(self.insHandling, name))
            Summary().commitEntries()

        Logme()('', 'NOTIME')
                #-------------------------------------------------------------
        # Done, write report file
        if self.__hasTimerAlarmed():
            Logme()('Maxium run time reached. Some of the selected '
                    'instruments may not have been processed.', 'WARNING')
        self.generateReport(args)
        self.spotDayOffsetWarner.generateWarning()

    def handleAbortion(self, ins, errorMsg='', ignoreMsg=''):
        Summary().abortEntries()
        if errorMsg:
            Summary().fail(ins, self.summaryInsAction, errorMsg,
                           ins.Name())
            Logme()('{0}'.format(errorMsg), 'ERROR')
        else:
            Summary().ignore(ins, self.summaryInsAction, ignoreMsg,
                                     ins.Name())
            Logme()('{0}'.format(ignoreMsg), 'WARNING')

    def isTraded(self, ins):
        """
        Returns:
        0 if the instrument is totally untraded, or
                the instrument doesn't exist
        1 if only the instrument itself is traded,
        2 if it has a traded derivative.
        """
        ret = 0
        if ins.Oid() in self.isTradedLookup:
            return self.isTradedLookup[ins.Oid()]
        if not ins:
            Logme()('Instrument does not exist.', 'WARNING')
            return 0
        nrOfTrades = len(ael.dbsql("select t.trdnbr from trade t where "
                "t.insaddr = {0}".format(ins.Oid()))[0])
        if nrOfTrades:
            ret = 1

        underlyingIds = ael.asql("select i.insaddr from instrument i where "
                "i.und_insaddr = {0}".format(ins.Oid()))
        references = [acm.FInstrument[e[0]] for e in underlyingIds[1][0]]
        legInsIds = ael.asql("select i.insaddr from instrument i, leg l "
                "where (l.insaddr = i.insaddr and l.credit_ref = {0})".format(
                ins.Oid()))
        references.extend([acm.FInstrument[e[0]] for e in legInsIds[1][0]])
        for der in references:
            if self.isTraded(der):
                ret = 2
                break
        self.isTradedLookup[ins.Oid()] = ret
        return ret

    def cashPost(self, ins, calcPositions, cpIns, ports):
        csp_trades = []
        for calcPos in calcPositions:
            calcTrades = calcPos[0]
            posTrades = calcPos[1]
            lastAcquireDay = "1900-01-01"
            for trade in posTrades:
                if lastAcquireDay < trade.AcquireDay():
                    lastAcquireDay = trade.AcquireDay()
            errMsg = 'Calculation of Position failed.'
            if ins.ExpiryDate() == None:
                errMsg = ('Recalculation of a position failed because the '
                        'expiry date has not been set')
                # We have used wrong end_date in ins.calculate_position for
                # this position, we need to call calculate_position again
                calcTrades = self.recalculatePosition(posTrades[0],
                        lastAcquireDay)
            else:
                if lastAcquireDay > ins.ExpiryDate():
                    errMsg = ('Recalculation of a position failed because the '
                            'acquire date ({0}) is after the expiry date '
                            '({1})'.format(lastAcquireDay, ins.ExpiryDate()))
                    # We have used wrong end_date in ins.calculate_position for
                    # this position, we need to call calculate_position again
                    calcTrades = self.recalculatePosition(posTrades[0],
                            lastAcquireDay)
            if not calcTrades:
                return (errMsg, csp_trades)
            if len(calcTrades) > 1:
                useCurrencyDependency = True
            else:
                useCurrencyDependency = False
            port = calcTrades[0].Portfolio()
            portName = str(port and port.Name())  # None is converted to 'None'
            posName = '[{0}:{1}]'.format(portName, ins.Name())
            for trd in calcTrades:
                if ports and trd.Portfolio() not in ports:
                    continue
                if not FBDPCommon.eps_compare(trd.Quantity()):
                    if ins.InsType() in ('Option', 'Warrant',
                            'Future/Forward'):
                        msg = 'Non-Zero Position in {0}.'.format(posName)
                        return (msg, csp_trades)
                if not trd.Payments() and FBDPCommon.eps_compare(
                        trd.AggregatePl()):
                    Logme()('Position {0} has no P/L.'.format(posName), 'INFO')
                    continue
                if not self.cashPostNonZeroPos:
                    if trd.Payments():
                        msg = 'Position {0} has P/L (Carry).'.format(posName)
                    else:
                        msg = 'Position {0} has P/L (RPL).'.format(posName)
                    return (msg, csp_trades)
                dependentTrades = []
                if useCurrencyDependency:
                    for trade in posTrades:
                        if trade.Currency() == trd.Currency():
                            dependentTrades.append(trade)
                else:
                    for trade in posTrades:
                        dependentTrades.append(trade)
                cspTrade, lastPayDay = self.CreateCSPTrade(ins, portName,
                        trd, cpIns)
                csp_trades.append([cspTrade, dependentTrades])
                if not self.allowLive and lastPayDay > ael.date_today():
                    msg = ('Instrument has not expired. (when including spot '
                            'days for cash posting)')
                    return (msg, csp_trades)
        return ('', csp_trades)

    def recalculatePosition(self, depTrade, endDate):
        recalcCpTrades = FBDPCalculatePosition.CalculatePosition(
                depTrade.Instrument(),
                start_date=None,
                end_date=endDate,
                portfolio=[depTrade.Portfolio()],
                usePlClearDate=1)
        for pos in recalcCpTrades:
            calcTrades = pos[0]
            dependentTrades = pos[1]
            for trade in dependentTrades:
                if depTrade.Oid() == trade.Oid():
                    return calcTrades
        return []

    def archivePositionsAndChildren(self, ins, cspTrades, ports):
        archivedTrdnbrs = []
        if cspTrades:
            for cspTrade, dependentTrades in cspTrades:
                if not dependentTrades:
                    continue
                if ports and dependentTrades[0].Portfolio() not in ports:
                    continue
                for depTrade in dependentTrades:
                    archivedTrdnbrs.append(depTrade.Oid())
                    self.archiveTradeAndChildren(depTrade, cspTrade)
        if not ports:
            for trade in ins.Trades():
                if trade.Oid() not in archivedTrdnbrs:
                    self.archiveTradeAndChildren(trade)

    def archiveTradeAndChildren(self, trade, trxTrade=None):

        if self.keepPL and tradeAfterExpiry(trade):
            return

        if FBDPCommon.is_acm_object(trade):
            trade = FBDPCommon.acm_to_ael(trade)
        aelClone = trade.clone()
        aelClone.archive_status = 1
        if aelClone.status != 'Confirmed Void':
            aelClone.status = 'Void'
        if trxTrade and aelClone.trx_trdnbr == 0:
            if FBDPCommon.is_acm_object(trxTrade):
                trxTrade = FBDPCommon.acm_to_ael(trxTrade)
            aelClone.trx_trdnbr = trxTrade.trdnbr
            self.add(aelClone, ['archive_status', 'trx_trdnbr', 'status'])
        else:
            self.add(aelClone, ['archive_status', 'status'])
        Summary().ok(aelClone, self.summaryInsAction, aelClone.trdnbr)
        Logme()('Archive Trade {0}'.format(aelClone.trdnbr), 'DEBUG')
        FBDPRollback.archive_children(aelClone, self.Testmode, self)
        self.nrOfArchivedTrades += 1
        if self.nrOfArchivedTrades > MAX_TRADES_IN_TRANSACTION:
            self.commitAddedEntities()
            self.nrOfArchivedTrades = 0

    def deletePositionsAndChildren(self, positions, ports):
        abort = False
        errorMsg = ''
        try:
            for position in positions:
                if ports and position[0].Portfolio() not in ports:
                    continue
                for trade in position:
                    # Do not remove settlement unless deleting the instrument
                    rollback_delete_object(trade, self)
        except Exception as ex:
            traceback.print_exc()
            abort = True
            errorMsg = str(ex)
        return abort, errorMsg

    def getCashPostingInstrument(self, ins):
        cpInstrument = self.cpInstrument
        if self.cpInUnderlying and ins.Underlying():
            #cpInstrument = None
            cpInstrument_tmp = ins.Underlying()
            if cpInstrument_tmp.Notional() and cpInstrument_tmp.Underlying():
                cpInstrument_tmp = cpInstrument_tmp.Underlying()
            if FBDPInstrument.isTradable(cpInstrument_tmp):
                cpInstrument = cpInstrument_tmp
            else:
                Logme()('Cash posting in the Underlying {0} is not possible '
                        'as it isn\'t tradable. Using alternative '
                        'instrument.'.format(cpInstrument_tmp.Name()),
                        'WARNING')
        return self.getOrCreateCSPInstrument(cpInstrument)

    def readArguments(self, args):
        self.instrumentNames = args.get('instruments')
        self.cpInUnderlying = args['cp_in_underlying']
        self.cpInstrument = None
        self.allowLive = args['allowLive']
        if args.get('cp_instrument'):
            self.cpInstrument = args['cp_instrument'][0]
        if self.allowLive:
            self.__expDay = None
            self.__excludeGeneric = not args['allowGeneric']
        else:
            self.__expDay = acm.Time.DateToday()
            self.__excludeGeneric = None
        self.reportPath = args['report_path']
        self.reportFilename = None
        self.maxRunTime = args.get('MaxRunTime')

    def checkExpirationHandling(self, args):
        """
        Set various flags depending on the expiration handling specified.  The
        flags to be set includes: insHandling, posHandling, includeZeroPos,
        cashPostNonZeroPos, keepPL, summaryInsAction.
        """

        expHandling = args['expiration_handling']
        alsoArcOrDelIns = True
        try:
            alsoArcOrDelIns = args['alsoArcOrDelIns']
        except:
            pass

        self.insHandling = None
        self.posHandling = None
        self.includeZeroPos = False
        self.cashPostNonZeroPos = False
        self.keepPL = True
        self.summaryInsAction = None

        if expHandling == FExpirationAction.ARC_UNTRD_INS:
            self.insHandling = _InsHandling.ARCHIVE
            self.posHandling = _PosHandling.ARCHIVE_WHOLE_INSTRUMENT
        elif expHandling == FExpirationAction.DEL_UNTRD_INS:
            self.insHandling = _InsHandling.DELETE
            self.posHandling = _PosHandling.DELETE_WHOLE_INSTRUMENT
        elif expHandling == FExpirationAction.ARC_INS_AND_POS_W_OUT_PL:
            self.insHandling = _InsHandling.ARCHIVE
            self.posHandling = _PosHandling.ARCHIVE_WHOLE_INSTRUMENT
            self.includeZeroPos = True
        elif expHandling == FExpirationAction.DEL_INS_AND_POS_W_OUT_PL:
            self.insHandling = _InsHandling.DELETE
            self.posHandling = _PosHandling.DELETE_WHOLE_INSTRUMENT
            self.includeZeroPos = True
        elif expHandling == FExpirationAction.ARC_INS_AND_CASH_POST_POS:
            self.insHandling = _InsHandling.ARCHIVE
            self.posHandling = _PosHandling.ARCHIVE_WHOLE_INSTRUMENT
            self.includeZeroPos = True
            self.cashPostNonZeroPos = True
            self.keepPL = True
        elif expHandling == FExpirationAction.DEL_INS_AND_CASH_POST_POS:
            self.insHandling = _InsHandling.DELETE
            self.posHandling = _PosHandling.DELETE_WHOLE_INSTRUMENT
            self.includeZeroPos = True
            self.cashPostNonZeroPos = True
            self.keepPL = True
        elif expHandling == FExpirationAction.ARC_INS_AND_TRD_W_OUT_CASH_POST:
            self.insHandling = _InsHandling.ARCHIVE
            self.posHandling = _PosHandling.ARCHIVE_WHOLE_INSTRUMENT
            self.keepPL = False
        elif expHandling == FExpirationAction.DEL_INS_AND_TRD_W_OUT_CASH_POST:
            self.insHandling = _InsHandling.DELETE
            self.posHandling = _PosHandling.DELETE_WHOLE_INSTRUMENT
            self.keepPL = False
        elif expHandling == FExpirationAction.ARC_AND_CASH_POST_POS:
            if alsoArcOrDelIns:
                self.insHandling = _InsHandling.ARCHIVE
                self.posHandling = _PosHandling.ARCHIVE_WHOLE_INSTRUMENT
            else:
                self.insHandling = _InsHandling.KEEP
                self.posHandling = _PosHandling.ARCHIVE_TARGET_POSITIONS
            self.includeZeroPos = True
            self.cashPostNonZeroPos = True
            self.keepPL = True
        elif expHandling == FExpirationAction.DEL_AND_CASH_POST_POS:
            if alsoArcOrDelIns:
                self.insHandling = _InsHandling.DELETE
                self.posHandling = _PosHandling.DELETE_WHOLE_INSTRUMENT
            else:
                self.insHandling = _InsHandling.KEEP
                self.posHandling = _PosHandling.DELETE_TARGET_POSITIONS
            self.includeZeroPos = True
            self.cashPostNonZeroPos = True
            self.keepPL = True
        elif expHandling == FExpirationAction.ARC_POS_W_OUT_CASH_POST:
            if alsoArcOrDelIns:
                self.insHandling = _InsHandling.ARCHIVE
                self.posHandling = _PosHandling.ARCHIVE_WHOLE_INSTRUMENT
            else:
                self.insHandling = _InsHandling.KEEP
                self.posHandling = _PosHandling.ARCHIVE_TARGET_POSITIONS
            self.keepPL = False
        elif expHandling == FExpirationAction.DEL_POS_W_OUT_CASH_POST:
            if alsoArcOrDelIns:
                self.insHandling = _InsHandling.DELETE
                self.posHandling = _PosHandling.DELETE_WHOLE_INSTRUMENT
            else:
                self.insHandling = _InsHandling.KEEP
                self.posHandling = _PosHandling.DELETE_TARGET_POSITIONS
            self.keepPL = False
        else:
            raise ValueError('Unknow expiration handling action {0!r}'.format(
                    expHandling))

        if self.insHandling == _InsHandling.DELETE:
            self.summaryInsAction = Summary().DELETE
        else:
            self.summaryInsAction = Summary().ARCHIVE

    def getInstruments(self):

        if not self.instrumentNames:
            Logme()('Dynamical query yielded no instruments.', 'INFO')
            return None
        insList = _selectInstruments(instruments=self.instrumentNames,
                exp_day=self.__expDay, exclude_generic=self.__excludeGeneric)
        return insList

    def getPortfolios(self, args):
        """
        Get the portfolios from the argument if the expiration handling is
        position related; otherwise return empty list.
        """
        if self.posHandling in [_PosHandling.ARCHIVE_TARGET_POSITIONS,
                                _PosHandling.DELETE_TARGET_POSITIONS]:
            ports = []
            for port in list(args['portfolios']):
                if not isinstance(port, type('')):
                    ports.append(port)
                else:
                    ports.append(acm.FPhysicalPortfolio[port])
            return ports
        else:
            return []

    def createReportFileName(self):

        if not self.reportPath:
            return
        import os
        if not os.path.exists(self.reportPath):
            os.makedirs(self.reportPath)
            Logme()('Created directory: {0}'.format(self.reportPath), 'ERROR')
        module = 'FExpiration'
        d_str = acm.Time.DateToday()
        fileprefix = os.path.join(self.reportPath, '{0}_{1}'.format(module,
                d_str))
        n = ''
        j = 0
        while os.path.exists(fileprefix + n + ".txt"):
            j = j + 1
            if j > 0:
                n = "_{0}".format(j)
            if j > 100:
                Logme()("More than 100 report files exists! Aborts execution!",
                        'ERROR')
                return
        self.reportFilename = os.path.normpath(fileprefix + n + ".txt")

    def generateReport(self, args):
        if not self.reportPath or not self.reportFilename:
            return
        try:
            fp = open(self.reportFilename, 'w')
        except:
            Logme()("Failed to open file: {0}. Can't generate report.".format(
                    self.reportFilename), 'ERROR')
            return
        fp.write(self.buildReportStr(args))
        fp.close()
        Logme()("Done Generating Report!", 'INFO')

    def buildReportStr(self, args):
        #Header
        reportStr = Summary().buildHeader()
        reportStr += '\n'
        #Execution Parameters
        reportStr += Summary().buildExecutionParametersStr(args)
        reportStr += '\n'
        # Handling section
        logTables = []
        if Logme().getLogMode() < 2:
            logTables = ['Instrument']
        reportStr += Summary().buildOkIdsStr(logTables)
        # Failed section
        reportStr += Summary().buildErrorsAndWarningsStr()
        reportStr += '\n'
        # Actions
        reportStr += Summary().buildActionStr()
        reportStr += '\n'
        return reportStr

    def isInTradedCombination(self, ins):
        for link in acm.FCombInstrMap.Select(
                'instrument={0}'.format(ins.Oid())):
            if self.isTraded(link.Combination()):
                return 1
        return 0

    def checkTrades(self, ins):
        simulatedExist = False
        for trade in ins.Trades():
            if trade.AcquireDay() > acm.Time.DateToday():
                return False
            if trade.Status() == 'Simulate':
                simulatedExist = True
        if simulatedExist:
            vp = acm.UsedValuationParameters()
            if vp.IncludeSimulatedTrades():
                msg = ('Instrument {0} has simulated trades and "Include '
                        'Simulated Trades" toggled in the '
                        'ValuationParameter'.format(ins.Name()))
                msg += '\nProfit and Loss may differ.'
                Logme()(msg, 'WARNING')
        return True

    def deAggregatePosition(self, ins, ports=None):
        aggregates = []
        useSelectedFundingDay = FBDPCommon.getUseSelectedFundingDay()
        for t in ins.Trades():
            if t.Aggregate() != 0:
                if not ports or t.Portfolio() in ports:
                    aggregates.append(t)
        if aggregates:
            if not self.Testmode:
                ins.DeaggregateTrades(1, useSelectedFundingDay)
                acm.PollDbEvents()
                for t in ins.Trades():
                    if t.Aggregate():
                        return False
        return True

    def CreateCSPTrade(self, ins, prfid, cp, cp_instrument):
        """ Creates a CSP Trade. """
        last_pay_day = ael.date_from_time(0)
        insid = ins.Name()
        csp = ael.Instrument[cp_instrument.Oid()]
        t = ael.Trade[cp.Oid()].new()
        t.insaddr = csp
        t.type = 'Cash Posting'
        if len(insid) > MAX_INS_NAME_LENGTH:
            t.text1 = insid[:MAX_INS_NAME_LENGTH - 1] + '$'
        if len(prfid) > MAX_INS_NAME_LENGTH:
            t.text2 = prfid[:MAX_INS_NAME_LENGTH - 1] + '$'
        else:
            t.text1 = insid
            t.text2 = prfid
        t.quantity = 0.0
        t.price = 0.0
        t.premium = 0.0
        for p in t.payments():
            if (p.type != 'Aggregated Funding' and
                    p.type != 'Aggregated Settled'):
                p.payday = ael.date_from_time(t.time)
            if p.payday > last_pay_day:
                last_pay_day = p.payday

        Logme()('Expired Instrument Type {0}'.format(ins.InsType()), 'DEBUG')
        if ins.InsType() == 'Option':
            Logme()('Underlying instrument Type {0}'.format(
                    ins.UnderlyingType()), 'DEBUG')
            isFXOption = ins.UnderlyingType() == 'Curr'
            if isFXOption and self.cpInUnderlying:
                # Underlying instrument currency (strike curr)
                aelIns = FBDPCommon.acm_to_ael(ins)
                strikeCurr = FBDPCommon.acm_to_ael(ins).strike_curr
                Logme()('Cash Posting Trade Currency is {0}'.format(
                        t.curr.display_id()), 'DEBUG')
                if not strikeCurr:
                    Logme()('Missing Strike Currency', 'WARNING')
                else:
                    Logme()('Underlying Instrument Strike Currency is '
                            '{0}'.format(strikeCurr.display_id()), 'DEBUG')
                # Strike currency is cash posting trade currency case.
                if strikeCurr.insaddr == t.curr.insaddr:
                    t.premium = t.aggregate_pl
                    t.aggregate_pl = 0
                # Underlying currency is cash posting trade currency
                elif aelIns.und_insaddr == t.curr:
                    t.quantity = t.aggregate_pl
                    t.aggregate_pl = 0
                #3 currency
                elif strikeCurr.insaddr != t.curr.insaddr:
                    pAggPlToPrem = ael.Payment.new(t)
                    pAggPlToPrem.valid_from = ael.date_from_time(t.time)
                    pAggPlToPrem.payday = t.value_day
                    pAggPlToPrem.curr = t.curr
                    pAggPlToPrem.amount = t.aggregate_pl
                    pAggPlToPrem.type = 'Premium'
                    t.aggregate_pl = 0

                # Only update the currency of the cash posting trade when the
                # strike currency is different from the trading currency of
                # the trade to be archived.
                if strikeCurr.insaddr != t.curr.insaddr:
                    t.curr = strikeCurr
                    Logme()('strikeCurr.insaddr != t.curr.insaddr', 'DEBUG')
                else:
                    Logme()('strikeCurr.insaddr = t.curr.insaddr', 'DEBUG')

        # Must add ael entities to rollback CREATE if abortTransaction should
        # work properly
        self.add_trade(t)
        self.spotDayOffsetWarner.recordCashPostedInstrument(insid,
                ins.SpotBankingDaysOffset(), cp_instrument.Name(),
                cp_instrument.SpotBankingDaysOffset())
        # Must return ael entity to retrieve correct trdnbr after
        # commitTransaction
        return (t, last_pay_day)
        # The P/L is saved in the aggregate_pl field

    def getOrCreateCSPInstrument(self, cp_instrument=None):
        #Returns the cash posting instrument. Creates if not exists.
        if cp_instrument:
            return cp_instrument
        else:
            insid = CSP
            ext_id1 = CSP_EXTID1
            ext_id2 = CSP_EXTID2
            text = 'For CashPosting'
            for t, c in [(insid, 'name'), (ext_id1, 'externalId1'),
                    (ext_id2, 'externalId2')]:
                i = acm.FInstrument.Select("{0}='{1}'".format(c, t))
                if i:
                    i = i[0]
                    if (ext_id1 not in self.isCSPIinsChecked and
                            not (i.ExternalId1() == ext_id1 and
                                    i.ExternalId2() == ext_id2)):
                        i2 = i.Clone()
                        i2.ExternalId1 = ext_id1
                        i2.ExternalId2 = ext_id2
                        if not self.Testmode:
                            FBDPCommon.commit(i2, i)
                        Summary().ok(i, Summary().UPDATE)
                        self.isCSPIinsChecked[ext_id1] = None
                        acm.PollDbEvents()
                        return i2
                    else:
                        self.isCSPIinsChecked[ext_id1] = None
                        return i
            i = acm.FFreeDefinedCashFlow()
            i.Name = insid
            i.ExternalId1 = ext_id1
            i.ExternalId2 = ext_id2
            i.ContractSize = 1.0
            i.SpotBankingDaysOffset = 0
            i.FreeText = text[:19]
            i.CreateLeg(False)

            if not self.Testmode:
                i.Commit()
            Summary().ok(i, Summary().CREATE, i.Name())
            self.isCSPIinsChecked[ext_id1] = None
            acm.PollDbEvents()
            return i


class _SpotDayOffsetWarner():
    """
    The class is responsible to record the instruments which trades had been
    cash-posted into instruments with different spot day offset, and to
    generate warnings based on the instruments recorded.

    The only data structure maintained is a dictionary, which takes the form:
        self.spotDayOffsetInstrumentDict = {
                insName1: (insSpot1, cpInsName1, cpInsSpot1),
                insName2: (insSpot2, cpInsName2, cpInsSpot2),
                ...
            }
    where the insName and insSpot refer to the instrument name string and
    the instrument spot day offset in integer.  The 'cpIns-' prefix denotes
    cash posting instruments.

    Two public methods are provided:
        recordCashPostedInstrument() should be called when the trades are
                cash-posted.
        generateWarning() should be called at the end, after all the cash-
                postings had been performed.
    """

    def __init__(self):

        # For recording instruments where different spot day offset cash-
        # posting occured.
        self.spotDayOffsetInstrumentDict = {}

    def recordCashPostedInstrument(self, insName, insSpot, cpInsName,
                                     cpInsSpot):
        """
        Record the instruments that cash posting had been performed upon.
        """

        # Only record when there is spot day offset difference.
        if insSpot != cpInsSpot:
            self.spotDayOffsetInstrumentDict[insName] = (insSpot, cpInsName,
                                                         cpInsSpot)

    def generateWarning(self):
        """
        Warn about trades in some instruments were cash posted to an
        instrument with different spot day offset.
        Only print the warning message if there is such case.
        """

        # No different spot day offset case, nothing to warn, return.
        if len(self.spotDayOffsetInstrumentDict) == 0:
            return

        # Warning messages are collected in msgs list before printing.
        msgs = []
        msgs.append('NOTE: Trades of the following instruments are cash '
                    'posted to instruments with different spot days offset:')

        # Loop through instruments that cash posting had been performed.
        numIns = 0
        showMaxNumOfIns = 10
        for insName in sorted(self.spotDayOffsetInstrumentDict):
            insSpot, cpInsName, cpInsSpot = \
                    self.spotDayOffsetInstrumentDict[insName]
            numIns += 1
            # Only show up to showMaxNumOfIns instruments.
            if numIns <= showMaxNumOfIns:
                msgs.append('    Instrument {0} -> {1}, Spot Days {2} -> '
                        '{3}.'.format(insName, cpInsName, insSpot, cpInsSpot))
            else:
                break
        # In case too many instruments, show the summary for the rest.
        if numIns > showMaxNumOfIns:
            msgs.append('    (Only {0} out of {1} shown)'.format(
                    showMaxNumOfIns, numIns))

        msgs.append('The spot day difference does not affect cash posting.')
        msgs.append('However, the Trading Manager may display slightly '
                    'different funding-related profit and loss values, '
                    'due to the change of valuation date.')

        # Finally, show the message
        for msg in msgs:
            Logme()(msg)

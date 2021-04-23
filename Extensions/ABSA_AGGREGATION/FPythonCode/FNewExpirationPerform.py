""" Compiled: 2020-01-21 09:44:09 """

#__src_file__ = "extensions/expiration/etc/FNewExpirationPerform.py"
#----------------------------------------------------------------------------
#    (c) Copyright 2021 SunGard Front Arena. All rights reserved.
#----------------------------------------------------------------------------
"""----------------------------------------------------------------------------
MODULE

    FNewExpirationPerform.py - New Expiration implementation.

DESCRIPTION

ENDDESCRIPTION
----------------------------------------------------------------------------"""


import collections


import acm
import ael


import FBDPPerform
import FNewExpirationHelper as helper
import importlib
importlib.reload(helper)
import FNewExpirationUtility as utility
importlib.reload(utility)
import FBDPCommon
import FBDPTimer
import FBDPInstrument

ACTION_ARCHIVE = 'Archive'
ACTION_DEARCHIVE = 'De-archive'
ACTION_DELETE = 'Delete'
ACTION_DELETE_POSITIONS = 'Delete Positions'

_OUTCOME_OK = 'ok'
_OUTCOME_IGNORE = 'ignored'
_OUTCOME_FAIL = 'failed'

_PERFORMERS = {}


def _perform_instruments_derivatives_trades(log, execParam):

    action = execParam['expiration_handling']
    instrumentsList = execParam['instruments']

    if len(instrumentsList) == 0:
        log.logError('No Instruments specified.')

    max_runtime = execParam.get('max_runtime')
    timer = FBDPTimer.Timer(max_runtime, log)
    timer.start()

    processedDerivatives = []

    for instOrInstName in instrumentsList:
        if timer.hasAlarmed():
            break

        name = instOrInstName
        if FBDPCommon.is_acm_object(instOrInstName):
            name = instOrInstName.Name()
        try:
            log.logInfo('Start Handling instrument %s' % name)
            if not utility.DoesInstExisted(instOrInstName):
                log.logError('Instrument %s does not exist.' % name)
                continue

            # Determining the type of task depending on the action
            inst = utility.getInstId(instOrInstName, log)
            if action == ACTION_ARCHIVE:
                if inst in processedDerivatives:
                    continue
                
                operationCompleted = []
                _perform(log, execParam, 'archive', 'trade', inst, operationCompleted)
                if not operationCompleted[0]:
                    msg = (
                            'Ignore to archive the instrument %s, '
                            'as its trades exist.' % (
                                name
                            )
                        )
                    log.summaryAddIgnore(
                        'Instrument', inst, 'ARCHIVE', [msg]
                    )
                    continue
                
                operationCompleted.clear()
                # archive Instrument if needed.
                archiveInst = execParam.get('alsoArchiveInstrument')
                if archiveInst:
                    # Check if instrument has expired

                    if execParam.get('preservePL') \
                        and not FBDPInstrument.isExpired(acm.FInstrument[name]):
                        msg = (
                            'Ignore the instrument %s, as the instrument has not expired yet.' % (
                             name))
                        log.logWarning(msg)
                        actionMsg = 'ARCHIVE'
                        log.summaryAddIgnore('Instrument', inst, 'ARCHIVE', [msg])
                        continue

                    derivatives = []
                    if utility.getDerivatives(inst, log, derivatives):
                        msg = (
                            'Archive traded derivatives or combinations '
                            'for the instrument %s ' % (name)
                        )
                        log.logInfo(msg)

                        # Archive derivative trades and itself
                        for der in derivatives:
                            _perform(log, execParam, 'archive', 'trade', der.Oid(), operationCompleted)
                            if operationCompleted[0]:
                                operationCompleted.clear()
                                _perform(log, execParam, 'archive', 'instrument', der.Oid(), operationCompleted)
                                if not operationCompleted[0]:
                                    break
                                else:
                                    operationCompleted.clear()
                            else:
                                msg = (
                                        'Ignore to archive the instrument %s, '
                                        'as derivative or combination trades cannot be archived.' % (
                                            name
                                        )
                                    )
                                log.summaryAddIgnore(
                                    'Instrument', inst, 'ARCHIVE', [msg]
                                )
                                break
                    else:                    
                        # Archive derivatives
                        for der in derivatives:
                            processedDerivatives.append(der.Oid())
                            _perform(log, execParam, 'archive', 'instrument', der.Oid(), operationCompleted)
                            if not operationCompleted[0]:
                                break
                            else:
                                operationCompleted.clear()
                    
                    # Archive the instrument
                    if not operationCompleted:
                        _perform(log, execParam, 'archive', 'instrument', inst, operationCompleted)
                    else:
                        msg = (
                                'Ignore to archive the instrument %s, '
                                'as a traded derivative or combination cannot be archived.' % (
                                    name
                                )
                            )
                        log.summaryAddIgnore(
                            'Instrument', inst, 'ARCHIVE', [msg]
                        )

            elif action == ACTION_DEARCHIVE:
                #
                # Always calling de-archive instrument first:
                #
                if inst in processedDerivatives:
                    continue
                operationCompleted = []
                _perform(log, execParam, 'dearchive', 'instrument', inst, operationCompleted)
                if operationCompleted[0]:
                    operationCompleted.clear()
                    _perform(log, execParam, 'dearchive', 'trade', inst, operationCompleted)
                    operationCompleted.clear()
                else:
                    continue

                derivatives = []
                insTraded = utility.getDerivatives(inst, log, derivatives)
                # Dearchive derivatives
                for der in derivatives:
                    processedDerivatives.append(der.Oid())
                    _perform(log, execParam, 'dearchive', 'instrument', der.Oid(), operationCompleted)
                    if operationCompleted[0]:
                        operationCompleted.clear()
                        _perform(log, execParam, 'dearchive', 'trade', der.Oid(), operationCompleted)
                    operationCompleted.clear()

            elif action == ACTION_DELETE_POSITIONS:
                operationCompleted = []
                _perform(log, execParam, 'live delete', 'trade', inst, operationCompleted)

            elif action == ACTION_DELETE:
                if not utility.isInstArchived(inst):
                    derivatives = []
                    isTraded = utility.isInstTraded(inst, log)
                    if not isTraded:
                        #Delete untraded instrument
                        operationCompleted = []
                        _perform(
                            log, execParam, 'live delete', 'instrument', inst, operationCompleted
                        )
                    else:
                        msg = (
                            'Ignore to delete the Instrument %s, as it '
                            'is a traded one.' % name
                        )
                        log.logInfo(msg)
                        log.summaryAddIgnore(
                            'Instrument', inst, 'DELETE', [msg]
                        )
                else:
                    operationCompleted = []
                    _perform(log, execParam, 'archive delete', 'trade', inst, operationCompleted)
                    if operationCompleted[0]:
                        operationCompleted.clear()
                        _perform(log, execParam, 'live delete', 'instrument', inst, operationCompleted)
            else:
                log.logError('No action selected.')

            log.logInfo('Complete Handling instrument %s\n\n' % name)

        except Exception as ex:
            msg = (
                'Errors when %s instrument %s with exception %s' % (
                    action, name, str(ex)
                )
            )
            log.logError(msg)
            if not execParam.get('suppress_exceptions', True):
                raise ex


def _perform_instruments_trades(log, execParam):

    action = execParam['expiration_handling']
    instrumentsList = execParam['instruments']

    if len(instrumentsList) == 0:
        log.logError('No Instruments specified.')

    max_runtime = execParam.get('max_runtime')
    timer = FBDPTimer.Timer(max_runtime, log)
    timer.start()
    
    for instOrInstName in instrumentsList:
        if timer.hasAlarmed():
            break
        name = instOrInstName
        if FBDPCommon.is_acm_object(instOrInstName):
            name = instOrInstName.Name()
        try:
            log.logInfo('Start Handling instrument %s' % name)
            if not utility.DoesInstExisted(instOrInstName):
                log.logError('Instrument %s does not exist.' % name)
                continue

            # Determining the type of task depending on the action
            inst = utility.getInstId(instOrInstName, log)
            if action == ACTION_ARCHIVE:
                operationCompleted = []
                _perform(log, execParam, 'archive', 'trade', inst, operationCompleted)
                
                # archive Instrument if needed.
                archiveInst = execParam.get('alsoArchiveInstrument')
                if archiveInst:
                    if not operationCompleted[0]:
                        msg = "Ingnore the instrument {0}, as the archiving trades failed".format(name)
                        log.logWarning(msg)
                        continue
                    
                    # Check if instrument has expired
                    if execParam.get('preservePL') \
                        and not FBDPInstrument.isExpired(acm.FInstrument[name]):
                        msg = (
                            'Ignore the instrument %s, as the instrument has not expired yet.' % (
                             name))
                        log.logWarning(msg)
                        actionMsg = 'ARCHIVE'
                        log.summaryAddIgnore('Instrument', inst, 'ARCHIVE', [msg])
                        continue

                    if utility.isInstTradedDerivativeOrCombination(inst, log):
                        msg = (
                            'Ignore to archive the instrument %s, '
                            'as a traded derivative or combination exists.' % (
                                name
                            )
                        )
                        log.logInfo(msg)
                        log.summaryAddIgnore(
                            'Instrument', inst, 'ARCHIVE', [msg]
                        )
                        continue

                    _perform(log, execParam, 'archive', 'instrument', inst)

            elif action == ACTION_DEARCHIVE:
                #
                # Always calling de-archive instrument first:
                #
                _perform(log, execParam, 'dearchive', 'instrument', inst)
                _perform(log, execParam, 'dearchive', 'trade', inst)

            elif action == ACTION_DELETE_POSITIONS:
                _perform(log, execParam, 'live delete', 'trade', inst)

            elif action == ACTION_DELETE:
                if not utility.isInstArchived(inst):
                    isTraded = utility.isInstTraded(inst, log)
                    if not isTraded:
                        #Delete untraded instrument
                        _perform(
                            log, execParam, 'live delete', 'instrument', inst
                        )
                    else:
                        msg = (
                            'Ignore to delete the Instrument %s, as it '
                            'is a traded one.' % name
                        )
                        log.logInfo(msg)
                        log.summaryAddIgnore(
                            'Instrument', inst, 'DELETE', [msg]
                        )
                else:
                    operationCompleted = []
                    _perform(log, execParam, 'archive delete', 'trade', inst, operationCompleted)
                    if not operationCompleted[0]:
                        msg = "Ingnore the instrument {0}, " \
                            "as the delete trades failed".format(name)
                        log.logWarning(msg)
                        continue
                    _perform(log, execParam, 'live delete', 'instrument', inst)

            else:
                log.logError('No action selected.')

            log.logInfo('Complete Handling instrument %s\n\n' % name)

        except Exception as ex:
            msg = (
                'Errors when %s instrument %s with exception %s' % (
                    action, name, str(ex)
                )
            )
            log.logError(msg)
            if not execParam.get('suppress_exceptions', True):
                raise ex    
    

def perform(log, execParam):
    """
    Determine type of task, and then dispatch to different task to complete the
    perform().
    """
    archiveDerivative = 0
    archiveInst = execParam.get('alsoArchiveInstrument', 0)
    if archiveInst:
        archiveDerivative = execParam.get('alsoArchiveDerivative', 0)
    
    try:
        if archiveInst and archiveDerivative:
            _perform_instruments_derivatives_trades(log, execParam)
        else:
            _perform_instruments_trades(log, execParam)
    except Exception as ex:
        if not execParam.get('suppress_exceptions', True):
            raise ex    

    # Finalise
    log.listTopWarningMessages()
    log.listTopErrorMessages()


def _initializePerformers():
    _PERFORMERS.clear()
    _PERFORMERS.update({
        'archive': {
            'trade': _ArchiveTrades,
            'instrument': _ArchiveInstrument,
        },
        'dearchive': {
            'trade': _DearchiveTrades,
            'instrument': _DearchiveInstrument,
        },
        'live delete': {
            'trade': _DeleteLiveTrades,
            'instrument': _DeleteInstrument,
        },
        'archive delete': {
            'trade': _DeleteArchiveTrades,
            'instrument': _DeleteInstrument,
        },
    })

def _createPerformer(log, action, object_type, inst):
    if not len(_PERFORMERS):
        _initializePerformers()

    performer_cls = _PERFORMERS[action][object_type]
    return performer_cls(inst=inst, log=log)

def _perform(log, execParam, action, object_type, inst, operationCompleted=None):
    p = _createPerformer(log, action, object_type, inst)
    p.perform(execParam, operationCompleted)
    p.end()


class _NewExpirationPerformBase(FBDPPerform.FBDPPerform):

    def __init__(self, inst, log):
        FBDPPerform.FBDPPerform.__init__(self, log)
        self.inst = inst
        self.curErrorCount = self._countErrorMessages()
        self.suppress_exceptions = True

    def __acquireRunParameter(self, execParam):
        """
        The ACQUIRING RUN PARAMETER phase of the perform()
        """
        self.suppress_exceptions = execParam.get('suppress_exceptions', True)
        self.deepArchive = execParam.get('deepArchive', 0)
        runParam = self._doAcquireRunParameter(execParam)
        return runParam

    def _validateMode(self):
        if acm.ArchivedMode():
            errMsg = 'This script must not be run in the Archived mode.'
            self._logError(errMsg)
        if acm.IsHistoricalMode():
            errMsg = 'This script must not be run in the Historical mode.'
            self._logError(errMsg)
        return

    def _perform(self, execParam, operationCompleted=None):
        # VALIDATE phase
        try:
            self._logInfo('Validating environment and parameters...')
            self._validateMode()
            if self._countErrorMessages() > self.curErrorCount:
                return

            # ACQUIRING PARAMETER phase
            self._logInfo('Acquiring run parameters...')
            runParam = self.__acquireRunParameter(execParam)
            if self._countErrorMessages() > self.curErrorCount:
                return

            # INSPECTION AND PROCESS phase
            toInspectQueue = collections.deque(runParam)
            inspectedFailedList = []
            toProcessQueue = collections.deque()
            processedFailedList = []
            processedIgnoredList = []
            processedSuccessList = []
            while True:
                if not toInspectQueue and not toProcessQueue:
                    break
                if toInspectQueue:
                    toInspecParam = toInspectQueue.popleft()
                    self.__inspect(inspectedFailedList, toProcessQueue,
                            toInspecParam)
                if toProcessQueue:
                    inspectionReport = toProcessQueue.popleft()
                    self.__process(processedFailedList,
                            processedIgnoredList, processedSuccessList,
                            inspectionReport)
            self._completeOperation(operationCompleted)
            return
        except Exception as ex:
            self._logError(str(ex))

    def __inspect(self, inspectFailedList, inspectSuccessQueue,
            toInspectQueue):
        inspectionReport = self._doInspect(toInspectQueue)
        self._doInspectReport(inspectionReport, inspectFailedList,
                inspectSuccessQueue)

    def __process(self, processedFailedList, processedIgnoredList,
            processedSuccessList, inspectionReport):

        processReport = self._doProcess(inspectionReport)
        self._doProcessReport(processReport, processedFailedList,
                processedIgnoredList, processedSuccessList)

    def _countErrorMessages(self):
        return 0

    def _completeOperation(self, operationCompleted=None):
        if operationCompleted is not None:
            operationCompleted.append(True)


class _DearchiveTrades(_NewExpirationPerformBase):
    """------------------------------------------------------------------------

    ------------------------------------------------------------------------"""

    def __init__(self, inst, log):
        _NewExpirationPerformBase.__init__(self, inst, log)

    def end(self):
        _NewExpirationPerformBase._end(self)

    def perform(self, execParam, operationCompleted=None):
        _NewExpirationPerformBase._perform(self, execParam, operationCompleted)

    __RunParam = collections.namedtuple('__RunParam', 'cpArcTrdsList')

    __InspectionReport = collections.namedtuple('__InspectionReport',
        'OpDeArcDeleteList')

    __ProcessReport = collections.namedtuple('__ProcessReport',
        'processedList')

    def _doAcquireRunParameter(self, execParam):
        """
        The ACQUIRING RUN PARAMETER phase of the perform()
        """
        arcTrds = helper.ArchivedInstTrds(self.inst,
                self._getWorldRef())
        allowed_trades = execParam.get('allowed_trades')
        if allowed_trades:
            setattr(arcTrds, 'allowed_trades', allowed_trades)
        cpArcTrdsList = arcTrds.GetArchivedTrdsAndItsCPTrds(execParam, 1)
        runParam = self.__RunParam(cpArcTrdsList=cpArcTrdsList)
        return runParam

    def _doInspect(self, cpArcTrdsList):

        OpList = []
        if cpArcTrdsList is None:
            inspectionReport = self.__InspectionReport(
                OpDeArcDeleteList=OpList
            )
            return inspectionReport
        for cpArcTrds in cpArcTrdsList:
            cpTrd = cpArcTrds.cpTrds
            arcTrdList = cpArcTrds.arcTrds

            for oid in arcTrdList:
                OpList.append(utility.Oplet(
                    ACTION_DEARCHIVE, 'Trade', oid))
            if cpTrd:
                OpList.append(utility.Oplet(
                    ACTION_DELETE, 'Trade', cpTrd))

        inspectionReport = self.__InspectionReport(OpDeArcDeleteList=OpList)
        return inspectionReport

    def _doProcess(self, inspectionReport):
        def process(opList):
            for opDetails in opList:
                if opDetails.opTyp == ACTION_DEARCHIVE:
                    utility.DeArchiveTrd(opDetails.oid, self.deepArchive,
                            self._getWorldRef())
                if opDetails.opTyp == ACTION_DELETE:
                    utility.DeleteObj(opDetails.oid,
                            opDetails.recTyp, self._getWorldRef())

            return

        processedList = []
        #for (delTrdOp, DeArcTrdsOp) in inspectionReport:
        for opList in inspectionReport:
            result = _OUTCOME_OK
            try:
                utility.performTransaction(
                    self._getWorldRef(), process, opList=opList
                )
            except Exception as ex:
                self._logError(str(ex))
                result = _OUTCOME_FAIL
                if not self.suppress_exceptions:
                    raise ex

            acm.PollDbEvents()
            processedList.append((result, opList))

        # Make the process report
        processReport = self.__ProcessReport(processedList=processedList)
        return processReport

    def _doInspectReport(self, inspectionReport, inspectFailedList,
            inspectSuccessQueue):
        inspectSuccessQueue.append(inspectionReport)

    def _doProcessReport(self, processReport, processedFailedList,
            processedIgnoredList, processedSuccessList):
        pass


class _ArchiveTrades(_NewExpirationPerformBase):
    """------------------------------------------------------------------------

    ------------------------------------------------------------------------"""

    def __init__(self, inst, log):
        _NewExpirationPerformBase.__init__(self, inst, log)

    def end(self):
        _NewExpirationPerformBase._end(self)

    def perform(self, execParam, operationCompleted=None):
        _NewExpirationPerformBase._perform(self, execParam, operationCompleted)

    __RunParam = collections.namedtuple('__RunParam', 'cpArcTrdsList')

    __InspectionReport = collections.namedtuple('__InspectionReport',
        'cspArcTrdsOpList')

    __ProcessReport = collections.namedtuple('__ProcessReport',
            'processedList')

    def _doAcquireRunParameter(self, execParam):
        """
        The ACQUIRING RUN PARAMETER phase of the perform()
        """
        liveInstTrds = helper.LiveInstTrds(self.inst,
                    self._getWorldRef())
        allowed_trades = execParam.get('allowed_trades')
        if allowed_trades:
            setattr(liveInstTrds, 'allowed_trades', allowed_trades)

        cpArcTrds = liveInstTrds.GetLiveTrdsAndGenerateCPTrds(execParam, 2)
        runParam = self.__RunParam(cpArcTrdsList=cpArcTrds)
        return runParam

    def _doInspect(self, InspectList):

        OpList = []
        for cpArcTrds in InspectList:
            cspTrd = cpArcTrds[0]
            arcTrds = cpArcTrds[1]
            cspTrdOps = None
            if cspTrd:
                cspTrdOps = ('Create', 'Trade', cspTrd)

            arcTrdsOpList = []
            try:
                for trd in arcTrds:
                    archiveOp = utility.GetOpsToArchiveTrd(trd, self.deepArchive,
                        self._getWorldRef())
                    arcTrdsOpList.append(archiveOp)
                OpList.append((cspTrdOps, arcTrdsOpList))

            except Exception as ex:
                self._logError(str(ex))
                if not self.suppress_exceptions:
                    raise ex

        inspectionReport = self.__InspectionReport(cspArcTrdsOpList=OpList)
        return inspectionReport

    def _doProcess(self, inspectionReport):
        def process(opList):
            for opDetails in opList:
                cpTrdOp = opDetails[0]
                cpTrd = None
                if (cpTrdOp and cpTrdOp[0] == 'Create' and
                        cpTrdOp[1] == 'Trade'):
                    cpTrd = cpTrdOp[2]
                    utility.CreateTrade(cpTrd,
                            self._getWorldRef())

                arcTrdsOps = opDetails[1]
                for arcTrd in arcTrdsOps:
                    for obj in arcTrd:
                        if obj.opTyp == ACTION_ARCHIVE:
                            utility.ArchiveObj(obj.oid,
                                    obj.recTyp, self._getWorldRef(), cpTrd)

            return

        processedList = []
        #for (delTrdOp, DeArcTrdsOp) in inspectionReport:
        for opList in inspectionReport:
            result = _OUTCOME_OK
            try:
                utility.performTransaction(
                    self._getWorldRef(), process, opList=opList
                )
            except Exception as ex:
                errorMsg = str(ex)
                self._logError(errorMsg)
                result = _OUTCOME_FAIL
                if not self.suppress_exceptions:
                    raise ex

            processedList.append((result, opList))

        acm.PollDbEvents()
        # Make the process report
        processReport = self.__ProcessReport(processedList=processedList)
        return processReport

    def _doInspectReport(self, inspectionReport, inspectFailedList,
            inspectSuccessQueue):
        inspectSuccessQueue.append(inspectionReport)

    def _doProcessReport(self, processReport, processedFailedList,
            processedIgnoredList, processedSuccessList):
        return

    def _completeOperation(self, operationCompleted=None):
    
        if operationCompleted is not None:
            numTrds = ael.dbsql(
                'select count(trdnbr) from trade where insaddr = %s and archive_status = 0' % (self.inst))
            operationCompleted.append(FBDPCommon.get_result_in_list(numTrds)[0] == 0)


class _ArchiveInstrument(_NewExpirationPerformBase):
    """------------------------------------------------------------------------

    ------------------------------------------------------------------------"""

    def __init__(self, inst, log):
        _NewExpirationPerformBase.__init__(self, inst, log)

    def end(self):
        _NewExpirationPerformBase._end(self)

    def perform(self, execParam, operationCompleted=None):
        _NewExpirationPerformBase._perform(self, execParam, operationCompleted)

    __RunParam = collections.namedtuple('__RunParam', 'instList')

    __InspectionReport = collections.namedtuple('__InspectionReport',
        'instOp')

    __ProcessReport = collections.namedtuple('__ProcessReport', 'result, id')

    def _doAcquireRunParameter(self, execParam):
        """
        The ACQUIRING RUN PARAMETER phase of the perform()
        """
        if utility.isInstArchived(self.inst):
            runParam = self.__RunParam(instList=[])
        else:
            runParam = self.__RunParam(instList=[self.inst])

        return runParam

    def _doInspect(self, InspectList):

        archiveInstOps = []
        if len(InspectList) > 1:
            self.log.logError('UnExpected length of Inspection List')

        elif len(InspectList) == 1:
            oid = InspectList[0]
            archiveInstOps = utility.GetOpsToArchiveInstrument(oid, self.deepArchive,
                        self._getWorldRef())
        inspectionReport = self.__InspectionReport(instOp=archiveInstOps)

        return inspectionReport

    def _doProcess(self, inspectionReport):
        def process():
            for opDetails in inspectionReport:
                for arcInst in opDetails:
                    if arcInst.opTyp == ACTION_ARCHIVE:
                        utility.ArchiveObj(arcInst.oid,
                                arcInst.recTyp, self._getWorldRef(), None)

            return

        r = _OUTCOME_OK
        try:
            utility.performTransaction(
                self._getWorldRef(), process
            )
        except Exception as ex:
            errorMsg = str(ex)
            self._logError(errorMsg)
            r = _OUTCOME_FAIL
            if not self.suppress_exceptions:
                raise ex

        acm.PollDbEvents()
        # Make the process report
        processReport = self.__ProcessReport(result=r, id=self.inst)
        return processReport

    def _doInspectReport(self, inspectionReport, inspectFailedList,
                inspectSuccessQueue):
        inspectSuccessQueue.append(inspectionReport)

    def _doProcessReport(self, processReport, processedFailedList,
            processedIgnoredList, processedSuccessList):
        return


class _DearchiveInstrument(_NewExpirationPerformBase):
    """------------------------------------------------------------------------

    ------------------------------------------------------------------------"""

    def __init__(self, inst, log):
        _NewExpirationPerformBase.__init__(self, inst, log)

    def end(self):
        _NewExpirationPerformBase._end(self)

    def perform(self, execParam, operationCompleted=None):
        _NewExpirationPerformBase._perform(self, execParam, operationCompleted)

    __RunParam = collections.namedtuple('__RunParam', 'arcInst')

    __InspectionReport = collections.namedtuple('__InspectionReport',
        'instOpList')

    __ProcessReport = collections.namedtuple('__ProcessReport', 'result, id')

    def _doAcquireRunParameter(self, execParam):
        """
        The ACQUIRING RUN PARAMETER phase of the perform()
        """

        if utility.isInstArchived(self.inst):
            runParam = self.__RunParam(arcInst=[self.inst])
        else:
            runParam = self.__RunParam(arcInst=[])

        return runParam

    def _doInspect(self, InspectList):

        deArchiveOp = []
        if len(InspectList) > 1:
            self.log.logError('UnExpected length of Inspection List')
        elif len(InspectList) == 1:
            oid = InspectList[0]
            deArchiveOp.append(utility.Oplet(
                ACTION_DEARCHIVE, 'Instrument', oid))

        inspectionReport = self.__InspectionReport(instOpList=deArchiveOp)
        return inspectionReport

    def _doProcess(self, inspectionReport):
        def process():
            for opDetails in inspectionReport:
                for deArcInst in opDetails:
                    if deArcInst.opTyp == ACTION_DEARCHIVE:
                        utility.DeArchiveInst(deArcInst.oid, self.deepArchive,
                            self._getWorldRef())

            return

        r = _OUTCOME_OK
        try:
            utility.performTransaction(
                self._getWorldRef(), process
            )
        except Exception as ex:
            errorMsg = str(ex)
            self._logError(errorMsg)
            r = _OUTCOME_FAIL
            if not self.suppress_exceptions:
                raise ex

        acm.PollDbEvents()
        # Make the process report
        processReport = self.__ProcessReport(result=r, id=self.inst)
        return processReport

    def _doInspectReport(self, inspectionReport, inspectFailedList,
            inspectSuccessQueue):
        inspectSuccessQueue.append(inspectionReport)

    def _doProcessReport(self, processReport, processedFailedList,
            processedIgnoredList, processedSuccessList):
        return


class _DeleteInstrument(_NewExpirationPerformBase):
    """------------------------------------------------------------------------

    ------------------------------------------------------------------------"""

    def __init__(self, inst, log):
        _NewExpirationPerformBase.__init__(self, inst, log)

    def end(self):
        _NewExpirationPerformBase._end(self)

    def perform(self, execParam, operationCompleted=None):
        _NewExpirationPerformBase._perform(self, execParam, operationCompleted)

    __RunParam = collections.namedtuple('__RunParam', 'arcInst')

    __InspectionReport = collections.namedtuple('__InspectionReport',
        'instOpList')

    __ProcessReport = collections.namedtuple('__ProcessReport', 'result, id')

    def _doAcquireRunParameter(self, execParam):
        """
        The ACQUIRING RUN PARAMETER phase of the perform()
        """

        runParam = self.__RunParam(arcInst=[self.inst])
        return runParam

    def _doInspect(self, InspectList):
        delOp = []
        if len(InspectList) > 1:
            self.log.logError('UnExpected length of Inspection List')

        elif len(InspectList) == 1:
            oid = InspectList[0]
            delOp.append(utility.Oplet(
                ACTION_DELETE, 'Instrument', oid))

        inspectionReport = self.__InspectionReport(instOpList=delOp)
        return inspectionReport

    def _doProcess(self, inspectionReport):

        r = _OUTCOME_OK
        try:
            for opDetails in inspectionReport:
                for delInst in opDetails:
                    if delInst.opTyp == ACTION_DELETE:
                        utility.DeleteInstrument(delInst.oid,
                                delInst.recTyp, self._getWorldRef())
        except Exception as ex:
            errorMsg = str(ex)
            self._logError(errorMsg)
            ael.abort_transaction()
            r = _OUTCOME_FAIL
            if not self.suppress_exceptions:
                raise ex

        acm.PollDbEvents()
        # Make the process report
        processReport = self.__ProcessReport(result=r, id=self.inst)
        return processReport

    def _doInspectReport(self, inspectionReport, inspectFailedList,
            inspectSuccessQueue):
        inspectSuccessQueue.append(inspectionReport)

    def _doProcessReport(self, processReport, processedFailedList,
            processedIgnoredList, processedSuccessList):
        return

class _DeleteArchiveTrades(_NewExpirationPerformBase):

    def __init__(self, inst, log):
        _NewExpirationPerformBase.__init__(self, inst, log)

    def end(self):
        _NewExpirationPerformBase._end(self)

    def perform(self, execParam, operationCompleted=None):
        _NewExpirationPerformBase._perform(self, execParam, operationCompleted)

    __RunParam = collections.namedtuple('__RunParam', 'cpArcTrdsList')

    __InspectionReport = collections.namedtuple('__InspectionReport',
        'OpDeArcDeleteList')

    __ProcessReport = collections.namedtuple('__ProcessReport',
            'processedList')

    def _doAcquireRunParameter(self, execParam):
        arcTrds = helper.ArchivedInstTrds(self.inst,
                self._getWorldRef())
        allowed_trades = execParam.get('allowed_trades')
        if allowed_trades:
            setattr(arcTrds, 'allowed_trades', allowed_trades)

        #Get the archived trades and its cashposing trades.
        cpArcTrdsList = arcTrds.GetArchivedTrdsAndItsCPTrds(execParam,
                True)
        runParam = self.__RunParam(cpArcTrdsList=cpArcTrdsList)
        return runParam

    def _doInspect(self, cpArcTrdsList):
        OpList = []
        if cpArcTrdsList is None:
            inspectionReport = self.__InspectionReport(
                OpDeArcDeleteList=OpList
            )
            return inspectionReport

        for cpArcTrds in cpArcTrdsList:
            cpTrd = cpArcTrds.cpTrds
            arcTrdList = cpArcTrds.arcTrds

            for oid in arcTrdList:
                OpList.append(utility.Oplet(
                    ACTION_DELETE, 'Trade', oid))

            #We want to keep the cashposting trade, no deletion operation here.

        inspectionReport = self.__InspectionReport(OpDeArcDeleteList=OpList)
        return inspectionReport

    def _doProcess(self, inspectionReport):

        processedList = []
        #for (delTrdOp, DeArcTrdsOp) in inspectionReport:
        for opList in inspectionReport:
            result = _OUTCOME_OK
            try:
                for obj in opList:
                    if obj.opTyp == ACTION_DELETE:
                        utility.DeleteTrade(obj.oid, obj.recTyp,
                                self._getWorldRef())

            except Exception as ex:
                ael.abort_transaction()
                result = _OUTCOME_FAIL
                if not self.suppress_exceptions:
                    raise ex

            acm.PollDbEvents()
            processedList.append((result, opList))

        # Make the process report
        processReport = self.__ProcessReport(processedList=processedList)
        return processReport

    def _doInspectReport(self, inspectionReport, inspectFailedList,
            inspectSuccessQueue):
        inspectSuccessQueue.append(inspectionReport)

    def _doProcessReport(self, processReport, processedFailedList,
            processedIgnoredList, processedSuccessList):
        pass

class _DeleteLiveTrades(_NewExpirationPerformBase):

    def __init__(self, inst, log):
        _NewExpirationPerformBase.__init__(self, inst, log)

    def end(self):
        _NewExpirationPerformBase._end(self)

    def perform(self, execParam, operationCompleted=None):
        _NewExpirationPerformBase._perform(self, execParam, operationCompleted)

    __RunParam = collections.namedtuple('__RunParam', 'cpDelTrdsList')

    __InspectionReport = collections.namedtuple('__InspectionReport',
        'cspDelTrdsOpList')

    __ProcessReport = collections.namedtuple('__ProcessReport',
            'processedList')

    def _doAcquireRunParameter(self, execParam):

        liveInstTrds = helper.LiveInstTrds(self.inst,
                    self._getWorldRef())
        allowed_trades = execParam.get('allowed_trades')
        if allowed_trades:
            setattr(liveInstTrds, 'allowed_trades', allowed_trades)

        genCP = 0
        if execParam['preservePL']:
            genCP = 2

        cpDelTrds = liveInstTrds.GetLiveTrdsAndGenerateCPTrds(execParam, genCP)
        runParam = self.__RunParam(cpDelTrdsList=cpDelTrds)

        return runParam

    def _doInspect(self, InspectList):

        OpList = []
        for cpDelTrds in InspectList:
            cspTrd = cpDelTrds[0]
            delTrds = cpDelTrds[1]
            cspTrdOps = None
            if cspTrd:
                cspTrdOps = ('Create', 'Trade', cspTrd)

            delOpTrds = []
            try:
                for trd in delTrds:
                    #delete the trades
                    delOpTrds.append(utility.Oplet(
                        ACTION_DELETE, 'Trade', trd.Oid()))

                OpList.append((cspTrdOps, delOpTrds))

            except Exception as ex:
                self._logError(str(ex))
                if not self.suppress_exceptions:
                    raise ex

        inspectionReport = self.__InspectionReport(cspDelTrdsOpList=OpList)
        return inspectionReport

    def _doProcess(self, inspectionReport):

        processedList = []
        for opList in inspectionReport:
            result = _OUTCOME_OK
            try:
                for opDetails in opList:
                    cpTrdOp = opDetails[0]
                    cpTrd = None
                    if (cpTrdOp and cpTrdOp[0] == 'Create' and
                            cpTrdOp[1] == 'Trade'):
                        cpTrd = cpTrdOp[2]
                        utility.CreateTrade(cpTrd,
                                    self._getWorldRef())

                    delTrdsOps = opDetails[1]
                    for obj in delTrdsOps:
                        if obj.opTyp == ACTION_DELETE:
                            utility.DeleteTrade(obj.oid, obj.recTyp,
                                    self._getWorldRef())

            except Exception as ex:
                self._logError(str(ex))
                result = _OUTCOME_FAIL
                if not self.suppress_exceptions:
                    raise ex

            acm.PollDbEvents()
            processedList.append((result, opList))

        # Make the process report
        processReport = self.__ProcessReport(processedList=processedList)
        return processReport

    def _doInspectReport(self, inspectionReport, inspectFailedList,
            inspectSuccessQueue):
        inspectSuccessQueue.append(inspectionReport)

    def _doProcessReport(self, processReport, processedFailedList,
            processedIgnoredList, processedSuccessList):
        pass

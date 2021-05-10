
import FPaceConsumer
import FPaceCoreTypes

GOOD_TASK_STATES = (FPaceCoreTypes.RTS_VALID,)
BAD_TASK_STATES = (FPaceCoreTypes.RTS_INVALID, FPaceCoreTypes.RTS_EXCEPTION, FPaceCoreTypes.RTS_BROKEN)

GOOD_DISPATCHER_STATES = (FPaceCoreTypes.RTDS_INFANT, FPaceCoreTypes.RTDS_PENDING_CREATE, FPaceCoreTypes.RTDS_ATTACHED)
BAD_DISPATCHER_STATES = (FPaceCoreTypes.RTDS_BROKEN, FPaceCoreTypes.RTDS_DETACHED)

class Consumer(FPaceConsumer.Events): # Events is an interface
    def __init__(self, updateParamsCb, signalBadStateCb, signalGoodStateCb):
        self._paceConsumer = None
        self._taskName = 'FrontArena.SpanLiveParams'
        self._updateParamsCb = updateParamsCb
        self._signalBadStateCb = signalBadStateCb
        self._signalGoodStateCb = signalGoodStateCb

    def __del__(self):
        self.Destroy()

    def Destroy(self):
        self._paceConsumer.Destroy()

    def DoCreate(self, definition):
        self._paceConsumer = FPaceConsumer.Create(self._taskName, definition)
        self._paceConsumer.AddObserver(self)

    def OnDelete(self, resultKey):
        pass
    
    def OnUpdateOrInsert(self, resultKey, result):
        self._updateParamsCb(int(resultKey.ins_oid), list(result.riskarray), result.delta)    
        
    def OnSignalGoodState(self):
        self._signalGoodStateCb()

    def OnSignalBadState(self):
        self._signalBadStateCb()

    def OnResultUpdated(self, resultKey, resultEvent, result):
        if resultEvent.number == FPaceCoreTypes.RE_INSERT:
            self.OnUpdateOrInsert(resultKey, result)
        elif resultEvent.number == FPaceCoreTypes.RE_UPDATE:
            self.OnUpdateOrInsert(resultKey, result)
        elif resultEvent.number == FPaceCoreTypes.RE_DELETE:
            self.OnDelete(resultKey)

        self.OnSignalState()

    def OnSignalState(self):
        task_state = self._paceConsumer.TaskState().number
        dispatcher_state = self._paceConsumer.DispatcherState().number
        if (task_state in GOOD_TASK_STATES and
            dispatcher_state in GOOD_DISPATCHER_STATES):
            self.OnSignalGoodState()
        else:
            self.OnSignalBadState()

    def OnTaskState(self):
        self.OnSignalState()

    def OnDispatcherState(self):
        self.OnSignalState()
        
    def OnInitialPopulateDone(self):
        pass
            

    @staticmethod
    def Create(traitsModule, updateParamsCb, signalBadStateCb, signalGoodStateCb, storedQueryOid):
        consumer = Consumer(updateParamsCb, signalBadStateCb, signalGoodStateCb)
        task_def = traitsModule.Definition()
        task_def.query_oid = storedQueryOid
        consumer.DoCreate(task_def)
        return consumer


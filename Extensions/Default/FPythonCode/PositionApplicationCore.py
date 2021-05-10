import acm
import FPaceConsumer
import FPaceCoreTypes

class TaskListenerBase( FPaceConsumer.Events, object):
    def __init__(self):
        self.m_consumer = None
        self.m_statusMessage = None
        self.m_isDone = False
        self.m_progress = 0
        self.m_msg = acm.Message.CreateMessageSend(self, 'Changed', [])
        self.m_owner = None
        self.m_encounteredErrors = 0
    
    def AddOwner(self, owner):
        self.m_owner = owner
        
    def Changed(self):
        self.m_msg.Value()

    def Create(self, definition):
        self.m_consumer = self.PrivateCreateTaskFromDefinition(definition)
        self.m_consumer.AddObserver(self)

    @classmethod
    def CreateActivity(Cls, definition):
        taskListener = Cls()
        taskListener.Create(definition)
        activity = acm.AsyncTask.NewActivity(taskListener, 'Task ' + str(taskListener.ObserverId()))
        taskListener.AddOwner(activity)
        return activity

    # FActivitySubjectAdapter interface
    def Destroy(self):
        if self.m_consumer:
            self.m_consumer.RemoveObserver(self)
            self.m_consumer.Destroy()
            self.m_consumer = None

    def IsDone(self):
        return self.m_isDone
        
    def Progress(self):
        return self.m_progress

    def StatusMessage(self):
        return self.m_statusMessage
    # --------------------------------
    
    def ObserverId(self):
        return self.m_consumer.ObserverId()

    def OnDispatcherState(self):
        pass
    
    def OnInitialPopulateDone(self):
        self.PrivateOnInitialPopulateDone()
        self.m_isDone = True
        self.Changed()
        self.m_owner.Destroy()
        
    def OnProgressUpdated(self, percent, progressText):
        if not self.m_isDone:
            self.m_progress = percent
            if self.m_statusMessage != progressText:
                self.m_statusMessage = progressText
            self.Changed()
        
    def OnResultUpdated(self, resultKey, resultEvent, result):
        if resultEvent.number == FPaceCoreTypes.RE_INSERT:
            self.PrivateOnResultUpdated(resultKey, resultEvent, result)
            self.Changed()

    def OnTaskState(self):
        taskState = self.m_consumer.TaskState().number
        if FPaceCoreTypes.RTS_VALID != taskState:
            self.m_statusMessage = self.m_consumer.StatusText()
            if FPaceCoreTypes.RTS_EXCEPTION == taskState:
                self.m_isDone = true
            self.Changed()
    
    def PrivateCreateTaskFromDefinition(self, definition):
        raise NotImplementedError
        
    def PrivateOnInitialPopulateDone(self):
        raise NotImplementedError
        
    def PrivateOnResultUpdated(self, resultKey, resultEvent, result):
        raise NotImplementedError

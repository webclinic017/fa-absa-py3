
import acm
# Pace Core Consumer
import FPaceConsumer
import FPaceCoreTypes

# Traits 
import IndexSearchScopeTraits
import IndexSearchQueryTraits

from IndexSearchConstants import TaskKeys

from IndexSearchUtils import unicode_encode
import uuid

def create_uuid() :
    return str(uuid.uuid4())    
#-------------------------------------------------------
# QueryTaskConsumer class
# - Inherits from python object and implements the FPaceConsumer.Events
#-------------------------------------------------------
class QueryTaskConsumer(FPaceConsumer.Events, object):
    def __init__(self, onResultCB):
        self._taskName = TaskKeys.Query
        self._onResultCB = onResultCB
        self._paceConsumer = None
            
    #-------------------------------------------------------
    #   Destory the created consumer and child consumers
    #-------------------------------------------------------
    def Destroy(self):
        if self._paceConsumer :
            self._paceConsumer.Destroy()
            self._paceConsumer = None
    
    def CreateChild(self, taskName, definition, parentConsumer, scope):
        consumer = FPaceConsumer.PaceConsumer.PrivateSetup(taskName, scope)
        definitionMessage = definition.SerializeToString()
        consumer._observerId = consumer._consumerStub.CreateChildTask(definitionMessage, parentConsumer.ObserverId(), '', parentConsumer._consumerStub, consumer)
        return consumer
    #-------------------------------------------------------
    #   Creates a child consumer with definition, with parentPaceConsumer and parentResultKey
    #-------------------------------------------------------
    def DoSearch(self, query, page, pageSize, parentPaceConsumer, scope):
        definition = IndexSearchQueryTraits.Definition()
        definition.query = query
        definition.page = page
        definition.pageSize = pageSize
        definition.uuid = create_uuid()

        self.Destroy()
        self._paceConsumer = self.CreateChild(self._taskName, definition, parentPaceConsumer, scope)
        self._paceConsumer.AddObserver(self)
        
    #-------------------------------------------------------
    # - FPaceCoreConsumer.Events Override
    #   Overriden to be able to receive result updates.
    #-------------------------------------------------------
    def OnResultUpdated(self, resultKey, resultEvent, result):  
        if self._onResultCB :
            self._onResultCB(result)

        
class ScopeTaskConsumer(FPaceConsumer.Events, object):
    def __init__(self, indexName, onResultCB, onProgressCB, stateCB, initialPopulateDoneCB):
        self._taskName = TaskKeys.Scope
        self._indexName = indexName
        self._onResultCB = onResultCB
        self._onProgressCB = onProgressCB
        self._onOutputCB = None
        self._stateCB = stateCB
        self._initialPopulateDoneCB = initialPopulateDoneCB
        self._scope = None

    def PaceConsumer(self):
        return self._paceConsumer

    #-------------------------------------------------------
    #   Destory the created consumer and child consumers
    #-------------------------------------------------------
    def Destroy(self):
        self._paceConsumer.Destroy()

    def InitScope(self) :
        self._scope = None
        storedCalulationEnvironment = acm.ConfigurationParameter.GetValue(acm.User(), 'defaultIndexSearchEnvironment' )
        if storedCalulationEnvironment :
            self._scope = acm.PACE.ScopeFromStoredEnvironment(storedCalulationEnvironment)

    def Scope(self) :
        return self._scope
    #-------------------------------------------------------
    #   Create a scope consumer with definition
    #-------------------------------------------------------
    def DoCreate(self):
        definition = IndexSearchScopeTraits.Definition()
        definition.id = 0
        definition.indexName = self._indexName

        self.InitScope()

        self._paceConsumer = FPaceConsumer.Create(self._taskName, definition, unicode_encode(self._indexName), self.Scope())
        self._paceConsumer.AddObserver(self)

    #-------------------------------------------------------
    #   Redirect output to registered output handler
    #-------------------------------------------------------
    def OnOutput(self, output):
        if self._onOutputCB :
            self._outputCB(output)
        
    #-------------------------------------------------------
    # - FPaceCoreConsumer.Events Override
    #   Overriden to be able to receive result updates.
    #   - Prints the scope task update id and value and creates 
    #     a child consumer per update.
    #-------------------------------------------------------
    def OnResultUpdated(self, resultKey, resultEvent, result):  
        if self._onResultCB :
            self._onResultCB(result)       

    def OnInitialPopulateDone(self) :
        if self._initialPopulateDoneCB :
            self._initialPopulateDoneCB()

    #-------------------------------------------------------
    # - FPaceCoreConsumer.Events Override
    #   Overriden to be able to fetch and print the dispatcher state when it change.
    #   Only implemented for the scope task since a master and a child task always share dispatcher.
    #-------------------------------------------------------
    def OnDispatcherState(self):
        if self._stateCB:
            self._stateCB(self._paceConsumer.DispatcherState().name, self._paceConsumer.StatusText())        
        # print ('DispatcherState: ' + self._paceConsumer.DispatcherState().name + ' Status: ' + self._paceConsumer.StatusText())
    
    #-------------------------------------------------------
    # - FPaceCoreConsumer.Events Override
    #   Overriden to be able to fetch and print the scope task state when it change.
    #-------------------------------------------------------
    def OnTaskState(self):
        pass
        #print ('TaskState: ' + self._paceConsumer.TaskState().name + ' Status: ' + self._paceConsumer.StatusText())
    
    #-------------------------------------------------------
    # - FPaceCoreConsumer.Events Override
    #   Overriden to be able to print the progress of the scope or/and query task.
    #-------------------------------------------------------
    def OnProgressUpdated(self, percent, progressText):
        if self._onProgressCB :
            self._onProgressCB(percent, progressText)    
        
    #-------------------------------------------------------
    #   Use to create a scope consumer
    #-------------------------------------------------------
    @staticmethod
    def Create(indexName, onResultCB, onProgressCB, stateCB, initialPopulateDoneCB):
        consumer = ScopeTaskConsumer(indexName, onResultCB, onProgressCB, stateCB, initialPopulateDoneCB)
        consumer.DoCreate()
        return consumer
        

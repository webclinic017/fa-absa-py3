""" Compiled: 2015-09-23 14:33:50 """

import FPaceProducer
import FOrderValidationCalculation
import acm
import traceback


class FOrderValidationProducerBase(FPaceProducer.Producer):
    def __init__(self):
        super(FOrderValidationProducerBase, self).__init__()
        self._space = FOrderValidationCalculation.Space.Instance
        self._tasks = {}
        
    '''
        Pace Core interface
    '''
    def OnCreateTask(self, taskId, request):
        try:
            prf = acm.FPhysicalPortfolio[ int(request.portfolio_oid) ] #why long for int32?
            self._tasks.setdefault( prf, {} )[ taskId ] = request
            self.HandleRequest( prf, request )
            self.SendInitialPopulateDone( taskId )
        except:
            self.SendException( taskId, traceback.format_exc() )

    def OnDoPeriodicWork(self):
        self.DoWork()

    def OnDestroyTask(self, taskId):
        for taskData in list(self._tasks.values()):
            if taskId in taskData:
                taskData.pop( taskId )

    '''
        Interface for subclasses to FOrderValidationProducerBase.FOrderValidationProducerBase
    '''
    def HandleRequest(self, prf, request):
        raise RuntimeError('*** Not implemented ***')

    def DoWork(self, **kwargs):
        raise RuntimeError('*** Not implemented ***')


class FQueuingProducer(FOrderValidationProducerBase):
    _busy = False
    def __init__(self):
        super(FQueuingProducer, self).__init__()
        self._queued = []

    def OnCreateTask(self, taskId, request):
        self._queued.append( ( self, ( taskId, request ) ) )
        self.OnDoPeriodicWork()

    def OnDoPeriodicWork(self):
        # Checking the "_busy" attribute is done to resolve re-entrancy issues (but is not thread-safe, since the use-case is assumed to be for a PACE producer, always invoked on the main thread)
        if FQueuingProducer._busy:
            return

        try:
            FQueuingProducer._busy = True
            if self._queued:
                instance, args = self._queued.pop( 0 )
                return FOrderValidationProducerBase.OnCreateTask( instance, * args )
            else:
                return FOrderValidationProducerBase.OnDoPeriodicWork( self )
        finally:
            FQueuingProducer._busy = False

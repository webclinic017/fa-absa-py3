""" Compiled: 2015-09-23 14:33:50 """

import FOrderValidationProducerBase
import FOrderValidationOrderIdMessages

def CreateProducer():
    return FValidationOrderIdProducer()

class FValidationOrderIdProducer(FOrderValidationProducerBase.FQueuingProducer):
    '''
        Interface for subclasses to FOrderValidationProducerBase.FOrderValidationProducerBase
    '''
    def HandleRequest(self, prf, request):
        # When calling HandleRequest, all current rows for this portfolio are retrieved
        portfolio = self._space.HandleRequest( prf )
        self.DoWork( portfolios = [ portfolio ] )
        
    def DoWork(self, *args, **kwargs):
        updated = self._space.GetUpdatedOrders( *args, **kwargs )
        self.HandleResult( updated ) 
    
    def HandleResult(self, updated):
        for prf, orderIds in updated.items():
            for taskId, request in self._tasks.get( prf, {} ).items():
                for orderId, versions in orderIds.items():
                    self.SendResult( taskId, request, prf, orderId, versions )

    def SendResult(self, taskId, request, prf, orderId, versions):
        resultKey = FOrderValidationOrderIdMessages.ResultKey()
        resultKey.portfolio_oid = prf.Oid()
        resultKey.order_id = orderId

        result = FOrderValidationOrderIdMessages.Result()
        updated = False
        deleted = False

        for state, data in versions:
            if state == False:
                deleted = True
                continue # Will trigger a SendDelete() below, no useful data to insert into InsertOrUpdate(), so continue with next state - although there shouldn't be any next state for a deleted order
            else:
                updated = True
                id, qty = data
                version = result.version.add()
                version.id = id
                version.quantity = qty

        if updated:
            self.SendInsertOrUpdate( taskId, resultKey, result )
        
        if deleted:
            self.SendDelete( taskId, resultKey )

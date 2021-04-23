""" Compiled: 2015-09-23 14:33:50 """

import FOrderValidationProducerBase
import FOrderValidationCalculationPbUtils as utils

def CreateProducer():
    return FValidationCalculationProducer()

class FValidationCalculationProducer(FOrderValidationProducerBase.FQueuingProducer):
    '''
        Interface for subclasses to FOrderValidationProducerBase.FOrderValidationProducerBase
    '''
    def HandleRequest(self, prf, request):
        # When calling HandleRequest, all current rows for this portfolio are retrieved
        portfolio = self._space.HandleRequest( prf, [str(x) for x in request.portfolio_column_id], [str(x) for x in request.position_column_id], request.active_orders )
        self.DoWork( portfolios = [ portfolio ], updatedOnly = False )
        
    def DoWork(self, *args, **kwargs):
        updated = self._space.GetUpdatedCalulcations( *args, **kwargs )
        self.HandleResult( updated ) 
    
    def HandleResult(self, updated):
        for prf, rows in updated.items():
            for taskId, request in self._tasks.get( prf, {} ).items():
                for rowObject, ( row, ssl, orderInfo ) in rows.items():
                    self.SendResult( taskId, request, prf, rowObject, row, ssl, orderInfo )

    def SendResult(self, taskId, request, prf, rowObject, row, ssl, orderInfo):
        if row:
            calculations = row.Current()
        elif ssl:
            calculations = { 'Total Available To Sell' : ssl.Current()[ 'Total Available To Sell' ] }
        else:
            calculations = {}
            
        resultKey, result = utils.createKeyAndResultMessage( rowObject, calculations, orderInfo, request )

        self.SendInsertOrUpdate( taskId, resultKey, result )

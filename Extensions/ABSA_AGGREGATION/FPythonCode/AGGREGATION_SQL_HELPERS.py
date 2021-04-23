
import acm, ael
from FBDPCurrentContext import Logme
from AGGREGATION_GEN_HELPERS import GENERIC_HELPERS

class TRADE_SQL_HELPERS():
    def setArchiveStatusAggregateTrdnbnrAggregate(self, trdnbrs, archiveFlag, aggTradeId, aggregate, selectionAttribute):
        helpers = GENERIC_HELPERS()
        nbrOfTrades = len(trdnbrs)
        idx = 0
        while idx < len(trdnbrs):
            lower = idx
            if idx + 1000 > len(trdnbrs):
                upper = len(trdnbrs)
            else:
                upper = idx + 1000
                
            Logme()('DEBUG: Setting archive_status, aggregate_trdnbr and aggregate %i to %i from a total of: %i trades' %(lower, upper, nbrOfTrades), 'DEBUG')
            query = r'''
            UPDATE trade
            SET updat_usrnbr = %i, updat_time = GETDATE(), archive_status = %i, aggregate_trdnbr = %s, aggregate = %i
            WHERE %s in (%s)
            SELECT @@ROWCOUNT
            ''' %(acm.User().Oid(), archiveFlag, aggTradeId, aggregate, selectionAttribute, ','.join([str(trade) for trade in trdnbrs[lower:upper]]))
            Logme()(query, 'DEBUG')
            result = ael.dbsql(query)
            if archiveFlag == 1:
                action = 'Archive'
            else:
                action = 'De-Archive'
            helpers.addToSummary('Trade', action, result[0][0][0])
            idx = idx + 1000

    def getAggregateTrades(self, trdnbrs, archiveFlag):
        totalTradeList = []
        nbrOfTrades = len(trdnbrs)
        idx = 0
        while idx < len(trdnbrs):
            lower = idx
            if idx + 1000 > len(trdnbrs):
                upper = len(trdnbrs)
            else:
                upper = idx + 1000
                
            Logme()('DEBUG: Selecting Aggregate trades %i to %i from a total of: %i trades' %(lower, upper, nbrOfTrades), 'DEBUG')
            query = r'''
            SELECT trdnbr
            FROM trade
            WHERE aggregate_trdnbr in (%s)
            AND archive_status = %i
            ''' %(','.join([str(trade) for trade in trdnbrs[lower:upper]]), archiveFlag)
            Logme()(query, 'DEBUG')
            result = ael.dbsql(query)
            idx = idx + 1000
            
            for item in result[0]:
                if item[0] not in totalTradeList:
                    totalTradeList.append(item[0])
        return totalTradeList

class SQL_HELPERS():
    def getObjectsFromSelectionObject(self, selectionObject, addInfoRecType = None):
        self.__selectionObject = selectionObject
        
        objectList = []
        nbrOfObject = len(self.__selectionObject.primarySelectionTuple[1])
        idx = 0
        while idx < nbrOfObject:
            lower = idx
            if idx + 1000 > nbrOfObject:
                upper = nbrOfObject
            else:
                upper = idx + 1000
            
            additionalCriteria = ''
            #'AND archive_status = 0'
            #('AND', 'archive_status', '=', '0')
            for item in self.__selectionObject.selectionList:
                additionalCriteria = ' %s %s %s %s %s' %(additionalCriteria, item[0], item[1], item[2], item[3])
            
            Logme()('DEBUG: Selecting %s %i to %i from a total of: %i %s' %(self.__selectionObject.fromTable, lower, upper, nbrOfObject, self.__selectionObject.primarySelectionTuple[0]), 'DEBUG')
            if addInfoRecType == None:
                query = r'''
                SELECT DISTINCT %s
                FROM %s
                WHERE %s in (%s)
                %s
                ''' %(self.__selectionObject.returnAttribute, self.__selectionObject.fromTable, self.__selectionObject.primarySelectionTuple[0], ','.join([str(object) for object in self.__selectionObject.primarySelectionTuple[1][lower:upper]]), additionalCriteria)
            else:
                query = r'''
                SELECT DISTINCT o.%s
                FROM %s o, additional_info_spec ais
                WHERE o.%s in (%s) and o.addinf_specnbr = ais.specnbr and ais.rec_type = %i
                %s
                ''' %(self.__selectionObject.returnAttribute, self.__selectionObject.fromTable, self.__selectionObject.primarySelectionTuple[0], ','.join([str(object) for object in self.__selectionObject.primarySelectionTuple[1][lower:upper]]), addInfoRecType, additionalCriteria)

            Logme()(query, 'DEBUG')
            result = ael.dbsql(query)
            idx = idx + 1000
            
            for item in result[0]:
                if item[0] not in objectList:
                    objectList.append(item[0])

        return objectList

    def archiveObjects(self, objects, table, attribute, usernbr, archiveFlag):
        helpers = GENERIC_HELPERS()
        Logme()('Total %s to archive: %i' %(table, len(objects)), 'DEBUG')
        if len(objects) == 0: return
        
        idx = 0
        while idx < len(objects):
            lower = idx
            if idx + 1000 > len(objects):
                upper = len(objects)
            else:
                upper = idx+1000
            
            Logme()('Archiving index %i to %i from a total of: %i' %(lower, upper, len(objects)), 'DEBUG')
            try:
                query = r'''
                UPDATE %s
                SET updat_usrnbr = %i, updat_time = GETDATE(), archive_status = %i
                WHERE %s in (%s) and archive_status <> %i
                SELECT @@ROWCOUNT
                ''' %(table, usernbr, archiveFlag, attribute, ','.join([str(object) for object in objects[lower:upper]]), archiveFlag)
                Logme()(query, 'DEBUG')
                result = ael.dbsql(query)
                
                if archiveFlag == 1:
                    action = 'Archive'
                else:
                    action = 'De-Archive'

                helpers.addToSummary(table, action, result[0][0][0])
            except Exception as e:
                msg = 'ERROR: Aborting Transaction: Archiving Objects. {0}'.format(e)
                Logme()(msg, 'ERROR')
                Logme()(query, 'ERROR')
                raise Exception(msg)
                
            idx = idx + 1000

class INSTRUMENT_SQL_HELPERS():
    def getInstrumentsWithNonArchiveTrades(self, insaddrs):
        nbrObjects = len(insaddrs)
        instrumentList = []
        idx = 0
        while idx < nbrObjects:
            lower = idx
            if idx + 1000 > nbrObjects:
                upper = nbrObjects
            else:
                upper = idx+1000
            
            Logme()('Selecting instruments with non archive trades: index %i to %i from a total of: %i' %(lower, upper, nbrObjects), 'DEBUG')
            
            objectQuery = r'''
            SELECT DISTINCT i.insaddr
            FROM instrument i, trade t
            WHERE i.insaddr in (%s)
            AND i.insaddr = t.insaddr
            AND t.archive_status = 0
            ''' %(','.join([str(object) for object in insaddrs[lower:upper]]))
            
            Logme()(objectQuery, 'DEBUG')
            
            objectResult = ael.dbsql(objectQuery)
            
            idx = idx + 1000
            
            for objectItem in objectResult[0]:
                if objectItem[0] not in instrumentList:
                    instrumentList.append(objectItem[0])
        
        return instrumentList

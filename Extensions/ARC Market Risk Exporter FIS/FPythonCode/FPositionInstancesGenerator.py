""" Compiled: 2020-08-14 16:40:05 """

#__src_file__ = "extensions/arc_writers/./etc/FPositionInstancesGenerator.py"
import acm
from FBDPCurrentContext import Logme
from FBDPCurrentContext import Summary
import FPositionUtils


def perform(log, execParam):
    taskNames = execParam['Tasks']
    posSpec = execParam['PositionSpecification']
    for n in taskNames:
        task = acm.FAelTask[n]
        if not task:
            Logme()("No task {0} found".format(n), "WARNING")
            continue

        posIntancePerform = FPosInstanceGenerator(task, posSpec)
        posIntancePerform.Perform(log)

class FPosInstanceGenerator:

    def __init__(self, aelTask, positionSpec):
        self._aelTask = aelTask
        self._posSpec = positionSpec
        self._taskParams = self._aelTask.Parameters()
        self._origPortfs = self._taskParams.At('portfolios', None)
        self._origQueries = self._taskParams.At('storedASQLQueries', None)
        self._origTradFilters = self._taskParams.At('tradeFilters', None)
        
    def valid(self):
        if self._origTradFilters:
            Logme()("No support to split task {0} with trade filter specified. ".format(self._aelTask.Name()), "WARNING")
            return False
        return True

    def __getTradesOnSingleObj(self, obj, type, trades):
    
        if len(obj) == 0:
            return trades

        trds = []
        if type == 'portfolios':
            p = acm.FPhysicalPortfolio[obj]
            if p:
                trds = p.Trades()
        elif type =='tradeFilters':
            trdFilter = acm.FTradeSelection[obj]
            if trdFilter:
                trds = trdFilter.Trades()
        elif type == 'storedASQLQueries':
            q = acm.FStoredASQLQuery[obj]
            if q:
                trds = q.Query().Select()

        for t in trds:
            trades.append(t)
        
        return trades
 
    def __getTrades(self, objs, type, trades):
        if not objs or len(objs) == 0:
            return trades
        
        if isinstance(objs, str):
            return self.__getTradesOnSingleObj(objs, type, trades)
            
        if isinstance(objs, list):
            for o in objs:
                trades = self.__getTradesOnSingleObj(o, type, trades)
        return trades

    def __addPortfsInQuery(self, q):
        portfolios = self._origPortfs.split(',')
        q.AddAttrNodeString('Portfolio.Name', portfolios, 'EQUAL')
        return q
    
    def __addOrigQueryInQuery(self, q):
        allQ = []
        queryNames = self._origQueries.split(',')
        for n in queryNames:
            query = acm.FStoredASQLQuery[n]
            if not query:
                continue
            allQ.append(query.Query())
        allQ.append(q)
        allQuery = acm.CreateFASQLQuery(acm.FTrade, 'AND')
        allQuery.AsqlNodes(allQ)
        return allQuery
    

    def __createStoredQuery(self, log, queryName, oid):

        if acm.FStoredASQLQuery[queryName]:
            return queryName

        positionInstance = acm.FCalculationRow[oid]
        attributes = positionInstance.Attributes()
        q = acm.CreateFASQLQuery(acm.FTrade, 'AND')
        for a in attributes:
            attName = a.DefinitionAsString()
            attValue = a.AttributeValue()
            if attName == "Instrument.Underlying.Name":
                if attValue in ['None', 'No Trade: Underlying']:
                    attValue = None
            q.AddAttrNodeString(attName, attValue, 'EQUAL');
        
        if self._origPortfs:
            q = self.__addPortfsInQuery(q)

        elif self._origQueries:
            q = self.__addOrigQueryInQuery(q)
        
        storedQuery = acm.FStoredASQLQuery()
        storedQuery.Query(q)
        storedQuery.Name(queryName)
        storedQuery.AutoUser(False)
        storedQuery.User(None)
        storedQuery.Commit()
        log.summaryAddOk(storedQuery.RecordType(), storedQuery.Oid(), 'CREATE')
        return queryName
        
    def Perform(self, log):

        if not self.valid():
            return 

        types = ["portfolios", 'tradeFilters', "storedASQLQueries"]
        trades = []
        for ty in types:
            objs = self._taskParams.At(ty, None)
            if isinstance(objs, str):
                objs = objs.split(',')
            trades = self.__getTrades(objs, ty, trades)

        creator = FPositionUtils.PositionCreator(self._posSpec)
        positions = creator.FindOrCreatePositions(trades)
        for p in positions:
            taskName = self._aelTask.Name()+ '_Pos_' + str(p.Oid())
            if acm.FAelTask[taskName]:
                Logme()("The task {0} has already been generated.".format(taskName), "INFO")
                continue
    
            newParams = self._taskParams
            newParams['portfolios'] = ''
            newParams['tradeFilters'] = ''
            newParams['storedASQLQueries'] = self.__createStoredQuery(log, taskName, p.Oid())
            newParams['Output File Prefix'] = taskName
            newTask = acm.FAelTask()
            newTask.Parameters(newParams)
            newTask.ModuleName(self._aelTask.ModuleName())
            newTask.Name(taskName)
            newTask.Commit()
            log.summaryAddOk(newTask.RecordType(), newTask.Oid(), 'CREATE')

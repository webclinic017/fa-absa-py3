"""----------------------------------------------------------------------------
MODULE
    pl_explain_AggregateQueryUpdate - 

    Gino Bellato, FIS

DESCRIPTION

    This script rolls the execution dates over for the trade query folders
    beginning with the prefix: "PLE_AggregateTrades_"

----------------------------------------------------------------------------"""
import acm, ael
from at_ael_variables import AelVariableHandler

today = acm.Time.DateToday()
yesterday = acm.Time.DateAdjustPeriod(today, '-1d', 'ZAR Johannesburg', 'Preceding')
dateDiff = str(acm.Time.DateDifference(yesterday, today)) + 'd'
masterAggregateTradeQueries = ['PLE_Master_Aggregate', 'PLE_Aggregate_Trades', 'PLE_Aggregate_Trades_Accrual']


def getAggregateTradeQueries(): 
    queryList = []
    for query in acm.FStoredASQLQuery.Select(''):
        if ('PLE_AggregateTrades' in query.Name()) and (not query.Name() in masterAggregateTradeQueries):
            queryList.append(query)
    return queryList


def queryFolderUpdate(filter, new_criteria, _field):
    """update a exsting query folder's node with new criteria"""
    print ('Updating the following query folder: {0}'.format(filter.Name()))
    query = filter.Query()
    print ('Query criteria before updates: {0}'.format(query))
    query.RegisterInStorage()
    nodes = query.AsqlNodes()
    if _field == 'ExecutionTime': execTime_node = nodes[2]
    
    execTime_nodes_array = execTime_node.AsqlNodes()
    if len(execTime_nodes_array) > 2:
        execTime_nodes_array.RemoveAt(2)

    execTime_nodes_array[0].AsqlValue(new_criteria)
    execTime_nodes_array[0].Commit()

    query.AsqlNodes(nodes)
    print ('==> Query criteria after updates: {0}'.format(query))
    filter.Query(query)
    filter.AutoUser(False)
    filter.Commit()

   
    print ('==> Successfully Added Execution Time: %s to %s.'%(new_criteria, filter.Name()))       

"""---------------------------------------------------------------------------------------------------------------------------------------------------------
------------------------------------------------------------------------------------------------------------------------------------------------------------
---------------------------------------------------------------------------------------------------------------------------------------------------------"""

days = ['Today', 'Yesterday']
ael_gui_parameters = {'hideExtracControls': True,
                      'windowCaption': 'PL Explain Aggregate Trade Query Folder Updates'}

ael_variables = []

      

def ael_main(ael_dict):  
    for query in getAggregateTradeQueries():
        try:
            queryFolderUpdate(query, dateDiff, 'ExecutionTime')
        except Exception as e:
            print ('Exception Raised: %s'%(e))

            
        


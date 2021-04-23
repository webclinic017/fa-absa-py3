"""
We have lots of query folders defined in the env and many of them are quite complex. 
Although the query folder gui gives us binary results of whether the concerned object is satisfying a query folder or not but it's 
not very easy to find out which condition(s) is exactly hitting/missing. 
This is a small python script wherein you pass an fobject, query folder name and it shows you details of which sections 
of the query folder are being hit and which are missed. 
There is a comments section at the end of the script which guides users how to use the script.

History
=======

2018-10-10 Sadanand Upase       Initial implementation.


"""


import acm
ATTR_NODE = {0: '=', 1: '=', 2: '<', 3: '>', 4: '<=', 5: '>=', 6: '*', 7: '<>'}

def check_if_node_is_satisfied(query_class, node, obj):
    folder = acm.FASQLQueryFolder()
    folder.Name('Temp folder')
    query = acm.CreateFASQLQuery(query_class, 'AND')
    query.AsqlNodes([node])
    folder.AsqlQuery(query)
    return folder.Query().IsSatisfiedBy(obj)
    
def get_string_for_attribute_node(node, query_class):
    return ''.join([str(query_class)+node.AsqlAttribute().AttributeString(), str(ATTR_NODE[node.AsqlOperator()]), str(node.AsqlValue())])
    #return ''.join([str(node.AsqlAttribute().AttributeString()), str(ATTR_NODE[node.AsqlOperator()]), str(node.AsqlValue())])

def organize_results(query_results, len_to_go_back):
    curr_big_node_res = query_results[-1][0]
    index = len_to_go_back + 1
    child_nodes = query_results[-index :-1]
    total_length = len(query_results)
    query_results = query_results[:(total_length-index)] + [{curr_big_node_res: child_nodes}]
    return query_results
    

def get_query_results(asqlnode, fobject, query_class, query_results):
    node_repr = []
    #global query_results
    for each in asqlnode.AsqlNodes():
        if each.IsKindOf(acm.FASQLOpNode):
            query_results = get_query_results(each, fobject, query_class, query_results)
        elif each.IsKindOf(acm.FASQLAttrNode):
            node_repr.append(get_string_for_attribute_node(each, query_class))
    operator = ' OR ' if asqlnode.AsqlOperator() == 1 else ' AND '
    node_result = 'Passing' if check_if_node_is_satisfied(query_class, asqlnode, fobject) else 'Not Passing'
    query_repr = ''.join(['NOT' if asqlnode.Not() else '', '(', operator.join(node_repr), ')'])
    query_results.append((node_result, query_repr))
    #Grouper node has no node_repr
    if not node_repr:
        query_results = organize_results(query_results, len(asqlnode.AsqlNodes()))
    return query_results


def pretty_print_query_results(results, level):
    space = '---'
    if type(results) == type([]):
        for each in results:
            if type(each) == type(()):
                print(space*level, each)
            else:
                pretty_print_query_results(each, level)
    if type(results) == type({}):
        for key, val in results.iteritems():
            print(space*level, key)
            level += 1
            pretty_print_query_results(val, level)

def analyze_query_result_for(query_name, fobject):
    qf = acm.FStoredASQLQuery.Select('name="%s"' % query_name)
    qf = qf.First()
    query_class = str(str(qf.Query().AsqlQueryClass()).split(' ')[0]).strip(',')
    query_results = []
    query_results = get_query_results(qf.Query(), fobject, query_class, query_results)
    pretty_print_query_results(query_results[0], 1)


'''
Below comments have the sample code for using query_folder_result_analyzer
'''


#For checking where trade is hitting/missing query folder
#analyze_query_result_for("settlementTradeFilterQuery", acm.FTrade[99062214])

#For checking where a settlement of type X is hitting/missing query folder
#If the settlement is generated then you can directly pass settlement and query name to check like below
#analyze_query_result_for("Settmnt_Prvnt_BONDSDesk", acm.FSettlement[99062206])

#If settlement is not generated i.e. stopped from generating by prevention query then you can use below to check as below
#remember 'get_settlements_to_be_created_for_trade' returns infant settlement objects which are not yet committed.

#from operations_troubleshooter import get_settlements_to_be_created_for_trade
#settlements = get_settlements_to_be_created_for_trade(acm.FTrade[99062214])
#for each in settlements:
#    if each.Type() == 'Security Nominal':
#            analyze_query_result_for("Settmnt_Prvnt_BONDSDesk", each)


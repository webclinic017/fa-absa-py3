""" Compiled: 2020-09-18 10:38:53 """

#__src_file__ = "extensions/operations/etc/FOperationsQueries.py"

import acm

#-------------------------------------------------------------------------
def CreateFilter(queryClass, queryOp, attribute, values, op):
    query = acm.CreateFASQLQuery(queryClass, queryOp)
    for value in values:
        query.AddAttrNode(attribute, op, value)
    return query

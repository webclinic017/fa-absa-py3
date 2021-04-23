""" Compiled: 2020-09-18 10:38:53 """

#__src_file__ = "extensions/reconciliation/./../AM_common/FPositionCreator.py"
"""-------------------------------------------------------------------------------------------------------
MODULE
    FPositionCreator

    (c) Copyright 2012 SunGard FRONT ARENA. All rights reserved.

DESCRIPTION

-------------------------------------------------------------------------------------------------------"""

import datetime
import time

import acm
import FAssetManagementUtils

logger = FAssetManagementUtils.GetLogger()

    
def _getPositionAttributeFunc(attributeDict):
    def attributeFromMethodChain(methodChain):
        try:
            return attributeDict[str(methodChain)]
        except KeyError:
            raise ValueError('Method chain "%s" is not in attribute dictionary' % methodChain)
    return attributeFromMethodChain    
    
def _getAttributeFunc(trade):
    def attributeFromMethodChain(methodChain):
        # pylint: disable-msg=W0123
        methodChainParentheses = str(methodChain).replace('.', '().') + '()'
        try:
            return eval('trade.' + methodChainParentheses)
        except Exception:
            raise ValueError('Trade %i does not support method chain "%s"' % \
                    (trade.Oid(), methodChainParentheses))
    return attributeFromMethodChain    

def _GetLatestTradeUpdateTime(trades):
    latestTime = max([t.UpdateTime() for t in trades])
    return time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(latestTime))

def _GetLastRunTime():
    extension = None
    try:
        extension = acm.GetDefaultContext().GetExtension('FStringResource', 'FTask', 'lastPositionCreatorRunTime')
    except Exception as stderr:
        logger.debug('Unable to get extension "lastPositionCreatorRunTime" : %s' % (stderr))
    
    if extension:
        lastRunTime = extension.Value()
    else:
        lastRunTime = (datetime.datetime.now() - datetime.timedelta(days=365)).strftime('%Y-%m-%d %H:%M:%S')
    return lastRunTime

def _SetLastRunTime(runTime):
    context = acm.GetDefaultContext()
    userModule = context.GetModule(acm.UserName())
    if userModule:
        definition = 'FTask:lastPositionCreatorRunTime\n' + runTime
        context.EditImport('FStringResource', definition, True, userModule)
        userModule.Commit()
    else:
        logger.warn('Could not load user module to persist last run time')


class FPositionSpecification(object):
    """Class representing a position specification."""

    def __init__(self, storedWildcardedQuery, allowIncompletePositions = False):
        """Create an FPositionSpecification based on a stored, wildcarded query."""
        if not self.IsPositionSpecification(storedWildcardedQuery) and allowIncompletePositions is False:
            raise ValueError('Stored wildcarded query "%s" is not a valid position specification' % storedWildcardedQuery.Name())
        self._storedWildcardedQuery = storedWildcardedQuery            

    @classmethod
    def IsPositionSpecification(cls, storedQuery):
        # pylint: disable-msg = W0511
        """Evaluates to whether or not the stored ASQL query represents a position specification."""
        return (storedQuery and \
                storedQuery.IsKindOf(acm.FStoredASQLQuery) and \
                # TODO: Disabled check to support reconciliation identification
                #storedQuery.QueryClass() == acm.FTrade and \
                cls.HasWildcardedAttribute(storedQuery.Query()))

    def Name(self):
        return self.StoredWildcardedQuery().Name()

    def StoredWildcardedQuery(self):
        """Return the underlying FStoredASQLQuery representing this position specification."""
        return self._storedWildcardedQuery

    def GetPosition(self, trade):
        """ Get a position (potentially creating one) that satisfies this specification
            for the passed trade. ValueError is thrown if the trade is not compatible with the
            specification. 
        """

        isValidPositionQuery = False
        if self.StoredWildcardedQuery().Query().IsSatisfiedBy(trade):
            query = self.StoredWildcardedQuery().Query().Clone()            
            isValidPositionQuery = self._SetWildcardedAttributes(query, _getAttributeFunc(trade))
        if not isValidPositionQuery:
            raise ValueError('Trade %d does not match position specification "%s"' % \
                    (trade.Oid(), self.Name()))

        positionStoredQuery = self.StoredWildcardedQuery()
        positionStoredQuery.Query(query)        
        return FPositionDefinition.GetPosition(positionStoredQuery)

    def GetInfantPositionFromDict(self, attributeDict, allowIncompletePositions=False):
        """ Get a dynamic position that satisfies this specification 
            given the passed dictionary of attributes.

            ValueError is thrown if the passed dictionary does not supply all required attributes
            for the specification and allowIncompletePositions is False.

        """

        # Careful here - have to clone the stored wildcard query, which is a storage image object!
        storedWildcardedQueryClone = self.StoredWildcardedQuery().Clone()
        query = storedWildcardedQueryClone.Query()
        isValidPositionQuery = self._SetWildcardedAttributes(query, _getPositionAttributeFunc(attributeDict))
        if not isValidPositionQuery and not allowIncompletePositions:
            raise ValueError('All wildcards in query were not filled using attribute dictionary:\n%s' % attributeDict)
            
        positionStoredQuery = self.StoredWildcardedQuery()
        positionStoredQuery.Query(query)
        position =  FPositionDefinition.GetPosition(positionStoredQuery, allowIncompletePositions)
        return position
        
    @classmethod
    def PositionQueryFromWildcardedQuery(cls, query, externalValuesDict, allowIncompletePositions = False):
        ''' Use this method from outside the recon engine to get the exact position
            The incoming query should be a wildcarded query. '''
        if cls.HasWildcardedAttribute(query):
            isValidPositionQuery = cls._SetWildcardedAttributes(query, _getPositionAttributeFunc(externalValuesDict))
            if not isValidPositionQuery and allowIncompletePositions is False:
                raise ValueError('All wildcards in query were not filled using attribute dictionary:\n %s' % str(externalValuesDict))
        return query
        
    @classmethod
    def GetInternalValuesDict(cls, storedQuery, trade):
        '''
            Get the internal values dict from the nodes of a
            stored query and a trade, where the query attributes
            are used as keys and the trade values are used to
            represent the values for the given keys.
        '''
 
        def SetNodeAttribute(node, attributeFromMethodChain, pyDict):
            if hasattr(node, 'AsqlNodes') and node.AsqlNodes():
                for n in node.AsqlNodes():
                    SetNodeAttribute(n, attributeFromMethodChain, pyDict)
            if node.IsKindOf(acm.FASQLAttrNode):
                methodChain = node.AsqlAttribute().AttributeString()
                try:
                    tradeAttributeValue = attributeFromMethodChain(methodChain)   
                    pyDict[str(methodChain).strip()] = tradeAttributeValue                    
                except ValueError:
                    pass
              
        internalValuesDict = {}      
        SetNodeAttribute(storedQuery.Query(), _getAttributeFunc(trade), internalValuesDict)
        return internalValuesDict                            

    @classmethod
    def _CompareStoredQueries(cls, left, right):
        leftNodes = left.Query().AsqlNodes()
        rightNodes = right.Query().AsqlNodes()
        if ((not leftNodes and rightNodes) or
            (not rightNodes and leftNodes) or
            len(leftNodes) != len(rightNodes)):
            return False
        if leftNodes and rightNodes:
            for leftNode, rightNode in zip(leftNodes, rightNodes):
                if not cls._CompareASQLNodes(leftNode, rightNode):
                    return False
        return True

    @classmethod
    def _CompareASQLNodes(cls, left, right):
        if type(left) != type(right):
            return False
        elif left.IsKindOf(acm.FASQLAttrNode):
            if (left.AsqlOperator() != right.AsqlOperator() or
                (str(left.AsqlValue()) != 'None' and left.AsqlValue() != right.AsqlValue())):
                return False
            return left.AsqlAttribute().AttributeString() == right.AsqlAttribute().AttributeString()
        elif left.IsKindOf(acm.FASQLOpNode):
            leftNodes = left.AsqlNodes()
            rightNodes = right.AsqlNodes()
            if ((not leftNodes and rightNodes) or
                (not rightNodes and leftNodes) or
                len(leftNodes) != len(rightNodes) or
                left.AsqlOperator() != right.AsqlOperator() or
                left.Not() != right.Not()):
                return False
            if leftNodes and rightNodes:
                for leftNode, rightNode in zip(leftNodes, rightNodes):
                    if not cls._CompareASQLNodes(leftNode, rightNode):
                        return False
        return True

    @classmethod
    def HasWildcardedAttribute(cls, query):
        def GetNodes(node, nodes=[]):
            # pylint: disable-msg=W0102
            if hasattr(node, 'AsqlNodes') and node.AsqlNodes():
                for n in node.AsqlNodes():
                    GetNodes(n, nodes)
            if node and node.IsKindOf(acm.FASQLNode):
                nodes.append(node)
            return nodes
        attributeNodes = (n for n in GetNodes(query) if n.IsKindOf(acm.FASQLAttrNode))
        attributeValues = (str(n.AsqlValue()) for n in attributeNodes)
        return 'None' in attributeValues

    @classmethod
    def _SetWildcardedAttributes(cls, query, attributeFromMethodChain):
        def SetNodeAttribute(node, attributeFromMethodChain): 
            # pylint: disable-msg=W0511
            #Recursive
            if hasattr(node, 'AsqlNodes') and node.AsqlNodes():
                for n in node.AsqlNodes():
                    SetNodeAttribute(n, attributeFromMethodChain)
            if node.IsKindOf(acm.FASQLAttrNode) and str(node.AsqlValue()) == 'None':
                methodChain = node.AsqlAttribute().AttributeString()
                try:
                    tradeAttributeValue = attributeFromMethodChain(methodChain)                    
                    if tradeAttributeValue is not None:
                        node.AsqlValue(tradeAttributeValue)                        
                except ValueError:
                    # TODO: Refactor this to visualize exceptions better 
                    # TODO: Disable logging as this will show up in the reconciliation workbench
                    #logger.debug('Position could not be formed: %s', e)
                    pass
        SetNodeAttribute(query, attributeFromMethodChain)
        return not cls.HasWildcardedAttribute(query)


class FPositionDefinition(object):
    """Class representing a position."""

    def __init__(self, infantPositionStoredQuery, allowIncompletePositions = False):
        '''Create an FPositionDefinition based on an infant, populated, FASQLStoredQuery.
           This query will be a copy of the identification rule that is used to represent this position,
           but with nodes populated with the data coming from the external document.
        '''
        self._infantPositionStoredQuery = infantPositionStoredQuery
        if not self.IsPosition(infantPositionStoredQuery) and allowIncompletePositions is False:
            raise ValueError('Position query "%s" is not a valid position' % infantPositionStoredQuery.Name()) 
            
    def InfantPositionStoredQuery(self):
        """Return the run-time instance of an FStoredASQLQuery representing this position"""
        return self._infantPositionStoredQuery            

    @classmethod
    def GetPosition(cls, infantPositionStoredQuery, allowIncompletePositions = False):
        """ Given a dynamically created FStoredASQL query, return an FPositionDefinition instance. 
            By returning an FPositionDefinition instance, the input query is also checked for eligibility; that is,
            whether the query represents an actual position or not.
        """
        assert infantPositionStoredQuery, 'No position query supplied'
        position = FPositionDefinition(infantPositionStoredQuery, allowIncompletePositions)
        return position

    @classmethod
    def IsPosition(cls, storedQuery):
        # pylint: disable-msg=W0511
        """Evaluates to whether or not the stored ASQL query represents a position."""
        return (storedQuery and \
                storedQuery.IsKindOf(acm.FStoredASQLQuery) and \
                not FPositionSpecification.HasWildcardedAttribute(storedQuery.Query())
                )
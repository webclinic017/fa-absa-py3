"""
This module contains functionality to analyse the mandate query folder to 
determine a best guess reason for the trade violating the mandate.
It uses score card reasoning to determine the most likely violation reason.
"""

from __future__ import division
import acm
import GenericMandatesCustomMethods


OP_NODE = {0: 'AND', 1: 'OR'}
ATTR_NODE = {0: '=', 1: '=', 2: '<', 3: '>', 4: '<=', 5: '>=', 6: '*', 7: '<>'}


""" Weights to assing to rules
"""
query_item_weights = {'Instrument.InsType': 100000,
                    'Instrument.Underlying.InsType': 1000,
                    'Currency.Name': 1000,
                    'Instrument.Issuer.Name': 10,
                    'Instrument.ExpiryDate': 10
                    }


class Rule():
    """ Represents a query folder rule and result of matching the rule to the trade.
    """

    def __init__(self, propertyName, operator, shouldBeValue, passTest, actualValue = None, level = None):
        self.propertyName = propertyName
        self.operator = operator
        self.shouldBeValue = shouldBeValue
        self.passTest = passTest
        self.actualValue = actualValue
        self.level = level
        self.score = 0
        
        self.SetRuleScore()


    def SetRuleScore(self):
        """ Assign the weight for the rule.
        """
        if self.passTest:
            if self.propertyName.Text() in query_item_weights:
                self.score = query_item_weights[self.propertyName.Text()]
            else:
                self.score = 1


    def GetRuleString(self):
        """ Format the rule into a string.
        """
        return "{0} = {1}".format(self.propertyName,
                                self.actualValue)


class RuleSetStructure():
    """ Structure of nested Mandate rules. This represents a Query Folder group or nested groups.
    """

    def __init__(self, product = None):
        self.product = product
        self.rules = []
        self.ruleSets = []
        
        self.ruleSetScore = 0


    def CalcScore(self):
        """ Add scores for rules on this level
        """
        self.ruleSetScore = 0
        
        for rule in self.rules:
            self.ruleSetScore = self.ruleSetScore + rule.score
            
        for ruleSet in self.ruleSets:
            self.ruleSetScore = self.ruleSetScore + ruleSet.ruleSetScore


    def AddRule(self, rule):
        self.rules.append(rule)
        
        
    def AddSet(self, ruleSet):
        self.ruleSets.append(ruleSet)


class ViolationBreachAnalyser():

    def __init__(self, trade, queryFolder):
        self.tree = RuleSetStructure(0)
        self.trade = trade
        self.queryFolder = queryFolder
        
        #analyse query folder and find and group rules
        for node in queryFolder.Query().AsqlNodes():
           self.tree.AddSet(self.FindNodes(node, self.trade, 0))
    
        
    def FindNodes(self, currentNode, trade, recursionCounter):
        """Analyse the query folder and build a workable ruleset object structure
        """
        recursionCounter = recursionCounter + 1
        ruleSet = RuleSetStructure(recursionCounter)
        
        if 'AsqlNodes' in dir(currentNode):
            for child_1 in currentNode.AsqlNodes():
                if child_1.Class() == acm.FASQLAttrNode:
                    newRule = self.CreateNewRule(child_1, trade, recursionCounter)
                    ruleSet.AddRule(newRule)
                    
                elif child_1.Class() == acm.FASQLOpNode:
                    #count nested complex nodes
                    complexElementCount = 0
                    portfolioNode = False

                    for child_2 in child_1.AsqlNodes():
                        if child_2.Class() == acm.FASQLAttrNode and child_2.AsqlAttribute().AttributeString().Text() == 'Portfolio.Name':
                            portfolioNode = True
                    
                        elif child_2.Class() is not acm.FASQLAttrNode:
                                complexElementCount = complexElementCount + 1

                    if complexElementCount > 0 and not portfolioNode:
                        ruleSet.AddSet(self.FindNodes(child_1, trade, recursionCounter))
                    else:
                        newRule = self.CreateNewRule(child_1, trade, recursionCounter, child_1.Not())
                        if newRule:
                            ruleSet.AddRule(newRule)

                elif type(currentNode) is type(acm.FArray()):
                    #FArray of asqlNodes
                    ruleSet.product = "%s" % OP_NODE[child_1.AsqlOperator()]
                    for child_2 in child_1:
                       ruleSet.AddSet(self.FindNodes(child_2, trade, recursionCounter))

        else:
            child_1 = currentNode
            #Attribute Nodes
            newRule = self.CreateNewRule(child_1, trade, recursionCounter)
            ruleSet.AddRule(newRule)
        
        #Cacluate the score for this current ruleset
        ruleSet.CalcScore()
        return ruleSet


    def CreateNewRule(self, node, trade, recursionCounter = 0, isNot = False):
        """ Create new 'Rule' object from the query folder node.
        """
        nodeAttributeString = ''
        tradePropertyValue = None
        shouldBeValue = None

        nodePass = self.CheckOpNode(node, trade, isNot)
        
        if node.Class() == acm.FASQLOpNode and node.AsqlNodes():
            nodeAttributeString = node.AsqlNodes()[0].AsqlAttribute().AttributeString()

            if isNot:
                operator = 'Not '
            else: 
                operator = ''

            if OP_NODE[node.AsqlOperator()] == 'AND':
                operator = '{0}BETWEEN'.format(operator)
            elif OP_NODE[node.AsqlOperator()] == 'OR':
                operator = '{0}IN'.format(operator)

            listOfShouldBeValues = []
            for childNode in node.AsqlNodes():

                if childNode.Class() == acm.FASQLAttrNode:
                    listOfShouldBeValues.append(childNode.AsqlValue().StringKey())
            shouldBeValue = ','.join(listOfShouldBeValues)

        elif node.Class() == acm.FASQLAttrNode:
            nodeAttributeString = node.AsqlAttribute().AttributeString()
            shouldBeValue = node.AsqlValue()
            
            if isNot:
                operator = '<>'
            else:
                operator = ATTR_NODE[node.AsqlOperator()]
            
        if nodeAttributeString:
            tradePropertyValue = self.EvalNode(nodeAttributeString, trade)    
            
            newRule = Rule(nodeAttributeString,
                            operator,
                            shouldBeValue,
                            nodePass,
                            tradePropertyValue, 
                            recursionCounter)
            return newRule
    
    
    def EvalNode(self, nodeAttributeString, trade):
        methodChain = nodeAttributeString
        method = acm.FMethodChain(acm.FSymbol(methodChain))
        tradePropertyValue = method.Call([trade])
        return tradePropertyValue
    

    def CheckOpNode(self, opNode, trade, isNot):
        folder = acm.FASQLQueryFolder()
        folder.Name('Temp folder')
        query = acm.CreateFASQLQuery('FTrade', 'OR')
        query.AsqlNodes(opNode)
        query.Not(isNot)
        folder.AsqlQuery(query)

        return folder.Query().IsSatisfiedBy(trade)
  
  
    def PrintRuleSet(self, ruleTree):
        """
            Print the ruleset for debugging purposes.
        """
        for ruleSet in ruleTree.ruleSets:
            print('-'*40)
            print('   ' * ruleSet.product, 'Level: {0} =RULE SET SCORE = {1} Child COUNT: {2}'.format(ruleSet.product, 
                                                                                                    ruleSet.ruleSetScore, 
                                                                                                    len(ruleSet.ruleSets)))
            level = 0
            for rule in ruleSet.rules:
                print('   ' * rule.level, '{0:60}{1!s:<20}[{2}], LEVEL_{3}, SCORE = {4}'.format(rule.GetRuleString(), 
                                                                                                rule.passTest, 
                                                                                                rule.actualValue, 
                                                                                                rule.level, 
                                                                                                rule.score))
                level = rule.level

            if ruleSet.ruleSets:
                self.PrintRuleSet(ruleSet)
            print('='*40)


    def FindBreachReason(self):
        """ Iterate through the rules to find the most likely reason for the non compliance.
        """
        rootBreachNode = self.FindBreachingRuleSetBranch(self.tree)
        mostLikelyBreachReasonlist = self.FindMostLikelyBreachReasons(rootBreachNode)
        
        for reason in mostLikelyBreachReasonlist:
            if 'Instrument.InsType' in reason:
                if self.trade.Instrument().InsType() not in reason:
                    mostLikelyBreachReasonlist = []
                    mostLikelyBreachReasonlist.append('Rules Error: No rule set for %s' % self.trade.Instrument().InsType())
                    break

        return mostLikelyBreachReasonlist


    def FindMostLikelyBreachReasons(self, ruleSetNode):
        """ Find the specific element that the trade does not comply too.
        """
        mostLikelyFailedRules = []

        for rule in ruleSetNode.rules:
            if not rule.passTest:
                mostLikelyFailedRules.append(rule.GetRuleString())


        nextMostLikelyBranch = self.FindBreachingRuleSetBranch(ruleSetNode)

        if nextMostLikelyBranch:
            mostLikelyFailedRules.extend(self.FindMostLikelyBreachReasons(nextMostLikelyBranch))
        
        return mostLikelyFailedRules


    def FindBreachingRuleSetBranch(self, ruleSetNode):
        """ Find the group of rules that is causing the non-compliance.
        """
        if ruleSetNode.ruleSets:
            ruleSetWithHighestScoreOnLevel = ruleSetNode.ruleSets[0]
            
            for ruleSet in ruleSetNode.ruleSets:
                if ruleSetWithHighestScoreOnLevel.ruleSetScore < ruleSet.ruleSetScore:
                    ruleSetWithHighestScoreOnLevel = ruleSet
                                
            return ruleSetWithHighestScoreOnLevel
        else:
            return None

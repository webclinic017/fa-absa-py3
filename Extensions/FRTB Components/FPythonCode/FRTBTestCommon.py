import acm

class FRTBTestCommonWriter(object):
    def __init__(self):
        self.m_positionKeyTable = {}
        self.m_positionInfoTable = {}
        self.m_resultDictionary = {}

    def addColumn(self, info, ID):
        pass

    def addRootPosition(self, info, ID):
        pass

    def positionKey(self, info):
        if info.parentInfoID:
            positionKey = self.positionKey(self.m_positionInfoTable[info.parentInfoID]) + '|' + info.name
        else:
            positionKey = info.acmDomainName + '|' + info.name
        return positionKey

    def addPosition(self, info, ID):
        self.m_positionInfoTable[ID] = info
        positionKey = self.positionKey(info)
        self.m_positionKeyTable[ID] = positionKey

    def results(self):
        return self.m_resultDictionary

def grouperForPositionSpecification(positionSpecification):
    groupingAttributes = acm.FArray()
    for attributeDefinition in positionSpecification.AttributeDefinitions():
        methodChain = attributeDefinition.Definition()
        groupingAttributes.Add([acm.Sheet.Column().MethodDisplayName(acm.FTrade, methodChain, acm.GetDefaultContext().Name()), methodChain, False])
    return acm.Risk().CreateChainedGrouperDefinition(acm.FTrade, 'Portfolio', False, 'Instrument', True, groupingAttributes)

def aelVariable(displayName, acmClass, constraint, toolTip, mandatory = False, allowMultipleInstances = True):
    return [displayName, displayName, acmClass.Name(), acmClass.Select(constraint), None, int(mandatory), int(allowMultipleInstances), toolTip]

def commonVariables():
    return [
        aelVariable('Position Specification', acm.FPositionSpecification, '', 'The Position Specification, where the position attributes are defined.', True, False),
        aelVariable('Risk Factor Setup', acm.FRiskFactorSetup, '', 'The Risk Factor Setup, repository for the Risk Factors.', True, False),
        aelVariable('Portfolios', acm.FPhysicalPortfolio, '', 'The physical portfolios. Values will be calculated on portfolio level and on instrument level'),
        aelVariable('Trade Filters', acm.FTradeSelection, '', 'The trade filters. Values will be calculated on portfolio level and on instrument level'),
        aelVariable('Trade Queries', acm.FStoredASQLQuery, 'user=0 and subType="FTrade"', 'The stored ASQL queries, queries shown are shared and of type trade. Values will be calculated on portfolio level and on instrument level')
    ]

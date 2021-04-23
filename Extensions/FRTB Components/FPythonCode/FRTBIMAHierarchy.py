
import acm
import collections

def RiskClassNames():
    return ['Commodity', 'Credit Spread', 'Equity', 'FX', 'Interest Rate', 'Unconstrained']

class FRTBIMAHierarchy():
    def __ClassCategoryAndLiquidityHorizon(self, node):
        riskClass = None
        riskFactorCategory = None
        liquidityHorizon = None
        while self.__imaHierarchyTree.Parent(node):
            for dataValue in node.HierarchyDataValues():
                columnName = dataValue.HierarchyColumnSpecification().Name()
                if 'Level Type' == columnName:
                    if (not riskClass) and ('Risk Class' == dataValue.DataValue()):
                        riskClass = node.DisplayName()
                    elif (not riskFactorCategory) and ('Risk Factor Category' == dataValue.DataValue()):
                        riskFactorCategory = node.DisplayName()
                    break
                elif (not liquidityHorizon) and ('Liquidity Horizon' == columnName):
                    liquidityHorizon = dataValue.DataValueVA()
            node = self.__imaHierarchyTree.Parent(node)
        return riskClass, riskFactorCategory, liquidityHorizon

    def __FillValidRiskFactorKeys(self):
        for collection in self.__imaRiskFactorSetup.RiskFactorCollections():
            riskClass = collection.AdditionalInfo().FRTB_IMA_Risk_Class()
            for instance in collection.RiskFactorInstances():
                riskFactorCategory = instance.AdditionalInfo().FRTB_IMA_Category()
                self.__imaValidRiskFactorKeys.add((riskClass, riskFactorCategory))
        return False

    def __RecurseTreeAndFillNodeCache(self, node):
        children = self.__imaHierarchyTree.Children(node)
        if children:
            for child in children:
                self.__RecurseTreeAndFillNodeCache(child)
        else:
            riskClass, riskFactorCategory, liquidityHorizon = self.__ClassCategoryAndLiquidityHorizon(node)
            cacheKey = (riskClass, riskFactorCategory)
            if cacheKey in self.__imaValidRiskFactorKeys:
                self.__imaLiquidityHorizonByKeyCache[cacheKey] = liquidityHorizon
                self.__imaValidLiquidityHorizonsPerRiskClass[riskClass].add(liquidityHorizon)

    def __init__(self, imaHierarchyName, imaRiskFactorSetupName):
        self.__imaHierarchy = acm.FHierarchy[imaHierarchyName]
        if not self.__imaHierarchy:
            errorMessage = 'Hierarchy with name ' + imaHierarchyName + ' not found.'
            print (errorMessage)
            raise Exception(errorMessage)

        self.__imaRiskFactorSetup = acm.FRiskFactorSetup[imaRiskFactorSetupName]
        if not self.__imaRiskFactorSetup:
            errorMessage = 'Risk Factor Setup with name ' + imaRiskFactorSetupName + ' not found.'
            print (errorMessage)
            raise Exception(errorMessage)

        self.__imaLiquidityHorizonByKeyCache = {}
        self.__imaHierarchyTree = acm.FHierarchyTree()
        self.__imaHierarchyTree.Hierarchy = self.__imaHierarchy
        self.__imaValidLiquidityHorizonsPerRiskClass = collections.defaultdict(set)
        self.__imaValidRiskFactorKeys = set()
        self.__FillValidRiskFactorKeys()
        self.__RecurseTreeAndFillNodeCache(self.__imaHierarchyTree.RootNode())

    def FRTBLiquidityHorizon(self, riskClass, riskFactorCategory):
        cacheKey = (riskClass, riskFactorCategory)
        if not cacheKey in self.__imaLiquidityHorizonByKeyCache:
            errorMessage = 'Node with key ', riskClass, riskFactorCategory, ' not found.'
            print (errorMessage)
            raise Exception(errorMessage)
        return self.__imaLiquidityHorizonByKeyCache[cacheKey]

    def FRTBValidLiquidityHorizons(self, riskClass):
        if 'Unconstrained' == riskClass:
            liquidityHorizons = set()
            for riskClass in self.__imaValidLiquidityHorizonsPerRiskClass:
                for lh in self.__imaValidLiquidityHorizonsPerRiskClass[riskClass]:
                    liquidityHorizons.add(lh)
            return sorted(liquidityHorizons)
        return sorted(self.__imaValidLiquidityHorizonsPerRiskClass[riskClass])

    def FRTBValidLiquidityHorizonsFiltered(self, riskClass, liquidityHorizonCandidates):
        validLiquidityHorizonsFiltered = set()
        validLiquidityHorizons = self.FRTBValidLiquidityHorizons(riskClass)
        for liquidityHorizon in liquidityHorizonCandidates:
            if liquidityHorizon in validLiquidityHorizons:
                validLiquidityHorizonsFiltered.add(liquidityHorizon)
            else:
                for validLiquidityHorizon in validLiquidityHorizons:
                    if validLiquidityHorizon > liquidityHorizon:
                        validLiquidityHorizonsFiltered.add(validLiquidityHorizon)
                        break
        return sorted(validLiquidityHorizonsFiltered)

    def FRTBLiquidityHorizonCandidates(self, liquidityHorizonInput):
        if liquidityHorizonInput:
            liquidityHorizonCandidates = liquidityHorizonInput
        else:
            liquidityHorizonCandidates = self.FRTBValidLiquidityHorizons('Unconstrained')
        return liquidityHorizonCandidates

    def FRTBLiquidityHorizonScenario(self, riskClass, liquidityHorizon):
        liquidityHorizonResult = liquidityHorizon

        liquidityHorizons = self.FRTBValidLiquidityHorizons(riskClass)
        if liquidityHorizon not in liquidityHorizons:
            if liquidityHorizon > liquidityHorizons[-1]:
                liquidityHorizonResult = 0
            else:
                for lh in liquidityHorizons:
                    if liquidityHorizon < lh:
                        liquidityHorizonResult = lh
                        break

        return liquidityHorizonResult



import acm, math, CreateHierarchyCommon

ael_variables = [['Hierarchy Name', 'Hierarchy Name', 'string', None, None, 1, 0, 'The desired name of the hierarchy and the hierarchy type.']]

__imaLevelTypeChoiceListName = 'FRTB IMA Level Type'

__imaHierarchyColumns = [
    ['Level Type', 'RecordRef', 32, __imaLevelTypeChoiceListName, 'The type describing the level'],
    ['Liquidity Horizon', 'Standard', 1, '', 'Liquidity Horizon for risk factors'],
    ['Unconstrained Weight', 'Standard', 4, '', 'The weight applied in the formula for aggregating unconstrained and constrained ES values'],
    ['Average Period', 'Standard', 1, '', 'The number of days used for calculating the average of ES values in the capital charge formula'],
    ['Capital Multiplier', 'Standard', 4, '', 'The multiplier used to scale the average ES value in the capital charge formula']
]

__imaHierarchy = [
    ['Total', {'Unconstrained Weight':0.5, 'Average Period':60, 'Capital Multiplier':1.5}, [
        ['Commodity', {'Level Type':'Risk Class'}, [
            ['Energy and Carbon Emissions', {'Level Type':'Risk Factor Category', 'Liquidity Horizon':20},  None],
            ['Precious and Non-Ferrous', {'Level Type':'Risk Factor Category', 'Liquidity Horizon':20}, None],
            ['Other Commodities', {'Level Type':'Risk Factor Category', 'Liquidity Horizon':60}, None],
            ['Energy and Carbon Emissions Volatility', {'Level Type':'Risk Factor Category', 'Liquidity Horizon':60},  None],
            ['Precious and Non-Ferrous Volatility', {'Level Type':'Risk Factor Category', 'Liquidity Horizon':60}, None],
            ['Other Commodities Volatility', {'Level Type':'Risk Factor Category', 'Liquidity Horizon':120}, None],
            ['Other Types', {'Level Type':'Risk Factor Category', 'Liquidity Horizon':120}, None]
            ]],
        ['Credit Spread', {'Level Type':'Risk Class'}, [
            ['Sovereign (IG)', {'Level Type':'Risk Factor Category', 'Liquidity Horizon':20},  None],
            ['Sovereign (HY)', {'Level Type':'Risk Factor Category', 'Liquidity Horizon':40}, None],
            ['Corporate (IG)', {'Level Type':'Risk Factor Category', 'Liquidity Horizon':40}, None],
            ['Corporate (HY)', {'Level Type':'Risk Factor Category', 'Liquidity Horizon':60},  None],
            ['Volatility', {'Level Type':'Risk Factor Category', 'Liquidity Horizon':120}, None],
            ['Other Types', {'Level Type':'Risk Factor Category', 'Liquidity Horizon':120}, None]
            ]],
        ['Equity', {'Level Type':'Risk Class'}, [
            ['Large Cap', {'Level Type':'Risk Factor Category', 'Liquidity Horizon':10},  None],
            ['Small Cap', {'Level Type':'Risk Factor Category', 'Liquidity Horizon':20}, None],
            ['Large Cap Volatility', {'Level Type':'Risk Factor Category', 'Liquidity Horizon':20},  None],
            ['Small Cap Volatility', {'Level Type':'Risk Factor Category', 'Liquidity Horizon':60}, None],
            ['Other Types', {'Level Type':'Risk Factor Category', 'Liquidity Horizon':60}, None]
            ]],
        ['FX', {'Level Type':'Risk Class'}, [
            ['Specified Currency Pairs', {'Level Type':'Risk Factor Category', 'Liquidity Horizon':10}, None],
            ['Other Currency Pairs', {'Level Type':'Risk Factor Category', 'Liquidity Horizon':20},  None],
            ['Volatility', {'Level Type':'Risk Factor Category', 'Liquidity Horizon':40}, None],
            ['Other Types', {'Level Type':'Risk Factor Category', 'Liquidity Horizon':40}, None]
            ]],
        ['Interest Rate', {'Level Type':'Risk Class'}, [
            ['Specified Currencies', {'Level Type':'Risk Factor Category', 'Liquidity Horizon':10},  None],
            ['Other Currencies', {'Level Type':'Risk Factor Category', 'Liquidity Horizon':20}, None],
            ['Volatility', {'Level Type':'Risk Factor Category', 'Liquidity Horizon':60}, None],
            ['Other Types', {'Level Type':'Risk Factor Category', 'Liquidity Horizon':60}, None]
            ]]
        ]]
]

def ael_main(parameters):
    choiceList = acm.FChoiceList.Select01('name="' + __imaLevelTypeChoiceListName + '" list="MASTER"', '')
    createChoiceList = None == choiceList
    if createChoiceList:
        choiceList = CreateHierarchyCommon.CreateNewChoiceList(__imaLevelTypeChoiceListName, 'MASTER')
        CreateHierarchyCommon.CreateNewChoiceList('Risk Class', __imaLevelTypeChoiceListName)
        CreateHierarchyCommon.CreateNewChoiceList('Risk Factor Category', __imaLevelTypeChoiceListName)

    ctxt = acm.ExtensionTools().GetDefaultContext()
    hTypeExt = ctxt.GetExtension('FExtensionValue', 'FObject', 'FRTBIMAHierarchyType')
    if hTypeExt:
        hierarchyType = CreateHierarchyCommon.CreateHierarchyType(hTypeExt.Value(), __imaHierarchyColumns)
        CreateHierarchyCommon.CreateHierarchy(hierarchyType, parameters['Hierarchy Name'], __imaHierarchy, createChoiceList, __imaLevelTypeChoiceListName)
    else:
        errorMessage = 'No hierarchy type found for FRTBIMAHierarchyType'
        print (errorMessage)

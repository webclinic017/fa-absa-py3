
import acm, CreateHierarchyCommon

#------------------------------------------------------------------------------
# SA-CCR Parameters Hierarchy
#------------------------------------------------------------------------------
class ColumnNames:
    ALPHA = 'Alpha'
    CORRELATION = 'Correlation'
    FACTOR = 'Factor'
    CLASS_TYPE = 'Class Type'
    MULTIPLIER_FLOOR = 'Multiplier Floor'
    VOLATILITY = 'Option Volatility'

__saccrHierarchyName = 'SA-CCR Parameters'
__saccrClassTypeChoiceListName = 'SA-CCR Class Type'

__saccrHierarchyColumns = [
    [ColumnNames.CLASS_TYPE, 'RecordRef', 32, __saccrClassTypeChoiceListName, 'The type describing the level'],
    [ColumnNames.FACTOR, 'Standard', 4, '', "Supervisory factor"],
    [ColumnNames.CORRELATION, 'Standard', 4, '', 'Correlation'],
    [ColumnNames.VOLATILITY, 'Standard', 4, '', 'Supervisory option volatility'],
    [ColumnNames.ALPHA, 'Standard', 4, '', 'Alpha used in EAD calculation'],
    [ColumnNames.MULTIPLIER_FLOOR, 'Standard', 4, '', 'Floor used in Add-On multiplier']
]

__saccrHierarchy = [
    [__saccrHierarchyName, {ColumnNames.ALPHA : 1.4, ColumnNames.MULTIPLIER_FLOOR : 0.05}, [
        ['Interest Rates', {ColumnNames.CLASS_TYPE:'Asset Class', ColumnNames.FACTOR : 0.005, ColumnNames.VOLATILITY : 0.50}, None],
        ['Foreign Exchange', {ColumnNames.CLASS_TYPE:'Asset Class', ColumnNames.FACTOR : 0.04, ColumnNames.VOLATILITY : 0.15}, None],
        ['Credit', {ColumnNames.CLASS_TYPE:'Asset Class'}, [
            ['Single Name', {ColumnNames.CLASS_TYPE : 'Entity Type'}, [
                ['AAA', {ColumnNames.CLASS_TYPE : 'Subclass', ColumnNames.FACTOR : 0.0038, ColumnNames.CORRELATION : 0.50, ColumnNames.VOLATILITY : 1.00}, None],
                ['AA', {ColumnNames.CLASS_TYPE : 'Subclass', ColumnNames.FACTOR : 0.0038, ColumnNames.CORRELATION : 0.50, ColumnNames.VOLATILITY : 1.00}, None],
                ['A', {ColumnNames.CLASS_TYPE : 'Subclass', ColumnNames.FACTOR : 0.0042, ColumnNames.CORRELATION : 0.50, ColumnNames.VOLATILITY : 1.00}, None],
                ['BBB', {ColumnNames.CLASS_TYPE : 'Subclass', ColumnNames.FACTOR : 0.0054, ColumnNames.CORRELATION : 0.50, ColumnNames.VOLATILITY : 1.00}, None],
                ['BB', {ColumnNames.CLASS_TYPE : 'Subclass', ColumnNames.FACTOR : 0.0106, ColumnNames.CORRELATION : 0.50, ColumnNames.VOLATILITY : 1.00}, None],
                ['B', {ColumnNames.CLASS_TYPE : 'Subclass', ColumnNames.FACTOR : 0.0160, ColumnNames.CORRELATION : 0.50, ColumnNames.VOLATILITY : 1.00}, None],
                ['CCC', {ColumnNames.CLASS_TYPE : 'Subclass', ColumnNames.FACTOR : 0.0600, ColumnNames.CORRELATION : 0.50, ColumnNames.VOLATILITY : 1.00}, None]
                ]
            ],
            ['Index', {ColumnNames.CLASS_TYPE : 'Entity Type'}, [
                ['IG', {ColumnNames.CLASS_TYPE : 'Subclass', ColumnNames.FACTOR : 0.0038, ColumnNames.CORRELATION : 0.80, ColumnNames.VOLATILITY : 0.80}, None],
                ['SG', {ColumnNames.CLASS_TYPE : 'Subclass', ColumnNames.FACTOR : 0.0106, ColumnNames.CORRELATION : 0.80, ColumnNames.VOLATILITY : 0.80}, None]
                ]
            ]
        ]],
        ['Equity', {ColumnNames.CLASS_TYPE:'Asset Class'}, [
            ['Single Name', {ColumnNames.CLASS_TYPE : 'Entity Type',ColumnNames.FACTOR : 0.32, ColumnNames.CORRELATION : 0.50, ColumnNames.VOLATILITY : 1.20}, None],
            ['Index', {ColumnNames.CLASS_TYPE : 'Entity Type', ColumnNames.FACTOR : 0.20, ColumnNames.CORRELATION : 0.80, ColumnNames.VOLATILITY : 0.75}, None]
        ]],
        ['Commodity', {ColumnNames.CLASS_TYPE:'Asset Class'}, [
            ['Electricity', {ColumnNames.CLASS_TYPE : 'Subclass', ColumnNames.FACTOR : 0.40, ColumnNames.CORRELATION : 0.40, ColumnNames.VOLATILITY : 1.50}, None],
            ['Oil/Gas', {ColumnNames.CLASS_TYPE : 'Subclass', ColumnNames.FACTOR : 0.18, ColumnNames.CORRELATION : 0.40, ColumnNames.VOLATILITY : 0.70}, None],
            ['Metals', {ColumnNames.CLASS_TYPE : 'Subclass', ColumnNames.FACTOR : 0.18, ColumnNames.CORRELATION : 0.40, ColumnNames.VOLATILITY : 0.70}, None],
            ['Agricultural', {ColumnNames.CLASS_TYPE : 'Subclass', ColumnNames.FACTOR : 0.18, ColumnNames.CORRELATION : 0.40, ColumnNames.VOLATILITY : 0.70}, None],
            ['Other', {ColumnNames.CLASS_TYPE : 'Subclass', ColumnNames.FACTOR : 0.18, ColumnNames.CORRELATION : 0.40, ColumnNames.VOLATILITY : 0.70}, None]
        ]]
    ]
]]

#------------------------------------------------------------------------------
# SA-CCR Hedging Set/Subset Hierarchy
#------------------------------------------------------------------------------
class CommodityColumnNames:
    LEVEL_TYPE = "Level Type"
    SUBCLASS = "Subclass"
    INSTRUMENT = "Instrument"

__saccrCommodityHierarchyName = 'SA-CCR Commodity'
__saccrLevelTypeChoiceListName = 'SA-CCR Level Type'

__saccrCommodityHierarchyColumns = [
    [CommodityColumnNames.LEVEL_TYPE, 'RecordRef', 32, __saccrLevelTypeChoiceListName, 'The type describing the level'],
    [CommodityColumnNames.SUBCLASS, 'Standard', 3, '', "Subclass used for finding applicable values in SA-CCR Parameters"],
    [CommodityColumnNames.INSTRUMENT, 'RecordRef', 4, '', 'Instrument belonging to the hedging subset']
]

__saccrCommodityHierarchy = [
    [__saccrCommodityHierarchyName, {CommodityColumnNames.LEVEL_TYPE : "Asset Class"}, [
        ["Agricultural", {CommodityColumnNames.LEVEL_TYPE : "Hedging Set"}, None],
        ["Energy", {CommodityColumnNames.LEVEL_TYPE : "Hedging Set"}, None],
        ["Metals", {CommodityColumnNames.LEVEL_TYPE : "Hedging Set"}, None],
        ["Other", {CommodityColumnNames.LEVEL_TYPE : "Hedging Set"}, None]
        ]    
    ]
]

#------------------------------------------------------------------------------
# Setup script
#------------------------------------------------------------------------------
def CreateChoiceList(name, items):
    choiceList = acm.FChoiceList.Select01('name="' + name + '" list="MASTER"', '')
    if not choiceList:
        choiceList = CreateHierarchyCommon.CreateNewChoiceList(name, 'MASTER')
        for item in items:
            CreateHierarchyCommon.CreateNewChoiceList(item, name)
           
#------------------------------------------------------------------------------
def CreateHierarchy(name, hierarchy, columns, choiceListName):
    typeName = name + ' Type'
    hierarchyType = CreateHierarchyCommon.CreateHierarchyType(typeName, columns)
    CreateHierarchyCommon.CreateHierarchy(hierarchyType, name, hierarchy, True, choiceListName)
    
#------------------------------------------------------------------------------
def Setup():
    CreateChoiceList(__saccrClassTypeChoiceListName, ['Asset Class', 'Subclass', 'Entity Type'])
    CreateChoiceList(__saccrLevelTypeChoiceListName, ['Asset Class', 'Hedging Set', 'Hedging Subset'])
    
    CreateHierarchy(__saccrHierarchyName, __saccrHierarchy, __saccrHierarchyColumns, __saccrClassTypeChoiceListName)
    CreateHierarchy(__saccrCommodityHierarchyName, __saccrCommodityHierarchy, __saccrCommodityHierarchyColumns, __saccrLevelTypeChoiceListName)

#------------------------------------------------------------------------------
ael_variables = []

#------------------------------------------------------------------------------
def ael_main(params):
    Setup()

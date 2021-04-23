from __future__ import print_function
import acm, time, CreateHierarchyCommon

__cemHierarchyName = 'CEM Parameters'

__cemLevelTypeChoiceListName = 'CEM Level Type'

__cemHierarchyColumns = [
    ['Level Type', 'RecordRef', 32, __cemLevelTypeChoiceListName, 'The type describing the level'],
    ['Factor', 'Standard', 4, '', 'The Add-On Factor']
]

__cemHierarchy = [
    [__cemHierarchyName, {}, [
        ['Interest Rates', {'Level Type':'Asset Class'}, [
            ['One Year or Less', {'Level Type':'Maturity', 'Factor':0.0},  None],
            ['Over One Year to Five Years', {'Level Type':'Maturity', 'Factor':0.005}, None],
            ['Over Five Years', {'Level Type':'Maturity', 'Factor':0.015}, None]
            ]],
        ['FX and Gold', {'Level Type':'Asset Class'}, [
            ['One Year or Less', {'Level Type':'Maturity', 'Factor':0.01},  None],
            ['Over One Year to Five Years', {'Level Type':'Maturity', 'Factor':0.05}, None],
            ['Over Five Years', {'Level Type':'Maturity', 'Factor':0.075}, None]
            ]],
        ['Equities', {'Level Type':'Asset Class'}, [
            ['One Year or Less', {'Level Type':'Maturity', 'Factor':0.06},  None],
            ['Over One Year to Five Years', {'Level Type':'Maturity', 'Factor':0.08}, None],
            ['Over Five Years', {'Level Type':'Maturity', 'Factor':0.1}, None]
            ]],
        ['Precious Metals Except Gold', {'Level Type':'Asset Class'}, [
            ['One Year or Less', {'Level Type':'Maturity', 'Factor':0.07},  None],
            ['Over One Year to Five Years', {'Level Type':'Maturity', 'Factor':0.07}, None],
            ['Over Five Years', {'Level Type':'Maturity', 'Factor':0.08}, None]
            ]],
        ['Other Commodities', {'Level Type':'Asset Class'}, [
            ['One Year or Less', {'Level Type':'Maturity', 'Factor':0.1},  None],
            ['Over One Year to Five Years', {'Level Type':'Maturity', 'Factor':0.12}, None],
            ['Over Five Years', {'Level Type':'Maturity', 'Factor':0.15}, None]
            ]],
        ['Credit', {'Level Type':'Asset Class'}, [
            ['Qualifying Reference Obligation', {'Level Type':'Rating', 'Factor':0.05},  None],
            ['Non-Qualifying Reference Obligation', {'Level Type':'Rating', 'Factor':0.1}, None]
            ]]
        ]]
]

def CreateChoiceList(name, items):
    choiceList = acm.FChoiceList.Select01('name="' + name + '" list="MASTER"', '')
    if not choiceList:
        choiceList = CreateHierarchyCommon.CreateNewChoiceList(name, 'MASTER')
        for item in items:
            CreateHierarchyCommon.CreateNewChoiceList(item, name)
           
def CreateAdditionalInfo(name, recType, dataTypeGroup, dataTypeType, description, subType):
    addInfoSpec = acm.FAdditionalInfoSpec[name]
    if not addInfoSpec:
        addInfoSpec = acm.FAdditionalInfoSpec(name = name, recType=recType, dataTypeGroup = dataTypeGroup, description = description)
        dataTypeTypeAsInt = acm.FEnumeration['enum(B92RecordType)'].Enumeration(dataTypeType)
        addInfoSpec.DataTypeType(dataTypeTypeAsInt)
        addInfoSpec.AddSubType( subType )
        addInfoSpec.Commit()
        print (time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()) + ' Created Additional Information Specification ' + name)

def Setup():
    CreateChoiceList(__cemLevelTypeChoiceListName, ['Asset Class', 'Maturity', 'Rating'])
    CreateAdditionalInfo('CVADocument', 'Instrument', 'RecordRef', 'ChoiceList', 'Standard Document', 'Credit Balance')
    typeName = __cemHierarchyName + ' Type'
    hierarchyType = CreateHierarchyCommon.CreateHierarchyType(typeName, __cemHierarchyColumns)
    CreateHierarchyCommon.CreateHierarchy(hierarchyType, __cemHierarchyName, __cemHierarchy, True, __cemLevelTypeChoiceListName)

#-------------------------------------------------------------------------
ael_variables = []

#-------------------------------------------------------------------------
def ael_main(params):
    Setup()

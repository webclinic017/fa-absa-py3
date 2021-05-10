""" Compiled: 2020-09-18 10:38:49 """

#__src_file__ = "extensions/operations_viewer/etc/FOperationsViewerExamplesHelperFunctions.py"
import Contracts_Tk_Messages_TkEnumerations as TkEnum

# Data Disp functions

#-------------------------------------------------------------------------
def AddTableValue(dataDisp, valueDict):
    newTableValue = dataDisp.tableValues.add()
    newTableValue.uniqueId = valueDict.get("uniqueId", "")

    newTableValue.attributeChain.SetInParent()
    for attributeId in valueDict.get("attributeChain.attributeIds", []):
        newTableValue.attributeChain.attributeIds.append(attributeId)

    newTableValue.defaults.SetInParent()
    newTableValue.defaults.formattingOptions.SetInParent()

    newTableValue.displayInformation.SetInParent()
    if valueDict.get("displayInformation.icon", "") != "":
        newTableValue.displayInformation.icon = valueDict.get("displayInformation.icon", "")

    newTableValue.displayInformation.label.SetInParent()
    if valueDict.get("displayInformation.label.formatString", "") != "":
        newTableValue.displayInformation.label.formatString = valueDict.get("displayInformation.label.formatString", "")
    
    if valueDict.get("displayInformation.description.formatString", "") != "":
        newTableValue.displayInformation.description.SetInParent()
        newTableValue.displayInformation.description.formatString = valueDict.get("displayInformation.description.formatString", "")

    newTableValue.formattingOptions.SetInParent()
    
    if valueDict.get("formattingOptions.formatterUniqueId", "") != "":
        newTableValue.formattingOptions.formatterUniqueId = valueDict.get("formattingOptions.formatterUniqueId", "")
    if valueDict.get("formattingOptions.overideNumberOfDecimals", "") != "":
        newTableValue.formattingOptions.overideNumberOfDecimals = valueDict.get("formattingOptions.overideNumberOfDecimals", "")

#-------------------------------------------------------------------------
def AddTableFormulaAndParameterValues(dataDisp, valueDict):
    formulaAndParameters = dataDisp.namedTableFormulaAndParameterValues.add()
    formulaAndParameters.uniqueId = valueDict.get("uniqueId", "")

    formulaAndParameters.displayInformation.label.SetInParent()
    if valueDict.get("displayInformation.label.formatString", "") != "":
        formulaAndParameters.displayInformation.label.formatString = valueDict.get("displayInformation.label.formatString", "")
    
    if valueDict.get("formulaWithFormatting.formula.formulaId", "") != "":
        formulaAndParameters.formulaWithFormatting.SetInParent()
        formulaAndParameters.formulaWithFormatting.formula.SetInParent()
        formulaAndParameters.formulaWithFormatting.formula.formulaId = valueDict.get("formulaWithFormatting.formula.formulaId", "")
        
        for value in valueDict.get("formulaWithFormatting.formula.values", []):
            newValue = formulaAndParameters.formulaWithFormatting.formula.values.add()
            newValue.parameterId = value["parameterId"]
            newValue.literalValue.SetInParent()
            newValue.literalValue.variant.SetInParent()
            newValue.literalValue.variant.type = value["value.type"]
            newValue.literalValue.variant.int32Value = value["value.int32Value"]
            
        formulaAndParameters.formulaWithFormatting.formattingOptions.SetInParent()
        if valueDict.get("formulaWithFormatting.formattingOptions.formatterUniqueId", "") != "":
            formulaAndParameters.formulaWithFormatting.formattingOptions.formatterUniqueId = valueDict["formulaWithFormatting.formattingOptions.formatterUniqueId"]
            if valueDict.get("formulaWithFormatting.formattingOptions.overideNumberOfDecimals", "") != "":
                formulaAndParameters.formulaWithFormatting.formattingOptions.overideNumberOfDecimals = valueDict["formulaWithFormatting.formattingOptions.overideNumberOfDecimals"]

#-------------------------------------------------------------------------     
def AddNamedFilter(dataDisp, namedFilterDict):
    newNamedFilter = dataDisp.namedFilters.add()

    newNamedFilter.uniqueId = namedFilterDict["uniqueId"]

    newNamedFilter.displayInformation.SetInParent()

    newNamedFilter.displayInformation.label.SetInParent()
    newNamedFilter.displayInformation.label.formatString = namedFilterDict["displayInformation.label.formatString"]
    newNamedFilter.filter.SetInParent()
    
    PopulateFilter(newNamedFilter.filter, namedFilterDict["filter.op"], namedFilterDict["filter.descendents"])

#-------------------------------------------------------------------------
def AddPreFilter(dataDisp, preFilterDict):
    dataDisp.preFilter.SetInParent()
    
    PopulateFilter(dataDisp.preFilter, preFilterDict["filter.op"], preFilterDict["filter.descendents"])

#-------------------------------------------------------------------------
def AddStringCondition(filter, id, conditionDict):
    descendent = filter.descendents.add()
    
    descendent.part.SetInParent()
    descendent.part.uniqueId = id
    if conditionDict.get("isNot", "") != "":
        descendent.part.isNot = conditionDict["isNot"]
    else:
        descendent.part.isNot = False
    
    descendent.part.compare.SetInParent()
    descendent.part.compare.op = TkEnum.CO_EQUAL
    
    for value in conditionDict.get("values", []):
        newValue = descendent.part.compare.values.add()
        newValue.variant.SetInParent()
        newValue.variant.type = TkEnum.PVT_STRING
        newValue.variant.stringValue = value
        
    if conditionDict.get("textMatchMode", "") == TkEnum.TMM_EXACT:
        descendent.part.compare.textMatchMode = TkEnum.TMM_EXACT
    else:
        descendent.part.compare.textMatchMode = TkEnum.TMM_CONTAINS
        descendent.part.compare.textMatchCase = False

#-------------------------------------------------------------------------        
def AddDoubleCondition(filter, id, conditionDict):
    descendent = filter.descendents.add()
    
    descendent.part.SetInParent()
    descendent.part.uniqueId = id
    
    descendent.part.isNot = False
    
    descendent.part.ranges.SetInParent()
    descendent.part.ranges.ranges.add()
 
#-------------------------------------------------------------------------   
def AddIntCondition(filter, id, conditionDict):
    descendent = filter.descendents.add()
    
    descendent.part.SetInParent()
    descendent.part.uniqueId = id
    
    descendent.part.isNot = False
    
    descendent.part.ranges.SetInParent()
    descendent.part.ranges.ranges.add()

#-------------------------------------------------------------------------    
def AddBoolCondition(filter, id, conditionDict):
    descendent = filter.descendents.add()
    
    descendent.part.SetInParent()
    descendent.part.uniqueId = id
    
    if conditionDict.get("isNot", "") != "":
        descendent.part.isNot = conditionDict["isNot"]
    else:
        descendent.part.isNot = False
    
    descendent.part.compare.SetInParent()
    descendent.part.compare.op = TkEnum.CO_EQUAL
    if conditionDict.get("value", "") != "":
        value = descendent.part.compare.values.add()
        value.variant.SetInParent()
        value.variant.type = TkEnum.PVT_BOOL
        value.variant.boolValue = conditionDict.get("value", "")

#-------------------------------------------------------------------------   
def AddDateCondition(filter, id, conditionDict):
    descendent = filter.descendents.add()
    
    descendent.part.SetInParent()
    descendent.part.uniqueId = id
    
    descendent.part.isNot = False
    
    descendent.part.ranges.SetInParent()
    if conditionDict.get("start", ""):
        range = descendent.part.ranges.ranges.add()
        range.start.SetInParent()
        range.start.type = TkEnum.PVT_STRING
        range.start.stringValue = conditionDict.get("start", "")

#-------------------------------------------------------------------------
def PopulateFilter(filter, op, valuesDict):
    if op == "And":
        filter.op = TkEnum.LO_AND
    if op == "Or":
        filter.op = TkEnum.LO_OR
        
    for (id, type, condition) in valuesDict:
        if type == "string":
            AddStringCondition(filter, id, condition)
        if type == "int":
            AddIntCondition(filter, id, condition)
        if type == "double":
            AddDoubleCondition(filter, id, condition)
        if type == "date":
            AddDateCondition(filter, id, condition)
        if type == "bool":
            AddBoolCondition(filter, id, condition)

#-------------------------------------------------------------------------           
def AddQuickFilters(dataDisp, ids):
    for id in ids:
        quickFilter = dataDisp.quickFilterParts.add()
        quickFilter.tableValueUniqueId = id


# View Disp Functions


#-------------------------------------------------------------------------
def AddTree(viewDisp, treeDict):
    newTree = viewDisp.trees.add()
    newTree.uniqueId = treeDict["uniqueId"]
    
    newTree.displayInformation.SetInParent()
    newTree.displayInformation.label.SetInParent()
    newTree.displayInformation.label.formatString = treeDict["displayInformation.label.formatString"]
    
    newTree.root.SetInParent()
    newTree.root.includeLevelInProjection = treeDict["root.includeLevelInProjection"]
    
    newTree.root.contribution.SetInParent()
    
    for child in treeDict.get("root.children", []):
        AddChildGrouping(newTree.root, child)

#-------------------------------------------------------------------------    
def AddChildGrouping(root, childDict):
    newChild = root.children.add()
    newChild.includeLevelInProjection = childDict["includeLevelInProjection"]
    
    newChild.contribution.SetInParent()
    newChild.groupBy.SetInParent()
    newChild.groupBy.type.SetInParent()
    newChild.groupBy.type.tableValue.SetInParent()
    newChild.groupBy.type.tableValue.tableValueId = childDict["groupBy.type.tableValue.tableValueId"]
    
    if childDict.get("groupBy.showLeafs.sort.tableValueId", "") != "":
        newChild.groupBy.showLeafs.SetInParent()
        newChild.groupBy.showLeafs.sort.SetInParent()
        newChild.groupBy.showLeafs.sort.tableValueId = childDict["groupBy.showLeafs.sort.tableValueId"]
        if childDict.get("groupBy.showLeafs.sort.ascending", "") != "":
            newChild.groupBy.showLeafs.sort.ascending = childDict["groupBy.showLeafs.sort.ascending"]
            
    newChild.groupBy.nodeDetails.SetInParent()
    newChild.groupBy.nodeDetails.sort.SetInParent()
    if childDict.get("groupBy.nodeDetails.sort.ascending", "") != "":
        newChild.groupBy.nodeDetails.sort.ascending = childDict["groupBy.nodeDetails.sort.ascending"]
        
    if childDict.get("groupBy.partition.tableFormula.namedFormulaId", "") != "":
        newChild.groupBy.partition.SetInParent()
        newChild.groupBy.partition.tableFormula.SetInParent()
        newChild.groupBy.partition.tableFormula.namedFormulaId = childDict["groupBy.partition.tableFormula.namedFormulaId"]
        
    for child in childDict.get("children", []):
        AddChildGrouping(newChild, child)

#-------------------------------------------------------------------------
def AddColumn(viewDisp, columnDict):
    newColumn = viewDisp.columns.add()
    newColumn.uniqueId = columnDict["uniqueId"]

    newColumn.displayInformation.SetInParent()
    if columnDict.get("displayInformation.icon", "") != "":
        newColumn.displayInformation.icon = columnDict["displayInformation.icon"]
    newColumn.displayInformation.label.SetInParent()
    newColumn.displayInformation.label.formatString = columnDict["displayInformation.label.formatString"]
    if columnDict.get("displayInformation.description.formatString", "") != "":
        newColumn.displayInformation.description.SetInParent()
        newColumn.displayInformation.description.formatString = columnDict["displayInformation.description.formatString"]

    newColumn.root.SetInParent()
    newColumn.root.contribution.SetInParent()
    newColumn.root.includeLevelInProjection = True

    for child in columnDict.get("root.children", []):
        AddChild(newColumn, child)

#-------------------------------------------------------------------------
def AddChild(column, childDict):
    newChild = column.root.children.add()
    newChild.contribution.SetInParent()

    AddSummarizationFormula(newChild, childDict["contribution.formula"])

    if childDict.get("contribution.backgroundColorFormula", "") != "":
      AddBackgroundColorFormula(newChild, childDict["contribution.backgroundColorFormula"])

#-------------------------------------------------------------------------
def AddSummarizationFormula(child, summarizationFormulaDict):
    child.contribution.formula.SetInParent()
    if summarizationFormulaDict.get("namedFormulaId", "") != "":
        child.contribution.formula.namedFormulaId = summarizationFormulaDict["namedFormulaId"]
    else:
        child.contribution.formula.formulaWithFormattingOptions.SetInParent()

        formulaWithFormattingOptions = child.contribution.formula.formulaWithFormattingOptions

        AddFormula(formulaWithFormattingOptions, summarizationFormulaDict["formulaWithFormattingOptions.formula"])

        AddFormattingOptions(formulaWithFormattingOptions, summarizationFormulaDict["formulaWithFormattingOptions.formattingOptions"])
 
#------------------------------------------------------------------------- 
def AddBackgroundColorFormula(child, backgroundColorformulaDict):
    child.contribution.backgroundColorFormula.SetInParent()
    child.contribution.backgroundColorFormula.formulaWithFormattingOptions.SetInParent()

    formulaWithFormattingOptions = child.contribution.backgroundColorFormula.formulaWithFormattingOptions

    AddFormula(formulaWithFormattingOptions, backgroundColorformulaDict["formulaWithFormattingOptions.formula"])

    AddFormattingOptions(formulaWithFormattingOptions, backgroundColorformulaDict["formulaWithFormattingOptions.formattingOptions"])

#-------------------------------------------------------------------------  
def AddTableFormulaReference(value, tableFormulaReferenceDict):
    value.tableFormulaReference.SetInParent()
    value.tableFormulaReference.formulaWithFormattingOptions.SetInParent()

    formulaWithFormattingOptions = value.tableFormulaReference.formulaWithFormattingOptions

    AddFormula(formulaWithFormattingOptions, tableFormulaReferenceDict["formulaWithFormattingOptions.formula"])
    
    AddFormattingOptions(formulaWithFormattingOptions, tableFormulaReferenceDict["formulaWithFormattingOptions.formattingOptions"])

#-------------------------------------------------------------------------
def AddFormula(formulaWithFormattingOptions, formulaDict):
    formulaWithFormattingOptions.formula.SetInParent()
    formulaWithFormattingOptions.formula.formulaId = formulaDict["formulaId"]
    
    for value in formulaDict["values"]:
        AddValue(formulaWithFormattingOptions.formula, value)

#-------------------------------------------------------------------------
def AddFormattingOptions(formula, formattingOptionsDict):
    formula.formattingOptions.SetInParent()
    if formattingOptionsDict.get("formatterUniqueId", "") != "":
      formula.formattingOptions.formatterUniqueId = formattingOptionsDict["formatterUniqueId"]
      if formattingOptionsDict.get("overideNumberOfDecimals", "") != "":
          formula.formattingOptions.overideNumberOfDecimals = formattingOptionsDict["overideNumberOfDecimals"]

#-------------------------------------------------------------------------
def AddValue(formula, valueDict):
    newValue = formula.values.add()
    newValue.parameterId = valueDict["parameterId"]

    if valueDict.get("tableValueId", "") != "":
        newValue.tableValueId = valueDict["tableValueId"]

    elif valueDict.get("tableFormulaReference", "") != "":
        AddTableFormulaReference(newValue, valueDict["tableFormulaReference"])
        
# Template Functions

#-------------------------------------------------------------------------
def AddColumnId(contents, columdIdDict):
    columndId = contents.columnIds.add()
    columndId.name = columdIdDict["name"]

#-------------------------------------------------------------------------   
def AddColumnSetting(settings, columnSettingDict):
    columnSetting = settings.columnSettings.add()
    columnSetting.columnUniqueId = columnSettingDict["columnUniqueId"]
    columnSetting.columnWidth = columnSettingDict["columnWidth"]
    columnSetting.configuredColumnAppearance.SetInParent()
    if columnSettingDict.get("customLabel", "") != "":
        columnSetting.customLabel = columnSettingDict["customLabel"]
    
    if columnSettingDict.get("configuredColumnAppearance.bold", "") != "":
        columnSetting.configuredColumnAppearance.bold = columnSettingDict["configuredColumnAppearance.bold"]
        
    if columnSettingDict.get("configuredColumnAppearance.fontSize", "") != "":
        columnSetting.configuredColumnAppearance.fontSize = columnSettingDict["configuredColumnAppearance.fontSize"]
        
    if columnSettingDict.get("configuredColumnAppearance.bkgColor", "") != "":
        columnSetting.configuredColumnAppearance.bkgColor = columnSettingDict["configuredColumnAppearance.bkgColor"]

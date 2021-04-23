from __future__ import print_function
import acm
import FUxCore

class DockKeys :
    SimulationPanelCreate = 'SimulationPanelCreateDockWindow'
    SimulationPanel = 'SimulationPanelDockWindow'

s_rowHeight = 20
s_domainsWithManyInstances = ['FParty',
                              'FCounterParty', 
                              'FTransactionHistory', 
                              'FCashFlow', 
                              'FInstrument', 
                              'FOrderBook', 
                              'FTradingInterface', 
                              'FTrade' ]

def S(s) :
    return acm.FSymbol(s)

class ContentsKey :
    AutoSimulateCheckBox = S('enabledCheckbox')
    AddedRiskFactors = S('addedRiskFactors')
    ZoomFactor = S('zoomFactor')
    ColumnWidths = S('columnWidths')
    RowHeaderWidth = S('rowHeaderWidth')
    InputColumnWidth = S('inputColumnWidth')

class InitialRiskFactors :
    def __init__(self) :
        self.m_riskFactor = None
        self.m_expanded = False

class ShiftFunctionParameter(object):
    def __init__(self, shiftFunctionInfo):
        self.m_shiftFunctionInfo = shiftFunctionInfo
        self.m_value = None
        self.m_operand = None
        self.m_displayName = None
        self.m_description = None
        self.m_defaultValue = None
        self.m_formatter = None
        self.m_mandatory = True

    def DisplayName(self) :
        return self.m_displayName

class ShiftFunctionInfo(object):
    def __init__(self, shiftGroupInfo):
        self.m_shiftGroupInfo = shiftGroupInfo
        self.m_shiftFunction = None
        self.m_functionParameters = []
        self.m_displayName = None
        self.m_filterValue = None
        self.m_shiftFunctionInformation = None

    def DisplayName(self) :
        return self.m_displayName


class ShiftFilterInfo(object):
    def __init__(self, shiftGroupInfo):
        self.m_shiftGroupInfo = shiftGroupInfo
        self.m_domain = None
        self.m_transform = None
        self.m_value = None



class ShiftGroupInfo(object):
    def __init__(self, riskFactor):
        self.m_displayName = None
        self.m_name = None
        self.m_extensionGroupItem = None
        self.m_riskFactor = riskFactor
        self.m_shiftFunctions = []
        self.m_shiftFilter = None
        self.m_currentShiftInfo = None

    def DisplayName(self) :
        displayName = ''

        if self.m_displayName :
            displayName = self.m_displayName
        elif self.m_extensionGroupItem :
            displayName = self.m_extensionGroupItem
        else:
            displayName = self.m_name

        return displayName
    


class GridCommandItem(FUxCore.MenuItem):
    def __init__(self, subject, invokeMethod, enabledMethod = None):
        self.m_subject = subject
        self.m_invokeMethod = invokeMethod
        self.m_enabledMethod = enabledMethod
    @FUxCore.aux_cb
    def Invoke(self, cd):
        if self.m_subject:
            return self.m_invokeMethod(self.m_subject)
    
    def Applicable(self):
        return True
        
    def Enabled(self):
        return self.m_enabledMethod(self.m_subject) if self.m_enabledMethod else True
    
    def Checked(self):
        return False

class SimulationPanel (FUxCore.LayoutPanel):
    def __init__(self, parent):
        self.m_grid = None
        self.m_enabledCheckbox = None
        self.m_clearButton = None
        self.m_activeSheetInput = None
        self.m_controlBackround = None
        self.m_inputCol = None
    
        self.m_shiftGroupByRow = {}
        self.m_functionParameterByRow = {}
        self.m_shiftFilterInfoByRow = {}

        self.m_shiftGroupInfos = []
        self.m_availableGroupInfos = []

        self.m_activeSheet = None
        self.m_applicableSheets = []
        self.m_initialRiskFactors = []
        self.m_previousSheets = None
        self.m_rowHeaderColumnWidth = 200
        self.m_inputColumnWidth = 250

        self.m_enabledColor = acm.UX().Colors().Create(255, 255, 255)
        self.m_disabledColor = acm.UX().Colors().Create(234, 234, 234)

    def RowKey(self, row):
        return row #row.GetCell(self.m_grid.RowHeaderColumn())

    def HandleContents(self, contents, load) :
        if contents != None:
            try :
                if load :
                    if contents.HasKey(ContentsKey.AutoSimulateCheckBox) :
                        self.m_enabledCheckbox.SetCheck(contents.At(ContentsKey.AutoSimulateCheckBox))
                    if contents.HasKey(ContentsKey.AddedRiskFactors) :
                        self.SetRiskFactorNames(contents.At(ContentsKey.AddedRiskFactors))
                    if contents.HasKey(ContentsKey.ZoomFactor) :
                        self.m_grid.SetZoom(int(contents.At(ContentsKey.ZoomFactor)))
                    if contents.HasKey(ContentsKey.ColumnWidths) :
                        self.SetColumnsWidth(contents.At(ContentsKey.ColumnWidths))
                else:
                    contents.AtPut(ContentsKey.AutoSimulateCheckBox, self.m_enabledCheckbox.GetCheck())
                    contents.AtPut(ContentsKey.ZoomFactor, self.m_grid.GetZoom())
                    contents.AtPut(ContentsKey.ColumnWidths, self.GetColumnWidths())
                    contents.AtPut(ContentsKey.AddedRiskFactors, self.GetRiskFactorNames())
            except:
                pass

    def GetContents(self):
        contents = acm.FDictionary()
        self.HandleContents(contents, False)

        return contents

    def GetRiskFactorNames(self) :
        riskFactorsNames = acm.FArray()

        for shiftGroupInfo in self.m_shiftGroupInfos :
            riskFactorsNames.Add(shiftGroupInfo.m_name)

        return riskFactorsNames

    def SetRiskFactorNames(self, riskFactorNames):
        for riskFactorName in riskFactorNames :
            for shiftGroupInfo in self.m_availableGroupInfos :
                if riskFactorName == shiftGroupInfo.m_name :
                    self.m_initialRiskFactors.append(shiftGroupInfo.m_riskFactor)


    def GetColumnWidths(self) :
        columnsWidths = acm.FDictionary()

        columnsWidths.AtPut(ContentsKey.RowHeaderWidth, self.m_grid.RowHeaderColumn().Width())
        columnsWidths.AtPut(ContentsKey.InputColumnWidth, self.m_inputCol.Width())

        return columnsWidths

    def SetColumnsWidth(self, columnWidths) :
        columnIterator = self.m_grid.GridColumnIterator()
        zoomFactor = self.m_grid.GetZoom() / 100.0

        self.m_rowHeaderColumnWidth = int(int(columnWidths.At(ContentsKey.RowHeaderWidth)) * zoomFactor)
        self.m_inputColumnWidth = int(int(columnWidths.At(ContentsKey.InputColumnWidth)) * zoomFactor)

    def ShiftGroupInfoSortKey(self, shiftGroupInfo) :
        return shiftGroupInfo.DisplayName()

    def HandleDestroy(self):
        self.ClearSimulation()

    def HandleCreate( self ):
        layout = self.SetLayout(self.CreateLayout())

        self.m_activeSheetInput = layout.GetControl('activeSheet')
        self.UpdateActiveSheetList()
        self.m_activeSheetInput.AddCallback('Changed', self.OnActiveSheetInputChanged, self)
        self.m_grid = layout.GetControl('simulationGrid')

        self.m_grid.AddCallback('ContextMenu', self.OnContextMenu, self.m_grid)
        self.m_grid.AddCallback('SelectionChanged', self.OnSelectionChanged, self.m_grid)
        self.m_grid.AddCallback('CellCreate', self.OnCellCreate, self.m_grid)

        self.m_grid.ShowRowHeaders(True)
        self.m_grid.ShowColumnHeaders(True)
        self.m_grid.SetEnterKeyMove(True, 'Down')
        self.m_grid.SetCellBorderStyle('Horizontal')
        self.m_grid.TabDirection(True)
        self.m_grid.RowHeaderCaption('Type')
        #self.m_grid.SetCellTypeProperty('List', 'DropdownOnly', True)

        self.m_enabledCheckbox = layout.GetControl('enabledCheckbox')
        self.m_enabledCheckbox.SetCheck('Checked')
        self.m_controlBackround = layout.GetControl('backgroundBox')
        self.m_clearButton = layout.GetControl('clearButton')

        self.m_enabledCheckbox.AddCallback( 'Activate', self.OnEnabledCheckbox, self )
        self.m_clearButton.AddCallback( 'Activate', self.OnClearSimulate, self )

        context = acm.GetDefaultContext()
        availableRiskFactors = context.GetAllExtensions('FRiskFactorDefinition', 'FObject', True, True, 'simulation panel')
        self.SetupShiftGroupsAndFunctions(availableRiskFactors, self.m_availableGroupInfos)
        self.m_availableGroupInfos.sort(key=self.ShiftGroupInfoSortKey)

        self.HandleContents(self.InitialContents(), True)

        if self.m_initialRiskFactors :
            self.SetupShiftGroupsAndFunctions(self.m_initialRiskFactors, self.m_shiftGroupInfos)
        else:
            defaultRiskFactors = context.GetAllExtensions('FRiskFactorDefinition', 'FObject', True, True, 'simulation panel', 'default')
            self.SetupShiftGroupsAndFunctions(defaultRiskFactors, self.m_shiftGroupInfos)
            self.m_shiftGroupInfos.sort(key = lambda shiftGroupInfo: shiftGroupInfo.DisplayName())
        
        self.SetupColumns()
        self.Populate()
        self.UpdateControls()

    def UpdateControls(self) :
        color = self.m_enabledColor if self.m_enabledCheckbox.Checked() else self.m_disabledColor

        self.m_controlBackround.SetColor('Background', color)
        self.m_activeSheetInput.GetLabelControl().SetColor('Background', color)
        self.m_enabledCheckbox.SetColor('Background', color)

    def OnClearSimulate(self, ud, cd ):
        self.DoClearValues()
        self.ClearSimulation()

    def DoClearValues(self) :
        for shiftGroupInfo in self.m_shiftGroupInfos :
            for shiftFunctionInfo in shiftGroupInfo.m_shiftFunctions :
                for functionParameters in shiftFunctionInfo.m_functionParameters :
                    functionParameters.m_value = None


        for row in self.m_functionParameterByRow.keys() :
            cell = row.GetCell(self.m_inputCol)
            cell.SetData('')

        for row, shiftFilterInfo in self.m_shiftFilterInfoByRow.iteritems() :
            cell = row.GetCell(self.m_inputCol)
            cell.SetData('')
            shiftFilterInfo.m_value = None

    def FormatterFromDomain(self, domain ):
        formatter = domain.DefaultFormatter()

        if domain.StringKey() == 'double':
            formatter = acm.Get('formats/FullPrecisionHideNaN')
        
        return formatter

    def ParseValue(self, domain, value, formatter) :
        if value :
            if not formatter :
                formatter = self.FormatterFromDomain(domain)
        
            if formatter:
                parsedValue = formatter.Parse(value)
                if parsedValue != None :
                    if domain.StringKey() == 'double' and not parsedValue:
                        value = '0'
                    else :
                        value = parsedValue
                else :
                    print(value + ' is not a valid ' + domain.Name())
                    value = None

        return value

    def ValidShiftParameterValues(self, shiftInfo) :
        shiftParameterValues = []

        if shiftInfo :
            valid = True
            for functionParameter in shiftInfo.m_functionParameters:
                if functionParameter.m_value :
                    shiftParameterValues.append(functionParameter.m_value)
                elif functionParameter.m_defaultValue:
                    shiftParameterValues.append(functionParameter.m_defaultValue)
                elif not functionParameter.m_mandatory :
                    shiftParameterValues.append(None)
                else:
                    shiftParameterValues = []
                    break

        return shiftParameterValues

    def CreateScenarioDimension(self) :
        dimension = None 

        for shiftGroupInfo in self.m_shiftGroupInfos :
            riskFactor = shiftGroupInfo.m_riskFactor
            shiftInfo = shiftGroupInfo.m_currentShiftInfo
            shiftParameterValues = self.ValidShiftParameterValues(shiftInfo)

            if shiftParameterValues :
                if not dimension :
                    dimension = acm.FScenarioDimension()

                displayText = shiftGroupInfo.DisplayName()
                shiftFilter = self.GetShiftFilter(shiftGroupInfo.m_shiftFilter)
                shiftVector = acm.Risk.CreateShiftVectorFromRiskFactorDefinition(riskFactor)
                shiftVector.SetFilter(shiftFilter)                
                shiftVector.Function(shiftInfo.m_shiftFunction.Name())
                shiftVector.AddShiftItem(shiftParameterValues, displayText )

                dimension.AddShiftVector(shiftVector)

        return dimension

    def GetShiftFilter(self, shiftFilterInfo) :
        shiftFilter = None

        if shiftFilterInfo and shiftFilterInfo.m_value:
            attributes = ['name']
            operators = ['RE_LIKE_NOCASE']
            values = [shiftFilterInfo.m_value]

            shiftFilter = acm.Filter.SimpleAndQuery(shiftFilterInfo.m_domain, attributes, operators, values)
        elif shiftFilterInfo :
            shiftFilter = acm.GetClass(shiftFilterInfo.m_domain)

        return shiftFilter

    def AutoSimulate(self):
        if self.m_enabledCheckbox.Checked() :
            self.DoSimulate()

    def DoSimulate(self):
        activeGridBuilder = self.ActivePortfolioGridBuilder()
        if activeGridBuilder:
            dimension = self.CreateScenarioDimension()     
            scenario = None

            if dimension :   
                scenario = acm.FExplicitScenario()
                scenario.Name('Sim')
                scenario.AddDimension(dimension)

            activeGridBuilder.TransientVerticalScenario(scenario)


    def OnEnabledCheckbox(self, ud, cd ):
        checked = self.m_enabledCheckbox.Checked()
        if checked :
            self.DoSimulate()
        else :
            self.ClearSimulation()

        self.UpdateControls()
        
    def UpdateValueColumns(self):
        pass

    def Populate(self):
        self.m_grid.RemoveAllItems()
        self.m_shiftGroupByRow = {}
        self.m_functionParameterByRow = {}
        self.m_shiftFilterInfoByRow = {}

        for shiftGroupInfo in self.m_shiftGroupInfos :
            self.AddRow(self.m_grid, self.m_grid.GetRootItem(), shiftGroupInfo)


    def SetupColumns(self) :
        self.m_grid.RowHeaderColumn().Width(self.m_rowHeaderColumnWidth)
        self.m_inputCol = self.m_grid.AddColumn('Input', self.m_inputColumnWidth)
        gridColumnIterator = self.m_grid.GridColumnIterator()

        while gridColumnIterator.Next() :
            columnHeader = gridColumnIterator.GridColumn()
            if columnHeader.IsRowHeaderColumn() :
                rowColHeaderCell.AddCallback(self.OnColumnHeaderEvent, column)
                break


    def ActivePortfolioGridBuilder(self):
        self.m_activeSheet = self.m_activeSheetInput.GetData()

        if not self.m_activeSheet :
           self.m_activeSheet = self.Owner().ActiveSheet() 
        if self.m_activeSheet:
            if self.m_activeSheet.GridBuilder().IsKindOf('FPortfolioGridBuilder'):
                return self.m_activeSheet.GridBuilder()

        return None


    def OnColumnHeaderEvent(self, event, eventData, args):
        column = args
        if event == 'DefaultAction':
            self.SortColumn(column)

    def RemoveTreeChildren(self, treeGrid) :
        child = treeGrid.Iterator().FirstChild()
        children = []
        while child:
            item = child.Tree()
            children.append(item)
            item = self.RowKey(item)
            self.m_functionParameterByRow.pop(item, None)
            self.m_shiftFilterInfoByRow.pop(item, None)

            child = child.NextSibling()      

        for child in children :
            child.Remove()

    def UpdateShiftFunction(self, row, shiftFunctionInfo) :
        shiftGroupInfo = shiftFunctionInfo.m_shiftGroupInfo

        self.RemoveTreeChildren(row)
        
        for functionParameter in shiftFunctionInfo.m_functionParameters :
            child = row.AddChild()
            child.Height(self.GetRowHeight())
            label = functionParameter.DisplayName()
            if functionParameter.m_mandatory :
                child.Icon('Required')
            
            child.Label(label)

            if functionParameter.m_description:
                child.Tooltip(functionParameter.m_description)

            self.m_functionParameterByRow[self.RowKey(child)] = functionParameter

            # This will trigger OnCellCreate
            child.GetCell(self.m_inputCol) 

        shiftFilter = shiftFunctionInfo.m_shiftGroupInfo.m_shiftFilter
        if shiftFilter:
            child = row.AddChild()
            child.Height(self.GetRowHeight())

            label = self.GetFilterLabel(shiftFilter)
            child.Label(label)
            child.Icon('Filter')
            self.m_shiftFilterInfoByRow[self.RowKey(child)] = shiftFilter
            child.GetCell(self.m_inputCol)


        row.Expand(1)

        self.UpdateRowHeights()


    def UpdateRowHeights(self):
        rowIter = self.m_grid.RowTreeIterator()
        while rowIter:
            rowIter.Tree().Height(self.GetRowHeight())
            rowIter = rowIter.NextUsingDepthFirst()


    def GetFilterLabel(self, shiftFilter) :
        domainName = shiftFilter.m_domain

        s = acm.GetDefaultContext().GetExtension('FStringResource', domainName, 'objectNameSingular')
            
        if s:
            domainName = s.Value()

        return 'Filter (' + domainName + ')'

    def AddRow(self, grid, parent, shiftGroupInfo):
        if shiftGroupInfo.m_shiftFunctions:
            row = parent.AddChild()
            row.Label(shiftGroupInfo.DisplayName())
    
            if shiftGroupInfo.m_riskFactor.HasValue('Description') :
                row.Tooltip(shiftGroupInfo.m_riskFactor.GetString('Description'))
        
            row.Icon('Folder')
            row.Height(self.GetRowHeight())
            self.m_shiftGroupByRow[self.RowKey(row)] = shiftGroupInfo

            # This will trigger OnCellCreate
            row.GetCell(self.m_inputCol) 
            if not shiftGroupInfo.m_currentShiftInfo :
                shiftGroupInfo.m_currentShiftInfo = shiftGroupInfo.m_shiftFunctions[0]

            self.UpdateShiftFunction(row, shiftGroupInfo.m_currentShiftInfo)


    def GetShiftFunction(self, functionName) :
        shiftFunction = None
        if hasattr(acm.Risk, 'GetShiftFunction') :
            shiftFunction = acm.Risk.GetShiftFunction(functionName) 
        else :
            for i in range(2, 100) :
                shiftFunction = acm.GetFunction(functionName, i)
                if shiftFunction :
                    break

        return shiftFunction
    
    def GetShiftFunctionInfos(self, shiftGroupInfo) :
        shiftFunctionInfos = []

        riskFactor = shiftGroupInfo.m_riskFactor
        shiftFunctions = riskFactor.ShiftFunctions()

        if shiftFunctions :
            for shiftFunctionName in shiftFunctions :
                shiftFunctionInfo = ShiftFunctionInfo(shiftGroupInfo)
                shiftFunctionInfo.m_shiftFunction = self.GetShiftFunction(shiftFunctionName)
                shiftFunctionInfo.m_displayName = self.GetFunctionDisplayName(shiftFunctionName)
                shiftFunctionInfos.append(shiftFunctionInfo)

        shiftFunctionInformations = riskFactor.ShiftFunctionInformations()

        if shiftFunctionInformations :
            for shiftFunctionInformationName in shiftFunctionInformations :
                shiftFunctionInformation = acm.GetDefaultContext().GetExtension('FShiftFunctionInformation', 'FObject', shiftFunctionInformationName)

                if shiftFunctionInformation :
                    shiftFunctionInformation = shiftFunctionInformation.Value()
                    if shiftFunctionInformation.HasValue('Function') :
                        shiftFunctionInfo = ShiftFunctionInfo(shiftGroupInfo)
                        shiftFunctionInfo.m_shiftFunctionInformation = shiftFunctionInformation
                        shiftFunctionName = shiftFunctionInformation.GetString('Function')
                        shiftFunctionInfo.m_shiftFunction = self.GetShiftFunction(shiftFunctionName)

                        if shiftFunctionInformation.HasValue('DisplayName') :
                            shiftFunctionInfo.m_displayName = shiftFunctionInformation.GetString('DisplayName')
                        else :
                            shiftFunctionInfo.m_displayName = self.GetFunctionDisplayName(shiftFunctionName)


                        shiftFunctionInfos.append(shiftFunctionInfo)

        return shiftFunctionInfos                

    def SetupShiftFunctionParameter(self, shiftFunctionInfo, shiftFunctionParameter) :
        operand = shiftFunctionParameter.m_operand
        resourceKey = str(shiftFunctionInfo.m_shiftFunction.Name()) + '.' + str(operand.Name())

        displayName = ''
        s = None
        
        if shiftFunctionInfo.m_shiftFunctionInformation:
            operandInfo = shiftFunctionInfo.m_shiftFunctionInformation.OperandInformation(operand.Name())        

            if operandInfo :
                if operandInfo.HasValue('DisplayName'):
                    s = operandInfo.GetString('DisplayName')
                if operandInfo.HasValue('Description'):
                    shiftFunctionParameter.m_description = operandInfo.Description()
                if operandInfo.HasValue('Formatter'):
                    shiftFunctionParameter.m_formatter = acm.Get('formats/' + str(operandInfo.Formatter()))
                if operandInfo.HasValue('DefaultValue'):
                    shiftFunctionParameter.m_defaultValue = operandInfo.DefaultValue()
                if operandInfo.HasValue('Mandatory'):
                    shiftFunctionParameter.m_mandatory = operandInfo.Mandatory()

        
        if not s :                
            s = acm.GetDefaultContext().GetExtension('FStringResource', 'FFunction', resourceKey)
            if s :
                s = s.Value()

        if s :
            displayName = str(s)
        else:
            displayName = str(operand.Name())

        domainName = operand.Domain().StringKey()

        #if operand.Domain().IsEnum() :
        #    domainName = domainName[5:-1] #ugly, format string to remove 'enum(' and ')'

        #displayName += ' (' + domainName + ')'

        shiftFunctionParameter.m_displayName = displayName

    

    def CreateShiftGroupInfo(self, riskFactor, shiftGroupInfos) :
        shiftGroupInfo = ShiftGroupInfo(riskFactor)

        shiftGroupInfo.m_name = riskFactor.Name()

        stringResource = acm.GetDefaultContext().GetExtension('FStringResource', 'FObject', shiftGroupInfo.m_name)
        
        if stringResource:
            shiftGroupInfo.m_displayName = stringResource.Value()
            
        if riskFactor.HasValue('ExtensionAttributeGroupItem') :
            shiftGroupInfo.m_extensionGroupItem = riskFactor.GetString('ExtensionAttributeGroupItem')
            stringResource = acm.GetDefaultContext().GetExtension('FStringResource', 'FObject', shiftGroupInfo.m_extensionGroupItem)

            if not shiftGroupInfo.m_displayName and stringResource :
                shiftGroupInfo.m_displayName = stringResource.Value()

        shiftGroupInfos.append(shiftGroupInfo)

        shiftFunctionInfos = self.GetShiftFunctionInfos(shiftGroupInfo)

        if riskFactor.HasValue('FilterType') :
            shiftFilterInfo = ShiftFilterInfo(shiftGroupInfo)
            shiftGroupInfo.m_shiftFilter = shiftFilterInfo
            shiftGroupInfo.m_shiftFilter.m_domain = str(riskFactor.GetString('FilterType'))
        if riskFactor.HasValue('FilterTransform') and shiftGroupInfo.m_shiftFilter:
            shiftGroupInfo.m_shiftFilter.m_transform = str(riskFactor.GetString('FilterTransform'))

        for shiftFunctionInfo in shiftFunctionInfos:
            shiftFunctionInfo.m_shiftGroupInfo = shiftGroupInfo
            if shiftFunctionInfo.m_shiftFunction :
                operands = shiftFunctionInfo.m_shiftFunction.Operands()
                first = True
                for operand in operands:
                    if not first : # ignore first argument, since it's self
                        if operand != shiftFunctionInfo.m_shiftFunction.ReturnDataOperand() :
                            shiftFunctionParameter = ShiftFunctionParameter(shiftFunctionInfo)
                            shiftFunctionParameter.m_operand = operand
                            self.SetupShiftFunctionParameter(shiftFunctionInfo, shiftFunctionParameter)
                            shiftFunctionInfo.m_functionParameters.append(shiftFunctionParameter)
                    first = False

            shiftGroupInfo.m_shiftFunctions.append(shiftFunctionInfo)

        return shiftGroupInfo

    def SetupShiftGroupsAndFunctions(self, riskFactors, shiftGroupInfos):
        for riskFactor in riskFactors :
            self.CreateShiftGroupInfo(riskFactor, shiftGroupInfos)


    def UpdateCellValue(self, row, cell):
        item = self.RowKey(row)

        if item in self.m_functionParameterByRow :
            functionParameter = self.m_functionParameterByRow[item]
            functionParameter.m_value = self.ParseValue(functionParameter.m_operand.Domain(), cell.GetData(), functionParameter.m_formatter) 
            cell.SetData(self.FormatValue(functionParameter.m_value, functionParameter.m_formatter if functionParameter.m_formatter else self.FormatterFromDomain(functionParameter.m_operand.Domain())))
        elif item in self.m_shiftGroupByRow :
            shiftGroupInfo = self.m_shiftGroupByRow[item]
            shiftGroupInfo.m_currentShiftInfo = None
            if len(shiftGroupInfo.m_shiftFunctions) == 1:
                shiftGroupInfo.m_currentShiftInfo = shiftGroupInfo.m_shiftFunctions[0]
            else:
                for shiftInfo in shiftGroupInfo.m_shiftFunctions :
                    if shiftInfo.DisplayName() == cell.GetData() :
                        shiftGroupInfo.m_currentShiftInfo = shiftInfo
                        self.UpdateShiftFunction(row, shiftGroupInfo.m_currentShiftInfo)
                        break
        elif item in self.m_shiftFilterInfoByRow :
            shiftFilterInfo = self.m_shiftFilterInfoByRow[item]
            shiftFilterInfo.m_value = cell.GetData()

    def ValueChanged(self, row, newValue):
        valueChanged = True

        if row in self.m_shiftGroupByRow :
            if newValue :
                shiftGroupInfo = self.m_shiftGroupByRow[row]
                valueChanged = shiftGroupInfo.m_currentShiftInfo.m_displayName != newValue
            else:
                valueChanged = False

        elif row in self.m_functionParameterByRow:
            functionParameter = self.m_functionParameterByRow[row]
            valueChanged = functionParameter.m_value != newValue

        return valueChanged

    def RevertIfNeeded(self, row, cell) :
        if row in self.m_shiftGroupByRow :
            shiftGroupInfo = self.m_shiftGroupByRow[row]
            value = shiftGroupInfo.m_currentShiftInfo.m_displayName
            cell.SetData(value)


    def OnCellEvent(self, event, eventData, cellData):
        cell = cellData['cell']
        row = cellData['row']

        if event == 'Input':
            listBoxItems = None
            if row in self.m_shiftGroupByRow :
                shiftGroupInfo = self.m_shiftGroupByRow[row]
                listBoxItems = self.GetShiftFunctionDisplayNames(shiftGroupInfo)
            elif row in self.m_functionParameterByRow:
                functionParameter = self.m_functionParameterByRow[row]
                listBoxItems = self.GetItemsFromDomainName(functionParameter.m_operand.Domain())

            if listBoxItems :
                searchString = eventData.lower()
                if searchString :
                    eventData = None
                    for displayName in listBoxItems :
                        if searchString in displayName.lower():
                            eventData = displayName
                            break        



        if event == 'Changed':
            if self.ValueChanged(row, eventData) :
                self.UpdateCellValue(row, cell)
                self.AutoSimulate()

            if not eventData:
                self.RevertIfNeeded(row, cell)

        return eventData


    def OnSelectionChanged(self, control, cd):
        pass

    def GetSheetName(self, sheet) :
        name = sheet.Name()

        if not name : # it's a utility view...
            sheetType = acm.Sheet.GetSheetDefinition(sheet.SheetClass()).DisplayName()
            name = sheetType + ' Viewer'

        return name

    def UpdateActiveSheetList(self) :
        workbook = self.Owner().ActiveWorkbook()
        if workbook :
            sheets = []
            selection = self.m_activeSheetInput.GetData()
            for sheet in workbook.Sheets() :
                if sheet.GridBuilder().IsKindOf('FPortfolioGridBuilder'):
                    sheets.append(sheet)

            portfolioViewerSheet = self.Owner().GetUtilityView('PortfolioViewer')

            if portfolioViewerSheet :
                portfolioViewerSheet.Name('Portfolio Viewer')
                sheets.append(portfolioViewerSheet)

            self.m_activeSheetInput.Populate(sheets)

            if not selection:
                selection = self.Owner().ActiveSheet()

            if not self.m_previousSheets :
                self.m_previousSheets = sheets

            if len(self.m_previousSheets) != len(sheets): # A sheet has been removed or a new one has been added
                self.m_activeSheet = self.Owner().ActiveSheet()
                selection = self.m_activeSheet
                self.m_previousSheets = sheets
                self.m_activeSheetInput.SetData(selection)

                for sheet in sheets :
                    self.ClearSheetSimulation(sheet)

                self.AutoSimulate()

            self.m_activeSheetInput.SetData(selection)

    
    def ClearSheetSimulation(self, sheet) :
        if sheet :
            activeGridBuilder = sheet.GridBuilder()
            if activeGridBuilder:
                activeGridBuilder.TransientVerticalScenario(None)

    def ClearSimulation(self) :
        self.ClearSheetSimulation(self.m_activeSheet)            

    def OnActiveSheetInputChanged(self, ud, cd) :
        self.ClearSimulation()
        self.AutoSimulate()

    def OnActiveSheetChanged(self):
        self.UpdateActiveSheetList()

    def GetFunctionDisplayName(self, shiftFunction) :
        stringResource = acm.GetDefaultContext().GetExtension('FStringResource', 'FFunction', shiftFunction)
        if stringResource :
            stringResource = stringResource.Value()
        else:
            stringResource = shiftFunction

        return stringResource

    def CreateCellEventData(self, row, cell) :
        return {'row':row, 'cell':cell}

    def GetShiftFunctionDisplayNames(self, shiftGroupInfo) :
        shiftFunctionsDisplayNames = []

        if shiftGroupInfo.m_shiftFunctions :
            for shiftFunction in shiftGroupInfo.m_shiftFunctions :
                shiftFunctionsDisplayNames.append(shiftFunction.DisplayName())

        return shiftFunctionsDisplayNames        

    def PopulateParameterCell(self, cell, row, shiftGroupInfo) :
        if shiftGroupInfo.m_shiftFunctions :
            shiftFunctionsDisplayNames = self.GetShiftFunctionDisplayNames(shiftGroupInfo)

            if len(shiftFunctionsDisplayNames) > 1 :
                cell.SetControlType('List', shiftFunctionsDisplayNames)
            else:
                cell.EnableEditing(False)

            selectedShiftInfo = shiftGroupInfo.m_currentShiftInfo.DisplayName() if shiftGroupInfo.m_currentShiftInfo else shiftFunctionsDisplayNames[0]

            cell.SetData(selectedShiftInfo)
            cell.AddCallback(self.OnCellEvent, self.CreateCellEventData(row, cell))
            cell.Tooltip('Shift Function')
            cell.Bold(True)
        else:
            cell.EnableEditing(False)

    def GetItemsFromDomainName(self, domainName) :
        domain = acm.GetDomain(domainName)
        values = None

        if domain:
            acmValues = None
            if domain.Class().IncludesBehavior(acm.FEnumeration) :
                 acmValues = domain.Enumerators()

            if acmValues :
                values = []
                for value in acmValues:
                    values.append(value)

        return values

    def GetRowHeight(self) :
        return s_rowHeight * self.m_grid.GetZoom() / 100.0


    def FormatValue(self, value, formatter) :
        if formatter :
            value = formatter.Format(value)

        return value

    def OnCellCreate(self, control, cd):
        row = cd.At('row')
        column = cd.At('column')
        cell = cd.At('cell')

        item = self.RowKey(row)

        if cell.HeaderType() == 'ColumnHeader' :
            row.Height(self.GetRowHeight())
        elif cell.HeaderType() == 'None':
            cell.BorderStyle('All')
            cell.EnableEditing(True)
            cell.AddCallback(self.OnCellEvent, self.CreateCellEventData(row, cell))


            if item in self.m_shiftGroupByRow :
                shiftGroupInfo = self.m_shiftGroupByRow[item]
                riskFactor = shiftGroupInfo.m_riskFactor
        
                if column == self.m_inputCol:
                    self.PopulateParameterCell(cell, row, shiftGroupInfo)

            if item in self.m_functionParameterByRow :
                functionParameterInfo = self.m_functionParameterByRow[item]
                items = self.GetItemsFromDomainName(functionParameterInfo.m_operand.Domain())
                if items :
                    cell.SetControlType('List', items)

                if functionParameterInfo.m_value :
                    cell.SetData(self.FormatValue(functionParameterInfo.m_value, functionParameterInfo.m_formatter))
                elif functionParameterInfo.m_defaultValue :
                    cell.SetData(self.FormatValue(functionParameterInfo.m_defaultValue, functionParameterInfo.m_formatter))
                    cell.Tooltip(functionParameterInfo.DisplayName() + '\nDefault value: ' + str(functionParameterInfo.m_defaultValue))
                elif functionParameterInfo.m_mandatory :
                    cell.SetData('')
                    cell.Tooltip(str(functionParameterInfo.DisplayName()) + ' (required)')        
                else:
                    cell.SetData('')

                
                cell.Alignment('Right')
            if item in self.m_shiftFilterInfoByRow :
                shiftFilter = self.m_shiftFilterInfoByRow[item]
                label = self.GetFilterLabel(shiftFilter)
                cell.SetData(shiftFilter.m_value)
                cell.Tooltip(label)
                cell.Alignment('Right')

    def Move(self, shiftGroupInfo, up) :
        index = self.m_shiftGroupInfos.index(shiftGroupInfo)
        
        if up :
            if index - 1 > -1 :
                self.m_shiftGroupInfos[index] = self.m_shiftGroupInfos[index - 1]
                self.m_shiftGroupInfos[index - 1] = shiftGroupInfo
        else :
            if index != -1 and index + 1 < len(self.m_shiftGroupInfos) :
                self.m_shiftGroupInfos[index] = self.m_shiftGroupInfos[index + 1]
                self.m_shiftGroupInfos[index + 1] = shiftGroupInfo
                
        self.Populate()

    def EnableMoveUp(self, shiftGroupInfo) :
        index = self.m_shiftGroupInfos.index(shiftGroupInfo)
        
        return index > 0

    def EnableMoveDown(self, shiftGroupInfo) :
        index = self.m_shiftGroupInfos.index(shiftGroupInfo)
        
        return index < (len(self.m_shiftGroupInfos) - 1)

    def OnMoveUp(self, shiftGroupInfo):
        self.Move(shiftGroupInfo, True)

    def OnMoveDown(self, shiftGroupInfo):
        self.Move(shiftGroupInfo, False)

    def RowFromRowKey(self, rowKey) :
        row = None 
        rowIter = self.m_grid.RowTreeIterator()
        while rowIter:
            if rowKey == self.RowKey(rowIter.Tree()):
                row = rowIter.Tree()
                break
            rowIter = rowIter.NextUsingDepthFirst()
        
        return row


    def OnRemoveShiftGroup(self, shiftGroupInfo):
        foundRow = None
        for rowKey, shiftGroupInfoInMap in self.m_shiftGroupByRow.iteritems() :
            if shiftGroupInfoInMap == shiftGroupInfo :
                foundRow = rowKey
                break

        if foundRow :
            self.m_shiftGroupByRow.pop(foundRow)
            self.m_shiftGroupInfos.remove(shiftGroupInfo)

            self.RemoveTreeChildren(foundRow)
            foundRow.Remove()
            self.AutoSimulate()

    def OnAddShiftGroup(self, shiftGroupInfo):
        shiftGroupInfo = self.CreateShiftGroupInfo(shiftGroupInfo.m_riskFactor, self.m_shiftGroupInfos)
        self.AddRow(self.m_grid, self.m_grid.GetRootItem(), shiftGroupInfo)

    def CreateCommand(self, cmdName, displayName, cb, default = False) :
        command = []

        command.append(cmdName)
        command.append('')
        command.append(displayName)
        command.append('')
        command.append('')
        command.append('')
        command.append(cb)
        command.append(default)

        return command

    def BuildAvailableRiskFactorsCommands(self, commands) :
        for shiftGroupInfo in self.m_availableGroupInfos :
            commands.append(self.CreateCommand('addShiftGroupCommand', 'Add/' + shiftGroupInfo.DisplayName(), lambda x = shiftGroupInfo: GridCommandItem(x, self.OnAddShiftGroup)))

    def BuildRemoveRiskFactorsCommands(self, commands, selectedShiftGroupInfo) :
        sortedShiftGroupInfos = list(self.m_shiftGroupInfos)
        sortedShiftGroupInfos.sort(key=self.ShiftGroupInfoSortKey)
        for shiftGroupInfo in sortedShiftGroupInfos :
            if shiftGroupInfo != selectedShiftGroupInfo :
                commands.append(self.CreateCommand('removeShiftGroupCommand', 'Remove/' + shiftGroupInfo.DisplayName(), lambda x = shiftGroupInfo: GridCommandItem(x, self.OnRemoveShiftGroup)))

    def OnContextMenu(self, control, cd):
        menuBuilder = cd.At('menuBuilder')
        selectedCell = control.GetSelectedCell()
        selectedRow = control.GetSelectedItem()

        commands = []

        defaultMenu = True

        if selectedCell and selectedRow:
            rowKey = self.RowKey(selectedRow)
            if rowKey in self.m_shiftGroupByRow:
                shiftGroupInfo = self.m_shiftGroupByRow[rowKey]
                if 'RowHeader' == str(selectedCell.HeaderType()):
                    defaultMenu = False

                    commands.append(self.CreateCommand('moveUpCommand', 'Move/Up', lambda: GridCommandItem(shiftGroupInfo, self.OnMoveUp, self.EnableMoveUp)))
                    commands.append(self.CreateCommand('moveDownCommand', 'Move/Down', lambda: GridCommandItem(shiftGroupInfo, self.OnMoveDown, self.EnableMoveDown)))
                    commands.append(FUxCore.Separator())
                    self.BuildAvailableRiskFactorsCommands(commands)
                    commands.append(FUxCore.Separator())
                    commands.append(self.CreateCommand('removeCommand', 'Remove (' + shiftGroupInfo.DisplayName() + ')', lambda: GridCommandItem(shiftGroupInfo, self.OnRemoveShiftGroup)))

        if defaultMenu:
            self.BuildAvailableRiskFactorsCommands(commands)
            #self.BuildRemoveRiskFactorsCommands(commands, None)

        if commands :
            menuBuilder.RegisterCommands(FUxCore.ConvertCommands(commands))


    def CreateLayout( self ):
        b = acm.FUxLayoutBuilder()
        b.BeginVertBox()
        b.BeginVertBox('Invisible', '', 'backgroundBox')
        b.  BeginHorzBox()
        b.      AddOption('activeSheet', 'Active Sheet')
        b.      AddCheckbox('enabledCheckbox', 'Enabled')
        b.  EndBox()
        b.  AddGrid('simulationGrid', 350, 100)
        b.  BeginHorzBox()
        b.      AddFill()
        b.      AddButton('clearButton', 'Clear')
        b.  EndBox()
        b.EndBox()
        b.EndBox()
        return b

def OnSheetSelectionChanged(eii, sheetChanged):
    basicApp = eii.ExtensionObject()
    layoutPanel = basicApp.GetCustomDockWindow(DockKeys.SimulationPanel)
    if layoutPanel and sheetChanged:
        simulationPanel = layoutPanel.CustomLayoutPanel()
        simulationPanel.OnActiveSheetChanged()

def Create(eii) :
    basicApp = eii.ExtensionObject()

    dockWindow = basicApp.GetCustomDockWindow(DockKeys.SimulationPanel)
    if dockWindow :
        basicApp.DestroyDockWindow(DockKeys.SimulationPanel)
    else:
        basicApp.CreateRegisteredDockWindow(DockKeys.SimulationPanelCreate, DockKeys.SimulationPanel, 'Simulation Panel', 'Left')

def CreateSimulationPanel(eii) :
    basicApp = eii.ExtensionObject()
    myPanel = SimulationPanel(basicApp)

    return myPanel

def OnCreate(eii):
    basicApp = eii.ExtensionObject()
    basicApp.RegisterDockWindowType(DockKeys.SimulationPanelCreate, 'SimulationPanel.CreateSimulationPanel')
    #basicApp.CreateRegisteredDockWindow(DockKeys.SimulationPanelCreate, DockKeys.SimulationPanel, 'Simulation Panel', 'Left', True, True, False, True)


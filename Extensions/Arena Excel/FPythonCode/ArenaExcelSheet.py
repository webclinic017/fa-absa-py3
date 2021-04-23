""" Compiled: 2020-09-18 10:38:52 """

#__src_file__ = "extensions/ArenaExcel/etc/ArenaExcelSheet.py"
import acm
import base64

from collections import OrderedDict

TOPIC_MAX_CHARS = 255
LIST_SEPARATOR = ','

def Split(line, n):
    return [line[i:i+n] for i in range(0, len(line), n)]

def IsColumnHeader(cell):
    return cell.IsHeaderCell() and cell.RowObject() is None
    
def IsRowHeader(cell):
    return cell.IsHeaderCell() and cell.RowObject()


class Selection(object):

    def __init__(self, sheet):
        self._selection = sheet.Selection().SelectedCells()
        self._columnHeaderCells = OrderedDict()
        self._matrix = OrderedDict()
        self._Init()
        
    def _Init(self):
        for cell in self._selection:
            column = cell.Column()
            if (IsColumnHeader(cell) and 
                column not in self._columnHeaderCells):
                self._columnHeaderCells[column] = cell
            if column not in self._matrix:
                self._matrix[column] = []
            if IsColumnHeader(cell) is False:
                self._matrix[column].append(cell)
                
    def Cells(self):
        for cell in self._columnHeaderCells.itervalues():
            yield cell
        yield NewLineCellInfo()
        transpose = list(zip(*self._matrix.itervalues()))
        lastRowIndex = len(transpose) - 1
        for index, row in enumerate(transpose):
            for cell in row:
                yield cell
            if index < lastRowIndex:
                yield NewLineCellInfo()
                

class SheetAdaptor(object):

    def __init__(self, sheet, visibleCellsOnly=False):
        self._sheet = sheet
        self._visibleCellsOnly = visibleCellsOnly
        
    def _ColumnHeaderCells(self):
        yield ColumnHeaderCellInfoProxy()
        columnIter = self._sheet.GridColumnIterator()
        while columnIter.Next():
            yield ColumnHeaderCellInfoProxy(columnIter.GridColumn())
        yield NewLineCellInfo()

    def Cells(self):
        for cell in self._ColumnHeaderCells():
            yield cell
    
        rowHeader = None
        rowIterProxy = CreateRowIterProxy(self._sheet, self._visibleCellsOnly)
        while rowIterProxy.NextUsingDepthFirst():
            columnIter = self._sheet.GridColumnIterator()
            row = rowIterProxy.Tree().Item()
            if rowHeader != row:
                rowHeader = row
                yield self._sheet.GetCell(rowIterProxy.Iter(), columnIter)
            columnIter = self._sheet.GridColumnIterator()
            while columnIter.Next():
                yield self._sheet.GetCell(rowIterProxy.Iter(), columnIter)
            yield NewLineCellInfo()    

    
def SheetMatrix(sheet, visibleCellsOnly=False):
    for cell in SheetAdaptor(sheet, visibleCellsOnly).Cells():
        if IsRowHeader(cell):
            yield RowHeaderCellInfo(cell)
        elif IsColumnHeader(cell):         
            yield ColumnHeaderCellInfo(cell.Column())
        else:
            yield cell

def SelectionMatrix(sheet):
    for cell in Selection(sheet).Cells():
        if IsRowHeader(cell):
            yield RowHeaderCellInfo(cell)
        elif IsColumnHeader(cell):         
            yield ColumnHeaderCellInfo(cell.Column())
        else:
            yield cell
     
def SelectedCells(sheet):
    cells = []
    for cell in list(SelectionMatrix(sheet)):
        cells.append(Cell.Factory(cell, sheet))
    return cells

def SheetCells(sheet, visibleCellsOnly):
    cells = []
    for cell in list(SheetMatrix(sheet, visibleCellsOnly)):
        cells.append(Cell.Factory(cell, sheet))
    return cells
    
def CellsFromSelection(selectionMatrix, sheet, settings=None):
    cells = []
    for cell in selectionMatrix:
        cells.append(Cell.Factory(cell, sheet, settings))
    return cells
    
def CellsFromSheet(sheetMatrix, sheet, settings=None):
    cells = []
    for cell in sheetMatrix:
        cells.append(Cell.Factory(cell, sheet, settings))
    return cells
    
def ExcelDelimiter():
    try:
        import _winreg
        aReg = _winreg.ConnectRegistry(None, _winreg.HKEY_CURRENT_USER)
        aKey = _winreg.OpenKey(aReg, r'Control Panel\International')
        val, _type = _winreg.QueryValueEx(aKey, 'sList')
        return str(val)
    except (ImportError, WindowsError):
        return LIST_SEPARATOR


class Printer(object):

    def __init__(self, cellMatrix):
        self._cellMatrix = cellMatrix
        
    def Print(self):
        raise NotImplementedError
        
        
class TextPrinter(Printer):

    CELL_SEPARATOR = '\t'
    
    def _ColumnHeaders(self):
        headers = []
        for header in self._cellMatrix:
            if isinstance(header, NewLineCell):
                break
            elif isinstance(header, ColumnHeaderCell):
                headers.append(header)
        return headers
        
    def _GroupHeadersDict(self):
        groupHeaders = OrderedDict()
        for column in self._ColumnHeaders():
            groupLabel = column.GroupLabel
            if groupLabel not in groupHeaders:
                groupHeaders[groupLabel] = 1
            else:
                groupHeaders[groupLabel] += 1
        return groupHeaders
        
    def _GroupHeaders(self):
        text = []
        groupHeaders = self._GroupHeadersDict()
        if groupHeaders:
            for header in groupHeaders:
                text.append(header)
                text.append(groupHeaders[header]*self.CELL_SEPARATOR)
            text.append(NewLineCell().Value)
        return text
        
    def _IsAtEnd(self, index):
        try:
            cell = self._cellMatrix[index]
            nextCell = self._cellMatrix[index+1]
            if not (isinstance(nextCell, NewLineCell) or 
                    isinstance(cell, NewLineCell)):
                return False
        except IndexError:
            pass
        return True

    def Print(self):
        text = []
        text.extend(self._GroupHeaders())
        for index, cell in enumerate(self._cellMatrix):
            text.append(cell.Value)
            if not self._IsAtEnd(index):
                text.append(self.CELL_SEPARATOR)
        return ''.join(text)
        

class Cell(object):
    
    def __init__(self, gridCellInfo, sheet, settings=None):
        self._gridCellInfo = gridCellInfo
        self._sheetClassName = sheet.SheetClass().StringKey()
        self._settings = settings or acm.FDefinition()
        
    @classmethod
    def Factory(cls, gridCellInfo, sheet, settings=None):
        if isinstance(gridCellInfo, RowHeaderCellInfo):
            return RowHeaderCell(gridCellInfo, sheet, settings)
        elif isinstance(gridCellInfo, ColumnHeaderCellInfo):
            return ColumnHeaderCell(gridCellInfo, sheet, settings)
        elif isinstance(gridCellInfo, NewLineCellInfo):
            return NewLineCell()
        elif gridCellInfo.TreeSpecification():
            return TreeSpecCell(gridCellInfo, sheet, settings)
        elif gridCellInfo.RowObject():
            return RowObjectCell(gridCellInfo, sheet, settings)
        return cls(gridCellInfo, sheet, settings)
        
    @property
    def Settings(self):
        return self._settings
                
    @property
    def SheetClassName(self):
        return self._sheetClassName
        
    @property
    def ContextName(self):
        return self._gridCellInfo.Column().Context().Name() or acm.GetDefaultContext().Name()     
        
    @property        
    def ColumnId(self):
        return self._gridCellInfo.Column().ColumnId()
        
    @property        
    def IsHeaderCell(self):
        return self._gridCellInfo.IsHeaderCell()

    @property        
    def Formatter(self):
        if not self.IsHeaderCell:
            return CellFormatter(self._gridCellInfo)
        return HeaderFormatter()
        
    @property
    def Path(self):
        raise NotImplementedError

    @property        
    def Value(self):
        raise NotImplementedError

        
class TreeSpecCell(Cell):

    _encodedArgsCache = {}

    def __init__(self, gridCellInfo, sheet, settings):
        super(TreeSpecCell, self).__init__(gridCellInfo, sheet, settings)
        self._value = None

    @property
    def ScenarioDisplayType(self):
        scenarioSettings = self._gridCellInfo.ScenarioSettings()
        if scenarioSettings:
            return scenarioSettings.ShiftDisplayType()
        return None
        
    @property
    def DistributedMode(self):
        return self._gridCellInfo.RowObject().IsKindOf(acm.FDistributedRow)
        
    @property    
    def Configuration(self):
        return self._gridCellInfo.CalculationSpecification().Configuration()

    @property    
    def ColumnId(self):
        return self._gridCellInfo.CalculationSpecification().ColumnName()
        
    @property    
    def ContextName(self):
        return self._gridCellInfo.CalculationSpecification().ContextName()
    
    @property    
    def TreeSpecification(self):
        return self._gridCellInfo.TreeSpecification()
        
    @property
    def Grouper(self):
        return self.TreeSpecification.Grouper().StringKey()
    
    @property
    def OriginObject(self):
        return self.TreeSpecification.OriginObject().StringKey()
    
    @property
    def Path(self):
        if self.TreeSpecification and self.TreeSpecification.Constraints():
            limitTarget = acm.FLimitTarget()
            limitTarget.TreeSpecification(self.TreeSpecification)
            return limitTarget.Path()
        return ""
            
    @property
    def RowArguments(self):
        rowObj = self._gridCellInfo.RowObject()
        if rowObj not in self._encodedArgsCache:
            xmlArchive = acm.FXmlArchive()
            xmlArchive.Add('treeSpec', self._gridCellInfo.TreeSpecification())
            encoded = base64.b64encode(xmlArchive.Compressed())
            splitted = Split('Row:{0}'.format(encoded), TOPIC_MAX_CHARS)
            rowArg = ExcelDelimiter().join(('"{0}"'.format(s) for s in splitted))
            self._encodedArgsCache[rowObj] = rowArg
        return self._encodedArgsCache[rowObj]
        
    @property
    def ColumnArguments(self):
        columnObj = self._gridCellInfo.Column()
        if columnObj not in self._encodedArgsCache:
            xmlArchive = acm.FXmlArchive()
            xmlArchive.Add('sheetClass', self.SheetClassName)
            xmlArchive.Add('contextName', self.ContextName)
            xmlArchive.Add('columnId', self.ColumnId)
            xmlArchive.Add('configuration', self.Configuration)
            xmlArchive.Add('projectionParts', self._gridCellInfo.ProjectionParts())
            xmlArchive.Add('distributedMode', self.DistributedMode)
            xmlArchive.Add('scenarioDisplayType', self.ScenarioDisplayType)
            encoded = base64.b64encode(xmlArchive.Compressed())
            splitted = Split('Column:{0}'.format(encoded), TOPIC_MAX_CHARS)
            columnArg = ExcelDelimiter().join(('"{0}"'.format(s) for s in splitted))
            self._encodedArgsCache[columnObj] = columnArg
        return self._encodedArgsCache[columnObj]
    
    @property        
    def BasicValue(self):
        rtd_formula = (
           '=RTD("ArenaExcel"{delimiter}'
           '{delimiter}'
           '{delimiter}'
           '"CalculationInterface"{delimiter}'
           '"GetValue"{delimiter}'
           '"{0.SheetClassName}"{delimiter}'
           '"{0.ColumnId}"{delimiter}'
           '"{0.OriginObject}"{delimiter}'
           '"{0.Grouper}"{delimiter}'
           '"{0.Path}"{delimiter}'
           '"{0.ContextName}")'
            )
        return rtd_formula.format(self, delimiter=ExcelDelimiter())
        
    @property        
    def AdvancedValue(self):
        rtd_formula = (
           '=RTD("ArenaExcel"{delimiter}'
           '{delimiter}'
           '{delimiter}'
           '"AdvancedCalculationInterface"{delimiter}'
           '"GetValue"{delimiter}'
           '{0.RowArguments}{delimiter}'
           '{0.ColumnArguments})'         
            )
        return rtd_formula.format(self, delimiter=ExcelDelimiter())
    
    @property
    def Value(self):
        if self._value is None:
            if self.Settings.GetBool('AdvancedCalculation'):
                self._value = self.AdvancedValue
            else: self._value = self.BasicValue
        return self._value
        
        
class RowObjectCell(Cell):

    @property
    def Path(self):
        return self._gridCellInfo.RowObject().StringKey()
    
    @property        
    def Value(self):
        rtd_formula = (
           '=RTD("ArenaExcel"{delimiter}'
           '{delimiter}'
           '{delimiter}'           
           '"CalculationInterface"{delimiter}'
           '"GetValue"{delimiter}'
           '"{0.SheetClassName}"{delimiter}'
           '"{0.ColumnId}"{delimiter}'
           '"{0.Path}"{delimiter}'
           '"{0.ContextName}")'           
            )
        return rtd_formula.format(self, delimiter=ExcelDelimiter())

        
class HeaderCell(Cell):

    @property        
    def Value(self):
        return str(self._gridCellInfo.Value())
        
        
class ColumnHeaderCell(HeaderCell):

    @property
    def GroupLabel(self):
        label = str(self._gridCellInfo.GroupLabel())
        return label if label != 'None' else ''
    
    
class RowHeaderCell(HeaderCell):

    PATH_SEPARATOR = '|'
    INDENTATION = 2 * ' '

    def FullRowPath(self):
        tree = self._gridCellInfo.Tree()
        path = []
        while tree and tree.Parent():
            path.append(tree.StringKey())
            tree = tree.Parent()
        return self.PATH_SEPARATOR.join(reversed(path))
        
    def RowValue(self):
        depth = self._gridCellInfo.Tree().Depth() - 1    
        return self.INDENTATION * depth + self._gridCellInfo.Value()
        
    @property
    def Value(self):
        if self.Settings.GetBool('FullRowPath'):
            return self.FullRowPath()
        return self.RowValue()


class NewLineCell(object):

    NEW_LINE = '\n'

    @property        
    def Value(self):
        return self.NEW_LINE
        

class CellFormatter(object):

    def __init__(self, gridCellInfo):
        self._gridCellInfo = gridCellInfo
        self._appearance = gridCellInfo.Column().ColumnAppearance()
        
    @property
    def IsBold(self):
        return self._appearance.FontBold()
        
    @property
    def BkgColor(self):
        return (self._appearance.Background() or
            self.GetColor('Background'))
        
    @property
    def BkgStripeColor(self):
        return (self._appearance.BkgStripe() or
            self.GetColor('BkgStripe'))
        
    @property
    def Stripes(self):
        if self._appearance.HasKey('Stripes'):
            return self._appearance.Stripes()
        return True
        
    @property
    def TextColor(self):
        return self._appearance.Text()
        
    @property
    def Alignment(self):
        return self._appearance.Alignment()
    
    @property
    def NumFormatter(self):
        return self._gridCellInfo.Formatter()
        
    @staticmethod
    def GetColor(name):
        return acm.GetDefaultContext().GetExtension(
            acm.FColor, acm.FObject, name).Value()
            

class HeaderFormatter(object):

    def __getattr__(self, name):
        return None
        
    def __nonzero__(self):
        return False

        
class HeaderCellInfo(object):

    def __init__(self, cellInfoProxy):
        self._cellInfoProxy = cellInfoProxy
        
    def Value(self):
        return self._cellInfoProxy.Value()
    
    def IsHeaderCell(self):
        return True
        

class ColumnHeaderCellInfo(HeaderCellInfo):

    def Column(self):
        return self._cellInfoProxy

    def Value(self):
        return self.Column().Label()
        
    def GroupLabel(self):
        return self.Column().GroupLabel()
    
    
class RowHeaderCellInfo(HeaderCellInfo):

    def Tree(self):
        return self._cellInfoProxy.Tree()
        
        
class NewLineCellInfo(object):

    def IsHeaderCell(self):
        return False
            

class CellInfoProxy(object):

    def __init__(self, cellValue=None):
        self._cellValue = cellValue
    
    def Value(self):
        return self._cellValue or ''
        

class ColumnHeaderCellInfoProxy(object):

    def __init__(self, gridColumn=None):
        self._gridColumn = gridColumn

    def IsHeaderCell(self):
        return True
        
    def Column(self):
        return self._gridColumn or GridColumnProxy()
        
    def RowObject(self):
        return None


class GridColumnProxy(object):

    def Label(self):
        return ''
        
    def GroupLabel(self):
        return ''
    

class RowIterProxy(object):

    def __init__(self, sheet):
        self._rowIter = sheet.RowTreeIterator(False)
        
    def Iter(self):
        return self._rowIter
        
    def Tree(self):
        return self._rowIter.Tree()
        
    def NextUsingDepthFirst(self):
        return self._rowIter.NextUsingDepthFirst()
    

class VisibleRowIterProxy(RowIterProxy):
    
    def __init__(self, sheet):
        self._rowIter = sheet.RowTreeIterator(True)
        
    def NextUsingDepthFirst(self):
        while self._rowIter.NextUsingDepthFirst():
            parent = self._rowIter.Tree().Parent()
            if parent and parent.IsExpanded():
                return self._rowIter

 
def CreateRowIterProxy(sheet, visibleRowsOnly=False):
    if visibleRowsOnly is True:
        return VisibleRowIterProxy(sheet)
    return RowIterProxy(sheet)

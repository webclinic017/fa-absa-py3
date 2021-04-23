""" Compiled: 2020-09-18 10:38:52 """

#__src_file__ = "extensions/ArenaExcel/etc/ArenaExcelHtmlSheet.py"
import acm
import ArenaExcelSheet

from collections import OrderedDict


class HtmlTablePrinter(ArenaExcelSheet.Printer):

    def __init__(self, htmlMatrix):
        self._htmlMatrix = self._HtmlMatrix(htmlMatrix)
        self._hmtTable = []
        self._hasHeaders = None
        self._columnHeaders = None
        
    def _HtmlMatrix(self, htmlMatrix):
        matrix, row = [], []
        for cell in htmlMatrix:
            if isinstance(cell, ArenaExcelSheet.NewLineCell):
                matrix.append(row)
                row = []
            else:
                row.append(cell)
        matrix.append(row)
        return matrix        

    def _HasHeaders(self):
        if self._hasHeaders is None:
            try:
                self._hasHeaders = all(isinstance(c, HtmlColumnHeaderCell) for c in self._htmlMatrix[0])
            except IndexError:
                self._hasHeaders = False
        return self._hasHeaders
        
    def _ColumnHeaders(self):
        if self._columnHeaders is None:
            self._columnHeaders = self._htmlMatrix[0] if self._HasHeaders() else []
        return self._columnHeaders
        
    def _GroupHeadersDict(self):
        groupHeaders = OrderedDict()
        for column in self._ColumnHeaders():
            groupLabel = column.GroupLabel
            if groupLabel not in groupHeaders:
                groupHeaders[groupLabel] = 1
            else:
                groupHeaders[groupLabel] += 1
        return groupHeaders
            
    def _DataCells(self):
        try:
            return self._htmlMatrix[1:] if self._HasHeaders() else self._htmlMatrix
        except IndexError:
            return []
            
    def _AddGroupHeaders(self):
        groupHeaders = self._GroupHeadersDict()
        if groupHeaders:
            self._hmtTable.append('<tr>')
            for label in groupHeaders:
                self._hmtTable.append('<th colspan="{0}">{1}</th>'.format(groupHeaders[label], label))
            self._hmtTable.append('</tr>')
            
    def _AddColumnHeaders(self):
        columnHeaders = self._ColumnHeaders()
        if columnHeaders:
            self._hmtTable.append('<tr>')
            for column in columnHeaders:
                self._hmtTable.append(column.Value())
            self._hmtTable.append('</tr>')
            
    def _AddDataCells(self):
        dataCells = self._DataCells()
        if dataCells:
            for rowIndex, row in enumerate(dataCells):
                self._hmtTable.append('<tr>')
                for column in row:
                    self._hmtTable.append(column.Value(rowIndex))
                self._hmtTable.append('</tr>')
                
    def Print(self):
        self._hmtTable.append('<table>')
        self._AddGroupHeaders()
        self._AddColumnHeaders()
        self._AddDataCells()
        self._hmtTable.append('</table>')
        return ''.join(self._hmtTable)
        
    
class HtmlCell(object):

    def __init__(self, cell):
        self._cell = cell
        self._styles = []
        
    @classmethod
    def Factory(cls, gridCell, sheet, settings=None):
        cell = ArenaExcelSheet.Cell.Factory(gridCell, sheet, settings)
        return cls.FromArenaExcelSheet(cell)
        
    @classmethod
    def FromArenaExcelSheet(cls, cell):
        if isinstance(cell, ArenaExcelSheet.ColumnHeaderCell):
            return HtmlColumnHeaderCell(cell)
        elif isinstance(cell, ArenaExcelSheet.RowHeaderCell):
            return HtmlHeaderCell(cell)
        elif isinstance(cell, ArenaExcelSheet.NewLineCell):
            return cell
        elif isinstance(cell, ArenaExcelSheet.Cell):
            return HtmlDataCell(cell)
        return cls(cell)    
        
    @property
    def Formatter(self):
        return self._cell.Formatter
        
    @staticmethod
    def RGB(color):
        ref = color.ColorRef()
        colorRefs = {
            'blue': (ref >> 16) & 0xFF,
            'green': (ref >> 8) & 0xFF,
            'red': ref & 0xFF
            }
        rgb = 'rgb({red}, {green}, {blue})'
        return rgb.format(**colorRefs)
        
    @staticmethod
    def LeadingSpaces(aString):
        return len(aString) - len(aString.lstrip(' '))
        
    @classmethod
    def FormattedValue(cls, aString):
        ls = cls.LeadingSpaces(aString)
        return ''.join((ls * '&nbsp;', aString[ls:]))
        
    def GetBkgColor(self, rowIndex=0):
        bkgColor = self.Formatter.BkgColor
        if self.Formatter.Stripes and rowIndex % 2 != 0:
            bkgColor = self.Formatter.BkgStripeColor
        return self.RGB(bkgColor)
            
    def Value(self, rowIndex=0):
        raise NotImplementedError
        

class HtmlHeaderCell(HtmlCell):

    ALIGNMENT = 'left'

    def Value(self, _rowIndex=0):
        hmtTable = '<th align="{0}">{1}</th>' 
        return hmtTable.format(self.ALIGNMENT, self._cell.Value)


class HtmlColumnHeaderCell(HtmlHeaderCell):

    def Value(self, _rowIndex=0):
        hmtTable = '<th>{0}</th>' 
        return hmtTable.format(self._cell.Value)

    @property
    def GroupLabel(self):
        return self._cell.GroupLabel
    
    
class HtmlDataCell(HtmlCell):

    def AddBkgColor(self, rowIndex=0):
        if self.Formatter.BkgColor:
            style = 'background-color:{0};'.format(self.GetBkgColor(rowIndex))
            self._styles.append(style)
            
    def AddTextColor(self):
        if self.Formatter.TextColor:
            style = 'color:{0};'.format(self.RGB(self.Formatter.TextColor))
            self._styles.append(style)
            
    def AddAlignment(self):
        if self.Formatter.Alignment:
            style = 'text-align:{0};'.format(self.Formatter.Alignment)
            self._styles.append(style)
            
    def AddNumberFormat(self):
        if self.Formatter.NumFormatter:
            numDecimals = self.Formatter.NumFormatter.NumDecimals()
            decimals = ''.join(('.', ''.join('0' for d in range(numDecimals)))) if numDecimals else '0'
            style = 'mso-number-format:\#\,\#\#0\{0};'.format(decimals)
            self._styles.append(style)
            
    def AddStyles(self, rowIndex=0):
        if self.Formatter:
            self._styles.append(' style="')
            
            if self._cell.Settings.GetBool('FormattedValue'):            
                self.AddNumberFormat()
            if self._cell.Settings.GetBool('BkgColor'):
                self.AddBkgColor(rowIndex)
            if self._cell.Settings.GetBool('TextColor'):                
                self.AddTextColor()
            if self._cell.Settings.GetBool('Alignment'):                            
                self.AddAlignment()
            self._styles.append('"')
        return ''.join(self._styles)

    def Value(self, rowIndex=0):
        hmtTable = []
        hmtTable.append('<td')
        hmtTable.append(self.AddStyles(rowIndex))
        hmtTable.append('>')
        if self.Formatter.IsBold:
            hmtTable.append('<b>')
        hmtTable.append(self.FormattedValue(self._cell.Value))
        if self.Formatter.IsBold:
            hmtTable.append('</b>')
        hmtTable.append('</td>')
        return ''.join(hmtTable)


def SelectedHtmlCells(sheet):
    selectionMatrix = ArenaExcelSheet.SelectionMatrix(sheet)
    return [HtmlCell.Factory(cell, sheet) for cell in selectionMatrix]
    
def SheetHtmlCells(sheet, visibleCellsOnly=False):
    sheetMatrix = ArenaExcelSheet.SheetMatrix(sheet, visibleCellsOnly)
    return [HtmlCell.Factory(cell, sheet) for cell in sheetMatrix]
    
def HtmlCellsFromSelection(selectionMatrix, sheet):
    return [HtmlCell.Factory(cell, sheet) for cell in selectionMatrix]
    
def HtmlCellsFromSheet(sheetMatrix, sheet):
    return [HtmlCell.Factory(cell, sheet) for cell in sheetMatrix]
    
def HtmlCellsFromArenaExcelSelection(arenaExcelSelection):
    return [HtmlCell.FromArenaExcelSheet(cell) for cell in arenaExcelSelection]
    
def HtmlCellsFromArenaExcelSheet(arenaExcelSheet):
    return [HtmlCell.FromArenaExcelSheet(cell) for cell in arenaExcelSheet]

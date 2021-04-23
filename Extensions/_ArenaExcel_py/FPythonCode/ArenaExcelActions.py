""" Compiled: 2020-09-18 10:38:52 """

#__src_file__ = "extensions/ArenaExcel/etc/ArenaExcelActions.py"
import ArenaExcelHtmlSheet
import FHtmlClipboard
import ArenaExcelSheet
import FClipboard


from ArenaExcelUtils import logger, ClipboardSettings


def Copy(data, clipFormat=FClipboard.CF_TEXT):
    source = FClipboard.ToClipboardData(data)
    FClipboard.SetClipboardData(clipFormat, source)
    
def CopyCells(cells, htmlCells):
    with FClipboard.ClipboardHandler():
        Copy(Html(htmlCells), clipFormat=FClipboard.CF_HTML)
        Copy(Text(cells))
        
def Html(htmlCellMatrix):
    htmlTable = ArenaExcelHtmlSheet.HtmlTablePrinter(htmlCellMatrix).Print()
    return FHtmlClipboard.HtmlClipboard().GetSource(htmlTable)
    
def Text(cellMatrix):
    return ArenaExcelSheet.TextPrinter(cellMatrix).Print()

def CopyAllCells(eii):
    try:
        sheet = eii.ExtensionObject().ActiveSheet()
        sheetMatrix = list(ArenaExcelSheet.SheetMatrix(sheet))
        sheetCells = ArenaExcelSheet.CellsFromSheet(sheetMatrix, sheet, ClipboardSettings())
        sheetHtmlCells = ArenaExcelHtmlSheet.HtmlCellsFromArenaExcelSheet(sheetCells)
        CopyCells(sheetCells, sheetHtmlCells)
    except Exception as err:
        logger.error(err, exc_info=True)

def CopySelectedCells(eii):
    try:
        sheet = eii.ExtensionObject().ActiveSheet()
        selectionMatrix = list(ArenaExcelSheet.SelectionMatrix(sheet))
        selectedCells = ArenaExcelSheet.CellsFromSelection(selectionMatrix, sheet, ClipboardSettings())
        selectedHtmlCells = ArenaExcelHtmlSheet.HtmlCellsFromArenaExcelSelection(selectedCells)
        CopyCells(selectedCells, selectedHtmlCells)
    except Exception as err:
        logger.error(err, exc_info=True)
        
def CopyVisibleCells(eii):
    try:
        sheet = eii.ExtensionObject().ActiveSheet()
        sheetMatrix = list(ArenaExcelSheet.SheetMatrix(sheet, visibleCellsOnly=True))
        sheetCells = ArenaExcelSheet.CellsFromSheet(sheetMatrix, sheet, ClipboardSettings())
        sheetHtmlCells = ArenaExcelHtmlSheet.HtmlCellsFromArenaExcelSheet(sheetCells)
        CopyCells(sheetCells, sheetHtmlCells)
    except Exception as err:
        logger.error(err, exc_info=True)

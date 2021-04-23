import acm, pprint
from FC_UTILS import FC_UTILS as UTILS

def GetSheetColumnCustomLabel(sheet, uniqueId):
    sheetContents = sheet.Contents()
    for contentKey in sheetContents.Keys():
        if contentKey.Text() == "columnsettings":
            for settingKey in sheetContents[contentKey].Keys():
                if uniqueId == settingKey:
                    for valueKey in sheetContents[contentKey][settingKey].Keys():
                        if valueKey.Text() == "customLabel":
                            return sheetContents[contentKey][settingKey][valueKey].Text()
                            
def ListAllColumns(wbname):
    workbookName = wbname
    if workbookName:
        workbook = acm.FWorkbook[workbookName]
        for sheet in workbook.Sheets():
            sheetName = sheet.SheetName()
            print sheetName, ":"
            columns = sheet.ColumnCollection(acm.FColumnCreatorCreateContext())
            for column in columns:
                columnLabel = GetSheetColumnCustomLabel(sheet, column.UniqueId())
                print '    ', column.ColumnId(), '  -  ', columnLabel
                
ListAllColumns('FC_DYNAMIC_DATA')

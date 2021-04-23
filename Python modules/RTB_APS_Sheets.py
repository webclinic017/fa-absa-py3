import acm

workbook_sheet_calc_environment_map = {}
all_worksheets = acm.FWorkbook.Select('')

for workbook in all_worksheets:
    for sheet in workbook.Sheets():
        
        if sheet.CalculationEnvironmentName():
            
            if sheet.CalculationEnvironmentName() not in workbook_sheet_calc_environment_map:
                workbook_sheet_calc_environment_map[sheet.CalculationEnvironmentName()] = {}
                
            if workbook.Name() not in workbook_sheet_calc_environment_map[sheet.CalculationEnvironmentName()]:
                workbook_sheet_calc_environment_map[sheet.CalculationEnvironmentName()][workbook.Name()] = []
                
            sheet_name = sheet.SheetName()
            sheet_class = sheet.TradingSheetDefinition().SheetClass().Name()
            
            if sheet.Name() not in workbook_sheet_calc_environment_map[sheet.CalculationEnvironmentName()][workbook.Name()]:
                workbook_sheet_calc_environment_map[sheet.CalculationEnvironmentName()][workbook.Name()].append((sheet_class, sheet_name))
                

print('{0:35}|{1:40}|{2:35}|{3}'.format('Calc Environment', 'Workbook', 'Sheet Type', 'Work Sheet'))
print('-'*130)
for ce in workbook_sheet_calc_environment_map:
    for wb in workbook_sheet_calc_environment_map[ce]:
        for sheet in workbook_sheet_calc_environment_map[ce][wb]:
            print('{0:35}|{1:40}|{2:35}|{3}'.format(ce, wb, sheet[0], sheet[1]))

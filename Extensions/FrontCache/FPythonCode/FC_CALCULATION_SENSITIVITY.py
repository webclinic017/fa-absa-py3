'''----------------------------------------------------------------------------------------------------------
MODULE                  :       FC_CALCULATION_SENSITIVITY
PROJECT                 :       Front Cache
PURPOSE                 :       Used for extracting values from FReportBuilder for a given object
DEPARTMENT AND DESK     :       All Departments and all Desks.
REQUASTER               :       Front Cache
DEVELOPER               :       Gavin Wienand
CR NUMBER               :       XXXXXX
-------------------------------------------------------------------------------------------------------------
'''
#*********************************************************#
#Importing Modules
#*********************************************************#
import acm
from FC_UTILS import FC_UTILS as UTILS

class FC_CALCULATION_SENSITIVITY:

    def __init__(self, ReportBuilder, RowObject, sensType):
        self.reportBuilder = ReportBuilder
        self.rowObject     = RowObject.FObject
        self.workbook      = acm.FWorkbook[UTILS.Constants.fcGenericConstants.FC_DYNAMIC_SENSITIVITY]
        self.containerName = UTILS.Constants.fcGenericConstants.CONTAINER_NAME
        self.templateName  = UTILS.Constants.fcGenericConstants.TEMPLATE_NAME
        self.objectName = RowObject.PortfolioName
        self.objectNumber = RowObject.PortfolioNumber
        self.sensType = sensType
        if self.sensType==UTILS.Constants.fcGenericConstants.INSTRUMENT:
            self.objectName   = RowObject.InstrumentName
            self.objectNumber = RowObject.InstrumentNumber
            self.workbook     = acm.FWorkbook[UTILS.Constants.fcGenericConstants.FC_DYNAMIC_INS_SENSITIVITY]

    #Returns XSL output based on consumed template
    def returnXmlPortion(self):
        extension    = acm.GetDefaultContext().GetExtension('FXSLTemplate', 'FObject', self.templateName)
        xsl_template = extension.Value()
        transformer  = acm.CreateWithParameter('FXSLTTransform', xsl_template)
        return transformer.Transform(self.output.AsString())

    #Returns the Row Columns of a Vertical Portfolio Sheet
    def returnVertPortRowColumns(self):
        rowColumns = []
        contents = self.tradingSheet.Contents()
        for key in contents:
            if key.AsString() == 'rowColumnCreators':
                i = 0
                creators = contents[key]
                while i < creators.Size():
                    rowColumns.append(creators.At(i).StringKey())
                    i+=1
        return rowColumns

    #Return rows without the trailing pipe
    def returnCleanRows(self, rows):
        row_num = 0
        while row_num < len(rows):
            row = rows[row_num][:-1]
            rows[row_num] = row
            row_num += 1
        return rows

    #Update a dictionary with (str 01,str 02,str 03,str 04) = str 05 setup
    #Additional functions can be created to extract different levels of data.
    def AddVertPortCustom01Values(self, columns, rows):
        #---------------------------------------------------------------------
        #This custom method will update a dictionary that contains;
        #str 01 = The Object in the vertical portfolio sheet
        #str 02 = The Row Column
        #str 03 = One of the yield curve relevant to the object and row column
        #str 04 = The column, tenur in this case
        #str 05 = The cell value
        #Skip the FPortfolioInstrumentAndTrades level
        #---------------------------------------------------------------------
        rowColumns = self.returnVertPortRowColumns()
        for row in rows[1:]:
            row_list = row.split('|')
            row_name = row_list[0]
            if row_name in rowColumns:
                #This means the current row is the Row Column level and
                #the next level will be the yield curve level.
                if row_name == 'Benchmark Delta Per Curve':
                    rowColumn = 'Interest Rate Benchmark Delta Per Yield Curve'
                else:
                    rowColumn = row_name
                continue
            else:
                yieldCurve = row_name
                try:
                    yc = acm.FYieldCurve[row_name]
                    if yc is not None and yc.ArchiveStatus() is 1:
                        yieldCurve = yc.OriginalCurve().Name()
                except Exception, e:
                    print str(e)


            col_num = 0
            for cell in row_list[1:]:
                column    = columns[col_num]
                try:      value = round(float(cell), 8)
                except:   value = 0
                if value: self.final[(self.objectName, self.objectNumber, rowColumn, yieldCurve, column)] = '%.8f' %value
                col_num   += 1

    def AddPortSheetCustom01Values(self, columns, rows):
        #---------------------------------------------------------------------
        #This custom method will update a dictionary that contains;
        #str 01 = The Object at FSingleInstrumentAndTrades level
        #str 02 = The Column
        #str 03 = None
        #str 04 = None
        #str 05 = The cell value
        #Skip the FPortfolioInstrumentAndTrades level
        #---------------------------------------------------------------------
        for row in rows[1:2]:
            row_list = row.split('|')
            col_num = 0
            for cell in row_list[1:]:
                column    = columns[col_num]
                try:      value = round(float(cell), 8)
                except:   value = 0
                if value: self.final[(self.objectName, self.objectNumber, column, 'None', 'None')] = '%.8f' %value
                col_num   += 1

    def AddPortSheetCustom02Values(self, columns, rows):
        #---------------------------------------------------------------------
        #This custom method will update a dictionary that contains;
        #str 01 = The Object at FSingleInstrumentAndTrades level
        #str 02 = The Column
        #str 03 = None
        #str 04 = None
        #str 05 = The cell value
        #Skip the FPortfolioInstrumentAndTrades level
        #---------------------------------------------------------------------
        for row in rows[0:1]:
            row_list = row.split('|')
            col_num = 0
            for cell in row_list[1:]:
                column    = columns[col_num]
                try:      value = round(float(cell), 8)
                except:   value = 0
                if value:
                    self.final[(self.objectName, self.objectNumber, column, 'None', 'None')] = '%.8f' %value
                col_num   += 1

    def AddPortSheetCustom03Values(self, columns, rows):
        #---------------------------------------------------------------------
        #This custom method will update a dictionary that contains;
        #str 01 = The Object at FPortfolioInstrumentAndTrades level
        #str 02 = The Column
        #str 03 = None
        #str 04 = None
        #str 05 = The cell value
        #Skip the FPortfolioInstrumentAndTrades level only read lower levels
        #This module will sum up all the FSingleInstrumentAndTrades levels
        #---------------------------------------------------------------------
        col_val = {}
        for row in rows[1:]:
            row_list = row.split('|')
            col_num = 0
            for cell in row_list[1:]:
                column    = columns[col_num]
                try:      value = float(cell)
                except:   value = 0
                if value:
                    if column not in col_val:
                        col_val[column] = value
                    else:
                        col_val[column] += value
                col_num   += 1

        for column, value in col_val.iteritems():
            if value: self.final[(self.objectName, self.objectNumber, column, 'None', 'None')] = '%.8f' %value

    def createNamedParameter(self, vector, currency):
        param = acm.FNamedParameters();
        param.AddParameter('currency', currency)
        vector.Add(param)

    def setColumnConfig(self):
        vector = acm.FArray()
        for currency in acm.FCurrency.Select(''):
            self.createNamedParameter(vector, currency)
        return acm.Sheet.Column().ConfigurationFromVector(vector)

    def returnVectorValues(self, columnConfig):
        columns = self.tradingSheet.ColumnCollection(acm.FColumnCreatorCreateContext())
        for col in columns:
            columnId = col.ColumnId().Text()
            columnId = columnId[:columnId.find('[0]')]
            try: resultList = self.calcSpace.CreateCalculation(self.node, columnId, columnConfig).Value()
            except: resultList = []
            if str(type(resultList)) == "<type 'FDenominatedValueArray'>":
                for result in resultList:
                    if result.Number():
                        self.final[(self.objectName, self.objectNumber, str(col.ColumnName())+' '+result.Unit(), 'None', 'None')] = '%.8f' %result.Number()
            elif str(type(resultList)) == "<type 'FDenominatedValue'>" and resultList.Number():
                self.final[(self.objectName, self.objectNumber, str(col.ColumnName())+' '+resultList.Unit(), 'None', 'None')] = '%.8f' %resultList.Number()


    def AddPortSheetVector01Values(self):
        columnConfig = self.setColumnConfig()
        vectorValues = self.returnVectorValues(columnConfig)

    def AddPortSheetBucket01Values(self):
        columns = self.tradingSheet.ColumnCollection(acm.FColumnCreatorCreateContext())
        for col in columns:
            print type(col)


    def returnObjectSensitivity(self):
        self.final = {}
        for self.tradingSheet in self.workbook.Sheets():
            self.reportGrid, self.output = self.reportBuilder.createReportGridBySheet(self.tradingSheet, False, self.containerName)
            self.reportGrid.GridBuilder().InsertItem(self.rowObject)
            self.reportBuilder.simulateSheetSettings(self.reportGrid, str(self.tradingSheet.ClassName()))
            self.reportGrid.Generate()

            csv     = self.returnXmlPortion()
            rows    = self.returnCleanRows(csv.split('\r\n')[1:-1])
            columns = self.returnCleanRows([csv.split('\r\n')[0]])[0].split('|')

            if  self.tradingSheet.IsKindOf(UTILS.Constants.fcGenericConstants.FVERTICALPORTFOLIOSHEET):
                self.AddVertPortCustom01Values(columns, rows)
                continue

            if  self.tradingSheet.IsKindOf(UTILS.Constants.fcGenericConstants.FPORTFOLIOSHEET) \
                    and self.tradingSheet.SheetName() == 'FC_SENSITIVITY_VECTOR':
                self.calcSpace = acm.Calculations().CreateCalculationSpace(acm.GetDefaultContext(), UTILS.Constants.fcGenericConstants.FPORTFOLIOSHEET)
                self.node      = self.calcSpace.InsertItem(self.rowObject)
                self.AddPortSheetVector01Values()
                continue

            if  self.tradingSheet.IsKindOf(UTILS.Constants.fcGenericConstants.FPORTFOLIOSHEET) \
            and self.sensType==UTILS.Constants.fcGenericConstants.INSTRUMENT:
                self.AddPortSheetCustom01Values(columns, rows)
                continue

            if  self.tradingSheet.IsKindOf(UTILS.Constants.fcGenericConstants.FPORTFOLIOSHEET) \
            and self.rowObject.RecordType() == UTILS.Constants.fcGenericConstants.PORTFOLIO:
                self.AddPortSheetCustom02Values(columns, rows)
                continue

        return self.final

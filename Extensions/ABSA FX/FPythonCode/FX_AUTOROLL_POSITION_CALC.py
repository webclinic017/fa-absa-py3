import acm, ael
import FReportAPI
import FReportAPIBase
from FBDPCurrentContext import Logme

class POSITION_CALC_PER_TIME_BUCKET():
    def __init__(self, queryFolder, currency):
        self.__workbookName = 'FX_AUTOROLL_TIMEBUCKET'
        self.__workbook = None
        self.__getWorkbook()
        self.__sheetsPerCurrency = {}
        self.__getSheet()
        self.__queryFolder = queryFolder
        self.__currency = currency
        self.__reportParameters = None
        self.__reportBuilder = None
        self.__setReportAPIParameters()
        self.__output = None
        self.__positionPerCurrencyPerTimeBucket = {}
        if self.__currency in self.__sheetsPerCurrency.keys():
            self.__generateReport()
            self.__csv = self.__returnXmlPortion()
            self.__headers = self.__returnCleanHeaders(self.__csv.splitlines()[0])
            self.__rows = self.__returnCleanRows(self.__csv.splitlines()[1:])
            self.__setPositionPerCurrencyPerTimeBucket()

    @property
    def positionPerCurrencyPerTimeBucket(self):
        return self.__positionPerCurrencyPerTimeBucket
    
    @property
    def timeBucketNames(self):
        return self.__headers
        
    def __getWorkbook(self):
        try:
            self.__workbook = acm.FWorkbook.Select01('name = "' + self.__workbookName + '" and createUser = ' + str(acm.FUser['FMAINTENANCE'].Oid()), '')
            if not self.__workbook:
                Logme()('ERROR: Could not find the workbook in Front Arena %s' %self.__workbookName, 'ERROR')
        except Exception, e:
            self.__workbook = None
            Logme()('ERROR: Could not find the workbook in Front Arena %s' %self.__workbookName, 'ERROR')
    
    def __getSheet(self):
        if self.__workbook:
            for sheet in self.__workbook.Sheets():
                self.__sheetsPerCurrency[sheet.SheetName()] = sheet
    
    def __setReportAPIParameters(self):
        self.__reportParameters = FReportAPI.FWorksheetReportApiParameters(includeRawData=True)
        self.__reportBuilder = FReportAPIBase.FReportBuilder(self.__reportParameters)
    
    def __generateReport(self):
        reportGrid, self.__output = self.__reportBuilder.createReportGridBySheet(self.__sheetsPerCurrency[self.__currency], False, 'AutoRollTimeBucket')
        reportGrid.GridBuilder().InsertItem(self.__queryFolder)
        try:
            reportGrid.Generate()
        except Exception, e:
            Logme()('ERROR: Could not generate the report %s' %str(e), 'ERROR')
        
    def __returnXmlPortion(self):
        extension = acm.GetDefaultContext().GetExtension('FXSLTemplate', 'FObject', 'FCSVBasic')
        xsl_template = extension.Value()
        transformer = acm.CreateWithParameter('FXSLTTransform', xsl_template)
        return transformer.Transform(self.__output.AsString())
    
    def __returnCleanRows(self, rows):
        row_num = 0
        while row_num < len(rows):
            row = rows[row_num][:-1]
            rows[row_num] = row
            row_num += 1
        return rows

    def __returnCleanHeaders(self, headers):
        headersList = headers.split('|')
        headersList = headersList[:len(headersList) - 1]
        dateHeaderList = []
        for item in headersList:
            dateHeaderList.append(ael.date(item).to_string('%Y-%m-%d'))
        return dateHeaderList
        
    def __setPositionPerCurrencyPerTimeBucket(self):
        count = 2
        rowLength = len(self.__rows)
        while count < rowLength:
            values = self.__rows[count].split('|')
            currency = values[0]
            columnCount = 1
            dataList = []
            while columnCount <= 8:
                try:
                    dataList.append(round(-1*float(values[columnCount]), 2))
                except:
                    Logme()('ERROR: %s : Got the following value from Trading Manager %s' %(self.__queryFolder.Name(), str(values[columnCount])), 'ERROR')
                    dataList.append(0.00)
                columnCount += 1
            self.__positionPerCurrencyPerTimeBucket[currency] = dataList
            count = count + 1

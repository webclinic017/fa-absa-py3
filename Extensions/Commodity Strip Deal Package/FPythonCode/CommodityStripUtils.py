
from __future__ import print_function
import acm
from CommodityStripExtensionPoints import CustomStripTypeFromInstruments, CustomExpiryTypeFromInstruments, CustomStructureTypeFromInstruments, StripDealTypeMapping, CustomGetBulletExpiryDate, ExportHook, ImportHook, EXCEL_SEPARATOR, EXCEL_NEW_LINE, InitTrade, SelectMonthFuture
from DealPackageDevKit import DealPackageException, DealPackageUserException, CommandActionBase
from DealPackageUtil import UnDecorate

def GetBulletExpiryDate(underlying, month, year, useCurrentFuture):
    customExpiry = CustomGetBulletExpiryDate(underlying, month, year, useCurrentFuture)
    if customExpiry is not None:
        return customExpiry
    else:
        calendar = GetSettlementCalendar(underlying)
        if useCurrentFuture and underlying.InsType() == 'Future/Forward':
            expDateOnly = calendar.AdjustBankingDays(underlying.ExpiryDateOnly(), -2)
        else:
            monthDate = acm.Time.DateFromYMD(year, month, 1)
            expDateOnly = calendar.ModifyDate(None, None, monthDate, 'EOM')
        dateAsTime = acm.Time.DateTimeToTime(expDateOnly)
        # Set expiry time to 22:59
        return acm.Time.DateTimeFromTime(dateAsTime + 82740)

def GetSettlementCalendar(instrument):
    commodity = instrument.UnderlyingOrSelf()
    return commodity.SettlementCalendar() if commodity.SettlementCalendar() else instrument.Currency().Calendar()

def IsSameMonthExpiry(ins1, ins2):
    return (acm.Time.DateToYMD(ins1.ExpiryDateOnly())[0] == acm.Time.DateToYMD(ins2.ExpiryDateOnly())[0] and
            acm.Time.DateToYMD(ins1.ExpiryDateOnly())[1] == acm.Time.DateToYMD(ins2.ExpiryDateOnly())[1])

def RemoveDuplicateCurrentFutures(allFutures):
    if not allFutures:
        return allFutures
    nonDuplicateFutures = []
    sameMonthFutures = [allFutures[0]]
    currentMonthFuture = allFutures[0]
    for future in range(1, len(allFutures)):
        if not IsSameMonthExpiry(currentMonthFuture, allFutures[future]):
            nonDuplicateFutures.append(SelectMonthFuture(sameMonthFutures))
            sameMonthFutures = []
        sameMonthFutures.append(allFutures[future])
    nonDuplicateFutures.append(SelectMonthFuture(sameMonthFutures))
    return nonDuplicateFutures

def GetCurrentFuturesAsMonthDict(currentFutures):
    currentFuturesDict = acm.FDictionary()
    for future in currentFutures:
        currentFuturesDict.AtPut(GetMonth(future.ExpiryDateOnly()), future)
    return currentFuturesDict

def GetCurrentFutures(dp):
    und = dp.GetAttribute('baseUnderlying')
    if und:
        allDerivatives = acm.FInstrument.Select("underlying = '%s' and currency = '%s' and generic = false and otc = false and insType = 'Future/Forward' " % (und.Name(), und.Currency().Name()))
        compareEndDate = LastDayOfMonth(dp.GetAttribute('stripDates_endDate'))
        compareStartDate = acm.Time.FirstDayOfMonth(dp.GetAttribute('stripDates_startDate'))
        futures = sorted([i for i in allDerivatives if acm.Time.DateDifference(compareEndDate, i.ExpiryDateOnly()) >= 0 and acm.Time.DateDifference(compareStartDate, i.ExpiryDateOnly()) <= 0], key=getTimeSortingKey)
        futuresAsList = RemoveDuplicateCurrentFutures(futures)
        return GetCurrentFuturesAsMonthDict(futuresAsList)
    else:
        return acm.FDictionary()

def LastDayOfMonth(inputDate):
    return acm.Time.DateFromYMD(acm.Time.DateToYMD(inputDate)[0], acm.Time.DateToYMD(inputDate)[1], acm.Time.DaysInMonth(inputDate))

def getTimeSortingKey(ins):
    # return the difference between today and the expiry date of the instrument
    return acm.Time.DateDifference(ins.ExpiryDateOnly(), acm.Time.DateToday())

def getTimePeriodSortingKey(ins):
    return acm.Time.DateDifference(acm.Time.DateAdjustPeriod(acm.Time.DateToday(), ins.ExpiryPeriod()), acm.Time.DateToday())

def FirstDate(date1, date2):
    return date1 if acm.Time.DateDifference(date1, date2) < 0 else date2

def LastDate(date1, date2):
    return date1 if acm.Time.DateDifference(date1, date2) > 0 else date2

def GetIsCurrentFutureFromInstruments(instruments):
    if len(instruments) > 1:
        und = instruments[0].Underlying()
        for i in range(1, len(instruments)):
            if instruments[i].Underlying() != und:
                return True
    return False

def GetStripTypeFromInstruments(instruments):
    stripType = CustomStripTypeFromInstruments(instruments)
    ins = instruments[0]
    if stripType is None:
        stripTypeMapping = {'Future/Forward':'Bullet','Average Future/Forward':'Asian', 'Option':'BulletOption'}
        stripType = stripTypeMapping.get(ins.InsType(), '')
    if stripType not in StripDealTypeMapping():
        raise DealPackageException ('Inconcictency in strip type customizations')
    return stripType

def IsFirstDayOfMonth(date):
    return acm.Time.DateDifference(date, acm.Time.FirstDayOfMonth(date)) == 0

def IsLastDayOfMonth(date):
    return acm.Time.DateDifference(date, acm.Time.DateAddDelta(acm.Time.FirstDayOfMonth(acm.Time.DateAddDelta(date, 0, 1, 0)), 0, 0, -1)) == 0

def IsCustomExpiryDate(ins):
    expiryAsYMD = acm.Time.DateToYMD(ins.ExpiryDateOnly())
    standardExp = GetBulletExpiryDate(ins.Underlying(), expiryAsYMD.At(1), expiryAsYMD.At(0), False)
    return acm.Time.DateDifference(standardExp, ins.ExpiryDate()) != 0
    
def GetExpiryTypeFromInstruments(instruments):
    expiryType = CustomExpiryTypeFromInstruments(instruments)
    if expiryType is None:
        if len(instruments) >= 1:
            if instruments[0].InsType() == 'Average Future/Forward':
                # Asian strip
                startDate = instruments[0].LegStartDate()
                endDate = instruments[len(instruments) - 1].LegEndDate()
                startStandard = IsFirstDayOfMonth(startDate)
                endStandard = IsLastDayOfMonth(endDate)
                if not (startStandard and endStandard):
                    firstEnd = instruments[0].LegEndDate()
                    firstEndStandard = IsLastDayOfMonth(firstEnd)
                    if firstEndStandard or len(instruments) == 1:
                        return 'Custom'
                    else:
                        return 'Custom Settlement'
            else:
                # Bullet
                if not GetIsCurrentFutureFromInstruments(instruments):
                    lastComponent = instruments[len(instruments) - 1]
                    if IsCustomExpiryDate(lastComponent):
                        return 'Custom'
        expiryType = 'Standard'
    return expiryType
    
def GetStructureTypeFromInstruments(instruments):
    structureType = CustomStructureTypeFromInstruments(instruments)
    if structureType is None:
        if len(instruments) == 1:
            if instruments[0].InsType() == 'Future/Forward' or instruments[0].InsType() == 'Option':
                return 'Single Leg'
            elif instruments[0].InsType() == 'Average Future/Forward':
                if acm.Time.DateDifference(instruments[0].LegEndDate(), acm.Time.DateAdjustPeriod(instruments[0].LegStartDate(), '1M')) > 1:
                    return 'Single Leg'
        elif len(instruments) > 1 and instruments[0].InsType() == 'Option':
            expiryMonth = acm.Time.FirstDayOfMonth(instruments[0].ExpiryDateOnly())
            for i in range(1, len(instruments)):
                if expiryMonth != acm.Time.FirstDayOfMonth(instruments[i].ExpiryDateOnly()):
                    return 'Strip'
            return 'Single Leg'
    else:
        return structureType
    return 'Strip'

def UpdateTradeInstrument(trade, instrument):
    if not instrument.IsInfant():
        instrument = instrument.StorageImage()
                
    tradeIns = trade.Instrument().Instrument()
    for dpLink in trade.DealPackageTradeLinks():
        for tradeLink in dpLink.DealPackage().TradeLinks():
            if tradeLink.Instrument() == tradeIns and tradeLink.Trade() != trade.Trade():
                dpLink.DealPackage().AddInstrument(instrument)
                break
        else:
            for insLink in dpLink.DealPackage().InstrumentLinks():
                
                if insLink.Instrument() == tradeIns:
                    insLink.Instrument(instrument)
                    break
            else:
                if len(dpLink.DealPackage().InstrumentLinks()) == 1 and len(dpLink.DealPackage().TradeLinks()) == 1:
                    dpLink.DealPackage().InstrumentLinks().First().Instrument(instrument)
                else:
                    print ('COULD NOT UPDATE INSTRUMENT LINK IN %s FOR TRADE' % dpLink.DealPackage().DefinitionName(), trade.Oid(), tradeIns.Oid(), [(insLink.Instrument() == tradeIns, insLink.Instrument().Oid()) for insLink in dpLink.DealPackage().InstrumentLinks()])

    trade.Instrument(instrument)
    InitTrade(UnDecorate(trade))

def ValidateDateInMonth(input, monthDate, calendar):
    transformedDate = TransformToDateInMonth(input, monthDate)

    try:
        acm.Time.AsDate(transformedDate)
    except:
        raise DealPackageUserException('Not a valid date')

    ymd = acm.Time().DateToYMD(monthDate)    
    ymdDate = acm.Time().DateToYMD(transformedDate)

    if not (ymd[0] == ymdDate[0] and ymd[1] == ymdDate[1]):
        raise DealPackageUserException('Date must be in the current month')

    if calendar and calendar.IsNonBankingDay(None, None, transformedDate):
        raise DealPackageUserException('Not a valid business day according to the %s calendar' % calendar.Name())
    
def TransformToDateInMonth(input, monthDate):
    date = ''
    timeOfDay = 0
    monthDateOnly = acm.Time.AsDate(monthDate)
    ymd = acm.Time().DateToYMD(monthDateOnly)    
    try:
        day = int(input)
        if 0 < day and day <= acm.Time().DaysInMonth(monthDateOnly): 
            date = acm.Time().DateFromYMD(ymd[0], ymd[1], day)
            timeOfDay = acm.Time.DateTimeToTime(monthDate) - acm.Time.DateTimeToTime(acm.Time.AsDate(monthDate))
    except:
        pass
    if date == '':
        period = acm.Time().PeriodSymbolToDate(input)
        if period:
            date = period
            timeOfDay = acm.Time.DateTimeToTime(monthDate) - acm.Time.DateTimeToTime(acm.Time.AsDate(monthDate))
        else:
            # No time period or integer number of days, should be a date
            return input

    # Keep the time stamp if a period or number of days is entered
    dateAsTime = acm.Time.DateTimeToTime(date) + timeOfDay
    return acm.Time.DateTimeFromTime(dateAsTime)
    
def CopyTrade(trade):
    copy = trade.StorageNew()
    copy.Instrument = trade.Instrument().StorageNew()
    copy.Instrument().InitializeUniqueIdentifiers()
    return copy

GetMonth = lambda date:tuple(acm.Time.DateToYMD(date)[:2])

LockedInstrumentPartAttributes = [
'stripDates_startDate',
'stripDates_endDate',
'structureType',
'stripType',
'isOptionStrip',
'expiryType',
'instrumentGroup',
'baseUnderlying',
'underlying',
'quotation',
'contractSizeInQuotation',
'currency',
'otc',
'payDayOffset',
'payOffsetMethod',
'payDayMethod',
'fxSource',
'convType',
'fxFixRule',
'fixingSource',
'importStripComponents',
'insPackageName',
'suggestNameButton',
'contractsPerPeriod',
'optionData1_optionType',
'optionData1_strikePrice',
'optionData2_optionType',
'optionData2_strikePrice',
'optionData3_optionType',
'optionData3_strikePrice',
'optionData4_optionType',
'optionData4_strikePrice',
'optionData5_optionType',
'optionData5_strikePrice',
'exerciseType',
'settlementType',
'payType',
'spotDaysOffset',
'useCurrentFuture']

class StripMonth:

    def __init__(self, month, year):
        self._month = month
        self._year = year
    
    def Add(self, addition):
        fraction = (self.Month() + addition) % 12
        if fraction != 0:
            self.Year(self.Year() + int((self.Month() + addition) / 12.0))
            self.Month((self.Month() + addition) % 12)
        else:
            self.Year(self.Year() + int((self.Month() + addition) / 12.0) - 1)
            self.Month(12)
        

    def Month(self, value = 'NoValue'):
        if value == 'NoValue':
            return self._month
        else:
            self._month = value

    def Year(self, value = 'NoValue'):
        if value == 'NoValue':
            return self._year
        else:
            self._year = value

    def IsEqual(self, compareMonth):
        return self.Month() == compareMonth.Month() and self.Year() == compareMonth.Year()

    def IsBigger(self, compareMonth):
        return compareMonth.Year() < self.Year() or (compareMonth.Year() == self.Year() and compareMonth.Month() < self.Month())

    def IsBiggerEqual(self, compareMonth):
        return self.IsEqual(compareMonth) or self.IsBigger(compareMonth)

    def IsSmaller(self, compareMonth):
        return not self.IsBiggerEqual(compareMonth)
    
    def IsSmallerEqual(self, compareMonth):
        return not self.IsBigger(compareMonth)
        
    def FirstDayOfMonth(self):
        return acm.Time.DateFromYMD(self.Year(), self.Month(), 1)

    def DaysInMonth(self):
        return acm.Time.DaysInMonth(self.FirstDayOfMonth())
    
    def LastDayOfMonth(self):
        return acm.Time.DateFromYMD(self.Year(), self.Month(), self.DaysInMonth())

    def Copy(self):
        return StripMonth(self.Month(), self.Year())
    
    def pp(self):
        return '--- Month: %i, Year: %i ---' % (self.Month(), self.Year())



class TransactionHistoryAction(CommandActionBase):
    DISPLAY_NAME = 'Transaction History'

    def Invoke(self):
        import TransactionHistory
        arr = acm.FArray()
        arr.Add(acm.FTransactionHistory)
        customPanel = TransactionHistory.TransactionHistoryPanel()
        query = self.getQuery()
        ii = acm.StartFASQLEditor('Transaction History', arr, None, query, None, None, True, customPanel)
        ii.SortColumn('UpdateTime', False)

    def Enabled(self):
        return not self.DealPackage().IsInfant()

    def getQuery(self):
        query = acm.CreateFASQLQuery(acm.FTransactionHistory, 'AND')

        time = query.AddOpNode('AND')
        time.AddAttrNode('UpdateTime', 'LESS_EQUAL', None)
        time.AddAttrNode('UpdateTime', 'GREATER_EQUAL', None)

        name = query.AddOpNode('OR')
        name.AddAttrNode('Name', 'RE_LIKE_NOCASE', None)

        description = query.AddOpNode('OR')
        description.AddAttrNode('Description', 'RE_LIKE_NOCASE', None)

        version = query.AddOpNode('OR')
        version.AddAttrNode('Version', 'LESS_EQUAL', None)
        version.AddAttrNode('Version', 'GREATER_EQUAL', None)

        subquery = query.AddOpNode('OR')
        first = self.DealPackage().Trades().First().Originator().Oid()
        last = self.DealPackage().Trades().Last().Originator().Oid()
        sub = subquery.AddOpNode('AND')
        typeNode = sub.AddOpNode('OR')
        typeNode.AddAttrNode('TransRecordType', 'EQUAL', 19)
        sub.AddAttrNodeNumerical('RecordId', first, last)

        user = query.AddOpNode('OR')
        user.AddAttrNode('UpdateUser.Name', 'RE_LIKE_NOCASE', None)

        return query

def GetStrip(tempDeal):
    strip = None
    links = tempDeal.TradeAt('Trade').DealPackageTradeLinks()
    for link in links:
        if not link.DealPackage().IsTransient():
            strip = link.DealPackage()
            break
    return strip
    
class Clipboard(object):
    def __init__(self, dp):
        self._dp = dp
       
    def __DealPackage(self):
        return self._dp
        
    def __DataToClipboard(self, text):
        import FClipboardUtilities
        FClipboardUtilities.SetClipboardText(text)

    def __FetchData(self):
        return ExportHook(self.__DealPackage())
        
    def __SetData(self, data):
        ImportHook(self.__DealPackage(), data)
        
    def __FormatData(self, data):
        text = ''
        for row in data:
            for value in row:
                text = text + str(value) + EXCEL_SEPARATOR
            text = text + EXCEL_NEW_LINE
        return text[:-1]
        
    def __DataStringToMatrix(self, data):
        dataAsMatrix = []
        for row in data.split(EXCEL_NEW_LINE):
            dataAsMatrix.append(row.split(EXCEL_SEPARATOR))
        return dataAsMatrix[:-1]
            
    def DpToClipboard(self):
        data = self.__FetchData()
        text = self.__FormatData(data)
        self.__DataToClipboard(text)
        
    def ClipboardToDp(self):
        import FClipboardUtilities

        dataAsString = FClipboardUtilities.GetClipboardText()
        dataAsMatrix = self.__DataStringToMatrix(dataAsString)      
        self.__SetData(dataAsMatrix)

class StripPriceFormatter(object):
    #Use standard fomatter InstrumentDefinitionPrice but do not show NaN
    def __init__(self):
        self.baseFormatter = acm.Get('formats/InstrumentDefinitionPrice')
    
    def Format(self, value):
        # Going from the db to the GUI
        if value is None:
            return ''
        return self.baseFormatter.Format(value)
    
    def __getattr__(self, name):
        # Handle Parse as well as other FNumFormatter methods
        return getattr(self.baseFormatter, name) 

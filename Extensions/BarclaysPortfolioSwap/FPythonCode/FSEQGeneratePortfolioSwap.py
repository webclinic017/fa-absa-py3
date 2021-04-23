""" Compiled: 2013-11-07 14:33:49 """

import acm
import ael
import FBDPGui

import FSEQPortfolioSwap
reload(FSEQPortfolioSwap)
import FSEQPortfolioSwapUtil as Util
reload(Util)

from PS_FormUtils import DateField


def NameComp(x, y):
    if x.Name().upper() > y.Name().upper():
        return 1
    elif x.Name().upper() < y.Name().upper():
        return -1
    return 0
    
def SortByName(collection):
    collection.sort(NameComp)
    
def ConvertPeriodToDate(periodOrDate):
    return acm.Time.PeriodSymbolToDate(periodOrDate) and \
            acm.Time.PeriodSymbolToDate(periodOrDate) or periodOrDate
            
def ConvertResetDates(startDate, endDate, singleFixingDate, isSingleDateMode):
    startDate = isSingleDateMode and ConvertPeriodToDate(singleFixingDate) or ConvertPeriodToDate(startDate)
    endDate = isSingleDateMode and startDate or ConvertPeriodToDate(endDate)
    return (startDate, endDate)

def ValidDate(dateAsString):
    try:
        acm.Time.AsDate(dateAsString)
        return True
    except:
        return False

portSwaps = [pfs for pfs in acm.FPortfolioSwap.Select("")]
rateIndices = [rateIndex for rateIndex in acm.FRateIndex.Select("")]
today = acm.Time.DateToday()
calendars = [calendar for calendar in acm.FCalendar.Select("")]
daycountMethods = [e for e in acm.FEnumeration["enum(DaycountMethod)"].Enumerators() \
                    if str(e) != "None"]
paydayOffsetMethods = [e for e in acm.FEnumeration["enum(BusinessDayMethod)"].Enumerators() \
                    if str(e) != "None"]

SortByName(portSwaps)
SortByName(rateIndices)
SortByName(calendars)
daycountMethods.sort()
paydayOffsetMethods.sort()

ttFixingDate = 'A single date for which fixing will be made'
ttTerminate = 'If toggled, the portfolio swap will be terminated and the end return resets will be fixed.'
ttFixingMode = 'If toggled, fixing will be made for the single fixing date \'Fixing Date\' without regeneration of legs'
ttPfSwap = 'Portfolio swap instrument'
ttPreviousPfSwap = 'The previous Portfolio Swap in case the current swap is next in a continuous sequence of Portfolio Swaps in the same portfolio'
ttRateIndex = 'Rate index for daily funding rates'
ttRollingBaseDay = 'The start day of the first rolling period (portfolio swap start date is default)'
ttFixPeriod = 'Use fix period lengths without adjustment for weekends'
ttPaydayOffset = 'The number of banking days from cash flow end day until cash flow pay day'
ttpaydayOffsetMethod = 'Defines how weekends should be handled when calculating cash flow pay day'
ttStartDate = 'The start date (inclusive) of the Portfolio Swap generate script.'
ttStartDateCustom = 'Custom start date.'
ttEndDate = 'The end date (inclusive) of the Portfolio Swap generate script.'
ttEndDateCustom = 'Custom end date.'

START_DATES = DateField.get_captions([
    'Inception',
    'First Of Year',
    'Last of Previous Year',
    'First Of Month',
    'Last of Previous Month',
    'TwoBusinessDaysAgo',
    'PrevBusDay',
    'Custom Date'])

END_DATES = DateField.get_captions([
    'PrevBusDay',
    'Now',
    'Custom Date'])

class PortfolioSwapVariables(FBDPGui.AelVariables):
    def __init__(self):
        # [fieldId, fieldLabel, fieldType, fieldValues, defaultValue, isMandatory, insertItemsDialog, toolTip, callback, enabled]
        self.ael_variables = [
            ['fixingDate', 'Fixing date_Fixing', 'string', END_DATES, 'Now', 0, 0, ttFixingDate, 0, 1],
            
            ['startDate', 'Start Date', 'string', START_DATES, 'Yesterday', 1, 0, ttStartDate],
            ['startDateCustom', 'Start Date Custom', 'string', None, DateField.read_date('First Of Month'), 1, 0, ttStartDateCustom],
            ['endDate', 'End Date', 'string', END_DATES, 'Now', 1, 0, ttEndDate],
            ['endDateCustom', 'End Date Custom', 'string', None, DateField.read_date('Now'), 1, 0, ttEndDateCustom],
            
            ['regenerate', 'Regenerate legs and cash flows_Fixing', 'int', [0, 1], 0, 0, 0],
            ['fixingMode', 'Single fixing day_Fixing', 'int', [0, 1], 1, 0, 0, ttFixingMode],
            ['terminate', 'Terminate Swap_Termination', 'int', [0, 1], 0, 0, 0, ttTerminate],
            ['pfSwap', 'Portfolio swap_Parameters', 'FPortfolioSwap', portSwaps, None, 1, 0, ttPfSwap],
            ['previousPfSwap', 'Previous portfolio swap_Parameters', 'FPortfolioSwap', portSwaps, None, 0, 0, ttPreviousPfSwap],
            ['floatRef', 'Float rate reference_Parameters', 'FRateIndex', rateIndices, None, 1, 0, ttRateIndex],
            ['calendar', 'Reset calendar_Parameters', 'FCalendar', calendars, None, 1, 0],
            ['daycountMethod', 'Day count method_Parameters', 'string', daycountMethods, 'ACT/360', 1, 0],
            ['rollingBaseDay', 'Rolling base day_Parameters', 'string', None, '', 0, 0, ttRollingBaseDay],
            ['isFixPeriod', 'Fix Period_Parameters', 'int', [0, 1], 0, 0, 0, ttFixPeriod],
            ['paydayOffset', 'Payday offset_Parameters', 'dateperiod', None, '0d', 1, 0, ttPaydayOffset],
            ['paydayOffsetMethod', 'Pay Offset Method_Parameters', 'enum(BusinessDayMethod)', paydayOffsetMethods, 'Following', 1, 0, ttpaydayOffsetMethod],
            ['spreadLong', 'Spread long (bp)_Parameters', 'double', None, 0.0, 1, 0],
            ['spreadShort', 'Spread short (bp)_Parameters', 'double', None, 0.0, 1, 0],
            ['payOrReceive', 'Total return leg pay or receive_Parameters', 'string', ['Pay', 'Receive'], 'Pay', 0, 0]]

        FBDPGui.AelVariables.__init__(self, *self.ael_variables)

    def cBFixingMode(self, index, fieldValues):
        isSingleDateMode = '0' != fieldValues[index] and 1 or 0
        notIsSingleDateMode = not isSingleDateMode and 1 or 0

        self.fixingDate.enable(isSingleDateMode)
        self.resetStartDate.enable(notIsSingleDateMode)
        self.resetEndDate.enable(notIsSingleDateMode)
        self.regenerate.enable(notIsSingleDateMode)
        return fieldValues

def ValidateInput(dictionary):
    isValidInput = True
    fixingMode = dictionary["fixingMode"]
    fixingDate = dictionary["fixingDate"]
    pfSwap = dictionary["pfSwap"]
    previousPfSwap = dictionary["previousPfSwap"]
    resetStartDate = dictionary["resetStartDate"]
    resetEndDate = dictionary["resetEndDate"]
    regenerate = dictionary["regenerate"]
    calendar = dictionary["calendar"]
    rollingBaseDay = dictionary["rollingBaseDay"]
    isFixPeriod = dictionary["isFixPeriod"]
    spreadLong = dictionary["spreadLong"]
    spreadShort = dictionary["spreadShort"]
    payOrReceive = dictionary["payOrReceive"]

    returnLegIsPayLeg = ("Pay" == payOrReceive) and True or False
    (resetStartDate, resetEndDate) = ConvertResetDates(resetStartDate, \
                                                        resetEndDate, \
                                                        fixingDate, \
                                                        fixingMode)
    
    if fixingMode:
        regenerate = False

    if pfSwap:
        pfsStartDate = pfSwap.StartDate()
        pfsEndDate = pfSwap.ExpiryDate()
    else:
        acm.Log("No Portfolio Swap selected")
        isValidInput = False


    if isValidInput:
        if not ValidDate(resetStartDate):
            acm.Log("Invalid start date: %s"%resetStartDate)
            isValidInput = False            
    
    if isValidInput:
        if not ValidDate(resetEndDate):
            acm.Log("Invalid end date: %s"%resetEndDate)
            isValidInput = False            

    if isValidInput:
        if "Terminated" == pfSwap.OpenEnd():
            acm.Log("The selected portfolio swap is terminated. Please select a live portfolio swap.")
            isValidInput = False

    if isValidInput:
        if not pfSwap.FundPortfolio():
            acm.Log("No valid portfolio selected for portfolio swap '%s'"%pfSwap.Name())
            isValidInput = False

    if isValidInput:
        if previousPfSwap:
            if "Terminated" != previousPfSwap.OpenEnd():
                acm.Log("The previous portfolio swap should be terminated.")
                isValidInput = False
            if isValidInput and previousPfSwap.FundPortfolio() != pfSwap.FundPortfolio():
                acm.Log("The previous portfolio swap must refer to the same portfolio as the current swap.")
                isValidInput = False
    
    if isValidInput:
        if acm.Time.DateDifference(resetStartDate, resetEndDate) > 0:
            acm.Log("Start date can not be later than end date. Please check reset dates.")
            isValidInput = False
    
    if isValidInput:
        if acm.Time.DateDifference(resetEndDate, acm.Time.DateToday()) > 0:
            acm.Log("Can not generate resets later than todays date. Please select an earlier to date.")
            isValidInput = False
            
    if isValidInput:
        if acm.Time.DateDifference(resetStartDate, pfsStartDate) < 0:
            acm.Log("Can not generate resets previous of portfolio swap start date. Please select other reset dates.")
            isValidInput = False
            
    if isValidInput:
        if "Open End" != pfSwap.OpenEnd() and acm.Time.DateDifference(resetEndDate, pfsEndDate) > 0:
            acm.Log("Can not generate resets after portfolio swap end date. Please select other reset dates.")
            isValidInput = False
    
    if isValidInput:
        if rollingBaseDay and not ValidDate(rollingBaseDay):
            acm.Log("Invalid rolling base date: %s"%rollingBaseDay)
            isValidInput = False
    
    if isValidInput:
        if rollingBaseDay and acm.Time.DateDifference(rollingBaseDay, pfsStartDate) < 0:
            acm.Log("Rolling base day can not be before the portfolio swap start day.")
            isValidInput = False

    if isValidInput:
        if None == spreadLong:
            acm.Log("Please define a long spread. Use 0.0 if no spread is intended.")
            isValidInput = False

    if isValidInput:
        if None == spreadShort:
            acm.Log("Please define a short spread. Use 0.0 if no spread is intended.")
            isValidInput = False
            
    if isValidInput:
        if "Open End" == pfSwap.OpenEnd():
            if regenerate and acm.Time.DateDifference(pfsStartDate, resetStartDate):
                acm.Log("Can not regenerate an open ended portfolio swap with a reset from date different from the portfolio swap start date. Please adjust reset from date.")
                isValidInput = False
    
    if isValidInput:
        if calendar.IsNonBankingDay(None, None, resetStartDate):
            acm.Log("Warning: The selected reset from date is not a banking day according to the selected calendar. Fixing will begin on the first banking day in the period.")
            
    return isValidInput

ael_variables = PortfolioSwapVariables()
def ael_main(dictionary):
    if dictionary['startDate'] == 'Custom Date':
        dictionary['resetStartDate'] = dictionary['startDateCustom']
    else:
        dictionary['resetStartDate'] = DateField.read_date(dictionary['startDate'])
    if dictionary['endDate'] == 'Custom Date':
        dictionary['resetEndDate'] = dictionary['endDateCustom']
    else:
        dictionary['resetEndDate'] = DateField.read_date(dictionary['endDate'])
    dictionary['fixingDate'] = DateField.read_date(dictionary['fixingDate'])

    if ValidateInput(dictionary):
        fixingMode = dictionary["fixingMode"]
        fixingDate = dictionary["fixingDate"]
        terminate = dictionary["terminate"]
        pfSwap = dictionary["pfSwap"]
        previousPfSwap = dictionary["previousPfSwap"]
        floatRef = dictionary["floatRef"]
        resetStartDate = dictionary["resetStartDate"]
        resetEndDate = dictionary["resetEndDate"]
        regenerate = dictionary["regenerate"]
        calendar = dictionary["calendar"]
        daycountMethod = dictionary["daycountMethod"]
        rollingBaseDay = dictionary["rollingBaseDay"]
        isFixPeriod = dictionary["isFixPeriod"]
        paydayOffset = dictionary["paydayOffset"]
        paydayOffsetMethod = dictionary["paydayOffsetMethod"]
        spreadLong = dictionary["spreadLong"]
        spreadShort = dictionary["spreadShort"]
        payOrReceive = dictionary["payOrReceive"]

        (resetStartDate, resetEndDate) = ConvertResetDates(resetStartDate, \
                                                            resetEndDate, \
                                                            fixingDate, \
                                                            fixingMode)        
        if fixingMode:
            regenerate = False
        
        if spreadLong:
            spreadLong /= 100.0
        if spreadShort:
            spreadShort /= 100.0
            
        returnLegIsPayLeg = ("Pay" == payOrReceive) and True or False
        portfolio = pfSwap.FundPortfolio()
        
        if not rollingBaseDay:
            rollingBaseDay = pfSwap.StartDate()
        
        pfsParameters = Util.PortfolioSwapParameters({"portfolioSwap" : pfSwap, \
                                                "previousPfSwap" : previousPfSwap, \
                                                "floatRef" : floatRef, \
                                                "calendar" : calendar, \
                                                "daycountMethod" : daycountMethod, \
                                                "rollingBaseDay" : rollingBaseDay, \
                                                "isFixPeriod" : isFixPeriod, \
                                                "paydayOffset" : paydayOffset, \
                                                "paydayOffsetMethod" : paydayOffsetMethod, \
                                                "spreadLong" : spreadLong, \
                                                "spreadShort" : spreadShort, \
                                                "returnLegIsPayLeg" : returnLegIsPayLeg, \
                                                "paramDict" : dictionary})

        FSEQPortfolioSwap.AssertPaymentTypes(pfsParameters)
    
        if "Open End" == pfSwap.OpenEnd() and \
                not FSEQPortfolioSwap.CheckEndReturnResets(pfsParameters, resetStartDate):
            acm.Log("The Portfolio Swap (Open ended) has not been extended until the selected from date and cannot be extended from this date. Please select an earlier from date or, if neccessary, regenerate the Portfolio Swap from start.")
            return

        if calendar.IsNonBankingDay(None, None, resetStartDate):
            resetStartDate = calendar.ModifyDate(None, None, resetStartDate)
    
        if acm.Time.DateDifference(resetEndDate, resetStartDate) < 0:
            return

        if terminate:
            FSEQPortfolioSwap.TerminatePortfolioSwap(pfsParameters)
        else:
            if regenerate:
                FSEQPortfolioSwap.GeneratePortfolioSwap(pfsParameters, resetEndDate)
            else:
                FSEQPortfolioSwap.RestorePortfolioSwapEndDate(pfsParameters, resetEndDate)
                FSEQPortfolioSwap.AddNewLegs(pfsParameters, resetStartDate, resetEndDate)
                FSEQPortfolioSwap.AddNewCashFlows(pfsParameters, resetStartDate, resetEndDate)

                FSEQPortfolioSwap.ClearResetsFromDateUntilEnd(pfsParameters, resetStartDate)
                FSEQPortfolioSwap.ClearCashFlowsFromDateUntilEnd(pfsParameters, resetStartDate)
                FSEQPortfolioSwap.ClearPaymentsFromDateUntilEnd(pfsParameters, resetStartDate)
                
                FSEQPortfolioSwap.GenerateEndReturnResets(pfsParameters, resetStartDate)
            acm.PollDbEvents()

            FSEQPortfolioSwap.PerformDailyUpdatesInPeriod(pfsParameters, resetStartDate, resetEndDate)
            
           
            # Handle the transfer of cash and cash flows when a switch between swaps is made
            if not acm.Time.DateDifference(resetStartDate, pfSwap.StartDate()) and \
                    previousPfSwap and "Terminated" == previousPfSwap.OpenEnd():
                FSEQPortfolioSwap.TransferPreviousPortfolioSwapData(pfsParameters, resetStartDate)
        for leg in pfSwap.Legs():
            if leg.LegType() == "Total Return" and leg.NominalScaling() == "Price":
                leg.NominalScaling("Dividend")
                leg.Commit()
        acm.Log("Completed successfully.")

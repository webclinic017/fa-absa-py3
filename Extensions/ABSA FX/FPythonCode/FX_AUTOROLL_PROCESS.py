'''
PROCESS FLOW:

    With the query folder in hand the following needs to happen
    1. get the latest O/N postions per currency
    2. run through the currencies in the list config and book swaps from O/N to
        T/N except for USD and ZAR currency.
    3. get again the latest O/N positions per currency.
    4. book a O/N to T/N USD/ZAR trade.
    5. get the latest T/N positions per currency.
    6. run through all of the currencies in the config and book a T/N to spot
        except for the USD and ZAR currency.
    7. get the latest T/N positions per currency.
    8. book a T/N to spot USD/ZAR trade.
    9. Done
'''
import acm, gc
from FBDPCurrentContext import Logme
from FX_AUTOROLL_POSITION_CALC import POSITION_CALC_PER_TIME_BUCKET
from FX_AUTOROLL_PARAMETERS import AUTOROLL_PARAMETERS
from FX_AUTOROLL_UTILS import AUTOROLL_UTILS
from FX_AUTOROLL_BOOKING import AutoRollBooking

class AUTOROLL_PROCESS():
    def __init__(self, queryFolder, runOption, rollZARAgainstUSD):
        gc.enable()
        self.__queryFolder = queryFolder
        self.__runOption = runOption
        self.__rollZARAgainstUSD = rollZARAgainstUSD
        self.__parameters = None
        self.__positionDict = None
        self.__defaultPositionDict = None
        self.__timeBucketNames = None
        self.__targetPortfolio = None
        self.__targetAcquirer = None
        self.__getParameters()
        self.__setTargetPortfolio()
        self.__setTargetAcquirer()
        self.__getDefaultPositionPerCurrency()
        self.__configPass = self.__testConfiguration()
        if self.__configPass == True:
            if self.__runOption in ['Overnight', 'Both']:
                self.__processNonUSDZAR_ONtoTN()
                self.__processUSDZAR_ONtoTN()
            if self.__runOption in ['Tom Next', 'Both']:
                self.__processNonUSDZAR_TNtoSPOT()
                self.__processUSDZAR_TNtoSPOT()

    def __resetPositionDict(self):
        self.__positionDict = None
    
    def __resetDefaultPositionDict(self):
        self.__defaultPositionDict = None
        
    def __getParameters(self):
        self.__parameters = AUTOROLL_PARAMETERS(self.__queryFolder.Name())
    
    def __setTargetPortfolio(self):
        try:
            self.__targetPortfolio = acm.FPhysicalPortfolio[self.__parameters.targetPortfolioDictionary[self.__queryFolder.Name()]]
        except Exception, e:
            Logme()('WARNING: Could not find Query Folder %s from the Target Portfolio config in FParameters. No autoroll will be done for this query folder.' %self.__queryFolder.Name(), 'WARNING')
    
    def __setTargetAcquirer(self):
        if self.__targetPortfolio:
            self.__targetAcquirer = self.__targetPortfolio.PortfolioOwner()
    
    def __getPositionPerCurrency(self, currency):
        Logme()('DEBUG: Calculating position per currency for currency %s' %currency, 'DEBUG')
        self.__resetPositionDict()
        positionCalcPerTimeBucket = POSITION_CALC_PER_TIME_BUCKET(self.__queryFolder, currency)
        self.__positionDict = positionCalcPerTimeBucket.positionPerCurrencyPerTimeBucket

    def __getDefaultPositionPerCurrency(self):
        Logme()('DEBUG: Calculating the default position per currency for sheet FX_AUTOROLL', 'DEBUG')
        self.__resetDefaultPositionDict()
        positionCalcPerTimeBucket = POSITION_CALC_PER_TIME_BUCKET(self.__queryFolder, 'FX_AUTOROLL')
        self.__defaultPositionDict = positionCalcPerTimeBucket.positionPerCurrencyPerTimeBucket
        self.__timeBucketNames = positionCalcPerTimeBucket.timeBucketNames

    def __isValidOvernightDate(self, curr, date):
        validDate = True
        if self.__parameters.currencyDictionary[curr][0] == 'FALSE':
            validDate = False
        else:
            acmCurr = acm.FCurrency[curr]
            calendar = acmCurr.Calendar()
            isNonBankingDay = calendar.IsNonBankingDay(calendar, calendar, date)
            if isNonBankingDay == True:
                validDate = False
        
        #Check is the currency USD has a public holiday
        acmUSDCurr = acm.FCurrency['USD']
        calendarUSD = acmUSDCurr.Calendar()
        isNonBankingDayUSD = calendarUSD.IsNonBankingDay(calendarUSD, calendarUSD, date)
        if isNonBankingDayUSD == True:
            validDate = False
                
        return validDate

    def __isValidTomNextDate(self, curr, date):
        validDate = True
        if curr == 'USD':
            currencyPair = AUTOROLL_UTILS.getCurrencyPair(curr, 'ZAR')
        else:
            currencyPair = AUTOROLL_UTILS.getCurrencyPair(curr, 'USD')
        spotDate = currencyPair.SpotDate(acm.Time.DateNow())
        if date >= spotDate:
            validDate = False
        
        cal1 = currencyPair.Currency1().Calendar()
        cal2 = currencyPair.Currency2().Calendar()
        isNonBankingDayCurr1 = cal1.IsNonBankingDay(cal1, cal1, date)
        isNonBankingDayCurr2 = cal1.IsNonBankingDay(cal2, cal2, date)
        
        if isNonBankingDayCurr1 == True or isNonBankingDayCurr2 == True:
            validDate = False
            
        return validDate
        
    
    def __bookAutoroll(self, curr1, curr2, positionIndex):
        currencyPair = AUTOROLL_UTILS.getCurrencyPair(curr1, curr2)
        overnight, tomNext, spot = AUTOROLL_UTILS.getOvernightAndTomNextAndSpotDates(currencyPair)
        
        isValidOvernightDate = self.__isValidOvernightDate(curr1, overnight)
        if positionIndex == 0 and isValidOvernightDate == False:
            Logme()('DEBUG: Overnight date %s for currency %s is not valid. No trade will be booked' %(overnight, curr1), 'DEBUG')
            return
        
        isValidTomNextDate = self.__isValidTomNextDate(curr1, tomNext)
        if positionIndex == 1 and isValidTomNextDate == False:
            Logme()('DEBUG: TomNext date %s for currency %s is not valid. No trade will be booked' %(tomNext, curr1), 'DEBUG')
            return
        
        overnightListPosition = [i for i, x in enumerate(self.__timeBucketNames) if x == overnight]
        overnightAmount = self.__defaultPositionDict[curr1][overnightListPosition[0]]
        Logme()('DEBUG: Overnight Amount %s' %str(overnightAmount), 'DEBUG')
        
        tomNextAmount = 0.00
        for dateKey in self.__timeBucketNames:
            if dateKey > overnight and dateKey <= tomNext:
                dateKeyListPosition = [i for i, x in enumerate(self.__timeBucketNames) if x == dateKey]
                tomNextAmount += self.__defaultPositionDict[curr1][dateKeyListPosition[0]]
        Logme()('DEBUG: Tom Next Amount %s' %str(tomNextAmount), 'DEBUG')
        
        if positionIndex == 0:
            amount = overnightAmount
        else:
            amount = tomNextAmount
            if isValidOvernightDate == False:
                amount += overnightAmount
        Logme()('DEBUG: Roll Amount %s' %str(amount), 'DEBUG')
        
        if abs(amount) > 0:
            #positionIndex: 0 = O/N, 1 = T/N
            destinationPortfolio = acm.FPhysicalPortfolio[self.__parameters.currencyDictionary[curr1][2]]
            if destinationPortfolio != self.__targetPortfolio:
                destinationCounterparty = destinationPortfolio.PortfolioOwner()
                if positionIndex == 0:
                    Logme()('INFO: Booking currency %s ON to TN: %s' %(curr1, amount), 'INFO')
                else:
                    Logme()('INFO: Booking currency %s TN to SPOT: %s' %(curr1, amount), 'INFO')
                Logme()('INFO: Target Portfolio %s' %self.__targetPortfolio.Name(), 'INFO')
                Logme()('INFO: Target Acquirer %s' %self.__targetAcquirer.Name(), 'INFO')
                Logme()('INFO: Target CP Portfolio %s' %destinationPortfolio.Name(), 'INFO')
                Logme()('INFO: Targer Counterparty %s' %destinationCounterparty.Name(), 'INFO')
                Logme()('INFO: Currency Pair %s' %currencyPair.Name(), 'INFO')
                
                if positionIndex == 0:
                    bookingInstance = AutoRollBooking(self.__targetAcquirer.Name(), destinationCounterparty.Name(), self.__targetPortfolio.Name(), destinationPortfolio.Name(), self.__parameters.status, amount, curr1, currencyPair, overnight, tomNext)
                    bookingInstance.create_swap_roll_trade()
                else:
                    bookingInstance = AutoRollBooking(self.__targetAcquirer.Name(), destinationCounterparty.Name(), self.__targetPortfolio.Name(), destinationPortfolio.Name(), self.__parameters.status, amount, curr1, currencyPair, tomNext, spot)
                    bookingInstance.create_swap_roll_trade()
    
    def __testConfiguration(self):
        Logme()('DEBUG: Testing the configuration', 'DEBUG')
        Logme()('DEBUG: Test if the Query Folder selected exist in the config', 'DEBUG')
        try:
            self.__parameters.targetPortfolioDictionary[self.__queryFolder.Name()]
        except Exception, e:
            Logme()('WARNING: Could not find Query Folder %s from the Target Portfolio config in FParameters. No autoroll will be done for this query folder.' %self.__queryFolder.Name(), 'WARNING')
            return False
        
        return True
    
    def __processNonUSDZAR_ONtoTN(self):
        Logme()('INFO: Processing Autoroll from Overnight to Tom Next for non USD and ZAR Split currencies...', 'INFO')
        currList = self.__defaultPositionDict.keys()
        currList.sort()
        for currency in currList:
            if currency not in ('USD', 'ZAR'):
                if currency in self.__defaultPositionDict.keys() and currency in self.__parameters.currencyDictionary.keys():
                    if self.__parameters.currencyDictionary[currency][0] == 'TRUE':
                        self.__bookAutoroll(currency, 'USD', 0)
        acm.Memory().GcWorldStoppedCollect()
        gc.collect()
    
    def __processUSDZAR_ONtoTN(self):
        Logme()('INFO: Processing Autoroll from Overnight to Tom Next for USD/ZAR currency...', 'INFO')
        self.__getDefaultPositionPerCurrency()
        currList = self.__defaultPositionDict.keys()
        currList.sort()
        for currency in currList:
            if currency in ('USD'):
                if self.__rollZARAgainstUSD == True:
                    continue
                    
                if currency in self.__defaultPositionDict.keys() and currency in self.__parameters.currencyDictionary.keys():
                    if self.__parameters.currencyDictionary[currency][0] == 'TRUE':
                        self.__bookAutoroll(currency, 'ZAR', 0)
            if currency in ('ZAR'):
                if self.__rollZARAgainstUSD == True:
                    if currency in self.__defaultPositionDict.keys() and currency in self.__parameters.currencyDictionary.keys():
                        if self.__parameters.currencyDictionary[currency][0] == 'TRUE':
                            self.__bookAutoroll(currency, 'USD', 0)
        acm.Memory().GcWorldStoppedCollect()
        gc.collect()
    
    def __processNonUSDZAR_TNtoSPOT(self):
        Logme()('INFO: Processing Autoroll from Tom Next to SPOT for non USD and ZAR Split currencies...', 'INFO')
        self.__getDefaultPositionPerCurrency()
        currList = self.__defaultPositionDict.keys()
        currList.sort()
        for currency in currList:
            if currency not in ('USD', 'ZAR'):
                if currency in self.__defaultPositionDict.keys() and currency in self.__parameters.currencyDictionary.keys():
                    if self.__parameters.currencyDictionary[currency][1] == 'TRUE':
                        self.__bookAutoroll(currency, 'USD', 1)
        acm.Memory().GcWorldStoppedCollect()
        gc.collect()

    def __processUSDZAR_TNtoSPOT(self):
        Logme()('INFO: Processing Autoroll from Tom Next to SPOT for USD/ZAR currency...', 'INFO')
        self.__getDefaultPositionPerCurrency()
        currList = self.__defaultPositionDict.keys()
        currList.sort()
        for currency in currList:
            if currency in ('USD'):
                if self.__rollZARAgainstUSD == True:
                    continue

                if currency in self.__defaultPositionDict.keys() and currency in self.__parameters.currencyDictionary.keys():
                    if self.__parameters.currencyDictionary[currency][1] == 'TRUE':
                        self.__bookAutoroll(currency, 'ZAR', 1)

            if currency in ('ZAR'):
                if self.__rollZARAgainstUSD == True:
                    if currency in self.__defaultPositionDict.keys() and currency in self.__parameters.currencyDictionary.keys():
                        if self.__parameters.currencyDictionary[currency][1] == 'TRUE':
                            self.__bookAutoroll(currency, 'USD', 1)

        acm.Memory().GcWorldStoppedCollect()
        gc.collect()

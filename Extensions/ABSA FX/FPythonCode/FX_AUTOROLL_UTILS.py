import acm
from FBDPCurrentContext import Logme

class AUTOROLL_UTILS(object):
    
    @staticmethod
    def getCurrencyPair(curr1, curr2):
        Logme()('DEBUG: Entering getCurrencyPair', 'DEBUG')
        currency1 = acm.FCurrency[curr1]
        currency2 = acm.FCurrency[curr2]
        
        currencyPair = currency1.CurrencyPair(currency2)
        Logme()('DEBUG: Currency Pair: %s' %currencyPair.Name(), 'DEBUG')
        return currencyPair

    @staticmethod
    def getOvernightAndTomNextAndSpotDates(currencyPair):
        Logme()('DEBUG: Entering getOvernightAndTomNextAndSpotDates', 'DEBUG')
        calendar = currencyPair.SpotCalendar()
        today = acm.Time().DateToday()
        overnight = today
        spotDate = currencyPair.SpotDate(acm.Time.DateNow())
        curr1 = currencyPair.Currency1()
        curr2 = currencyPair.Currency2()
        curr1TomNext = curr1.Calendar().AdjustBankingDays(today, 1)
        curr2TomNext = curr2.Calendar().AdjustBankingDays(today, 1)
        if curr1TomNext >= curr2TomNext:
            tomNext = curr1TomNext
        else:
            tomNext = curr2TomNext
        while curr1.Calendar().IsNonBankingDay(curr1.Calendar(), curr1.Calendar(), tomNext) == True or curr2.Calendar().IsNonBankingDay(curr2.Calendar(), curr2.Calendar(), tomNext) == True:
            tomNext1 = curr1.Calendar().AdjustBankingDays(tomNext, 1)
            tomNext2 = curr2.Calendar().AdjustBankingDays(tomNext, 1)
            if tomNext1 <= tomNext2:
                tomNext = tomNext1
            else:
                tomNext = tomNext2
                
        Logme()('DEBUG: Overnight: %s\tTom Next: %s\tSpot: %s' %(overnight, tomNext, spotDate), 'DEBUG')
        return overnight, tomNext, spotDate

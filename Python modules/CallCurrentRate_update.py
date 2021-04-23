import ael, CurrencyETNPricing

ael_variables = [['currencies', 'Input Currencies', 'FInstrument', None, None, 1, 1, 'Currencies', None, 1]]

def ael_main(ael_dict):
    currencyList = [ael.Instrument[currency.Name()] for currency in ael_dict['currencies']]
    CurrencyETNPricing.storeDailyRates(currencyList)
    CurrencyETNPricing.updateResetCurrencyETNs()
    
    print('Completed Successfully')
    

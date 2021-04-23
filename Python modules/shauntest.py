import ael, string, FSQL_functions
print 'IsBankingDay:', FSQL_functions.isBankingDay(ael.date_today().add_days(-1), 'ZAR')
print 'PreviousBankingDay:', FSQL_functions.previousBankingDay(ael.date_today(), 'ZAR')
ael.disconnect()

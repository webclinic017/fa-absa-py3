import ael

#-----------------------------------------------------------------------------------------------------------------
#  Developer           : [Anwar], [Willie]
#  Purpose             : [ISDA Matrix definitions used for confirmations to Trident
#                        Code merge was missing ISDA_EXERCISE_BUSINESS_DAYS],[Added section for Swaptions]
#  Department and Desk : [Operations]
#  Requester           : [Miguel]
#  CR Number           : [617525, ECR622988], [655450 21/05/2011]
#-----------------------------------------------------------------------------------------------------------------


ISDA_EXERCISE_CURR = 0
ISDA_BUSINESS_CENTRE = 1
ISDA_EARLIEST = 2
ISDA_LATEST = 3
ISDA_EXERCISE = 4
ISDA_CSPD_OFFSET = 5
ISDA_EXERCISE_BUSINESS_DAYS = 6

ISDA_SETTLE_VALUATION_BUSINESS_DAYS = 7
ISDA_SETTLE_EXERCISE_BUSINESS_DAYS = 8
ISDA_CASH_SETTLED_FALLBACK = 9
ISDA_CASH_SETTLE_METHOD = 10
ISDA_CASH_SETTLE_RATE = 11
ISDA_CASH_SETTLE_PD = 12

#dictionary key = cross currencies traded
#list = cash settlement curr, calendar, earliest, latest, expiry, cashsettlement valuation
ISDA_CCS_MATRIX = {
    'CAD/USD':['USD', 'CATO', '09:00:00', '16:00:00', '16:00:00', -2, ['CATO', 'GBLO', 'USNY']],
    'MXN/USD':['USD', 'USNY', '09:00:00', '12:30:00', '12:30:00', -1, ['MXMC', 'GBLO', 'USNY']],
    'CHF/EUR':['EUR', 'GBLO', '09:00:00', '11:00:00', '11:00:00', -2, ['CHZU', 'GBLO', 'EUTA']],
    'CHF/PLN':['CHF', 'PLWA', '09:00:00', '11:00:00', '11:00:00', -2, ['PLWA', 'GBLO', 'CHZU']],
    'CHF/USD':['USD', 'GBLO', '09:00:00', '11:00:00', '11:00:00', -2, ['CHZU', 'GBLO', 'USNY']],
    'CZK/EUR':['EUR', 'CZPR', '09:00:00', '11:00:00', '11:00:00', -2, ['CZPR', 'GBLO', 'EUTA']], 
    'CZK/USD':['USD', 'CZPR', '09:00:00', '11:00:00', '11:00:00', -2, ['CZPR', 'GBLO', 'USNY']],
    'DKK/EUR':['EUR', 'DKCO', '09:00:00', '11:00:00', '11:00:00', -2, ['DKCO', 'GBLO', 'EUTA']],
    'DKK/USD':['USD', 'DKCO', '09:00:00', '11:00:00', '11:00:00', -2, ['DKCO', 'GBLO', 'USNY']],
    'EUR/USD':['USD', 'BEBR', '09:00:00', '11:00:00', '11:00:00', -2, ['GBLO', 'EUTA', 'USNY']],
    'EUR/USD/LIBOR':['USD', 'GBLO', '09:00:00', '11:00:00', '11:00:00', -2, ['GBLO', 'EUTA', 'USNY']],
    'GBP/EUR':['EUR', 'GBLO', '09:00:00', '11:00:00', '11:00:00', 0, ['GBLO', 'EUTA']],
    'GBP/USD':['USD', 'GBLO', '09:00:00', '11:00:00', '11:00:00', 0, ['GBLO', 'USNY']],
    'HUF/EUR':['EUR', 'HUBU', '09:00:00', '11:00:00', '11:00:00', -2, ['HUBU', 'GBLO', 'EUTA']],
    'HUF/USD':['USD', 'HUBU', '09:00:00', '11:00:00', '11:00:00', -2, ['HUBU', 'GBLO', 'USNY']],
    'ILS/USD':['USD', 'ILTA', '09:00:00', '11:00:00', '11:00:00', -2, ['ILTA', 'GBLO', 'USNY']],
    'NOK/EUR':['EUR', 'NOOS', '09:00:00', '12:00:00', '12:00:00', -2, ['NOOS', 'GBLO', 'EUTA']],
    'NOK/USD':['USD', 'NOOS', '09:00:00', '12:00:00', '12:00:00', -2, ['NOOS', 'GBLO', 'USNY']],
    'PLN/EUR':['EUR', 'PLWA', '09:00:00', '11:00:00', '11:00:00', -2, ['PLWA', 'GBLO', 'EUTA']],
    'PLN/USD':['USD', 'PLWA', '09:00:00', '11:00:00', '11:00:00', -2, ['PLWA', 'GBLO', 'USNY']],
    'SEK/EUR':['EUR', 'SEST', '09:00:00', '11:00:00', '11:00:00', -2, ['SEST', 'GBLO', 'EUTA']],
    'SEK/USD':['USD', 'SEST', '09:00:00', '11:00:00', '11:00:00', -2, ['SEST', 'GBLO', 'USNY']],
    'TRY/EUR':['EUR', 'TRIS', '09:00:00', '11:00:00', '11:00:00', -2, ['TRIS', 'GBLO', 'EUTA']],
    'TRY/USD':['USD', 'TRIS', '09:00:00', '11:00:00', '11:00:00', -2, ['TRIS', 'GBLO', 'USNY']],
    'ZAR/EUR':['EUR', 'ZAJO', '09:00:00', '11:00:00', '11:00:00', -2, ['ZAJO', 'GBLO', 'EUTA']],
    'ZAR/USD':['USD', 'ZAJO', '09:00:00', '11:00:00', '11:00:00', -2, ['ZAJO', 'GBLO', 'USNY']],
    'AUD/USD':['USD', 'AUSY', '09:00:00', '11:00:00', '11:00:00', -2, ['AUSY', 'GBLO', 'USNY']],
    'HKD/EUR':['EUR', 'HKHK', '09:00:00', '11:00:00', '11:00:00', -2, ['HKHK', 'EUTA']],
    'HKD/GBP':['GBP', 'HKHK', '09:00:00', '11:00:00', '11:00:00', -2, ['HKHK', 'GBLO']],
    'HKD/USD':['USD', 'HKHK', '09:00:00', '11:00:00', '11:00:00', -2, ['HKHK', 'USNY', 'GBLO']],
    'JPY/EUR':['EUR', 'JPTO', '09:00:00', '15:00:00', '15:00:00', -2, ['JPTO', 'GBLO', 'EUTA']],
    'JPY/USD':['USD', 'JPTO', '09:00:00', '15:00:00', '15:00:00', -2, ['JPTO', 'GBLO', 'USNY']],
    'NZD/USD':['USD', 'NZWE', '09:00:00', '11:00:00', '11:00:00', -2, ['NZAU', 'NZWE', 'USNY', 'GBLO']],
    'SGD/GBP':['GBP', 'SGSI', '09:00:00', '11:00:00', '11:00:00', -2, ['SGSI', 'GBLO']],
    'SGD/USD':['USD', 'SGSI', '09:00:00', '11:00:00', '11:00:00', -2, ['SGSI', 'GBLO', 'USNY']]
}

ISDA_VANILLA_MATRIX = {
    'CAD':['CAD', 'CATO', '09:00:00', '16:00:00', '16:00:00', -2, ['CATO']],
    'CAD/LIBOR':['CAD', 'CATO', '09:00:00', '16:00:00', '16:00:00', -2, ['CATO', 'GBLO']],
    'MXN':['MXN', 'USNY', '09:00:00', '12:30:00', '12:30:00', -1, ['MXMC']],
    'USD':['USD', 'USNY', '09:00:00', '11:00:00', '11:00:00', -2, ['USNY']],
    'USD/LIBOR':['USD', 'USNY', '09:00:00', '11:00:00', '11:00:00', -2, ['USNY', 'GBLO']],
    'CHF':['CHF', 'GBLO', '09:00:00', '11:00:00', '11:00:00', -2, ['CHZU', 'GBLO']],
    'CZK':['CZK', 'CZPR', '09:00:00', '11:00:00', '11:00:00', -2, ['CZPR', 'GBLO']],
    'DKK':['DKK', 'DKCO', '09:00:00', '11:00:00', '11:00:00', -2, ['DKCO']],
    'EUR':['EUR', 'BEBR', '09:00:00', '11:00:00', '11:00:00', -2, ['GBLO', 'EUTA']],
    'EUR/LIBOR':['EUR', 'GBLO', '09:00:00', '11:00:00', '11:00:00', -2, ['GBLO', 'EUTA']],
    'GBP':['GBP', 'GBLO', '09:00:00', '11:00:00', '11:00:00', 0, ['GBLO']],
    'HUF':['HUF', 'HUBU', '09:00:00', '11:00:00', '11:00:00', -2, ['HUBU', 'GBLO']],
    'ILS':['ILS', 'GBLO', '09:00:00', '11:00:00', '11:00:00', -2, ['ILTA', 'GBLO']],
    'NOK':['NOK', 'NOOS', '09:00:00', '12:00:00', '12:00:00', -2, ['NOOS']],
    'PLN':['PLN', 'GBLO', '09:00:00', '11:00:00', '11:00:00', -2, ['PLWA', 'GBLO']],
    'SEK':['SEK', 'SEST', '09:00:00', '11:00:00', '11:00:00', -2, ['SEST', 'GBLO']],
    'TRY':['TRY', 'TRIS', '09:00:00', '11:00:00', '11:00:00', -2, ['TRIS', 'GBLO']],
    'ZAR':['ZAR', 'ZAJO', '09:00:00', '11:00:00', '11:00:00', -2, ['ZAJO', 'GBLO']],
    'AUD':['AUD', 'AUSY', '09:00:00', '11:00:00', '11:00:00', -2, ['AUSY']],
    'CNY':['CNY', 'CNBE', '09:00:00', '11:00:00', '11:00:00', -2, ['CNBE']],
    'HKD':['HKD', 'HKHK', '09:00:00', '11:00:00', '11:00:00', 0, ['HKHK']],
    'IDR':['IDR', 'IDJA', '09:00:00', '11:00:00', '11:00:00', -2, ['IDJA']],
    'INR':['INR', 'INMU', '09:00:00', '11:00:00', '11:00:00', -2, ['INMU']],
    'JPY':['JPY', 'JPTO', '09:00:00', '15:00:00', '15:00:00', -2, ['JPTO']],
    'JPY/LIBOR':['JPY', 'JPTO', '09:00:00', '15:00:00', '15:00:00', -2, ['JPTO', 'GBLO']],
    'KRW':['KRW', 'KRSE', '09:00:00', '11:00:00', '11:00:00', -2, ['KRSE']],
    'MYR':['MYR', 'MYKL', '09:00:00', '11:00:00', '11:00:00', -2, ['MYKL', 'SGSI']],
    'NZD':['NZD', 'NZWE', '09:00:00', '11:00:00', '11:00:00', -2, ['NZAU', 'NZWE']],
    'PHP':['PHP', 'PHMA', '09:00:00', '11:00:00', '11:00:00', -2, ['PHMA']],
    'SGD':['SGD', 'SGSI', '09:00:00', '11:00:00', '11:00:00', -2, ['SGSI']],
    'THB':['THB', 'THBA', '09:00:00', '11:00:00', '11:00:00', -2, ['THBA']],
    'TWD':['TWD', 'TWTA', '09:00:00', '11:00:00', '11:00:00', -2, ['TWTA']]
}

ISDA_SWAPTION_MATRIX = {
    'CAD':['CAD', 'CATO', '09:00:00', '16:00:00', '16:00:00', -2, ['CATO'], ['CATO'], ['CATO'], 'Fallback Exercise', 'Cash', 'Mid', 1],
    'CAD/LIBOR':['CAD', 'CATO', '09:00:00', '16:00:00', '16:00:00', -2, ['CATO', 'GBLO'], ['CATO', 'GBLO'], ['CATO', 'GBLO'], 'Fallback Exercise', 'Cash', 'Mid', 1],
    'MXN':['MXN', 'USNY', '09:00:00', '12:30:00', '12:30:00', -1, ['MXMC'], ['MXMC'], ['MXMC'], 'Fallback Exercise', 'Cash', 'Mid', 1],
    'USD':['USD', 'USNY', '09:00:00', '11:00:00', '11:00:00', -2, ['USNY'], ['USNY'], ['USNY'], 'Fallback Exercise', 'Cash', 'Mid', 2],
    'USD/LIBOR':['USD', 'USNY', '09:00:00', '11:00:00', '11:00:00', -2, ['USNY', 'GBLO'], ['USNY', 'GBLO'], ['USNY', 'GBLO'], 'Fallback Exercise', 'Cash', 'Mid', 2],
    'CHF':['CHF', 'GBLO', '09:00:00', '11:00:00', '11:00:00', -2, ['CHZU', 'GBLO'], ['CHZU'], ['CHZU', 'GBLO'], 'Automatic Exercise', 'ParYieldCurveUnadjusted', 'ISDA Source', 2],
    'CZK':['CZK', 'CZPR', '09:00:00', '11:00:00', '11:00:00', -2, ['CZPR', 'GBLO'], ['CZPR', 'GBLO'], ['CZPR', 'GBLO'], 'Fallback Exercise', 'Cash', 'Mid', 2],
    'DKK':['DKK', 'DKCO', '09:00:00', '11:00:00', '11:00:00', -2, ['DKCO'], ['DKCO'], ['DKCO'], 'Automatic Exercise', 'ParYieldCurveUnadjusted', 'Reference Banks', 2],
    'EUR':['EUR', 'BEBR', '09:00:00', '11:00:00', '11:00:00', -2, ['GBLO', 'EUTA'], ['EUTA'], ['GBLO', 'EUTA'], 'Automatic Exercise', 'ParYieldCurveUnadjusted', 'ISDA Source', 2],
    'EUR/LIBOR':['EUR', 'GBLO', '09:00:00', '11:00:00', '11:00:00', -2, ['GBLO', 'EUTA'], ['EUTA'], ['GBLO', 'EUTA'], 'Automatic Exercise', 'ParYieldCurveUnadjusted', 'ISDA Source', 2],
    'GBP':['GBP', 'GBLO', '09:00:00', '11:00:00', '11:00:00', -2, ['GBLO'], ['GBLO'], ['GBLO'], 'Automatic Exercise', 'ParYieldCurveUnadjusted', 'ISDA Source', 0],
    'HUF':['HUF', 'HUBU', '09:00:00', '11:00:00', '11:00:00', -2, ['HUBU', 'GBLO'], ['HUBU', 'GBLO'], ['HUBU', 'GBLO'], 'Fallback Exercise', 'Cash', 'Mid', 2],
    'ILS':['ILS', 'GBLO', '09:00:00', '11:00:00', '11:00:00', -2, ['ILTA', 'GBLO'], ['ILTA', 'GBLO'], ['ILTA', 'GBLO'], 'Fallback Exercise', 'Cash', 'Mid', 2],
    'NOK':['NOK', 'NOOS', '09:00:00', '12:00:00', '12:00:00', -2, ['NOOS'], ['NOOS'], ['NOOS'], 'Automatic Exercise', 'ParYieldCurveUnadjusted', 'Reference Banks', 2],
    'PLN':['PLN', 'GBLO', '09:00:00', '11:00:00', '11:00:00', -2, ['PLWA', 'GBLO'], ['PLWA', 'GBLO'], ['PLWA', 'GBLO'], 'Fallback Exercise', 'Cash', 'Mid', 2],
    'SEK':['SEK', 'SEST', '09:00:00', '11:00:00', '11:00:00', -2, ['SEST'], ['SEST'], ['SEST'], 'Automatic Exercise', 'ParYieldCurveUnadjusted', 'Reference Banks', 2],
    'TRY':['TRY', 'TRIS', '09:00:00', '11:00:00', '11:00:00', -2, ['TRIS', 'GBLO'], ['TRIS', 'GBLO'], ['TRIS', 'GBLO'], 'Fallback Exercise', 'Cash', 'Mid', 2],
    'ZAR':['ZAR', 'ZAJO', '09:00:00', '11:00:00', '11:00:00', -2, ['ZAJO', 'GBLO'], ['ZAJO'], ['ZAJO', 'GBLO'], 'Fallback Exercise', 'ParYieldCurveUnadjusted', 'Reference Banks', 0],
    'AUD':['AUD', 'AUSY', '09:00:00', '11:00:00', '11:00:00', -2, ['AUSY'], ['AUSY'], ['AUSY'], 'Automatic Exercise', 'ParYieldCurveUnadjusted', 'IRSW 10AM', 2],
    'AUD/LIBOR':['AUD', 'AUSY', '09:00:00', '11:00:00', '11:00:00', -2, ['AUSY'], ['AUSY'], ['AUSY', 'GBLO'], 'Automatic Exercise', 'ParYieldCurveUnadjusted', 'IRSW 10AM', 2],
    'CNY':['CNY', 'CNBE', '09:00:00', '11:00:00', '11:00:00', -2, ['CNBE'], ['CNBE'], ['CNBE'], 'Fallback Exercise', 'Cash', 'Mid', 2],
    'HKD':['HKD', 'HKHK', '09:00:00', '11:00:00', '11:00:00', 0, ['HKHK'], ['HKHK'], ['HKHK'], 'Fallback Exercise', 'Cash', 'Mid', 0],
    'IDR':['IDR', 'IDJA', '09:00:00', '11:00:00', '11:00:00', -2, ['IDJA'], ['IDJA'], ['IDJA'], 'Fallback Exercise', 'Cash', 'Mid', 2],
    'INR':['INR', 'INMU', '09:00:00', '11:00:00', '11:00:00', -2, ['INMU'], ['INMU'], ['INMU'], 'Fallback Exercise', 'Cash', 'Mid', 2],
    'JPY':['JPY', 'JPTO', '09:00:00', '15:00:00', '15:00:00', -2, ['JPTO'], ['JPTO'], ['JPTO'], 'Fallback Exercise', 'ZeroCouponYield', '17143', 2],
    'JPY/LIBOR':['JPY', 'JPTO', '09:00:00', '15:00:00', '15:00:00', -2, ['JPTO', 'GBLO'], ['JPTO', 'GBLO'], ['JPTO', 'GBLO'], 'Fallback Exercise', 'ZeroCouponYield', '17143', 2],
    'KRW':['KRW', 'KRSE', '09:00:00', '11:00:00', '11:00:00', -2, ['KRSE'], ['KRSE'], ['KRSE'], 'Fallback Exercise', 'Cash', 'Mid', 2],
    'MYR':['MYR', 'MYKL', '09:00:00', '11:00:00', '11:00:00', -2, ['MYKL', 'SGSI'], ['MYKL', 'USNY'], ['MYKL', 'SGSI'], 'Fallback Exercise', 'Cash', 'Mid', 2],
    'NZD':['NZD', 'NZWE', '09:00:00', '11:00:00', '11:00:00', -2, ['NZAU', 'NZWE'], ['NZAU', 'NZWE'], ['NZAU', 'NZWE'], 'Automatic Exercise', 'ParYieldCurveUnadjusted', 'Reference Banks', 2],
    'PHP':['PHP', 'PHMA', '09:00:00', '11:00:00', '11:00:00', -2, ['PHMA'], ['PHMA'], ['PHMA'], 'Fallback Exercise', 'Cash', 'Mid', 2],
    'SGD':['SGD', 'SGSI', '09:00:00', '11:00:00', '11:00:00', -2, ['SGSI'], ['SGSI'], ['SGSI'], 'Fallback Exercise', 'Cash', 'Mid', 2],
    'THB':['THB', 'THBA', '09:00:00', '11:00:00', '11:00:00', -2, ['THBA'], ['THBA'], ['THBA'], 'Fallback Exercise', 'Cash', 'Mid', 2],
    'TWD':['TWD', 'TWTA', '09:00:00', '11:00:00', '11:00:00', -2, ['TWTA'], ['TWTA'], ['TWTA'], 'Fallback Exercise', 'Cash', 'Mid', 2]
}

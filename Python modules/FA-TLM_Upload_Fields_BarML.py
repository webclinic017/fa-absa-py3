import ael, acm, SAGEN_IT_Functions

def AdditionalInfoSpec(toClone, fieldName, rec_type, description):
    ais = ael.AdditionalInfoSpec[toClone].new()
    ais.field_name = fieldName
    ais.rec_type = rec_type
    ais.description = description
    try:
        ais.commit()
        return 'Additional info Spec: ' + fieldName + ' was created successfuly.'
    except:
        return 'Additional info Spec: ' + fieldName + ' encountered an error.'

def Load_Floating_Ref_Free_Text(info):
    for i in info:
        ins = acm.FInstrument[i[0]]
        try:
            ins.FreeText(i[1])
            ins.Commit()
            print 'Free Text on Instrument: ' + i[0] + ' was set successfuly.'
        except:
            print 'Free Text on Instrument: ' + i[0] + ' encountered an error.'
    return 'Floating Rates upload done'
    
def Load_Earliest_Time(info):
    for i in info:
        try:
            SAGEN_IT_Functions.set_AdditionalInfoValue_ACM(acm.FCurrency[i[0]], 'EarliestExTime', i[1])
            print 'Earliest time on Instrument: ' + i[0] + ' was set successfuly.'
        except:
            print 'Earliest time on Instrument: ' + i[0] + ' encountered an error.'
    return 'Earliest Time upload done'
    
def Load_Latest_Time(info):
    for i in info:
        try:
            SAGEN_IT_Functions.set_AdditionalInfoValue_ACM(acm.FCurrency[i[0]], 'LatestExTime', i[1])
            print 'Latest time on Instrument: ' + i[0] + ' was set successfuly.'
        except:
            print 'Latest time on Instrument: ' + i[0] + ' encountered an error.'
    return 'Latest Time upload done'


#print AdditionalInfoSpec(453,'EarliestExTime','Instrument','Trident EarliestExerciseTime') #String
#print AdditionalInfoSpec(453,'LatestExTime','Instrument','Trident LatestExerciseTime') #String


floating_rate = acm.FArray()
floating_rate.Add(('CAD-LIBOR-3M', 'CAD-LIBOR-BBA'))
floating_rate.Add(('CHF-LIBOR-12M', 'CHF-LIBOR-BBA'))
floating_rate.Add(('CHF-LIBOR-1M', 'CHF-LIBOR-BBA'))
floating_rate.Add(('CHF-LIBOR-3M', 'CHF-LIBOR-BBA'))
floating_rate.Add(('CHF-LIBOR-6M', 'CHF-LIBOR-BBA'))
floating_rate.Add(('CZK-PRIBOR-3M', 'CZK-PRIBOR-Reference Banks'))
floating_rate.Add(('CZK-PRIBOR-6M', 'CZK-PRIBOR-Reference Banks'))
floating_rate.Add(('EUR-EURIBOR-12M', 'EUR-EURIBOR-Reference Banks'))
floating_rate.Add(('EUR-EURIBOR-1M', 'EUR-EURIBOR-Reference Banks'))
floating_rate.Add(('EUR-EURIBOR-1W', 'EUR-EURIBOR-Reference Banks'))
floating_rate.Add(('EUR-EURIBOR-2M', 'EUR-EURIBOR-Reference Banks'))
floating_rate.Add(('EUR-EURIBOR-3M', 'EUR-EURIBOR-Reference Banks'))
floating_rate.Add(('EUR-EURIBOR-6M', 'EUR-EURIBOR-Reference Banks'))
floating_rate.Add(('EUR-EURIBOR-9M', 'EUR-EURIBOR-Reference Banks'))
floating_rate.Add(('GBP-LIBOR-12M', 'GBP-LIBOR-BBA'))
floating_rate.Add(('GBP-LIBOR-1M', 'GBP-LIBOR-BBA'))
floating_rate.Add(('GBP-LIBOR-1W', 'GBP-LIBOR-BBA'))
floating_rate.Add(('GBP-LIBOR-3M', 'GBP-LIBOR-BBA'))
floating_rate.Add(('GBP-LIBOR-6M', 'GBP-LIBOR-BBA'))
floating_rate.Add(('GBP-LIBOR-9M', 'GBP-LIBOR-BBA'))
floating_rate.Add(('HUF-BUBOR-3M', 'HUF-BUBOR-Reference Banks'))
floating_rate.Add(('HUF-BUBOR-6M', 'HUF-BUBOR-Reference Banks'))
floating_rate.Add(('ILS-TELBOR-3M', 'ILS-TELBOR-Reference Banks'))
floating_rate.Add(('ILS-TELBOR-6M', 'ILS-TELBOR-Reference Banks'))
floating_rate.Add(('JPY-LIBOR-9M', 'JPY-LIBOR-BBA'))
floating_rate.Add(('JPY-LIBOR-6M', 'JPY-LIBOR-BBA'))
floating_rate.Add(('JPY-LIBOR-3M', 'JPY-LIBOR-BBA'))
floating_rate.Add(('JPY-LIBOR-1W', 'JPY-LIBOR-BBA'))
floating_rate.Add(('JPY-LIBOR-1M', 'JPY-LIBOR-BBA'))
floating_rate.Add(('JPY-LIBOR-12M', 'JPY-LIBOR-BBA'))
floating_rate.Add(('PLN-WIBOR-3M', 'PLZ-WIBOR-Reference Banks'))
floating_rate.Add(('PLN-WIBOR-6M', 'PLZ-WIBOR-Reference Banks'))
floating_rate.Add(('USD-LIBOR-9M', 'USD-LIBOR-BBA'))
floating_rate.Add(('USD-LIBOR-6M', 'USD-LIBOR-BBA'))
floating_rate.Add(('USD-LIBOR-3M', 'USD-LIBOR-BBA'))
floating_rate.Add(('USD-LIBOR-1W', 'USD-LIBOR-BBA'))
floating_rate.Add(('USD-LIBOR-1M', 'USD-LIBOR-BBA'))
floating_rate.Add(('USD-LIBOR-12M', 'USD-LIBOR-BBA'))
floating_rate.Add(('ZAR-JIBAR-12M', 'ZAR-JIBAR-SAFEX'))
floating_rate.Add(('ZAR-JIBAR-1M', 'ZAR-JIBAR-SAFEX'))
floating_rate.Add(('ZAR-JIBAR-3M', 'ZAR-JIBAR-SAFEX'))
floating_rate.Add(('ZAR-JIBAR-3M-Spec', 'ZAR-JIBAR-SAFEX'))
floating_rate.Add(('ZAR-JIBAR-3M/FundingSpr', 'ZAR-JIBAR-SAFEX'))
floating_rate.Add(('ZAR-JIBAR-3dc', 'ZAR-JIBAR-SAFEX'))
floating_rate.Add(('ZAR-JIBAR-6M', 'ZAR-JIBAR-SAFEX'))
floating_rate.Add(('ZAR-JIBAR-9M', 'ZAR-JIBAR-SAFEX'))
floating_rate.Add(('ZAR-PRIME-AVERAGE', 'ZAR-PRIME-AVERAGE'))
floating_rate.Add(('SACPI', 'ZAR-CPI'))
floating_rate.Add(('ZAR-PRIME', 'ZAR-PRIME-AVERAGE'))
floating_rate.Add(('ZAR-PRIME-1M', 'ZAR-PRIME-AVERAGE'))
floating_rate.Add(('ZAR-PRIME-3M', 'ZAR-PRIME-AVERAGE'))
floating_rate.Add(('AUD-LIBOR-3M', 'AUD-LIBOR-BBA'))
floating_rate.Add(('MXN-MEXIBOR-1M', 'MXN-MEXIBOR'))
print Load_Floating_Ref_Free_Text(floating_rate)



#NB!!!! IDR, KRW, PHP AND TWD are not currencies loaded in FA, but are provisioned for in the ISDA matrix.  Included below for sake of completeness
#NB!!!! so should we load them into prod pre-go-live then it exists

earliest_time = acm.FArray()
earliest_time.Add(('EUR', '09:00:00'))
earliest_time.Add(('USD', '09:00:00'))
earliest_time.Add(('ZAR', '09:00:00'))
earliest_time.Add(('JPY', '09:00:00'))
earliest_time.Add(('GBP', '09:00:00'))
earliest_time.Add(('MXN', '09:00:00'))
earliest_time.Add(('CHF', '09:00:00'))
earliest_time.Add(('HUF', '09:00:00'))
earliest_time.Add(('ILS', '09:00:00'))
earliest_time.Add(('NOK', '09:00:00'))
earliest_time.Add(('PLN', '09:00:00'))
earliest_time.Add(('SEK', '09:00:00'))
earliest_time.Add(('TRY', '09:00:00'))
earliest_time.Add(('AUD', '09:00:00'))
earliest_time.Add(('CNY', '09:00:00'))
earliest_time.Add(('HKD', '09:00:00'))
earliest_time.Add(('IDR', '09:00:00'))
earliest_time.Add(('INR', '09:00:00'))
earliest_time.Add(('CAD', '09:00:00'))
earliest_time.Add(('CZK', '09:00:00'))
earliest_time.Add(('DKK', '09:00:00'))
earliest_time.Add(('KRW', '09:00:00'))
earliest_time.Add(('MYR', '09:00:00'))
earliest_time.Add(('NZD', '09:00:00'))
earliest_time.Add(('PHP', '09:00:00'))
earliest_time.Add(('SGD', '09:00:00'))
earliest_time.Add(('THB', '09:00:00'))
earliest_time.Add(('TWD', '09:00:00'))

print Load_Earliest_Time(earliest_time)

latest_time = acm.FArray()
latest_time.Add(('EUR', '11:00:00'))
latest_time.Add(('USD', '11:00:00'))
latest_time.Add(('ZAR', '11:00:00'))
latest_time.Add(('JPY', '15:00:00'))
latest_time.Add(('GBP', '11:00:00'))
latest_time.Add(('MXN', '12:30:00'))
latest_time.Add(('CHF', '11:00:00'))
latest_time.Add(('HUF', '11:00:00'))
latest_time.Add(('ILS', '11:00:00'))
latest_time.Add(('NOK', '12:00:00'))
latest_time.Add(('PLN', '11:00:00'))
latest_time.Add(('SEK', '11:00:00'))
latest_time.Add(('TRY', '11:00:00'))
latest_time.Add(('AUD', '11:00:00'))
latest_time.Add(('CNY', '11:00:00'))
latest_time.Add(('HKD', '11:00:00'))
latest_time.Add(('IDR', '11:00:00'))
latest_time.Add(('INR', '11:00:00'))
latest_time.Add(('CAD', '16:00:00'))
latest_time.Add(('CZK', '11:00:00'))
latest_time.Add(('DKK', '11:00:00'))
latest_time.Add(('KRW', '11:00:00'))
latest_time.Add(('MYR', '11:00:00'))
latest_time.Add(('NZD', '11:00:00'))
latest_time.Add(('PHP', '11:00:00'))
latest_time.Add(('SGD', '11:00:00'))
latest_time.Add(('THB', '11:00:00'))
latest_time.Add(('TWD', '11:00:00'))

print Load_Latest_Time(latest_time)

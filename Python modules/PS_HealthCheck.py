import acm
import FRunScriptGUI
import FBDPGui
import FBDPString
import at_time
from datetime import timedelta
from time import mktime

logme = FBDPString.logme

calendar = acm.FCalendar['ZAR Johannesburg']
TODAY = acm.Time().DateToday()
YESTERDAY = acm.Time().DateAddDelta(TODAY, 0, 0, -1)
TWODAYSAGO = acm.Time().DateAddDelta(TODAY, 0, 0, -2)
PREVBUSDAY = calendar.AdjustBankingDays(TODAY, -1)
TWOBUSDAYSAGO = calendar.AdjustBankingDays(TODAY, -2)

# Generate date lists to be used as drop downs in the GUI.
startDateList   = {'PrevBusDay':PREVBUSDAY,
                   'TwoBusinessDaysAgo':TWOBUSDAYSAGO,
                   'TwoDaysAgo':TWODAYSAGO,
                   'Yesterday':YESTERDAY,
                   'Custom Date':TODAY,
                   'Now':TODAY}
startDateKeys = startDateList.keys()
startDateKeys.sort()

def enableCustomStartDate(index, fieldValues):
    ael_variables[1][9] = (fieldValues[0] == 'Custom Date')
    return fieldValues

SCRIPT_NAME     = 'PS_HealthCheck'

# Variable Name, Display Name, Type, Candidate Values, Default,
# Mandatory, Multiple, Description, Input Hook, Enabled
ael_variables = FBDPGui.LogVariables(['date', 'Date', 'string', startDateKeys,
        'Now', 1, 0, 'Date for which the file should be selected.',
        enableCustomStartDate, 1],
    ['dateCustom', 'Date Custom', 'string', None, TODAY,
        0, 0, 'Custom date', None, 0],
    ['cutoffHour', 'Stale Price Cutoff Hour', 'int', None, 4,
        0, 0, 'Prices earlier than this hour will be considered stale', None, 1],
    ['priceQF', 'Stale Price Check Query', 'FStoredASQLQuery', None, 'Instrument_Check',
        0, 0, 'Custom date', None, 1])

def ael_main(dictionary):
    logme.setLogmeVar(SCRIPT_NAME,
                      dictionary['Logmode'],
                      dictionary['LogToConsole'],
                      dictionary['LogToFile'],
                      dictionary['Logfile'],
                      dictionary['SendReportByMail'],
                      dictionary['MailList'],
                      dictionary['ReportMessageType'])

    if dictionary['date'] == 'Custom Date':
        date = dictionary['dateCustom']
    else:
        date = startDateList[dictionary['date']]

    try:
        Instrument_Check(date, dictionary['priceQF'], dictionary['cutoffHour'])
    except Exception as e:
        logme('Unexpected problems: %s' %(e), 'ERROR')
        logme(None, 'FINISH')
        raise       
    
    print('completed successfully')
    logme(None, 'FINISH')

            
def Instrument_Check(runDate, query_folder, cutoffHour):
    ''' For the specified instruments (query_folder), check if the SPOT price
    on the specified date (runDate) are not stale.
    
    A price is considered to be stale if the update time is smaller than the
    runDate + cutoffHour
    
    The function logs warnings if the price is missing or is stale.
    '''
    stalePeriod = exec_delay(runDate, cutoffHour)
    print("Cutoff start: %s" %stalePeriod)
    ins = query_folder.Query().Select()
    for i in ins:
        if runDate == TODAY:
            run_date_prices = i.Prices()
        else:
            run_date_prices = i.HistoricalPrices()

        spot = [p for p in run_date_prices if p.Market().Name() == "SPOT" 
                and p.Day() == runDate]
        if spot:            
            spot = spot[0]
            updateTime = at_time.to_datetime(spot.UpdateTime())
            broken = updateTime < stalePeriod
            
            if i.add_info("Exchange") == "BESA":
                # BESA instruments should have SPOT and SPOT_BESA same at the end of the day
                besa = [p for p in run_date_prices if p.Market().Name() == "SPOT_BESA" 
                    and p.Day() == runDate]
                if not besa:
                    logme("BESA price is missing (and SPOT is stale) for %s for %s" %
                            (i.Name(), runDate), "WARNING")
                elif spot.Settle() != besa[0].Settle():
                    logme("SPOT (%f) and BESA (%f) prices are different for %s for %s." %
                        (spot.Settle(), besa[0].Settle(), i.Name(), runDate), "WARNING")
                continue
            
            if broken:
                logme("Update missing for %s for %s, last updated at %s" %
                        (i.Name(), runDate, updateTime), "WARNING")
        else:
            logme("SPOT missing for %s for %s" %(i.Name(), runDate), "WARNING")

def exec_delay(runDate, cutoffHour):
    exec_delay = mktime(
        (at_time.to_datetime(runDate) + timedelta(hours=cutoffHour)).timetuple())
    return at_time.to_datetime(exec_delay)

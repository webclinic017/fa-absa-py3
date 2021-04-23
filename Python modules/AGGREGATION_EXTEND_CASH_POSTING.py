import acm
import FBDPGui
import importlib
importlib.reload(FBDPGui)

ael_variables = FBDPGui.LogVariables(
                                    ['instruments', 'Cash Posting Instruments', acm.FInstrument, acm.FInstrument, None, 1, 1, 'Expiry dates of the selected instruments will be extended to the last business day of the previous month.', None, 1]
                                   )

def setInstrumentExpiry(instrument, newEndDate):
    new_end_date = newEndDate

    ins_obj = instrument

    for leg_obj in ins_obj.Legs():
        leg_obj.EndDate(new_end_date)
        
    ins_obj.ExpiryDate(new_end_date)

    try:
        ins_obj.Commit()
        for leg_obj in ins_obj.Legs():
            leg_obj.GenerateCashFlows(0)
            
    except Exception, errorMessage:
        print 'ERROR: The following instrument could not be extended: %s - ERROR: %s.' %(instrument.Name(), errorMessage.message)
        leg_obj.Undo()
        ins_obj.Undo()

def ael_main(dict):
    scriptName = __name__
    listOfInstruments = dict['instruments']
    
    print 'INFO: STARTING SCRIPT: %s.' %scriptName
    print 'INFO: The following instruments are selected to be extended:'
    for instrument in listOfInstruments:
        print 'INFO: \t\t %s' %instrument.Name()
    
    valParam = acm.UsedValuationParameters()
    calendar = valParam.AccountingCurrency().Calendar()
    today = acm.Time.DateToday()
    lastMonth = acm.Time.DateAddDelta(today, 0, -1, 0)
    firstDayOfLastMonth = acm.Time.FirstDayOfMonth(lastMonth)
    firstBusinessDayOfLastMonth = calendar.ModifyDate(calendar, calendar, firstDayOfLastMonth, 3)

    print 'INFO: Last business day of the previous month: %s' %firstBusinessDayOfLastMonth

    for instrument in listOfInstruments:
        instrumentExpiryDate = instrument.ExpiryDate().split(' ')[0]
        
        if not (instrumentExpiryDate == firstBusinessDayOfLastMonth):
            print 'INFO: %s - setting expiry date to %s.' %(instrument.Name(), firstBusinessDayOfLastMonth)
            setInstrumentExpiry(instrument, firstBusinessDayOfLastMonth)
        else:
            print 'INFO: %s is already set to the correct date.' %instrument.Name()

    print 'Completed successfully.'


import FUxCore
import acm, ael

ACTION_DELETE = "DELETE"
ACTION_CREATE = "CREATE"
ACTION_RESET  = "RESET"
global win

def showActionPopUp(eventValues, action):

    import FxPriceSwapNotify
    reload(FxPriceSwapNotify)
    dlg = FxPriceSwapNotify.FxPriceSwapNotify(eventValues, action)
    builder = dlg.CreateLayout()    
    shell = win.ExtensionObject().Shell()    
    params = acm.UX().Dialogs().ShowCustomDialogModal(shell, builder, dlg )
    if params:
        return True
    else:
        return False
       
def validateSelectedInstrument(ins):

    floatReferences = []
    fixedRates = []
    existingEventDates = {}
    existingResetDates = {}
    currency = None
    func=acm.GetFunction('msgBox', 3)     

    if ins:
        if ins.InsType() != "PriceSwap":
            func("ERROR", "Instrument is not of type Price Swap.", 0)
            return None      

        for leg in ins.Legs():
            if leg.FloatRateReference():
                floatReferences.append(leg.FloatRateReference().Name())
                currency =leg.FloatRateReference().Currency()
                for cashflow in leg.CashFlows():
                   for reset in cashflow.Resets():
                        existingResetDates[reset.Day()] = -1
            if leg.FixedRate():
                fixedRates.append(leg.FixedRate())
            
        if len(fixedRates) == 2:
            func("ERROR", "Two Fixed Rate references set on Instrument.", 0)
            return None  
        if len(floatReferences) == 2:
            func("ERROR", "Two Float Rate references set on Instrument: %s" % floatReferences, 0)
            return None
        if len(floatReferences) == 0:
            func("ERROR", "No Float Rate references set on Instrument: %s" % floatReferences, 0)
            return None
            
        for exoticEvent in ins.ExoticEvents():
            if exoticEvent.Type() == 'Fx Rate':
                existingEventDates[exoticEvent.Date()] = exoticEvent.Oid()
            else:
                func("ERROR", "Exotic Events not of type \'Fx Rate\' exist on instrument.", 0) 
                return None
    else:
        func=acm.GetFunction('msgBox', 3) 
        func("ERROR", "No instrument is selected.", 0)
        return None
    
    returnDict = {}
    returnDict['existingEventDates'] = existingEventDates
    returnDict['existingResetDates'] = existingResetDates
    returnDict['currency'] = currency
    return returnDict

def commitExoticEvents(actionDictionary, instrument, currency, action):
    DEFAULT_EVENT_VALUE = -1
    displayDict = {}

    if action == ACTION_CREATE:
        for eventDate in actionDictionary.keys():
            displayDict[eventDate] = DEFAULT_EVENT_VALUE
        if showActionPopUp(displayDict, "Create"):
            for eventDate in actionDictionary.keys():
                event = acm.FExoticEvent()
                event.Date(eventDate)
                event.EndDate(eventDate)
                event.Instrument(instrument)
                event.ComponentInstrument(currency)
                event.EventValue(DEFAULT_EVENT_VALUE)
                event.Type("Fx Rate")
                event.Commit()
            return True
    elif action == ACTION_RESET:
        for eventDate in actionDictionary.keys():
            displayDict[eventDate] = DEFAULT_EVENT_VALUE
        if showActionPopUp(displayDict, "Reset"):
            for eventDate in actionDictionary.keys():
                eventClone = acm.FExoticEvent[actionDictionary[eventDate]]
                eventClone.EventValue(DEFAULT_EVENT_VALUE)
                eventClone.Commit()
            return True
    elif action == ACTION_DELETE:
        for eventDate in actionDictionary.keys():
            displayDict[eventDate] = acm.FExoticEvent[actionDictionary[eventDate]].EventValue()
        if showActionPopUp(displayDict, "Delete"):    
            for date in actionDictionary.keys():
                event = acm.FExoticEvent[actionDictionary[date]]
                event.Delete()
            return True

def createExoticEvents(eii):
    global win
    win = eii
    obj = eii.ExtensionObject()
    instrument = obj.OriginalInstrument()
    func=acm.GetFunction('msgBox', 3)
    missingEventDates = {}
    deleteEventDates  = {}
    currency = None
    validate = validateSelectedInstrument(instrument)
    if validate:
        existingResetDates = validate['existingResetDates']
        existingEventDates = validate['existingEventDates']
        currency           = validate['currency']
    else:
        func("ERROR", "Cannot create Exotic Events.", 0)
        return None
                   
    if instrument and currency:
        for date in existingResetDates.keys():
            if date not in existingEventDates.keys():
                missingEventDates[date] = -1
    
        for date in existingEventDates.keys():
            if date not in existingResetDates.keys():
                deleteEventDates[date] = existingEventDates[date]
                
        if len(deleteEventDates.keys()) != 0:   #Delete events
        
            try:
            
                result = commitExoticEvents(deleteEventDates, instrument, currency, ACTION_DELETE)
                if result:
                    func("Done", "Done deleting Exotic Events.", 0)
                else:
                    pass
            except Exception, e:
                func("ERROR", "Cannot delete Exotic Events.\n%s" % str(e), 0)
                raise
        
        if len(missingEventDates.keys()) == 0: #Reset event values
            func("INFO", "All Exotic Events exist.", 0) 
                      
        elif len(existingEventDates.keys()) == 0:
            try:
                result = commitExoticEvents(existingResetDates, instrument, currency, ACTION_CREATE)               
                if result:
                    func("INFO", "Done creating Exotic Events.", 0)
                else:
                    pass        
            except Exception, e: 
                func("ERROR", "Cannot create Exotic Events.\n%s" % str(e), 0)        
                raise
                
        elif len(missingEventDates) != 0:
            try:
                result = commitExoticEvents(missingEventDates, instrument, currency, ACTION_CREATE)               
                if result: 
                    func("INFO", "Done creating Exotic Events.", 0)
                else:
                    pass
            except Exception, e:
                func("ERROR", "Cannot create Exotic Events.\n%s" % str(e), 0)
                raise
    else:
        func("ERROR", "Cannot create Exotic Events.", 0)
 
    eventArray = acm.FArray()
    for e in instrument.ExoticEvents():
        if ael.date(e.Date()) < ael.date_today():
            eventArray.Add(e)

    if len(eventArray) >= 1:
        popUpResult = func("INFO", "Fix %s historical Exotic Events?" % len(eventArray), 4)
        if popUpResult == 6:
        
            import FBDPString
            reload(FBDPString)
            import FBDPCommon
            reload(FBDPCommon)
            import FxPriceSwapFixExoticEventsPerform
            reload(FxPriceSwapFixExoticEventsPerform)    
            logme = FBDPString.logme
            
            dictionary = {}
            dictionary['exoticEvents'] = eventArray
            dictionary['SendReportByMail'] = 0
            dictionary['LogToConsole'] = 1
            dictionary['LogToFile'] = 0
            dictionary['MailList'] = ""
            dictionary['ReportMessageType'] = ('Full Log',)
            dictionary['Logmode'] = 1
            dictionary['testmode'] = 0
            dictionary['Logfile'] = 'BDP.log'
            
            ScriptName = "ExoticEventFixing"
            logme.setLogmeVar(ScriptName,
                              dictionary['Logmode'],
                              dictionary['LogToConsole'],
                              dictionary['LogToFile'],
                              dictionary['Logfile'],
                              dictionary['SendReportByMail'], 
                              dictionary['MailList'], 
                              dictionary['ReportMessageType'])
            FBDPCommon.execute_script(FxPriceSwapFixExoticEventsPerform.fixExoticEvents, dictionary)
            logme('FINISH')        
        else:
            pass



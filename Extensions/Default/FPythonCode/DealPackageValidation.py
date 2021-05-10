import acm

def ValidatePackage(package, validationAspect):
    errorStr = ""
    if validationAspect == 'DealPackage':
        errorStr = "Deal Package " + str(package.Originator().Oid()) + " in "
    try:
        error = package.IsValid(validationAspect)
        if error is not True:
            raise Exception(error)
    except Exception as e:
        errorStr += "Instrument Package '" + package.InstrumentPackage().Name() + "' is not valid. (" + str(e) + ")"
        raise Exception(errorStr)

def ApplyChangesToPackage(package, modifiedTradesAndInstruments):
    updatedInstruments = modifiedTradesAndInstruments.At("instrumentUpdates") 
    deletedInstruments = modifiedTradesAndInstruments.At("instrumentDeletes") 
    updatedTrades = modifiedTradesAndInstruments.At("tradeUpdates")
    deletedTrades = modifiedTradesAndInstruments.At("tradeDeletes")
    package.ReplaceTrades(updatedTrades)
    RemoveTrades(package, deletedTrades)
    package.ReplaceInstruments(updatedInstruments)
    RemoveInstruments(package, deletedInstruments)
    return package
    
def CreateDealPackageFromUpdatedInstrumentPackage(package, modifiedTradesAndInstruments):
    package = package.Copy()
    updatedInstruments = modifiedTradesAndInstruments.At("instrumentUpdates") 
    deletedInstruments = modifiedTradesAndInstruments.At("instrumentDeletes") 
    package.ReplaceInstruments(updatedInstruments)
    RemoveInstruments(package, deletedInstruments)
    package = acm.DealPackage.NewAsDecoratorFromInstrumentPackage(package)
    return package 

def ValidationAspect(package):
    validationAspect = 'DealPackage'
    if package.IsKindOf(acm.FInstrumentPackage):
        validationAspect = 'InstrumentPackage'
    return validationAspect

def RemoveTrades(package, tradeDeletes):
    for trade in tradeDeletes:
        for tradeLink in package.TradeLinks():
            if tradeLink.Trade().OriginalOrSelf() == trade.OriginalOrSelf():
                package.TradeLinks().Remove(tradeLink)
    
def RemoveInstruments(package, instrDeletes):
    for instrument in instrDeletes:
        for instrLink in package.InstrumentLinks():
            if instrLink.Instrument().OriginalOrSelf() == instrument.OriginalOrSelf():
                package.InstrumentLinks().Remove(instrLink)
                
def CreateModifiedTradesAndInstrumentsDict(package, dictionary):
    modifiedTradesAndInstruments = acm.FDictionary()
    modifiedTradesAndInstruments.AtPut("tradeUpdates", acm.FArray())
    modifiedTradesAndInstruments.AtPut("instrumentUpdates", acm.FArray())
    modifiedTradesAndInstruments.AtPut("tradeDeletes", acm.FArray())
    modifiedTradesAndInstruments.AtPut("instrumentDeletes", acm.FArray())
    dictionary.AtPut(package, modifiedTradesAndInstruments)
    return modifiedTradesAndInstruments
    
def GetModifiedTradesAndInstrumentsDict(package, dictionary):
    modifiedTradesAndInstruments = dictionary.At(package)
    if not modifiedTradesAndInstruments:
        modifiedTradesAndInstruments = CreateModifiedTradesAndInstrumentsDict(package, dictionary)
    return modifiedTradesAndInstruments

def AddInstrumentUpdateToDealPackageDictionary( dictionary, aelInstr, operation, packagesBeingDeleted ):
    instrument = acm.Ael().AelToFObject(aelInstr)
    dealPackInstrLinks = instrument.DealPackageInstrumentLinks()
    if not dealPackInstrLinks and instrument.Original():
        dealPackInstrLinks = instrument.Original().DealPackageInstrumentLinks()
    for instrLink in dealPackInstrLinks:
        package = instrLink.InstrumentPackage()
        if package not in packagesBeingDeleted:
            modifiedTradesAndInstruments = GetModifiedTradesAndInstrumentsDict(package, dictionary)
            if operation == 'Update':
                instruments = modifiedTradesAndInstruments.At("instrumentUpdates")
                instruments.Add(instrument)
            if operation == 'Delete':
                instruments = modifiedTradesAndInstruments.At("instrumentDeletes")
                instruments.Add(instrument)
            
def AddTradeUpdateToDealPackageDictionary( dictionary, aelTrade, operation, packagesBeingDeleted ):
    trade = acm.Ael().AelToFObject(aelTrade)
    package = trade.DealPackage()
    if not package and trade.Original() and trade.Original().OpeningDealPackage():
        package = trade.Original().DealPackage()
    if package:
        if package not in packagesBeingDeleted:
            modifiedTradesAndInstruments = GetModifiedTradesAndInstrumentsDict(package, dictionary)
            if operation == 'Update':
                trades = modifiedTradesAndInstruments.At("tradeUpdates")
                trades.Add(trade)
            if operation == 'Delete':
                trades = modifiedTradesAndInstruments.At("tradeDeletes")
                trades.Add(trade)
        
def CreateDictionaryOfAffectedDealPackages(t_list, packagesBeingDeleted):
    dealPackageDict = acm.FDictionary()
    for (element, operation) in t_list:
        if element.record_type == 'Instrument':
            AddInstrumentUpdateToDealPackageDictionary(dealPackageDict, element, operation, packagesBeingDeleted)
        if element.record_type == 'Trade':
            AddTradeUpdateToDealPackageDictionary(dealPackageDict, element, operation, packagesBeingDeleted)
    return dealPackageDict

def PackagesBeingDeleted(t_list):
    packagesBeingDeleted = acm.FArray()
    for (element, operation) in t_list:
        if (element.record_type == 'DealPackage' or element.record_type == 'InstrumentPackage') and operation == 'Delete':
            package = acm.Ael().AelToFObject(element)
            packagesBeingDeleted.Add(package)
    return packagesBeingDeleted

def ValidateDealPackageChanges(t_list):
    packagesBeingDeleted = PackagesBeingDeleted(t_list)
    dealPackageDict = CreateDictionaryOfAffectedDealPackages(t_list, packagesBeingDeleted)
    if dealPackageDict.Keys().Size() > 0:
        for package in dealPackageDict.Keys():
            if package.Oid() > 0 and package not in packagesBeingDeleted:
                modifiedTradesAndInstruments = dealPackageDict.At(package)
                validationAspect = ValidationAspect(package)
                
                if validationAspect == 'InstrumentPackage':
                    package = CreateDealPackageFromUpdatedInstrumentPackage(package, modifiedTradesAndInstruments)
                else:
                    package = package.Edit()
                    package = ApplyChangesToPackage(package, modifiedTradesAndInstruments)
                ValidatePackage(package, validationAspect)

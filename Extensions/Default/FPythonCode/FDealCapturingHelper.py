import acm

def createNewSwapFromSwaptionDefinition( swaption, newUnderlyingSwap ):
    """
    DESCRIPTION: Function enables support to modify the newUnderlyingSwap 
                  created from Swaption UI if ExtensionValue
                  _InsDef_CreateNewSwapFromSwaptionDefinitionIsEnabled is set to true.
    INPUT:       The swaption to be created. 
                 The newUnderlyingSwap originating from a generic swap.
    OUTPUT:      True or False
    """
   
    return 1

def suggestDiscountingType( trade ):
    """
    DESCRIPTION: Function enables support to modify the DiscountingType
                 of a trade or instrument.
    INPUT:       A trade object. DiscountingType should be set on the trade
                 or on the corresponding instrument. 
    OUTPUT:      True or False
    """
    
    passForTradeStatuses =["Simulated",
                           "Void",
                           "Reserved"]
    
    useFallBackDiscType  = False
    
    def fallBackDiscType( trade ):
        #Implement logic for fallback disc type.
        fallBackDiscType = acm.FChoiceList['IBOR']    
        return fallBackDiscType
        
    def cptyHasCollateralAgreement( trade ):
        collateralAgreements = trade.Counterparty().CollateralAgreementLinks()
        if collateralAgreements:
            return True
        return False
    
    def tradeStatusPass( trade ):
        trades = trade.Instrument().Originator().Trades()
        for t in trades:
            if t.Status() not in passForTradeStatuses:
                return False
        return True
            
    def validCounterparty( trade ):
        if not trade.Counterparty():
            acm.Math.ThrowError( "Discounting Type cannot be suggested as no trade Counterparty has been selected." )
        return True
            
    def instrumentOrTrade( trade ):
        instrumentOrTrade = trade.Instrument()
        if trade.Instrument().IsKindOf("FCurrency"):
            # Set value on the trade for fx cash
            instrumentOrTrade = trade
        return instrumentOrTrade

    def validDiscountingType( trade, discountingType ):
        iOrT = instrumentOrTrade( trade )
        if iOrT.Originator() and iOrT.DiscountingType():
            return True
        elif not discountingType:
            acm.Log( "Discounting Type will not be updated as no Disc Type has been selected in the Collateral Agreement used for the trade." )
            return False
        return True

    def validCollateralAgreement( collateralAgreement ):
        if not collateralAgreement:
            acm.Math.ThrowError( "Discounting Type cannot be suggested as no trade Collateral Agreement is available." )
        return True
                    
    def discountingTypeFromTrade( trade, useFallBackDiscType ):
        collateralAgreement  = trade.CollateralAgreement()
        if not collateralAgreement and useFallBackDiscType:
            fallBack = fallBackDiscType( trade )
            return fallBack
        return False if not validCollateralAgreement( collateralAgreement ) else collateralAgreement.DiscountingType()
        
    def checkDiscTypeInSync( instrument, discountingType):
        if instrument.IsKindOf("FCurrency"):
            return True
        else:
            return instrument.DiscountingType() == discountingType
        
    def setDiscountingType( trade, discountingType ):
        iOrT = instrumentOrTrade( trade )
        iOrT.DiscountingType(discountingType)
        valueSet = True
        collateralAgreement = trade.CollateralAgreement()
        if not collateralAgreement and useFallBackDiscType:
            if cptyHasCollateralAgreement( trade ):
                acm.Math.ThrowError("No trade Collateral Agreement chosen, Disc Type set to %s"%(fallBackDiscType( trade ).Name()))
            
    valueSet = False
    if validCounterparty( trade ):
        discountingType = discountingTypeFromTrade( trade, useFallBackDiscType )
        tradeStatusPassed = tradeStatusPass( trade )
        if tradeStatusPassed and validDiscountingType( trade, discountingType ):
            setDiscountingType(trade, discountingType)
        else:
            if checkDiscTypeInSync( trade.Instrument(), discountingType ):
                setDiscountingType(trade, discountingType)
            else:
                discTypeName = 'None' if not discountingType else discountingType.Name()
                acm.Math.ThrowError( "Discounting Type will not be updated as trades already exist in this instrument. Suggested Disc Type for this trade is " + discTypeName )
    return valueSet

def collateralAgreementChanged( trade ):
    """
    DESCRIPTION: Function enables support to modify the DiscountingType
                 of a trade or instrument and is called when collateral agreement is changed.
    INPUT:       A trade object. DiscountingType should be set on the trade
                 or on the corresponding instrument. 
    OUTPUT:      True or False
    """
    insTypesValidForAutoSuggest =["Swap",
                                  "IndexLinkedSwap",
                                  "CurrSwap",
                                  "Cap",
                                  "Floor",
                                  "FRA"]

    def shouldSuggestDiscountingType( trade ):
        valid = False
        insIsGeneric = trade.Instrument().Generic()
        for instype in insTypesValidForAutoSuggest:
            if instype == trade.Instrument().InsType() and not insIsGeneric:
                valid = True
        
        if "Option" == trade.Instrument().InsType() and trade.Instrument().Underlying() and not insIsGeneric:
            valid = trade.Instrument().Underlying().InsType() in ('SWAP', 'FRA')
        return valid
        
    if shouldSuggestDiscountingType(trade):
        return suggestDiscountingType(trade)
    return False

def suggestQuotation(suggestedQuotation, insType, undInsType, *args):
    """
    DESCRIPTION: Function enables support to modify the Quotation
                 of an instrument and is called when an instrument is created or when Generic is untoggled 
    INPUT:       The current suggested quotation of the instrument, the instrument type and
                 the instrument type of the underlying instrument
    OUTPUT:      The desired quotation
    """
    return suggestedQuotation

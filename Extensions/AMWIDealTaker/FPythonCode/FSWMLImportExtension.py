"""------------------------------------------------------------------------
MODULE
    FSWMLImportExtension -
DESCRIPTION:
    The APIs in this file are called during the deal Import. These APIs give the user the flexibility to add/override the trade attributes before the trade is committed
VERSION: 1.0.30 
--------------------------------------------------------------------------"""
import FFpMLLogger
import FFpMLACMException
import acm
import FFpMLACMUserAPIs
def importEntry(swmlMsg, userDictionary):
    try:
        #user will flood userDictionary on the basis of swmlMsg
        '''
        #Sample code to update first fixing on cashflows. 
        #Need to provide the float rate reference for which the fixing is being provided 
        floatRateRefDict = {}
        floatRateRefDict['GBP/LIBOR/6M'] = '0.45'
        floatRateRefDict['GBP/LIBOR/3M'] = '0.85'
        paymentType = {'AmendmentFee':'Allocation Fee', 'UpfrontFee':'Premium'}
        userDictionary['PaymentType'] = paymentType
        userDictionary['FirstFixingOnCashFlow'] = floatRateRefDict        
        userDictionary['ISDAIndexTenor'] = 'ISDAIndexTenorReuters'
        '''
        return userDictionary
    except Exception as e:
        errorMessage = 'An error occurred while flooding the userDictionary in importEntry hook'
        FFpMLLogger.ELOG('ImportAdaptation', str(e))
        raise FFpMLACMException.FAHookException(errorMessage)

def importExit(fTrade, swmlMsg, userDictionary):
    #the trade object is updated/altered with new parameters
    #SwmlMsg also provided for any further lookup
    ''' The standard adaptation method for imported messages before the
    tradeObject message is passed to the ADS.
    The tradeObject is complete after all the standard mappings from the
    incoming SWML message have been done, and is just to be written to the ADS.
    This tradeObject can be modified before the return from this function leads
    to the write to the ADS. Related and child objects like FParty and FInstrument
    can be accessed from this tradeObject.
    swmlMessage contains the original SWML message as received from the MarkitWire
    and all the desired values from swml can be fetched using
    1. getValueOfNode()
        e.g.  businessCenter = FFpMLACMUserAPIs.getValueOfNode(swmlMsg, \
           "SWML.swStructuredTradeDetails.FpML.trade.swap.swapStream @{'id':'fixedLeg'}.earlyTerminationProvision.optionalEarlyTermination.cashSettlement@{'id':'cashSettlement'}.businessCenter")
`       Now this function returns businessCenter which can be mapped to any possible acmTradeObj attribute.
        More help on getValueOfNode() can be found in the installation document.

    2. getAllValuesOfNode() 
        e.g.  adjustedDatesArray = FFpMLACMUserAPIs.getAllValuesOfNode(swmlMsg, \
           "SWML.swStructuredTradeDetails.FpML.trade.swap.earlyTerminationProvision.optionalEarlyTermination.cashSettlement.cashSettlementPaymentDate.adjustableDates.unadjustedDate")
`       Now this function returns all the adjustedDates in an array which can be used further.
        More help on getAllValuesOfNode() can be found in the installation document.

    3. getValueOfAttribute() 
        e.g.  payerPartyReference = FFpMLACMUserAPIs.getValueOfAttribute(swmlMsg, \
           "SWML.swStructuredTradeDetails.FpML.trade.swap @{'id':'fixedLeg'}.payerPartyReference", 'href')
`       Now this function returns value of the attribute href for the node payerPartyReference.
        More help on getValueOfAttribute() can be found in the installation document.

    4. getAllValuesOfAttribute() 
        e.g.  swapIds = FFpMLACMUserAPIs.getAllValuesOfAttribute(swmlMsg, \
           "SWML.swStructuredTradeDetails.FpML.trade.swap.swapStream", 'id')
`       Now this function returns value of all the attribute id of node swap in an array which can be used further.
        More help on getAllValuesOfAttribute() can be found in the installation document.
    '''
    FFpMLLogger.DLOG('ImportAdaptation', 'Entered into importExitHook()')
    try:
        '''
        #Sample code to access linked attributes
        counter = 1
        print "fTrade.Instrument().ExerciseEvents()", fTrade.Instrument().ExerciseEvents()
        for break_date in fTrade.Instrument().ExerciseEvents():
            break_date.NoticePeriodCount(-5)
            break_date.FreeText('Break' + str(counter))
            counter = counter + 1
        for leg in fTrade.Instrument().Legs():
            if leg.LegType() == 'Float':
                for stub_reset in leg.StubResetEstimations():
                    if stub_reset.FixingRef1() == acm.FInstrument['GBP/LIBOR/3M']:
                        stub_reset.FixingRef1(acm.FInstrument['GBP/LIBOR/1M'])
                        stub_reset.EstimationRef1(acm.FInstrument['GBP/LIBOR/1M'])
                if leg.FloatRateReference().Name() == 'GBP/LIBOR/3M':
                    cashFlow = (leg.CashFlows().SortByProperty('PayDate', True))[0]
                    reset = cashFlow.Resets()[0]
                    reset.FixingValue(25.87)
                    reset.ReadTime(ael.date_today())
                
        fTrade.AdditionalInfo().CCPmwire_user_msg('This is a sample message')         
        for payment in fTrade.Payments():
            if payment.Type() == 'Premium':
                payment.Type(acm.EnumFromString('PaymentType', 'Commission'))
        '''
        '''        
        messageStatus = ''
        addInfo = userDictionary['FAdditionalInfo']
        if addInfo.has_key('CCPmwire_message_st'):
            messageStatus = addInfo['CCPmwire_message_st']            
        if fTrade.Counterparty() and fTrade.Counterparty().Name() == 'LCH Clearnet Ltd Onboarding':
            if messageStatus == 'ClearingInitiated':
                clonedTrade = fTrade.Clone()
                clonedTrade.Contract(fTrade)
                clearingBroker = None        
                if fTrade.AdditionalInfo().CCPclr_broker_ptynb():
                    clearingBroker = fTrade.AdditionalInfo().CCPclr_broker_ptynb()
                    if clearingBroker:
                        clonedTrade.Counterparty(clearingBroker)
                if clonedTrade.Payments():
                    for payment in clonedTrade.Payments():                    
                        if payment.Party() and payment.Party() == addInfo['CCPoriginal_counter']:                            
                            payment.Party(fTrade.Counterparty())
                clonedTrade.Commit()        
                FFpMLACMUserAPIs.copyAddInfos(fTrade, 'CCPmiddleware_id', clonedTrade)
                FFpMLACMUserAPIs.copyAddInfos(fTrade, 'CCPmiddleware_versi', clonedTrade)
                FFpMLACMUserAPIs.copyAddInfos(fTrade, 'CCPmwire_booking_st', clonedTrade)
                FFpMLACMUserAPIs.copyAddInfos(fTrade, 'CCPmwire_contract_s', clonedTrade)
                FFpMLACMUserAPIs.copyAddInfos(fTrade, 'CCPclearing_process', clonedTrade)
                FFpMLACMUserAPIs.copyAddInfos(fTrade, 'CCPclearing_status', clonedTrade)
                cpty = FFpMLACMUserAPIs.getAdditionalInfoBySpec('CCPoriginal_counter', fTrade, userDictionary)
                if payments:
                    for payment in payments:
                        if payment.Party() and payment.Party() == fTrade.Counterparty():
                            payment.Party(cpty)
                fTrade.Counterparty(cpty)        
                trdStatus = acm.EnumFromString('TradeStatus', 'Void')
                fTrade.Status(trdStatus)
                FFpMLACMUserAPIs.removeAddInfoInTransaction(fTrade, 'CCPoriginal_counter', userDictionary)
                FFpMLACMUserAPIs.removeAddInfoInTransaction(fTrade, 'CCPmiddleware_id', userDictionary)
            else:
                clearingBroker = None        
                if fTrade.AdditionalInfo().CCPclr_broker_ptynb():
                    clearingBroker = fTrade.AdditionalInfo().CCPclr_broker_ptynb()
                    if clearingBroker:
                        fTrade.Counterparty(clearingBroker)
                FFpMLACMUserAPIs.removeAddInfoInTransaction(fTrade, 'CCPoriginal_counter', userDictionary)
        '''                        
        return fTrade
    except Exception as e:
        errorMessage = 'An error occurred while manipulating the fTrade object in importExit hook'
        FFpMLLogger.ELOG('ImportAdaptation', str(e))
        raise FFpMLACMException.FAHookException(errorMessage)

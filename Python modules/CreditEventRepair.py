import acm
import FUxCore
import FLogger
import TradeStatusDialog
import CreditEventParameters


def OnOpenButtonClicked(self, cd):
    self.OpenCreditEvent()
    
def OnNewButtonClicked(self, cd):
    self.PrepareNew()
    self.InitInstruments()
    self.FilterInstruments()
    self.UpdateTradeSheet()    

def OnUndoButtonClicked(self, cd):
    self.UndoCreditEvent()

def OnRunButtonClicked(self, cd):
    self.PerformCreditEvent()

def OnTradeRuleChanged(self, cd):
    self.m_tradeRule = self.m_tradeRuleCtrl.GetValue()

def OnSettlementDateChanged(self, cd):
    try:self.m_settlementDate = self.m_settlementDateCtrl.GetValue()
    except Exception, err:pass
        
def OnAuctioningDateChanged(self, cd):
    try:
        self.m_auctioningDate = self.m_auctioningDateCtrl.GetValue()
        if not self.m_auctioningDate:
            self.m_recoveryRateCtrl.SetValue( 0.0 )
    except Exception, err:
        pass
    if self.m_auctioningDate:
        self.m_recoveryRateCtrl.Enabled(True)
    else:
        self.m_recoveryRateCtrl.Enabled(False)
        
def OnRecoveryRateChanged(self, cd):
    try:self.m_recoveryRate = self.m_recoveryRateCtrl.GetValue()
    except Exception, err:pass

def OnCreditEventIdChanged(self, cd):
    self.m_creditEventId = self.m_creditEventIdCtrl.GetValue()

def OnFreeText1Changed(self, cd):
    self.m_freeText1 = self.m_freeText1Ctrl.GetValue()

def OnFreeText2Changed(self, cd):
    self.m_freeText2 = self.m_freeText2Ctrl.GetValue()

def OnEventStatusCtrlChanged(self, cd):
    self.m_eventStatus = acm.FEnumeration['enum(BusinessEventStatus)'].Enumeration(self.m_eventStatusCtrl.GetValue())

def OnTradeStatusClosingCtrlChanged(self, cd):
    self.m_tradeStatusClosing = acm.EnumFromString('TradeStatus', self.m_tradeStatusClosingCtrl.GetValue())

def OnTradeStatusModifyClosingCtrlChanged(self, cd):
    value = self.m_tradeStatusModifyClosingCtrl.GetValue()
    if value == "No Change":
        self.m_tradeStatusModifyClosing = 0
    else:
        self.m_tradeStatusModifyClosing = acm.EnumFromString('TradeStatus', value)
        
def OnTradeStatusModifyOtherCtrlChanged(self, cd):
    value = self.m_tradeStatusModifyOtherCtrl.GetValue()
    if value == "No Change":
        self.m_tradeStatusModifyOther = 0
    else:
        self.m_tradeStatusModifyOther = acm.EnumFromString('TradeStatus', value)

def OnEventTypeChanged(self, cd):
    self.m_eventType = acm.FEnumeration['enum(CreditEventType)'].Enumeration(self.m_eventTypeCtrl.GetValue())

def OnToggleAllChanged(self, cd):
    self.PerformToggleProcess()
    
def OnTestmodeChanged(self, cd):
    self.m_testmode = self.m_testmodeBox.Checked()

def OnSeniorityChanged(self, cd):
    self.m_seniority = CreditEventDialog.SENIORITY.At(self.m_seniorityCtrl.GetValue())
    self.m_filterInstruments = True

def OnRestructuringChanged(self, cd):
    self.m_restructuring = acm.FEnumeration['enum(RestructuringType)'].Enumeration(self.m_restructuringCtrl.GetValue())
    self.m_filterInstruments = True

def OnCurrencyChanged(self, cd):
    self.m_currency = self.m_currencyCtrl.GetValue()
    self.m_filterInstruments = True

def OnUndCurrencyChanged(self, cd):
    self.m_undCurrency = self.m_undCurrencyCtrl.GetValue()
    self.m_filterInstruments = True

def OnFilterChanged(self, cd):
    self.m_bankruptcy = self.m_bankruptcyBox.Checked()
    self.m_failureToPay = self.m_failureToPayBox.Checked()
    self.m_obligDefault = self.m_obligDefaultBox.Checked()
    self.m_obligAccel = self.m_obligAccelBox.Checked()
    self.m_repudiation = self.m_repudiationBox.Checked()
    self.m_govIntervention = self.m_govInterventionBox.Checked()
    self.m_filterInstruments = True

def OnUseFilterChanged(self, cd):
    self.m_useFilter = self.m_useFilterBox.Checked()
    self.UpdateFilterPanelProperties()
    self.m_filterInstruments = True

    self.m_bankruptcyBox.Visible(self.m_useFilter)
    self.m_failureToPayBox.Visible(self.m_useFilter)
    self.m_obligDefaultBox.Visible(self.m_useFilter)
    self.m_obligAccelBox.Visible(self.m_useFilter)
    self.m_repudiationBox.Visible(self.m_useFilter)
    self.m_govInterventionBox.Visible(self.m_useFilter)

def OnShowDetailsChanged(self, cd):
    visible = self.m_showDetailsBox.Checked()
    
    self.m_issuerCtrl.Visible(visible)
    self.m_seniorityCtrl.Visible(visible)
    self.m_currencyCtrl.Visible(visible)
    self.m_undCurrencyCtrl.Visible(visible)
    self.m_restructuringCtrl.Visible(visible)
    self.m_defaultDateCtrl.Visible(visible)
    self.m_auctioningDateCtrl.Visible(visible)
    self.m_settlementDateCtrl.Visible(visible)
    self.m_recoveryRateCtrl.Visible(visible)

    self.m_eventStatusCtrl.Visible(visible)
    self.m_eventTypeCtrl.Visible(visible)
    self.m_freeText1Ctrl.Visible(visible)
    self.m_freeText2Ctrl.Visible(visible)
    self.m_tradeStatusClosingCtrl.Visible(False)
    self.m_tradeStatusModifyClosingCtrl.Visible(False)
    self.m_tradeStatusModifyOtherCtrl.Visible(visible)
    self.m_useFilterBox.Visible(visible)
    self.m_tradeRuleCtrl.Visible(False)
    
    self.UpdateFilterPanelProperties()

def OnInstrumentTypeChanged(self, cd):
    self.m_instrumentType = CreditEventDialog.TYPE_TO_CLASS.At(self.m_instrumentTypeCtrl.GetValue())
    self.m_updateUseFilterToggle = True
    self.m_initInstruments = True

def OnDefaultDateChanged(self, cd):
    try:self.m_defaultDate = self.m_defaultDateCtrl.GetValue()
    except Exception, err:return
    self.m_initInstruments = True

def OnIssuerChanged(self, cd):
    try:self.m_issuer = self.m_issuerCtrl.GetValue()
    except Exception, err:return
    self.m_initInstruments = True
    
def OnStatusFilterButtonClicked(self, cd):
    domain = acm.GetDomain('enum(TradeStatus)')
    enum = acm.FEnumeration['enum(TradeStatus)']
    superset = domain.Elements()

    dlg = TradeStatusDialog.TradeStatusDialog(superset, self.m_statusFilter)
    selection = acm.UX().Dialogs().ShowCustomDialogModal(self.m_fuxDlg.Shell(), dlg.CreateLayout(), dlg)

    if selection != None:
        self.m_statusFilter = selection    
        self.FilterInstruments()
        self.UpdateTradeSheet()
        
def OnRefreshButtonClicked(self, cd):
    self.InitInstruments()
    self.FilterInstruments()
    self.UpdateTradeSheet()    

def OnIncludeTradelessBoxClicked(self, cd):
    self.m_includeTradeless = self.m_includeTradelessBox.Checked()
    self.FilterInstruments()
    self.UpdateTradeSheet()    
    
def OnTimerUpdate(self):
    if self.m_updateSheet:
        self.UpdateTradeSheet()
    if self.m_updateProcess:
        self.UpdateProcessToggle()
    if self.m_updateUseFilterToggle:
        self.UpdateUseFilterToggle()
    if self.m_showPhysicalNotSupported:
        self.ShowPhysicalNotSupportedDialog()
        
def MaxDate(date1, date2):
    return max(date1, date2, key=acm.Time().NumberOfUtcDays)

# This is a replacement for the DependentCreditInstruments function defined in c++
# which searches in the other direction
# This version starts at the issuer instead
def DependentCreditInstruments(issuer, date, cls):
    def ReverseCreditRef(ins):
        legs = acm.FLeg.Select('creditRef="%s" and legType="Credit Default"' % ins.Name())
        return [ leg.Instrument() for leg in legs ]
    
    def ReverseCombo(ins):
        maps = ins.CombinationMaps()    
        res = acm.FArray()
        
        if maps:
            for map in maps:
                if not map.DefaultDate():
                    res.Add(map.Combination())
                
                    # note: recursive call
                    res.AddAll(ReverseCombo(map.Combination()))
            
        return res

    def helper(issuer, ins, res, date, cls, visited, level = 1):
        if ins not in visited:
            
            visited.add(ins)
            
            spec = ins.CreditEventSpec()
            if spec and spec.DefaultDate():
                return
            
            if ins.IsExpiredAt(date):
                return
            
            if ins.Class().IsSubtype(cls): 
                # hardcoded condition
                if not ins.Generic():
                    res.Add(ins)
            
            for node in ReverseCombo(ins):
                if node not in visited:
                    helper(issuer, node, res, date, cls, visited, level + 1)
                
            for node in ReverseCreditRef(ins):
                if node not in visited:
                    helper(issuer, node, res, date, cls, visited, level + 1)
                    
    siblings = acm.FInstrument.Select('issuer=%s' % issuer.Name())

    res = acm.FArray()
    visited = set()
    for child in siblings:
        helper(issuer, child, res, date, cls, visited)
    
    return res

class CreditEventHandler( object ):
    
    LOGGER = FLogger.FLogger( 'CREDIT EVENT' )
    
    PARAMS = None
    
    SPACE = acm.FCalculationMethods().CreateStandardCalculationsSpaceCollection()
    
    PERFORMED_INDICES = acm.FDictionary()
    ISSUER_MAPS = acm.FDictionary()
    CREDIT_EVENTS = acm.FDictionary()
    EVENT_INSTRUMENTS = acm.FDictionary()
    LINKS = acm.FArray()
    
    ENTITY_LOG = acm.FDictionary()
    ENTITY_LOG.AtPut('CombInstrMap', ['Oid', 'Instrument.Name', 'DefaultDate', 'RecoveryRate'])
    ENTITY_LOG.AtPut('CreditEventSpec', ['Oid', 'Instrument.Name', 'DefaultDate', 'RecoveryRate'])
    ENTITY_LOG.AtPut('Trade', ['Oid', 'Contract.Oid', 'Instrument.Name', 'FaceValue', 'Portfolio.Name', 'Type', 'Status', 'Counterparty.Name'])
    ENTITY_LOG.AtPut('Payment', ['Oid', 'Trade.Oid', 'Trade.Instrument.Name', 'Amount', 'PayDay', 'Type'])
    ENTITY_LOG.AtPut('BusinessEvent', ['Oid', 'EventType', 'Status'])
    ENTITY_LOG.AtPut('CreditEvent', ['Name', 'Oid', 'EventType', 'Text1', 'RecordDate', 'SettlementDate', 'AuctioningDate', 'Text2', 'RecoveryRate', 'RestructuringType', 'Party.Name', 'SeniorityChlItem.Name', 'Currency.Name', 'UnderlyingCurrency.Name'])
    ENTITY_LOG.AtPut('BusinessEventInstrumentLink', ['Instrument.Name', 'BusinessEvent.Name'])
    ENTITY_LOG.AtPut('BusinessEventTradeLink', ['Trade.Oid', 'BusinessEvent.Name', 'Trade.Instrument.Name'])
    ENTITY_LOG.AtPut('BusinessEventPaymentLink', ['Payment.Oid', 'BusinessEvent.Name', 'Payment.Trade.Instrument.Name'])
    
    """------------------ Database ------------------"""
    
    def BeginTransaction( cls ):
        if not cls.PARAMS.At('testmode'):
            acm.BeginTransaction()
    BeginTransaction=classmethod(BeginTransaction)
    
    def AbortTransaction( cls ):
        if not cls.PARAMS.At('testmode'):
            acm.AbortTransaction()
    AbortTransaction=classmethod(AbortTransaction)
    
    def CommitTransaction( cls ):
        if not cls.PARAMS.At('testmode'):
            acm.CommitTransaction()
            acm.PollDbEvents()
    CommitTransaction=classmethod(CommitTransaction)
    
    def Commit( cls, entity, origEntity=None ):
        if origEntity:
            cls.LogEntity(entity, 'Modified')
        else:
            cls.LogEntity(entity, 'Created')
        if not cls.PARAMS.At('testmode'):
            entity.Commit()
    Commit=classmethod(Commit)
    
    def Delete( cls, entity ):
        cls.LogEntity(entity, 'Deleted')
        if not cls.PARAMS.At('testmode'):
            entity.Delete()
    Delete=classmethod(Delete)
    
    def GetEntity( cls, entity ):
        if cls.PARAMS.At('testmode'):
            return entity.Clone()
        return entity
    GetEntity=classmethod(GetEntity)
    
    def LogEntity( cls, entity, action ):
        logs = cls.ENTITY_LOG.At(entity.Category())
        args = acm.FArray()
        text = '-------- ' + action + ' ' + entity.Category() + ' --------'
        for log in logs:
            ent = entity
            parts = log.split('.')
            for part in parts:
                if not ent:
                    ent = ''
                    break
                try:
                    args.Clear()
                    args.Add(ent)
                    meth = ent.Class().GetMethod(part, 0)
                    ent = meth.Call(args)
                except:
                    ent = '#'
                    break
            text = text + '\n' + log + ': ' + str(ent)
        cls.LOGGER.LOG(text)
    LogEntity=classmethod(LogEntity)
    
    """------------------ Validation ------------------"""
    
    def StatusIsConfirmed(cls):
        eventStatus = cls.PARAMS.At('eventStatus')
        confirmedStatus = acm.EnumFromString('BusinessEventStatus', 'Confirmed')
        return eventStatus == confirmedStatus
    StatusIsConfirmed=classmethod(StatusIsConfirmed)
    
    def ValidateCreditEvent( cls, tasks ):
        """----- ID and Structure -----"""
        creditEventId = cls.PARAMS.At('creditEventId')
        if not cls.PARAMS.At('testmode') and not creditEventId:
            return (None, None, 'An event name must be entered.')
        originalCreditEvent = cls.PARAMS.At('creditEvent')
        if not originalCreditEvent:
            originalBusinessEvent = None
            if not cls.PARAMS.At('testmode') and acm.FCreditEvent[creditEventId]:
                return (None, None, 'The event id <%s> already exists.' % creditEventId)
        else:
            originalBusinessEvent = originalCreditEvent.BusinessEvent()
            if not creditEventId == originalCreditEvent.Name():
                if not cls.PARAMS.At('testmode') and acm.FCreditEvent[creditEventId]:
                    return (None, None, 'The event id <%s> already exists.' % creditEventId)
    
        """----- Issuer -----"""
        if not cls.PARAMS.At('issuer'):
            return (None, None, 'Issuer is required')
        
        """----- Confirmed Event -----"""
        if originalBusinessEvent and originalBusinessEvent.Status() == 'Confirmed':
            acm.UX().Dialogs().MessageBoxInformation(cls.PARAMS.At('shell'), 'The credit event is in status Confirmed. In order to re-run the event the current event must first be deleted by using the "Undo Event" command.')
            return (None, None, -1)
        
        """----- Required Parameters -----"""
        if not cls.PARAMS.At('defaultDate'):
            return (None, None, 'A default date must be specified.')
        if not cls.PARAMS.At('settlementDate'):
            return (None, None, 'A settlement date must be specified.')
    
        """----- Date sequence -----"""
        systemDate = acm.Time.FromDate(acm.Time.DateToday())
        defaultDate = acm.Time.FromDate(cls.PARAMS.At('defaultDate'))
        settlementDate = acm.Time.FromDate(cls.PARAMS.At('settlementDate'))
        
        if cls.PARAMS.At('auctioningDate'):
            auctioningDate = acm.Time.FromDate(cls.PARAMS.At('auctioningDate'))
        else:
            auctioningDate = None
        
        if settlementDate < defaultDate:
            return (None, None, 'Settlement date cannot be prior to the default date.')
    
        if settlementDate <= systemDate:
            if not auctioningDate:
                return (None, None, 'Auctioning date is required when settlement date is reached.')
    
        if auctioningDate:
            if auctioningDate < defaultDate:
                return (None, None, 'Auctioning date cannot be prior to the default date.')
            if auctioningDate > settlementDate:
                return (None, None, 'Auctioning date cannot be later than the settlement date.')
        
        if cls.StatusIsConfirmed():
            if not auctioningDate:
                return (None, None, 'Auctioning date is required for confirmed events.')
            if auctioningDate > systemDate:
                return (None, None, 'Auctioning date cannot be in the future for confirmed events.')
    
        """----- Recovery rate -----"""
        rr = cls.PARAMS.At('recoveryRate')
        '''
        if auctioningDate and rr == 0.0:
            text = 'Are you sure you want to use 0 as recovery rate for this credit event?'
            if acm.UX().Dialogs().MessageBoxOKCancel(cls.PARAMS.At('shell'), 3, text) == 'Button2':
                return (None, None, -1)            
        '''
        if rr < 0 or rr > 1:
            return (None, None, 'Recovery rate must be between 0 and 100.')
    
        """----- Supported Instruments -----"""
        insToProcess = acm.FDictionary()
        ins = []
        for task in tasks:
            insToProcess.AtPut(task.At('instrument'), None)
            if not task.At('type') in CreditEventParameters.SUPPORTED_TYPES:
                ins.append(task.At('instrument').Name())
        if ins:
            return (None, None, 'Instruments not supported (%s).' % ','.join(ins))
            
        """----- Physical Delivery -----"""
        ins = []
        for instrument in insToProcess.Keys():
            if instrument.SettlementType() == 'Physical Delivery':
                ins.append(instrument.Name())
        if ins:
            return (None, None, 'Physical settlements must be handled manually (%s).' % ', '.join(ins))
        
        """----- FullCouponAndRebate -> StubAccrual not supported -----"""
        if originalCreditEvent:
            prevSettlementDateStr = originalCreditEvent.SettlementDate()
            newSettlementDateStr = cls.PARAMS.At('settlementDate')
            
            if newSettlementDateStr < prevSettlementDateStr:
                defaultDateStr = cls.PARAMS.At('defaultDate')
                insBreakingRule = []
                for instrument in insToProcess.Keys():
                    if cls.IsSettlementDateAfterNextCoupon( instrument, defaultDateStr, prevSettlementDateStr ):
                        if not cls.IsSettlementDateAfterNextCoupon( instrument, defaultDateStr, newSettlementDateStr ):
                            insBreakingRule.append(instrument.Name())
                
                if insBreakingRule:
                    msg = 'It is not supported to change the settlement date from being after next coupon to being before. Undo credit event first if this is desired.\n'
                    if len(insBreakingRule) <= 10:
                        first10Ins = insBreakingRule
                    else:
                        first10Ins = insBreakingRule[:10]
                        first10Ins.append('...')
                    msg += '(%s)' % ', '.join(first10Ins)
                    return (None, None, msg)
        
        basketMap = cls.GetBasketMap()
        """----- Create New -----"""
        if not originalCreditEvent:
            
            """----- Same reference index -----"""
            ins = []
            for instrument in insToProcess.Keys():
                if instrument.IsCreditBasket():
                    insTemp = []
                    for instr in basketMap.At(instrument.CreditReference()):
                        if not insToProcess.HasKey(instr):
                            insTemp.append(instr.Name())
                    if insTemp:
                        ins.append('%s: (%s)' % (instrument.Name(), ','.join(insTemp)))
            if ins:
                text = 'The following Instruments to be processed share the same defaulted credit reference as the Instruments listed with them. Are you sure you want to continue without processing these dependent Instruments?\n\n%s' % ('\n'.join(ins))
                if acm.UX().Dialogs().MessageBoxOKCancel(cls.PARAMS.At('shell'), 3, text) == 'Button2':
                    return (None, None, -1)

        """----- Older or same day events -----"""
        (ins, insEvents, insSameDay, insSameDayEvents) = cls.CheckBasketDays(insToProcess.Keys(), basketMap)
        if ins or insSameDay:
            text1 = None
            text2 = None
            eventsText1 = None
            eventsText2 = None
            if not originalCreditEvent:
                affected = 'Tranche and Nth-To-Default'
            else:
                affected = 'Tranche'
            if ins:
                text1 = 'Later events have occured for basket instruments and previously calculated payments for %s instruments might be affected. Process later occured Credit Events again in chronological order:\n%s' % (affected, '\n'.join(ins))
                eventsText1 = 'Later events:\n%s' % '\n'.join(insEvents)
            if insSameDay:
                text2 = 'Events have occured on the same date for basket instruments and previously calculated payments for %s instruments might be affected. Process Credit Events on the same date again in chronological order if they happened after the current event:\n%s' % (affected, '\n'.join(ins))
                eventsText2 = 'Events on the same date:\n%s' % '\n'.join(insSameDayEvents)
            logText = ''
            if eventsText2:
                logText = eventsText2
            if eventsText1:
                if logText:
                    logText = logText + '\n'
                logText = logText + eventsText1
            cls.LOGGER.LOG('-------- Connected Processed Events --------\n%s' % logText)
            messText = ''
            if text2:
                messText = text2
            if text1:
                if messText:
                    messText = messText + '\n\n'
                messText = messText + text1
            messText = messText + '\n\n' + logText + '\n\n' + 'Proceed with processing Credit Event?'
            if acm.UX().Dialogs().MessageBoxOKCancel(cls.PARAMS.At('shell'), 3, messText) == 'Button2':
                return (None, None, -1)
        return (originalCreditEvent, originalBusinessEvent, None)
    ValidateCreditEvent=classmethod(ValidateCreditEvent)
    
    def ValidateUndoCreditEvent( cls, tasks ):
        originalCreditEvent = cls.PARAMS.At('creditEvent')
        originalBusinessEvent = originalCreditEvent.BusinessEvent()
        
        """----- Confirmed Event -----"""
        if originalBusinessEvent.Status() == 'Confirmed':
            if acm.UX().Dialogs().MessageBoxOKCancel(cls.PARAMS.At('shell'), 4, 'The Credit Event is about to be removed but is in status "Confirmed". Settlements for payments might be affected and need to be verified manually.\n\nProceed with undoing Credit Event?') == 'Button2':
                return (None, None, 1)
        
        """----- Older or same day events -----"""
        basketMap = cls.GetBasketMap()
        insToProcess = acm.FArray()
        for task in tasks:
            insToProcess.Add(task.At('instrument'))
        (ins, insEvents, insSameDay, insSameDayEvents) = cls.CheckBasketDays(insToProcess, basketMap)
        if ins or insSameDay:
            text1 = None
            text2 = None
            eventsText1 = None
            eventsText2 = None
            if ins:
                text1 = 'Later events have occured for basket instruments and previously calculated payments for Tranche and Nth-To-Default instruments might be affected. Process later occured Credit Events again in chronological order:\n%s' % '\n'.join(ins)
                eventsText1 = 'Later events:\n%s' % '\n'.join(insEvents)
            if insSameDay:
                text2 = 'Events have occured on the same date for basket instruments and previously calculated payments for Tranche and Nth-To-Default instruments might be affected. Process Credit Events on the same date again in chronological order if they happened after the current event:\n%s' % '\n'.join(insSameDay)
                eventsText2 = 'Events on the same date:\n%s' % '\n'.join(insSameDayEvents)
            logText = ''
            if eventsText2:
                logText = eventsText2
            if eventsText1:
                if logText:
                    logText = logText + '\n'
                logText = logText + eventsText1
            cls.LOGGER.LOG('-------- Connected Processed Events --------\n%s' % logText)
            messText = ''
            if text2:
                messText = text2
            if text1:
                if messText:
                    messText = messText + '\n\n'
                messText = messText + text1
            messText = messText + '\n\n' + logText + '\n\n' + 'Proceed with undoing Credit Event?'
            if acm.UX().Dialogs().MessageBoxOKCancel(cls.PARAMS.At('shell'), 3, messText) == 'Button2':
                return (None, None, 1)
        return (originalCreditEvent, originalBusinessEvent, None)
    ValidateUndoCreditEvent=classmethod(ValidateUndoCreditEvent)
        
    """------------------ Processing ------------------"""

    def UndoCreditEvent( cls, parameters, tasks ):
        cls.ClearCache()
        cls.PARAMS = parameters
        (creditEvent, businessEvent, err) = cls.ValidateUndoCreditEvent(tasks)
        if err:
            return [None, -1]
        text = 'Started removing of Credit Event Processing for event: %s' % creditEvent.Name()
        if cls.PARAMS.At('testmode'):
            text = text + ' (TESTMODE)'
        cls.LOGGER.LOG(text)
        cls.BeginTransaction()
        try:
            tradesToVoid = []
            entities = acm.FArray()
            for link in businessEvent.TradeLinks():
                contractTrade = link.Trade()
                closingTrade = CreditEventDialog.GetClosingTrade( contractTrade )
                if cls.PARAMS.At('tradeRule') == 'Delete Trades':
                    entities.Add(closingTrade)
                else:
                    trade = cls.GetEntity(closingTrade)
                    tradesToVoid.append((trade, closingTrade))
            for link in businessEvent.PaymentLinks():
                entities.Add(link.Payment())
            cls.PARAMS.AtPut('defaultDate', None)
            cls.PARAMS.AtPut('recoveryRate', 0.0)
            for task in tasks:
                if task.At('type') == 'Singlename CDS':
                    cls.PerformCreditEventSpec(task, True)
                elif task.At('type') in ['Index CDS', 'Tranche CDS', 'Nth-To-Default CDS']:
                    cls.PerformIndex(task, True)
            cls.Delete(creditEvent)
            cls.Delete(businessEvent)
            for (trade, closingTrade) in tradesToVoid:
                trade.Status('Void')
                cls.Commit(trade, closingTrade)
            for entity in entities:
                cls.Delete(entity)
            cls.CommitTransaction()
            if not cls.PARAMS.At('testmode'):
                return [1, None]
            return [None, None]
        except Exception, err:
            cls.AbortTransaction()
            cls.LOGGER.ELOG(err, exc_info=1)
            raise RuntimeError, err
    UndoCreditEvent=classmethod(UndoCreditEvent)
    
    def PerformCreditEvent( cls, parameters, tasks ):
        cls.ClearCache()
        cls.PARAMS = parameters
        (originalCreditEvent, originalBusinessEvent, mess) = cls.ValidateCreditEvent(tasks)
        if mess:
            return [None, mess]
        creditEventId = cls.PARAMS.At('creditEventId')
        text = 'Started Credit Event Processing for event: %s' % creditEventId
        if cls.PARAMS.At('testmode'):
            text = text + ' (TESTMODE)'
        cls.LOGGER.LOG(text)
        if not originalCreditEvent:
            businessEvent = acm.FBusinessEvent()
            businessEvent.EventType(acm.FEnumeration['enum(BusinessEventType)'].Enumeration('Credit'))
            creditEvent = acm.FCreditEvent()
            creditEvent.BusinessEvent(businessEvent)
            creditEvent.Party(cls.PARAMS.At('issuer'))
            creditEvent.RecordDate(cls.PARAMS.At('defaultDate'))
            creditEvent.RestructuringType(cls.PARAMS.At('restructuring'))
            creditEvent.SeniorityChlItem(cls.PARAMS.At('seniority'))
            creditEvent.Currency(cls.PARAMS.At('currency'))
            creditEvent.UnderlyingCurrency(cls.PARAMS.At('undCurrency'))
            creditEvent.EventType(cls.PARAMS.At('eventType'))
        else:
            businessEvent = cls.GetEntity(originalBusinessEvent)
            creditEvent = cls.GetEntity(originalCreditEvent)
        businessEvent.Status(cls.PARAMS.At('eventStatus'))
        creditEvent.Name(creditEventId)
        creditEvent.SettlementDate(cls.PARAMS.At('settlementDate'))
        creditEvent.AuctioningDate(cls.PARAMS.At('auctioningDate'))
        creditEvent.RecoveryRate( cls.PARAMS.At('recoveryRate') )
        creditEvent.Text1(cls.PARAMS.At('freeText1'))
        creditEvent.Text2(cls.PARAMS.At('freeText2'))
        cls.BeginTransaction()
        try:
            for task in tasks:
                if task.At('type') == 'Singlename CDS':
                    cls.PerformSinglenameCDS(task, businessEvent)
                elif task.At('type') in ['Index CDS', 'Tranche CDS', 'Nth-To-Default CDS']:
                    cls.PerformBasketCDS(task, businessEvent)
            cls.Commit(businessEvent, originalBusinessEvent)
            cls.Commit(creditEvent, originalCreditEvent)
            for link in cls.LINKS:
                cls.Commit(link)
            cls.CommitTransaction()
            if not cls.PARAMS.At('testmode'):
                return [acm.FCreditEvent[creditEventId], None]
            return [None, None]
        except Exception, err:
            cls.AbortTransaction()
            cls.LOGGER.ELOG(err, exc_info=1)
            raise RuntimeError, err
    PerformCreditEvent=classmethod(PerformCreditEvent)
    
    def PerformEntities(cls, task, recovery, accrued, keepAccrued, closeTrade, businessEvent, instrumentFunction):
        createInsLink = True
        if cls.AlreadyClosed(task):
            cls.RemoveTradeTasks(task, instrumentFunction)
        else:
            for tradeTask in task.At('trades'):
                faceNominal = tradeTask.At('nominal')
                position = tradeTask.At('position')

                if closeTrade:
                    # create closing trade
                    createInsLink = False
                    cls.PerformTrade(faceNominal, cls.PARAMS.At('defaultDate'), tradeTask, businessEvent)
                if position:
                    if recovery:
                        # create recovery payment on closing trade
                        createInsLink = False
                        cls.PerformRecoveryPayment( cls.PARAMS.At('settlementDate'), tradeTask, businessEvent )
                    elif tradeTask.At('recoveryPaymentLink'):
                        # delete recovery payment
                        link = tradeTask.At('recoveryPaymentLink')
                        cls.DeleteLinkAndPayment(link)
                        if tradeTask.At('recoveryRebatePaymentLink'):
                            # delete recovery rebate payment since there is no point having a recovery rebate if you do not have a recovery
                            link = tradeTask.At('recoveryRebatePaymentLink')
                            cls.DeleteLinkAndPayment(link)

                    if accrued or (tradeTask.At('recoveryInterestPaymentLink') and keepAccrued):
                        # create payment of type recovery coupon, recovery rebate and recovery interest
                        createInsLink = False
                        cls.PerformCreditCoupons( cls.PARAMS.At('settlementDate'), tradeTask, businessEvent, keepAccrued)
                    else:
                        # delete payments of type recovery coupon, recovery rebate and recovery interest
                        link = tradeTask.At('recoveryCouponPaymentLink')
                        cls.DeleteLinkAndPayment(link)
                        link = tradeTask.At('recoveryInterestPaymentLink')
                        cls.DeleteLinkAndPayment(link)
                        link = tradeTask.At('recoveryRebatePaymentLink')
                        cls.DeleteLinkAndPayment(link)
                if not closeTrade and tradeTask.At('tradeLink'):
                    # delete closing trade
                    link = tradeTask.At('tradeLink')
                    closingTrade  = tradeTask.At('closingTrade')
                    cls.Delete(link)
                    if cls.PARAMS.At('tradeRule') == 'Delete Trades':
                        cls.Delete( closingTrade )
                    else:
                        trade = cls.GetEntity( closingTrade )
                        trade.Status('Void')
                        cls.Commit( trade, closingTrade )
        instrumentFunction(task)
        if createInsLink:
            if not task.At('instrumentLink'):
                intrumentLink = acm.FBusinessEventInstrumentLink()
                intrumentLink.Instrument(task.At('instrument'))
                intrumentLink.BusinessEvent(businessEvent)
                cls.LINKS.Add(intrumentLink)
        elif task.At('instrumentLink'):
            cls.Delete(task.At('instrumentLink'))
    PerformEntities=classmethod(PerformEntities)
    
    def PerformSinglenameCDS( cls, task, businessEvent ):
        instrument = task.At('instrument')
        accruedIncluded = instrument.AccruedIncluded()
        cls.PerformEntities(task, 1.0, accruedIncluded, False, False, businessEvent, cls.PerformCreditEventSpec)
    PerformSinglenameCDS=classmethod(PerformSinglenameCDS)
    
    def PerformBasketCDS( cls, task, businessEvent ):
        instrument = task.At('instrument')
        accruedIncluded = instrument.AccruedIncluded()
        defaultDate=cls.PARAMS.At('defaultDate')
        
        if not instrument.CreditReference().InstrumentMaps(defaultDate).Size() or not cls.GetIssuerMap(instrument.CreditReference()):
            cls.PerformEntities(task, 0.0, 0.0, False, False, businessEvent, cls.PerformCreditEventSpec)
        else:
            if cls.InstrumentIsNthToDefault( instrument ) or task.At('type') == 'Tranche CDS':
                recoveryRate = cls.GetRecoveryRate(task)
                createPayments = cls.CreditPaymentTrigger( instrument, recoveryRate )
            else:
                createPayments = 1
            #closeTrade = instrument.Calculation().CloseCreditBasketTrade(cls.SPACE, cls.PARAMS.At('defaultDate'), cls.GetRecoveryRate(task) * 100.0, cls.PARAMS.At('issuer'))
            cls.PerformEntities(task, createPayments, createPayments and accruedIncluded, task.At('type') == 'Index CDS' and accruedIncluded, False, businessEvent, cls.PerformIndex)
    PerformBasketCDS=classmethod(PerformBasketCDS)
    
    def UpdateTradeStatus( cls, originalTrade ):
        trade = cls.GetEntity( originalTrade )
        tradeStatus = None
        
        if originalTrade.Oid() < 0:
            return
        elif trade.Type() == 'Closing':
            tradeStatus = cls.PARAMS.At('tradeStatusModifyClosing')
        else:
            tradeStatus = cls.PARAMS.At('tradeStatusModifyOther')
             
        if tradeStatus:
            # a payment has been creted / updated, update the trade status of the trade
            trade.Status(tradeStatus)
            cls.Commit( trade, originalTrade )
        return
    UpdateTradeStatus=classmethod(UpdateTradeStatus)
    
    def UseClosingTrade(cls, task):
        return (task.At('type') not in ('Index CDS', 'Tranche CDS', 'Nth-To-Default CDS')) and task.At('closingTrade')
    UseClosingTrade=classmethod(UseClosingTrade)
    
    def PerformRecoveryPayment( cls, settlementDate, task, businessEvent ):
        trade = task.At('trade')
        defaultDate = cls.PARAMS.At('defaultDate')
        if cls.UseClosingTrade(task):
            trade = task.At('closingTrade')
        elif trade.Type() == "Closing":
            trade = trade.Contract()
        
        if task.At('recoveryPaymentLink'):
            paymentLink = None
            originalPayment = task.At('recoveryPaymentLink').Payment()
            payment = cls.GetEntity(originalPayment)
        else:
            originalPayment = None
            (payment, paymentLink) = cls.CreatePayment(trade, trade.Instrument().Currency(), businessEvent)
            #payment.Type('Recovery')
            payment.Type('Allocation Fee') # Ensure no cash impact - 2014 did not include Credit Default amount in cash when CDS reference defaulted.
        recoveryAmount = cls.CalculateRecoveryAmount( trade, cls.GetRecoveryRate(task) )
        payment.Amount( recoveryAmount )
        payment.PayDay(settlementDate)
        payment.ValidFrom(defaultDate)
        cls.Commit(payment, originalPayment)
        if paymentLink:
            cls.LINKS.Add(paymentLink)
        cls.UpdateTradeStatus( trade )
    PerformRecoveryPayment=classmethod(PerformRecoveryPayment)
    
    
    def PerformRecoveryCoupon( cls, trade, defaultDate, settlementDate, task, businessEvent ):
        defaultOrAcquireDate = MaxDate(defaultDate, trade.AcquireDay())
        if trade.Type() == "Closing":
            contractTrade = trade.Contract()
        else:
            contractTrade = trade
        instrument = trade.Instrument()
        instrumentType = CreditEventDialog.GetColumnValue(instrument, 'Credit Event Instrument Type')
    
        # Recovery Coupon
        cashFlow       = cls.GetOngoingCashFlow( instrument, defaultOrAcquireDate )
        legCurrency    = cashFlow.Leg().Currency()
        
        if task.At('recoveryCouponPaymentLink'):
            originalPayment  = task.At('recoveryCouponPaymentLink').Payment()
            payment = cls.GetEntity(originalPayment)
            paymentLink = None
        else:
            if task.At('recoveryInterestPaymentLink'):
                # reuse the Recovery Interest payment
                originalPayment = task.At('recoveryInterestPaymentLink').Payment()
                payment = cls.GetEntity(originalPayment)
                payment.Type('Recovery Coupon')
                if not cls.PARAMS.At('testmode'):
                    task.AtPut('recoveryInterestPaymentLink', None)
                paymentLink = None
            else:
                originalPayment = None
                (payment, paymentLink) = cls.CreatePayment(trade, legCurrency, businessEvent)
                payment.Type('Recovery Coupon')


        recoveryCouponValue = cls.ProjectedBeforeDefault( instrument, contractTrade, cls.PARAMS.At('issuer'), defaultDate)
        
        if task.At('type') in ('Index CDS', 'Tranche CDS'):
            recoveryRate = cls.GetRecoveryRate( task )
            recoveryCouponValueAfter = cls.ProjectedAfterDefault( instrument, contractTrade, cls.PARAMS.At('issuer'), defaultDate, recoveryRate)
            recoveryCouponValue = recoveryCouponValue - recoveryCouponValueAfter

        payment.Amount( recoveryCouponValue )
        payment.PayDay( cashFlow.PayDate() )
        payment.ValidFrom( defaultDate )
        cls.Commit(payment, originalPayment)
        if paymentLink:
            cls.LINKS.Add(paymentLink)

        # Recovery Rebate
        paymentLink = task.At('recoveryRebatePaymentLink')
        if paymentLink:
            originalPayment = paymentLink.Payment()
            payment = cls.GetEntity(originalPayment)
            paymentLink = None
        else:
            originalPayment = None
            if cls.UseClosingTrade(task):
                # single name CDS stores Recovery Rebate payment on closing trade
                (payment, paymentLink) = cls.CreatePayment(trade, legCurrency, businessEvent)
            else:
                # basket CDS stores Recovery Rebate payments on contract trade
                (payment, paymentLink) = cls.CreatePayment( contractTrade, legCurrency, businessEvent )
                
            payment.Type('Recovery Rebate')
            
        if instrumentType == 'Index CDS':
            type, value = cls.AccruedOrRebate( contractTrade, defaultOrAcquireDate, settlementDate )
            amount = value * cls.PartyWeightInIndex(trade.Instrument(), cls.PARAMS.At('issuer'))
        elif instrumentType == 'Tranche CDS':
            recoveryRate = cls.GetRecoveryRate(task)
            type, amount = cls.AccruedOrRebate( contractTrade, defaultOrAcquireDate, settlementDate, recoveryRate )
        else:
            type, amount = cls.AccruedOrRebate( contractTrade, defaultOrAcquireDate, settlementDate )

        payment.Amount( (-1.0) * amount)
        payment.PayDay(settlementDate)
        payment.ValidFrom(defaultDate)
        cls.Commit(payment, originalPayment)
        if paymentLink:
            cls.LINKS.Add(paymentLink)                
        cls.UpdateTradeStatus( trade )
    PerformRecoveryCoupon=classmethod(PerformRecoveryCoupon)
    
    def PerformCreditCoupons( cls, settlementDate, task, businessEvent, keepAccrued ):
        trade = task.At('trade')
        if cls.UseClosingTrade(task):
            trade = task.At('closingTrade')
            
        defaultDate = cls.PARAMS.At('defaultDate')
        if cls.IsSettlementDateAfterNextCoupon( trade.Instrument(), defaultDate, settlementDate ):
            # CREATE / UPDATE recovery coupon payment and recovery rebate payments
            text = "Credit Event Processing of type 'Full Coupon and Rebate'"
            cls.LOGGER.LOG(text)            
            cls.PerformRecoveryCoupon( trade, defaultDate, settlementDate, task, businessEvent)        
        else:
            # CREATE / UPDATE recovery interest payment
            text = "Credit Event Processing of type 'Stub Accrual'"
            cls.LOGGER.LOG(text)            
            cls.PerformRecoveryInterestPayment( settlementDate, task, businessEvent, keepAccrued )        
    PerformCreditCoupons=classmethod(PerformCreditCoupons)
    
    def PerformRecoveryInterestPayment( cls, settlementDate, task, businessEvent, keepAccrued ):
        taskType = task.At('type')
        trade = task.At('trade')
        defaultDate = cls.PARAMS.At('defaultDate')
        if cls.UseClosingTrade(task):
            trade = task.At('closingTrade')  
        
        if task.At('recoveryInterestPaymentLink'):
            paymentLink = None
            originalPayment = task.At('recoveryInterestPaymentLink').Payment()
            payment = cls.GetEntity(originalPayment)
        else:
            originalPayment = None
            (payment, paymentLink) = cls.CreatePayment(trade, trade.Instrument().Currency(), businessEvent)
            payment.Type('Recovery Interest')
        
        defaultDate = MaxDate(cls.PARAMS.At('defaultDate'), trade.AcquireDay())
        recoveryRate = cls.GetRecoveryRate(task)
        type, amount = cls.AccruedOrRebate( trade, defaultDate, settlementDate, recoveryRate )
        if taskType == 'Index CDS':
            amount = amount * cls.PartyWeightInIndex( trade.Instrument(), cls.PARAMS.At('issuer') )
        elif taskType == 'Tranche CDS':
            amount = amount

        if cls.UseClosingTrade(task):
            payment.Amount( -amount )
        else:
            payment.Amount( amount )
            
        payment.PayDay(settlementDate)
        payment.ValidFrom(defaultDate)
        cls.Commit(payment, originalPayment)
        if paymentLink:
            cls.LINKS.Add(paymentLink)                
        cls.UpdateTradeStatus( trade )
    PerformRecoveryInterestPayment=classmethod(PerformRecoveryInterestPayment)
    
    def PerformTrade( cls, faceNominal, acquireDate, task, businessEvent ):
        if not task.At('tradeLink'):
            contractTrade = task.At('trade')
            acquireDate = MaxDate(contractTrade.AcquireDay(), acquireDate)
            if cls.PARAMS.At('testmode'):
                trade = contractTrade.Clone()
                trade.AcquireDay(acquireDate)
                trade.ValueDay(acm.Time.DateNow())
                trade.FaceValue(faceNominal * -1.0)
                trade.TradeTime(acm.Time.TimeNow())
                trade.ContractTrdnbr(contractTrade.Oid())
                trade.OpeningBoTrade(contractTrade.OpeningBoTrade())
                trade.Type('Closing')
                trade.Price(0.0)
                trade.Premium(0.0)
            else:
                trade = acm.TradeActions().CloseTrade(contractTrade, acquireDate, acm.Time.DateNow(), faceNominal * -1.0, 0.0, [])
            trade.Status( cls.PARAMS.At('tradeStatusClosing') )
            tradeLink = acm.FBusinessEventTradeLink()
            tradeLink.Trade(contractTrade)
            tradeLink.BusinessEvent(businessEvent)
            tradeLink.TradeEventType('New')
            cls.Commit(trade)
            cls.LINKS.Add(tradeLink)
            task.AtPut('closingTrade', trade)
    PerformTrade=classmethod(PerformTrade)
    
    def PerformCreditEventSpec( cls, task, undo=False ):
        instrument = task.At('instrument')
        originalSpec = instrument.CreditEventSpec()
        spec = cls.GetEntity(originalSpec)
        
        if undo:
            spec.RecoveryRate(0.0)
            spec.DefaultDate(None)
            spec.AuctioningDate(None)
            spec.SettlementDate(None)
        else:
            spec.DefaultDate(cls.PARAMS.At('defaultDate'))
            spec.AuctioningDate(cls.PARAMS.At('auctioningDate'))
            if spec.AuctioningDate():
                cdsLeg = instrument.FirstCreditDefaultLeg()
                if cdsLeg.Digital(): 
                    spec.RecoveryRate(100.0 - cdsLeg.DigitalPayoff())
                else:
                    spec.RecoveryRate(cls.PARAMS.At('recoveryRate') * 100)
                spec.SettlementDate(cls.PARAMS.At('settlementDate'))
            else:
                spec.SettlementDate( None )
                spec.RecoveryRate( 0.0 )
            
        cls.Commit(spec, originalSpec)
    PerformCreditEventSpec=classmethod(PerformCreditEventSpec)
    
    def PerformIndex( cls, task, undo=False ):
        instrument = task.At('instrument')
        if not cls.PERFORMED_INDICES.HasKey(instrument.CreditReference()):
            originalMap = cls.GetIssuerMap(instrument.CreditReference())
            map = cls.GetEntity(originalMap)
            if map:
                if undo:
                    map.RecoveryRate(0.0)
                    map.DefaultDate(None)
                    map.AuctioningDate(None)
                    map.SettlementDate(None)
                else:
                    map.DefaultDate(cls.PARAMS.At('defaultDate'))
                    map.AuctioningDate(cls.PARAMS.At('auctioningDate'))
                    if map.AuctioningDate():
                        map.SettlementDate(cls.PARAMS.At('settlementDate'))
                        map.RecoveryRate(cls.PARAMS.At('recoveryRate') * 100.0)
                    else:
                        map.SettlementDate( None)
                        map.RecoveryRate( 0.0 )
                cls.Commit(map, originalMap)
                cls.PERFORMED_INDICES.AtPut(instrument.CreditReference(), None)
            else:
                text = "WARNING: instrument %s with credit reference %s was NOT performed." % ( instrument.Name(), instrument.CreditReference().Name() )
                cls.LOGGER.LOG(text)
    PerformIndex=classmethod(PerformIndex)
    
    def PerformInstrument( cls, task, undo=False ):
        originalInstrument = task.At('instrument')
        instrument = cls.GetEntity(originalInstrument)
        if undo:
            instrument.Incomplete('None')
        else:
            instrument.Incomplete('Defaulted')
        cls.Commit(instrument, originalInstrument)
    PerformInstrument=classmethod(PerformInstrument)
    
    def ClearCache( cls ):
        cls.PERFORMED_INDICES.Clear()
        cls.ISSUER_MAPS.Clear()
        cls.CREDIT_EVENTS.Clear()
        cls.EVENT_INSTRUMENTS.Clear()
        cls.LINKS.Clear()
    ClearCache=classmethod(ClearCache)
    
    """------------------ Help Methods ------------------"""
    
    def AlreadyClosed( cls, task ):
        alreadyClosed = True
        for tradeTask in task.At('trades'):
            trade = tradeTask.At('trade')
            defaultOrAcquireDate = MaxDate(cls.PARAMS.At('defaultDate'), trade.AcquireDay())
            
            tradeLink = tradeTask.At('tradeLink')
            remainingQuantityAtDefaultDate = acm.TradeActionUtil().RemainingQuantityAtDate(trade, defaultOrAcquireDate, True)
            remainingQuantityIsZeroAtDefaultDate = acm.Math.AlmostZero(remainingQuantityAtDefaultDate, 1e-10)
            
            alreadyClosed = (not tradeLink and     remainingQuantityIsZeroAtDefaultDate) or\
                            (    tradeLink and not remainingQuantityIsZeroAtDefaultDate)
            
            if not alreadyClosed:
                break
        
        return alreadyClosed
    AlreadyClosed=classmethod(AlreadyClosed)
    
    def RemoveTradeTasks( cls, task, instrumentFunction ):
        for tradeTask in task.At('trades'):
            if tradeTask.At('recoveryPaymentLink'):
                link = tradeTask.At('recoveryPaymentLink')
                payment = link.Payment()
                cls.Delete(link)
                cls.Delete(payment)
            if tradeTask.At('recoveryInterestPaymentLink'):
                link = tradeTask.At('recoveryInterestPaymentLink')
                payment = link.Payment()
                cls.Delete(link)
                cls.Delete(payment)
            if tradeTask.At('recoveryRebatePaymentLink'):
                link = tradeTask.At('recoveryRebatePaymentLink')
                payment = link.Payment()
                cls.Delete(link)
                cls.Delete(payment)
            if tradeTask.At('recoveryCouponPaymentLink'):
                link = tradeTask.At('recoveryCouponPaymentLink')
                payment = link.Payment()
                cls.Delete(link)
                cls.Delete(payment)
            if tradeTask.At('tradeLink'):
                link = tradeTask.At('tradeLink')
                contractTrade = link.Trade()
                closingTrade = CreditEventDialog.GetClosingTrade( contractTrade )
                cls.Delete(link)
                if cls.PARAMS.At('tradeRule') == 'Delete Trades':
                    cls.Delete(closingTrade)
                else:
                    trade = cls.GetEntity(closingTrade)
                    trade.Status('Void')
                    cls.Commit(trade, closingTrade)
    RemoveTradeTasks=classmethod(RemoveTradeTasks)
    
    def GetBasketMap( cls ):
        basketMap = acm.FDictionary()
        for instrument in cls.PARAMS.At('allInstruments'):
            if instrument.IsCreditBasket():
                ref = instrument.CreditReference()
                if not basketMap.HasKey(ref):
                    basketMap.AtPut(ref, acm.FArray())
                basketMap.At(ref).Add(instrument)
        return basketMap
    GetBasketMap=classmethod(GetBasketMap)
    
    def CheckBasketDays( cls, toProcess, basketMap ):
        ins = {}
        insEvents = {}
        insSameDay = {}
        insSameDayEvents = {}
        for instrument in toProcess:
            if instrument.IsCreditBasket():
                ref = instrument.CreditReference()
                maps = []
                mapsSameDay = []
                for map in ref.InstrumentMaps(cls.PARAMS.At('defaultDate')):
                    if map.DefaultDate() > cls.PARAMS.At('defaultDate'):
                        event = cls.CreditEventFromInstrumentMap(map)
                        if event:
                            eventName = event.Name()
                            insEvents[eventName] = None
                        else:
                            eventName = '?'
                        maps.append('%s [Event: %s]' % (map.Instrument().Name(), eventName))
                    if not map.Instrument().IsIssuerSensitive(cls.PARAMS.At('issuer'), cls.PARAMS.At('defaultDate')) and map.DefaultDate() == cls.PARAMS.At('defaultDate'):
                        event = cls.CreditEventFromInstrumentMap(map)
                        if event:
                            eventName = event.Name()
                            insSameDayEvents[eventName] = None
                        else:
                            eventName = '?'
                        mapsSameDay.append('%s [Event: %s]' % (map.Instrument().Name(), eventName))
                if maps:
                    ins['Index: %s, Constituents: (%s), Instruments: (%s)' % (ref.Name(), ','.join(maps), ','.join([instr.Name() for instr in basketMap.At(ref)]))] = None
                if mapsSameDay:
                    insSameDay['Index: %s, Constituents: (%s), Instruments: (%s)' % (ref.Name(), ','.join(mapsSameDay), ','.join([instr.Name() for instr in basketMap.At(ref)]))] = None
        return (ins.keys(), insEvents.keys(), insSameDay.keys(), insSameDayEvents.keys())
    CheckBasketDays=classmethod(CheckBasketDays)
    
    def GetIssuerMap( cls, index ):
        if not cls.ISSUER_MAPS.HasKey(index):
            issuerMap = None
            for map in index.InstrumentMaps():
                if map.Instrument().IsIssuerSensitive(cls.PARAMS.At('issuer'), cls.PARAMS.At('defaultDate')):
                    issuerMap = map
                    break
            cls.ISSUER_MAPS.AtPut(index, issuerMap)
            if not issuerMap:
                text = "WARNING: instrument %s is not sensitive to issuer %s." % ( index.Name(), cls.PARAMS.At('issuer').Name() )
                cls.LOGGER.LOG(text)
            return issuerMap
        return cls.ISSUER_MAPS.At(index)
    GetIssuerMap=classmethod(GetIssuerMap)

    def CreatePayment( cls, trade, currencySymbol, businessEvent ):
        payment = acm.FPayment()
        payment.Trade(trade)
        payment.Party(trade.Counterparty())
        payment.Currency(currencySymbol)
        paymentLink = acm.FBusinessEventPaymentLink()
        paymentLink.Payment(payment)
        paymentLink.BusinessEvent(businessEvent)
        return (payment, paymentLink)
    CreatePayment=classmethod(CreatePayment)
    
    def CreditEventFromInstrumentMap( cls, map ):
        if not cls.CREDIT_EVENTS.HasKey(map):
            event = None
            date = map.DefaultDate()
            ref = map.Combination()
            instrument = map.Instrument()
            creditEvents = acm.FCreditEvent.Instances()
            for creditEvent in creditEvents:
                businessEvent = creditEvent.BusinessEvent()
                if businessEvent:
                    if creditEvent.RecordDate() == date:
                        if instrument.IsIssuerSensitive(creditEvent.Party(), creditEvent.RecordDate()):
                            eventInstruments = cls.InstrumentsFromEvent(businessEvent)
                            for eventInstrument in eventInstruments:
                                if eventInstrument.IsCreditBasket():
                                    if eventInstrument.CreditReference().IsEqual(ref):
                                        event = creditEvent
                                        break
                            if event:
                                break
            cls.CREDIT_EVENTS.AtPut(map, event)
            return event
        return cls.CREDIT_EVENTS.At(map)
    CreditEventFromInstrumentMap=classmethod(CreditEventFromInstrumentMap)
    
    def InstrumentsFromEvent( cls, businessEvent ):
        if not cls.EVENT_INSTRUMENTS.HasKey(businessEvent):
            instruments = acm.FDictionary()
            for link in businessEvent.InstrumentLinks():
                instrument = link.Instrument()
                if not instruments.HasKey(instrument):
                    instruments.AtPut(instrument, None)
            for link in businessEvent.TradeLinks():
                instrument = link.Trade().Instrument()
                if not instruments.HasKey(instrument):
                    instruments.AtPut(instrument, None)
            for link in businessEvent.PaymentLinks():
                instrument = link.Payment().Trade().Instrument()
                if not instruments.HasKey(instrument):
                    instruments.AtPut(instrument, None)
            insArray = instruments.Keys()
            cls.EVENT_INSTRUMENTS.AtPut(businessEvent, insArray)
            return insArray
        return cls.EVENT_INSTRUMENTS.At(businessEvent)
    InstrumentsFromEvent=classmethod(InstrumentsFromEvent)
    
    def GetOngoingCashFlow(cls, ins, defaultDate):
        cashFlow = None
        for leg in ins.Legs():
            if leg.LegType() == "Fixed":
                for cf in leg.CashFlows():
                    if cf.StartDate() < defaultDate and defaultDate <= cf.EndDate():
                        cashFlow = cf
                        break
        if not cashFlow:
            text = "GetOngoingCashFlow: No ongoing cashflow found for instrument %s on default date %s" % (ins.Name(), defaultDate)
            cls.LOGGER.WLOG(text)
        return cashFlow
    GetOngoingCashFlow=classmethod(GetOngoingCashFlow)

    def IsSettlementDateAfterNextCoupon(cls, ins, defaultDate, settlementDate):
        cashFlow = cls.GetOngoingCashFlow(ins, defaultDate)
        if cashFlow and cashFlow.PayDate() < settlementDate:
            return 1
        else:
            return 0
    IsSettlementDateAfterNextCoupon=classmethod(IsSettlementDateAfterNextCoupon)
        
    def CashflowData( cls, trade, defaultDate, recoveryRate ):
        noDays     = 0
        cfLength   = 1.0
        projected  = 0.0
        payDate    = None
        instrument = trade.Instrument()
        instrumentType = CreditEventDialog.GetColumnValue(instrument, 'Credit Event Instrument Type')
        for leg in instrument.Legs():
            if leg.LegType() == "Fixed":
                for cf in leg.CashFlows():
                    if cf.StartDate() < defaultDate and defaultDate <= cf.EndDate():
                        noDays    = acm.Time().DateDifference( defaultDate, cf.StartDate() )
                        cfLength  = acm.Time().DateDifference( cf.EndDate(), cf.StartDate() )
                        projected = cls.ProjectedBeforeDefault(instrument, trade, cls.PARAMS.At('issuer'), defaultDate)
                        if instrumentType == "Tranche CDS":
                            projectedAfter = cls.ProjectedAfterDefault( instrument, trade, cls.PARAMS.At('issuer'), defaultDate, recoveryRate)
                            projected = projected - projectedAfter
                        payDate   = cf.PayDate()
        if not payDate:
            text = "CashflowData: No ongoing cashflow found for trade %s on default date %s" % (trade.Oid(), defaultDate)
            cls.LOGGER.WLOG(text)
        return ( float(noDays), float(cfLength), projected, payDate )
    CashflowData=classmethod(CashflowData)

    def InstrumentIsNthToDefault( cls, instrument ):
        instrumentType = CreditEventDialog.GetColumnValue(instrument, 'Credit Event Instrument Type')
        return ( instrumentType == 'Nth-To-Default CDS' )
    InstrumentIsNthToDefault=classmethod( InstrumentIsNthToDefault )
    
    def CreditPaymentTrigger(cls, cds, recoveryRate):
        instrumentType = CreditEventDialog.GetColumnValue(cds, 'Credit Event Instrument Type')    
        
        if instrumentType == 'Nth-To-Default CDS':
            # return true if the trigger point has been hit
            num       = 0
            creditLeg = cds.FirstCreditDefaultLeg()
            creditRef = creditLeg.CreditRef()
            issuer    = cls.PARAMS.At('issuer')
            defaultDate = cls.PARAMS.At('defaultDate')
            for link in creditRef.InstrumentMaps(defaultDate):
                if link.Instrument().Issuer().Oid() == issuer.Oid():
                    num += 1
                elif link.DefaultDate():
                    num += 1
            return ( num >= creditLeg.ExoticNumber() )
        elif instrumentType == 'Tranche CDS':
            return cls.TrancheImpact(cds, recoveryRate) > 0.0
            
    CreditPaymentTrigger=classmethod(CreditPaymentTrigger)    

    def CalculateRecoveryAmount(cls, trade, recoveryRate):
        recovery       = acm.DenominatedValue( 0.0, None, None )
        if trade.Type() == "Closing":
            trade = trade.Contract()
        instrument     = trade.Instrument()
        instrumentType = CreditEventDialog.GetColumnValue(instrument, 'Credit Event Instrument Type')
        creditLeg      = instrument.FirstCreditDefaultLeg()
        factor         = -1.0 if creditLeg.PayLeg() else 1.0
        nominal  = instrument.NominalAmount() * trade.Quantity()
        
        if instrumentType == 'Nth-To-Default CDS':
            if cls.CreditPaymentTrigger(instrument, recoveryRate):
                if creditLeg.Digital():
                    recovery = nominal * (creditLeg.DigitalPayoff() / 100.0) * factor
                else:
                    recovery = nominal * (1.0 - recoveryRate) * factor
        elif instrumentType == 'Tranche CDS':
            settlementDate = acm.Time.FromDate(cls.PARAMS.At('settlementDate'))
            trancheImpact = cls.TrancheImpact(instrument, recoveryRate)
            recovery = nominal * trancheImpact * factor
        else:
            issuer = cls.PARAMS.At('issuer')
            if instrumentType in ['Index CDS', 'Tranche CDS', 'Nth-To-Default CDS']:
                weight = cls.PartyWeightInIndex(instrument, issuer, True)
            else:
                weight = 1.0
        
            if creditLeg.Digital():
                recovery = weight * nominal * ( creditLeg.DigitalPayoff() / 100.0 ) * factor
            else:
                recovery = weight * nominal * ( 1.0 - recoveryRate ) * factor
        return recovery
    CalculateRecoveryAmount=classmethod(CalculateRecoveryAmount)

    def AccruedOrRebate( cls, trade, defaultDate, settlementDate, recoveryRate = 0.0 ):
        # recoveryRate is required for Tranche CDS
        amount = 0.0
        type = None # accrual / rebate
        instrument        = trade.Instrument()
        leg               = cls.GetNonCreditLeg(instrument)
        calendar          = instrument.Currency().Calendar()
        
        if cls.IsSettlementDateAfterNextCoupon( instrument, defaultDate, settlementDate):
            # full coupon and rebate
            type = 'rebate'
            endDate = instrument.Legs()[0].EndDate()
            noDays, cfLength, projected, payDate = cls.CashflowData( trade, defaultDate, recoveryRate )
            rebateDays = 0
            
            # payment date on a banking date AND trade does not mature
            if not calendar.CalendarInformation().IsNonBankingDay( payDate ) and endDate != settlementDate:
                # Rebate accrues from and including: Day after Common Event Determination Date 
                # Rebate accrues to: To but excluding Affected Payment Date 
                rebateDays = cfLength - noDays - 1.0
                
            # payment date on a banking date AND trade does mature
            elif not calendar.CalendarInformation().IsNonBankingDay( payDate ) and endDate == settlementDate:
                # Rebate accrues from and including: Day after Common Event Determination Date 
                # Rebate accrues to: To and including Affected Payment Date 
                rebateDays = cfLength - noDays
                
            # payment date on a non banking date AND trade does not mature
            elif calendar.CalendarInformation().IsNonBankingDay( payDate ) and endDate != settlementDate:
                adjustedPayDate = calendar.ModifyDate(None, None, payDate)
                adjustedDays = acm.Time().DateDifference(adjustedPayDate, payDate)
                
                # Rebate accrues from and including: Day after Common Event Determination Date 
                # Rebate accrues to: To but excluding ADJUSTED Affected Payment Date 
                rebateDays = cfLength - noDays + adjustedDays - 1.0
                
            # payment date on a non banking date AND trade does mature
            elif calendar.CalendarInformation().IsNonBankingDay( payDate ) and endDate == settlementDate:                
                # Rebate accrues from and including: Day after Common Event Determination Date 
                # Rebate accrues to: To and including NON-ADJUSTED Affected Payment Date 
                rebateDays = cfLength - noDays
                
            else:
                text = "ERROR in AccruedOrRebate trdnbr %i, payDate %s, endDate %s, defaultDate %s, settlementDate %s" % (trade.Oid(), payDate, endDate, defaultDate, settlementDate)
                cls.LOGGER.LOG( text )
                
            amount = projected * (rebateDays / cfLength)
            amount = 0 #specific to repair of ABL CDSs
        
        else:
            # stub accrual
            type = 'accrued'
            noDays, cfLength, projected, payDate = cls.CashflowData( trade, defaultDate, recoveryRate )
            amount = projected * ( (noDays + 1.0) / cfLength )

        # type of payment, amount
        return type, amount   
    AccruedOrRebate=classmethod(AccruedOrRebate)
        
    def TotalLosses(cls, cds, excludeParty=None):
        sum = 0.0
        underlying = cds.Underlying()
        cdsLeg = cds.FirstCreditDefaultLeg()
        if underlying and underlying.IsKindOf(acm.FCombination):
            defaultDate = cls.PARAMS.At('defaultDate')
            sumOfWeight = 0.0
            for link in underlying.InstrumentMaps(defaultDate):
                sumOfWeight = sumOfWeight + link.Weight()
            for link in underlying.InstrumentMaps(defaultDate):
                if link.DefaultDate():
                    if not excludeParty or excludeParty.Oid() != link.Instrument().Issuer().Oid():
                        if cls.IsCdsDigital( cds ):
                            recoveryRate = ( 100.0 - cdsLeg.DigitalPayoff() )
                        else:
                            recoveryRate = link.RecoveryRate()
                        sum = sum + (link.Weight() / sumOfWeight) * (1 - recoveryRate / 100.0)
        if sum != 0.0:
            return sum * cds.NominalAmount()
        else:
            if cdsLeg.CashFlows().Size():
                return cds.NominalAmount() * (1 - cdsLeg.CashFlows().First().NominalFactor());
            else:
                return 0.0
    TotalLosses=classmethod(TotalLosses)
        
    def TrancheLossRatio(cls, cds, loss):
        lower = cds.AttachmentPoint() / 100.0
        upper = cds.DetachmentPoint() / 100.0
        cdsLoss = loss / cds.NominalAmount()
        trancheSize = upper - lower
        trancheLoss = max(cdsLoss - lower, 0.0)
        return min(trancheLoss / trancheSize, 1.0)
    TrancheLossRatio=classmethod(TrancheLossRatio)

    def TrancheImpact(cls, cds, recoveryRate):
        issuer = cls.PARAMS.At('issuer')
        weight = cls.PartyWeightInIndex(cds, issuer, True)
        oldLoss = cls.TotalLosses(cds, issuer)
        loss = weight * cds.NominalAmount() * ( 1.0 - recoveryRate )
        return cls.TrancheLossRatio(cds, oldLoss + loss) - cls.TrancheLossRatio(cds, oldLoss)
    TrancheImpact=classmethod(TrancheImpact)

    def PartyWeightInIndex( cls, cds, party, includeDefaulted = False ):
        weight = 0.0
        sumOfWeight = 0.0
        underlying = cds.Underlying()
        if underlying and underlying.IsKindOf(acm.FCombination):
            defaultDate = cls.PARAMS.At('defaultDate')
            for link in underlying.InstrumentMaps(defaultDate):
                if not link.Instrument().Issuer():
                    text = "PartyWeightInIndex: CDS %s, underlying instrument %s missing issuer." %(cds.Name(), link.Instrument().Name())
                    cls.LOGGER.WLOG(text)
                elif link.Instrument().Issuer().Oid() == party.Oid():
                    weight += link.Weight()
                    sumOfWeight += link.Weight()
                elif not link.DefaultDate() and not includeDefaulted:
                    sumOfWeight += link.Weight()
                elif includeDefaulted:
                    sumOfWeight += link.Weight()
                    
            weight = weight / sumOfWeight
        return weight
    PartyWeightInIndex=classmethod(PartyWeightInIndex)
    
    def DeleteLinkAndPayment(cls, link):
        if link:
            payment = link.Payment()
            cls.Delete(link)
            cls.Delete(payment)
    DeleteLinkAndPayment=classmethod(DeleteLinkAndPayment)
    
    def GetRecoveryRate(cls, task):

        def InstrumentFromTask(task):
            instrument = task.At('instrument')
            if not instrument:
                trade = task.At('trade')
                if not trade:
                    trade = task.At('closingTrade')
                instrument = trade.Instrument()
            return instrument
        
        def IsBasketCDS(instrument):
            return instrument.CreditReference() and instrument.CreditReference().Class().IncludesBehavior(acm.FCombination)
        
        def MatchYCAttribute(ins, mcl, issuer, seniority, currency, refCurrency, restructuring):
            cref = ins.CreditReference()
            ycc = mcl.Link().YieldCurveComponent()
            # Enum as string
            restructuringEnum = acm.FEnumeration['enum(RestructuringType)']
            restructuringType = restructuringEnum.Enumerator(restructuring)
            
            if (ycc.Class() == acm.FYCAttribute) and \
               (ycc.Issuer() == issuer) and \
               (ycc.SeniorityChlItem() == seniority or seniority is None) and \
               (cref.Currency() == refCurrency or refCurrency is None) and \
               (ins.Restructuring() == restructuringType or restructuringType == 'None') and \
               (ins.Currency() == currency or currency is None): 
                return ycc
            else:
                return None
        
        def FindMappedYCAttribute(ins, issuer, seniority, currency, refCurrency, restructuring, defaultDate):
            if IsBasketCDS(ins):
                for mcl in ins.MappedCreditLinks(True, defaultDate):
                    ycattr = MatchYCAttribute(ins, mcl, issuer, seniority, currency, refCurrency, restructuring)
                    if ycattr:
                        return ycattr
                return None
            else:
                mcl = ins.MappedCreditLink()
                return MatchYCAttribute(ins, mcl, issuer, seniority, currency, refCurrency, restructuring)
    
        recoveryRate   = cls.PARAMS.At('recoveryRate')
        auctioningDate = cls.PARAMS.At('auctioningDate')
        issuer         = cls.PARAMS.At('issuer')
        seniority      = cls.PARAMS.At('seniority')
        currency       = cls.PARAMS.At('currency')
        refCurrency    = cls.PARAMS.At('referenceCurrency')
        restructuring  = cls.PARAMS.At('restructuring')
        defaultDate    = cls.PARAMS.At('defaultDate')


        instrument = InstrumentFromTask(task)                
        cdsLeg = instrument.FirstCreditDefaultLeg()
        
        if cdsLeg and cdsLeg.Digital():
            recoveryRate = ( 1.0 - cdsLeg.DigitalPayoff() / 100.0 )
        elif not auctioningDate:
            mappedYCAttribute = FindMappedYCAttribute(instrument, issuer, seniority, currency, refCurrency, restructuring, defaultDate)
            if mappedYCAttribute:
                recoveryRate = mappedYCAttribute.RecoveryRate() / 100.0
            else:
                text = 'Unique credit curve row matching the defaulted Credit was not found, 100 percent used as estimated Recovery Rate.'
                cls.LOGGER.LOG(text)
                recoveryRate = 1.0
        return recoveryRate
    GetRecoveryRate=classmethod(GetRecoveryRate)

    def GetNonCreditLeg(cls, instrument):
        if instrument.InsType() == 'CreditDefaultSwap':
            for leg in instrument.Legs():
                if leg.LegType() in ("Fixed", "Float"):
                    return leg
        return None    
    GetNonCreditLeg=classmethod(GetNonCreditLeg)
    
    def ProjectedBeforeDefault( cls, cds, trade, party, defaultDate ):
        projected = 0.0

        if cds.Underlying() and cds.Underlying().IsKindOf(acm.FCombination):
            # basket CDS
            cdsClone = cds.Clone()
            cdsClone.RegisterInStorage()

            creditIndex = cdsClone.Underlying()
            creditIndexClone = creditIndex.Clone()
            creditIndexClone.RegisterInStorage()
            
            cashFlow = cls.GetOngoingCashFlow(cdsClone, defaultDate)
        
            for leg in cdsClone.Legs():
                leg.CreditRef(creditIndexClone)
        
            for link in creditIndexClone.InstrumentMaps(defaultDate):
                if link.Instrument().Issuer().Oid() == party.Oid():
                    link.DefaultDate( None )
                    projected = cashFlow.Calculation().Projected(cls.SPACE, trade).Number()
        else:
            # single name CDS
            cdsClone = cds.StorageImage()
            cdsClone.CreditEventSpec().DefaultDate(None)
            cashFlow  = cls.GetOngoingCashFlow(cdsClone, defaultDate)
            projected = cashFlow.Calculation().Projected(cls.SPACE, trade).Number()
        return projected
    ProjectedBeforeDefault=classmethod(ProjectedBeforeDefault)

    def ProjectedAfterDefault( cls, cds, trade, party, defaultDate, recoveryRate ):
        projected = 0.0

        if cds.Underlying() and cds.Underlying().IsKindOf(acm.FCombination):
            #basket cds
            cdsClone = cds.Clone()
            cdsClone.RegisterInStorage()

            creditIndex = cdsClone.Underlying()
            creditIndexClone = creditIndex.Clone()
            creditIndexClone.RegisterInStorage()
            
            cashFlow = cls.GetOngoingCashFlow(cdsClone, defaultDate)
        
            for leg in cdsClone.Legs():
                leg.CreditRef(creditIndexClone)
        
            for link in creditIndexClone.InstrumentMaps(defaultDate):
                if link.Instrument().Issuer().Oid() == party.Oid():
                    link.DefaultDate( defaultDate )
                    link.RecoveryRate( recoveryRate * 100.0)
                    projected = cashFlow.Calculation().Projected(cls.SPACE, trade).Number()
        else:
            # single name CDS
            cashFlow  = cls.GetOngoingCashFlow(cds, defaultDate)
            projected = cashFlow.Calculation().Projected(cls.SPACE, trade).Number()
        return projected
    ProjectedAfterDefault=classmethod(ProjectedAfterDefault)
    
    def IsCdsDigital( cls, entity ):
        returnValue = False
        instrument  = None
        if entity and entity.IsKindOf( acm.FInstrument ):
            instrument = entity
        elif entity and entity.IsKindOf( acm.FTrade ):
            instrument = entity.Instrument()

        if instrument:
            creditLeg = instrument.FirstCreditDefaultLeg()
            if creditLeg and creditLeg.Digital():
                returnValue = True
        
        return returnValue
    IsCdsDigital=classmethod(IsCdsDigital)

class CreditEventDialog( FUxCore.LayoutDialog ):
    
    LOGGER = FLogger.FLogger( 'CREDIT EVENT' )
    
    SENIORITY = acm.FDictionary()
    [SENIORITY.AtPut(c.Name(), c) for c in acm.FChoiceList.Select('name="Seniority" list="MASTER"')[0].Choices()]
    SENIORITY.AtPut('', None)
    
    TRADE_RULES = acm.FArray()
    [TRADE_RULES.Add(rule) for rule in ['Void Trades', 'Delete Trades']]
    
    STATUSES = acm.FArray()
    [STATUSES.Add(rule) for rule in acm.FEnumeration['enum(BusinessEventStatus)'].Values() if not rule == 'None']
    
    TRADE_STATUSES_CLOSING = acm.FArray()
    [TRADE_STATUSES_CLOSING.Add(status) for status in acm.FEnumeration['enum(TradeStatus)'].Values() if not status in CreditEventParameters.TRADE_STATUSES_CLOSING_EXCLUDE]

    TRADE_STATUSES_MODIFY_CLOSING = acm.FArray()
    [TRADE_STATUSES_MODIFY_CLOSING.Add(status) for status in acm.FEnumeration['enum(TradeStatus)'].Values() if not status in CreditEventParameters.TRADE_STATUSES_MODIFY_CLOSING_EXCLUDE]
    TRADE_STATUSES_MODIFY_CLOSING.Add("No Change")
    
    TRADE_STATUSES_MODIFY_OTHER = acm.FArray()
    [TRADE_STATUSES_MODIFY_OTHER.Add(status) for status in acm.FEnumeration['enum(TradeStatus)'].Values() if not status in CreditEventParameters.TRADE_STATUSES_MODIFY_OTHER_EXCLUDE]
    TRADE_STATUSES_MODIFY_OTHER.Add("No Change")

    TYPE_TO_CLASS = CreditEventParameters.InsTypeToClass()

    CLASS_TO_TYPE = CreditEventParameters.ClassToInsType()
    
    SPACE = acm.Calculations().CreateCalculationSpace(acm.GetDefaultContext(), 'FDealSheet')
    
    def __init__( self, dataDict ):
        CreditEventDialog.LOGGER.Reinitialize( level=1, keep=False, logOnce=False, logToConsole=False, logToPrime=True, logToFileAtSpecifiedPath=None, filters=None )
        self.m_creditEventIdCtrl = None
        self.m_issuerCtrl = None
        self.m_settlementDateCtrl = None
        self.m_defaultDateCtrl = None
        self.m_auctioningDateCtrl = None
        self.m_filterCtrl = None
        self.m_recoveryRateCtrl = None
        self.m_seniorityCtrl = None
        self.m_eventTypeCtrl = None
        self.m_currencyCtrl = None
        self.m_undCurrencyCtrl = None
        self.m_restructuringCtrl = None
        self.m_eventStatusCtrl = None
        self.m_tradeStatusClosingCtrl = None
        self.m_tradeStatusModifyClosingCtrl = None
        self.m_tradeStatusModifyOtherCtrl = None
        self.m_tradeRuleCtrl = None
        self.m_freeText1Ctrl = None
        self.m_freeText2Ctrl = None
        self.m_bankruptcyBox = None
        self.m_failureToPayBox = None
        self.m_obligDefaultBox = None
        self.m_obligAccelBox = None
        self.m_repudiationBox = None
        self.m_govInterventionBox = None
        self.m_useFilterBox = None
        self.m_useFilterPanel = None
        self.m_instrumentTypeCtrl = None
        self.m_toggleAllBox = None
        self.m_testmodeBox = None
        self.m_instrumentSheetCtrl = None
        self.m_tradeSheetCtrl = None
        self.m_openBtn = None
        self.m_newBtn = None
        self.m_showDetailsBox = None
        self.m_undoBtn = None
        self.m_runBtn = None
        self.m_closeBtn = None
        self.m_creditEvent = None
        self.m_creditEventId = None
        self.m_justPerformed = None
        self.m_testmode = False
        self.m_eventStatus = 1
        self.m_tradeStatusClosing = CreditEventParameters.TradeStatusClosingDefault()
        self.m_tradeStatusModifyClosing = CreditEventParameters.TradeStatusModifyClosingDefault()
        self.m_tradeStatusModifyOther = CreditEventParameters.TradeStatusModifyOtherDefault()
        self.m_useFilter = False
        self.m_updateUseFilterToggle = True
        self.m_allInstruments = acm.FArray()
        self.m_filteredInstruments = acm.FArray()
        self.m_settlementDate = acm.Time.DateValueDay()
        self.m_defaultDate = acm.Time.DateValueDay()
        self.m_auctioningDate = None
        self.m_recoveryRate = 0.0
        self.m_eventType = 0
        self.m_freeText1 = None
        self.m_freeText2 = None
        self.m_tasks = acm.FDictionary()
        self.m_parameters = acm.FDictionary()
        self.m_tradeRule = 'Delete Trades'
        if dataDict:
            self.m_issuer = dataDict.At('issuer')
            self.m_seniority = dataDict.At('seniority')
            self.m_currency = dataDict.At('currency')
            self.m_undCurrency = dataDict.At('undCurrency')
            self.m_instrumentType = dataDict.At('type')
            self.m_restructuring = dataDict.At('restructuring')
            self.m_bankruptcy = dataDict.At('bankruptcy')
            self.m_failureToPay = dataDict.At('failureToPay')
            self.m_obligDefault = dataDict.At('obligDefault')
            self.m_obligAccel = dataDict.At('obligAccel')
            self.m_repudiation = dataDict.At('repudiation')
            self.m_govIntervention = dataDict.At('govIntervention')
        else:
            self.m_issuer = None
            self.m_seniority = None
            self.m_currency = None
            self.m_undCurrency = None
            self.m_instrumentType = acm.FCreditDefaultSwap
            self.m_restructuring = 0
            self.m_bankruptcy = False
            self.m_failureToPay = False
            self.m_obligDefault = False
            self.m_obligAccel = False
            self.m_repudiation = False
            self.m_govIntervention = False
        self.m_layout = None
        self.m_bindings = None
        self.m_fuxDlg = None
        self.m_tradeMap = acm.FDictionary()
        self.m_updateSheet = False
        self.m_updateProcess = False
        self.m_showPhysicalNotSupported = False
        self.m_dependents = acm.FArray()
        self.m_filterInstruments = False
        self.m_initInstruments = True
        self.m_statusFilter = set()
        self.m_includeTradeless = False

        domain = acm.GetDomain('enum(TradeStatus)')
        # dont filter any trade statuses by default
        for e in domain.Elements():
            if e not in ('Simulated', 'Void', 'Confirmed Void', 'Terminated'):
                self.m_statusFilter.add(e)
        
        # used for non gui runs
        self.InitControls()
    
    """------------------ Processing ------------------"""
    
    def PerformCreditEvent( self, fUxDlg, instrument ):
        self.m_fuxDlg = fUxDlg
        try:
            self.StoreParameters()
            self.PrepareTasks(instrument)
            result = CreditEventHandler.PerformCreditEvent(self.m_parameters, self.m_tasks.Values())
        except Exception, err:
            CreditEventDialog.LOGGER.ELOG('Error while performing Credit Event Processing.', exc_info=1)
            return
        if result[1] and type(result[1]) == type(''):
            acm.UX().Dialogs().MessageBoxInformation(self.m_fuxDlg.Shell(), result[1])
    
    def UndoCreditEvent( self ):
        if self.m_testmode or acm.UX().Dialogs().MessageBoxOKCancel(self.m_fuxDlg.Shell(), 3, 'Are you sure you want to undo this Credit Event? Entities will be deleted and modified.') == 'Button1':
            try:
                self.StoreParameters()
                result = CreditEventHandler.UndoCreditEvent(self.m_parameters, self.m_tasks.Values())
                if result[0]:
                    self.PrepareNew()
                elif result[1] and type(result[1]) == type(''):
                    acm.UX().Dialogs().MessageBoxInformation(self.m_fuxDlg.Shell(), result[1])
            except Exception, err:
                CreditEventDialog.LOGGER.ELOG('Error while removing Credit Event Processing.', exc_info=1)
                return
                
    def PerformToggleProcess( self) :
        selectedRowObjects = self.m_instrumentSheetCtrl.Selection().SelectedRowObjects()
        col = self.m_instrumentSheetCtrl.GridColumnIterator().First()
        processCol = None
        while col:
            column = col.GridColumn()
            if column and column.ColumnId().Text() == 'Credit Event Process':
                processCol = col
                break
            col = col.Next()
            
        if not selectedRowObjects or not processCol:
            return
        
        physicalHandled = False
        for rowObj in selectedRowObjects:
            row = self.m_instrumentSheetCtrl.RowTreeIterator(False).Find(rowObj)
            cellInfo = self.m_instrumentSheetCtrl.GetCell(row, processCol)
            if cellInfo:
                evaluator = cellInfo.Evaluator()
                if evaluator:
                    physicalHandled = physicalHandled or rowObj.Instrument().SettlementType() == 'Physical Delivery'
                    evaluator.PostRemoteValue(self.m_toggleAllBox.Checked())
    
    def StoreParameters( self ):
        self.m_parameters.AtPut('creditEventId', self.m_creditEventId)
        self.m_parameters.AtPut('creditEvent', self.m_creditEvent)
        self.m_parameters.AtPut('issuer', self.m_issuer)
        self.m_parameters.AtPut('seniority', self.m_seniority)
        self.m_parameters.AtPut('eventType', self.m_eventType)
        self.m_parameters.AtPut('defaultDate', self.m_defaultDate)
        self.m_parameters.AtPut('auctioningDate', self.m_auctioningDate)
        self.m_parameters.AtPut('settlementDate', self.m_settlementDate)
        self.m_parameters.AtPut('recoveryRate', self.m_recoveryRate)
        self.m_parameters.AtPut('currency', self.m_currency)
        self.m_parameters.AtPut('undCurrency', self.m_undCurrency)
        self.m_parameters.AtPut('restructuring', self.m_restructuring)
        self.m_parameters.AtPut('eventStatus', self.m_eventStatus)
        self.m_parameters.AtPut('tradeStatusClosing', self.m_tradeStatusClosing)
        self.m_parameters.AtPut('tradeStatusModifyClosing', self.m_tradeStatusModifyClosing)
        self.m_parameters.AtPut('tradeStatusModifyOther', self.m_tradeStatusModifyOther)
        self.m_parameters.AtPut('testmode', self.m_testmode)
        self.m_parameters.AtPut('tradeRule', self.m_tradeRule)
        self.m_parameters.AtPut('freeText1', self.m_freeText1)
        self.m_parameters.AtPut('freeText2', self.m_freeText2)
        self.m_parameters.AtPut('allInstruments', self.m_allInstruments)
        self.m_parameters.AtPut('shell', self.m_fuxDlg.Shell())
    
    def PrepareTasks( self, instrument ):
        instruments = acm.FArray()
        instruments.Add(instrument)
        '''
        row = self.m_instrumentSheetCtrl.RowTreeIterator(False).FirstChild()
        while row:
            col = self.m_instrumentSheetCtrl.GridColumnIterator()
            if not self.m_creditEvent:
                while col:
                    column = col.GridColumn()
                    if column:
                        if column.ColumnId().Text() == 'Credit Event Process':
                            cellInfo = self.m_instrumentSheetCtrl.GetCell(row, col)
                            if cellInfo.FormattedValue() == 'Yes':
                                instruments.Add(cellInfo.RowObject().Instrument())
                                break
                    col = col.Next()
            else:
                cellInfo = self.m_instrumentSheetCtrl.GetCell(row, col)
                instruments.Add(cellInfo.RowObject().Instrument())
            row = row.NextSibling()
        '''
        for ins in instruments:
            if not self.m_tasks.HasKey(ins):
                self.CreateInstrumentTask(ins)
        
        for ins in self.m_tasks.Keys():
            if not instruments.Includes(ins):
                self.m_tasks.RemoveKey(ins)
    
    def CreateInstrumentTask( self, instrument, tradeDict=None, iLink=None ):
        task = acm.FDictionary()
        task.AtPut('instrument', instrument)
        task.AtPut('type', CreditEventDialog.GetColumnValue(instrument, 'Credit Event Instrument Type'))
        task.AtPut('instrumentLink', iLink)
        tradeArray = acm.FArray()
        for trade in acm.TradeActionUtil().ValidTrades(instrument, self.m_defaultDate, True):
            if trade.Status() in self.m_statusFilter:
                defaultDate = MaxDate(self.m_defaultDate, trade.AcquireDay())
                tradeTask = acm.FDictionary()
                tradeTask.AtPut('trade', trade)
                tradeTask.AtPut('nominal', acm.TradeActionUtil().RemainingNominalAtDate(trade, defaultDate, instrument.SpotDate(defaultDate), defaultDate, True))
                tradeTask.AtPut('position', acm.TradeActionUtil().RemainingQuantityAtDate(trade, defaultDate, True) * instrument.ContractSize())
                tradeTask.AtPut('tradeLink', None)
                tradeTask.AtPut('recoveryPaymentLink', None)
                tradeTask.AtPut('accPaymentLinks', None)
                tradeTask.AtPut('type', CreditEventDialog.GetColumnValue(instrument, 'Credit Event Instrument Type'))
                tradeArray.Add(tradeTask)
                if not tradeDict is None:
                    tradeDict.AtPut(trade, tradeTask)
        task.AtPut('trades', tradeArray)
        self.m_tasks.AtPut(instrument, task)
    
    """------------------ Open/New ------------------"""

    def PrepareNew( self ):
        self.m_tradeMap.Clear()
        self.m_tasks.Clear()
        self.m_creditEvent = None
        self.m_creditEventId = None
        self.m_creditEventIdCtrl.SetValue(self.m_creditEventId)
        self.m_issuer = None
        self.m_issuerCtrl.SetValue(self.m_issuer)
        self.m_freeText1 = None
        self.m_freeText1Ctrl.SetValue(self.m_freeText1)
        self.m_freeText2 = None
        self.m_freeText2Ctrl.SetValue(self.m_freeText2)
        self.m_fuxDlg.Caption('Credit Event Processing')
        self.m_freeText1 = None
        self.m_freeText1Ctrl.SetValue(self.m_freeText1)
        self.m_freeText2 = None
        self.m_freeText2Ctrl.SetValue(self.m_freeText2)
        self.m_currency = None
        self.m_currencyCtrl.SetValue(self.m_currency)
        self.m_undCurrency = None
        self.m_undCurrencyCtrl.SetValue(self.m_undCurrency)
        self.m_auctioningDate = None
        self.m_auctioningDateCtrl.SetValue(self.m_auctioningDate)        
        self.m_seniority = None
        self.m_seniorityCtrl.SetValue(self.m_seniority)
        self.m_restructuring = acm.FEnumeration['enum(RestructuringType)'].Enumeration('None')
        self.m_restructuringCtrl.SetValue(self.m_restructuring)
        self.m_defaultDate = acm.Time.DateValueDay()
        self.m_defaultDateCtrl.SetValue(self.m_defaultDate)
        self.m_settlementDate = acm.Time.DateValueDay()
        self.m_settlementDateCtrl.SetValue(self.m_settlementDate)      
        self.m_eventType = acm.FEnumeration['enum(CreditEventType)'].Enumeration('None')
        self.m_eventTypeCtrl.SetValue(self.m_eventType)
        self.m_includeTradeless = False
        self.m_includeTradelessBox.Checked(self.m_includeTradeless)
        self.m_testmode = True
        self.m_testmodeBox.Checked(self.m_testmode)
        self.m_undoBtn.Enabled(False)
        self.m_issuerCtrl.Enabled(True)
        self.m_seniorityCtrl.Enabled(True)
        self.m_currencyCtrl.Enabled(True)
        self.m_undCurrencyCtrl.Enabled(True)
        self.m_restructuringCtrl.Enabled(True)
        self.m_defaultDateCtrl.Enabled(True)
        self.m_eventTypeCtrl.Enabled(True)
        self.m_toggleAllBox.Enabled(False)
        self.m_toggleAllBox.SetCheck('Indeterminate')
        self.m_instrumentTypeCtrl.Enabled(False)
        self.SetColumns(self.m_instrumentSheetCtrl, CreditEventParameters.INSTRUMENT_COLUMNS)
        self.SetColumns(self.m_tradeSheetCtrl, CreditEventParameters.TRADE_COLUMNS, ['Credit Event Contract'])
        self.m_initInstruments = True
        self.m_updateUseFilterToggle = True
        self.m_tradeStatusClosingCtrl.Enabled(True)
        self.m_tradeStatusModifyClosingCtrl.Enabled(True)
        self.m_tradeStatusModifyOtherCtrl.Enabled(True)
        self.m_creditEventIdCtrl.Enabled(True)
        self.m_auctioningDateCtrl.Enabled(True)
        self.m_settlementDateCtrl.Enabled(True)
        self.m_recoveryRateCtrl.Enabled(False)
        self.m_useFilterBox.Enabled(True)
        self.m_eventStatusCtrl.Enabled(True)
        self.m_freeText1Ctrl.Enabled(True)
        self.m_freeText2Ctrl.Enabled(True)
        self.m_includeTradelessBox.Enabled(True)
        self.m_statusFilterBtn.Enabled(True)

    def OpenCreditEventNonGui( self, creditEvent = None ):
        # this if-statement is used by the unit tests
        if creditEvent:
            self.m_creditEvent = creditEvent
            self.m_justPerformed = True
            
        businessEvent = self.m_creditEvent.BusinessEvent()
        
        self.m_tasks.Clear()
        self.m_tradeMap.Clear()
        tempTradeDict = acm.FDictionary()
        for iLink in businessEvent.InstrumentLinks():
            ins = iLink.Instrument()
            self.m_tradeMap.AtPut(ins, acm.FArray())
            for trade in acm.TradeActionUtil().ValidTrades(ins, self.m_defaultDate, True):
                self.m_tradeMap.At(ins).Add(trade)
            self.CreateInstrumentTask(ins, tempTradeDict, iLink)
        for tLink in businessEvent.TradeLinks():
            contractTrade = tLink.Trade()
            closingTrade = CreditEventDialog.GetClosingTrade( contractTrade )
            ins = contractTrade.Instrument()
            if not self.m_tradeMap.HasKey(ins):
                self.m_tradeMap.AtPut(ins, acm.FArray())
                for trade in acm.TradeActionUtil().ValidTrades(ins, self.m_defaultDate, True):
                    self.m_tradeMap.At(ins).Add(trade)
                self.CreateInstrumentTask(ins, tempTradeDict)
            if tempTradeDict.HasKey(contractTrade):
                task = tempTradeDict.At(contractTrade)
            else:
                task = acm.FDictionary()
                task.AtPut('trade', contractTrade)
                task.AtPut('closingTrade', closingTrade)
                task.AtPut('recoveryPaymentLink', None)
                task.AtPut('recoveryInterestPaymentLink', None)
                task.AtPut('recoveryCouponPaymentLink', None)
                task.AtPut('recoveryRebatePaymentLink', None)
                self.m_tasks.At(ins).At('trades').Add(task)
                tempTradeDict.AtPut(contractTrade, task)
            defaultDate = MaxDate(self.m_defaultDate, contractTrade.AcquireDay())
            task.AtPut('tradeLink', tLink)
            task.AtPut('nominal', acm.TradeActionUtil().RemainingNominalAtDate(contractTrade, defaultDate, ins.SpotDate(defaultDate), defaultDate, True))
            task.AtPut('position', acm.TradeActionUtil().RemainingQuantityAtDate(contractTrade, defaultDate, True) * ins.ContractSize())
            if not self.m_tradeMap.At(ins).Includes(closingTrade):
                self.m_tradeMap.At(ins).Add(closingTrade)
            if not self.m_tradeMap.At(ins).Includes(contractTrade):
                self.m_tradeMap.At(ins).Add(contractTrade)
        for pLink in businessEvent.PaymentLinks():
            # all payments are connected to the closing trade, SINGLE NAME CDS
            # all payments are connected to the contract trade, BASKET CDS
            payment = pLink.Payment()
            paymentTrade  = payment.Trade()
            closingTrade  = CreditEventDialog.GetClosingTrade( paymentTrade )
            if closingTrade:
                contractTrade = closingTrade.Contract()
            else:
                contractTrade = paymentTrade
                
            ins = paymentTrade.Instrument()
            
            if not self.m_tradeMap.HasKey(ins):
                self.m_tradeMap.AtPut(ins, acm.FArray())
                for trade in acm.TradeActionUtil().ValidTrades(ins, self.m_defaultDate, True):
                    self.m_tradeMap.At(ins).Add(trade)
                self.CreateInstrumentTask(ins, tempTradeDict)
            if tempTradeDict.HasKey(paymentTrade):
                task = tempTradeDict.At(paymentTrade)
            else:
                task = acm.FDictionary()
                task.AtPut('trade', paymentTrade)
                task.AtPut('closingTrade', closingTrade)
                task.AtPut('tradeLink', None)
                task.AtPut('recoveryPaymentLink', None)
                task.AtPut('recoveryInterestPaymentLink', None)
                task.AtPut('recoveryRebatePaymentLink', None)
                task.AtPut('recoveryCouponPaymentLink', None)
                task.AtPut('nominal', paymentTrade.FaceValue() * -1.0)
                task.AtPut('position', paymentTrade.Quantity() * ins.ContractSize() * -1.0)
                self.m_tasks.At(ins).At('trades').Add(task)
                tempTradeDict.AtPut(paymentTrade, task)
                if not self.m_tradeMap.At(ins).Includes(paymentTrade):
                    self.m_tradeMap.At(ins).Add(paymentTrade)
            if payment.Type() == 'Recovery':
                task.AtPut('recoveryPaymentLink', pLink)
            elif payment.Type() == 'Recovery Coupon':
                task.AtPut('recoveryCouponPaymentLink', pLink)
            elif payment.Type() == 'Recovery Interest':
                task.AtPut('recoveryInterestPaymentLink', pLink)
            elif payment.Type() == 'Recovery Rebate':
                task.AtPut('recoveryRebatePaymentLink', pLink)
            tLink = CreditEventDialog.GetBusinessEventTradeLink( businessEvent, contractTrade )
            task.AtPut('tradeLink', tLink)   

            if paymentTrade != closingTrade:
                # basket CDS
                task.AtPut('nominal', paymentTrade.FaceValue())
                task.AtPut('position', paymentTrade.Quantity() * ins.ContractSize())
         
        if self.m_tradeMap.Keys().Size():
            self.m_instrumentType = self.m_tradeMap.Keys().At(0).Class()
        if not self.m_justPerformed:
            self.CreateInstrumentList()
            self.FilterInstrumentList()
            newInstruments = acm.FArray()
            for ins in self.m_filteredInstruments:
                if not self.m_tradeMap.HasKey(ins):
                    newInstruments.Add(ins)
            if newInstruments.Size():
                text = "Instruments exist that match this Credit Event:\n(%s)\n\nInclude these instruments for processing?" % ','.join([ins.Name() for ins in newInstruments])
                
                if self.m_eventStatus != acm.FEnumeration['enum(BusinessEventStatus)'].Enumeration('Confirmed'):
                    if acm.UX().Dialogs().MessageBoxYesNo(self.m_fuxDlg.Shell(), 3, text) == 'Button1':
                        for ins in newInstruments:
                            self.m_tradeMap.AtPut(ins, None)
        self.m_allInstruments.Clear()
        self.m_filteredInstruments.Clear()
        self.m_allInstruments.AddAll(self.m_tradeMap.Keys())
        self.m_filteredInstruments.AddAll(self.m_tradeMap.Keys())
        
        return

    
    def OpenCreditEvent( self, creditEvent=None ):
        try:
            if creditEvent:
                self.m_justPerformed = True
                self.m_testmode = True
                self.m_testmodeBox.Checked(self.m_testmode)
            else:
                self.m_justPerformed = False
                creditEvent = acm.UX().Dialogs().SelectObjectsInsertItems(self.m_fuxDlg.Shell(), acm.FCreditEvent, False)
                if not creditEvent:
                    return
            businessEvent = creditEvent.BusinessEvent()
            if not businessEvent:
                acm.UX().Dialogs().MessageBoxInformation(self.m_fuxDlg.Shell(), 'There must be a BusinessEvent linked to the CreditEvent.')
                return
            self.m_creditEvent = creditEvent
            self.m_creditEventId = self.m_creditEvent.Name()
            self.m_creditEventIdCtrl.SetValue(self.m_creditEventId)
            self.m_fuxDlg.Caption('Credit Event Processing - %s' % self.m_creditEventId)
            self.m_freeText1 = self.m_creditEvent.Text1()
            self.m_freeText1Ctrl.SetValue(self.m_freeText1)
            self.m_freeText2 = self.m_creditEvent.Text2()
            self.m_freeText2Ctrl.SetValue(self.m_freeText2)
            self.m_undoBtn.Enabled(True)
            self.m_issuer = self.m_creditEvent.Party()
            self.m_issuerCtrl.SetValue(self.m_issuer)
            self.m_issuerCtrl.Enabled(False)
            self.m_seniority = self.m_creditEvent.SeniorityChlItem()
            self.m_seniorityCtrl.SetValue(self.m_seniority)
            self.m_seniorityCtrl.Enabled(False)
            self.m_currency = self.m_creditEvent.Currency()
            self.m_currencyCtrl.SetValue(self.m_currency)
            self.m_currencyCtrl.Enabled(False)
            self.m_undCurrency = self.m_creditEvent.UnderlyingCurrency()
            self.m_undCurrencyCtrl.SetValue(self.m_undCurrency)
            self.m_undCurrencyCtrl.Enabled(False)
            self.m_restructuring = acm.FEnumeration['enum(RestructuringType)'].Enumeration(self.m_creditEvent.RestructuringType())
            self.m_restructuringCtrl.SetValue(self.m_restructuring)
            self.m_restructuringCtrl.Enabled(False)
            self.m_defaultDate = self.m_creditEvent.RecordDate()
            self.m_defaultDateCtrl.SetValue(self.m_defaultDate)
            self.m_defaultDateCtrl.Enabled(False)
            self.m_settlementDate = self.m_creditEvent.SettlementDate()
            self.m_settlementDateCtrl.SetValue(self.m_settlementDate)
            self.m_auctioningDate = self.m_creditEvent.AuctioningDate()
            self.m_auctioningDateCtrl.SetValue(self.m_auctioningDate)
            self.m_recoveryRate = self.m_creditEvent.RecoveryRate()
            self.m_recoveryRateCtrl.SetValue(self.m_recoveryRate)
            self.m_eventType = self.m_creditEvent.EventType()
            self.m_eventTypeCtrl.SetValue(self.m_eventType)
            self.m_eventTypeCtrl.Enabled(False)
            self.m_eventStatus = acm.EnumFromString('BusinessEventStatus', businessEvent.Status())
            self.m_eventStatusCtrl.SetValue( acm.EnumToString('BusinessEventStatus', self.m_eventStatus) )
            
            if businessEvent.Status() == "Confirmed":
                self.m_tradeStatusClosingCtrl.Enabled(False)
                self.m_tradeStatusModifyClosingCtrl.Enabled(False)
                self.m_tradeStatusModifyOtherCtrl.Enabled(False)
                self.m_auctioningDateCtrl.Enabled(False)
                self.m_settlementDateCtrl.Enabled(False)
                self.m_recoveryRateCtrl.Enabled(False)
                self.m_eventStatusCtrl.Enabled(False)
                self.m_creditEventIdCtrl.Enabled(False)
                self.m_freeText1Ctrl.Enabled(False)
                self.m_freeText2Ctrl.Enabled(False)
            else:
                self.m_tradeStatusClosingCtrl.Enabled(True)
                self.m_tradeStatusModifyClosingCtrl.Enabled(True)
                self.m_tradeStatusModifyOtherCtrl.Enabled(True)
                self.m_auctioningDateCtrl.Enabled(True)
                self.m_settlementDateCtrl.Enabled(True)
                if self.m_auctioningDate:
                    self.m_recoveryRateCtrl.Enabled(True)
                else:
                    self.m_recoveryRateCtrl.Enabled(False)
                self.m_eventStatusCtrl.Enabled(True)
                self.m_creditEventIdCtrl.Enabled(True)
                self.m_freeText1Ctrl.Enabled(True)
                self.m_freeText2Ctrl.Enabled(True)
                

            if self.m_tradeStatusModifyClosing:
                self.m_tradeStatusModifyClosingCtrl.SetValue( acm.EnumToString('TradeStatus', self.m_tradeStatusModifyClosing) )
            else:
                self.m_tradeStatusModifyClosingCtrl.SetValue( "No Change" )
                
            if self.m_tradeStatusModifyOther:
                self.m_tradeStatusModifyOtherCtrl.SetValue( acm.EnumToString('TradeStatus', self.m_tradeStatusModifyOther) )
            else:
                self.m_tradeStatusModifyOtherCtrl.SetValue( "No Change" )
                
            self.m_includeTradelessBox.Enabled(False)
            self.m_statusFilterBtn.Enabled(False)
            self.m_toggleAllBox.SetCheck('Indeterminate')
            self.m_toggleAllBox.Enabled(False)
            self.m_testmode = True
            self.m_testmodeBox.Checked(self.m_testmode)
            self.m_useFilter = False
            self.m_useFilterBox.Checked(self.m_useFilter)
            self.m_useFilterBox.Enabled(False)
            self.UpdateFilterPanelProperties()
            self.m_instrumentTypeCtrl.Enabled(False)
            self.SetColumns(self.m_instrumentSheetCtrl, CreditEventParameters.INSTRUMENT_COLUMNS, ['Credit Event Process'])
            self.SetColumns(self.m_tradeSheetCtrl, CreditEventParameters.TRADE_COLUMNS)
            
            self.OpenCreditEventNonGui()
            
            self.UpdateInstrumentSheet()

        except Exception, err:
            CreditEventDialog.LOGGER.ELOG('Error while opening CreditEvent. %s', str(err), exc_info=1)
            self.PrepareNew()
    
    """------------------ Instruments/Trades Sheet ------------------"""
    
    def InitInstruments( self ):
        if not self.m_creditEvent:
            self.CreateInstrumentList()
            self.FilterInstruments()
        self.m_initInstruments = False
        
    def FilterInstruments( self ):
        if not self.m_creditEvent:
            self.FilterInstrumentList()
            self.UpdateInstrumentSheet()
        self.m_filterInstruments = False
    
    def CreateInstrumentList( self ):
        self.m_allInstruments.Clear()
        if self.m_issuer:
            res = DependentCreditInstruments(self.m_issuer, self.m_defaultDate, self.m_instrumentType)
                
            for ins in res:
                self.m_allInstruments.Add(ins)
    
    def FilterInstrumentList( self ):
        self.m_filteredInstruments.Clear()
        if self.m_useFilter:
            bankruptcy = self.m_bankruptcy
            failureToPay = self.m_failureToPay
            obligDefault = self.m_obligDefault
            obligAccel = self.m_obligAccel
            repudiation = self.m_repudiation
            govIntervention = self.m_govIntervention
        else:
            bankruptcy = False
            failureToPay = False
            obligDefault = False
            obligAccel = False
            repudiation = False
            govIntervention = False
        for ins in self.m_allInstruments:
            if acm.TradeActionUtil().SatisfiesEventFilter(ins, self.m_seniority, self.m_issuer, self.m_currency, self.m_undCurrency, self.m_restructuring, self.m_useFilter, bankruptcy, failureToPay, obligDefault, obligAccel, repudiation, govIntervention):
                trades = acm.TradeActionUtil().ValidTrades(ins, self.m_defaultDate, True)
                if (self.m_includeTradeless and trades.IsEmpty()) or self.AnyTradeAfterFiltering(ins, trades):
                    self.m_filteredInstruments.Add(ins)                      
                
    def AnyTradeAfterFiltering(self, ins, trades):
        for trade in trades:
            if trade.Status() in self.m_statusFilter:
                return True
    
        return False
    
    def UpdateInstrumentSheet( self ):
        self.RemoveDependents()
        self.m_instrumentSheetCtrl.RemoveAllRows()
        self.m_instrumentSheetCtrl.InsertObject(self.m_filteredInstruments.SortByProperty('Name'), 'IOAP_LAST')
        self.m_tradeSheetCtrl.RemoveAllRows()
        row = self.m_instrumentSheetCtrl.RowTreeIterator(False).FirstChild()
        while row:
            col = self.m_instrumentSheetCtrl.GridColumnIterator()
            while col:
                column = col.GridColumn()
                if column:
                    if column.ColumnId().Text() == 'Credit Event Process':
                        cellInfo = self.m_instrumentSheetCtrl.GetCell(row, col)
                        if cellInfo:
                            evaluator = cellInfo.Evaluator()
                            if evaluator:
                                self.AddDependent(evaluator)
                            instrument = cellInfo.RowObject().Instrument()
                            if instrument:
                                self.AddDependent(instrument.Trades())
                col = col.Next()
            row = row.NextSibling()
        
    def UpdateTradeSheet( self ):
        if not self.m_instrumentSheetCtrl.IsConsistent():
            return
        self.m_instrumentSheetCtrl.GridBuilder().Refresh()
        self.m_tradeSheetCtrl.RemoveAllRows()
        selection = self.m_instrumentSheetCtrl.Selection().SelectedInstruments()
        if selection:
            tradeList = acm.FArray()
            for ins in selection:
                if self.m_tradeMap.At(ins):
                    for trade in self.m_tradeMap.At(ins):
                        if trade.Status() in self.m_statusFilter:
                            tradeList.Add(trade)
                else:
                    for trade in acm.TradeActionUtil().ValidTrades(ins, self.m_defaultDate, True):
                        if trade.Status() in self.m_statusFilter:
                            tradeList.Add(trade)
            self.m_tradeSheetCtrl.InsertObject(tradeList.SortByProperty('Oid'), 'IOAP_LAST')
        self.m_updateSheet = False
    
    def UpdateProcessToggle( self ):
        if self.m_creditEvent:
            self.m_updateProcess = False
            return
        if not self.m_instrumentSheetCtrl.IsConsistent():
            return
        value = 'None'
        selectedRowObjects = self.m_instrumentSheetCtrl.Selection().SelectedRowObjects()
        enable = len(selectedRowObjects) > 0
        col = self.m_instrumentSheetCtrl.GridColumnIterator().First()
        while col:
            column = col.GridColumn()
            if column and column.ColumnId().Text() == 'Credit Event Process':
                row = self.m_instrumentSheetCtrl.RowTreeIterator(False).FirstChild()
                while row:
                    cellInfo = self.m_instrumentSheetCtrl.GetCell(row, col)
                    if cellInfo and selectedRowObjects.Includes(cellInfo.RowObject()):
                        if cellInfo.IsInitialized():
                            if value == 'None':
                                value = cellInfo.FormattedValue()
                            else:
                                if not value == cellInfo.FormattedValue():
                                    value = 'None'
                                    break
                    row = row.NextSibling()
                break
            col = col.Next()

        self.m_toggleAllBox.Enabled(enable)
        if value == 'Yes':
            self.m_toggleAllBox.Checked(True)
        elif value == 'No':
            self.m_toggleAllBox.Checked(False)
        else:
            self.m_toggleAllBox.SetCheck('Indeterminate')
        self.m_updateProcess = False
    
    def UpdateUseFilterToggle( self ):
        tempIns = self.m_instrumentType.BasicNew(None)
        if tempIns.HasCreditEventSpec():
            self.m_useFilterBox.Enabled(True)
            self.UpdateFilterPanelProperties()
        else:
            self.m_useFilter = False
            self.m_useFilterBox.Enabled(False)
            self.m_useFilterBox.Checked(False)
            self.UpdateFilterPanelProperties()
        tempIns.Delete()
        self.m_updateUseFilterToggle = False
        
    def setShowPhysicalNotSupported( self, sender ):
        if sender.IsKindOf(acm.FVarEvaluator):
            fobj = sender.Proprietor()
            if fobj.IsKindOf(acm.FTradeRow):
                if sender.Value():
                    includesPhysical = [ins for ins in fobj.Instruments() if ins.SettlementType() == 'Physical Delivery']
                    if includesPhysical:
                        self.m_showPhysicalNotSupported = True
    
    """------------------ GUI Core ------------------"""
    
    def AddDependent( self, dependent ):
        dependent.AddDependent(self)
        self.m_dependents.Add(dependent)
    
    def RemoveDependents( self ):
        for dependent in self.m_dependents:
            dependent.RemoveDependent(self)
        self.m_dependents.Clear()
    
    def ServerUpdate( self, sender, aspect, parameter ):
        if str(aspect) == 'SelectionChanged':
            self.m_updateSheet = True
            self.m_updateProcess = True
        if str(aspect) == 'varUpdate':
            self.m_updateProcess = True
            self.setShowPhysicalNotSupported(sender)
        if str(aspect) == 'insert':
            self.m_updateSheet = True
    
    def CreateLayout( self ):
        b = acm.FUxLayoutBuilder()
        b.BeginVertBox()
        b.  AddSpace(3)
        b.  BeginHorzBox()
        b.    AddSpace(8)
        b.    AddButton('open', 'Open...')
        b.    AddButton('new', 'New')
        b.    AddButton('refresh', 'Refresh')
        b.    AddFill()
        b.    AddCheckbox('showDetails', 'Show Details')
        b.  EndBox()
        b.  AddSpace(5)
        b.  BeginHorzBox()
        b.    AddSpace(8)
        self.m_creditEventIdCtrl.BuildLayoutPart(b, 'Credit Event ID')
        b.    AddSpace(5)
        self.m_instrumentTypeCtrl.BuildLayoutPart(b, 'Instrument Type')
        b.    AddSpace(8)
        b.  EndBox()
        b.  AddSpace(5)
        b.  BeginHorzBox('EtchedIn', 'Default Details')
        b.    BeginVertBox()
        self.m_issuerCtrl.BuildLayoutPart(b, 'Issuer')
        self.m_seniorityCtrl.BuildLayoutPart(b, 'Seniority')
        self.m_currencyCtrl.BuildLayoutPart(b, 'Currency')
        self.m_undCurrencyCtrl.BuildLayoutPart(b, 'Ref Currency')
        self.m_restructuringCtrl.BuildLayoutPart(b, 'Restructuring')
        self.m_defaultDateCtrl.BuildLayoutPart(b, 'Default Date')
        self.m_auctioningDateCtrl.BuildLayoutPart(b, 'Auctioning Date')
        self.m_settlementDateCtrl.BuildLayoutPart(b, 'Settlement Date')
        self.m_recoveryRateCtrl.BuildLayoutPart(b, 'Recovery Rate')
        b.      EndBox()
        b.      AddSpace(5)
        b.      BeginVertBox()
        self.m_eventStatusCtrl.BuildLayoutPart(b, 'Event Status')
        self.m_eventTypeCtrl.BuildLayoutPart(b, 'Event Type')
        self.m_freeText1Ctrl.BuildLayoutPart(b, 'Comment 1')
        self.m_freeText2Ctrl.BuildLayoutPart(b, 'Comment 2')
        #b.        AddSpace(5)
        #b.        BeginVertBox('EtchedIn', 'Trade Status')
        self.m_tradeStatusClosingCtrl.BuildLayoutPart(b, 'Create Closing')
        self.m_tradeStatusModifyClosingCtrl.BuildLayoutPart(b, 'Modify Closing')
        self.m_tradeStatusModifyOtherCtrl.BuildLayoutPart(b, 'Trade Status')
        #b.        EndBox()
        b.        AddSpace(2)
        b.        AddCheckbox('useFilterBox', 'Use Event Filter' )
        b.        BeginVertBox('EtchedIn', 'Event Filter', 'useFilterPanel')
        b.        AddCheckbox('bankruptcyBox', 'Bankruptcy' )
        b.        AddCheckbox('failureToPayBox', 'Failure To Pay' )
        b.        AddCheckbox('obligDefaultBox', 'Obligation Default' )
        b.        AddCheckbox('obligAccelBox', 'Obligation Acceleration' )
        b.        AddCheckbox('repudiationBox', 'Repudiation' )
        b.        AddCheckbox('govInterventionBox', 'Governmental Intervention' )
        b.      EndBox()
        b.    EndBox()
        b.  EndBox()
        b.  BeginVertBox()
        b.    BeginVertBox('EtchedIn', 'Dependent Instruments')
        b.      BeginHorzBox()
        b.        AddButton('statusFilter', 'Status Filter...')
        b.        AddSpace(10)
        b.        AddCheckbox('toggleAllBox', 'Process' )
        b.        AddSpace(10)
        b.        AddCheckbox('includeTradeless', 'Include Instruments with no Trades')
        b.      EndBox()
        b.      AddCustom('instrumentSheet', 'sheet.FDealSheet', 500, 200)
        b.    EndBox()
        b.    BeginVertBox('Invisible', 'Trades:')
        b.        AddCustom('tradeSheet', 'sheet.FTradeSheet', 500, 100, -1, 250)
        b.    EndBox()
        b.  EndBox()
        b.  BeginHorzBox()
        self.m_tradeRuleCtrl.BuildLayoutPart(b, None)
        b.    AddButton('undo', 'Undo Event...')
        b.    AddFill()
        b.    AddCheckbox('testmodeBox', 'Test Mode' )
        b.    AddButton('run', 'Process...')
        b.    AddButton('cancel', 'Close')
        b.    AddSpace(8)
        b.  EndBox()
        b.EndBox()
        return b
    
    def HandleCreate( self, dlg, layout ):
        self.m_fuxDlg = dlg
        self.m_fuxDlg.Caption('Credit Event Processing')
        self.m_fuxDlg.RegisterTimer( OnTimerUpdate, 150)
        self.m_layout = layout
        self.m_bindings.AddLayout(layout)
        self.m_openBtn = layout.GetControl('open')
        self.m_openBtn.AddCallback('Activate', OnOpenButtonClicked, self)
        self.m_openBtn.ToolTip('Open')
        self.m_newBtn = layout.GetControl('new')
        self.m_newBtn.AddCallback('Activate', OnNewButtonClicked, self)
        self.m_newBtn.ToolTip('New')
        self.m_refreshBtn = layout.GetControl('refresh')
        self.m_refreshBtn.AddCallback('Activate', OnRefreshButtonClicked, self)
        self.m_refreshBtn.ToolTip('Refresh content in Dependent Instruments and Trades sections')
        self.m_undoBtn = layout.GetControl('undo')
        self.m_showDetailsBox = layout.GetControl('showDetails')
        self.m_showDetailsBox.AddCallback('Activate', OnShowDetailsChanged, self)
        self.m_showDetailsBox.ToolTip('Show/Hide default details')
        self.m_showDetailsBox.Checked(True)
        self.m_undoBtn.AddCallback('Activate', OnUndoButtonClicked, self)
        self.m_undoBtn.Enabled(False)
        self.m_undoBtn.ToolTip('Undo the open Credit Event')
        self.m_runBtn = layout.GetControl('run')
        self.m_runBtn.AddCallback('Activate', OnRunButtonClicked, self)
        self.m_runBtn.ToolTip('Process Credit Event with selected parameters')
        self.m_closeBtn = layout.GetControl('cancel')
        self.m_closeBtn.ToolTip('Close')
        self.m_creditEventIdCtrl.SetValue(self.m_creditEventId)
        self.m_creditEventIdCtrl.ToolTip('The ID of the Credit Event')
        self.m_layout.GetControl('creditEventIdCtrl').AddCallback('Changed', OnCreditEventIdChanged, self)
        self.m_issuerCtrl.SetValue(self.m_issuer)
        self.m_issuerCtrl.ToolTip('The defaulted issuer')
        self.m_layout.GetControl('issuerCtrl').AddCallback('Changed', OnIssuerChanged, self)
        if self.m_seniority:
            self.m_seniorityCtrl.SetValue(self.m_seniority.Name())
        else:
            self.m_seniorityCtrl.SetValue('')
        self.m_seniorityCtrl.ToolTip('The seniority of the instrument or the reference instrument.')
        self.m_layout.GetControl('seniorityCtrl').AddCallback('Changed', OnSeniorityChanged, self)
        self.m_instrumentTypeCtrl.SetValue('Credit Default Swap')
        self.m_instrumentTypeCtrl.ToolTip('Filter instruments on the selected instrument type.')
        self.m_instrumentTypeCtrl.Enabled(False)
        self.m_layout.GetControl('instrumentTypeCtrl').AddCallback('Changed', OnInstrumentTypeChanged, self)
        self.m_settlementDateCtrl.SetValue(self.m_settlementDate)
        self.m_settlementDateCtrl.ToolTip('Pay date for recovery related trade payments. If auctioning date is not set the settlement date is considered an estimate.')
        self.m_layout.GetControl('settlementDateCtrl').AddCallback('Changed', OnSettlementDateChanged, self)
        self.m_defaultDateCtrl.SetValue(self.m_defaultDate)
        self.m_defaultDateCtrl.ToolTip('Default date for this credit event. Positions are closed out on this date if needed.')
        self.m_layout.GetControl('defaultDateCtrl').AddCallback('Changed', OnDefaultDateChanged, self)
        self.m_auctioningDateCtrl.SetValue(self.m_auctioningDate)
        self.m_auctioningDateCtrl.ToolTip('Date when settlement date and recovery rate information is considered confirmed. If not set recovery rate used to calculate trade payments is sourced from used hazard rate curves.')
        self.m_layout.GetControl('auctioningDateCtrl').AddCallback('Changed', OnAuctioningDateChanged, self)
        self.m_recoveryRateCtrl.SetValue(self.m_recoveryRate)
        self.m_recoveryRateCtrl.ToolTip('Percentage recovery rate used for this credit event. If auctioning date is not set the recovery rate is sourced from used hazard rate curves.')
        self.m_layout.GetControl('recoveryRateCtrl').AddCallback('Changed', OnRecoveryRateChanged, self)
        self.m_eventTypeCtrl.SetValue(self.m_eventType)
        self.m_eventTypeCtrl.ToolTip('The type of event that occurred. Only stored for information purposes.')
        self.m_layout.GetControl('eventTypeCtrl').AddCallback('Changed', OnEventTypeChanged, self)
        self.m_currencyCtrl.SetValue(self.m_currency)
        self.m_currencyCtrl.ToolTip('The currency of the instrument.')
        self.m_layout.GetControl('currencyCtrl').AddCallback('Changed', OnCurrencyChanged, self)
        self.m_freeText1Ctrl.SetValue(self.m_freeText1)
        self.m_freeText1Ctrl.ToolTip('Free comment field')
        self.m_layout.GetControl('freeText1Ctrl').AddCallback('Changed', OnFreeText1Changed, self)
        self.m_freeText2Ctrl.SetValue(self.m_freeText2)
        self.m_freeText2Ctrl.ToolTip('Free comment field')
        self.m_layout.GetControl('freeText2Ctrl').AddCallback('Changed', OnFreeText2Changed, self)
        self.m_undCurrencyCtrl.SetValue(self.m_undCurrency)
        self.m_undCurrencyCtrl.ToolTip('The currency of the reference instrument.')
        self.m_layout.GetControl('undCurrencyCtrl').AddCallback('Changed', OnUndCurrencyChanged, self)
        self.m_restructuringCtrl.SetValue(self.m_restructuring)
        self.m_restructuringCtrl.ToolTip('The restructuring type')
        self.m_layout.GetControl('restructuringCtrl').AddCallback('Changed', OnRestructuringChanged, self)
        self.m_eventStatusCtrl.SetValue(acm.FEnumeration['enum(BusinessEventStatus)'].Enumerator(self.m_eventStatus))
        self.m_eventStatusCtrl.ToolTip('Set to Confirmed at auctioning date to indicate that recovery related payments are approved for settlement.')
        self.m_tradeStatusClosingCtrl.SetValue(acm.EnumToString('TradeStatus', self.m_tradeStatusClosing ) )
        self.m_tradeStatusClosingCtrl.ToolTip('Determines the Trade Status used if closing trades (Trade Type equals "Closing") are created by the Credit Event.')

        if self.m_tradeStatusModifyClosing:
            self.m_tradeStatusModifyClosingCtrl.SetValue(acm.EnumToString('TradeStatus', self.m_tradeStatusModifyClosing ) )
        else:
            self.m_tradeStatusModifyClosingCtrl.SetValue( "No Change" )
        self.m_tradeStatusModifyClosingCtrl.ToolTip('Trade Status for any existing trade, where Trade Type equals "Closing", is controlled by this field if payments on this trade are booked or modified.')
        
        if self.m_tradeStatusModifyOther:
            self.m_tradeStatusModifyOtherCtrl.SetValue(acm.EnumToString('TradeStatus', self.m_tradeStatusModifyOther ) )
        else:
            self.m_tradeStatusModifyOtherCtrl.SetValue( "No Change" )
        self.m_tradeStatusModifyOtherCtrl.ToolTip('Trade Status for any existing trade is controlled by this field if payments on this trade are booked or modified.')

        self.m_layout.GetControl('eventStatusCtrl').AddCallback('Changed', OnEventStatusCtrlChanged, self)
        self.m_layout.GetControl('tradeStatusClosingCtrl').AddCallback('Changed', OnTradeStatusClosingCtrlChanged, self)
        self.m_layout.GetControl('tradeStatusModifyClosingCtrl').AddCallback('Changed', OnTradeStatusModifyClosingCtrlChanged, self)
        self.m_layout.GetControl('tradeStatusModifyOtherCtrl').AddCallback('Changed', OnTradeStatusModifyOtherCtrlChanged, self)
        self.m_tradeRuleCtrl.SetValue(self.m_tradeRule)
        self.m_tradeRuleCtrl.ToolTip('Decides if closing trades are deleted or voided when "Undo Event" is used (or when increase in Recovery Rate causes reverts of closing trades for Tranche CDSs).')
        self.m_layout.GetControl('tradeRuleCtrl').AddCallback('Changed', OnTradeRuleChanged, self)
        self.m_useFilterBox = layout.GetControl('useFilterBox')
        self.m_useFilterBox.AddCallback('Activate', OnUseFilterChanged, self)
        self.m_useFilterBox.ToolTip('Decides if instruments should be filtered by protected events.')
        self.m_useFilterPanel = layout.GetControl('useFilterPanel')
        self.m_bankruptcyBox = layout.GetControl('bankruptcyBox')
        self.m_bankruptcyBox.AddCallback('Activate', OnFilterChanged, self)
        self.m_bankruptcyBox.Checked(self.m_bankruptcy)
        self.m_bankruptcyBox.ToolTip('Bankruptcy')
        self.m_failureToPayBox = layout.GetControl('failureToPayBox')
        self.m_failureToPayBox.AddCallback('Activate', OnFilterChanged, self)
        self.m_failureToPayBox.Checked(self.m_failureToPay)
        self.m_failureToPayBox.ToolTip('Failure to pay')
        self.m_obligDefaultBox = layout.GetControl('obligDefaultBox')
        self.m_obligDefaultBox.AddCallback('Activate', OnFilterChanged, self)
        self.m_obligDefaultBox.Checked(self.m_obligDefault)
        self.m_obligDefaultBox.ToolTip('Obligation default')
        self.m_obligAccelBox = layout.GetControl('obligAccelBox')
        self.m_obligAccelBox.AddCallback('Activate', OnFilterChanged, self)
        self.m_obligAccelBox.Checked(self.m_obligAccel)
        self.m_obligAccelBox.ToolTip('Obligation acceleration')
        self.m_repudiationBox = layout.GetControl('repudiationBox')
        self.m_repudiationBox.AddCallback('Activate', OnFilterChanged, self)
        self.m_repudiationBox.Checked(self.m_repudiation)
        self.m_repudiationBox.ToolTip('Repudiation')
        self.m_govInterventionBox = layout.GetControl('govInterventionBox')
        self.m_govInterventionBox.AddCallback('Activate', OnFilterChanged, self)        
        self.m_govInterventionBox.Checked(self.m_govIntervention)
        self.m_govInterventionBox.ToolTip('Governmental intervention')
        self.m_toggleAllBox = layout.GetControl('toggleAllBox')
        self.m_toggleAllBox.AddCallback('Activate', OnToggleAllChanged, self)
        self.m_toggleAllBox.Enabled(False)
        self.m_toggleAllBox.ToolTip('Change value in selected "Process" cells')
        self.m_toggleAllBox.SetCheck('Indeterminate')
        self.m_testmodeBox = layout.GetControl('testmodeBox')
        self.m_testmodeBox.AddCallback('Activate', OnTestmodeChanged, self)
        self.m_testmodeBox.Checked(self.m_testmode)
        self.m_testmodeBox.ToolTip('Process event in test mode, does not commit any values to the database.')
        self.m_instrumentSheetCtrl = layout.GetControl('instrumentSheet').GetCustomControl()
        self.m_instrumentSheetCtrl.InitHiddenCellsToRowTreeLevel(10)
        self.m_instrumentSheetCtrl.ShowGroupLabels(False)
        self.m_instrumentSheetCtrl.RowHeaderCaption('Instrument')
        CreditEventDialog.SetColumns(self.m_instrumentSheetCtrl, CreditEventParameters.INSTRUMENT_COLUMNS)
        self.m_instrumentSheetCtrl.AddDependent(self)
        self.m_statusFilterBtn = layout.GetControl('statusFilter')
        self.m_statusFilterBtn.AddCallback('Activate', OnStatusFilterButtonClicked, self)
        self.m_statusFilterBtn.ToolTip('Select which instruments and trades that should be processed based on trade status.')        
        self.m_includeTradelessBox = layout.GetControl('includeTradeless')
        self.m_includeTradelessBox.AddCallback('Activate', OnIncludeTradelessBoxClicked, self)
        self.m_includeTradelessBox.Checked(self.m_includeTradeless)
        self.m_includeTradelessBox.ToolTip('Select in order to list Dependent Instruments that has no trades (regardless of Trade Statuses).')                            
        self.m_tradeSheetCtrl = layout.GetControl('tradeSheet').GetCustomControl()
        self.m_tradeSheetCtrl.ShowGroupLabels(False)
        self.UpdateFilterPanelProperties()
        CreditEventDialog.SetColumns(self.m_tradeSheetCtrl, CreditEventParameters.TRADE_COLUMNS, ['Credit Event Contract'])
        
        OnShowDetailsChanged(self, None)
        
        self.UpdateInstrumentSheet()
        
    def UpdateFilterPanelProperties(self):
        enabled = self.m_useFilterBox.Enabled() and self.m_useFilter
        visible = self.m_useFilterBox.Visible() and self.m_useFilter
        
        self.m_bankruptcyBox.Enabled(enabled)
        self.m_bankruptcyBox.Visible(visible)
        
        self.m_failureToPayBox.Enabled(enabled)
        self.m_failureToPayBox.Visible(visible)
        
        self.m_obligDefaultBox.Enabled(enabled)
        self.m_obligDefaultBox.Visible(visible)
        
        self.m_obligAccelBox.Enabled(enabled)
        self.m_obligAccelBox.Visible(visible)
        
        self.m_repudiationBox.Enabled(enabled)
        self.m_repudiationBox.Visible(visible)
        
        self.m_govInterventionBox.Enabled(enabled)
        self.m_govInterventionBox.Visible(visible)        
        
        self.m_useFilterPanel.Enabled(enabled)
        self.m_useFilterPanel.Visible(visible)
        
    def HandleDestroy( self ):
        self.RemoveDependents()
        self.m_instrumentSheetCtrl.RemoveDependent(self)
    
    def InitControls( self ):
        self.m_bindings = acm.FUxDataBindings()
        self.m_bindings.AddDependent(self)
        self.m_creditEventIdCtrl = self.m_bindings.AddBinder('creditEventIdCtrl', acm.GetDomain('string'))
        self.m_issuerCtrl = self.m_bindings.AddBinder('issuerCtrl', acm.GetDomain('FParty'))
        self.m_seniorityCtrl = self.m_bindings.AddBinder('seniorityCtrl', acm.GetDomain('string'), None, CreditEventDialog.SENIORITY.Keys().Sort())
        self.m_settlementDateCtrl = self.m_bindings.AddBinder('settlementDateCtrl', acm.GetDomain('date'))
        self.m_defaultDateCtrl = self.m_bindings.AddBinder('defaultDateCtrl', acm.GetDomain('date'))
        self.m_auctioningDateCtrl = self.m_bindings.AddBinder('auctioningDateCtrl', acm.GetDomain('date'))
        self.m_recoveryRateCtrl = self.m_bindings.AddBinder('recoveryRateCtrl', acm.GetDomain('double'), acm.Get('formats/PercentShowZero'))
        self.m_eventTypeCtrl = self.m_bindings.AddBinder('eventTypeCtrl', acm.GetDomain('enum(CreditEventType)'))
        self.m_currencyCtrl = self.m_bindings.AddBinder('currencyCtrl', acm.GetDomain('FCurrency'))
        self.m_undCurrencyCtrl = self.m_bindings.AddBinder('undCurrencyCtrl', acm.GetDomain('FCurrency'))
        self.m_restructuringCtrl = self.m_bindings.AddBinder('restructuringCtrl', acm.GetDomain('enum(RestructuringType)'))
        self.m_eventStatusCtrl = self.m_bindings.AddBinder('eventStatusCtrl', acm.GetDomain('string'), None, CreditEventDialog.STATUSES)
        self.m_tradeStatusClosingCtrl = self.m_bindings.AddBinder('tradeStatusClosingCtrl', acm.GetDomain('string'), None, CreditEventDialog.TRADE_STATUSES_CLOSING)
        self.m_tradeStatusModifyClosingCtrl = self.m_bindings.AddBinder('tradeStatusModifyClosingCtrl', acm.GetDomain('string'), None, CreditEventDialog.TRADE_STATUSES_MODIFY_CLOSING)
        self.m_tradeStatusModifyOtherCtrl = self.m_bindings.AddBinder('tradeStatusModifyOtherCtrl', acm.GetDomain('string'), None, CreditEventDialog.TRADE_STATUSES_MODIFY_OTHER)
        self.m_tradeRuleCtrl = self.m_bindings.AddBinder('tradeRuleCtrl', acm.GetDomain('string'), None, CreditEventDialog.TRADE_RULES)
        self.m_freeText1Ctrl = self.m_bindings.AddBinder('freeText1Ctrl', acm.GetDomain('string'))
        self.m_freeText2Ctrl = self.m_bindings.AddBinder('freeText2Ctrl', acm.GetDomain('string'))
        self.m_instrumentTypeCtrl = self.m_bindings.AddBinder('instrumentTypeCtrl', acm.GetDomain('string'), None, CreditEventDialog.TYPE_TO_CLASS.Keys().Sort())
    
    """------------------ Help Methods ------------------"""
    
    def SetColumns( cls, sheet, addColumns, exceptColumns=None ):
        sheet.ColumnCreators().Clear()
        if not exceptColumns:
            exceptColumns = []
        columnsCreators = acm.GetColumnCreators(addColumns, acm.GetDefaultContext())
        i = 0
        while i < columnsCreators.Size():
            creator = columnsCreators.At(i)
            if not creator.ColumnId().Text() in exceptColumns:
                sheet.ColumnCreators().Add(creator)
            i = i + 1
    SetColumns=classmethod(SetColumns)
    
    def GetColumnValue( cls, entity, columnId ):
        cls.SPACE.Clear()
        object = cls.SPACE.InsertItem(entity)
        return cls.SPACE.CreateCalculation(object, columnId).Value()
    GetColumnValue=classmethod(GetColumnValue)
    
    def GetClosingTrade( cls, trade ):
        if trade.Type() == "Closing":
            return trade
            
        st = "contractTrdnbr=%i" % ( trade.Oid() )
        trades = acm.FTrade.Select( st )
        for t in trades:
            if t.Type() == "Closing" and t.Status() != 'Void':
                return t
        return None
    GetClosingTrade=classmethod(GetClosingTrade)

    def GetBusinessEventTradeLink( cls, businessEvent, trade ):
        st = "trade = %i and businessEvent = %i" % (trade.Oid(), businessEvent.Oid())
        tradeLink = acm.FBusinessEventTradeLink.Select01( st, "")
        return tradeLink
    GetBusinessEventTradeLink=classmethod(GetBusinessEventTradeLink)
    
    def CreateDataDictionary( ins=None ):
        dataDict = acm.FDictionary()
        dataDict.AtPut('issuer', None)
        dataDict.AtPut('seniority', None)
        dataDict.AtPut('currency', None)
        dataDict.AtPut('undCurrency', None)
        dataDict.AtPut('type', acm.FCreditDefaultSwap)
        dataDict.AtPut('restructuring', 0)
        dataDict.AtPut('bankruptcy', False)
        dataDict.AtPut('failureToPay', False)
        dataDict.AtPut('obligDefault', False)
        dataDict.AtPut('obligAccel', False)
        dataDict.AtPut('repudiation', False)
        dataDict.AtPut('govIntervention', False)
        if ins:
            ref = ins.CreditReferenceOrSelf()
            if not ins.IsCreditBasket():
                dataDict.AtPut('issuer', ref.Issuer())
                dataDict.AtPut('seniority', ref.Seniority())
                dataDict.AtPut('undCurrency', ref.Currency())

            dataDict.AtPut('currency', ins.Currency())
            dataDict.AtPut('type', ins.Class())
            creditSpec = ins.CreditEventSpec()
            if creditSpec:
                dataDict.AtPut('restructuring', acm.FEnumeration['enum(RestructuringType)'].Enumeration(creditSpec.RestructuringType()))
                dataDict.AtPut('bankruptcy', creditSpec.Bankruptcy())
                dataDict.AtPut('failureToPay', creditSpec.FailureToPay())
                dataDict.AtPut('obligDefault', creditSpec.ObligationDefault())
                dataDict.AtPut('obligAccel', creditSpec.ObligationAcceleration())
                dataDict.AtPut('repudiation', creditSpec.Repudiation())
                dataDict.AtPut('govIntervention', creditSpec.GovernmentalIntervention())
        return dataDict
    CreateDataDictionary=staticmethod(CreateDataDictionary)
    
    def ShowPhysicalNotSupportedDialog(self):
        self.m_showPhysicalNotSupported = False
        acm.UX().Dialogs().MessageBoxInformation(self.m_fuxDlg.Shell(), 'Physical settled CDSs are not supported by the core Credit Event Processing functionality.')

def CreditEvent(shell, dataDict):
    dialog = CreditEventDialog(dataDict)
    acm.UX().Dialogs().ShowCustomDialog(shell, dialog.CreateLayout(), dialog)
    dialog.m_recoveryRateCtrl.Enabled(False)

def PerformCreditEventInsDef(ins, shell):
    dataDict = None
    if ins:
        dataDict = CreditEventDialog.CreateDataDictionary(ins)
    CreditEvent(shell, dataDict)
    
def PerformCreditEventPartyDef(eii):
    partydef = eii.ExtensionObject()
    shell = partydef.Shell()
    dataDict = CreditEventDialog.CreateDataDictionary()
    dataDict.AtPut('issuer', partydef.CurrentObject())
    CreditEvent(shell, dataDict)

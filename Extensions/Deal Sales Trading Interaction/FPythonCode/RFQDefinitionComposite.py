import acm
from DealPackageDevKit import CompositeAttributeDefinition, DealPackageException 
from DealPackageDevKit import Action, Str, Object, Float, CalcVal

from CustomTextImportExport import ToClipboard
from QuoteRequestCustomizations import QuoteRequestCustomDefinition

from RFQTopPanelComposite import RFQTopPanel
from RFQRequestComposite import RFQRequest
from RFQReplyComposite import RFQReply
from RFQHistoryComposite import RFQHistory
from RFQSummaryComposite import RFQSummary

from QuoteRequestsData import QuoteRequestsData
from InternalMarketInterface import IMInterface
from RFQUtils import Direction, Status, Time, Amount, Misc, QuoteRequest
from RFQHistoryUtil import FromRequest

def RFQOnTimeLeftTimerTick(pSelf, *args):
    pSelf.FetchHistoryIfNeeded()
    if pSelf.ThrowExceptions(pSelf.IMInterface().AccumulatedExceptionStr()):
        if not pSelf.status:
            pSelf.request.requestButtonClicked = False
            pSelf.timeDrive += 1
    pSelf.RegisterTimeLeftTicker()

        
class RFQDefinition(CompositeAttributeDefinition):
    def Attributes(self):
        self.CreateQRData()
        self.CreateIMInterface()
        
        ''' Register callbacks '''
        self.UniqueCallback('TradingQuoteRequestInfo')
        self.UniqueCallback('CustomerQuoteRequestInfo')
        self.UniqueCallback('TradingQuoteTimeoutColumnId')
        self.UniqueCallback('CustomerQuoteTimeoutColumnId')
        methodNames = {'instrumentMethod' : self.UniqueCallback('Instrument'),
                       'tradeMethod' : self.UniqueCallback('Trade'),
                       'originalTradeIdMethod' : self.UniqueCallback('OriginalTradeId'),
                       'dealPackageMethod' : self.UniqueCallback('RFQDealPackage'),
                       'isRfqOnDealPackageMethod' : self.UniqueCallback('IsRFQOnDealPackage'),
                       'qrDataMethod' : self.UniqueCallback('QRData'),
                       'imInterfaceMethod' : self.UniqueCallback('IMInterface'),
                       'originalObjectMethod' : self.UniqueCallback('OriginalObject'),
                       'customAttributesMethod' : self.UniqueCallback('CustomAttributesAttr')}

        ''' Define attributes '''
        attributes = {}
        
        ''' General '''
        attributes.update({
        
                'initFromQuoteRequestInfo'      : Action(       action=self.UniqueCallback('@InitFromQuoteRequestInfoAction')),
                                                                                                    
                'timeDrive'                     : Float(),
                
                #This calcval is necessary for the clocks to tick, even though it is not explicitly used anywhere
                'customerTimeLeft'              : CalcVal(      calcMapping=self.UniqueCallback('CustomerQuoteRequestInfo') + ':FQuoteRequestPriceSheet:' + self.UniqueCallback('CustomerQuoteTimeoutColumnId')),
    
                'status'                        : Object(       objMapping=self.UniqueCallback('QRData') + '.QuoteRequestStatus'),
                
                'customerStatus'                : Object(       objMapping=self.UniqueCallback('QRData') + '.CustomerQuoteRequestStatus'),

                'topPanel'                      : RFQTopPanel(  timeLeft=self.UniqueCallback('TraderTimeLeft'),
                                                                customerTimeLeft=self.UniqueCallback('CustomerTimeLeft'),
                                                                status=self.PrefixedName('status'),
                                                                customerStatus=self.PrefixedName('customerStatus'),
                                                                tradeCreationSetting=self.UniqueCallback('TradeCreationSetting'),
                                                                topPanelActions=self.UniqueCallback('TopPanelActions'),
                                                                customerQuoteRequestInfoMethod=self.UniqueCallback('CustomerQuoteRequestInfo'),
                                                                requestSent=self.UniqueCallback('RequestSent'),
                                                                **methodNames),
                
                'request'                       : RFQRequest(   createNewQuoteRequest=self.UniqueCallback('CreateNewQuoteRequest'),
                                                                reOpening=self._reOpening,
                                                                checkLimits=self._checkLimits,
                                                                **methodNames),
                
                'askReply'                      : RFQReply(     direction=Direction.ask,
                                                                proposeToClient=self.UniqueCallback('SendQuoteRequestAnswer'),
                                                                onWireTimeChanged=self.UniqueCallback('PropagateWireTime'),
                                                                onLockAllInPriceChanged=self.UniqueCallback('PropagateLockAllInPrice'),
                                                                copyProposal=self.UniqueCallback('FetchProposalSummary'),
                                                                **methodNames),
                                                
                'bidReply'                      : RFQReply(     direction=Direction.bid,
                                                                proposeToClient=self.UniqueCallback('SendQuoteRequestAnswer'),
                                                                onWireTimeChanged=self.UniqueCallback('PropagateWireTime'),
                                                                onLockAllInPriceChanged=self.UniqueCallback('PropagateLockAllInPrice'),
                                                                copyProposal=self.UniqueCallback('FetchProposalSummary'),
                                                                **methodNames),
                                                   
                'history'                       : RFQHistory(   **methodNames),
                
                'summary'                       : RFQSummary(   **methodNames),
            
                'showDetails'                   : Action(       label=self.UniqueCallback('@ShowDetailsLabel'),
                                                                action=self.UniqueCallback('@FlipDetailsMode')),
                
                'customAttributes'              : QuoteRequestCustomDefinition(customerQuoteRequestInfoMethod=self.UniqueCallback('CustomerQuoteRequestInfo'),
                                                                               tradingQuoteRequestInfoMethod=self.UniqueCallback('TradingQuoteRequestInfo'),
                                                                               **methodNames),
                                                                               
                'qrData'                        : Action(       action=self.UniqueCallback('@QRData')),
                
                'fetchHistory'                  : Action(       action=self.UniqueCallback('@FetchHistoryIfNeeded')),
                
                'updateAll'                     : Action( action=self.UniqueCallback('@Update')),
                
                'lastException'                 : Str()})

           
        return attributes
    
    '''********************************************************************
    * Deal Misc
    ********************************************************************'''
    def OnInit(self, trade, dealPackage, originalObject, reOpening, checkLimits, **kwargs):
        self._trade = trade
        self._rfqDealPackage = dealPackage
        self._originalObject = originalObject
        self._reOpening = reOpening
        self._checkLimits = checkLimits
        self._timerEvent = None
        
    def OnNew(self):
        self.SetUpQRData()
        self.RegisterTimeLeftTicker()
        
    def OnDismantle(self):
        self.QRData().EndSubscriptions()
        self.RemoveTimerEvent()  
      
    '''********************************************************************
    * Timer
    ********************************************************************'''        
    def RegisterTimeLeftTicker(self):
        self._timerEvent = acm.Time().Timer().CreateTimerEvent(1, RFQOnTimeLeftTimerTick, self)
        
    def RemoveTimerEvent(self):
        if self._timerEvent:
            acm.Time().Timer().RemoveTimerEvent(self._timerEvent)
            self._timerEvent = None
    
    '''********************************************************************
    * Objects
    ********************************************************************'''        
    def Instrument(self):
        return self.Trade().Instrument()
    
    def QRData(self, *args):
        return self._qrData
    
    def TradingQRData(self):
        return self.QRData().TradingQuoteRequestsData()

    def IMInterface(self):
        return self._imInterface
    
    def RFQDealPackage(self):
        return self.GetMethod(self._rfqDealPackage)()
    
    def Trade(self):
        return self.GetMethod(self._trade)()
    
    def OriginalTradeId(self):
        return self.GetMethod(self._originalTradeId)()
    
    '''********************************************************************
    * From QRData
    ********************************************************************''' 
    def TradingQuoteRequestInfo(self):
        return self.QRData().PrimaryTradingQuoteRequestInfo()
    
    def CustomerQuoteRequestInfo(self):
        return self.QRData().CustomerQuoteRequestInfo()
        
    def QrQueryHandler(self):
        return self.QRData().QrQueryHandler()
    
    '''********************************************************************
    * Timers
    ********************************************************************''' 
    def DirectionFromInfoName(self, requestName):
        if requestName == 'Trading':
            quoteRequestInfo = self.TradingQuoteRequestInfo()
        else:
            quoteRequestInfo = self.CustomerQuoteRequestInfo()
        if quoteRequestInfo:
            direction = Direction.FromQuoteRequestInfo(quoteRequestInfo)
        else:
            direction = self.request_direction if self.request_direction else 'Ask'
        return direction
    
    def TradingQuoteTimeoutColumnId(self):
        direction = self.DirectionFromInfoName('Trading')
        return 'Quote Timeout ' + direction
    
    def CustomerQuoteTimeoutColumnId(self):
        direction = self.DirectionFromInfoName('Customer')
        return 'Quote Timeout ' + direction
    
    def TraderTimeLeft(self, *args):
        return self.QRData().TimeLeftFormatted()
    
    def CustomerTimeLeft(self, *args):
        return self.customerTimeLeft.Value() if self.customerTimeLeft else '' #self.QRData().CustomerTimeLeftFormatted()
    
    '''********************************************************************
    * Hooks
    ********************************************************************''' 
    def CustomizationHooks(self):
        return {'OnAcceptQuote' : self.customAttributes.OnAcceptQuote,
                'OnSendQuoteRequestAnswerToClient' : self.customAttributes.OnSendQuoteRequestAnswerToClient,
                'OnCreateQuoteRequest' : self.customAttributes.OnCreateQuoteRequest,
                'SuggestCustomerRequestName' : self.customAttributes.SuggestCustomerRequestName,
                'QuoteRequestCounterparties' : self.customAttributes.QuoteRequestCounterparties}
                
    '''********************************************************************
    * Misc
    ********************************************************************'''        
    def Update(self, *args):
        quoteRequest = args[-1] if len(args) else None
        if self.QRData().RequestForQuoteIsActive():
            if hasattr(quoteRequest, 'IsKindOf') and quoteRequest.IsKindOf('FQuoteRequestInfo'):
                self.AddQuoteRequestToHistoryList(quoteRequest)
        else:
            self.FetchHistoryNeeded(True)
        self.ExecuteAutoActions()
        oldStatus = self.status
        self.timeDrive += 1
        newStatus = self.status
        if oldStatus != newStatus:
            self.OnStatusChanged(oldStatus, newStatus)
        if self.ThrowExceptions(self.IMInterface().AccumulatedExceptionStr()):
            if not self.status:
                self.request.requestButtonClicked = False
    
    def OnStatusChanged(self, oldVal, newVal, *args):                
        if str(oldVal) == Status.countered:
            self.ResetCountered()

        if str(oldVal) in [Status.subject, Status.subjAccept] and str(newVal) == Status.firm:
            self.ResetCountered()
            
        if str(oldVal) in [Status.stream, Status.firm] and str(newVal) == Status.pending:
            self.ResetCountered() 
    
    def ExecuteAutoActions(self):
        if self.TraderPriceUpdatedAndCustomerPriceIsLocked():
            self.SendQuoteRequestAnswer()
            
    def TraderPriceUpdated(self):
        return self.customerStatus == Status.subject and self.status == Status.stream
    
    def TraderPriceUpdatedAndCustomerPriceIsLocked(self):
        return self.TraderPriceUpdated() and self.LockAllInPrice() and self.QRData().ProposedToClient()
    
    def OnRequestQuoteComplete(self, customerQuoteRequestInfo):
        self.request.OnRequestQuoteComplete(customerQuoteRequestInfo)
    
    def OnSendOrderComplete(self, orderHandler):
        self.request.OnSendOrderComplete(orderHandler)
        
    def ThrowExceptions(self, exceptionsStr):
        errorsFound = False
        if len(exceptionsStr):
            self.Owner().DealPackage().GUI().GenericMessage(exceptionsStr)
            self.lastException = exceptionsStr
            errorsFound = True
        return errorsFound
        
    def ResetCountered(self):
        self.askReply.ResetCountered()
        self.bidReply.ResetCountered()
    
    def OnFirstQueryResult(self, result):
        self.QRData().QrQueryHandler().RemoveObserverCallback(self.OnFirstQueryResult)
        self.QRData().InitAllVariables(result)
        self.Update()

    def AddQuoteRequestToHistoryList(self, quoteRequest):
        self.history.AddQuoteRequestToHistory(quoteRequest)
    
    def FetchHistoryFirstTime(self):
        self.QRData().QrQueryHandler().AddObserverCallback(self.OnFirstQueryResult)
        self.FetchHistoryNeeded(True)
    
    def FetchHistoryNeeded(self, val):
        self.history.FetchHistoryNeeded(val)
    
    def FetchHistoryIfNeeded(self, *args):
        self.history.FetchHistoryIfNeeded()
        
    def CreateNewQuoteRequest(self):
        self.QRData().EndSubscriptions()
        self.QRData().Reset()
        self.timeDrive += 1 # Necessary to renew all object mappings, since we have modified the object all traits map to. Cannot be done in self.CreateQRData() since it is also called in __init__ where self.timeDrive is not a trait yet...
        self.CreateIMInterface()
        self.SetUpQRData()
        self.history.ClearHistoryList()
        self.askReply.ClearReplyFields()
        self.bidReply.ClearReplyFields()

    def SendQuoteRequestAnswer(self):
        bidPrice = self.bidReply.allInPrice
        bidQuantity = self.bidReply.traderQuantity
        askPrice = self.askReply.allInPrice
        askQuantity = self.askReply.traderQuantity
        self.QRData().AllInPricesSetByUser(True)
        wireTime = self.askReply.GetWireTime() if self.request.direction == Direction.ask else self.bidReply.GetWireTime()
        self.IMInterface().SendQuoteRequestAnswer(bidPrice, bidQuantity, askPrice, askQuantity, wireTime)
    
    def PropagateWireTime(self, wireTime):
        self.SetAttribute('askReply_wireTimeToClient', wireTime, True)
        self.SetAttribute('bidReply_wireTimeToClient', wireTime, True)
    
    def PropagateLockAllInPrice(self, lockAllInPrice):
        self.SetAttribute('askReply_lockAllInPrice', lockAllInPrice, True)
        self.SetAttribute('bidReply_lockAllInPrice', lockAllInPrice, True)
    
    def LockAllInPrice(self):
        lockAllInPrice = False
        lockAllInPrice |= self.askReply.lockAllInPrice
        lockAllInPrice |= self.bidReply.lockAllInPrice
        return lockAllInPrice
        
    def FetchProposalSummary(self):
        allInPrices = {Direction.bid : self.bidReply.allInPrice,
                       Direction.ask : self.askReply.allInPrice}
        summary = self.summary.CreateCopyProposalSummaryText(allInPrices)
        ToClipboard(summary)
        
    def TopPanelActions(self):
        return self.customAttributes.TopPanelActions()

    def CustomerPriceAsFirmOrStream(self):
        return self.customAttributes.CustomerPriceAsFirmOrStream()
    
    def OriginalObject(self):
        return self.GetMethod(self._originalObject)()    
        
    def TradeCreationSetting(self, *args):
        return self.request.tradeCreationSetting
    
    def IsRFQOnDealPackage(self):
        return self.QRData().IsRFQOnDealPackage()
        
    def CustomAttributesAttr(self):
        return self.customAttributes

    def CustomRFQAttributesAsDict(self, *args):
        attrValDict = acm.FDictionary()
        try:
            for key in self.customAttributes.Attributes().keys():
                attrValDict.AtPut(key, self.customAttributes.GetAttribute(key))
        except Exception as e:
            print ('CustomRFQAttributesAsDict fail', e)
        return attrValDict
    
    def RequestSent(self):
        return self.request.requestButtonClicked
    
    def FlipDetailsMode(self, *args):
        self.Owner().DealPackage().GetAttribute('toggleAllShowModes')()

    def CreateNominalQuantityCalculations(self):
        self.CreateCustomerNominalQuantityCalculations()
        self.CreateTradingNominalQuantityCalculations()

    def CreateCustomerNominalQuantityCalculations(self):
        name = 'insNominalFactor'
        tradeCb = self.QRData().Trade
        columnId = 'Standard Calculations Instrument Nominal Factor'
        self.Owner()._dealPackageCalculations.RemoveCalculation(name)
        self.Owner()._dealPackageCalculations.CreateCalculation(name, tradeCb, 'FTradeSheet', columnId, None, None)
        self.QRData().NominalFactorCalculationCb(lambda : self.Owner().GetCalculation(name))

    def CreateTradingNominalQuantityCalculations(self):
        components = self.QRData().TradingQuoteRequestsData().Components()
        for componentName in components.Keys():
            name = componentName + '_insNominalFactor'
            tradingQRData = self.TradingQRData().QRDataAt(componentName)
            tradeCb = tradingQRData.Trade
            columnId = 'Standard Calculations Instrument Nominal Factor'
            self.Owner()._dealPackageCalculations.RemoveCalculation(name)
            self.Owner()._dealPackageCalculations.CreateCalculation(name, tradeCb, 'FTradeSheet', columnId, None, None)
            tradingQRData.NominalFactorCalculationCb(lambda : self.Owner().GetCalculation(name))

    def SetUpQRData(self):
        self.QRData().InitQuoteRequests()
        self.QRData().RegisterCbsOnTradingQuoteRequests()
        self.CreateNominalQuantityCalculations()
    
    def CreateQRData(self):
        self._qrData = QuoteRequestsData(self.Trade,
                                         self.RFQDealPackage,
                                         self.Update,
                                         self.CustomerPriceAsFirmOrStream)
    
    def CreateIMInterface(self):
        self._imInterface = IMInterface(self._qrData, self.OnSendOrderComplete, self.OnRequestQuoteComplete, self.CustomizationHooks)
    
    '''********************************************************************
    * Labels
    ********************************************************************'''
    def ShowDetailsLabel(self, *args):
        return self.Owner().DealPackage().GetAttributeMetaData('toggleAllShowModes', 'label')()
    
    '''********************************************************************
    * Init Methods
    ********************************************************************'''
    def InitFromQuoteRequestInfoAction(self, *args):
        customerQuoteRequest = args[1]
        self.DoInitFromQuoteRequestInfo(customerQuoteRequest)
                    
    def FindMostRecent(self, sortedRequests):
        orderedStatuses = [Status.firm, Status.pending, Status.countered, Status.subject, Status.subjAccept, Status.accepting, Status.accepted, Status.noAnswer, Status.cancelled, Status.passed, Status.expired, Status.rejected]
        mostRecentRequest = None
        if sortedRequests and sortedRequests.Size() > 0:
            mostRecentRequest = sortedRequests.First()
            for i in range(sortedRequests.Size()-1):
                nextRequest = sortedRequests.At(i+1)
                if mostRecentRequest.DateTime() == nextRequest.DateTime():
                    state1 = str(mostRecentRequest.State().GetDisplayName('FQuotePrice'))
                    state2 = str(nextRequest.State().GetDisplayName('FQuotePrice'))
                    if orderedStatuses.index(state2) > orderedStatuses.index(state1):
                        mostRecentRequest = nextRequest
                else:
                    break
        return mostRecentRequest
    
    def DoInitFromQuoteRequestInfo(self, quoteRequest):
        self.request.requestButtonClicked = True
        customerRequest = quoteRequest.CustomerRequest()
        requests = acm.Trading().FindRelatedQuoteRequests(customerRequest)
        activeTradingQuoteRequests = QuoteRequest.FindQuoteRequestsFromFromList(requests, 'Trading')
        activeSalesQuoteRequests = QuoteRequest.FindQuoteRequestsFromFromList(requests, 'Sales') 
        customerQuoteRequest = activeSalesQuoteRequests.First() if requests else None
        self.LoadMissingQuoteRequestInfos(customerQuoteRequest, activeTradingQuoteRequests)
        
        if requests.Size() != self.TradingQRData().NumberOfComponents() + 1:
            QuoteRequest.QueryQuoteRequests(customerRequest, self.QuoteRequestQueryResultCompleted)
        else:
            self.OnInitiateFromQuoteRequestInfosComplete()

    def QuoteRequestQueryResultCompleted(self, task):
        try:
            result = task.ResultOrThrow()
            salesQuoteRequests = QuoteRequest.FindQuoteRequestsFromFromList(result, 'Sales')
            tradingQuoteRequests = QuoteRequest.FindQuoteRequestsFromFromList(result, 'Trading')
            self.LoadMissingQuoteRequestInfos(salesQuoteRequests.First(), tradingQuoteRequests)
            self.OnInitiateFromQuoteRequestInfosComplete()
            return True
        except Exception as e:
            print ('QuoteRequestQueryResultCompleted Failed', e)
    
    def LoadMissingQuoteRequestInfos(self, customerQuoteRequest, tradingQuoteRequests):
        self.QRData().LoadMissingCustomerQuoteRequestInfo(customerQuoteRequest)
        self.QRData().LoadMissingTradingQuoteRequestInfos(tradingQuoteRequests)
        
    def OnInitiateFromQuoteRequestInfosComplete(self):
        self.customAttributes.CustomInitiateFromQuoteRequestInfos() 
        self.FetchHistoryFirstTime()
        

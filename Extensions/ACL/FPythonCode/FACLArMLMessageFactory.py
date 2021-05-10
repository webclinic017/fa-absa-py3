""" Compiled: 2020-09-18 10:38:50 """

#__src_file__ = "extensions/FACL/ACL/./etc/FACLArMLMessageFactory.py"
import acm
import amb

from FACLArMLMessageBuilder import FACLArMLMessageBuilder
from FACLAttributeMapper import FACLAttributeMapper
from FACLObjectGateway import find_mbf_section
import FOperationsUtils as Utils
from FACLProlong import GetProlonger
import FACLTradeActionUtils


class FACLArMLMessageFactory():
    def __init__(self, builder, mapper):
        self._builder = builder
        self._mapper = mapper
        
        self._armlMessages = [] # [(acmObject, armlMessage),...]

    def IsCreateObjectFromAMBAMessage(self, mbfObject):
        acrAction = self._GetAcrAction(mbfObject)
        
        if acrAction == 'DEAL_REVERSE':
            return False
        else:
            messageType = mbfObject.mbf_find_object('TYPE')
            if messageType.mbf_get_value() in ('DELETE_TRADE', 'TRADE_LIST'):
                return False
            else:
                return True

    def _PreparedForMapping(self, trade):
        
        def ScaledNominalTrade(trade, remainingNominal):
            tempTrade = acm.FTrade()
            tempTrade.Apply(trade)
            originalNominal = trade.FaceValue()
            factor = remainingNominal / originalNominal
            payments = tempTrade.Payments()
            #default scaling of payments
            for payment in payments:
                # validate payment types here
                payment.Amount(payment.Amount() * factor)

            tempTrade.FaceValue(remainingNominal)
            tempTrade.UpdatePremium(True)
            tempTrade.RegisterInStorage()
            tempTrade.AdditionalInfo().ACR_REF(trade.OriginalOrSelf().Oid())
            return tempTrade
        
        def ScaledNominalFxSwap(closedNearLeg, closedFarLeg):
            remainingNearNominal = FACLTradeActionUtils.calculate_remaining_nominal(closedNearLeg)
            remainingFarNominal = closedFarLeg.Nominal() * remainingNearNominal / closedNearLeg.Nominal() 
            nearLeg = ScaledNominalTrade(closedNearLeg, remainingNearNominal)
            farLeg = ScaledNominalTrade(closedFarLeg, remainingFarNominal)
            farLeg.ConnectedTrade(nearLeg)
            nearLeg.RegisterInStorage()
            farLeg.RegisterInStorage()
            return nearLeg, farLeg

        if trade.IsFxSwapFarLeg():
            nearLeg = trade.ConnectedTrade()
            farLeg = trade
            if nearLeg.IsClosingTrade() or nearLeg.IsDrawdownOffset():
                if not FACLTradeActionUtils.is_option_settlement_trade(nearLeg):
                    closedNearLeg = nearLeg.Contract()            
                    closedFarLeg = closedNearLeg.FxSwapFarLeg()
                    nearLeg, farLeg = ScaledNominalFxSwap(closedNearLeg, closedFarLeg)
                    trade = farLeg
            elif nearLeg.IsClosingOriginal() or nearLeg.IsDrawdownOriginal():
                nearLeg, farLeg = ScaledNominalFxSwap(nearLeg, farLeg)
                trade = farLeg
        else:
            if trade.IsClosingTrade() or trade.IsDrawdownOffset():
                if not FACLTradeActionUtils.is_option_settlement_trade(trade):
                    closingOriginal = trade.Contract()            
                    remainingNominal = FACLTradeActionUtils.calculate_remaining_nominal(closingOriginal) 
                    trade = ScaledNominalTrade(closingOriginal, remainingNominal)
            elif trade.IsClosingOriginal() or trade.IsDrawdownOriginal():
                remainingNominal = FACLTradeActionUtils.calculate_remaining_nominal(trade) 
                trade = ScaledNominalTrade(trade, remainingNominal)
        
        return trade
    
    def _HandleTrade(self, trade, mbfObject):
        acrAction = self._GetAcrAction(mbfObject)
        Utils.LogVerbose('Handle trade, ACR action is %s' % acrAction)

        if FACLTradeActionUtils.isFXNDF_trade(trade) and \
                trade.IsClosingTrade():
            Utils.LogAlways('NDF closing trade is ignored')
            return

        trade = self._PreparedForMapping(trade)

        attributes = None
        prolonger = GetProlonger(trade, self._mapper)
        
        if prolonger:
            if acrAction in ('DEAL_ADD', 'DEAL_MODIFY'):
                if prolonger.IsPartialProlong():
                    partial, attribs = prolonger.AddPartial()
                    self._HandleAcrAction(partial, attribs, mbfObject, acrAction)
                
                trade, attributes = prolonger.Add()
                self._HandleAcrAction(trade, attributes, mbfObject, 'DEAL_MODIFY')
                return
            elif acrAction == 'DEAL_REVERSE':
                attributes = self._mapper.MapAttributes(trade)                 
                self._HandleAcrAction(trade, attributes, mbfObject, 'DEAL_REVERSE')

                master, masterAttributes = prolonger.Reverse()
                self._HandleAcrAction(master, masterAttributes, mbfObject, 'DEAL_MODIFY')
                return
                        
        attributes = self._mapper.MapAttributes(trade)        
        self._HandleAcrAction(trade, attributes, mbfObject, acrAction)
        
    def _HandleAcrAction(self, trade, attributes, mbfObject, acrAction):                    
        if acrAction == 'DEAL_ADD':            
            armlMsg = self._builder.CreateRequestDealAdd(attributes, confirmationRequired = False)    
            self._armlMessages.append((trade, armlMsg))
        elif acrAction == 'DEAL_MODIFY':
            armlMsg = self._builder.CreateRequestDealModify(attributes, confirmationRequired = False)    
            self._armlMessages.append((trade, armlMsg))
        elif acrAction == 'DEAL_CONFIRM':
            armlMsg = self._builder.CreateRequestDealConfirm(attributes)    
            self._armlMessages.append((trade, armlMsg))
        elif acrAction == 'DEAL_CONFIRM_CHANGE_REF':
            changeRefAttributes   = attributes
            confimationAttributes = dict(attributes)
            currentAcrRef         = self._GetAcrRef(mbfObject)
            confimationAttributes['Reference'] = currentAcrRef

            confirmationMsg = self._builder.CreateRequestDealConfirm(confimationAttributes)
            self._armlMessages.append((trade, confirmationMsg))

            changeRefMsg = self._builder.CreateRequestDealChangeReference(currentAcrRef, changeRefAttributes)    
            self._armlMessages.append((trade, changeRefMsg))
        elif acrAction == 'DEAL_REVERSE':
            # TODO Use ACR_REF and figure this out in the AMBA hook, for consistency
            if trade.IsFxSwap():
                # Workaround due to the fact that the far leg connected trade
                # cannot be restored from the DELETE_TRADE message
                tradeSection = find_mbf_section(mbfObject, 'TRADE')
                connectedTrdnbr = tradeSection.mbf_find_object('CONNECTED_TRDNBR').mbf_get_value()
                attributes['Reference'] = connectedTrdnbr
            else:            
                # Workaround due to the fact that addinfo cannot be accessed on deleted trades
                tradeSection = find_mbf_section(mbfObject, 'TRADE')
                trdnbr = tradeSection.mbf_find_object('TRDNBR').mbf_get_value()
                attributes['Reference'] = trdnbr
                            
            armlMsg = self._builder.CreateRequestDealReverse(attributes)    
            self._armlMessages.append((trade, armlMsg))
            
        elif acrAction == 'DEAL_REVERSE_CLOSE':
            # TODO Try to find a way to have one single DEAL_REVERSE, using the ACR_REF method described above
            armlMsg = self._builder.CreateRequestDealReverse(attributes)    
            self._armlMessages.append((trade, armlMsg))
        else:
            Utils.LogVerbose('Cannot handle ACR action %s' % acrAction)
            
    def _HandleTradeSection(self, tradesSection):
        tradeMbfObject = tradesSection.mbf_first_object()
        while tradeMbfObject:
            tradeMbfString = tradeMbfObject.mbf_object_to_string()
            try:
                trade = acm.AMBAMessage.CreateObjectFromMessage(tradeMbfString)
            except:
                trade = None
            self._HandleTrade(trade, tradeMbfObject)
            tradeMbfObject = tradesSection.mbf_next_object()
    
    def _HandleInstrument(self, ins, mbfObject):
        acrAction = self._GetAcrAction(mbfObject)
        Utils.LogVerbose('Handing instrument, ACR action is %s' % acrAction)

        if acrAction == 'ADMIN_PUSH':
            attributes = self._mapper.MapAttributes(ins)
            arml = self._builder.CreateInstrument(attributes)
            self._armlMessages.append((ins, arml))
        
        insSection = find_mbf_section(mbfObject, 'INSTRUMENT')
        if insSection:
            tradesSection = find_mbf_section(insSection, 'TRADES')
            if tradesSection:
                self._HandleTradeSection(tradesSection)
            
    def _HandleParty(self, party):
        Utils.LogVerbose('Handling party')
        attributes = self._mapper.MapAttributes(party)

        arml = self._builder.CreateCounterparty(attributes)
        self._armlMessages.append((party, arml))
        
        # update permissions
        msg = self._builder.CreateGivePermission()
        self._armlMessages.append((party, msg))
        

    def _GetAcrAction(self, mbfObject):        
        acrAction = mbfObject.mbf_find_object('ACR_ACTION')
        if acrAction:
            return acrAction.mbf_get_value()
        else:
            return None

    def _GetAcrRef(self, mbfObject):        
        acrAction = mbfObject.mbf_find_object('ACR_REF')
        if acrAction:
            return acrAction.mbf_get_value()
        else:
            return None

    def Work(self, mbfObject, acmObj):
        self._armlMessages = []
        if not acmObj and self.IsCreateObjectFromAMBAMessage(mbfObject):
            mbfString = mbfObject.mbf_object_to_string()
            try:
                acmObj = acm.AMBAMessage.CreateObjectFromMessage(mbfString)
            except:
                acmObj = None
        
        mbfType = mbfObject.mbf_find_object('TYPE')
        if mbfType.mbf_get_value() == 'TRADE_LIST':
            tradesSection = mbfObject.mbf_find_object('TRADES')
            if tradesSection:
                self._HandleTradeSection(tradesSection)
            return self._armlMessages
        if not acmObj: 
            # Setting trade status of deleted trade to Simulated 
            # to allow remaining nominal to be calculated correctly
            tradeSection = find_mbf_section(mbfObject, 'TRADE')
            tradeSection.mbf_find_object('STATUS')
            tradeSection.mbf_replace_string('STATUS', 'TRADE_STATUS_SIMULATED')
            mbfString = mbfObject.mbf_object_to_string()
            try:
                acmObj = acm.AMBAMessage.CreatePreviousCloneFromMessage(mbfString)
            except:
                acmObj = None
        if acmObj:
            if acmObj.IsKindOf(acm.FTrade):
                self._HandleTrade(acmObj, mbfObject)
            elif acmObj.IsKindOf(acm.FInstrument):
                self._HandleInstrument(acmObj, mbfObject)
            elif acmObj.IsKindOf(acm.FParty):
                self._HandleParty(acmObj)
            else:
                Utils.LogVerbose('Ignoring object of type %s' % acmObj.ClassName())
        else:
            Utils.LogVerbose('Could not create object')
        
        return self._armlMessages


class FACLArMLMessageFactoryMtm(FACLArMLMessageFactory):
    def __init__(self, builder, mapper):
        FACLArMLMessageFactory.__init__(self, builder, mapper)

    def _HandleAcrAction(self, trade, attributes, mbfObject, acrAction):                    

        if acrAction not in ('DEAL_REVERSE', 'DEAL_REVERSE_CLOSE'):
            if 'Replacement Value' in attributes:
                armlMsg = self._builder.CreateMtM(attributes)
                self._armlMessages.append((trade, armlMsg))

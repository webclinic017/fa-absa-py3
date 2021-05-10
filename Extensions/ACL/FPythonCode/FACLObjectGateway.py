""" Compiled: 2020-09-18 10:38:50 """

#__src_file__ = "extensions/FACL/ACL/./etc/FACLObjectGateway.py"
import acm
import amb
from FACLFilterQuery import FACLFilterQuery, DefaultFilterCallbacks
from FACLTradeActionUtils import trade_is_repricing_close, trade_is_corrected, is_closing_type_trade, calculate_remaining_nominal, is_reprice_type_trade

def add_acr_action(mbfObject, name):
    # Must be after the header (TYPE, VERSION, TIME, SOURCE)
    mbfObject.mbf_find_object('SOURCE')    
    mbfObject.mbf_add_string('ACR_ACTION', name)

def add_acr_ref(mbfObject, value):
    # Must be after the header (TYPE, VERSION, TIME, SOURCE)
    mbfObject.mbf_find_object('SOURCE')    
    mbfObject.mbf_add_string('ACR_REF', value)

def find_mbf_section(mbfObject, sectionTag, prefixes = ['', '!', '+', '-']):
    mbfSection = None
    for pre in prefixes:
        tmpTag = pre + sectionTag
        mbfSection = mbfObject.mbf_find_object(tmpTag)
        if mbfSection:
            break
    return mbfSection

def extract_acr_ref(mbfObject):
    tradeSection = find_mbf_section(mbfObject, 'TRADE')
    
    addInfoSection = tradeSection.mbf_find_object('+ADDITIONALINFO')
    if not addInfoSection:
        addInfoSection = tradeSection.mbf_find_object('ADDITIONALINFO')
    
    while addInfoSection:
        tagName = addInfoSection.mbf_get_value()
        if tagName in ['+ADDITIONALINFO', 'ADDITIONALINFO']:
            fieldName = addInfoSection.mbf_find_object('ADDINF_SPECNBR.FIELD_NAME')
            if fieldName.mbf_get_value() == 'ACR_REF':
                fieldValue = addInfoSection.mbf_find_object('VALUE')
                return fieldValue.mbf_get_value()
        addInfoSection = tradeSection.mbf_next_object()
        
    return None

def is_b2b_fxswap_internals(trade):
    skip = False
    if trade.GroupTrdnbr():
        skip = not (trade.IsFxSwapFarLeg() and trade.ConnectedTrade().IsGroupParent())
        skip = skip and trade.IsFxSwap()
    return skip
    
def is_spot_cover_internals(trade):
    skip = (not trade.IsFxSwap() and trade.IsGroupChild())
    return skip

def should_not_propagate_trade(trade):
    origOrSelf = trade.OriginalOrSelf()
    return trade.IsFxSwapNearLeg() or \
           trade_is_corrected(origOrSelf) or \
           is_spot_cover_internals(origOrSelf) or \
           is_b2b_fxswap_internals(origOrSelf)
    
def create_mbf_object(acmObj, oldMbfObject):
    source = oldMbfObject.mbf_find_object('SOURCE').mbf_get_value()
    generator = acm.FAMBAMessageGenerator()
    generator.SourceName(source)
    mbfBuffer = amb.mbf_create_buffer_from_data(generator.Generate(acmObj).AsString())
    return mbfBuffer.mbf_read()


def build_exercise_trade_callback(current, trade, mbfObject):
    if trade.Type() in ['Exercise', 'Assign', 'Abandon']:
        return None
    if current.Type() in ['Exercise', 'Assign']:
        if trade.Instrument().SettlementType() == 'Physical Delivery':
            newCurrent = None
            newPrevious = trade
            newMbfObject = create_mbf_object(trade, mbfObject)
        else:
            newCurrent = trade
            newPrevious = trade
            newMbfObject = create_mbf_object(trade, mbfObject)
    elif current.Type() == 'Abandon':
        newCurrent = None
        newPrevious = trade
        newMbfObject = create_mbf_object(trade, mbfObject)
    callbacks = FACLExerciseAssignFilterCallbacks(newMbfObject)
    return newCurrent, newPrevious, callbacks


def exercise_assign_trades(current, previous, mbfObject):
    toReturn = []
    bEvents = current.OriginalOrSelf().BusinessEvents('Exercise/Assign')
    if bEvents:
        tradeLinks = bEvents[0].TradeLinks()
    else:
        trade = current.Contract()
        if trade:
            ret = build_exercise_trade_callback(current, trade, mbfObject)
            if ret:
                toReturn.append(ret)
        return toReturn

    for link in tradeLinks:
        trade = link.Trade()
        ret = build_exercise_trade_callback(current, trade, mbfObject)
        if ret:
            toReturn.append(ret)
    return toReturn

def get_closed_trade(closing):
    if closing.IsFxSwapFarLeg():
        closing = closing.ConnectedTrade()
    contractTrade = closing.Contract()
    if not contractTrade:
        raise Exception('Contract trade %d missing (undefined state)' % closing.ContractTrdnbr())
    return contractTrade

def trades_to_propagate(current, previous, mbfObject):
    toReturn = None
    
    if current.Instrument().IsKindOf(acm.FOption) and \
        current.Type() in ['Exercise', 'Assign', 'Abandon']:
            toReturn = exercise_assign_trades(current, previous, mbfObject)
    else:
        if current and current.IsFxSwap():
            acrRef = current.ConnectedTrade().AdditionalInfo().ACR_REF()
        else:
            acrRef = extract_acr_ref(mbfObject)

        if is_reprice_type_trade( current ):
            callbacks = FACLRepriceFilterCallbacks(mbfObject, acrRef)
        elif is_closing_type_trade(current):
            callbacks = FACLNonOptionPositionClosingCallbacks(mbfObject)
            current = previous = get_closed_trade(current)
        else:
            callbacks = FACLAmbaHookFilterCallbacks(mbfObject, acrRef)
            
        toReturn = [(current, previous, callbacks)]
        
    return toReturn
    
def handle_single_trade(current, previous, callbacks):
    from FACLParameters import CommonSettings
    queryName = CommonSettings.tradeFilterQuery
    
    faclFilter = FACLFilterQuery(queryName, callbacks)
    return faclFilter.EvaluateQuery(previous, current)

def merge_mbf_trade_objects(mbfObjects):
    if len(mbfObjects) == 1:
        return mbfObjects[0]
    elif len(mbfObjects) > 1:
        message = amb.mbf_start_message( None, 'TRADE_LIST', '1.0', None, 'FACL_AMBA_HOOK' )
        tradeList = message.mbf_start_list('TRADES')
        for mObj in mbfObjects:
            tradeList.mbf_insert_object(mObj)

        message.mbf_end_message()
        return message
    return None
    

def handle_trade(origCurrent, origPrevious, origMbfObject):
    if should_not_propagate_trade(origCurrent):
        return None
    tradesToPopagate = trades_to_propagate(origCurrent, origPrevious, origMbfObject)
    if not tradesToPopagate:
        return None
    mbfObjects = []
    for current, previous, callbacks in tradesToPopagate:
        tmp = handle_single_trade(current, previous, callbacks)
        if tmp:
            mbfObjects.append(tmp)
    return merge_mbf_trade_objects(mbfObjects)

def handle_instrument(ins, mbfObject):
    messageType = mbfObject.mbf_find_object('TYPE')

    if messageType.mbf_get_value() in ('INSERT_INSTRUMENT', 'INSTRUMENT'):
        if ins.Issuer():
            add_acr_action(mbfObject, 'ADMIN_PUSH')
            return mbfObject
        else:
            return None
    elif messageType.mbf_get_value() == 'UPDATE_INSTRUMENT':
        if ins.Issuer():
            add_acr_action(mbfObject, 'ADMIN_PUSH')
        insObj = find_mbf_section(mbfObject, 'INSTRUMENT')
        if not insObj:
            # Required element in instrument update message
            return None
        
        insid = insObj.mbf_find_object('INSID')
        if not insid:
            # Required element in instrument update message
            return None

        from FACLParameters import CommonSettings
        queryName = CommonSettings.tradeFilterQuery
        
        faclFilter = FACLFilterQuery(queryName, None)
        propagatedTrades = faclFilter.SelectTradesByInstrumentName(insid.mbf_get_value())
                
        if propagatedTrades:
            insObj.mbf_last_object()
            tradesList = insObj.mbf_start_list('TRADES')
            time = mbfObject.mbf_find_object('TIME').mbf_get_value()
            source = mbfObject.mbf_find_object('SOURCE').mbf_get_value()
            generator = acm.FAMBAMessageGenerator()
            
            for trade in propagatedTrades:
                tradeSection = amb.mbf_start_message(None, 'TRADE', '1.0', time, source)
                add_acr_action(tradeSection, 'DEAL_MODIFY')
                tradeMessage = generator.Generate(trade).AsString()
                tradeBuf = amb.mbf_create_buffer_from_data(tradeMessage)
                tradeObj = tradeBuf.mbf_read()
                tradeObj = tradeObj.mbf_find_object('TRADE')
                tradeSection.mbf_insert_object(tradeObj)
                tradesList.mbf_insert_object(tradeSection)
        
        return mbfObject
    else:
        return None

class FACLObjectGateway:
    def Process(self, mbfObject):
        mbfString = mbfObject.mbf_object_to_string()
        try:
            obj = acm.AMBAMessage.CreateCloneFromMessage(mbfString)
        except:
            obj = None
        if obj:
            # Insert or update
            if obj.IsKindOf(acm.FTrade):
                try:
                    prev = acm.AMBAMessage.CreatePreviousCloneFromMessage(mbfString)
                except:
                    prev = None
                return handle_trade(obj, prev, mbfObject)
            elif obj.IsKindOf(acm.FInstrument):
                return handle_instrument(obj, mbfObject) 
            elif obj.IsKindOf(acm.FParty):
                return mbfObject
        else:
            # Delete message
            try:
                obj = acm.AMBAMessage.CreatePreviousCloneFromMessage(mbfString)
            except:
                obj = None
            if obj:
                messageType = mbfObject.mbf_find_object('TYPE')
                if messageType.mbf_get_value() == 'DELETE_TRADE':
                    if obj.IsFxSwapNearLeg():
                        pass
                    else:
                        if is_closing_type_trade(obj):
                            # Deleting a closing trade should either add to original back (full close)
                            # or modify the original nominal (partial close)
                            add_acr_action(mbfObject, 'DEAL_ADD')
                            return mbfObject
                        else:
                            add_acr_action(mbfObject, 'DEAL_REVERSE')
                            return mbfObject
                elif messageType.mbf_get_value() == 'DELETE_INSTRUMENT':
                    add_acr_action(mbfObject, 'ADMIN_DELETE')
                    return mbfObject

        return None
    
# TODO Use separate filter callbacks for different trade actions
class FACLAmbaHookFilterCallbacks(DefaultFilterCallbacks):
    def __init__(self, mbfObject, acrRef):
        self._mbfObject = mbfObject
        self._acrRef = acrRef
    
    def OnIncludeToInclude(self, previous, current):
        if self._acrRef:
            add_acr_action(self._mbfObject, 'DEAL_CONFIRM')
        else:
            add_acr_action(self._mbfObject, 'DEAL_MODIFY')
        return self._mbfObject
    
    def OnIncludeToExclude(self, previous, current):
        if current and current.OriginalOrSelf().IsCorrectionMaster():
            add_acr_action(self._mbfObject, 'DEAL_REVERSE_CLOSE')
        else:
            add_acr_action(self._mbfObject, 'DEAL_REVERSE')
        return self._mbfObject
    
    def OnExcludeToInclude(self, previous, current):
        if current.OriginalOrSelf().BusinessEvents('Split'):
            add_acr_action(self._mbfObject, 'DEAL_ADD')
        elif current.Type() == 'Reprice':
            add_acr_action(self._mbfObject, 'DEAL_MODIFY')    
        elif self._acrRef:
            add_acr_action(self._mbfObject, 'DEAL_CONFIRM_CHANGE_REF')
            add_acr_ref(self._mbfObject, self._acrRef)
        else:
            add_acr_action(self._mbfObject, 'DEAL_ADD')
        return self._mbfObject
    
    def OnExcludeToExclude(self, previous, current):
        if current and current.OriginalOrSelf().IsCorrectionMaster():
            add_acr_action(self._mbfObject, 'DEAL_REVERSE_CLOSE')
            return self._mbfObject
        else:
            return None

class FACLRepriceFilterCallbacks(DefaultFilterCallbacks):

    def __init__(self, mbfObject, acrRef):
        self._mbfObject = mbfObject
        self._acrRef = acrRef

    def OnIncludeToInclude(self, previous, current):
        if trade_is_repricing_close(current):
            return None # if you update the closing trade it should still be excluded
        elif self._acrRef:
            add_acr_action(self._mbfObject, 'DEAL_CONFIRM')
        else:
            add_acr_action(self._mbfObject, 'DEAL_MODIFY')
        return self._mbfObject
    
    def OnIncludeToExclude(self, previous, current):
        if current and current.Type() == 'Reprice':
            add_acr_action(self._mbfObject, 'DEAL_REVERSE_CLOSE')
        elif calculate_remaining_nominal(current.Contract()) == 0:
            add_acr_action(self._mbfObject, 'DEAL_REVERSE_CLOSE')
        else:
            add_acr_action(self._mbfObject, 'DEAL_ADD')
        return self._mbfObject
    
    def OnExcludeToInclude(self, previous, current):
        if current.Type() == 'Reprice':
            add_acr_action(self._mbfObject, 'DEAL_MODIFY') 
        elif trade_is_repricing_close(current):
            return None # exclude newly created Closing trades
        return self._mbfObject
    
    def OnExcludeToExclude(self, previous, current):
        return None

class FACLNonOptionPositionClosingCallbacks(DefaultFilterCallbacks):

    def __init__(self, mbfObject):
        self._mbfObject = mbfObject

    def OnAnything(self, closed):
        if calculate_remaining_nominal(closed) == 0:
            add_acr_action(self._mbfObject, 'DEAL_REVERSE_CLOSE')
        else:
            add_acr_action(self._mbfObject, 'DEAL_ADD')
        return self._mbfObject
    
    def OnIncludeToInclude(self, previous, current):
        return self.OnAnything(current)
    
    def OnIncludeToExclude(self, previous, current):
        return self.OnAnything(current)
    
    def OnExcludeToInclude(self, previous, current):
        return self.OnAnything(current)
    
    def OnExcludeToExclude(self, previous, current):
        return None

class FACLExerciseAssignFilterCallbacks(DefaultFilterCallbacks):

    def __init__(self, mbfObject):
        self._mbfObject = mbfObject
    
    def OnIncludeToInclude(self, previous, current):
        add_acr_action(self._mbfObject, 'DEAL_MODIFY')
        return self._mbfObject
    
    def OnIncludeToExclude(self, previous, current):
        add_acr_action(self._mbfObject, 'DEAL_REVERSE')
        return self._mbfObject
    
    def OnExcludeToInclude(self, previous, current):
        add_acr_action(self._mbfObject, 'DEAL_ADD')
        return self._mbfObject
    
    def OnExcludeToExclude(self, previous, current):
        return None

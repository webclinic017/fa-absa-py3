''' =============================================================================================================

    Purpose		: This Module handles the Bounce back message from TMS, the Message needs to
                        : be updated for FXSwap, the Near and Far trade of an FXSwaps must be updated
                        : together, therefore for FXSwap the AMBA message must be executed within a Transaction.
    Department and Desk	:
    Requester		: Mathew Berry
    Developer		: Babalo Edwana
    CR Number		: 261644

================================================================================================================= '''
    
import acm, ael
from TMS_Functions_Common import *
from TMS_TradeWrapper_Base import *
    
class TransactionWrapper(Wrapper):
    def __init__(self, trade, fieldName, tmsID):
        Wrapper.__init__(self)
        
        if trade:
            nearTrade = trade
            farTrade  = self._otherLeg(trade)
            
            self._insertAddInfo(nearTrade.trdnbr, fieldName, tmsID)
            self._insertAddInfo(farTrade.trdnbr, fieldName, tmsID)
                
    def getTypeName(self):
        return "TRANSACTION"

    def _otherLeg(self, trade):
        for t in ael.Trade.select('connected_trdnbr=%s' % (trade.trdnbr)):
            if t.trdnbr != trade.trdnbr:
                return t
            
    def _insertAddInfo(self, trdnbr, field_name, tms_id):
        if trdnbr:
            self._addChild(AddInfoWrapper(trdnbr, field_name, tms_id))


class AddInfoWrapper(Wrapper):
    def __init__(self, trdnbr, fieldName, tmsId):
        Wrapper.__init__(self)
        
        self._addProperty('RECADDR', trdnbr)
        self._addProperty('ADDINF_SPECNBR.FIELD_NAME', fieldName)
        self._addProperty('VALUE', tmsId)

    def getTypeName(self):
        return "ADDITIONALINFO"

class TMSResponseMsgFactory():
    def supports(self, trade):
        if trade.insaddr.instype == "Curr":
            acmTrade = acm.FTrade[trade.trdnbr]
            if acmTrade and acmTrade.IsFxSwapNearLeg():
                return True
        return False

    def create(self, trade, fieldName, tmsID):
        return TransactionWrapper(trade, fieldName, tmsID)

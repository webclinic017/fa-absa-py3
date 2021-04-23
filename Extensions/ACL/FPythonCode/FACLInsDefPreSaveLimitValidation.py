""" Compiled: 2020-09-18 10:38:50 """

#__src_file__ = "extensions/FACL/ACL/./etc/FACLInsDefPreSaveLimitValidation.py"

import acm
import FACLMessageRouter
import FACLArMLMessageBuilder
import FACLAttributeMapper
import FUxCore
import FACLUtils
from FACLArMLResponse import FACLArMLResponse
from FACLFilterQuery import FACLFilterQuery, DefaultFilterCallbacks
from FACLParameters import PrimeSettings
from FACLInsDefLimitCheckPanel import FACLInsDefDetailsDialog
from FACLFunctions import IsTransientCorrectionMaster
from FACLUtils import IsProlongChild, IsDepositProlongChild, IsRepoProlongChild, IsSecurityLoanProlongChild
import traceback


    
class FACLInsDefPreSaveDialog(FACLInsDefDetailsDialog):
    def __init__(self, shell):
        FACLInsDefDetailsDialog.__init__(self, shell)
        self._ux_comments = None
        self._commentsString = None

    def HandleApply( self, *args ):
        self._commentsString = self._ux_comments.GetData()
        return True

    def HandleCreate(self, dlg, layout):
        FACLInsDefDetailsDialog.HandleCreate(self, dlg, layout)
        self._ux_ok = layout.GetControl('ok')
        self._ux_ok.Enabled(False)

        self._ux_comments = layout.GetControl('Comments')
        self._ux_comments.AddCallback('Changed', self.OnCommentsUpdated, None)

    def CreateLayoutCustomPane(self, b):
        b.AddSpace(5)
        b.BeginHorzBox('EtchedIn', 'Comments')
        b.  AddText('Comments', 600, 90, -1, 90)
        b.EndBox()
        b.BeginHorzBox('None')
        b.  AddFill()
        b.  AddButton('ok', 'Confirm')
        b.  AddButton('cancel', 'Reject')
        b.EndBox()

    def OnCommentsUpdated(self, _arg1, _arg2):
        self._ux_ok.Enabled(len(self._ux_comments.GetData().strip()) > 0)

    def ShowDetailsDialog(self, headline, details, response):
        return FACLInsDefDetailsDialog.ShowDetailsDialog(self, headline, details, response), self._commentsString

class FACLInsDefPreSaveLimitValidation():
    def __init__(self, msgRouter, msgBuilder, mapper, responseBuilder, saveDialog):
        self._msgRouter = msgRouter
        self._msgBuilder = msgBuilder
        self._mapper = mapper
        self._responseBuilder = responseBuilder
        self._saveDialog = saveDialog
        
    def exceptionHookSetup(self, acrRef, action):
        returnParams = acm.FDictionary()
        exceptionHookDict = acm.FDictionary()
        exceptionParameters = acm.FDictionary()
        exceptionParameters.AtPut('editObject', self._faclEditObject)
        exceptionParameters.AtPut('ACR_REF', acrRef)
        exceptionParameters.AtPut('action', action)
        exceptionHookDict.AtPut('exceptionHookCB', self.exceptionHookCB)
        exceptionHookDict.AtPut('exceptionHookParameters', exceptionParameters)
        returnParams.AtPut('exceptionHook', exceptionHookDict)
        return returnParams
    
    def exceptionHookCB(self, shell, params):
        faclEditObject = params['editObject']
        acrRef = params['ACR_REF']
        action = params['action']
        self.RejectDeal(faclEditObject, action, acrRef)
        return None

    def RejectDeal(self, faclEditObject, action, acrRef):
        if faclEditObject.IsKindOf(acm.FTrade) and acrRef:        
            params = self._mapper.MapAttributes(self._faclEditObject)
            params['Reference'] = acrRef
            msg = self._msgBuilder.CreateRequestDealReject(params)
            self._msgRouter.RouteMessage(self._faclEditObject, msg)
            if action != 'update':
                self._faclEditObject.AdditionalInfo().ACR_REF(None)
                self._faclEditObject.AdditionalInfo().ACR_COMMENT(None)
        
    def CreateInterimDeal(self, action, originalEditTrade):
        proceedWithSave = False
        acrRef = None
        addInfoHolder = None
        if self._faclEditObject.IsKindOf(acm.FTrade):
            if self._faclEditObject.IsFxSwapFarLeg() or self._faclEditObject.Instrument().InsType() == 'FXOptionDatedFwd':
                addInfoHolder = originalEditTrade
            else:
                addInfoHolder = self._faclEditObject

            try:                
                if action == 'create':
                    addInfoHolder.AdditionalInfo().ACR_REF(None)
                    
                if IsTransientCorrectionMaster(addInfoHolder):
                    addInfoHolder.AdditionalInfo().ACR_REF(None)
                    
                FACLUtils.ensureConnectedToAMB(PrimeSettings.ambUser, PrimeSettings.ambPassword, PrimeSettings.ambAddress)

                attributes = self._mapper.MapAttributes(self._faclEditObject)
                msg = self._CreateArMLMessage(action, attributes)
                responseArML = self._msgRouter.RouteMessagePersistentWithReply(self._faclEditObject, msg)
                response = self._responseBuilder(responseArML)
                
                if response.ExceptionOccurred():
                    proceedWithSave, comment = self._saveDialog.ShowDetailsDialog(response.Headline(), '', response)
                    addInfoHolder.AdditionalInfo().ACR_COMMENT(comment)
                    acrRef = response.AcrRef()
                else:
                    # Cannot read addinfo attribute while inside hook, 
                    # so the value needs to be handled separately
                    acrRef = response.AcrRef() 
                    if response.LimitOk():
                        proceedWithSave = True
                    else:
                        proceedWithSave, comment = self._saveDialog.ShowDetailsDialog(response.Headline(), '', response)
                        if comment:
                            addInfoHolder.AdditionalInfo().ACR_COMMENT(comment)

            except Exception as e:
                print(traceback.format_exc())
                msg = 'Error: %s' % str(e)
                proceedWithSave, comment = self._saveDialog.ShowDetailsDialog(msg, '', None)
                if comment:
                    addInfoHolder.AdditionalInfo().ACR_COMMENT(comment)
                    
            if proceedWithSave:
                if addInfoHolder and acrRef and not addInfoHolder.AdditionalInfo().ACR_REF():
                    addInfoHolder.AdditionalInfo().ACR_REF(acrRef)
                
        return proceedWithSave, acrRef
    
    def _CreateArMLMessage(self, action, attributes):
        if action == 'create':
            return self._msgBuilder.CreateRequestDealAdd(attributes)
        elif action == 'update':
            return self._msgBuilder.CreateRequestDealModify(attributes)
        else:
            raise Exception('Unknown action: %s' % (self._action))
            
    def _GetCurrentFaclEditObject(self, callData):
        currentEditObject = callData['editObject']
        extendedData = callData['extendedData']
        if extendedData:
            fxSwapDictionary = extendedData['fxSwapFarLeg']
        else:
            fxSwapDictionary = None
            
        if currentEditObject.Instrument().InsType() == 'FXOptionDatedFwd':
            currentFaclEditObject = FACLUtils.fxOptionDatedFwdTrade(currentEditObject, None)
        else:
            currentFaclEditObject = FACLUtils.fxSwapFarLegTradeFromNearLegTrade(currentEditObject, fxSwapDictionary)
        
        return currentFaclEditObject

    def _GetPreviousFaclEditObject(self, currentFaclEditObject, previousEditObject):
        if previousEditObject and previousEditObject.IsFxSwapNearLeg():
            previousFaclEditObject = acm.FX.GetSwapFarTrade(previousEditObject)
        else:
            if currentFaclEditObject.CorrectionTrade():
                # When doing a correct trade, the previous version is not the original of the edited clone,
                # but rather the correction original
                previousFaclEditObject = currentFaclEditObject.CorrectionTrade()
            else:
                previousFaclEditObject = previousEditObject
        
        return previousFaclEditObject

    def _GetAction(self, callData, currentFaclEditObject, previousFaclEditObject):
        from FACLParameters import CommonSettings

        queryName = CommonSettings.tradeFilterQuery
        callbacks = FACLInsDesPreSaveFilterCallbacks()
        faclFilter = FACLFilterQuery(queryName, callbacks)
        action = faclFilter.EvaluateQuery(previousFaclEditObject, currentFaclEditObject)
        return action

    def SkipInterimDeal(self, trade):
        origOrSelf = trade.OriginalOrSelf()
        return IsProlongChild(trade) or \
               IsDepositProlongChild(trade) or \
               IsRepoProlongChild(trade) or \
               IsSecurityLoanProlongChild(trade) or \
               origOrSelf.IsClosingTrade() or \
               origOrSelf.IsDrawdownOffset() or \
               origOrSelf.IsClosingOriginal() or \
               origOrSelf.IsDrawdownOriginal() or \
               not trade.BusinessEvents('Nominal Adjustment').IsEmpty() or \
               not trade.BusinessEvents('End Day Extension').IsEmpty() or \
               not trade.BusinessEvents('Merge').IsEmpty()

    def RunPreSaveHook(self, params):
        toReturn = params
        callData = params['initialData']
        
        if not callData:
            return None
        
        currentEditObject = callData['editObject']
        previousEditObject = callData['originalObject']
        
        if currentEditObject and currentEditObject.IsKindOf(acm.FTrade):
            if self.SkipInterimDeal(currentEditObject):
                currentEditObject.AdditionalInfo().ACR_REF(None)
                currentEditObject.AdditionalInfo().ACR_COMMENT(None)
            else:
                self._faclEditObject = self._GetCurrentFaclEditObject(callData)
                previousFaclEditObject = self._GetPreviousFaclEditObject(self._faclEditObject, previousEditObject)
                action = self._GetAction(callData, self._faclEditObject, previousFaclEditObject)
                
                if action and action != 'delete':                
                    proceedWithSave, acrRef = self.CreateInterimDeal(action, currentEditObject)
                    if proceedWithSave:
                        toReturn = self.exceptionHookSetup(acrRef, action)
                    else:
                        toReturn = None
                        if acrRef:
                            self.RejectDeal(currentEditObject, action, acrRef)
        
        return toReturn

class FACLInsDesPreSaveFilterCallbacks(DefaultFilterCallbacks):

    def OnIncludeToInclude(self, previous, current):
        return 'update'
    
    def OnIncludeToExclude(self, previous, current):
        return 'delete'
    
    def OnExcludeToInclude(self, previous, current):
        return 'create'
    
    def OnExcludeToExclude(self, previous, current):
        return None


# ###########################################################  
# ###################### UI VALIDATION ######################
# ###########################################################
def ael_custom_dialog_show(shell, params):
    from FACLParameters import PrimeSettings
    
    saveDialog = FACLInsDefPreSaveDialog(shell)
    msgRouter = FACLMessageRouter.FACLMessageRouter(
                    PrimeSettings.senderMBName, 
                    PrimeSettings.senderSource,
                    PrimeSettings.timeoutForReplyInSeconds, 
                    PrimeSettings.receiverMBName,
                    None,
                    1)
            
    msgBuilder = FACLArMLMessageBuilder.FACLArMLMessageBuilder()
    mapper = FACLAttributeMapper.FACLAttributeMapper()
    responseBuilder = FACLArMLResponse

    validator = FACLInsDefPreSaveLimitValidation(msgRouter, msgBuilder, mapper, responseBuilder, saveDialog)
    return validator.RunPreSaveHook(params)
    
    
def ael_custom_dialog_main( parameters, dictExtra ):
    # not used for validation
    return dictExtra

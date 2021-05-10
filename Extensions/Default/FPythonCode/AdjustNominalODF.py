
import acm
import math
import FUxCore
import CloseTrade

parKeyNominal = 'nominal'

def PerformNominalAdjustment(eii):
    insdef = eii.ExtensionObject()
    shell = insdef.Shell()
    trade = insdef.OriginalTrade()
    if ValidODFTrade(trade):
        dialog = AdjustNominalODFDialog(trade)
        if acm.UX().Dialogs().ShowCustomDialogModal(shell, dialog.CreateLayout(), dialog):
            newNominal = dialog.m_parameters[parKeyNominal]
            remainingDrawdownAmount = trade.RemainingDrawdownAmount()
            if ValidInput(trade, newNominal) and CheckUserPrivilege(math.fabs(newNominal), remainingDrawdownAmount):
                AdjustNominal(trade, newNominal)
            else:
                acm.UX().Dialogs().MessageBoxInformation(shell, "Not possible to perform nominal adjustment (see log for details).")
    else:
        acm.UX().Dialogs().MessageBoxInformation(shell, "The trade is not valid for nominal adjustment (see log for details).")

def ValidODFTrade(trade):

    if not trade:
        acm.Log("Not a valid ODF trade")
        return False
    if trade.Type() == 'Closing':
        acm.Log("Not possible to adjust nominal on closing or novated trade")
        return False
    if trade.ContractTrdnbr() != trade.Oid():
        acm.Log("Not possible to adjust nominal. Trade is part of contract")
        return False
    if trade.RemainingDrawdownAmount() == 0.0:
        acm.Log("Not possible to adjust nominal. Trade has no remaining amount left.")
        return False    
    return True

def ValidInput(trade, newNominal):
    if not trade.Instrument().Class() == acm.FOdf:
        acm.Log("Instrument is not ODF type")
        return False 
    isCallOption = trade.Instrument().OptionTypeIsCall()
    if newNominal < 0 and not isCallOption:
        acm.Log("Not possible to change direction of trade")
        return False
    if newNominal > 0 and isCallOption:
        acm.Log("Not possible to change direction of trade")
        return False
    return True
        
def CheckUserPrivilege(newRremainingDrawdownAmount, oldRremainingDrawdownAmount):
    def allow(type):
        actionType = acm.GetDomain("enum(ActionType)")
        allow = acm.FUser[acm.UserName()].ActionAllowed(actionType.Enumeration(type))
        if not allow:
            acm.Log("You don't have privilege to " + type)
        return allow
    
    if newRremainingDrawdownAmount > oldRremainingDrawdownAmount:
        return allow("Increase nominal")
    else: 
        return allow("Decrease nominal")

def AdjustNominal(trade, newNominal):
    businessEventHelper = AdjustNominalImpl(trade, newNominal)
    initData = acm.TradeActionData.GetBusinessEventInitData(businessEventHelper)
    acm.StartApplication("Instrument Definition", initData)
    
def AdjustNominalImpl(trade, newNominal):
    businessEventHelper = None
    if ValidODFTrade(trade) and ValidInput(trade, newNominal):
        newNominalAdjustedTrade = NominalAdjustedTrade(trade, newNominal)
        closeTrade = CloseOutODFTrade(trade)
        artifacts = []
        artifacts.append(closeTrade)
        artifacts = CreateBusinessEventAndLinks(trade, newNominalAdjustedTrade, artifacts)
        businessEventHelper = acm.BusinessEventUtil.CreateBusinessEventHelper(artifacts, newNominalAdjustedTrade)
    return businessEventHelper

def NominalAdjustedTrade(trade, newNominal):
    odf = trade.Instrument()
    nominalAdjustedOdf = acm.TradeActionUtil.CreateSimulatedCopy(odf)
    nominalAdjustedOdf.Name = nominalAdjustedOdf.SuggestName()
    nominalAdjustedTrade = acm.TradeActionUtil.CreateSimulatedCopy(trade)
    acm.BusinessEventUtil.InitializeTrade(nominalAdjustedTrade)
    nominalAdjustedTrade.Status('Simulated')
    nominalAdjustedTrade.Instrument = nominalAdjustedOdf
    nominalAdjustedTrade.Quantity = -math.fabs(newNominal)
    tradeLogicDecorator = acm.FTradeLogicDecorator(nominalAdjustedTrade, None)
    tradeLogicDecorator.TradeTime(acm.Time.DateToday())
    return nominalAdjustedTrade
    
def CloseOutODFTrade(trade):
    acquireDay = CalculateCloseOutAcquireDay(trade, acm.Time.DateToday())
    closeTrade = acm.TradeActions().CloseTrade(trade, 
                                                acquireDay, 
                                                acquireDay, 
                                                trade.RemainingDrawdownAmount(),
                                                0.0, 
                                                trade.Payments())
    return closeTrade
    
def CalculateCloseOutAcquireDay(trade, closeOutDate):
    odf = trade.Instrument()
    calendar = odf.GetCurrencyOne().Calendar()
    acquireDay = calendar.AdjustBankingDays(closeOutDate, odf.SpotBankingDaysOffset())
    return acquireDay

def CreateBusinessEventAndLinks(trade, newNominalAdjustedTrade, artifacts):
    if not artifacts:
        artifacts = []
    bEvent = acm.FBusinessEvent()
    bEvent.EventType = "Nominal Adjustment"
    artifacts.append(bEvent)
    
    origLink = acm.FBusinessEventTradeLink()
    origLink.Trade = trade
    origLink.TradeEventType = "Cancel"
    origLink.BusinessEvent = bEvent
    artifacts.append(origLink)
    
    nominalAdjustedLink = acm.FBusinessEventTradeLink()
    nominalAdjustedLink.Trade = newNominalAdjustedTrade
    nominalAdjustedLink.TradeEventType = "New"
    nominalAdjustedLink.BusinessEvent = bEvent
    artifacts.append(nominalAdjustedLink)
    return artifacts

# ########################## Adjust Nominal ODF Dialog #####################################
class AdjustNominalODFDialog(FUxCore.LayoutDialog):
    
    def __init__(self, trade):
        self.m_trade = trade
        self.m_bindings = None
        self.m_nominalCtrl = None
        self.m_fuxDialog = None
        self.m_parameters = {}
        self.InitControls()
    
    def InitControls(self):
        self.m_bindings = acm.FUxDataBindings()
        self.m_bindings.AddDependent(self)
        nominalFormatter = acm.Get('formats/InstrumentDefinitionNominal')
        self.m_nominalCtrl = self.m_bindings.AddBinder('nominalCtrl', acm.GetDomain('double'), nominalFormatter)
    
    def SetInitialValues(self):
        self.m_nominalCtrl.SetValue(0)
    
    def HandleCreate(self, dialog, layout):
        self.m_fuxDialog = dialog
        self.m_bindings.AddLayout(layout)
        okBtn = layout.GetControl('ok')
        okBtn.AddCallback('Activate', OnOkButtonClicked, self)
        dialog.Caption("Adjust Nominal")
        self.SetInitialValues()
    
    def CreateLayout(self):
        b = acm.FUxLayoutBuilder()
        b.BeginVertBox()
        b.      BeginVertBox('Invisible')
        self.           m_nominalCtrl.BuildLayoutPart(b, "New Nominal:")
        b.      EndBox()
        b.      BeginVertBox('Invisible')
        b.              BeginHorzBox()
        b.                      AddFill()
        b.                      AddButton('ok', 'OK')
        b.                      AddButton('cancel', 'Cancel')
        b.              EndBox()
        b.      EndBox()
        b.EndBox()
        return b
    
    def StoreParameters(self):
        self.m_parameters[parKeyNominal] = self.m_nominalCtrl.GetValue()

def OnOkButtonClicked(self, arg):
    self.StoreParameters()
    self.m_fuxDialog.CloseDialogOK()

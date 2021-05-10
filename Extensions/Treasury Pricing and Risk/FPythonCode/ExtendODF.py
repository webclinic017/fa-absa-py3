
import acm
import FUxCore
import CloseTrade

parKeyDate = 'date'
parKeyRate = 'rate'

def PerformExtend(eii):
    insdef = eii.ExtensionObject()
    shell = insdef.Shell()
    trade = insdef.OriginalTrade()
    if ValidateODFTrade(trade):
        dialog = ExtendODFDialog(trade)
        if acm.UX().Dialogs().ShowCustomDialogModal(shell, dialog.CreateLayout(), dialog):
            if ValidateExtendParameters(dialog.m_parameters, trade):
                ExtendODF(trade, dialog.m_parameters[parKeyDate], dialog.m_parameters[parKeyRate])
            else:
                acm.UX().Dialogs().MessageBoxInformation(shell, "Not possible to perform extension (see log for details).")
    else:
        acm.UX().Dialogs().MessageBoxInformation(shell, "The trade is not valid for extension (see log for details).")

def ExtendODF(trade, extendDate, extendRate):
    businessEventHelper = ExtendODFImpl(trade, extendDate, extendRate)
    initData = acm.TradeActionData.GetBusinessEventInitData(businessEventHelper)
    acm.StartApplication("Instrument Definition", initData)
    
def ExtendODFImpl(trade, extendDate, extendRate):
    artifacts = []
   
    extendedTrade = ExtendODFTrade(trade, extendDate, extendRate)

    closeTrade = CloseOutODFTrade(trade, extendDate)
    artifacts.append(closeTrade)
    
    artifacts = CreateBusinessEventAndLinks(trade, extendedTrade, artifacts)
    businessEventHelper = acm.BusinessEventUtil.CreateBusinessEventHelper(artifacts, extendedTrade)
    return businessEventHelper

def CloseOutODFTrade(trade, closeOutDate):
    acquireDay = CalculateCloseOutAcquireDay(trade, closeOutDate)
    closeTrade = acm.TradeActions().CloseTrade(trade, 
                                                acquireDay, 
                                                acquireDay, 
                                                trade.RemainingDrawdownAmount(), 
                                                0.0, 
                                                None)
    return closeTrade

def CalculateCloseOutAcquireDay(trade, closeOutDate):
    odf = trade.Instrument()
    calendar = odf.GetCurrencyOne().Calendar()
    acquireDay = calendar.AdjustBankingDays(closeOutDate, odf.SpotBankingDaysOffset())
    return acquireDay

def GetLastExerciseEvent(odf):
    exerciseEvents = acm.FExerciseEvent.Select("instrument = " + str(odf.Oid()))
    lastEvent = None
    for event in exerciseEvents:
        if not lastEvent or acm.Time.DateDifference(event.StartDate(), lastEvent.StartDate()) > 0:
            lastEvent = event
    return lastEvent

def ExtendODFTrade(trade, extendDate, extendRate):
    odf = trade.Instrument()
    extendedOdf = acm.TradeActionUtil.CreateSimulatedCopy(odf)
    extendedOdf.Name = extendedOdf.SuggestName()
    
    extendedTrade = acm.TradeActionUtil.CreateSimulatedCopy(trade)
    acm.BusinessEventUtil.InitializeTrade(extendedTrade)
    extendedTrade.Status('Simulated')
    extendedTrade.Instrument = extendedOdf
    extendedTrade.Quantity = -trade.RemainingDrawdownAmount()

    lastExerciseEvent = GetLastExerciseEvent(extendedOdf)
    if lastExerciseEvent:
        lastExerciseEvent.EndDate = extendDate
        lastExerciseEvent.Strike2 = extendRate
    tradeLogicDecorator = acm.FTradeLogicDecorator(extendedTrade, None)
    tradeLogicDecorator.TradeTime(acm.Time.DateToday())
    return extendedTrade

def ValidateODFTrade(trade):
    result = True
    if not trade:
        result = False
    if result and not GetLastExerciseEvent(trade.Instrument()):
        result = False
        acm.Log("At least one drawdown date must be defined in order to perform extend")
    elif result and trade.RemainingNominal() == 0.0:
        result = False
        acm.Log("Cannot extend a trade with zero remaining amount")
    return result

def ValidateExtendParameters(parameters, trade):
    result = True
    lastEvent = GetLastExerciseEvent(trade.Instrument())
    if acm.Time.DateDifference(lastEvent.StartDate(), parameters[parKeyDate]) > 0:
        result = False
        acm.Log("Extend date must be later than the start day on the last drawdown period")
    return result

def CreateBusinessEventAndLinks(trade, extendedTrade, artifacts):
    if not artifacts:
        artifacts = []
    
    bEvent = acm.FBusinessEvent()
    bEvent.EventType = "End Day Extension"
    artifacts.append(bEvent)
    
    origLink = acm.FBusinessEventTradeLink()
    origLink.Trade = trade
    origLink.TradeEventType = "Cancel"
    origLink.BusinessEvent = bEvent
    artifacts.append(origLink)
    
    extendLink = acm.FBusinessEventTradeLink()
    extendLink.Trade = extendedTrade
    extendLink.TradeEventType = "New"
    extendLink.BusinessEvent = bEvent
    artifacts.append(extendLink)
    return artifacts
    
# ########################## Extend ODF Dialog #####################################
class ExtendODFDialog (FUxCore.LayoutDialog):

    def __init__(self, trade):
        self.m_trade = trade
        self.m_bindings = None
        self.m_extendDateCtrl = None
        self.m_extendRateCtrl = None
        self.m_fuxDialog = None
        self.m_parameters = {}
        self.InitControls()
    
    def InitControls(self):
        self.m_bindings = acm.FUxDataBindings()
        self.m_bindings.AddDependent(self)
        dateFormatter = acm.Get('formats/DateOnly')
        rateFormatter = acm.Get('formats/FXRate')
        self.m_extendDateCtrl = self.m_bindings.AddBinder('extendDateCtrl', acm.GetDomain('date'), dateFormatter)
        self.m_extendRateCtrl = self.m_bindings.AddBinder('extendRateCtrl', acm.GetDomain('double'), rateFormatter)
    
    def SetInitialValues(self):
        self.m_extendDateCtrl.SetValue(self.LastPeriodEndDate())
        self.m_extendRateCtrl.SetValue(self.LastPeriodRate())
    
    def HandleCreate(self, dialog, layout):
        self.m_fuxDialog = dialog
        self.m_bindings.AddLayout(layout)
        okBtn = layout.GetControl('ok')
        okBtn.AddCallback('Activate', OnOkButtonClicked, self)
        dialog.Caption("Extend ODF")
        self.SetInitialValues()
        
    def CreateLayout(self):
        b = acm.FUxLayoutBuilder()
        b.BeginVertBox()
        b.      BeginVertBox('Invisible')
        self.           m_extendDateCtrl.BuildLayoutPart(b, "Extend Date")
        self.           m_extendRateCtrl.BuildLayoutPart(b, "Extend Rate")
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

    def LastPeriodEndDate(self):
        lastDate = self.m_trade.Instrument().LastDrawdownDate()
        return lastDate and lastDate or acm.Time.DateToday()

    def LastPeriodRate(self):
        rates = self.m_trade.Instrument().GetDrawDownPeriods(self.LastPeriodEndDate())
        lastRateDv = rates.Last()
        if lastRateDv:
            return lastRateDv.Number()
        return 0.0
        
    def StoreParameters(self):
        self.m_parameters[parKeyDate] = self.m_extendDateCtrl.GetValue()
        self.m_parameters[parKeyRate] = self.m_extendRateCtrl.GetValue()

def OnOkButtonClicked(self, arg):
    self.StoreParameters()
    self.m_fuxDialog.CloseDialogOK()

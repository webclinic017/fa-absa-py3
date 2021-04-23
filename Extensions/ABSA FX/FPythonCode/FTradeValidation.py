import acm
import FUxCore                  #Built In
import FUxUtils                 #Built In
import FXUtils                  #Custom for some usefull FX related functions
import FRoutingExtensions
'''================================================================================================
================================================================================================'''
def GetToleranceRates(Object, CurrencyPair):
    return 5.5
'''================================================================================================
================================================================================================'''
def FX_RateToleranceCheck(Trade,FarData = None):

    CurrPair    = Trade.CurrencyPair()
    Rates       = GetToleranceRates(Trade, CurrPair) 

    if trade.Instrument().InsType() == 'Curr': 

        if FarData:
            MarketRate = FRoutingExtensions.get_fx_rate(CurrPair, FarData[0])  
            Price      = float(FarData[1])
        else:
            MarketRate = FRoutingExtensions.get_fx_rate(CurrPair, Trade.ValueDay())  
            Price      = Trade.Price()   

        UpperLimitSpread        = Price * (Rates[0]/100)
        LowerLimitSpread        = Price * (Rates[1]/100)
        UpSide                  = Price + UpperLimitSpread
        DownSide                = Price - LowerLimitSpread
        
        if MarketRate > UpSide: 
            WarningMessage = 'WARNING: The Rate Tolerance of %f for Trade %d has been exceeded , the Market is %f and the Price is %f' % (Rates[0], Trade.Oid(), MarketRate, Price)
            acm.Log(WarningMessage)
            return False

        if MarketRate < DownSide: 
            WarningMessage = 'WARNING: The Rate Tolerance of %f for Trade %d has been exceeded , the Market is %f and the Price is %f' % (Rates[1], Trade.Oid(), MarketRate, Price)
            acm.Log(WarningMessage)
            return False

    return True
'''================================================================================================
================================================================================================'''
def FX_RateToleranceBreach(Trade):
    try:
        if str(acm.ObjectServer().ClassName()) != 'FTmServer': #only check if not entered via the GUI , What about other trades
            if not FX_RateToleranceCheck(Trade):
                TagBreach(dlg.m_edittrade) 
    except Exception, e:
        ErrorMessage = ''
        pass
'''================================================================================================
================================================================================================'''
class myCustomDialog (FUxCore.LayoutDialog):

    def __init__(self):
        self.m_reason   = None  
        self.m_fuxDlg   = None
        self.m_object   = None
        m_edittrade     = None  
   
    def CreateLayout(self):
        b = acm.FUxLayoutBuilder()
        b.BeginVertBox('EtchedIn', 'Authorize the Tolerance Breach?')
        b.  BeginVertBox()
        b.    AddInput("authorizationReason ", "Authorization Reason*: ", 15, 50) #why are we doing it this way ?
        b.  EndBox()
        b.  BeginHorzBox()
        b.    AddSpace(200)
        b.    AddFill()
        b.    AddButton('ok', 'OK')
        b.    AddButton('cancel', 'Cancel')
        b.  EndBox()
        b.EndBox()
        return b

    def HandleCreate(self, dlg, layout):
        self.m_fuxDlg = dlg
        if self.m_object.RecordType() == 'Instrument':
            self.m_fuxDlg.Caption('Authorisation for Tolerance Breach for ' + self.m_object.RecordType() + ' ' + self.m_object.Name())
        else:
            self.m_fuxDlg.Caption('Authorisation for Tolerance Breach for ' + self.m_object.RecordType())
        self.m_reason = layout.GetControl("authorizationReason")
    def HandleApply(self):
        self.m_edittrade.AdditionalInfo().FX_BreachReason(self.m_reason.GetData()) #easy enough - sets the value from the 
        if self.m_reason.GetData():
            return self.m_reason.GetData()
        else:
            #If Object is Intrumnet and real trade is nOt real
            acm.UX().Dialogs().MessageBoxInformation(self.m_fuxDlg.Shell(), 'Mandatory field, please fill in a reason')
            return None
            
'''================================================================================================
================================================================================================'''
def ael_custom_dialog_show(Shell, params):


    if not params: return params #there are NO parameters not sure if we will have this sceanrio.
    m_params = FUxUtils.UnpackInitialData(params)
    if not m_params: return params #if there is NO data to unpack
    m_object = m_params.At('editObject') 

    if not m_object:return params
    
    m_Frame     = GetFrame(Shell) 
    m_edittrade = m_Frame.EditTrade() 
    if m_edittrade.Status() in ['Simulated', 'Void', 'Tolerance Exceeded', 'BO Confirmed']:return params #Save the trade as normal    
   
    if FXUtils.TradeIsCash(m_edittrade):  
 
        dlg             = myCustomDialog()
        dlg.m_object    = m_object
        dlg.m_edittrade = m_edittrade  
        RatePassed      = FX_RateToleranceCheck(m_edittrade)  #Maybe pass the object rather

        print 'Doing Trade Validation on ' + ' ' + dlg.m_object.Name()
        if FXUtils.TradeIsSwap(m_edittrade):
            FarData     = m_Frame.GetFieldValue('trade_fx_far_value_day'), m_Frame.GetFieldValue('trade_fx_far_price')
            RatePassed  = FX_RateToleranceCheck(m_edittrade, FarData) 
            
        if RatePassed == False: 
            m_realtrade = acm.FTrade[m_Frame.GetFieldValue('trade_trdnbr').replace(chr(160), '')]    
            #TagBreach(m_edittrade) 
            builder    = dlg.CreateLayout() #does this call handlecreate?
            dialogData = acm.UX().Dialogs().ShowCustomDialogModal(Shell, builder, dlg)

            if dialogData:
                m_Trade = m_realtrade if m_realtrade else m_edittrade
                resultDict = acm.FDictionary()
                resultDict.AtPut('dialogData', dialogData)
                #m_edittrade.AdditionalInfo().FX_BreachReason(resultDict.At('dialogData')) #why did we have this / what operation
                return resultDict 
            else:
                return None  

    return params 
'''================================================================================================
================================================================================================'''
def ael_custom_dialog_main(parameters, dictExtra): return dictExtra
'''================================================================================================
================================================================================================'''
def GetFrame(Shell):
    for Application in acm.ApplicationList():
        if Application.Shell() == Shell:
            return Application
    return None
'''================================================================================================
================================================================================================'''
'''


[ABSA FX]FCurrency:ValidationTemp =
  DisplayName=TradeValidation
  Module=FTradeValidation
'''

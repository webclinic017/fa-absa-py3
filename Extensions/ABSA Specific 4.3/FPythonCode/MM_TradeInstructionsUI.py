"""

Initial implementation
======================

Department: Money Market Desk,Operations
Requesters: Elaine Visagie
Developers: Johann Duvenage


History
=======

2017-10-02 Johann Duvenage                      ABITFA-4803: Capture a unique trade instruction and place settlements on Hold based on the logic caputed as trade instruction.
2018-04-17 Willie vd Bank       CHG1000369571   Updated so that settlement add_infos will be updated even if they aren't in Authorised status.
2018-07-06 Tawanda Mukhalela                    Added end date check for none banking day maturity dates
2019-04-18 Cuen Edwards                         FAOPS-425: Removal of direct updates to settlements.
2019-06-24 Cuen Edwards                         FAOPS-541: Updated validations to support ceded deposits.
"""

import acm	
import FUxCore
import FCallDepositCustom
from at_logging import getLogger
from at_ux import msg_dialog
from FCallDepositFunctions import numstr_to_float
LOGGER = getLogger(__name__)


SETTLE_TYPE_ADD_INFO = 'Settle_Type'
SETTLE_INSTRUCT_ADD_INFO = 'Settle_Instruct'
ACCOUNT_CEDED_ADD_INFO = 'MM_Account_Ceded'


def getPeriod(instrument, start, period_key):
    
    # Define a function to determine the start and end date of a new term trade based on logic provided in the GUI.
    leg = instrument.Legs().First()
    
    period = None
    if period_key in period_dict.keys():
        period = period_dict[period_key]
        
    if not period:
        difference = acm.Time.DateDifference(leg.EndDate(), leg.StartDate())
        period = (0, 0, difference)
        if difference >= 360:
            years = int(round((difference / 365.0), 0))
            period = (years, 0, 0)
        else:
            months = int(round((difference/30.5), 0))
            period = (0, months, 0)
        if period == (0, 0, 0):
            period = (0, 0, difference)
            
    if start == start_options[0]:
        startDate = leg.EndDate()
        calInfo = instrument.Currency().Calendar().CalendarInformation()
        if calInfo.IsNonBankingDay(startDate):
            startDate = calInfo.AdjustBankingDays(startDate, 1)
    else:
        startDate = start
    y, m, d = period
    endDate = acm.Time.DateAddDelta(startDate, y, m, d)
    calendar = instrument.Currency().Calendar()
    if  calendar.CalendarInformation().IsNonBankingDay(endDate):
        endDate= calendar.ModifyDate(None, None, endDate, 'Mod. Following')
        
    if str("-") in period_key:
        endDate = period_key
        if  calendar.CalendarInformation().IsNonBankingDay(endDate):
            endDate= calendar.ModifyDate(None, None, endDate, 'Mod. Following')
    
   
    return startDate, endDate
    

def CopyCalendars(sourceLeg, targetLeg):

    # Define a function to copy all the calendars from the maturing trade.

    targetLeg.PayCalendar(sourceLeg.PayCalendar())
    if sourceLeg.Pay2Calendar():
        targetLeg.Pay2Calendar(sourceLeg.Pay2Calendar())
        
    if sourceLeg.Pay3Calendar():
        targetLeg.Pay3Calendar(sourceLeg.Pay3Calendar())
        
    if sourceLeg.Pay4Calendar():
        targetLeg.Pay4Calendar(sourceLeg.Pay4Calendar())


def getCallAccountByCounterparty(party_name):

    INVALID_STATUSES = ['Void', 'Simulated', 'Terminated']
    
    query = acm.CreateFASQLQuery('FTrade', 'AND')
            
    op = query.AddOpNode('AND')
    op.AddAttrNode('Instrument.InsType', 'EQUAL', acm.EnumFromString('InsType', 'Deposit'))
    op = query.AddOpNode('AND')
    op.AddAttrNode('Instrument.OpenEnd', 'EQUAL', acm.EnumFromString('OpenEndStatus', 'Open End'))
    
    op = query.AddOpNode('AND')
    op.AddAttrNode('Quantity', 'NOT_EQUAL', -1)
    op = query.AddOpNode('AND')
    for status in INVALID_STATUSES:
        op.AddAttrNode('Status', 'NOT_EQUAL', acm.EnumFromString('TradeStatus', status))
    party = acm.FParty[party_name]
    if party:
        op = query.AddOpNode('AND')
        op.AddAttrNode('Counterparty.Oid', 'EQUAL', party.Oid())
        
        return query.Select().Flatten()
    else:
        
        return acm.FSortedCollection().Flatten()

        
def getAllCallAccountsCounterparties():

    INVALID_STATUSSES = ['Void', 'Simulated', 'Terminated']
    
    query = acm.CreateFASQLQuery('FTrade', 'AND')
            
    op = query.AddOpNode('AND')
    op.AddAttrNode('Instrument.InsType', 'EQUAL', acm.EnumFromString('InsType', 'Deposit'))
    op = query.AddOpNode('AND')
    op.AddAttrNode('Instrument.OpenEnd', 'EQUAL', acm.EnumFromString('OpenEndStatus', 'Open End'))
    op = query.AddOpNode('AND')
    op.AddAttrNode('Quantity', 'NOT_EQUAL', -1)
    op = query.AddOpNode('AND')
    for status in INVALID_STATUSSES:
        op.AddAttrNode('Status', 'NOT_EQUAL', acm.EnumFromString('TradeStatus', status))
        
    trades = query.Select()
    
    counterparties = ()
    for trade in trades:
        counterparties+=(trade.Counterparty().Name(),)
        
    #remove duplicates.
    counterparties = tuple([item for index, item in enumerate(counterparties) if item not in counterparties[:index]])
    return counterparties


def setTermSettlementInstruction(instruction, amount, trade):
    cash_flows = getCashFlowsAffectedByInstruction(trade.Instrument(), instruction)
    if not cash_flows:
        raise ValueError('No term cash flows found that are affected by the instruction.')
    for cash_flow in cash_flows:
        validateCashFlowEligibleForSettlementInstruction(trade, cash_flow)
        setCashFlowSettlementInstruction(instruction, amount, cash_flow)


def getCashFlowsAffectedByInstruction(instrument, instruction):
    cash_flows = list()
    today = acm.Time.DateToday()
    for cash_flow in instrument.MainLeg().CashFlows().AsArray():
        if cash_flow.PayDate() != today:
            continue
        if not doesInstructionAffectCashFlow(cash_flow, instruction):
            continue
        cash_flows.append(cash_flow)
    return cash_flows


def doesInstructionAffectCashFlow(cash_flow, instruction):
    cash_flow_type = cash_flow.CashFlowType()
    if cash_flow_type == 'Fixed Amount':
        return 'Capital' in instruction or 'Multiple' in instruction
    elif cash_flow_type in ['Fixed Rate', 'Float Rate']:
        return 'Interest' in instruction or 'Multiple' in instruction
    return False


def validateCashFlowEligibleForSettlementInstruction(trade, cash_flow):
    cash_flow_type = cash_flow.CashFlowType()
    # Prevent setting of instruction for cash flows that already have
    # settlement details specified.
    current_settle_type = cash_flow.AddInfoValue(SETTLE_TYPE_ADD_INFO)
    if current_settle_type:
        message = "Term '{cash_flow_type}' cash flow {cash_flow_oid} already "
        message += "set to '{addinfo_value}'."
        raise ValueError(message.format(
            cash_flow_type=cash_flow_type,
            cash_flow_oid=cash_flow.Oid(),
            addinfo_value=current_settle_type
        ))
    # Prevent setting of instruction for cash flows that do not have
    # settlements eligible for update if the account is not ceded.
    account_ceded = trade.AddInfoValue(ACCOUNT_CEDED_ADD_INFO)
    if not account_ceded and not hasSettlementsEligibleForUpdate(trade, cash_flow):
        message = "Term '{cash_flow_type}' cash flow {cash_flow_oid} has no "
        message += "settlements eligible for update."
        raise ValueError(message.format(
            cash_flow_type=cash_flow_type,
            cash_flow_oid=cash_flow.Oid()
        ))


def setCashFlowSettlementInstruction(instruction, amount, cash_flow):
    # Set settlement details.
    instrument_image = cash_flow.Leg().Instrument().StorageImage()
    cash_flow_image = getCashFlowStorageImageByOid(instrument_image, cash_flow.Oid())
    cash_flow_image.AddInfoValue(SETTLE_TYPE_ADD_INFO, instruction)
    if 'Partial' in instruction or 'Multiple' in instruction:
        cash_flow_image.AddInfoValue('Settle_Amount', numstr_to_float(str(amount)))
    instrument_image.Commit()


def hasSettlementsEligibleForUpdate(trade, cash_flow):
    select_expression = 'trade = {trade_oid} and cashFlow = {cash_flow_oid}'.format(
        trade_oid=trade.Oid(),
        cash_flow_oid=cash_flow.Oid()
    )
    for settlement in acm.FSettlement.Select(select_expression).AsArray():
        if settlement.Status() not in ['Authorised', 'Exception']:
            continue
        settle_instruct = settlement.AddInfoValue(SETTLE_INSTRUCT_ADD_INFO)
        if not settle_instruct:
            return True
    return False


def getCashFlowStorageImageByOid(instrument_image, cash_flow_oid):
    for cash_flow_image in instrument_image.MainLeg().CashFlows().AsArray():
        if cash_flow_image.OriginalOrSelf().Oid() == cash_flow_oid:
            return cash_flow_image
    return None


def createNewDeposit(trade, amount, startNewTrade, period, settleInstruct):
    
    # Create a new deposit Instrument and Trade based on another exiting Deposit Instrument and Trade.
     
    oldDepIns = trade.Instrument()
    oldDepTrade = trade
    
    # Create a new deposit instrument
    newDepIns = acm.DealCapturing.CreateNewInstrument('Deposit')

    # Set infomation on the new instrument
    newDepIns.ValuationGrpChlItem(oldDepIns.ValuationGrpChlItem())
    newDepIns.DiscountingType(oldDepIns.DiscountingType())
    newDepIns.QuoteType(oldDepIns.QuoteType())
    newDepIns.SpotBankingDaysOffset(oldDepIns.SpotBankingDaysOffset())
    newDepIns.RoundingSpecification(oldDepIns.RoundingSpecification())
    newDepIns.SettleCategoryChlItem(oldDepIns.SettleCategoryChlItem())
    newDepIns.SettlementCalendar(oldDepIns.SettlementCalendar())
    newDepIns.ContractSize(abs(amount))
    newDepIns.Currency(oldDepIns.Currency())

    # Set leg start and end dates as well as other instrument information on the first leg
    newStartDate, newEndDate = getPeriod(oldDepIns, startNewTrade, period)
    firstLeg = newDepIns.Legs()[0]
    sourceFirstLeg = oldDepIns.Legs()[0]
    firstLeg.StartDate(newStartDate)
    firstLeg.EndDate(newEndDate)
    firstLeg.DayCountMethod(sourceFirstLeg.DayCountMethod())
    firstLeg.RollingPeriod(sourceFirstLeg.RollingPeriod())
    firstLeg.RollingPeriodBase(sourceFirstLeg.RollingPeriodBase())
    firstLeg.RollingPeriodCount(sourceFirstLeg.RollingPeriodCount())
    firstLeg.RollingPeriodUnit(sourceFirstLeg.RollingPeriodUnit())
    firstLeg.RollingPeriodBase(newEndDate)
    CopyCalendars(sourceFirstLeg, firstLeg)
    firstLeg.LegType(sourceFirstLeg.LegType())
    firstLeg.AmortType(sourceFirstLeg.AmortType())
    firstLeg.FixedRate(sourceFirstLeg.FixedRate())

    firstLeg.AmortGeneration()

    # Suggest a new name for the instrument
    #newDepIns.Name(newDepIns.SuggestName())

    # Generate cash flows
    firstLeg.GenerateCashFlows(0, False, False)

    # Display the instrument after instrument updates
    #acm.StartApplication('Bond', newDepIns)

    # Create new trade linked to newly created deposit instrument
    newTrade = acm.DealCapturing.CreateNewTrade(newDepIns)

    # Set Front Office information on the new trade
    if amount > 0:
        quantity = -1.0
    else:
        quantity = 1.0
        
    newTrade.Quantity(quantity)
    newTrade.Counterparty(oldDepTrade.Counterparty())
    newTrade.Acquirer(oldDepTrade.Acquirer())
    newTrade.TradeTime(newStartDate)
    newTrade.ValueDay(newStartDate)
    newTrade.AcquireDay(newStartDate)

    # Set Back Office information on the new trade
    newTrade.ContractTrade(oldDepTrade)
    newTrade.ConnectedTrade(oldDepTrade.Oid())

    # Set Additional Info on the new trade
    newTrade.AdditionalInfo().Trade_Instruct(settleInstruct)

    # Start a new instrument application
    x = acm.StartApplication('Bond', newTrade)
    x.EditTrade().Quantity(quantity + 1)
    x.EditTrade().Quantity(quantity)
    
        
# -------------------------------------------------------------------------
# Define all lists and dictionaries. 
# -------------------------------------------------------------------------

term_settlement_types = [
    "",
    "Term To Term: Capital and Interest",
    "Term To Term: Capital",
    "Term To Term: Interest",
    "Term To Term: Partial Capital and Interest",
    "Term To Term: Partial Capital",
    "Term To Call: Capital and Interest",
    "Term To Call: Capital",
    "Term To Call: Interest",
    "Term To Call: Partial Capital and Interest",
    "Term To Call: Partial Capital",
    "Term To Multiple",
    "Pay Out : Capital and Interest",
    "Pay Out : Capital",
    "Pay Out : Interest"
]

period_list = [
    "",
    "Same as original Deposit",
    "1 Month",
    "3 Months",
    "6 Months",
    "9 Months",
    "1 Year",
    "2 Years",
    "Other"
]

start_options = [
    acm.Time.DateToday()
]
                
period_dict = {
    "Same as original Deposit": None,
    "1 Month": (0, 1, 0),
    "3 Months": (0, 3, 0),
    "6 Months": (0, 6, 0),
    "9 Months": (0, 9, 0),
    "1 Year": (1, 0, 0),
    "2 Years": (2, 0, 0)
}


counterparty_list = getAllCallAccountsCounterparties()

# -------------------------------------------------------------------------
# Define a class for the Money Markets - Trade Instructions dialog.
# -------------------------------------------------------------------------
	
class MMSettlementUI( FUxCore.LayoutDialog ):	
   
    def __init__( self, trade_row, eii, shell):			
        self.tradeinstructCtrl = None
        self.trade = trade_row.Trade()
        self.startDate = None
        self.newPeriod = None
        self.counterParties = None
        self._amoutCrtl = None
        self.periodCtrl = None
        self.callAccounts = None
        self.eii = eii
        self.shell = shell
        #self._tradeCrtl = None
        self._InitDataBindingControls()

    @FUxCore.aux_cb
    def HandleApply(self):
        try:
            newStartDate = self.startDate.GetData()

            if self.periodCtrl.GetValue():
               newPeriod = self.periodCtrl.GetValue()
            else:
                newPeriod = self.newPeriod.GetData()

            #counterParty = self.counterParties.GetData()
            #self.callAccounts = getCallAccountByCounterparty(counterParty)
            newAmount = self._amoutCrtl.GetValue()
            callAccounts = self.callAccounts
            settlementInstruct = self.tradeinstructCtrl.GetData()
            oldTrade = self.trade

            if "Term To Term" in settlementInstruct:
                if newStartDate and newPeriod and newAmount:
                    setTermSettlementInstruction(settlementInstruct, newAmount, oldTrade)
                    createNewDeposit(oldTrade, newAmount, newStartDate, newPeriod, settlementInstruct)
                else:
                    raise ValueError("Insufficient trade information provided.")

            elif "Term To Call" in settlementInstruct:
                if self.counterParties.GetData() != "":
                    if self.callAccounts.GetData() != "":
                        callAccount_id = self.callAccounts.GetData()
                        callAccount = acm.FInstrument.Select("name = '%s'"%(callAccount_id)).At(0)
                        callAccount_id = self.callAccounts.GetData()
                    else:
                        raise ValueError("Insufficient trade information provided.")
                else:
                    raise ValueError("Insufficient trade information provided.")

                if newAmount and callAccount_id:
                    if callAccount.Trades()[0]:
                        #oldTrade.AdditionalInfo().Trade_Instruct(settlementInstruct)
                        #oldTrade.Commit()
                        setTermSettlementInstruction(settlementInstruct, newAmount, oldTrade)
                        callAccountT = callAccount.Trades()[0]
                        dialog = FCallDepositCustom.create_call_deposit_menu_item([self.eii, callAccountT])
                        dialog.Invoke([self.eii, callAccountT, settlementInstruct, newAmount])
                    else:
                        raise ValueError("No trade found on Call Account provided.")
                else:
                    raise ValueError("Insufficient trade information provided.")

            elif "Term To Multiple" in settlementInstruct:
                callAccount_id = None
                if self.callAccounts.GetData()!="":
                    callAccount_id = self.callAccounts.GetData()
                    callAccount = acm.FInstrument.Select("name = '%s'"%(callAccount_id)).At(0)
                if newStartDate and newPeriod and newAmount and callAccount_id:
                    if callAccount.Trades()[0]:
                        setTermSettlementInstruction(settlementInstruct, newAmount, oldTrade)
                        createNewDeposit(oldTrade, newAmount, newStartDate, newPeriod, settlementInstruct)
                        callAccountT = callAccount.Trades()[0]
                        dialog = FCallDepositCustom.create_call_deposit_menu_item([self.eii, callAccountT])
                        dialog.Invoke([self.eii, callAccount, settlementInstruct, newAmount])
                    else:
                        raise ValueError("No trade found on Call Account provided.")
                else:
                    raise ValueError("Insufficient trade information provided.")

            elif "Pay Out" in settlementInstruct:
                setTermSettlementInstruction(settlementInstruct, newAmount, oldTrade)

            elif "" in settlementInstruct:
                setTermSettlementInstruction(settlementInstruct, newAmount, oldTrade)
                oldTrade.AdditionalInfo().Trade_Instruct("")
            return settlementInstruct, newAmount

        except Exception as exception:
            LOGGER.exception(exception)
            msg_dialog(str(exception), type_="Error", shell=self.shell)
            return None
        
    def HandleDestroy( self ):
        return None

    def CreateLayout( self ):	
        b = acm.FUxLayoutBuilder()	
        b.BeginVertBox('None')	
        b.  BeginHorzBox('EtchedIn', 'Trade Instruction')	
        b.    AddOption('settIns', 'Trade Instruction', 40, 40) 
        b.  EndBox()
        b.  BeginVertBox('EtchedIn', 'Trade Spesifics - New Trade')
        b.    AddOption('startDate', 'New Deposit Start Date*:')  
        b.  BeginHorzBox('EtchedIn', '')
        b.    AddOption('period', 'New Deposit Period*:')
        self.periodCtrl.BuildLayoutPart(b, 'Other*:')
        b.  EndBox()
        self._amoutCrtl.BuildLayoutPart(b, 'Reinvestment Amount*:')
        b.  EndBox()
        b.  BeginVertBox('EtchedIn', 'Trade Specifics - Call Account')
        b.      AddOption('counterparty', 'Counter Party:')
        b.      AddOption('callaccount', 'Call Account ID:')
        b.  EndBox()
        b.  BeginHorzBox('None')	
        b.    AddButton('ok', 'OK', True)	
        b.    AddButton('cancel', 'Cancel', True)	
        b.  EndBox()	
        b.EndBox()	
        return b        
	
    def _InitDataBindingControls(self):
        self._bindings = acm.FUxDataBindings()
        formatter = acm.Get('formats/LimitValues')
        self._amoutCrtl = self._bindings.AddBinder('amount', 'double', formatter)
        #self._tradeCrtl = self._bindings.AddBinder('insCtrl', acm.GetDomain('FInstrument'), None)
        self.periodCtrl = self._bindings.AddBinder('defaultDateCtrl', acm.GetDomain('date'), None) 
        self._bindings.AddDependent(self)
        
    def HandleCreate( self, dlg, layout):	
        self.fuxDlg = dlg	
        self.fuxDlg.Caption('Money Markets - Trade Instructions' )	
        self.layout = layout	
        self.binder = acm.FUxDataBindings()
        gc = self.layout.GetControl
        
        self.tradeinstructCtrl = gc('settIns')
        self.startDate = gc('startDate')
        self.newPeriod  = gc('period')
        self.counterParties = gc('counterparty')
        self.callAccounts = gc('callaccount')
        self._amoutCrtl.InitLayout(self.layout)
        self.periodCtrl.InitLayout(self.layout)
        self._bindings.AddLayout(layout)

        self.tradeinstructCtrl.AddCallback('Changed', self.updateControls, None)
        self.counterParties.AddCallback('Changed', self.updateControls, None)
        self.newPeriod.AddCallback('Changed', self.updateControls, None)

        # Johann : Setup drop down lists
        
        for st in term_settlement_types:
            
            self.tradeinstructCtrl.AddItem(st)

        self.startDate.AddItem(start_options[0])

        for per in period_list:	
            self.newPeriod.AddItem(per)
        
        sortedList = sorted(counterparty_list)
        for party in sortedList:
            self.counterParties.AddItem(party)
       
            
    # -------------------------------------------------------------------------
    # Define callback functions.
    # -------------------------------------------------------------------------
    
    def updateControls( self,*_):
        self.startDate.Editable(False)
        self.newPeriod.Editable(False)
        self.callAccounts.Editable(False)
        self.periodCtrl.Editable(False)
        self.periodCtrl.SetValue("")
        self.counterParties.Editable(True)
        self.startDate.SetData("")
        self.startDate.Editable(False)
                      
        self.callAccounts.Clear()
        call_deposits_list = getCallAccountByCounterparty(self.counterParties.GetData())
        
        for call_deposit in call_deposits_list:
            self.callAccounts.AddItem(call_deposit.Instrument().Name())

        if "Capital and Interest" in self.tradeinstructCtrl.GetData():
            if "Partial" in self.tradeinstructCtrl.GetData():
                self._amoutCrtl.SetValue("")
            else:
                self.amount = self.trade.EndCash()*-1
                self._amoutCrtl.SetValue(round(self.amount, 2))
            
            
        elif "Capital" in self.tradeinstructCtrl.GetData():
            if "Partial" in self.tradeinstructCtrl.GetData():
                self._amoutCrtl.SetValue("")
            else:
                nom = -1 * self.trade.Quantity() * self.trade.Instrument().ContractSize()
                self._amoutCrtl.SetValue(round(nom, 2))
            
        elif "Interest" in self.tradeinstructCtrl.GetData():
            calcSpace = acm.Calculations().CreateCalculationSpace(acm.GetDefaultContext(), 'FDealSheet')
            calculation = calcSpace.CreateCalculation(self.trade, 'Portfolio Interest End', )
            self.amount = calculation.Value()*-1
            
            self._amoutCrtl.SetValue(round(self.amount, 2))
           
            
        if "Term To Term" in self.tradeinstructCtrl.GetData():
            self.startDate.SetData(acm.Time.DateToday())
            self.newPeriod.Editable(True)
            self.counterParties.Editable(False)
            if self.newPeriod.GetData()=='' or self.newPeriod.GetData()=='Other':
                self.periodCtrl.Editable(True)
                
                
            
        if "Term To Call" in self.tradeinstructCtrl.GetData():
            self.callAccounts.Editable(True)
        if "Term To Multiple" in self.tradeinstructCtrl.GetData():
            self.startDate.SetData(acm.Time.DateToday())
            self._amoutCrtl.Editable(True)
            self.newPeriod.Editable(True)
            self.callAccounts.Editable(True)
            if self.newPeriod.GetData()=='' or self.newPeriod.GetData()=='Other':
                self.periodCtrl.Editable(True)
            
        if "Partial" in self.tradeinstructCtrl.GetData():
            self._amoutCrtl.Editable(True)
            self.amount = self._amoutCrtl.GetValue()
        if "Pay Out" in self.tradeinstructCtrl.GetData():
            self.newPeriod.Editable(False)
            self.callAccounts.Editable(False)
            self.periodCtrl.Editable(False)
            self.periodCtrl.SetValue("")
            self.counterParties.Editable(False)
            self._amoutCrtl.Editable(False)
            if "Other" in self.tradeinstructCtrl.GetData():
                self._amoutCrtl.Editable(True)
                self._amoutCrtl.SetValue(0.0)
                
            
            
# -------------------------------------------------------------------------
# Start dialog from menu.
# -------------------------------------------------------------------------

def getTradeInstruction(trade):
    
    settlements = trade.Settlements()
    for settlement in settlements:
        if settlement.AdditionalInfo().Settle_Instruct():
            if "Capital and Interest" in settlement.AdditionalInfo().Settle_Instruct():
                return settlement.AdditionalInfo().Settle_Instruct()
            elif "Capital" in settlement.AdditionalInfo().Settle_Instruct():
                return settlement.AdditionalInfo().Settle_Instruct()
            else:
                return settlement.AdditionalInfo().Settle_Instruct()


def StartDialogFromMenu(eii):
    shell = eii.ExtensionObject().Shell()	
    trdManager = eii.ExtensionObject()	
    sheet = trdManager.ActiveSheet()	
    selection = sheet.Selection()	
    selectedCell = selection.SelectedCell()	
    trade = selectedCell.BusinessObject()	
    customDlg = MMSettlementUI(trade, eii, shell)	
    result=acm.UX().Dialogs().ShowCustomDialogModal( shell, customDlg.CreateLayout(), customDlg )

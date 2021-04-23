import acm
import FUxCore
import datetime


doubleCast = acm.GetFunction('double', 1)

def ReallyStartDialog( shell, trade ):
    brokerSplitDlg = BrokerSplitDialog( trade )
    brokerSplitDlg.InitControls()
    acm.UX().Dialogs().ShowCustomDialogModal( shell, brokerSplitDlg.CreateLayout(GetMaxPartyWidth()), brokerSplitDlg )

def StartDialog( eii ):
    activeSheet = eii.ExtensionObject().ActiveSheet()
    cell = activeSheet.Selection().SelectedCell()
    if cell:
        rowObject = cell.RowObject()
        try:
            instrOrTrade = rowObject.SingleInstrumentOrSingleTrade()
        except:
            instrOrTrade = None
        shell = eii.ExtensionObject().Shell()
        if (instrOrTrade and instrOrTrade.IsKindOf('FTrade')):
            if IsCounterpartyBroker(instrOrTrade):
                ins = instrOrTrade.Instrument()
                if IsInstrumentExpired(ins):
                    acm.UX().Dialogs().MessageBoxInformation(shell, 'Expired instruments cannot be Broker split')
                else:
                    if IsInstrumentExcluded(ins):
                        acm.UX().Dialogs().MessageBoxInformation(shell, 'Call Deposit/Loan cannot be Broker split')
                    elif IsFXSwapOrGrouping(instrOrTrade):
                        acm.UX().Dialogs().MessageBoxInformation(shell, 'FX Swap or Other Grouping trades cannot be Broker split')
                    else:
                        ReallyStartDialog( shell, instrOrTrade );
            else:
                acm.UX().Dialogs().MessageBoxInformation(shell, 'Counterparty has to be the same as the Broker')    
        else:
            acm.UX().Dialogs().MessageBoxInformation(shell, 'Broker Split is allowed only for Trades')    

def GetMaxPartyWidth():
    parties = GetAllParties()
    width = 5
    for p in parties:
        if width < len(p.Name()):
            width = len(p.Name())
    return width
    
def GetAllParties():
    whereClause = "type = 1"
    return acm.FParty.Select( whereClause ).AsArray().Sort()

def IsFXSwapOrGrouping(trade):
    return trade.TradeProcess() != 0 and trade.TradeProcess() != 4096 and trade.TradeProcess() != 8192

def IsCounterpartyBroker(trade):
    return trade.Broker() and trade.Broker() == trade.Counterparty()

def IsInstrumentExpired(ins):
    result = 0
    today = acm.Time.DateNow()
    if ins.ExpiryDate() and ins.ExpiryDate() < today:
        result = 1
    return result

def IsInstrumentExcluded(ins):
    result = 0
    legs = ins.Legs()
    if legs:
        leg = legs.At(0)
    if ins.InsType() == 'Deposit' and ins.OpenEnd() == 'Open End' and leg and \
      (leg.LegType() == 'Call Fixed Adjustable' or leg.LegType() == 'Call Fixed' or leg.LegType() == 'Call Float'): 
        result = 1
    return result

class BrokerSplitDialog( FUxCore.LayoutDialog ):
    def __init__( self, instrOrTrade ):
        self.m_tradeToBrokerSplit = instrOrTrade
        self.m_okBtn = 0
        self.m_trdnbrEdit = 0
        self.m_brokerEdit = 0
        self.m_remainingAmountEdit = 0
        self.m_counterparties = 0
        self.m_splitAmountCtrl = 0
        self.m_quantityIsDerived = instrOrTrade.QuantityIsDerived()
        
    def InitControls(self):
        self.m_bindings = acm.FUxDataBindings()
        self.m_bindings.AddDependent( self )
        self.m_splitAmountCtrl = self.m_bindings.AddBinder( 'splitAmountCtrl', acm.GetDomain('double'), None )
        
    def PopulateData( self ):
        self.m_trdnbrEdit.SetData( self.m_tradeToBrokerSplit.Oid() )
        self.m_brokerEdit.SetData( self.m_tradeToBrokerSplit.Broker() )
        self.m_remainingAmountEdit.SetData(self.GetRemainingAmount())
        self.m_splitAmountCtrl.SetValue( self.GetRemainingAmount() )
        self.m_amountPriorToSplitEdit.SetData( self.GetRemainingAmount() )
        counterparties = GetAllParties()
        self.m_counterparties.Populate( counterparties )

    def GetRemainingAmount( self ):
        contractSize = 1
        if self.m_quantityIsDerived:
            amount = self.m_tradeToBrokerSplit.Premium()
        else:
            amount = self.m_tradeToBrokerSplit.Quantity()
            ins = self.m_tradeToBrokerSplit.Instrument()
            if ins:
                contractSize = ins.ContractSize() 
                amount = amount * contractSize
        return round(amount, 2)
        
    def GetRemainingQuantity( self ):
        amount = doubleCast(self.m_remainingAmountEdit.GetData())
        amount = self.GetQuantity( amount )
        return amount

    def GetQuantity( self, amount ):
        if not self.m_quantityIsDerived:
            ins = self.m_tradeToBrokerSplit.Instrument()
            if ins:
                contractSize = ins.ContractSize()
            if contractSize != 0.0:
                amount = amount / contractSize
        return round(amount, 2)
        
    def UpdateControls(self):
        self.m_trdnbrEdit.Editable( 0 )
        self.m_brokerEdit.Editable( 0 )
        self.m_remainingAmountEdit.Editable( 0 )
        self.m_amountPriorToSplitEdit.Editable( 0 )
        
    def HandleApply( self ):
        self.CreateAndCommitTrades( )
        self.m_fuxDlg.CloseDialogCancel()
    
    def CreateAndCommitTrades( self ):
        acm.BeginTransaction()
        trades = self.CreateNewTrade()
        try: 
            for trade in trades:
                trade.Commit()
            acm.CommitTransaction()
        except:
            acm.AbortTransaction()
            raise
            
    def CreateNewTrade( self ):
        trades = acm.FArray()
        originalQuantity  = self.m_tradeToBrokerSplit.Quantity()
        originalPremium   = self.m_tradeToBrokerSplit.Premium()
        remainingAmount   = self.GetRemainingQuantity()
        if self.m_quantityIsDerived:
            remainingPremium = remainingAmount
            if originalPremium != 0.0:
                fraction = remainingPremium / originalPremium
                remainingQuantity = originalQuantity * fraction
            else:
                fraction = 0.0
                remainingQuangity = 0.0
        else:
            remainingQuantity = remainingAmount
            if originalQuantity != 0.0:
                fraction = remainingQuantity / originalQuantity
                remainingPremium = originalPremium * fraction
            else:
                fraction = 0.0
                remainingPremium = 0.0
        if remainingAmount != 0.0:
            origTrade = self.m_tradeToBrokerSplit
            trade = self.SetTradeQuantityAndPremium(origTrade, round(remainingQuantity, 2), round(remainingPremium, 2))
            trades.Add(trade)
            #trade = self.m_tradeToBrokerSplit.Clone()
            trade = self.MakeCloneTrade(origTrade)
            trade.Counterparty(self.m_counterparties.GetData())
            trade = self.SetTradeQuantityAndPremium(trade, round(originalQuantity * (1 - fraction)), round(originalPremium * (1 - fraction)))
            trades.Add(trade)
        else:
            self.m_tradeToBrokerSplit.Counterparty(self.m_counterparties.GetData())
            trades.Add(self.m_tradeToBrokerSplit)
        return trades    
        
    def MakeCloneTrade( self, trade ):    
        newTrade = acm.FTrade()
        newTrade.AcquireDay(trade.AcquireDay())
        newTrade.Acquirer(trade.Acquirer())
        newTrade.ClsStatus(trade.ClsStatus())
        newTrade.Broker(trade.Broker())
        newTrade.Counterparty(trade.Counterparty())
        newTrade.CreateTime(trade.CreateTime())
        newTrade.CreateUser(trade.CreateUser())
        newTrade.Currency(trade.Currency())
        newTrade.Fee(trade.Fee())
        newTrade.Guarantor(trade.Guarantor())
        newTrade.Haircut(trade.Haircut())
        newTrade.HaircutType(trade.HaircutType())
        newTrade.Instrument(trade.Instrument())
        newTrade.Market(trade.Market())
        newTrade.MatchDay(trade.MatchDay())
        newTrade.OptKey1(trade.OptKey1())
        newTrade.OptKey2(trade.OptKey2())
        newTrade.OptKey3(trade.OptKey3())
        newTrade.OptKey4(trade.OptKey4())
        newTrade.Owner(trade.Owner())
        newTrade.PayAccount1(trade.PayAccount1())
        newTrade.PayAccount2(trade.PayAccount2())
        newTrade.Portfolio(trade.Portfolio())
        newTrade.Price(trade.Price())
        newTrade.QuantityIsDerived(trade.QuantityIsDerived())
        newTrade.Protection(trade.Protection())
        newTrade.Quotation(trade.Quotation())
        newTrade.RecordType(trade.RecordType())
        newTrade.ReferencePrice(trade.ReferencePrice())
        newTrade.SalesCredit(trade.SalesCredit())
        newTrade.SalesMargin(trade.SalesMargin())
        newTrade.SalesPerson(trade.SalesPerson())
        newTrade.SpecialTerms(trade.SpecialTerms())
        newTrade.Status(trade.Status())
        newTrade.Tax(trade.Tax())
        newTrade.Text1(trade.Text1())
        newTrade.Text2(trade.Text2())
        newTrade.TradeProcess(trade.TradeProcess())
        newTrade.TradeTime(trade.TradeTime())
        newTrade.TradeCategory(trade.TradeCategory())
        newTrade.Type(trade.Type())
        newTrade.ValueDay(trade.ValueDay())
        newTrade.Trader(trade.Trader())
        newTrade.YourRef(trade.YourRef())
        newTrade.PointsSalesMargin(trade.PointsSalesMargin())
        return newTrade
        
    
    def SetTradeQuantityAndPremium( self, trade, quantity, premium):
        trade.Quantity( quantity )
        trade.Premium(  round(premium, 2) )
        return trade 

    def ServerUpdate(self, sender, aspectSymbol, parameter):
        split_amount = self.m_splitAmountCtrl.GetValue()
        self.m_remainingAmountEdit.SetData( round(self.GetRemainingAmount() - split_amount, 2) )
        
    def HandleCreate( self, dlg, layout ):
        self.m_fuxDlg = dlg
        self.m_fuxDlg.Caption( 'Broker Split' )    
        self.m_bindings.AddLayout( layout )
        self.m_okBtn = layout.GetControl( "ok" )
        self.m_trdnbrEdit = layout.GetControl( "trdnbr" )
        self.m_brokerEdit = layout.GetControl( "broker" )
        self.m_remainingAmountEdit = layout.GetControl( "remaining_amount" )
        self.m_counterparties = layout.GetControl( "counterparties" )
        self.m_amountPriorToSplitEdit = layout.GetControl("amount_prior_to_split")
        self.PopulateData()
        self.UpdateControls()
               
    def CreateLayout( self, size ):
        b = acm.FUxLayoutBuilder()
        b.BeginVertBox( 'None' )
        b.  BeginVertBox( 'Invisible' )
        b.    AddInput( 'trdnbr', 'Trade Number' )
        b.    AddInput( 'broker', 'Broker' )
        b.    AddInput( 'amount_prior_to_split', 'Amount Prior to Split' )
        b.  EndBox()
        b.  BeginVertBox('EtchedIn', 'Broker Split Details' )
        self.m_splitAmountCtrl.BuildLayoutPart( b, 'Split amount' )
        b.    AddOption( 'counterparties', 'Counterparty', size, size)
        b.  EndBox()
        b.  BeginVertBox( 'Invisible' )
        b.    AddInput( 'remaining_amount', 'Remaining Amount' )
        b.  EndBox()
        b.  BeginHorzBox( 'None' )
        b.    AddFill()
        b.    AddButton( 'ok', 'OK' )
        b.    AddButton( 'cancel', 'Cancel' )
        b.  EndBox()
        b.EndBox()
        return b

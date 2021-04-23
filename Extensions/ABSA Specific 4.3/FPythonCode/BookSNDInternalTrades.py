import acm
import FTradeCreator
from FUploaderUtils import CreateOutput
from at_ux import msg_box

from at_logging import getLogger

logger = getLogger(__name__)

def book_swap_trade(client,acquirer,cpty,portfolio,cpty_portfolio,trxTrade,val_group = None, ins_name = False):
    try:
        trade = client.Clone()
        trade.Acquirer(acm.FParty[acquirer])
        trade.Portfolio(acm.FPhysicalPortfolio[portfolio])
        trade.MirrorPortfolio(acm.FPhysicalPortfolio[cpty_portfolio])
        trade.Counterparty(acm.FParty[cpty])
        trade.TrxTrade(trxTrade)
        for addinf in trade.AddInfoSpecs():
            name =  addinf.Name()
            try:
                setattr(trade.AdditionalInfo(), name, None)
            except:
                continue

        if val_group and ins_name:
            clone = trade.Instrument().Clone()        
            new_name = clone.Name().replace('/external', '')        
            clone.ValuationGrpChlItem(acm.FChoiceList[val_group])
            clone.Name(clone.SuggestName())            
            clone.Commit()
            trade.Instrument(clone)        
        trade.OptionalKey(None)
        trade.Status('Simulated')
        trade.Commit()
        logger.info("Booking new swap for ZCB {}".format(trade.Name()))
        return trade
    except:
        raise

def create_trade(portfolio, instrument, acquirer,mirror,cpty,client,client_facing = False):
    try:
        trade_data = {"Acquirer": acquirer,
                      "MirrorPortfolio": mirror,
                      "Counterparty": cpty,
                      "Instrument": instrument.Name(),
                      "Portfolio": portfolio,
                      "ValueDay": instrument.StartDate(),
                      "AcquireDay": instrument.StartDate(),
                      "Type": 'Normal'}

        trade = FTradeCreator.DecoratedTradeCreator(trade_data).CreateTrade()
        nominal = -1*client.Nominal()
        premium = client.Nominal()
        trade.Premium(premium)
        trade.Nominal(nominal)
        trade.RegisterInStorage()
        if client_facing:
            trade.AdditionalInfo().Approx_46_load('Yes')
            trade.AdditionalInfo().Approx_46_load_ref('4p_3')
            trade.AdditionalInfo().Funding_Instype('FDE')
            trade.AdditionalInfo().InsOverride('Combination - Rates Linked Note')
        else:
            trade.AdditionalInfo().Funding_Instype('CD')
        trade.Commit()
        logger.info("Booking new deposit for ZCB {}".format(trade.Name()))
        return trade
    except:
        raise

def create_leg(instrument, client_leg):
    leg_data = {"FloatRateReference": client_leg.FloatRateReference().Name(),
                "DayCountMethod": client_leg.DayCountMethod(),
                "LegType": 'Float',
                "NominalFactor": 1,
                "StartDate": client_leg.StartDate(),
                "EndDate": client_leg.EndDate(),
                "EndPeriodCount": client_leg.EndPeriodCount(),
                "AmortEndDay": client_leg.AmortEndDay(),
                "AmortStartDay": client_leg.AmortStartDay(),
                "Spread": client_leg.Spread(),
                "ResetPeriodUnit": client_leg.ResetPeriodUnit(),
                "ResetType": client_leg.ResetType(),
                "AmortDaycountMethod": client_leg.AmortDaycountMethod(),
                "ResetPeriodCount": 3,
                "ResetDayMethod": client_leg.ResetDayMethod(),
                "RollingPeriodBase": client_leg.RollingPeriodBase(),
                "ResetDayOffset": 0,
                "Currency": client_leg.Currency().Name(),
                "Rounding": "Normal",
                "NominalAtEnd": True,
                "FloatRateFactor": 1}
    leg = instrument.CreateLeg(1)
    FTradeCreator.TradeCreator.SetProperties(leg, leg_data)

def get_recieve_leg(ins):
    for l in ins.Legs():
        if not l.PayLeg():
            return  l
        
def create_instrument(client):
    try:     
        deposit = acm.FBusinessLogicDecorator.WrapObject(acm.FDeposit())
        deposit.ValuationGrpChlItem(acm.FChoiceList['AC_GLOBAL_Funded'])
        deposit.Quotation('Pct of Nominal')
        deposit.QuoteType('Pct of Nominal')
        leg = get_recieve_leg(client.Instrument())
        create_leg(deposit, leg)
        deposit.RegisterInStorage()
        deposit.Commit()
        return deposit.DecoratedObject()
    except:
        logger.exception("Failed to create deposit instrument")
        raise

def book_deposits(client):
    try:
        trades = []
        ins = create_instrument(client)
        trade1 = create_trade('Liabilities 2474 Complex', ins, 'Funding Desk', 'Funding Mismatch Accrual', 'Funding Desk', client)
        trade1.TrxTrade(trade1.Name())
        trade1.Commit()
        trades.append(trade1)
        trade2 = create_trade('Funding Mismatch FV', ins, client.Acquirer(), client.MirrorPortfolio(), client.Counterparty(), client, True)
        trade2.TrxTrade(trade1.Name())   
        trade2.Commit()
        trades.append(trade2)
        return trades
    except:
        logger.exception("Failed to create deposit trades")
        if len(trades) > 0:
            for t in trades:
                t.Delete()            
        raise
        

def render_output(trades):    
    shell = acm.UX().SessionManager().Shell()
    dlg = CreateOutput('ZCB Trades', trades)
    acm.UX().Dialogs().ShowCustomDialogModal(shell, dlg.CreateLayout(), dlg)

def book_trades(client): 
    try:
        trades = book_deposits(client)
        swap1 =  book_swap_trade(client, 'IRD DESK', 'ABCAP CRT', 'Swap Flow', 'CD_CRT_OIS', trades[0], 'AC_OIS_ZAR', True)
        trades.append(swap1)
        swap2 =  book_swap_trade(client, 'ABCAP CRT', 'STRUCT NOTES DESK', 'CD_EC_IR', 'SND Fair Value', trades[0])
        trades.append(swap2)
        client.TrxTrade(trades[0].Name())
        client.AdditionalInfo().Approx_46_load('Yes')
        client.AdditionalInfo().Approx_46_load_ref('4p_3')
        client.AdditionalInfo().Funding_Instype('FDE')
        client.AdditionalInfo().InsOverride('Combination - Rates Linked Note')
        client.Commit()
        render_output(trades)
    except:  
        if len(trades) > 0:
            logger.exception("Failed to book all ZCB trades")
            msg_box('Failed to book all ZCB trades', 'Error')
            for t in trades:
                t.Delete()
    
    
def book(eii):
    object = eii.ExtensionObject().CurrentObject()
    if object is None:
        msg_box('No Object selected', 'Error')
        return
    elif object.IsKindOf(acm.FTrade):
       book_trades(object)



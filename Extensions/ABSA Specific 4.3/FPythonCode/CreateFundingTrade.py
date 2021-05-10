import acm
import FUxCore
from at_ux import msg_box
from at_logging import getLogger

logger = getLogger(__name__)


class FundingTradeCreator(FUxCore.LayoutDialog):

    def __init__(self, client_trade):
        self.client_trade = client_trade
        self.rate = None
        self.CreateLayout()

    @staticmethod
    def set_val_group(ins):
        if ins.Currency().Name() == 'ZAR':
            val_group = 'AC_GLOBAL_Funded'
        else:
            val_group = 'AC_GLOBAL_{}_DirtyFunded'.format(ins.Currency().Name())
        ins.ValuationGrpChlItem(acm.FChoiceList[val_group])

    @staticmethod
    def add_rate_to_cashflow(instrument, rate):
        leg = instrument.Legs()[0]
        try:
            leg.CashFlows().RemoveAt(0)
            cashflow = leg.CreateCashFlow()
            cashflow.CashFlowType(2)
            cashflow.FixedRate(rate)
            cashflow.StartDate(leg.StartDate())
            cashflow.EndDate(leg.EndDate())
            cashflow.PayDate(leg.EndDate())
            cashflow.NominalFactor(1)
            cashflow.Commit()
            leg.Commit()
        except:
            logger.exception("Failed to book funding trade")

    def book_funding_trade(self):
        rate = self.rate.GetData()
        deposit = self.client_trade.Instrument().Clone()
        leg = deposit.Legs()[0].Clone()
        leg.FixedRate(rate)
        deposit.Legs().RemoveAt(0)
        deposit.Legs().Add(leg)
        deposit.RegisterInStorage()
        deposit.Name(deposit.SuggestName())
        self.set_val_group(deposit)
        deposit.Commit()
        self.add_rate_to_cashflow(deposit, rate)
        funding_trade = self.client_trade.Clone()
        funding_trade.OptionalKey(None)
        funding_trade.RegisterInStorage()
        nominal = -1 * self.client_trade.Nominal()
        premium = abs(self.client_trade.Nominal())
        funding_trade.Nominal(nominal)
        funding_trade.Premium(premium)
        funding_trade.Instrument(deposit)
        funding_trade.Status('Simulated')

        if self.client_trade.Currency().Name() == 'ZAR':
            funding_trade.AdditionalInfo().Funding_Instype('CD')
            funding_trade.Counterparty('Funding Desk')
            funding_trade.MirrorPortfolio('Int Term Fund Econ Alloc')
        else:
            funding_trade.AdditionalInfo().Funding_Instype('CD Non Zar')
            funding_trade.Counterparty('MONEY MARKET DESK')
            funding_trade.MirrorPortfolio('Non Zar Mismatch2')

        funding_trade.Commit()
        logger.info("Booked funding trade {} ".format(funding_trade.Name()))

        mirror = funding_trade.MirrorTrade()
        if self.client_trade.Currency().Name() == 'ZAR':
            mirror.AdditionalInfo().Funding_Instype('CL')
        else:
            mirror.AdditionalInfo().Funding_Instype('CL Non Zar')

        app = acm.StartApplication("Trade", funding_trade)

    def HandleApply(self):
        try:
            self.book_funding_trade()
        except:
            logger.exception("Failed to book funding trade")
        return True

    def HandleCreate(self, dlg, layout):
        '''Runs when the GUI is being created.'''
        gc = layout.GetControl
        self.fux_dialog = dlg
        self.fux_dialog.Caption('Funding Trade Rate')
        self.rate = gc('rate')
        gc("ok").SetFocus()

    def CreateLayout(self):

        b = acm.FUxLayoutBuilder()
        b.BeginVertBox('None')
        b.BeginHorzBox()
        b.AddInput('rate', 'Rate')
        b.EndBox()
        b.BeginHorzBox()
        b.AddButton('ok', 'OK')
        b.AddButton("cancel", "Cancel")
        b.EndBox()
        b.EndBox()

        self.layout = b


def startDialog(eii):
    object = eii.ExtensionObject().CurrentObject()
    if object is None:
        msg_box('No Object selected', 'Error')
        return
    elif object.IsKindOf(acm.FTrade):
        shell = eii.ExtensionObject().Shell()
        customDlg = FundingTradeCreator(object)
        acm.UX().Dialogs().ShowCustomDialogModal(shell,
                                                 customDlg.layout,
                                                 customDlg)

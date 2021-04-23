"""----------------------------------------------------------------------------------------------------------
MODULE                  :       Funding Trade Bridge
PURPOSE                 :       Automate trade booking for the Treasury and Money Markets Desks
DEPARTMENT AND DESK     :       Money Markets
REQUESTER               :       MarilizeJ Knoetze
DEVELOPER               :       Mighty Mkansi
CR NUMBER               :       
-------------------------------------------------------------------------------------------------------------

"""


import acm
import FUxCore
import CorpotrateTradeBooking
import at_time
from InternalCrtBridge import get_existing_bridge_trades

BLUECOLOR = acm.UX().Colors().Create(222, 235, 255)
REDCOLOR = acm.UX().Colors().Create(195, 31, 0)
GREENCOLOR = acm.UX().Colors().Create(30, 170, 30)
    

class CreateClientAndInternalTrades(FUxCore.LayoutDialog):
    """The GUI-managing class."""

    def __init__(self, trade):
        """Init with an acm.FTrade instance."""        
        self.TRADE_STATES = ['Simulated', 'FO Confirmed']
        self.DEFAULT_TRADE_STATE = 'Simulated'

        # prepare the layout
        self.CreateLayout()
        self.trade = trade

        
    def _load_trades(self, *args):   
    
        trade_status = self.fux_trade_status_list.GetData()        
        fixed_rate = self.mm_fixed_rate.GetData()  
        internal_trade_portfolio = self.mm_internal_portfolios.GetData()
        mirror_trade_portfolio = self.mm_mirror_portfolios.GetData()
        internal_trade_acquirer = self.mm_internal_counterparties.GetData()
        mirror_trade_acquirer = self.mm_mirror_counterparties.GetData()
                
        trades = CorpotrateTradeBooking.createClientTrade(self.trade, fixed_rate,  
                                                                    mirror_trade_portfolio, internal_trade_acquirer, 
                                                                    mirror_trade_acquirer, internal_trade_portfolio, 
                                                                    trade_status)
        trade_numbers = []
        for int_trade in trades:
            trade_numbers.append(int_trade.Oid())
        self.mm_new_trades.Populate(trade_numbers)
        
    
    def HandleCreate(self, dlg, layout):
        '''Runs when the GUI is being created.'''

        self.fux_dialog = dlg
        self.fux_dialog.Caption('Funding Trades Bridge')  
            
        self.mm_internal_counterparties = layout.GetControl('internal_counterparties')
        self.mm_internal_counterparties.SetData('Funding Desk')
        
        self.mm_mirror_counterparties = layout.GetControl('mirror_counterparties')  
        self.mm_mirror_counterparties.SetData('Funding Desk')
      
        self.mm_internal_portfolios = layout.GetControl('internal_portfolios')
        self.mm_internal_portfolios.SetData('GROUP FUND 2476')
        
        self.mm_mirror_portfolios = layout.GetControl('mirror_portfolios')
        self.mm_internal_portfolios.SetData('Allocate_Pfolio_GroupFin')
     
        self.mm_fixed_rate = layout.GetControl('fixed_rate')
        
        self.fux_trade_status_list = layout.GetControl('trade_status_list')
        self.fux_trade_status_list.SetData('Simulated')
        
        self.mm_new_trades = layout.GetControl('new_trades')
        self.mm_new_trades.ShowGridLines()
        self.mm_new_trades.ShowColumnHeaders()
        self.mm_new_trades.EnableMultiSelect(True)
        self.mm_create_trades = layout.GetControl("create_trades")
        self.mm_create_trades.AddCallback("Activate", self._load_trades, None)      
        
        self.mm_new_trades.AddColumn('Trade Number')        
               
        self.mm_new_trades.Editable(True)
        self.mm_new_trades.SetColor("Foreground", BLUECOLOR)
        self.mm_new_trades.SetColor("Text", GREENCOLOR)
        self.mm_new_trades.SetStandardFont("Bold")
        
        
        tooltip = ('These are amounts that the acquirer will be receiving. '
                   'Thus a negative amount indicates a pay away '
                   'by the acquirer.')
                
                      
        internal_portfolios = ['Corp Liab 7744 CAPE', 'Corp Liab 7744 DBN', 'Corp Liab 7744 GAUTENG', 'Non ZAR Corporate Deposits']
        self.mm_internal_portfolios.Populate(internal_portfolios)
        
        mirror_portfolios = ['Allocate_Pfolio_GroupFin', 'Liab 2474 - Corp', 'GFTB_Non Zar Deposits']
        self.mm_mirror_portfolios.Populate(mirror_portfolios)       
       
       
        internal_counterparties = ['Funding Desk', 'MONEY MARKET DESK']
        self.mm_internal_counterparties.Populate(internal_counterparties)        
            
        trade_status_listt = ['Simulated', 'FO Confirmed', 'FO Sales']
        self.fux_trade_status_list.Populate(trade_status_listt)        
        
        mirror_counterparties = ['Funding Desk', 'MONEY MARKET DESK']
        self.mm_mirror_counterparties.Populate(mirror_counterparties)
              
        default_trade_state = 'Simulated'
        
        if default_trade_state not in self.TRADE_STATES:
            default_trade_state = self.DEFAULT_TRADE_STATE
        self.fux_trade_status_list.SetData(default_trade_state)

       

        default_currency = acm.FCurrency['ZAR']
        
    def CreateLayout(self):
        """Creates the layout of the GUI dialog."""

        b = acm.FUxLayoutBuilder()
        b. BeginVertBox('None')        
        b. BeginVertBox('EtchedIn', label='Internal Trades Booking')     
                
        b. AddInput('fixed_rate', 'Fixed Rate', 30, 30)        
        b. AddOption('internal_portfolios', 'Portfolio', 30, 30)
        b. AddOption('mirror_portfolios', 'Mirror Trade Portfolio', 30, 30)
        b. AddOption('internal_counterparties', 'Trade Acquirer', 30, 30)
        b. AddOption('mirror_counterparties', 'Mirror Trade Acquirer', 30, 30)
        b. AddOption('trade_status_list', 'Trade status', 30, 30)               
        b. EndBox()      
        b. AddSpace(10)       
        
        b. BeginHorzBox('None')
        b.  AddFill()
        b.  AddButton('create_trades', 'Create trades')
        b.  AddButton('cancel', 'Cancel')
        b. EndBox()
        b.  BeginVertBox('EtchedIn', 'Processed Trades')
        b.    AddList('new_trades', 5, -1, 75, -1)
        b.  EndBox()
        
        b.EndBox()

        self.layout = b

    
def startDialog_cb(eii, *rest):
    """Starts the dialog for comment adding."""
    
    trade = eii.ExtensionObject().CurrentObject()
    if _confirm_action(trade):
        shell = eii.ExtensionObject().Shell()
        customDlg = CreateClientAndInternalTrades(trade)
        acm.UX().Dialogs().ShowCustomDialogModal(shell,
                                                     customDlg.layout,
                                                     customDlg)


def _confirm_action(trade):
    """Checks for already existing bridge trades
    and displays a warning if there are any"""

    # Check if the trade is existing
    dialog_func = acm.GetFunction('msgBox', 3)
    # or trade.Status() in ('Simulated', 'Void')
    if not trade:
        message = 'Trade needs to be saved first.'
        dialog_func('Warning', message, 0)
        return False

    bridge_trades = get_existing_bridge_trades(trade)

    if bridge_trades:
        message = 'There already are existing internal corporate bridge trades:\n'
        for br_trade in bridge_trades:
            message += ' - {0}\n'.format(br_trade.Oid())
        message += 'To add more trades anyway, click OK.'
        buttonSelected = dialog_func('Warning', message, 1)

        return buttonSelected == 1

    return True

class ValidationError(Exception):
    """
    Exception class for raising user errors e.g. invalid arguments and other
    preconditions for running the script.
    """

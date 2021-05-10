import acm
import FUxCore


BLUECOLOR = acm.UX().Colors().Create(222, 235, 255)
REDCOLOR = acm.UX().Colors().Create(195, 31, 0)
GREENCOLOR = acm.UX().Colors().Create(30, 170, 30)
    

class ResidualCapacityBalance(FUxCore.LayoutDialog):
    """The GUI-managing class."""

    def __init__(self, portfolio):
            
        # prepare the layout
        self.CreateLayout()
        self.portfolio = portfolio
        
    def _update_balance(self, *args):  
    
        balance = self.mm_balance.GetData()
        portfolio = self.mm_portfolio.GetData()
        account_max_balance = self.mm_account_max_balance.GetData()
        
        portfolio_object = acm.FPhysicalPortfolio[portfolio]
        updates = []
       
        if balance:      
            portfolio_object.AdditionalInfo().Residual_Capacity(balance)
            portfolio_object.Commit()
            new_threshold = 'Succesfully updated residual balance to %s'%portfolio_object.AdditionalInfo().Residual_Capacity()
            updates.append(new_threshold)
                
        if account_max_balance:            
            portfolio_object.AdditionalInfo().Deposit_Threshold(account_max_balance)
            portfolio_object.Commit()
            new_threshold = 'Succesfully updated threashold to %s'%portfolio_object.AdditionalInfo().Deposit_Threshold()
            updates.append(new_threshold)
        
        self.mm_portfolio_result.Populate(updates)  
          
    def HandleCreate(self, dlg, layout):
        '''Runs when the GUI is being created.'''

        self.fux_dialog = dlg
        self.fux_dialog.Caption('Update Residual Capacity Balance')             
        self.mm_portfolio = layout.GetControl('portfolio') 
        self.mm_balance = layout.GetControl('balance')      
        self.mm_account_max_balance = layout.GetControl('account_max_balance') 
                    
        portfolio = ['Call_0892 CIB GAUTENG', 'Call_Access Deposit Note 370d', 'Call_Access Deposit Note 95d']
        self.mm_portfolio.Populate(portfolio) 
        self.mm_portfolio_update = layout.GetControl("update_balance")
        self.mm_portfolio_update.AddCallback("Activate", self._update_balance, None)  
        
        self.mm_portfolio_result = layout.GetControl('new_balances')
        self.mm_portfolio_result.ShowGridLines()
        self.mm_portfolio_result.ShowColumnHeaders()
        self.mm_portfolio_result.EnableMultiSelect(True)
        
        self.mm_portfolio_result.AddColumn('Update Status')        
               
        self.mm_portfolio_result.Editable(True)
        self.mm_portfolio_result.SetColor("Foreground", BLUECOLOR)
        self.mm_portfolio_result.SetColor("Text", GREENCOLOR)
        self.mm_portfolio_result.SetStandardFont("Bold")
        
        
    def CreateLayout(self):
        """Creates the layout of the GUI dialog."""

        b = acm.FUxLayoutBuilder()
        b. BeginVertBox('None')        
        b. BeginVertBox('EtchedIn', label='Residual')
        b. AddOption('portfolio', 'Portfolio', 30, 30)
        b. AddInput('balance', 'Update Residual Balance', 30, 30)
        b. AddInput('account_max_balance', 'Account Threshold', 30, 30)
        b. EndBox()      
        b. AddSpace(10)       
        b. BeginHorzBox('None')
        b.  AddFill()
        b.  AddButton('update_balance', 'Update')
        b.  AddButton('cancel', 'Cancel')
        b. EndBox()
        b.  BeginVertBox('EtchedIn', 'Result Console')
        b.    AddList('new_balances', 5, -1, 75, -1)
        b.  EndBox()
        b.EndBox()
        self.layout = b

    
def start_dialog(eii, *rest):
    """Starts the dialog for comment adding."""
    
    portfolio = eii.ExtensionObject().CurrentObject()    
    
    shell = eii.ExtensionObject().Shell()
    customDlg = ResidualCapacityBalance(portfolio)
    acm.UX().Dialogs().ShowCustomDialogModal(shell,
                                                 customDlg.layout,
                                                 customDlg)

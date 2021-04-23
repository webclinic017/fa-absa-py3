
"""-----------------------------------------------------------------------------
MODULE
    ps_external_bond_booking

DESCRIPTION
    Date                : 2016-06-14
    Purpose             : Simplify booking of external bond trades via custom form.
    Department and Desk : Prime Services
    Requester           : Eveshnee Naidoo
    Developer           : Ondrej Bahounek
    CR Number           : 3706586
ENDDESCRIPTION

HISTORY
=============================================================================================
Date       Change no    Developer          Description
---------------------------------------------------------------------------------------------
2016-06-14 3706586      Ondrej Bahounek    Initial implementation
2016-09-03 3918920      Ondrej Bahounek    Add Prime Broker checkbox.
2016-12-06 4141341      Ondrej Bahounek    Update filter of recently used parties.
------------------------------------------------------------------------------------------"""

import acm, ael
import FUxCore
import FLogger
from ps_bond_booking import TARGET_PORTFS

logger = FLogger.FLogger(logToConsole=False, logToPrime=True)

BOOKING_STATUS = "FO Confirmed"
SIMULATED_STATUS = "Simulated"

BOOKING_TEXT1 = "PS_ExternalBond"
RISK_PORTF = acm.FPhysicalPortfolio[3498].Name()  # "PB_RISK_FV_CLIENTBONDS"

WHITE_COLOR = acm.UX().Colors().Create(255, 255, 255)
YELLOW_COLOR = acm.UX().Colors().Create(255, 255, 180)


ALLOWED_TYPES = ["Bond", "FRN", "IndexLinkedBond"]


def get_counterparties():
    query = acm.CreateFASQLQuery('FTrade', 'AND')
    query.AddAttrNode('Text1', 'EQUAL', BOOKING_TEXT1)
    query.AddAttrNode('Counterparty.Cid', 'NOT_EQUAL', 'Intern Dept')
    
    qor = query.AddOpNode('OR')
    for portf in TARGET_PORTFS:
        qor.AddAttrNode('Portfolio.Name', 'EQUAL', portf)
        
    # only recently used counterparties
    query.AddAttrNode('TradeTime', 'GREATER', '-2m')
    
    qor = query.AddOpNode('OR')
    for trd_status in ['FO Confirmed', 'BO Confirmed', 'BO-BO Confirmed']:
        qor.AddAttrNode('Status', 'EQUAL', trd_status)
    trades = query.Select()
    return sorted(set(t.Counterparty().Name() for t in trades))


def get_instruments():
    query = acm.CreateFASQLQuery('FTrade', 'AND')
    
    qor = query.AddOpNode('OR')
    for portf in TARGET_PORTFS:
        qor.AddAttrNode('Portfolio.Name', 'EQUAL', portf)
    
    query.AddAttrNode('Text1', 'EQUAL', BOOKING_TEXT1)
    qor = query.AddOpNode('OR')
    for ins_type in ALLOWED_TYPES:
        qor.AddAttrNode('Instrument.InsType', 'EQUAL', ins_type)

    # only recently used trades' instruments
    query.AddAttrNode('TradeTime', 'GREATER', '-2m')
    
    qor = query.AddOpNode('OR')
    for trd_status in ['FO Confirmed', 'BO Confirmed', 'BO-BO Confirmed']:
        qor.AddAttrNode('Status', 'EQUAL', trd_status)
    trades = query.Select()
    return sorted(set(trd.Instrument().Name() for trd in trades))


def run_bond_booking(eii):
    eobj = eii.ExtensionObject()
    shell = eobj.Shell()
    customDlg = EI_CustomDialog()
    builder = customDlg.CreateLayout()
    acm.UX().Dialogs().ShowCustomDialog(shell, builder, customDlg)

    
def _is_banking_day(ins_name, the_date):
    ins = acm.FInstrument[ins_name]
    cal = ins.Currency().Calendar()
    inf = cal.CalendarInformation()
    return not inf.IsNonBankingDay(the_date)


def perform_booking(ins_name, portf_name, cpty_name, quantity, price, trade_date, offset,
    is_prime_broker, trd_status):
    ins = acm.FInstrument[ins_name]
    portf = acm.FPhysicalPortfolio[portf_name]
    cpty = acm.FParty[cpty_name]
    cal = ins.Currency().Calendar()
    
    trade = acm.FTrade()
    trade.Instrument(ins)
    trade.Portfolio(portf)
    trade.Counterparty(cpty)
    trade.Currency(ins.Currency())
    trade.Quantity(quantity)
    trade.Price(price)
    trade.TradeTime(trade_date)
    
    
    settle_date = cal.AdjustBankingDays(trade_date, offset)
    trade.ValueDay(settle_date)
    trade.AcquireDay(settle_date)
    
    trade.Acquirer(acm.FParty['PRIME SERVICES DESK'])  
    trade.Trader(acm.User())
    trade.Status('Simulated')
    trade.Text1(BOOKING_TEXT1)
    trade.PremiumCalculationMethod('Consideration')
    trade.RegisterInStorage()
    
    # PB trades fed into Nutron must have Prime_Broker flag set from 2016-06-20
    if acm.FAdditionalInfoSpec.Select01('name="Prime_Broker"', '') and is_prime_broker:
        trade.AdditionalInfo().Prime_Broker('Yes')

    trade.Commit()
    print("Trade booked: %d" %trade.Oid())

    print("Setting premium and '%s' status..." % trd_status)
    # premium has to be calculated by ael function
    ael_trade = ael.Trade[trade.Oid()]
    premium = ael_trade.premium_from_quote(ael.date(trade.ValueDay()), trade.Price())
    trade.Premium(premium)
    trade.Status(trd_status)
    trade.Commit()    
    
    return trade
    
    
    
class EI_CustomDialog(FUxCore.LayoutDialog):
    
    def __init__(self):
        self.pb_checked = True
        
    def _set_colors(self, color):
        self.m_fuxDlg.SetBackgroundColor(color)
        self.vertbox1.SetColor(0, color)
        self.vertbox2.SetColor(0, color)
        
    def HandleCreate(self, dlg, layout):
        self.m_fuxDlg = dlg
        self.m_fuxDlg.Caption('Prime Services - External Bond Booking')
        
        self.vertbox1 = layout.GetControl('vertbox1')
        self.vertbox2 = layout.GetControl('vertbox2')
        
        # buttons
        self.btnAddInstr = layout.GetControl('btn_add_instr')
        self.btnAddCpty = layout.GetControl('btn_add_cpty')
        self.btnAddPortf = layout.GetControl('btn_add_portf')
        self.btnBook = layout.GetControl('btn_book')
        self.btnClose = layout.GetControl('btn_close')
        
        # inputs
        self.inptTradeQty = layout.GetControl('inpt_trade_qty')
        self.inptTradePrice = layout.GetControl('inpt_trade_price')
        self.inptTradeDate = layout.GetControl('inpt_trade_date')
        self.inptOffsetDate = layout.GetControl('inpt_offset_date')
        
        # option boxes
        self.optInstr = layout.GetControl('opt_instr')
        self.optCpty = layout.GetControl('opt_cpty')
        self.optPortf = layout.GetControl('opt_portf')
        
        # check boxes
        self.chbPrimeBroker = layout.GetControl('chb_prime_br_flag')
        self.chb_simulated = layout.GetControl('chb_simulated')
                

        # ========================
        # setting controls
        
        self.inptTradeDate.SetData(acm.Time.DateToday())
        self.inptOffsetDate.SetData("")

        for ins_name in get_instruments():
            self.optInstr.AddItem(ins_name)

        for cp_name in get_counterparties():
            self.optCpty.AddItem(cp_name)
            
        for portf in TARGET_PORTFS:
            self.optPortf.AddItem(portf)
        
        self.optPortf.SetData(RISK_PORTF)
        
        self.chbPrimeBroker.Checked(self.pb_checked)
        
        self.trd_status = BOOKING_STATUS
        self.chb_simulated.Checked(False)
        self._set_colors(WHITE_COLOR)
        
        # callbacks
        self.btnAddInstr.AddCallback("Activate", self.OnAddInstrButtonPressed, None)
        self.btnAddCpty.AddCallback("Activate", self.OnAddCptyButtonPressed, None)
        self.btnAddPortf.AddCallback("Activate", self.OnAddPortfButtonPressed, None)
        self.btnBook.AddCallback("Activate", self.OnBookButtonPressed, None)
        self.btnClose.AddCallback("Activate", self.OnCloseButtonPressed, None)
        self.optInstr.AddCallback("Changing", self.OnInstrumentSelectionChanged, None)
        self.chbPrimeBroker.AddCallback("Activate", self.OnChbPrimeBrokerChecked, None)
        self.chb_simulated.AddCallback("Activate", self.OnChbSimulatedChecked, None)
        

    def ShowInformation(self, msg):
        """ Show message in information dialog. """
        acm.UX().Dialogs().MessageBoxInformation(self.m_fuxDlg.Shell(), msg)
        
    def ShowError(self, msg):
        """ Show error message box."""
        acm.UX().Dialogs().MessageBox(self.m_fuxDlg.Shell(), 'Error', "Error: " + msg,
            'Cancel', None, None, 'Button1', 'Button1')
            
    def _update_offset(self):
        """ Set spot days offset from selected instrument. """
        ins = self.optInstr.GetData()
        self.inptOffsetDate.SetData(acm.FInstrument[ins].SpotBankingDaysOffset())
        
    def OnChbPrimeBrokerChecked(self, cd, data):
        """Set Prime Broker flag from check box."""
        self.pb_checked = self.chbPrimeBroker.Checked()
        
    def OnChbSimulatedChecked(self, cd, data):
        if self.chb_simulated.Checked():
            self._set_colors(YELLOW_COLOR)
            self.trd_status = SIMULATED_STATUS
        else:
            self._set_colors(WHITE_COLOR)
            self.trd_status = BOOKING_STATUS
        
    def OnInstrumentSelectionChanged(self, cd, data):
        """ Set spot days offset from selected instrument. """
        self._update_offset()
    
    def OnAddCptyButtonPressed(self, cd, data):
        """ Show dialog with all counterparties
            Add counterparty to the counterparty option box.
        """
        parties = acm.FCounterParty.Select('notTrading = False').AsSet()
        parties.Union(acm.FClient.Select('notTrading = False'))
        parties = sorted(parties)

        cpty = acm.UX().Dialogs().SelectObject(self.m_fuxDlg.Shell(),
                                                'Select Counterparty',
                                                'Counterparties',
                                                parties,
                                                None)
        if not cpty:
            return            
        if not self.optCpty.ItemExists(cpty.Name()):
            self.optCpty.AddItem(cpty.Name())
        self.optCpty.SetData(cpty.Name())
        
    def OnAddInstrButtonPressed(self, cd, data):
        """ Show dialog with all instruments
            Add instrument to the instrument option box.
        """
        instruments = []
        for ins_type in ALLOWED_TYPES:
            instrs = acm.FInstrument.Select('insType = "%s" and expiryDate > "%s"' \
                %(ins_type, acm.Time.DateToday()))
            instruments.extend(instrs)

        ins = acm.UX().Dialogs().SelectObject(self.m_fuxDlg.Shell(),
                                                'Select Instrument',
                                                '%s' %ALLOWED_TYPES,
                                                sorted(instruments),
                                                None)
        if not ins:
            return            
        if not self.optInstr.ItemExists(ins.Name()):
            self.optInstr.AddItem(ins.Name())
        self.optInstr.SetData(ins.Name())
        self._update_offset()
            
    def OnAddPortfButtonPressed(self, cd, data):
        """ Show dialog with all portfolios
            Add portfolio to the portfolio option box.
        """
        portfs = sorted(acm.FPhysicalPortfolio.Instances())
        portf = acm.UX().Dialogs().SelectObject(self.m_fuxDlg.Shell(),
                                                'Select Portfolio',
                                                'Portfolios',
                                                portfs,
                                                None)
        if not portf:
            return            
        if not self.optPortf.ItemExists(portf.Name()):
            self.optPortf.AddItem(portf.Name())
        self.optPortf.SetData(portf.Name())
                
    def OnBookButtonPressed(self, cd, data):
        """ Book split trades. """
        logger.LOG("==== Booking started ====")
        try:
            ins = self.optInstr.GetData()
            if not ins:
                raise RuntimeError("Instrument not selected.")
            print("Instrument: '%s'" %ins)
            
            portf = self.optPortf.GetData()
            if not portf:
                raise RuntimeError("Portfolio not selected.")
            print("Portfolio: '%s'" %portf)
                
            cpty = self.optCpty.GetData()
            if not cpty:
                raise RuntimeError("Counterparty not selected.")
            print("Counterparty: '%s'" %cpty)
                
            quantity = self.inptTradeQty.GetData()
            if not quantity:
                raise RuntimeError("Quantity not set.")
            quantity = float(quantity)
            if quantity == 0.0:
                raise RuntimeError("Quantity can't be zero.")
            print("Quantity: %f" %quantity)
                
            price = self.inptTradePrice.GetData()
            if not price:
                raise RuntimeError("Price not set.")
            price = float(price)
            if price == 0.0:
                raise RuntimeError("Price can't be zero.")
            print("Price: %f" %price)
                
            trade_date = self.inptTradeDate.GetData()
            if not trade_date or trade_date == "Today":
                trade_date = acm.Time.DateToday()
            if not _is_banking_day(ins, trade_date):
                raise RuntimeError("Date '%s' is not a banking day." %trade_date)
            print("Date: %s" %trade_date)
            
            offset = self.inptOffsetDate.GetData()
            if not offset:
                raise RuntimeError("Date Offset not set.")
            offset = int(offset)
            if offset < 0.0:
                raise RuntimeError("Incorrect Date Offset value: %d" %offset)
            print("Date Offset: %d" %offset)


            trade = perform_booking(ins, portf, cpty, quantity, price, trade_date,
                offset, self.pb_checked, self.trd_status)
            
            self.ShowInformation("Booking process completed (trade: %d)." %trade.Oid())
            logger.LOG("==== Booking completed ====")
        except Exception as exc:
            self.ShowError("Booking failed: %s" %str(exc))
            raise
    
    def OnCloseButtonPressed(self, cd, data):
        """ Close main dialog. """
        self.m_fuxDlg.CloseDialogOK()
            
    def CreateLayout(self):
        b = acm.FUxLayoutBuilder()
        b.BeginVertBox('None')
        b.  BeginVertBox('EtchedIn', 'External Source trade properties', 'vertbox1')
        b.    BeginHorzBox('None')
        b.      AddOption('opt_instr', 'Instrument:', 50, 50)
        b.      AddButton('btn_add_instr', 'Add...')
        b.    EndBox()
        b.    BeginHorzBox('None')
        b.      AddOption('opt_portf', 'Portfolio:', 50, 50)
        b.      AddButton('btn_add_portf', 'Add...')
        b.    EndBox()
        b.    AddInput('inpt_trade_qty', 'Quantity:', 15, 15)
        b.    AddInput('inpt_trade_price', 'Price:', 15, 15)
        b.    BeginVertBox('EtchedIn', 'Counterparty', 'vertbox2')
        b.      BeginHorzBox('None')
        b.        AddOption('opt_cpty', 'Name:', 50, 50)
        b.        AddButton('btn_add_cpty', 'Add...')
        b.      EndBox()
        b.      AddCheckbox('chb_prime_br_flag', 'Prime Broker?')
        b.    EndBox()
        b.    AddInput('inpt_trade_date', 'Date:', 15, 15)
        b.    AddInput('inpt_offset_date', 'Date Offset T+:', 15, 15)
        b.  EndBox()
        
        b.  AddSpace(10)
        b.  BeginHorzBox('None')
        b.    AddButton('btn_book', 'Book')
        b.    AddSpace(10)
        b.    AddCheckbox('chb_simulated', 'Simulated?')
        b.    AddFill()
        b.    AddButton('btn_close', 'Close')
        b.  EndBox()
        b.EndBox()
        return b
        

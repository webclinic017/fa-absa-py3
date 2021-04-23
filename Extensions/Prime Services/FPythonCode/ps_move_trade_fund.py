"""-----------------------------------------------------------------------------
MODULE
    ps_move_trade_fund

DESCRIPTION
    Date                : 2016-12-06
    Purpose             : Place 'Move trade fund' functionality to FA
    Department and Desk : Prime Services
    Requester           : Eveshnee Naidoo
    Developer           : Ondrej Bahounek
    CR Number           : CHNG0004143940
ENDDESCRIPTION

HISTORY
=============================================================================================
Date        Change no    Developer        Description
---------------------------------------------------------------------------------------------
2016-12-06  4143940    Ondrej Bahounek    Initial implementation. 
                                          Create a 'Fund Move Trade' tool as a replacement
                                          for 'Fund Move Trade' and 'Fin vs FF Move Trade' 
                                          uploaders from PrimeServices_TradeUploader excel 
                                          upload sheet.
2016-12-15  4185370    Ondrej Bahounek    ABITFA-4607
                                          Clear fields when input data combination doesn't 
                                          have any existing portfolio.
                                          Mark fund trades as 'PS No Fees'.
2017-04-10  4485748    Ondrej Bahounek    Corporate CR trades booked on MTM instruments.
2018-05-15  CHG1000460221 O. Bahounek     Add Option for Simulated trades
------------------------------------------------------------------------------------------"""

import acm
import ael
import FUxCore
import FLogger

from PS_Functions import (
                          get_pb_fund_shortname,
                          get_pb_fund_counterparties,
                          get_pb_fund_counterparty)
                          
from ps_bond_booking import (
    GOV_BOND_ISSUER,
    FUNDS_EXTRA_NAMES,
    )

from at_logging import  getLogger, bp_start
LOGGER = getLogger()

ALIASES = None  # will be populated after a dialog for all funds will be opened

ABSA_BANK = acm.FParty[209].Name()  # "ABSA BANK LTD"
ACQUIRER = acm.FParty[32737]  # "PRIME SERVICES DESK"
RISK_PORTF = acm.FPhysicalPortfolio[3498].Name()  # "PB_RISK_FV_CLIENTBONDS"

BOOKING_STATUS = "FO Confirmed"
SIMULATED_STATUS = "Simulated"
BOOKING_TEXT1 = "PSMoveTrade"

ALLOWED_TYPES = ["Bond", "FRN", "IndexLinkedBond"]

GOV_TYPE = "Government"
CORP_TYPE = "Corporate"

FIN_TYPE = "Financed"
FF_TYPE = "FF"

BLUE_COLOR = acm.UX().Colors().Create(55, 55, 255)
GREEN_COLOR = acm.UX().Colors().Create(55, 255, 55)
WHITE_COLOR = acm.UX().Colors().Create(255, 255, 255)
YELLOW_COLOR = acm.UX().Colors().Create(255, 255, 180)


def run(eii):
    eobj = eii.ExtensionObject()
    shell = eobj.Shell()
    custom_dlg = MoveTradeDialog()
    builder = custom_dlg.CreateLayout()
    acm.UX().Dialogs().ShowCustomDialog(shell, builder, custom_dlg)
    
    
def get_instruments():
    query = acm.CreateFASQLQuery('FTrade', 'AND')
    query.AddAttrNode('Portfolio.Name', 'EQUAL', RISK_PORTF)
    #query.AddAttrNode('Text1', 'EQUAL', BOOKING_TEXT1)
    qor = query.AddOpNode('OR')
    for ins_type in ALLOWED_TYPES:
        qor.AddAttrNode('Instrument.InsType', 'EQUAL', ins_type)

    qor = query.AddOpNode('OR')
    for trd_status in ['FO Confirmed', 'BO Confirmed', 'BO-BO Confirmed']:
        qor.AddAttrNode('Status', 'EQUAL', trd_status)
    # only recently used trades' instruments
    query.AddAttrNode('TradeTime', 'GREATER', '-4m')
    trades = query.Select()
    return sorted(set(trd.Instrument() for trd in trades))
    

def get_recent_aliases():
    """Get recent aliases."""
    query = acm.CreateFASQLQuery('FTrade', 'AND')
    query.AddAttrNode('Portfolio.Name', 'EQUAL', RISK_PORTF)
    #query.AddAttrNode('Text1', 'EQUAL', BOOKING_TEXT1)
    
    qor = query.AddOpNode('OR')
    for ins_type in ALLOWED_TYPES:
        qor.AddAttrNode('Instrument.InsType', 'EQUAL', ins_type)
        
    qor = query.AddOpNode('OR')
    for trd_status in ['FO Confirmed', 'BO Confirmed', 'BO-BO Confirmed']:
        qor.AddAttrNode('Status', 'EQUAL', trd_status)
        
    # only recently used counterparties
    query.AddAttrNode('TradeTime', 'GREATER', '-4m')
    
    trades = query.Select()
    cparties = set(t.Counterparty() for t in trades)
    return sorted(get_pb_fund_shortname(cp) for cp in cparties 
                  if cp.Alias("SoftBroker"))
    

def exists_portf(portf_name):
    return acm.FPhysicalPortfolio[portf_name] is not None


def is_gov_bond(bond):
    if isinstance(bond, str):
        bond = acm.FInstrument[bond]
    return bond.Issuer().Name() == GOV_BOND_ISSUER
    
    
def get_issuer_type(acm_bond):
    if is_gov_bond(acm_bond):
        return GOV_TYPE
    return CORP_TYPE
    

def is_banking_day(instrument, the_date):
    if isinstance(instrument, str):
        ins = acm.FInstrument[instrument]
    else:
        ins = instrument        
    cal = ins.Currency().Calendar()
    inf = cal.CalendarInformation()
    return not inf.IsNonBankingDay(the_date)
    
    
def book_trades(trades, trade_date, offset):
    new_trades = []
    chl_no_fees = acm.FChoiceList.Select01('list="TradeKey3" and name="PS No Fees"', '')
    acm.BeginTransaction()
    try:
        for (i, trd_info) in enumerate(trades, 1):
            LOGGER.info("Creating a trade #%d:" %i)
            LOGGER.info("\tParty: '%s'" % trd_info.cparty)
            LOGGER.info("\tPortfolio: '%s'" % trd_info.portfolio)
            LOGGER.info("\tQuantity: %d" % trd_info.quantity)
            
            ins_name = trd_info.instrument
            if trd_info.is_mtm:
                ins_name += "/MTM"
            
            instr = acm.FInstrument[ins_name]
            if not instr:
                raise RuntimeError("Nonexisting instrument '%s'" % ins_name)
            
            
            LOGGER.info("\tInstrument: %s" % instr.Name())
            party = acm.FParty[trd_info.cparty]
            portf = acm.FPhysicalPortfolio[trd_info.portfolio]
            cal = instr.Currency().Calendar()
            settle_date = cal.AdjustBankingDays(trade_date, offset)
            
            trade = acm.FTrade()
            trade.Instrument(instr)
            trade.Currency(instr.Currency())
            trade.Portfolio(portf)
            trade.Counterparty(party)
            trade.Acquirer(ACQUIRER)
            trade.Price(trd_info.price)
            trade.Quantity(trd_info.quantity)
            
            trade.TradeTime(trade_date)
            trade.ValueDay(settle_date)
            trade.AcquireDay(settle_date)
            
            trade.Trader(acm.User())
            trade.Status("Simulated")
            trade.Text1(BOOKING_TEXT1)
            trade.PremiumCalculationMethod('Consideration')
            
            if trade.PortfolioId() != RISK_PORTF:
                trade.OptKey3(chl_no_fees)  # mark fund trades as 'PS No Fees'
            
            trade.Commit()
            
            new_trades.append(trade)
            
        acm.CommitTransaction()
        
    except Exception as exc:
        acm.AbortTransaction()
        raise
        
    return new_trades
    
    
def set_premiums(trades):
    acm.BeginTransaction()
    try:
        for trd in trades:
            ael_trade = ael.Trade[trd.Oid()]
            # TODO: replace with acm
            premium = ael_trade.premium_from_quote(
                        ael.date(trd.ValueDay()), trd.Price())
            trd.Premium(premium)
            trd.Commit()
        acm.CommitTransaction()
    except Exception:
        acm.AbortTransaction()
        raise
    
    
def set_final_status(trades, trd_status):
    
    first_trd = trades[0]
    acm.BeginTransaction()
    try:
        for trd in trades:
            trd.Status(trd_status)
            trd.TrxTrade(first_trd)  # trades from the transaction should be traceable
            trd.Commit()
        acm.CommitTransaction()
    except Exception:
        acm.AbortTransaction()
        raise
        

class MoveTradeDialog(FUxCore.LayoutDialog):
    
        
    def _set_colors(self, color):
        self.m_fuxDlg.SetBackgroundColor(color)
        self.vertbox1.SetColor(0, color)
        self.vertbox2.SetColor(0, color)
        self.vertbox3.SetColor(0, color)
    
    def HandleCreate(self, dlg, layout):
        self.m_fuxDlg = dlg
        self.m_fuxDlg.Caption('Prime Services - Fund Move Trade')
        
        self.vertbox1 = layout.GetControl('vertbox1')
        self.vertbox2 = layout.GetControl('vertbox2')
        self.vertbox3 = layout.GetControl('vertbox3')
        
        self.label_info = layout.GetControl('label_info')
        self.label_info.SetFont("Arial", 12, 1, 0)
        self.label_info.SetAlignment("Center")
        
        # list views
        self.m_list1 = layout.GetControl('list_trades1')
        self.m_list2 = layout.GetControl('list_trades2')
        
        # buttons
        self.btnAddInstr = layout.GetControl('btn_add_instr')
        self.btnAddFund1 = layout.GetControl('btn_add_fund1')
        self.btnAddFund2 = layout.GetControl('btn_add_fund2')
        self.btnBook = layout.GetControl('btn_book')
        self.btnClose = layout.GetControl('btn_close')
        
        # inputs
        self.inptTradeQty = layout.GetControl('inpt_trade_qty')
        self.inptTradePrice = layout.GetControl('inpt_trade_price')
        self.inptTradeDate = layout.GetControl('inpt_trade_date')
        self.inptOffsetDate = layout.GetControl('inpt_offset_date')
        
        # option boxes
        self.optIssuerType = layout.GetControl('opt_issuer_type')
        self.optInstr = layout.GetControl('opt_instr')
        self.optCpty1 = layout.GetControl('opt_cpty1')
        self.optCpty2 = layout.GetControl('opt_cpty2')
        
        # check boxes
        self.chbFF1 = layout.GetControl('chb_ff1')
        self.chbFF2 = layout.GetControl('chb_ff2')
        self.chb_simulated = layout.GetControl('chb_simulated')
                

        # ========================
        # setting controls
        
        self.inptTradeDate.SetData(acm.Time.DateToday())
        self.inptOffsetDate.SetData("")

        for ins in get_instruments():
            self.optInstr.AddItem(ins)

        for cp_alias in get_recent_aliases():
            self.optCpty1.AddItem(cp_alias)
            self.optCpty2.AddItem(cp_alias)
            
       
        self.chbFF1.Checked(True)
        self.chbFF1.Checked(True)
        self.chb_simulated.Checked(False)
        self._set_colors(WHITE_COLOR)
        self.trd_status = BOOKING_STATUS
        
        
        self.optIssuerType.AddItem(GOV_TYPE)
        self.optIssuerType.AddItem(CORP_TYPE)
        
        for m_list in (self.m_list1, self.m_list2):
            m_list.ShowGridLines()
            m_list.ShowColumnHeaders()
            m_list.AddColumn("Quantity", -1, "Trade Quantity")
            m_list.AddColumn("Price", -1, "Trade Price")
            m_list.AddColumn("Fully Funded", -1, "Is fully funded trade?")
            m_list.AddColumn("Counterparty", -1, "Trade Counterparty ")
            m_list.AddColumn("Portfolio", -1, "Trade Portfolio")
            
            m_list.AdjustColumnWidthToFitItems(0)
            m_list.AdjustColumnWidthToFitItems(1)
            m_list.AdjustColumnWidthToFitItems(2)
            m_list.AdjustColumnWidthToFitItems(3)
            m_list.AdjustColumnWidthToFitItems(4)
        
        # callbacks
        self.optInstr.AddCallback("Changing", self.OnInstrumentSelectionChanged, None)
        self.btnAddInstr.AddCallback("Activate", self.OnAddInstrButtonPressed, None)
        self.btnAddFund1.AddCallback("Activate", self.OnAddFundButtonPressed, self.optCpty1)
        self.btnAddFund2.AddCallback("Activate", self.OnAddFundButtonPressed, self.optCpty2)
        self.btnBook.AddCallback("Activate", self.OnBookButtonPressed, None)
        self.btnClose.AddCallback("Activate", self.OnCloseButtonPressed, None)
        self.chb_simulated.AddCallback("Activate", self.OnChbSimulatedChecked, None)
        
        self.inptTradeQty.AddCallback("Changing", self.OnValueChanged, None)
        self.inptTradePrice.AddCallback("Changing", self.OnValueChanged, None)
        self.optIssuerType.AddCallback("Changing", self.OnValueChanged, None)
        self.chbFF1.AddCallback("Changing", self.OnValueChanged, None)
        self.chbFF2.AddCallback("Changing", self.OnValueChanged, None)
        self.optCpty1.AddCallback("Changing", self.OnValueChanged, None)
        self.optCpty2.AddCallback("Changing", self.OnValueChanged, None)
        
        self.SetDefaults()
        self.PopulateData()
        
    def is_valid_instr_and_issuer_type(self):
        if not (self.optIssuerType.GetData() and self.optInstr.GetData()):
            return False
        return True
    
    def _is_gov_bond(self):
        if self.optIssuerType.GetData():
            return self.optIssuerType.GetData() == GOV_TYPE
        raise RuntimeError("Missing issuer type")
        
    def _is_ff1(self):
        return self.chbFF1.Checked() == True
        
    def _is_ff2(self):
        return self.chbFF2.Checked() == True
        
    def _get_alias1(self):
        return self.optCpty1.GetData()
        
    def _get_alias2(self):
        return self.optCpty2.GetData()
        
    def _get_quantity(self):
        quantity = self.inptTradeQty.GetData()
        if not quantity:
            return ""
        quantity = float(quantity)
        if quantity == 0.0:
            raise RuntimeError("Quantity can't be zero.")
        return quantity
        
    def _get_price(self):
        price = self.inptTradePrice.GetData()
        if not price:
            return ""
        price = float(price)
        if price == 0.0:
            raise RuntimeError("Price can't be zero.")
        return price
        
    def _get_fund_portfolio(self, alias, is_fully_funded):
        """Return portfolio name for party, isFF flag portfolio and issuer of a bond.
        There are 4 possible groups:
            Fin-Corp -- [CORPBOND]
            Fin-Gov -- [REPOBOND, GOVIBOND]
            FF-Corp -- [CORPBOND_FF]
            FF-Gov -- [GOVIBOND_FF, NAKEDBOND_FF, NAKEDBOND]

        There should exist only one (or none) portfolio for given input.
        """
        is_government = self._is_gov_bond()        

        if alias in FUNDS_EXTRA_NAMES.keys():
            iss_type_key = GOV_TYPE if is_government else CORP_TYPE
            strategy_key = FF_TYPE if is_fully_funded else FIN_TYPE
            try:
                portf = FUNDS_EXTRA_NAMES[alias][iss_type_key][strategy_key]
            except Exception:
                raise RuntimeError('Nonexisting portfolio (alias:{0}, FF:{1}, isGOV:{2})'
                    .format(alias, is_fully_funded, is_government))
            return portf
            
        ff = 'FF_' if is_fully_funded else ''
        govi_ff_names = ['GOVIBOND_FF', 'NAKEDBOND_FF', 'NAKEDBOND']
        govi_fin_names = ['GOVIBOND', 'REPOBOND']
        portfs_result = []
        if not is_government:
            portf_name = 'PB_CORPBOND_' + ff + alias + '_CR'
            if exists_portf(portf_name):
                portfs_result.append(portf_name)
        else:
            if is_fully_funded:
                for bond_type in govi_ff_names:
                    portf_name = 'PB_' + bond_type + '_' + alias + '_CR'
                    if exists_portf(portf_name):
                        portfs_result.append(portf_name)
            else:
                for bond_type in govi_fin_names:
                    portf_name = 'PB_' + bond_type + '_' + alias + '_CR'
                    if exists_portf(portf_name):
                        portfs_result.append(portf_name)

        if not portfs_result:
            raise RuntimeError('Nonexisting portfolio (alias:{0}, FF:{1}, isGOV:{2})'
                .format(alias, is_fully_funded, is_government))
        if len(portfs_result) > 1:
            raise RuntimeError('Too many candidate portfolios (alias:{0}, FF:{1}, isGOV:{2}): {3}'
                .format(alias, is_fully_funded, is_government, ','.join(portfs_result)))
        return portfs_result[0]
        
    def SetDefaults(self):
        # do nothing, probably not needed
        return
    
    def _check_same_parties(self):
        (alias1, alias2) = (self._get_alias1(), self._get_alias2())
        if alias1 and alias2:
            if alias1 == alias2:
                self.chbFF2.Checked(not self.chbFF1.Checked())
                self.chbFF2.Enabled(False)
                self.label_info.Label("Financed <--> FF move trade")
                self.label_info.SetColor("Text", GREEN_COLOR)
                
            else:
                self.chbFF2.Enabled(True)
                self.label_info.Label("Fund move trade")
                self.label_info.SetColor("Text", BLUE_COLOR)
            
    def _invalidate_form(self):
        """Prevent displaying outdated data and performing booking action."""
        self.m_list1.RemoveAllItems()
        self.m_list2.RemoveAllItems()
        self.btnBook.Enabled(False)
        
    def PopulateData(self):
            
        is_valid = True
        try:
            self._check_same_parties()
            
            book_info = self._get_trades()

            self.m_list1.RemoveAllItems()
            self.m_list2.RemoveAllItems()

            root_item1 = self.m_list1.GetRootItem()
            root_item2 = self.m_list2.GetRootItem()


            for trade in book_info.get_leg1_trades():
                child1 = root_item1.AddChild()
                child1.Label(trade.quantity, 0)
                child1.Label(trade.price, 1)
                child1.Label(trade.is_ff, 2)
                child1.Label(trade.cparty, 3)
                child1.Label(trade.portfolio, 4)

            for trade in book_info.get_leg2_trades():
                child1 = root_item2.AddChild()
                child1.Label(trade.quantity, 0)
                child1.Label(trade.price, 1)
                child1.Label(trade.is_ff, 2)
                child1.Label(trade.cparty, 3)
                child1.Label(trade.portfolio, 4)
                
            for i in range(5):
                self.m_list1.AdjustColumnWidthToFitItems(i)
                self.m_list2.AdjustColumnWidthToFitItems(i)
                
            if book_info.is_valid():
                self.btnBook.Enabled(True)                
            else:
                self.btnBook.Enabled(False)
        except Exception as exc:
            self._invalidate_form()
            LOGGER.error(str(exc))
            raise

    def _get_trades(self):
        quantity = self._get_quantity()
        price = self._get_price()
        instrument = self.optInstr.GetData()
        
        is_mtm = not self._is_gov_bond()
        is_fully_funded1 = self._is_ff1()
        cparty1 = portf1 = ""
        alias1 = self._get_alias1()
        if alias1:
            cparty1 = get_pb_fund_counterparty(alias1).Name()
            portf1 = self._get_fund_portfolio(alias1, is_fully_funded1)
            
            
        is_fully_funded2 = self._is_ff2()
        cparty2 = portf2 = ""
        alias2 = self._get_alias2()
        if alias2:
            cparty2 = get_pb_fund_counterparty(alias2).Name()
            portf2 = self._get_fund_portfolio(alias2, is_fully_funded2)
        
        # bank trade #1
        trade_l1_p1 = TradeInfo(quantity=quantity,
                                price=price,
                                instrument=instrument,
                                cparty=ABSA_BANK,
                                portfolio=portf1,
                                is_ff=is_fully_funded1,
                                is_mtm=is_mtm)  # Corporate instruments are always MTM in CR portf
        
        # bank trade #2
        trade_l2_p1 = TradeInfo(quantity=-1 * quantity,
                                price=price,
                                instrument=instrument,
                                cparty=ABSA_BANK,
                                portfolio=portf2,
                                is_ff=is_fully_funded2,
                                is_mtm=is_mtm)  # Corporate instruments are always MTM in CR portf
        
        bank_trades = (trade_l1_p1, trade_l2_p1)
        client_trades = None
        
        if alias1 and alias2 and alias1 != alias2:
            
            # client trade #1
            trade_l1_p2 = TradeInfo(quantity=-1 * quantity,
                                    price=price,
                                    instrument=instrument,
                                    cparty=cparty1,
                                    portfolio=RISK_PORTF,
                                    is_ff=is_fully_funded1,
                                    is_mtm=False)
                                    
            # client trade #2                        
            trade_l2_p2 = TradeInfo(quantity=quantity,
                                    price=price,
                                    instrument=instrument,
                                    cparty=cparty2,
                                    portfolio=RISK_PORTF,
                                    is_ff=is_fully_funded2,
                                    is_mtm=False)
            client_trades = (trade_l1_p2, trade_l2_p2)
                                
        
        is_valid = True
        if not (alias1 and alias2 and cparty1 and cparty2 and 
                self.is_valid_instr_and_issuer_type() and price and quantity):
            is_valid = False
        

        self.book_info = BookInfo(is_valid, bank_trades, client_trades)
        return self.book_info
        
    def ShowInformation(self, msg):
        """Show message in information dialog."""
        acm.UX().Dialogs().MessageBoxInformation(self.m_fuxDlg.Shell(), msg)
        
    def ShowError(self, msg):
        """Show error message box."""
        acm.UX().Dialogs().MessageBox(self.m_fuxDlg.Shell(), 'Error', "Error: " + msg,
            'Cancel', None, None, 'Button1', 'Button1')
                
    def OnValueChanged(self, cd, data):
        self.PopulateData()
        
    def OnInstrumentSelectionChanged(self, cd, data):
        """Set spot days offset from selected instrument."""
        ins = self.optInstr.GetData()
        instrument = acm.FInstrument[ins]
        self.inptOffsetDate.SetData(instrument.SpotBankingDaysOffset())
        if instrument.Issuer().Name() == GOV_BOND_ISSUER:
            self.optIssuerType.SetData(GOV_TYPE)
        else:
            self.optIssuerType.SetData(CORP_TYPE)
        self.PopulateData()
    
    def OnAddFundButtonPressed(self, cd, data):
        """Display all PB funds' aliases.
           Add fund alias to the option box.
        """
        
        global ALIASES
        if not ALIASES:
            ALIASES = sorted(get_pb_fund_shortname(cparty) for cparty in get_pb_fund_counterparties())
        alias = acm.UX().Dialogs().SelectObject(self.m_fuxDlg.Shell(),
                                                'Select Fund',
                                                'Counterparties',
                                                ALIASES,
                                                None)
        if not alias:
            return
            
        if not cd.ItemExists(alias):
            cd.AddItem(alias)

        cd.SetData(alias)
        self.PopulateData()
        
    def OnAddInstrButtonPressed(self, cd, data):
        """Show dialog with all instruments.
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
        
    def OnBookButtonPressed(self, cd, data):
        """Run the booking. Check all inputs first."""
        
        LOGGER.info("==== Booking started ====")
        try:
            ins = acm.FInstrument[self.optInstr.GetData()]
            
            trade_date = self.inptTradeDate.GetData()
            if not trade_date or trade_date.upper() == "TODAY":
                trade_date = acm.Time.DateToday()
            if not is_banking_day(ins, trade_date):
                raise RuntimeError("Date '%s' is not a banking day." % trade_date)
            LOGGER.info("Date: %s" % trade_date)
            
            offset = self.inptOffsetDate.GetData()
            if not offset:
                raise RuntimeError("Date Offset not set.")
            offset = int(offset)
            if offset < 0.0:
                raise RuntimeError("Incorrect Date Offset value: %d" % offset)
            LOGGER.info("Date Offset: %d" % offset)
            
            LOGGER.info("Booking trades...")
            trades = book_trades(self.book_info.get_all_trades(), trade_date, offset)
            LOGGER.info("Trades booked: {0}".format(list(map(str, [t.Oid() for t in trades]))))
            
            LOGGER.info("Setting premiums...")
            set_premiums(trades)
            
            LOGGER.info("Setting final status...")
            set_final_status(trades, self.trd_status)
            
            LOGGER.info("==== Booking completed successfully.")
            self.ShowInformation("Booking completed successfully.\nCheck log for details.")
            
        except Exception as exc:
            LOGGER.error(str(exc))
            self.ShowError("Booking failed: %s" % str(exc))
            raise
    
    def OnChbSimulatedChecked(self, cd, data):
        if self.chb_simulated.Checked():
            self._set_colors(YELLOW_COLOR)
            self.trd_status = SIMULATED_STATUS
        else:
            self._set_colors(WHITE_COLOR)
            self.trd_status = BOOKING_STATUS
    
    def OnCloseButtonPressed(self, cd, data):
        """Close main dialog."""
        self.m_fuxDlg.CloseDialogOK()

    def CreateLayout(self):
        b = acm.FUxLayoutBuilder()
        b.BeginVertBox('None')
        b.  BeginVertBox('EtchedIn', 'Fund trade properties', 'vertbox1')
        b.    BeginHorzBox('None')
        b.      AddOption('opt_instr', 'Instrument:', 40, 40)
        b.      AddButton('btn_add_instr', 'Add...')
        b.    EndBox()
        b.    AddOption('opt_issuer_type', 'Issuer Type:', 40, 40)
        b.    AddInput('inpt_trade_qty', 'Quantity:', 15, 15)
        b.    AddInput('inpt_trade_price', 'Price:', 15, 15)
        b.    BeginVertBox('EtchedIn', 'Counterparty 1', 'vertbox2')
        b.      BeginHorzBox('None')
        b.        AddOption('opt_cpty1', 'Name:', 50, 50)
        b.        AddButton('btn_add_fund1', 'Add Fund...')
        b.      EndBox()
        b.      AddCheckbox('chb_ff1', "Fully Funded")
        b.    EndBox()
        b.    BeginVertBox('EtchedIn', 'Counterparty 2', 'vertbox3')
        b.      BeginHorzBox('None')
        b.        AddOption('opt_cpty2', 'Name:', 50, 50)
        b.        AddButton('btn_add_fund2', 'Add Fund...')
        b.      EndBox()
        b.      AddCheckbox('chb_ff2', "Fully Funded")
        b.    EndBox()
        b.    AddInput('inpt_trade_date', 'Date:', 15, 15)
        b.    AddInput('inpt_offset_date', 'Date Offset T+:', 15, 15)
        b.  EndBox()

        b.  AddList('list_trades1', 4, -1, 110, -1)
        b.  AddSpace(10)
        b.  AddList('list_trades2', 4, -1, 110, -1)
        
        b.  AddSpace(10)
        b.  BeginHorzBox('None')
        b.    AddButton('btn_book', 'Book')
        b.    AddSpace(10)
        b.    AddCheckbox('chb_simulated', 'Simulated?')
        b.    AddLabel('label_info', '', 220, -1)
        b.    AddFill()
        b.    AddButton('btn_close', 'Close')
        b.  EndBox()
        b.EndBox()
        return b
      
      
class TradeInfo(object):
    
    def __init__(self, quantity, price, instrument, cparty, portfolio, is_ff, is_mtm):
        self.quantity = quantity
        self.price = price
        self.instrument = instrument
        self.cparty = cparty
        self.portfolio = portfolio
        self.is_ff = is_ff
        self.is_mtm = is_mtm
        
        
class BookInfo(object):

    def __init__(self, is_valid, bank_trades, client_trades):
        self._is_valid = is_valid
        self.bank_trades = bank_trades
        self.client_trades = client_trades
        
    def is_valid(self):
        return self._is_valid
        
    def get_leg1_trades(self):
        trades = [self.bank_trades[0]]
        if self.client_trades:
            trades.append(self.client_trades[0])
        return trades
        
    def get_leg2_trades(self):
        trades = [self.bank_trades[1]]
        if self.client_trades:
            trades.append(self.client_trades[1])
        return trades
        
    def get_all_trades(self):
        if self.client_trades:
            return self.bank_trades + self.client_trades
        return self.bank_trades
    
    

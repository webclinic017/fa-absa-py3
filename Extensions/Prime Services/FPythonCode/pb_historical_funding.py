"""-----------------------------------------------------------------------------
PURPOSE                 :  This tool calculates the difference between posted 
                           and recalculated funding if the funding rate changes.
                           Accessible from Tools -> PB Historical Funding 
                           Calculator.
DEVELOPER               :  Libor Svoboda
--------------------------------------------------------------------------------

HISTORY
================================================================================
Date         Change no     Developer              Description
--------------------------------------------------------------------------------
2016-08-25   3905913       Libor Svoboda          Initial Implementation                                         
"""
import acm
import FUxCore
import PS_Functions
from PS_FundingSweeper import (FundingQuery, TradingManagerSweeper, 
                               _IsOvernightSpreadInstrument, 
                               GetOvernightFundingRate, GetShortFundingRate)
from PS_ExtendPortfolioSwap import (_GenerateValStartQuery, 
                                    _CalculateOvernightSpreadValStart)
from PS_FundingCalculations import CalculateFunding


def start_dialog(eii):
    """Callback from menu extension to start the main dialog."""
    shell = eii.ExtensionObject().Shell()
    builder = create_layout()
    sc_dialog = HistoricalFundingDialog()
    acm.UX().Dialogs().ShowCustomDialogModal(shell, builder, sc_dialog)


def show_custom_dialog(shell, message, dialog_type):
    """Show a custom dialog."""
    acm.UX().Dialogs().MessageBox(shell, dialog_type, message, 'OK', 
                                  None, None, 'Button1', 'Button1')


def is_number(value):
    try:
        value = float(value)
    except ValueError:
        return False
    
    if not value == value:
        return False
    return True


class HistoricalFundingDialog(FUxCore.LayoutDialog):
    
    def __init__(self):
        self._counterparties = PS_Functions.get_pb_fund_counterparties()
        self._funds = {}
        for party in self._counterparties:
            self._funds[PS_Functions.get_pb_fund_shortname(party)] = party
        self._cal = acm.FCalendar['ZAR Johannesburg']
        self._today = acm.Time.DateToday()

    def HandleCreate(self, dlg, layout):
        """Register controls."""
        self._fux_dlg = dlg
        self._shell = dlg.Shell()
        self._fux_dlg.Caption('PB Historical Funding Calculator')

        self._calculate_btn = layout.GetControl('ok')
        self._cancel_btn = layout.GetControl('cancel')
        
        self._shortname = layout.GetControl('shortname')
        self._compound = layout.GetControl('compound')
        self._pswap = layout.GetControl('pswap')
        self._start_date = layout.GetControl('start_date')
        self._end_date = layout.GetControl('end_date')
        
        self._start_short = layout.GetControl('start_short')
        self._start_long = layout.GetControl('start_long')
        self._end_short = layout.GetControl('end_short')
        self._end_long = layout.GetControl('end_long')
        
        self._new_short_rate = layout.GetControl('new_short_rate')
        self._new_long_rate = layout.GetControl('new_long_rate')
        
        self._posted = layout.GetControl('posted')
        self._calculated = layout.GetControl('calculated')
        self._diff = layout.GetControl('diff')
        self._set_defaults()
    
    def HandleApply(self):        
        start_date = self.validate_date(self._start_date.GetData())
        end_date = self.validate_date(self._end_date.GetData())
        if not start_date or not end_date:
            msg = 'Please specify valid start and end dates.'
            show_custom_dialog(self._shell, msg, 'Warning')
            return
        
        try:
            new_short_rate = float(self._new_short_rate.GetData())
        except ValueError:
            msg = 'New short rate is invalid.'
            show_custom_dialog(self._shell, msg, 'Error')
            return
        try:
            new_long_rate = float(self._new_long_rate.GetData())
        except ValueError:
            msg = 'New long rate is invalid.'
            show_custom_dialog(self._shell, msg, 'Error')
            return
        
        total_posted = 0
        total_recalc = 0
        query = _GenerateValStartQuery(acm.FCompoundPortfolio[self._compound.GetData()])
        for date in PS_Functions.DateGenerator(start_date, end_date):
            if self._cal.IsNonBankingDay(None, None, date):
                continue
            val_start = _CalculateOvernightSpreadValStart(query, date)
            recalc_funding, instruments = self._recalculate_funding(date, new_short_rate, 
                                                                    new_long_rate, val_start)
            posted_funding = self._get_funding(date, instruments)
            total_recalc += recalc_funding
            total_posted += posted_funding
        
        self._posted.SetData(total_posted)
        self._calculated.SetData(total_recalc)
    
    def _get_funding(self, date, instruments):
        funding = []
        pswap = self._pswap.GetData()
        yesterday =  acm.Time.DateAddDelta(date, 0, 0, -1)
        for ins in instruments:
            funding.append(CalculateFunding(ins, pswap, yesterday, date))
        return sum(funding)
    
    def _recalculate_funding(self, date, short_rate, long_rate, total_val_start):
        """Using logic from PS_FundingSweeper.GenerateFunding."""
        total_funding = []
        instruments = []
        pswap = self._pswap.GetData()
        portfolio = pswap.FundPortfolio()
        query = FundingQuery(portfolio, pswap.Currency().Name())
        prev_banking_day = self._cal.AdjustBankingDays(date, -1)
        ins_val_ends = TradingManagerSweeper(query, prev_banking_day, 
                                             ["Portfolio Value End"], False)
        
        for ins, val_ends in ins_val_ends.items():
            val_end = val_ends[0]
            ins = acm.FInstrument[ins]
            ins_type = ins.InsType()
            
            if not val_end:
                continue
            if ins_type in ['BuySellback', 'Repo/Reverse']:
                continue
            
            if is_number(total_val_start) and _IsOvernightSpreadInstrument(ins):
                spread_val = total_val_start
            else:
                spread_val = val_end
            
            if spread_val < 0:
                fund_rate = short_rate
            else:
                fund_rate = long_rate
            
            if ins_type in ['Stock', 'Bond', 'ETF']:
                if val_end < 0:
                    short_rate = GetShortFundingRate(pswap, ins, prev_banking_day)
                    fund_rate -= short_rate
            
            day_count = acm.Time().DateDifference(date, prev_banking_day)
            total = -day_count * fund_rate * val_end / 36500.0
            total_funding.append(total)
            instruments.append(ins)
        return (sum(total_funding), instruments)
        
    def _set_defaults(self):
        self._shortname.Populate(sorted(self._funds.keys()))
        self._compound.Editable(False)
        self._start_date.SetData(self._cal.AdjustBankingDays(self._today, -1))
        self._end_date.SetData(self._cal.AdjustBankingDays(self._today, -1))
        
        self._start_short.SetData('0.0')
        self._start_short.Editable(False)
        self._start_long.SetData('0.0')
        self._start_long.Editable(False)
        self._end_short.SetData('0.0')
        self._end_short.Editable(False)
        self._end_long.SetData('0.0')
        self._end_long.Editable(False)
        
        self._posted.Editable(False)
        self._calculated.Editable(False)
        self._diff.Editable(False)
        
        self._new_short_rate.SetData('0.0')
        self._new_long_rate.SetData('0.0')
        self._posted.SetData('0.0')
        self._calculated.SetData('0.0')
        self._posted.AddCallback('Changed', self._funding_changed, None)
        self._calculated.AddCallback('Changed', self._funding_changed, None)
        
        self._calculate_btn.Enabled(False)
        self._shortname.AddCallback('Changed', self._shortname_changed, None)
        self._pswap.AddCallback('Changed', self._pswap_changed, None)
        self._start_date.AddCallback('Changed', self._start_date_changed, None)
        self._end_date.AddCallback('Changed', self._end_date_changed, None)
    
    def _funding_changed(self, *args):
        try:
            posted = float(self._posted.GetData())
            calculated = float(self._calculated.GetData())
        except:
            return
        
        diff = calculated - posted
        self._diff.SetData(diff)
        
    def _shortname_changed(self, *args):
        self._start_short.SetData('0.0')
        self._start_long.SetData('0.0')
        self._end_short.SetData('0.0')
        self._end_long.SetData('0.0')
        self._calculate_btn.Enabled(False)
        shortname = self._shortname.GetData()
        if not shortname:
            return
        party = self._funds[shortname]
        compound = PS_Functions.get_pb_reporting_portfolio(party)
        self._compound.SetData(compound)
        pswaps = PS_Functions.get_pb_fund_pswaps(party)
        self._pswap.Populate(pswaps)
    
    @classmethod
    def validate_date(cls, date):
        try:
            ymd = acm.Time.DateToYMD(date)
        except:
            return ''
        return date
    
    def _start_date_changed(self, *args):
        pswap = self._pswap.GetData()
        start_date = self.validate_date(self._start_date.GetData())
        if not pswap or not start_date:
            self._calculate_btn.Enabled(False)
            self._start_short.SetData('0.0')
            self._start_long.SetData('0.0')
            return
        prev_banking_day = self._cal.AdjustBankingDays(start_date, -1)
        funding_index = acm.FInstrument[pswap.add_info('PSONPremIndex')]
        try:
            short_rate = GetOvernightFundingRate(funding_index, prev_banking_day, 'Short')
        except:
            short_rate = '0.0'
        try:
            long_rate = GetOvernightFundingRate(funding_index, prev_banking_day, 'Long')
        except:
            long_rate = '0.0'
        self._start_short.SetData(short_rate)
        self._start_long.SetData(long_rate)
        if self.validate_date(self._end_date.GetData()):
            self._calculate_btn.Enabled(True)

    def _end_date_changed(self, *args):
        pswap = self._pswap.GetData()
        end_date = self.validate_date(self._end_date.GetData())
        if not pswap or not end_date:
            self._calculate_btn.Enabled(False)
            self._end_short.SetData('0.0')
            self._end_long.SetData('0.0')
            return
        prev_banking_day = self._cal.AdjustBankingDays(end_date, -1)
        funding_index = acm.FInstrument[pswap.add_info('PSONPremIndex')]
        try:
            short_rate = GetOvernightFundingRate(funding_index, prev_banking_day, 'Short')
        except:
            short_rate = '0.0'
        try:
            long_rate = GetOvernightFundingRate(funding_index, prev_banking_day, 'Long')
        except:
            long_rate = '0.0'
        self._end_short.SetData(short_rate)
        self._end_long.SetData(long_rate)
        if self.validate_date(self._start_date.GetData()):
            self._calculate_btn.Enabled(True)
    
    def _pswap_changed(self, *args):
        pswap = self._pswap.GetData()
        if not pswap:
            return
        self._start_date_changed()
        self._end_date_changed()


def create_layout():
    """Return dialog layout."""
    b = acm.FUxLayoutBuilder()
    b.BeginVertBox('None')
    b.  AddOption('shortname', 'Fund')
    b.  AddInput('compound', 'Reporting Portfolio')
    b.  AddOption('pswap', 'Portfolio Swap')
    b.  BeginVertBox('EtchedIn', 'Start')
    b.    AddInput('start_date', 'Date')
    b.      AddInput('start_short', 'Short Rate')
    b.      AddInput('start_long', 'Long Rate')
    b.  EndBox()
    b.  BeginVertBox('EtchedIn', 'End')
    b.    AddInput('end_date', 'Date')
    b.      AddInput('end_short', 'Short Rate')
    b.      AddInput('end_long', 'Long Rate')
    b.  EndBox()
    b.  AddInput('new_short_rate', 'New Short Rate')
    b.  AddInput('new_long_rate', 'New Long Rate')
    b.  AddInput('posted', 'Posted Funding')
    b.  AddInput('calculated', 'Recalculated Funding')
    b.  AddInput('diff', 'Difference')
    b.  AddFill()
    b.  AddSpace(10)
    b.  BeginHorzBox('None')
    b.    AddFill()
    b.    AddButton('ok', 'Calculate')
    b.    AddButton('cancel', 'Cancel')
    b.  EndBox()
    b.EndBox()
    return b

    

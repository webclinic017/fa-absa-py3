"""-----------------------------------------------------------------------------
PURPOSE                 :  This tool correctly sets cashflow and reset dates
                           for TRS with equity underlyings. It is a workaround 
                           for an FA core bug.
                           Accessible from Total Return Swap -> Extensions ->
                               Adjust Cashflows.
REQUESTER, DESK         :  Naval Singh, Equity Trading
DEVELOPER               :  Libor Svoboda
--------------------------------------------------------------------------------

HISTORY
================================================================================
Date        Change no     Developer              Description
--------------------------------------------------------------------------------
2016-07-26    3826581     Libor Svoboda          Initial Implementation                                         
"""
import acm
import FUxCore


def show_custom_dialog(shell, message, dialog_type):
    """Show a custom dialog."""
    acm.UX().Dialogs().MessageBox(shell, dialog_type, message, 'OK', 
                                  None, None, 'Button1', 'Button1')


def start_dialog(eii):
    """Callback from menu extension to start the main dialog."""
    shell = eii.ExtensionObject().Shell()
    ins = eii.ExtensionObject().OriginalInstrument()
    if not ins:
        show_custom_dialog(shell, 'Please save the instrument.', 'Error')
        return
    builder = create_layout()
    sc_dialog = AdjustCashflowsDialog(ins)
    acm.UX().Dialogs().ShowCustomDialogModal(shell, builder, sc_dialog)


class AdjustCashflowsDialog(FUxCore.LayoutDialog):

    def __init__(self, instrument):
        self._ins = instrument
        self.cals_adjust_days = acm.GetFunction('calendarsAdjustBankingDays', 3)
        self._float_legs = [leg for leg in self._ins.Legs() 
                            if leg.LegType() == 'Float']
    
    def HandleCreate(self, dlg, layout):
        """Register controls."""
        self._fux_dlg = dlg
        self._shell = dlg.Shell()
        self._fux_dlg.Caption('Adjust TRS Cashflows')

        self._ok_btn = layout.GetControl('ok')
        self._cancel_btn = layout.GetControl('cancel')
        
        self._start_date = layout.GetControl('start_date')
        self._end_date = layout.GetControl('end_date')
        
        self._start_date.Editable(False)
        self._end_date.Editable(False)
        
        self._start_date.SetData(self._ins.StartDate())
        self._end_date.SetData(self._ins.EndDate())
        
        self._offset = layout.GetControl('offset')
        self._offset.AddCallback('Changed', self._update_ui_dates, None)
        
        index_ref = self._float_legs[0].IndexRef()
        if index_ref and index_ref.InsType() == 'Stock':
            self._offset.SetData(index_ref.SpotBankingDaysOffset())
    
    def HandleApply(self):
        offset = self._offset.GetData()
        try:
            offset = int(offset)
        except ValueError:
            msg = 'Please enter valid offset.'
            show_custom_dialog(self._shell, msg, 'Error')
            return
        
        for leg in self._ins.Legs():
            if leg.LegType() == 'Float':
                self.update_float_leg(leg, offset)
            elif leg.LegType() == 'Total Return':
                self.update_total_return_leg(leg)
        show_custom_dialog(self._shell, 'Done.', 'Information')
    
    def _update_ui_dates(self, *args):
        offset = self._offset.GetData()
        if not offset:
            offset = 0
        try:
            offset = int(offset)
        except ValueError:
            msg = 'Please enter valid offset.'
            show_custom_dialog(self._shell, msg, 'Error')
            return
        float_cals = self.get_leg_calendars(self._float_legs[0])
        start_date = self.cals_adjust_days(float_cals, 
                                           self._ins.StartDate(), offset)
        end_date = self.cals_adjust_days(float_cals, 
                                         self._ins.EndDate(), offset)
        self._start_date.SetData(start_date)
        self._end_date.SetData(end_date)
    
    @classmethod
    def get_leg_calendars(cls, leg):
        calendars = acm.FArray()
        calendars.Add(leg.PayCalendar())
        if leg.Pay2Calendar():
            calendars.Add(leg.Pay2Calendar())
        if leg.Pay3Calendar():
            calendars.Add(leg.Pay3Calendar())
        if leg.Pay4Calendar():
            calendars.Add(leg.Pay4Calendar())
        if leg.Pay5Calendar():
            calendars.Add(leg.Pay5Calendar())
        return calendars

    @classmethod
    def get_reset_calendars(cls, leg):
        calendars = acm.FArray()
        calendars.Add(leg.ResetCalendar())
        if leg.Reset2Calendar():
            calendars.Add(leg.Reset2Calendar())
        if leg.Reset3Calendar():
            calendars.Add(leg.Reset3Calendar())
        if leg.Reset4Calendar():
            calendars.Add(leg.Reset4Calendar())
        if leg.Reset5Calendar():
            calendars.Add(leg.Reset5Calendar())
        return calendars
    
    @classmethod
    def get_cashflows(cls, leg, cf_type=None):
        cfs = acm.FArray()
        for cf in leg.CashFlows():
            if cf_type:
                if cf.CashFlowType() == cf_type:
                    cfs.Add(cf)
            else:
                cfs.Add(cf)
        cfs = cfs.SortByProperty('StartDate')
        return cfs
    
    def update_total_return_leg(self, leg):
        for cf in leg.CashFlows():
            if not cf.CashFlowType() == 'Total Return':
                continue
            acm.BeginTransaction()
            try:
                for reset in cf.Resets():
                    reset.Day(reset.StartDate())
                    reset.Commit()
                acm.CommitTransaction()
            except Exception as exc:
                acm.AbortTransaction()
                print('Failed to update cashflow %s: %s' % (cf.Oid(), str(exc)))
    
    def update_float_leg(self, leg, offset):
        if not leg.CashFlows():
            return
        
        float_rate_cfs = self.get_cashflows(leg, 'Float Rate')
        leg_cals = self.get_leg_calendars(leg)
        reset_cals = self.get_reset_calendars(leg)
        orig_dates = acm.DealCapturing.GenerateStripOfOptionDates(
            leg.StartDate(), leg.EndDate(), leg.RollingPeriod(), 
            leg.StartDate(), leg.PayDayMethod(), leg_cals, leg.LongStub())
        new_dates = [self.cals_adjust_days(leg_cals, date, offset) 
                     for date in orig_dates]
        
        if not len(new_dates) - 1 == len(float_rate_cfs):
            msg = ('Number of Float Rate cashflows does not correspond to the'
                   ' number of time periods. Please update manually.')
            show_custom_dialog(self._shell, msg, 'Error')
            return
        
        for index, cf in enumerate(float_rate_cfs):
            acm.BeginTransaction()
            try:
                cf.StartDate(new_dates[index])
                cf.EndDate(new_dates[index+1])
                for reset in cf.Resets():
                    reset.StartDate(new_dates[index])
                    reset.EndDate(new_dates[index+1])
                    if reset.ResetType() == leg.ResetType():
                        reset_day = self.cals_adjust_days(reset_cals, 
                                                          new_dates[index], 
                                                          leg.ResetDayOffset())
                        reset.Day(reset_day)
                    elif reset.ResetType() == 'Nominal Scaling':
                        reset.Day(orig_dates[index])
                    else:
                        reset.Day(new_dates[index])
                    reset.Commit()
                cf.Commit()
                acm.CommitTransaction()
            except Exception as exc:
                acm.AbortTransaction()
                print('Failed to update cashflow %s: %s' % (cf.Oid(), str(exc)))


def create_layout():
    """Return dialog layout."""
    b = acm.FUxLayoutBuilder()
    b.BeginVertBox('None')
    b.  AddInput('offset', 'Float Leg Day Offset')
    b.  AddInput('start_date', 'Start Date')
    b.  AddInput('end_date', 'End Date')
    b.  AddFill()
    b.  AddSpace(10)
    b.  BeginHorzBox('None')
    b.    AddFill()
    b.    AddButton('ok', 'Update')
    b.    AddButton('cancel', 'Cancel')
    b.  EndBox()
    b.EndBox()
    return b

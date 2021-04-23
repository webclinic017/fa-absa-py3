"""-----------------------------------------------------------------------------
PURPOSE              :  TRS trade action tool automating manual TCU processes.
                        Following actions are currently supported:
                          Roll - close old TRS and create new TRS, 
                             BSB (if necessary) and corresponding trades.
                          New - create new TRS, BSB (if necessary) 
                             and corresponding trades.
                          Expired - close old TRS.
REQUESTER, DEPATMENT :  Sean Laing, TCU
DEVELOPER            :  Libor Svoboda
--------------------------------------------------------------------------------

HISTORY
================================================================================
Date        Change no     Developer              Description
--------------------------------------------------------------------------------
2018-06-19  1000584777    Libor Svoboda          Initial Implementation
"""
import csv
import xlrd
import calendar
import acm
import FUxCore
import SAFI_BOND_TRS
from collections import defaultdict, OrderedDict
from at_calculation_space import calculate_value


CALC_SPACE = acm.Calculations().CreateStandardCalculationsSpaceCollection()
GEN_TRS_ILB = acm.FInstrument['ZAR/TRS/GEN/ILB']
GEN_TRS_BOND = acm.FInstrument['ZAR/TRS/GEN/BOND']

INPUT_COLUMNS = OrderedDict([
    ('Trade Number', 'trade'),
    ('Action', 'string'),
    ('Counterparty', 'party'),
    ('Nominal', 'float'),
    ('Acquirer', 'party'),
    ('Portfolio', 'portfolio'),
    ('Cpty Portfolio', 'portfolio'),
    ('Start Date', 'date'),
    ('End Date', 'date'),
    ('Value Date', 'date'),
    ('Bond', 'bond'),
    ('YTM', 'float'),
    ('Repo Rate', 'float'),
    ('Forward Price', 'float'),
    ('Spread', 'float'),
    ('Rolling', 'float'),
    ('Payment Date', 'date'),
    ('Fee', 'float'),
    ('Settlement Amount', 'float'),
    ('Approx. load', 'bool'),
    ('Approx. load ref', 'string'),
    ('InsOverride', 'enum(cl_InsOverride)'),
    ('SND_Cash', 'string'),
    ('SND_Nominal', 'string'),
    ('SND_Rate', 'string'),
    
])
ROLL_MANDATORY = (
    'Trade Number',
    'Counterparty',
    'Acquirer',
    'Portfolio',
    'Settlement Amount',
    'Start Date',
    'End Date',
    'Value Date',
    'Repo Rate',
    'Bond',
    'YTM',
    'Forward Price',
)
EXPIRED_MANDATORY = (
    'Trade Number',
    'Settlement Amount',
)
NEW_MANDATORY = (
    'Counterparty',
    'Nominal',
    'Acquirer',
    'Portfolio',
    'Start Date',
    'End Date',
    'Value Date',
    'Bond',
    'YTM',
    'Repo Rate',
    'Forward Price',
)
IMPORT_FILTER = 'Excel Files (*.xlsx)|*.xlsx|Excel Files (*.xls)|*.xls|'
INITDIR = 'C:\\'
FIRST_DATA_ROW = 2
DATE_TODAY = acm.Time.DateToday()
DEFAULT_REPORT_PATH = r'C:\temp\TRS_ACTIONS_%s.csv' % DATE_TODAY
ZAR_CALENDAR = acm.FCalendar['ZAR Johannesburg']
PREV_BUSINESS_DAY = ZAR_CALENDAR.AdjustBankingDays(DATE_TODAY, -1)
COL_RED = 8686  # acm.UX().Colors().Create(255, 0, 0).ColorRef()
CONTEXT = acm.GetDefaultContext()
TRADE_SHEET_COLUMNS = OrderedDict([
    ('Instrument', 'Trade Instrument'),
    ('Price', 'Trade Price'),
    ('Quantity', 'Trade Quantity'),
    ('Premium', 'Trade Premium'),
    ('Acquire Day', 'Trade Acquire Day'),
    ('Portfolio', 'Trade Portfolio'),
    ('Currency', 'Trade Currency'),
    ('Status', 'Trade Status'),
    ('Counterparty', 'Trade Counterparty'),
    ('Trader', 'Trade Trader'),
    ('Total Val End', 'Total Val End'),
    ('Cash End', 'Portfolio Cash End'),
    ('TPL', 'Portfolio Total Profit and Loss'),
])
DIFF_COLUMNS = OrderedDict([
    ('Total Val End', 'Total Val End'),
    ('Cash End', 'Portfolio Cash End'),
    ('TPL', 'Portfolio Total Profit and Loss'),
])
ADD_INFOS_TO_CLEAR = (
    'AmendReasonIns',
    'AmendReasonTypeIns',
)


def create_layout():
    b = acm.FUxLayoutBuilder()
    b.BeginVertBox('None')
    b.  BeginHorzBox('None')
    b.    AddInput('input_path', 'Input Data')
    b.    AddButton('import_btn', 'Import')
    b.  EndBox()
    b.  AddList('input_data', numlines=10, width=200)
    b.  BeginHorzBox('None')
    b.   AddFill()
    b.   AddButton('ok', 'Run')
    b.   AddButton('cancel', 'Cancel')
    b.  EndBox()
    b.  BeginVertBox('EtchedIn', 'Output')
    b.    AddCustom('trade_sheet', 'sheet.FTradeSheet', 240, 200)
    b.    BeginHorzBox('None')
    b.      AddInput('report_path', 'CSV Report')
    b.      AddButton('export_btn', 'Export')
    b.    EndBox()
    b.    BeginHorzBox('None')
    b.      AddFill()
    b.      AddButton('run_safi_bond_trs', 'Run SAFI_BOND_TRS')
    b.    EndBox()
    b.  EndBox()
    b.EndBox()
    return b


def start_dialog(eii):
    shell = eii.ExtensionObject().Shell()
    builder = create_layout()
    sc_dialog = TRSActionDialog()
    acm.UX().Dialogs().ShowCustomDialogModal(shell, builder, sc_dialog)


def show_custom_dialog(shell, message, dialog_type):
    acm.UX().Dialogs().MessageBox(shell, dialog_type, message, 'OK', 
                                  None, None, 'Button1', 'Button1')


def read_data_from_row(row):
    data_dict = {}
    for i, column_name in enumerate(INPUT_COLUMNS.keys()):
        try:
            value = str(row[i].value)
        except IndexError:
            data_dict[column_name] = ''
        else:
            data_dict[column_name] = value
    return data_dict


def get_trades_as_folder(label, trades):
    folder = acm.FASQLQueryFolder()
    folder.Name(label)
    query = acm.CreateFASQLQuery('FTrade', 'OR')
    for trade in trades:
        if not trade:
            continue
        query.AddOpNode('OR')
        query.AddAttrNode('Oid', 'EQUAL', trade.Oid())
    folder.AsqlQuery(query)
    return folder


def iterate_ins_name(current_name):
    split_name = current_name.split('#')
    try:
        index = int(split_name[-1])
    except ValueError:
        new_name = current_name + '#1'
    else:
        new_name = '#'.join(split_name[:-1] + [str(index+1)])
        
    if acm.FInstrument[new_name]:
        return iterate_ins_name(new_name)
    return new_name


def calc_column_val(column_id, trade):
    if not trade:
        return
    try:
        value = calculate_value('FTradeSheet', trade, column_id)
    except Exception as exc:
        print('Failed to calculate "%s" for trade %s: %s' % (column_id, trade.Oid(), str(exc)))
        return
    try:
        return value.Name()
    except AttributeError:
        try:
            return float(value)
        except ValueError:
            return str(value)


class BusinessDataError(Exception):
    pass


class TRSActionDialog(FUxCore.LayoutDialog):
    
    def __init__(self):
        self._init_directory = None
        self._new_instruments = []
    
    def _perform_actions(self):
        shell = self._fux_dlg.Shell()
        output = {}
        for item in self._input_data.items():
            if not item.is_valid():
                continue
            action = item.get_action()
            action_key = action.get_action_key()
            acm.BeginTransaction()
            try:
                action.perform()
                acm.CommitTransaction()
            except Exception as exc:
                acm.AbortTransaction()
                msg = 'Action "%s" (%s) failed: %s' % (action.action_name, action_key, str(exc))
                show_custom_dialog(shell, msg, 'Error')
                continue
            new_trs = action.get_new_trs()
            orig_trade = action.get_orig_trade()
            new_trade = action.get_new_trade()
            if new_trs:
                self._new_instruments.append(new_trs)
            if not orig_trade and not new_trade:
                continue
            if action_key in output:
                output[action_key].extend([orig_trade, new_trade])
            else:
                output[action_key] = [orig_trade, new_trade]
        return output
    
    def _write_csv_report(self, csvfile):
        writer = csv.writer(csvfile, dialect='excel')
        writer.writerow(ActionData.report_columns)
        for item in self._input_data.items():
            rows = item.get_action_rows()
            for row in rows:
                writer.writerow(row)
    
    def _import_data_from_file(self, file_path):
        shell = self._fux_dlg.Shell()
        workbook = xlrd.open_workbook(file_path)
        try:
            worksheet = workbook.sheet_by_index(0)
        except xlrd.XLRDError:
            msg = "The file '%s' does not contain any sheets." % file_path
            show_custom_dialog(shell, msg, 'Error')
            return
        curr_row = FIRST_DATA_ROW - 1
        num_rows = worksheet.nrows
        while curr_row < num_rows:
            row = worksheet.row(curr_row)
            if row[1].value:
                data_dict = read_data_from_row(row)
                action_data = ActionData(data_dict, workbook.datemode)
                action_data.validate_data()
                self._input_data.add_item(action_data)
                curr_row += 1
            else:
                msg = ('Finished importing at row %d due to a blank "Action"'
                       ' field.' % (curr_row+1))
                show_custom_dialog(shell, msg, 'Information')
                break
    
    def _reload_table(self):
        self._input_data.refresh_labels()
        self._input_data.mark_invalid()
    
    def _on_export(self, arg1, arg2):
        shell = self._fux_dlg.Shell()
        path  = self._report_path.GetData()
        try:
            with open(path, 'wb') as csvfile:
                self._write_csv_report(csvfile)
        except Exception as exc:
            msg = 'Failed to create report: %s' % str(exc)
            show_custom_dialog(shell, e.strerror, 'Error')
        else:
            msg = 'Report created successfully.'
            show_custom_dialog(shell, msg, 'Information')
    
    def _on_import(self, arg1, arg2):
        shell = self._fux_dlg.Shell()
        self._run_btn.Enabled(False)
        directory = self._init_directory if self._init_directory else INITDIR
        selections = acm.UX().Dialogs().BrowseForFiles(shell, IMPORT_FILTER,
                                                       directory)
        if not selections:
            return
        if len(selections) > 1:
            msg = 'Please select just one file.'
            show_custom_dialog(shell, msg, 'Information')
            return
        selection = selections[0]
        self._init_directory = selection.SelectedDirectory().Text()
        input_path = self._init_directory + selection.SelectedFile().Text()
        self._input_path.SetData(input_path)
        self._input_data.remove_all_items()
        self._import_data_from_file(input_path)
        if any([item.is_valid() for item in self._input_data.items()]):
            self._run_btn.Enabled(True)
        self._reload_table()
        self._trade_sheet.RemoveAllRows()
        self._new_instruments = []
        self._run_script_btn.Enabled(False)
        self._export_btn.Enabled(False)
    
    def _on_run_script(self, arg1, arg2):
        shell = self._fux_dlg.Shell()
        data = {}
        data['Instruments'] = self._new_instruments
        try:
            SAFI_BOND_TRS.ael_main(data)
        except Exception as exc:
            msg = 'SAFI_BOND_TRS failed: %s' % str(exc)
            show_custom_dialog(shell, msg, 'Error')
        else:
            msg = 'SAFI_BOND_TRS finished.'
            show_custom_dialog(shell, msg, 'Information')
    
    def HandleCreate(self, dlg, layout):
        self._fux_dlg = dlg
        self._fux_dlg.Caption('TRS Actions')
        
        self._run_btn = layout.GetControl('ok')
        self._run_btn.Enabled(False)
        self._run_script_btn = layout.GetControl('run_safi_bond_trs')
        self._run_script_btn.Enabled(False)
        self._run_script_btn.AddCallback('Activate', self._on_run_script, self)
        self._cancel_btn = layout.GetControl('cancel')
        self._import_btn = layout.GetControl('import_btn')
        
        self._input_path = layout.GetControl('input_path')
        self._input_path.Editable(False)
        self._input_data = ListControl(layout, 'input_data', ActionData.columns)
        
        self._report_path = layout.GetControl('report_path')
        self._report_path.SetData(DEFAULT_REPORT_PATH)
        self._export_btn = layout.GetControl('export_btn')
        self._export_btn.Enabled(False)
        self._export_btn.AddCallback('Activate', self._on_export, self)
        
        self._trade_sheet_control = layout.GetControl('trade_sheet')
        self._trade_sheet = self._trade_sheet_control.GetCustomControl()
        default_columns = acm.GetColumnCreators(TRADE_SHEET_COLUMNS.values(), CONTEXT)
        columns = self._trade_sheet.ColumnCreators()
        columns.Clear()
        for i in range(default_columns.Size()):
            columns.Add(default_columns.At(i))
        
        self._import_btn.AddCallback('Activate', self._on_import, self)
    
    def HandleApply(self):
        shell = self._fux_dlg.Shell()
        self._trade_sheet.RemoveAllRows()
        self._new_instruments = []
        self._run_script_btn.Enabled(False)
        self._export_btn.Enabled(False)
        output = self._perform_actions()
        if not output:
            msg = 'No actions were performed.'
            show_custom_dialog(shell, msg, 'Information')
            return
        show_custom_dialog(shell, 'Done', 'Information')
        self._export_btn.Enabled(True)
        for folder_name, trades in output.iteritems():
            trades_folder = get_trades_as_folder(folder_name, trades)
            self._trade_sheet.InsertObject(trades_folder, 'IOAP_LAST')
        if self._new_instruments:
            self._run_script_btn.Enabled(True)


class ListControl(object):

    def __init__(self, layout, name, columns):
        self._list_control = layout.GetControl(name)
        self._list_control.ShowGridLines()
        self._list_control.ShowColumnHeaders()
        for column in columns:
            self._list_control.AddColumn(column, -1, '')
        self._adjust_column_widths()

    def _adjust_column_widths(self):
        for i in range(self._list_control.ColumnCount()):
            self._list_control.AdjustColumnWidthToFitItems(i)
    
    def add_item(self, list_data):
        root_item = self._list_control.GetRootItem()
        child = root_item.AddChild()
        child.SetData(list_data)
    
    def refresh_labels(self):
        root_item = self._list_control.GetRootItem()
        for child in root_item.Children():
            labels = child.GetData().get_labels()
            for i in range(len(labels)):
                child.Label(labels[i], i)
        self._adjust_column_widths()
    
    def mark_invalid(self):
        root_item = self._list_control.GetRootItem()
        for child in root_item.Children():
            is_valid = child.GetData().is_valid()
            if is_valid:
                continue
            labels = child.GetData().get_labels()
            for i in range(len(labels)):
                child.Style(i, False, 0, COL_RED)
    
    def remove_all_items(self):
        self._list_control.RemoveAllItems()
        self._adjust_column_widths()
    
    def items(self):
        root_item = self._list_control.GetRootItem()
        for child in root_item.Children():
            yield child.GetData()


class Action(object):
    
    action_name = ''
    
    def __init__(self, data):
        self._data = data
        self._trade = None
        self._trs = None
        self._new_trade = None
        self._new_trs = None
        self._tr_cf = None
        self._successful = False
    
    @classmethod
    def date_to_name(cls, acm_date):
        year, month, _ = acm.Time.DateToYMD(acm_date)
        return calendar.month_abbr[month].upper() + str(year)[2:]
    
    @classmethod
    def get_ins_name(cls, old_name, old_end_date, new_end_date):
        old_name_date = cls.date_to_name(old_end_date)
        if not old_name_date in old_name:
            msg = 'The name %s does not correspond to the date %s.' % (
                old_name, old_end_date)
            raise BusinessDataError(msg)
        new_name_date = cls.date_to_name(new_end_date)
        return old_name.replace(old_name_date, new_name_date)
    
    @classmethod
    def get_new_ins_name(cls, bond_name, end_date, ins):
        if not bond_name.startswith('ZAR/'):
            msg = 'Underlying does not start with "ZAR/": %s.' % bond_name
            raise BusinessDataError(msg)
        name_date = cls.date_to_name(end_date)
        if ins.IsKindOf(acm.FBuySellBack):
            return 'TRS_%s_%s' % (bond_name.split('ZAR/')[1], name_date)
        elif ins.IsKindOf(acm.FTotalReturnSwap):
            return 'ZAR/TRS/%s/%s' % (bond_name.split('ZAR/')[1], name_date)
        raise RuntimeError('Invalid instype.')
    
    @classmethod
    def adjust_trs_date(cls, trs_date):
        leg = GEN_TRS_ILB.FirstTotalReturnLeg()
        return leg.PayCalendar().ModifyDate(None, None, trs_date, leg.PayDayMethod())
    
    def _get_total_return_cf(self):
        if self._tr_cf:
            return self._tr_cf
        cfs = [cf for leg in self._trs.Legs() for cf in leg.CashFlows()
               if cf.CashFlowType() == 'Total Return']
        if len(cfs) != 1:
            msg = 'The current TRS %s needs to have one Total Return cashflow.' % self._trs.Name()
            raise BusinessDataError(msg)
        self._tr_cf = cfs[0]
        return self._tr_cf
    
    def _get_init_price(self):
        return 100 * self._data['Forward Price']
    
    def _get_quantity(self, ins):
        if self._trade:
            return self._trade.Quantity()
        return self._data['Nominal'] / ins.ContractSize()
    
    def _get_trader(self):
        if self._trade:
            return self._trade.Trader()
        return acm.User()
    
    def _get_payment(self):
        if not (self._data['Payment Date'] and 
                self._data['Fee']):
            return None
        payment = acm.FPayment()
        valid_from = min([DATE_TODAY, self._data['Payment Date']])
        payment.Amount(self._data['Fee'])
        payment.Currency(acm.FCurrency['ZAR'])
        payment.Party(self._data['Counterparty'])
        payment.PayDay(self._data['Payment Date'])
        payment.Type('Cash')
        payment.ValidFrom(valid_from)
        return payment
    
    def _calculate_new_return(self):
        tr_cf = self._get_total_return_cf()
        cf_calcs = tr_cf.Calculation()
        cf_nominal = cf_calcs.Nominal(CALC_SPACE, self._trade).Number()
        trade_nominal = self._trade.Quantity() * self._trs.ContractSize()
        return 100 * (self._data['Settlement Amount'] + cf_nominal) / trade_nominal
    
    def _get_last_return_reset(self):
        tr_cf = self._get_total_return_cf()
        resets = [reset for reset in tr_cf.Resets() if reset.ResetType() == 'Return']
        resets.sort(key=lambda x: x.Day())
        return resets[-1]
    
    def _update_trs_legs(self, trs, bond):
        end_date = self.adjust_trs_date(self._data['End Date'])
        init_index = self._get_init_price()
        for leg in trs.Legs():
            leg.StartDate(self._data['Start Date'])
            leg.EndDate(end_date)
            leg.RollingPeriodBase(end_date)
            leg.IsLocked(True)
            leg.ExtendedFinalCf(False)
            leg_init_price = None
            # Total Return leg
            if leg.LegType() == 'Total Return' and not leg.PayLeg():
                leg.InitialIndexValue(init_index)
                leg.ResetDayOffset(0)
                leg_init_price = init_index
                leg.IndexRef(bond)
                leg.FloatRateReference(bond)
            # Coupon leg
            elif leg.LegType() == 'Fixed' and not leg.PayLeg():
                leg.IsLocked(False)
                leg.CreditRef(bond)
                leg.FloatRateReference(None)
                leg.FloatRateFactor(0.0)
                leg.IndexRef(None)
                leg.NominalScaling('None')
                leg.ResetType('None')
                bond_leg = bond.Legs()[0]
                leg.EndPeriod(bond_leg.EndPeriod())
                leg.RollingPeriod(bond_leg.RollingPeriod())
                leg.RollingPeriodBase(bond_leg.RollingPeriodBase())
                leg.FixedRate(bond_leg.FixedRate())
                leg_init_price = bond_leg.FixedRate()
                if bond.IsKindOf(acm.FIndexLinkedBond):
                    leg.InflationBaseValue(bond_leg.InflationBaseValue())
                    leg.InflationScaling(bond_leg.InflationScaling())
                    leg.InflationScalingRef(bond_leg.InflationScalingRef())
            else:
                leg.FixedRate(0.0)
            leg.GenerateCashFlows(leg_init_price)
    
    def _create_new_trs(self):
        bond = self._data['Bond']
        if bond.IsKindOf(acm.FIndexLinkedBond):
            trs = acm.DealCapturing.CreateNewInstrumentFromGenericInstrument(GEN_TRS_ILB)
        elif bond.IsKindOf(acm.FBond):
            trs = acm.DealCapturing.CreateNewInstrumentFromGenericInstrument(GEN_TRS_BOND)
        else:
            raise BusinessDataError('Invalid underlying: %s.' % bond.Name())
        end_date = self.adjust_trs_date(self._data['End Date'])
        trs_name = self.get_new_ins_name(bond.Name(), end_date, trs)
        if acm.FInstrument[trs_name]:
            trs_name = iterate_ins_name(trs_name)
        trs.Quotation(acm.FQuotation['Pct of Nominal'])
        trs.Name(trs_name)
        self._update_trs_legs(trs, bond)
        trs.RegisterInStorage()
        trs.Commit()
        return trs
    
    def _roll_trs(self):
        orig_trs = self._trs
        end_date = self.adjust_trs_date(self._data['End Date'])
        try:
            trs_name = self.get_ins_name(orig_trs.Name(), orig_trs.EndDate(), end_date)
        except BusinessDataError:
            trs_name = self.get_new_ins_name(self._data['Bond'].Name(), end_date, orig_trs)
        if acm.FInstrument[trs_name]:
            trs_name = iterate_ins_name(trs_name)
        trs = orig_trs.StorageNew()
        trs.Name(trs_name)
        self._update_trs_legs(trs, self._data['Bond'])
        trs.Commit()
        self._clear_add_infos(trs)
        return trs
    
    def _close_old_trs(self):
        trs = self._trs
        if trs.Name().endswith('divswap'):
            msg = 'The current TRS %s already ends with "divswap".' % trs.Name()
            raise BusinessDataError(msg)
        trs_name = trs.Name() + 'divswap'
        if acm.FInstrument[trs_name]:
            msg = 'The updated current TRS %s already exists.' % trs_name
            raise BusinessDataError(msg)
        last_return_reset = self._get_last_return_reset()
        new_reset_value = self._calculate_new_return()
        
        last_return_reset.FixingValue(new_reset_value)
        last_return_reset.Commit()
        trs.Name(trs_name)
        trs.Commit()
    
    def _book_trs_trade(self, trs):
        trs_trade = acm.DealCapturing.CreateNewTrade(trs)
        trs_trade.Counterparty(self._data['Counterparty'])
        trs_trade.Acquirer(self._data['Acquirer'])
        trs_trade.Quantity(self._get_quantity(trs))
        trs_trade.Portfolio(self._data['Portfolio'])
        trs_trade.Trader(self._get_trader())
        trs_trade.Status('Simulated')
        trade_time = acm.Time.TimeNow()
        if self._data['Value Date'] < DATE_TODAY:
            trade_time = self._data['Value Date'] + trade_time[10:]
        trs_trade.TradeTime(trade_time)
        trs_trade.ValueDay(self._data['Value Date'])
        trs_trade.AcquireDay(self._data['Value Date'])
        if self._data['Cpty Portfolio']:
            trs_trade.MirrorPortfolio(self._data['Cpty Portfolio'])
        trs_trade.RegisterInStorage()
        if self._data['Approx. load'] != None:
            trs_trade.AdditionalInfo().Approx_46_load(self._data['Approx. load'])
        if self._data['Approx. load ref']:
            trs_trade.AdditionalInfo().Approx_46_load_ref(self._data['Approx. load ref'])
        if self._data['SND_Cash']:
            trs_trade.AdditionalInfo().SND_Cash(self._data['SND_Cash'])
        if self._data['SND_Nominal']:
            trs_trade.AdditionalInfo().SND_Nominal(self._data['SND_Nominal'])
        if self._data['SND_Rate']:
            trs_trade.AdditionalInfo().SND_Rate(self._data['SND_Rate'])
        trs_trade.Commit()
        return trs_trade
    
    def _add_payment(self, trs_trade):
        payment = self._get_payment()
        if not payment:
            return
        if payment.PayDay() <= self._data['Start Date'] and self._trade:
            payment.Trade(self._trade)
        else:
            payment.Trade(trs_trade)
        payment.Commit()
    
    def _create_new_bsb(self):
        end_date = self.adjust_trs_date(self._data['End Date'])
        bond = self._data['Bond']
        if bond.IsKindOf(acm.FIndexLinkedBond):
            underlying_type = 'IndexLinkedBond'
            underlying_name = 'TRS_%s' % bond.Name()
            underlying = acm.FInstrument[underlying_name]
            if not underlying:
                msg = 'BuySellback underlying does not exist: %s.' % underlying_name
                raise BusinessDataError(msg)
            val_group = GEN_TRS_ILB.ValuationGrpChlItem()
        elif bond.IsKindOf(acm.FBond):
            underlying_type = 'Bond'
            underlying = bond
            val_group = GEN_TRS_BOND.ValuationGrpChlItem()
        else:
            raise BusinessDataError('Invalid underlying: %s.' % bond.Name())
        bsb = acm.FBuySellBack()
        bsb_name = self.get_new_ins_name(bond.Name(), end_date, bsb)
        bsb.Name(bsb_name)
        bsb.DayCountMethod('Act/365')
        bsb.QuoteType('Pct of Nominal')
        bsb.SpotBankingDaysOffset(0)
        bsb.StrikeCurrency(acm.FCurrency['ZAR'])
        bsb.StartDate(PREV_BUSINESS_DAY)
        bsb.ExpiryDate(end_date)
        bsb.UnderlyingType(underlying_type)
        bsb.Underlying(underlying)
        bsb.ValuationGrpChlItem(val_group)
        bsb.Rate(self._data['Repo Rate'])
        bsb.RefPrice(self._data['YTM'])
        bsb.RegisterInStorage()
        bsb.Commit()
        return bsb
    
    def _create_bsb_from_existing(self, orig_bsb, new_name):
        end_date = self.adjust_trs_date(self._data['End Date'])
        bsb = acm.FInstrument[new_name]
        if not bsb or (bsb and bsb.ExpiryDate()[:10] != end_date):
            if bsb:
                new_name = iterate_ins_name(new_name)
            bsb = orig_bsb.StorageNew()
            bsb.Name(new_name)
            bsb.StartDate(PREV_BUSINESS_DAY)
            bsb.ExpiryDate(end_date)
            bsb.Commit()
            self._clear_add_infos(bsb)
        bsb.Rate(self._data['Repo Rate'])
        bsb.RefPrice(self._data['YTM'])
        bsb.Commit()
        return bsb
    
    def _book_bsb_trade(self, bsb):
        if bsb.Trades():
            return
        bsb_trade = acm.DealCapturing.CreateNewTrade(bsb)
        bsb_trade.Status('Simulated')
        bsb_trade.TradeTime(acm.Time.TimeNow())
        bsb_trade.ValueDay(DATE_TODAY)
        bsb_trade.Commit()
    
    def _update_new_trs(self, trs, bsb):
        trs.AdditionalInfo().TRS_Ref_Instrument(bsb)
        trs.Commit()
    
    def _clear_add_infos(self, ins):
        for add_info_name in ADD_INFOS_TO_CLEAR:
            try:
                add_info = getattr(ins.AdditionalInfo(), add_info_name)
            except AttributeError:
                continue
            if not add_info():
                continue
            add_info(None)
            ins.Commit()
    
    def get_action_key(self):
        return '%s - %s' % (self.action_name, self._trade.Name())
    
    def get_orig_trade(self):
        return self._trade
    
    def get_new_trade(self):
        return self._new_trade
    
    def get_new_trs(self):
        return self._new_trs
    
    def performed_successfully(self):
        return self._successful


class ActionRoll(Action):

    action_name = 'Roll'
    
    def __init__(self, data):
        super(ActionRoll, self).__init__(data)
        self._trade = self._data['Trade Number']
        self._trs = self._trade.Instrument()
    
    def _get_new_bsb(self):
        end_date = self.adjust_trs_date(self._data['End Date'])
        orig_trs = self._trs
        orig_bsb = orig_trs.AdditionalInfo().TRS_Ref_Instrument()
        if not orig_bsb:
            msg = 'The current TRS %s has no TRS Ref Instrument.' % orig_trs.Name()
            raise BusinessDataError(msg)
        try:
            bsb_name = self.get_ins_name(orig_bsb.Name(), orig_bsb.ExpiryDate()[:10], end_date)
        except BusinessDataError:
            bsb_name = self.get_new_ins_name(self._data['Bond'].Name(), end_date, orig_bsb)
        return self._create_bsb_from_existing(orig_bsb, bsb_name)
    
    def perform(self):
        self._new_trade = None
        self._new_trs = None
        self._successful = False
        trs = self._roll_trs()
        self._close_old_trs()
        new_trade = self._book_trs_trade(trs)
        self._add_payment(new_trade)
        bsb = self._get_new_bsb()
        self._book_bsb_trade(bsb)
        self._update_new_trs(trs, bsb)
        self._new_trade = new_trade
        self._new_trs = trs
        self._successful = True


class ActionNew(Action):
    
    action_name = 'New'
    
    def _get_new_bsb(self):
        end_date = self.adjust_trs_date(self._data['End Date'])
        bsb_name = self.get_new_ins_name(self._data['Bond'].Name(), end_date, acm.FBuySellBack())
        orig_bsb = acm.FInstrument[bsb_name]
        if not orig_bsb:
            return self._create_new_bsb()
        return self._create_bsb_from_existing(orig_bsb, bsb_name)
    
    def get_action_key(self):
        return '%s - %s_%s_%s' % (self.action_name, self._data['Bond'].Name(),
                                  self._data['Portfolio'].Name(), self._data['End Date'])
    
    def perform(self):
        self._new_trade = None
        self._new_trs = None
        self._successful = False
        trs = self._create_new_trs()
        new_trade = self._book_trs_trade(trs)
        self._add_payment(new_trade)
        bsb = self._get_new_bsb()
        self._book_bsb_trade(bsb)
        self._update_new_trs(trs, bsb)
        self._new_trade = new_trade
        self._new_trs = trs
        self._successful = True


class ActionExpired(Action):
    
    action_name = 'Expired'
    
    def __init__(self, data):
        super(ActionExpired, self).__init__(data)
        self._trade = self._data['Trade Number']
        self._trs = self._trade.Instrument()
    
    def perform(self):
        self._successful = False
        self._close_old_trs()
        self._successful = True


class ActionData(object):
    
    columns = ['Status',] + INPUT_COLUMNS.keys() + DIFF_COLUMNS.keys() + ['Import Error',]
    report_columns = (['Action', 'Trade Number'] + TRADE_SHEET_COLUMNS.keys()
                      + ['Orig %s' % name for name in DIFF_COLUMNS.keys()]
                      + ['Diff %s' % name for name in DIFF_COLUMNS.keys()])
    
    def __init__(self, data_dict, datemode=0):
        self._raw_data = defaultdict(str)
        self._raw_data.update(data_dict)
        self._datemode = datemode
        self._processed_data = {}
        self._error_msg = ''
        self._invalid_columns = []
        self._action = None
        self._valid = False
    
    def _set_invalid(self, column_name):
        self._invalid_columns.append(column_name)
    
    def _validate_acm_object(self, column_name, acm_object):
        if not acm_object:
            self._set_invalid(column_name)
            self._processed_data[column_name] = None
            return
        self._processed_data[column_name] = acm_object
        self._raw_data[column_name] = acm_object.Name()
    
    def _validate_trade(self, column_name):
        try:
            trade_number = int(float(self._raw_data[column_name]))
        except ValueError:
            self._processed_data[column_name] = None
            self._set_invalid(column_name)
            return
        trade = acm.FTrade[trade_number]
        self._validate_acm_object(column_name, trade)
    
    def _validate_party(self, column_name):
        party = acm.FParty[self._raw_data[column_name]]
        self._validate_acm_object(column_name, party)
    
    def _validate_portfolio(self, column_name):
        prf = acm.FPhysicalPortfolio[self._raw_data[column_name]]
        self._validate_acm_object(column_name, prf)
    
    def _validate_date(self, column_name):
        xl_date = self._raw_data[column_name]
        if not xl_date:
            self._processed_data[column_name] = ''
            return
        try:
            dt = xlrd.xldate.xldate_as_datetime(float(xl_date), self._datemode)
            date = dt.strftime('%Y-%m-%d')
        except ValueError:
            self._processed_data[column_name] = ''
            self._set_invalid(column_name)
            return
        self._processed_data[column_name] = date
        self._raw_data[column_name] = date
    
    def _validate_float(self, column_name):
        if not self._raw_data[column_name]:
            self._processed_data[column_name] = None
            return
        try:
            value = float(self._raw_data[column_name])
        except ValueError:
            self._processed_data[column_name] = None
            self._set_invalid(column_name)
            return
        self._processed_data[column_name] = value
    
    def _validate_bond(self, column_name):
        bond = acm.FBond[self._raw_data[column_name]]
        il_bond = acm.FIndexLinkedBond[self._raw_data[column_name]]
        if bond:
            ins = bond
        elif il_bond:
            ins = il_bond
        else:
            ins_name = 'ZAR/%s' % self._raw_data[column_name]
            ins = acm.FInstrument[ins_name]
        self._validate_acm_object(column_name, ins)
    
    def _validate_string(self, column_name):
        raw_data = self._raw_data[column_name]
        self._processed_data[column_name] = raw_data
        if not raw_data:
            return
        try:
            float_data = float(raw_data)
            int_data = int(float_data)
        except ValueError:
            return
        if float_data == int_data:
            self._processed_data[column_name] = str(int_data)
    
    def _validate_bool(self, column_name):
        raw_data = self._raw_data[column_name].upper()
        if not raw_data:
            self._processed_data[column_name] = None
            return
        if raw_data in ('TRUE', 'YES'):
            self._processed_data[column_name] = True
            return
        if raw_data in ('FALSE', 'NO'):
            self._processed_data[column_name] = False
            return
        self._processed_data[column_name] = None
        self._set_invalid(column_name)
    
    def _validate_enum(self, column_name, enum_name):
        if not self._raw_data[column_name]:
            self._processed_data[column_name] = None
            return
        enumerators = acm.FEnumeration[enum_name].Enumerators()
        if self._raw_data[column_name] in enumerators:
            self._processed_data[column_name] = self._raw_data[column_name]
            return
        self._processed_data[column_name] = None
        self._set_invalid(column_name)
    
    def _validate_action(self):
        action_name = self._processed_data['Action']
        errors = []
        if action_name == 'Roll':
            errors = list(set(ROLL_MANDATORY) & set(self._invalid_columns))
            self._action = ActionRoll(self._processed_data)
        elif action_name == 'Expired':
            errors = list(set(EXPIRED_MANDATORY) & set(self._invalid_columns))
            self._action = ActionExpired(self._processed_data)
        elif action_name == 'New':
            errors = list(set(NEW_MANDATORY) & set(self._invalid_columns))
            self._action = ActionNew(self._processed_data)
        else:
            self._error_msg = 'Invalid Action.'
            self._valid = False
            return
        if not errors:
            self._valid = True
            return
        self._error_msg = 'Invalid %s.' % ', '.join(errors)
        self._valid = False
    
    def _calculate_columns(self):
        orig_trade = self._action.get_orig_trade()
        if not orig_trade:
            return
        for column_label, column_id in DIFF_COLUMNS.iteritems():
            value = calc_column_val(column_id, orig_trade)
            if value is None:
                continue
            self._raw_data[column_label] = value
        
    def get_labels(self):
        return [self._raw_data[col] for col in self.columns]
    
    def is_valid(self):
        return self._valid
    
    def validate_data(self):
        self._invalid_columns = []
        for column in self._raw_data:
            if not column in INPUT_COLUMNS:
                continue
            column_type = INPUT_COLUMNS[column]
            if column_type == 'trade':
                self._validate_trade(column)
            elif column_type == 'party':
                self._validate_party(column)
            elif column_type == 'date':
                self._validate_date(column)
            elif column_type == 'float':
                self._validate_float(column)
            elif column_type == 'bond':
                self._validate_bond(column)
            elif column_type == 'portfolio':
                self._validate_portfolio(column)
            elif column_type == 'string':
                self._validate_string(column)
            elif column_type == 'bool':
                self._validate_bool(column)
            elif 'enum' in column_type:
                self._validate_enum(column, column_type)
        self._validate_action()
        if not self.is_valid():
            self._raw_data['Status'] = 'Error'
            self._raw_data['Import Error'] = self._error_msg
        self._calculate_columns()
    
    def get_action(self):
        return self._action
    
    def _get_trade_row(self, trade, action_name, include_diff=False):
        row_dict = defaultdict(str)
        row_dict['Action'] = action_name
        row_dict['Trade Number'] = str(trade.Oid())
        for column_label, column_id in TRADE_SHEET_COLUMNS.iteritems():
            value = calc_column_val(column_id, trade)
            if value is None:
                continue
            row_dict[column_label] = str(value)
        if not include_diff:
            return [row_dict[key] for key in self.report_columns]
        for column_label, column_id in DIFF_COLUMNS.iteritems():
            value = calc_column_val(column_id, trade)
            orig_value = self._raw_data[column_label]
            row_dict['Orig %s' % column_label] = str(orig_value)
            if value is None or orig_value == '':
                continue
            row_dict['Diff %s' % column_label] = str(orig_value - value)
        return [row_dict[key] for key in self.report_columns]
    
    def get_action_rows(self):
        rows = []
        action = self._action
        if not action or not action.performed_successfully():
            return []
        orig_trade = action.get_orig_trade()
        new_trade = action.get_new_trade()
        if orig_trade:
            row = self._get_trade_row(orig_trade, action.action_name, True)
            rows.append(row)
        if new_trade:
            row = self._get_trade_row(new_trade, action.action_name)
            rows.append(row)
        return rows


"""-----------------------------------------------------------------------------
PROJECT                 :  AbCap BTB - Markets IT - Pricing & Risk, Minor Works
PURPOSE                 :  A tool enabling bulk updates of Sales Credits data.
                           For this purpose, the tool provides a user interface,
                           which can be also used to import desired sales 
                           credits data from an excel file, edit the data 
                           and/or add it manually.
DEPATMENT AND DESK      :  Performance Analysis - FDS
REQUESTER               :  Jerome Govender
DEVELOPER               :  Libor Svoboda
CR NUMBER               :  1878341
--------------------------------------------------------------------------------
HISTORY

================================================================================
Date        Change no     Developer           Description
--------------------------------------------------------------------------------
2014-04-14  1878341       Libor Svoboda       Initial Implementation
2014-09-08  2296169       Nico Louw           Included functionality to,
                                              remove all non-ascii chars when
                                              reading input from input file.
2018-11-13  CHG1001100033 Libor Svoboda       Add workaround for triggering CAL 
                                              pop-up and reporting.
"""
import csv
import xlrd
import acm
import FUxCore

# Number of input sets consisting of Sales Person, Sales Credit,
# Value Add, and SalesCreditSubTeam.
INPUT_SETS_NUM = 5
# Name of the excel sheet to import data from.
EXCEL_SHEET = 'Template'
# First row in the excel sheet containing relevant data to import.
FIRST_EXCEL_ROW = 3
# Definition of import filter.
IMPORT_FILTER = 'Excel Files (*.xlsx)|*.xlsx|Excel Files (*.xls)|*.xls|'
# Default directory to import data from and export data to.
INITDIR = 'C:\\'
# Default file to export data to.
DEFAULT_OUTPUT_FILE = 'output.csv'
# Names of columns of displayed as well as exported data.
COLUMNS = (
    'Input Status',
    'Trade Number',
    'Sales Person 1',
    'Sales Credit 1',
    'Value Add 1',
    'SalesCreditSubTeam1',
    'Sales Person 2',
    'Sales Credit 2',
    'Value Add 2',
    'SalesCreditSubTeam2',
    'Sales Person 3',
    'Sales Credit 3',
    'Value Add 3',
    'SalesCreditSubTeam3',
    'Sales Person 4',
    'Sales Credit 4',
    'Value Add 4',
    'SalesCreditSubTeam4',
    'Sales Person 5',
    'Sales Credit 5',
    'Value Add 5',
    'SalesCreditSubTeam5',
    'RWA Counterparty',
    'Relationship Party',
    'Shadow Revenue',
    'Country',
    'Broker Status',
    'Nominal',
    'Portfolio',
    'Trade Date',
    'Counterparty',
    'Trade Status',
    'Error Message',
)
# Additional specifications of input sales credits data ordered
# according to the columns of the input excel file.
INPUT_SPECS = (
    ('Trade Number', 'trade', None),
    ('Sales Person 1', 'user', None),
    ('Sales Credit 1', 'credit', None, '0.0'),
    ('Value Add 1', 'value', 'ValueAddCredits', None),
    ('SalesCreditSubTeam1', 'team', 
        'SalesCreditSubTeam1', 'enum(cl_SalesCreditSubTeam)'),
    ('Sales Person 2', 'user', 'Sales_Person2'),
    ('Sales Credit 2', 'credit', 'Sales_Credit2', None),
    ('Value Add 2', 'value', 'ValueAddCredits2', None),
    ('SalesCreditSubTeam2', 'team', 
        'SalesCreditSubTeam2', 'enum(cl_SalesCreditSubTeam)'),
    ('Sales Person 3', 'user', 'Sales_Person3'),
    ('Sales Credit 3', 'credit', 'Sales_Credit3', None),
    ('Value Add 3', 'value', 'ValueAddCredits3', None),
    ('SalesCreditSubTeam3', 'team', 
        'SalesCreditSubTeam3', 'enum(cl_SalesCreditSubTeam)'),
    ('Sales Person 4', 'user', 'Sales_Person4'),
    ('Sales Credit 4', 'credit', 'Sales_Credit4', None),
    ('Value Add 4', 'value', 'ValueAddCredits4', None),
    ('SalesCreditSubTeam4', 'team', 
        'SalesCreditSubTeam4', 'enum(cl_SalesCreditSubTeam)'),
    ('Sales Person 5', 'user', 'Sales_Person5'),
    ('Sales Credit 5', 'credit', 'Sales_Credit5', None),
    ('Value Add 5', 'value', 'ValueAddCredits5', None),
    ('SalesCreditSubTeam5', 'team', 
        'SalesCreditSubTeam5', 'enum(cl_SalesCreditSubTeam)'),
    ('RWA Counterparty', 'party', 'RWA_Counterparty'),
    ('Relationship Party', 'party', 'Relationship_Party'),
    ('Shadow Revenue', 'enum', 
        'Shadow_Revenue_Type', 'enum(cl_Shadow_Revenue_Type)'),
    ('Country', 'enum', 'Country', 'enum(cl_Country)'),
    ('Broker Status', 'enum', 'Broker Status', 'enum(cl_BrokerStatus)'),
)
# The first three columns of INPUT_SPECS denote the corresponding name,
# data type (i.e. trade, user, credit, value, team or enum) and 
# additional info name as follows.
NAME = 0
DATA_TYPE = 1
ADD_INFO_NAME = 2


def start_dialog(eii):
    """Callback from menu extension to start the main dialog."""
    shell = eii.ExtensionObject().Shell()
    builder = create_layout()
    sc_dialog = SalesCreditsUpdaterDialog()
    acm.UX().Dialogs().ShowCustomDialogModal(shell, builder, sc_dialog)

    
def show_custom_dialog(shell, message, dialog_type):
    """Show a custom dialog.
    
    Arguments:
        shell - parent of the dialog
        message - message to be shown
        dialog_type - type of the dialog
    """
    acm.UX().Dialogs().MessageBox(shell, dialog_type, message, 'OK', 
                                  None, None, 'Button1', 'Button1')


def update_add_info(entity, name, value):
    """Update additional info.
    
    Arguments:
        entity - acm object to be updated
        name - name of additional info
        value - value of additional info
    """    
    add_infos = acm.FAdditionalInfo.Select('recaddr=%d' % entity.Oid())
    index = [i for (i, ai) in enumerate(add_infos) if 
             name == ai.AddInf().Name()]
    if index:
        if not value:
            add_infos.At(index).Delete()
        else:
            add_infos.At(index).FieldValue(value)
            add_infos.At(index).Commit()
    elif value:
        add_info = acm.FAdditionalInfo()
        add_info.Recaddr(entity.Oid())
        add_info.AddInf(acm.FAdditionalInfoSpec[name])
        add_info.FieldValue(value)
        add_info.Commit()


def is_trade_valid(trade_number):
    """Return True if input trade number is valid."""
    if not trade_number:
        return False
        
    if acm.FTrade[trade_number]:
        return True
    else:
        return False


def get_sales_persons(trade_number):
    """Return a dictionary of Sales Persons.
    
    Arguments:
        trade_number - number of a corresponding trade
    """
    trade = acm.FTrade[trade_number]
    return {
        'Sales Person 1': trade.SalesPerson(),
        'Sales Person 2': trade.AdditionalInfo().Sales_Person2(),
        'Sales Person 3': trade.AdditionalInfo().Sales_Person3(),
        'Sales Person 4': trade.AdditionalInfo().Sales_Person4(),
        'Sales Person 5': trade.AdditionalInfo().Sales_Person5(),
    }

    
def get_sales_credits(trade_number):
    """Return a dictionary of Sales Credits.
    
    Arguments:
        trade_number - number of a corresponding trade
    """
    trade = acm.FTrade[trade_number]
    return {
        'Sales Credit 1': trade.SalesCredit(),
        'Sales Credit 2': trade.AdditionalInfo().Sales_Credit2(),
        'Sales Credit 3': trade.AdditionalInfo().Sales_Credit3(),
        'Sales Credit 4': trade.AdditionalInfo().Sales_Credit4(),
        'Sales Credit 5': trade.AdditionalInfo().Sales_Credit5(),
    }


def get_value_add_credits(trade_number):
    """Return a dictionary of Value Add Credits.
    
    Arguments:
        trade_number - number of a corresponding trade
    """
    additional_info = acm.FTrade[trade_number].AdditionalInfo()
    return {
        'Value Add 1': additional_info.ValueAddCredits(),
        'Value Add 2': additional_info.ValueAddCredits2(),
        'Value Add 3': additional_info.ValueAddCredits3(),
        'Value Add 4': additional_info.ValueAddCredits4(),
        'Value Add 5': additional_info.ValueAddCredits5(),
    }


def get_sales_credit_sub_teams(trade_number):
    """Return a dictionary of Sales Credit Sub Teams.
    
    Arguments:
        trade_number - number of a corresponding trade
    """
    additional_info = acm.FTrade[trade_number].AdditionalInfo()
    return {
        'SalesCreditSubTeam1': additional_info.SalesCreditSubTeam1(),
        'SalesCreditSubTeam2': additional_info.SalesCreditSubTeam2(),
        'SalesCreditSubTeam3': additional_info.SalesCreditSubTeam3(),
        'SalesCreditSubTeam4': additional_info.SalesCreditSubTeam4(),
        'SalesCreditSubTeam5': additional_info.SalesCreditSubTeam5(),
    }
    

def get_misc_sc_data(trade_number):
    """Return a dictionary of misc. sales credits data.
    
    Arguments:
        trade_number - number of a corresponding trade
    """
    additional_info = acm.FTrade[trade_number].AdditionalInfo()
    return {
        'RWA Counterparty': additional_info.RWA_Counterparty(),
        'Relationship Party': additional_info.Relationship_Party(),
        'Shadow Revenue': additional_info.Shadow_Revenue_Type(),
        'Country': additional_info.Country(),
        'Broker Status': additional_info.Broker_Status(),
    }
    

def get_other_infos(trade_number):
    """Return a dictionary of other selected trade information.
    
    Arguments:
        trade_number - number of a corresponding trade
    """
    trade = acm.FTrade[trade_number]
    return {
        'Nominal': trade.Nominal(),
        'Portfolio': trade.Portfolio(),
        'Trade Date': trade.TradeTime()[0:10],
        'Counterparty': trade.Counterparty(),
        'Trade Status': trade.Status(),
    }


def get_trade_data(trade_number):
    """Return a dictionary of desired trade information.
    
    Arguments:
        trade_number - number of a corresponding trade
    """
    data_dict = {}
    data_dict['Trade Number'] = trade_number
    data_dict.update(get_sales_persons(trade_number))
    data_dict.update(get_sales_credits(trade_number))
    data_dict.update(get_value_add_credits(trade_number))
    data_dict.update(get_sales_credit_sub_teams(trade_number))
    data_dict.update(get_misc_sc_data(trade_number))
    data_dict.update(get_other_infos(trade_number))
    return data_dict


def read_data_from_row(row):
    """Return a dictionary of sales credits data from input excel row.
    
    Arguments:
        row - list of (xlrd) cell objects
    """
    data_dict = {}
    for i, input_spec in enumerate(INPUT_SPECS):
        try:
            #remove all non-ascii characters from cells 
            if row[i].ctype == 1:
                value = (str("".join(char for char in row[i].value if 
                        ord(char)<128)).strip())
            else:
                value = str(row[i].value)
                
            data_dict[input_spec[NAME]] = value
            
        except IndexError:
            data_dict[input_spec[NAME]] = ''
    return data_dict


class InputError(Exception):
    """Create a custom Input Error Exception."""
    pass


class SalesCreditsUpdaterDialog(FUxCore.LayoutDialog):

    """Handle functionality of the main dialog."""
    
    def __init__(self):        
        self._persons = []
        self._credits = []
        self._values = []
        self._teams = []
        
        self._init_directory = None
        self._table_input = {}
        self._table_input['new'] = 'Data to be updated'
        self._table_input['old'] = 'Current data'

    def HandleCreate(self, dlg, layout):
    
        """Register controls and add callbacks."""
        
        self._fux_dlg = dlg
        self._fux_dlg.Caption('Sales Credits Bulk Updater')
        
        self._add_btn = layout.GetControl('addBtn')
        self._rmv_all_btn = layout.GetControl('rmvAllBtn')
        self._rmv_sel_btn = layout.GetControl('rmvSelBtn')
        self._edit_sel_btn = layout.GetControl('editSelBtn')
        self._ok_btn = layout.GetControl('ok')
        self._cancel_btn = layout.GetControl('cancel')
        self._import_btn = layout.GetControl('importBtn')
        self._export_btn = layout.GetControl('exportBtn')
        self._populate_fields_btn = layout.GetControl('populateFieldsBtn')
        
        self._trade_number = layout.GetControl('tradeNumber')
        for i in range(1, INPUT_SETS_NUM + 1):
            self._persons.append(layout.GetControl('person%d' % i))
            self._credits.append(layout.GetControl('credit%d' % i))
            self._values.append(layout.GetControl('value%d' % i))
            self._teams.append(layout.GetControl('team%d' % i))
            
        self._rwa_counterparty = layout.GetControl('RWACounterparty')
        self._relationship_party = layout.GetControl('relationshipParty')
        self._shadow_revenue = layout.GetControl('shadowRevenue')
        self._country = layout.GetControl('country')
        self._broker_status = layout.GetControl('brokerStatus')
        self._export_path = layout.GetControl('exportPath')
        self._table_option = layout.GetControl('tableOption')
        self._nominal = layout.GetControl('nominal')
        self._portfolio = layout.GetControl('portfolio')
        self._trade_date = layout.GetControl('tradeDate')
        self._trade_status = layout.GetControl('tradeStatus')
        
        self._sc_list = SalesCreditsListControl(layout, 'salesCreditList')
        
        self._populate_fields_btn.AddCallback('Activate', 
                                              self._on_populate_fields, self)
        self._add_btn.AddCallback('Activate', self._on_add, self)
        self._edit_sel_btn.AddCallback('Activate', 
                                       self._on_edit_selected, self)
        self._rmv_all_btn.AddCallback('Activate', self._on_remove_all, self)
        self._rmv_sel_btn.AddCallback('Activate', 
                                      self._on_remove_selected, self)
        self._import_btn.AddCallback('Activate', self._on_import, self)
        self._export_btn.AddCallback('Activate', self._on_export, self)
        self._table_option.AddCallback('Changed',
                                       self._on_show_table_changed, self)
        
        self._set_defaults()

    def _set_defaults(self):
    
        """Set default state of the dialog."""
        
        self._credits[0].SetData('0.0')
        self._export_path.SetData(INITDIR + DEFAULT_OUTPUT_FILE)
        
        users = acm.FUser.Select('')
        users.Add(acm.FUser())
        for i in range(INPUT_SETS_NUM):
            self._persons[i].Populate(users)
            for team in acm.FEnumeration[
                    'enum(cl_SalesCreditSubTeam)'].Enumerators():
                self._teams[i].AddItem(team)                

        parties = acm.FCounterParty.Select('').AsSet()
        parties.Union(acm.FClient.Select(''))
        parties.Add(acm.FCounterParty())
        self._rwa_counterparty.Populate(parties)
        self._relationship_party.Populate(parties)
        
        for revenue_type in acm.FEnumeration[
                'enum(cl_Shadow_Revenue_Type)'].Enumerators():
            self._shadow_revenue.AddItem(revenue_type)

        for country in acm.FEnumeration['enum(cl_Country)'].Enumerators():
            self._country.AddItem(country)

        for broker_status in acm.FEnumeration[
                'enum(cl_BrokerStatus)'].Enumerators():
            self._broker_status.AddItem(broker_status)
            
        self._table_option.AddItem(self._table_input['new'])
        self._table_option.AddItem(self._table_input['old'])
        self._table_option.SetData(self._table_input['new'])
        self._label_type = 'new'
        
        self._nominal.Editable(False)
        self._portfolio.Editable(False)
        self._trade_date.Editable(False)
        self._trade_status.Editable(False)
        
    def HandleApply(self):
        """Perform 'Update' button action."""
        shell = self._fux_dlg.Shell()
        if not self._sc_list.item_count():
            show_custom_dialog(shell, 'No data to be updated.', 'Warning')
        else:
            updated_count = self._sc_list.update_items()
            msg = '%d trade(s) updated successfully!' % updated_count
            show_custom_dialog(shell, msg, 'Information')
        return None

    def _on_populate_fields(self, arg1, arg2):
        """Perform 'Populate Fields' button action."""
        trade_number = self._trade_number.GetData().replace(',', '')
        if is_trade_valid(trade_number):
            data_dict = get_trade_data(trade_number)
            self._populate_fields(data_dict)
        else:
            shell = self._fux_dlg.Shell()
            show_custom_dialog(shell, 'Invalid trade number.', 'Warning')
    
    def _on_add(self, arg1, arg2):
        """Perform 'Add' button action."""
        data_dict = self._read_data_from_fields()
        sc_data = SalesCreditsData(data_dict)
        sc_data.validate_data()
        try:
            self._sc_list.add_item(sc_data)
            self._reload_table()
        except InputError as e:
            shell = self._fux_dlg.Shell()
            show_custom_dialog(shell, '%s.' % e, 'Error')
            
    def _on_edit_selected(self, arg1, arg2):
        """Perform 'Edit Selected' button action."""
        sc_data = self._sc_list.return_and_remove_selected_item()
        if sc_data:
            self._populate_fields(sc_data.get_current_data())
        
    def _on_remove_all(self, arg1, arg2):
        """Perform 'Remove All' button action."""
        self._sc_list.remove_all_items()
       
    def _on_remove_selected(self, arg1, arg2):
        """Perform 'Remove Selected' button action."""
        self._sc_list.remove_selected_item()
        
    def _on_import(self, arg1, arg2):
        """Perform 'Import' button action."""
        shell = self._fux_dlg.Shell()
        directory = self._init_directory if self._init_directory else INITDIR
        selections = acm.UX().Dialogs().BrowseForFiles(shell, IMPORT_FILTER,
                                                       directory)
        if selections:
            for selection in selections:
                self._init_directory = selection.SelectedDirectory().Text()
                path = self._init_directory + selection.SelectedFile().Text()
                self._export_path.SetData(
                    selection.SelectedDirectory().Append(DEFAULT_OUTPUT_FILE))
                self._import_data_from_file(path)
            self._reload_table()
                
    def _on_export(self, arg1, arg2):
        """Perform 'Export' button action."""
        path  = self._export_path.GetData()
        shell = self._fux_dlg.Shell()
        if not self._sc_list.item_count():
            show_custom_dialog(shell, 'No data to be exported.', 'Warning')
            return
        try:
            with open(path, 'wb') as csvfile:
                self._sc_list.export_to_csv(csvfile, self._label_type)
                msg = 'Data exported successfully.'
                show_custom_dialog(shell, msg, 'Information')
        except IOError as e:
            show_custom_dialog(shell, e.strerror, 'Error')
            
    def _on_show_table_changed(self, arg1, arg2):
        """Handle behaviour after changing the 'Show' option."""
        if self._table_option.GetData() == self._table_input['new']:
            self._label_type = 'new'
            self._edit_sel_btn.Enabled(True)
            self._ok_btn.Enabled(True)
        elif self._table_option.GetData() == self._table_input['old']:
            self._label_type = 'old'
            self._edit_sel_btn.Enabled(False)
            self._ok_btn.Enabled(False)
        self._reload_table()
            
    def _populate_fields(self, data_dict):
        """Populate dialog's fields with sales credits data.
        
        Arguments:
            data_dict - dictionary of sales credits data
        """
        self._trade_number.SetData(data_dict['Trade Number'])
        for i in range(INPUT_SETS_NUM):
            self._persons[i].SetData(data_dict['Sales Person %d' %(i+1)])
            self._credits[i].SetData(data_dict['Sales Credit %d' %(i+1)])
            self._values[i].SetData(data_dict['Value Add %d' %(i+1)])
            self._teams[i].SetData(data_dict['SalesCreditSubTeam%d' %(i+1)])
        
        # Check for 'nil' values
        for i in range(INPUT_SETS_NUM):
            if self._credits[i].GetData() == 'nil':
                self._credits[i].SetData('')
            if self._values[i].GetData() == 'nil':
                self._values[i].SetData('')
            
        self._rwa_counterparty.SetData(data_dict['RWA Counterparty'])
        self._relationship_party.SetData(data_dict['Relationship Party'])
        self._shadow_revenue.SetData(data_dict['Shadow Revenue'])
        self._country.SetData(data_dict['Country'])
        self._broker_status.SetData(data_dict['Broker Status'])
        self._nominal.SetData(data_dict['Nominal'])
        self._portfolio.SetData(data_dict['Portfolio'])
        self._trade_date.SetData(data_dict['Trade Date'])
        self._trade_status.SetData(data_dict['Trade Status'])
        
            
    def _read_data_from_fields(self):
        """Return a dictionary of data from dialog's fields."""
        data_dict = {}
        data_dict['Trade Number'] = self._trade_number.GetData()
        for i in range(INPUT_SETS_NUM):
            data_dict['Sales Person %d' %(i+1)] = self._persons[i].GetData()
            data_dict['Sales Credit %d' %(i+1)] = self._credits[i].GetData()
            data_dict['Value Add %d' %(i+1)] = self._values[i].GetData()
            data_dict['SalesCreditSubTeam%d' %(i+1)] = self._teams[i].GetData()
            
        data_dict['RWA Counterparty'] = self._rwa_counterparty.GetData()
        data_dict['Relationship Party'] = self._relationship_party.GetData()
        data_dict['Shadow Revenue'] = self._shadow_revenue.GetData()
        data_dict['Country'] = self._country.GetData()
        data_dict['Broker Status'] = self._broker_status.GetData()
        return data_dict
        
    def _import_data_from_file(self, path):
        """Import data from an excel file.
        
        Arguments:
            path - path to the excel file
        """
        shell = self._fux_dlg.Shell()
        workbook = xlrd.open_workbook(path)
        try:
            worksheet = workbook.sheet_by_name(EXCEL_SHEET)
        except xlrd.XLRDError:
            msg = ("The file '%s' does not contain any sheet named '%s'."
                   % (path, EXCEL_SHEET))
            show_custom_dialog(shell, msg, 'Error')
            return
        curr_row = FIRST_EXCEL_ROW - 1
        num_rows = worksheet.nrows
        while curr_row < num_rows:
            row = worksheet.row(curr_row)
            if row[0].value:
                data_dict = read_data_from_row(row)
                sc_data = SalesCreditsData(data_dict)
                sc_data.validate_data()
                try:
                    self._sc_list.add_item(sc_data)
                except InputError as e:
                    msg = 'Input Error at row %d: %s.' % (curr_row+1, e)
                    show_custom_dialog(shell, msg, 'Error')
                curr_row += 1
            else:
                msg = ('Finished importing at row %d due to a blank trade'
                       ' number field.' % (curr_row+1))
                show_custom_dialog(shell, msg, 'Information')
                break
            
    def _reload_table(self):
        """Reload shown data in dialog's table."""
        self._sc_list.refresh_labels(self._label_type)


class SalesCreditsListControl(object):

    """Control functionality of the list of sales credits data.
    
    Instance variables:
        _list_control - FUxListControl object for storing sales credits
            data
            
    Public methods:
        item_count - return number of items in the list
        export_to_csv - export data from the list to a csv file
        remove_all_items - remove all items from the list
        remove_selected_item - remove selected item from the list
        return_and_remove_selected_item - return and then remove
            selected item from the list
        add_item - add item to the list
        refresh_labels - refresh list labels
        update_items - commit list items
    """
    
    def __init__(self, layout, name):
        """Initialize _list_control.
        
        Arguments:
            layout - FUxLayout object
            name - name of the control
        """
        self._list_control = layout.GetControl(name)
        self._list_control.ShowGridLines()
        self._list_control.ShowColumnHeaders()
        
        for column in COLUMNS:
            self._list_control.AddColumn(column, -1, '')
            
        self._adjust_column_widths()
        
    def _adjust_column_widths(self):
        """Adjust column widths to fit the data."""
        for i in range(self._list_control.ColumnCount()):
            self._list_control.AdjustColumnWidthToFitItems(i)
    
    def item_count(self):
        """Return number of items in the list."""
        root_item = self._list_control.GetRootItem()
        return root_item.ChildrenCount()
        
    def export_to_csv(self, csvfile, label_type):
        """Export data from the list to a csv file."""
        root_item = self._list_control.GetRootItem()
        writer = csv.writer(csvfile, dialect='excel')
        writer.writerow(COLUMNS)
        for child in root_item.Children():
            labels = child.GetData().get_labels(label_type)
            writer.writerow(labels)
            
    def remove_all_items(self):
        """Remove all items from the list."""
        self._list_control.RemoveAllItems()
        self._adjust_column_widths()
        
    def remove_selected_item(self):
        """Remove selected item from the list."""
        self._list_control.RemoveAllSelectedItems(False)
        self._adjust_column_widths()
        
    def return_and_remove_selected_item(self):
        """Return and then remove selected item from the list."""
        if self._list_control.SelectedCount():
            selected_item = self._list_control.GetSelectedItem().GetData()
            self.remove_selected_item()
            return selected_item
            
    def add_item(self, sc_data):
        """Add item to to the list.
        
        Arguments:
            sc_data - SalesCreditsData object
        """
        root_item = self._list_control.GetRootItem()
        trades_in_list = [child.GetData().get_trade_number() 
                          for child in root_item.Children()]
        if sc_data.get_trade_number() in trades_in_list:
            raise InputError("Duplicate trade number '%s'" 
                             % (sc_data.get_trade_number()))
        child = root_item.AddChild()
        child.SetData(sc_data)
    
    def refresh_labels(self, label_type):
        """Refresh list labels.
        
        Arguments:
            label_type - type of labels, i.e. either 'old' or 'new'
        """
        root_item = self._list_control.GetRootItem()
        for child in root_item.Children():
            labels = child.GetData().get_labels(label_type)
            for i in range(len(labels)):
                child.Label(labels[i], i)
        self._adjust_column_widths()
        
    def update_items(self):
        """Commit list items and return their count."""
        updated_items_count = 0
        root_item = self._list_control.GetRootItem()
        for child in root_item.Children():
            if child.GetData().update_data():
                updated_items_count += 1
        return updated_items_count


class SalesCreditsData(object):
    
    """Handle sales credits data validation and transformation.
    
    Instance variables:
        _new_data - dictionary of input (to be updated) sales credits
            data
        _old_data - dictionary of current sales credits data
        _valid - boolean representing validity of input data
    
    Public methods:
        validate_data - validate and transform input data
        update_data - commit updates to the database
        get_labels - return a list of string representations of the
            data corresponding to the COLUMNS entries
        get_trade_number - return the corresponding trade number
        get_current_data - return a dictionary of current data
    """
    
    def __init__(self, data_dict):
        """Initialize instance variables.
        
        Arguments:
            data_dict - input dictionary of sales credits data
        """
        self._new_data = {}
        self._old_data = {}
        for column in COLUMNS:
            self._new_data[column] = ''
            self._old_data[column] = ''
        
        self._new_data['Input Status'] = 'Valid'
        self._old_data['Input Status'] = 'Valid'
        self._old_data['Trade Number'] = data_dict['Trade Number']
        self._new_data.update(data_dict)
        self._valid = True
    
    def _set_invalid(self, message):
        """Set invalid input data flag.
        
        Arguments:
            message - message describing the cause of invalid data
        """
        self._valid = False
        self._new_data['Input Status'] = 'Invalid'
        # Input Status of _old_data is just for information purposes
        # and is in fact related to _new_data.
        self._old_data['Input Status'] = 'Invalid'
        self._new_data['Error Message'] += message
        
    def _validate_trade(self, message, input_spec):
        """Ensure that input trade number and the corresponding trade
        is valid (i.e. is not archived, terminated or void, and is not
        from any prior year).
        
        Arguments:
            message - message describing the cause of invalid data
            input_spec - corresponding tuple from INPUT_SPECS
        """
        name, _, _ = input_spec
        trade_number = self._new_data[name].replace(',', '')
        
        try:
            # Float casting needed due to input excel format.
            trade_number = str(int(float(trade_number)))
        except ValueError:
            self._set_invalid(message)
            return
            
        self._new_data[name] = trade_number
        
        trade = acm.FTrade[trade_number]
        if trade:
            self._new_data.update(get_other_infos(trade_number))
            #self._old_data.update(get_trade_data(trade_number))
        else:
            self._set_invalid(message)
            return
        
        temp_message = ''
        if trade.ArchiveStatus() is 1:
            temp_message += 'No change allowed to Archived trades. '
            
        if trade.Status() in ['Terminated', 'Void']:
            temp_message += 'No change allowed to %s trades. ' % trade.Status()
            
        if trade.TradeTime()[0:4] != acm.Time().DateToday()[0:4]:
            temp_message += 'No change allowed to prior years trades. '
            
        if temp_message:
            self._set_invalid(message + temp_message)

    def _validate_user(self, message, input_spec):
        """Ensure that input user is valid or None.
        
        Arguments:
            message - message describing the cause of invalid data
            input_spec - corresponding tuple from INPUT_SPECS
        """
        name, _, _ = input_spec
        user = self._new_data[name]
            
        if not user:
            user = None
        elif isinstance(user, basestring):
            if acm.FUser[user]:
                user = acm.FUser[user]
            else:
                self._set_invalid(message)
                return
        elif not user.Name():
            user = None
            
        self._new_data[name] = user

    def _validate_credit(self, message, input_spec):
        """Ensure that input credit is valid or None.
        
        Arguments:
            message - message describing the cause of invalid data
            input_spec - corresponding tuple from INPUT_SPECS
        """
        name, _, _, default_value = input_spec
        credit = self._new_data[name]
        
        if not credit:
            if default_value:
                credit = default_value
            else:
                credit = None
        else:
            try:
                credit = str(float(credit))
            except ValueError:
                self._set_invalid(message)
                return
        
        self._new_data[name] = credit
    
    def _validate_enum(self, message, input_spec):
        """Ensure that input belongs to a specific enum type or is None.
        
        Arguments:
            message - message describing the cause of invalid data
            input_spec - corresponding tuple from INPUT_SPECS
        """
        name, _, _, enum_type = input_spec
        item = self._new_data[name]
        
        if not item:
            self._new_data[name] = None
        elif item not in acm.FEnumeration[enum_type].Enumerators():
            self._set_invalid(message)

    def _validate_party(self, message, input_spec):
        """Ensure that input party is valid or None.
        
        Arguments:
            message - message describing the cause of invalid data
            input_spec - corresponding tuple from INPUT_SPECS
        """
        name, _, _ = input_spec
        party = self._new_data[name]
            
        if not party:
            party = None
        elif isinstance(party, basestring):
            if acm.FCounterParty[party]:
                party = acm.FCounterParty[party]
            elif acm.FClient[party]:
                party = acm.FClient[party]
            else:
                self._set_invalid(message)
                return
        elif not party.Name():
            party = None
            
        self._new_data[name] = party
        
    def _validate_person_change(self, person_key, credit_key, value_key):
        """Set values of Sales Person, Credit and Value Add if once
        populated Sales Person is attempted to be deleted.
        
        Arguments:
            person_key - key representing Sales Person
            credit_key - key representing Sales Credit
            value_key - key representing Value Add Credits
        """
        if not self._new_data[person_key] and self._old_data[person_key]:
            self._new_data[person_key] = self._old_data[person_key]
            self._new_data[credit_key] = '0.0'
            self._new_data[value_key] = '0.0'
    
    def _is_input_set_valid(self, person_key, credit_key, value_key, team_key):
        """Validate combination of Sales Person, Credit, Value Add
        and SubTeam.
        
        Arguments:
            person_key - key representing Sales Person
            credit_key - key representing Sales Credit
            value_key - key representing Value Add Credits
            team_key - key representing SalesCreditSubTeam
        """
        person = self._new_data[person_key]
        credit = self._new_data[credit_key]
        value = self._new_data[value_key]
        team = self._new_data[team_key]                
        if person and (credit or value):
            return True
        if not (person or team or value or (credit and float(credit))):
            return True
        return False

    def _are_persons_unique(self, person_keys):
        """Validate that persons are unique.
        
        Arguments:
            person_keys - list of keys representing Sales Persons
            
        Returns:
            True if no Sales Person is used more than once
        """
        persons = filter(bool, [self._new_data[key] for key in person_keys])
        return len(set(persons)) == len(persons)
            
    def _get_keys(self, data_type):
        """Return a list of keys corresponding to a specific
        data type as in INPUT_SPECS.
        
        Arguments:
            data_type - data type as in INPUT_SPECS
        """
        return [input_spec[NAME] for input_spec in 
                INPUT_SPECS if input_spec[DATA_TYPE] == data_type]

    def validate_data(self):
        """Validate and transform raw sales credits data."""
        for input_spec in INPUT_SPECS:
            message = 'Invalid %s. ' % input_spec[NAME]
            if input_spec[DATA_TYPE] == 'trade':
                self._validate_trade(message, input_spec)
            elif input_spec[DATA_TYPE] == 'user':
                self._validate_user(message, input_spec)
            elif (input_spec[DATA_TYPE] == 'credit' or 
                    input_spec[DATA_TYPE] == 'value'):
                self._validate_credit(message, input_spec)
            elif (input_spec[DATA_TYPE] == 'enum' or 
                    input_spec[DATA_TYPE] == 'team'):
                self._validate_enum(message, input_spec)
            elif input_spec[DATA_TYPE] == 'party':
                self._validate_party(message, input_spec)
                
        if not self._valid:
            return
            
        persons = self._get_keys('user')
        credits = self._get_keys('credit')
        values = self._get_keys('value')
        teams = self._get_keys('team')
        if not self._are_persons_unique(persons):
            self._set_invalid('Same Sales Person should not be '
                              'populated in more than one field. ')
            
        for person, credit, value, team in zip(persons, credits, 
                                               values, teams):
            if not self._is_input_set_valid(person, credit, value, team):
                self._set_invalid('Invalid combination of %s, %s, %s and %s. '
                                  % (person, credit, value, team))
                
            if self._valid:
                self._validate_person_change(person, credit, value)

    def update_data(self):
        """Commit updates to the database."""
        if self._valid:
            trade = acm.FTrade[self.get_trade_number()]
            
            acm.BeginTransaction()
            trade.SalesPerson(self._new_data['Sales Person 1'])
            # Workaround for triggering CAL pop-up and reporting,
            # can be reverted as soon as the CAL solution supports trade add infos.
            trade.SalesCredit(float(self._new_data['Sales Credit 1']) + 1e-6)
            trade.Commit()
        
            
            for input_spec in INPUT_SPECS:
                if input_spec[ADD_INFO_NAME]:
                    update_add_info(trade, input_spec[ADD_INFO_NAME], 
                                    self._new_data[input_spec[NAME]])
            acm.CommitTransaction()
            # Update current state of 'old' data.
            self._old_data.update(get_trade_data(self.get_trade_number()))
            return True
        else:
            return False
        
    def get_labels(self, label_type):
        """Return a list of string representations of the data 
        corresponding to COLUMNS.
        
        Arguments:
            label_type - 'old' resp. 'new' corresponding to the current
                resp. updated sales credits data
        """
        data = self._new_data if label_type == 'new' else self._old_data
        labels = [data[col] for col in COLUMNS]
            
        for i in range(len(labels)):
            try:
                labels[i] = labels[i].Name()
            except AttributeError:
                pass
            
        return labels
        
    def get_trade_number(self):
        """Return the corresponding trade number."""
        return self._new_data['Trade Number']
        
    def get_current_data(self):
        """Return a dictionary of current data (i.e. _new_data)."""
        return self._new_data


def create_layout():
    """Return dialog layout."""
    b = acm.FUxLayoutBuilder()
    b.BeginVertBox('None')
    b. BeginHorzBox('EtchedIn', 'Sales Credits Data')
    b.  BeginVertBox('None')
    b.   BeginHorzBox('None')
    b.    AddButton('importBtn', 'Import')
    b.    AddButton('rmvAllBtn', 'Remove All')
    b.    AddButton('rmvSelBtn', 'Remove Selected')
    b.    AddButton('editSelBtn', 'Edit Selected')
    b.    AddOption('tableOption', 'Show')
    b.   EndBox()
    b.   AddList('salesCreditList', 10, -1, 50)
    b.   AddInput('exportPath', 'CSV File')
    b.  EndBox()
    b.  BeginVertBox('None')
    b.   AddFill()
    b.   AddButton('ok', 'Update')
    b.   AddButton('exportBtn', 'Export')
    b.  EndBox()
    b. EndBox()
    b. BeginHorzBox('EtchedIn', 'Edit Sales Credits')
    b.  BeginVertBox('None')
    b.   BeginHorzBox('None')
    b.    AddInput('tradeNumber', 'Trade Number')
    b.    AddButton('populateFieldsBtn', 'Populate Fields')
    b.    AddFill()
    b.   EndBox()
    b.   BeginHorzBox('None')
    b.    BeginVertBox('EtchedIn', 'Sales Person')
    b.     AddOption('person1', 'Sales Person 1')
    b.     AddOption('person2', 'Sales Person 2')
    b.     AddOption('person3', 'Sales Person 3')
    b.     AddOption('person4', 'Sales Person 4')
    b.     AddOption('person5', 'Sales Person 5')  
    b.    EndBox()
    b.    BeginVertBox('EtchedIn', 'Standard Sales Credit')
    b.     AddInput('credit1', 'Sales Credit 1')
    b.     AddInput('credit2', 'Sales Credit 2')
    b.     AddInput('credit3', 'Sales Credit 3')
    b.     AddInput('credit4', 'Sales Credit 4')
    b.     AddInput('credit5', 'Sales Credit 5')
    b.    EndBox()
    b.    BeginVertBox('EtchedIn', 'Value Add')
    b.     AddInput('value1', 'Value Add 1')
    b.     AddInput('value2', 'Value Add 2')
    b.     AddInput('value3', 'Value Add 3')
    b.     AddInput('value4', 'Value Add 4')
    b.     AddInput('value5', 'Value Add 5')
    b.    EndBox()
    b.   EndBox()
    b.   BeginHorzBox('None')
    b.    BeginVertBox('EtchedIn', 'Sales Credit Sub Team')
    b.     AddOption('team1', 'SalesCreditSubTeam1')
    b.     AddOption('team2', 'SalesCreditSubTeam2')
    b.     AddOption('team3', 'SalesCreditSubTeam3')
    b.     AddOption('team4', 'SalesCreditSubTeam4')
    b.     AddOption('team5', 'SalesCreditSubTeam5')
    b.    EndBox()
    b.    BeginVertBox('EtchedIn', 'Misc')
    b.     AddOption('RWACounterparty', 'RWA Counterparty')
    b.     AddOption('relationshipParty', 'Relationship Party')
    b.     AddOption('shadowRevenue', 'Shadow Revenue')
    b.     AddOption('country', 'Country')
    b.     AddOption('brokerStatus', 'Broker Status')
    b.    EndBox()
    b.   EndBox()
    b.   BeginHorzBox('EtchedIn', 'Other')
    b.    BeginVertBox('None')
    b.     AddInput('nominal', 'Nominal')
    b.     AddInput('portfolio', 'Portfolio')
    b.    EndBox()
    b.    AddSpace(20)
    b.    BeginVertBox('None')
    b.     AddInput('tradeDate', 'Trade Date')
    b.     AddInput('tradeStatus', 'Trade Status')
    b.    EndBox()
    b.   EndBox()
    b.  EndBox()
    b.  BeginVertBox('None')
    b.   AddFill()
    b.   AddButton('addBtn', 'Add')
    b.  EndBox()
    b. EndBox()
    b. BeginHorzBox('None')
    b.  AddFill()
    b.  AddButton('cancel', 'Cancel')
    b. EndBox()
    b.EndBox()
    return b

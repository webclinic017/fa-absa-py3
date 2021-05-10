""" Compiled: 2020-09-18 10:38:52 """

#__src_file__ = "extensions/BDExport/./etc/FCustomExportSetupDialog.py"
import acm
import FUxCore
import FLogger
import FExportUtils
import FExportBaseConfiguration
logger = FLogger.FLogger.GetLogger("BD Export")


class FCustomExportSetupDialog(FUxCore.LayoutDialog):

    def __init__(self, shell, params):
        self.shell = shell
        self.caption = 'Custom Export Setup'
        self.params = self.__parse_params(params['selected'])
        self.m_fuxDlg = None

        # Custom Integration Module
        self.custom_integration = None

        # Sheet Template Creation variables
        self.sheet_template_grid = None
        self.sheet_template_button = None

        # FUxWorkbook sheet variables
        self.t_sheet_control = None
        self.p_sheet_control = None

        self.t_sheet = None
        self.p_sheet = None
        
        # List of created objects
        self.created_trade_state_chart = ''
        self.created_ins_state_chart = ''
        self.created_ins_sheet = ''
        self.created_trade_sheet = ''

        # Additional Info panel
        self.add_info_list = None
        self.create_add_info_button = None

        # Sheet Template panel
        self.trade_checked = None
        self.trade_sheet_name = None
        self.trade_group_label = None
        self.trade_state_chart = None

        self.instrument_checked = None
        self.instrument_sheet_name = None
        self.instrument_group_label = None
        self.instrument_state_chart = None
        self.create_sheet_templates_button = None

        # New Trade Status panel
        self.trade_status_name = None
        self.create_trade_status_button = None
        
        # Create party contact add info
        self.create_contact_add_infos_checkbox = None
        self.create_contact_add_info_button = None

        # Create state chart add info
        self.create_state_chart_add_infos_checkbox = None
        self.create_state_chart_add_info_button = None
        
        # Create All and Cancel buttons
        self.create_all_button = None
        self.cancel_button = None
        # Return dict of dialog box
        self.return_dictionary = acm.FDictionary()

    def __parse_params(self, params):
        parameters = params.At(0).split('|')
        params_dict = {}
        for param in parameters:
            key, value = param.split('=')
            params_dict[key] = value
        return params_dict
		
		
    def HandleCancel(self):
        resultDic = acm.FDictionary()
        result  = 'Custom=' + self.params['Custom']
        result = result + '|State Chart=' + self.created_trade_state_chart
        result = result + '|TradeSheet=' + self.created_trade_sheet
        result = result + '|InsSheet=' + self.created_ins_sheet
        result = result + '|insStateChart=' + self.created_ins_state_chart
        resultDic.AtPut('result', [result])
        self.return_dictionary = resultDic
        return 1

    def HandleApply(self):
        resultDic = acm.FDictionary()
        result  = 'Custom=' + self.params['Custom']
        result = result + '|State Chart=' + self.created_trade_state_chart
        result = result + '|TradeSheet=' + self.created_trade_sheet
        result = result + '|InsSheet=' + self.created_ins_sheet
        result = result + '|insStateChart=' + self.created_ins_state_chart
        resultDic.AtPut('result', [result])
        self.return_dictionary = resultDic
        return resultDic

    def HandleCreate(self, dlg, layout):

        self.m_fuxDlg = dlg
        self.m_fuxDlg.Caption(self.caption)

        self.t_sheet_control = layout.GetControl('trade_sheet')
        self.t_sheet_control.Visible(False)

        self.p_sheet_control = layout.GetControl('price_sheet')
        self.p_sheet_control.Visible(False)

        self.t_sheet = self.t_sheet_control.GetCustomControl()
        self.p_sheet = self.p_sheet_control.GetCustomControl()

        module = acm.GetDefaultContext().GetModule(self.params['Custom'])
        if module:
            self.custom_integration = FExportUtils.import_custom_integration_module(self.params['Custom'])

        # Additional Info
        self.add_info_list = layout.GetControl('add_info_list')
        self.add_info_list.ShowGridLines()
        self.add_info_list.EnableMultiSelect()
        self.add_info_list.ShowColumnHeaders()
        self.add_info_list.ShowCheckboxes()
        self.add_info_list.AddColumn('Object Type', -1, '')
        self.add_info_list.AddColumn('Additional Info Name', -1, '')

        self.create_add_info_button = layout.GetControl('create_add_infos_button')
        self.create_add_info_button.AddCallback('Activate', self.__on_create_add_infos_clicked, None)
        
        
        # Create party contact add info
        self.create_contact_add_infos_checkbox = layout.GetControl('create_contact_add_infos_checkbox')
        self.create_contact_add_info_button = layout.GetControl('create_contact_add_info')
        self.create_contact_add_info_button.AddCallback('Activate', self.__on_create_contact_add_infos_clicked, None)
        
        # Create state chart add info
        self.create_state_chart_add_infos_checkbox = layout.GetControl('state_chart_add_infos_checkbox')
        self.create_state_chart_add_info_button = layout.GetControl('state_chart_add_info')
        self.create_state_chart_add_info_button.AddCallback('Activate', self.__on_create_state_chart_add_infos_clicked, None)
        
        
        if module:
            try:
                add_infos = self.custom_integration.add_info
            except NameError:
                add_infos = {}

            rootItem = self.add_info_list.GetRootItem()
            for key in add_infos:
                list = add_infos[key]
                for item in list:
                    child = rootItem.AddChild()
                    child.Label(key, 0)
                    child.Label(item, 1)
                    child.SetData([key, item])

            self.add_info_list.AdjustColumnWidthToFitItems(1)
        else:
            self.add_info_list.Enabled(False)
            self.create_add_info_button.Enabled(False)

        # Sheet Template
        self.trade_checked = layout.GetControl('trade_checkbox')
        self.trade_sheet_name = layout.GetControl('trade_sheet_name')
        self.trade_group_label = layout.GetControl('trade_group')
        self.trade_state_chart = layout.GetControl('trade_state_chart')

        trade_group_prefix = True if "trade_group_prefix" in dir(self.custom_integration) else False
        instrument_group_prefix = True if "instrument_group_prefix" in dir(self.custom_integration) else False

        if module and trade_group_prefix:
            self.trade_checked.Checked(True)
            self.trade_checked.AddCallback('Activate', self.__on_trade_check, None)
            [self.trade_group_label.AddItem(group)
             for group in self.__get_column_groups_from_module(module,
                                                               self.custom_integration.trade_group_prefix())]
            self.trade_group_label.SetData(self.trade_group_label.GetItemAt(0))
        else:
            self.trade_checked.Enabled(False)
            self.trade_checked.Checked(False)
            self.trade_sheet_name.Enabled(False)
            self.trade_group_label.Enabled(False)
            self.trade_state_chart.Enabled(False)

        self.trade_state_chart.SetData(self.params['State Chart'])

        self.instrument_checked = layout.GetControl('instrument_checkbox')
        self.instrument_checked.Checked(False)

        self.instrument_sheet_name = layout.GetControl('price_sheet_name')
        self.instrument_sheet_name.Enabled(False)

        self.instrument_group_label = layout.GetControl('instrument_group')
        self.instrument_group_label.Enabled(False)

        self.instrument_state_chart = layout.GetControl('instrument_state_chart')
        self.instrument_state_chart.SetData(self.params['insStateChart'])
        self.instrument_state_chart.Enabled(False)

        if module and instrument_group_prefix:
            self.instrument_checked.AddCallback('Activate', self.__on_instrument_check, None)
            [self.instrument_group_label.AddItem(group)
             for group in self.__get_column_groups_from_module(module,
                                                               self.custom_integration.instrument_group_prefix())]
            self.instrument_group_label.SetData(self.instrument_group_label.GetItemAt(0))
        else:
            self.instrument_checked.Enabled(False)

        self.create_sheet_templates_button = layout.GetControl('create_sheet_templates_button')

        if module and (trade_group_prefix or instrument_group_prefix):
            self.create_sheet_templates_button.AddCallback('Activate', self.__on_create_sheet_template_clicked, None)
        else:
            self.create_sheet_templates_button.Enabled(False)

        # Trade status
        self.trade_status_name = layout.GetControl('trade_status_name')
        self.create_trade_status_button = layout.GetControl('create_trade_status_button')
        self.create_trade_status_button.AddCallback('Activate', self.__on_create_trade_status_clicked, None)

        # Create and Cancel button
        self.create_all_button = layout.GetControl('create_all')
        self.create_all_button.AddCallback('Activate', self.__on_create_all_clicked, None)

        self.cancel_button = layout.GetControl('ok')

    @FUxCore.aux_cb
    def __on_trade_check(self, ud, cd):
        if self.trade_checked.Checked():
            self.trade_sheet_name.Enabled(True)
            self.trade_group_label.Enabled(True)
            self.trade_state_chart.Enabled(True)
        else:
            self.trade_sheet_name.Enabled(False)
            self.trade_group_label.Enabled(False)
            self.trade_state_chart.Enabled(False)

    @FUxCore.aux_cb
    def __on_instrument_check(self, ud, cd):
        if self.instrument_checked.Checked():
            self.instrument_sheet_name.Enabled(True)
            self.instrument_group_label.Enabled(True)
            self.instrument_state_chart.Enabled(True)
        else:
            self.instrument_sheet_name.Enabled(False)
            self.instrument_group_label.Enabled(False)
            self.instrument_state_chart.Enabled(False)

    @FUxCore.aux_cb
    def __on_create_add_infos_clicked(self, arg1=None, arg2=None):
        checked_items = self.add_info_list.GetCheckedItems()
        for item in checked_items:
            FExportUtils.create_add_info(item.GetData()[0], item.GetData()[1])
            
    @FUxCore.aux_cb
    def __on_create_contact_add_infos_clicked(self, arg1=None, arg2=None):
        FExportBaseConfiguration.CheckContactInfo()
    
    @FUxCore.aux_cb
    def __on_create_state_chart_add_infos_clicked(self, arg1=None, arg2=None):
        FExportUtils.create_add_info("StateChart", 'StateChartType')
        

    @FUxCore.aux_cb
    def __on_create_sheet_template_clicked(self, arg1=None, arg2=None):
        self.__create_state_charts(self.trade_state_chart.GetData(), self.instrument_state_chart.GetData())
        self.__create_sheet_templates()

    @FUxCore.aux_cb
    def __on_create_trade_status_clicked(self, arg1=None, arg2=None):
        self.__create_trade_status()

    @FUxCore.aux_cb
    def __on_create_all_clicked(self, arg1, arg2):
        if self.create_add_info_button.Enabled():
            self.__on_create_add_infos_clicked()

        if self.create_sheet_templates_button.Enabled():
            self.__on_create_sheet_template_clicked()

        self.__on_create_trade_status_clicked()
        
        if self.create_contact_add_infos_checkbox.Checked():
            FExportBaseConfiguration.CheckContactInfo()
            
        if self.create_state_chart_add_infos_checkbox.Checked():
            FExportUtils.create_add_info("StateChart", 'StateChartType')
            

    def __get_column_groups_from_module(self, module, prefix):
        groups = acm.FSet()
        for column in module.GetAllExtensions('FColumnDefinition'):
            column_creator_template = acm.Sheet().Column().GetCreatorTemplate(column.Name(),
                                                                              acm.GetDefaultContext())
            group_label = column_creator_template.GroupLabel()
            if group_label.Text().startswith(prefix):
                groups.Add(group_label)

        return groups

    def __create_trade_state_chart(self, state_chart_name):
        if state_chart_name:
            try:
                FExportUtils.CreateStandardExportStateChart(state_chart_name)
                self.created_trade_state_chart = state_chart_name
            except:
                FExportUtils.CreateStandardExportStateChart(state_chart_name)
                self.created_trade_state_chart = state_chart_name

    def __create_instrument_state_chart(self, state_chart_name):
        if state_chart_name:
            try:
                FExportUtils.CreateInstrumentExportStateChart(state_chart_name)
                self.created_ins_state_chart = state_chart_name
            except:
                FExportUtils.CreateInstrumentExportStateChart(state_chart_name)
                self.created_ins_state_chart = state_chart_name

    def __create_state_charts(self, trade_state_chart, instrument_state_chart):
        self.__create_trade_state_chart(trade_state_chart)
        self.__create_instrument_state_chart(instrument_state_chart)

    def __create_sheet_templates(self):
        context = acm.GetDefaultContext()
        module = context.GetModule(self.params['Custom'])
        if module:
            if self.trade_checked.Checked():
                if self.trade_sheet_name.GetData():
                    parameters = acm.FDictionary()
                    parameters[acm.FSymbol('StateChart')] = acm.FStateChart[self.trade_state_chart.GetData()] \
                        if self.trade_state_chart.GetData() else ''

                    t_columns = []
                    for column in module.GetAllExtensions('FColumnDefinition'):
                        if column.Definition() and 'tradesheet' in column.Definition().Memberships()['sheet columns']:
                            t_columns.append(column)

                    self.t_sheet.Name('Trades')
                    self.__create_sheet_template(self.t_sheet, self.trade_sheet_name.GetData(), t_columns,
                                                self.trade_group_label.GetData(), parameters)
                else:
                    acm.UX.Dialogs().MessageBoxInformation(self.m_fuxDlg.Shell(),
                                                           'Please enter a name for Trade Sheet Template.')

            if self.instrument_checked.Checked():
                if self.instrument_sheet_name.GetData():
                    parameters = acm.FDictionary()
                    parameters[acm.FSymbol('StateChart')] = acm.FStateChart[self.instrument_state_chart.GetData()] \
                        if self.instrument_state_chart.GetData() else ''

                    p_columns = []
                    for column in module.GetAllExtensions('FColumnDefinition'):
                        if column.Definition() and 'dealsheet' in column.Definition().Memberships()['sheet columns']:
                            p_columns.append(column)

                    self.p_sheet.Name('Instruments')
                    self.__create_sheet_template(self.p_sheet, self.instrument_sheet_name.GetData(), p_columns,
                                                self.instrument_group_label.GetData(), parameters)
                else:
                    acm.UX.Dialogs().MessageBoxInformation(self.m_fuxDlg.Shell(),
                                                           'Please enter a name for Instrument Sheet Template.')

    def __create_sheet_template(self, ux_sheet, template_name, columns, group_label, parameters):
        column_creators = ux_sheet.ColumnCreators()
        column_creators.Clear()
        for column in columns:
            new_column_creator_template = acm.Sheet().Column().GetCreatorTemplate(column.Name(),
                                                                                  acm.GetDefaultContext())
            if new_column_creator_template.GroupLabel().Text() == group_label:
                new_column_creator = new_column_creator_template.CreateCreator(
                    acm.Sheet().Column().CreatorConfigurationFromColumnParameterDefinitionNamesAndValues(parameters))
                column_creators.Add(new_column_creator)

        t_trading_sheet_template = acm.FTradingSheetTemplate[template_name]
        if not t_trading_sheet_template:
            t_trading_sheet_template = acm.FTradingSheetTemplate()
            t_trading_sheet_template.Name(template_name)
            t_trading_sheet_template.AutoUser(False)
            t_trading_sheet_template.Commit()

        ux_sheet.ApplyToTemplate(t_trading_sheet_template)
        t_trading_sheet_template.Commit()
        logger.info("Trading Sheet Template {} created successfully.".format(template_name))
        if ux_sheet.Name() == 'Trades':
            self.created_trade_sheet = template_name
        if ux_sheet.Name() == 'Instruments':
            self.created_ins_sheet = template_name
        

    def __create_trade_status(self):
        status_name = self.trade_status_name.GetData()
        if status_name:
            trade_status = acm.FTradeStatusValue.Select('systemName =' + status_name)
            if not trade_status:
                trade_status = acm.FTradeStatusValue()
                trade_status.NiceName(str(status_name))
                trade_status.SystemName(str(status_name))
                if status_name == 'FO Amend':
                    trade_status.EnumValue(21)
                    trade_status.Ordnbr(12)
                trade_status.Commit()
                acm.UX.Dialogs().MessageBoxInformation(self.m_fuxDlg.Shell(),
                                                       'Successfully created {} trade status. Please restart PRIME so '
                                                       'this change can take effect.'
                                                       .format(status_name))
                logger.info("Trade Status {} created successfully.".format(status_name))
        else:
            acm.UX.Dialogs().MessageBoxInformation(self.m_fuxDlg.Shell(),
                                                   'Please enter a name for new trade status for successful creation.')

    def CreateLayout(self):
        builder = acm.FUxLayoutBuilder()
        builder.BeginVertBox()

        # Create additional info part
        builder.BeginVertBox('EtchedIn', 'Additional Info')
        builder.AddList('add_info_list', -1, -1, -1, -1)
        builder.BeginHorzBox()
        builder.AddFill()
        builder.AddButton('create_add_infos_button', 'Create Additional Info(s)', False, True)
        builder.EndBox()
        builder.EndBox()

        # Create sheet template part
        builder.BeginVertBox('EtchedIn', 'Sheet Templates')
        builder.BeginHorzBox()
        builder.BeginVertBox('EtchedIn')
        builder.AddCheckbox('trade_checkbox', 'Trade')
        builder.AddInput('trade_sheet_name', 'Template Name')
        builder.AddOption('trade_group', 'Group Label')
        builder.AddInput('trade_state_chart', 'State Chart')
        builder.EndBox()
        builder.BeginVertBox('EtchedIn')
        builder.AddCheckbox('instrument_checkbox', 'Instrument')
        builder.AddInput('price_sheet_name', 'Template Name')
        builder.AddOption('instrument_group', 'Group Label')
        builder.AddInput('instrument_state_chart', 'State Chart')
        builder.EndBox()
        builder.EndBox()
        builder.BeginHorzBox()
        builder.AddFill()
        builder.AddButton('create_sheet_templates_button', 'Create Sheet Template(s)', False, True)
        builder.EndBox()
        builder.EndBox()

        # Create new trade status
        builder.BeginVertBox('EtchedIn', 'Trade Status')
        builder.AddInput('trade_status_name', 'Trade Status Name')
        builder.BeginHorzBox()
        builder.AddFill()
        builder.AddButton('create_trade_status_button', 'Create Trade Status', False, True)
        builder.EndBox()
        builder.EndBox()
        
        # Create party contact add info
        builder.BeginHorzBox('EtchedIn', '')
        builder.AddCheckbox('create_contact_add_infos_checkbox', 'Create Party Additional Info Specification')
        builder.BeginHorzBox()
        builder.AddFill()
        builder.AddButton('create_contact_add_info', 'Create Party Additional Info Specification', False, True)
        builder.EndBox()
        builder.EndBox()
        
        
        # Create State Chart add info specification
        builder.BeginHorzBox('EtchedIn', '')
        builder.AddCheckbox('state_chart_add_infos_checkbox', 'Create State Chart AddInfo Specification')
        builder.BeginHorzBox()
        builder.AddFill()
        builder.AddButton('state_chart_add_info', 'Create State Chart AddInfo Specification', False, True)
        builder.EndBox()
        builder.EndBox()
        

        # Create all and Cancel buttons
        builder.BeginHorzBox()
        builder.AddFill()
        builder.AddButton('create_all', 'Create All')
        builder.AddButton('ok', 'Close')
        builder.EndBox()

        # FUxWorkboosheet part
        builder.AddCustom('trade_sheet', 'sheet.FTradeSheet', 20, 30)
        builder.AddCustom('price_sheet', 'sheet.FDealSheet', 20, 30)
        builder.EndBox()
        return builder
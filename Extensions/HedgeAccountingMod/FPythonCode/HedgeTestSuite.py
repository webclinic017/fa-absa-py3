'''
===================================================================================================
PURPOSE: This module contain the main Hedge Effectiveness Testing Application. It defines the Hedge
            Effectivess GUI and all related control functions and functionality. It is the main
            entry point into the application.
HISTORY:
---------------------------------------------------------------------------------------------------
XX-XX-2016      FIS Team                Initial implementation
29-08-2018      FIS Team                Dedesignation implementation
18-03-2021      Qaqamba Ntshobane       Added termination nominal, recalculated percentage of 
                                        dedesignated HR and added HR ref to new HR
===================================================================================================
'''
import re

import clr  # Need to import the clr module in order to use .Net
import acm
import FUxCore
import FUxNet
import FLogger

import HedgeTemplate
import HedgeRelation
import HedgeEffectivenessCharts
import HedgeConstants
import HedgeDealPackage
import HedgeUtils
import HedgeChildTradeUtils
from HedgeValidation import UserAccess
import importlib


importlib.reload(HedgeRelation)
importlib.reload(HedgeDealPackage)
importlib.reload(HedgeChildTradeUtils)

userAccess = UserAccess(acm.User())
clr.AddReference(HedgeConstants.STR_CLR_REFERENCE)
clr.AddReference(HedgeConstants.STR_CLR_REFERENCE)
logger = FLogger.FLogger(HedgeConstants.STR_HEDGE_TITLE)

# Formatters
doubleFormatter = acm.FDomain['double'].DefaultFormatter()
dateFormatter = acm.FDomain['date'].DefaultFormatter()


def CreateApplicationInstance():
    return HedgeTestSuiteApplication()


def ReallyStartApplication(shell, count):
    uxLayout = acm.UX().SessionManager().StartApplication(HedgeConstants.STR_HEDGE_TEST_SUITE, None)
    uxLayout.Maximize()


def StartApplication(eii):
    importlib.reload(HedgeConstants)
    shell = eii.ExtensionObject().Shell()
    ReallyStartApplication(shell, 0)


class AuditDlg(FUxCore.LayoutApplication):
    ''' The change history of the hedge relation is
            contained withing this window.
    '''
    def __init__(self, hedge_relation):
        self.m_hedgeRelation = hedge_relation

    def HandleCreate(self, dlg, layout):
        self.m_fuxDlg = dlg
        self.m_fuxDlg.Caption('Hedge Relation Change Log')
        self.m_doc_text = layout.GetControl('doc_text')
        self.m_doc_text.SetStandardFont(2)
        self.m_doc_text.Editable = False
        self.m_doc_text.SetData(self.m_hedgeRelation.get_audit_details())
        return True

    def HandleCancel(self):
        return True

    def CreateLayout(self):
        b = acm.FUxLayoutBuilder()
        b.BeginVertBox('None')
        b.  AddText('doc_text', 1200, 800, -1, -1)
        b.EndBox()
        return b


class TestHistoryDlg(FUxCore.LayoutApplication):
    ''' The testing history of the hedge relation is
            contained withing this window.
    '''
    def __init__(self, hedge_relation):
        self.m_hedgeRelation = hedge_relation  # MS

    def HandleCreate(self, dlg, layout):
        self.m_fuxDlg = dlg
        self.m_fuxDlg.Caption('Hedge Relation Testing Log')
        self.m_doc_text = layout.GetControl('doc_text')
        self.m_doc_text.SetStandardFont(2)
        self.m_doc_text.Editable = False
        self.m_doc_text.SetData(self.m_hedgeRelation.get_test_history())
        return True

    def HandleCancel(self):
        return True

    def CreateLayout(self):
        b = acm.FUxLayoutBuilder()
        b.BeginVertBox('None')
        b.  AddText('doc_text', 1200, 800, -1, -1)
        b.EndBox()
        return b


class InformationDlg(FUxCore.LayoutApplication):
    ''' General information about the hedge effectiveness testing is
            contained withing this window.
    '''
    def __init__(self, hedge_relation):
        self.m_hedgeRelation = hedge_relation

    def HandleCreate(self, dlg, layout):
        self.m_fuxDlg = dlg
        self.m_fuxDlg.Caption('External Relationship Information')
        self.m_doc_text = layout.GetControl('doc_text')
        self.m_doc_text.Editable = False
        self.m_doc_text.SetData(self.generate_documentation())

    def generate_documentation(self):
        trades = self.m_hedgeRelation.get_trades()
        hedgeRelationshipStatus = self.m_hedgeRelation.get_status()

        if hedgeRelationshipStatus is None or not trades:
            # return the default help text for new Hedge Relationships that have not
            # been saved yet.
            return HedgeConstants.STR_HELP_FILE

        testSettings = self.m_hedgeRelation.get_test_settings()

        hedgeType = self.m_hedgeRelation.get_type()
        hedgeSubType = self.m_hedgeRelation.get_sub_type()

        # Get the Hedge Risk Type
        hedgedRiskType = None
        if testSettings and \
           'Properties' in testSettings and \
           'HedgeRiskType' in testSettings['Properties']:

            hedgedRiskType = testSettings['Properties']['HedgeRiskType']

        # retrieve the selected test methodolies for Pro- and Retrospective testings
        if testSettings['ProDollarOffset']['Enabled'] == 'True':
            prospectiveTest = 'Dollar Offset'
        if testSettings['Regression']['Enabled'] == 'True':
            prospectiveTest = 'Regression test'
        if testSettings['ProVRM']['Enabled'] == 'True':
            prospectiveTest = 'Variable Reduction'
        if testSettings['RetroDollarOffset']['Enabled'] == 'True':
            retroSpectiveTest = 'Dollar Offset'
        if testSettings['RetroVRM']['Enabled'] == 'True':
            retroSpectiveTest = 'Variable Reduction'

        # assume if there is more than one hypo, they should all use the same
        # refs.
        firstHypoTrade = None
        for trdnbr in trades:
            m_type, _, _ = trades[trdnbr]
            trade = acm.FTrade[trdnbr]
            if m_type == 'Hypo':
                firstHypoTrade = acm.FTrade[trade.Oid()]

        if hedgeType == 'Cash Flow' and\
           hedgeSubType in ('AIB', 'FRR', 'FSTI', 'Structural') and\
           hedgedRiskType == 'Interest Rate':
            help_doc = HedgeConstants.STR_HELP_STRAT_1
            formatted_help_doc = help_doc % (prospectiveTest, retroSpectiveTest)

        elif hedgeType == 'Cash Flow' and\
                hedgeSubType == 'Standard Cash Flow' and\
                hedgedRiskType == 'Interest Rate':

            if firstHypoTrade and firstHypoTrade.Instrument().GetFloatReferences():
                rateName = firstHypoTrade.Instrument().GetFloatReferences()[0].Name()
            else:
                rateName = 'n/a'

            help_doc = HedgeConstants.STR_HELP_STRAT_2
            formatted_help_doc = help_doc % (rateName, prospectiveTest, retroSpectiveTest)

        elif hedgeType == 'Cash Flow' and\
                hedgeSubType == 'Opex' and\
                hedgedRiskType == 'Currency':

            if firstHypoTrade:
                currPair = firstHypoTrade.Instrument().Name()
            else:
                rateName = 'n/a'

            help_doc = HedgeConstants.STR_HELP_STRAT_3
            formatted_help_doc = help_doc % (currPair, prospectiveTest, retroSpectiveTest)

        elif hedgeType == 'Cash Flow' and\
                hedgeSubType == 'Foreign Debt (fix/float)' and\
                hedgedRiskType == 'Currency':

            if firstHypoTrade:
                currPair = firstHypoTrade.Instrument().Name()
            else:
                rateName = 'n/a'

            help_doc = HedgeConstants.STR_HELP_STRAT_4
            formatted_help_doc = help_doc % (currPair, prospectiveTest, retroSpectiveTest)

        elif (hedgeType == 'Fair Value AC' or hedgeType == 'Fair Value AFS') and\
                hedgeSubType == 'Foreign Debt (fix)' and\
                hedgedRiskType == 'Interest Rate':

            if firstHypoTrade and firstHypoTrade.Instrument().GetFloatReferences():
                rateName = firstHypoTrade.Instrument().GetFloatReferences()[0].Name()
            else:
                rateName = 'n/a'

            help_doc = HedgeConstants.STR_HELP_STRAT_5
            formatted_help_doc = help_doc % (rateName, prospectiveTest, retroSpectiveTest)

        elif (hedgeType == 'Fair Value AC' or hedgeType == 'Fair Value AFS') and\
                hedgeSubType in ('LiqAssetPort AFS', 'Other AFS') and\
                hedgedRiskType in ('Interest Rate', 'Inflation'):

            if firstHypoTrade and firstHypoTrade.Instrument().GetFloatReferences():
                rateName = firstHypoTrade.Instrument().GetFloatReferences()[0].Name()
            else:
                rateName = 'n/a'

            help_doc = HedgeConstants.STR_HELP_STRAT_6
            formatted_help_doc = help_doc % (rateName, prospectiveTest, retroSpectiveTest)

        elif (hedgeType == 'Fair Value AC' or hedgeType == 'Fair Value AFS') and\
                hedgeSubType in ('Fixed Rate Assets AC', 'Fixed Rate Liability AC') and\
                hedgedRiskType == 'Interest Rate':

            if firstHypoTrade and firstHypoTrade.Instrument().GetFloatReferences():
                rateName = firstHypoTrade.Instrument().GetFloatReferences()[0].Name()
            else:
                rateName = 'n/a'

            help_doc = HedgeConstants.STR_HELP_STRAT_7
            formatted_help_doc = help_doc % (rateName, prospectiveTest, retroSpectiveTest)

        elif hedgeType == 'Net Investment Hedge' and\
                hedgeSubType == 'Net Investment Hedge' and\
                hedgedRiskType == 'Currency':

            if firstHypoTrade:
                currPair = firstHypoTrade.Instrument().Name()
            else:
                rateName = 'n/a'

            help_doc = HedgeConstants.STR_HELP_STRAT_8
            formatted_help_doc = help_doc % (currPair, prospectiveTest, retroSpectiveTest)

        else:
            formatted_help_doc = HedgeConstants.STR_HELP_FILE

        return formatted_help_doc

    def HandleCancel(self):
        return True

    def CreateLayout(self):
        b = acm.FUxLayoutBuilder()
        b.BeginVertBox('None')
        b.  AddText('doc_text', 800, 600, -1, -1)
        b.EndBox()
        return b


class DeDesignateDlg(FUxCore.LayoutApplication):
    ''' GUI which contains the options and logic for de-designations.
    '''
    def __init__(self, hedge_relation):
        self.m_hedgeRelation = hedge_relation
        self.m_valid = False
        self.termination_reason = None
        self.termination_nominal = None
        self.termination_date = None

    def HandleCreate(self, dlg, layout):
        self.m_fuxDlg = dlg
        self.m_fuxDlg.Caption('De-designate Current External Relationship')

        self.m_termination_reason = layout.GetControl('termination')
        self.m_termination_nominal = layout.GetControl('terminationNominal')
        self.m_termination_date = layout.GetControl('terminationDate')
        self.m_buttonOK = layout.GetControl('ok')

        self.m_buttonOK.Enabled = False
        self.m_termination_nominal.Visible(False)

        self.m_termination_reason.Populate(HedgeConstants.DedesignationReason.get_all_as_list())

        self.m_termination_reason.AddCallback('Changed', self.on_termination_reason_changed, self)
        self.m_termination_nominal.AddCallback('Changed', self.on_termination_nominal_changed, self)
        self.m_termination_date.AddCallback('Changed', self.on_termination_date_changed, self)

    def HandleCancel(self):
        return True

    def HandleApply(self):
        self.m_hedgeRelation.set_termination(self.termination_reason)
        self.m_hedgeRelation.set_nominal(self.termination_nominal)
        self.m_hedgeRelation.set_termination_date(self.termination_date)
        #self.m_hedgeRelation.set_status(HedgeConstants.Hedge_Relation_Status.DeDesignated)
        self.m_hedgeRelation.save()
        return "Applied"

    def on_termination_reason_changed(self, self2, cd):
        self.termination_reason = self.m_termination_reason.GetData()
        self.show_nominal_field()
        self.on_field_changed()

    def on_termination_nominal_changed(self, self2, cd):
        self.termination_nominal = self.m_termination_nominal.GetData()
        self.on_field_changed()

    def date_adjust_period(self, date, period):
        try:
            date = acm.Time().DateAdjustPeriod(HedgeConstants.DAT_TODAY, period)
            return date
        except:
            pass
        return period

    def on_termination_date_changed(self, self2, cd):
        self.m_termination_date.SetData(self.date_adjust_period(HedgeConstants.DAT_TODAY,
                                                                self.m_termination_date.GetData()))
        self.termination_date = self.m_termination_date.GetData()
        if len(self.termination_date) == 10:
            try:
                acm.Time.IsValidDateTime(self.termination_date)
                self.on_field_changed()
            except Exception:
                self.m_buttonOK.Enabled = False
        else:
            self.m_buttonOK.Enabled = False

    def show_nominal_field(self):
        if self.termination_reason == HedgeConstants.DedesignationReason.PartialDedesignation:
            self.m_termination_nominal.Visible(True)
        else:
            self.m_termination_nominal.Visible(False)

    def on_field_changed(self):
        if ((self.m_termination_reason.Enabled() and not self.termination_reason) or
                (self.m_termination_nominal.Visible() and self.m_termination_nominal.Enabled() and not self.termination_nominal) or
                (self.m_termination_date.Enabled() and not self.termination_date)):
            self.m_buttonOK.Enabled = False
        else:
            self.m_buttonOK.Enabled = True

    def CreateLayout(self):
        b = acm.FUxLayoutBuilder()
        b.BeginVertBox('None')
        b.  AddOption('termination', 'Termination Reason', 50, -1)
        b.  AddInput('terminationNominal', 'Termination Nominal', 20, -1)
        b.  AddInput('terminationDate', 'Termination Date (yyyy-mm-dd)', 20, -1)
        b.  BeginHorzBox('None')
        b.    AddSpace(50)
        b.    AddFill()
        b.    AddButton('ok', 'De-Designate')
        b.    AddButton('cancel', 'Cancel')
        b.  EndBox()
        b.EndBox()
        return b


class EditDlg(FUxCore.LayoutApplication):
    ''' GUI which allows for the selection and editing of trades within the
            Hedge Relationship.
    '''
    def __init__(self, hedge_relationship, data=None):
        if data is None:
            data = [None, None, None]
        self.hedge_relationship = hedge_relationship
        if data[0]:  # Edit
            self.m_trade = acm.FTrade[data[0]]
            self.m_type = data[1]
            self.m_percent = data[2]
        else:  # New
            self.m_trade = None
            self.m_type = 'External'
            self.m_percent = 100

    def HandleCreate(self, dlg, layout):
        self.m_fuxDlg = dlg
        if self.m_trade:
            self.m_fuxDlg.Caption('Edit Trade')
        else:
            self.m_fuxDlg.Caption('Add Trade')

        self.m_inputTrade = layout.GetControl('trade')
        self.m_buttonSelect = layout.GetControl('select')
        self.m_inputInstrument = layout.GetControl('instrument')
        self.m_inputType = layout.GetControl('type')
        self.m_inputPercent = layout.GetControl('percent')
        self.m_buttonOK = layout.GetControl('ok')

        self.m_inputType.Populate(HedgeConstants.Hedge_Trade_Types.get_all_as_list())

        self.m_buttonSelect.AddCallback('Activate', self.OnButtonSelectClick, self)
        self.m_inputTrade.AddCallback('Activate', self.OnInputTrade, 'Activate')

        self.UpdateGUI()

    def HandleApply(self):
        oid = self.m_inputTrade.GetData()
        # Remove spaces and commas from input trade number
        oid = str(''.join(ch for ch in oid if ch.isdigit()))
        self.m_trade = acm.FTrade[oid]
        if not self.m_trade:
            error_msg = 'Could not find the selected trade number (%s).' % oid
            acm.UX().Dialogs().MessageBoxOKCancel(self.m_fuxDlg.Shell(), 'Error', error_msg)
            return None
        exclusive_existing_allocation, HRs_with_trades = HedgeUtils.\
            get_exclusive_alocated_percent(self.m_trade.Oid(), self.hedge_relationship)
        input_percent = float(self.m_inputPercent.GetData())
        new_allocation = exclusive_existing_allocation + float(input_percent)
        if input_percent > 100:
            over_allocation_msg = 'Allocations of more than 100% are illegal.'
            acm.UX().Dialogs().MessageBoxOKCancel(self.m_fuxDlg.Shell(),
                                                  'Error',
                                                  over_allocation_msg)
            return None
        elif (new_allocation > 100) and \
            (not self.hedge_relationship.get_HR_reference()) and\
                ((self.m_type == HedgeConstants.Hedge_Trade_Types.Original) or
                 (self.m_type == HedgeConstants.Hedge_Trade_Types.External)):
            over_allocation_msg = '%s%% of trade %s has been allocated in other HRs (%s). '\
                                  'The new allocation would be %s%%, but the maximum is 100%%.'\
                                  % (exclusive_existing_allocation,
                                     self.m_trade.Oid(),
                                     HRs_with_trades,
                                     new_allocation)
            acm.UX().Dialogs().MessageBoxOKCancel(self.m_fuxDlg.Shell(),
                                                  'Error',
                                                  over_allocation_msg)
            return None
        elif (new_allocation > 200):
            over_allocation_msg = '%s%% of trade %s has been allocated in other HRs (%s). ' \
                    'The new allocation would be %s%%, but the maximum is 200%%, as this HR is '\
                    'non-ZAR and has a currency component.'\
                    % (exclusive_existing_allocation,
                       self.m_trade.Oid(),
                       HRs_with_trades,
                       new_allocation)
            acm.UX().Dialogs().MessageBoxOKCancel(self.m_fuxDlg.Shell(),
                                                  'Error',
                                                  over_allocation_msg)
            return None
        in_a_deal_package = acm.FDealPackageTradeLink.Select("trade = %s" % self.m_trade.Oid())
        if in_a_deal_package:
            msg = 'The parent trade (%s) is already in a deal package. Therefore, its children '\
                  'cannot be in deal packages either.' % self.m_trade.Oid()
            acm.UX().Dialogs().MessageBoxInformation(self.m_fuxDlg.Shell(), msg)
            return None

        return [str(self.m_trade.Oid()), self.m_inputType.GetData(), input_percent]

    def HandleCancel(self):
        return True

    def OnButtonSelectClick(self, self2, cd):
        trade = acm.UX().Dialogs().SelectObjectsInsertItems(self.m_fuxDlg.Shell(),
                                                            'FTrade',
                                                            False)
        if trade:
            self.m_trade = trade
        self.UpdateGUI()

    def OnInputTrade(self, self2, cd):
        oid = self.m_inputTrade.GetData()
        self.m_trade = acm.FTrade[oid]
        self.UpdateGUI()

    def UpdateGUI(self):
        if self.m_trade:
            self.m_inputTrade.SetData(self.m_trade.Oid())
            self.m_inputInstrument.SetData(self.m_trade.Instrument().Name())
            self.m_buttonOK.Enabled(True)
        else:
            self.m_inputTrade.SetData('')
            self.m_inputInstrument.SetData('')
        self.m_inputType.SetData(self.m_type)
        self.m_inputPercent.SetData(self.m_percent)

    def CreateLayout(self):
        b = acm.FUxLayoutBuilder()
        b.BeginVertBox('None', '')
        b.  BeginHorzBox('None', '')
        b.    AddInput('trade', 'Trade')
        b.    AddButton('select', '>', 4, 4)
        b.    AddInput('instrument', 'Instrument', 40)
        b.    AddPopuplist('type', 'Type')
        b.    AddInput('percent', 'Percentage')
        b.  EndBox()
        b.  BeginHorzBox('None', '')
        b.    AddFill()
        b.    AddButton('cancel', 'Cancel')
        b.    AddButton('ok', 'OK')
        b.  EndBox()
        b.EndBox()
        return b


class HedgeTestSuiteCommandItem(FUxCore.MenuItem):
    ''' Class to control the ribbon
    '''
    def __init__(self, parent, command=None):
        self.m_command = command
        self.m_parent = parent

    def Invoke(self, cd):
        if cd.Definition().GetName().Text() == 'runTests':
            self.m_parent.on_run_test_button_press(None)
        if cd.Definition().GetName().Text() == 'viewTestHistory':
            self.m_parent.on_run_test_history_press(None)
        if cd.Definition().GetName().Text() == 'addTrade':
            self.m_parent.on_doc_add_button_press(None)
        if cd.Definition().GetName().Text() == 'editTrade':
            self.m_parent.on_doc_edit_button_press(None)
        if cd.Definition().GetName().Text() == 'removeTrade':
            self.m_parent.on_doc_delete_button_press(None)
        if cd.Definition().GetName().Text() == 'openTrade':
            self.m_parent.on_doc_open_button_press(None)
        if cd.Definition().GetName().Text() == 'openChild':
            self.m_parent.on_child_trade_open_button_press(None)
        if cd.Definition().GetName().Text() == 'deDesignate':
            self.m_parent.on_doc_deDesignate_button_press(None)
        if cd.Definition().GetName().Text() == 'timeBucketEditor':
            self.m_parent.on_button_timebucket_editor_activate(None)
        if cd.Definition().GetName().Text() == 'information':
            self.m_parent.on_button_information_activate(None)
        if cd.Definition().GetName().Text() == 'audit':
            self.m_parent.on_button_audit_activate(None)

    def Applicable(self):
        return True

    def Enabled(self):
        if self.m_command in ['addTrade', 'editTrade', 'removeTrade']:
            return bool(HedgeConstants.BLN_MODIFY_TRADES)
        if self.m_command == 'deDesignate':
            return bool(HedgeConstants.BLN_CAN_DEDESIGNATE)
        return True

    def Checked(self):

        return False


class HedgeTestSuiteApplication(FUxCore.LayoutApplication, FUxCore.LayoutTabbedDialog):
    ''' Class to create and conrtol the Hedge Relationship GUI
    '''
    def __init__(self):
        FUxCore.LayoutApplication.__init__(self)
        self.m_template = HedgeTemplate.HedgeTemplate()
        self.m_hedgeRelation = HedgeRelation.HedgeRelation(None)
        self.m_hedgeRelation.new()
        self.m_statusList = HedgeConstants.Hedge_Relation_Status.get_all_as_list()
        self.invalid_tests_selected = False
        self.handle_object_on_create = None
        self.modified = False

        self.m_PDO_textDescription = None
        self.m_PDO_list = None
        self.m_PDO_original = None
        self.m_PDO_external = None
        self.m_PDO_do_percent = None
        self.m_PDO_graphpanel = None
        self.m_PDO_checkDollarOffset = None
        self.m_PDO_checkWarningBoundaries = None
        self.m_PDO_checkLimitBoundaries = None


    def HandleRegisterCommands(self, builder):
        ''' Each command contains:
        The name of the item
        A parent(such as View,Tools etc).
        File is not allowed and is handled by registering as described below.
        The path of the item ending with the item label.
        A tooltip text, use empty string for no tooltip.
        The accelerator for the item, use empty string for no accelerator.
        The mnemonic for the command, use empty string for no mnemonic.
        A callback method that creates a FUxCore.MenuItem that is used for invoking the command &
              for controlling it's appearance.
        A boolean that specifies if the command should be the default command
              (only applicable for context menus).
        All parameters must be supplied when calling ConvertCommands
              itemName, parent, path, tooltiptext, accelerator, mnemonic, callback, default
        '''
        commands = [
            ['addTrade',
             'View',
             'Add Trade',
             'Add Trade',
             '',
             '',
             self.CreateCommandCBAddTrade,
             False],
            ['editTrade',
             'View',
             'Edit Trade',
             'Edit Selected Trade',
             '',
             '',
             self.CreateCommandCBEditTrade,
             False],
            ['removeTrade',
             'View',
             'Remove Trade',
             'Remove Selected Trade',
             '',
             '',
             self.CreateCommandCBRemoveTrade,
             False],
            ['openTrade',
             'View',
             'Open Parent',
             'Open Selected Parent Trade with Instrument Definition',
             '',
             '',
             self.CreateCommandCB,
             False],
            ['openChild',
             'View',
             'Open Child',
             'Open Selected Child Trade with Instrument Definition',
             '',
             '',
             self.CreateCommandCB,
             False],
            ['runTests',
             'View',
             'Run Tests',
             'Run Tests',
             '',
             '',
             self.CreateCommandCB,
             False],
            ['viewTestHistory',
             'View',
             'Test History',
             'View Test History',
             '',
             '',
             self.CreateCommandCB,
             False],
            ['timeBucketEditor',
             'View',
             'Show Test Calendar',
             'Show Test Calendar',
             '',
             '',
             self.CreateCommandCB,
             False],
            ['deDesignate',
             'View',
             'De-designate HR',
             'De-designate Current External Relationship',
             '',
             '',
             self.CreateCommandCBDeDesignateTrade,
             False],
            ['information',
             'View',
             'Information',
             '',
             '',
             '',
             self.CreateCommandCB,
             False],
            ['audit',
             'View',
             'Audit',
             '',
             '',
             '',
             self.CreateCommandCB,
             False]
        ]

        # To be able to use the standard File commands(Open,Save,Save As etc) create an FSeT
        #       and add the enumerator values corresponding to the commands desired. Look at
        #       the FUxStandardFileCommands enum for a list of available commands.

        fileCommands = acm.FSet()
        fileCommands.Add('FileNew')
        fileCommands.Add('FileOpen')
        fileCommands.Add('FileSave')
        fileCommands.Add('FileRevert')
        builder.RegisterCommands(FUxCore.ConvertCommands(commands), fileCommands)

    def CreateCommandCB(self):
        return HedgeTestSuiteCommandItem(self)

    def CreateCommandCBAddTrade(self):
        return HedgeTestSuiteCommandItem(self, 'addTrade')

    def CreateCommandCBEditTrade(self):
        return HedgeTestSuiteCommandItem(self, 'editTrade')

    def CreateCommandCBRemoveTrade(self):
        return HedgeTestSuiteCommandItem(self, 'removeTrade')

    def CreateCommandCBDeDesignateTrade(self):
        return HedgeTestSuiteCommandItem(self, 'deDesignate')

    def HandleStandardFileCommandInvoke(self, commandName):
        if commandName == 'FileNew':
            self.on_file_new()
        if commandName == 'FileOpen':
            self.on_file_open()
        if commandName == 'FileSave':
            self.on_file_save()
        if commandName == 'FileRevert':
            self.on_file_revert()

    def HandleStandardFileCommandEnabled(self, commandName):
        ''' Rules to enable/disable the Save Button
        '''
        if commandName == 'FileSave':
            if self.modified:
                return True

            return self.check_if_modified()

        # rules to enable/disable the Revert Button
        elif commandName == 'FileRevert':
            if self.m_Doc_inputIdentifier.GetData() == "" or\
               self.m_hedgeRelation.get_id() == "":
                return False

        return True

    def HandleSetContents(self, contents):
        if contents is not None:
            if contents.IsKindOf('FCustomTextObject'):
                self.handle_object_on_create = contents

    def HandleObject(self, obj):
        self.m_Doc_inputIdentifier.SetData(obj)
        self.on_input_identifier_activate(None)

    def GetApplicationIcon(self):
        return 'Hedge'

    def DoChangeCreateParameters(self, createParams):
        ''' Essentially use default settings
        '''
        createParams.UseSplitter(True)
        createParams.SplitHorizontal(True)
        createParams.LimitMinSize(True)
        createParams.AutoShrink(True)
        createParams.AdjustPanesWhenResizing(True)

    def HandleClose(self):
        ask = False
        if self.modified:
            ask = True
        else:
            ask = self.check_if_modified()
        if ask:
            question = 'Save hedge relation?'
            reallyClose = acm.UX().Dialogs().MessageBoxYesNoCancel(self.Shell(),
                                                                   "Question",
                                                                   question)
            if reallyClose == 'Button3':
                return False
            elif reallyClose == 'Button2':
                return True
            else:
                logger.LOG('Saved before exiting')
                self.save()
        return True

    def HandleCreate(self, creationInfo):
        ''' Add Tabs
        '''
        self.m_tabControlPane = creationInfo.AddTabControlPane('tabs')
        self.m_layoutDocumentation = self.m_tabControlPane.AddLayoutPage(
            self.create_layout_documentation(),
            'Documentation'
        )
        self.m_layoutProDO = self.m_tabControlPane.AddLayoutPage(
            self.create_layout_dollar_offset(),
            'Pro Dollar Offset'
        )
        self.m_layoutRetroDO = self.m_tabControlPane.AddLayoutPage(
            self.create_layout_dollar_offset(),
            'Retro Dollar Offset'
        )
        self.m_layoutRegression = self.m_tabControlPane.AddLayoutPage(
            self.create_layout_regression(),
            'Regression'
        )
        self.m_layoutProVRM = self.m_tabControlPane.AddLayoutPage(
            self.create_layout_vrm(),
            'Pro Variable Reduction'
        )
        self.m_layoutRetroVRM = self.m_tabControlPane.AddLayoutPage(
            self.create_layout_vrm(),
            'Retro Variable Reduction'
        )
        self.m_layoutCriticalTerms = self.m_tabControlPane.AddLayoutPage(
            self.create_layout_critical_terms(),
            'Critical Terms'
        )

        # Initialise tabs
        self.initialise_documentation()
        self.initialise_pro_dollar_offset()
        self.initialise_retro_dollar_offset()
        self.initialise_regression()
        self.initialise_retro_vrm()
        self.initialise_pro_vrm()
        self.initialise_critical_terms()

        if self.handle_object_on_create:
            obj = self.handle_object_on_create
            self.handle_object_on_create = None
            self.HandleObject(obj)

    def on_file_new(self):
        self.m_hedgeRelation.new()
        HedgeTemplate.set_test_settings_default(self)
        self.populate_default_values()
        self.update_documentation_trades()
        self.reset_test_summary()
        self.initialise_dealpackage_grid(None)
        self.update_based_on_hr_status(None, self.m_hedgeRelation.get_status())
        self.modified = False

    def on_file_open(self):
        ''' Commented code is for a simplified selection dialog, which only allows for the
               selection of Text Objects which are Hedge Relationships. The existing
               selection dialog allows for ANY text object to be selected, even those
               which cannot be opened/processed by this code.
        selectedObject = acm.UX().Dialogs().SelectObject(self.Shell(),
                                                            'Select External Relation',
                                                            'External Relation',
                                                            HedgeRelation.get_hedge_relations(),
                                                            None)
        '''
        selectedObject = acm.UX().Dialogs().SelectObjectsInsertItems(
            self.Shell(),
            'FCustomTextObject',
            False
        )
        if selectedObject:
            try:
                baseName = selectedObject.Name()
            except:
                error_msg = 'Invalid HR selected.'
                acm.UX().Dialogs().MessageBoxOKCancel(self.Shell(), 'Error', error_msg)
                return
        else:
            return
        dealPackageBaseNamePattern = HedgeConstants.STR_DEALPACKAGE_BASENAME_PATTERN
        baseNameValidationResult = re.match(dealPackageBaseNamePattern, baseName)
        if not baseNameValidationResult:
            error_msg = "Please select a valid hedge relationship. Valid hedge relationships "\
                        "start with 'HR/'"
            acm.UX().Dialogs().MessageBoxOKCancel(self.Shell(), 'Error', error_msg)
            logger.ELOG('Invalid Hedge Relationship selected')
            return

        if selectedObject is not None:
            self.HandleObject(selectedObject)
            self.update_based_on_hr_status(None, self.m_hedgeRelation.get_status())
            self.on_input_identifier_activate(None)
            self.modified = False

    def on_file_save(self):
        if self.save():
            self.modified = False

    def on_file_save_as(self):
        name = acm.UX().Dialogs().SaveObjectAs(self.Shell(),
                                               'Save External Template',
                                               'External Templates',
                                               HedgeRelation.get_hedge_relations(),
                                               None,
                                               self.on_validate_CB,
                                               None)
        if not name:
            logger.WLOG('No valid name given for template')
            return
        self.m_Doc_inputIdentifier.SetData(name)
        if self.save():
            self.modified = False

    def on_file_revert(self):
        if self.m_hedgeRelation.get_id():
            self.HandleObject(self.m_hedgeRelation.get_id())
            self.modified = False

    def on_validate_CB(self, shell, m_object, arg3, arg4):
        ''' Function to validate name when using "Save As"
        '''
        if m_object in HedgeRelation.get_hedge_relations():
            acm.UX().Dialogs().MessageBoxInformation(
                shell,
                'An external template with this name already exists.')
            return False
        return True

    def on_save_validate_allocation(self, tradeDict):
        ''' Check for the over-allocation of trades. Preliminary validation is done when trades are
               added or edited, but conflicts can arise if more than one instance of the the test
               suite are open simultaneously.
        '''
        for tradeOid in tradeDict:
            exclusive_existing_allocation, HRs_with_trades = HedgeUtils.\
                get_exclusive_alocated_percent(int(tradeOid), self.m_hedgeRelation)
            input_percent = float(tradeDict[tradeOid][1])
            new_allocation = exclusive_existing_allocation + float(input_percent)
            
            hedge_trade_type = tradeDict[tradeOid][0]
                        
            if input_percent > 100:
                over_allocation_msg = 'Allocations of more than 100% are illegal.'
                acm.UX().Dialogs().MessageBoxOKCancel(self.Shell(), 'Error', over_allocation_msg)
                return False
            elif (new_allocation > 100) and not self.m_hedgeRelation.get_HR_reference() and \
                 ((hedge_trade_type == HedgeConstants.Hedge_Trade_Types.Original) or
                  (hedge_trade_type == HedgeConstants.Hedge_Trade_Types.External)):
                over_allocation_msg = '%s%% of trade %s has been allocated in other HRs (%s). ' \
                                      'The new allocation would be %s%%, but the maximum is 100%%.'\
                                      ' Save aborted.'\
                                      % (exclusive_existing_allocation,
                                         tradeOid,
                                         HRs_with_trades,
                                         new_allocation)
                acm.UX().Dialogs().MessageBoxOKCancel(self.Shell(), 'Error', over_allocation_msg)
                return True
            elif new_allocation > 200:
                over_allocation_msg = '%s%% of trade %s has been allocated in other HRs. The new '\
                                      'allocation would be %s%%, but the maximum is 200%%, as this'\
                                      'HR is non-ZAR & has a currency component. Save aborted.'\
                                      % (exclusive_existing_allocation,
                                         tradeOid,
                                         new_allocation)
                acm.UX().Dialogs().MessageBoxOKCancel(self.Shell(), 'Error', over_allocation_msg)
                return True

    def on_save_validate_overall_pass(self, status):
        ''' Run tests and do not permit an HR to be saved in 'Active' status unless the tests yield
                an overall pass.
        '''
        overall_pass_achieved = self.m_hedgeRelation.overall_pass_achieved()
        if status == HedgeConstants.Hedge_Relation_Status.Active:
            warning_msg = "Saving as 'Active': Have the tests been run for the existing " \
                "configuration?"
            tests_run = acm.UX().Dialogs().MessageBoxYesNo(self.Shell(), 'Warning', warning_msg)
            if tests_run:
                if not overall_pass_achieved:
                    error_msg = "Hedge relationships cannot be saved in status 'Active' unless " \
                                "the most recent tests have yielded an overall pass. Please " \
                                "view the test history for more details."
                    acm.UX().Dialogs().MessageBoxOKCancel(self.Shell(), 'Error', error_msg)
                    return True
            else:
                return True

    def on_save_validate_backdating(self, status, tradeDict):
        ''' Check for back-dated Hedge Relationships and prompt for a reason
        '''
        backdate_reason = self.m_hedgeRelation.get_backdate_reason()
        try:
            date_delta = acm.Time.DateDifference(self.m_Doc_startdate.GetData(),
                                                 HedgeConstants.DAT_TODAY)
        except:
            error_msg = "The start date is invalid. Save aborted."
            acm.UX().Dialogs().MessageBoxOKCancel(self.Shell(), 'Error', error_msg)
            return True

        for tradeOid in tradeDict:
            trade = acm.FTrade[tradeOid]
            ins = trade.Instrument()
            if acm.Time.DateDifference(ins.StartDate(), self.m_Doc_startdate.GetData()[0:10]) > 0:
                warning_msg = "The instrument %s has a start date (%s) that is after the " \
                              "proposed start date of the hedge relationship. Abort save?" \
                              % (ins.Name(), ins.StartDate())
                abort_save = acm.UX().Dialogs().MessageBoxYesNo(self.Shell(),
                                                                'Warning',
                                                                warning_msg)
                if abort_save == "Button1":
                    return True
        if date_delta < -HedgeConstants.INT_BACKDATE_DAYS:
            error_msg = "Hedge relationships cannot be backdated by more than %s days." \
                        % HedgeConstants.INT_BACKDATE_DAYS
            acm.UX().Dialogs().MessageBoxOKCancel(self.Shell(), 'Error', error_msg)
            return True
        if (date_delta < 0) \
            and (not backdate_reason)\
                and (status == HedgeConstants.Hedge_Relation_Status.Simulated):
            while len(backdate_reason) < HedgeConstants.INT_LEN_BACKDATE_REASON:
                backdate_reason = acm.UX().Dialogs().GetTextInput(
                    self.Shell(),
                    "Please Enter the Reason for Backdating",
                    "")
                if backdate_reason is None:
                    logger.LOG('Saving of backdated hedge relationship aborted.')
                    return True
                elif len(backdate_reason) < HedgeConstants.INT_LEN_BACKDATE_REASON:
                    acm.UX().Dialogs().MessageBoxInformation(
                        self.Shell(),
                        'Please Enter a Reason of at least %s Characters'
                        % HedgeConstants.INT_LEN_BACKDATE_REASON
                    )
            self.m_hedgeRelation.set_backdate_reason(backdate_reason)

    def on_save_validate_trade_statuses(self, tradeDict):
        ''' Hypos and Zero Bonds may not be in status 'Void' or 'Simualted', as FValidation checks
                may otherwise be circumvented.
        '''
        if self.m_Doc_optionStatus.GetData() != 'Simulated':

            for tradeOid in tradeDict:
                trade_type = tradeDict[tradeOid][0]
                if trade_type in [HedgeConstants.Hedge_Trade_Types.Hypo,
                                  HedgeConstants.Hedge_Trade_Types.ZeroBond]:
                    if acm.FTrade[tradeOid].Status() in ['Void', 'Simulated']:
                        error_msg = "Hypos and Zero Bonds may not be in status 'Void' or "\
                                    "'Simualted'. Save aborted."
                        acm.UX().Dialogs().MessageBoxOKCancel(self.Shell(), 'Error', error_msg)
                        return True

    def on_save_validate_dates(self):
        ''' Start and End Dates are compulsory
        '''
        start_date = self.m_Doc_startdate.GetData()
        end_date = self.m_Doc_enddate.GetData()
        try:
            if acm.Time.IsValidDateTime(end_date) and acm.Time.IsValidDateTime(start_date):
                return False
        except Exception, e:
            logger.LOG(e)
            acm.UX().Dialogs().MessageBoxOKCancel(self.Shell(), 'Error', e)
            return True
        error_msg = "Valid start and end dates are required. Save aborted."
        acm.UX().Dialogs().MessageBoxOKCancel(self.Shell(), 'Error', error_msg)
        return True

    def on_save_validate_test_selection(self):
        if self.invalid_tests_selected:
            error_msg = "Precisely one prospective and precisely one retrospective test " \
                        "must be selected. Save aborted."
            acm.UX().Dialogs().MessageBoxOKCancel(self.Shell(), 'Error', error_msg)
            return True

    def save(self):
        if self.m_Doc_optionStatus.GetData() == '':
            logger.LOG('No Status Selected')
            return False
        tradeDict = self.m_hedgeRelation.get_trades()
        hr_status = self.m_Doc_optionStatus.GetData()  # self.m_hedgeRelation.get_status()
        if self.on_save_validate_test_selection():
            return False

        if self.on_save_validate_allocation(tradeDict):
            return False

        if hr_status != self.m_hedgeRelation.get_status():
            if self.on_save_validate_overall_pass(hr_status):
                return False

        if self.on_save_validate_backdating(hr_status, tradeDict):
            return False

        if self.on_save_validate_trade_statuses(tradeDict):
            return False

        if self.on_save_validate_dates():
            return False
        # Update the audit log
        self.m_hedgeRelation.set_audit_details()

        self.m_hedgeRelation.set_HR_reference(self.m_Doc_referenceHR.GetData())
        self.m_hedgeRelation.set_status(self.m_Doc_optionStatus.GetData())
        self.m_hedgeRelation.set_start_date(self.m_Doc_startdate.GetData())
        self.m_hedgeRelation.set_end_date(self.m_Doc_enddate.GetData())
        self.m_hedgeRelation.set_termination(self.m_Doc_termination.GetData())
        self.m_hedgeRelation.set_nominal(self.m_Doc_nominal.GetData())
        self.m_hedgeRelation.set_termination_date(self.m_Doc_terminationDate.GetData())

        # Save Test Settings: Template or standalone
        if self.m_Doc_checkboxUseTemplate.Checked():
            template_name = self.m_Doc_popuplistTemplates.GetData()
            if not template_name:
                logger.LOG('No test settings template has been selected.')
                return False
            self.m_hedgeRelation.set_template_name(template_name)
            self.m_hedgeRelation.set_test_settings({})
        else:
            self.m_hedgeRelation.set_template_name('')
            testsettings = HedgeTemplate.get_test_settings(self)
            self.m_hedgeRelation.set_test_settings(testsettings)

        # Create DealPackage and set dealPackage in XML.
        hedgeRelationshipName = self.m_hedgeRelation.get_id()
        tradeList = self.m_hedgeRelation.get_trades()
        status = self.m_hedgeRelation.get_status()
        designationDate = self.m_hedgeRelation.get_start_date()

        # initialise return variables
        names = [None, None]
        updatedTradeList = None

        try:
            if hedgeRelationshipName:
                _, dealPackageName = self.m_hedgeRelation.get_deal_package()
                names, updatedTradeList = HedgeDealPackage.set_dealpackage(
                    self.Shell(),
                    hedgeRelationshipName,
                    tradeList,
                    designationDate,
                    status,
                    dealPackageName
                )
            else:
                # first save to build the HR name to be used when creating the Deal Package as well.
                self.m_hedgeRelation.save()

                # re-retrieve Id after it was set on TextObject creation
                hedgeRelationshipName = self.m_hedgeRelation.get_id()

                # Create DealPackage
                names, updatedTradeList = HedgeDealPackage.set_dealpackage(
                    self.Shell(),
                    hedgeRelationshipName,
                    tradeList,
                    designationDate,
                    status,
                    None
                )

        except Exception, ex:
            message = 'Error creation new Deal Package. Message: %s' % (ex)
            logger.ELOG(message)
            acm.UX().Dialogs().MessageBoxOKCancel(self.Shell(), 'Error', message)
            return False

        if updatedTradeList:
            self.m_hedgeRelation.set_trades(updatedTradeList)

        if names and len(names) > 1 and\
           names[0] and names[1]:
            self.m_hedgeRelation.set_dealpackage(names[0], names[1])

        # save completed HedgeRelation
        self.m_hedgeRelation.save()

        self.populate_documentation_from_saved()

        if names and len(names) > 1:
            self.initialise_dealpackage_grid(names[1])
        return True

    def on_pro_do_button_press(self, self2, cd):
        ''' Which series to show? (include warning and limit?)
        '''
        self.m_PDO_chart.EnableSeries(
            self.m_PDO_checkDollarOffset.Checked(),
            self.m_PDO_checkWarningBoundaries.Checked(),
            self.m_PDO_checkLimitBoundaries.Checked())

    def on_retro_do_button_press(self, self2, cd):
        ''' Which series to show? (include warning and limit?)
        '''
        self.m_RDO_chart.EnableSeries(
            self.m_RDO_checkDollarOffset.Checked(),
            self.m_RDO_checkWarningBoundaries.Checked(),
            self.m_RDO_checkLimitBoundaries.Checked())

    def on_reg_checkbox_press(self, self2, cd):
        ''' Which series to show?
        '''
        self.m_Reg_chart.EnableSeries(
            self.m_Reg_show0.Checked(),
            self.m_Reg_show1.Checked(),
            self.m_Reg_show2.Checked(),
            self.m_Reg_show3.Checked())

    def on_pro_vrm_button_press(self, self2, cd):
        ''' Which series to show?
        '''
        self.m_PVRM_chart.EnableSeries(
            self.m_PVRM_checkVariableReduction.Checked(),
            self.m_PVRM_checkWarningBoundaries.Checked(),
            self.m_PVRM_checkLimitBoundaries.Checked())

    def on_retro_vrm_button_press(self, self2, cd):
        ''' Which series to show?
        '''
        self.m_RVRM_chart.EnableSeries(
            self.m_RVRM_checkVariableReduction.Checked(),
            self.m_RVRM_checkWarningBoundaries.Checked(),
            self.m_RVRM_checkLimitBoundaries.Checked())

    def reset_test_summary(self):
        ''' Reset Test Summary in Documentation Pane
        '''
        self.m_Doc_inputResultProDollarOffset.SetData('Test Not Run.')
        self.m_Doc_inputResultRetroDollarOffset.SetData('Test Not Run.')
        self.m_Doc_inputResultRegression.SetData('Test Not Run.')
        self.m_Doc_inputResultProVRM.SetData('Test Not Run.')
        self.m_Doc_inputResultRetroVRM.SetData('Test Not Run.')
        self.m_Doc_inputResultCriticalTerms.SetData('Test Not Run.')
        self.m_Doc_inputResultOverall.SetData('Tests Not Run.')

        self.update_test_summary_color()
        self.update_gui_pro_dollar_offset({})
        self.update_gui_retro_dollar_offset({})
        self.update_gui_regression({})
        self.update_gui_pro_vrm({})
        self.update_gui_retro_vrm({})
        self.update_gui_critical_terms({})

    def update_test_summary_color(self):

        def lookup(text, active):
            if not active:
                return HedgeConstants.CLR_LIGHT_GRAY
            else:
                if text == 'Pass':
                    return HedgeConstants.CLR_LIGHT_GREEN
                if text == 'Warning':
                    return HedgeConstants.CLR_LIGHT_ORANGE
                if text == 'Fail':
                    return HedgeConstants.CLR_LIGHT_RED
                return HedgeConstants.CLR_LIGHT_GRAY

        testsettings = self.m_hedgeRelation.get_test_settings()

        PDO_enabled = bool(testsettings) and (testsettings['ProDollarOffset']['Enabled'] == 'True')
        RDO_enabled = bool(testsettings) and (testsettings['RetroDollarOffset']['Enabled']
                                              == 'True')
        REG_enabled = bool(testsettings) and (testsettings['Regression']['Enabled'] == 'True')
        PVRM_enabled = bool(testsettings) and (testsettings['ProVRM']['Enabled'] == 'True')
        RVRM_enabled = bool(testsettings) and (testsettings['RetroVRM']['Enabled'] == 'True')
        CT_enabled = bool(testsettings) and (testsettings['CriticalTerms']['Enabled'] == 'True')
        cond = [PDO_enabled, RDO_enabled, REG_enabled, PVRM_enabled, RVRM_enabled, CT_enabled]
        overall_enabled = any(cond)

        self.m_Doc_inputResultProDollarOffset.SetColor(0, lookup(
            self.m_Doc_inputResultProDollarOffset.GetData(), PDO_enabled))
        self.m_Doc_inputResultRetroDollarOffset.SetColor(0, lookup(
            self.m_Doc_inputResultRetroDollarOffset.GetData(), RDO_enabled))
        self.m_Doc_inputResultRegression.SetColor(0, lookup(
            self.m_Doc_inputResultRegression.GetData(), REG_enabled))
        self.m_Doc_inputResultProVRM.SetColor(0, lookup(
            self.m_Doc_inputResultProVRM.GetData(), PVRM_enabled))
        self.m_Doc_inputResultRetroVRM.SetColor(0, lookup(
            self.m_Doc_inputResultRetroVRM.GetData(), RVRM_enabled))
        self.m_Doc_inputResultCriticalTerms.SetColor(0, lookup(
            self.m_Doc_inputResultCriticalTerms.GetData(), CT_enabled))
        self.m_Doc_inputResultOverall.SetColor(0, lookup(
            self.m_Doc_inputResultOverall.GetData(), overall_enabled))

    def format_tradeNbr_output(self, trades):
        strTradeNbrs = ''
        for trade in trades:
            strTradeNbrs = strTradeNbrs + trade + ', '
        if strTradeNbrs:
            strTradeNbrs = strTradeNbrs[:-2]
        return strTradeNbrs

    def update_gui_pro_dollar_offset(self, results):

        self.m_PDO_chart.ClearChart()
        if results == {}:
            self.m_PDO_original.Clear()
            self.m_PDO_external.Clear()
            self.m_PDO_do_percent.Clear()
            self.m_PDO_list.RemoveAllItems()
            return

        # Update List
        self.m_PDO_list.RemoveAllItems()
        rootItem = self.m_PDO_list.GetRootItem()

        data = results['data']
        dates = data.keys()
        dates.sort()

        # Set Static fields
        self.m_PDO_original.SetData(self.format_tradeNbr_output(results['original']))
        self.m_PDO_external.SetData(self.format_tradeNbr_output(results['external']))
        self.m_PDO_do_percent.SetData(round(results['do'][dates[-1]], 2))

        testsettings = self.m_hedgeRelation.get_test_settings()
        loLimit = float(testsettings['ProDollarOffset']['LoLimit'])
        hiLimit = float(testsettings['ProDollarOffset']['HiLimit'])
        loWarning = float(testsettings['ProDollarOffset']['LoWarning'])
        hiWarning = float(testsettings['ProDollarOffset']['HiWarning'])
        warnings = [loWarning, hiWarning]
        limits = [loLimit, hiLimit]

        for date in dates:
            x = doubleFormatter.Format(data[date]['Original'])
            y = doubleFormatter.Format(data[date]['External'])
            d_x = doubleFormatter.Format(data[date]['DOriginal'])
            d_y = doubleFormatter.Format(data[date]['DExternal'])

            if 'do' in results:
                d_o = doubleFormatter.Format(results['do'][date])
            else:
                d_o = float('NaN')

            # List
            child = rootItem.AddChild()
            child.Label(dateFormatter.Format(date), 0)
            child.Label(x, 1)
            child.Label(y, 2)
            child.Label(d_x, 3)
            child.Label(d_y, 4)
            child.Label(d_o, 5)

        self.m_PDO_chart.UpdateChart(results, warnings, limits)
        self.m_PDO_chart.EnableSeries(True, True, True)

        # Update the conclusion value / colour
        self.m_Doc_inputResultProDollarOffset.SetData(results['result'])
        if results['result'] == 'Pass':
            self.m_Doc_inputResultProDollarOffset.SetColor('Background',
                                                           HedgeConstants.CLR_LIGHT_GREEN)
        else:
            self.m_Doc_inputResultProDollarOffset.SetColor('Background',
                                                           HedgeConstants.CLR_LIGHT_RED)

        # Adjust List columns
        self.m_PDO_list.AdjustColumnWidthToFitItems(0)
        self.m_PDO_list.AdjustColumnWidthToFitItems(1)
        self.m_PDO_list.AdjustColumnWidthToFitItems(2)
        self.m_PDO_list.AdjustColumnWidthToFitItems(3)
        self.m_PDO_list.AdjustColumnWidthToFitItems(4)
        self.m_PDO_list.AdjustColumnWidthToFitItems(5)

    def update_gui_retro_dollar_offset(self, results):
        self.m_RDO_chart.ClearChart()
        if results == {}:
            self.m_RDO_original.Clear()
            self.m_RDO_external.Clear()
            self.m_RDO_do_percent.Clear()
            self.m_RDO_list.RemoveAllItems()
            return

        # Update List
        self.m_RDO_list.RemoveAllItems()
        rootItem = self.m_RDO_list.GetRootItem()

        data = results['data']
        dates = data.keys()
        dates.sort()

        # Set Static fields
        self.m_RDO_original.SetData(self.format_tradeNbr_output(results['original']))
        self.m_RDO_external.SetData(self.format_tradeNbr_output(results['external']))

        if 'do' in results:
            self.m_RDO_do_percent.SetData(doubleFormatter.Format(results['do'][dates[-1]]))
        else:
            self.m_RDO_do_percent.SetData(float('NaN'))

        testsettings = self.m_hedgeRelation.get_test_settings()
        loLimit = float(testsettings['RetroDollarOffset']['LoLimit'])
        hiLimit = float(testsettings['RetroDollarOffset']['HiLimit'])
        loWarning = float(testsettings['RetroDollarOffset']['LoWarning'])
        hiWarning = float(testsettings['RetroDollarOffset']['HiWarning'])
        warnings = [loWarning, hiWarning]
        limits = [loLimit, hiLimit]

        for date in dates:
            x = doubleFormatter.Format(data[date]['Original'])
            y = doubleFormatter.Format(data[date]['External'])
            d_x = doubleFormatter.Format(data[date]['DOriginal'])
            d_y = doubleFormatter.Format(data[date]['DExternal'])

            if 'do' in results:
                d_o = doubleFormatter.Format(results['do'][date])
            else:
                d_o = float('NaN')

            # List
            child = rootItem.AddChild()
            child.Label(dateFormatter.Format(date), 0)
            child.Label(x, 1)
            child.Label(y, 2)
            child.Label(d_x, 3)
            child.Label(d_y, 4)
            child.Label(d_o, 5)

        self.m_RDO_chart.UpdateChart(results, warnings, limits)
        self.m_RDO_chart.EnableSeries(True, True, True)

        # Update the conclusion value / colour
        self.m_Doc_inputResultRetroDollarOffset.SetData(results['result'])
        if results['result'] == 'Pass':
            self.m_Doc_inputResultRetroDollarOffset.SetColor('Background',
                                                             HedgeConstants.CLR_LIGHT_GREEN)
        else:
            self.m_Doc_inputResultRetroDollarOffset.SetColor('Background',
                                                             HedgeConstants.CLR_LIGHT_RED)

        # Adjust List columns
        self.m_RDO_list.AdjustColumnWidthToFitItems(0)
        self.m_RDO_list.AdjustColumnWidthToFitItems(1)
        self.m_RDO_list.AdjustColumnWidthToFitItems(2)
        self.m_RDO_list.AdjustColumnWidthToFitItems(3)
        self.m_RDO_list.AdjustColumnWidthToFitItems(4)
        self.m_RDO_list.AdjustColumnWidthToFitItems(5)

    def update_gui_regression(self, results):

        testsettings = self.m_hedgeRelation.get_test_settings()
        self.m_Reg_chart.ClearChart()
        if results == {}:
            self.m_Reg_InputOriginal.Clear()
            self.m_Reg_InputHedge.Clear()
            self.m_Reg_InputStdErr.Clear()
            self.m_Reg_InputAlpha.Clear()
            self.m_Reg_InputBeta.Clear()
            self.m_Reg_InputCorrelation.Clear()
            self.m_Reg_InputR2.Clear()
            self.m_Reg_InputPSignificance.Clear()
            self.m_Reg_InputPValue.Clear()
            self.m_Reg_list.RemoveAllItems()
            return

        # Set test results variables
        stdErr = float(results['Std_Err'])
        alpha = float(results['alpha'])
        beta = float(results['beta'])
        correlation = float(results['correlation'])
        R2 = float(results['R2'])
        if 'PValue' in results:
            PValue = float(results['PValue'])
        PStatistic = testsettings['Regression']['PValueLimit']
        data = results['data']

        # Set Static fields
        self.m_Reg_InputOriginal.SetData(self.format_tradeNbr_output(results['original']))
        self.m_Reg_InputHedge.SetData(self.format_tradeNbr_output(results['external']))
        self.m_Reg_InputStdErr.SetData(round(stdErr, 2))
        self.m_Reg_InputAlpha.SetData(round(alpha, 2))
        self.m_Reg_InputBeta.SetData(round(beta, 2))
        self.m_Reg_InputCorrelation.SetData(round(correlation, 2))
        self.m_Reg_InputR2.SetData(round(R2, 2))
        self.m_Reg_InputPValue.SetData(round(PValue, 2))
        self.m_Reg_InputPSignificance.SetData(PStatistic)

        # Clear previous series: List & Graph
        self.m_Reg_list.RemoveAllItems()

        # Populate List & Graph: Original, External
        graphdict = {}
        rootItem = self.m_Reg_list.GetRootItem()
        dates = data.keys()
        dates.sort()
        for date in dates:
            x = doubleFormatter.Format(data[date]['Original'])
            y = doubleFormatter.Format(data[date]['External'])
            d_x = doubleFormatter.Format(data[date]['DOriginal'])
            d_y = doubleFormatter.Format(data[date]['DExternal'])

            # List
            child = rootItem.AddChild()
            child.Label(dateFormatter.Format(date), 0)
            child.Label(x, 1)
            child.Label(y, 2)
            child.Label(d_x, 3)
            child.Label(d_y, 4)

        self.m_Reg_chart.UpdateChart(results)
        self.m_Reg_chart.EnableSeries(False, False, True, True)

        # Adjust List columns
        self.m_Reg_list.AdjustColumnWidthToFitItems(0)
        self.m_Reg_list.AdjustColumnWidthToFitItems(1)
        self.m_Reg_list.AdjustColumnWidthToFitItems(2)
        self.m_Reg_list.AdjustColumnWidthToFitItems(3)
        self.m_Reg_list.AdjustColumnWidthToFitItems(4)

    def update_gui_pro_vrm(self, results):
        self.m_PVRM_chart.ClearChart()
        if results == {}:
            self.m_PVRM_original.Clear()
            self.m_PVRM_external.Clear()
            self.m_PVRM_vr_percent.Clear()
            self.m_PVRM_list.RemoveAllItems()
            return

        # Update List
        self.m_PVRM_list.RemoveAllItems()
        rootItem = self.m_PVRM_list.GetRootItem()

        data = results['data']
        dates = data.keys()
        dates.sort()

        # Set Static fields
        self.m_PVRM_original.SetData(self.format_tradeNbr_output(results['original']))
        self.m_PVRM_external.SetData(self.format_tradeNbr_output(results['external']))

        if 'vr' in results:
            self.m_PVRM_vr_percent.SetData(round(results['vr'][dates[-1]], 2))
        else:
            self.m_PVRM_vr_percent.SetData(float('NaN'))

        testsettings = self.m_hedgeRelation.get_test_settings()
        limit = float(testsettings['ProVRM']['Limit'])
        warning = float(testsettings['ProVRM']['Warning'])

        for date in dates:
            x = doubleFormatter.Format(data[date]['Original'])
            y = doubleFormatter.Format(data[date]['External'])
            d_x = doubleFormatter.Format(data[date]['DOriginal'])
            d_y = doubleFormatter.Format(data[date]['DExternal'])

            if 'vr' in results:
                v_r = doubleFormatter.Format(results['vr'][date])
            else:
                v_r = float('NaN')

            # List
            child = rootItem.AddChild()
            child.Label(dateFormatter.Format(date), 0)
            child.Label(x, 1)
            child.Label(y, 2)
            child.Label(d_x, 3)
            child.Label(d_y, 4)
            child.Label(v_r, 5)

        self.m_PVRM_chart.UpdateChart(results, warning, limit)
        self.m_PVRM_chart.EnableSeries(True, True, True)

        # Update the conclusion value / colour
        self.m_Doc_inputResultProVRM.SetData(results['result'])
        if results['result'] == 'Pass':
            self.m_Doc_inputResultProVRM.SetColor('Background', HedgeConstants.CLR_LIGHT_GREEN)
        else:
            self.m_Doc_inputResultProVRM.SetColor('Background', HedgeConstants.CLR_LIGHT_RED)

        # Adjust List columns
        self.m_PVRM_list.AdjustColumnWidthToFitItems(0)
        self.m_PVRM_list.AdjustColumnWidthToFitItems(1)
        self.m_PVRM_list.AdjustColumnWidthToFitItems(2)
        self.m_PVRM_list.AdjustColumnWidthToFitItems(3)
        self.m_PVRM_list.AdjustColumnWidthToFitItems(4)
        self.m_PVRM_list.AdjustColumnWidthToFitItems(5)

    def update_gui_retro_vrm(self, results):
        self.m_RVRM_chart.ClearChart()
        if results == {}:
            self.m_RVRM_original.Clear()
            self.m_RVRM_external.Clear()
            self.m_RVRM_vr_percent.Clear()
            self.m_RVRM_list.RemoveAllItems()
            return

        # Update List
        self.m_RVRM_list.RemoveAllItems()
        rootItem = self.m_RVRM_list.GetRootItem()

        data = results['data']
        dates = data.keys()
        dates.sort()

        # Set Static fields
        self.m_RVRM_original.SetData(self.format_tradeNbr_output(results['original']))
        self.m_RVRM_external.SetData(self.format_tradeNbr_output(results['external']))

        if 'vr' in results:
            self.m_RVRM_vr_percent.SetData(round(results['vr'][dates[-1]], 2))
        else:
            self.m_RVRM_vr_percent.SetData(float('NaN'))

        testsettings = self.m_hedgeRelation.get_test_settings()
        limit = float(testsettings['RetroVRM']['Limit'])
        warning = float(testsettings['RetroVRM']['Warning'])

        for date in dates:
            x = doubleFormatter.Format(data[date]['Original'])
            y = doubleFormatter.Format(data[date]['External'])
            d_x = doubleFormatter.Format(data[date]['DOriginal'])
            d_y = doubleFormatter.Format(data[date]['DExternal'])

            if 'vr' in results:
                v_r = doubleFormatter.Format(results['vr'][date])
            else:
                v_r = float('NaN')

            # List
            child = rootItem.AddChild()
            child.Label(dateFormatter.Format(date), 0)
            child.Label(x, 1)
            child.Label(y, 2)
            child.Label(d_x, 3)
            child.Label(d_y, 4)
            child.Label(v_r, 5)

        self.m_RVRM_chart.UpdateChart(results, warning, limit)
        self.m_RVRM_chart.EnableSeries(True, True, True)

        # Update the conclusion value / colour
        self.m_Doc_inputResultRetroVRM.SetData(results['result'])
        if results['result'] == 'Pass':
            self.m_Doc_inputResultRetroVRM.SetColor('Background', HedgeConstants.CLR_LIGHT_GREEN)
        else:
            self.m_Doc_inputResultRetroVRM.SetColor('Background', HedgeConstants.CLR_LIGHT_RED)

        # Adjust List columns
        self.m_RVRM_list.AdjustColumnWidthToFitItems(0)
        self.m_RVRM_list.AdjustColumnWidthToFitItems(1)
        self.m_RVRM_list.AdjustColumnWidthToFitItems(2)
        self.m_RVRM_list.AdjustColumnWidthToFitItems(3)
        self.m_RVRM_list.AdjustColumnWidthToFitItems(4)
        self.m_RVRM_list.AdjustColumnWidthToFitItems(5)

    def update_gui_critical_terms(self, results):
        if results == {}:
            self.m_CT_results.RemoveAllItems()
            while self.m_CT_results.ColumnCount() > 1:
                self.m_CT_results.RemoveColumn(1)
            self.m_CT_result.Clear()
            self.m_CT_result.SetColor('Background', HedgeConstants.CLR_WHITE)
            return

        # Clean previous data
        self.m_CT_results.RemoveAllItems()
        while self.m_CT_results.ColumnCount() > 1:
            self.m_CT_results.RemoveColumn(1)

        # Re-add Columns
        columns = {}
        count = 1

        trade_list = self.m_hedgeRelation.get_trades()
        for trdnbr in trade_list:
            m_type, _, childTradeId = trade_list[trdnbr]

            if m_type == HedgeConstants.Hedge_Trade_Types.External:
                self.m_CT_results.AddColumn(childTradeId, -1, childTradeId)
                columns[childTradeId] = count
                count += 1
            elif m_type == HedgeConstants.Hedge_Trade_Types.Hypo:
                self.m_CT_results.AddColumn(trdnbr, -1, trdnbr)
                columns[trdnbr] = count
                count += 1

        columns['Compare'] = count
        columns['Result'] = count+1

        self.m_CT_results.AddColumn('Comparison', -1, 'Comparison')
        self.m_CT_results.AddColumn('Result', -1, 'Result')

        info = results['info']
        rootItem = self.m_CT_results.GetRootItem()
        for key in info.keys():
            child = rootItem.AddChild()
            child.Label(key, 0)
            values = info[key]
            column = 1

            for value in values.keys():
                if str(value) in columns:
                    column = columns[str(value)]
                    child.Label(values[value], column)

                    if not values['Result']:
                        child.Icon('Warning')

        # Align the columns nicely
        for x in range(self.m_CT_results.ColumnCount()):
            self.m_CT_results.AdjustColumnWidthToFitItems(x)

        # Update the conclusion value / colour
        self.m_CT_result.SetData(results['result'])
        if results['result'] == 'Pass':
            self.m_CT_result.SetColor('Background', HedgeConstants.CLR_LIGHT_GREEN)
        else:
            self.m_CT_result.SetColor('Background', HedgeConstants.CLR_LIGHT_RED)

    def update_based_on_hr_status(self, cd, status=None):
        if not status:
            status = self.m_Doc_optionStatus.GetData()
        if status == HedgeConstants.Hedge_Relation_Status.Simulated:
            self.m_statusList = HedgeConstants.Hedge_Relation_Status.get_status_per_simulated()
            self.m_Doc_startdate.Enabled(True)
            self.m_Doc_enddate.Enabled(True)
            self.m_Doc_checkboxUseTemplate.Enabled(True)
            HedgeConstants.BLN_CAN_DEDESIGNATE = False
            HedgeConstants.BLN_MODIFY_TRADES = True
            HedgeConstants.BLN_MODIFY_DATES = True
            HedgeConstants.BLN_MODIFY_SETTINGS = True
        elif status == HedgeConstants.Hedge_Relation_Status.Proposed:
            self.m_statusList = HedgeConstants.Hedge_Relation_Status.get_status_per_proposed()
            self.m_Doc_startdate.Enabled(True)
            self.m_Doc_enddate.Enabled(True)
            self.m_Doc_checkboxUseTemplate.Enabled(True)
            HedgeConstants.BLN_CAN_DEDESIGNATE = False
            HedgeConstants.BLN_MODIFY_TRADES = True
            HedgeConstants.BLN_MODIFY_DATES = True
            HedgeConstants.BLN_MODIFY_SETTINGS = True
        elif status == HedgeConstants.Hedge_Relation_Status.Active:
            self.m_statusList = HedgeConstants.Hedge_Relation_Status.get_status_per_active()
            self.m_Doc_startdate.Enabled(False)
            self.m_Doc_enddate.Enabled(False)
            self.m_Doc_checkboxUseTemplate.Enabled(False)
            HedgeConstants.BLN_MODIFY_TRADES = False
            HedgeConstants.BLN_MODIFY_DATES = False
            HedgeConstants.BLN_MODIFY_SETTINGS = False
            HedgeConstants.BLN_CAN_DEDESIGNATE = True
        elif status == HedgeConstants.Hedge_Relation_Status.DeDesignated:
            self.m_statusList = HedgeConstants.Hedge_Relation_Status.get_status_per_deDesignated()
            self.m_Doc_startdate.Enabled(False)
            self.m_Doc_enddate.Enabled(False)
            self.m_Doc_checkboxUseTemplate.Enabled(False)
            HedgeConstants.BLN_MODIFY_TRADES = False
            HedgeConstants.BLN_MODIFY_DATES = False
            HedgeConstants.BLN_MODIFY_SETTINGS = False
            HedgeConstants.BLN_CAN_DEDESIGNATE = False
        elif status == HedgeConstants.Hedge_Relation_Status.Discard:
            self.m_statusList = HedgeConstants.Hedge_Relation_Status.get_status_per_discard()
            HedgeConstants.BLN_CAN_DEDESIGNATE = False
        HedgeTemplate.set_fields_enabled(self, HedgeConstants.BLN_MODIFY_SETTINGS)

        # Update the drop down list control
        self.m_Doc_optionStatus.Clear()
        for item in self.m_statusList:
            self.m_Doc_optionStatus.AddItem(item)

        self.m_Doc_optionStatus.SetData(status)

    def propose_expiry_date(self, trades):
        ''' Determine earliest instrument expiry date, to be proposed as the HR end date
        '''
        valid_date_found = False
        earliest_ins_expiry = acm.Time.DateAddDelta(HedgeConstants.DAT_TODAY, 100, 0, 0)
        for trade in trades:
            try:
                ins_end_date = acm.FTrade[trade].Instrument().EndDate()
                valid_date_found = True
                if acm.Time.DateDifference(ins_end_date, earliest_ins_expiry) < 0:
                    earliest_ins_expiry = ins_end_date
            except Exception, e:
                logger.WLOG('Warning: ', e)
        if not valid_date_found:
            earliest_ins_expiry = HedgeConstants.DAT_TODAY
        self.m_Doc_enddate.SetData(earliest_ins_expiry)

    def on_doc_add_button_press(self, cd):
        ''' Add trade to External Relation
        '''
        self.m_hedgeRelation.set_HR_reference(self.m_Doc_referenceHR.GetData())
        editDlg = EditDlg(self.m_hedgeRelation)
        builder = editDlg.CreateLayout()
        shell = self.Frame().Shell()
        result = acm.UX().Dialogs().ShowCustomDialogModal(shell, builder, editDlg)
        if result:
            # Update Dictionary with trades
            trades = self.m_hedgeRelation.get_trades()
            trades[result[0]] = [result[1], result[2], '']
            self.m_hedgeRelation.set_trades(trades)
            self.propose_expiry_date(trades)
            self.modified = True
        self.update_documentation_trades()

    def on_doc_edit_button_press(self, cd):
        ''' Edit trade in External Relation
        '''
        item = self.m_Doc_listtrades.GetSelectedItem()
        if item:
            data = item.GetData()
            editDlg = EditDlg(self.m_hedgeRelation, data)
            builder = editDlg.CreateLayout()
            shell = self.Frame().Shell()
            result = acm.UX().Dialogs().ShowCustomDialogModal(shell, builder, editDlg)
            if result:
                # Update Dictionary with trades
                trades = self.m_hedgeRelation.get_trades()
                del trades[data[0]]
                trades[result[0]] = [result[1], result[2], '']
                self.m_hedgeRelation.set_trades(trades)
                self.propose_expiry_date(trades)
                self.modified = True
            self.update_documentation_trades()

    def on_doc_delete_button_press(self, cd):
        ''' Delete trade from External Relation
        '''
        item = self.m_Doc_listtrades.GetSelectedItem()
        if item:
            oid = item.GetData()[0]
            trades = self.m_hedgeRelation.get_trades()
            del trades[oid]
            self.m_hedgeRelation.set_trades(trades)
            self.modified = True
            self.update_documentation_trades()

    def on_doc_open_button_press(self, cd):
        ''' Open selected parent trade (Instrument Definition)
        '''
        item = self.m_Doc_listtrades.GetSelectedItem()
        if item:
            oid = item.GetData()[0]
            parent_trade = acm.FTrade[oid]
            acm.StartApplication('Instrument Definition', parent_trade)

    def on_child_trade_open_button_press(self, cd):
        ''' Open selected child trade (Instrument Definition)
        '''
        item = self.m_Doc_listtrades.GetSelectedItem()
        if item:
            oid = item.GetData()[0]
            trade_list = self.m_hedgeRelation.get_trades()
            for trdnbr in trade_list:
                _, _, childTradeId = trade_list[trdnbr]
                if childTradeId and (trdnbr == oid):
                    childTrade = acm.FTrade[childTradeId]
                    acm.StartApplication('Instrument Definition', childTrade)

    def on_run_test_button_press(self, cd):
        if not self.save():
            logger.LOG('Tests not run due to failed save.')
            return
        else:
            self.modified = False

        testsettings = self.m_hedgeRelation.get_test_settings()

        # load the Test Engine only at this point since the HedgeTestEngine
        # will load NumPy and SciPy which is slow to load for user that do
        # not have the libs locally configured.
        from HedgeTestEngine import run_tests

        results = run_tests(self.m_hedgeRelation)

        if not results:
            return

        if 'Pro Dollar Offset' in results:
            result = results['Pro Dollar Offset']['result']
            self.m_Doc_inputResultProDollarOffset.SetData(result)
            self.update_gui_pro_dollar_offset(results['Pro Dollar Offset'])
        else:
            self.m_Doc_inputResultProDollarOffset.SetData('Test Not Run.')
            self.update_gui_pro_dollar_offset({})

        if 'Retro Dollar Offset' in results:
            result = results['Retro Dollar Offset']['result']
            self.m_Doc_inputResultRetroDollarOffset.SetData(result)
            self.update_gui_retro_dollar_offset(results['Retro Dollar Offset'])
        else:
            self.m_Doc_inputResultRetroDollarOffset.SetData('Test Not Run.')
            self.update_gui_retro_dollar_offset({})

        if 'Regression' in results:
            result = results['Regression']['result']
            self.m_Doc_inputResultRegression.SetData(result)
            self.update_gui_regression(results['Regression'])
        else:
            self.m_Doc_inputResultRegression.SetData('Test Not Run.')
            self.update_gui_regression({})

        if 'Pro Variable Reduction' in results:
            result = results['Pro Variable Reduction']['result']
            self.m_Doc_inputResultProVRM.SetData(result)
            self.update_gui_pro_vrm(results['Pro Variable Reduction'])
        else:
            self.m_Doc_inputResultProVRM.SetData('Test Not Run.')
            self.update_gui_pro_vrm({})

        if 'Retro Variable Reduction' in results:
            result = results['Retro Variable Reduction']['result']
            self.m_Doc_inputResultRetroVRM.SetData(result)
            self.update_gui_retro_vrm(results['Retro Variable Reduction'])
        else:
            self.m_Doc_inputResultRetroVRM.SetData('Test Not Run.')
            self.update_gui_retro_vrm({})

        if 'Critical Terms' in results:
            result = results['Critical Terms']['result']
            self.m_Doc_inputResultCriticalTerms.SetData(result)
            self.update_gui_critical_terms(results['Critical Terms'])
        else:
            self.m_Doc_inputResultCriticalTerms.SetData('Test Not Run.')
            self.update_gui_critical_terms({})

        if 'Overall Result' in results:
            self.m_Doc_inputResultOverall.SetData(results['Overall Result'])
        else:
            self.m_Doc_inputResultOverall.SetData(results['Overall Result'])

        self.update_test_summary_color()

    def on_run_test_history_press(self, cd):
        testHistoryDlg = TestHistoryDlg(self.m_hedgeRelation)
        builder = testHistoryDlg.CreateLayout()
        shell = self.Frame().Shell()
        acm.UX().Dialogs().ShowCustomDialogModal(
            shell,
            builder,
            testHistoryDlg
        )

    def on_button_timebucket_editor_activate(self, cd):
        shell = acm.UX().SessionManager().Shell()
        time_bucket = acm.FStoredTimeBuckets[HedgeConstants.STR_DEFAULT_TIME_BUCKETS]
        acm.UX().Dialogs().SelectTimeBuckets(shell, time_bucket)

    def on_doc_deDesignate_button_press(self, cd):
        deDesignateDlg = DeDesignateDlg(self.m_hedgeRelation)
        builder = deDesignateDlg.CreateLayout()
        shell = self.Frame().Shell()
        result = bool(acm.UX().Dialogs().ShowCustomDialogModal(shell, builder, deDesignateDlg))

        if result:
            # clone the Hedge Relation in order to re-designate new Hedge Relation
            clonedNewHedgeRelation = self.create_dedesignation_clone()

            if clonedNewHedgeRelation == 'bad dedes amount':
                message = 'Dedesignation nominal is greater than original trade nominal'
                acm.UX().Dialogs().MessageBoxOKCancel(shell,
                                                      'Error',
                                                      message)
                logger.ELOG(message)
                return

            # Add amortisation payments to the dedesignated trades
            HedgeChildTradeUtils.dedesignation(self.m_hedgeRelation)
        
            self.m_hedgeRelation.set_status(HedgeConstants.Hedge_Relation_Status.DeDesignated)
            self.m_hedgeRelation.save()

            status = self.m_hedgeRelation.get_status()

            if status == HedgeConstants.Hedge_Relation_Status.DeDesignated:
                terminationReason = self.m_hedgeRelation.get_termination()

                if terminationReason == HedgeConstants.DedesignationReason.PartialDedesignation:

                    if clonedNewHedgeRelation:
                        dedesignatedHedgeName = self.m_hedgeRelation.get_id()

                        self.m_hedgeRelation = clonedNewHedgeRelation

                        self.modified = False
                        message = '{0} was de-designated and cloned ready to be updated and ' \
                                  'saved as a new Hedge Relationship. Please update the Hedge '\
                                  'details and click "Save" to create and save a new Hedge '\
                                  'Relationship in the Simulated state.'\
                                  .format(dedesignatedHedgeName)
                        acm.UX().Dialogs().MessageBoxInformation(shell, message)

            self.populate_documentation_from_saved()
            self.reset_test_summary()
            self.update_based_on_hr_status(None, self.m_hedgeRelation.get_status())

    def calculate_percentage(self, dedes_nominal, percentage, nominal):
    
        new_percentage = float(percentage) * (1 - float(dedes_nominal) / nominal)
        new_percentage = round(new_percentage, 2)

        return new_percentage

    def create_dedesignation_clone(self):
        '''Creates a Clone of the current hedgeRelation with:
            - the current Hr termination date as start date,
            - a clean transaction log,
            - current Original, External, Internal & Zero-bond trades
                (excluding Hypo trades),
            - status set to 'Simulated'
            - Id set to None (not yet saved) and
            - no dealPackage.
        '''

        clonedNewHedgeRelation = HedgeRelation.HedgeRelation(None)
        clonedNewHedgeRelation.new()

        # clone required properties to new HedgeRelation
        inceptionDate = self.m_hedgeRelation.get_inception_date()
        if inceptionDate:
            clonedNewHedgeRelation.set_inception_date(inceptionDate)

        templateName = self.m_hedgeRelation.get_template_name()
        if templateName:
            clonedNewHedgeRelation.set_template_name(templateName)

        testSettings = self.m_hedgeRelation.get_test_settings()
        if testSettings:
            clonedNewHedgeRelation.set_test_settings(testSettings)

        endDate = self.m_hedgeRelation.get_end_date()
        if endDate:
            clonedNewHedgeRelation.set_end_date(endDate)

        startDate = self.m_hedgeRelation.get_termination_date()
        if startDate:
            clonedNewHedgeRelation.set_start_date(startDate)

        hrReference = self.m_hedgeRelation.get_id()
        if hrReference:
            clonedNewHedgeRelation.set_HR_reference(hrReference)

        clonedNewHedgeRelation.set_status(HedgeConstants.Hedge_Relation_Status.Simulated)

        # Get & Set trades
        tradeList = self.m_hedgeRelation.get_trades()

        nominal = 1

        clonedTradeList = {}
        external_trade_holder = []

        for tradeOid in tradeList:
            [m_type, percentage, childtradeOid] = tradeList[tradeOid]

            # only copy trades for selected trade types
            if m_type == HedgeConstants.Hedge_Trade_Types.Original or\
               m_type == HedgeConstants.Hedge_Trade_Types.External or\
               m_type == HedgeConstants.Hedge_Trade_Types.Internal or\
               m_type == HedgeConstants.Hedge_Trade_Types.ZeroBond:

                terminationReason = self.m_hedgeRelation.get_termination()

                if terminationReason == HedgeConstants.DedesignationReason.PartialDedesignation:
                    dedesignation_nominal = self.m_hedgeRelation.get_nominal()

                    if dedesignation_nominal and childtradeOid:
                        childTrade = acm.FTrade[childtradeOid]
        
                        if m_type == HedgeConstants.Hedge_Trade_Types.Internal:
                            nominal = childTrade.Nominal()

                        new_percentage = self.calculate_percentage(dedesignation_nominal, percentage, nominal)

                        if nominal == 1:
                            external_trade_holder = [tradeOid, m_type, percentage]
                            continue

                        if nominal != 1 and external_trade_holder:
                            new_ext_percentage = self.calculate_percentage(dedesignation_nominal, external_trade_holder[2], nominal)
                            external_trade_holder = [external_trade_holder[0], external_trade_holder[1], new_ext_percentage]

                            if new_ext_percentage < 0 or new_ext_percentage > 100:
                                return 'bad dedes amount'

                        if new_percentage < 0 or new_percentage > 100:
                            return 'bad dedes amount'
                        percentage = new_percentage

                if acm.FTrade[tradeOid].Type() != 'Closing':
                    if external_trade_holder:
                        clonedTradeList[external_trade_holder[0]] = [external_trade_holder[1], external_trade_holder[2], '']
                    clonedTradeList[tradeOid] = [m_type, percentage, '']

        if clonedTradeList:
            clonedNewHedgeRelation.set_trades(clonedTradeList)

        return clonedNewHedgeRelation

    def on_button_audit_activate(self, cd):
        auditDlg = AuditDlg(self.m_hedgeRelation)
        builder = auditDlg.CreateLayout()
        shell = self.Frame().Shell()
        result = acm.UX().Dialogs().ShowCustomDialogModal(shell, builder, auditDlg)

    def on_button_information_activate(self, cd):
        informationDlg = InformationDlg(self.m_hedgeRelation)
        builder = informationDlg.CreateLayout()
        shell = self.Frame().Shell()
        result = acm.UX().Dialogs().ShowCustomDialogModal(shell, builder, informationDlg)

    def on_popup_list_templates_activate(self, cd, m_object):
        ''' Set available hedge templates
        '''
        for template in HedgeTemplate.get_templates():  # Do not use Populate()
            self.m_Doc_popuplistTemplates.AddItem(template)

        name = self.m_Doc_popuplistTemplates.GetData()
        if name:
            self.m_template.set_id(name)
            self.m_template.read()
            HedgeTemplate.set_test_settings(self, self.m_template.get_test_settings())

    def update_documentation_trades(self):
        self.m_Doc_listtrades.RemoveAllItems()
        rootItem = self.m_Doc_listtrades.GetRootItem()
        trades = self.m_hedgeRelation.get_trades()

        for trdnbr in trades.keys():
            child = rootItem.AddChild()
            [m_type, percent, childTradeId] = trades[trdnbr]
            t = acm.FTrade[trdnbr]
            if t:
                child.SetData([str(t.Oid()), m_type, percent])
                child.Label(t.Oid(), 0)
                child.Label(t.Instrument().Name(), 1)
                child.Label(m_type, 2)
                child.Label(percent, 3)
                child.Label(childTradeId, 4)

        # Adjust trade list columns nicely
        self.m_Doc_listtrades.AdjustColumnWidthToFitItems(0)
        self.m_Doc_listtrades.AdjustColumnWidthToFitItems(1)
        self.m_Doc_listtrades.AdjustColumnWidthToFitItems(2)
        self.m_Doc_listtrades.AdjustColumnWidthToFitItems(3)

        # Initialise the DealPackage view with the saved DealPackage
        dealPackageNames = self.m_hedgeRelation.get_deal_package()

        if dealPackageNames and len(dealPackageNames) > 1:
            self.initialise_dealpackage_grid(dealPackageNames[1])

    def on_checkbox_use_template_activate(self, cd, um):
        if self.m_Doc_checkboxUseTemplate.Checked():
            self.m_Doc_popuplistTemplates.Enabled(True)
        else:
            self.m_Doc_popuplistTemplates.Enabled(False)
            self.m_Doc_popuplistTemplates.SetData('')
            HedgeTemplate.on_hedgetemplate_testsetting_change(self, cd)
        HedgeTemplate.set_fields_enabled(self, (not self.m_Doc_checkboxUseTemplate.Checked())
                                         and (HedgeConstants.BLN_MODIFY_SETTINGS))

    def on_input_identifier_activate(self, cd):
        if self.m_Doc_inputIdentifier.GetData():
            self.m_hedgeRelation = HedgeRelation.HedgeRelation(
                self.m_Doc_inputIdentifier.GetData()
            )
        result = self.m_hedgeRelation.read()
        self.populate_documentation_from_saved()
        self.reset_test_summary()

    def on_start_date_input(self, self2, cd):
        self.m_Doc_startdate.SetData(self.date_adjust_period(HedgeConstants.DAT_TODAY,
                                                             self.m_Doc_startdate.GetData()))

    def on_end_date_input(self, self2, cd):
        self.m_Doc_enddate.SetData(self.date_adjust_period(HedgeConstants.DAT_TODAY,
                                                           self.m_Doc_enddate.GetData()))

    def date_adjust_period(self, date, period):
        try:
            date = acm.Time().DateAdjustPeriod(HedgeConstants.DAT_TODAY, period)
            return date
        except:
            pass
        return period

    def check_if_modified(self):
        ''' Check if the m_hedgeRelation matches the m_documentions
        '''
        if self.m_hedgeRelation is None or self.m_hedgeRelation.get_file_name() is None:
            return False
        if self.m_hedgeRelation.get_status() == 'De-Designated':
            return False

        if self.m_hedgeRelation.get_template_name() and self.m_Doc_popuplistTemplates.GetData():
            if self.m_Doc_popuplistTemplates.GetData() != self.m_hedgeRelation.get_template_name():
                return True
        elif self.m_hedgeRelation.get_template_name() or self.m_Doc_popuplistTemplates.GetData():
            return True

        trueFalse = ['False', 'True']
        saved_test_settings = self.m_hedgeRelation.get_test_settings()
        document_test_settings = HedgeTemplate.get_test_settings(self)

        if (saved_test_settings['Properties']['HedgeType'] !=
                document_test_settings['Properties']['HedgeType']):
            return True
        if (saved_test_settings['Properties']['HedgeSubType'] !=
                document_test_settings['Properties']['HedgeSubType']):
            return True
        if (saved_test_settings['Properties']['HedgeRiskType'] !=
                document_test_settings['Properties']['HedgeRiskType']):
            return True
        if (saved_test_settings['Properties']['HedgeObjective'] !=
                document_test_settings['Properties']['HedgeObjective']):
            return True
        if (bool(trueFalse.index(saved_test_settings['ProDollarOffset']['Enabled'])) !=
                document_test_settings['ProDollarOffset']['Enabled']):
            return True
        if (saved_test_settings['ProDollarOffset']['LoWarning'] !=
                document_test_settings['ProDollarOffset']['LoWarning']):
            return True
        if (saved_test_settings['ProDollarOffset']['HiWarning'] !=
                document_test_settings['ProDollarOffset']['HiWarning']):
            return True
        if (bool(trueFalse.index(saved_test_settings['Regression']['Enabled'])) !=
                document_test_settings['Regression']['Enabled']):
            return True
        if (saved_test_settings['Regression']['HiBetaWarning'] !=
                document_test_settings['Regression']['HiBetaWarning']):
            return True
        if (saved_test_settings['Regression']['LoBetaWarning'] !=
                document_test_settings['Regression']['LoBetaWarning']):
            return True
        if (saved_test_settings['Regression']['R2Warning'] !=
                document_test_settings['Regression']['R2Warning']):
            return True
        if (saved_test_settings['Regression']['PValueWarning'] !=
                document_test_settings['Regression']['PValueWarning']):
            return True
        if (bool(trueFalse.index(saved_test_settings['CriticalTerms']['Enabled'])) !=
                document_test_settings['CriticalTerms']['Enabled']):
            return True
        if (bool(trueFalse.index(saved_test_settings['ProVRM']['Enabled'])) !=
                document_test_settings['ProVRM']['Enabled']):
            return True
        if saved_test_settings['ProVRM']['Warning'] != document_test_settings['ProVRM']['Warning']:
            return True
        if (bool(trueFalse.index(saved_test_settings['RetroDollarOffset']['Enabled'])) !=
                document_test_settings['RetroDollarOffset']['Enabled']):
            return True
        if (saved_test_settings['RetroDollarOffset']['LoWarning'] !=
                document_test_settings['RetroDollarOffset']['LoWarning']):
            return True
        if (saved_test_settings['RetroDollarOffset']['HiWarning'] !=
                document_test_settings['RetroDollarOffset']['HiWarning']):
            return True
        if (bool(trueFalse.index(saved_test_settings['RetroVRM']['Enabled'])) !=
                document_test_settings['RetroVRM']['Enabled']):
            return True
        if (saved_test_settings['RetroVRM']['Warning'] !=
                document_test_settings['RetroVRM']['Warning']):
            return True
        if (saved_test_settings['TimeBuckets']['TimeBuckets'] !=
                document_test_settings['TimeBuckets']['TimeBuckets']):
            return True
        if self.m_hedgeRelation.get_end_date() != self.m_Doc_enddate.GetData():
            return True
        if self.m_hedgeRelation.get_start_date() != self.m_Doc_startdate.GetData():
            return True
        if self.m_hedgeRelation.get_status() != self.m_Doc_optionStatus.GetData():
            return True
        if self.m_hedgeRelation.get_HR_reference() != self.m_Doc_referenceHR.GetData():
            return True
        return False

    def populate_documentation_from_saved(self):
        termination_reason = self.m_hedgeRelation.get_termination()

        self.m_Doc_inputIdentifier.SetData(self.m_hedgeRelation.get_id())

        self.m_Doc_referenceHR.SetData(self.m_hedgeRelation.get_HR_reference())
        saved_hr_status = self.m_hedgeRelation.get_status()
        self.update_based_on_hr_status(None, saved_hr_status)

        self.m_Doc_backdateReason.SetData(self.m_hedgeRelation.get_backdate_reason())
        self.m_Doc_startdate.SetData(self.m_hedgeRelation.get_start_date())
        self.m_Doc_enddate.SetData(self.m_hedgeRelation.get_end_date())
        self.m_Doc_termination.SetData(termination_reason)
        
        if termination_reason == HedgeConstants.DedesignationReason.PartialDedesignation:
            self.m_Doc_nominal.SetData(self.m_hedgeRelation.get_nominal())

        self.m_Doc_terminationDate.SetData(self.m_hedgeRelation.get_termination_date())

        self.update_documentation_trades()

        # Set Test Settings - check if using template or standalone
        testsettings = {}
        template_name = self.m_hedgeRelation.get_template_name()
        if template_name:
            self.m_Doc_popuplistTemplates.SetData(template_name)
            self.m_Doc_checkboxUseTemplate.Checked(True)
            testsettings = self.m_hedgeRelation.get_test_settings()
        else:
            self.m_Doc_checkboxUseTemplate.Checked(False)
            testsettings = self.m_hedgeRelation.get_test_settings()

        if testsettings != {}:
            HedgeTemplate.set_test_settings(self, testsettings)

        # Create Documentation
        self.on_checkbox_use_template_activate(None, 0)
        self.modified = False

    def populate_default_values(self):
        self.m_Doc_inputIdentifier.Clear()
        self.m_Doc_backdateReason.Clear()
        hedge_relations = HedgeRelation.get_hedge_relations()
        hedge_relations.sort()
        for hedge_relation in hedge_relations:
            self.m_Doc_referenceHR.AddItem(hedge_relation)
        self.m_Doc_referenceHR.AddItem('')
        self.m_Doc_referenceHR.SetData('')
        self.m_Doc_optionStatus.Clear()
        self.m_Doc_optionStatus.AddItem(HedgeConstants.Hedge_Relation_Status.Simulated)
        self.m_Doc_optionStatus.SetData(HedgeConstants.Hedge_Relation_Status.Simulated)
        self.m_Doc_startdate.SetData(HedgeConstants.DAT_TODAY)
        self.m_Doc_enddate.Clear()

    def initialise_documentation(self):
        self.m_Doc_inputIdentifier = self.m_layoutDocumentation.GetControl('inputIdentifier')
        self.m_Doc_referenceHR = self.m_layoutDocumentation.GetControl('referenceHR')
        self.m_Doc_optionStatus = self.m_layoutDocumentation.GetControl('optionStatus')
        self.m_Doc_backdateReason = self.m_layoutDocumentation.GetControl('backdateReason')
        self.m_Doc_listtrades = self.m_layoutDocumentation.GetControl('listtrades')

        self.m_Doc_sheet = self.m_layoutDocumentation.GetControl('sheet')

        self.m_Doc_startdate = self.m_layoutDocumentation.GetControl('startdate')
        self.m_Doc_enddate = self.m_layoutDocumentation.GetControl('enddate')
        self.m_Doc_termination = self.m_layoutDocumentation.GetControl('termination')
        self.m_Doc_nominal = self.m_layoutDocumentation.GetControl('terminationNominal')
        self.m_Doc_terminationDate = self.m_layoutDocumentation.GetControl('terminationDate')

        self.m_Doc_inputResultProDollarOffset = self.m_layoutDocumentation.GetControl(
            'inputResultProDollarOffset'
        )
        self.m_Doc_inputResultRetroDollarOffset = self.m_layoutDocumentation.GetControl(
            'inputResultRetroDollarOffset'
        )
        self.m_Doc_inputResultRegression = self.m_layoutDocumentation.GetControl(
            'inputResultRegression'
        )
        self.m_Doc_inputResultProVRM = self.m_layoutDocumentation.GetControl(
            'inputResultProVRM'
        )
        self.m_Doc_inputResultRetroVRM = self.m_layoutDocumentation.GetControl(
            'inputResultRetroVRM'
        )
        self.m_Doc_inputResultCriticalTerms = self.m_layoutDocumentation.GetControl(
            'inputResultCriticalTerms'
        )
        self.m_Doc_inputResultOverall = self.m_layoutDocumentation.GetControl('inputResultOverall')

        # Set Default Status
        self.m_Doc_optionStatus.SetData(HedgeConstants.Hedge_Relation_Status.Simulated)

        # Enable/Disable Fields
        self.m_Doc_inputIdentifier.Enabled = False
        self.m_Doc_backdateReason.Enabled = False
        self.m_Doc_termination.Enabled = False
        self.m_Doc_nominal.Enabled = False
        self.m_Doc_terminationDate.Enabled = False

        # Initialise External Template
        self.m_Doc_checkboxUseTemplate = self.m_layoutDocumentation.GetControl(
            'checkboxUseTemplate')
        self.m_Doc_popuplistTemplates = self.m_layoutDocumentation.GetControl(
            'popuplistTemplates')
        HedgeTemplate.HandleCreate(self, None, self.m_layoutDocumentation)

        for template in HedgeTemplate.get_templates():  # Do not use Populate()
            self.m_Doc_popuplistTemplates.AddItem(template)

        # Define List
        self.m_Doc_listtrades.ShowGridLines(True)
        self.m_Doc_listtrades.ShowColumnHeaders(True)
        self.m_Doc_listtrades.Editable(True)
        self.m_Doc_listtrades.AddColumn('Trade', -1, 'Trade')
        self.m_Doc_listtrades.AddColumn('Instrument', -1, 'Instrument')
        self.m_Doc_listtrades.AddColumn('Type', -1, 'Type')
        self.m_Doc_listtrades.AddColumn('%', -1, '%')
        self.m_Doc_listtrades.AddColumn('Child Trade', -1, 'Child Trade')

        self.m_Doc_startdate.AddCallback('Activate', self.on_start_date_input, None)
        self.m_Doc_enddate.AddCallback('Activate', self.on_end_date_input, None)

        self.m_Doc_checkboxUseTemplate.AddCallback('Activate',
                                                   self.on_checkbox_use_template_activate,
                                                   None)
        self.m_Doc_popuplistTemplates.AddCallback('Activate',
                                                  self.on_popup_list_templates_activate,
                                                  None)

        # Populate fields with default values
        self.populate_default_values()

    def initialise_dealpackage_grid(self, dealPackageName):
        '''
        Insert the deal package window into the HR GUI
        '''

        self.m_Doc_sheet.GetCustomControl().RemoveAllRows()

        if dealPackageName:
            sheet = self.m_Doc_sheet.GetCustomControl()
            sheet.RemoveAllRows()

            package = acm.FDealPackage[dealPackageName]
            sheet.GridBuilder().InsertItem(package)

            userPref = acm.GetUserPreferences().Clone()
            try:
                userPref.RestoreDealPackageApplicationSheetContents(
                    acm.FDealPackage[dealPackageName].Definition()
                )
            except Exception, e:
                logger.ELOG(e)
                return
            acm.GetUserPreferences().Apply(userPref)
            try:
                acm.GetUserPreferences().Commit()
            except Exception, e:
                logger.ELOG(e)
                acm.GetUserPreferences().Undo()
            if self.m_Doc_sheet:
                columnCreators = sheet.ColumnCreators()
                while columnCreators.Size() > 0:
                    creator = columnCreators.At(0)
                    columnCreators.Remove(creator)
                defaultColumns = HedgeConstants.LST_DP_DEFAULT_COLUMNS
                ''' Cannot access GetAttribute if DP in a consistent storage state
                package_clone = package.Copy()
                defaultColumns = package_clone.GetAttribute("sheetDefaultColumns")
                if not defaultColumns or len(defaultColumns) == 0:
                    defaultColumns = HedgeConstants.LST_DP_DEFAULT_COLUMNS
                '''
                if (package.Definition() and
                        acm.GetUserPreferences().DealPackageApplicationSheetContents(
                            package.Definition())):
                    sheet.SheetContents(
                        acm.GetUserPreferences().DealPackageApplicationSheetContents(
                            package.Definition()
                        )
                    )
                else:
                    context = acm.GetDefaultContext()
                    creators = acm.GetColumnCreators(defaultColumns, context)
                    i = 0
                    while i < creators.Size():
                        creator = creators.At(i)
                        sheet.ColumnCreators().Add(creator)
                        i = i + 1

    def initialise_pro_dollar_offset(self):
        ''' Set Controls
        '''
        self.m_PDO_textDescription = self.m_layoutProDO.GetControl('textDescription')
        self.m_PDO_list = self.m_layoutProDO.GetControl('items')
        self.m_PDO_original = self.m_layoutProDO.GetControl('original')
        self.m_PDO_external = self.m_layoutProDO.GetControl('external')
        self.m_PDO_do_percent = self.m_layoutProDO.GetControl('do_percent')
        self.m_PDO_graphpanel = self.m_layoutProDO.GetControl('graphpanel').GetCustomControl()
        self.m_PDO_checkDollarOffset = self.m_layoutProDO.GetControl('checkDollarOffset')
        self.m_PDO_checkWarningBoundaries = self.m_layoutProDO.GetControl('checkWarningBoundaries')
        self.m_PDO_checkLimitBoundaries = self.m_layoutProDO.GetControl('checkLimitBoundaries')

        # Set initial values
        self.m_PDO_checkDollarOffset.Checked(True)
        self.m_PDO_checkWarningBoundaries.Checked(True)
        self.m_PDO_checkLimitBoundaries.Checked(True)

        text = HedgeConstants.STR_PDO_INFORMATION.replace('\\t', '\t')
        text = text.split('\n')[0]
        self.m_PDO_textDescription.SetData(text)
        self.m_PDO_textDescription.Editable(False)
        self.m_PDO_textDescription.SetColor('BackgroundReadonly', HedgeConstants.CLR_LIGHT_GRAY2)

        # Enable/Disable
        self.m_PDO_original.Editable(False)
        self.m_PDO_external.Editable(False)
        self.m_PDO_do_percent.Editable(False)

        # Set List Properties
        self.m_PDO_list.ShowGridLines()
        self.m_PDO_list.ShowColumnHeaders()
        self.m_PDO_list.EnableMultiSelect(True)
        self.m_PDO_list.EnableHeaderSorting(True)
        self.m_PDO_list.AddColumn('Date', -1, 'Date')
        self.m_PDO_list.AddColumn('Hypo', -1, 'Hypo')
        self.m_PDO_list.AddColumn('External', -1, 'External')
        self.m_PDO_list.AddColumn('Diff Hypo', -1, 'Diff Hypo')
        self.m_PDO_list.AddColumn('Diff External', -1, 'Diff External')
        self.m_PDO_list.AddColumn('Dollar Offset', -1, 'Dollar Offset')

        # Graph stuff
        self.m_PDO_chart = HedgeEffectivenessCharts.DOChart()
        self.m_PDO_graphpanel.Controls.Add(self.m_PDO_chart.m_chart)

        # Add Callbacks
        self.m_PDO_checkWarningBoundaries.AddCallback('Activate',
                                                      self.on_pro_do_button_press,
                                                      None)
        self.m_PDO_checkLimitBoundaries.AddCallback('Activate',
                                                    self.on_pro_do_button_press,
                                                    None)
        self.m_PDO_checkDollarOffset.AddCallback('Activate',
                                                 self.on_pro_do_button_press,
                                                 None)

        # Initialise Graph - which series to show
        self.on_pro_do_button_press(None, None)

    def initialise_retro_dollar_offset(self):
        ''' Set Controls
        '''
        self.m_RDO_textDescription = self.m_layoutRetroDO.GetControl('textDescription')
        self.m_RDO_list = self.m_layoutRetroDO.GetControl('items')
        self.m_RDO_original = self.m_layoutRetroDO.GetControl('original')
        self.m_RDO_external = self.m_layoutRetroDO.GetControl('external')
        self.m_RDO_do_percent = self.m_layoutRetroDO.GetControl('do_percent')
        self.m_RDO_graphpanel = self.m_layoutRetroDO.GetControl('graphpanel').GetCustomControl()
        self.m_RDO_checkDollarOffset = self.m_layoutRetroDO.GetControl('checkDollarOffset')
        self.m_RDO_checkWarningBoundaries = self.m_layoutRetroDO.GetControl(
            'checkWarningBoundaries')
        self.m_RDO_checkLimitBoundaries = self.m_layoutRetroDO.GetControl('checkLimitBoundaries')

        # Set initial values
        self.m_RDO_checkDollarOffset.Checked(True)
        self.m_RDO_checkWarningBoundaries.Checked(True)
        self.m_RDO_checkLimitBoundaries.Checked(True)

        text = HedgeConstants.STR_RDO_INFORMATION
        text = text.split('\n')[0]
        self.m_RDO_textDescription.SetData(text)
        self.m_RDO_textDescription.Editable(False)
        self.m_RDO_textDescription.SetColor('BackgroundReadonly', HedgeConstants.CLR_LIGHT_GRAY2)

        # Enable/Disable
        self.m_RDO_original.Editable(False)
        self.m_RDO_external.Editable(False)
        self.m_RDO_do_percent.Editable(False)

        # Set List Properties
        self.m_RDO_list.ShowGridLines()
        self.m_RDO_list.ShowColumnHeaders()
        self.m_RDO_list.EnableMultiSelect(True)
        self.m_RDO_list.EnableHeaderSorting(True)
        self.m_RDO_list.AddColumn('Date', -1, 'Date')
        self.m_RDO_list.AddColumn('Hypo', -1, 'Hypo')
        self.m_RDO_list.AddColumn('External', -1, 'External')
        self.m_RDO_list.AddColumn('Diff Hypo', -1, 'Diff Hypo')
        self.m_RDO_list.AddColumn('Diff External', -1, 'Diff External')
        self.m_RDO_list.AddColumn('Dollar Offset', -1, 'Dollar Offset')

        # Graph stuff
        self.m_RDO_chart = HedgeEffectivenessCharts.DOChart()
        self.m_RDO_graphpanel.Controls.Add(self.m_RDO_chart.m_chart)

        # Add Callbacks
        self.m_RDO_checkWarningBoundaries.AddCallback('Activate',
                                                      self.on_retro_do_button_press,
                                                      None)
        self.m_RDO_checkLimitBoundaries.AddCallback('Activate',
                                                    self.on_retro_do_button_press,
                                                    None)
        self.m_RDO_checkDollarOffset.AddCallback('Activate',
                                                 self.on_retro_do_button_press,
                                                 None)

        # Initialise Graph - which series to show
        self.on_retro_do_button_press(None, None)

    def initialise_regression(self):
        self.m_Reg_textDescription = self.m_layoutRegression.GetControl('textDescription')
        self.m_Reg_list = self.m_layoutRegression.GetControl('items')
        self.m_Reg_InputOriginal = self.m_layoutRegression.GetControl('original')
        self.m_Reg_InputHedge = self.m_layoutRegression.GetControl('hedge')
        self.m_Reg_InputStdErr = self.m_layoutRegression.GetControl('stdErr')
        self.m_Reg_InputAlpha = self.m_layoutRegression.GetControl('alpha')
        self.m_Reg_InputBeta = self.m_layoutRegression.GetControl('beta')
        self.m_Reg_InputCorrelation = self.m_layoutRegression.GetControl('inputCorrelation')
        self.m_Reg_InputR2 = self.m_layoutRegression.GetControl('R2')
        self.m_Reg_InputPSignificance = self.m_layoutRegression.GetControl('inputPSignificance')
        self.m_Reg_InputPValue = self.m_layoutRegression.GetControl('inputPValue')
        self.m_Reg_graphpanel = self.m_layoutRegression.GetControl('graphpanel').GetCustomControl()
        self.m_Reg_chart = HedgeEffectivenessCharts.RegressionChart()

        self.m_Reg_InputOriginal.Editable(False)
        self.m_Reg_InputHedge.Editable(False)
        self.m_Reg_InputStdErr.Editable(False)
        self.m_Reg_InputAlpha.Editable(False)
        self.m_Reg_InputBeta.Editable(False)
        self.m_Reg_InputCorrelation.Editable(False)
        self.m_Reg_InputR2.Editable(False)
        self.m_Reg_InputPSignificance.Editable(False)
        self.m_Reg_InputPValue.Editable(False)

        self.m_Reg_show0 = self.m_layoutRegression.GetControl('show0')
        self.m_Reg_show1 = self.m_layoutRegression.GetControl('show1')
        self.m_Reg_show2 = self.m_layoutRegression.GetControl('show2')
        self.m_Reg_show3 = self.m_layoutRegression.GetControl('show3')

        # Initialize List
        self.m_Reg_list.ShowGridLines()
        self.m_Reg_list.ShowColumnHeaders()
        self.m_Reg_list.EnableMultiSelect(True)
        self.m_Reg_list.EnableHeaderSorting(True)
        self.m_Reg_list.AddColumn('Date', -1, 'Date')
        self.m_Reg_list.AddColumn('Hypo', -1, 'Hypo')
        self.m_Reg_list.AddColumn('External', -1, 'External')
        self.m_Reg_list.AddColumn('Diff Hypo', -1, 'Diff Hypo')
        self.m_Reg_list.AddColumn('Diff External', -1, 'Diff External')

        # Graph Stuff
        self.m_Reg_graphpanel.Controls.Add(self.m_Reg_chart.m_chart)

        text = HedgeConstants.STR_REG_INFORMATION
        text = text.split('\n')[0]
        self.m_Reg_textDescription.SetData(text)
        self.m_Reg_textDescription.Editable(False)
        self.m_Reg_textDescription.SetColor('BackgroundReadonly', HedgeConstants.CLR_LIGHT_GRAY2)

        # Initialise checkbox settings
        self.m_Reg_show0.Checked(False)
        self.m_Reg_show1.Checked(False)
        self.m_Reg_show2.Checked(True)
        self.m_Reg_show3.Checked(True)

        # Add Callbacks
        self.m_Reg_show0.AddCallback('Activate', self.on_reg_checkbox_press, None)
        self.m_Reg_show1.AddCallback('Activate', self.on_reg_checkbox_press, None)
        self.m_Reg_show2.AddCallback('Activate', self.on_reg_checkbox_press, None)
        self.m_Reg_show3.AddCallback('Activate', self.on_reg_checkbox_press, None)

        # Initialize which series to show
        self.on_reg_checkbox_press(None, None)

    def initialise_retro_vrm(self):
        ''' Set Controls
        '''
        self.m_RVRM_textDescription = self.m_layoutRetroVRM.GetControl('textDescription')
        self.m_RVRM_list = self.m_layoutRetroVRM.GetControl('items')
        self.m_RVRM_original = self.m_layoutRetroVRM.GetControl('original')
        self.m_RVRM_external = self.m_layoutRetroVRM.GetControl('external')
        self.m_RVRM_vr_percent = self.m_layoutRetroVRM.GetControl('vr_percent')
        self.m_RVRM_graphpanel = self.m_layoutRetroVRM.GetControl('graphpanel').GetCustomControl()
        self.m_RVRM_checkVariableReduction = self.m_layoutRetroVRM.GetControl(
            'checkVariableReduction')
        self.m_RVRM_checkWarningBoundaries = self.m_layoutRetroVRM.GetControl(
            'checkWarningBoundaries')
        self.m_RVRM_checkLimitBoundaries = self.m_layoutRetroVRM.GetControl('checkLimitBoundaries')

        # Set initial values
        self.m_RVRM_checkVariableReduction.Checked(True)
        self.m_RVRM_checkWarningBoundaries.Checked(True)
        self.m_RVRM_checkLimitBoundaries.Checked(True)

        text = HedgeConstants.STR_RVRM_INFORMATION
        text = text.split('\n')[0]
        self.m_RVRM_textDescription.SetData(text)
        self.m_RVRM_textDescription.Editable(False)
        self.m_RVRM_textDescription.SetColor('BackgroundReadonly', HedgeConstants.CLR_LIGHT_GRAY2)

        # Enable/Disable
        self.m_RVRM_original.Editable(False)
        self.m_RVRM_external.Editable(False)
        self.m_RVRM_vr_percent.Editable(False)

        # Set List Properties
        self.m_RVRM_list.ShowGridLines()
        self.m_RVRM_list.ShowColumnHeaders()
        self.m_RVRM_list.EnableMultiSelect(True)
        self.m_RVRM_list.EnableHeaderSorting(True)
        self.m_RVRM_list.AddColumn('Date', -1, 'Date')
        self.m_RVRM_list.AddColumn('Hypo', -1, 'Hypo')
        self.m_RVRM_list.AddColumn('External', -1, 'External')
        self.m_RVRM_list.AddColumn('Diff Hypo', -1, 'Diff Hypo')
        self.m_RVRM_list.AddColumn('Diff External', -1, 'Diff External')
        self.m_RVRM_list.AddColumn('Cum Var Reduction', -1, 'Cum Var Reduction')

        # Graph stuff
        self.m_RVRM_chart = HedgeEffectivenessCharts.VRMChart()
        self.m_RVRM_graphpanel.Controls.Add(self.m_RVRM_chart.m_chart)

        # Add Callbacks
        self.m_RVRM_checkWarningBoundaries.AddCallback('Activate',
                                                       self.on_retro_vrm_button_press,
                                                       None)
        self.m_RVRM_checkLimitBoundaries.AddCallback('Activate',
                                                     self.on_retro_vrm_button_press,
                                                     None)
        self.m_RVRM_checkVariableReduction.AddCallback('Activate',
                                                       self.on_retro_vrm_button_press,
                                                       None)

        # Initialise Graph - which series to show
        self.on_retro_vrm_button_press(None, None)

    def initialise_pro_vrm(self):
        ''' Set Controls
        '''
        self.m_PVRM_textDescription = self.m_layoutProVRM.GetControl('textDescription')
        self.m_PVRM_list = self.m_layoutProVRM.GetControl('items')
        self.m_PVRM_original = self.m_layoutProVRM.GetControl('original')
        self.m_PVRM_external = self.m_layoutProVRM.GetControl('external')
        self.m_PVRM_vr_percent = self.m_layoutProVRM.GetControl('vr_percent')
        self.m_PVRM_graphpanel = self.m_layoutProVRM.GetControl('graphpanel').GetCustomControl()
        self.m_PVRM_checkVariableReduction = self.m_layoutProVRM.GetControl(
            'checkVariableReduction')
        self.m_PVRM_checkWarningBoundaries = self.m_layoutProVRM.GetControl(
            'checkWarningBoundaries')
        self.m_PVRM_checkLimitBoundaries = self.m_layoutProVRM.GetControl('checkLimitBoundaries')

        # Set initial values
        self.m_PVRM_checkVariableReduction.Checked(True)
        self.m_PVRM_checkWarningBoundaries.Checked(True)
        self.m_PVRM_checkLimitBoundaries.Checked(True)

        text = HedgeConstants.STR_PVRM_INFORMATION
        text = text.split('\n')[0]
        self.m_PVRM_textDescription.SetData(text)
        self.m_PVRM_textDescription.Editable(False)
        self.m_PVRM_textDescription.SetColor('BackgroundReadonly', HedgeConstants.CLR_LIGHT_GRAY2)

        # Enable/Disable
        self.m_PVRM_original.Editable(False)
        self.m_PVRM_external.Editable(False)
        self.m_PVRM_vr_percent.Editable(False)

        # Set List Properties
        self.m_PVRM_list.ShowGridLines()
        self.m_PVRM_list.ShowColumnHeaders()
        self.m_PVRM_list.EnableMultiSelect(True)
        self.m_PVRM_list.EnableHeaderSorting(True)
        self.m_PVRM_list.AddColumn('Date', -1, 'Date')
        self.m_PVRM_list.AddColumn('Hypo', -1, 'Hypo')
        self.m_PVRM_list.AddColumn('External', -1, 'External')
        self.m_PVRM_list.AddColumn('Diff Hypo', -1, 'Diff Hypo')
        self.m_PVRM_list.AddColumn('Diff External', -1, 'Diff External')
        self.m_PVRM_list.AddColumn('Cum Var Reduction', -1, 'Cum Var Reduction')

        # Graph stuff
        self.m_PVRM_chart = HedgeEffectivenessCharts.VRMChart()
        self.m_PVRM_graphpanel.Controls.Add(self.m_PVRM_chart.m_chart)

        # Add Callbacks
        self.m_PVRM_checkWarningBoundaries.AddCallback('Activate',
                                                       self.on_pro_vrm_button_press,
                                                       None)
        self.m_PVRM_checkLimitBoundaries.AddCallback('Activate',
                                                     self.on_pro_vrm_button_press,
                                                     None)
        self.m_PVRM_checkVariableReduction.AddCallback('Activate',
                                                       self.on_pro_vrm_button_press,
                                                       None)

        # Initialise Graph - which series to show
        self.on_pro_vrm_button_press(None, None)

    def initialise_critical_terms(self):
        ''' Set Controls
        '''
        self.m_CT_textDescription = self.m_layoutCriticalTerms.GetControl('textDescription')
        self.m_CT_result = self.m_layoutCriticalTerms.GetControl('result')
        self.m_CT_results = self.m_layoutCriticalTerms.GetControl('results')

        # Set initial values
        text = HedgeConstants.STR_CRITICAL_INFORMATION
        self.m_CT_textDescription.SetData(text)
        self.m_CT_textDescription.Editable(False)
        self.m_CT_textDescription.SetColor('BackgroundReadonly', HedgeConstants.CLR_LIGHT_GRAY2)

        # Initialise List
        self.m_CT_results.ShowGridLines()
        self.m_CT_results.ShowColumnHeaders()
        self.m_CT_results.EnableMultiSelect(True)
        self.m_CT_results.EnableHeaderSorting(True)
        self.m_CT_results.AddColumn('Term', -1, 'Term')

    def create_layout_dollar_offset(self):
        b = acm.FUxLayoutBuilder()
        b.BeginVertBox('None', '')
        b.  BeginHorzBox('EtchedIn', 'Description')
        b.    AddText('textDescription', -1, 60, -1, 60)
        b.  EndBox()
        b.  BeginHorzBox('None', '')
        b.    BeginVertBox('EtchedIn', 'Data')
        b.      AddList('items', -1, -1, 50)
        b.    EndBox()
        b.    BeginVertBox('EtchedIn', 'Graph')
        b.      BeginVertBox('EtchedIn', '')
        b.        BeginHorzBox('None', '')
        b.          AddInput('original', 'Hypo')
        b.          AddInput('external', 'External')
        b.          AddInput('do_percent', 'Dollar Offset')
        b.        EndBox()
        b.      EndBox()
        b.      BeginVertBox('None', '')
        FUxNet.AddWinFormsControlToBuilder(b,
                                           'graphpanel',
                                           'System.Windows.Forms.Panel',
                                           'System.Windows.Forms',
                                           100,
                                           100)
        b.      EndBox()
        b.      BeginVertBox('EtchedIn', 'Show Series')
        b.        BeginHorzBox('None', '')
        b.          AddCheckbox('checkDollarOffset', 'Dollar Offset')
        b.          AddCheckbox('checkWarningBoundaries', 'Show Warning Thresholds')
        b.          AddCheckbox('checkLimitBoundaries', 'Show Limit Thresholds')
        b.        EndBox()
        b.      EndBox()
        b.    EndBox()
        b.  EndBox()
        b.EndBox()
        return b

    def create_layout_vrm(self):
        b = acm.FUxLayoutBuilder()
        b.BeginVertBox('None', '')
        b.  BeginHorzBox('EtchedIn', 'Description')
        b.    AddText('textDescription', -1, 60, -1, 60)
        b.  EndBox()
        b.  BeginHorzBox('None', '')
        b.    BeginVertBox('EtchedIn', 'Data')
        b.      AddList('items', -1, -1, 50)
        b.    EndBox()
        b.    BeginVertBox('EtchedIn', 'Graph')
        b.      BeginVertBox('EtchedIn', '')
        b.        BeginHorzBox('None', '')
        b.          AddInput('original', 'Hypo')
        b.          AddInput('external', 'External')
        b.          AddInput('vr_percent', 'Variable Reduction')
        b.        EndBox()
        b.      EndBox()
        b.      BeginVertBox('None', '')
        FUxNet.AddWinFormsControlToBuilder(b,
                                           'graphpanel',
                                           'System.Windows.Forms.Panel',
                                           'System.Windows.Forms',
                                           100,
                                           100)
        b.      EndBox()
        b.      BeginVertBox('EtchedIn', 'Show Series')
        b.        BeginHorzBox('None', '')
        b.          AddCheckbox('checkVariableReduction', 'Variable Reduction')
        b.          AddCheckbox('checkWarningBoundaries', 'Show Warning Threshold')
        b.          AddCheckbox('checkLimitBoundaries', 'Show Limit Threshold')
        b.        EndBox()
        b.      EndBox()
        b.    EndBox()
        b.  EndBox()
        b.EndBox()
        return b

    def create_layout_regression(self):
        b = acm.FUxLayoutBuilder()
        b.BeginVertBox('None', '')
        b.  BeginHorzBox('EtchedIn', 'Description')
        b.    AddText('textDescription', -1, -1, -1, 90)
        b.  EndBox()
        b.  BeginHorzBox('None', '')
        b.    BeginVertBox('EtchedIn', 'Data')
        b.      AddList('items', -1, -1, 50)
        b.    EndBox()
        b.    BeginVertBox('EtchedIn', 'Graph')
        b.      BeginVertBox('EtchedIn', '')
        b.        BeginHorzBox('None', '')
        b.          AddInput('original', 'Hypo')
        b.          AddInput('hedge', 'External')
        b.          AddInput('stdErr', 'Std Err')
        b.        EndBox()
        b.        BeginHorzBox('None', '')
        b.          AddInput('alpha', 'Alpha')
        b.          AddInput('beta', 'Beta')
        b.          AddInput('inputPValue', 'P Value')
        b.        EndBox()
        b.        BeginHorzBox('None', '')
        b.          AddInput('inputCorrelation', 'Correlation')
        b.          AddInput('R2', 'R Square')
        b.          AddInput('inputPSignificance', 'P Significance')
        b.        EndBox()
        b.      EndBox()
        b.      BeginVertBox('None', '')
        FUxNet.AddWinFormsControlToBuilder(b,
                                           'graphpanel',
                                           'System.Windows.Forms.Panel',
                                           'System.Windows.Forms',
                                           100,
                                           100)
        b.      EndBox()
        b.      BeginHorzBox('EtchedIn', 'Show Series')
        b.        AddCheckbox('show0', 'Hypo')
        b.        AddCheckbox('show1', 'External')
        b.        AddCheckbox('show2', 'Hypo vs External')
        b.        AddCheckbox('show3', 'Regression Plot')
        b.      EndBox()
        b.    EndBox()
        b.  EndBox()
        b.EndBox()
        return b

    def create_layout_documentation(self):
        b = acm.FUxLayoutBuilder()
        b.BeginVertBox('None', '')
        b.  BeginHorzBox('None', '')
        b.    BeginVertBox('None', '')
        b.      BeginVertBox('EtchedIn', 'External Properties')
        b.        BeginHorzBox('None', '')
        b.          AddInput('inputIdentifier', 'Id')
        b.          AddOption('referenceHR', 'Ref HR')
        b.        EndBox()
        b.        BeginHorzBox('None', '')
        b.          AddInput('backdateReason', 'Backdate Reason')
        b.          AddOption('optionStatus', 'Status')
        b.        EndBox()
        b.        BeginHorzBox('None', '')
        b.          AddInput('startdate', 'Start Date')
        b.          AddInput('enddate', 'End Date')
        b.        EndBox()
        b.        BeginVertBox('EtchedIn', 'De-designation')
        b.          BeginHorzBox('None', '')
        b.            AddInput('termination', 'Reason', 35, -1)
        b.          EndBox()
        b.          BeginHorzBox('None', '')
        b.            AddInput('terminationNominal', 'Nominal', 35, -1)
        b.          EndBox()
        b.          BeginHorzBox('None', '')
        b.            AddInput('terminationDate', 'Date', 12, -1)
        b.          EndBox()
        b.        EndBox()
        b.        BeginVertBox('EtchedIn', 'Hedge Relationship Trades (Parents)')
        b.          AddList('listtrades', 6, 6)
        b.        EndBox()
        b.        BeginVertBox('EtchedIn', 'Deal Package (Child Trades)')
        b.          AddCustom('sheet',
                              'sheet.FDealPackageSheet',
                              150,
                              150,
                              -1,
                              -1,
                              acm.DealCapturing().CreateGridConfiguration(False, False))
        b.        EndBox()
        b.      EndBox()
        b.      BeginVertBox('EtchedIn', 'Test Results (Inactive tests are greyed out)')
        b.        BeginHorzBox('EtchedIn', 'Individual Results')
        b.          BeginVertBox('None', '')
        b.            AddInput('inputResultProDollarOffset', 'Pro Dollar Offset', 20, 20)
        b.            AddInput('inputResultProVRM', 'Pro Variable Reduction', 20, 20)
        b.            AddInput('inputResultRegression', 'Regression', 20, 20)
        b.          EndBox()
        b.          BeginVertBox('None', '')
        b.            AddInput('inputResultRetroDollarOffset', 'Retro Dollar Offset', 20, 20)
        b.            AddInput('inputResultRetroVRM', 'Retro Variable Reduction', 20, 20)
        b.            AddInput('inputResultCriticalTerms', 'Critical Terms', 20, 20)
        b.          EndBox()
        b.        EndBox()
        b.        BeginHorzBox('EtchedIn', 'Overall Result')
        b.          AddInput('inputResultOverall', '', 40, -1)
        b.        EndBox()
        b.      EndBox()
        b.    EndBox()
        b.    BeginVertBox('EtchedIn', 'Test Settings')
        b.      BeginVertBox('None', 'Test Settings')
        b.        BeginHorzBox('EtchedIn', '')
        b.          AddCheckbox('checkboxUseTemplate', 'Use Template')
        b.          AddPopuplist('popuplistTemplates', '')
        b.        EndBox()
        HedgeTemplate.CreateLayout(b)
        b.      EndBox()
        b.    EndBox()
        b.  EndBox()
        b.EndBox()
        return b

    def create_layout_critical_terms(self):
        b = acm.FUxLayoutBuilder()
        b.BeginVertBox('None', '')
        b.  BeginHorzBox('EtchedIn', 'Description')
        b.    AddText('textDescription', -1, -1, -1, 90)
        b.  EndBox()
        b.  BeginVertBox('None', '')
        b.    AddInput('result', 'Result')
        b.    AddList('results')
        b.  EndBox()
        b.EndBox()
        return b


class CreateObject(FUxCore.MenuItem):
    def __init__(self, extObj):
        self.m_extObj = extObj

    def Invoke(self, eii):
        if userAccess.is_hedge_user():
            StartApplication(eii)
        else:
            return None

    def Applicable(self):
        return userAccess.is_hedge_user()

    def Enabled(self):
        return userAccess.is_hedge_user()

    def Checked(self):
        return False


def DisplayCheck(extObj):
    return CreateObject(extObj)

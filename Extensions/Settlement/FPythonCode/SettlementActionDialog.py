""" Compiled: 2020-09-18 10:38:49 """

#__src_file__ = "extensions/settlement/etc/gui/SettlementActionDialog.py"
from __future__ import print_function
import acm
import FUxCore

from SettlementDiaryDialog import SettlementDiaryDialog
from SettlementBankingDay import HandleBankingDay

#---------------------------------------------------------------------------
class SettlementActionDialog (FUxCore.LayoutDialog):
    def __init__(self, command, actionName):
        self.m_actionName = actionName
        self.reviewAPI = command
        self.m_settlements = self.reviewAPI.GetEditableObjects()
        self.m_originalSettlements = self.reviewAPI.GetOriginalObjects()
        self.m_editableFields = self.reviewAPI.EditableFields()
        self.m_selectedSettlement = self.m_settlements[0]
        self.m_bindings = None
        self.m_oid = None
        self.m_trade = None
        self.m_currency = None
        self.m_valueDay = None
        self.m_createTime = None
        self.m_status = None
        self.m_save = None
        self.m_getFromHook = None
        self.m_partialSettlementType = None
        self.m_text = None
        self.m_processStatus = None
        self.m_notificationDay = None
        self.m_topRowSelected = True
        self.m_exceptionQuestionId = 'ContinueDespiteException'
        self.m_diaryQuestionId = 'FillInDiary'

        self.m_list = 0
        self.m_restrictNet = 0
        self.m_isValueDayCheckIgnored = 0

        self.m_statusPopulator = acm.FChoiceListPopulator()
        self.m_statusPopulator.SetChoiceListSource(self.m_selectedSettlement.StatusValidInput())

        self.m_acquirerPopulator = acm.FChoiceListPopulator()
        self.m_acquirerPopulator.SetChoiceListSource(self.m_selectedSettlement.AcquirerValidInput())

        self.m_acquirerAccountRefPopulator = acm.FChoiceListPopulator()
        self.m_acquirerAccountRefPopulator.SetChoiceListSource(self.m_selectedSettlement.AcquirerAccountRefValidInput())

        self.m_counterpartyPopulator = acm.FChoiceListPopulator()
        self.m_counterpartyPopulator.SetChoiceListSource(self.m_selectedSettlement.CounterpartyValidInput())

        self.m_counterpartyAccountRefPopulator = acm.FChoiceListPopulator()
        self.m_counterpartyAccountRefPopulator.SetChoiceListSource(self.m_selectedSettlement.CounterpartyAccountRefValidInput())

        self.m_currencyPopulator = acm.FChoiceListPopulator()
        self.m_currencyPopulator.SetChoiceListSource(self.m_selectedSettlement.CurrencyValidInput())

        self.m_partialSettlementTypePopulator = acm.FChoiceListPopulator()
        self.m_partialSettlementTypePopulator.SetChoiceListSource(self.m_selectedSettlement.PartialSettlementTypeValidInput())

    #---------------------------------------------------------------------------
    def IsDiaryDisabled(self):
        diary = acm.GetDefaultContext().GetExtension('FExtensionValue', 'FSettlement', 'HideDiaryForAction')
        if diary:
            if diary.Value().find(self.m_actionName) != -1:
                return True
        return False

    #---------------------------------------------------------------------------
    def HandleApply(self):
        answers = acm.FSettlementActionAnswers()

        exceptionQuestion, diaryQuestion = GetPopUpQuestions(self.reviewAPI.QuestionsToAnswer(),
                                                             self.m_exceptionQuestionId,
                                                             self.m_diaryQuestionId)

        continueWithSave = self.HandleExceptionQuestion(exceptionQuestion, answers)
        continueWithSave = self.HandleDiaryQuestion(diaryQuestion, answers) if continueWithSave else False

        result = None

        if continueWithSave:
            try:
                result = self.reviewAPI.Save(answers)
            except Exception as e:
                acm.UX().Dialogs().MessageBox(self.m_fuxDlg.Shell(), 'Error', str(e), 'OK', None, None,  'Button1', 'Button2')

                if self.reviewAPI.IsConsumed():
                    result = acm.FDictionary()

        return result

    #---------------------------------------------------------------------------
    def HandleExceptionQuestion(self, exceptionQuestion, answers):
        continueWithSave = True
        if exceptionQuestion:
            answer = acm.UX().Dialogs().MessageBoxYesNo(self.m_fuxDlg.Shell(), 'Warning', exceptionQuestion.Question())
            if answer == 'Button1':
                answers.SetContinueDespiteExceptionAnswer('Yes')
            else:
                continueWithSave = False
        return continueWithSave

    #---------------------------------------------------------------------------
    def HandleDiaryQuestion(self, diaryQuestion, answers):
        continueWithSave = True

        if diaryQuestion:
            customDlg = SettlementDiaryDialog(self.m_selectedSettlement)
            output = acm.UX().Dialogs().ShowCustomDialogModal(self.m_fuxDlg.Shell(), customDlg.CreateLayout(), customDlg)

            if output != None:
                answers.SetFillInDiaryInput(output)
                answers.SetFillInDiaryAnswer('Save')
            else:
                continueWithSave = False

        return continueWithSave

    #---------------------------------------------------------------------------
    def ServerUpdate(self, sender, aspectSymbol, binder):

        if self.m_selectedSettlement and not self.m_updateValues and self.m_topRowSelected:
            value = binder.GetValue()
            labelName = binder.Label()
            if binder == self.m_acquirer:
                labelName = "Acquirer"
            elif binder == self.m_counterparty:
                labelName = "Counterparty"
            elif binder == self.m_acquirerAccount:
                labelName = "AcquirerAccountRef"
            elif binder == self.m_counterpartyAccount:
                labelName = "CounterpartyAccountRef"
            elif binder == self.m_partialSettlementType:
                labelName = "PartialSettlementType"
            elif binder == self.m_notificationDay:
                value = HandleBankingDay(self.m_fuxDlg.Shell(), self.m_selectedSettlement, value)
                labelName = "NotificationDay"
                self.m_updateValues = True
                binder.SetValue(value)
                self.m_updateValues = False
            elif binder == self.m_valueDay:
                value = HandleBankingDay(self.m_fuxDlg.Shell(), self.m_selectedSettlement, value)
                labelName = "ValueDay"
                self.m_updateValues = True
                binder.SetValue(value)
                self.m_updateValues = False
            try:
                eval('self.m_selectedSettlement.{}(value)'.format(labelName))
            except Exception as e:
                acm.UX().Dialogs().MessageBoxOKCancel(self.m_fuxDlg.Shell(), 'Error', str(e))
            self.UpdateValues()

    #---------------------------------------------------------------------------
    def SetField(self, field, value):
        field.SetValue(value)

    #---------------------------------------------------------------------------
    def SetCheckbox(self, field, value):
        field.Checked(value)

    #---------------------------------------------------------------------------
    def SetEnabled(self, field, key):
        field.Enabled(self.m_editableFields.At(key, False))
    
    #---------------------------------------------------------------------------
    def SetPopulator(self, populator, validInput, fieldName, fieldValue):
        if self.m_topRowSelected:
            if self.m_editableFields[fieldName]:
                populator.SetChoiceListSource(validInput)
            else:
                populator.SetChoiceListSource([fieldValue])
        else:
            populator.SetChoiceListSource([fieldValue])

    #---------------------------------------------------------------------------
    def UpdateValues(self):
        self.m_updateValues = True
        if self.m_selectedSettlement:
            self.SetPopulator(self.m_statusPopulator, self.m_selectedSettlement.StatusValidInput(), "Status", self.m_selectedSettlement.Status())
            self.SetPopulator(self.m_acquirerPopulator, self.m_selectedSettlement.AcquirerValidInput(), "Acquirer", self.m_selectedSettlement.Acquirer())
            self.SetPopulator(self.m_acquirerAccountRefPopulator, self.m_selectedSettlement.AcquirerAccountRefValidInput(), "AcquirerAccountRef", self.m_selectedSettlement.AcquirerAccountRef())
            self.SetPopulator(self.m_counterpartyPopulator, self.m_selectedSettlement.CounterpartyValidInput(), "Counterparty", self.m_selectedSettlement.Counterparty())
            self.SetPopulator(self.m_counterpartyAccountRefPopulator, self.m_selectedSettlement.CounterpartyAccountRefValidInput(), "CounterpartyAccountRef", self.m_selectedSettlement.CounterpartyAccountRef())
            self.SetPopulator(self.m_currencyPopulator, self.m_selectedSettlement.CurrencyValidInput(), "Currency", self.m_selectedSettlement.Currency())
            self.SetPopulator(self.m_partialSettlementTypePopulator, self.m_selectedSettlement.PartialSettlementTypeValidInput(), "PartialSettlementType", self.m_selectedSettlement.PartialSettlementType())

        self.SetField(self.m_oid, self.m_selectedSettlement.Oid() if self.m_selectedSettlement else None)
        self.SetField(self.m_trade, self.m_selectedSettlement.Trade() if self.m_selectedSettlement else None)
        self.SetField(self.m_currency, self.m_selectedSettlement.Currency() if self.m_selectedSettlement else None)
        self.SetField(self.m_amount, self.m_selectedSettlement.Amount() if self.m_selectedSettlement else None)
        self.SetField(self.m_valueDay, self.m_selectedSettlement.ValueDay() if self.m_selectedSettlement else None)
        self.SetField(self.m_status, self.m_selectedSettlement.Status() if self.m_selectedSettlement else None)
        self.SetField(self.m_notificationDay, self.m_selectedSettlement.NotificationDay() if self.m_selectedSettlement else None)
        self.SetField(self.m_partialSettlementType, self.m_selectedSettlement.PartialSettlementType() if self.m_selectedSettlement else None)
        self.SetField(self.m_text, self.m_selectedSettlement.Text() if self.m_selectedSettlement else None)
        self.SetField(self.m_processStatus, self.m_selectedSettlement.ProcessStatus() if self.m_selectedSettlement else None)
        self.SetCheckbox(self.m_restrictNet, self.m_selectedSettlement.RestrictNet() if self.m_selectedSettlement else None)
        self.SetCheckbox(self.m_isValueDayCheckIgnored, self.m_selectedSettlement.IsValueDayCheckIgnored() if self.m_selectedSettlement else None)
        self.SetField(self.m_acquirer, self.m_selectedSettlement.Acquirer() if self.m_selectedSettlement else None)
        self.SetField(self.m_acquirerAccount, self.m_selectedSettlement.AcquirerAccountRef() if self.m_selectedSettlement else None)

        self.SetField(self.m_externalCutoffTime, self.m_selectedSettlement.ExternalCutoffTimeInHHMM() if self.m_selectedSettlement else None)
        self.SetField(self.m_externalCutoffDay, self.m_selectedSettlement.ExternalCutoffDay() if self.m_selectedSettlement else None)
        self.SetField(self.m_internalCutoffTime, self.m_selectedSettlement.InternalCutoffTimeInHHMM() if self.m_selectedSettlement else None)
        self.SetField(self.m_internalCutoffDay, self.m_selectedSettlement.InternalCutoffDay() if self.m_selectedSettlement else None)
        self.SetField(self.m_counterparty, self.m_selectedSettlement.Counterparty() if self.m_selectedSettlement else None)
        self.SetField(self.m_counterpartyAccount, self.m_selectedSettlement.CounterpartyAccountRef() if self.m_selectedSettlement else None)

        if self.m_selectedSettlement:
            self.SetField(self.m_counterpartyAccountNumber, self.m_selectedSettlement.CounterpartyAccountRef().Account() if self.m_selectedSettlement.CounterpartyAccountRef() else '')
            self.SetField(self.m_theirCorrBankName, self.m_selectedSettlement.CounterpartyAccountRef().CorrespondentBank() if self.m_selectedSettlement.CounterpartyAccountRef() else None)
            self.SetField(self.m_theirCorrBankName2, self.m_selectedSettlement.CounterpartyAccountRef().CorrespondentBank2() if self.m_selectedSettlement.CounterpartyAccountRef() else None)
            self.SetField(self.m_acquirerAccountNumber, self.m_selectedSettlement.AcquirerAccountRef().Account() if self.m_selectedSettlement.AcquirerAccountRef() else '')
            self.SetField(self.m_corrBankName, self.m_selectedSettlement.AcquirerAccountRef().CorrespondentBank() if self.m_selectedSettlement.AcquirerAccountRef() else None)
            self.SetField(self.m_corrBankName2, self.m_selectedSettlement.AcquirerAccountRef().CorrespondentBank2() if self.m_selectedSettlement.AcquirerAccountRef() else None)
            self.SetField(self.m_createTime, acm.Time.DateTimeFromTime(self.m_selectedSettlement.CreateTime()))

        else:
            self.SetField(self.m_createTime, None)
            self.SetField(self.m_counterpartyAccountNumber, None)
            self.SetField(self.m_theirCorrBankName, None)
            self.SetField(self.m_theirCorrBankName2, None)
            self.SetField(self.m_acquirerAccountNumber, None)
            self.SetField(self.m_corrBankName, None)
            self.SetField(self.m_corrBankName2, None)
            
        self.m_statusExplanation.SetData(self.m_selectedSettlement.StatusExplanation(self.m_topRowSelected) if self.m_selectedSettlement else "")
        updateTable(self.m_adjustedSettlementList, self.m_settlements)
        updateTable(self.m_originalSettlementList, self.m_originalSettlements)
        self.m_updateValues = False

    #---------------------------------------------------------------------------
    def UpdateControls(self):
        self.SetEnabled(self.m_trade, 'Trade')
        self.SetEnabled(self.m_amount, 'Amount')
        self.SetEnabled(self.m_currency, 'Currency')
        self.SetEnabled(self.m_valueDay, 'ValueDay')
        self.SetEnabled(self.m_restrictNet, 'RestrictNet')
        self.SetEnabled(self.m_isValueDayCheckIgnored, 'IsValueDayCheckIgnored')
        self.SetEnabled(self.m_notificationDay, 'NotificationDay')
        self.SetEnabled(self.m_status, 'Status')
        self.SetEnabled(self.m_partialSettlementType, 'PartialSettlementType')
        self.SetEnabled(self.m_text, 'Text')
        self.SetEnabled(self.m_acquirer, 'Acquirer')
        self.SetEnabled(self.m_acquirerAccount, 'AcquirerAccountRef')
        self.SetEnabled(self.m_counterparty, 'Counterparty')
        self.SetEnabled(self.m_counterpartyAccount, 'CounterpartyAccountRef')
        self.SetEnabled(self.m_getFromHook, 'NotificationDay')

        self.m_oid.Enabled(False)
        self.m_createTime.Enabled(False)
        self.m_processStatus.Enabled(False)
        self.m_acquirerAccountNumber.Enabled(False)
        self.m_corrBankName.Enabled(False)
        self.m_corrBankName2.Enabled(False)
        self.m_externalCutoffTime.Enabled(False)
        self.m_externalCutoffDay.Enabled(False)
        self.m_internalCutoffTime.Enabled(False)
        self.m_internalCutoffDay.Enabled(False)
        self.m_counterpartyAccountNumber.Enabled(False)
        self.m_theirCorrBankName.Enabled(False)
        self.m_theirCorrBankName2.Enabled(False)
        self.m_statusExplanation.Enabled(False)
        self.m_save.Enabled(True)


    #---------------------------------------------------------------------------
    def DisableControls(self):
        self.m_oid.Enabled(False)
        self.m_trade.Enabled(False)
        self.m_currency.Enabled(False)
        self.m_amount.Enabled(False)
        self.m_valueDay.Enabled(False)
        self.m_createTime.Enabled(False)
        self.m_status.Enabled(False)
        self.m_notificationDay.Enabled(False)
        self.m_partialSettlementType.Enabled(False)
        self.m_text.Enabled(False)
        self.m_processStatus.Enabled(False)
        self.m_restrictNet.Enabled(False)
        self.m_isValueDayCheckIgnored.Enabled(False)
        self.m_acquirer.Enabled(False)
        self.m_acquirerAccount.Enabled(False)
        self.m_acquirerAccountNumber.Enabled(False)
        self.m_corrBankName.Enabled(False)
        self.m_corrBankName2.Enabled(False)
        self.m_externalCutoffTime.Enabled(False)
        self.m_externalCutoffDay.Enabled(False)
        self.m_internalCutoffTime.Enabled(False)
        self.m_internalCutoffDay.Enabled(False)
        self.m_counterparty.Enabled(False)
        self.m_counterpartyAccount.Enabled(False)
        self.m_counterpartyAccountNumber.Enabled(False)
        self.m_theirCorrBankName.Enabled(False)
        self.m_theirCorrBankName2.Enabled(False)
        self.m_getFromHook.Enabled(False)

    #---------------------------------------------------------------------------
    def HandleCreate( self, dlg, layout):
        self.m_fuxDlg = dlg
        self.m_fuxDlg.Caption(self.m_actionName)
        self.m_bindings.AddLayout(layout)

        self.m_restrictNet = layout.GetControl('restrictNetCtrl')
        self.m_isValueDayCheckIgnored = layout.GetControl('isValueDayCheckIgnoredCtrl')
        self.m_statusExplanation = layout.GetControl('statusExplanation')

        self.m_adjustedSettlementList = layout.GetControl('adjustedSettlements')
        createSettlementTable(self.m_adjustedSettlementList)
        for settlement in self.m_settlements:
            populateTable(self.m_adjustedSettlementList, settlement)
        self.m_adjustedSettlementList.SetSelectedItems([self.m_adjustedSettlementList.GetRootItem().FirstChild()])
        self.m_adjustedSettlementList.AddCallback('SelectionChanged', OnSelectionChangedAdjustedSettlements, self)

        self.m_originalSettlementList = layout.GetControl('originalSettlements')
        createSettlementTable(self.m_originalSettlementList)
        for settlement in self.m_originalSettlements:
            populateTable(self.m_originalSettlementList, settlement)
        self.m_originalSettlementList.AddCallback('SelectionChanged', OnSelectionChangedOriginalSettlements, self)

        self.m_getFromHook = layout.GetControl('getFromHookCtrl')
        self.m_getFromHook.Enabled(self.m_editableFields['NotificationDay'])
        self.m_getFromHook.AddCallback("Activate", OnHookButtonClicked, self)

        self.m_save = layout.GetControl('save')
        self.m_save.AddCallback("Activate", OnSaveClicked, self)

        self.UpdateControls()
        self.UpdateValues()

        #Normal stuff
        self.m_isValueDayCheckIgnored.AddCallback('Activate', OnUpdatedIsValueDayCheckIgnored, [self])
        self.m_restrictNet.AddCallback('Activate', OnUpdatedRestrictNet, [self])

    #---------------------------------------------------------------------------
    def InitControls(self):
        self.m_bindings = acm.FUxDataBindings()
        self.m_bindings.AddDependent( self )
        self.m_oid = self.m_bindings.AddBinder( 'oidCtrl', acm.GetDomain('int'), None )
        self.m_trade = self.m_bindings.AddBinder( 'tradeCtrl', acm.GetDomain('FTrade'), None )
        self.m_currency = self.m_bindings.AddBinder( 'currencyCtrl', acm.GetDomain('FCurrency'), None, self.m_currencyPopulator)
        self.m_amount = self.m_bindings.AddBinder( 'amountCtrl', acm.GetDomain('double'), None )
        self.m_valueDay = self.m_bindings.AddBinder( 'valueDayCtrl', acm.GetDomain('date'), None )
        self.m_createTime = self.m_bindings.AddBinder( 'createTimeCtrl', acm.GetDomain('string'), None )
        self.m_notificationDay = self.m_bindings.AddBinder( 'notificationDayCtrl', acm.GetDomain('date'), None )
        self.m_status = self.m_bindings.AddBinder( 'statsuCtrl', acm.GetDomain('enum(SettlementStatus)'), None, self.m_statusPopulator )
        self.m_partialSettlementType = self.m_bindings.AddBinder( 'partialSettlementTypeCtrl', acm.GetDomain('enum(PartialSettlementType)'), None, self.m_partialSettlementTypePopulator )
        self.m_text = self.m_bindings.AddBinder( 'textCtrl', acm.GetDomain('string'), None )
        self.m_acquirer = self.m_bindings.AddBinder( 'acquirerCtrl', acm.GetDomain('FInternalDepartment'), None, self.m_acquirerPopulator)
        self.m_acquirerAccount = self.m_bindings.AddBinder( 'acquirerAccountCtrl', acm.GetDomain('FAccount'), None, self.m_acquirerAccountRefPopulator)
        self.m_acquirerAccountNumber = self.m_bindings.AddBinder( 'acquirerAccountNumberCtrl', acm.GetDomain('string'), None )
        self.m_corrBankName = self.m_bindings.AddBinder( 'corrBankNameCtrl', acm.GetDomain('string'), None )
        self.m_corrBankName2 = self.m_bindings.AddBinder( 'corrBankName2Ctrl', acm.GetDomain('string'), None )
        self.m_processStatus = self.m_bindings.AddBinder( 'processStatus', acm.GetDomain('string'), None )
        self.m_externalCutoffTime = self.m_bindings.AddBinder( 'externalCutoffTimeCtrl', acm.GetDomain('string'), None )
        self.m_externalCutoffDay = self.m_bindings.AddBinder( 'externalCutoffDayCtrl', acm.GetDomain('string'), None )
        self.m_internalCutoffTime = self.m_bindings.AddBinder( 'internalCutoffTimeCtrl', acm.GetDomain('string'), None )
        self.m_internalCutoffDay = self.m_bindings.AddBinder( 'internalCutoffDayCtrl', acm.GetDomain('string'), None )
        self.m_counterparty = self.m_bindings.AddBinder( 'counterpartyCtrl', acm.GetDomain('FParty'), None, self.m_counterpartyPopulator)
        self.m_counterpartyAccount = self.m_bindings.AddBinder( 'counterpartyAccountCtrl', acm.GetDomain('FAccount'), None, self.m_counterpartyAccountRefPopulator)
        self.m_counterpartyAccountNumber = self.m_bindings.AddBinder( 'counterpartyAccountNumberCtrl', acm.GetDomain('string'), None )
        self.m_theirCorrBankName = self.m_bindings.AddBinder( 'theirCorrBankNameCtrl', acm.GetDomain('string'), None )
        self.m_theirCorrBankName2 = self.m_bindings.AddBinder( 'theirCorrBankName2Ctrl', acm.GetDomain('string'), None )

    #---------------------------------------------------------------------------
    def CreateLayout(self):
        b = acm.FUxLayoutBuilder()
        b.BeginVertBox('None')
        b.  BeginHorzBox('None')
        b.    BeginVertBox('Invisible', '')
        self.m_oid.BuildLayoutPart(b, 'Oid')
        self.m_trade.BuildLayoutPart(b, 'Trade')
        self.m_amount.BuildLayoutPart(b, 'Amount')
        self.m_currency.BuildLayoutPart(b, 'Currency')
        self.m_valueDay.BuildLayoutPart(b, 'Value Day')
        self.m_createTime.BuildLayoutPart(b, 'Create Time')
        b.      AddCheckbox('restrictNetCtrl', 'Restrict Net')
        b.      AddCheckbox('isValueDayCheckIgnoredCtrl', 'Value Day Check Ignored')
        b.      AddSpace(4)
        b.      BeginHorzBox()
        self.m_notificationDay.BuildLayoutPart(b, 'Notification Day')
        b.        AddButton('getFromHookCtrl', '&&Get From Hook')
        b.      EndBox()
        b.    EndBox()
        b.    BeginVertBox('Invisible', '')
        self.m_status.BuildLayoutPart(b, 'Status')
        self.m_partialSettlementType.BuildLayoutPart(b, 'Partial Type')
        self.m_text.BuildLayoutPart(b, 'Text')
        self.m_processStatus.BuildLayoutPart(b, 'Process Status')
        b.    AddSpace(4)
        b.    BeginHorzBox('Invisible', 'StatusExplanation')
        b.      AddText("statusExplanation", -1, -1, -1)
        b.    EndBox()
        b.    EndBox()
        b.  EndBox()
        b.  BeginHorzBox()
        b.    BeginVertBox('EtchedIn', 'Acquirer')
        self.m_acquirer.BuildLayoutPart(b, 'Name')
        self.m_acquirerAccount.BuildLayoutPart(b, 'Account')
        self.m_acquirerAccountNumber.BuildLayoutPart(b, 'Acc Number')
        b.      BeginHorzBox('EtchedIn', 'Our Corr Bank')
        b.        BeginHorzBox()
        self.m_corrBankName.BuildLayoutPart(b, '')
        self.m_corrBankName2.BuildLayoutPart(b, '')
        b.        EndBox()
        b.      EndBox()
        b.      BeginVertBox()
        b.        BeginHorzBox()
        self.m_externalCutoffTime.BuildLayoutPart(b, 'External Cut Off:')
        self.m_externalCutoffDay.BuildLayoutPart(b, '')
        b.        EndBox()
        b.        BeginHorzBox()
        self.m_internalCutoffTime.BuildLayoutPart(b, 'Internal Cut Off:')
        self.m_internalCutoffDay.BuildLayoutPart(b, '')
        b.        EndBox()
        b.      EndBox()
        b.    EndBox()
        b.    BeginVertBox('EtchedIn', 'Counterparty')
        self.m_counterparty.BuildLayoutPart(b, 'Name')
        self.m_counterpartyAccount.BuildLayoutPart(b, 'Account')
        self.m_counterpartyAccountNumber.BuildLayoutPart(b, 'Acc Number')
        b.      BeginHorzBox('EtchedIn', 'Their Corr Bank')
        b.        BeginHorzBox()
        self.m_theirCorrBankName.BuildLayoutPart(b, '')
        self.m_theirCorrBankName2.BuildLayoutPart(b, '')
        b.        EndBox()
        b.      EndBox()
        b.    EndBox()
        b.  EndBox()
        b.  BeginVertBox('EtchedIn', 'Adjusted Settlements')
        b.    AddList('adjustedSettlements', 5)
        b.  EndBox()
        b.  BeginVertBox('EtchedIn', 'Original Settlements')
        b.    AddList('originalSettlements', 5)
        b.  EndBox()
        b.  BeginHorzBox()
        b.    AddFill()
        b.    AddButton('save', '&&Save')
        b.    AddButton('cancel', 'C&&ancel')
        b.  EndBox()
        b.EndBox()
        return b

#---------------------------------------------------------------------------
# GUI Callbacks
#---------------------------------------------------------------------------
#---------------------------------------------------------------------------
def ErrorDialogDecorator(f):
    def wrapper(*args):
        self = args[0][0]
        try:
            f(*args)
        except RuntimeError as e:
            acm.UX().Dialogs().MessageBoxOKCancel(self.m_fuxDlg.Shell(), 'Error', str(e))
        self.UpdateValues()
    return wrapper

#---------------------------------------------------------------------------
@ErrorDialogDecorator
def OnUpdatedRestrictNet(callbackData, cd):
    dialog = callbackData[0]
    if not dialog.m_selectedSettlement:
        return
        
    if dialog.m_selectedSettlement.RestrictNet() != dialog.m_restrictNet.Checked():
        dialog.m_selectedSettlement.RestrictNet(dialog.m_restrictNet.Checked())

#---------------------------------------------------------------------------
@ErrorDialogDecorator
def OnUpdatedIsValueDayCheckIgnored(callbackData, cd):
    dialog = callbackData[0]
    if not dialog.m_selectedSettlement:
        return
        
    if dialog.m_selectedSettlement.IsValueDayCheckIgnored() != dialog.m_isValueDayCheckIgnored.Checked():
        dialog.m_selectedSettlement.IsValueDayCheckIgnored(dialog.m_isValueDayCheckIgnored.Checked())

#---------------------------------------------------------------------------
def OnSelectionChangedAdjustedSettlements(self, cd):
    SelectionChangedInList(self, cd, True, self.m_adjustedSettlementList, self.m_originalSettlementList)

#---------------------------------------------------------------------------
def OnSelectionChangedOriginalSettlements(self, cd):  
    SelectionChangedInList(self, cd, False, self.m_originalSettlementList, self.m_adjustedSettlementList)

def SelectionChangedInList(self, cd, topRowSelected, selectedList, notSelectedList):
    if(self.m_adjustedSettlementList.SelectedCount() == 0) and (self.m_originalSettlementList.SelectedCount() == 0):
        #Wen no row is selected
        self.m_selectedSettlement = None
        self.UpdateControls()
        self.UpdateValues()
        self.DisableControls()
    elif(selectedList.SelectedCount() == 0):
        #When no row is selected on this controller
        pass
    else:
        #When a row is selected
        self.m_topRowSelected = topRowSelected
        self.m_selectedSettlement = selectedList.GetSelectedItem().GetData()
        self.UpdateValues()
        if topRowSelected:
            self.UpdateControls()
        else:
            self.DisableControls()
        notSelectedList.SelectAllItems(False)

#---------------------------------------------------------------------------
def OnHookButtonClicked(self, cd):
    self.m_selectedSettlement.NotificationDayFromHook()
    self.UpdateValues()

#---------------------------------------------------------------------------
def OnSaveClicked(self, cd):
    self.m_fuxDlg.CloseDialogOK()

#---------------------------------------------------------------------------
# Helper functions
#---------------------------------------------------------------------------

#---------------------------------------------------------------------------
def createSettlementTable(table):
    table.ShowColumnHeaders()
    table.AddColumn("ID")
    table.AddColumn("Amount")
    table.AddColumn("Currency")
    table.AddColumn("Value Day")
    table.AddColumn("Status")
    table.AddColumn("Acquirer")
    table.AddColumn("Counterparty")
    table.AddColumn("To Portfolio")
    table.AddColumn("From Portfolio")

#---------------------------------------------------------------------------
def populateTable(table, object):
    root = table.GetRootItem()
    child = root.AddChild()
    formatter = acm.FNumFormatter('').Clone()
    child.Label(object.Oid(), 0)
    child.Label(formatter.Format(object.Amount()), 1)
    child.Label(object.Currency(), 2)
    child.Label(object.ValueDay(), 3)
    child.Label(object.Status(), 4)
    child.Label(object.Acquirer(), 5)
    child.Label(object.Counterparty(), 6)
    child.Label(object.ToPortfolio(), 7)
    child.Label(object.FromPortfolio(), 8)
    child.SetData(object)
    table.AdjustColumnWidthToFitItems(0)
    table.AdjustColumnWidthToFitItems(1)
    table.AdjustColumnWidthToFitItems(2)
    table.AdjustColumnWidthToFitItems(3)
    table.AdjustColumnWidthToFitItems(4)
    table.AdjustColumnWidthToFitItems(5)
    table.AdjustColumnWidthToFitItems(6)
    table.AdjustColumnWidthToFitItems(7)
    table.AdjustColumnWidthToFitItems(8)

#---------------------------------------------------------------------------
def updateTable(table, objects):
    i = 0
    for child in table.GetRootItem().Children():
        formatter = acm.FNumFormatter('').Clone()
        object = objects.At(i)
        child.Label(object.Oid(), 0)
        child.Label(formatter.Format(object.Amount()), 1)
        child.Label(object.Currency(), 2)
        child.Label(object.ValueDay(), 3)
        child.Label(object.Status(), 4)
        child.Label(object.Acquirer(), 5)
        child.Label(object.Counterparty(), 6)
        child.Label(object.ToPortfolio(), 7)
        child.Label(object.FromPortfolio(), 8)
        child.SetData(object)
        table.AdjustColumnWidthToFitItems(0)
        table.AdjustColumnWidthToFitItems(1)
        table.AdjustColumnWidthToFitItems(2)
        table.AdjustColumnWidthToFitItems(3)
        table.AdjustColumnWidthToFitItems(4)
        table.AdjustColumnWidthToFitItems(5)
        table.AdjustColumnWidthToFitItems(6)
        table.AdjustColumnWidthToFitItems(7)
        table.AdjustColumnWidthToFitItems(8)
        i = i + 1

#---------------------------------------------------------------------------
def GetPopUpQuestions(questions, exceptionQuestionId, diaryQuestionId):
    exceptionQuestion = None
    diaryQuestion = None

    for question in questions:

        if question.QuestionId() == exceptionQuestionId:
            exceptionQuestion = question

        if question.QuestionId() == diaryQuestionId:
            diaryQuestion = question

    return exceptionQuestion, diaryQuestion

#---------------------------------------------------------------------------
def StartDialogWithShell(args):
    shell = args['shell']
    command = args['command']
    name = args['name']
    customDlg = SettlementActionDialog(command, name)
    customDlg.InitControls()
    return acm.UX().Dialogs().ShowCustomDialogModal(shell, customDlg.CreateLayout(), customDlg )
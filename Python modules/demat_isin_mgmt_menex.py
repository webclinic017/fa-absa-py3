"""
HISTORY
==============================================================================================================
Date        Change no       Developer           Description
--------------------------------------------------------------------------------------------------------------
2017-12-11  CHNG0005220511  Manan Ghosh         DIS go-live
2019-11-07  FAOPS-641       Stuart Wilson       Clean up and added check for acquirer and issuer BPID to be
                                                equal for demat position to change
2020-07-27  FAOPS-780       Ntokozo Skosana     Minor refactor to dis_issued_amount function
2020-12-11  FAOPS-968       Metse Moshobane     Modified dis_issued_amount function
"""

import acm
import FUxCore
import demat_swift_mt598
from decimal import *
from logging import getLogger


LOGGER = getLogger(__name__)
MMSS_ISIN_REQUEST_STATE_CHART_NAME = 'MM ISIN Management'
DIS_ISIN_REQUEST_STATE_CHART_NAME = 'DIS ISIN Management'
TRILLION = 1000000000000
NEW_ISIN_REQUEST_PENDING = 'New ISIN Request Pending'


def get_party_demat_BPID(party):
    for alias in party.Aliases():
        if alias.Type():
            if alias.Type().Name() == 'MM_DEMAT_Issuer_BPID':
                return alias.Alias()


def is_active(subject):
    """
    This indicates if the Instrument is in Business Process and the Current State is 'Ready'
    """
    processes = acm.BusinessProcess.FindBySubjectAndStateChart(subject, MMSS_ISIN_REQUEST_STATE_CHART_NAME)
    if len(processes) > 0:
        process = processes[0]
        cs = process.CurrentStep()
        return True, (cs.State().Name() == 'Ready')
    else:
        return False, False


def get_business_process(subject_name, process_name):
    bp = None
    if subject_name:
        ins = acm.FInstrument.Select01("name = '{name}' ".format(name=subject_name), "")
        bp = acm.FBusinessProcess.Select01("subject_seqnbr = {oid} and stateChart='{state_chart_name}' "
                                           .format(oid=ins.Oid(), state_chart_name=process_name), "")
    return bp


def dis_initial_amount(subject):
    """
    This sums all "Amount" fields on "Active" steps. If Amount is not available on Active step
    Note will be parsed as a "Manual Adjustment to Auth Amount"
    """
    if subject.AdditionalInfo().DIS_Instrument():
        processes = acm.BusinessProcess.FindBySubjectAndStateChart(subject, DIS_ISIN_REQUEST_STATE_CHART_NAME)
    else:
        processes = acm.BusinessProcess.FindBySubjectAndStateChart(subject, MMSS_ISIN_REQUEST_STATE_CHART_NAME)

    if processes and len(processes) > 0:
        process = processes[0]
        safety_cnt = 0
        auth_amount = 0.0
        cs = process.CurrentStep()
        while cs and safety_cnt < 100:

            if cs.State().Name() == 'Ready':
                break
            elif cs.State().Name() == NEW_ISIN_REQUEST_PENDING:
                try:
                    auth_amount += float(cs.DiaryEntry().Parameters()['Initial Amount'])
                except:
                    try:
                        auth_amount += float(cs.DiaryEntry().Notes()[0])
                    except Exception:
                        LOGGER.exception('No valid note found to use as manual adjustment to Authorised Amount')
            cs = cs.PreviousStep()
        return auth_amount
    else:
        LOGGER.warning('Instrument not in Business Process')
        return None


def current_authorised_amount(subject):
    """
    This sums all "Amount" fields on "Active" steps. If Amount is not available on Active step,
    Note will be parsed as a "Manual Adjustment to Auth Amount"
    """
    processes = None
    if subject.AdditionalInfo().DIS_Instrument():
        processes = acm.BusinessProcess.FindBySubjectAndStateChart(subject, DIS_ISIN_REQUEST_STATE_CHART_NAME)
    else:
        processes = acm.BusinessProcess.FindBySubjectAndStateChart(subject, MMSS_ISIN_REQUEST_STATE_CHART_NAME)

    if processes and len(processes) > 0:
        process = processes[0]
        safety_cnt = 0
        auth_amount = 0.0
        cs = process.CurrentStep()
        while cs and safety_cnt < 100:
            if cs.State().Name() == 'Ready':
                break
            elif cs.State().Name() in ['Active', 'DeIssued'] and cs.PreviousStep().State().Name() != 'Error':
                try:
                    if cs.DiaryEntry().Parameters()['Amount'] is not None:
                        auth_amount += float(cs.DiaryEntry().Parameters()['Amount'] )
                    elif cs.DiaryEntry().Notes()[0] is not None:
                        auth_amount += float(cs.DiaryEntry().Notes()[0])
                    else:
                        auth_amount += 0.0
                except:
                    LOGGER.exception('No valid note found to use as manual adjustment to Authorised Amount')
            cs = cs.PreviousStep()
        return auth_amount
    else:
        LOGGER.warning('Instrument not in Business Process')
        return None


def dis_issued_amount(subject, excludeTrade=None):
    """
    This gets the difference between auth amount and all Nominal amounts on non (Void/terminated/Simulated) trades on the subject
    """
    if subject is None:
        return 0

    trades = acm.FTrade.Select("instrument = '{name}'".format(name=subject.Name()))
    issued = 0.0

    for trades in trades:
        if _qualifying_trade(subject, trades, excludeTrade):
            issued += -trades.Nominal()
    return issued


def _qualifying_trade(instrument, trade, exclude_trade):
    acquirer = _get_acquirer_from_trade(trade)
    issuer = _get_issuer_from_ins(instrument)
    settlement_category = _get_dis_settlecategory(trade)

    if trade.Oid() == exclude_trade:
        return False
    if trade.Status() != "BO-BO Confirmed":
        return False
    if not trade.Instrument().AdditionalInfo().DIS_Instrument():
        return False
    if settlement_category != 'DIS':
        return False
    if acquirer == issuer:
        return True
    if _struct_note_desk_trade(trade):
        return True
    return False


def _struct_note_desk_trade(trade):
    acquirer = _get_acquirer_from_trade(trade)
    issuer = _get_instrument_issuer_from_trade(trade)
    if not acquirer == 'STRUCT NOTES DESK':
        return False
    if not issuer == 'ABSA BANK LTD':
        return False
    return True

def _get_dis_settlecategory(trade):
    instrument = trade.Instrument()
    if instrument is None:
        return None
    settle_cat = trade.Instrument().SettleCategoryChlItem()
    if settle_cat is None:
        return None
    return settle_cat.Name()

def _get_acquirer_from_trade(trade):

    if trade.Acquirer() is None:
        return None
    return trade.Acquirer().Name()


def _get_instrument_issuer_from_trade(trade):
    instrument = trade.Instrument()
    if instrument is None:
        return None
    if instrument.Issuer() is None:
        return None
    return instrument.Issuer().Name()


def _get_issuer_from_ins(instrument):

    if instrument.Issuer() is None:
        return None
    return instrument.Issuer().Name()


def dis_authorised_amount(subject):
    """
    This sums all "Amount" fields on "Active" steps. If Amount is not available on Active step,
    Note will be parsed as a "Manual Adjustment to Auth Amount"
    """
    process = get_business_process(subject.Name(), DIS_ISIN_REQUEST_STATE_CHART_NAME)
    if process:
        safety_cnt = 0
        auth_amount = 0
        cs = process.CurrentStep()
        while cs is not None and safety_cnt < 100:
            if cs.State().Name() == 'Ready':
                break
            elif cs.State().Name() == 'Active' and cs.PreviousStep().State().Name() != 'Error':
                try:
                    auth_amount += float(cs.DiaryEntry().Parameters()['Amount'])
                except:
                    try:
                        auth_amount += float(cs.DiaryEntry().Notes()[0])
                    except Exception:
                        LOGGER.exception('No valid note found to use as manual adjustment to Authorised Amount')

            cs = cs.PreviousStep()
        return auth_amount
    else:
        LOGGER.warning('Instrument not in Business Process')
        return 0


def dis_unissued_amount(subject):
    """
    This unissued amount is the amount of (Authrosied Amount) - (Issued Amount)
    """
    auth_amount = dis_authorised_amount(subject)
    issued_amount = dis_issued_amount(subject)
    unissued_amount = auth_amount - issued_amount

    return unissued_amount


def demat_issued_amount(subject):
    """
    This gets the difference between auth amount and all Nominal amounts on non (Void/terminated/Simulated) trades on the subject
    """
    if subject:
        issuer_BPID = get_party_demat_BPID(subject.Issuer())
        trades = acm.FTrade.Select("instrument = '{name}'".format(name=subject.Name()))
        invalid_status = ['Simulated', 'Void', 'Terminated']
        issued = 0.0
        acquirer_BPID = None
        for t in trades:
            if t.Acquirer():
                acquirer_BPID = get_party_demat_BPID(t.Acquirer())
            if t.Status() not in invalid_status and issuer_BPID == acquirer_BPID:
                issued += -t.Nominal()
        return issued
    else:
        return 0


def demat_available_amount(subject, return_all=False):
    """
    This gets the difference between auth amount and all
    Nominal amounts on non (Void/terminated/Simulated) trades on the subject
    """
    auth = demat_authorised_amount(subject)
    issued = demat_issued_amount(subject)
    available = auth - issued
    if return_all:
        return available, auth, issued
    else:
        return available


def demat_authorised_amount(subject):
    """
    This sums all "Amount" fields on "Active" steps. If Amount is not available on Active step,
    Note will be parsed as a "Manual Adjustment to Auth Amount"
    """
    process = get_business_process(subject.Name(), MMSS_ISIN_REQUEST_STATE_CHART_NAME)
    if process:
        safety_cnt = 0
        auth_amount = 0
        cs = process.CurrentStep()
        while cs and safety_cnt < 100:
            if cs.State().Name() == 'Ready':
                break
            elif cs.State().Name() == 'Active' and cs.PreviousStep().State().Name() != 'Error':
                try:
                    auth_amount += float(cs.DiaryEntry().Parameters()['Amount'])
                except:
                    try:
                        auth_amount += float(cs.DiaryEntry().Notes()[0])
                    except Exception:
                        LOGGER.exception('valid note found to use as manual adjustment to Authorised Amount')

            cs = cs.PreviousStep()
        return auth_amount
    else:
        LOGGER.warning('Instrument not in Business Process')
        return 0


def current_ins_authorised_amount(subject):
    """
    This gets the Nominal amounts on non (Void/terminated/Simulated) trades on the subject
    """
    if subject:
        if subject.AdditionalInfo().DIS_Instrument():
            return dis_authorised_amount(subject)
        elif subject.AdditionalInfo().Demat_Instrument():
            return current_authorised_amount(subject)


def current_ins_issued_amount(subject, excludeTrade=None):
    """
    This gets the Nominal amounts on non (Void/terminated/Simulated) trades on the subject
    """
    if subject:
        if subject.AdditionalInfo().DIS_Instrument():
            return dis_issued_amount(subject, excludeTrade)
        elif subject.AdditionalInfo().Demat_Instrument():
            return current_issued_amount(subject)


def current_ins_available_amount(subject, excludeTrade=None):
    """
    This gets the Nominal amounts on non (Void/terminated/Simulated) trades on the subject
    """
    if subject:
        return current_ins_authorised_amount(subject) - current_ins_issued_amount(subject, excludeTrade)

    return 0.0


def current_ins_amount(subject):
    """
    This gets the available, issued and available amount for instruments
    """
    avail_amount = current_ins_available_amount(subject)
    auth_amount = current_ins_authorised_amount(subject)
    issued_amount = current_ins_issued_amount(subject)
    return avail_amount, auth_amount, issued_amount


def current_issued_amount(subject):
    """
    This gets the Nominal amounts on non (Void/terminated/Simulated) trades on the subject
    """
    if subject.AdditionalInfo().DIS_Instrument():
        return
    trades = subject.Trades()
    issued = 0.0
    issuer_BPID = get_party_demat_BPID(subject.Issuer())
    acquirer_BPID = None
    for t in trades:
        if t.Acquirer():
            acquirer_BPID = get_party_demat_BPID(t.Acquirer())

        if t.Status() == 'BO-BO Confirmed' and issuer_BPID == acquirer_BPID:
            issued += -t.Nominal()
    return issued


def current_available_amount(subject, return_all=False):
    """
    This gets the difference between auth amount and all Nominal amounts on non (Void/terminated/Simulated) trades on the subject
    """
    auth = current_authorised_amount(subject)
    issued = current_issued_amount(subject)
    if not auth:
        available = issued
    else:
        available = auth - issued
    if return_all:
        return available, auth, issued
    else:
        return available


def dis_capital_event(sett):
    return (sett.Payment() and sett.Payment().Text()) or (sett.CashFlow()
                                                          and sett.CashFlow().AdditionalInfo().Demat_CE_Reference())


def create_business_process(subject, state_chart):
    return acm.BusinessProcess.InitializeProcess(subject, state_chart)


def apply_shortcode_to_amount(amount_str):
    amount_str = amount_str.replace(' ', '').lower()
    if 'b' in amount_str:
        amount_str = amount_str.replace('b', '').replace('m', '').replace('k', '')
        result = float(amount_str)*1000000000
    elif 'm' in amount_str:
        amount_str = amount_str.replace('b', '').replace('m', '').replace('k', '')
        result = float(amount_str)*1000000
    elif 'k' in amount_str:
        amount_str = amount_str.replace('b', '').replace('m', '').replace('k', '')
        result = float(amount_str)*1000
    else:
        result = float(amount_str)
    return result


class LogDialog(FUxCore.LayoutDialog):

    def __init__(self, logtext):
        self.text = logtext
        self.log = logtext.Text()
        self.logs = self.log.split('\n')
        self.logEntries = 0

    def HandleApply(self):
        return 1

    def HandleDestroy(self):
        return None

    def HandleCreate(self, dlg, layout):
        self.fuxDlg = dlg
        self.fuxDlg.Caption('Incoming ISIN Process Log')
        self.heading = layout.GetControl('headingLabel')
        self.heading.SetAlignment('Left')

    def CreateLayout(self):

        b = acm.FUxLayoutBuilder()
        b.BeginVertBox('None')
        b. BeginHorzBox('None')
        b.  AddFill()
        b.  AddLabel('headingLabel', 'THE FOLLOWING ISIN MESSAGES WERE NOT PROCESSED')
        b.  AddFill()
        b.  AddFill()
        b.  AddFill()
        b. EndBox()
        self.logEntries = 0
        b.BeginHorzBox('None')

        for log in self.logs:
            b.AddLabel('logEntry' + self.logEntries, 5*' ' + log)
        b.EndBox()
        b.EndBox()

        return b


def show_process_log(eii):
    shell = eii.ExtensionObject().Shell()
    textObj = acm.FCustomTextObject['SWIFT_MESSAGES']
    customDlg = LogDialog(textObj)
    acm.UX().Dialogs().ShowCustomDialogModal(shell, customDlg.CreateLayout(), customDlg)


class RequestDialog(FUxCore.LayoutDialog):
    def __init__(self, ins):
        self.ins = ins
        self.binder = None
        self.instrumentCtrl = None
        self.currentState = None
        self.dialog_func = acm.GetFunction('msgBox', 3)
        self.isDebtIns = ins.AdditionalInfo().DIS_Instrument()
        self.stateChart = self.isDebtIns and DIS_ISIN_REQUEST_STATE_CHART_NAME or MMSS_ISIN_REQUEST_STATE_CHART_NAME

        self.process = acm.BusinessProcess.FindBySubjectAndStateChart(ins, acm.FStateChart[self.stateChart])
        if len(self.process) > 0:
            self.currentState = self.process[0].CurrentStep().State().Name()

    def _get_amount(self):
        return apply_shortcode_to_amount(str(self.reqNewISINAmount.GetData()))

    def _get_request_amount(self):
        return apply_shortcode_to_amount(str(self.requestAmount.GetData()))

    def check_amount_below_trillion(self, amount):
        if amount >= TRILLION:
            message = 'Amount cannot exceed R 1 trillion\nPlease see log for details'
            LOGGER.warning('Amount cannot exceed R 1 trillion')
            LOGGER.warning('Please fix and re-request')
            self.dialog_func('Failure', message, 0)
            return False
        return True

    def check_amount_below_trillion_for_topup(self, amount):
        if amount >= TRILLION:
            message = 'Requested amount too large\nPlease see log for details'
            LOGGER.warning('The requested amount will result in an authorised amount larger than one trillion')
            LOGGER.warning('Please fix and re-request')
            self.dialog_func('Failure', message, 0)
            return False
        return True

    def check_amount_greater_than_zero_for_topup(self, amount):
        if amount <= 0:
            message = 'The requested reduction amount is equal/larger than available amount\nPlease see log for details'
            LOGGER.warning('The requested reduction amount is larger than available amount')
            LOGGER.warning('Please fix and re-request')
            self.dialog_func('Failure', message, 0)
            return False
        return True

    def check_min_tradable_denomination(self, amount):
        if Decimal(str(abs(amount))) % Decimal(str(self.ins.AdditionalInfo().Demat_MinTrdDeno())) != 0:
            message = 'Required amount is not a multiple of Min Tradable denomination\nPlease see log for details'
            LOGGER.warning('Required amount is not a multiple of Min Tradable denomination')
            LOGGER.warning('Please fix and re-request')
            self.dialog_func('Failure', message, 0)
            return False
        return True

    def check_amount_greater_than_zero(self, amount):
        if amount <= 0:
            message = 'New ISIN amount must be greater than zero\nPlease see log for details'
            LOGGER.warning('New ISIN amount must be greater than zero')
            LOGGER.warning('Please fix and re-request')
            self.dialog_func('Failure', message, 0)
            return False
        return True

    def failed_amount_checks(self, amount):
        if not self.check_amount_below_trillion(amount):
            return True
        if not self.check_min_tradable_denomination(amount):
            return True
        if not self.check_amount_greater_than_zero(amount):
            return True
        return False

    def failed_amount_checks_for_topup(self, amount):
        if not self.check_amount_below_trillion(amount):
            return True
        if not self.check_min_tradable_denomination(amount):
            return True
        if not self.check_amount_below_trillion_for_topup(amount + current_ins_authorised_amount(self.ins)):
            return True
        if not self.check_amount_greater_than_zero_for_topup(current_ins_available_amount(self.ins) + amount):
            return True
        return False

    def _manual_new_isin_insert(self, *other):
        sc = acm.FStateChart[self.stateChart]
        dialog_func = acm.GetFunction('msgBox', 3)
        bp_process = acm.BusinessProcess.FindBySubjectAndStateChart(self.ins, sc)
        if len(bp_process) == 0:
            bp = create_business_process(self.ins, sc)
        else:
            bp = bp_process[0]
        try:
            amount = self._get_amount()
            if self.failed_amount_checks(amount):
                return

            bp.ForceToState('Active', str(amount))
            bp.Commit()
            message = 'New ISIN request was manually inserted\ninto ISIN Management'
            dialog_func('Success', message, 0)
            self.fuxDlg.CloseDialogOK()
        except Exception:
            message = 'Could not do manual insertion new ISIN\nPlease see log for details'
            LOGGER.exception('Please fix and retry')
            dialog_func('Failure', message, 0)
            return

    def _resend_new_isin_request(self, *other):
        dialog_func = acm.GetFunction('msgBox', 3)
        try:
            amount = self._get_amount()
            if self.failed_amount_checks(amount):
                return

            paramDict = {'Initial Amount': amount}
            isin_resend_event = acm.FStateChartEvent('Resend')
            self.process[0].HandleEvent(isin_resend_event, params = paramDict)
            self.process[0].Commit()
            message = 'New ISIN request was resent'
            dialog_func('Success', message, 0)
            self.fuxDlg.CloseDialogOK()
        except Exception:
            message = 'Could not resend new ISIN\nPlease see log for details'
            LOGGER.exception('Please fix and re-request')
            dialog_func('Failure', message, 0)
            return

    def _create_bp(self, *other):

        if self.isDebtIns:
            sc = acm.FStateChart[DIS_ISIN_REQUEST_STATE_CHART_NAME]
            isin_request_event = acm.FStateChartEvent('Await ISIN')
        else:
            sc = acm.FStateChart[MMSS_ISIN_REQUEST_STATE_CHART_NAME]
            isin_request_event = acm.FStateChartEvent('Request ISIN')

        try:
            bp = create_business_process(self.ins, sc)
            message = 'Instrument has been inserted into the\nISIN Management Business Process'
            try:
                amount = self._get_amount()
                if self.failed_amount_checks(amount):
                    return

                paramDict = {'Initial Amount': amount}
            except:
                message = 'Could not request ISIN\nPlease see log for details'
                LOGGER.exception('Exception while creating business process for instrument')
                self.dialog_func('Failure', message, 0)
                return

            if bp.CanHandleEvent(isin_request_event, params = paramDict):
                bp.HandleEvent(isin_request_event, params = paramDict)
                bp.Commit()
                LOGGER.info('New ISIN to be requested')
                self.dialog_func('Success', message, 0)
                self.fuxDlg.CloseDialogOK()
            else:
                LOGGER.warning('Instrument has been inserted into the\nISIN Management Business Process BUT could not be transitioned to New ISIN request to be sent')

        except Exception:
            message = 'Could not create Business Process\nPlease see log for more details\n'
            LOGGER.exception(message)
            self.dialog_func('Failure', message, 0)

    def _resend_topupReduceRequest(self, *other):
        topupReduce_request_event = acm.FStateChartEvent('Resend')
        try:
            amount = self._get_request_amount()
            if self.failed_amount_checks_for_topup(amount):
                return
            paramDict = {'Amend Amount': amount}
        except Exception:
            message = 'Could not request Topup/Reduce\nPlease see log for details'
            LOGGER.exception(message)
            self.dialog_func('Failure', message, 0)
            return

        if self.process[0].CanHandleEvent(topupReduce_request_event, params = paramDict):
            self.process[0].HandleEvent(topupReduce_request_event, params = paramDict)
            self.process[0].Commit()
            message = 'Topup / Reduce to be requested'
            self.dialog_func('Success', message, 0)
            self.fuxDlg.CloseDialogOK()

    def _cancel_topupReduceRequest(self, *other):
        cancel_event = acm.FStateChartEvent('Cancel')

        paramDict = {'Amount': 0.0}

        if self.process[0].CanHandleEvent(cancel_event, params = paramDict):
            self.process[0].HandleEvent(cancel_event, params = paramDict)
            self.process[0].Commit()
            message = 'Topup / Reduce Request Cancelled'
            self.dialog_func('Success', message, 0)
            self.fuxDlg.CloseDialogOK()

    def _topupReduceRequest(self, *other):
        topupReduce_request_event = acm.FStateChartEvent('Request Topup or Reduce')
        try:
            amount = self._get_request_amount()
            if self.failed_amount_checks_for_topup(amount):
                return
            paramDict = {'Amend Amount': amount}
        except Exception, e:
            message = 'Could not request Topup/Reduce\nPlease see log for details'
            print message, e
            self.dialog_func('Failure', message, 0)
            return

        if self.process[0].CanHandleEvent(topupReduce_request_event, params=paramDict):
            self.process[0].HandleEvent(topupReduce_request_event, params=paramDict)
            self.process[0].Commit()
            message = 'Topup / Reduce to be requested'
            self.dialog_func('Success', message, 0)
            self.fuxDlg.CloseDialogOK()

    def _resend_deissueRequest(self, *other):
        resend_request_event = acm.FStateChartEvent('Resend')
        self.process[0].HandleEvent(resend_request_event)
        self.process[0].Commit()
        message = 'Deissue to be requested'
        self.dialog_func('Success', message, 0)
        self.fuxDlg.CloseDialogOK()

    def _cancel_deissueRequest(self, *other):
        cancel_event = acm.FStateChartEvent('Cancel')
        dialog_func = acm.GetFunction('msgBox', 3)

        paramDict = {'Amount': 0.0}

        if self.process[0].CanHandleEvent(cancel_event, params=paramDict):
            self.process[0].HandleEvent(cancel_event, params=paramDict)
            self.process[0].Commit()
            message = 'Deissue Request Cancelled'
            dialog_func('Success', message, 0)
            self.fuxDlg.CloseDialogOK()

    def _deissueRequest(self, *other):
        topupReduce_request_event = acm.FStateChartEvent('Request Deissue')
        self.process[0].HandleEvent(topupReduce_request_event)
        self.process[0].Commit()
        message = 'Deissue to be requested'
        self.dialog_func('Success', message, 0)
        self.fuxDlg.CloseDialogOK()

    def HandleApply(self):
        return 1

    def HandleDestroy(self):
        return None

    def HandleCreate(self, dlg, layout):
        self.fuxDlg = dlg
        self.fuxDlg.Caption('ISIN Management Dialog')

        self.reqNewISIN = layout.GetControl('reqNewISIN')
        self.resendNewISIN = layout.GetControl('resendNewISIN')
        self.manualNewISIN = layout.GetControl('manualNewISIN')
        self.reqNewISINAmount = layout.GetControl('initialAmount')
        self.reqTopupReduce = layout.GetControl('reqTopupReduce')
        self.resendTopupReduce = layout.GetControl('resendTopupReduce')
        self.cancelTopupReduce = layout.GetControl('cancelTopupReduce')
        self.requestAmount = layout.GetControl('requestAmount')
        self.reqDeissue = layout.GetControl('reqDeissue')
        self.resendDeissue = layout.GetControl('resendDeissue')
        self.cancelDeissue = layout.GetControl('cancelDeissue')
        self.authAmount = layout.GetControl('authAmount')
        self.issuedAmount = layout.GetControl('issuedAmount')
        self.availAmount = layout.GetControl('availAmount')
        self.currentStateLabelVal = layout.GetControl('currentStateLabelVal')

        self.reqNewISIN.Editable(False)
        self.resendNewISIN.Editable(False)
        self.manualNewISIN.Editable(False)
        self.reqNewISINAmount.Editable(False)
        self.reqTopupReduce.Editable(False)
        self.resendTopupReduce.Editable(False)
        self.cancelTopupReduce.Editable(False)
        self.requestAmount.Editable(False)
        self.reqDeissue.Editable(False)
        self.resendDeissue.Editable(False)
        self.cancelDeissue.Editable(False)

        self.authAmount.Editable(True)
        self.issuedAmount.Editable(True)
        self.currentStateLabelVal.Editable(True)
        self.availAmount.Editable(True)

        self.reqNewISIN.Visible(False)
        self.resendNewISIN.Visible(False)
        self.manualNewISIN.Visible(False)
        self.reqNewISINAmount.Visible(False)
        self.reqTopupReduce.Visible(False)
        self.resendTopupReduce.Visible(False)
        self.cancelTopupReduce.Visible(False)
        self.requestAmount.Visible(False)
        self.reqDeissue.Visible(False)
        self.resendDeissue.Visible(False)
        self.cancelDeissue.Visible(False)

        self.reqNewISIN.AddCallback("Activate", self._create_bp, None)
        self.resendNewISIN.AddCallback("Activate", self._resend_new_isin_request, None)
        self.manualNewISIN.AddCallback("Activate", self._manual_new_isin_insert, None)
        self.reqTopupReduce.AddCallback("Activate", self._topupReduceRequest, None)
        self.resendTopupReduce.AddCallback("Activate", self._resend_topupReduceRequest, None)
        self.cancelTopupReduce.AddCallback("Activate", self._cancel_topupReduceRequest, None)
        self.reqDeissue.AddCallback("Activate", self._deissueRequest, None)
        self.resendDeissue.AddCallback("Activate", self._resend_deissueRequest, None)
        self.cancelDeissue.AddCallback("Activate", self._cancel_deissueRequest, None)

        if self.currentState is None:
            self.display_state_none()

        elif self.currentState == 'Active':
           self.display_state_active()

        elif self.currentState == 'New ISIN Failed Response':
            self.display_state_new_ISIN_Failed()

        elif self.currentState == 'Topup Reduce Failed Response':
            self.display_state_topup_reduced_failed()

        elif self.currentState == 'Deissue Failed Response':
            self.display_state_deissue_failed()

        elif self.currentState == 'New ISIN Request Pending':
            self.display_state_pending_new_ISIN_request()

        if self.currentState:
            self.currentStateLabelVal.Label(self.currentState)
            currAvailAmount = current_ins_amount(self.ins)[0]
            currAuthAmount  = current_ins_amount(self.ins)[1]
            currIssuedAmount = current_ins_amount(self.ins)[2]
            self.authAmount.Label(currAuthAmount)
            self.issuedAmount.Label(currIssuedAmount)
            self.availAmount.Label(currAvailAmount)
        else:
            self.currentStateLabelVal.Label('Not requested yet')

    def display_state_none(self):
        LOGGER.info('Instrument not in ISIN Management at the moment')
        self.reqNewISIN.Editable(True)
        self.reqNewISINAmount.Editable(True)
        self.manualNewISIN.Editable(True)
        self.reqNewISIN.Visible(True)
        self.manualNewISIN.Visible(True)
        self.reqNewISINAmount.Visible(True)
        self.currentStateLabelVal.Label('Not being managed at the moment')

    def display_state_active(self):
        self.reqTopupReduce.Editable(True)
        self.requestAmount.Editable(True)
        self.reqDeissue.Editable(True)
        self.reqTopupReduce.Visible(True)
        self.requestAmount.Visible(True)
        self.reqDeissue.Visible(True)

    def display_state_new_ISIN_Failed(self):
        self.resendNewISIN.Editable(True)
        self.manualNewISIN.Editable(True)
        self.reqNewISINAmount.Editable(True)
        self.resendNewISIN.Visible(True)
        self.manualNewISIN.Visible(True)
        self.reqNewISINAmount.Visible(True)

    def display_state_topup_reduced_failed(self):
        self.resendTopupReduce.Editable(True)
        self.cancelTopupReduce.Editable(True)
        self.requestAmount.Editable(True)
        self.resendTopupReduce.Visible(True)
        self.cancelTopupReduce.Visible(True)
        self.requestAmount.Visible(True)

    def display_state_deissue_failed(self):
        self.resendDeissue.Editable(True)
        self.cancelDeissue.Editable(True)
        self.resendDeissue.Visible(True)
        self.cancelDeissue.Visible(True)

    def display_state_pending_new_ISIN_request(self):
        self.resendNewISIN.Editable(True)
        self.manualNewISIN.Editable(True)
        self.reqNewISINAmount.Editable(True)
        self.resendNewISIN.Visible(True)
        self.manualNewISIN.Visible(True)
        self.reqNewISINAmount.Visible(True)

    def CreateLayout(self):
        b = acm.FUxLayoutBuilder()
        b.BeginVertBox('None')
        b.AddFill()
        b. BeginHorzBox('None')
        b.  AddInput('initialAmount', 'Amount')
        b.  AddFill()
        b.  AddButton('reqNewISIN', 'New ISIN')
        b.  AddButton('resendNewISIN', 'Resend')
        b.  AddButton('manualNewISIN', 'Manual Insert')
        b. EndBox()
        b. BeginHorzBox('None')
        b.  AddInput('requestAmount', 'Amount')
        b.  AddFill()
        b.  AddButton('reqTopupReduce', 'Topup/Reduce')
        b.  AddButton('resendTopupReduce', 'Resend')
        b.  AddButton('cancelTopupReduce', 'Cancel')
        b. EndBox()
        b. BeginHorzBox('None')
        b.  AddFill()
        b.  AddFill()
        b.  AddButton('reqDeissue', 'Deissue')
        b.  AddButton('resendDeissue', 'Resend')
        b.  AddButton('cancelDeissue', 'Cancel')
        b. EndBox()
        b.AddFill()
        b.AddSeparator()
        b. BeginHorzBox('None')
        b.  AddLabel('currentStateLabel', '%-25s' % 'Current State:')
        b.  AddLabel('currentStateLabelVal', '', width=200)
        b. EndBox()
        b.AddFill()
        b. BeginHorzBox('None')
        b.  AddLabel('authAmountLabel', '%-20s' % 'Authorized Amount:')
        b.  AddLabel('authAmount', '')
        b. EndBox()
        b.AddFill()
        b. BeginHorzBox('None')
        b.  AddLabel('issuedAmountLabel', '%-23s' % 'Issued Amount:')
        b.  AddLabel('issuedAmount', '')
        b. EndBox()
        b.AddFill()
        b. BeginHorzBox('None')
        b.  AddLabel('availAmountLabel', '%-22s' % 'Available Amount:')
        b.  AddLabel('availAmount', '')
        b. EndBox()
        b.EndBox()
        return b


def _confirm_action(ins):
    acm.PollDbEvents()
    dialog_func = acm.GetFunction('msgBox', 3)
    if not ins:
        message = 'Please create an Instrument\nbefore starting ISIN Management.'
        dialog_func('Warning', message, 0)
        return False
    elif not ins.AdditionalInfo().Demat_Instrument() and not ins.AdditionalInfo().DIS_Instrument():
        message = 'Please make sure the "Demat Instrument" field is checked'
        dialog_func('Warning', message, 0)
        return False
    if ins:
        helper = demat_swift_mt598.Demat_MT598_Helper(ins)
        if not helper.validate():
            message = 'Please see log before starting ISIN Management.\nSome fields are invalid'
            dialog_func('Warning', message, 0)
            return False

    return True


def ProcessInstrument(shell, ins):
    customDlg = RequestDialog(ins)
    acm.UX().Dialogs().ShowCustomDialogModal(shell, customDlg.CreateLayout(), customDlg)


def menu_request_isin(eii):
    obj = eii.ExtensionObject()
    shell = eii.ExtensionObject().Shell()
    ins = obj.OriginalInstrument()
    if _confirm_action(ins):
        ProcessInstrument(shell, ins)

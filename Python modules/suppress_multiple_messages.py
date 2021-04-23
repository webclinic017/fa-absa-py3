"""--------------------------------------------------------------------------------------------------------------------------------------
MODULE
    suppress_multiple_messages

DESCRIPTION
Logic to select and place multiple settlements into 'Pending Closure' status and Operations document linked to
'Sent successfully' in Settlement menu from Operations Manager

-----------------------------------------------------------------------------------------------------------------------------------------
HISTORY
=========================================================================================================================================
Date            Change no       Developer               Requester               Description
-----------------------------------------------------------------------------------------------------------------------------------------
2018-04-26      CHG1000697002   Stuart Wilson           Martin Wortmann          Initial Implementation
-----------------------------------------------------------------------------------------------------------------------------------------
"""


import acm
import FUxCore
from FTradeStatus import is_component_in_user_profile


class DiaryDialogCreator(FUxCore.LayoutDialog):
    """Creates GUI to enter diary entry for settlements"""

    def __init__(self):
        self.m_okBtn = None
        self.m_diary_entry = None
        self.diary_entry = None
        self.m_fuxDlg = None

    def HandleCreate(self, dlg, layout):
        self.m_fuxDlg = dlg
        self.m_fuxDlg.Caption('Settlement Diary')
        self.m_diary_entry = layout.GetControl("diary_entry")
        self.m_okBtn = layout.GetControl("ok")

    def HandleApply(self):
        self.diary_entry = self.m_diary_entry.GetData()

        return True

    def get_diary_entry(self):
        return self.diary_entry


def create_layout():
    """Creates GUI layout for diary entry"""
    b = acm.FUxLayoutBuilder()
    b.BeginVertBox('None')
    b.AddInput('diary_entry', 'Diary Entry', 80, 20)
    b.BeginHorzBox('None')
    b.AddFill()
    b.AddButton('ok', 'save')
    b.EndBox()
    b.EndBox()

    return b


def is_authorised_user():
    """Tests if required profile components exists for user"""
    msg_box = acm.GetFunction('msgBox', 3)
    if is_component_in_user_profile('Suppress Payments Message') != 1:
        message = 'Request not allowed. Please contact Front Arena support.'
        msg_box('Warning', message, 0)
        return False
    else:
        return True


def start_diary_dialog(shell):
    """Starts diary dialog for settlement diary entry"""
    builder = create_layout()
    diary_dialog = DiaryDialogCreator()
    print(acm.UX().Dialogs().ShowCustomDialogModal(shell, builder, diary_dialog))

    return diary_dialog.get_diary_entry()


def set_settlement_pending_closure(settlement):
    """Sets settlement status to Pending Closure"""
    settlement.Status('Pending Closure')
    settlement.Commit()


def add_diary_entry(settlement, diary_entry):
    """Adds a diary entry to settlements diary"""
    settlement.AddDiaryNote(diary_entry)
    settlement.Diary().Commit()


def set_op_docs_sent_successfully(settlement):
    """Changes operation docs statuses under settlement to Sent successfully"""
    for doc in settlement.Documents():
        doc.Status("Sent successfully")
        doc.Commit()


def validate_settlement_eligibility_for_message_suppression(settlement):
    """Tests required conditions before transaction is executed on settlements"""
    settle_id = settlement.Oid()
    if settlement.Status() not in ["Exception", "Manual Match", "Hold", "Authorised", "Not Acknowledged"]:

        raise ValueError('Status error with settlement: {settle_id}'.format(settle_id = settle_id))

    elif settlement.RelationType() in ["Cancellation", "Cancel Correct"]:

        raise ValueError('RelationType error with settlement: {settle_id}'.format(settle_id = settle_id))

    elif settlement.IsMissingData():

        raise ValueError('Missing data error with settlement: {settle_id}'.format(settle_id = settle_id))

    elif settlement.PairOffParent() is not None:
        if settlement.PairOffParent().Status() == "Exception":

            raise ValueError('PairOffParent error with settlement: {settle_id}'.format(settle_id = settle_id))


def set_settlements_statuses_and_append_diary(eii, diary_entry):
    """Changes statuses and appends diary entries to selected settlements"""

    for settlement in eii.ExtensionObject().ActiveSheet().Selection().SelectedRowObjects():
        acm.BeginTransaction()
        try:
            validate_settlement_eligibility_for_message_suppression(settlement)
            add_diary_entry(settlement, diary_entry)
            set_settlement_pending_closure(settlement)
            set_op_docs_sent_successfully(settlement)
            acm.CommitTransaction()
        except ValueError as ex:
            # Expected error thrown for settlement that is not
            # eligible for suppression - abort the transaction
            # and log so that user can see why some settlements
            # were not suppressed but don't stop processing of
            # settlements.
            acm.AbortTransaction()
            print(ex)
        except:
            # Any other error is unexpected - abort the
            # transaction and let the process fail.
            acm.AbortTransaction()
            raise


def process_settlements(eii):
    """Processes selected settlements in Operations Manager using menu option under right click Settlements"""
    msg_box = acm.GetFunction('msgBox', 3)

    if is_authorised_user():

        message = 'Do you want to set selected settlements to Pending Closure?'

        if msg_box('Suppress Multiple Settlements', message, 1) == 1:

            shell = eii.Parameter('shell')
            diary_entry = start_diary_dialog(shell)
            set_settlements_statuses_and_append_diary(eii, diary_entry)















"""--------------------------------------------------------------------------------------------------------------------------------------
MODULE
    SBL_settlements_settle_unsettle

DESCRIPTION
Logic to select and place multiple settlements into settled or unsettled status in Settlement menu from Operations Manager

-----------------------------------------------------------------------------------------------------------------------------------------
"""


import acm
import FUxCore
from at_logging import getLogger
from FTradeStatus import is_component_in_user_profile


ALLOWED_GROUPS = ['IT RTB', 'OPS SecLend', 'PCG Collateral']
LOGGER = getLogger()

def is_authorised_user():
    """Tests if required profile components exists for user"""
    if acm.User().UserGroup().Name() not in ALLOWED_GROUPS:
        return False
    else:
        return True

class ViewMenuItem(FUxCore.MenuItem):
    def __init__(self, extObj):
        self._frame = extObj
        self._bp = None
        self._shell = self._frame.Shell()

    def Invoke(self, eii):
        process_settlements(eii)
    
    def Enabled(self):
        return is_authorised_user()

    def Applicable(self):
        return is_authorised_user()



class DialogCreator(FUxCore.LayoutDialog):
    """Creates GUI to enter entry for settlements"""

    def __init__(self):
        self.m_okBtn = None
        self.m_diary_entry = None
        self.m_status = None
        self.m_fuxDlg = None
        self.diary_entry = ''
        self.status_entry = ''
    
    def InitData(self):
        self.m_status_entry.AddItem('Settled')
        self.m_status_entry.AddItem('Authorised')
        self.m_status_entry.SetData('Settled')
        self._status_entry_Changed()
        
    def _status_entry_Changed(self, *args):
        if self.m_status_entry.GetData() == 'Settled':
            self.m_diary_entry.SetData('Settlement set to Settled manually')
        if self.m_status_entry.GetData() == 'Authorised':
            self.m_diary_entry.SetData('Settlement set to Authorised manually')
                        
    def HandleCreate(self, dlg, layout):
        self.m_fuxDlg = dlg
        self.m_shell = dlg.Shell()
        self.m_fuxDlg.Caption('SBL Settlement Status Setter')
        self.m_status_entry = layout.GetControl("status_entry")
        self.m_diary_entry = layout.GetControl("diary_entry")
        self.m_okBtn = layout.GetControl("ok")
        self.m_status_entry.AddCallback('Changed', self._status_entry_Changed, self)
        self.InitData()
        
    def HandleApply(self):
        self.diary_entry = self.m_diary_entry.GetData()
        self.status_entry = self.m_status_entry.GetData()
        return True

    def get_diary_entry(self):
        return self.diary_entry

    def get_status_entry(self):
        return self.status_entry


def create_layout():
    """Creates GUI layout for diary entry"""
    b = acm.FUxLayoutBuilder()
    b.BeginVertBox('None')
    b.AddOption('status_entry', 'To Status', 30, 30)
    b.AddFill()
    b.AddInput('diary_entry', 'Diary Text', 50, 20)
    b.BeginHorzBox('None')
    b.AddFill()
    b.AddButton('ok', 'Apply')
    b.AddButton('cancel', 'Cancel') 
    b.EndBox()
    b.EndBox()
    return b


def set_settlement_status(settlement, to_status):
    """Sets settlement status to provided status"""
    settlement.Status(to_status)


def add_diary_entry(settlement, diary_entry):
    """Adds a diary entry to settlements diary"""
    settlement.AddDiaryNote(diary_entry)


def is_valid_SBL_settlement(settlement):
    trade = settlement.Trade()
    
    if not trade:
        return False
        
    if trade.Acquirer().Name() not in ["SECURITY LENDINGS DESK", "SBL AGENCY I/DESK"]:
        return False
    
    if not (trade.Instrument().InsType() == "SecurityLoan" or trade.TradeCategory() == "Collateral"):
        return False
    
    if trade.AdditionalInfo().SL_SWIFT() is None:
        return False

    return True


def satisfies_nonrtb_usergroup_rules(settlement, to_status, msg_settle_id):

    if to_status == "Settled" and settlement.Status() not in ["Authorised", "Exception"]:
        raise ValueError('Status error {}. Settlement should be in either Authorised, Not Acknowledged or Exception status.'.format(msg_settle_id))

    if settlement.PairOffParent() is not None:
        if settlement.PairOffParent().Status() == "Exception" and to_status == "Settled":
            raise ValueError('PairOffParent error {}'.format(msg_settle_id))

    if settlement.IsMissingData():
        raise ValueError('Missing data error {}'.format(msg_settle_id))

    if settlement.RelationType() in ["Cancellation", "Cancel Correct"]:
        raise ValueError('RelationType error {}'.format(msg_settle_id))
    return True


def user_in_rtb_usergroup():

    return acm.User().UserGroup().Name() == "IT RTB"


def validate_settlement_eligibility_for_message(settlement, to_status):
    """Tests required conditions before transaction is executed on settlements"""
    settle_id = settlement.Oid()
    msg_settle_id = 'with settlement {}'.format(settle_id)

    if not user_in_rtb_usergroup():
        satisfies_nonrtb_usergroup_rules(settlement, to_status, msg_settle_id)

    if not is_valid_SBL_settlement(settlement):
        raise ValueError('SBL settlement type error {}'.format(msg_settle_id))

    if settlement.Type() not in ["Security Nominal", "End Security"]:
        raise ValueError('Type error {}. Settlement type should be either Security Nominal or End Security status.'.format(msg_settle_id))


def set_settlements_statuses_and_append_diary(eii, diary_entry, status_entry):
    """Changes statuses and appends diary entries to selected settlements"""
    for settlement in eii.ExtensionObject().ActiveSheet().Selection().SelectedRowObjects():
        acm.BeginTransaction()
        try:
            settlement_si = settlement.StorageImage()
            validate_settlement_eligibility_for_message(settlement_si, status_entry)
            add_diary_entry(settlement_si, diary_entry)
            set_settlement_status(settlement_si, status_entry)
            settlement_si.Diary().Commit()
            settlement_si.Commit()
            acm.CommitTransaction()
        except ValueError as ex:
            # Expected error thrown for settlement that is not eligible for suppression - abort the transaction
            # and log so that user can see why some settlements were not suppressed but don't stop processing of
            # settlements.
            acm.AbortTransaction()
            LOGGER.exception('Error processing settlement')
        except:
            # Any other error is unexpected - abort the transaction and let the process fail.
            acm.AbortTransaction()
            raise


def process_settlements(eii):
    """Processes selected settlements in Operations Manager using menu option under right click Settlements"""
    LOGGER.msg_tracker.reset()
    if is_authorised_user():
        shell = eii.Parameter('shell')
        builder = create_layout()
        dialog = DialogCreator()
        if acm.UX().Dialogs().ShowCustomDialogModal(shell, builder, dialog):
            status = dialog.get_status_entry()
            diary_text = dialog.get_diary_entry()
            set_settlements_statuses_and_append_diary(eii, diary_text, status)

    if LOGGER.msg_tracker.errors_counter:
        raise RuntimeError("ERRORS occurred. Please check the log.")

    LOGGER.info("Completed successfully")


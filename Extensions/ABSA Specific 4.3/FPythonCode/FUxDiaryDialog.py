"""----------------------------------------------------------------------------------------------------------
MODULE                  :       FUxDiaryDialog
PURPOSE                 :       This module is used to display a dialog window with the reset diary entry.
DEPARTMENT AND DESK     :       Operations
REQUESTER               :       Linda Breytenbach
DEVELOPER               :       Andrei Conicov
CR NUMBER               :       ABITFA-2611
-------------------------------------------------------------------------------------------------------------

DESCRIPTION OF MODULE:

The reset diary offers the possibility to add any text to any trade.
Each diary entry is saved to a text object (type Customizable) with the name ResetDiary+trdnbr.

Documentation:
    http://confluence.barcapint.com/display/ABCAPFA/Reset+Diary

HISTORY
=============================================================================================================
Date            Change no       Developer                       Description
-------------------------------------------------------------------------------------------------------------
2015-07-01      CHNG0002958196          Andrei Conicov                     Initial Implementation
"""

import traceback
from datetime import datetime

import acm
import FUxCore
from comment_history import JSONTextObjectCommentHistory

class ResetDiaryDialog(FUxCore.LayoutDialog):
    """
    Handles the creation of the custom reset diary dialog
    and all the required operations.
    """
    def __init__(self, params):
        self._fux_dlg = None
        self.params = params
        self.result = None

    def HandleApply(self):
        """Called when the user selects the default action (ok button)

        Return the diary entry
        """
        self.result = self._diary_entry_text.GetData()
        return True

    def HandleCancel(self):
        '''Called when the user cancels or closes the dialog with the red cross
        return True to let the dialog close'''

        self.result = None
        return True

    def HandleCreate(self, dlg, layout):
        """Construct the entire GUI using uxLayoutCreateContext
        """
        self._fux_dlg = dlg
        if self.params.has_key("caption"):
            self._fux_dlg.Caption(self.params["caption"])
        trades_list = layout.GetControl("tradesList")
        self._diary_entry_text = layout.GetControl("diaryEntryText")

        trades_list.Populate(self.params["trades"])
        if not self.params["trades"]:
            ok_btn = layout.GetControl("ok")
            ok_btn.Enabled(False)
            trades_list.SetColor("Background", acm.UX().Colors().Create(255, 0, 0))
        self._diary_entry_text.AppendText(self.params["diary"])

def show_dialog(shell, params):
    """ Display the ResetDiaryDialog  with the specified parameters"""
    builder = _create_layout()
    dialog = ResetDiaryDialog(params)
    acm.UX().Dialogs().ShowCustomDialogModal(shell, builder, dialog)
    
    return dialog.result

def _create_layout():
    b = acm.FUxLayoutBuilder()
    b.BeginVertBox("None")
    b.AddLabel("tradesLbl", "Trades:")
    b.AddList("tradesList", numlines=5, width=80)
    b.AddLabel("DiaryEntryLbl", "Diary:")
    b.AddText("diaryEntryText", height=140, width=80)
    b.BeginHorzBox("None")
    b.AddFill()
    b.AddButton("ok", "OK")
    b.AddButton("cancel", "Cancel")
    b.EndBox()
    b.EndBox()
    return b


def _get_trades_from_invokation_info(invokationInfo):
    """
    Returns a set of trades for the provided selection (from workbook).

    !!! can be merged with the same function from ATSEconTradeAmend
    """
    trades = []
    selection = invokationInfo.ExtensionObject().ActiveSheet().Selection()
    cells = selection.SelectedCells()
    for cell in cells:
        rowObject = cell.RowObject()
        if hasattr(rowObject, "Trade"):
            trade = rowObject.Trade()
            trades.append(trade.Oid())

    return set(trades)

def _log(msg):
    print("{0}: {1}".format(datetime.now().strftime("%y%m%d %H%M%S"), msg))

def show(invocation_info):
    """Show the diary dialog for the list of selected trades"""
    trades = list(_get_trades_from_invokation_info(invocation_info))
    params = {}
    params["caption"] = 'Reset Diary'
    params["trades"] = trades

    diary = ''
    if len(trades) == 1:
        diary = get_unformatted_reset_diary_entries(acm.FTrade[trades[0]])
    else:
        for trdnbr in trades:
            reset_diary = get_unformatted_reset_diary_entries(acm.FTrade[trdnbr])
            diary += "{0}\n{1}\n".format(trdnbr, reset_diary)

    params["diary"] = diary

    extension_object = invocation_info.ExtensionObject()
    shell = extension_object.Shell()

    diary_entry = show_dialog(shell, params)

    if diary_entry == None:
        _log("No diary entry provided")
        return

    for trdnbr in trades:
        _update_reset_diary(trdnbr, diary_entry)

_PREFIX = "ResetDiary"

def _update_reset_diary(trdnbr, diary_entry):

    _log("Saving a new entry to the diary, trdnbr {0}".format(trdnbr))
    acm_trade = acm.FTrade[trdnbr]
    text_obj = JSONTextObjectCommentHistory(acm_trade, _PREFIX)
    text_obj.set(diary_entry)

    try:
        text_obj.save()
    finally:
        # this will trigger the update of the additional info
        acm_trade.Touch()
        acm_trade.Commit()

def get_unformatted_reset_diary_entries(acm_trade):
    """
    Returns unformatted reset diary entries for the specified trade.
    """
    if not acm_trade:
        return
    text_obj = JSONTextObjectCommentHistory(acm_trade, _PREFIX)

    if not text_obj:
        return ""

    return "\n".join(text_obj.unformatted_comments())

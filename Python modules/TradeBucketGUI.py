"""----------------------------------------------------------------------------------------------------------
MODULE                  :       TradeBucketGUI
PURPOSE                 :       This module will add diaries to trade objects.
DEPARTMENT AND DESK     :       Operations
REQUESTER               :       Letitia Roux
DEVELOPER               :       Heinrich Cronje, Jan Sinkora
CR NUMBER               :       XXXXXX
-------------------------------------------------------------------------------------------------------------

HISTORY
=============================================================================================================
Date            Change no       Developer                       Description
-------------------------------------------------------------------------------------------------------------
2012-07-05      XXXXXX          Heinrich Cronje                 Initial Implementation
2012-10-17      XXXXXX          Jan Sinkora                     Complete rewrite using AUX instead of CLR tools, which caused FA to freeze
2013-11-11      XXXXXX          Jan Sinkora                     Populating choice lists with Populate() doesn't allow item selecting. Replacing this with AddItem.
-------------------------------------------------------------------------------------------------------------

DESCRIPTION OF MODULE:

    This module will be called up from Trading Manager when a user want to add "Trade Bucket Comments" to a trade.
    The script will open a GUI which will show historic comments and have an input box where new comments can be added.
    Additional information that can be set:
        - Responsible person
        - Responsible area (IT, Front office, Legal, ...)
        - Affirmation status (Yes/No)

    All of these info will be available in the ASQL SAGEN_Trade_Buckets.
"""

import os
import acm, ael
import at
import FUxCore
from comment_history import JSONTextObjectCommentHistory

class TradeBucketDialog(FUxCore.LayoutDialog):
    """The GUI-managing class."""

    def __init__(self, trade):
        """Init with an acm.FTrade instance."""

        self.comment_history = None

        # prepare the layout
        self.CreateLayout()

        # setup the data
        self.trade = trade

        self.comment_history = JSONTextObjectCommentHistory(trade)

    def HandleApply(self):
        # runs when "ok" is clicked

        # save the comment
        new_comment_text = self.fux_comment_today.GetData()
        self.comment_history.append(new_comment_text)
        self.comment_history.save()

        at.addInfo.save_or_delete(self.trade, 'Affirmation', self.fux_affirmation.GetData())
        at.addInfo.save_or_delete(self.trade, 'Responsible Person', self.fux_responsible_person.GetData())
        at.addInfo.save_or_delete(self.trade, 'Responsible Area', self.fux_responsible_area.GetData())

        # return None => dialog stays open
        # return anything else => dialog closes
        return True
    def HandleCreate(self, dlg, layout):
        # runs when the gui is being created

        self.fux_dialog = dlg
        self.fux_dialog.Caption('Trade bucket comments')
        self.fux_comment_history = layout.GetControl('comment_history')
        self.fux_comment_today = layout.GetControl('comment_today')
        self.fux_affirmation = layout.GetControl('affirmation')
        self.fux_responsible_person = layout.GetControl('responsible_person')
        self.fux_responsible_area = layout.GetControl('responsible_area')

        # this is a subset of the values associated with 'Affirmation' addinfo
        choices = ['', 'Yes', 'No']
        # this doesn't work in 2013
        #self.fux_affirmation.Populate(choices)
        for choice in choices:
            self.fux_affirmation.AddItem(choice)
        self.fux_affirmation.SetData(self.trade.AdditionalInfo().Affirmation())

        choiceList = at.choiceList.get('Responsible Area')
        choices = ['']
        choices.extend([c.Name() for c in choiceList.Choices()])
        # this doesn't work in 2013
        #self.fux_responsible_area.Populate(choices)
        for choice in choices:
            self.fux_responsible_area.AddItem(choice)
        self.fux_responsible_area.SetData(at.addInfo.get_value(self.trade, 'Responsible Area'))

        self.fux_comment_history.Populate(self.comment_history.formatted_comments())

        self.fux_responsible_person.SetData(self.trade.add_info('Responsible Person'))

    def CreateLayout(self):
        """Creates the layout of the GUI dialog."""

        b = acm.FUxLayoutBuilder()
        b.BeginVertBox('None', 'Trade bucket comments')
        b. AddLabel('comment_history_label', 'Comment history:')
        b. AddList('comment_history', 5, 5, 120, 120)
        b. AddInput('comment_today', 'New comment:')
        b. AddSpace(10)
        b. AddOption('affirmation', 'Affirmation:', 30, 30)
        b. AddInput('responsible_person', 'Responsible person:', 30, 30)
        b. AddOption('responsible_area', 'Responsible area:', 30, 30)
        b. BeginHorzBox('None')
        b.  AddFill()
        b.  AddButton('ok', 'OK')
        b.  AddButton('cancel', 'Cancel')
        b. EndBox()
        b.EndBox()
        self.layout = b

def startDialog_cb(eii, *rest):
    """Starts the dialog for comment adding."""
    shell = eii.Parameter('shell')
    customDlg = TradeBucketDialog(eii.ExtensionObject()[0])
    acm.UX().Dialogs().ShowCustomDialogModal(shell, customDlg.layout, customDlg)

def get_formatted_comments(text_object, *rest):
    """
    A convenience method for getting the formatted comments.
    """

    return "\n".join(JSONTextObjectCommentHistory.parse_and_format(text_object))

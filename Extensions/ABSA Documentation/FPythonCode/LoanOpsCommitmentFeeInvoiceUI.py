"""
-----------------------------------------------------------------------------------------------------------------------------------------
HISTORY
=========================================================================================================================================
Date            Change no       Developer               Requester               Description
-----------------------------------------------------------------------------------------------------------------------------------------
2019-09-05      FAOPS-530       Joash Moodley                      Initial Implementation.
-----------------------------------------------------------------------------------------------------------------------------------------

"""

import acm
import FUxCore

from at_logging import getLogger
from LoanOpsCommitmentFeeCreator import LoanOpsCommitmentFeeCreator as creator


LOGGER = getLogger(__name__)

options = [
    "Please Select",
    "Generate",
    "Generate Amendment"
]


def release_confirmation(confirmation):
    """
    """
    LOGGER.info('Releasing confirmation {confirmation_oid}.'.format(
        confirmation_oid=confirmation.Oid()
   ))
    confirmation = confirmation.StorageImage()
    confirmation.Status('Released')
    confirmation.Commit()


def generate_confirmation(trade, date, event_name):
    """
    """
    LOGGER.info('generating confirmation  for trade {trade_oid}.'.format(
        trade_oid=trade.Oid()
   ))
    invoice = creator(
        event_name,
        trade,
        date,
   )

    invoice.create_commitment_fee_invoice()


class InvoiceUI(FUxCore.LayoutDialog):

    def __init__(self, rows, eii, shell):
        self.trades = rows
        self.newOption = None
        self.futureDate = None
        self.eii = eii
        self.shell = shell
        self._InitDataBindingControls()

    @FUxCore.aux_cb
    def HandleApply(self):
        futureDate = self.futureDate.GetValue()
        for trade in self.trades:
            if self.newOption.GetData() == 'Generate':
                generate_confirmation(trade.Trade(), futureDate, "Loan Ops Commitment Fee Future Date")
            elif self.newOption.GetData() == 'Generate Amendment':
                generate_confirmation(trade.Trade(), futureDate, "Loan Ops Commitment Fee Amendment")
        return True

    def HandleDestroy(self):
        return None

    def CreateLayout(self):
        b = acm.FUxLayoutBuilder()
        b.BeginVertBox('None')
        b.BeginHorzBox('EtchedIn', 'Please Choose An Option')
        b.BeginHorzBox('None')
        self.futureDate.BuildLayoutPart(b, 'Date*:')
        b.EndBox()
        b.AddOption('options', 'Options', 40, 40)
        b.EndBox()
        b.BeginHorzBox('None')
        b.AddButton('ok', 'OK', True)
        b.AddButton('cancel', 'Cancel', True)
        b.EndBox()
        b.EndBox()
        return b

    def _InitDataBindingControls(self):
        self._bindings = acm.FUxDataBindings()
        formatter = acm.Get('formats/LimitValues')
        self.futureDate = self._bindings.AddBinder('defaultDateCtrl', acm.GetDomain('date'), None)
        self._bindings.AddDependent(self)

    def HandleCreate(self, dlg, layout):
        self.fuxDlg = dlg
        self.fuxDlg.Caption('Amend / Generate Invoice(s)')
        self.layout = layout
        self.binder = acm.FUxDataBindings()
        gc = self.layout.GetControl
        self.newOption  = gc('options')
        for option in options:
            self.newOption.AddItem(option)
        self.newOption.SetData('Please Select')
        self.futureDate.InitLayout(self.layout)
        self._bindings.AddLayout(layout)
        self.newOption.AddCallback('Changed', self.updateControls, None)

    def updateControls(self, *_):
        self.newOption.Editable(True)
        self.futureDate.Editable(True)


def StartDialogFromMenu(eii):
    shell = eii.ExtensionObject().Shell()
    opsManager = eii.ExtensionObject()
    sheet = opsManager.ActiveSheet()
    selection = sheet.Selection()
    selectedCells = selection.SelectedRowObjects()
    customDlg = InvoiceUI(selectedCells, eii, shell)
    result=acm.UX().Dialogs().ShowCustomDialogModal(shell, customDlg.CreateLayout(), customDlg)

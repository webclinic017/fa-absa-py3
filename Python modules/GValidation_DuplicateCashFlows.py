"""
Custom dialog displaying a money flow sheet containing cash flows. It is intended to prompt the user when
duplicate cash flows are booked to an instrument.

DESCRIPTION

Amendment Diary
2019-05-31        Hugo Decloedt         FAOPS-475       Add check for cash flow duplicates and prompt user to confirm
                                                        saving trade if there are duplicates.
"""

# pylint: disable=import-error
import acm
import FUxCore


def CreateLayout():
    """
    Creating the layout.
    :return: FUxLayoutBuilder
    """
    label = "This trade contains duplicate cash flows. Are you sure you want to save this trade with the duplicates?"
    b = acm.FUxLayoutBuilder()  # pylint: disable=no-member
    b.BeginVertBox()
    b.AddLabel('msg', label)
    b.BeginVertBox('EtchedIn', 'Duplicate cash flows')
    b.BeginVertBox()
    b.AddCustom('flowSheet', 'sheet.FMoneyFlowSheet', 250, 150)
    b.EndBox()
    b.AddSeparator()
    b.EndBox()

    b.BeginHorzBox()
    b.AddFill()
    b.AddButton('cancel', 'Cancel')
    b.AddButton('ok', 'Save')
    b.EndBox()

    b.EndBox()

    return b


class DialogDuplicateCashFlows(FUxCore.LayoutDialog):
    """
    Dialog displaying the duplicate cash flows and prompting the user to confirm saving the trade with the duplicates.
    """

    def __init__(self, flows):
        self._flowSheet = None
        self._flows = flows

    def HandleCreate(self, dialog, layout):
        """
        Event handler when the dialog gets created.
        :param dialog: FUxDialog
        :param layout: FUxLayout
        """
        del dialog
        ctrl = layout.GetControl
        self._flowSheet = ctrl('flowSheet').GetCustomControl()
        self.__initialiseSheet()

    # pylint: disable=no-self-use
    def HandleApply(self):
        """
        OnClick event handler when the user clicks on Save.
        :return: bool
        """
        return True

    # pylint: disable=no-self-use
    def HandleCancel(self):
        """
        OnClick event handler when the user clicks on Cancel.
        :return: bool
        """
        return False

    def __initialiseSheet(self):
        columns = self._flowSheet.ColumnCreators()
        columns.Clear()

        # Populate the limit sheet columns
        extContext = acm.GetDefaultContext()  # pylint: disable=no-member
        columnNames = ('Cash Analysis Pay Day', 'Cash Analysis Nominal')
        defaultColumns = acm.GetColumnCreators(columnNames, extContext)  # pylint: disable=no-member

        for i in range(defaultColumns.Size()):
            columns.Add(defaultColumns.At(i))
        for flow in self._flows:
            self._flowSheet.InsertObject(flow, 'IOAP_LAST')

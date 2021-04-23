import acm
import FUxCore
from DividendCashFlow import GenerateDividendCashFlow
from at_ux import msg_box
from at_logging import getLogger

logger = getLogger(__name__)


class RegenerateDividendCashFlowDialog(FUxCore.LayoutDialog):
    """The GUI-managing class."""

    def __init__(self, instrument):
        """Init with an acm.FTrade instance."""
        self._start_date = None
        self._start_date_control = None
        self._end_date = None
        self._end_date_control = None
        self.instrument = instrument

        # prepare the layout
        self.CreateLayout()


    def HandleApply(self):
        start_date = self._start_date_control.GetData()
        end_date = self._end_date_control.GetData()
        try:
            logger.info("Regenerating for '%s': (StartDate: '%s' EndDate: '%s')" %(self.instrument.Name(), start_date, end_date))
            div = GenerateDividendCashFlow(self.instrument, start_date, end_date)
            if not div.cash_flow_exists():
                div.generate_dividend_cash_flow()
            logger.info('Successfully Run')
        except Exception, e:
            msg_box('Could not create dividend, please check date format', "ERROR")
            logger.error(e)
        return True

    def HandleCreate(self, dlg, layout):
        '''Runs when the GUI is being created.'''
        gc = layout.GetControl
        
        self.fux_dialog = dlg
        self.fux_dialog.Caption('Regenerate Dividend Cash Flows')
        self._start_date_control = gc("startDate")
        self._end_date_control = gc("endDate")
        
        _today = acm.Time.DateToday()
        
        self._start_date_control.SetData(acm.Time.DateAddDelta(_today, 0, 0, -1))
        self._end_date_control.SetData(acm.Time.DateAddDelta(_today, 0, 0, 14))
        gc("ok").SetFocus()
        
    def CreateLayout(self):
        """Creates the layout of the GUI dialog."""

        b = acm.FUxLayoutBuilder()
        b.BeginVertBox('None')
        b. AddLabel("lblValues", "Regenerate Dividend Cash Flows")
        b. BeginHorzBox()
        b.  AddInput('startDate', 'Start Date')
        b.  AddInput('endDate', 'End Date')
        b. EndBox()
        b. BeginHorzBox()
        b.  AddButton('ok', 'Run')
        b.  AddButton("cancel", "Close")
        b. EndBox()
        b.EndBox()

        self.layout = b


def startDialog(eii, *rest):
    """Starts the dialog for comment adding."""
    
    object = eii.ExtensionObject().CurrentObject()
    if object is None:
        msg_box('No Object selected', 'Error')
        return
    elif object.IsKindOf(acm.FInstrument):
        instrument = object
    elif object.IsKindOf(acm.FTrade):
        instrument = object.Instrument()
    if not instrument.IsKindOf(acm.FTotalReturnSwap):
        msg_box('Instrument not of type Total Return Swap', 'Error')
        return
    shell = eii.ExtensionObject().Shell()
    customDlg = RegenerateDividendCashFlowDialog(instrument)
    acm.UX().Dialogs().ShowCustomDialogModal(shell,
                                             customDlg.layout,
                                             customDlg)

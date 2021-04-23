""" Compiled: 2020-09-18 10:38:51 """

#__src_file__ = "extensions/BuySideOMS/./etc/FOMSDiagnosisDialog.py"
"""--------------------------------------------------------------------------
MODULE
    FOMSDiagnosisDialog

    (c) Copyright 2018 FIS FRONT ARENA. All rights reserved.

DESCRIPTION

-----------------------------------------------------------------------------"""


import acm
import FUxCore
import FOMSDiagnosis
import threading

def ReallyStartDialog(shell, count):
    builder = CreateLayout()
    customDlg = myCustomDialog()
    acm.UX().Dialogs().ShowCustomDialogModal(shell, builder, customDlg )

def StartDialog(eii):
    shell = eii.ExtensionObject().Shell()
    ReallyStartDialog(shell, 0);

# Refresh main dialog of diagnosisi tool on every 1000 ms
def OnTimer(self):
    self.UpdateControls()

class myCustomDialog(FUxCore.LayoutDialog):
    
    def __init__(self):
        # progress bar value variables
        self._progress_aims = None
        self._progress_tab = None
        self._progress_ats = None
        self._progress_start_check = None
        #button colored variables
        self._btn_aims = None
        self._btn_tab = None
        self._btn_ats = None
        self._btn_start = None
        # log variables responsible for showing logs
        self._conected_to_aims = None
        self._order_program_created = None
        self._mirror_trade_created = None
        self._deal_package_created = None
        self._business_process_created = None
        self._sales_order_released_for_exceution = None
        # BSOMSDiagnosis class implement methods and attribute for checking workflow
        self._control_value = FOMSDiagnosis.BSOMSDiagnosis()
        # thread which run diagnosisi tool check
        self._thread = None
        # dict of colors 
        self._color = {'Start': acm.UX().Colors().Create(220, 220, 220),'Yes': acm.UX().Colors().Create(89, 168, 35), 'No': acm.UX().Colors().Create(255, 94, 94), 'Undefine': acm.UX().Colors().Create(0, 119, 255)}
    
    def UpdateControls(self):
        self._conected_to_aims.Label(self._control_value._conected_to_market[1])
        self._progress_aims.SetData(self._control_value._progress_aims)
        self._progress_ats.SetData(self._control_value._progress_ats)
        self._progress_tab.SetData(self._control_value._progress_tab)
        self._progress_aims.ForceRedraw()
        self._mirror_trade_created.Label(self._control_value._mirror_trade_created[1])
        self._deal_package_created.Label(self._control_value._deal_package_created[1])
        self._business_process_created.Label(self._control_value._business_process_created[1])
        self._order_program_created.Label(self._control_value._order_program_created[1])
        self._sales_order_released_for_exceution.Label(self._control_value._sales_order_released_ex[1])
        self._fill_trades_properly_created.Label(self._control_value._fill_trades_properly_created[1])
        self._btn_aims.SetColor(0, self._color[self._control_value.AimsWork()])
        self._btn_ats.SetColor(0, self._color[self._control_value.AtsWork()])
        self._btn_tab.SetColor(0, self._color[self._control_value.TabWork()])
        
        
    def HandleCreate( self, dlg, layout):
        self.m_fuxDlg = dlg
        self.m_fuxDlg.RegisterTimer( OnTimer, 1000) 
        self.m_fuxDlg.Caption('OMS Diagnosis Dialog')
        self._progress_aims = layout.GetControl('Progress_aims')
        self._progress_tab = layout.GetControl('Progress_tab')
        self._progress_ats = layout.GetControl('Progress_ats')
        self._btn_aims = layout.GetControl('aims')
        self._btn_tab = layout.GetControl('tab')
        self._btn_ats = layout.GetControl('ats')
        self._btn_start = layout.GetControl('strat_check')
        self._btn_start.AddCallback( "Activate", On_strat_check_Clicked, self)
        self._conected_to_aims = layout.GetControl('conected_to_aims')
        self._order_program_created = layout.GetControl('order_program_created')
        self._mirror_trade_created = layout.GetControl('mirror_trade_created')
        self._deal_package_created = layout.GetControl('deal_package_created')
        self._business_process_created = layout.GetControl('business_process_created')
        self._sales_order_released_for_exceution = layout.GetControl('sales_order_released_for_exceution')
        self._fill_trades_properly_created = layout.GetControl('fill_trades_properly_created')
    
# Start check button control method
def On_strat_check_Clicked(self, cd):
    self._btn_aims.SetColor(0, acm.UX().Colors().Create(210, 210, 210))
    self._btn_aims.SetColor(2, acm.UX().Colors().Create(0, 0, 0))
    self._btn_aims.SetColor(3, acm.UX().Colors().Create(0, 0, 0))
    self._btn_ats.SetColor(0, acm.UX().Colors().Create(210, 210, 210))
    self._btn_ats.SetColor(2, acm.UX().Colors().Create(0, 0, 0))
    self._btn_ats.SetColor(3, acm.UX().Colors().Create(0, 0, 0))
    self._btn_tab.SetColor(0, acm.UX().Colors().Create(210, 210, 210))
    self._btn_tab.SetColor(2, acm.UX().Colors().Create(0, 0, 0))
    self._btn_tab.SetColor(3, acm.UX().Colors().Create(0, 0, 0))
    self._mirror_trade_created.Label("")
    self._deal_package_created.Label("")
    self._business_process_created.Label("")
    self._conected_to_aims.Label("")
    self._order_program_created.Label("")
    self._conected_to_aims.Label("")
    self._sales_order_released_for_exceution.Label("")
    self._progress_aims.SetData(0)
    self._progress_tab.SetData(0)
    self._progress_ats.SetData(0)
    self._control_value = FOMSDiagnosis.BSOMSDiagnosis()
    self._thread =  threading.Thread(target = self._control_value.OMSDiagnosis, args=())
    self._thread.daemon = True
    self._thread.start()
    
    
    
def CreateLayout():
    b = acm.FUxLayoutBuilder()
    b.BeginHorzBox('EtchedIn', '')
    b. BeginVertBox()
    b.  AddButton('strat_check', 'Start Check')
    b. EndBox()
    # AIMS part
    b. BeginVertBox()
    b.  BeginVertBox()
    b.   BeginHorzBox()
    b.     AddButton('aims', 'AIMS')
    b.     AddProgress('Progress_aims', 300, 13, -1, 12)
    b.   EndBox()
    b.     AddLabel('conected_to_aims', '')
    b.     AddLabel('order_program_created', '')
    b.EndBox()
    # TAB part
    b.   BeginHorzBox()
    b.     AddButton('tab', 'TAB')
    b.     AddProgress('Progress_tab', 300, 13, -1, 12)
    b.   EndBox()
    b.  BeginVertBox()
    b.     AddLabel('deal_package_created', '')
    b.     AddLabel('mirror_trade_created', '')
    b.     AddLabel('business_process_created', '')
    b.     AddLabel('fill_trades_properly_created', '')
    b.   EndBox()
    b.   BeginHorzBox()
    # ATS part
    b.     AddButton('ats', 'ATS')
    b.     AddProgress('Progress_ats', 300, 13, -1, 12)
    b.   EndBox()
    b.  BeginVertBox()
    b.     AddLabel('sales_order_released_for_exceution', '')
    b.     AddLabel('ocharacteristics', '')
    b.  EndBox()
    b. EndBox()
    b. BeginVertBox()
    b.  AddFill()
    b. EndBox()
    b.EndBox()
    return b
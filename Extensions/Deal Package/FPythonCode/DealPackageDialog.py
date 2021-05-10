import acm
import FUxCore
from DealPackageUtil import RefreshDealPackageProxy, UnpackPaneInfo, WrapAsTabControlList, OpenTraitDialog

class DealPackageDialog(FUxCore.LayoutTabbedDialog):
    def __init__(self, dealPackage):
        self.m_fuxDlg = None
        self.m_fuxLayout = None
        self.m_fuxTopLayout = None
        self.m_slimDetailButton = None
        self.m_dealPackage = dealPackage
        self.m_GUIPanes = acm.FArray()
        self.m_paneInfos = None
        self.m_refreshProxy = RefreshDealPackageProxy(self.DealPackage())
        self.RefreshProxy().RegisterObserver(self._UpdateTraitsTabValues)
        self.SetDealPackageUxCallbacks()
        
    def DealPackage(self):    
        return self.m_dealPackage

    def GetAttribute(self, traitName):
        return self.DealPackage().GetAttribute(traitName)
    
    def GetAttributeMetaData(self, traitName, metaKey):
        return self.DealPackage().GetAttributeMetaData(traitName, metaKey)
    
    def Shell(self):
        return self.m_fuxDlg.Shell()
    
    def Application(self):
        return self

    def OnCloseDialogUxCallback(self):
        self._FuxDialog().CloseDialogOK()

    def SetDealPackageUxCallbacks(self):
        uxCallbacks = self.DealPackage().GetAttribute('uxCallbacks')
        if not uxCallbacks:
            uxCallbacks = acm.FDictionary()
        uxCallbacks.AtPut('closeDialogCb', self.OnCloseDialogUxCallback)
        uxCallbacks.AtPut('dialog', self.Dialog)
        self.DealPackage().SetAttribute('uxCallbacks', uxCallbacks)
        
    def HandleDestroy(self,*args):
        self.RefreshProxy().UnregisterObserver(self._UpdateTraitsTabValues)
    
    def RefreshProxy(self):
        return self.m_refreshProxy
    
    def Caption(self):
        return ''
    
    def CustomPanes(self):
        pass
    
    def Dialog(self, obj, attribute, *dialogArgs):
        return OpenTraitDialog(self.Shell(), obj, attribute, *dialogArgs)
    
    def NoButtonMode(self):
        return False

    def AddSlimDetailControl(self):
        return False if self.NoButtonMode() else True
    
    def HandleCreate( self, dialog, layout ):
        self._SetFuxDialog(dialog)
        self._SetFuxLayout(layout)
        self._GetCustomPaneInfos()
        for paneInfo in self.m_paneInfos:
            paneName, customLayout = UnpackPaneInfo(paneInfo)
            
            self._BuildCustomPane(paneName, customLayout)
                
        self.GetCustomControls(layout)
        self._UpdateTraitsTabValues()
    
    def HandleApply(self):
        return True
    
    def HandleCancel(self):
        return True
   
    def HasCustomBottomLayout(self):
        return False
    
    def CreateCustomBottomLayout(self):
        return None
        
    def CreateButtonLayout(self):
        b = acm.FUxLayoutBuilder()
        b.BeginHorzBox('None')
        if not self.NoButtonMode():
            if self.AddSlimDetailControl():
                self._AddSlimDetailButton(b)
            b.AddFill()    
            self._AddApplyButton(b)
            self._AddCancelButton(b)
        b.EndBox()
        return b
        
    def CreateBottomLayout(self):
        layout = None
        if self.HasCustomBottomLayout():
            layout = self.CreateCustomBottomLayout()
        else:
            layout = self.CreateButtonLayout()
        return layout
    
    def ApplyLabel(self):
        return 'OK'
    
    def CancelLabel(self):
        return 'Cancel'
        
    def ShowDialog(self, shell, modalMode=True):
        fUxLayoutBuilder = self.CreateBottomLayout()
        if modalMode:
            return acm.UX().Dialogs().ShowCustomDialogModal(shell, fUxLayoutBuilder, self)
        else:
            return acm.UX().Dialogs().ShowCustomDialog(shell, fUxLayoutBuilder, self)
    
    def _AddApplyButton(self, b):
        if self.ApplyLabel():
            b.AddButton('_ok_', self.ApplyLabel())
            
    def _AddCancelButton(self, b):
        if self.CancelLabel():
            b.AddButton('cancel', self.CancelLabel())
    
    def _AddSlimDetailButton(self, b):
        b.AddButton('_slimDetail_', 'Detail Mode')
    
    def _FuxDialog(self):
        return self.m_fuxDlg
    
    def _SetFuxDialog(self, dialog):
        self.m_fuxDlg = dialog
        self.m_fuxDlg.Caption( self.Caption() )
        self.m_fuxDlg.RegisterTimer( self._OnTimerTick, 150)
        
    def _SetFuxLayout(self, layout):
        self.m_fuxLayout = layout
        
    def _FuxLayout(self):
        return self.m_fuxLayout
        
    def _SetFuxTopLayout(self, layout):
        self.m_fuxTopLayout = layout
        
    def _FuxTopLayout(self):
        return self.m_fuxTopLayout
        
    def _OnTimerTick(self, ud):
        self.RefreshProxy().Refresh()
    
    def _AddTopLayout(self):
        topBuilder = acm.FUxLayoutBuilder()
        topBuilder.BeginVertBox('None')
        topBuilder.EndBox()
        
        topLayout = self._FuxDialog().AddTopLayout( "Top", topBuilder )

    def _BuildCustomPane(self, paneName, customLayout):
        from DealPackageUxTraitsTabPane import TraitsPane
        fuxLayoutBuilder = acm.FUxLayoutBuilder()
        customPane = TraitsPane(self, paneName)
        customPane.BuildPaneLayout(fuxLayoutBuilder, customLayout) 
        if self._UseTabbedDialog():
            layout = self._FuxDialog().AddPane( paneName, fuxLayoutBuilder ) 
        else:
            layout = self._FuxDialog().AddTopLayout( paneName, fuxLayoutBuilder )
            self._SetFuxTopLayout(layout)
        customPane.AddLayoutToBindingsAndInitControls(layout)
        self._GUIPanes().Add(customPane)
        return customPane

    def GetCustomControls(self, layout):
        if self.ApplyLabel():
            okButton = layout.GetControl('_ok_')
            okButton.AddCallback("Activate", self._OnButtonClicked, self ) 

        if self.AddSlimDetailControl():
            self.m_slimDetailButton = layout.GetControl('_slimDetail_')
            self.m_slimDetailButton.AddCallback("Activate", self._OnSlimDetailClicked, self )
            self._UpdateSlimDetailLabel()
    
    def _UpdateTraitsTabValues(self):
        for customPane in self._GUIPanes():
            customPane.HandleOnIdle()
            
    def _OnButtonClicked(self, notUsed1, notUsed2):
        self._FuxDialog().CloseDialogOK()
        
    def _OnSlimDetailClicked(self, notUsed1, notUsed2):
        self.DealPackage().GetAttribute('toggleAllShowModes')()
        self._UpdateSlimDetailLabel()

    def _UpdateSlimDetailLabel(self):
        if self.m_slimDetailButton:
            label = self.DealPackage().GetAttributeMetaData('toggleAllShowModes', 'label')()
            self.m_slimDetailButton.Label(label)
        
    def _GUIPanes(self):
        return self.m_GUIPanes
        
    def _GetCustomPaneInfos(self):
        self.m_paneInfos = []
        customPaneInfos = self.CustomPanes()
        customPaneInfos = WrapAsTabControlList(customPaneInfos)
        for tabsInfo in customPaneInfos:
            tabContolName, tabControlLayout = UnpackPaneInfo(tabsInfo)
            for paneInfo in tabControlLayout:
                self.m_paneInfos.append(paneInfo)
        
    def _UseTabbedDialog(self):
        return self.m_paneInfos and len(self.m_paneInfos) > 1
    
class DealPackageAttributeDialog(DealPackageDialog):
    def __init__(self, dealPackage, caption, customPanes, btnLabel = 'Close'):
        DealPackageDialog.__init__(self, dealPackage)
        self._caption = caption
        self._customPanes = customPanes
        self._btnLabel = btnLabel
    
    def Caption(self):
        return self._caption
    
    def CustomPanes(self):
        return self._customPanes
        
    def NoButtonMode(self):
        return not self.BtnLabel()
        
    def BtnLabel(self):
        return self._btnLabel
                
    def ApplyLabel(self):
        return self.BtnLabel()
    
    def CancelLabel(self):
        return None
    
    def AddSlimDetailControl(self):
        return False
    
    def HandleApply(self):
        dp = self.DealPackage()        
        return True

class UXDialogsWrapper(object):
    def __init__(self, function, *args):
        self._args = args
        self._function = function
    
    def ShowDialog(self, shell):
        return self._function(shell, *self._args)
        

""" Compiled: 2020-09-18 10:38:54 """

#__src_file__ = "extensions/SalesTrading/./etc/FSalesActivityUx.py"
"""-------------------------------------------------------------------------------------------------------
MODULE
    FSalesActivityUx

    (c) Copyright 2014 SunGard FRONT ARENA. All rights reserved.

DESCRIPTION

-------------------------------------------------------------------------------------------------------"""
import acm, FSheetUtils, FUxCore, FSalesTradingMenuItem
from EditObjectUx import EditObjectUx

'''*********************************************************************
*
* Edit Object Ux
*
*********************************************************************'''
class SalesActivityUx(EditObjectUx):

    def __init__(self):
        self.diaryPane = None
        self.editObjectDiary = None
        self.pricingPane = None
        self.showDiary = True
        EditObjectUx.__init__(self)
        
    def RegisterCustomCommands(self):
        
        commands = [
                    ['diary',               'View', 'Diary',         'Show Diary',              '',      '',     self.DiaryCb,                  False ],
                    ['editDiary',           'View', 'Edit Diary',    'Edit Diary',              '',      '',     self.EditDiaryCb,              False ],
                    ['calculateVolatility', 'View', 'Calculate',     'Calculate Volatility',    '',      '',     self.CalculateVolCb,           False ],
                    ['contact',             'View', 'Contact',       'Open Contact',            '',      '',     self.ContactCb,                False ],
                    ['counterparty',        'View', 'Counterparty',  'Open Counterparty',       '',      '',     self.CounterpartyCb,           False ],
                    ['instrument',          'View', 'Instrument',    'Open Instrument',         '',      '',     self.InstrumentCb,             False ],
                    ['viewProtection',      'View', 'Protection',    'View Protection',         '',      '',     self.ViewProtectionCb,         False ],
                    ['trade',               'View', 'Trade',         'Open Trade',              '',      '',     self.TradeCb,                  False ],
                    ['inspector',           'View', 'Properties',    'Open Inspector',          '',      '',     self.InspectorCb,              False ]
        ]         
        return commands
        
    def OnFileAdvancedOpenEnabled(self):
        return False
    
    def DiaryCb(self):
        return FSalesTradingMenuItem.DiaryMenuItem(self)
        
    def EditDiaryCb(self):
        return FSalesTradingMenuItem.EditDiaryMenuItem(self)
        
    def InstrumentCb(self):
        return FSalesTradingMenuItem.SalesActivityOpenAttribute(self, 'instrument')
        
    def ContactCb(self):
        return FSalesTradingMenuItem.SalesActivityContact(self)
    
    def CalculateVolCb(self):
        return FSalesTradingMenuItem.SalesActivityVolatilityMenuItem(self)
    
    def CounterpartyCb(self):
        return FSalesTradingMenuItem.SalesActivityOpenAttribute(self, 'counterparty')
        
    def InspectorCb(self):
        return FSalesTradingMenuItem.InspectorMenuItem(self)
        
    def TradeCb(self):
        return FSalesTradingMenuItem.SalesActivityOpenAttribute(self, 'underlyingTrade')
        
    def ViewProtectionCb(self):
        return FSalesTradingMenuItem.ViewProtection(self)
        
    def AddPricingPane(self, layout):
        self.pricingPane = SalesActivityPricingPane(self)
        layout = layout.AddPane(
                self.pricingPane.CreateLayout(), self.pricingPane.KEY)
        self.pricingPane.HandleCreate(layout)
        salesActivity = self.UnDecorate(self.DealPackage().Object())
        self.pricingPane.Insert(salesActivity)
        
    def AddDiaryPane(self):
        self.diaryPane = SalesActivityDiaryPane(self)
        self.Frame().CreateCustomDockWindow(self.diaryPane, self.diaryPane.KEY,
            self.diaryPane.CAPTION, self.diaryPane.POSITION, None,
            self.diaryPane.STRECH, False)
            
    def UpdatePanels(self, diary=None):
        if diary:
            self.editObjectDiary = diary
        else:
            editObjectDiary = self.DealPackage().GetAttribute('salesActivityPanel_diary')
            self.editObjectDiary = editObjectDiary
    
        if self.diaryPane and self.pricingPane:
            self.diaryPane.UpdateDiary(self.editObjectDiary)
            salesActivity = self.UnDecorate(self.DealPackage().Object())
            self.pricingPane.Insert(salesActivity)
   
    def OnFileSave(self):
        diary = self.DealPackage().GetAttribute('salesActivityPanel_diary')
        EditObjectUx.OnFileSave(self)
        self.UpdatePanels(diary)
        
    def OnFileSaveNew(self):
        self.diaryPane.OnSaveNew()
        EditObjectUx.OnFileSaveNew(self)
        self.UpdatePanels()
        
    def OnFileNew(self):
        salesActivity = acm.FSalesActivity()
        self.HandleObject(salesActivity)
        
    def OnFileDelete(self):
        EditObjectUx.OnFileDelete(self)
        self.UpdatePanels()
        
    def SetNewDiary(self, diary):
        self.editObjectDiary = diary
        self.DealPackage().SetAttribute('salesActivityPanel_diary', diary)
        self.DealPackage().Object().Touch()
        self.DealPackage().Changed()
        
    def HandleObject(self, obj):
        EditObjectUx.HandleObject(self, obj)
        self.UpdatePanels()
        
    def UnDecorate(self, acmObj):
        if hasattr(acmObj, 'DecoratedObject'):
            return acmObj.DecoratedObject()
        return acmObj
        
    def HandleSetContents(self, contents ):
        EditObjectUx.HandleSetContents(self, contents)
        
    def ShowDiary(self):
        if self.showDiary:
            self.Frame().ShowDockWindow(self.diaryPane.KEY, True)   

    def HandleShowDiary(self):
        if self.DealPackage().GetAttribute('salesActivityPanel_type') == 'Note':
            self.ShowDiary()
            self.showDiary = False
        else:
            self.showDiary = True
        
    def HandleOnIdle(self):
        self.HandleShowDiary()
        EditObjectUx.HandleOnIdle(self)

    def HandleCreate(self, layout):
        EditObjectUx.HandleCreate(self, layout)
        self.AddDiaryPane()
        self.AddPricingPane(layout)
        self.UpdatePanels()
        
    def HandleActiveView(self, *args):
        pass
        
    def HandleViewTypes(self, *args):
        pass

'''*********************************************************************
*
* CreateApplicationInstance
*
*********************************************************************'''
def CreateApplicationInstance():
    return SalesActivityUx()


class SalesActivityPricingPane(FUxCore.LayoutPanel):

    EXT_NAME = 'SalesActivityApplication_DefaultColumns'
    
    KEY = 'SalesActivityPricingPane'
    HEIGHT = 50

    def __init__(self, parent):
        self.parent = parent
        self.sheet = None
    
    def Insert(self, salesActivity):
        self.sheet.RemoveAllRows()
        self.sheet.InsertObject(salesActivity, 0)
        
    def InitSheetSettings(self):
        self.sheet.ShowGroupLabels(False)
        self.sheet.ShowRowHeaders(False)

    def Setup(self):
        setup = FSheetUtils.CreateSheetSetup()
        columnIds = FSheetUtils.ColumnIds(self.EXT_NAME, 'FSalesActivitySheet')
        setup.ColumnCreators(FSheetUtils.ColumnCreators(columnIds))
        return setup
        
    def CreateLayout(self):
        b = acm.FUxLayoutBuilder()
        b.BeginHorzBox()
        b. AddCustom('sheet', 'sheet.FSalesActivitySheet', -1, self.HEIGHT, -1, -1, 
            FSheetUtils.Contents(self.Setup()))
        b.EndBox()
        return b
        
    def SetupControls(self):
        sheetCtrl = self.layout.GetControl('sheet')
        self.sheet = sheetCtrl.GetCustomControl()
        
    def HandleCreate(self, layout):
        self.layout = layout
        self.SetupControls()
        self.InitSheetSettings()
        

class SalesActivityDiaryPane(FUxCore.LayoutPanel):

    KEY = 'SalesActivityDiary'
    CAPTION = ''
    POSITION = 'Right'
    STRECH = False
    SHOW_INITIALY = False
    GREY = None

    def __init__(self, parent):
        self.parent = parent
        self.historyCtrl = None
        self.diaryCtrl = None
        self.diary = None

    def OnSaveNew(self):
        if self.diary and not self.diary.Originator().IsInfant():
            text = self.diaryCtrl.GetData()
            if text:
                self.SetNewDiary(self.Header() + text)
            else:
                self.parent.SetNewDiary(None)

    def OnDiaryChanged(self, cd, params):
        self.SetNewDiary(self.AddToDiary())
        
    def OnHistoryChanged(self, cd, params):
        self.SetNewDiary(self.historyCtrl.GetData())
        
    def SetNewDiary(self, diaryText):
        if self.diary is None:
            self.diary = acm.FSalesActivityDiary()
        elif not (self.diary.IsInfant() or self.diary.IsStorageImage()):
            self.diary = self.diary.StorageImage()
        timeNow = acm.Time.RealTimeNow()
        self.diary.Name('Diary{0}'.format(timeNow))
        self.diary.Text(diaryText)
        self.parent.SetNewDiary(self.diary)

    def Header(self):
        timeNow = acm.Time.RealTimeNow()
        return '{0} {1}\n'.format('[' + acm.UserName() + ']', timeNow[:-4])
        
    def AddToDiary(self):
        newEntry = ''.join((
            self.Header(),
            self.diaryCtrl.GetData(), 2*'\n',
            self.historyCtrl.GetData()))
        return newEntry
        
    def SetupControls(self, layout):
        self.historyCtrl = layout.GetControl('history')
        self.historyCtrl.Editable(False)
        self.historyCtrl.SetColor('BackgroundReadonly', self.Grey())
        self.historyCtrl.AddCallback('Changed', self.OnHistoryChanged, None)
        self.diaryCtrl = layout.GetControl('diary')
        self.diaryCtrl.SetColor('BackgroundReadonly', self.Grey())
        self.diaryCtrl.AddCallback('Changed', self.OnDiaryChanged, None)

    def HandleCreate(self):
        # pylint: disable-msg=W0221
        layout = self.SetLayout(self.CreateLayout()) # pylint: disable-msg=E1101
        self.SetupControls(layout)
        self.UpdateDiary(self.diary)
    
    def CreateLayout(self):
        b = acm.FUxLayoutBuilder()
        b.BeginVertBox('None')
        b.  BeginVertBox('None')
        b.    AddText('history', 280, 180)
        b.    AddText('diary', 280, 125)
        b.  EndBox()
        b.EndBox()
        return b
        
    def ChangeActiveField(self, activateCtrl=None, deactivateCtrl=None):
        try:
            if activateCtrl is None:
                activateCtrl = self.diaryCtrl if self.historyCtrl.Editable() else self.historyCtrl
                deactivateCtrl = self.historyCtrl if self.historyCtrl.Editable() else self.diaryCtrl
            activateCtrl.Editable(True)
            activateCtrl.SetFocus()
            deactivateCtrl.Editable(False)
        except AttributeError:
            pass
        
    def ClearDiary(self):
        try:
            self.historyCtrl.Clear()
            self.diaryCtrl.Clear()
        except AttributeError:
            pass
        
    def UpdateDiary(self, diary):
        self.ClearDiary()
        self.diary = diary
        if diary and self.historyCtrl:
            self.historyCtrl.SetData(diary.Text())
        self.ChangeActiveField(self.diaryCtrl, self.historyCtrl)

    @classmethod
    def Grey(cls):
        if cls.GREY is None:
            cls.GREY = acm.GetDefaultContext().GetExtension(
                'FColor', 'FObject', 'BkgEvalClone').Value()
        return cls.GREY
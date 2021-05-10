import acm
import FUxCore

#-------------------------------------------------------------------------
class CreditBalancePortfolioView(FUxCore.LayoutPanel):
    
    COLUMNS = 'columns'

    def __init__(self, parent, defaultColumns=None):
        self.m_parent = parent
        self.m_portfolioSheet = None
        
        self.m_columnIds = defaultColumns if defaultColumns else []        
        self.m_creditBalance = None

    def GetContents(self):
        """ Called by UX framework when saving a workspace to obtain the LayoutPanels contents.
        """        
        contents = acm.FDictionary()
        contents[self.COLUMNS] = acm.FArray()
        
        columnCreators = self.m_portfolioSheet.ColumnCreators()
        
        i = 0
        while i < columnCreators.Size():
            creator = columnCreators.At(i)
            contents[self.COLUMNS].Add(creator.ColumnId())
            i += 1

        return contents

    def GetInitialContents(self):
        """ Use initial contents if any.
        """
        initialContents = self.InitialContents()
        if initialContents:
            self.m_columnIds = initialContents[self.COLUMNS]

    def UpdateColumns(self):
        self.RemoveColumns()
        self.InsertColumns()

    def RemoveColumns(self):
        columnCreators = self.m_portfolioSheet.ColumnCreators()
        while columnCreators.Size() > 0:
            creator = columnCreators.At(0)
            columnCreators.Remove(creator)
        
    def InsertColumns(self):
        creators = acm.GetColumnCreators(self.m_columnIds, acm.GetDefaultContext())
        i = 0
        while i < creators.Size():
            creator = creators.At(i)
            self.m_portfolioSheet.ColumnCreators().Add(creator)
            i = i + 1
    
    def UpdateSheetContent(self):
        creditBalance = self.GetSelectedCreditBalance()
        if creditBalance != self.m_creditBalance:
            self.m_creditBalance = creditBalance
            self.m_portfolioSheet.RemoveAllRows()
            self.InsertCreditBalancePortfolioInSheet()
    
    def GetSelectedSheetCell(self):
        sheet = self.m_parent.ActiveSheet()
        if sheet:
            selection = sheet.Selection()
            if selection:
                return selection.SelectedCell()
                
    def GetRowObject(self):
        row = None 
        cell = self.GetSelectedSheetCell()
        if cell:
            row = cell.RowObject()
        return row       
    
    def GetSelectedCreditBalance(self):
        rowObject = self.GetRowObject()
        if rowObject:
            instrument = rowObject.Instrument()
            return instrument if instrument.Class() == acm.FCreditBalance else None
        else:
            return None
    
    def InsertCreditBalancePortfolioInSheet(self):
        adHocPortfolio = acm.FAdhocPortfolio(self.m_creditBalance.BalancePortfolio().Trades())
        adHocPortfolio.Name(self.m_creditBalance.Name())
        treeProxy = self.m_portfolioSheet.GridBuilder().InsertItem(adHocPortfolio)
        treeProxy.Expand(True)
    
    def ServerUpdate(self, sender, aspect, parameter ):
        pass

    def HandleCreate(self):
        layout = self.SetLayout( self.CreateLayout() )
        self.GetInitialContents()
        
        self.m_portfolioSheet = layout.GetControl('sheet').GetCustomControl()
        self.m_portfolioSheet.ShowGroupLabels(False)
        
        self.UpdateSheetContent()
        self.UpdateColumns()
        
        self.Owner().AddDependent(self)
        
    def HandleDestroy(self):
        self.Owner().RemoveDependent(self)

    def CreateLayout(self):
        b = acm.FUxLayoutBuilder()
        b.BeginVertBox()
        b.    AddCustom('sheet', 'sheet.FPortfolioSheet', 125, 125)
        b.EndBox()
        return b

#-------------------------------------------------------------------------
class CreditBalancePortfolioMenuItem(FUxCore.MenuItem):
    def __init__(self, extObj, dockWindowCaption, dockWindowType, dockWindowKey):
        self.m_extObj = extObj
        self.m_dockWindowCaption = dockWindowCaption
        self.m_dockWindowType = dockWindowType
        self.m_dockWindowKey = dockWindowKey
        
    def IsMenuEnabled(self, extObj):
        applicable = False
        
        try:
            instrument = extObj.ActiveSheet().Selection().SelectedCell().RowObject().Instrument()
            
            if instrument and (instrument.Class() == acm.FCreditBalance):
                applicable = True
        except:
            pass
            
        return applicable
            
    def Invoke(self, eii):
        basicApp = eii.ExtensionObject()
        if self.IsMenuEnabled(basicApp):
            try :
                basicApp.ShowDockWindow(self.m_dockWindowKey, True)
            except Exception as e:
                basicApp.CreateRegisteredDockWindow(self.m_dockWindowType, self.m_dockWindowKey, self.m_dockWindowCaption, 'Bottom', True, True, False, True)
                
            customDockWindow = basicApp.GetCustomDockWindow(self.m_dockWindowKey)
            customDockWindow.CustomLayoutPanel().UpdateSheetContent()

    def Applicable(self):
        return True

    def Enabled(self):
        return self.IsMenuEnabled(self.m_extObj)

'''================================================================================================
midas trades in front
running total fixes
recon fix
USD/ZAR NB
This get trades from Midas but what about getting the trades from Front ?
the proplem comes in that the values are so different  ? may use a tolerance ???
================================================================================================'''
import acm
import ael
import re
import pyodbc as odbc
import FUxCore
'''================================================================================================
================================================================================================'''
columns =\
['RECI', 'DLNO', 'RCDT', 'RCDC', 'CNUM', 'BRCD', 'DTYP', 'DLST', 'DDAT', 'VDAT', 'OTDT', 'ZZ002', 'BRKC', 'BAGE', 'PUCY', 'PUAM', 'EXRT', 'ZZ023',
'SLCY', 'SLAM', 'ZZ021', 'BCEQ', 'OBCE', 'LCXR', 'PCST', 'OPCA', 'TSCN', 'SCST', 'OSCA', 'TPCN', 'ZZ006', 'ORPA', 'ZZ006A', 'ORSA', 'FSLI', 'LITD',
'LILA', 'DITD', 'DILA', 'SPPD', 'SPLA', 'SPLC', 'ILCY', 'ILAM', 'IDCY', 'IDAM', 'IDIA', 'SODN', 'ZZ009', 'FACO', 'SPI', 'ZZ002A', 'VBCD', 'VCAT1',
'VCAT2', 'VCAT3', 'DKNO', 'SBNK', 'ZZ004', 'DNSI', 'DSTI', 'CNFI', 'ACEI', 'TLXI', 'ZZ007', 'ILCM', 'IDCM', 'ZZ001A', 'LSWC', 'LSWS', 'ZZ002B', 'ORED', 'LCD', 'CHTP', 'TNLU']
listColumns = ['DealNo', 'Rec', 'Type', 'TradeDate', 'ValueDate', 'Currecny1', 'Amount1', 'Rate', 'Currecny2', 'Amount2', 'Portfolio', 'Broker']
'''================================================================================================
================================================================================================'''
def ReallyStartDialog(shell):
    builder = CreateLayout()
    customDlg = myCustomDialog()
    acm.UX().Dialogs().ShowCustomDialogModal(shell, builder, customDlg )
'''================================================================================================
================================================================================================'''
def StartDialog(eii):
    shell = eii.ExtensionObject().Shell()
    ReallyStartDialog(shell);
'''================================================================================================
================================================================================================'''
def OnListButtonPressed(self, cd ):
    self.m_list.RemoveAllItems()
    self.GetMidasTrades(self.m_inputMidasNo.GetData())
    
def Format(val, dec): return re.sub("(\d)(?=(\d{3})+(?!\d))", r"\1,", "%s" % round(val, dec))
'''================================================================================================
================================================================================================'''
class myCustomDialog (FUxCore.LayoutDialog):

    def __init__(self):
        self.m_list = 0
        #self.TradeDict = {}
        
        self.TradeDict = acm.FDictionary() 
        self.julianDate = '1971-12-31'
        self.PROD = 'JHBPCM05015v05a\FXB_MAIN1_LIVE'
        self.UAT = 'JHBPSM05017\FXB_MAIN1_UAT'
        self.SQLConnection = None

    def GetMidasTrades(self, midsno):
    
        self.TradeDict.Clear()
        SQLConnection = None
        if SQLConnection == None:
            connectionString = 'DRIVER={SQL Server};SERVER=%s;DATABASE=%s' % (self.PROD, 'MMG_FXF') 
            sqlConnection = odbc.connect(connectionString, autocommit=True) 
            SQLConnection = sqlConnection.cursor() 
    
        resultSet = SQLConnection.execute("SELECT * FROM OPENQUERY (MIDAS, 'SELECT * FROM MIDDBLIB/DEALSDB WHERE DLNO IN (%s) ORDER BY DDAT DESC')"  % midsno).fetchall()   
        for x in resultSet:
            TradeDate = acm.Time.DateAdjustPeriod(self.julianDate, str(x[8])+ 'd') 
            values = []
            [values.append(str(c)) for c in x]
            self.TradeDict[TradeDate] = values
 
        resultSet = SQLConnection.execute("SELECT * FROM OPENQUERY (MIDAS, 'SELECT * FROM MIDDBLIB/DEALSDBH WHERE DLNO IN (%s) ORDER BY DDAT DESC')"  % midsno).fetchall()   
        for x in resultSet:
            TradeDate = acm.Time.DateAdjustPeriod(self.julianDate, str(x[8])+ 'd') 
            values = []
            [values.append(str(c)) for c in x]
            self.TradeDict[TradeDate] = values

        SQLConnection.close()
        
        rootItem = self.m_list.Clear()
        rootItem = self.m_list.GetRootItem()

        for trade in self.TradeDict.Keys().Sort():#.FIndexedCollection.SortByProperty()
            DealDate = acm.Time.DateAdjustPeriod(self.julianDate, self.TradeDict[trade][columns.index('DDAT')]+'d')
            ValDate = acm.Time.DateAdjustPeriod(self.julianDate, self.TradeDict[trade][columns.index('VDAT')]+'d')
            Amount1 = Format(float(self.TradeDict[trade][columns.index('PUAM')])/1000, 6)
            Amount2 = Format(float(self.TradeDict[trade][columns.index('SLAM')])/1000, 6)
            
            child = rootItem.AddChild()
            child.Label(self.TradeDict[trade][columns.index('DLNO')])
            child.Label(self.TradeDict[trade][columns.index('RECI')], 1)
            child.Label(self.TradeDict[trade][columns.index('DTYP')], 2)
            child.Label(DealDate, 3)
            child.Label(ValDate, 4)
            child.Label(self.TradeDict[trade][columns.index('PUCY')], 5)
            child.Label(Amount1, 6)
            child.Label(self.TradeDict[trade][columns.index('EXRT')], 7)
            child.Label(self.TradeDict[trade][columns.index('SLCY')], 8)
            child.Label(Amount2, 9)
            child.Label(self.TradeDict[trade][columns.index('VCAT2')], 10)
            child.Label(self.TradeDict[trade][columns.index('BRKC')], 11)
 
 
 
        self.m_list.AdjustColumnWidthToFitItems(0)
        self.m_list.AdjustColumnWidthToFitItems(1)
        self.m_list.AdjustColumnWidthToFitItems(2)
        self.m_list.AdjustColumnWidthToFitItems(3)
        self.m_list.AdjustColumnWidthToFitItems(4)
        self.m_list.AdjustColumnWidthToFitItems(5)
    
    def HandleCreate( self, dlg, layout):
        self.m_fuxDlg = dlg
        self.m_fuxDlg.Caption('Midas Trades')
        self.m_list = layout.GetControl('items')
        self.m_listButton = layout.GetControl('refreshButton')
        self.m_inputMidasNo = layout.GetControl('midsNo')   
        self.m_inputMidasNo.SetData(421136)
        self.m_list.ShowGridLines()
        self.m_list.ShowColumnHeaders()
        self.m_list.SetColor("Text", acm.UX().Colors().Create(255, 255, 255) )
        self.m_list.SetColor("Foreground", acm.UX().Colors().Create(0, 36, 89) )

        for column in listColumns:
            self.m_list.AddColumn(column, -1, column)
        self.m_listButton.AddCallback("Activate", OnListButtonPressed, self)


def CreateLayout():
    b = acm.FUxLayoutBuilder()
    b.BeginHorzBox('None')
    b.          BeginVertBox('None')
    b.          BeginHorzBox('None')
    b.                  AddInput("server", "Server", 10)      
    b.                  AddInput("midsNo", "Midas Number", 10)      
    b.          EndBox()    
    b.                  AddList("items", 20, -1, 200)
    b.                  BeginHorzBox('None')
    b.                          AddFill()
    b.                          AddButton("refreshButton", "Refresh")
    b.                  EndBox()
    b.          EndBox()
    b.EndBox()
    return b

ReallyStartDialog( acm.UX().SessionManager().Shell())


def Run(eii):
    ReallyStartDialog(eii.ExtensionObject().Shell())
    


















'''================================================================================================
#import clr
#clr.AddReference("System.Windows.Forms.DataVisualization")
================================================================================================'''
import acm
import FUxCore
import re
from FxTimeBuckets import TimeBucket #must cache these
myPanel = None
'''================================================================================================
================================================================================================'''
def USDAmount(trade):
    if trade.Instrument().Name() == 'USD': return trade.Quantity() 
    if trade.Currency().Name() == 'USD': return trade.Premium()
    return 0 
'''================================================================================================
================================================================================================'''
def Curr1Amount(trade): return trade.Quantity() if trade.IsInverse() == False else trade.Premium()
def Curr2Amount(trade): return trade.Premium() if trade.IsInverse() == False else trade.Quantity()
def Format(val, dec): return re.sub("(\d)(?=(\d{3})+(?!\d))", r"\1,", "%d" % round(val, dec))
def Format2(val, dec): 
    if val != None: return Format(val, dec)
'''================================================================================================
================================================================================================'''
USDPOS = 0
CURR1POS = 1
CURR2POS = 2
AVEPRICE = 3
AVEPRICEINV = 4
TRADECOUNT = 5
'''================================================================================================
================================================================================================'''
def AddAmountToCurrencyInBasket(dict, trade): 

    Curr1 = trade.Instrument().Name()
    Curr2 = trade.Currency().Name()
    Bucket = TimeBucket(trade)

    if dict.HasKey(Curr1):
        BucketDict = dict.At(Curr1)
        if BucketDict.HasKey(Bucket):
            BucketDict[Bucket] +=  trade.Quantity() 
        else: 
            BucketDict[Bucket] = trade.Quantity()
        if BucketDict.HasKey(Bucket):
            BucketDict['TOTAL'] +=  trade.Quantity() 
        else: 
            BucketDict['TOTAL'] = trade.Quantity()
    else:
        dict.AtPut(Curr1, {Bucket:trade.Quantity()})
        dict.At(Curr1).AtPut('TOTAL', trade.Quantity())

    if dict.HasKey(Curr2):
        BucketDict = dict.At(Curr2)
        if BucketDict.HasKey(Bucket):
            BucketDict[Bucket] +=  trade.Premium() 
        else: 
            BucketDict[Bucket] = trade.Premium()
        if BucketDict.HasKey(Bucket):
            BucketDict['TOTAL'] +=  trade.Premium() 
        else: 
            BucketDict['TOTAL'] = trade.Premium()
    else:
        dict.AtPut(Curr2, {Bucket:trade.Premium()})
        dict.At(Curr2).AtPut('TOTAL', trade.Premium())
    return dict

'''================================================================================================
================================================================================================'''
def SelectionChanged(eii, b):
   
    #myPanel = uiTrdMngr.GetProperty('RunningTotal')
    global myPanel
    
    if myPanel != None:

        uiTrdMngr = eii.ExtensionObject()
        active_sheet = uiTrdMngr.ActiveSheet()  
        tradeDict = acm.FDictionary()
        bucketDict = acm.FDictionary() 

        if active_sheet != None:
        
            rowObjects = active_sheet.Selection().SelectedRowObjects()  #what if we selct more then one currency
            
            if  myPanel.m_list != None: 
                myPanel.m_list.Clear()
                
                if rowObjects.Size() > 0:
                    tradeDict.Clear()
                    trades = acm.FSet()
                    if myPanel.m_voidtrades.Checked() == True:
                       [trades.AddAll(row.Trades()) for row in rowObjects]
                    else:
                        for row in rowObjects:
                            for t in row.Trades():
                                if t.Status() != 'Void': trades.Add(t)
                    
                    TotalUSDAmount = 0.00  
                    
                    for trade in trades:
                    
                        if trade.Instrument().InsType() == 'Curr':
                        
                            AddAmountToCurrencyInBasket(bucketDict, trade) 
                            
                            USD = USDAmount(trade)
                            TotalUSDAmount = TotalUSDAmount + USD
                 
                            if trade.CurrencyPair() != None:
                                Curr1 = Curr1Amount(trade)
                                Curr2 = Curr2Amount(trade)
                                if trade.IsInverse() == True:
                                    Price = 1/trade.Price() if trade.Price() != 0 else trade.Price() 
                                else:
                                    Price = trade.Price()
                                    
                                if tradeDict.HasKey(trade.CurrencyPair().Name()):
                                    properties = tradeDict.At(trade.CurrencyPair().Name())
                                    properties = [ properties[USDPOS]+USD, properties[CURR1POS]+Curr1, properties[CURR2POS]+Curr2, properties[AVEPRICE]+Price, 0, properties[TRADECOUNT]+1 ]  
                                else:
                                
                                    properties = [USD, Curr1, Curr2, Price, 0, 1]
                                tradeDict.AtPut(trade.CurrencyPair().Name(), properties)
     
                    myPanel.m_usdamount.SetData(Format(TotalUSDAmount, 2))
                    rootItem = myPanel.m_list.GetRootItem()
                    
                    for cp in tradeDict.Keys(): #CurrencyPair Key
                    
                        child = rootItem.AddChild()
                        USD = Format(tradeDict.At(cp).At(USDPOS), 2)
                        Curr1 = Format(tradeDict.At(cp).At(CURR1POS), 2)
                        Curr2 = Format(tradeDict.At(cp).At(CURR2POS), 2)
                        Count = tradeDict.At(cp).At(TRADECOUNT)
                        Ave = tradeDict.At(cp).At(AVEPRICE)
                        AveIn = 0
                        if Ave != 0: 
                            Ave = round(Ave/Count, 6)
                            AveIn = round(1/Ave, 6)                  
                        child.Label(cp)                                          
                        child.Label(USD, USDPOS+1)    
                        child.Label(Curr1, CURR1POS+1)             
                        child.Label(Curr2, CURR2POS+1)             
                        child.Label(Ave, AVEPRICE+1)             
                        child.Label(AveIn, AVEPRICEINV+1)        
                        child.Label(Count, TRADECOUNT+1)    

                    myPanel.m_list.AdjustColumnWidthToFitItems(0)
                    myPanel.m_list.AdjustColumnWidthToFitItems(1)
                    myPanel.m_list.AdjustColumnWidthToFitItems(2)
                    myPanel.m_list.AdjustColumnWidthToFitItems(3)
                    myPanel.m_list.AdjustColumnWidthToFitItems(4)
                    myPanel.m_list.AdjustColumnWidthToFitItems(5)
                    myPanel.m_list.AdjustColumnWidthToFitItems(6)
                    
                    myPanel.m_buckets.Clear()
                    rootItem = myPanel.m_buckets.GetRootItem()
                    
                    for currency in bucketDict.Keys().Sort(): #Currency Key
                        child = rootItem.AddChild()
                        child.Label(currency)

                        TOTAL = Format2(bucketDict.At(currency).At('TOTAL'), 2)
                        SPOT = Format2(bucketDict.At(currency).At('SPOT'), 2)
                        CASH = Format2(bucketDict.At(currency).At('CASH'), 2)
                        TOM = Format2(bucketDict.At(currency).At('TOM'), 2)
                        TODAY = Format2(bucketDict.At(currency).At('TODAY'), 2)
                        SPOTNEXT = Format2(bucketDict.At(currency).At('SPOT NEXT'), 2)
                        ONEW = Format2(bucketDict.At(currency).At('1W'), 2)
                        TWOW = Format2(bucketDict.At(currency).At('2W'), 2)
                        ONEM = Format2(bucketDict.At(currency).At('1M'), 2)
                        THREEM = Format2(bucketDict.At(currency).At('3M'), 2)
                        SIXM = Format2(bucketDict.At(currency).At('6M'), 2)
                        NINEM = Format2(bucketDict.At(currency).At('9M'), 2)
                        TWELVEM = Format2(bucketDict.At(currency).At('12M'), 2)
                        EIGHTEENM = Format2(bucketDict.At(currency).At('18M'), 2)
                        TWENTYFOURM = Format2(bucketDict.At(currency).At('24M'), 2)
                        REST = Format2(bucketDict.At(currency).At('REST'), 2)
                                         
                        child.Label(TOTAL, 1)    
                        child.Label(SPOT, 2)    
                        child.Label(CASH, 3)             
                        child.Label(TOM, 4)             
                        child.Label(TODAY, 5)             
                        child.Label(SPOTNEXT, 6)        
                        child.Label(ONEW, 7)   
                        child.Label(TWOW, 8)   
                        child.Label(ONEM, 9)   
                        child.Label(THREEM, 10)   
                        child.Label(SIXM, 11)   
                        child.Label(NINEM, 12)   
                        child.Label(TWELVEM, 13)   
                        child.Label(EIGHTEENM, 14)   
                        child.Label(TWENTYFOURM, 15) 
                        child.Label(REST, 16)     
                    
                    myPanel.m_buckets.AdjustColumnWidthToFitItems(0)
                    myPanel.m_buckets.AdjustColumnWidthToFitItems(1)
                    myPanel.m_buckets.AdjustColumnWidthToFitItems(2)
                    myPanel.m_buckets.AdjustColumnWidthToFitItems(3)
                    myPanel.m_buckets.AdjustColumnWidthToFitItems(4)
                    myPanel.m_buckets.AdjustColumnWidthToFitItems(5)
                    myPanel.m_buckets.AdjustColumnWidthToFitItems(6)
                    myPanel.m_buckets.AdjustColumnWidthToFitItems(7)
                    myPanel.m_buckets.AdjustColumnWidthToFitItems(8)
                    myPanel.m_buckets.AdjustColumnWidthToFitItems(9)
                    myPanel.m_buckets.AdjustColumnWidthToFitItems(10)
                    myPanel.m_buckets.AdjustColumnWidthToFitItems(11)
                    myPanel.m_buckets.AdjustColumnWidthToFitItems(12)
                    myPanel.m_buckets.AdjustColumnWidthToFitItems(13)
                    myPanel.m_buckets.AdjustColumnWidthToFitItems(14)
                    myPanel.m_buckets.AdjustColumnWidthToFitItems(15)
'''================================================================================================
================================================================================================'''
class FUX_FXToolsDockWindow (FUxCore.LayoutPanel):

    def __init__(self, parent):
        self.m_parent = parent
        self.m_shell = parent.Shell()
        self.layout = None  
        self.m_list = None
        self.m_usdamount = None
        self.m_buckets = None

    def HandleCreate( self ):
        #self.m_list.SetAlignment('Right')
        #self.m_list.SetColor("Foreground", 'FxBlotterLightBlue' )
        #self.m_chart = clr.System.Windows.Forms.DataVisualization.Charting.Chart()
        #self.m_graph = self.layout.GetControl('graph')
        self.layout = self.SetLayout( self.CreateLayout() )
        self.m_usdamount = self.layout.GetControl('usd')
        self.m_voidtrades = self.layout.GetControl('includeVoid')
        
        self.m_list = self.layout.GetControl('items')
        self.m_list.SetColor("Text", acm.UX().Colors().Create(255, 255, 255) )
        self.m_list.SetColor("Foreground", acm.UX().Colors().Create(0, 36, 89) )
        self.m_list.ShowGridLines([True])
        self.m_list.ShowColumnHeaders()
        self.m_list.AddColumn('Pair', -1)
        self.m_list.AddColumn('USD', -1)
        self.m_list.AddColumn('Curr1', -1)
        self.m_list.AddColumn('Curr2', -1)
        self.m_list.AddColumn('Ave Price', -1)
        self.m_list.AddColumn('Ave Price Inv', -1)
        self.m_list.AddColumn('Count', -1)

        self.m_buckets = self.layout.GetControl('buckets')
        self.m_buckets.SetColor("Text", acm.UX().Colors().Create(255, 255, 255) )
        self.m_buckets.SetColor("Foreground", acm.UX().Colors().Create(0, 36, 89) )
        self.m_buckets.ShowGridLines([True])
        self.m_buckets.ShowColumnHeaders()
        self.m_buckets.AddColumn('Curr', -1)
        self.m_buckets.AddColumn('Total', -1)
        self.m_buckets.AddColumn('Spot', -1)
        self.m_buckets.AddColumn('Cash', -1)
        self.m_buckets.AddColumn('Tom', -1)
        self.m_buckets.AddColumn('Today', -1)
        self.m_buckets.AddColumn('Spot Next', -1)
        self.m_buckets.AddColumn('1W', -1)
        self.m_buckets.AddColumn('2W', -1)
        self.m_buckets.AddColumn('1M', -1)
        self.m_buckets.AddColumn('3M', -1)
        self.m_buckets.AddColumn('6M', -1)
        self.m_buckets.AddColumn('9M', -1)
        self.m_buckets.AddColumn('12M', -1)
        self.m_buckets.AddColumn('18M', -1)
        self.m_buckets.AddColumn('24M', -1)
        self.m_buckets.AddColumn('Rest', -1)
        
    def CreateLayout( self ):
        b = acm.FUxLayoutBuilder()
        b.BeginVertBox()
        b.BeginHorzBox()
        b.    AddInput('usd', 'USD Total')
        b.    AddCheckbox('includeVoid', 'Include Void Trades')
        b.EndBox()    
        b.BeginVertBox()
        b.    AddList("items", 5, 50, 5, 10)
        b.EndBox()
        b.BeginVertBox()
        b.    AddList("buckets", 5, 50, 5, 10)
        b.EndBox()
        #b.BeginVertBox()
        #b.  Add2DChart('graph',420,50)
        #b.EndBox()
        b.EndBox()
        return b    
'''================================================================================================
================================================================================================'''
def OnCreate(eii):
    global myPanel
    fUiTrdMgrFrame = eii.ExtensionObject()
    myPanel = FUX_FXToolsDockWindow(fUiTrdMgrFrame) 
    fUiTrdMgrFrame.CreateCustomDockWindow(myPanel, 'RunningTotal', 'Running Total', 'Right', None, True, False)
    fUiTrdMgrFrame.WriteProperty('RunningTotal', myPanel)
'''================================================================================================
 
================================================================================================'''















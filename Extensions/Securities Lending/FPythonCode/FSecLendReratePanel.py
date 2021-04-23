""" Compiled: 2020-09-18 10:38:55 """

#__src_file__ = "extensions/SecuritiesLending/etc/FSecLendReratePanel.py"

"""------------------------------------------------------------------------------------------------
MODULE
    FSecLendReratePanel

    (c) Copyright 2017 FIS FRONT ARENA. All rights reserved.

DESCRIPTION
     Panel for Rerate functionality making use of FSecLendDealUtils.

------------------------------------------------------------------------------------------------"""

import acm
import FUxCore
import FSheetUtils
from ACMPyUtils import Transaction
from FPanel import Panel
from FEvent import EventCallback
from FSecLendRerate import LOGGER
import FSecLendRerate
import math
from numbers import Number
from collections import OrderedDict

BATCH_SIZE = 50

#REQUIRED_COLUMNS = ['Security Loan Fixing Value','Security Loan Fixing Date']


Rerate_Fee_Col = 'Security Loan Fixing Value'
Rerate_Date_Col = 'Security Loan Fixing Date'

REQUIRED_COLUMNS = [Rerate_Fee_Col, Rerate_Date_Col]

APPLY_RERATE_CMD = 'Rerate Apply'


class SecLendReratePanel(Panel):

    def __init__(self):
        super(SecLendReratePanel,self).__init__()
        self.m_processBtn = None
        self.m_fixingValBtn = None
        self.m_sheet = None
        self.m_sheetCtrl = None
        self.m_fuxDlg = None
        self.m_siats = None
        self.m_trades = None
        
    def ReactOnEvent(self):
        return True

    def GetApplyRerateExtension(self):
        return acm.GetDefaultContext().GetExtension('FCommandExtension', 'FUiTrdMgrFrame', APPLY_RERATE_CMD)
        
    
    def CreateLayout(self):
        b = acm.FUxLayoutBuilder()
        b.BeginVertBox('None')
        b.  BeginHorzBox('None')
        b.      BeginVertBox('None')
        b.          AddButton('Process',self.GetApplyRerateExtension().Value().GetString('RibbonLabel'),True,False)
        b.      EndBox()
        b.  EndBox()
        b.  AddCustom('sheet','sheet.FPortfolioSheet',740,200,-1,-1, self.SettingsContents())
        b.EndBox()
        return b
   
    def SettingsContents(self):
        return FSheetUtils.SheetContents(self.Settings()).ForControl()     
   
    def InitControls(self, layout):
        self.m_sheet = FSheetUtils.Sheet(layout.GetControl('sheet').GetCustomControl())
        self.InitProcessAllControl(layout)
    
    def InitProcessAllControl(self, layout):
        self.m_processBtn = layout.GetControl('Process')
        self.m_processBtn.ToolTip(self.GetApplyRerateExtension().Value().GetString('ToolTip'))
        self.m_processBtn.SetIcon(self.GetApplyRerateExtension().Value().GetString('icon'),False)
        self.m_processBtn.AddCallback('Activate', SecLendReratePanelController(self.m_sheet,Rerate_Fee_Col, Rerate_Date_Col).OnProcessButtonClicked,self)
    
    def CheckAndInsertColumns(self,columns):
        for column in columns:
            if not FSheetUtils.ColumnIsInSheet(self.m_sheet,column):
                FSheetUtils.AddColumn(self.m_sheet,column)
        
    def SingleInstrumentAndTradesFromSelection(self, selection):
        siats = acm.FArray()
        tradesByInstruments = OrderedDict()
        for rowObject in selection:
            if not rowObject.IsKindOf(acm.FPortfolioInstrumentAndTrades):
                for trd in rowObject.Trades():
                    tradesByInstruments.setdefault(trd.Instrument(),[]).append(trd) if self.IsValidTradeForRerate(trd) else None       
        for ins in tradesByInstruments:
            if self.IsValidForRerate(ins):
                portfolio = acm.FAdhocPortfolio()
                portfolio.AddAll(tradesByInstruments[ins])
                siatBuilder = acm.Risk.CreateSingleInstrumentAndTradesBuilder(portfolio,ins)
                siats.Add(siatBuilder.GetTargetInstrumentAndTrades())
        return siats

    @staticmethod
    def IsValidTradeForRerate(trd):
        import FSecLendHooks
        return FSecLendHooks.IsValidTradeForRerate(trd)

    @staticmethod
    def IsValidForRerate(ins):
        import FSecLendHooks
        return FSecLendHooks.IsValidForRerate(ins)
          
    @EventCallback
    def OnRerateButtonClicked(self,event):
        if self.IsVisible():
            self.Visible('False')
        else:
            self.Visible('True')
            siats = self.SingleInstrumentAndTradesFromSelection(event.SelectedRowObjects())
            self.PopulateSheet(siats)
                
    @EventCallback
    def OnPositionSelection(self,event):
        if self.IsVisible():
            siats = self.SingleInstrumentAndTradesFromSelection(event.SelectedRowObjects())
            self.PopulateSheet(siats)
            
    def PopulateSheet(self,selection):
        self.CheckAndInsertColumns(REQUIRED_COLUMNS)
        self.m_sheet.RemoveAllRows(True)
        self.m_sheet.InsertObject(selection,'IOAP_LAST')


class SecLendReratePanelController():

    def __init__(self,sheet,rerateFee,rerateDate):
        self.m_sheet = sheet
        self.m_rerate_fee = rerateFee
        self.m_rerate_date = rerateDate
    
    def CheckColumn(self,column):
        return FSheetUtils.ColumnIsInSheet(self.m_sheet,column)
        
    def OnProcessButtonClicked(self,*args):
        columnsId = [self.m_rerate_fee,self.m_rerate_date] 
        for column in columnsId:
            if not self.CheckColumn(column):
                acm.UX.Dialogs().MessageBoxInformation(self.Shell(), "Error in action: Column '{0}' is missing".format(column))
        values = self.GetValues(columnsId)
        RerateProcessing(values)


    # ---------   Utility functions for Get Rerate Fee & Rerate actions   ---------   
    
    def CleanInputColumn(self,column): 
        rowIterator =  self.m_sheet.RowTreeIterator(True)
        child = rowIterator.FirstChild()
        while child:
            columnIt = self.FindColumnIt( self.m_sheet,column)
            eval= self.m_sheet.GetCell(child,columnIt).Evaluator()
            eval.Value(None)
            child = child.NextSibling()
            
                        
    def GetValues(self,columnsId):
        # Util function that return a dictionary where:
        # Key = Name of the instrument
        # Value = Array with Fee, Date and Instrument
        rowIterator = self.m_sheet.RowTreeIterator(True)
        child = rowIterator.FirstChild()
        cellInfo = acm.FDictionary()
        while child:
            values = []
            for col in columnsId:
                columnIt = self.FindColumnIt(self.m_sheet,col)
                value = self.m_sheet.GetCell(child,columnIt).Value()
                values.append(value)
            if values:
                # Adding the instrument into the dictionary to improve the performance when reading  
                values.append(child.Tree().Item().Instrument())
                cellInfo.AtPut(child.Tree().StringKey(),values)
            child = child.NextSibling()
        return cellInfo

    @staticmethod
    def FindColumnIt(sheet, columnId):
        columnIt = acm.FDictionary()
        columnIterator = sheet.GridColumnIterator()
        def DoFindColumnIt(it,col):
            if it and it.GridColumn():
                if str(it.GridColumn().ColumnId()) == col:
                    return it
                else:
                    return DoFindColumnIt(it.Next(),col)
        first = columnIterator.First()
        return DoFindColumnIt(first,columnId)
                    

def SplitDictionary(dict, batch):
    #The function will create new dictionaries based on the batch size
    dict_iterator = iter(dict)
    
    for i in [dict_iterator[x:x+batch] for x in range(0, len(dict), batch)]:
        yield {k:dict[k] for k in i}

            
def RerateProcessing(values):
    
    LOGGER.info('--------------------------------------------------')
    LOGGER.info('Starting Rerating process for selected Instruments')
    LOGGER.info('--------------------------------------------------')

    keys = values.Keys()
    # First loop needs to ExtendOpenEnd instruments if necessary.
    # Need to be sure the instrument is extended before fixing a reset.
    # The instrument should have been already extended. This might be performance demanding.
    for key in keys:
        instrument = values[key][2].StorageImage()
        fee = values[key][0]
        dateTime = values[key][1]
        if (acm.Math.IsFinite(fee)) and (dateTime): 
            date = ConvertToDate(dateTime)
            LOGGER.info('Rerating {0} fee:{1}  date:{2}'.format(instrument.Originator().Name(), fee, date))
            try:
                rerate = FSecLendRerate.SecLendRerate(instrument, fee, date)
                rerate.ExtendSecurityLoan()
                rerate.DoRerate()
                rerate.SaveInstrument()
            except Exception as e:
                LOGGER.error('Error: "{0}"'.format(str(e)))
                return None

    LOGGER.info('Rerating process FINISHED')
    LOGGER.info('--------------------------------------------------')


def ConvertToDate(str):
    dateStr = str[0:10]
    return dateStr


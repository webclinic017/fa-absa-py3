""" Compiled: 2020-09-18 10:38:53 """

#__src_file__ = "extensions/PortfolioTrading/etc/FInstrumentView.py"
"""-------------------------------------------------------------------------------------------------
MODULE
    FInstrumentView

    (c) Copyright 2018 FIS FRONT ARENA. All rights reserved.

DESCRIPTION
    The button View Instrument creates a portfolio sheet that is instrument centric instead of 
    Portfolio centric by inserting a query for all trades on that instrument. By setting a
    compound portfolio in InstrumentViewSettings the query will be filtered by those portfolios.
    The new sheet will use a sheet template if est in the settings otherwise it will be based on the 
    currently used sheet.
-------------------------------------------------------------------------------------------------"""
import acm
import FSheetUtils
from FTradeProgramMenuItem import TradeProgramMenuItem
from FOpenPositionTM import OpenPositionDlg
from FTradeProgramAction import OpenPositionAction
from FTradeProgramTM import FTradeProgramTM
from FTradeCreator import DecoratedTradeCreator, TradeFromRowCreator
from FParameterSettings import ParameterSettingsCreator

def InstrumentView(eii):
    return InstrumentViewMenuItem(eii)

class InstrumentViewMenuItem(TradeProgramMenuItem):
    
    SETTINGS = ParameterSettingsCreator.FromRootParameter('InstrumentViewSettings')
    
    def _GetSelectedInstrument(self, eii):
        selectInsDialog = SelectInstrumentDialog(eii)
        return acm.UX().Dialogs().ShowCustomDialogModal(
            self._frame.Shell(),
            selectInsDialog.CreateLayout(),
            selectInsDialog
            )
    
    def _Portfolios(self):
        prtf = acm.FCompoundPortfolio[self.SETTINGS.CompoundPortfolio()]
        if prtf and prtf.IsKindOf(acm.FCompoundPortfolio):
            return prtf.AllPhysicalPortfolios()
        else:
            return self._PortfoliosInSheet(self._frame.ActiveSheet())
    
    def Invoke(self, eii):
        underlying_show, instrument = self._GetSelectedInstrument(eii)
        if instrument:
            portfolios = self._Portfolios()
            sheetCreator = InstrumentViewSheetCreator(eii, instrument, portfolios, self.SETTINGS.SheetTemplate(), underlying_show)
            sheet = sheetCreator.CreateSheet()
        
    @staticmethod
    def _PortfoliosInSheet(sheet):
        iter = sheet.RowTreeIterator(True).FirstChild()
        portfolios = []
        while iter:
            portfolios.append(TradeFromRowCreator.Portfolio(iter.Tree().Item()))
            iter = iter.NextSibling()
        return portfolios   
        
        
class SelectInstrumentDialog(OpenPositionDlg):
        
    def _InitControls(self, layout):
        self._InitInsTypeControl(layout)
        self._InitInsNameControl(layout)
        self._include_derivates = layout.GetControl('include_derivates')
        self._SetStartingValues()
    
    def _SetStartingValues(self):
        ins = self._SelectedInstrument()
        if ins:
            self._insTypeCtrl.SetData(ins.InsType())
            self._insTypeCtrl.GetData() #Must call GetData for ctrl to update properly
            self._UpdateInsNameCtrl()
            self._insNameCtrl.SetData(ins.Name())
            
    def _SelectedInstrument(self):
        selectedRows = self._eii.ExtensionObject().ActiveSheet().Selection().SelectedRowObjects()
        try:
            return selectedRows[0].Instrument()
        except AttributeError as IndexError:
            return None
    
    def HandleCreate( self, dlg, layout):
        self._include_derivates = layout.GetControl('include_derivates')
        self.m_fuxDlg = dlg
        self.m_fuxDlg.Caption('Select Instrument')
        self._InitControls(layout)
        self._bindings.AddDependent(self)
    
    def HandleApply(self):
        return self._include_derivates.Checked(), acm.FInstrument[self._insNameCtrl.GetData()]
    
    def BuildControlCb(self, name, builder):
        if str(name) == 'ins_Type':
            builder.AddPopuplist('insType', 'Ins Type', 15)
        elif str(name) == 'ins_Name':
            builder.AddPopuplist('insName', 'Name', 30)
        elif str(name) == 'action_Sell':
            builder.AddButton('ok', 'OK')
        elif str(name) == 'action_Buy':
            builder.AddCheckbox('include_derivates', 'Include derivates')
            
    
    
class TradeProgramSheetCreator(object):
    
    def __init__(self, eii, sheetTemplate=None):
        self._eii = eii
        self._frame = eii.ExtensionObject()
        self._sheetTemplate = sheetTemplate
        self._grouper = None
    
    def CreateSheet(self):
        sheet = self._InsertSheet()
        self._InsertContent(sheet)      
        self._AddPlaceholderTrades()  
        self._ApplyGrouper(sheet)  
        return sheet
    
    def _TradeQuery(self):
        return acm.CreateFASQLQuery('FTrade', 'AND')

    def _PlaceholderTrades(self):
        return []
    
    def _Name(self):
        return ''
    
    def _InsertSheet(self):
        if self._sheetTemplate:
            sheet = self._InsertSheetFromTemplate(self._Workbook(), self._sheetTemplate, self._Name())
            return sheet
        else:
            currentSheet = self._Workbook().ActiveSheet()
            self._grouper = FSheetUtils.GetGrouperFromSheet(currentSheet)
            return self._InsertSheetFromCurrentSheet(currentSheet, self._Workbook(), self._Name())
    
    def _InsertContent(self, sheet):
        folder = acm.FASQLQueryFolder()
        query = self._TradeQuery()
        folder.AsqlQuery(query)
        folder.Name(self._Name())
        sheet.InsertObject(folder, 'IOAP_REPLACE')
    
    @staticmethod
    def _InsertSheetFromTemplate(workbook, templateName, name):
        template = acm.FTradingSheetTemplate[templateName]
        assert template, 'No sheet template with name {0} found'.format(template)
        template = template.Clone()
        template.FromArchive('TradingSheet').ToArchive('sname', name)
        workbook.InsertSheet(template)
        return workbook.ActiveSheet()
        
    @staticmethod
    def _InsertSheetFromCurrentSheet(sheet, workbook, name):
        sheetSetup = FSheetUtils.CreateSheetSetup()
        columnCreators = sheet.ColumnCreators().Clone()
        sheetSetup.ColumnCreators(columnCreators)
        sheetSetup.SheetTitle(name)
        return workbook.NewSheet('PortfolioSheet', None, sheetSetup)
    
    def _ApplyGrouper(self, sheet):
        if self._grouper:
            FSheetUtils.ApplyGrouperInstanceToSheet(sheet, self._grouper)
        sheet.PrivateTestSyncSheetContents()
        grouper = FSheetUtils.GetGrouperFromSheet(sheet)
        levels = len(grouper.Groupers())+1 if grouper.IsKindOf(acm.FChainedGrouper) else 2
        FSheetUtils.ExpandTree(sheet, level=levels)

    def _Workbook(self):
        return self._frame.ActiveWorkbook()
    
    def _AddPlaceholderTrades(self):
        tradeProgramTM = FTradeProgramTM(self._eii, OpenPositionAction('Placeholder'))
        tradeProgramTM.ExecutePlaceholder(self._PlaceholderTrades())

class InstrumentViewSheetCreator(TradeProgramSheetCreator):
    
    def __init__(self, eii, instrument, portfolios, sheetTemplate=None, underlying_show=False):
        self._instrument = instrument
        self._portfolios = portfolios
        self._include_derivates = underlying_show
        super(InstrumentViewSheetCreator, self).__init__(eii, sheetTemplate)
    
    def _TradeQuery(self):
        query = acm.CreateFASQLQuery('FTrade', 'AND')
        insNode = query.AddOpNode('OR')
        insNode.AddAttrNode('Instrument.Name', 'EQUAL', self._instrument.Name())
        if self._include_derivates:
            insNode.AddAttrNode('Instrument.Underlying.Name', 'EQUAL', self._instrument.Name())
        prtfNode = query.AddOpNode('OR')
        for portfolio in self._portfolios:
            prtfNode.AddAttrNode('Portfolio.Name', 'EQUAL', portfolio.Name())
        return query
    
    def _Name(self):
        return self._instrument.Name()
    
    def _PlaceholderTrades(self):
        prtfsNoInstrument = self._PortfoliosNotInQuery(self._TradeQuery(), self._portfolios)
        trades = []
        for prtf in prtfsNoInstrument:
            trade = DecoratedTradeCreator({'Instrument':self._instrument,
                                            'Portfolio':prtf,
                                            'Status':'FO Confirmed'
                                            }).CreateTrade()
            trades.append(trade)
        return trades

    @staticmethod
    def _PortfoliosNotInQuery(query, portfolios):
        portfoliosInQuery = {trade.Portfolio() for trade in query.Select()}
        return set(portfolios) - portfoliosInQuery

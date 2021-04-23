""" Compiled: 2020-09-18 10:38:53 """

#__src_file__ = "extensions/PortfolioTrading/etc/FOpenPositionTM.py"
"""--------------------------------------------------------------------------
MODULE
    FOpenPositionTM

    (c) Copyright 2018 FIS FRONT ARENA. All rights reserved.

DESCRIPTION
-----------------------------------------------------------------------------"""

import acm
import FUxCore
from contextlib import contextmanager
from FOpenPosition import FOpenPosition
from FTradeProgramTM import FTradeProgramTM
from FTradeProgramUtils import Logger, CandidateTradeCreator, TradeProgramSettings
from FTradeProgramMenuItem import TradeProgramActionMenuItem
from FParameterSettings import ParameterSettingsCreator
from FTradeProgramAction import Action, OpenPositionAction
from FQuantityCalculator import FindNode
from FOpenFXPositionDlg import OpenFXPositionDlg
from FTradeCreator import TradeFromTreeSpecCreator

@Action
def OpenPosition(eii):
    return QuickOpenPositionMenuItem(eii)

@Action
def OpenFXPosition(eii):
    return OpenFXPositionMenuItem(eii)

class OpenPositionMenuItem(TradeProgramActionMenuItem):
    
    def InvokeAsynch(self, eii):
        candidateTrades, placeholderTrades = self._CandidateAndPlaceholderTrades(self.CreateTrades(eii))
        if placeholderTrades:
            FTradeProgramTM(eii, self.Action()).ExecutePlaceholder(placeholderTrades)
            self.GoToRow(self._frame.ActiveSheet(), placeholderTrades[0])
        if candidateTrades:
            FTradeProgramTM(eii, self.Action()).Execute(candidateTrades)
            self.GoToRow(self._frame.ActiveSheet(), candidateTrades[0])
    
    def _CandidateAndPlaceholderTrades(self, trades):
        candidateTrades = []
        placeholderTrades  = []
        for trade in trades or []:
            if trade.Quantity() == 0:
                placeholderTrades.append(trade)
            else:
                candidateTrades.append(trade)
        return candidateTrades, placeholderTrades
    
    @classmethod
    def GoToRow(cls, sheet, trade):
        instrument = cls._Instrument(trade)
        sheet.PrivateTestSyncSheetContents()
        iterator = sheet.RowTreeIterator(False)
        while(iterator.NextUsingDepthFirst()):
            row = iterator.Tree().Item()
            if row.IsKindOf(acm.FSingleInstrumentAndTrades) and row.Instrument() == instrument:
                if trade in row.Trades():
                    sheet.NavigateTo(row)
                    break
    
    @staticmethod
    def _Instrument(trade):
        return trade.Instrument()
    
    def CreateTrades(self, eii=None):
        raise NotImplementedError
    
    def Action(self):
        return OpenPositionAction('Open Position')


class OpenFXPositionMenuItem(OpenPositionMenuItem):
    
    def CreateTrades(self, eii):
        decoratedTrades = []
        try:
            treeSpec = eii.ExtensionObject().ActiveSheet().Selection().SelectedCell().TreeSpecification()
            _trades = OpenFXPositionDlg(eii, treeSpec).Trades()
            for trade in _trades:
                trade.Status(TradeProgramSettings().CandidateTradeStatus())
                tradeDecorator = acm.FBusinessLogicDecorator.WrapObject(acm.FTrade())
                tradeDecorator.Apply(trade)
                decoratedTrades.append(tradeDecorator.DecoratedObject())
            return decoratedTrades
        except Exception as e:
            Logger().error('Failed to open position. Reason {0}'.format(e))
    
    @staticmethod
    def _Instrument(trade):
        return acm.FX.CreateFxRate(trade.Instrument(), trade.Currency())

class QuickOpenPositionMenuItem(OpenPositionMenuItem):

    def CreateTrades(self, eii):
        openPositionDlg = OpenPositionDlg(eii)
        trade = acm.UX().Dialogs().ShowCustomDialogModal(
                                    self._frame.Shell(),
                                    openPositionDlg.CreateLayout(),
                                    openPositionDlg
                                    )
        return [trade] if trade is not None else None 

                                            
    def Action(self):
        return OpenPositionAction('Open Position')


class OpenPositionAdvancedMenuItem(OpenPositionMenuItem):
    
    def CreateTrades(self, eii):
        trade = OpenPositionAdvancedDlg(eii).CreateTrade()
        if trade is not None:
            trade.Status(TradeProgramSettings().CandidateTradeStatus())
            return [self.ModifyState(trade)]
    
    def ModifyState(self, trade):
        #Workaround to make the infant trade being correctly inserted into portfolio
        tradeDecorator = acm.FBusinessLogicDecorator.WrapObject(acm.FTrade())
        tradeDecorator.Apply(trade)
        tradeDecorator.Instrument(self.Instrument(trade.Instrument()))
        tradeDecorator.Simulate()
        return tradeDecorator.DecoratedObject()
     
    def Instrument(self, instrument):
        if instrument.Difference(instrument.Originator(), True).Differences():
            newInstrument = instrument.StorageImage()
            name = newInstrument.Name()
            newInstrument.StorageSetNew()
            newInstrument.InitializeUniqueIdentifiers()
            newInstrument.Name(name)
            return newInstrument
        else:
            return instrument.Originator()
    
    def Action(self):
        return OpenPositionAction('Open Position')

class ModifyPositionMenuItem(OpenPositionAdvancedMenuItem):

    def InvokeAsynch(self, eii):
        trade = ModifyPositionDlg(eii).CreateTrade()
        if trade is not None:
            trade.Status(TradeProgramSettings().CandidateTradeStatus())
            FTradeProgramTM(eii, self.Action()).Execute([self.ModifyState(trade)])
      
    def EnabledFunction(self):
        if TradeProgramActionMenuItem.EnabledFunction(self):
            return (self._Selection().Size() == 1) and self._Selection()[0].IsKindOf(acm.FSingleInstrumentAndTrades)
        return False
      
    def Action(self):
        return OpenPositionAction('Modify Position')


class OpenPositionAdvancedDlg(object):
    
    DEFAULT_INS_TYPE = "Stock"
    
    def __init__(self, eii):
        self.eii = eii
        self.instrument = None
        
    def ParamDict(self):
        return self.eii.MenuExtension()
        
    def InsType(self):
        return self.ParamDict().At('InsType')
        
    def UnderlyingType(self):
        return self.ParamDict().At('UnderlyingType')

    def Shell(self):
        return self.eii.ExtensionObject().Shell()

    def Application(self):
        return self.ParamDict().At('CustomInstrumentDefinition')

    def EditTrade(self, trade):
        customInsDef =  self.Application() or acm.DealCapturing().CustomInstrumentDefinition(trade)
        initData = acm.DealCapturing().UX().InitDataFromTemplate(trade, customInsDef)
        return acm.DealCapturing().UX().InstrumentDefinitionDialog(self.Shell(), initData, "Ok")
    
    def TreeSpec(self):
        return self.eii.ExtensionObject().ActiveSheet().Selection().SelectedCell().TreeSpecification()
    
    def CreateTrade(self):
        try:
            self.SelectInstrument()
            if self.instrument is not None:
                trade = self.CreateTradeTemplate()
                return self.EditTrade(trade)
        except Exception as e:
            Logger().error('Failed to open position. Reason {0}'.format(e))

    def CreateTradeTemplate(self):
        trade = TradeFromTreeSpecCreator(self.TreeSpec(), self.instrument).CreateTrade()
        return acm.DealCapturing().CreateNewTrade(self.instrument).Apply(trade)

    def SelectInstrumentImpl(self, insType, undInsType):
        return acm.UX().Dialogs().SelectInstrumentDefaultUnderlyingType( 
            self.Shell(), 
            insType or self.DEFAULT_INS_TYPE,
            undInsType or 0, 
            self.InstrumentSelectedCb, 
            None)

    def InstrumentTypeFromSelection(self):
        try:
            selection = self.eii.ExtensionObject().ActiveSheet().Selection()
            return selection.SelectedRowObjects().First().Instrument().InsType()
        except AttributeError:
            return 0
            
    def UnderlyingTypeFromSelection(self):
        try:
            selection = self.eii.ExtensionObject().ActiveSheet().Selection()
            return selection.SelectedRowObjects().First().Instrument().UnderlyingType()
        except AttributeError:
            return 0
            
    def SelectInstrument(self):
        insType = self.InsType() or self.InstrumentTypeFromSelection()
        undType = self.UnderlyingType() or self.UnderlyingTypeFromSelection()
        self.SelectInstrumentImpl(insType, undType)
        
    @FUxCore.aux_cb
    def InstrumentSelectedCb(self, shell, instrument, *args):
        self.instrument = instrument

class ModifyPositionDlg(OpenPositionAdvancedDlg):
    
    def SelectInstrument(self):
        rows = self.eii.ExtensionObject().ActiveSheet().Selection().SelectedRowObjects()
        self.instrument = rows.First().Instrument()
    
    def EditTrade(self, trade):
        customInsDef =  self.Application() or acm.DealCapturing().CustomInstrumentDefinition(trade)
        with self.StripPanes.Strip(customInsDef):
            initData = acm.DealCapturing().UX().InitDataFromTemplate(trade, customInsDef)
            return acm.DealCapturing().UX().InstrumentDefinitionDialog(self.Shell(), initData, "Ok")
    
    class StripPanes(object):

        mod_attrs = {"VisiblePanes": "TradePane;PricingPane", "ShowPlaceExcluded": "trade_Status;trade_bo_trdnbr;trade_payments"}

        @classmethod
        def PatchAppl(cls, customInsDef):
            for key, val in cls.mod_attrs.iteritems():
                customInsDef.AtPut(key, val)

        @classmethod
        def RestoreAppl(cls, target, source):
            for key in target.Keys():
                if key in source.Keys():
                    target.AtPut(key, source.At(key))
                else:
                    target.RemoveKey(key)
                
        @staticmethod
        def IsApplicable(customInsDef):
            return str(customInsDef.InstantiatedAs()) == "Abstract"
        
        @classmethod
        @contextmanager
        def Strip(cls, customInsDef):
            if cls.IsApplicable(customInsDef):
                cloned = customInsDef.Clone()
                cls.PatchAppl(customInsDef)
                yield
                cls.RestoreAppl(customInsDef, cloned)
            else:
                yield

class OpenPositionDlg(FUxCore.LayoutDialog):

    def __init__(self, eii):
        self._eii = eii
        self._bindings = acm.FUxDataBindings()
        self._targetValueCtrl = self._bindings.AddBinder('targetValue', acm.GetDomain('float'))
        self._trade = None

    def HandleApply(self):
        return self._trade

    def HandleCreate( self, dlg, layout):
        self.m_fuxDlg = dlg
        self.m_fuxDlg.Caption('Open Position')
        self._InitControls(layout)
        self._bindings.AddDependent(self)

    def _InitControls(self, layout):
        self._InitInsTypeControl(layout)
        self._InitInsNameControl(layout)
        self._InitBuySellContols(layout)
        self._InitTargetValueControl(layout)

    def _InitInsTypeControl(self, layout):
        self._insTypeCtrl = layout.GetControl('insType')
        self._insTypeCtrl.Populate(acm.FEnumeration['enum(InsType)'].Enumerators().Sort())
        self._insTypeCtrl.SetData(acm.FSymbol('Stock'))
        self._insTypeCtrl.AddCallback('Changed', self._OnInsTypeCtrlChanged, None)

    def _InitInsNameControl(self, layout):
        self._insNameCtrl = layout.GetControl('insName')
        self._UpdateInsNameCtrl()

    def _InitTargetValueControl(self, layout):
        self._targetValueCtrl.InitLayout(layout)

    def _InitBuySellContols(self, layout):
        self._buyCtrl = layout.GetControl('buy')
        self._buyCtrl.AddCallback('Activate', self._OnBuySellClicked, 'Buy')
        self._sellCtrl = layout.GetControl('sell')
        self._sellCtrl.AddCallback('Activate', self._OnBuySellClicked, 'Sell' )

    def _OnInsTypeCtrlChanged(self, args, cd):
        self._UpdateInsNameCtrl()

    def _OnBuySellClicked(self, buyOrSell, cd):
        if self._insNameCtrl.GetData():
            instrument = acm.FInstrument[self._insNameCtrl.GetData()]
            targetValue = self._targetValueCtrl.GetValue()
            inputValue = -targetValue if buyOrSell == 'Sell' else targetValue
            self._trade = FOpenPositionTM(self._eii, instrument, inputValue).Trade()
            self.m_fuxDlg.CloseDialogOK()

    def _UpdateInsNameCtrl(self):
        query = 'insType = "{0}" and generic = 0'.format(self._insTypeCtrl.GetData())
        instruments = [ins for ins in acm.FInstrument.Select(query) if not ins.IsExpired()]
        self._insNameCtrl.Populate(instruments)

    def CreateLayout(self):
        customLayout = self.GetCustomPanesFromExtValue('CustomLayout_OpenPosition')
        fuxLayoutBuilder = acm.FUxLayoutBuilder()
        fuxLayoutBuilder.BeginVertBox()
        acm.UX.CompileLayout(self.BuildControlCb, fuxLayoutBuilder, customLayout, fuxLayoutBuilder, None)
        fuxLayoutBuilder.EndBox()
        return fuxLayoutBuilder

    def BuildControlCb(self, name, builder):
        if str(name) == 'ins_Type':
            builder.AddPopuplist('insType', 'Ins Type', 15)
        elif str(name) == 'ins_Name':
            builder.AddPopuplist('insName', 'Name', 30)
        elif str(name) == 'ins_Position':
            self._targetValueCtrl.BuildLayoutPart(builder, 'Position')
        elif str(name) == 'action_Buy':
            builder.AddButton('buy', 'Buy')
        elif str(name) == 'action_Sell':
            builder.AddButton('sell', 'Sell')

    @staticmethod
    def GetCustomPanesFromExtValue(panesName):
        extCustomPanes = acm.GetDefaultContext().GetExtension('FExtensionValue', acm.FObject, panesName)
        return extCustomPanes.Value()


class FOpenPositionTM(FTradeProgramTM):

    SETTINGS = 'OpenPositionSettings'

    def __init__(self, eii, instrument, inputValue):
        FTradeProgramTM.__init__(self, eii, OpenPositionAction('Open Position'))
        self.instrument = instrument
        self.inputValue = inputValue
        self._settings = None
        self._templateRow = None
        self._targetRow = None
        self._trade = None

    def Trade(self):
        try:
            if self._TemplateRow():
                targetRow = self._TargetRow()
                if targetRow:
                    return FOpenPosition(
                                    targetRow,
                                    self._Trade(),
                                    self.Settings().ColumnId(),
                                    self.inputValue
                                    ).Trade()
        except Exception as e:
            Logger().error('Failed to open position. Reason {0}'.format(e))
            Logger().debug(e, exc_info=True)
            self._RemoveTrade()
    
    def Settings(self):
        if self._settings is None:
            self._settings = ParameterSettingsCreator.FromRootParameter(self.SETTINGS)
        return self._settings

    def _FirstSelectedRow(self):
        try:
            return self.frame.ActiveSheet().Selection().SelectedRowObjects().First()
        except Exception as e:
            Logger().error('Failed to find selected row. Reason {0}'.format(e))
            Logger().debug(e, exc_info=True)

    def _TemplateRow(self):
        if self._templateRow is None:
            self._templateRow = self._FirstSelectedRow()
        return self._templateRow

    def _CreateTrade(self):
        creator = CandidateTradeCreator(self._TemplateRow(), self.instrument)
        return creator.CreateTrade()

    def _InsertTrade(self):
        self._Trade().Simulate()

    def _RemoveTrade(self):
        self._Trade().Unsimulate()
        self._trade = None

    def _Trade(self):
        if self._trade is None:
            self._trade = self._CreateTrade()
        return self._trade

    def _InferParentRow(self, row):
        if row.IsKindOf(acm.FMultiInstrumentAndTrades):
            return row
        return self._InferParentRow(row.Parent())

    def _ActiveSheet(self):
        return self.frame.ActiveSheet()

    def _SynchContents(self):
        self._ActiveSheet().PrivateTestSyncSheetContents()

    def _ParentNode(self):
        parentRow = self._InferParentRow(self._TemplateRow())
        treeIter = self._ActiveSheet().RowTreeIterator(0)
        return FindNode(treeIter.Tree(), parentRow)

    def _TargetRow(self):
        if self._targetRow is None:
            self._targetRow = self._FindTargetRow()
        return self._targetRow

    def _FindTargetRow(self):
        self._InsertTrade()
        self._SynchContents()
        try:
            parentIter = self._ParentNode().Iterator()
            return parentIter.Find(self.instrument).Tree().Item()
        except AttributeError:
            raise AttributeError('Could not find row {0} '
                                 'under ({1})'.format(
                                                    self.instrument.Name(),
                                                    self._ParentNode().StringKey()
                                                    ))
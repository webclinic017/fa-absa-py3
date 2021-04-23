""" Compiled: 2020-09-18 10:38:55 """

#__src_file__ = "extensions/SecuritiesLending/etc/FSecLendOrderCapturePanelBase.py"
from __future__ import print_function
"""--------------------------------------------------------------------------
MODULE
    FSecLendOrderCapturePanelBase

    (c) Copyright 2017 FIS FRONT ARENA. All rights reserved.

DESCRIPTION
    Order Manager - Base Panel for capturing new orders from customer requests.

-----------------------------------------------------------------------------"""
import acm
import traceback

import FPortfolioRouter
import FSecLendHooks
import FSecLendRecordLookup
from FParameterSettings import ParameterSettingsCreator
import FSecLendReturns
import FUxCore
from FPanel import Panel
from FSecLendDealUtils import SecurityLoanCreator
from FSecLendEvents import (OnOrderManagerOrdersEntered,
                            OnOrderCaptureInstrumentChanged,
                            OnOrderCaptureCounterpartyChanged)
from FSecLendUtils import (IsShowDropDownKey, SetSource,
                           TradeFromInstrument, CommitTrades, logger, fn_timer)
from FTradeStreamBase import (FStreamReader, NoCounterpartyFoundError, ParsingError, FullTextNotProcessedError)
_SETTINGS = ParameterSettingsCreator.FromRootParameter('SecLendSettings')

class SecLendOrderCapturePanelBase(Panel):
    GREEN = acm.UX().Colors().Create(204, 255, 204)
    RED = acm.UX().Colors().Create(255, 204, 204)

    def __init__(self):
        try:
            super(SecLendOrderCapturePanelBase, self).__init__()
            self._orderTypes = self.GetOrderTypes()
            self._collateralCtrl = None
            self._acquirerCtrl = None
            self._quantityCtrl = None
            self._orderTypeCtrl = None
            self._quantityFuxCtrl = None
            self._rateCtrl = None  # add callback to change the label of the control
            self._feeLimitCtrl = None
            self._fromFileBtn = None
            self._fromClipboardBtn = None
            self._clearBtn = None
            self._saveBtn = None
            self._bindings = None
            self._isRebateCtrl = None
            self._isReturnCtrl = None
            self._isRecallCtrl = None
            self._isHoldCtrl = None
            self._layout = None
            self.BorrowOutLabel = _SETTINGS.BorrowOutLabel()
            self.BorrowInLabel = _SETTINGS.BorrowInLabel()
            self._defaultPortfolio = FSecLendHooks.DefaultPortfolio()
            self.InitDataBindings()
            lookupSettings = ParameterSettingsCreator.FromRootParameter('SecLendRecordLookupSettings')
            self._instrumentCtrl = FSecLendRecordLookup.SearchControl('Instrument',
                                                                      FSecLendRecordLookup.InstrumentLookup,
                                                                      lookupSettings.InstrumentLookUpIds(),
                                                                      displayAllIds=lookupSettings.DisplayAllIds())
            self._counterpartyCtrl = FSecLendRecordLookup.SearchControl('Party',
                                                                        FSecLendRecordLookup.PartyLookup,
                                                                        lookupSettings.PartyLookUpIds(),
                                                                        displayAllIds=lookupSettings.DisplayAllIds())
            self.stream_reader = FStreamReader() #build the child class first
            self._simulatedTrade = None
            self._showSuggestFee = True

        except Exception:
            logger.error('Exception Error:{}'.format(traceback.format_exc()))

    def CreateLayout(self):
        b = acm.FUxLayoutBuilder()
        b.BeginHorzBox()
        b.AddSpace(10)
        b.BeginVertBox()
        b.AddSpace(10)
        b.BeginHorzBox()
        b.AddLabel('import', 'Add Orders From: ')
        b.AddButton('clipboard', 'Clipboard')
        b.AddButton('file', 'File...')
        b.EndBox()
        b.AddSpace(10)
        b.BeginVertBox('EtchedIn', 'OrderEntry')
        self._counterpartyCtrl.BuildLayoutPart(b, 'Counterparty')
        self._instrumentCtrl.BuildLayoutPart(b, 'Security')
        self._quantityCtrl.BuildLayoutPart(b, self.BorrowOutLabel)
        self._rateCtrl.BuildLayoutPart(b, 'Suggest Fee')
        self._feeLimitCtrl.BuildLayoutPart(b, 'Fee Limit')
        self._orderTypeCtrl.BuildLayoutPart(b, 'Order Type')
        self._acquirerCtrl.BuildLayoutPart(b, 'Acquirer')
        b.AddComboBox('_collateralCtrl', 'Collateral Profile', 30, 30)
        b.AddSpace(10)
        b.BeginHorzBox()
        b.AddCheckbox('_isRebateCtrl', 'Rebate')
        b.AddCheckbox('_isReturnCtrl', 'Return')
        b.AddCheckbox('_isRecallCtrl', 'Recall')
        b.AddCheckbox('_isHoldCtrl', 'Hold')
        b.EndBox()
        b.EndBox()
        b.AddSpace(10)
        self.ExtendedCreateLayout(b)
        b.AddFill()
        b.BeginHorzBox()
        b.AddFill()
        b.AddButton('save', 'OK')
        b.AddButton('clear', 'Clear')
        b.AddSpace(10)
        b.EndBox()
        b.EndBox()
        b.AddSpace(10)
        b.EndBox()
        return b

    def ExtendedCreateLayout(self, uxlb):
        pass

    def AddToEventQueue(self, event):
        pass  # Don't queue events when hidden

    def HandleViewDestroyed(self, view):
        if view.ClassName() == 'SecLendOrderManagerView':
            self.ClearOrderEntry()

    def InitDataBindings(self):
        self._bindings = acm.FUxDataBindings()

        self._acquirerCtrl = self._bindings.AddBinder(
            'acquirer', acm.GetDomain('FInternalDepartment'),
            choiceListSource=acm.FInternalDepartment.Instances(),
            width=30, maxWidth=30)

        self._quantityCtrl = self._bindings.AddBinder(
            'quantity', acm.GetDomain('FTradeQuantity'), formatter=acm.Get('formats/Imprecise'),
            width=30, maxWidth=30, useSpinButtons=False)

        self._rateCtrl = self._bindings.AddBinder(
            'rate', acm.GetDomain('float'),
            width=30, maxWidth=30, useSpinButtons=False)

        self._feeLimitCtrl = self._bindings.AddBinder(
            'feeLimit', acm.GetDomain('float'),
            width=30, maxWidth=30, useSpinButtons=False)

        self._orderTypeCtrl = self._bindings.AddBinder(
            'orderType', acm.GetDomain('FChoiceList'),
            choiceListSource=self._orderTypes.values(),
            width=30, maxWidth=30)

        self._bindings.AddDependent(self)

    def InitInstrumentControl(self):
        self._instrumentCtrl.HandleCreate(self._layout)
        self._instrumentCtrl.AddCallback('Activate', self.OnInstrumentLooseFocusActivate, self)
        self._instrumentCtrl.AddCallback('LooseFocus', self.OnInstrumentLooseFocusActivate, self)
        self._instrumentCtrl.PopulateControl()

    def InitPartyControl(self):
        self._counterpartyCtrl.HandleCreate(self._layout)
        self._counterpartyCtrl.AddCallback('Activate', self.OnPartyLooseFocusActivate, self)
        self._counterpartyCtrl.AddCallback('LooseFocus', self.OnPartyLooseFocusActivate, self)
        self._counterpartyCtrl.PopulateControl()

    def InitCollateralControl(self):
        self._collateralCtrl = self._layout.GetControl('_collateralCtrl')
        if IsShowDropDownKey():
            self._collateralCtrl.EnableShowDropDownOnKeyDown(True)
        self._collateralFuxCtrl = self._layout.GetControl('_collateralCtrl')
        self._collateralFuxCtrl.AddCallback('Changing', self.OnCollateralChanging, self)

    def InitAcquirerControl(self):
        self.SetDefaultAcquirer()
        if IsShowDropDownKey():
            self._layout.GetControl('acquirer').EnableShowDropDownOnKeyDown(True)

    def InitOrderTypeControl(self):
        self.SetDefaultOrderType()
        if IsShowDropDownKey():
            self._layout.GetControl('orderType').EnableShowDropDownOnKeyDown(True)
        self._orderTypeFuxCtrl = self._layout.GetControl('orderType')
        self._orderTypeFuxCtrl.AddCallback('LooseFocus', self.OnOrderTypeLooseFocusActivate, self)
        self._orderTypeFuxCtrl.AddCallback('Activate', self.OnOrderTypeLooseFocusActivate, self)

    def InitQuantityControl(self):
        self._quantityFuxCtrl = self._layout.GetControl('quantity')
        self._quantityFuxCtrl.SetColor('Background', self.RED)
        self._quantityFuxCtrl.AddCallback('Changing', self.OnQuantityChanging, self)
        self._quantityFuxCtrl.AddCallback('LooseFocus', self.OnQuantityLooseFocusActivate, self)
        self._quantityFuxCtrl.AddCallback('Activate', self.OnQuantityLooseFocusActivate, self)

    def InitRateControl(self):
        self._rateFuxCtrl = self._layout.GetControl('rate')
        self._rateFuxCtrl.ToolTip('The suggested fee is shown until the user starts to edit the control.')
        self._rateFuxCtrl.AddCallback('LooseFocus', self.OnRateLooseFocusActivate, self)
        self._rateFuxCtrl.AddCallback('Activate', self.OnRateLooseFocusActivate, self)

    def InitFeeLimitControl(self):
        self._feeLimitFuxCtrl = self._layout.GetControl('feeLimit')
        self._feeLimitFuxCtrl.AddCallback('LooseFocus', self.OnFeeLimitLooseFocusActivate, self)
        self._feeLimitFuxCtrl.AddCallback('Activate', self.OnFeeLimitLooseFocusActivate, self)

    def InitRebateControl(self):
        self._isRebateCtrl = self._layout.GetControl('_isRebateCtrl')

    def InitReturnControl(self):
        self._isReturnCtrl = self._layout.GetControl('_isReturnCtrl')
        self._isReturnCtrl.AddCallback('Activate', self.OnReturnClicked, self)

    def InitRecallControl(self):
        self._isRecallCtrl = self._layout.GetControl('_isRecallCtrl')
        self._isRecallCtrl.AddCallback('Activate', self.OnRecallClicked, self)

    def InitHoldControl(self):
        self._isHoldCtrl = self._layout.GetControl('_isHoldCtrl')

    def GetOrderTypes(self):
        orderTypes = dict()
        for orderType in acm.FChoiceList.Select("list='SBL_OrderType'"):
            orderTypes[orderType.Name()] = orderType
        return orderTypes

    def ShowSuggestFee(self):
        return self._showSuggestFee

    def SetShowSuggestFee(self, showFee=True):
        self._showSuggestFee = showFee

    def SetDefaultOrderType(self):
        if self._orderTypes[_SETTINGS.DefaultOrderType()]:
            self._orderTypeCtrl.SetValue(_SETTINGS.DefaultOrderType())
        else:
            orderType = self._orderTypes.values()[0]

    def SetDefaultAcquirer(self):
        if FSecLendHooks.DefaultAcquirer():
            self._acquirerCtrl.SetValue(FSecLendHooks.DefaultAcquirer())
        else:
            self._acquirerCtrl.SetValue(acm.FInternalDepartment.Instances()[0])

    def InitFromClipboardControl(self):
        self._fromClipboardBtn = self._layout.GetControl('clipboard')
        self._fromClipboardBtn.AddCallback('Activate', self.OnFromClipboardClicked, None)
        self._fromClipboardBtn.ToolTip('Generate Trades from Clipboard (Ctrl+Alt+V)')

    def InitFromFileControl(self):
        self._fromFileBtn = self._layout.GetControl('file')
        self._fromFileBtn.AddCallback('Activate', self.OnFromFileClicked, None)

    def InitClearControl(self):
        self._clearBtn = self._layout.GetControl('clear')
        self._clearBtn.AddCallback('Activate', self.ClearOrderEntry, None)
        self._clearBtn.Enabled(False)

    def InitSaveControl(self):
        self._saveBtn = self._layout.GetControl('save')
        self._saveBtn.AddCallback('Activate', self.OnSaveClicked, None)
        self._saveBtn.Enabled(False)

    def _SendSheetChanged(self, sheet):
        pass

    def InitControls(self, layout):
        self._layout = layout
        try:
            self._bindings.AddLayout(layout)
            self.InitFromClipboardControl()
            self.InitFromFileControl()
            self.InitClearControl()
            self.InitSaveControl()
            self.InitInstrumentControl()
            self.InitPartyControl()
            self.InitCollateralControl()
            self.InitRateControl()
            self.InitFeeLimitControl()
            self.InitAcquirerControl()
            self.InitOrderTypeControl()
            self.InitQuantityControl()
            self.InitRebateControl()
            self.InitReturnControl()
            self.InitRecallControl()
            self.InitHoldControl()
            self.UpdateButtons()
        except Exception:
            logger.error('Exception Error:{}'.format(traceback.format_exc()))

    def UpdateButtons(self):
        hascounterparty = bool(self._counterpartyCtrl.GetData())
        hasInstrument = bool(self._instrumentCtrl.GetData())
        hasquantity = bool(self._quantityCtrl.GetValue())
        hasrate = bool(self._rateCtrl)
        hasFeeLimit = bool(self._feeLimitCtrl)
        hasacquirer = bool(self._acquirerCtrl)
        hascollateral = bool(self._collateralCtrl.GetData())
        isRebate = self._isRebateCtrl.Checked() if self._isRebateCtrl else False
        isReturn = self._isReturnCtrl.Checked() if self._isReturnCtrl else False
        isRecall = self._isRecallCtrl.Checked() if self._isRecallCtrl else False
        isHold = self._isHoldCtrl.Checked() if self._isHoldCtrl else False
        self._saveBtn.Enabled(hasInstrument)
        self._clearBtn.Enabled(
            any([hasInstrument, hascounterparty, hasquantity, hasrate, hasFeeLimit,
                 hasacquirer, hascollateral, isRebate, isReturn, isRecall, isHold]))

    def EnableControls(self, enabled=True):
        self._orderTypeCtrl.Enabled(enabled)
        self._rateCtrl.Enabled(enabled)
        self._feeLimitCtrl.Enabled(enabled)
        self._acquirerCtrl.Enabled(enabled)
        self._collateralCtrl.Enabled(enabled)
        self._isRebateCtrl.Enabled(enabled)
        self._isHoldCtrl.Enabled(enabled)

    def CalculateAndSetSuggestedFee(self):
        if self._simulatedTrade:
            calc_space = acm.Calculations().CreateCalculationSpace(acm.GetDefaultContext(), 'FTradeSheet')
            suggestedFee = calc_space.CreateCalculation(self._simulatedTrade, 'Security Loan Suggested Fee')
            if suggestedFee:
                self._rateCtrl.SetValue(suggestedFee.FormattedValue())

    def OnCollateralChanging(self, *args):
        if self._simulatedTrade is not None and self.ShowSuggestFee() and\
                acm.FCollateralAgreement[self._collateralCtrl.GetData()]:
            self._simulatedTrade.AdditionalInfo().CollateralAgreement(self._collateralCtrl.GetData())
            self.CalculateAndSetSuggestedFee()
        self.UpdateButtons()

    def OnQuantityLooseFocusActivate(self, *args):
        if self._quantityCtrl.Validate(False):
            if self._simulatedTrade is not None and self.ShowSuggestFee():
                self._simulatedTrade.Quantity(self._quantityCtrl.GetValue())
                self.CalculateAndSetSuggestedFee()
        else:
            self._quantityCtrl.SetValue('')
        self.UpdateButtons()

    def OnQuantityChanging(self, *args):
        try:
            quantity = self._quantityCtrl.GetValue()
        except:
            pass
        else:
            if quantity >= 0:
                self._quantityFuxCtrl.SetColor('Background', self.GREEN)
                self._quantityFuxCtrl.Label(self.BorrowInLabel)
            else:
                self._quantityFuxCtrl.SetColor('Background', self.RED)
                self._quantityFuxCtrl.Label(self.BorrowOutLabel)
            self.UpdateButtons()

    def OnReturnClicked(self, *args):
        if self._isReturnCtrl.Checked():
            self._orderTypeCtrl.SetValue("")
            self._rateCtrl.SetValue("")
            self._rateCtrl.Label('Fee')
            self._feeLimitCtrl.SetValue("")
            self.SetShowSuggestFee(False)
            self._acquirerCtrl.SetValue("")
            self._collateralCtrl.SetData("")
            self._isRebateCtrl.Checked(False)
            self._isRecallCtrl.Checked(False)
            self._isRecallCtrl.Enabled(False)
            self._isHoldCtrl.Checked(False)
            self.EnableControls(False)
        else:
            if self.ShowSuggestFee():
                self.CalculateAndSetSuggestedFee()
            self.SetDefaultOrderType()
            self.SetDefaultAcquirer()
            self._isRecallCtrl.Enabled(True)
            self.EnableControls()

    def OnRecallClicked(self, *args):
        if self._isRecallCtrl.Checked():
            self._orderTypeCtrl.SetValue("")
            self._rateCtrl.SetValue("")
            self._rateCtrl.Label('Fee')
            self._feeLimitCtrl.SetValue("")
            self.SetShowSuggestFee(False)
            self._acquirerCtrl.SetValue("")
            self._collateralCtrl.SetData("")
            self._isReturnCtrl.Checked(False)
            self._isReturnCtrl.Enabled(False)
            self._isRebateCtrl.Checked(False)
            self._isHoldCtrl.Checked(False)
            self.EnableControls(False)
        else:
            if self.ShowSuggestFee():
                self.CalculateAndSetSuggestedFee()
            self.SetDefaultOrderType()
            self.SetDefaultAcquirer()
            self._isReturnCtrl.Enabled(True)
            self.EnableControls()

    def HasUserTypedInRateCtrl(self):
        if not self._rateCtrl.GetValue():
            return False
        if self._simulatedTrade:
            calc_space = acm.Calculations().CreateCalculationSpace(acm.GetDefaultContext(), 'FTradeSheet')
            suggestedFee = calc_space.CreateCalculation(self._simulatedTrade, 'Security Loan Suggested Fee')
            if suggestedFee and suggestedFee.FormattedValue():
                if float(suggestedFee.FormattedValue()) == self._rateCtrl.GetValue():
                    return False
        return True

    def OnRateLooseFocusActivate(self, *args):
        if self._rateCtrl.Validate(False):
            if self.ShowSuggestFee():
                if self.HasUserTypedInRateCtrl():
                    self.SetShowSuggestFee(False)
                    self._rateCtrl.Label('Fee')
        else:
            self._rateCtrl.SetValue('')
        self.UpdateButtons()

    def OnFeeLimitLooseFocusActivate(self, *args):
        if not self._feeLimitCtrl.Validate(False):
            self._feeLimitCtrl.SetValue('')
        self.UpdateButtons()

    def OnOrderTypeLooseFocusActivate(self, *args):
        if not self._orderTypeCtrl.Validate(False) or not self._orderTypeCtrl.GetValue():
            self.SetDefaultOrderType()
        self.UpdateButtons()

    def GetTradesFromStream(self, text, reference, fileName=''):
        """
        Get Trades From ClipBoard Input that got validated. Use Quick Order Entry to enrich the
        parsed data if there will be some missing.
        """
        return self.stream_reader.TradesFromString(text,
                                                   Reference=reference,
                                                   FileName=fileName,
                                                   Source='Manual',
                                                   Counterparty=acm.FParty[self._counterpartyCtrl.GetData()],
                                                   CollateralAgreement=self._collateralCtrl.GetData(),
                                                   isReturn=self._isReturnCtrl.Checked(),
                                                   isRecall=self._isRecallCtrl.Checked(),
                                                   acquirer=self._acquirerCtrl.GetValue(),
                                                   isRebate=self._isRebateCtrl.Checked(),
                                                   isHold=self._isHoldCtrl.Checked())

    def CreateTradesFromText(self, text, reference, fileName=''):
        if text:
            trades = self.GetTradesFromStream(text, reference, fileName)
            CommitTrades(trades, _SETTINGS.CommitChunkSize())
            if self.stream_reader.getInvalidInput():
                if (reference == 'ClipBoard' and _SETTINGS.ShowClipboardBuffer()) or \
                        (reference == 'File' and _SETTINGS.ShowFileBuffer()):
                    buffer_dialog = StreamBufferDialog(self.stream_reader.getInvalidInput())
                    acm.UX().Dialogs().ShowCustomDialogModal(self.Shell(),
                                                             buffer_dialog.CreateLayout(), buffer_dialog)
            return trades

    @fn_timer
    def OnFromClipboardClicked(self, *args):
        try:
            trades = self.CreateTradesFromText(self.stream_reader.TextFromClipboard(), 'ClipBoard')
        except NoCounterpartyFoundError:
            acm.UX().Dialogs().MessageBoxInformation(self.Shell(),
                                                     'No counterparty set.')
            logger.error('No counterparty set.')
        except (StandardError, ParsingError) as e:
            acm.UX().Dialogs().MessageBoxInformation(self.Shell(),
                                                     'Clipboard text could not be parsed for trade information. Error:{}'.format(
                                                         e))
            logger.error(
                'Clipboard text could not be parsed for trade information. Error:{}'.format(traceback.format_exc()))
        except FullTextNotProcessedError:
            acm.UX().Dialogs().MessageBoxInformation(self.Shell(),
                                                     'The clipboard information was not processed due to clipboard exceeding maximum number of characters. '
                                                     'The maximum number of characters can be configured in SecLendSettings.')
        else:
            self.SendEvent(OnOrderManagerOrdersEntered(self, trades))

    @fn_timer
    def OnFromFileClicked(self, *args):
        try:
            fileName, text = self.stream_reader.TextFromFile(self.Shell())
            trades = self.CreateTradesFromText(text, 'File', fileName)

        except NoCounterpartyFoundError:
            acm.UX().Dialogs().MessageBoxInformation(self.Shell(), 'No counterparty set.')
        except (StandardError, ParsingError) as e:
            acm.UX().Dialogs().MessageBoxInformation(self.Shell(),
                                                     'Failed to read trade information from file.')
            logger.error('Failed to read trade information from file. Error:{}'.format(traceback.format_exc()))
        except FullTextNotProcessedError:
            acm.UX().Dialogs().MessageBoxInformation(self.Shell(),
                                                     'The file information was not processed due to file exceeding maximum number of characters. '
                                                     'The maximum number of characters can be configured in SecLendSettings.')
        else:
            self.SendEvent(OnOrderManagerOrdersEntered(self, trades))

    def CreateSuggestedReturnTrades(self, underlying, counterparty, quantity, **kwargs):
        trades = []
        try:
            query = FSecLendHooks.ActiveLoansQuery(counterparty, [underlying])
            query.AddAttrNode('Status', 'NOT_EQUAL', FSecLendHooks.DefaultTradeStatus())
            query.AddAttrNode('Status', 'NOT_EQUAL', FSecLendHooks.OnHoldTradeStatus())
            activeLoans = query.Select()
            trades = FSecLendReturns.CreateReturnTrades(activeLoans,
                                                        quantity,
                                                        clientReturns=False if quantity < 0 else True,
                                                        returnPartial=False, **kwargs)
        except FSecLendReturns.NoQuantityFoundError:
            acm.UX.Dialogs().MessageBoxInformation(self.Shell(), 'Quantity to return must be a number.')
        except FSecLendReturns.NoReturnLoansFoundError:
            acm.UX.Dialogs().MessageBoxInformation(self.Shell(), 'No loans found to return from.')
        except Exception as e:
            acm.UX.Dialogs().MessageBoxInformation(self.Shell(), str(e))
            logger.error('CreateReturnTrades Error:{}'.format(traceback.format_exc()))
        return trades

    @fn_timer
    def OnSaveTrade(self):
        trades = []
        if self._instrumentCtrl.GetData():
            if self._instrumentCtrl.IsValidData():
                instrument = acm.FInstrument[self._instrumentCtrl.GetData()]
                if self._isReturnCtrl.Checked() or self._isRecallCtrl.Checked():  # Create return/recall trades
                    if self._counterpartyCtrl.GetData():
                        trades = self.CreateSuggestedReturnTrades(underlying=instrument,
                                                                  counterparty=acm.FParty[self._counterpartyCtrl.GetData()],
                                                                  quantity=self._quantityCtrl.GetValue(),
                                                                  status=FSecLendHooks.DefaultTradeStatus(),
                                                                  acquirer=self._acquirerCtrl.GetValue(),
                                                                  source='Manual',
                                                                  returntype='return' if self._isReturnCtrl.Checked() else 'recall')
                    else:
                        raise NoCounterpartyFoundError()
                else:
                    loan = SecurityLoanCreator.CreateInstrument(underlying=instrument,
                                                                fee=(self._rateCtrl.GetValue() or 0) / 100,
                                                                isRebate=self._isRebateCtrl.Checked())
                    trades.append(SecurityLoanCreator.CreateTrade(
                        loan,
                        quantity=self._quantityCtrl.GetValue() if self._quantityCtrl.GetValue() else 0,
                        acquirer=self._acquirerCtrl.GetValue(),
                        counterparty=acm.FParty[self._counterpartyCtrl.GetData()],
                        collateralAgreement=self._collateralCtrl.GetData() if self._collateralCtrl.GetData() else None,
                        status=FSecLendHooks.DefaultTradeStatus(),
                        source='Manual',
                        orderType=self._orderTypeCtrl.GetValue(),
                        holdTime=True if self._isHoldCtrl.Checked() else False,
                        feeLimit=self._feeLimitCtrl.GetValue() / 100 if self._feeLimitCtrl.GetValue() else None))
                    for t in trades:
                        t.Portfolio(FPortfolioRouter.GetPortfolio(t))
            else:
                acm.UX().Dialogs().MessageBoxInformation(self.Shell(),
                                                         "Security '{}' is invalid and cannot be used.".format(
                                                             self._instrumentCtrl.GetData()))
                logger.error('Security "{}" is invalid and cannot be used.'.format(self._instrumentCtrl.GetData()))
                self._instrumentCtrl.Clear()
        return trades

    @fn_timer
    def OnSaveClicked(self, *args):
        try:
            trades = self.OnSaveTrade()
            if trades:
                CommitTrades(trades)
                self.SendEvent(OnOrderManagerOrdersEntered(self, trades))
                self.ClearOrderEntry()
        except NoCounterpartyFoundError:
            acm.UX().Dialogs().MessageBoxInformation(self.Shell(),
                                                     'No counterparty set.')
        except Exception:
            logger.error('OnSaveClicked Error:{}'.format(traceback.format_exc()))

    def OnInstrumentLooseFocusActivate(self, *args):
        if self._instrumentCtrl.GetData():
            if self._instrumentCtrl.IsValidData():
                def GenerateTrade():
                    trade = TradeFromInstrument(acm.FInstrument[self._instrumentCtrl.GetData()])
                    party = acm.FParty[self._counterpartyCtrl.GetData()] if self._counterpartyCtrl else None
                    if trade and party:
                        trade.Counterparty(party)
                        SetSource(trade, 'Manual')
                    return trade

                if _SETTINGS.ActiveQOEInstrEvent():
                    self.SendEvent(OnOrderCaptureInstrumentChanged(self, acm.FInstrument[self._instrumentCtrl.GetData()]))
                if not (self._isReturnCtrl.Checked() or self._isRecallCtrl.Checked()) and self.ShowSuggestFee():
                    self._simulatedTrade = GenerateTrade()
                    self.CalculateAndSetSuggestedFee()
            else:
                acm.UX().Dialogs().MessageBoxInformation(self.Shell(),
                                                         "Security '{}' is invalid and cannot be used.".format(
                                                             self._instrumentCtrl.GetData()))
                logger.error('Security "{}" is invalid and cannot be used.'.format(self._instrumentCtrl.GetData()))
                self._instrumentCtrl.Clear()
        self.UpdateButtons()

    def OnPartyLooseFocusActivate(self, *args):
        if self._counterpartyCtrl.GetData():
            if  self._counterpartyCtrl.IsValidData():
                party = acm.FParty[self._counterpartyCtrl.GetData()]
                if self._simulatedTrade is not None and self.ShowSuggestFee():
                    self._simulatedTrade.Counterparty(party)
                    self.CalculateAndSetSuggestedFee()
                if _SETTINGS.ActiveQOEPartyEvent():
                    self.SendEvent(OnOrderCaptureCounterpartyChanged(self, party))
                self._collateralCtrl.Clear()
                for col in FSecLendHooks.GetCollateralAgreementChoices(party):
                    self._collateralCtrl.AddItem(col.Name())
                self.UpdateButtons()
            else:
                acm.UX().Dialogs().MessageBoxInformation(self.Shell(),
                                                         "CounterParty '{}' is invalid and cannot be used.".format(
                                                             self._counterpartyCtrl.GetData()))
                logger.error('CounterParty "{}" is invalid and cannot be used.'.format(self._counterpartyCtrl.GetData()))
                self._counterpartyCtrl.Clear()

    def GetSelectedInstrument(self, *args):
        return self._instrumentCtrl.GetData()

    def GetSelectedCounterparty(self, *args):
        return self._counterpartyCtrl.GetData()

    def ClearOrderEntry(self, *args):
        self._counterpartyCtrl.Clear()
        self.SetDefaultAcquirer()
        self._instrumentCtrl.Clear()
        self._collateralCtrl.Clear()
        self._isRebateCtrl.Checked(False)
        self._isReturnCtrl.Checked(False)
        self._isReturnCtrl.Enabled(True)
        self._isRecallCtrl.Checked(False)
        self._isRecallCtrl.Enabled(True)
        self._isHoldCtrl.Checked(False)
        self._quantityCtrl.SetValue("")
        self._rateCtrl.SetValue("")
        self._rateCtrl.Label('Suggest Fee')
        self._feeLimitCtrl.SetValue("")
        self.SetShowSuggestFee(True)
        self.SetDefaultOrderType()
        self._simulatedTrade = None
        self.EnableControls()
        self.UpdateButtons()


def GetTradesFromClipboard(eii):
    for app in acm.ApplicationList():
        if app.IsKindOf(acm.FUiTrdMgrFrame):
            clp = app.GetCustomDockWindow('SecLendOrdersOrderCapturePanel')
            if clp:
                panel = clp.CustomLayoutPanel()
                panel.OnFromClipboardClicked()


def SaveOrderEntryTrade(eii):
    for app in acm.ApplicationList():
        if app.IsKindOf(acm.FUiTrdMgrFrame):
            clp = app.GetCustomDockWindow('SecLendOrdersOrderCapturePanel')
            if clp:
                panel = clp.CustomLayoutPanel()
                panel.OnSaveClicked()


class StreamBufferDialog(FUxCore.LayoutDialog):
    # No needed. use text box instead. Wait with requirements first
    RETURN_LOAN = 0
    NEW_LOAN = 1

    def __init__(self, input, caption='Trade Stream Buffer', editable=True):
        self.m_fuxDlg = None
        self.m_SaveLoans = None
        self.m_bufferEditor = None
        self.input = input
        self.m_buffer_Content = ""
        self.caption = caption
        self.editable = editable

    def HandleCreate(self, dlg, layout):
        self.m_fuxDlg = dlg
        self.m_fuxDlg.Caption(self.caption)
        self.m_SaveLoans = layout.GetControl("Save")
        self.m_bufferEditor = layout.GetControl("bufferEditor")
        self.m_bufferEditor.SetData(self.input)
        self.m_bufferEditor.Editable(self.editable)
        self.m_SaveLoans.AddCallback('Activate', self.OnSaveLoansButtonClicked, self)

    def OnSaveLoansButtonClicked(self, *args):
        self.m_buffer_Content = self.m_bufferEditor.GetData()
        self.m_fuxDlg.CloseDialogOK()

    def GetContent(self):
        return self.m_buffer_Content

    def CreateLayout(self):
        b = acm.FUxLayoutBuilder()
        b.BeginVertBox('None')
        b.AddText('bufferEditor', 400, 400)
        b.BeginHorzBox('None')
        b.AddSpace(10)
        b.AddFill()
        b.AddButton('Save', 'OK')
        b.AddButton('cancel', 'Cancel')
        b.EndBox()
        b.EndBox()
        return b

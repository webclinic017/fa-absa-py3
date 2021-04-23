""" Compiled: 2020-09-18 10:38:55 """

#__src_file__ = "extensions/SecuritiesLending/etc/FSecLendOrdersMenuItems.py"
from __future__ import print_function
"""--------------------------------------------------------------------------
MODULE
    FSecLendOrdersMenuItems

    (c) Copyright 2017 FIS FRONT ARENA. All rights reserved.

DESCRIPTION
    Order Manager - Menu items.

---------------------------------------------------------------------------"""
import acm

import FSecLendHooks
import FSecLendUtils
import FSecLendHoldTrade
from ACMPyUtils import Transaction
from FClipboardUtilities import SetClipboardText  # @UnresolvedImport pylint: disable=import-error
from FSecLendHooks import ClipBoardTextHookFromTrades
from FSecLendMenuItem import SecLendMenuItemBase
from FSecLendOrderCapturePanelBase import StreamBufferDialog
from FSecLendWorkflow import SecLendWorkflow
from GenerateOrderReportAPI import GetReportParameters
from SecLendingReportingATS import SEC_LEND_REPORT_TO_DESTINATIONS
from FWorkflowMenuItem import MultiWorkflowMenuItem
from FParameterSettings import ParameterSettingsCreator
from datetime import datetime, timedelta

_SETTINGS = ParameterSettingsCreator.FromRootParameter('SecLendSettings')

class SecLendingWorkflowMenuItem(MultiWorkflowMenuItem, SecLendMenuItemBase):
    EVENT = None
    BP_CACHE = {}

    def __init__(self, extObj):
        super(SecLendingWorkflowMenuItem, self).__init__(extObj, SecLendWorkflow, self.EVENT)


    def _BusinessProcess(self, trade):
        try:
            if not trade in self.BP_CACHE:
                bp = acm.BusinessProcess.FindBySubjectAndStateChart(trade, self._workflow.StateChart())[0]
                self.BP_CACHE[trade] = bp
            return self.BP_CACHE[trade]
        except IndexError:
            return None

    def _SelectedTrades(self, maxNbrOfTrades=1000):
        return [trade for trade in self._frame.ActiveSheet().Selection().SelectedTrades()[0:maxNbrOfTrades] 
                if not trade.IsDeleted()]

    def BusinessProcesses(self):
        trades = self._SelectedTrades(100)  # Cut off because of performance
        if not trades:
            return None
        return filter(lambda x: bool(x), [self._BusinessProcess(trade) for trade in trades])

    def Applicable(self):
        return True

    def _HandleEvent(self, businessProcess, parameters=None, notes=None):
        MIFIDParams = FSecLendUtils.ColumnValuesFromExtensionattribute(businessProcess.Subject(),
                                                                       "_SecurityLoan_Reporting_Columns")
        if parameters:
            parameters.update(MIFIDParams)
        self.Workflow()(businessProcess)._HandleEvent(self.Event(), parameters, notes)

    def _IsValidUserForAction(self):
        validUser = []
        trades = self._SelectedTrades()
        if trades:
            return FSecLendHooks.IsValidUserForRibbon(trades)
        else:
            return False
    
    def _IsValidEvent(self):
        if self.EVENT:
            return MultiWorkflowMenuItem.Enabled(self)
        else:
            return True
        
    def Enabled(self):
        return bool(self._SelectedTrades()) and self._IsValidUserForAction() and SecLendMenuItemBase.Enabled(self) and self._IsValidEvent()
        

class ReCheckMenuItem(SecLendingWorkflowMenuItem):
    EVENT = 'Re-check'

    def Invoke(self, eii):
        """ Force error state if state is different from 
        or handle event to the previous state. Apply all changes if there are any.."""
        notes, parameters = self._NotesAndParameters()
        for bp in self.BusinessProcesses():
            if bp.CurrentStep().IsInErrorState():
                bp.HandleEvent("Revert")
                bp.Commit()
            elif self._SatisfiesCondition(bp, parameters):
                self._HandleEvent(bp, parameters, notes)


class ManualApproveMenuItem(SecLendingWorkflowMenuItem):
    EVENT = 'Manual approve'


class SecLendingWorkflowReplyingMenuItem(SecLendingWorkflowMenuItem):

    def Invoke(self, eii):
        if not self.VerifyValidCollection(eii):
            return
        notes, parameters = self._NotesAndParameters()
        if not self.VerifyOrderReportMapping(eii, parameters):
            return
        if not self.SetClipboardTextAndShowBuffer(eii):
            return
        self.SetRespondTrades(parameters)
        for bp in self.BusinessProcesses():
            trade = bp.Subject()
            self.SetRespondSource(eii, parameters, trade)
            if self._SatisfiesCondition(bp, parameters):
                self._HandleEvent(bp, parameters, notes)
    
    def SelectedTradesString(self):
        return ','.join([str(trade.Oid()) for trade in self._SelectedTrades(100)])
        
    def VerifyOrderReportMapping(self, eii, parameters = {}):
        destination = self.GetDestination(eii)
        if destination:
            if destination in SEC_LEND_REPORT_TO_DESTINATIONS:
                sheet = eii.Parameter('sheet') or eii.ExtensionObject().ActiveSheet()
                trade = sheet.Selection().SelectedCell().RowObject().Trade()
                try:
                    GetReportParameters(destination, trade.Counterparty())
                except Exception as e:
                    dialogMsg = "%s. Do you want to %s it anyway without a confirmation?" % (e, self.EVENT)
                    if acm.UX().Dialogs().MessageBoxYesNo(self._frame.Shell(), "Warning", dialogMsg) == 'Button1':
                        parameters.update({"Response":"NO [%s]" % e})
                        return True
                    return False
            elif destination not in  ('Clipboard', "Manual"):
                dialogMsg = "No confirmation can be sent to %s. Do you want to %s it anyway without a confirmation?" % (destination, self.EVENT)
                return acm.UX().Dialogs().MessageBoxYesNo(self._frame.Shell(), "Warning", dialogMsg ) == 'Button1'
                
        return True
        
    def VerifyValidCollection(self, eii):
        destination = eii.MenuExtension().GetString('Destination')
        if destination == '*SOURCE*':
            sources = set(trade.Market() and trade.Market().Name() for trade in self._SelectedTrades())
            if len(sources) == 1:
                destination = sources.pop()
            elif set(SEC_LEND_REPORT_TO_DESTINATIONS) & sources:
                msg = 'Trades from multiple sources %s cannot be sent in the same message' % list(sources)
                acm.UX().Dialogs().MessageBox(self._frame.Shell(), "Error", msg, 'Ok', None, None, 'Button1', 'Button3' )
                return False
            else:
                #Multiple sources but no source is a reporting source
                destination = None
                    
        if destination and destination in SEC_LEND_REPORT_TO_DESTINATIONS:
            source = '_NO_VALUE_'
            counterparty = '_NO_VALUE_'
            error = ''
            for trade in self._SelectedTrades():
                s = trade.AddInfoValue('SBL_TradeOriginId')
                if source != '_NO_VALUE_' and s != source:
                    error = 'source objects'
                cp = trade.Counterparty()
                if counterparty != '_NO_VALUE_' and cp != counterparty:
                    error = 'counterparties'
                if error:
                    msg = 'Trades from multiple %s cannot be sent in the same message' % error
                    acm.UX().Dialogs().MessageBox(self._frame.Shell(), "Error", msg, 'Ok', None, None, 'Button1', 'Button3' )
                    return False
                source = s
                counterparty = cp
            nbrOfTrades = len(self._SelectedTrades())

            if source:
                sourceTrades = acm.FAdditionalInfo.Select("addInf = 'SBL_TradeOriginId' and fieldValue = '%s'" % source)
                if sourceTrades.Size() > nbrOfTrades:
                    msg = 'Only %d of %d orders from the import where selected, do you want to send the reply anyway?' % \
                            (nbrOfTrades, sourceTrades.Size())
                    if acm.UX().Dialogs().MessageBoxYesNo(self._frame.Shell(), "Warning", msg) == 'Button1':
                        return True
                    return False
                if sourceTrades.Size() < nbrOfTrades:
                    print("ERROR - shouldn't end up here, there has to be multiple sources, %d, %d" %\
                        (sourceTrades.Size(), nbrOfTrades))
                    return False
        return True
        
    def GetDestination(self, eii, defaultValue = ''):
        destination = eii.MenuExtension().GetString('Destination', defaultValue)
        if destination == '*SOURCE*':
            sheet = eii.Parameter('sheet') or eii.ExtensionObject().ActiveSheet()
            trade = sheet.Selection().SelectedCell().RowObject().Trade()
            destination = trade.Market() and trade.Market().Name()
        return destination

    def SetClipboardTextAndShowBuffer(self, eii):
        destination = self.GetDestination(eii, eii.MenuExtension().Name().AsString())
        try:
            text = ClipBoardTextHookFromTrades(self._SelectedTrades(), self.Event())
            SetClipboardText(text)
            if destination == "Manual" and _SETTINGS.ShowRespondBuffer():
                buffer_dialog = StreamBufferDialog(text, 'Text To Clipboard', False)
                return acm.UX().Dialogs().ShowCustomDialogModal(self._frame.Shell(),
                                                        buffer_dialog.CreateLayout(), buffer_dialog)
        except Exception as e:
            print('Failed to set content to clipboard', e)
        return True
    
    def SetRespondTrades(self, parameters):
        parameters.update({"TargetTrades":self.SelectedTradesString()})
        
    def SetRespondSource(self, eii, parameters, trade):
        buttonName = eii.MenuExtension().Name().AsString()
        if buttonName == self.EVENT:
            parameters.update({"TargetSource":trade.Market() and trade.Market().Name()})
        else:
            assert acm.FMarketPlace[buttonName] is not None, \
                "No FMarketPlace named '{}' to route orders to." \
                    .format(buttonName)
            parameters.update({"TargetSource":buttonName})
            
    def Enabled(self):
        return SecLendingWorkflowMenuItem.Enabled(self) and \
               FSecLendHooks.IsCompliantToSourceMapping(self._SelectedTrades())


class RespondMenuItem(SecLendingWorkflowReplyingMenuItem):
    EVENT = 'Respond'
    
    def SelectedTradesAreNotReturns(self):
        for t in self._SelectedTrades():
            if t.Type() == 'Closing':
                return False
        return True

    def Enabled(self):
        return self.SelectedTradesAreNotReturns() and super(RespondMenuItem, self).Enabled()

class RejectMenuItem(SecLendingWorkflowReplyingMenuItem):
    EVENT = 'Reject'
    
    def SetRespondSource(self, eii, parameters, trade):
        destination = self.GetDestination(eii)
        if destination:
            assert acm.FMarketPlace[destination] is not None, \
                    "No FMarketPlace named '{}' to route orders to. The destination is specified in the menu extension '{}'" \
                    .format(destination, eii.MenuExtension().Name())
            parameters.update({"TargetSource":destination})
        else:
            parameters.update({"TargetSource":trade.Market().Name(),
                                    "Response":"NO"})


class BookMenuItem(SecLendingWorkflowReplyingMenuItem):
    EVENT = 'Book'

    def Invoke(self, eii):
        if not all(FSecLendHooks.IsValidForProcessing(trade) for trade in self._SelectedTrades()):
            acm.GetFunction('msgBox', 3)('Security Lending', "One or more trades is not suitable for booking", 0)
            return
        isOverClosing, instrument = FSecLendHooks.IsOverClosingPosition([trade for trade in self._SelectedTrades() \
            if trade.Type() == 'Closing'])
        if isOverClosing:
            acm.GetFunction('msgBox', 3)('Closing Position', "To high quantity to return for order(s) in " \
                "instrument %s. Adjust the quantity of the order(s)." %(instrument), 0)
            return    
        super(BookMenuItem, self).Invoke(eii)

    def SetRespondSource(self, eii, parameters, trade):
        destination = self.GetDestination(eii)
        if destination:
            assert acm.FMarketPlace[destination] is not None, \
                "No FMarketPlace named '{}' to route orders to. The destination is specified in the menu extension '{}'" \
                .format(destination, eii.MenuExtension().Name())
            parameters.update({"TargetSource":destination})
        else:
            parameters.update({"TargetSource":trade.Market().Name(),
                                    "Response":"NO"})


class InspectWorkflowMenuItem(SecLendingWorkflowMenuItem):

    def Invoke(self, eii):
        businessProcesses = self.BusinessProcesses()
        if len(businessProcesses) > 1:
            acm.StartApplication("Operations Manager", businessProcesses)
        elif len(businessProcesses) == 1:
            acm.StartApplication("Business Process Details", businessProcesses[0])

    def Enabled(self):
        return bool(self.BusinessProcesses())


class DeleteTradeMenuItem(SecLendingWorkflowMenuItem):

    def Invoke(self, eii):
        res = acm.UX.Dialogs().MessageBoxYesNo(self._frame.Shell(), 'Question',
                                               'Are you sure you want to delete the selected trades?')
        if res == 'Button1':  # Yes
            trades = self._SelectedTrades()
            instruments = [t.Instrument() for t in trades]
            for bp in self.BusinessProcesses():
                bp.Delete()
            for trade in trades:
                trade.Delete()
            for ins in set(instruments):
                if not ins.Trades():
                    ins.Delete()


class AssignMenuItem(SecLendingWorkflowMenuItem):

    def Invoke(self, eii):
        editedTrades = []
        assignedTrades = {}
        for trade in self._SelectedTrades():
            assignedTrades.setdefault(trade.Trader(), []).append(trade)
        with Transaction():
            for trade in self._SelectedTrades():
                if trade.StorageId() == trade.Originator().StorageId():
                    trade = trade.StorageImage()
                    trade.Trader(acm.User())
                    trade.AddInfoValue('SBL_ToDoList', eii.MenuExtension().GetString('ToDoList'))
                    trade.Commit()
                else:
                    editedTrades.append(trade)
        # Edited trades need to be handled separetly.
        # They shouldn't be commited as they're already an image of the original
        # They can't be changed within a transaction as that will mute notifications
        # The should only be changed it the transaction succeeds
        for trade in editedTrades:
            trade.Trader(acm.User())
            
        for trader, trades in assignedTrades.items():
            if trader != acm.User():
                acm.SendUserMessage([trader], "Assigned orders", "%s has assigned himself to the attached orders" % acm.User().Name(), trades)

    def Enabled(self):
        return bool(self._SelectedTrades())


class HoldMenuItem(SecLendingWorkflowMenuItem):

    def Invoke(self, eii):
        self.HoldTrade()
    
    def SetHoldTime(self, trade, time, hold):
        FSecLendHoldTrade.HoldTrade(trade, time) if hold else FSecLendHoldTrade.UnholdTrade(trade)

    def HoldTrade(self, time=None, hold=True):
        editedTrades = []
        with Transaction():
            for trade in self._SelectedTrades():
                if trade.StorageId() == trade.Originator().StorageId():
                    self.SetHoldTime(trade, time, hold)
                    trade.Commit()
                else:
                    editedTrades.append(trade)
        # Edited trades need to be handled separetly.
        # They shouldn't be commited as they're already an image of the original
        # They can't be changed within a transaction as that will mute notifications
        # The should only be changed it the transaction succeeds
        for trade in editedTrades:
            self.SetHoldTime(trade, time, hold)

class HoldOneHourMenuItem(HoldMenuItem):

    def Invoke(self, eii):
        timeOneHour = datetime.now()+timedelta(hours=1)
        self.HoldTrade(timeOneHour)


class HoldThreeHoursMenuItem(HoldMenuItem):

    def Invoke(self, eii):
        timeThreeHours = datetime.now()+timedelta(hours=3)
        self.HoldTrade(time=timeThreeHours)


class HoldEndOfDayMenuItem(HoldMenuItem):

    def Invoke(self, eii):
        if _SETTINGS.EndOfBusinessDay() is not None:
            hour, min = _SETTINGS.EndOfBusinessDay().split(':')
            timeEndOfDay = datetime.today().replace(hour=int(hour), minute=int(min), second=0, microsecond=0)
            self.HoldTrade(timeEndOfDay)
        else:
            timeEndOfDay = datetime.today().replace(hour=18, minute=0, second=0, microsecond=0)
            self.HoldTrade(timeEndOfDay)


class RemoveHoldMenuItem(HoldMenuItem):
    
    def Invoke(self, eii):
        self.HoldTrade(hold=False)


class TradeOrigin(SecLendingWorkflowMenuItem):

    def Invoke(self, eii):
        trade = self._SelectedTrades()[0]
        info = FSecLendHooks.GetTradeOriginInfo(trade)
        dlg = FSecLendUtils.InformationDialog("Trade Origin", info, 500, 500)
        acm.UX().Dialogs().ShowCustomDialog(self._frame.Shell(), dlg.CreateLayout(), dlg)

    def Enabled(self):
        enabled = False
        if len(self._SelectedTrades()) == 1:
            enabled = bool(self._SelectedTrades()[0].AddInfoValue('SBL_TradeOriginId'))
        return enabled


class FlipSignMenuItem(SecLendingWorkflowMenuItem):

    def Invoke(self, eii):
        editedTrades = []
        with Transaction():
            for trade in self._SelectedTrades():
                if trade.StorageId() == trade.Originator().StorageId():
                    trade.Quantity(-trade.Quantity())
                    trade.Commit()
                else:
                    editedTrades.append(trade)
        # Edited trades need to be handled separetly.
        # They shouldn't be commited as they're already an image of the original
        # They can't be changed within a transaction as that will mute notifications
        # The should only be changed it the transaction succeeds
        for trade in editedTrades:
            trade.Quantity(-trade.Quantity())


class ApplySuggestedFeeItem(SecLendingWorkflowMenuItem):

    def Invoke(self, eii):
        editedTrades = []
        with Transaction():
            for trade in self._SelectedTrades():
                if trade.StorageId() == trade.Originator().StorageId() and trade.StorageId() > 0:
                    FSecLendUtils.SetDefaultRate(trade) # Only changes the instrument
                    trade.Instrument().Commit()
                else:
                    editedTrades.append(trade)
        # Edited trades need to be handled separetly.
        # They shouldn't be commited as they're already an image of the original
        # They can't be changed within a transaction as that will mute notifications
        # The should only be changed it the transaction succeeds
        for trade in editedTrades:
            FSecLendUtils.SetDefaultRate(trade)


def FlipSign(eii):
    return FlipSignMenuItem(eii)


def Assign(eii):
    return AssignMenuItem(eii)

    
def Hold(eii):
    return HoldMenuItem(eii)


def HoldOneHour(eii):
    return HoldOneHourMenuItem(eii)


def HoldThreeHours(eii):
    return HoldThreeHoursMenuItem(eii)


def RemoveHold(eii):
    return RemoveHoldMenuItem(eii)
    

def HoldEndOfDay(eii):
    return HoldEndOfDayMenuItem(eii)


def InspectWorkflow(eii):
    return InspectWorkflowMenuItem(eii)


def Book(eii):
    return BookMenuItem(eii)


def ReCheck(eii):
    return ReCheckMenuItem(eii)


def Respond(eii):
    return RespondMenuItem(eii)


def Reject(eii):
    return RejectMenuItem(eii)


def ManualApprove(eii):
    return ManualApproveMenuItem(eii)


def DeleteTrade(eii):
    return DeleteTradeMenuItem(eii)


def ApplySuggestedFee(eii):
    return ApplySuggestedFeeItem(eii)
    

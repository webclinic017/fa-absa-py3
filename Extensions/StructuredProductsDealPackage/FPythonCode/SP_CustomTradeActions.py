
import acm
import types
from DealPackageDevKit import DealPackageDefinition, CommandActionBase, Object, DealPackageUserException, Bool, Str, DealPackageException
from DealPackageTradeActionBase import TradeActionBase
from DealPackageTradeActionCommands import AsFArray
from SP_DealPackageHelper import InstrumentAndDealPackageId
from FBDPCurrentContext import Logme


class SPExerciseBase(TradeActionBase):

    exDate       = Object(label      = 'Exercise Date',
                          domain     = 'date')
    
    doCommit     = Bool(defaultValue = True)
    
    priceMode    = Str(defaultValue  = 'Strike')
    
    useBdpLogme  = Bool(defaultValue = False)
    
    uiLogLevel   = Str(defaultValue  = 'Information',
                       label         = 'Log Level',
                       choiceListSource = ['Error', 'Information'],
                       visible = '@IsShowModeDetail')
        
    def OpenAfterSave(self, config):
        return None

    def CustomPanes(self):
        return [{'Exercise':'exDate;uiLogLevel;'}]

    def LogMsg(self, msg, level):
        if self.useBdpLogme:
            Logme()(msg, level)
        else:
            if level == 'ERROR' or (level == 'INFO' and self.uiLogLevel == 'Information'):
                acm.Log(msg)

class MultiSettlingExercise(SPExerciseBase):

    def AttributeOverrides(self, overrideAccumulator):
        overrideAccumulator({'exDate': dict(transform  = '@TransformExerciseDate')})

    def StartExerciseProcess(self):
    
        # validate the exercise date
        try:
            self.ValidateExerciseDateIsExpiryDate()
        except DealPackageUserException as e:
            if self.useBdpLogme is True:
                self.LogMsg('%s "(%s)"' % (str(e), InstrumentAndDealPackageId(self.OriginalDealPackage(), self.OriginalDealPackage().Trades().At(0))), 'DEBUG')
                return
            else:
                raise e

        try:
            exerciseObjects, closingDP = self.OriginalDealPackage().GetAttribute('exercise')(self.exDate)
        except DealPackageUserException as e:
            if self.useBdpLogme is True:
                self.LogMsg('%s "(%s)"' % (str(e), InstrumentAndDealPackageId(self.OriginalDealPackage(), self.OriginalDealPackage().Trades().At(0))), 'ERROR')
                return
            else:
                raise e
        except RuntimeError as e:
            msg = str(e).split(':')[-1]
            if self.useBdpLogme is True:
                self.LogMsg('%s "(%s)"' % (msg, InstrumentAndDealPackageId(self.OriginalDealPackage(), self.OriginalDealPackage().Trades().At(0))), 'ERROR')
                return
            else:
                raise DealPackageUserException(msg)

        for singleExObject in exerciseObjects:
            if singleExObject.IsKindOf(acm.FTrade):
                if self.OriginalDealPackage().IncludesTrade(singleExObject):
                    msg = 'Created exercise for %s' % (InstrumentAndDealPackageId(self.OriginalDealPackage(), singleExObject))
                    self.LogMsg(msg, 'INFO')
                else:
                    if len(self.OriginalDealPackage().Trades()) == 1:
                        msg = 'Created exercise trade for "%s"' % (InstrumentAndDealPackageId(self.OriginalDealPackage(), self.OriginalDealPackage().Trades().At(0))) 
                    else:
                        msg = 'Created exercise trade for "%s"' % (InstrumentAndDealPackageId(self.OriginalDealPackage())) 
                    self.LogMsg(msg, 'INFO')
            if singleExObject.IsKindOf(acm.FPayment):
                if len(self.OriginalDealPackage().Trades()) == 1:
                    msg = 'Created exercise for "%s"' % (InstrumentAndDealPackageId(self.OriginalDealPackage(), self.OriginalDealPackage().Trades().At(0))) 
                else:
                    msg = 'Created exercise for "%s"' % (InstrumentAndDealPackageId(self.OriginalDealPackage())) 
                self.LogMsg(msg, 'INFO')
                
            elif singleExObject.IsKindOf(acm.FInstrument):
                msg = 'Expiry %s for Instrument %s has been set to exercised' % (
                        str(self.exDate),
                        InstrumentAndDealPackageId(self.OriginalDealPackage()) )
                self.LogMsg(msg, 'INFO')

            if self.doCommit:
                self._objectsToCommit.append(singleExObject)
            else:
                if singleExObject.IsKindOf('FPayment'):
                    singleExObject.Unsimulate()

        if closingDP:
            if self.doCommit:
                # Workaround sue to issue with trade time on original, has to be reset
                originalTrades = closingDP.ChildDealPackageAt('original').Trades()
                for t in originalTrades:
                    t.TradeTime(t.Originator().TradeTime())
                # End workaround
                newClosingDP = closingDP.Save()[0]
            if len(self.OriginalDealPackage().Trades()) == 1:
                msg = 'Created closing deal package for "%s"' % (
                            InstrumentAndDealPackageId(self.OriginalDealPackage(), self.OriginalDealPackage().Trades().At(0)) )
            else:
                msg = 'Created closing deal package for "%s"' % (
                            InstrumentAndDealPackageId(self.OriginalDealPackage()) )
            self.LogMsg(msg, 'INFO')

    def TransformExerciseDate(self, attrName, newValue):
        if newValue is not None and newValue.upper() in ('T', '0D', 'TODAY'):
            return acm.Time().DateToday()
        return newValue

    def ValidateExerciseDateIsExpiryDate(self):
        if self.exDate not in self.GetAllExerciseDates():
            raise DealPackageUserException ('%s is not a valid exercise date' % str(self.exDate) )

    def GetAllExerciseDates(self):
        raise NotImplementedError('GetAllExerciseDates not implemented')

    def OnSave(self, config):
        config.InstrumentPackage("Exclude")
        config.DealPackage("Exclude")
                
        self.StartExerciseProcess()
        
        if self._objectsToCommit:
            return {'commit':self._objectsToCommit,
                    'delete':[]}

    def OnInit(self):
        self._objectsToCommit = []

    def AssemblePackage(self, arguments):
        origDp = arguments['dealPackage']
        origEdit = origDp.Edit()
        self.DealPackage().AddChildDealPackage(origEdit, 'original')
    
    def OriginalDealPackage(self):
        return self.DealPackage().ChildDealPackageAt('original')


class AccumulatorExercise(MultiSettlingExercise):

    def GetAccumulatorExpiryTable(self):
        return self.OriginalDealPackage().GetAttribute('expiryTable')

    def GetAllExerciseDates(self):
        allDates = acm.FArray()
        for expiry in self.GetAccumulatorExpiryTable():
            if acm.Time().DateDifference(acm.Time().DateToday(), expiry.Date()) >= 0:
                allDates.Add(expiry.Date())
        return allDates


class TrfExercise(MultiSettlingExercise):

    def GetTrfExpiries(self):
        return self.OriginalDealPackage().GetAttribute('exoticEvents')

    def GetAllExerciseDates(self):
        allDates = acm.FArray()
        # vvv Work-around vvv
        #       The Trade Date that sits on OriginalDealPackage() is adjusted to 
        #       the time when the deal package was copied. That trade time is 
        #       incorrect for validating the exercise date. Thus, as an against-
        #       design-work-around, fetch the trade time from the originator:
        orgTrade = self.OriginalDealPackage().Originator().Trades().First()
        tradeTime = orgTrade.TradeTime()
        # ^^^ Work-around ^^^
        for expiry in self.GetTrfExpiries():
            diffTodayExp = acm.Time().DateDifference(
                acm.Time().DateToday(), expiry.Date())
            diffTrdTimeExp = acm.Time().DateDifference(
                tradeTime, expiry.Date())
            if diffTodayExp >= 0 and diffTrdTimeExp <= 0:
                allDates.Add(expiry.Date())
        return allDates

class MultiExerciseActionBase(CommandActionBase):
    DISPLAY_NAME = 'Exercise'
    dpName = None
    statusAttr = 'tradeStatus'

    def _IsNotModified(self):
        return not self.DealPackage().IsModified()

    def _HasPastExpiries(self):
        for expiry in self.GetExpiries():
            if (acm.Time().DateDifference(acm.Time().DateToday(), expiry.Date()) >= 0 and
                acm.Time().DateDifference(self.DealPackage().Trades().At(0).TradeTime(), expiry.Date()) <= 0):
                return True
        return False
    
    def GetExpiries(self):
        raise NotImplementedError('GetExpiries() not implemented')

    def _IsValidStatus(self):
        return self.DealPackage().GetAttribute(self.statusAttr) not in ('Simulated', 'Void')

    def _LastHistoricalExpiry(self):
        lastExpiry = acm.Time().SmallDate()
        for expiry in self.GetExpiries():
            if (acm.Time().DateDifference(acm.Time().DateToday(), expiry.Date()) >= 0 and
                acm.Time().DateDifference(expiry.Date(), lastExpiry) >= 0 and 
                acm.Time().DateDifference(self.DealPackage().Trades().At(0).TradeTime(), expiry.Date()) <= 0) :
                lastExpiry = expiry.Date()
        return lastExpiry

    def _IsOpeningDealPackage(self):
        return self.DealPackage().Type() == 'Opening'

    def _IsExerciseEventType(self):
        return self.DealPackage().EventType() in ('Correct', 'Novated Assigned')

    def _IsValidTradeType(self):
        return self.DealPackage().Trades().First().Type() in ('Normal', 'Novated Assigned')

    def SelectedDate(self):
        return None

    def GetSelectedDate(self):
        selectedDate = self.SelectedDate()
        if selectedDate in ('', None):
            return None
        else:
            try:
                return acm.Time.AsDate(selectedDate)
            except:
                return None

    def __DefaultDate(self):
        selectedDate = self.GetSelectedDate()
        if (selectedDate is not None and 
           acm.Time().DateDifference(acm.Time().DateToday(), selectedDate) >=0 and
           acm.Time().DateDifference(self.DealPackage().Trades().At(0).TradeTime(), selectedDate) <= 0):
            return selectedDate
        else:
            return self._LastHistoricalExpiry()

    def Invoke(self, *args):
        newDp = acm.DealPackage.NewAsDecorator(self.dpName, self.DealPackage().GUI(), self.KeyWordArguments())
        newDp.SetAttribute('exDate', self.__DefaultDate())
        return AsFArray(newDp)

    def Enabled(self):
        return ( self._IsNotModified() and
                 self._HasPastExpiries() and
                 self._IsValidStatus() and
                 self._IsValidTradeType() and
                 (self._IsOpeningDealPackage() or self._IsExerciseEventType()) )

class AccumulatorExerciseAction(MultiExerciseActionBase):
    dpName = 'SP_AccumulatorExercise'
    statusAttr = 'tradeInput_status'

    def GetExpiries(self):
        return self.DealPackage().GetAttribute('expiryTable')

    def SelectedDate(self):
        return self.DealPackage().GetAttribute('selectedEndDate')

class TrfExerciseAction(MultiExerciseActionBase):
    dpName = 'SP_TrfExercise'

    def GetExpiries(self):
        return self.DealPackage().GetAttribute('exoticEvents')

    def SelectedDate(self):
        return self.DealPackage().GetAttribute('fixingEditer_fixingDate')
    
class CopyFieldValues(CommandActionBase):

    def Invoke(self, *args):
        fields = self.KeyWordArguments().get('FieldMapping', [])
        if type(fields) != types.ListType:
            raise DealPackageException ('"%s" action must be defined with a list of field mappings'
                                        % self.DISPLAY_NAME )

        for fieldPair in fields:
        
            if type(fieldPair) != types.DictType:
                raise DealPackageException('Each field mapping in "%s" action must be a dictionary"'
                                            % self.DISPLAY_NAME )

            if not (fieldPair.has_key('FromField') and fieldPair.has_key('ToField')):
                raise DealPackageException('Each field mapping in "%s" action must have keys "FromField" and "ToField"'
                                            % self.DISPLAY_NAME )
            
            fromValue = self.DealPackage().GetAttribute(fieldPair.get('FromField'))
            
            if hasattr(fromValue, 'IsKindOf') and fromValue.IsKindOf(acm.FCalculation):
                fromValue = fromValue.Value().Number()

            self.DealPackage().SetAttribute(fieldPair.get("ToField"), fromValue)
    
    
class UpdatePriceAction(CopyFieldValues):
    DISPLAY_NAME = 'Update prices'

class RunDealPackageAction(CommandActionBase):
    DISPLAY_NAME = "No Name Action"

    def Invoke(self, *args):
        actionName = self.KeyWordArguments().get('ActionName', None)
        if actionName is not None and self.DealPackage().HasAttribute(actionName):
            self.DealPackage().GetAttribute(actionName)()

    def Enabled(self, *args):
        return False
    
class FlipTRFBuySellAction(RunDealPackageAction):
    DISPLAY_NAME = 'Flip Buy-Sell'

    def Enabled(self, *args):
        return True    


class CheckTargetLevelAction(CommandActionBase):
    DISPLAY_NAME = 'Check Target Level'
    
    def Enabled(self, *args):
        return True
    
    def Invoke(self, *args):
        updated = self.DealPackage().GetAttribute('checkTargetLevel')()
        if updated is True:
            return self.DealPackage()
        else:
            return None

    def Applicable(self, *args):
        return False

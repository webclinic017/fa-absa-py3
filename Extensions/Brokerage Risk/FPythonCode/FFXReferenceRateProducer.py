""" Compiled: 2020-09-18 10:38:55 """

#__src_file__ = "extensions/BrokerageRisk/etc/FFXReferenceRateProducer.py"

import FPaceProducer
import FXReferenceRateMessages
import acm
import traceback
import math
import time

def CreateProducer():
    return FFXReferenceRateProducer()

def GetConfigValue(name, default):
    value = acm.GetDefaultValueFromName( acm.GetDefaultContext(), acm.FObject, name )
    if value != None:
        print('Found FExtensionValue named %s, using %s' % ( name, value ))
    else:
        print('Failed to get FExtensionValue named %s, using default: %s' % ( name, default ))
        value = default
    return value


class FFXReferenceRateProducer(FPaceProducer.Producer):
    def __init__(self):
        super(FFXReferenceRateProducer, self).__init__()
        self._tasks = {}
        self._currencies = acm.FCurrency.Select("")
        self._currencies.AddDependent(self)
        self._calcSpace = acm.Calculations().CreateStandardCalculationsSpaceCollection()
        self._fxList = []
        self._fxList.extend(FXSubscriber(self, self._currencies, self._currencies).GetFXList())
        self.updates = set()
        self.updatetime = time.time()
        self.updateInterval = self.GetUpdateInterval()

    '''
        Pace Core interface
    '''
    def OnCreateTask(self, taskId, request):
        try:
            self.Send(self._fxList, taskId)
            self._tasks.setdefault( taskId, request)
            self.SendInitialPopulateDone( taskId )
        except:
            self.SendException( taskId, traceback.format_exc() )

    def OnDoPeriodicWork(self):
        if time.time() > self.updatetime + self.updateInterval:
            self.Send(list( self.updates ))
            self.updatetime = time.time()
            self.updates.clear()

    def OnDestroyTask(self, taskId):
        if taskId in self._tasks.keys():
            self._tasks.pop( taskId )

    def SendPeriodic(self, fxCalc):
        self.updates.add(fxCalc)

    def Send(self, fxList, taskId = None, forceDelete = False):
        for fx in fxList:
            fxPair = fx.Value().Unit().Text()
            fxRate = fx.Value().Number()
            resultKey = FXReferenceRateMessages.ResultKey()
            resultKey.fromCurrency = fxPair[4:]
            resultKey.toCurrency = fxPair[:3]
            result = FXReferenceRateMessages.Result()
            result.fxReferenceRate = fxRate
            taskIds = [ taskId ] if taskId != None else self._tasks.keys()
            for tid in taskIds:
                if fxRate != 0 and not math.isnan(fxRate) and not math.isinf(fxRate) and not forceDelete:
                    self.SendInsertOrUpdate( tid, resultKey, result )
                else:
                    self.SendDelete( tid, resultKey )

    def ServerUpdate(self, sender, aspect, param):
        def eq(text, str):
            return text[:3] == str or text[4:] == str
        def not_eq(text, str):
            return text[:3] != str and text[4:] != str

        if aspect.AsString() == "remove" and len(param.Name()) == 3:
            '''
            fxDeleteList = [fx for fx in self._fxList if eq(fx.Value().Unit().Text(), param.Name())]
            print len(fxDeleteList)
            self.Send(fxDeleteList, None, True)
            '''
            self._fxList = [fx for fx in self._fxList if not_eq(fx.Value().Unit().Text(), param.Name())]
            #print len(self._fxList)
        if aspect.AsString() == "insert":
            self._fxList.extend(FXSubscriber(self, sender, [param]).GetFXList())
            self._fxList.extend(FXSubscriber(self, [param], sender).GetFXList())
            #print len(self._fxList)
        '''
        if aspect.AsString() == "update":
            fxList = [fx for fx in self._fxList if eq(fx.Value().Unit().Text(), param.Name())]
            if len(fxList) == 0:
                self._fxList.extend(FXSubscriber(self, sender, [param]).GetFXList())
                self._fxList.extend(FXSubscriber(self, [param], sender).GetFXList())
                print len(self._fxList)
            else:
                print param.Name()
        '''

    def GetUpdateInterval(self):
        '''
            Get wait time (in seconds) between updates - if set to a value > 0, the producer will cache fx rate updates 
            as they happen in real-time, but will only send them to PACE on a periodic basis.
            
            If for example the FExtensionValue 'fxReferenceRateInterval' is set to 30, an "update batch" will be send to consumers 
            once every 30 seconds with the most current fx rates (of the fx rates updated since the last "batch") at that point
            
            If set to 0, no wait occurs and updates are sent immediately
        '''
        try:
            return int( GetConfigValue( 'fxReferenceRateInterval', '0' ) )
        except:
            return 0

class FXSubscriber:
    def __init__(self, producer, fromCurrencyList, toCurrencyList):
        self._producer = producer
        self._fxList = []
        for fromCurrency in fromCurrencyList:
            if len(fromCurrency.Name()) == 3:
                for toCurrency in toCurrencyList:
                    if len(toCurrency.Name()) == 3 and fromCurrency != toCurrency:
                        fx = fromCurrency.Calculation().FXRateSource(self._producer._calcSpace, toCurrency)
                        fx.Value()
                        fx.AddDependent(self)
                        self._fxList.append(fx)

    def GetFXList(self):
        return self._fxList

    def ServerUpdate(self, sender, aspect, param):
        self._producer.SendPeriodic( sender )

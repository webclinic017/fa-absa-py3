
import acm
import datetime
from FSpanLiveParamsConsumer import Consumer
import FSpanLiveParamsTraits as TraitsModule


# only delivers risk arrays for now
class LiveCache(object):
    """A LiveCache instance caches live SPAN parameters and automatically updates them."""
    def __init__(self, initialLiveParams, queryOid, timeLimitForBadState):
        self._emptyParams = acm.FSpanLiveParameters()
        self._liveParams = self._emptyParams.Clone()
        if initialLiveParams is not None:
            self._liveParams = initialLiveParams.Clone()
        self._riskArrayConsumer = Consumer.Create(TraitsModule,
                                                  self.updateParams,
                                                  self.setBadState,
                                                  self.setGoodState,
                                                  queryOid)
        self._timeLimitForBadState = datetime.timedelta(0, int(timeLimitForBadState))
        self.hasLiveParamsGoodState = True
        self._timeWhenBadStateFirstNoticed = None
        self._logInvalid = True

    def updateParams(self, instrumentId, risk_array, delta):
        self._liveParams.AddOrReplaceRiskArray(instrumentId, risk_array)
        self._liveParams.AddOrReplaceDelta(instrumentId, delta)

    def removeInstrument(self, instrumentId):
        pass

    def getLiveParamsIfValidOtherwiseEmptyParams(self):
        rv = self._liveParams 
        if not self.hasLiveParamsGoodState:
            now = datetime.datetime.now()
            timeInBadState = now - self._timeWhenBadStateFirstNoticed
            riskArraysInvalid = timeInBadState >= self._timeLimitForBadState
            if riskArraysInvalid:
                rv = self._emptyParams
                if self._logInvalid:
                    self._logInvalid = False
                    acm.Log("Live SPAN parameters requested when invalid. Returning empty parameters.")
        return rv
        
    def setBadState(self):
        if self.hasLiveParamsGoodState:
            self._timeWhenBadStateFirstNoticed = datetime.datetime.now() 
        self.hasLiveParamsGoodState = False

    def setGoodState(self):
        self.hasLiveParamsGoodState = True
        self._timeWhenBadStateFirstNoticed = None
        self._logInvalid = True

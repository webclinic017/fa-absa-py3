""" Compiled: 2020-09-18 10:38:54 """

#__src_file__ = "extensions/structured_eq/admin/FSEQBarrierMonitoring.py"
"""----------------------------------------------------------------------------
MODULE
    FSEQBarrierMonitoring

    (c) Copyright 2006 SunGard FRONT ARENA. All rights reserved.

DESCRIPTION
    The module monitors barrier options for underlying price and
    updates their "crossed status" accordingly.

----------------------------------------------------------------------------"""
import acm
import datetime

dateDifference = acm.GetFunction('dateDifference', 2)

"""----------------------------------------------------------------------------
BarrierStrategy
    Implements the "optionStrategy"-interface used by Module FSEQOptionMonitorBase.
----------------------------------------------------------------------------"""
class BarrierStrategy:

    def __init__(self, isHiLoMonitoring):
        self.lastUpdateDateTime = datetime.datetime.now()
        self.calcSpaceCollection = acm.FCalculationSpaceCollection()
        self.createNewCalculationSpace()
        self.isHiLoMonitoring = isHiLoMonitoring

    def __getattr__(self, attrname):
        if attrname == "ListenToPriceUpdates":
            return True
        else:
            raise AttributeError(attrname)

    def createNewCalculationSpace(self):
        context = acm.GetDefaultContext()
        self.calculationSpace = self.calcSpaceCollection.GetSpace("FDealSheet", context)

    def clearCalculationSpace(self):
        self.calcSpaceCollection.Clear()
        self.createNewCalculationSpace()

    def needToCheck(self, barrierOption):

        if not barrierOption.IsBarrier():
            return False

        exotic = barrierOption.Exotic()

        if not exotic:
            acm.Log("BarrierUpdateHandler.needToCheck - instrument.Exotic returned None, instrumentId: %i"%barrierOption.Oid())
            return False

        is_expired = barrierOption.IsExpired()
        barriers_crossed = self.barriersCrossed(barrierOption)

        dateToday = acm.Time.TimeNow()
        expiryDate = barrierOption.ExpiryDate()
        valuationParameters = acm.GetFunction('mappedValuationParameters', 0)().Parameter()
        if ("Full Day" == valuationParameters.ValuationClockInterval()):
            dateCastFunction = acm.GetFunction('date', 1)
            dateToday = dateCastFunction(dateToday)
            expiryDate = dateCastFunction(expiryDate)
        barrierIsActive = barrierOption.IsKikoOption() or (acm.GetFunction('dateIsInBarrierWindow', 3)(barrierOption, dateToday, expiryDate) and not (exotic.BarrierMonitoring() == "Discrete"))

        return (not is_expired \
                and not exotic.BarrierOptionType() == "Custom" \
                and not barriers_crossed \
                and barrierIsActive)

    def checkOption(self, instrumentId, calcObject):
        instr = acm.FInstrument[instrumentId]
        try:
            exoticObj = instr.Exotic()

            # Check for already crossed or confirmed barriers.
            if self.barriersCrossed(instr):
                return False

            # Check for forward start dates beyond today.
            if exoticObj.ForwardStartType() != "None" \
                and dateDifference(exoticObj.ForwardStartDate(), acm.Time.DateToday()) > 0:
                return False

            isCrossed = False
            if instr.IsKikoOption():
                [isCrossedIn, isCrossedOut] = calcObject.Value()
                if isCrossedIn and self.monitorKikoInBarrier(exoticObj):
                    exoticObjClone = exoticObj.Clone()
                    exoticObjClone.KikoInBarrierCrossDate(str(acm.Time.DateToday()))
                    exoticObjClone.KikoInBarrierCrossedStatus("Crossed")
                    exoticObj.Apply(exoticObjClone)
                    exoticObj.Commit()
                    isCrossed = True
                if isCrossedOut and self.monitorKikoOutBarrier(exoticObj):
                    exoticObjClone = exoticObj.Clone()
                    exoticObjClone.KikoOutBarrierCrossDate(str(acm.Time.DateToday()))
                    exoticObjClone.KikoOutBarrierCrossedStatus("Crossed")
                    exoticObj.Apply(exoticObjClone)
                    exoticObj.Commit()
                    isCrossed = True
            else:
                isCrossed = calcObject.Value()
                if isCrossed:
                    exoticObjClone = exoticObj.Clone()
                    exoticObjClone.BarrierCrossDate = str(acm.Time.DateToday())
                    exoticObjClone.BarrierCrossedStatus = "Crossed"
                    exoticObj.Apply(exoticObjClone)
                    exoticObj.Commit()

            if isCrossed:
                self.logBarrierCrossed(instr)
                return True

        except Exception as msg:
            acm.Log('BarrierStrategy - Failed to update Crossed Status for instrument: %s, %s'%(instr.Name(), msg))
        return False

    def createEvaluator(self, barrierOption, context, ebTag):
        if barrierOption.IsKikoOption():
            if self.isHiLoMonitoring:
                return self.calculationSpace.CreateCalculation(barrierOption, "Monitor Kiko Barrier Is Crossed HiLo")
            return self.calculationSpace.CreateCalculation(barrierOption, "Monitor Kiko Barrier Is Crossed")
        if self.isHiLoMonitoring:
            return self.calculationSpace.CreateCalculation(barrierOption, "Monitor Barrier Is Crossed HiLo")
        return self.calculationSpace.CreateCalculation(barrierOption, "Monitor Barrier Is Crossed")


    def logBarrierCrossed(self, barrierOption):
        if self.isHiLoMonitoring:
            crossedBarrier = self.calculationSpace.CalculateValue(barrierOption, "Monitor Crossed Barrier HiLo")
        else:
            crossedBarrier = self.calculationSpace.CalculateValue(barrierOption, "Monitor Crossed Barrier")
        acm.Log('Barrier crossed - Instrument: %s, Time: %s, Barrier: %s'%(barrierOption.Name(),\
                                                                    acm.FDateTime(),\
                                                                    str(crossedBarrier)))

    def barriersCrossed(self, barrierOption):
        exotic = barrierOption.Exotic()
        barriersCrossed = False
        if exotic:
            if barrierOption.IsKikoOption():
                barriersCrossed = (not self.monitorKikoInBarrier(exotic)) and (not self.monitorKikoOutBarrier(exotic))
            else:
                barriersCrossed = exotic.BarrierCrossedStatus() in ('Confirmed', 'Crossed')
        return barriersCrossed

    def monitorKikoInBarrier(self, exotic):
        if exotic.KikoInBarrierMonitoring() == 'Continuous':
            return (exotic.KikoInBarrierCrossedStatus() not in ('Confirmed', 'Crossed')) and (exotic.KikoOutBarrierCrossedStatus() not in ('Confirmed', 'Crossed'))
        return False

    def monitorKikoOutBarrier(self, exotic):
        if exotic.KikoOutBarrierMonitoring() == 'Continuous':
            return exotic.KikoOutBarrierCrossedStatus() not in ('Confirmed', 'Crossed')
        return False

""" Compiled: 2020-09-18 10:38:50 """

#__src_file__ = "extensions/cva/adaptiv_xva/./etc/AADataCreator.py"
import acm
import AAUtilFunctions as Util
import AADataUtilFunctions as DataUtil
import AAComposer
import math
import AAParamsAndSettingsHelper as Params
import AAParameterFiltration as ParamsFilter

logger = Params.getAdaptivAnalyticsLogger()
EXCEL_EPOCH = "1899-12-31"
DEFAULT_CALENDAR = acm.FCalendar["Target"]
    
try:
    import AAValuation
except:
    logger.ELOG("Could not import module AAValuation")


def getCurrency(irCurveInformation):
    currency = irCurveInformation.CurrencySymbol()
    if not currency:
        shiftedCurve = irCurveInformation.IsKindOf("FShiftedIrCurveInformation")
        if shiftedCurve:
            origCurveInfo = irCurveInformation.OriginalCurve()
            currencyName = origCurveInfo.YieldCurveComponent().Currency().Name()
            return currencyName
        else:
            return irCurveInformation.YieldCurveComponent().Currency().Name()
    else:
        return currency.AsString()


class YCPriceFactor:
    def __init__(self, irCurveInformation, valuationDate):
        self._irCurveInformation = irCurveInformation
        self._valuationDate = valuationDate

    def getBucketDates(self, bucket_dates):
        if self._irCurveInformation.IsKindOf("FShiftedIrCurveInformation"):
            bucket_dates.append(self._irCurveInformation.BucketStartDate())
            bucket_dates.append(self._irCurveInformation.BucketDate())
            bucket_dates.append(self._irCurveInformation.BucketEndDate())

    def getPointDates(self):
        point_dates = []
        if self._irCurveInformation.IsKindOf("FShiftedIrCurveInformation"):
            curveInfo = self._irCurveInformation.OriginalCurve()
            if not curveInfo:
                curveInfo = self._irCurveInformation
            point_dates.extend(DataUtil.pointDates(curveInfo))
            point_dates.extend(acm.Curve.GenerateDates(self._valuationDate, DataUtil.lastPointDate(curveInfo), Params.getNumberOfCurvePoints()))
            self.getBucketDates(point_dates)
        elif self._irCurveInformation.IsKindOf("FIrCurveInformation"):
            curveInfo = self._irCurveInformation
            point_dates.extend(DataUtil.pointDates(curveInfo))
            point_dates.extend(acm.Curve.GenerateDates(self._valuationDate, DataUtil.lastPointDate(curveInfo), Params.getNumberOfCurvePoints()))
    	return point_dates

    def getRate(self, date):
        return 0.0

    def createYCPointsList(self):
        yc_point_list = []
        valuation_date = self._valuationDate
        point_dates = self.getPointDates()
        calendarInformation = self._irCurveInformation.CalendarInformation()
        for date in point_dates:
            if date != "":
                rate = self.getRate(date)
                year_period = calendarInformation.YearsBetween(valuation_date, date, "Act/365")
                yc_point = (year_period, rate)
                yc_point_list.append(yc_point)
        return yc_point_list

class InterestRatePriceFactor(YCPriceFactor):

    def spreadYieldCurveComponent(self):
        if self._irCurveInformation.IsKindOf("FShiftedIrCurveInformation"):
            curveInfo = self._irCurveInformation.OriginalCurve()
            if not curveInfo:
                curveInfo = self._irCurveInformation
        else:
            curveInfo = self._irCurveInformation
        yieldCurveComponent = curveInfo.YieldCurveComponent()
        if DataUtil.isSpread(yieldCurveComponent):
            return True
        else:
            return False

    def getRate(self, date):
        if self.spreadYieldCurveComponent():
            rate = self._irCurveInformation.Rate(self._valuationDate, date, "Continuous", "Act/365", 'Spot Rate', None, 1)
        else:
            rate = self._irCurveInformation.Rate(self._valuationDate, date, "Continuous", "Act/365", 'Spot Rate')
        return rate

    def createPriceFactorDictionary(self):
        price_factor = AAComposer.ComposablePriceFactorList()
        price_factor["InterestRate"] = DataUtil.getPriceFactorName(self._irCurveInformation)
        price_factor["Day_Count"] = Util.createDayCountString("Act/365")
        price_factor["Currency"] = getCurrency(self._irCurveInformation)
        price_factor["Curve"] = self.createYCPointsList()
        return price_factor

class SurvivalProbPriceFactor(YCPriceFactor):

    def getRate(self, date):
        survival_prob = self._irCurveInformation.SurvivalProbability(self._valuationDate, date)
        rate = math.fabs(math.log(survival_prob))
        return rate

    def getPointDates(self):
        point_dates = []
        # SurvivalProb requires a rate at time 0 (today)
        point_dates.append(self._valuationDate)
        point_dates.extend(YCPriceFactor.getPointDates(self))
        return point_dates

    def createPriceFactorDictionary(self):
        price_factor = AAComposer.ComposablePriceFactorList()
        price_factor["SurvivalProb"] = DataUtil.getCounterPartyID(self._irCurveInformation)
        price_factor["Recovery_Rate"] = str(self._irCurveInformation.RecoveryRate() * 0.01)
        price_factor["Curve"] = self.createYCPointsList()
        return price_factor

class SurvivalProbPriceFactorOnCurveName(SurvivalProbPriceFactor):

    def createPriceFactorDictionary(self):
        price_factor = AAComposer.ComposablePriceFactorList()
        price_factor["SurvivalProb"] = self._irCurveInformation.Name()
        price_factor["Recovery_Rate"] = str(self._irCurveInformation.RecoveryRate() * 0.01)
        price_factor["Curve"] = self.createYCPointsList()
        return price_factor

class InflationRatePriceFactor(YCPriceFactor):
    def __init__(self, irCurveInformation, valuationDate, priceIndex, instrumentFixingMethod, seasonalityAdjustment):
        YCPriceFactor.__init__(self, irCurveInformation, valuationDate)
        self._priceIndex = priceIndex
        if instrumentFixingMethod == "None":
            self._fixingMethod = priceIndex.IndexType()
        else:
            self._fixingMethod = instrumentFixingMethod
        if seasonalityAdjustment:
            self._seasonalityAdjustment = seasonalityAdjustment
        else:
            self._seasonalityAdjustment = ""

    def lag(self):
        return Util.getLag(self._fixingMethod)

    def inflationBaseDate(self):
        return DataUtil.lastPriceDate(self._priceIndex)

    def getRate(self, date):
        adjusted_inflation_base = acm.Time().DateAddDelta(self.inflationBaseDate(), 0, self.lag(), 0)
	rate = self._irCurveInformation.Rate(adjusted_inflation_base, date, "Continuous", "Act/365", 'Spot Rate')
	return rate

    def createYCPointsList(self):
        yc_point_list = []
        adjusted_inflation_base = acm.Time().DateAddDelta(self.inflationBaseDate(), 0, self.lag(), 0)
        point_dates = self.getPointDates()
        calendarInformation = self._irCurveInformation.CalendarInformation()
        for date in point_dates:
            if date and date > adjusted_inflation_base:
                rate = self.getRate(date)
                year_period = calendarInformation.YearsBetween(self.inflationBaseDate(), acm.Time().DateAddDelta(date, 0, -self.lag(), 0), "Act/365")
                yc_point = (year_period, rate)
                yc_point_list.append(yc_point)
        return yc_point_list

    def createPriceFactorDictionary(self):
	price_factor = AAComposer.ComposablePriceFactorList()
	price_factor["InflationRate"] = DataUtil.getPriceFactorName(self._irCurveInformation)
	price_factor["Price_Index"] = self._priceIndex.StringKey()
	price_factor["Seasonal_Adjustment"] = self._seasonalityAdjustment
	price_factor["Day_Count"] = Util.createDayCountString("Act/365")
	price_factor["Reference_Name"] = Util.getReferenceNameFromFixingMethod(self._fixingMethod)
	price_factor["Currency"] = getCurrency(self._irCurveInformation)
	price_factor["Curve"] = self.createYCPointsList()
	return price_factor

class ReferencePriceFactor():

    def __init__(self, inst):

        self._name = DataUtil.parameterName(inst)
        mappedPriceLink = inst.MappedPriceLink()
        self._irCurveInformation = None
        if mappedPriceLink:
            curve = mappedPriceLink.Link().YieldCurveComponent()
            self._irCurveInformation = curve.IrCurveInformation()

        self._calendar = inst.SettlementCalendar()
        if not self._calendar:
            self._calendar = DEFAULT_CALENDAR

    def getPointDates(self):
        min_date = None
        max_date = None
        dates = self._irCurveInformation.PointDates()
        for date in dates:
            if not min_date or date < min_date:
                min_date = date
            if not max_date or date > max_date:
                max_date = date

        dates = []
        date = min_date
        while date <= max_date:
            dates.append(date)
            date = self._calendar.AdjustBankingDays(date, 1)

        return dates

    #Build the DataDateCurve
    def createYCPointsList(self):
        if not self._irCurveInformation:
            return [(0, 0), (365000, 365000)]

        yc_point_list = []
        point_dates = self.getPointDates()
        for date in point_dates:
            date_int = acm.Time.DateDifference(date, EXCEL_EPOCH)
            yc_point_list.append((date_int, date_int))

        if len(yc_point_list) == 1:
            date_int = yc_point_list[0][0] + 365 * 10
            yc_point_list.append((date_int, date_int))

        return yc_point_list

    def createPriceFactorDictionary(self):
        price_factor = AAComposer.ComposablePriceFactorList()
        price_factor["ReferencePrice"] = self._name
        price_factor["Fixing_Curve"] = self.createYCPointsList()
        price_factor["ForwardPrice="] = self._name
        price_factor["Property_Aliases"] = ""
        return price_factor


class FuturePriceFactor():

    def __init__(self, future, price):
        self._future = future
        self._price = price
        
    def __createMMYYString(self, date):
        ymd = date.split('-')
        assert(len(ymd) == 3), "Invalid date format"  
        return Util.monthAbbreviation(ymd[1]).upper() + ymd[0][2:]

    def __getName(self):
        settleDate = self._future.SettlementDate()
        return self._future.Name() + "." + self.__createMMYYString(settleDate.split(' ')[0])
            
    def createPriceFactorDictionary(self):
        price_factor = AAComposer.ComposablePriceFactorList()
        price_factor["FuturesPrice"] = self.__getName()
        price_factor["Property_Aliases"] = ""
        price_factor["Price"] = self._price
        return price_factor

class ForwardPriceFactor():

    def __init__(self, inst):

        self._inst = inst
        self._name = DataUtil.parameterName(inst)
        mappedPriceLink = inst.MappedPriceLink()
        self._irCurveInformation = None
        if mappedPriceLink:
            curve = mappedPriceLink.Link().YieldCurveComponent()
            self._irCurveInformation = curve.IrCurveInformation()

        self._calendar = inst.SettlementCalendar()
        if not self._calendar:
            self._calendar = DEFAULT_CALENDAR

    #Build the DataValueCurve
    def createYCPointsList(self):

        if not self._irCurveInformation:
            return None

        SCALE = 100
        yc_point_list = []
        last_value = (0.0, "")
        for date, value in zip(self._irCurveInformation.PointDates(), self._irCurveInformation.PointValues()):
            date_int = acm.Time.DateDifference(date, EXCEL_EPOCH)
            if value:
                yc_point_list.append((date_int, value * SCALE))
                last_value = (date_int, value)

        return yc_point_list

    def createPriceFactorDictionary(self):
        price_factor = AAComposer.ComposablePriceFactorList()
        price_factor["ForwardPrice"] = self._name
        if self._irCurveInformation:
            price_factor["Curve"] = self.createYCPointsList()
        price_factor["Currency"] = self._inst.Currency().Name()
        price_factor["Fixings"] = ""
        price_factor["Property_Aliases"] = ""
        return price_factor


#The New Inflation Framework
class InflationCurvePriceFactor(InflationRatePriceFactor):
    def __init__(self, irCurveInformation, valuationDate, priceIndex, instrumentFixingMethod, seasonalityAdjustment):
        InflationRatePriceFactor.__init__(self, irCurveInformation, valuationDate, priceIndex, instrumentFixingMethod, seasonalityAdjustment)

    def curveStartDate(self):
        return DataUtil.refPriceDate(self._priceIndex)

    def getRate(self, date):
        adjusted_inflation_base = self.curveStartDate()
        rate = self._irCurveInformation.Rate(adjusted_inflation_base, date, "Continuous", "Act/365", 'Spot Rate')
        return rate

    def createYCPointsList(self):
        yc_point_list = []
        point_dates = self.getPointDates()
        calendarInformation = self._irCurveInformation.CalendarInformation()
        for date in point_dates:
            if date and date > self.inflationBaseDate():
                rate = self.getRate(date)
                year_period = calendarInformation.YearsBetween(self.inflationBaseDate(), date, "Act/365")
                yc_point = (year_period, rate)
                yc_point_list.append(yc_point)
        return yc_point_list

class PriceIndexPriceFactor():
    def __init__(self, index, valuationDate):
        self._priceIndex = index
        self._valuationDate = valuationDate

    def nextPublicationDate(self):
        # duration between last period start and next publication date should be at least 31 days
        date1 = acm.Time().DateAddDelta(acm.Time().FirstDayOfMonth(self.lastPeriodStart()), 0, 2, 0)
        date2 = acm.Time().DateAddDelta(self._valuationDate, 0, 0, 1)
        if (date2 < date1):
            return date1
        else:
            return date2

    def lastPeriodStart(self):
        return DataUtil.lastPriceDate(self._priceIndex)

    def createPriceFactorDictionary(self):
        price_factor = AAComposer.ComposablePriceFactorList()
        price_factor["PriceIndex"] = self._priceIndex.Name()
        price_factor["Currency"] = self._priceIndex.Currency().StringKey()
        price_factor["Index"] = self.createIndexList()
        price_factor["Next_Publication_Date"] = Util.createDateString(self.nextPublicationDate())
        price_factor["Last_Period_Start"] = Util.createDateString(self.lastPeriodStart())
        price_factor["Publication_Period"] = "Monthly"
        return price_factor

    def getHistoricalPriceDates(self):
        hist_dates = set()
        hist_prices = self._priceIndex.HistoricalPrices()
        for hist_price in hist_prices:
            hist_dates.add(hist_price.Day())
        return hist_dates

    def createIndexList(self):
        price_list = []
        days_between = acm.GetFunction("days_between", 4)
        priceInfo = self._priceIndex.PriceInformation()
        hist_dates = self.getHistoricalPriceDates()
        for date in hist_dates:
            price = priceInfo.GetPrice(date).Number()
            if price != 0:
                day_period = days_between('1899-12-30', date, "Act/365", None)
                index_price = (day_period, price)
                price_list.append(index_price)
        return price_list

class SeasonalFactorPriceFactor():
    def __init__(self, irCurveInformation):
        self._irCurveInformation = irCurveInformation

    def createPriceFactorDictionary(self):
	price_factor = AAComposer.ComposablePriceFactorList()
	price_factor["SeasonalFactor"] = self._irCurveInformation.StringKey()
	price_factor["Rates"] = self._irCurveInformation.PointValues()
	price_factor["Publication_Period"] = "Monthly"
	return price_factor

class MarketPriceVolatilityPriceFactor():

    def __init__(self, volatilityInformation, valuationDate, priceMapping):
        self._volatilityInformation = volatilityInformation
        self._valuationDate = valuationDate
        self._spotPrice = priceMapping.Second().Number()
        self._marketPriceName = DataUtil.parameterName(priceMapping.First())
        self._currencyName = DataUtil.parameterName(priceMapping.First().Currency())


    def createVolPointsList(self):
        vol_points = []
        #func = acm.GetFunction("absoluteStrikePriceFromRelativeInType", 3)
        strikes = self._volatilityInformation.PointStrikes()
        expiryDates = self._volatilityInformation.PointExpiryDates()
        for expiryDate, strike in zip(expiryDates, strikes):
            if strike == 0.0:
                logger.WLOG("Warning: Zero Strike Price in \"%s\". " % self._volatilityInformation.Name())
                continue
            moneyness = self._spotPrice / strike
            #absoluteStrike = func()
            vol = self._volatilityInformation.Value(expiryDate, strike)
            vol_point = (moneyness, DataUtil.getPeriodVolatility(self._valuationDate, expiryDate), vol)
            vol_points.append(vol_point)
        return vol_points

    def createVolSurfaceList(self):
        vol_surface_list = []
        dimension = 2
        vol_surface_list.append(dimension)
        vol_surface_list.append(self._volatilityInformation.ExpiryExtrapolationMethod())
        vol_surface_list.extend(self.createVolPointsList())
        return vol_surface_list

class EquityVolatilityPriceFactor(MarketPriceVolatilityPriceFactor):

    def createPriceFactorDictionary(self):
        price_factor = AAComposer.ComposablePriceFactorList()
        price_factor["EquityPriceVol"] = self._marketPriceName + '.' + self._currencyName
        price_factor["Surface"] = self.createVolSurfaceList()
        return price_factor

class CommodityVolatilityPriceFactor(MarketPriceVolatilityPriceFactor):

    def createPriceFactorDictionary(self):
        price_factor = AAComposer.ComposablePriceFactorList()
        price_factor["CommodityPriceVol"] = self._marketPriceName
        price_factor["Surface"] = self.createVolSurfaceList()
        return price_factor

class ForwardPriceVolatilityPriceFactor(MarketPriceVolatilityPriceFactor):

    def __init__(self, name, volatilityInformation, valuationDate):
        self._volatilityInformation = volatilityInformation
        self._valuationDate = valuationDate
        self._name = name

    def createPriceFactorDictionary(self):
        price_factor = AAComposer.ComposablePriceFactorList()
        price_factor["ForwardPriceVol"] = self._name
        price_factor["Surface"] = self.createVolSurfaceList()
        return price_factor

    def createVolSurfaceList(self):
        vol_points = []
        vol_points.append(3)
        vol_points.append("Flat")

        strikes = self._volatilityInformation.PointStrikes()
        expiryDates = self._volatilityInformation.PointExpiryDates()
        for expiryDate, strike in zip(expiryDates, strikes):
            moneyness = 1.0 / (1.5 - strike)
            vol_expiry = DataUtil.getPeriodVolatility(self._valuationDate, expiryDate)
            vol = self._volatilityInformation.Value(expiryDate, strike)
            vol_point = (vol_expiry, vol_expiry, moneyness, vol)
            vol_points.append(vol_point)

        return vol_points

class ReferenceVolatilityPriceFactor(MarketPriceVolatilityPriceFactor):

    def __init__(self, volatilityInformation, valuationDate, referenceVolParam):
        self._volatilityInformation = volatilityInformation
        self._valuationDate = valuationDate
        self._name = DataUtil.parameterName(referenceVolParam)

    def createPriceFactorDictionary(self):
        price_factor = AAComposer.ComposablePriceFactorList()
        price_factor["ReferenceVol"] = self._name
        price_factor["ForwardPriceVol"] = self._name
        #price_factor["Surface"] = self.createVolSurfaceList()
        return price_factor


class ConvenienceYieldPriceFactor(InterestRatePriceFactor):
    def __init__(self, name, irCurveInformation, valuationDate):
        InterestRatePriceFactor.__init__(self, irCurveInformation, valuationDate)
        self.name = name

    def createPriceFactorDictionary(self):
        price_factor = AAComposer.ComposablePriceFactorList()
        price_factor["ConvenienceYield"] = self.name
        price_factor["Currency"] = self._irCurveInformation.CurrencySymbol().AsString()
        price_factor["Curve"] = self.createYCPointsList()
        price_factor["Property_Aliases"] = ""

        return price_factor

class InterestVolatilityPriceFactor():

    def __init__(self, volatilityInformation, curveName, forwardRatesDict, valueDate):
        self._volatilityInformation = volatilityInformation
        self._curveName = curveName
        self._forwardRatesDict = forwardRatesDict
        self._valueDate = valueDate

    def createVolPointsList(self):
        vol_points = []
        undMatDates = self._volatilityInformation.PointUnderlyingMaturityDates()
        expiryDates = self._volatilityInformation.PointExpiryDates()
        strikes = self._volatilityInformation.PointStrikes()
        undMatYearFractions = self._volatilityInformation.PointUnderlyingMaturityYearFractions()
        expiryYearFractions = self._volatilityInformation.PointExpiryYearFractions()
        underlyingIsGeneric = self._volatilityInformation.PointUnderlyingMaturityIsGeneric()
        for undMatDate, expiryDate, strike, undMatYearFraction, expiryYearFraction, undIsGeneric in zip(undMatDates, expiryDates, strikes, undMatYearFractions, expiryYearFractions, underlyingIsGeneric):
            vol = self._volatilityInformation.Value(undMatDate, expiryDate, strike, True, undIsGeneric)
            vol_point = (self.convertedStrike(strike), expiryYearFraction, undMatYearFraction, vol)
            vol_points.append(vol_point)
        return vol_points

    def createVolSurfaceList(self):
        vol_surface_list = []
        dimension = 3
        vol_surface_list.append(dimension)
        vol_surface_list.append(self._volatilityInformation.ExpiryExtrapolationMethod())
        vol_surface_list.extend(self.createVolPointsList())
        return vol_surface_list

    def convertedStrike(self, strike):
        return -strike / 100.0

class InterestYieldVolPriceFactor(InterestVolatilityPriceFactor):

    def createPriceFactorDictionary(self):
        price_factor = AAComposer.ComposablePriceFactorList()
        price_factor["InterestYieldVol"] = self._curveName
        price_factor["Surface"] = self.createVolSurfaceList()
        return price_factor

class InterestRateVolPriceFactor(InterestVolatilityPriceFactor):

    def createPriceFactorDictionary(self):
        price_factor = AAComposer.ComposablePriceFactorList()
        price_factor["InterestRateVol"] = self._curveName
        price_factor["Surface"] = self.createVolSurfaceList()
        return price_factor

    def createVolPointsList(self):
        vol_points = []
        surface = self._volatilityInformation.CapFloorMoneynessSurface(self._forwardRatesDict)
        for moneyness, expiry, tenor, vol in zip(surface.At("moneyness"), surface.At("expiries"), surface.At("tenors"), surface.At("volatilities")):
            vol_point = (moneyness, expiry, tenor, vol)
            vol_points.append(vol_point)
        return vol_points

class FXVolatilityPriceFactor():

    def __init__(self, currencyPair, volatilityInformation, fxSpotPrice, valuationDate):
        self._currencyPair = currencyPair
        self._volatilityInformation = volatilityInformation
        self._valuationDate = valuationDate
        self._fxSpotPrice = fxSpotPrice.Number()

    def convertedStrike(self, strike):
        if not strike == 0.0:
            currency1 = self._currencyPair.Currency1()
            currency2 = self._currencyPair.Currency2()
            currency1Name = currency1.Name()
            currency2Name = currency2.Name()
            if currency1Name < currency2Name:
                return self._fxSpotPrice / strike
            else:
                return strike / self._fxSpotPrice
        else:
            # zero division error
            return strike

    def createVolPointsList(self):
        vol_points = []
        if self._volatilityInformation.IsKindOf("FMalzParametricVolatilityInformation"):
            point_dictionary = self._volatilityInformation.AsPointDictionary(self._fxSpotPrice, 0, 0)
            strikes = point_dictionary.At("strikes")
            expiries = point_dictionary.At("expiries")
            volatilities = point_dictionary.At("volatilities")
            i = 0
            for expiry in expiries:
                strikesAtExpiry = strikes[i]
                volatilitiesAtExpiry = volatilities[i]
                for strike, volatility in zip(strikesAtExpiry, volatilitiesAtExpiry):
                    moneyness = self.convertedStrike(strike)
                    vol_point = (moneyness, expiry, volatility)
                    vol_points.append(vol_point)
                i += 1
        else:
            strikes = self._volatilityInformation.PointStrikes()
            expiryDates = self._volatilityInformation.PointExpiryDates()
            for expiryDate, strike in zip(expiryDates, strikes):
                vol = self._volatilityInformation.Value(expiryDate, strike)
                moneyness = self.convertedStrike(strike)
                vol_point = (moneyness, DataUtil.getPeriodVolatility(self._valuationDate, expiryDate), vol)
                vol_points.append(vol_point)
        return vol_points

    def fxVolString(self):
        currency1 = self._currencyPair.Currency1()
        currency2 = self._currencyPair.Currency2()
        currency1Name = currency1.Name()
        currency2Name = currency2.Name()
        if currency1Name > currency2Name:
            fxVolString = currency2Name + '.' + currency1Name
        else:
            fxVolString = currency1Name + '.' + currency2Name
        return fxVolString

    def createVolSurfaceList(self):
        vol_surface_list = []
        dimension = 2
        vol_surface_list.append(dimension)
        vol_surface_list.append('Flat')
        vol_surface_list.extend(self.createVolPointsList())
        return vol_surface_list

    def createPriceFactorDictionary(self):
        price_factor = AAComposer.ComposablePriceFactorList()
        price_factor["FXVol"] = self.fxVolString()
        price_factor["Surface"] = self.createVolSurfaceList()
        return price_factor

def SystemParameters():
    sp_string = "<System Parameters>"
    sp_string += "\n"
    if Params.useRealTimeMarketData():
        sp_string += "Base_Currency="
        sp_string += Params.getBaseCurrency()

    return sp_string

def createFxRatesAndFxCurvesXml(fxDiscountCurves, fxRates, baseCurrency):
    price_factors = []
    if fxDiscountCurves and fxRates:
        for key in fxRates.Keys():
            price_factor = AAComposer.ComposablePriceFactorList()
            price_factor["FxRate"] = key.Text()
            if key.Text()==baseCurrency:
                price_factor["Domestic_Currency"] = ""
            else:
                price_factor["Domestic_Currency"] = baseCurrency
            price_factor["Interest_Rate"] = DataUtil.getPriceFactorName(fxDiscountCurves[key])
            spotRate = 0.0
            if isinstance(fxRates[key], int):
                spotRate = fxRates[key]
            else:
                spotRate = fxRates[key].Number()
            price_factor["Spot"] = str(spotRate)
            price_factors.append(price_factor.compose())
    return '\n'.join(price_factors)

def PriceFactors(cvaMarketDataStrings, customMarketDataString):
    xml = []
    xml.append("\n<Price Factors>")
    xml.append(cvaMarketDataStrings)
    if customMarketDataString:
        xml.append(customMarketDataString)

    return '\n'.join(xml)

def getMarketDataFilePath(calculationType, valuationDate, ignoreUseRealTimeMarketData):
    if calculationType == 'BaseValuation':
        return Params.getMarketDataFileBaseVal(valuationDate)

    if calculationType == 'CVA':
        return Params.getMarketDataFileCva(valuationDate, ignoreUseRealTimeMarketData)

    if calculationType == 'PFE':
        return Params.getMarketDataFilePfe(valuationDate, ignoreUseRealTimeMarketData)

    if calculationType == 'FVA':
        return Params.getMarketDataFileFva(valuationDate, ignoreUseRealTimeMarketData)

    logger.WLOG("Warning: Unknown calculation type \"%s\". Using default Market Data file" % calculationType)
    return Params.getMarketDataFileCva(valuationDate, ignoreUseRealTimeMarketData)

def createDataXML(systemParameters, priceFactors, valuationDate, calculationType):
    staticMarketDataFile = getMarketDataFilePath(
        calculationType=calculationType, valuationDate=valuationDate,
        ignoreUseRealTimeMarketData=False
    )
    xml = []
    xml.append("<MergeMarketData>")
    xml.append("<MarketDataFile>")
    xml.append(staticMarketDataFile)
    xml.append("</MarketDataFile>")
    xml.append("<ExplicitMarketData><![CDATA[")
    xml.append(systemParameters)
    xml.append(priceFactors)
    xml.append("]]>")
    xml.append("</ExplicitMarketData>")
    xml.append("</MergeMarketData>")
    return ''.join(xml)

def getIrCurveInformations(adaptiveYieldCurves, fxDiscountCurves, deflationCurve):
    irCurveInformations = acm.FIdentitySet()
    for curve in adaptiveYieldCurves:
        irCurveInformations.Add(curve)
    for key in fxDiscountCurves.Keys():
        irCurveInformations.Add(fxDiscountCurves.At(key))
    if deflationCurve:
        irCurveInformations.Add(deflationCurve)
    return irCurveInformations


def createPFEMarketDataXML(pfeMarketDataString, pfeCurrency, customMarketDataString, valuationDate):
    systemParameters = SystemParameters()
    priceFactors = PriceFactors('\n'.join(pfeMarketDataString), '\n'.join(customMarketDataString))
    return createDataXML(systemParameters, priceFactors, valuationDate, 'PFE')

def createMarketDataXML(cvaMarketDataString, cvaCurrency, customMarketDataString, valuationDate, calculationType):
    systemParameters = SystemParameters()
    priceFactors = PriceFactors('\n'.join(cvaMarketDataString), '\n'.join(customMarketDataString))
    return createDataXML(systemParameters, priceFactors, valuationDate, calculationType)

def createIrVolatilityStructures(curves, fxDiscountCurves, deflationCurve):
    volatilityStructures = []
    irCurveInformations = getIrCurveInformations(curves, fxDiscountCurves, deflationCurve)
    for irCurveInformation in irCurveInformations:
        vol = None
        try:
            curveInfo = irCurveInformation.OriginalCurve()
            if not curveInfo:
                curveInfo = irCurveInformation
            vol = curveInfo.YieldCurve().OriginalOrSelf().LiveEntity().AdditionalInfo().Volatility()
        except:
            vol = None
            #nothing
        if vol:
            volatilityStructures.append(vol)
    return volatilityStructures

def createFxVolatilityString(keys, volatilityInformations, fxRates, valuationDate):
    priceFactors = []
    fxVolatilityString = ''
    for key, volatilityInformation, fxRate in zip(keys, volatilityInformations, fxRates):
        if ParamsFilter.isValidFxSurface(volatilityInformation):
            priceFactor = FXVolatilityPriceFactor(key, volatilityInformation, fxRate, valuationDate).createPriceFactorDictionary()
            priceFactors.append(priceFactor.compose())
    return '\n'.join(priceFactors)

def createFxVolatilityStructures(currencies):
    dict = acm.FDictionary()
    currencyPairs = acm.FIdentitySet()
    for currency1 in currencies:
            for currency2 in currencies:
                currencyPair = currency1.CurrencyPair(currency2)
                if currencyPair:
                    currencyPairs.Add(currencyPair)
    for currencyPair in currencyPairs:
        currency1 = currencyPair.Currency1()
        currency2 = currencyPair.Currency2()
        mappingLink = currency1.MappedFXVolatilityLink(currency2)
        dict.AtPut(currencyPair, mappingLink)
    return dict

def createSurvivalCurveString(curve, valuationDate):
    if not curve:
        raise AssertionError("Credit curve not found.")
    curveString = ""
    if curve:
        price_factor = SurvivalProbPriceFactor(curve, valuationDate)
        price_factor_dict = price_factor.createPriceFactorDictionary()
        curveString = price_factor_dict.compose()
    return curveString

def createFundingSurvivalCurveString(curve, valuationDate):
    if not curve:
        raise AssertionError("Credit curve not found.")
    curveString = ""
    if curve:
        price_factor = SurvivalProbPriceFactorOnCurveName(curve, valuationDate)
        price_factor_dict = price_factor.createPriceFactorDictionary()
        curveString = price_factor_dict.compose()
    return curveString
    
def createEquityPriceString(equityPriceMappings):
    price_factors = []
    for equityPriceMapping in equityPriceMappings:
        price_factor = AAComposer.ComposablePriceFactorList()
        price_factor["EquityPrice"] = DataUtil.parameterName(equityPriceMapping.First())
        price_factor["Issuer"] = ""
        price_factor["Respect_Default"]="Yes"
        price_factor["Jump_Level"]= "0%"
        price_factor["Currency"] = DataUtil.parameterName(equityPriceMapping.First().Currency())
        price_factor["Interest_Rate"] = DataUtil.getPriceFactorName(equityPriceMapping.First().MappedDiscountLink())
        price_factor["Spot"] = str(equityPriceMapping.Second().Number())
        price_factors.append(price_factor.compose())
    return '\n'.join(price_factors)

def createEquityPriceRepoString(equityPriceMappings):
    price_factors = []
    for equityPriceMapping in equityPriceMappings:
        price_factor = AAComposer.ComposablePriceFactorList()
        price_factor["EquityPrice"] = DataUtil.parameterName(equityPriceMapping.First())
        price_factor["Issuer"] = ""
        price_factor["Respect_Default"]="Yes"
        price_factor["Jump_Level"]= "0%"
        price_factor["Currency"] = DataUtil.parameterName(equityPriceMapping.First().Currency())
        price_factor["Interest_Rate"] = DataUtil.getPriceFactorName(equityPriceMapping.First().MappedRepoLink(equityPriceMapping.First().Currency()))
        price_factor["Spot"] = str(equityPriceMapping.Second().Number())
        price_factors.append(price_factor.compose())
    return '\n'.join(price_factors)

def createCommodityPriceString(commodityPriceMappings):
    price_factors = []
    for commodityPriceMapping in commodityPriceMappings:
        price_factor = AAComposer.ComposablePriceFactorList()
        price_factor["CommodityPrice"] = DataUtil.parameterName(commodityPriceMapping.First())
        price_factor["Currency"] = DataUtil.parameterName(commodityPriceMapping.First().Currency())
        price_factor["Interest_Rate"] = DataUtil.getPriceFactorName(commodityPriceMapping.First().MappedDiscountLink())
        price_factor["Spot"] = str(commodityPriceMapping.Second().Number())
        price_factor["Property_Aliases"] = ''
        price_factors.append(price_factor.compose())
    return '\n'.join(price_factors)

def getUnderlyingCurveInfo(curve, cache, top):
    if not top:
        orig = curve.OriginalCurve()
        if not orig:
            orig = curve.YieldCurveComponent()
        curve = orig.UnderlyingCurve()
    if curve:
        if not curve in cache:
            cache.append(curve)
        getUnderlyingCurveInfo(curve, cache, 0)

def getConstituentCurveInfo(curve, cache):
    yc = acm.FYieldCurve[curve.Name()]
    if not yc or yc.Type() != 'Composite':
        return
    ycLinks = yc.YieldCurveLinks()
    for l in ycLinks:
        constituent = l.ConstituentCurve()
        if constituent:
            conIrInfo = constituent.IrCurveInformation()
            if not conIrInfo in cache:
                cache.append(conIrInfo)
                getUnderlyingCurveInfo(conIrInfo, cache, 0)

def createIrCurveString(curves, fxDiscountCurves, deflationCurve, valuationDate):
    price_factors = []
    curve_infos = []
    irCurveInformations = getIrCurveInformations(curves, fxDiscountCurves, deflationCurve)
    for irCurveInformation in irCurveInformations:
    	getUnderlyingCurveInfo(irCurveInformation, curve_infos, 1)
    	getConstituentCurveInfo(irCurveInformation, curve_infos)
    for curve in curve_infos:
        price_factor = InterestRatePriceFactor(curve, valuationDate)
        price_factor_dict = price_factor.createPriceFactorDictionary()
        price_factors.append(price_factor_dict.compose())
    return '\n'.join(price_factors)


def createInterestRateVolatilityString(volatilityInformations, forwardRatesDict, valuationDate):
    price_factors = []
    if volatilityInformations:

        for volatilityInformation in volatilityInformations:
            if ParamsFilter.isValidInterestRateVolatilitySurface(volatilityInformation):
                if volatilityInformation.CapFloorVolatilityType() == 'Par' or volatilityInformation.CapFloorVolatilityType() == 'Forward':
                    price_factor = InterestRateVolPriceFactor(volatilityInformation, DataUtil.getPriceFactorName(volatilityInformation), forwardRatesDict[volatilityInformation.OriginalVolatility().VolatilityStructure().OriginalOrSelf().LiveEntity()], valuationDate)
                else:
                    price_factor = InterestYieldVolPriceFactor(volatilityInformation, DataUtil.getPriceFactorName(volatilityInformation), None, valuationDate)
                price_factor_dict = price_factor.createPriceFactorDictionary()
                price_factors.append(price_factor_dict.compose())
    return '\n'.join(price_factors)

def createInflationCurveString(inflationComponents, valuationDate):
    inflationString = ""
    seasonalityCurves = acm.FIdentitySet()
    priceIndicies = acm.FIdentitySet()
    price_factors = []
    for component in inflationComponents:
        curve = component.First()
        priceIndex = component.Second().First()
        insFixingMethod = component.Second().Second()
        priceIndicies.Add(priceIndex)
        curveInfo = curve.OriginalCurve()
        if not curveInfo:
            curveInfo = curve
        if curveInfo.YieldCurveComponent().IsKindOf("FSeasonalityCurve"):
            #seasonalityCurves.Add(curve)
            #inflation_rate_dict = InflationRatePriceFactor(curve.UnderlyingCurve(), valuationDate, priceIndex, str(insFixingMethod), curve.StringKey()).createPriceFactorDictionary()
            logger.LOG("Seasonality curve is not supported price factor. Seasonality curve '%s' mapped to the price index '%s' won't be included in the calculations." % (curve.StringKey(), priceIndex.StringKey()))
            inflation_rate_dict = InflationRatePriceFactor(curve.UnderlyingCurve(), valuationDate, priceIndex, str(insFixingMethod), None).createPriceFactorDictionary()
        elif curveInfo.YieldCurveComponent().IsKindOf("FInflationCurve"):
            inflation_rate_dict = InflationCurvePriceFactor(curve, valuationDate, priceIndex, str(insFixingMethod), None).createPriceFactorDictionary()
        else:
            logger.LOG("This curve type has been deprecated and support will be removed from future releases.")
            inflation_rate_dict = InflationRatePriceFactor(curve, valuationDate, priceIndex, str(insFixingMethod), None).createPriceFactorDictionary()
        price_factors.append(inflation_rate_dict.compose())
    price_factors.append(createPriceIndexString(priceIndicies, valuationDate))
    price_factors.append(createSeasonalFactorString(seasonalityCurves))
    return '\n'.join(price_factors)

def createPriceIndexString(priceIndices, valuationDate):
    price_factors = []
    for index in priceIndices:
        price_index_dict = PriceIndexPriceFactor(index, valuationDate).createPriceFactorDictionary()
        price_factors.append(price_index_dict.compose())
    return '\n'.join(price_factors)

def createSeasonalFactorString(seasonalityCurves):
    price_factors = []
    for curve in seasonalityCurves:
        seasonal_factor_dict = SeasonalFactorPriceFactor(curve).createPriceFactorDictionary()
        price_factors.append(seasonal_factor_dict.compose())
    return '\n'.join(price_factors)

def createEquityVolatilityString(equityVolatilityInformations, equityPriceMappings, valuationDate):
    price_factors = []
    if equityVolatilityInformations:
        for volatilityInformation, equityPriceMapping in zip(equityVolatilityInformations, equityPriceMappings):
            if ParamsFilter.isValidEquitySurface(volatilityInformation):
                price_factor = EquityVolatilityPriceFactor(volatilityInformation, valuationDate, equityPriceMapping)
                price_factor_dict = price_factor.createPriceFactorDictionary()
                price_factors.append(price_factor_dict.compose())
    return '\n'.join(price_factors)

def createCommodityVolatilityString(commodityVolatilityInformations, commodityPriceMappings, valuationDate):
    price_factors = []
    if commodityVolatilityInformations:
        for volatilityInformation, commodityPriceMapping in zip(commodityVolatilityInformations, commodityPriceMappings):
            if ParamsFilter.isValidCommoditySurface(volatilityInformation):
                price_factor = CommodityVolatilityPriceFactor(volatilityInformation, valuationDate, commodityPriceMapping)
                price_factor_dict = price_factor.createPriceFactorDictionary()
                price_factors.append(price_factor_dict.compose())
    return '\n'.join(price_factors)


def createDividendCurve(dividendForecast, valuationDate, optionExpiry):
    dividends = dividendForecast.Dividends(valuationDate, optionExpiry, 1, 1.0)
    dividendPoints = []
    for dividend in dividends:
        date = acm.Time().AsDate(dividend.DateTime())
        dividendPoint = (acm.Time().DateDifference(date, valuationDate) / 365, dividend.Number())
        dividendPoints.append(dividendPoint)
    return dividendPoints


def createDividendString(dividendForecasts, instruments, valuationDate, optionExpiries):
    price_factors = []
    for dividendForecast, instrument, optionExpiry in zip(dividendForecasts, instruments, optionExpiries):
        if dividendForecast:
            price_factor = AAComposer.ComposablePriceFactorList()
            price_factor['DividendRate'] = DataUtil.getPriceFactorName(instrument)
            #price_factor['Floor']
            price_factor['Currency'] = DataUtil.parameterName(instrument.Currency())
            price_factor['Curve'] = createDividendCurve(dividendForecast, valuationDate, optionExpiry)
            price_factors.append(price_factor.compose())
    return '\n'.join(price_factors)


def getLastCashFlow(cashflows):
    cfLast = cashflows.Last();
    for cf in cashflows:
        if cf.EndDate() > cfLast.EndDate():
            cfLast = cf
    return cfLast


def createBenchmarkCashFlowDict(volatilityStructures, valuationDate):
    benchmarkCashFlowDict = {}
    for volatilityStructure in volatilityStructures:
        if volatilityStructure.CapFloorVolatilityType() == 'Par' or volatilityStructure.CapFloorVolatilityType() == 'Forward':
            dict = {}
            for point in volatilityStructure.Points():
                if point.Benchmark() and point.Benchmark().Legs():
                    cf = getLastCashFlow(point.Benchmark().Legs().First().CalculationCashFlows(valuationDate))
                    dict[point.Benchmark()] = cf
            benchmarkCashFlowDict[volatilityStructure.OriginalOrSelf().LiveEntity()] = dict
    return benchmarkCashFlowDict

def createConvenienceYieldString(instruments, curves, valuationDate):

    price_factors = []
    for instrument, curve in zip(instruments, curves):
        inst = instrument
        if inst.IsKindOf("FOption") or inst.IsKindOf("FFuture"):
            inst = instrument.Underlying()

        if not inst.IsKindOf("FCommodity"):
            continue

        name = DataUtil.parameterName(inst)
        price_factor = ConvenienceYieldPriceFactor(name, curve, valuationDate)
        price_factor_dict = price_factor.createPriceFactorDictionary()
        price_factors.append(price_factor_dict.compose())

    return '\n'.join(price_factors)


def createForwardPriceVolatilityString(instruments, volatilityInformations, valuationDate):

    price_factors = []
    for instrument, volatilityInformation in zip(instruments, volatilityInformations):

        if not instrument.IsKindOf("FOption") and not instrument.IsKindOf("FFuture"):
            continue

        underlying = instrument.Underlying()
        if not underlying.IsKindOf("FCommodity"):
            continue

        name = DataUtil.parameterName(underlying)
        price_factor = ForwardPriceVolatilityPriceFactor(name, volatilityInformation, valuationDate)
        price_factor_dict = price_factor.createPriceFactorDictionary()
        price_factors.append(price_factor_dict.compose())
    return '\n'.join(price_factors)


def createReferencePriceString(instruments):

    price_factors = []
    for instrument in instruments:
        inst = instrument
        if inst.IsKindOf("FOption") or inst.IsKindOf("FFuture"):
            inst = instrument.Underlying()

        if not inst.IsKindOf("FCommodity"):
            continue

        price_factor = ReferencePriceFactor(inst)
        price_factor_dict = price_factor.createPriceFactorDictionary()
        price_factors.append(price_factor_dict.compose())

    return '\n'.join(price_factors)

def createFuturePriceString(inst, price):

    price_factors = []
    if not inst.IsKindOf("FFuture"):
        return ""
    underlying = inst.Underlying()
    if not underlying.IsKindOf("FBond"):
        return ""

    if not price:
        logger.ELOG("Missing spot price for instrument %s", inst.Name())
        return ""
        
    price_factor = FuturePriceFactor(inst, price)
    price_factor_dict = price_factor.createPriceFactorDictionary()
    price_factors.append(price_factor_dict.compose())

    return '\n'.join(price_factors)

def createReferencePriceVolatilityString(instruments):

    price_factors = []
    for instrument in instruments:
        if not instrument.IsKindOf("FOption") and not instrument.IsKindOf("FFuture"):
            continue

        underlying = instrument.Underlying()
        if not underlying.IsKindOf("FCommodity"):
            continue

        name = DataUtil.parameterName(underlying)
        price_factor = AAComposer.ComposablePriceFactorList()
        price_factor["ReferenceVol"] = name
        price_factor["ForwardPriceVol="] = name
        price_factor["ReferencePrice="] = name
        price_factor["Property_Aliases"] = ""
        price_factors.append(price_factor.compose())

    return '\n'.join(price_factors)

def createForwardPriceString(instruments):

    price_factors = []
    for inst in instruments:
        if not (inst.IsKindOf("FOption") or inst.IsKindOf("FFuture")):
            continue
            
        underlying = inst.Underlying()
        if not underlying.IsKindOf("FCommodity"):
            continue

        price_factor = ForwardPriceFactor(inst)
        price_factor_dict = price_factor.createPriceFactorDictionary()
        price_factors.append(price_factor_dict.compose())

    return '\n'.join(price_factors)


def createForwardPriceVolatilityStructure(instrument):
    link = instrument.MappedVolatilityLink()
    if not link:
        return []
    return [link.Link().VolatilityStructure()]

def _getCorrelationReferenceName(ref):
    if ref.IsKindOf("FFuture") or ref.IsKindOf("FOption"):
        underlying = ref.Underlying()
        ref = underlying

    if ref.IsKindOf("FCommodity"):
        return "ReferencePrice.%s.%s" % (DataUtil.parameterName(ref).upper().replace(" ", "_"), ref.Currency().Name())

    if ref.IsKindOf("FCurrencyPair"):
        return "FxRate.%s" % DataUtil.parameterName(ref).replace("/", ".")

    logger.WLOG("WARNING: Don't know how to map correlation reference item: %s" % ref.Class().Name())
    return "Unknown.%s" % DataUtil.parameterName(ref)

def createCorrelationString(instruments):

    price_factors = []
    for instrument in instruments:
        inst = instrument
        if inst.IsKindOf("FOption") or inst.IsKindOf("FFuture"):
            inst = instrument.Underlying()

        if not inst.IsKindOf("FCommodity"):
            continue

        link = inst.MappedCorrelationLink()
        if not link:
            continue

        matrix = link.Link()
        for correlation in matrix.Correlations():
            ref1 = correlation.Reference0()
            ref2 = correlation.Reference1()
            name = "%s/%s" % (_getCorrelationReferenceName(ref2), _getCorrelationReferenceName(ref1))

            price_factor = AAComposer.ComposablePriceFactorList()
            price_factor["Correlation"] = name
            price_factor["Property_Aliases"] = ""
            price_factor["Value"] = correlation.Correlation()
            price_factors.append(price_factor.compose())

    return "\n".join(price_factors)


def createForwardPriceSampleString(instruments):

    price_factors = []
    for instrument in instruments:
        inst = instrument
        if inst.IsKindOf("FOption") or inst.IsKindOf("FFuture"):
            inst = instrument.Underlying()

        if not inst.IsKindOf("FCommodity"):
            continue

        currency = inst.Currency()
        price_factor = AAComposer.ComposablePriceFactorList()
        price_factor["ForwardPriceSample"] = currency.Name().upper()
        #"DAILY-NEXT %s" %currency.Calendar().Name().upper()
        price_factor["Offset"] = 0
        price_factor["Holiday_Calendar"] = currency.Calendar().Name()
        price_factor["Sampling_Convention"] = "ForwardPriceSampleDaily"
        price_factors.append(price_factor.compose())

    return "\n".join(price_factors)
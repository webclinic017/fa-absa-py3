import acm
import amb
import ApexCollateralUtils  as Utils
import ApexParameters

Params = ApexParameters.load()

class PositionAmountType:
    Balance = "0"
    Movement = "1"


class PositionMovementDirection:
    Receive = "1"
    Deliver = "-1"


class InstrumentProcessor(object):
    messageHandler = None

    def __init__(self, messageHandler):
        self.messageHandler = messageHandler

    def process(self, entity, date, recordNumber):
        if not entity.IsKindOf(acm.FInstrument):
            raise Exception(
                "%s cannot process entity of type %s" %
                (__name__, type(entity))
            )
        else:
            instrument = entity

        # Only process instruments with valid ISINs
        if (instrument.Isin() != '' and len(instrument.Isin()) == 12):
            message = Utils.generateMessage(instrument)
            instrumentObject = Utils.getObject(message, "INSTRUMENT")

            exDivPeriodInDays = instrument.ExCouponPeriodCount()
            if instrument.ExCouponPeriodUnit() == "Months":
                exDivPeriodInDays *= 30

            if exDivPeriodInDays > 0:
                instrumentObject.mbf_add_string(
                    "EX_DIV_PERIOD_DAYS", str(exDivPeriodInDays)
                )

            if not (
                instrument.IsKindOf(acm.FStock) or
                instrument.IsKindOf(acm.FETF)
            ):
                legObject = Utils.getObject(instrumentObject, "LEG")
                legObject.mbf_add_string(
                    "ROLLING_PERIOD_COUNT",
                    str(instrument.Legs()[0].RollingPeriodCount())
                )
                legObject.mbf_add_string(
                    "ROLLING_PERIOD_UNIT",
                    instrument.Legs()[0].RollingPeriodUnit()
                )

            self.messageHandler.handle(
                message.mbf_object_to_string_xml(), recordNumber
            )
        else:
            Utils.log("Skipping record {0}: Insrument does not have a valid ISIN"
                .format(recordNumber)
            )


def convertPrice(instrument, valueDate, fromQuotation, toQuotation, price):
    cs = acm.FCalculationMethods().CreateStandardCalculationsSpaceCollection()
    calc = instrument.Calculation().PriceConvertRounded(
        cs, price, fromQuotation, toQuotation, valueDate
    )
    cs.Clear()
    return calc.Number()


class BondPriceProcessor(object):

    def __init__(self, messageHandler):
        self.messageHandler = messageHandler
        context = acm.GetDefaultContext()
        sheetType = 'FDealSheet'
        self.calculationSpace = acm.Calculations().CreateCalculationSpace(
            context, sheetType
        )

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self.calculationSpace.Clear()

    def process(self, entity, date, recordNumber):
        if not (entity.IsKindOf(acm.FBond) or
                entity.IsKindOf(acm.FIndexLinkedBond)):
            raise Exception(
                "%s cannot process entity of type %s" %
                (__name__, type(entity))
            )
        else:
            instrument = entity
        if (instrument.Isin() == '' or len(instrument.Isin()) != 12):
            Utils.log(("Skipping record with ISIN (%s) Insrument does not have a valid ISIN", instrument.Isin()))
            return

        if date is None:
            date = acm.Time.DateNow()
        market = Params.Market
        if instrument.Currency().Name() == "ZAR":
            market = "SPOT_BESA"

        message = Utils.generateMessage(acm.FPrice())
        priceObject = Utils.getObject(message, "PRICE")
        priceObject.mbf_add_string("INSADDR.ISIN", instrument.Isin())
        priceObject.mbf_add_string("CURR.INSID", instrument.Currency().Name())
        priceObject.mbf_add_string("DATE", date)

        cal = instrument.Currency().Calendar()
        #Added 1 due to bonds only being used on the next business day
        #speak to Darrylin to explain
        spotDate = cal.AdjustBankingDays(
            date, instrument.SpotBankingDaysOffset()
        )

        if instrument.MtmFromFeed():
            usedPrice = instrument.UsedPrice(
                date, instrument.Currency(), market
            )
            print "usedPrice:", usedPrice
            price = usedPrice
        else:
            context = acm.GetDefaultContext()
            sheetType = 'FDealSheet'
            calculationSpace = acm.Calculations().CreateCalculationSpace(
                context, sheetType
            )
            calculationSpace.SimulateValue(instrument, 'Valuation Date', date)
            theorPrice = calculationSpace.CalculateValue(
                instrument, 'Price Theor').Number()
            print "theorPrice:", theorPrice
            calculationSpace.Clear()
            price = theorPrice

        dirtyPrice = convertPrice(
            instrument, spotDate,
            acm.FQuotation[instrument.Quotation().Name()],
            acm.FQuotation['Pct of Nominal'], price
        )
        cleanPrice = convertPrice(
            instrument, spotDate, acm.FQuotation['Pct of Nominal'],
            acm.FQuotation['Clean'], dirtyPrice
        )

        if dirtyPrice is not None and cleanPrice is not None:
            accruedInterest = dirtyPrice - cleanPrice
        else:
            accruedInterest = None

        priceObject.mbf_add_string("CLEAN_PRICE", str(cleanPrice / 100))
        priceObject.mbf_add_string("DIRTY_PRICE", str(dirtyPrice / 100))
        priceObject.mbf_add_string(
            "ACCRUED_INTEREST", str(accruedInterest / 100)
        )

        self.messageHandler.handle(
            message.mbf_object_to_string_xml(), recordNumber
        )


class EquityPriceProcessor(object):
    messageHandler = None

    def __init__(self, messageHandler):
        self.messageHandler = messageHandler

    def process(self, entity, date, recordNumber):
        if not (entity.IsKindOf(acm.FStock) or entity.IsKindOf(acm.FETF)):
            raise Exception(
                "%s cannot process entity of type %s" %
                (__name__, type(entity))
            )
        else:
            instrument = entity

        if (instrument.Isin() == '' or len(instrument.Isin()) != 12):
            Utils.log(("Skipping record with ISIN (%s) Insrument does not have a valid ISIN", instrument.Isin()))
            return

        if date is None:
            date = acm.Time.DateNow()
        market = Params.Market

        # Only process instruments with valid ISINs
        if (instrument.Isin() != '' and len(instrument.Isin()) == 12):
            message = Utils.generateMessage(acm.FPrice())
            priceObject = Utils.getObject(message, "PRICE")
            priceObject.mbf_add_string("INSADDR.ISIN", instrument.Isin())
            priceObject.mbf_add_string(
                "CURR.INSID", instrument.Currency().Name()
            )
            priceObject.mbf_add_string("DATE", date)

            usedPrice = instrument.UsedPrice(
                date, instrument.Currency(), market
            )
            print "usedPrice:", usedPrice
            price = usedPrice

            priceObject.mbf_add_string("CLEAN_PRICE", str(price))

            self.messageHandler.handle(
                message.mbf_object_to_string_xml(), recordNumber
            )
        else:
            Utils.log("Skipping record {0}: Insrument does not have a valid ISIN"
                .format(recordNumber)
            )


class IndexRateProcessor(object):
    messageHandler = None

    def __init__(self, messageHandler):
        self.messageHandler = messageHandler

    def process(self, entity, date, recordNumber):
        if not entity.IsKindOf(acm.FRateIndex):
            raise Exception(
                "%s cannot process entity of type %s" %
                (__name__, type(entity))
            )
        else:
            instrument = entity
        if date is None:
            date = acm.Time.DateNow()
        usedPrice = instrument.UsedPrice(date, instrument.Currency(), None)
        message = Utils.generateMessage(acm.FPrice())
        priceObject = Utils.getObject(message, "PRICE")
        priceObject.mbf_add_string("INSTRUMENT", instrument.Name())
        priceObject.mbf_add_string("CURR.INSID", instrument.Currency().Name())
        priceObject.mbf_add_string("DATE", date)

        usedPrice = instrument.UsedPrice(date, instrument.Currency(), None)
        priceObject.mbf_add_string("RATE", str(usedPrice / 100))

        self.messageHandler.handle(
            message.mbf_object_to_string_xml(), recordNumber
        )


class FXRateProcessor(object):
    messageHandler = None

    def __init__(self, messageHandler):
        self.messageHandler = messageHandler

    def process(self, entity, date, recordNumber):
        if not entity.IsKindOf(acm.FCurrency):
            raise Exception(
                "%s cannot process entity of type %s" %
                (__name__, type(entity))
            )

        quoteCurrency = entity
        rate = Utils.getFXRate(entity, acm.FMarketPlace[Params.Market], date)

        message = amb.mbf_start_message(
            None, "FXRATE", Params.MessageVersion, acm.Time.TimeNow(),
            Params.MessageSource
        )
        rateList = amb.mbf_start_list("FXRATE")
        rateList.mbf_add_string("BASE_CURRENCY", Params.BaseCurrency)
        rateList.mbf_add_string("QUOTED_CURRENCY", quoteCurrency.Name())
        if date is None:
            rateList.mbf_add_string("DATE", acm.Time.DateNow())
        else:
            rateList.mbf_add_string("DATE", date)

        rateList.mbf_add_string("RATE", str(rate))
        rateList.mbf_end_list()
        message.mbf_insert_object(rateList)
        message.mbf_end_message()

        self.messageHandler.handle(
            message.mbf_object_to_string_xml(), recordNumber
        )


class BondPositionProcessor(object):

    messageHandler = None
    positionAmountType = None

    def __init__(self, messageHandler, positionAmountType):
        self.messageHandler = messageHandler
        self.positionAmountType = positionAmountType

    def process(
            self, (portfolio, instrument, positionAmount, valueDate),
            date, recordNumber):
        if date is None:
            date = acm.Time.DateNow()
        if (instrument.Isin() == '' or len(instrument.Isin()) != 12):
            Utils.log(("Skipping record with ISIN (%s) Insrument does not have a valid ISIN", instrument.Isin()))
            return

        message = amb.mbf_start_message(
            None, "POSITION", Params.MessageVersion, acm.Time.TimeNow(),
            Params.MessageSource
        )
        positionList = amb.mbf_start_list("POSITION")
        positionList.mbf_add_string("CURR.INSID", instrument.Currency().Name())
        positionList.mbf_add_string("INSADDR.INSID", instrument.Name())
        positionList.mbf_add_string("INSADDR.ISIN", instrument.Isin())
        positionList.mbf_add_string("PRFNBR.PRFID", portfolio.Name())
        positionList.mbf_add_string("PRFNBR", str(portfolio.Oid()))
        positionList.mbf_add_string("POSITION_DATE", date)
        positionList.mbf_add_string("VALUE_DATE", valueDate)
        positionList.mbf_add_string(
            "POSITION_ID", portfolio.Name() + "|" + instrument.Isin()
        )
        positionList.mbf_add_string("AMOUNT_TYPE", self.positionAmountType)

        if self.positionAmountType == PositionAmountType.Movement:
            direction = None
            if positionAmount > 1:
                direction = PositionMovementDirection.Receive
            if positionAmount < 1:
                direction = PositionMovementDirection.Deliver

            positionList.mbf_add_string("MOVEMENT_DIRECTION", direction)
            positionAmount = abs(positionAmount)

        positionList.mbf_add_string("AMOUNT", str(round(positionAmount, 5)))

        positionList.mbf_end_list()
        message.mbf_insert_object(positionList)
        message.mbf_end_message()
        self.messageHandler.handle(
            message.mbf_object_to_string_xml(), recordNumber
        )


class EquityPositionProcessor(object):

    messageHandler = None
    positionAmountType = None

    def __init__(self, messageHandler, positionAmountType):
        self.messageHandler = messageHandler
        self.positionAmountType = positionAmountType

    def process(
            self, (portfolio, instrument, positionAmount, valueDate),
            date, recordNumber):

        if (instrument.Isin() == '' or len(instrument.Isin()) != 12):
            Utils.log(("Skipping record with ISIN (%s) Insrument does not have a valid ISIN", instrument.Isin()))
            return

        if date is None:
            date = acm.Time.DateNow()

        # Only process instruments with valid ISINs
        if (instrument.Isin() != '' and len(instrument.Isin()) == 12):

            message = amb.mbf_start_message(
                None, "POSITION", Params.MessageVersion, acm.Time.TimeNow(),
                Params.MessageSource
            )
            positionList = amb.mbf_start_list("POSITION")
            positionList.mbf_add_string(
                "CURR.INSID", instrument.Currency().Name()
            )
            positionList.mbf_add_string("INSADDR.INSID", instrument.Name())
            positionList.mbf_add_string("INSADDR.ISIN", instrument.Isin())
            positionList.mbf_add_string("PRFNBR.PRFID", portfolio.Name())
            positionList.mbf_add_string("POSITION_DATE", date)
            positionList.mbf_add_string("VALUE_DATE", valueDate)
            positionList.mbf_add_string("POSITION_ID", str(portfolio.Oid()))
            positionList.mbf_add_string("AMOUNT_TYPE", self.positionAmountType)

            if self.positionAmountType == PositionAmountType.Movement:
                direction = None
                if positionAmount > 1:
                    direction = PositionMovementDirection.Receive
                if positionAmount < 1:
                    direction = PositionMovementDirection.Deliver

                positionList.mbf_add_string("MOVEMENT_DIRECTION", direction)
                positionAmount = abs(positionAmount)

            positionList.mbf_add_string(
                "AMOUNT", str(round(positionAmount, 5))
            )

            positionList.mbf_end_list()
            message.mbf_insert_object(positionList)
            message.mbf_end_message()
            self.messageHandler.handle(
                message.mbf_object_to_string_xml(), recordNumber
            )
        else:
            Utils.log("Skipping record {0}: Insrument does not have a valid ISIN"
                .format(recordNumber)
            )


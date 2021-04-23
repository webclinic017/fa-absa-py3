'''----------------------------------------------------------------------------------------------------------
MODULE                  :       FC_SERIALIZATION
PROJECT                 :       FX onto Front Arena
PURPOSE                 :       Helper module for trade serialization
DEPARTMENT AND DESK     :       All Departments and all Desks.
REQUASTER               :       FX onto Front Arena Project
DEVELOPER               :       BBD
CR NUMBER               :       XXXXXX
----------------------------------------------------------------------------------------------------------'''
from xml.etree.ElementTree import Element, SubElement, tostring
import json
import FC_PROTOBUF_SENSITIVITY as pbSens
import FC_PORTFOLIO_INSTRUMENT_PROTOBUF as piSens
import FC_ENUMERATIONS
import FC_UTILS
import re
from FC_UTILS import FC_UTILS as UTILS

# constants
#trade serialization
rootElementName = 'trade'
serializationTypeAttributeName = 'serializationType'
tradeStaticElementName = 'static'
tradeScalarElementName = 'scalar'
tradeInstrumentElementName = 'instrument'
tradeLegsElementName = 'legs'
tradeLegElementName = 'leg'
tradeUnderlyingInstrumentsElementName = 'underlyingInstruments'
tradeUnderlyingInstrumentElementName = 'instrument'
tradeMoneyflowsElementName = 'moneyflows'
tradeMoneyflowElementName = 'moneyflow'
tradeSalesCreditsElementName = 'salesCredits'
tradeSalesCreditElementName = 'salesCredit'


def GetTradeElementXml(tradeElementName, tradeElement):
    newElement = Element(tradeElementName)
    if tradeElement:
        for key in sorted(tradeElement.CalculationResults.keys()):
            #for key in tradeElement.CalculationResults:
            attributeTag = Element(str(key))
            attributeTag.text = str(tradeElement.CalculationResults[key])
            newElement.append(attributeTag)
    return newElement

    '''
def GetElementCollectionXml(tradeElementCollectionName, tradeElementName, tradeElementCollection):
    newElement = Element(tradeElementCollectionName)
    if tradeElementCollection:
        for item in tradeElementCollection:
            childElement = Element(tradeElementName)
            for key in item.CalculationResults:
                attributeTag = Element(str(key))
                attributeTag.text = str(item.CalculationResults[key])
                childElement.append(attributeTag)
            newElement.append(childElement)
    return newElement
'''


def GetElementCollectionXml(tradeElementCollectionName, tradeElementName, tradeElementCollection):
    newElement = Element(tradeElementCollectionName)
    if tradeElementCollection:
        for tradeElement in tradeElementCollection:
            newElement.append(GetTradeElementXml(tradeElementName, tradeElement))
    return newElement


def GetElementXml(elementName, item):
    root = Element(elementName)
    if item and item.CalculationResults:
        for key in sorted(item.CalculationResults.keys()):
            element = Element(str(key))
            value = item.CalculationResults[key]
            if value and value != '':
                value = unicode(value, errors='ignore')
            element.text = str(value)
            root.append(element)
    return root


def GetSettlementAsXml(settlement):
    settlementDataElement = Element(UTILS.Constants.fcGenericConstants.SETTLEMENT)
    staticElement = GetElementXml(UTILS.Constants.fcGenericConstants.STATIC, settlement.Data)
    settlementDataElement.append(staticElement)
    #scalarElement = GetElementXml(UTILS.Constants.fcGenericConstants.SCALAR,settlement.Scalar)
    #settlementDataElement.append(scalarElement)
    return settlementDataElement


def GetTradeAsXml(trade):
    tradeDataElement = Element('trade')
    #Data
    staticElement = GetElementXml('tradeStatic', trade.Static)
    tradeDataElement.append(staticElement)
    #Scalar
    scalarElement = GetElementXml('tradeScalar', trade.Scalar)
    tradeDataElement.append(scalarElement)
    #Instrument
    instrumentElement = GetElementXml('instrument', trade.Instrument)
    tradeDataElement.append(instrumentElement)
    #Legs
    legsElement = GetElementCollectionXml('legs', 'leg', trade.Legs)
    instrumentElement.append(legsElement)
    #UnderlyingInstruments
    underlyingInstrumentsElement = GetElementCollectionXml('underlyingInstruments', 'underlyingInstrument',
                                                           trade.UnderlyingInstruments)
    instrumentElement.append(underlyingInstrumentsElement)
    #Moneyflows
    moneyflowsElement = GetElementCollectionXml('moneyflows', 'moneyflow', trade.Moneyflows)
    tradeDataElement.append(moneyflowsElement)
    #SalesCredits
    salesCreditsElement = GetElementCollectionXml('salesCredits', 'salesCredit', trade.SalesCredits)
    tradeDataElement.append(salesCreditsElement)

    underlyingKeysElement = GetElementCollectionXml('tradeUnderlyingKeys', 'tradeUnderlyingKey', trade.UnderlyingKeys)
    tradeDataElement.append(underlyingKeysElement)

    return tradeDataElement


def GetSettlementAsJSON(settlement):
    d = {UTILS.Constants.fcGenericConstants.SETTLEMENT:
             [
                 {
                     UTILS.Constants.fcGenericConstants.STATIC: [{key: settlement.Data.CalculationResults[key]}
                                                                 for key in settlement.Data.CalculationResults]
                 }
             ]
    }
    jsonResult = json.dumps(d)
    return jsonResult


def GetTradeAsJSON(trade):
    d = {UTILS.Constants.fcGenericConstants.TRADE:
             [
                 {
                     UTILS.Constants.fcGenericConstants.STATIC: [{key: trade.Static.CalculationResults[key]}
                                                                 for key in trade.Data.CalculationResults],
                     UTILS.Constants.fcGenericConstants.SCALAR: [{key: trade.Scalar.CalculationResults[key]}
                                                                 for key in trade.Scalar.CalculationResults],
                     UTILS.Constants.fcGenericConstants.INSTRUMENT_JSON: [
                         {key: trade.Instrument.CalculationResults[key]}
                         for key in trade.Instrument.CalculationResults],
                     UTILS.Constants.fcGenericConstants.LEGS:
                         [{UTILS.Constants.fcGenericConstants.LEG:
                               [{key: leg.CalculationResults[key]} for key in leg.CalculationResults],
                          } for leg in trade.Legs
                         ],
                     UTILS.Constants.fcGenericConstants.UNDERLYING_INSTRUMENTS:
                         [{UTILS.Constants.fcGenericConstants.INSTRUMENT_JSON:
                               [{key: underlying.CalculationResults[key]} for key in underlying.CalculationResults],
                          } for underlying in trade.UnderlyingInstruments
                         ],
                     UTILS.Constants.fcGenericConstants.MONEYFLOWS:
                         [{UTILS.Constants.fcGenericConstants.MONEYFLOW:
                               [{key: moneyflow.CalculationResults[key]} for key in moneyflow.CalculationResults],
                          } for moneyflow in trade.Moneyflows
                         ],
                     UTILS.Constants.fcGenericConstants.SALES_CREDITS:
                         [{UTILS.Constants.fcGenericConstants.SALES_CREDIT:
                               [{key: salesCredit.CalculationResults[key]} for key in salesCredit.CalculationResults],
                          } for salesCredit in trade.SalesCredits
                         ]
                 }
             ]
    }
    jsonResult = json.dumps(d)
    return jsonResult


#Main entry point for settlement serialization
def SerializeSettlement(serializationType, settlement):
    if not serializationType:
        raise Exception(UTILS.Constants.fcExceptionConstants.TYPE_IS_REQUIRED)
    if not settlement:
        raise Exception(UTILS.Constants.fcExceptionConstants.FC_STL_DATA_INSTANCE_MUST_BE_PROVIDED)
    #create the root element (always XML)
    attributes = {}
    attributes[UTILS.Constants.fcGenericConstants.SERIALIZATION_TYPE] = str(serializationType.name)
    rootElement = FC_UTILS.createRootElementWithAttributes(UTILS.Constants.fcGenericConstants.SETTLEMENT_DATA,
                                                           attributes)

    #Get the serialized content
    if serializationType == FC_ENUMERATIONS.SerializationType.XML:
        rootElement.append(GetSettlementAsXml(settlement))
    elif serializationType == FC_ENUMERATIONS.SerializationType.JSON:
        rootElement.text = GetSettlementAsJSON(settlement)
    elif serializationType == FC_ENUMERATIONS.SerializationType.XML_COMPRESSED:
        xmlTradeData = tostring(GetSettlementAsXml(settlement))
        rootElement.text = FC_UTILS.deflate_and_base64_encode(xmlTradeData)
    elif serializationType == FC_ENUMERATIONS.SerializationType.JSON_COMPRESSED:
        rootElement.text = FC_UTILS.deflate_and_base64_encode(GetSettlementAsJSON(settlement))
    else:
        raise Exception(UTILS.Constants.fcExceptionConstants.TYPE_S_IS_NOT_SUPPORTED % str(serializationType))

    return tostring(rootElement)


#Main entry point for trade serialization
def SerializeTrade(serializationType, trade):
    if not serializationType:
        raise Exception(UTILS.Constants.fcExceptionConstants.TYPE_IS_REQUIRED)
    if not trade:
        raise Exception(UTILS.Constants.fcExceptionConstants.FC_TRD_DATA_TYPE_MUST_BE_PROVIDED)
    #create the root element (always XML)
    attributes = {}
    attributes[UTILS.Constants.fcGenericConstants.SERIALIZATION_TYPE] = str(serializationType.name)
    rootElement = FC_UTILS.createRootElementWithAttributes(UTILS.Constants.fcGenericConstants.TRADE_DATA, attributes)

    #Get the serialized content
    if serializationType == FC_ENUMERATIONS.SerializationType.XML:
        rootElement.append(GetTradeAsXml(trade))
    elif serializationType == FC_ENUMERATIONS.SerializationType.JSON:
        rootElement.text = GetTradeAsJSON(trade)
    elif serializationType == FC_ENUMERATIONS.SerializationType.XML_COMPRESSED:
        xmlTradeData = tostring(GetTradeAsXml(trade))
        rootElement.text = FC_UTILS.deflate_and_base64_encode(xmlTradeData)
    elif serializationType == FC_ENUMERATIONS.SerializationType.JSON_COMPRESSED:
        rootElement.text = FC_UTILS.deflate_and_base64_encode(GetTradeAsJSON(trade))
    else:
        raise Exception(UTILS.Constants.fcExceptionConstants.TYPE_S_IS_NOT_SUPPORTED % str(serializationType))

    return tostring(rootElement)


def SerializeSensitivity(serializationType, sensitivity, sensType):
    dict_results = sensitivity.SensitivityWorkbook.CalculationResults
    if serializationType == FC_ENUMERATIONS.SerializationType.XML:
        return CustomDictToXMLString(dict_results, sensitivity.FObject.ClassName(), sensType)
    elif serializationType == FC_ENUMERATIONS.SerializationType.PROTOBUF:
        if sensType == UTILS.Constants.fcGenericConstants.INSTRUMENT:
            return CustomDictToProtobufInstrument(dict_results, sensitivity.InstrumentName,
                                                  sensitivity.InstrumentNumber,
                                                  sensitivity.PortfolioName, sensitivity.PortfolioNumber)
        return CustomDictToProtobuf(dict_results, sensitivity.PortfolioName, sensitivity.PortfolioNumber)
    elif serializationType == FC_ENUMERATIONS.SerializationType.JSON:
        if sensType == UTILS.Constants.fcGenericConstants.INSTRUMENT:
            return CustomInstrumentDictToJSON(dict_results)
        else:
            return CustomDictToJSON(dict_results)
    elif serializationType == FC_ENUMERATIONS.SerializationType.JSON_COMPRESSED:
        if sensType == UTILS.Constants.fcGenericConstants.INSTRUMENT:
            return FC_UTILS.deflate_and_base64_encode(CustomInstrumentDictToJSON(dict_results))
        else:
            return FC_UTILS.deflate_and_base64_encode(CustomDictToJSON(dict_results))
    else:
        raise Exception(UTILS.Constants.fcExceptionConstants.TYPE_S_IS_NOT_SUPPORTED % str(serializationType))


class dayStrings:
    def __init__(self, DayStringList):
        self.dayStringList = DayStringList
        self.char_value = {'D': 1, 'W': 7, 'M': 30.4375, 'Q': 30.4375 * 4, 'Y': 365.25}

    def number_of_days(self, date_string):
        day_char = date_string[-1:]
        if day_char in self.char_value:
            multiply = self.char_value[day_char]
            num_list = re.findall("\d+", date_string)
            if num_list:
                date_num = int(num_list[0])
                return multiply * date_num
        return 0

    def soonestFirst(self):
        date_ordered = []
        add_to_end = []
        for disord in self.dayStringList:
            disord_days = self.number_of_days(disord)
            if not (disord_days):
                add_to_end.append(disord)
                continue
            if not (date_ordered):
                date_ordered.append(disord)
                continue
            for order in date_ordered:
                order_days = self.number_of_days(order)
                index_spot = date_ordered.index(order) + 1
                if disord_days <= order_days:
                    index_spot = date_ordered.index(order)
                    break
            date_ordered.insert(index_spot, disord)
        date_ordered += add_to_end
        return date_ordered

    def oldestFirst(self):
        dayList = self.soonestFirst()
        dayList.reverse()
        return dayList


def CustomDictToJSON(dict):
    class MyEncoder(json.JSONEncoder):
        """
        JSONEncoder subclass that leverages an object's `__json__()` method,
        if available, to obtain its default JSON representation.
        """

        def default(self, obj):
            if hasattr(obj, '__json__'):
                return obj.__json__()
            return json.JSONEncoder.default(self, obj)

    class clsObject:
        def __init__(self, Workbook):
            self.workbook = Workbook

        def __json__(self):
            return {"Workbook": self.workbook}

    class clsWorkbook:
        def __init__(self, Name, Number, VerticalPortfolioSheetItem, PortfolioSheet):
            self.name = Name
            self.number = Number
            self.verticalPortfolioSheetItem = VerticalPortfolioSheetItem
            self.portfolioSheet = PortfolioSheet

        def __json__(self):
            return {"Name": self.name, "Number": self.number,
                    "FVerticalPortfolioSheet": self.verticalPortfolioSheetItem, "FPortfolioSheet": self.portfolioSheet}

    #
    # Portfolio sheet
    #
    class clsPortfolioSheetItem:
        def __init__(self):
            self.sensitivities = []

        def __json__(self):
            return {"Sensitivities": self.sensitivities}

    class clsSensitivity:
        def __init__(self, Name, Value):
            self.name = Name
            self.value = Value

        def __json__(self):
            return {"Name": self.name, "Value": self.value}

    #
    # Vertical sheet
    #
    class clsVerticalPortfolioSheetItem:
        def __init__(self):
            self.yieldSensitivity = []

        def __json__(self):
            return {"YieldSensitivities": self.yieldSensitivity}

    class clsYieldSensitivity:
        def __init__(self, Name):
            self.name = Name
            self.yieldCurves = []

        def __json__(self):
            return {"Name": self.name, "YieldCurves": self.yieldCurves}

    class clsYieldCurve:
        def __init__(self, Name):
            self.name = Name
            self.benchmarks = []

        def __json__(self):
            return {"Name": self.name, "Benchmarks": self.benchmarks}

    class clsBenchmark:
        def __init__(self, Name, Value):
            self.name = Name
            self.value = Value

        def __json__(self):
            return {"Name": self.name, "Value": self.value}

    objects = {}
    passed_attributes = {}

    #Any key that is not a tuple will be assumed to be an attribute the Object
    for tuple in dict:
        try:
            value = dict[tuple]

            if str(type(tuple)) != "<type 'tuple'>" and len(tuple) <> 5:
                passed_attributes[tuple] = value
                continue

            object = tuple[0]
            object_number = tuple[1]
            sensitivity = tuple[2]
            yieldcurve = tuple[3]
            benchmark = tuple[4]

            if object not in objects:
                workbook = clsWorkbook(object, object_number, clsVerticalPortfolioSheetItem(), clsPortfolioSheetItem())
                objO = clsObject(workbook)
                objects[object] = objO
            next = objects[object]

            if yieldcurve == "None":
                psens_list = [s.name for s in next.workbook.portfolioSheet.sensitivities if s.name == sensitivity]
                if len(psens_list) == 0:
                    ObjSens = clsSensitivity(sensitivity, value)
                    next.workbook.portfolioSheet.sensitivities.append(ObjSens)
            else:
                ysens_list = [ys.name for ys in next.workbook.verticalPortfolioSheetItem.yieldSensitivity if
                              ys.name == sensitivity]
                if len(ysens_list) == 0:
                    yieldSensitivityObj = clsYieldSensitivity(sensitivity)
                    next.workbook.verticalPortfolioSheetItem.yieldSensitivity.append(yieldSensitivityObj)
                next = \
                [ys for ys in next.workbook.verticalPortfolioSheetItem.yieldSensitivity if ys.name == sensitivity][0]
                yc_list = [yc.name for yc in next.yieldCurves if yc.name == yieldcurve]
                if len(yc_list) == 0:
                    ObjYield = clsYieldCurve(yieldcurve)
                    next.yieldCurves.append(ObjYield)
                next = [yc for yc in next.yieldCurves if yc.name == yieldcurve][0]
                bm_list = [bm.name for bm in next.benchmarks if bm.name == benchmark]
                if len(bm_list) == 0:
                    objB = clsBenchmark(benchmark, value)
                    next.benchmarks.append(objB)
        except Exception, e:
            raise Exception("JSON serialization failed with error : %s" % str(e))
    keys = objects.keys()
    if len(keys) > 0:
        return json.dumps(objects[keys[0]], cls=MyEncoder)
    else:
        return json.dumps({})


def CustomInstrumentDictToJSON(dict):
    class MyEncoder(json.JSONEncoder):
        """
        JSONEncoder subclass that leverages an object's `__json__()` method,
        if available, to obtain its default JSON representation.
        """

        def default(self, obj):
            if hasattr(obj, '__json__'):
                return obj.__json__()
            return json.JSONEncoder.default(self, obj)

    class clsObject:
        def __init__(self):
            self.workbook = []

        def __json__(self):
            return {"Workbook": self.workbook}

    class clsWorkbook:
        def __init__(self, Name, Number, VerticalPortfolioSheetItem, PortfolioSheet):
            self.name = Name
            self.number = Number
            self.verticalPortfolioSheetItem = VerticalPortfolioSheetItem
            self.portfolioSheet = PortfolioSheet

        def __json__(self):
            return {"Name": self.name, "Number": self.number,
                    "FVerticalPortfolioSheet": self.verticalPortfolioSheetItem, "FPortfolioSheet": self.portfolioSheet}

    #
    # Portfolio sheet
    #
    class clsPortfolioSheetItem:
        def __init__(self):
            self.sensitivities = []

        def __json__(self):
            return {"Sensitivities": self.sensitivities}

    class clsSensitivity:
        def __init__(self, Name, Value):
            self.name = Name
            self.value = Value

        def __json__(self):
            return {"Name": self.name, "Value": self.value}

    #
    # Vertical sheet
    #
    class clsVerticalPortfolioSheetItem:
        def __init__(self):
            self.yieldSensitivity = []

        def __json__(self):
            return {"YieldSensitivities": self.yieldSensitivity}

    class clsYieldSensitivity:
        def __init__(self, Name):
            self.name = Name
            self.yieldCurves = []

        def __json__(self):
            return {"Name": self.name, "YieldCurves": self.yieldCurves}

    class clsYieldCurve:
        def __init__(self, Name):
            self.name = Name
            self.benchmarks = []

        def __json__(self):
            return {"Name": self.name, "Benchmarks": self.benchmarks}

    class clsBenchmark:
        def __init__(self, Name, Value):
            self.name = Name
            self.value = Value

        def __json__(self):
            return {"Name": self.name, "Value": self.value}

    objects = {}
    passed_attributes = {}
    objO = clsObject()
    #Any key that is not a tuple will be assumed to be an attribute the Object
    for tuple in dict:
        try:
            value = dict[tuple]

            if str(type(tuple)) != "<type 'tuple'>" and len(tuple) <> 5:
                passed_attributes[tuple] = value
                continue

            object = tuple[0]
            object_number = tuple[1]
            sensitivity = tuple[2]
            yieldcurve = tuple[3]
            benchmark = tuple[4]

            if object not in objO.workbook:
                workbook = clsWorkbook(object, object_number, clsVerticalPortfolioSheetItem(), clsPortfolioSheetItem())
                objO.workbook.append(workbook)
                #objects[object] = objO
            next = [obj for obj in objO.workbook if obj.name == object][0]

            if yieldcurve == "None":
                psens_list = [s.name for s in next.portfolioSheet.sensitivities if s.name == sensitivity]
                if len(psens_list) == 0:
                    ObjSens = clsSensitivity(sensitivity, value)
                    next.portfolioSheet.sensitivities.append(ObjSens)
            else:
                ysens_list = [ys.name for ys in next.verticalPortfolioSheetItem.yieldSensitivity if
                              ys.name == sensitivity]
                if len(ysens_list) == 0:
                    yieldSensitivityObj = clsYieldSensitivity(sensitivity)
                    next.verticalPortfolioSheetItem.yieldSensitivity.append(yieldSensitivityObj)
                next = [ys for ys in next.verticalPortfolioSheetItem.yieldSensitivity if ys.name == sensitivity][0]
                yc_list = [yc.name for yc in next.yieldCurves if yc.name == yieldcurve]
                if len(yc_list) == 0:
                    ObjYield = clsYieldCurve(yieldcurve)
                    next.yieldCurves.append(ObjYield)
                next = [yc for yc in next.yieldCurves if yc.name == yieldcurve][0]
                bm_list = [bm.name for bm in next.benchmarks if bm.name == benchmark]
                if len(bm_list) == 0:
                    objB = clsBenchmark(benchmark, value)
                    next.benchmarks.append(objB)
        except Exception, e:
            print str(e)
    return json.dumps(objO, cls=MyEncoder)


def CustomDictToXMLString(dict, className, sensType):
    #<SensitivityData>
    #  <FClassName name="MAN_Bond">
    #    <FPortfolioSheet>
    #      <Sensitivity name="Vega">
    #        <Value>0.00000198</Value>
    #      </Sensitivity>
    #    </FPortfolioSheet>
    #    <FVerticalPortfolioSheet>
    #      <Sensitivity name="Interest Rate Benchmark Delta Per Yield Curve">
    #        <YieldCurve name="ZAR-SWAP">
    #          <Benchmark name="1 D">
    #            <Value>0.00000198</Value>
    #          </Benchmark>
    #        </YieldCurve>
    #      </Sensitivity>
    #    </FVerticalPortfolioSheet>
    #  </FClassName>
    #</SensitivityData>

    class clsObject:
        def __init__(self, Name, Number):
            self.name = Name
            self.number = Number
            self.sensitivities = {}

    class clsPortfolioSheetItem:
        kind = 'clsPortfolioSheetItem'

        def __init__(self, Name, Value):
            self.name = Name
            self.value = Value

    class clsVerticalPortfolioSheetItem:
        kind = 'clsVerticalPortfolioSheetItem'

        def __init__(self, Name):
            self.name = Name
            self.yieldcurves = {}

    class clsYieldcurve:
        def __init__(self, Name):
            self.name = Name
            self.benchmarks = {}

    class clsBenchmark:
        def __init__(self, Name, Value):
            self.name = Name
            self.value = Value

    objects = {}
    passed_attributes = {}
    #Any key that is not a tuple will be assumed to be an attribute the Object
    for tuple in dict:
        value = dict[tuple]

        if str(type(tuple)) != "<type 'tuple'>" and len(tuple) <> 5:
            passed_attributes[tuple] = value
            continue

        object = tuple[0]
        number = tuple[1]
        sensitivity = tuple[2]
        yieldcurve = tuple[3]
        benchmark = tuple[4]

        if object not in objects:
            objO = clsObject(object, number)
            objects[object] = objO
        next = objects[object]

        if yieldcurve == "None":
            if sensitivity not in next.sensitivities:
                ObjSens = clsPortfolioSheetItem(sensitivity, value)
                next.sensitivities[sensitivity] = ObjSens
        else:
            if sensitivity not in next.sensitivities:
                ObjSens = clsVerticalPortfolioSheetItem(sensitivity)
                next.sensitivities[sensitivity] = ObjSens
            next = next.sensitivities[sensitivity]

            if yieldcurve not in next.yieldcurves:
                ObjYield = clsYieldcurve(yieldcurve)
                next.yieldcurves[yieldcurve] = ObjYield
            next = next.yieldcurves[yieldcurve]

            if benchmark not in next.benchmarks:
                objB = clsBenchmark(benchmark, value)
                next.benchmarks[benchmark] = objB

    root = Element("Workbook")
    elSensTypeS = None
    elSensTypeC = None
    for p in objects:
        elClass = root
        if sensType == UTILS.Constants.fcGenericConstants.INSTRUMENT:
            elSensTypeS = None
            elSensTypeC = None
            elClass = SubElement(root, className)

        elClass.set("name", p)
        elClass.set("number", str(objects[p].number))
        for attr in passed_attributes:
            attr_value = passed_attributes[attr]
            elAttr = SubElement(elClass, attr)
            elAttr.text = attr_value
        for sens_n, sens_o in objects[p].sensitivities.iteritems():
            if sens_o.kind == 'clsPortfolioSheetItem':
                if not (elSensTypeS):
                    elSensTypeS = SubElement(elClass, "FPortfolioSheet")
                elSensName = SubElement(elSensTypeS, "Sensitivities")
                elSensName.set("name", sens_n)
                elSensName.set("value", sens_o.value)
            else:
                if not (elSensTypeC):
                    elSensTypeC = SubElement(elClass, "FVerticalPortfolioSheet")
                    elSensName = SubElement(elSensTypeC, "YieldSensitivities")
                elSensName.set("name", sens_n)
                for yield_n, yield_o in sens_o.yieldcurves.iteritems():
                    elYieldCurve = SubElement(elSensName, "YieldCurves")
                    elYieldCurve.set("name", yield_n)
                    DayStringList = dayStrings(yield_o.benchmarks.keys())
                    for bench_n in DayStringList.soonestFirst():
                        bench_o = yield_o.benchmarks[bench_n]
                        elBenchMark = SubElement(elYieldCurve, "Benchmarks")
                        elBenchMark.set("name", bench_n)
                        elBenchMark.set("value", bench_o.value)
    return tostring(root)


# Some instrument name EG ZAR/JI/151127-171229/#6£4 contain non ascii
def safe_unicode(obj, *args):
    """ return the unicode representation of obj """
    try:
        return unicode(obj, *args)
    except UnicodeDecodeError:
        # obj is byte string
        ascii_text = str(obj).encode('string_escape')
        return unicode(ascii_text)


def CustomDictToProtobuf(dict, objName, objNumber):
    def set_benchmarks(yield_curve, benchDict):
        DayStringList = dayStrings(benchDict.keys())
        for benchmark_name in DayStringList.soonestFirst():
            benchmark = yield_curve.Benchmarks.add()
            benchmark.Name = benchmark_name
            benchmark.Value = benchDict[benchmark_name]

    def get_yieldCurve(yield_sensitivity, name):
        #If it already exists, return it. Else create it
        for yield_curve in yield_sensitivity.YieldCurves:
            if yield_curve.Name == name:
                return yield_curve
        yield_curve = yield_sensitivity.YieldCurves.add()
        yield_curve.Name = name
        return yield_curve

    def get_yieldSensitivity(vertical_portfolio_sheet, name):
        #If it already exists, return it. Else create it
        for yield_sensitivity in vertical_portfolio_sheet.YieldSensitivities:
            if yield_sensitivity.Name == name:
                return yield_sensitivity
        yield_sensitivity = vertical_portfolio_sheet.YieldSensitivities.add()
        yield_sensitivity.Name = name
        return yield_sensitivity

    def append_yieldSensitivity(vPortSheet, sensitivity_name, yield_curve_name, benchDict):
        yield_sensitivity = get_yieldSensitivity(vPortSheet, sensitivity_name)
        yield_curve = get_yieldCurve(yield_sensitivity, yield_curve_name)
        set_benchmarks(yield_curve, benchDict)

    def append_sensitivity(portSheet, sens_name, sens_value):
        sensitivity = portSheet.Sensitivities.add()
        sensitivity.Name = sens_name
        sensitivity.Value = sens_value

    sensData = pbSens.SensitivityData()
    workbook = sensData.Workbook
    PortDict = {}
    vPortDict = {}

    #tuple -> (instrument/portfolio,sensitivity,yieldcurve,benchmark)
    for tuple in dict:
        sensitivity = tuple[2]
        yieldcurve = tuple[3]
        benchmark = tuple[4]
        try:
            value = float(dict[tuple])
        except:
            continue

        if not (workbook.Name): workbook.Name = safe_unicode(objName)  #tuple[0]

        if workbook.Number is 0: workbook.Number = objNumber  #tuple[1]

        #FPortfolioSheet
        if yieldcurve == "None":
            PortDict[sensitivity] = value
        #FVerticalPortfolioSheet
        else:
            if (sensitivity, yieldcurve) not in vPortDict:
                vPortDict[(sensitivity, yieldcurve)] = {benchmark: value}
            else:
                bDict = vPortDict[(sensitivity, yieldcurve)]
                bDict[benchmark] = value
                vPortDict[(sensitivity, yieldcurve)] = bDict

    if PortDict:
        portSheet = workbook.FPortfolioSheet
        for sens in PortDict:
            append_sensitivity(portSheet, sens, PortDict[sens])

    if vPortDict:
        vPortSheet = workbook.FVerticalPortfolioSheet
        for sensTuple, benchDict in vPortDict.iteritems():
            append_yieldSensitivity(vPortSheet, sensTuple[0], sensTuple[1], benchDict)

    serializedData = sensData.SerializeToString()
    #deserializedData = pbSens.SensitivityData()
    #deserializedData.ParseFromString(serializedData)
    return serializedData


def CustomDictToProtobufInstrument(dict, instrumentName, instrumentNumber, portfolioName, portfolioNumber):
    def set_benchmarks(yield_curve, benchDict):
        DayStringList = dayStrings(benchDict.keys())
        for benchmark_name in DayStringList.soonestFirst():
            benchmark = yield_curve.Benchmarks.add()
            benchmark.Name = benchmark_name
            benchmark.Value = benchDict[benchmark_name]

    def get_yieldCurve(yield_sensitivity, name):
        #If it already exists, return it. Else create it
        for yield_curve in yield_sensitivity.YieldCurves:
            if yield_curve.Name == name:
                return yield_curve
        yield_curve = yield_sensitivity.YieldCurves.add()
        yield_curve.Name = name
        return yield_curve

    def get_yieldSensitivity(vertical_portfolio_sheet, name):
        #If it already exists, return it. Else create it
        for yield_sensitivity in vertical_portfolio_sheet.YieldSensitivities:
            if yield_sensitivity.Name == name:
                return yield_sensitivity
        yield_sensitivity = vertical_portfolio_sheet.YieldSensitivities.add()
        yield_sensitivity.Name = name
        return yield_sensitivity

    def append_yieldSensitivity(vPortSheet, sensitivity_name, yield_curve_name, benchDict):
        yield_sensitivity = get_yieldSensitivity(vPortSheet, sensitivity_name)
        yield_curve = get_yieldCurve(yield_sensitivity, yield_curve_name)
        set_benchmarks(yield_curve, benchDict)

    def append_sensitivity(portSheet, sens_name, sens_value):
        sensitivity = portSheet.Sensitivities.add()
        sensitivity.Name = sens_name
        sensitivity.Value = sens_value

    sensData = piSens.PortfolioInstrumentData()
    workbook = sensData.PortfolioInstrumentWorkbook
    PortDict = {}
    vPortDict = {}

    #tuple -> (instrument/portfolio,sensitivity,yieldcurve,benchmark)
    for tuple in dict:
        sensitivity = tuple[2]
        yieldcurve = tuple[3]
        benchmark = tuple[4]
        try:
            value = float(dict[tuple])
        except:
            continue

        if not (workbook.InstrumentName): workbook.InstrumentName = safe_unicode(instrumentName)
        if workbook.InstrumentNumber is 0: workbook.InstrumentNumber = instrumentNumber
        if not (workbook.PortfolioName): workbook.PortfolioName = safe_unicode(portfolioName)
        if workbook.PortfolioNumber is 0: workbook.PortfolioNumber = portfolioNumber

        #FPortfolioSheet
        if yieldcurve == "None":
            PortDict[sensitivity] = value
        #FVerticalPortfolioSheet
        else:
            if (sensitivity, yieldcurve) not in vPortDict:
                vPortDict[(sensitivity, yieldcurve)] = {benchmark: value}
            else:
                bDict = vPortDict[(sensitivity, yieldcurve)]
                bDict[benchmark] = value
                vPortDict[(sensitivity, yieldcurve)] = bDict

    if PortDict:
        portSheet = workbook.PortfolioSheet
        for sens in PortDict:
            append_sensitivity(portSheet, sens, PortDict[sens])

    if vPortDict:
        vPortSheet = workbook.VerticalPortfolioSheet
        for sensTuple, benchDict in vPortDict.iteritems():
            append_yieldSensitivity(vPortSheet, sensTuple[0], sensTuple[1], benchDict)

    serializedData = sensData.SerializeToString()
    #deserializedData = pbSens.SensitivityData()
    #deserializedData.ParseFromString(serializedData)
    return serializedData

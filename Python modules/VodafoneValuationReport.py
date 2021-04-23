"""
Vodafone valuation report


History
=======

2014-02-06 Dusan Fasko      CHNG0001698447 Initial deployment; requested by Angelique Macnabe.
2017-05-24 Vojtech Sidorin  FAU-938 Update dependency on elementtree.
"""

import acm
from at_ael_variables import AelVariableHandler
import at_report
import collections
import xml.etree.ElementTree as ElementTree
import os


ael_gui_parameters = {
    'windowCaption': 'Generate the report',
    'runButtonLabel': '&&Generate',
    'closeWhenFinished': True
}

ael_variables = AelVariableHandler()


ael_variables.add(
    'instrument_id',
    label = 'InstrumenID of required instrument',
    default = 'ZAR-GBP/CCS/F-F/130515-160516/0.722',
    mandatory = True,
    alt = 'InstrumenID (insid) of required instrument'
)


ael_variables.add(
    'report_title',
    label = 'Title of the report',
    default = "GBP/ZAR CCIRS Pricer",
    mandatory = True,
    alt = 'Title of the report'
)


ael_variables.add(
    'target_folder',
    label = 'Target folder path',
    default = os.path.join("C:\\", "temp", "FAReports", "VodafoneValuationReport"),
    mandatory = True,
    alt = 'Path to folder where the file will be stored'
)

ael_variables.add(
    'file_name',
    label = 'File name',
    default = "VodafoneValuationReport",
    mandatory = True,
    alt = 'Report file name'
)


def ael_main(params):
    """Main run creates the valuation report and save it as a file."""

    xsl_template = acm.GetDefaultContext().GetExtension(
        'FXSLTemplate', 'FObject', 'VodafoneValuationReport')

    report = ReportCreator(file_name=params['file_name'], file_suffix="xls",
        path=params['target_folder'], xsl_template=xsl_template, 
        instrument_id=params['instrument_id'], title=params['report_title'])

    report.create_report()


class ReportCreator(at_report.DataToXMLReportCreator):
    """Class responsible for creating the valuation report."""

    # To be refactored

    @staticmethod
    def validate_string_length(value, min_length=None, max_length=None):
        """Validate the length of string. 
        
        Should return list of validation messages.

        """

        validation_errors = list()

        if min_length and len(value) < min_length:
            msg = "{0} should be at least {1} characters long.".format(
                value, min_length)
            validation_errors.append(msg)

        if max_length and len(value) > max_length:
            msg = "{0} shouldn't be longer than {1} characters.".format(
                value, max_length)
            validation_errors.append(msg)

        return validation_errors
    # /To be refactored


    def __init__(self, file_name, file_suffix, path,
        xsl_template, instrument_id, title):

        super(ReportCreator, self).__init__(
            file_name=file_name,
            file_suffix=file_suffix,
            path=path,
            xsl_template=xsl_template)

        self.file_name = file_name + "-" + self.date
        self.title = title
        self.instrument = acm.FInstrument[instrument_id]
        self.xsl_template = xsl_template

        self.pay_leg = None
        self.receive_leg = None

        self.currency_from = None
        self.currency_to = None
        self.currency_usd = None

        self.pay_leg_yield_curve = None
        self.receive_leg_yield_curve = None
        self.pay_leg_sumary = None
        self.receive_leg_sumary = None

        self.fx_spot_ratio = 0
        self.valuation = []
        self.yield_curves = dict()
        self.calculation_space = (
            acm.Calculations().CreateStandardCalculationsSpaceCollection())

        # To be refactored

        self.validation_errors = []
        self.validation_errors.extend(
            self.validate_string_length(
                file_suffix, min_length=2, max_length=4))
        self.validation_errors.extend(
            self.validate_string_length(
                file_name, min_length=2))

        if self.validation_errors:
            for validation_error in self.validation_errors:
                print(validation_error)
        # /To be refactored


    def _add_yield_curve(self, yield_curve):
        """Add yield curve to dict.

        Take given yield curve turn it into simplified and add simplified 
        representation of yield curve to dict. Yield curve name is used 
        as a key.

        """

        simplified_yield_curve = self._get_simplified_yield_curve(yield_curve)
        self.yield_curves[simplified_yield_curve.name] = simplified_yield_curve


    def _collect_currencies(self):
        """Collect all relevant currencies."""

        self.currency_from = self.receive_leg.Currency()
        self.currency_to = self.pay_leg.Currency()
        self.currency_usd = acm.FCurrency["USD"]


    def _collect_data(self):
        """Get relevant data from Front Arena."""

        self._collect_legs()
        self._collect_currencies()
        self.fx_spot_ratio = self._get_fx_spot_ratio()
        self._collect_yield_curves()
        self._collect_valuation_data()


    def _collect_legs(self):
        """Get pay and receive legs."""

        if len(self.instrument.Legs()) == 2:
            for leg in self.instrument.Legs():
                if leg.PayLeg():
                    self.pay_leg = leg
                else:
                    self.receive_leg = leg
        else:
            print("Invalid count of legs.")


    def _collect_valuation_data(self):
        """Collect valuation data for the instrument."""

        cash_flows_receive = {}
        cash_flows_pay = {}
        keys = set()
        pay_leg_present_value_sum = 0
        pay_leg_projected_value_sum = 0
        receive_leg_present_value_sum = 0
        receive_leg_projected_value_sum = 0

        for cash_flow_receive in self.receive_leg.CashFlows():
            point = self._get_valuation_cash_flow_point(cash_flow_receive, 
                self.receive_leg_yield_curve,  self.receive_leg.Currency())
            cash_flows_receive[(point.pay_date, point.cashflow_type)] = point
            receive_leg_present_value_sum += point.present_value
            receive_leg_projected_value_sum += point.projected_value

        for cash_flow_pay in self.pay_leg.CashFlows():
            point = self._get_valuation_cash_flow_point(cash_flow_pay, 
                self.pay_leg_yield_curve, self.pay_leg.Currency())
            cash_flows_pay[(point.pay_date, point.cashflow_type)] = point
            pay_leg_present_value_sum += point.present_value
            pay_leg_projected_value_sum += point.projected_value

        keys = set(cash_flows_receive.keys() + cash_flows_pay.keys())

        for (date, cashflow_type) in keys:
            days = acm.Time.DateDifference(date, self.date)
            point_pay = self._get_cash_flow_point(
                cash_flows_pay, date, cashflow_type)
            point_receive = self._get_cash_flow_point(
                cash_flows_receive, date, cashflow_type)
            fx_rate = self._get_fx_spot_ratio_for_date(date)
            valuation_point = ValuationPoint(
                date=date, days=days,
                pay_data=point_pay, receive_data=point_receive,
                fx_rate=fx_rate, cashflow_type=cashflow_type)
            self.valuation.append(valuation_point)

        self.valuation.sort(key=lambda x: (x.date, x.cashflow_type))
        self.pay_leg_sumary = CashFlowLegSumary(
            pay_leg_present_value_sum, pay_leg_projected_value_sum)
        self.receive_leg_sumary = CashFlowLegSumary(
            receive_leg_present_value_sum, receive_leg_projected_value_sum)


    def _collect_yield_curves(self):
        """Collect all relevant Yield curves from both legs."""

        self.pay_leg_yield_curve = self.pay_leg.MappedDiscountLink().Link()

        self.receive_leg_yield_curve = (
            self.receive_leg.MappedDiscountLink().Link())

        self._walk_yield_curve_hierarchy(self.pay_leg_yield_curve)
        self._walk_yield_curve_hierarchy(self.receive_leg_yield_curve)


    def _get_cash_flow_point(self, cash_flows, date, cashflow_type):
        """Finds cash flow point in cash flows."""

        return cash_flows[(date, cashflow_type)]


    def _get_fx_spot_ratio(self):
        """Calculate FX ratio of pay and receive leg currencies."""

        return self._get_fx_spot_ratio_for_date(self.date)


    def _get_fx_spot_ratio_for_date(self, date):
        """Calculate FX ratio for pay and receive leg currencies for date."""

        if self.currency_from.Name() == "USD":
            fx_spot_ratio = 1
        else:
            fx_spot_ratio = self.currency_from.UsedPrice(
                date, "USD", "SPOT"
            )

        fx_spot_ratio *= self.currency_usd.UsedPrice(
            date, self.currency_to.Name(), "SPOT"
        )

        return fx_spot_ratio


    def _get_simplified_yield_curve(self, yield_curve):
        """Returns simplified yield curve derived from given yield_curve."""

        yield_curve_points = self._get_simplified_yield_curve_points(yield_curve)
        yield_curve_points.sort(key=lambda x: x.date)

        simplified_yield_curve = SimplifiedYieldCurve(
            name=yield_curve.Name(), 
            yield_curve_type=str(type(yield_curve).__name__),
            points=yield_curve_points)

        return simplified_yield_curve


    def _get_simplified_yield_curve_points(self, yield_curve):
        """Returns simplified points for given yield_curve."""

        points = []

        if yield_curve.IsKindOf(acm.FAttributeSpreadCurve):
            for attribute in yield_curve.Attributes():
                for spread in attribute.Spreads():
                    point = SimplifiedYieldCurvePoint(
                        date=spread.Point().PointDate(),
                        period=spread.Point().DatePeriod(),
                        value=spread.Spread()
                    )
                    points.append(point)
        elif yield_curve.IsKindOf(acm.FBenchmarkCurve):
            for yield_point in yield_curve.Points():
                point = SimplifiedYieldCurvePoint(
                    date=yield_point.ActualDate(),
                    period=yield_point.DatePeriod(),
                    value=yield_point.PointValue()
                )
                points.append(point)

        return points


    def _get_valuation_cash_flow_point(self, cash_flow, yield_curve, currency):
        """Put valuation point into ValuationPointCashFlowDetail object."""

        nominal = cash_flow.Calculation().Nominal(
            self.calculation_space, None).Number()

        pay_date = cash_flow.PayDate()
        rate = cash_flow.FixedRate()

        present_value = cash_flow.Calculation().PresentValue(
            self.calculation_space, None).Number()

        projected_value = cash_flow.Calculation().Projected(
            self.calculation_space, None).Number()

        forward_rate = cash_flow.Calculation().ForwardRate(
            self.calculation_space)

        cashflow_type = cash_flow.CashFlowType()

        yc_attribute = yield_curve.YieldCurveComponent().Curve().YCAttribute(
            currency, currency)

        curr_swap = yc_attribute.IrCurveInformation(
            yield_curve.UnderlyingComponent().YieldCurveComponent().IrCurveInformation(self.date),
            self.date).Rate(self.date, pay_date)

        curr_basis = (
            yield_curve.UnderlyingComponent().YieldCurveComponent().IrCurveInformation().Rate(
                self.date, pay_date))

        if projected_value != 0:
            difference = present_value / projected_value
        else:
            difference = 0

        return ValuationPointCashFlowDetail(
            nominal=nominal, pay_date=pay_date, rate=rate,
            curr_swap=curr_swap, curr_basis=curr_basis,
            present_value=present_value, projected_value=projected_value, 
            forward_rate=forward_rate, cashflow_type=cashflow_type, difference=difference
        )


    def _generate_xml(self):
        """Put valuation report data into XML report."""

        # Format XML Strucuture of the report. Go from top to bottom.

        # Level 1 of the structure <Report>.

        xml_report = ElementTree.Element("Report")
        xml_report.set("Title", self.title)
        xml_report.set("Date", str(self.date))


        # Level 2 of the structure <General>

        xml_general = ElementTree.SubElement(xml_report, "General")
        xml_general.set("FXSpotRatio", str(self.fx_spot_ratio))
        xml_general.set("SumOfPVs", str(
            self.pay_leg_sumary.present_values_sum + (
                self.receive_leg_sumary.present_values_sum * self.fx_spot_ratio)))


        # Level 3 of the strucutre childrens of <General>. 

        xml_instrument = ElementTree.SubElement(xml_general, "Instrument")
        xml_instrument.set("InstrumentId", self.instrument.Name())
        xml_instrument.set("ContractSize", str(self.instrument.ContractSize()))

        xml_pay_leg = self._generate_xml_leg_summary(
            self.pay_leg, self.pay_leg_sumary, "PayLeg")
        xml_general.append(xml_pay_leg)
        
        xml_receive_leg = self._generate_xml_leg_summary(
            self.receive_leg, self.receive_leg_sumary, "ReceiveLeg")
        xml_general.append(xml_receive_leg)


        # Level 2 of the structure <Valuation>.

        xml_valuation = ElementTree.SubElement(xml_report, "Valuation")
        for valuation_point in self.valuation:
            xml_valuation_point = self._generate_xml_valuation_point(
                valuation_point)
            xml_valuation.append(xml_valuation_point)


        # Level 2 of the structure <YieldCurves>.

        xml_yield_curves = ElementTree.SubElement(
            xml_report, "YieldCurves")
        for key, simplified_yield_curve in self.yield_curves.iteritems():
            xml_yield_curve = self._generate_xml_yield_curve(simplified_yield_curve)
            xml_yield_curves.append(xml_yield_curve)

        # Turn XML structure into string.

        xml_report_as_str = (
            '<?xml version="1.0" encoding="utf-8"?>' +
            ElementTree.tostring(xml_report))

        return xml_report_as_str


    def _generate_xml_leg_summary(self, leg, cash_flow_leg_sumary, tag_name):
        """Generate leg summary data XML statement."""

        xml_leg = ElementTree.Element(tag_name)
        xml_leg.set("NominalFactor", str(leg.NominalFactor()))
        xml_leg.set("FixedRate", str(leg.FixedRate()))
        xml_leg.set("Currency", leg.Currency().Name())
        xml_leg.set("DayCountMethod", leg.Currency().Legs()[0].DayCountMethod())
        xml_leg.set(
            "NominalAmount", 
            str(leg.NominalFactor() *
            self.instrument.ContractSize())
        )
        xml_leg.set("PresentValuesSum", str(
            cash_flow_leg_sumary.present_values_sum))
        xml_leg.set("ProjectedValuesSum", str(
            cash_flow_leg_sumary.projected_values_sum))

        return xml_leg


    def _generate_xml_valuation_point(self, valuation_point):
        """Generate valuation point XML statement."""
        xml_valuation_point = ElementTree.Element("Point")
        xml_valuation_point.set("PayDate", valuation_point.date)
        xml_valuation_point.set("Days", str(valuation_point.days))

        xml_valuation_point.append(self._generate_xml_valuation_point_values(
            "PayData", valuation_point.pay_data))

        xml_valuation_point.append(self._generate_xml_valuation_point_values(
            "ReceiveData", valuation_point.receive_data))

        xml_valuation_point.set("FXRate", str(valuation_point.fx_rate))

        return xml_valuation_point


    def _generate_xml_valuation_point_values(self, tag_name, cash_flow_detail):
        """Generate valuation point cash flow XML statement."""

        xml_values = ElementTree.Element(tag_name)
        if cash_flow_detail:

            xml_values.set("CurrSwap",
                str(cash_flow_detail.curr_swap))

            xml_values.set("CurrBasis",
                str(cash_flow_detail.curr_basis))

            xml_values.set("Nominal",
                str(cash_flow_detail.nominal))

            xml_values.set("PresentValue",
                str(cash_flow_detail.present_value))

            xml_values.set("ProjectedValue",
                str(cash_flow_detail.projected_value))

            xml_values.set("ForwardRate",
                str(cash_flow_detail.forward_rate))

            xml_values.set("Difference",
                str(cash_flow_detail.difference))

        return xml_values


    def _generate_xml_yield_curve(self, simplified_yield_curve):
        """Generate Yield curve XML statement."""

        xml_yield_curve = ElementTree.Element("YieldCurve")
        xml_yield_curve.set("Name", simplified_yield_curve.name)
        xml_yield_curve.set("Type", simplified_yield_curve.yield_curve_type)

        for point in simplified_yield_curve.points:
            xml_point = ElementTree.Element("Point")
            xml_point.set("Date", point.date)
            xml_point.set("Period", point.period)
            xml_point.set("Value", str(point.value))
            xml_point.set("ValueRounded", str(round(point.value, 4)))
            xml_yield_curve.append(xml_point)

        return xml_yield_curve


    def _walk_yield_curve(self, yield_curve):
        """Loop through yield curve hierarchy."""

        if yield_curve.IsKindOf(acm.FYieldCurveHierarchy):
            self._walk_yield_curve_hierarchy(yield_curve)
        else:
            self._add_yield_curve(yield_curve)


    def _walk_yield_curve_hierarchy(self, yield_curve):
        """Loop through yield curve hierarchy."""

        self._walk_yield_curve(yield_curve.YieldCurveComponent().Curve())
        self._walk_yield_curve(
            yield_curve.UnderlyingComponent().YieldCurveComponent())


SimplifiedYieldCurve = collections.namedtuple(
    'SimplifiedYieldCurve', ['name', 'yield_curve_type', 'points'])


SimplifiedYieldCurvePoint = collections.namedtuple(
    'SimplifiedYieldCurvePoint', ['date', 'period', 'value'])


ValuationPoint = collections.namedtuple('ValuationPoint',
    ['date', 'days', 'pay_data', 'receive_data', 'fx_rate', 'cashflow_type'])


ValuationPointCashFlowDetail = collections.namedtuple(
    'ValuationPointCashFlowDetail', 
    ['nominal', 'pay_date', 'rate', 'curr_swap', 'curr_basis', 'present_value',
    'projected_value', 'forward_rate', 'cashflow_type', 'difference'])


CashFlowLegSumary = collections.namedtuple(
    'CashFlowLegSumary', ['present_values_sum', 'projected_values_sum'])



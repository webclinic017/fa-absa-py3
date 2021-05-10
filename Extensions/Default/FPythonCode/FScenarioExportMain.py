""" Compiled: 2020-09-18 10:38:54 """

#__src_file__ = "extensions/risk_export/./etc/FScenarioExportMain.py"
import acm
import FLogger


from FScenarioExportContentManager import ContentError


logger = FLogger.FLogger.GetLogger('FAReporting')


HEADER_VERSION_TAG = 'version'
HEADER_VERSION_DEFAULT_VALUE = 'v02'
HEADER_SEPARATOR_TAG = 'separator'
HEADER_MEASURE_GROUP_TAG = 'measure_group'
HEADER_DIMENSION_DEFAULTS_TAG = 'dimension_defaults'
HEADER_DIMENSION_DEFAULTS_DEFAULT_VALUE = ''
HEADER_DEFAULT_VALUES_TAG = 'default_values'
HEADER_COLUMN_GROUPING_TAG = 'column_grouping'


NEWLINE = "\n"
HORIZON_TOKEN = "Horizon"
HORIZON_ORDER_TOKEN = "Horizon Order"
PL_SOURCE_TOKEN = "PL Source"
VAR_TYPE_TOKEN = "VaR Type"
CURVE_DATE_TOKEN = "Curve Date"
MONEYNESS_TOKEN = "Moneyness"
SCENARIO_TOKEN = "Scenario"
SCENARIO_DATE_TOKEN = "Scenario Date"
SCENARIO_COUNT_TOKEN = "Scenario Count"
STRESS_TYPE_TOKEN = "Stress Type"


def static_header_info(horizon, horizon_order, var_type=None,
    pl_source=None, curve_date=None, moneyness=None,
    scenario=None, stress_type=None):
    labels = [HORIZON_TOKEN, horizon, HORIZON_ORDER_TOKEN, str(horizon_order)]

    if pl_source:
        labels.extend([PL_SOURCE_TOKEN, pl_source])
    if var_type:
        labels.extend([VAR_TYPE_TOKEN, var_type])
    # The following parts of the header are added for the upgrade to 13.2
    if curve_date:
        labels.extend([CURVE_DATE_TOKEN, curve_date])
    if moneyness:
        labels.extend([MONEYNESS_TOKEN, moneyness])
    if scenario:
        labels.extend([SCENARIO_TOKEN, scenario])
    if stress_type:
        labels.extend([STRESS_TYPE_TOKEN, stress_type])
    return labels


def extract_info_from_content_managers(*content_managers):
    all_measure_groups_values = []
    all_dimension_defaults_values = []
    all_column_grouping_values = []
    for cmanager in content_managers:
        if not cmanager:
            continue

        measure_group_vals = cmanager.measure_group_header()
        dimension_default_vals = cmanager.dimension_defaults_header()
        column_grouping_vals = cmanager.column_grouping_header()

        if measure_group_vals:
            all_measure_groups_values.extend(measure_group_vals)
        if dimension_default_vals:
            all_dimension_defaults_values.extend(dimension_default_vals)
        if column_grouping_vals:
            all_column_grouping_values.extend(column_grouping_vals)
    return (all_dimension_defaults_values, all_measure_groups_values,
            all_column_grouping_values)


def produce_report_header_using_content_managers(delimiter, scen_delimiter,
        ostream, horizon, horizon_order, var_type, pl_source, curve_date,
        moneyness, scenario, stress_type, *content_managers):
    (dimension_defaults_values, measure_groups_values, column_grouping_values)\
 = extract_info_from_content_managers(*content_managers)
    dimension_defaults = delimiter.join(dimension_defaults_values)
    column_grouping = delimiter.join(column_grouping_values)
    measure_groups = delimiter.join(measure_groups_values)

    produce_report_header(delimiter, scen_delimiter, ostream, horizon,
        horizon_order, var_type, pl_source, curve_date, moneyness, scenario,
        stress_type, measure_groups, column_grouping, dimension_defaults)


def produce_report_header(delimiter, scen_delimiter, ostream,
    horizon, horizon_order, var_type, pl_source,
    curve_date, moneyness, scenario, stress_type, measure_groups,
    column_group_headers, dimension_defaults_header):
    """ Note that the "column header" row is not part of the header! """

    template_data = {}

    template_data[HEADER_SEPARATOR_TAG] = "".join([delimiter, scen_delimiter])

    template_data[HEADER_MEASURE_GROUP_TAG] = measure_groups

    static_header_values = static_header_info(horizon, horizon_order,
        var_type, pl_source, curve_date, moneyness, scenario, stress_type)

    template_data[HEADER_DEFAULT_VALUES_TAG] = \
        delimiter.join(static_header_values)

    template_data[HEADER_COLUMN_GROUPING_TAG] = column_group_headers

    template_data[HEADER_DIMENSION_DEFAULTS_TAG] = dimension_defaults_header

    headers = generate_header_from_template(template_data)
    ostream.Write(headers)
    return


def get_existing_value_or_default(dct, key, default=None):
    try:
        return dct[key]
    except KeyError:
        if default is not None:
            return default
        else:
            raise Exception('Unable to determine the value for %s' % key)


def generate_header_from_template(data):

    result = []

    result.append(get_existing_value_or_default(data, HEADER_VERSION_TAG,
        HEADER_VERSION_DEFAULT_VALUE))
    result.append(NEWLINE)

    result.append(get_existing_value_or_default(data, HEADER_SEPARATOR_TAG))
    result.append(NEWLINE)

    result.append(get_existing_value_or_default(data,
        HEADER_MEASURE_GROUP_TAG))
    result.append(NEWLINE)

    result.append(get_existing_value_or_default(data,
        HEADER_DIMENSION_DEFAULTS_TAG,
        HEADER_DIMENSION_DEFAULTS_DEFAULT_VALUE))
    result.append(NEWLINE)

    result.append(get_existing_value_or_default(data,
        HEADER_DEFAULT_VALUES_TAG))
    result.append(NEWLINE)

    result.append(get_existing_value_or_default(data,
        HEADER_COLUMN_GROUPING_TAG))
    result.append(NEWLINE)

    return result


def produce_scenario_count_report(delimiter, scen_delimiter, horizon,
        horizon_order, var_type, ostream, pv_scenario_content):

    measure_groups = delimiter.join([SCENARIO_COUNT_TOKEN, str(1)])
    column_grouping = None
    pl_source = None
    dimension_defaults = None
    produce_report_header(delimiter, scen_delimiter, ostream, horizon,
            horizon_order, var_type, pl_source, None, None, None, None,
            measure_groups, column_grouping, dimension_defaults)

    ostream.Write(SCENARIO_COUNT_TOKEN)
    ostream.Write(NEWLINE)
    ostream.Write(pv_scenario_content.get_scenario_count())
    ostream.Write(NEWLINE)

    return


def process_content_managers(content_managers, trdnbr, space_collection):
    """
    Broken out as a function to avoid nested for-loops and difficulties
    'continuing' the outer one in case of exceptions.
    """
    for cmanager in content_managers:
        if not cmanager:
            continue
        cmanager.add_output(
            cmanager.get_content(trdnbr, space_collection))


def produce_report(trades, delimiter, ostreams, *content_managers):
    for cmanager in content_managers:
        if not cmanager:
            continue
        cmanager.add_output(cmanager.column_headers())
    first = True
    for cmanager in content_managers:
        if not cmanager:
            continue
        cmanager.flush_output(delimiter, first)
        first = False
    for ostream in ostreams:
        ostream.Write(NEWLINE)

    space_collection = acm.Calculations().\
        CreateStandardCalculationsSpaceCollection()

    for trdnbr in trades:
        try:
            process_content_managers(content_managers, trdnbr,
                space_collection)
        except ContentError as msg:
            err_msg = "Could not process trade %s: %s" % (trdnbr, msg)
            logger.ELOG(err_msg)
            for cmanager in content_managers:
                if cmanager:
                    cmanager.clear_output()
            continue
        first = True
        for cmanager in content_managers:
            if not cmanager:
                continue
            cmanager.flush_output(delimiter, first)
            first = False
        for ostream in ostreams:
            ostream.Write(NEWLINE)
    space_collection.Clear()

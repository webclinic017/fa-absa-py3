import acm
from at_logging import getLogger
from at_ael_variables import AelVariableHandler

LOGGER = getLogger(__name__)
ael_variables = AelVariableHandler()

INTERVAL_VALUE = 0

ael_variables.add("Benchmark_Curve",
                  label="Benchmark Curve",
                  cls=acm.FStoredASQLQuery,
                  default ='Benchmark_Curve_',
                  collection=acm.FStoredASQLQuery.Select("subType='FYieldCurve'"))


def change_updateinterval(benchmark_curve, interval_value):
    """Updates he updateinterval of the curve"""
    yc_clone = benchmark_curve.Clone()
    yc_clone.UpdateInterval(interval_value)
    benchmark_curve.Apply(yc_clone)
    try:
        benchmark_curve.Commit()
        LOGGER.info("Successfully updated curve: %s", benchmark_curve.Name())
    except Exception as exc:
        LOGGER.exception("Error while committing the changes on the curve: %s", exc)

def ael_main(ael_dict):
    benchmark_curve = ael_dict["Benchmark_Curve"].Query().Select()
    for curve in benchmark_curve:
        change_updateinterval(curve, INTERVAL_VALUE)




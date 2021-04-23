""" Compiled: 2020-09-18 10:38:52 """

#__src_file__ = "extensions/frtb/./etc/FRTBCommon.py"
from __future__ import print_function
import collections
import inspect

import acm

import FRTBUtility
import importlib

IS_OPTION_COLUMN_ID = 'FRTB Is Option'
SA_SBA_COLUMN_ID = 'FRTB Measure'
SA_DRC_SCALING_COLUMN_ID = 'FRTB DRC JTD Scaling'
SA_DRC_MATURITY_COLUMN_ID = 'FRTB DRC Remaining Maturity'
SA_DRC_IS_LONG_EXPOSURE_COLUMN_ID = 'FRTB DRC Is Long Exposure'
SA_DRC_MARKET_VALUE_COLUMN_ID = 'FRTB DRC Bond Equivalent Market Value'
SA_DRC_NOTIONAL_COLUMN_ID = 'FRTB DRC Bond Equivalent Notional'
SA_RRAO_NOTIONAL_COLUMN_ID = 'FRTB Residual Risk Notional'
SA_RRAO_TYPE_COLUMN_ID = 'FRTB Residual Risk Type'
IMA_ES_BASE_VALUE_COLUMN_ID = 'Expected Shortfall Base Value'
IMA_DRC_LIQUIDITY_HORIZON = 'FRTB DRC Liquidity Horizon'
IMA_ES_COLUMN_ID = (
    'Portfolio Theoretical Total Profit and Loss in Accounting Currency'
)
IMA_PL_BASE_VALUE_COLUMN_ID = 'Hypothetical P&L Base Value'
IMA_PL_HYPOTHETICAL_COLUMN_ID = (
    'Portfolio Hypothetical Total Profit and Loss in Accounting Currency'
)
IMA_PL_RISK_COLUMN_ID = (
    'Portfolio Risk Total Profit and Loss in Accounting Currency'
)
IMA_SES_COLUMN_ID = 'FRTB Stressed Capital Add-On Per Risk Factor'
IMA_DRC_CURRENT_VALUE_COLUMN_ID = 'Portfolio Theoretical Value'
IMA_DRC_VALUE_DEFAULT_COLUMN_ID = 'FRTB IMA Value After Default'
IMA_PL_ACTUAL_COLUMN_ID = 'Portfolio Total Profit and Loss'
SA_PL_ACTUAL_COLUMN_ID = 'Portfolio Total Profit and Loss'
ACCOUNTING_CURRENCY_CALENDAR = acm.GetFunction(
    'mappedValuationParameters', 0
)().Parameter().AccountingCurrency().Calendar()


DEFAULT_DAYS = (
    acm.Time.DateToday(),
    'Today',
    'First of Month',
    'First of Quarter',
    'First of Year',
    'Previous Banking Day',
    '0d',
    '-1d'
)
class CalculationGroup(object):
    """
    Class representing the available FRTB calculations, identified by the
    combination of group name, calculation class and calculation name.
    """
    class CalculationType(object):
        def __init__(
            self, group_short, class_short, class_long, name_short, name_long
        ):
            self.group_short = group_short
            self.class_short = class_short
            self.class_long = class_long
            self.name_short = name_short
            self.name_long = name_long

        def getAttribute(self, name):
            name = name.lower()
            if name.startswith('calc_'):
                name = name.replace('calc_', '')
                if not name.endswith('_long'):
                    name += '_short'

                return getattr(self, name, None)

            return None

    def __init__(self):
        self._types = collections.OrderedDict()
        self._last_keys = None

    def empty(self):
        return len(self._types) == 0

    def addType(
        self, group_short, class_short, class_long,
        name_short=None, name_long=None
    ):
        self.addTypeForExtension(
            group_short=group_short,
            class_short=class_short,
            class_long=class_long
        )
        self.extendLast(
            name_short=name_short, name_long=name_long, case_sensitive=False
        )
        return

    def addTypeForExtension(self, group_short, class_short, class_long):
        group_short = group_short.upper()
        class_short = class_short.upper()
        class_long = class_long.title()
        group = self._types.setdefault(
            group_short, collections.OrderedDict()
        )
        class_key = (class_short, class_long)
        group.setdefault(class_key, collections.OrderedDict())
        self._last_keys = (group_short, class_key)
        return

    def extendLast(self, name_short, name_long, case_sensitive=True):
        group_short = self._last_keys[0]
        class_short = self._last_keys[1][0]
        class_long = self._last_keys[1][1]
        types = self._types[group_short][self._last_keys[1]]
        type_key = [class_short, class_long]
        if name_short:
            type_key[0] += name_short if case_sensitive else name_short.upper()

        if name_long:
            type_key[1] += ' ' + name_long if case_sensitive else name_long.upper()

        type_key = tuple(type_key)
        if type_key not in types:
            types[type_key] = self.CalculationType(
                group_short=group_short,
                class_short=class_short,
                class_long=class_long,
                name_short=type_key[0],
                name_long=type_key[1]
            )

        return

    def get(self, name):
        group = self._types[name.upper()]
        calc_types = []
        for types in group.values():
            calc_types.extend(types.values())

        return calc_types

_CALCULATION_GROUPS = CalculationGroup()
def _initCalculationGroups():
    # Available FRTB calculations (order dependent<group: <class: calc>>)
    if not _CALCULATION_GROUPS.empty():
        return

    _CALCULATION_GROUPS.addType('sa', 'sba', 'Sensitivity Based Approach')
    _CALCULATION_GROUPS.addType('sa', 'drc', 'default risk charge')
    _CALCULATION_GROUPS.addType('sa', 'rrao', 'residual risk add-on')
    _CALCULATION_GROUPS.addTypeForExtension('ima', 'es', 'expected shortfall')
    _CALCULATION_GROUPS.extendLast('FC', 'Full-Current')
    _CALCULATION_GROUPS.extendLast('RC', 'Reduced-Current')
    _CALCULATION_GROUPS.extendLast('RS', 'Reduced-Stressed')
    _CALCULATION_GROUPS.addTypeForExtension('ima', 'pl', 'Profit and Loss Attribution')
    _CALCULATION_GROUPS.extendLast('Hyp', 'Hypothetical')
    _CALCULATION_GROUPS.extendLast('Act', 'Actual')
    _CALCULATION_GROUPS.extendLast('Risk', 'Risk-Theoretical')
    _CALCULATION_GROUPS.addTypeForExtension('sa', 'pl', 'Profit and Loss Attribution')
    _CALCULATION_GROUPS.extendLast('Act', 'Actual')
    _CALCULATION_GROUPS.addType('ima', 'ses', 'stressed capital add-on')
    _CALCULATION_GROUPS.addType('ima', 'drc', 'default risk charge')
    return

def getExporters(group_name):
    try:
        return _getExporters(group_name=group_name)
    except Exception as e:
        print('Failed to initialise FRTB %s exporters: %s' % (
            group_name, e
        ))
        raise

    return

def aelMain(parameters, exporters):
    import FRTBExportPerform
    importlib.reload(FRTBExportPerform)

    FRTBExportPerform.perform(
        name=FRTBUtility.getCaller().__name__,
        parameters=parameters,
        exporters=exporters
    )
    return

def _getExporters(group_name):
    """
    Using the short names given in the _CALCULATION_GROUPS spec,
    this function imports modules matching the expected name:
        FRTB<group_name><calc_class>Export
    Then for every calculation type, this function populates the
    caller module's tuples of exporter classes matching the expected names:
        <calc_name>Export
    In these classes he long and short calculation class
    names, calculation names and column ids are automatically set.

    Hence, what is required of any new exporter is:
        Create export with the expected name signature.
        Exporter must specify it's results collector and all related writers.
    """
    import FRTBBaseWriter
    importlib.reload(FRTBBaseWriter)
    import FRTBExport
    importlib.reload(FRTBExport)

    _initCalculationGroups()
    group_name = group_name.upper()
    calc_types = _CALCULATION_GROUPS.get(name=group_name)
    FRTBBaseWriter.Writer.resetCache(group=group_name)
    exporters = []
    known = {}
    for ct in calc_types:
        mod_name = 'FRTB%s%sExport' % (ct.group_short, ct.class_short)
        em = known.get(mod_name)
        if not em:
            em = known[mod_name] = __import__(mod_name)
            importlib.reload(em)

        exporter = getattr(em, ct.name_short + 'Export')
        exporters.append(exporter)
        results_collector = exporter.RESULTS_COLLECTOR_CLASS
        if hasattr(results_collector, 'resetCache'):
            results_collector.resetCache()

        writer_classes = []
        for cls in exporter.WRITER_CLASSES:
            if cls.__name__ not in known:
                writer_classes.append(cls)
                known[cls.__name__] = True
                if not cls.COLUMN_IDS:
                    cls.COLUMN_IDS = results_collector.COLUMN_IDS

                if cls.CALC_NAME and not cls.CALC_NAME_LONG:
                    cls.CALC_NAME_LONG = ct.getAttribute(name='CALC_NAME_LONG')
                    cls.CALC_NAME_LONG += ' ' + cls.CALC_NAME

        for name, _ in inspect.getmembers(exporter):
            val = ct.getAttribute(name=name)
            if val:
                for cls in writer_classes + [exporter]:
                    if not getattr(cls, name, None):
                        setattr(cls, name, val)

        for cls in exporter.WRITER_CLASSES:
            if not cls.OUTPUT_SUB_DIR:
                cls.OUTPUT_SUB_DIR = cls.CALC_CLASS

    return tuple(e() for e in exporters)

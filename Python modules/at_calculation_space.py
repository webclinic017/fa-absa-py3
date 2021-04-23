import operator

import acm
from at_functools import curried
from functools import reduce


class CalculationSpaceException(Exception):
    """General Exception for Calculation Space dictionary."""


class CalculationSpace(dict):
    """Class accessing virtual Trading Manager."""

    def __init__(self, calc_space, node):
        """Fill the internal dictionary with data from Trading Manager view."""
        super(CalculationSpace, self).__init__()
        self.calc_space = calc_space
        self.node = node

        child = self.node.Clone().FirstChild()
        while child:
            key = child.Tree().Item().StringKey()
            self[key] = CalculationSpace(self.calc_space, child)
            child = child.Clone().NextSibling()

    @classmethod
    def from_source(cls, source, sheet_type='FPortfolioSheet', grouper=None,
            context=acm.GetDefaultContext()):
        # Create underlying calculation space
        calc_space = acm.Calculations().CreateCalculationSpace(
            context, sheet_type)

        # Apply grouper (if necessary)
        top_node = calc_space.InsertItem(source)
        if grouper:
            top_node.ApplyGrouper(grouper)

        # Refresh the calculation space to apply the amendments
        calc_space.Refresh()

        # Top node of the Trading Manager view
        node = top_node.Iterator()
        return cls(calc_space, node)

    def simulate_value(self, column_id, value):
        """Simulate value on the source."""
        self.calc_space.SimulateGlobalValue(column_id, value)

    def column_value(self, column_id, calc_config=None):
        """Get column value from calculation space."""
        return self.calc_space.CreateCalculation(
            self.node.Tree(), column_id, calc_config)

    def retrieve(self, sequence):
        """
        Retreive item located at the specified sequence of keys.
        
        Can be used on sequences coming from the 'traverse' method.

        """
        return reduce(operator.getitem, sequence, self)


def calculate_value(sheet_name, item, column_name, formatted=False, simulated={}, vector=[], vector_currs=[]):
    """Calculate value for the given sheet, item and column_name.

    :param sheet_name: name of the sheet class, i.e. ``FTradeSheet``
    :type sheet_name: string
    :param item: ACM entity to be used for calculation
    :type item: subclass of ``FPersistent``, i.e. ``FTrade``
    :param column_name: name of the column
    :type column_name: string
    :param formatted: return the formatted value or the raw value
    :type formatted: bool
    :param simulated: a dict with the names of columns as keys
    :type simulated: dict
    :param vector: a vector of column parameters
    :type vector: list of tuples, e.g. [('currency', acm.FCurrency['ZAR']), ('currency', 'acm.FCurrency['USD'])]
    :param vector_currs: a shortcut for vector of currencies (see above)
    :type vector_currs: list of currency names, e.g. ['USD', 'ZAR']
    """
    if '.' in column_name:
        return _call_property(column_name, item, formatted)

    if not sheet_name in calculate_value._calc_space_cache:
        calculate_value._calc_space_cache[sheet_name] = acm.FCalculationSpace(sheet_name)

    cspace = calculate_value._calc_space_cache[sheet_name]

    if simulated:
        for (column_id, value) in simulated.items():
            cspace.SimulateValue(item, column_id, value)

    result = None
    
    if vector_currs:
        vector = [('currency', acm.FCurrency[val]) for val in vector_currs]
        
    if vector:
        conf_vector = acm.FArray()
        for vec_key, vec_value in vector:
            param = acm.FNamedParameters();
            param.AddParameter(vec_key, vec_value)
            conf_vector.Add(param)
            
        calc_config = acm.Sheet.Column().ConfigurationFromVector(conf_vector)
        calc = cspace.CreateCalculation(item, column_name, calc_config)
        if formatted: 
            result = calc.FormattedValue()
        else:
            result = calc.Value()
    else:
        if formatted:
            result = cspace.CreateCalculation(item, column_name).FormattedValue()
        else:
            result = cspace.CalculateValue(item, column_name)

    if simulated:
        for (column_id, value) in simulated.items():
            cspace.RemoveSimulation(item, column_id)
    
    if not vector:
        cspace.Clear() # for some reason this throws an exception for vector columns
    return result

calculate_value._calc_space_cache = {}

def _call_property(column_name, item, formatted):
    """Translate column_name to chained method call.

    ``Instrument.Currency`` => ``item.Instrument().Currency()``

    """
    method_chain = column_name.split('.')
    for method_name in method_chain:
        if item == None: return None
        item = getattr(item, method_name)()

    if formatted and hasattr(item, 'Name'):
        return str(item.Name())

    return item


"""Prepare calculation space for column values' retrieval.

This function supports currying, see usage:

prepare_row = prepare_calc_space('FTradeSheet')
for t in trades:
    get_column = prepare_row(t)
    values = [get_column('Pre-Trade Analysis MI Permanent Price Impact Absolute Customer Currency'),
              get_column('Total Val End'),
              get_column('Instrument.InsType'),
              ...]

For params see ``at_calculation_space.calculate_value``.
"""
prepare_calc_space = curried(calculate_value)


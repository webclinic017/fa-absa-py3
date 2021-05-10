"""
:Author: Andreas Bayer <Andreas.Bayer@absa.africa;
:Version: 1.0, 2020-05-08
:Summary: utilities script for extracting the calculation report for bond index valuation
"""

from BondIndex import calculation_report as nominal_bond_report
from CPIBondIndex import calculation_report as cpi_bond_report
import acm
from at_type_helpers import to_ael

from at_ael_variables import AelVariableHandler

ael_variables = AelVariableHandler()

ael_variables.add(
    'bond_index', 
    label = 'Bond Index', 
    cls = acm.FCombination, 
    collection = acm.FCombination.Select(''), 
    default = 'ZAR/ALBI_Weights',
)

def ael_main(ael_dict):
    """Report only works for select instrumets
    :param bond_index: name of an jse bond index instrument
    :type bond_index: FCombination
    :return: None, calculation report is printed into console
    :rtype: None, calculation report is a string printed into console
    """
    if ael_dict['bond_index'].Name() in ('ZAR/ALBI_TEST', 'ZAR/GOVI_TEST', 'ZAR/ALBI_Weights', 'ZAR/GOVI_Weights'):
        nominal_bond_report(to_ael(ael_dict['bond_index']), 'No')
    elif ael_dict['bond_index'].Name() in ('ZAR/IGOV_Weights'):
        cpi_bond_report(to_ael(ael_dict['bond_index']), 'No')

"""--------------------------------------------------------------------------------------------------------------------------------------
MODULE
    NeoXActivityReportParameters

DESCRIPTION
    This module contains parameters used to configure Neox Activity Reports functionality within Front Arena.

-----------------------------------------------------------------------------------------------------------------------------------------
HISTORY
=========================================================================================================================================
Date            Change no       Developer               Requester               Description
-----------------------------------------------------------------------------------------------------------------------------------------
2020-10-21      FAOPS-959       Ncediso Nkabmule        Cuen Edwards            Initial implementation.
2021-03-16      FAOPS-982       Ncediso Nkambule        Gasant Thulsie          Added functions to handle Cashflow driven events.

-----------------------------------------------------------------------------------------------------------------------------------------
"""

import EnvironmentFunctions
from SBLCollateralActivityNeoxHook import SBLCollateralActivityHook as CollateralHook
from SBLSecurityLoanActivityNeoxHook import SBLSecurityLoansActivityNeoxHook as SecurityLoanHook
from SBLCashCollateralActivityNeoxHook import SBLCashCollateralActivityHook as CashCollateralHook


ambAddress = '{amb_host}:{amb_port}{amb_login}'.format(
    amb_host=EnvironmentFunctions.get_neox_activity_report_parameter('Host'),
    amb_port=EnvironmentFunctions.get_neox_activity_report_parameter('Port'),
    amb_login=EnvironmentFunctions.get_neox_activity_report_parameter('Login')
)

receiverMBName = EnvironmentFunctions.get_neox_activity_report_parameter('ReceiverName')

receiverSource = EnvironmentFunctions.get_neox_activity_report_parameter('ReceiverSource')

eventTables = [
    'INSTRUMENT',
    'SETTLEMENT',
    'TRADE'
]

reportHooks = [
    SecurityLoanHook(),
    CollateralHook(),
    CashCollateralHook()
]

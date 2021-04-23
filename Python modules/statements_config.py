"""-----------------------------------------------------------------------------
PURPOSE              :  Client Valuation Statements Automation
                        Main configuration defining active statement types and
                        its parameters.
DESK                 :  PCG Collateral
DEVELOPER            :  Libor Svoboda
--------------------------------------------------------------------------------

HISTORY
================================================================================
Date        Change no      Developer           Description
--------------------------------------------------------------------------------
2019-02-14  CHG1001362755  Libor Svoboda       Initial Implementation (FEC)
2019-03-14  CHG1001488095  Libor Svoboda       Enable Option statements
2019-04-12  CHG1001590405  Libor Svoboda       Enable Swap, Cap & Floor, and 
                                               Structured Deal statements
2020-06-03  CHG0103217     Libor Svoboda       Add SBL client statements
2020-10-20  CHG0132720     Libor Svoboda       Enable Deposit statements
"""
from statements_process import (FECStatementProcess, OptionStatementProcess, 
                                SwapStatementProcess, CapFloorStatementProcess,
                                StructuredStatementProcess,
                                SBLFeeStatementProcess, 
                                SBLMovementStatementProcess,
                                SBLOpenPosCollStatementProcess,
                                SBLOpenPosOpsStatementProcess,
                                SBLMarginCallStatementProcess,
                                SBLFinderFeeStatementProcess,
                                SBLDividendNotificationProcess,
                                DepositStatementProcess)
from statements_util import StatementConfig


STATEMENTS = {
    'FEC': 
        StatementConfig(FECStatementProcess, 'Valuation Statement', 'Curr', 
                        'Statements_FEC', 
                        additional_trade_query='Statements_FEC_MIDAS'),
    'Option': 
        StatementConfig(OptionStatementProcess, 'Valuation Statement', 
                        'Option', 'Statements_Option'),
    'Swap': 
        StatementConfig(SwapStatementProcess, 'Valuation Statement', 'Swap',
                        'Statements_Swap'),
    'Cap & Floor': 
        StatementConfig(CapFloorStatementProcess, 'Valuation Statement', 
                        'Cap', 'Statements_Cap_Floor'),
    'Structured Deal': 
        StatementConfig(StructuredStatementProcess, 'Valuation Statement', 
                        'Combination', 'Statements_Structured'),
    'Deposit': 
        StatementConfig(DepositStatementProcess, 'Valuation Statement', 
                        'Deposit', 'Statements_Deposit'),
    'SBL Fee': 
        StatementConfig(SBLFeeStatementProcess, 'SBL Fee Statement', 
                        'SecurityLoan', 'Statements_SBL_Fees', period='Month'),
    'SBL Finder Fee': 
        StatementConfig(SBLFinderFeeStatementProcess, 'SBL Finder Fee Statement', 
                        'SecurityLoan', 'Statements_SBL_Fees', period='Month'),
    'SBL Movement': 
        StatementConfig(SBLMovementStatementProcess, 'SBL Movement Statement', 
                        'SecurityLoan', 'Statements_SBL_Movement',
                        additional_trade_query='Statements_SBL_Collateral_incl_Terminated',
                        always_new_bp=True),
    'SBL Open Position Coll': 
        StatementConfig(SBLOpenPosCollStatementProcess, 'SBL Open Position Coll Statement', 
                        'SecurityLoan', 'Statements_SBL_Open_Position',
                        additional_trade_query='Statements_SBL_Collateral'),
    'SBL Open Position Ops': 
        StatementConfig(SBLOpenPosOpsStatementProcess, 'SBL Open Position Ops Statement', 
                        'SecurityLoan', 'Statements_SBL_Open_Position',
                        additional_trade_query='Statements_SBL_Collateral'),
    'SBL Margin Call': 
        StatementConfig(SBLMarginCallStatementProcess, 'SBL Margin Call Statement', 
                        'SecurityLoan', 'Statements_SBL_Margin_Call',
                        additional_trade_query='Statements_SBL_Collateral'),
    'SBL Dividend Notification': 
        StatementConfig(SBLDividendNotificationProcess, 'SBL Dividend Notification Statement', 
                        'SecurityLoan', 'Statements_SBL_Dividend_Notification'),
}


def get_bp_config(bp):
    for config in STATEMENTS.values():
        if config.matches(bp):
            return config
    return None

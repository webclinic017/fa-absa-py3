"""
onboarding directory: 'y:\Jhb\FAReports\AtlasEndOfDay\PrimeClients\SAXO\Onboarding\2017_JAN\'
"""

import acm



ONBOARD_UPLOAD_TRADES = [
    "PB_Saxo_upload_csv_TRADES_ONBOARDING_2017JAN",
    ]

ONBOARD_UPLOAD_PRICES = [
    "PB_Saxo_upload_csv_PRICES_CFD_ONBOARDING_2017JAN",
    "PB_Saxo_upload_csv_PRICES_ETO_ONBOARDING_2017JAN",
    "PB_Saxo_upload_csv_PRICES_FUT_ONBOARDING_2017JAN",
    "PB_Saxo_upload_csv_PRICES_FXO_ONBOARDING_2017JAN",
    "PB_Saxo_upload_csv_PRICES_STO_ONBOARDING_2017JAN",
    ]

ONBOARD_SWEEPING = [
    "PB_Saxo_sweeping_FTMOKA_CFD_ONBOARDING",
    "PB_Saxo_sweeping_MROC_ETO_ONBOARDING",
    "PB_Saxo_sweeping_NMRQL_CFD_ONBOARDING",
    "PB_Saxo_sweeping_NMRQL_FUT_ONBOARDING",
    "PB_Saxo_sweeping_NMRQL_FXO_ONBOARDING",
    "PB_Saxo_sweeping_NMRQL_FX_ONBOARDING",
    "PB_Saxo_sweeping_NMRQL_STO_ONBOARDING",
    "PB_Saxo_sweeping_SANMAC_FX_ONBOARDING",
    ]
    
RERUN_UPLOAD_TRADES = [
    "PB_Saxo_upload_csv_TRADES_RERUN_2017JAN",
    ]

RERUN_UPLOAD_PRICES = [
    "PB_Saxo_upload_csv_PRICES_CFD_RERUN_2017JAN",
    "PB_Saxo_upload_csv_PRICES_ETO_RERUN_2017JAN",
    "PB_Saxo_upload_csv_PRICES_FUT_RERUN_2017JAN",
    ]

RERUN_SWEEPING = [
    "PB_Saxo_sweeping_CORINOV_CFD_RERUN",
    "PB_Saxo_sweeping_CORINOV_ETO_RERUN",
    "PB_Saxo_sweeping_CORINOV_FUT_RERUN",
    "PB_Saxo_sweeping_MROC_FUT_RERUN",
    "PB_Saxo_sweeping_NOVFI3_FUT_RERUN",
    "PB_Saxo_sweeping_SANMAC_FUT_RERUN",    
    ]

TASKS_TRADES = RERUN_UPLOAD_TRADES + ONBOARD_UPLOAD_TRADES
TASKS_PRICES = RERUN_UPLOAD_PRICES + ONBOARD_UPLOAD_PRICES
TASKS_SWEEPING = RERUN_SWEEPING + ONBOARD_SWEEPING

TASKS = TASKS_TRADES + TASKS_PRICES + TASKS_SWEEPING
        

for task_name in TASKS:
    print("Executing task: '%s'" % task_name)
    task = acm.FAelTask[task_name]
    task.Execute()
    
    print("*" * 50)
    print("Completed successfully.")

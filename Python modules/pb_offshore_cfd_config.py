"""-----------------------------------------------------------------------------
Stores all configurable details for prime services offshore CFD processes.

HISTORY
================================================================================
Date           Developer          Description
--------------------------------------------------------------------------------
2020-11-20     Marcus Ambrose     Implemented
2021-02-24     Marcus Ambrose     Include portfolios
-----------------------------------------------------------------------------"""
EXECUTION_RATES = {
    "EUR": 0.0008,
    "CHF": 0.0008,
    "DKK": 0.0008,
    "GBP": 0.0008,
    "NOK": 0.0008,
    ("RUB", "USD"): 0.0008,
    "SEK": 0.0008,
    "JPY": 0.0008,
    "HKD": 0.0008,
    "AUD": 0.0008,
    "SGD": 0.0008,
    ("USD", "USD"): 0.0005,
    "CAD": 0.0005,
    ("NZD", "USD"): 0.0008,
}

# Add alias for specific client rate
CLIENT_ABSA_RATES = {"default": 2.0}

BROKER_ONBOARDING_CONFIG = {
    "SocGen": {
        "file_dir": r"Y:\Jhb\FAReports\AtlasEndOfDay\PrimeClients\SOCGEN\${DATE}",
        "funding_file": "Funding-cost",
        "synthetic_file": "Daily-Synthetic-MtM",
        "funding_sweeping_report": r"/services/frontnt/Task/${CLIENT}_FundingSweepingReport_SocGen_${RUN_DATE}.csv",
        "pnl_sweeping_report": r"/services/frontnt/Task/${CLIENT}_PnLSweepingReport_SocGen_${RUN_DATE}.csv",
    }
}

BROKER_PORTFOLIOS = {
    "SocGen": "PB_OFFSHORE",
}


def get_exchange_rates():
    return EXECUTION_RATES


def get_absa_rate(alias):
    if alias in CLIENT_ABSA_RATES:
        return CLIENT_ABSA_RATES[alias]
    return CLIENT_ABSA_RATES["default"]


def get_broker_onboarding_config(broker):
    if broker in BROKER_ONBOARDING_CONFIG:
        return BROKER_ONBOARDING_CONFIG[broker]
    raise ValueError("No configuration found for {} on boarding".format(broker))

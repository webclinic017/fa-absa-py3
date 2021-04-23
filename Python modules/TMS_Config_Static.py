''' =======================================================================
    TMS Config Static

    This module contains static mappings for use by all other modules in
    the TMS project.

    Eben Mare
    ======================================================================= '''

CALENDAR_MAPPING = {
    "AED - UAE Dirham": "[NYB]",
    "AUD Sydney": "[SYB]",
    "BRL Brasilia": "[BRZ]",
    "BWP Gaborone": "[GAB]",
    "CAD Toronto": "[TRB]",
    "CHF Zurich": "[ZUB]",
    "CZK Prague": "[CZB]",
    "DKK Copenhagen": "[COB]",
    "EGP Cairo": "[CRO]",
    "EUR Euro": "[TGT]",
    "GBP London": "[LNB]",
    "GHC Accra": "[JOB]",
    "HKD Hong Kong": "[HKB]",
    "HUF Budapest": "[BDB]",
    "ILS - Israel": "[TAB]",
    "INR New Delhi": "[BMB]",
    "JPY Tokyo": "[LTO]",
    "KES Nairobi": "[JOB]",
    "KWD Kuwait City": "[KUB]",
    "MUR Port Louis": "[PLB]",
    "MXN Mexico": "[MXB]",
    "MYR Kuala Lumpur": "[KLX]",
    "NGN Lagos": "[JOB]",
    "NOK Oslo": "[OSS]",
    "NZD Auckland": "[AKW]",
    "PKR Islamabad": "[KAB]",
    "PLN Warsaw": "[WAB]",
    "SAR Riyad": "[RIB]",
    "SEK Stockholm": "[STB]",
    "SGD Singapore": "[SIB]",
    "THB - Thai": "[BKB]",
    "TZS Dar es Salaam": "[JOB]",
    "Target": "[TGT]",
    "UGX Uganda": "[JOB]",
    "USD New York": "[NYB]",
    "ZAR Johannesburg": "[JOB]",
    "ZMK Lusaka": "[JOB]",
    "ZMW Lusaka": "[JOB]",
    }

DAYCOUNT_MAPPING = {
    "Act/360": ("Act", "360"),
    "Act/364": ("Act", "365"),
    "Act/365": ("Act", "365F"),
    "Act/ActAFB": ("Act", "ActA"),
    "Act/ActISMA": ("Act", "ISMA"),
    "30/360": ("30",  "360"),
    "30/360GERMAN": ("30G", "360"),
    "30/365": ("30",  "365F"),
    "30E/365": ("30E", "365F"),
    "30E/360": ("30E", "360"),
    "30U/360": ("30N", "360"),
    }

ROLLCONVENTION_MAPPING = {
    "None": "None",
    "Following": "Following",
    "Mod. Following": "ModifiedFollowing",
    "Preceding": "Previous",
    "Mod. Preceding": "ModifiedPrevious",
    "EOM": "EndOfMonth",                          
    }

CASHFLOWTYPE_MAPPING = {
    "Termination Fee": "Settlement",
    "Cash": "Settlement",
    "Exercise Cash": "Settlement"
    }

ABCAP_LEGALENTITY = 40483404

FIXING_TIMESERIES = "AvgRateWeightings"

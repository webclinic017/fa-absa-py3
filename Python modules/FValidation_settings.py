"""FValidation - Settings for core modules.

Before changing the code, please consult the Developer's Guide available at
<https://confluence-agl.absa.co.za/display/ABCAPFA/FValidation+Developer%27s+Guide>.

The list of implemented FValidation rules is kept at
<https://confluence-agl.absa.co.za/display/ABCAPFA/FValidation+rules>.
Please keep it in sync with the code.


This module contains settings used by other FValidation core modules.
No FValidation rule should be put into this module.


History
=======

2016-05-09 Vojtech Sidorin  Initial implementation; ABITFA-3286: Move constants to module FValidation_settings.
2017-03-30 Vojtech Sidorin  FAU-816: Add the FValidation_CreditEventSpecHotfix module.
2017-05-11 Vojtech Sidorin  FAU-816: Remove the FValidation_CreditEventSpecHotfix module. The bug was fixed in FA 2017.1.1.
2018-11-13 Libor Svoboda    FtF-CAL: Add FValidation_cal.
2019-02-14 Libor Svoboda    FtF-CAL: Add FValidation_text_object.
2019-10-15 Stuart Wilson    FAOPS-607: Added ability to force super user to validate against particular validations
2020-06-03 Libor Svoboda    Remove redundant module FValidation_depr_SecLending
2020-08-25 Snowy Mabilu 	ARR-60 - Validation rules for FINRA reporting
2020-10-08 Libor Svoboda    Add FValidation_user_profile.
2021-02-23 Libor Svoboda    Add FValidation_price_testing.
"""

# Enable FValidation.  True for normal operation in production.  Set to False
# to bypass all validation rules.
ENABLE_VALIDATION = True

# Turn on debugging messages.  False for normal operation in production.
DEBUG = False

# Users that bypass FValidation.
SUPERUSERS = [
        "FMAINTENANCE",
        "UPGRADE43",
        "FORE_FRONT_TST",
        "FORE_FRONT_PRD",
        "ATS_AMWI_PRD",
        "ATS_AMWI_TST",
        "AGGREGATION"
        ]
# does not support FValidation_depr
SUPERUSER_VALIDATIONS = {
    'FORE_FRONT_PRD': ['fv138set_security_settlement_fields']
}

# Modules with the FValidation rules.
# These modules contain functions decorated with the FValidation decorators.
# A decorated function becomes an FValidation rule.  In most cases you won't
# need to care about the order in which the rules are called.  If you do,
# however, the order is given by:
#  (1) The decorator type:  First, functions decorated with
#      @validate_transaction are called, then functions decorated with
#      @validate_entity(..., caller=validate_transaction), and finally
#      functions decorated with @validate_entity(...).
#  (2) The module type:  The enrichment rules defined in the ENRICHMENT_MODULES
#      list are called before the rules defined in the VALIDATION_MODULES list.
#  (3) The order in which the rules are defined within a module.
#
# ENRICHMENT_MODULES -- modules with rules that modify entities.
# VALIDATION_MODULES -- modules with general validation rules.
#
# If you are implementing a new rule and are unsure where to put it, add the
# rule to the FValidation_General module.
#
# NOTE: No new code should go into the _depr_ modules, only hotfixes if
# necessary.  These modules are deprecated, and the rules defined there should
# be progressively refactored and moved into non-deprecated modules.
ENRICHMENT_MODULES = [
        "FValidation_enrich_SecLending",
        ]
VALIDATION_MODULES = [
        "FValidation_General",
        "FValidation_FixedIncome",
        "FValidation_depr_General",
        "FValidation_depr_MoneyMarket",
        "FValidation_depr_PaceFXO",
        "FValidation_YC_Vol_Access",
        "FValidation_SettleConf",
        "FValidation_SecLending",
        "FValidation_FOCallTrader",
        "FValidation_DatesTimes",
        "FValidation_Volcker",
        "FValidation_cal",
        "FValidation_text_object",
        "FValidation_FINRA_Reporting",
        "FValidation_user_profile",
        "FValidation_price_testing",
        ]

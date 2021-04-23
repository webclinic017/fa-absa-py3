from datetime import datetime
import acm
from PS_Functions import (get_pb_fund_shortname,
                          get_pb_fund_counterparties)
from at_email import EmailHelper


SAXO_PAYMENT_PORTF = "PB_SAXO"
REPORT_PORTF_TEMPL = "PB_SAXO_PRINCIPAL"
DEPO_PORTFOLIO = "PB_SAXO_DEPO"

CF_TPL_TYPE = "PB_Saxo_%(saxotype)s_TPL"
CF_PRREFUND_TYPE = "PB_Saxo_Prefund"
CF_INITMARGIN_TYPE = "PB_Saxo_InitMargin"

SAXO_COUNTERPARTY = "SAXO BANK AS"


INT_FUTURES_NAME = "FUT"
INT_CFD_NAME = "CFD"
INT_ETO_NAME = "ETO"
INT_FX_SPOT_FWD_NAME = "FX"
INT_FX_OPTION_NAME = "FXO"
INT_SHARES_NAME = "STO"

SAXO_FUT_TYPE = "Contract Futures"
SAXO_CFD_TYPE = "CFDs"
SAXO_ETO_TYPE = "Contract Options"
SAXO_FX_TYPE = "Fx Spot & Forwards"
SAXO_FXO_TYPE = "Fx Options"
SAXO_STO_TYPE = "Shares"


# Saxo instype -> FA alias mapping
SAXO_TYPES = {
              SAXO_FUT_TYPE: INT_FUTURES_NAME,
              SAXO_CFD_TYPE: INT_CFD_NAME,
              SAXO_ETO_TYPE: INT_ETO_NAME,
              SAXO_FX_TYPE: INT_FX_SPOT_FWD_NAME,
              SAXO_STO_TYPE: INT_SHARES_NAME,
              SAXO_FXO_TYPE: INT_FX_OPTION_NAME
              }


CP_ALIASES = None  # store all existing aliases/shortnames here during the run
# alias mapping:
# Saxo alias -> FA alias
SAXO_FA_ALIAS_MAP = {
                     "CORG": "CORINOV",
                     "NOVFI3A": "NOVFI3"
                     }

EMAIL_RECIPIENTS = "PrimeServicesTS@absacapital.com,CIBAfricaTSDevPrime@internal.barclayscapital.com"


CALENDAR = acm.FCalendar['ZAR Johannesburg']


def get_prev_nonweekend_day(the_date):
    """
    Get previous non-weekend date for the input date.

    '2016-12-23' (Friday) -> '2016-12-22' (Thursday)
    '2016-12-24' (Saturday) -> '2016-12-23' (Friday)
    '2016-12-26' (Monday) -> '2016-12-23' (Friday)
    """
    WEEKEND_DAYS = ("Saturday", "Sunday")
    for day_delta in range(-1, -4, -1):
        prev_date = acm.Time.DateAddDelta(the_date, 0, 0, day_delta)
        prev_day = acm.Time.DayOfWeek(prev_date)
        if prev_day not in WEEKEND_DAYS:
            return prev_date


TODAY = acm.Time().DateToday()
PREVBUSDAY = CALENDAR.AdjustBankingDays(TODAY, -1)
PREV_NON_WEEKEND = get_prev_nonweekend_day(TODAY)
DATE_LIST = {
             'PrevNonWeekendDay': PREV_NON_WEEKEND,
             'Now': TODAY,
             'Custom Date': TODAY,
             }
DATE_KEYS = DATE_LIST.keys()
DATE_KEYS.sort()


def get_account_alias(acc_number):
    """Get fund alias from Saxo ID
    Examples:
        # 78500/MROC --> MROC
        # 78500/MROCGBP --> MROC
        # 78500/NOVFI3aGBP --> NOVFI3
        # 78500/CORGGBP --> CORINOV
        # 78500/CORG --> CORINOV
    """
    alias = acc_number[acc_number.find('/') + 1:]
    global CP_ALIASES
    if not CP_ALIASES:
        CP_ALIASES = [get_pb_fund_shortname(cp) for cp in get_pb_fund_counterparties()]
    if alias in CP_ALIASES:
        return alias
    elif SAXO_FA_ALIAS_MAP.has_key(alias):
        return SAXO_FA_ALIAS_MAP[alias]
    elif '/' in acc_number:  # first function call, remove suffix
        return get_account_alias(alias[:-3])
    return None


def get_saxo_types():
    return SAXO_TYPES.keys()


def get_alias_from_alias_or_cp(alias_or_cp):
    if isinstance(alias_or_cp, str):
        return alias_or_cp
    return get_pb_fund_shortname(alias_or_cp)


def get_fund_portf(alias_or_cp):
    alias = get_alias_from_alias_or_cp(alias_or_cp)
    # no alias required for now. For future dev
    return acm.FPhysicalPortfolio[REPORT_PORTF_TEMPL % {'alias': alias}]


def get_saxo_depo_portfolio():
    return acm.FPhysicalPortfolio[DEPO_PORTFOLIO]


def get_saxo_cp():
    return acm.FParty[SAXO_COUNTERPARTY]


def get_saxo_instype_alias(saxo_ins_type):
    return SAXO_TYPES[saxo_ins_type]


def get_saxo_type_from_fa_type(fa_type):
    for saxo_t, fa_t in SAXO_TYPES.items():
        if fa_type == fa_t:
            return saxo_t
    raise RuntimeError("Unknown FA instrument type alias: '%s'" % fa_type)


def get_cf_tpl_type(saxo_type):
    return CF_TPL_TYPE % {'saxotype': saxo_type}


def send_mail(subject, body, recipients_list):
    environment = acm.FDhDatabase['ADM'].InstanceName()
    email_helper = EmailHelper(
        body,
        '{} - {}'.format(subject, environment),
        recipients_list,
    )
    if str(acm.Class()) == "FACMServer":
        email_helper.sender_type = EmailHelper.SENDER_TYPE_SMTP
        email_helper.host = EmailHelper.get_acm_host()

    try:
        email_helper.send()
    except Exception as exc:
        print "Error while sending e-mail: %s" % str(exc)


def get_backend_date(date_str):
    if "-" in date_str:
        return date_str
    return datetime.strptime(date_str, '%d/%m/%Y').strftime('%Y-%m-%d')

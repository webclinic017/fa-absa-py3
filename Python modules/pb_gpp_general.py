from datetime import datetime
import csv
import os

import acm
from PS_Functions import (get_pb_fund_shortname,
                          get_pb_fund_counterparties)


ACCOUNTS_FILE_PATH = None  # r"c:\DEV\Perforce\FA\features\ABITFA-4916 - GPP - go live.br\input\accounts.csv"
ACCOUNTS_FILE_PATH_FRONT = r"y:\Jhb\FAReports\AtlasEndOfDay\PrimeClients\GPP\config\accounts.csv"
ACCOUNTS_FILE_PATH_BACK = r"/nfs/fa/reports/EMEA/prod/FAReports/AtlasEndOfDay/PrimeClients/GPP/config/accounts.csv"

INSTRS_FILE_PATH = None  # r"c:\DEV\Perforce\FA\features\ABITFA-4916 - GPP - go live.br\input\instruments.csv"
INSTRS_FILE_PATH_FRONT = r"y:\Jhb\FAReports\AtlasEndOfDay\PrimeClients\GPP\config\instruments.csv"
INSTRS_FILE_PATH_BACK = r"/nfs/fa/reports/EMEA/prod/FAReports/AtlasEndOfDay/PrimeClients/GPP/config/instruments.csv"

GPP_COUNTERPARTY = 48938  # "GLOBAL PRIME PARTNERS LIMITED"

PAYMENT_PORTF = 9523  # "PB_GPP"  # prefund portfolio
TRADING_PORTF = 9524  # "PB_GPP_PRINCIPAL"
DEPO_PORTFOLIO = 9525  # "PB_GPP_DEPO"

CF_TPL_TYPE = "PB_GPP_%(gpptype)s_TPL"
CF_PRREFUND_TYPE = "PB_GPP_Prefund"
CF_INITMARGIN_TYPE = "PB_GPP_InitMargin"

CP_ALIASES = None  # store all existing aliases/shortnames during the run

# extra alias mapping when a different alias than in FA is used in GPP
# GPP alias -> FA alias
GPP_FA_ALIAS_MAP = None

# INSTR -> UNDERLYING
INSTR_UND_MAP = None

GPP_FUT_TYPE = "Futures"
GPP_CFD_TYPE = "Equity Swap"
GPP_OPT_TYPE = "Listed Equity Option"
GPP_STO_TYPE = "Equity"

INT_FUT_NAME = "FUT"
INT_CFD_NAME = "CFD"
INT_OPT_NAME = "OPT"
INT_STO_NAME = "STO"


GPP_TYPES = {
             GPP_FUT_TYPE:INT_FUT_NAME,
             GPP_CFD_TYPE:INT_CFD_NAME,
             GPP_OPT_TYPE:INT_OPT_NAME,
             GPP_STO_TYPE:INT_STO_NAME,
             }

QFOLDERS = {
            GPP_FUT_TYPE:"PB_GPP_FUT",
            GPP_CFD_TYPE:"PB_GPP_CFD",
            GPP_OPT_TYPE:"PB_GPP_OPT",
            GPP_STO_TYPE:"PB_GPP_STO",
            }


# underlyings:
GPP_COMM = "GPP_commodity"
GPP_FI = "GPP_FI"
GPP_FX = "GPP_FX"
GPP_EQIDX = "GPP_equityindex"
GPP_EQ = "GPP_equity"


def is_valid_gpp_instype(gpp_type):
    return gpp_type in GPP_TYPES


def get_fa_instype_alias(gpp_ins_type):
    return GPP_TYPES.get(gpp_ins_type)


def get_gpp_ins_types():
    return GPP_TYPES.keys()


def get_query_folder(gpp_ins_type):
    return QFOLDERS.get(gpp_ins_type)


def get_gpp_type_from_fa_type(fa_instype):
    for gpp_t,fa_t in SAXO_TYPES.items():
        if fa_instype == fa_t:
            return gpp_t
    raise RuntimeError("Unknown FA instrument type alias: '%s'" % fa_instype)


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


def get_five_bus_days_ago(the_date):
    cal = acm.FCurrency['ZAR'].Calendar()
    return cal.AdjustBankingDays(the_date, -5)


TODAY = acm.Time().DateToday()
PREV_NON_WEEKEND = get_prev_nonweekend_day(TODAY)
FIVE_BUS_DAYS_AGO = get_five_bus_days_ago(TODAY)
DATE_LIST = {
             'PrevNonWeekendDay':PREV_NON_WEEKEND,
             'FiveBusDaysAgo':FIVE_BUS_DAYS_AGO,
             'Now':TODAY,
             'Custom Date':TODAY,
             }
DATE_KEYS = DATE_LIST.keys()
DATE_KEYS.sort()



def get_gpp_cp():
    return acm.FParty[GPP_COUNTERPARTY]


def get_trading_portf():
    return acm.FPhysicalPortfolio[TRADING_PORTF]


def get_depo_portf():
    return acm.FPhysicalPortfolio[DEPO_PORTFOLIO]


def get_payment_portf():
    return acm.FPhysicalPortfolio[PAYMENT_PORTF]


def get_cf_tpl_type(gpp_ins_type):
    return CF_TPL_TYPE % {'gpptype':gpp_ins_type}


def get_account_alias(account_name):
    """Get fund alias from GPP ID
    Examples:
        # ABSA Bank Ltd - 1.1 --> MAP501
        # ABSA Bank Ltd - 5 FTMOKA --> FTMOKA
    """
    global GPP_FA_ALIAS_MAP
    if not GPP_FA_ALIAS_MAP:
        GPP_FA_ALIAS_MAP = load_accounts(ACCOUNTS_FILE_PATH)

    alias = GPP_FA_ALIAS_MAP.get(account_name.upper())
    if not alias:
        return None

    global CP_ALIASES
    if not CP_ALIASES:
        CP_ALIASES = [get_pb_fund_shortname(cp) for cp in get_pb_fund_counterparties()]
    if alias in CP_ALIASES:
        return alias


def get_underlying(bloomberg_code):
    global INSTR_UND_MAP
    if not INSTR_UND_MAP:
        INSTR_UND_MAP = load_underlyings(INSTRS_FILE_PATH)

    return INSTR_UND_MAP.get(bloomberg_code)


def get_alias_from_alias_or_cp(alias_or_cp):
    if type(alias_or_cp) == str:
        return alias_or_cp
    return get_pb_fund_shortname(alias_or_cp)


def remove_nonascii(name):
    return ''.join(chr if ord(chr) < 128 else '' for chr in name)


def get_backend_date(date_str):
    if "-" in date_str:
        return date_str
    return datetime.strptime(date_str, '%d/%m/%Y').strftime('%Y-%m-%d')


def und_from_cfi(cfi_code):
    ins_type = cfi_code[0]

    # OPTION
    if ins_type == 'O':
        und_asset = cfi_code[3]

        if und_asset == 'S':
            return acm.FInstrument[GPP_EQ]
        elif und_asset == 'I':
            return acm.FInstrument[GPP_EQIDX]
        elif und_asset == 'C':
            return acm.FInstrument[GPP_FX]
        elif und_asset == 'T':
            return acm.FInstrument[GPP_COMM]
        elif und_asset == 'B':
            return acm.FInstrument[GPP_EQIDX]

    # FUTURE
    if ins_type == 'F':
        und_type = cfi_code[1]

        if und_type == 'C':
            return acm.FInstrument[GPP_COMM]

        und_asset = cfi_code[2]
        if und_asset == 'S':
            return acm.FInstrument[GPP_EQ]
        elif und_asset == 'I':
            return acm.FInstrument[GPP_EQIDX]
        elif und_asset == 'C':
            return acm.FInstrument[GPP_FX]
        elif und_asset == 'B':
            return acm.FInstrument[GPP_EQIDX]


def load_accounts(accounts_file):
    """
    Return dictionary with GPP -> FA account aliases.
    """
    acnt_dct = {}
    with open(accounts_file, "rb") as csv_file:
        reader = csv.DictReader(csv_file, delimiter=",")
        for dict_line in reader:
            gpp_alias = dict_line["GPP Account name"].upper()
            if gpp_alias:
                acnt_dct[gpp_alias] = dict_line["FA Alias"]

    return acnt_dct


def load_underlyings(underlyings_file):
    """
    Return dictionary with Instrument -> Und Ins mappings.
    """
    ins_dct = {}
    with open(underlyings_file, "rb") as csv_file:
        reader = csv.DictReader(csv_file, delimiter=",")
        for dict_line in reader:
            instr = dict_line["BloombergCode"]
            if instr:
                ins_dct[instr] = dict_line["Underlying"]

    return ins_dct


def add_common_aelvars(ael_variables, tab_name="Settings"):

    tab_label = ""
    if tab_name and tab_name != "General":
        tab_label = "_" + tab_name

    ael_variables.add("file_accounts",
        label="Accounts File%s" % tab_label,
        default=ACCOUNTS_FILE_PATH_FRONT,
        collection=(ACCOUNTS_FILE_PATH_FRONT, ACCOUNTS_FILE_PATH_BACK),
        alt="A path to accounts input file.")

    ael_variables.add("file_instrs",
        label="Instruments File%s" % tab_label,
        default=INSTRS_FILE_PATH_FRONT,
        collection=(INSTRS_FILE_PATH_FRONT, INSTRS_FILE_PATH_BACK),
        alt="A path to instruments input file.")


def set_general_input(ael_dict):
    global ACCOUNTS_FILE_PATH
    ACCOUNTS_FILE_PATH = ael_dict["file_accounts"]

    global INSTRS_FILE_PATH
    INSTRS_FILE_PATH = ael_dict["file_instrs"]


def get_filepaths(directory, file_substr):
    file_list = []
    for root, dirs, files in os.walk(directory):

        # for each file in root directory
        for filename in files:
            if file_substr in filename:
                fullpath = os.path.join(root, filename)
                file_list.append(fullpath)
    return file_list


def get_account_nbr(filepath):
    filename = os.path.basename(filepath)
    parts = filename.split('_')
    return parts[1]


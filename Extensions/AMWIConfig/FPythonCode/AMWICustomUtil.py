"""

AMWICustomUtil

"""
from inspect import stack
from os import mkdir
from os.path import isdir, exists
from traceback import print_exc

import FFpMLParserUtils
import acm
from xml.dom.minidom import parseString

from AMWICommon import AMWI_STATUS_BO_CONFIRMED, AMWI_STATUS_BOBO_CONFIRMED, AMWI_STATUS_TERMINATED, AMWI_STATUS_VOID
from AMWICommon import log_error, log_debug, AMWI_STATUS_SIMULATED, AMWI_STATUS_FO_CONFIRMED
from AMWIIdentity import update_all_mirrors, is_allocate_trade
from AMWITradeUtil import unfix_basis_swap_resets

STATUS_PRIORITY = {
    AMWI_STATUS_SIMULATED: 0,
    AMWI_STATUS_FO_CONFIRMED: 1,
    AMWI_STATUS_BO_CONFIRMED: 2,
    AMWI_STATUS_BOBO_CONFIRMED: 3,
    AMWI_STATUS_TERMINATED: 4,
    AMWI_STATUS_VOID: 5,
}

VALID_ALLOCATION_STATUS = [
    AMWI_STATUS_SIMULATED,
    AMWI_STATUS_FO_CONFIRMED,
    AMWI_STATUS_TERMINATED,
    AMWI_STATUS_VOID,
]

EVENT_TO_STATUS = {
    "ready": AMWI_STATUS_FO_CONFIRMED,
    "pickedup": AMWI_STATUS_FO_CONFIRMED,
    "affirmed": AMWI_STATUS_FO_CONFIRMED,
    "cptyaffirmed": AMWI_STATUS_BO_CONFIRMED,
    "agreed": AMWI_STATUS_BO_CONFIRMED,
    "released": AMWI_STATUS_BOBO_CONFIRMED,
    "withdrawn": AMWI_STATUS_VOID,

    # Clearing statuses
    "chsubmitted": AMWI_STATUS_VOID,
    "registered": AMWI_STATUS_BO_CONFIRMED,
    "cleared": AMWI_STATUS_BO_CONFIRMED,
    "beta cleared": AMWI_STATUS_BOBO_CONFIRMED,
    "rejected": AMWI_STATUS_VOID,

    # Novation statuses
    "novation initiated": AMWI_STATUS_SIMULATED,
    "novation affirmed": AMWI_STATUS_SIMULATED,

    # Target state is error on a new workflow
    "error": None,
}

FSWML_LOG_DIR = None
IGNORE_TRADE_LIST = None
IGNORE_USER_LIST = None


def _get_status_order(status, default=0):
    if status in STATUS_PRIORITY:
        return STATUS_PRIORITY[status]
    else:
        log_debug("Unknown status: %s" % status)
        return default


def _get_caller_name():
    module = stack()[2][1]
    method = stack()[2][3]
    return "%s.%s()" % (module, method)


def _get_trade_description(trade):
    if trade:
        r = []
        r.append("mw_id=%s" % str(trade.AdditionalInfo().CCPmiddleware_id()))
        if trade.ContractTrdnbr():
            r.append("contract_id=%i" % trade.ContractTrdnbr())
        if trade.ConnectedTrdnbr():
            r.append("trade_id=%i" % trade.ConnectedTrdnbr())

        return ", ".join(r)

    return ""


def _get_context_description(context):
    if context and context.Subject():
        return _get_trade_description(context.Subject())

    return ""


def _load_ignore_trades(filename):
    r = {}
    with open(filename, "r") as fin:
        for line in fin:
            trade = acm.FTrade[int(line)]
            if trade:
                mw_id = trade.AdditionalInfo().CCPmiddleware_id()
                if mw_id:
                    r[mw_id] = trade

        return r


# Gets a list of Front trade IDs that should be ignored from a file
# pointed to by FParameter:
#   FSWMLImportConfig.FSWML_EXCLUDE_TRADES_FILE
def get_ignore_trades():
    global IGNORE_TRADE_LIST
    if IGNORE_TRADE_LIST is None:
        IGNORE_TRADE_LIST = {}
        try:
            log_debug("Loading Exclude Trade list")
            parameter_ex = acm.GetDefaultContext().GetExtension(acm.FParameters, acm.FObject, "FSWMLImportConfig")
            if parameter_ex:
                filename = parameter_ex.Value()["FSWML_EXCLUDE_TRADES_FILE"]
                if filename:
                    filename = filename.Text()
                    if exists(filename):
                        log_debug("Loading ignore trades from %s" % filename)
                        IGNORE_TRADE_LIST = _load_ignore_trades(filename)
                        log_debug("  %i trade ids loaded" % len(IGNORE_TRADE_LIST))
                    else:
                        log_error("Cannot find ignore trades file: %s" % filename)
                else:
                    log_debug("  FParameter FSWMLImportConfig.FSWML_EXCLUDE_TRADES_FILE not found.")
        except Exception as x:
            log_error("Exception loading IGNORE_TRADE_LIST: %s" % str(x))
            print_exc()

    return IGNORE_TRADE_LIST


# Gets a list of user prefixes to be ignored from Fparameter:
#   FSWMLImportConfig.FSWML_EXCLUDE_USERS
def get_ignore_users():
    global IGNORE_USER_LIST
    if IGNORE_USER_LIST is None:
        IGNORE_USER_LIST = []
        try:
            log_debug("Loading Exclude User list")
            parameter_ex = acm.GetDefaultContext().GetExtension(acm.FParameters, acm.FObject, "FSWMLImportConfig")
            if parameter_ex:
                users = parameter_ex.Value()["FSWML_EXCLUDE_USERS"]
                if users:
                    IGNORE_USER_LIST = [s.strip() for s in users.Text().split(",") if s.strip()]
                    log_debug("  Ignore user prefixes loaded: %s" % ", ".join(IGNORE_USER_LIST))
                else:
                    log_debug("  FParameter FSWMLImportConfig.FSWML_EXCLUDE_USERS not found.")
        except Exception as x:
            log_error("Exception loading IGNORE_TRADE_LIST: %s" % str(x))
            print_exc()

    return IGNORE_USER_LIST


def get_log_dir(subdir=None):
    global FSWML_LOG_DIR
    if not FSWML_LOG_DIR:
        FSWML_LOG_DIR = "."
        parameter_ex = acm.GetDefaultContext().GetExtension(acm.FParameters, acm.FObject, "FSWMLLogConfig")
        if not parameter_ex:
            log_error("Cannot find FParameters: FSWMLLogConfig")
        else:
            log_dir = parameter_ex.Value()["FSWML_LOG_DIR"]
            if not log_dir:
                log_error("FParameter FSWMLLogConfig.FSWML_LOG_DIR not set")
            else:
                log_dir = log_dir.Text().replace("'", "").replace("\\\\", "\\")
                if not isdir(log_dir):
                    log_error("Log directory does not exist: %s" % log_dir)
                else:
                    log_debug("FSWML_LOG_DIR: %s" % log_dir)
                    FSWML_LOG_DIR = log_dir

    r = FSWML_LOG_DIR
    if subdir:
        r = "%s/%s" % (r, subdir)
        if not isdir(r):
            mkdir(r)

    return r


def get_swml_filename(trade_id):
    log_dir = get_log_dir("messages")
    sub_dir = "%s/%s%s" % (log_dir, trade_id[0:3], "x" * (len(trade_id) - 3))
    if not isdir(sub_dir):
        mkdir(sub_dir)

    for i in range(1, 99):
        filename = "%s/%s_%02i.xml" % (sub_dir, trade_id, i)
        if not exists(filename):
            return filename

    return "%s/%s_xx.xml" % (sub_dir, trade_id)


def get_status_transition_direction(current_status, new_status):
    current_order = _get_status_order(current_status)
    new_order = _get_status_order(new_status)

    if current_order == new_order:
        return 0
    elif current_order < new_order:
        return 1
    elif current_status in (AMWI_STATUS_VOID, AMWI_STATUS_TERMINATED):
        # Clearing trades can go from void to another status
        return 1
    else:
        return -1


def _set_status(context, new_status, allow_reverse_transition, log_info):
    current_status = context.Subject().Status()
    direction = get_status_transition_direction(current_status, new_status)

    if new_status not in VALID_ALLOCATION_STATUS and is_allocate_trade(context.Subject()):
        log_debug("REJECT_STATUS (ALLOCATION_PORTFOLIO) %s" % log_info)
    elif direction < 0 and not allow_reverse_transition:
        log_debug("REJECT_STATUS %s" % log_info)
    elif direction == 0:
        log_debug("IGNORE_STATUS %s" % log_info)
    else:
        log_debug("SET_STATUS %s" % log_info)

        context.Subject().Status(new_status)

    target_state = context.TargetState().Name().lower()
    if target_state in ("released", "withdrawn"):
        update_all_mirrors(context.Subject())

    amended_resets = unfix_basis_swap_resets(context.Subject().Instrument(), acm.Time.DateToday())
    if amended_resets:
        context.Subject().Instrument().Commit()


def set_status(context, new_status, allow_reverse_transition=False):
    log_info = "%s: %s, old_status=%s, new status=%s" % (_get_caller_name(),
                                                         _get_context_description(context),
                                                         context.Subject().Status(),
                                                         new_status)

    _set_status(context, new_status, allow_reverse_transition, log_info)


def set_status_by_context(context):
    target_state = context.TargetState().Name().lower()
    if target_state in EVENT_TO_STATUS:
        new_status = EVENT_TO_STATUS[target_state]
        log_info = "%s: %s, event=%s, old_status=%s, new status=%s" % (_get_caller_name(),
                                                                       _get_context_description(context),
                                                                       context.Event().Name(),
                                                                       context.Subject().Status(),
                                                                       new_status)

        if new_status:
            _set_status(context, new_status, False, log_info)
    else:
        log_error("INVALID_STATE %s: %s, state=%s, event=%s" % (_get_caller_name(),
                                                                _get_context_description(context),
                                                                target_state,
                                                                context.Event().Name()))


def set_contract_status(context, new_status):
    trade = context.Subject().Contract()
    log_debug("SET_CONTRACT_STATUS %s: %s, old_status=%s, new status=%s" % (_get_caller_name(),
                                                                            _get_context_description(context),
                                                                            trade.Status(),
                                                                            new_status))

    trade.Status(new_status)
    trade.Commit()


def set_type(context, new_type):
    log_debug("SET_TYPE %s: %s, old_type=%s, new type=%s" % (_get_caller_name(),
                                                             _get_context_description(context),
                                                             context.Subject().Type(),
                                                             new_type))

    context.Subject().Type(new_type)


def is_mwire_new_status(trade, new_status):
    trade_new_status = trade.AdditionalInfo().CCPmwire_new_status()
    if trade_new_status == new_status:
        return True

    return False


def log_in_method(context=None):
    if context:
        log_debug("IN_METHOD %s: %s" % (_get_caller_name(),
                                        _get_context_description(context)))
    else:
        log_debug("IN_METHOD %s" % _get_caller_name())


def log_in_method_trade(trade):
    log_debug("IN_METHOD %s: %s" % (_get_caller_name(),
                                    _get_trade_description(trade)))


def swml_all_nodes(swml, path):
    swml_doc = parseString(swml)
    try:
        return FFpMLParserUtils.retrieveAllNodesValues(path, [swml_doc], True)
    except Exception as x:
        log_error("Exception whilst attempting to retrieve XML: %s" % path)
        print_exc()
        return None


def swml_attr_value(swml, path, attr_name):
    swml_doc = parseString(swml)
    attr_values = FFpMLParserUtils.retrieveAttributeValue(path, [swml_doc], attr_name)
    if attr_values:
        return attr_values[0]

    return ""


def swml_value(swml, path, error_message=""):
    node_values = swml_all_nodes(swml, path)
    if node_values:
        return node_values[0]

    if error_message:
        log_debug("No value for node %s: %s" % (path, error_message))

    return ""


# Initialise singletons
get_ignore_trades()
get_ignore_users()

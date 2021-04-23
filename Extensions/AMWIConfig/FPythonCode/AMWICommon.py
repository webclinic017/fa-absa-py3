AMWI_STATUS_SIMULATED = "Simulated"
AMWI_STATUS_FO_CONFIRMED = "FO Confirmed"
AMWI_STATUS_BO_CONFIRMED = "BO Confirmed"
AMWI_STATUS_BOBO_CONFIRMED = "BO-BO Confirmed"
AMWI_STATUS_TERMINATED = "Terminated"
AMWI_STATUS_VOID = "Void"

AMWI_TYPE_CLOSING = "Closing"
AMWI_TYPE_NORMAL = "Normal"

AMWI_NEW_STATUS_REJECTED_CLEARING = "RejectedForClearing"


def log_debug(message):
    print("[DEBUG] %s" % message)


def log_error(message):
    print("ERROR: %s" % message)


def log_warning(message):
    print("WARNING: %s" % message)

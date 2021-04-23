import acm
import FUxUtils
from traceback import print_exc
'''The following group names are FO TCU Management, System Processes, and IT RTB'''
AMWI_ALLOWED_GROUPS = [646, 495, 563]


def _get_frame(shell):
    for Application in acm.ApplicationList():
        if Application.Shell() == shell:
            return Application

    return None


def _is_allowed_user(user):
    if user.UserGroup().Oid() in AMWI_ALLOWED_GROUPS:
        return True

    return False


def _is_markitwire_trade(shell, params):
    data = FUxUtils.UnpackInitialData(params)
    if data:
        trade = _get_frame(shell).EditTrade()
        if trade:
            if trade.Contract():
                trade = trade.Contract()

            if trade.AdditionalInfo().CCPmiddleware_id():
                return True

    return False


def ael_custom_dialog_show(shell, params):
    list_of_users = []
    try:
        if _is_markitwire_trade(shell, params):
            user = acm.User()
            if not _is_allowed_user(user):
                msg = "User %s must be in one of the following groups \n" + \
                      "in order to modify a MarkitWire trade: \n * %s"
                for user_allowed in AMWI_ALLOWED_GROUPS:
                    group_user = acm.FUserGroup[user_allowed]
                    list_of_users.append(group_user.Name())
                acm.UX().Dialogs().MessageBoxInformation(shell, msg % (user.UserGroup().Name(),
                                                                   "\n * ".join(list_of_users)))

                return None

    except Exception, e:
        print_exc()
        print("Exception in AMWI_TradeValidation: %s" % str(e))

    return params


def ael_custom_dialog_main(parameters, dict_extra):
    del parameters
    return dict_extra

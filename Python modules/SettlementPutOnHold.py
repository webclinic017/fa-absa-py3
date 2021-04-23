"""-----------------------------------------------------------------------------
PURPOSE                 : Logic for Put on Hold context menu option
                          for Settlement menu
DEPATMENT AND DESK      :
REQUESTER               : Elaine Visagie
DEVELOPER               : Gabriel Marko
CR NUMBER               :
--------------------------------------------------------------------------------

HISTORY
================================================================================
Date        Change no       Developer      Description
--------------------------------------------------------------------------------
2016-11-29  CHNG0004156927  Gabriel Marko  Initial implementation
"""

import acm


def put_settlement_on_hold(settlement):
    msg_box = acm.GetFunction('msgBox', 3)
    if msg_box('Put Settlement On Hold', 'Do you want to put settlement %s on hold?' % settlement.Oid(), 1) == 1:
        try:
            settlement.Status('Hold')
            settlement.Commit()
        except Exception as ex:
            acm.Log("Error while commiting the settlement %s:\r%s" % (settlement.Oid(), ex))
            raise


def start_dialog_cb(eii, *rest):
    if eii.ExtensionObject().IsKindOf(acm.FIndexedCollection):
        settlement = eii.ExtensionObject().At(0)
        if settlement:
            put_settlement_on_hold(settlement)
        else:
            acm.Log('No settlement was selected.')

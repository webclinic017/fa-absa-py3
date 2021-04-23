'''----------------------------------------------------------------------------------------------------------
MODULE                  :       FC_AMBA_TRD_HOOK
PROJECT                 :       FX onto Front Arena
PURPOSE                 :       This module will remove all the PAYMENT AMB objects from an incoming trade
                                AMBA message
DEPARTMENT AND DESK     :       All Departments and all Desks.
REQUASTER               :       FX onto Front Arena Project
DEVELOPER               :       Aaron Viljoen
CR NUMBER               :       XXXXXX
----------------------------------------------------------------------------------------------------------'''

import datetime
import acm
from at_time import to_datetime
'''----------------------------------------------------------------------------------------------------------
Import custom modules
----------------------------------------------------------------------------------------------------------'''
from AMBA_Helper_Functions import AMBA_Helper_Functions as AMBA_Utils

class FC_AMBA_TRD_HOOK(object):
    @staticmethod
    def remove_SPECIFIC_Object(trade_obj, prefix, objectName):
        for obj in AMBA_Utils.objects_by_name(trade_obj, prefix, objectName):
            trade_obj.mbf_remove_object()

def FC_AMBA_Trd_Hook_Modify_Sender(msg, s):

    msgType = AMBA_Utils.get_object_type(msg)
    
    if not msgType:
        return None

    ambTrade = msg.mbf_find_object("TRADE", "MBFE_BEGINNING")
    if ambTrade:
        status = ambTrade.mbf_find_object("STATUS", "MBFE_BEGINNING").mbf_get_value()
        if status and str(status) == 'Simulated':
            return None

    trade_obj = AMBA_Utils.object_by_name(msg, ['+', '!', ''], msgType)
    if not trade_obj:
        return None

    try:
        FC_AMBA_TRD_HOOK.remove_SPECIFIC_Object(trade_obj, ['+', '!', '', '-'], 'PAYMENT')
    except Exception, e:
        print 'ERROR on removing AMBA Object %s: %s' %('PAYMENT', str(e))

    try:
        trdnbr = ambTrade.mbf_find_object("TRDNBR", "MBFE_BEGINNING").mbf_get_value()
	list = []
	t = acm.FTrade[trdnbr]
	if t not in list:
	    list.append(t)
	    if t.IsFxSwap():
	        connectedTrades = acm.FTrade.Select('connectedTrdnbr = %s' % t.ConnectedTrade().Oid())
	        for connectedTrade in connectedTrades:
	            if connectedTrade not in list:
	                list.append(connectedTrade)

	mirror = t.TrueMirror()
	if mirror:
	    if mirror not in list:
	        connectedTrades = acm.FTrade.Select('connectedTrdnbr = %s' % mirror.ConnectedTrade().Oid())
	        for connectedTrade in connectedTrades:
	            if connectedTrade not in list:
	                list.append(connectedTrade)

	if t.GroupTrdnbr():
	    result = acm.FTrade.Select('groupTrdnbr = %s' % t.GroupTrdnbr().Oid())
	    for item in result:
	        if item not in list:
	            list.append(item)

        ambTrade.mbf_add_int("CONSTELLATION_COUNT", len(list))

        #check term account backdate
        try:
            if t.Instrument().InsType() == 'Deposit' and to_datetime(t.CreateTime()).date() == datetime.datetime.now().date() and datetime.datetime.strptime(t.ExecutionTime(), "%Y-%m-%d %H:%M:%S").date() > datetime.datetime.strptime(t.Instrument().StartDate(), "%Y-%m-%d").date():
                trade_obj.mbf_add_string("BACKDATE_START", '%s 00:00:00' % t.Instrument().StartDate())
        except Exception, err:
            print 'Failed check term backdate with error (%s)' % err

    except Exception, e:
        print 'ERROR on selection constellation count : %s' % str(e)

    return msg, s

'''----------------------------------------------------------------------------------------------------------
MODULE                  :       FC_AMBA_INS_HOOK
PROJECT                 :       FX onto Front Arena
PURPOSE                 :       This module will remove all the LEG AMB objects from an incoming instrument 
                                AMBA message
DEPARTMENT AND DESK     :       All Departments and all Desks.
REQUASTER               :       FX onto Front Arena Project
DEVELOPER               :       Heinrich Cronje
CR NUMBER               :       XXXXXX
----------------------------------------------------------------------------------------------------------'''
from datetime import datetime
import acm
'''----------------------------------------------------------------------------------------------------------
Import custom modules
----------------------------------------------------------------------------------------------------------'''
from AMBA_Helper_Functions import AMBA_Helper_Functions as AMBA_Utils

'''----------------------------------------------------------------------------------------------------------
Input Parameters
----------------------------------------------------------------------------------------------------------'''
AMBA_Objects_To_Remove = ['LEG', 'COMBINATIONLINK', 'CREDITEVENTSPEC', 'EXERCISEEVENT', 'EXOTICEVENT', 'DIVIDEND', \
                        'MONEYMARKETDECOMP']

'''----------------------------------------------------------------------------------------------------------
Class containing static methods to be applied on incoming AMBA messages
----------------------------------------------------------------------------------------------------------'''
class FC_AMBA_INS_HOOK(object):
    @staticmethod
    def remove_SPECIFIC_Object(instrument_obj, prefix, objectName):
        for obj in AMBA_Utils.objects_by_name(instrument_obj, prefix, objectName):
            instrument_obj.mbf_remove_object()
    @staticmethod
    def stringTodate(datestr,format="%Y-%m-%d"):
        return datetime.strptime(datestr, format).date()

def AddBackDateStart(instrument_obj):
    legsobects = AMBA_Utils.object_by_name(instrument_obj, ['+', '!', ''], 'LEG')
    if legsobects is not None:
        backDateTypes = ['Call Fixed Rate Adjustable', 'Fixed Rate Adjustable']
        cashflowsObjects = AMBA_Utils.objects_by_name(legsobects, ['+', '!', ''], 'CASHFLOW')
        if cashflowsObjects is not None:
            for cashflowsObject in cashflowsObjects:
                startDayObj = cashflowsObject.mbf_find_object("START_DAY", "MBFE_BEGINNING")
                payDayObj = cashflowsObject.mbf_find_object("PAY_DAY", "MBFE_BEGINNING")
                typeObj = cashflowsObject.mbf_find_object("TYPE", "MBFE_BEGINNING")
                cashflownbrObj = cashflowsObject.mbf_find_object("CFWNBR", "MBFE_BEGINNING")
                if startDayObj is not None and payDayObj is not None and typeObj is not None and cashflownbrObj is not None:
                    startDayObjVal = FC_AMBA_INS_HOOK.stringTodate(startDayObj.mbf_get_value())
                    payDayObjVal = FC_AMBA_INS_HOOK.stringTodate(payDayObj.mbf_get_value())
                    typeObjVal = typeObj.mbf_get_value()
                    createDate = FC_AMBA_INS_HOOK.stringTodate(acm.Time.DateTimeFromTime(acm.FCashFlow[cashflownbrObj.mbf_get_value()].CreateTime())[:10])
                    updatedateDate = FC_AMBA_INS_HOOK.stringTodate(acm.Time.DateTimeFromTime(acm.FCashFlow[cashflownbrObj.mbf_get_value()].UpdateTime())[:10])
                    if (createDate == datetime.now().date() or updatedateDate == datetime.now().date()) and startDayObjVal < payDayObjVal and datetime.now().date() <= payDayObjVal and startDayObjVal <= datetime.now().date() and typeObjVal in backDateTypes:
                        print 'DEBUG POSSIBLE BACK DATE', cashflowsObject.mbf_object_to_string()
                        instrument_obj.mbf_add_string("BACKDATE_START", '%s 00:00:00' % startDayObjVal)
                        break
        
def FC_AMBA_Ins_Hook_Modify_Sender(msg, s):
    msgType = AMBA_Utils.get_object_type(msg)
    if not (msgType == 'INSTRUMENT'):
        return None
    
    msgEventType = AMBA_Utils.get_AMBA_Object_Value(msg, 'TYPE')
    if (not msgEventType) or (msgEventType == 'INSERT_INSTRUMENT'):
        return None
    
    instrument_obj = AMBA_Utils.object_by_name(msg, ['+', '!', ''], msgType)
    if not object:
        return None
    #print instrument_obj.mbf_object_to_string()
    try:
        AddBackDateStart(instrument_obj)
    except Exception, e:
        print 'FAILED %s' % str(e), '*'*50
    for AMBA_Object_To_Remove in AMBA_Objects_To_Remove:
        try:
            FC_AMBA_INS_HOOK.remove_SPECIFIC_Object(instrument_obj, ['+', '!', '', '-'], AMBA_Object_To_Remove)
        except Exception, e:
            print 'ERROR on removing AMBA Object %s: %s' %(AMBA_Object_To_Remove, str(e))

    return (msg, s)

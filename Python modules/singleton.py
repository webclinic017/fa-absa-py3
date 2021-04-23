"""
----------------------------------------------------------------------------------------------
MODULE
    Singleton

DESCRIPTION
    Date                : 02/12/2016
    Purpose             : Implementation of singleton functionality for ATS OPS start ups.
    Department and Desk : Back Office
    Requester           : Anwar Banoo
    Developer           : Mighty Mkansi
    CR Number           : CHNG0004142324
HISTORY
==============================================================================================
Date           CR number        Developer       Description
----------------------------------------------------------------------------------------------
02/12/2016     CHNG0004142324   Mighty Mkansi   Implementation of singleton functionality for 
                                                ATS OPS start ups.
----------------------------------------------------------------------------------------------
"""

import acm
import os
import inspect


try:
    import FOperationsUtils as Utils
except Exception, error:
    print("Failed to import FOperationsUtils, "  + str(error))

machineName = os.environ['COMPUTERNAME']

userName = acm.UserName()

TEXTOBJ_SING_ID = 'ATS_SINGLETON_%s' %userName

def trap_process_details():    
        
    modName = None
    try:
        frm = inspect.stack()[len(inspect.stack()) - 1]
        mod = inspect.getmodule(frm[0])
        modName = mod.__name__
        
    except Exception, e:
        print(e)        
    machineName = os.environ['COMPUTERNAME']
    pid = os.getpid()
    return machineName, pid, modName

def lock_singleton():
    machineName, pid, modName = trap_process_details()
    sing_id = '{"machine":"%s","pid":%d,"module":"%s", "user":"%s"}' %(machineName, pid, modName, userName)
    #print sing_id
   
    textobj = acm.FCustomTextObject[TEXTOBJ_SING_ID]
    if not textobj:
        Utils.LogVerbose("Creating Singleton instance '%s:%s'" %(TEXTOBJ_SING_ID, sing_id))
        textobj = acm.FCustomTextObject()
        textobj.Name(TEXTOBJ_SING_ID)
        textobj.Text(sing_id)
        textobj.Commit()

def unlock_singleton():
    textobj = acm.FCustomTextObject[TEXTOBJ_SING_ID]
    if not textobj:
        raise RuntimeError("Nonexisting singleton instance '%s'" %TEXTOBJ_SING_ID)
    Utils.LogVerbose("Deleting Singleton instance '%s:%s'" %(TEXTOBJ_SING_ID, textobj.Text()))
    textobj.Delete()
    print('Singleton Deleted')



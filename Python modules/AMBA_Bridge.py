'''---------------------------------------------------------------------------------
     MODULE
        AMBA_Bridge - Hook in AMBA to modify passing messages.
         
        (c) Copyright 2007 by SunGard FrontArena. All rights reserved.
     
     DESCRIPTION    
     
            This module is part of the AMBA Bridge project. It is intended as
            a wrapper for FAMBA_Bridge.
            
            For the AMBA Bridge project, enter in AMBA configuration:
                
              If on source_system:
                ael_module_name = AMBA_Bridge 
                ael_sender_modify = sender_modify
            
    
              If on destination_system    
                ael_module_name = AMBA_Bridge
                ael_receiver_modify = receiver_modify
                           
            
            The receiver_modify/sender_modify functions in FAMBA_Bridge contains 
            the main part of the logic. However, if any exceptions are raised in 
            the FAMBA_Bridge code, they are caught and handled here.
    
        
        NOTE: In sys.path.append below you need to write the path to 
        FAMBA_Bridge.py, which is stored outside Prime.  
     
---------------------------------------------------------------------------------'''

import time

debugOutput = False  #convenience
performanceTest = False # controls message output while dealing with messages
    
def dprint(msg):
    global debugOutput
    if debugOutput:
        print "@ ", msg 

####### get the performance time of the AMBA Bridge ##########

perfTime = time.clock() 
def performanceTick():
    global perfTime
    perfTime = time.clock()
def performanceTock():
    delta = time.clock() - perfTime
    print "@ Message Processed in ", delta, " sec"

##############################################################

# should be set to pass in production environments
def dreload():
    global debugOutput
    if debugOutput:
            #for checking a bit (not yet doing anything major)
            import inspect
            print "Stack size ", len(inspect.stack()), "limit", sys.getrecursionlimit(), "avail",
            print sys.getrecursionlimit() - len(inspect.stack())
            #will destroy other items
            #reload(FAMBA_Bridge) # if running debug
            FAMBA_Bridge.isInDebugMode = True
            dprint(FAMBA_Bridge.dReply())

# for cmake
__version__ = '1.15.7'
    
import ael
import sys
import traceback


#
#Removed for remote testing
#

sys.path.append('D:\\clearcase\\view2\\base\\bec\\AMBAbridge\\src')
# macro that is replaced when installing using the ambab script
# with the script directory
#sys.path.append('MACROCURRENTDIRECTORYMACRO')

try:
        import AMBA_Bridge_pref
        if AMBA_Bridge_pref.measurePerformance:
                performanceTest = True
                print "Measuring performance"
        else:
                print "Not logging performance"
        if AMBA_Bridge_pref.isInDebugMode:
                debugOutput = True
except:
        pass

try:
    import testmarker
    debugOutput = True
except:
    pass

dprint("Loading module!")
try:
    import FAMBA_Bridge
    if debugOutput:
        FAMBA_Bridge.isInDebugMode = True
        dprint("debug set in the FAMBA_Bridge!!")
except:
    dprint("Error while loading FAMBA_Bridge")
    traceback.print_exc()
    raise ("Error while loading FAMBA_Bridge")

# should not be present in the product server ?
# because this will be executed every time a message runs
dprint(FAMBA_Bridge.dReply()) 
dprint("Exiting load")
    
VERSION = '1.15.7'

def dispLastError(X=None):
    """Alternative and better error tracking"""
    print "=-"*30
    print "Stack Trace"
    print "=-"*30    
    #fetch error
    o = sys.exc_info()[2]
    p = o
    i = 0
    while p:
        fname = p.tb_frame.f_code.co_filename
        funn  = p.tb_frame.f_code.co_name
        print "%5s File (%s) Fun (%s) Line (%s) Where (%s) " % (i, fname, funn, p.tb_lineno, p.tb_lasti)
        p = p.tb_next
        i = i +1
    print "=-"*15
    print "Last object state as seen in AMBA Bridge"
    print "=-"*15
    try:
        print X.mbf_object_to_string()
    except Exception, e:
        print "object could not be converted to string"
    print "=-"*15
    print "End of stack Trace"
    print "=-"*30


##############################################################
#Forward direction, old -> new
##############################################################



def receiver_modify(m):
        """ Entry point for receiver hook function. Changes the message to fit the 
            structure in the receiving system. """
        try:
            performanceTick()
            dreload()
            m = FAMBA_Bridge.receiver_modify(m)
            performanceTock()
        except Exception, e:
            """Catch exception in FAMBA_Bridge. """
            print "=-"*15
            print e
            dispLastError(m)
            return None
        
        return m
    
# Note the default value is to make it easy to use this with amba from console    
def sender_modify(m, s="DebugThisModule"):
        """ Entry point for sender hook function. Changes the settlement
            fields of a trade message if necessary. """
        try:
            performanceTick()
            dreload()
            res = FAMBA_Bridge.sender_modify(m, s)
            performanceTock()
            if res != None:
                m, s = res
            else:
                # silently ignore the message to avoid filling the MB and AMB 
                # with data
                #print "Silent remove of message!! (remove this message outside testing)"
                return None
        except Exception, e:
            """ Catch exception in FAMBA_Bridge. """
            m = None
            s = None
            print "=-"*15
            print e
            dispLastError(m)
        
        if s == "DebugThisModule":
            return m
        else:
            return (m, s)


##############################################################
#Backward direction, new -> old
##############################################################
    
def reverse_receiver_modify(m):
        """ Entry point for receiver hook function. Changes the message to fit the 
            structure in the receiving system. """
        try:
            performanceTick()
            dreload()
            m = FAMBA_Bridge.reverse_receiver_modify(m)
            performanceTock()
        except Exception, e:
            """Catch exception in FAMBA_Bridge. """
            print e
            dispLastError(m)
            return None
        
        return m
    
# Note the default value is to make it easy to use this with amba from console    
def reverse_sender_modify(m, s="DebugThisModule"):
        """ Entry point for sender hook function. Changes the settlement
            fields of a trade message if necessary. """
        try:
            performanceTick()
            dreload()
            res = FAMBA_Bridge.reverse_sender_modify(m, s)
            performanceTock()
            if res != None:
                m, s = res
            else:
                # silently ignore the message to avoid filling the MB and AMB 
                # with data
                #print "Silent remove of message!! (remove this message outside testing)"
                return None
        except Exception, e:
            """ Catch exception in FAMBA_Bridge. """
            print e
            dispLastError(m)
            return None
        
        if s == "DebugThisModule":
            return m
        else:
            return (m, s)

    
    
def amba_bridge_validate_entity_dest(e, op):
        """ Prohibits dangerous changes in the receiving system. """
        return FAMBA_Bridge.amba_bridge_validate_entity_dest(e, op)
    
def amba_bridge_validate_entity_source(e, op):
        """ Prohibits dangerous changes in the sending system. """
        return FAMBA_Bridge.amba_bridge_validate_entity_source(e, op)


#=========================================================================
#
#Test functions
#
#=========================================================================

#
#a lot like the other function
#
def update2insert_sender(e,op="debug"):
    """  Convert an update to an insert and run  """
    dreload()
    try: 
        ex = FAMBA_Bridge.update2insert_sender(e)        
    except Exception, er:
        print "Error ", er
        print "|"*60
        traceback.print_exc()
        print "|"*60
        ex = e
    return sender_modify(ex, op)


def rev_upd2ins_sender(e,op="debug"):
    """  Convert an update to an insert and run  """
    dreload()
    try: 
        ex = FAMBA_Bridge.update2insert_sender(e)        
    except Exception, er:
        print "Error ", er
        print "|"*60
        traceback.print_exc()
        print "|"*60
        ex = e
    return reverse_sender_modify(ex, op)


def update2delete_sender(e,op="debug"):
    """  Convert an update to a delete and run  """
    dreload()
    try: 
        ex = FAMBA_Bridge.update2delete_sender(e)        
    except Exception, er:
        print "Error ", er
        print "|"*60
        traceback.print_exc()
        print "|"*60
        ex = e
    return sender_modify(ex, op)

    
    
    




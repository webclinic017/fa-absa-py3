from __future__ import print_function
import time
import sys
import acm
import FVaRUserDefinedData

def introspect_callers_caller_info():
    if FVaRUserDefinedData.LOG_FUNCTION_NAME:
        try:
            fcode = sys._getframe(2).f_code
            return fcode.co_filename + "." + fcode.co_name
        except:
            return None
    else:
        return None

def calculate_stack_depth(frame):
    depth = 0
    try:
        break_cond = False
        b = frame
        while not break_cond:
            b_temp = b.f_back
            if b_temp:
                b = b_temp
                depth += 1
            else:
                break_cond = True
    except Exception as msg:
        pass
    return depth

def format_log_prefix(call_info):
    pref = []
    if FVaRUserDefinedData.INDENT_LOG_MESSAGES:
        frame = sys._getframe(2)
        depth = calculate_stack_depth(frame)
        pref.append("  "*depth)        
    if call_info:
        pref.append(call_info)
        pref.append(": ")
    return "".join(pref)
    
def log_trace(log_msg):
    """
    Log function for very detailed trace logging of
    values during calculations.
    """
    if FVaRUserDefinedData.LOG_TRACE:
        hd = format_log_prefix(introspect_callers_caller_info())
        acm.Log("FVaR TRACE:"+ hd + log_msg)

def log_trace_object(log_msg, object):
    """
    Similar to the one above, but logs the message  plus
    the String-representation of an FObject.
    """
    if FVaRUserDefinedData.LOG_TRACE:
        log_trace(log_msg + " " + object.AsString())
    
def log_debug(log_msg):
    """
    Log function for detailed functional logging of
    the processing stages.
    """
    if FVaRUserDefinedData.LOG_DEBUG:
        frame = sys._getframe(1)
        hd = format_log_prefix(introspect_callers_caller_info())
        acm.Log("FVaR DEBUG:"+ hd + log_msg)

def log_error(log_msg):
    """
    Log function for error logging, used in conjuction
    with exception handling.
    """
    acm.Log("FVaR ERROR: %s" % log_msg)

ENABLE_LOGGING = False
LOG_FUNCTION_ARGUMENTS = True
LOG_PERF_METRICS = True
DO_GC_COLLECT = True

def print_perf_metrics(func_name, del_time, del_gc_free_bytes,
        del_gc_heap_size, del_vm_size):
    print ("PERFORMANCE LOG (%s)" % func_name)
    print ("\tWall time delta: %s" % del_time)
    print ("\tGC Free bytes delta: %s" % del_gc_free_bytes)
    print ("\tGC heap size delta: %s" % del_gc_heap_size)
    print ("\tVM size delta: %s" % del_vm_size)
    print ()

def short_name(ent):
    try:
        sname = ent.StringKey()
    except:
        return str(ent)
    return sname

def acm_perf_log(func):
    """
    This decorator dumps out the arguments passed to a function before calling it
    and also log som performance numbers
    """
    if not ENABLE_LOGGING:
        return func
    argnames = func.func_code.co_varnames[:func.func_code.co_argcount]
    fname = func.func_name
    modname = func.__module__
    fullname = modname+"."+fname
    def echo_func(*args,**kwargs):
        if LOG_FUNCTION_ARGUMENTS:
            print ("ARGUMENT DUMP (%s)" % fullname)
            for (argname, argval) in list(zip(argnames,args)) + kwargs.items():
                print ("\t%s=%r" % (argname, short_name(argval)))

        if LOG_PERF_METRICS:
            if DO_GC_COLLECT:
                acm.Memory().GcWorldStoppedCollect()
            base_time = time.clock()
            base_gc_free_bytes = acm.Memory().GcNumberOfFreeBytes()
            base_gc_heap_size  = acm.Memory().GcHeapSize()
            base_vm_size = acm.Memory().VirtualMemorySize()
            
        # do the actual function call
        res = func(*args, **kwargs)
        if LOG_PERF_METRICS:
            del_time = time.clock() - base_time
            
            # collect
            if DO_GC_COLLECT:
                acm.Memory().GcWorldStoppedCollect()
            del_gc_free_bytes = acm.Memory().GcNumberOfFreeBytes() - \
                                base_gc_free_bytes
            del_gc_heap_size = acm.Memory().GcHeapSize() - base_gc_heap_size
            del_vm_size = acm.Memory().VirtualMemorySize() - base_vm_size

            print_perf_metrics(fullname, del_time, del_gc_free_bytes,
                               del_gc_heap_size, del_vm_size)
        return res
    return echo_func

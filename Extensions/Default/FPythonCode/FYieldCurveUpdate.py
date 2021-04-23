from __future__ import print_function
"""----------------------------------------------------------------------------
MODULE
    FYieldCurveUpdate - Module which updates YieldCurves.

    (c) Copyright 2011 by SunGard FRONT ARENA. All rights reserved.

DESCRIPTION
    This is a module which automatically updates YieldCurves. It is to be 
    started from the Arena Task Server, ATS.

    ats -server teststo04:9013 -user my_user -module_name FYieldCurveUpdate -command_port 4711

    Stopped by the following command:
    ats_monitor 127.0.0.1:4711 -monitor shutdown

    The ATS can be monitored by the following command

    ats_monitor 127.0.0.1:4711 -monitor module_status


    The update intervals for each yield curve will be taken from the 
    update_interval column in the yield curve table.
    
    To change the yield curves which this script updates, update 
    FYieldCurveUpdateVariables.


    Parameters:
    
    yield_curves        list with the names of the yield curves which should 
                        be updated
    
                    

----------------------------------------------------------------------------"""


import acm
import time
import FYieldCurveUpdateVariables

# ################ #
# Global Variables #
# ################ #

# Yield Curve type to update, no yield curve types should be added to this list,
# but it is alright to remove yield curve types
save_type = ['BenchmarkCurve', 'BenchmarkSpreadCurve', 'InstrumentSpreadCurve', 'InstrumentSpreadCurveBidAsk', 'SpreadCurve']

epsilon = FYieldCurveUpdateVariables.epsilon
epsilon2 = FYieldCurveUpdateVariables.epsilon2

# price_type, if instrument spread curves should be updated with price type market or theor
# 0  = theor, 1 = market
price_type = 0 

yc_main_list = []
work_counter = 0


class My_list:
    def __init__(self):
        self.list = []
        
    #only append curves which can be updated, and no duplicates   
    def my_append(self, new_yc):
        if new_yc.Category() in save_type:
            for yc in self.list:
                if yc == new_yc:
                    return
            self.list.append(new_yc)
        return
        
    def my_list(self):
        return self.list
        
    def prt(self):
        for l in self.list:
            print (l.Name())

class YCholder:    
    def __init__(self, yc, update_time = 0):
        if update_time:
            self.update_time = update_time
        else:
            self.update_time = yc.UpdateTime()
        self.last_update = time.time()
        self.yc = yc
        self.yc_list = self.create_yc_list(yc)
    def prt(self):
        print (20*'*')
        print (self.yc.Name())
        print (self.update_time)
        self.yc_list.prt()
    def create_yc_list(self, top_yc):
        my_list = My_list()
        yc_down(top_yc, my_list)
        my_list.my_append(top_yc)
        return my_list
    def list(self):
        return self.yc_list.my_list()
    def set_last_update(self):
        self.last_update = time.time()
    def get_last_update(self):
        return self.last_update        
    def get_yc_name(self):
        return self.yc.Name()
        
# ############################################# #
# Functions to find all underlying yield curves
# ############################################# #       
        
def yc_attribute_spread(yc, list):
    str = "curve = %s" % (yc.StorageId())
    attrs = acm.FYCAttribute.Select(str)
    for a in attrs:
        yc2 = a.UnderlyingCurve()
        if yc2:
            yc_down(yc2, list)
            list.my_append(yc2)
    # also add the base curve
    if yc.UnderlyingCurve():
        yc2 = yc.UnderlyingCurve()
        yc_down(yc2, list)
        list.my_append(yc2)
    return
    
# Create a list with all underlying yc, base first and top last, no duplicates.
def yc_down(yc, list):
    if not yc:
        return
    if yc.Category()=='InstrumentSpreadCurve' or yc.Category()=='InstrumentSpreadCurveBidAsk':
        for yis in yc.InstrumentSpreads():
            used_yc = None
            und_yc   = yis.UnderlyingYieldCurve()
            und_ins1 = yis.Benchmark()
            und_ins2 = yis.Benchmark2()
            if und_yc:
                yc_down(und_yc, list)
                list.my_append(und_yc)
                continue
            elif und_ins1:
                used_acm_yc = und_ins1.MappedDiscountCurve().Parameter()
                if len(used_acm_yc.Name())>0:
                    used_yc = acm.FYieldCurve[used_acm_yc.Name()]
            elif und_ins2:
                used_acm_yc = und_ins2.MappedDiscountCurve().Parameter()
                if len(used_acm_yc.Name())>0:
                    used_yc = acm.FYieldCurve[used_acm_yc.Name()]
            if used_yc:
                yc_down(used_yc, list)
                list.my_append(used_yc)
    
    elif yc.Category()=='BenchmarkSpreadCurve' or yc.Category()=='SpreadCurve':
        yc_down(yc.NextCurve(), list)
        list.my_append(yc)
    elif yc.Category() == 'BenchmarkCurve':
        pass
    elif yc.Category() == 'AttributeSpreadCurve':
            yc_attribute_spread(yc, list)
        
    return 

# get a list of yield curves from the global variable yield_curves
def get_yc_list():
    yield_curves = FYieldCurveUpdateVariables.yield_curves
    yc_list = []

    if not yield_curves:
        print ("You have not specified the yield curves which are to be updated.")
        print ("Add the variable update_yield_curves to the module")
        print ("FYieldCurveUpdateVariables.")
        print ("Example: yield_curves = ['EUR-SWAP', 'EUR-IS-2','ALL-SWAP']")
        return
    for str in yield_curves:
        yc = acm.FYieldCurve[str]
        if yc == None:
            print ("NO YieldCurve with name %s" % (str))
            continue
        yc_list.append(yc)
        
    return yc_list

# ################################ #
# Functions to update yield curves #
# ################################ #

def yc_update_is(yc):
    global epsilon
    global price_type
    updated = 0
    ycc = yc.Clone()

    print (ycc.Name())
    for yis in ycc.InstrumentSpreads():
        ins = yis.Instrument()
        spread = ins.CurrentSpread(price_type)

        if abs(yis.Spread() - spread) > epsilon:
            yis.Spread(spread)
            updated = 1
        
    if updated:
        try:
            yc.Apply(ycc)
            yc.Commit()
        except:
            str = "Could not update %s" % (yc.Name())
            acm.Log(str)
            return 0
    return 1

def yc_update(ych):
    for yc in ych.list():
        if yc.Category() in ('BenchmarkCurve', 'BenchmarkSpreadCurve', 'SpreadCurve'):
            try:
                ycc = yc.Clone()
                ycc.Calculate()
                yc.Apply(ycc)
                yc.Commit()
 
            except:
                str = "Could not update %s" % (yc.Name())
                acm.Log(str)
                continue
        else: # instrument spread
            if yc_update_is(yc) == 0:
                continue
        ych.set_last_update()
        
    return
    
# ##### #
# START #
# ##### #

def start():
    global yc_list
    global yc_main_list
    
    yc_main_list = []
    
    yc_list = get_yc_list()
    
    for yc in yc_list:
        ych = YCholder(yc)
        yc_main_list.append(ych)
        
    str = "FYieldCurveUpdate started %s" % (time.ctime())
    acm.Log(str)
    print ("Updating the following YieldCurves:")
    for ych in yc_main_list:
        ych.prt()
    
    return

# #### #
# STOP #
# #### #
def stop():
    str = "FYieldCurveUpdate stopped %s" % (time.ctime())
    ael.log(str)
    return

# ###### #
# STATUS #
# ###### #
def status():
    global yc_main_list
    str = ''
    for ych in yc_main_list:
        str = str+"Updated "+ych.get_yc_name()+" "+time.ctime(ych.get_last_update())+'\n'
    
    return str
    
# ###### #
# WORK   #
# ###### #
def work():
    global work_counter
        
    work_counter = work_counter + 1
    if work_counter > 10:
        work_counter = 0
        for ych in yc_main_list:
            if ych.last_update < time.time() - ych.update_time:
                yc_update(ych)
    return

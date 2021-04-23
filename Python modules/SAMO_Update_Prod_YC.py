'''
Purpose: [Scheduled to run each night and update the yield curve additional info, Prod_YC.  
         Prod_YC is a boolean value and specifies whether a yield curve or its parent 
         is mapped in ACMB Global.],
         [Updated to populate additional Info for benchmark Instruments],
         [Updated to include contect link parameters of type Repo.]
Department and Desk: PCG
Requester: Dirk Strauss
Developer: Paul Jacot-Guillarmod, Ickin Vural, Willie van der Bank
CR Number:  [207116 (updated 2010-01-22, originally written during the upgrade, Nov 2009)],[C000000487640],[C705221, 07/07/2011]

'''

import ael

binsl = []

def set_addinfo(entity, ai_name, ai_value):
    # Sets an additional info field for a given entity
    ent_clone = entity.clone()
    
    # Clone the additional info entity if it exists, otherwise create a new additional info
    for ai in entity.additional_infos():
        if ai.addinf_specnbr.field_name == ai_name:
            new_ai = ai.clone()
            break
    else:
        new_ai = ael.AdditionalInfo.new(ent_clone)
        new_ai.addinf_specnbr = ael.AdditionalInfoSpec[ai_name]
    
    new_ai.value = str(ai_value)
    try:
        new_ai.commit()
        ent_clone.commit()
    except:
        print entity.insid
        print 'Error: Could not update additional info value %s' %(ai_name)

def get_addinfo(entity, ai_name):
    # Return the value of an additional info field for a given entity
    val = None
    for ai in entity.additional_infos():
        if ai.addinf_specnbr.field_name == ai_name:
            val = ai.value
            break
    return val

def return_underlying_yc(yc):
    # Recursively extract all the underlying yield curves for a given yield curve
    yc_list = set([])
    
    if yc.underlying_yield_curve_seqnbr:
        yc_list.add(yc)
        temp = return_underlying_yc(yc.underlying_yield_curve_seqnbr)
        for y in temp:
            yc_list.add(y)
    else:
        yc_list.add(yc)
    return yc_list

def get_acmb_yc():
    # generate a set of yield curves in ACMB global or whos parent is in ACMB global
    acmb_yc = set([])

    for l in ael.Context['ACMB Global'].links():
        #if l.type == 'Yield Curve':
        if l.type in ('Yield Curve', 'Repo'):    #Updated by WvdB
            try:
                temp = return_underlying_yc(ael.YieldCurve[l.name])
                for y in temp:
                    acmb_yc.add(y.yield_curve_name)
            except:
                print l.name
    return acmb_yc

def set_yield_curve_addinfo():
    # throw away code
    acmb_yc = get_acmb_yc()

    for yc in ael.YieldCurve:
        if yc.yield_curve_name in acmb_yc:
            set_addinfo(yc, 'Prod_YC', 'Yes')
        else:
            set_addinfo(yc, 'Prod_YC', 'No')
            
def update_benchmark_ins():
    
    for yc in ael.YieldCurve:
        for bi in yc.benchmarks(): 
            if (get_addinfo(yc, 'Prod_YC') == 'Yes'):
                set_addinfo(bi.instrument, 'Prod_Benchmark_Ins', 'Yes')
                if (bi.instrument) not in binsl:
                    binsl.append(bi.instrument)
             

def set_to_No():

    for yc in ael.YieldCurve:
        for bi in yc.benchmarks():
            if (get_addinfo(yc, 'Prod_YC') == 'No'):
                if (bi.instrument) not in binsl:
                    print get_addinfo(bi.instrument, 'Prod_Benchmark_Ins'), 'set to No'
                    set_addinfo(bi.instrument, 'Prod_Benchmark_Ins', 'No') 
                    
def update_yield_curve_addinfo():
    ''' Scheduled to run each night and update the yield curve additional info, Prod_YC.  
        Prod_YC is a boolean value and specifies whether a yield curve or its parent 
        is mapped in ACMB Global.
    '''
    
    acmb_yc = get_acmb_yc()        
    
    for yc in ael.YieldCurve:
        if (yc.yield_curve_name in acmb_yc) and (get_addinfo(yc, 'Prod_YC') != 'Yes'):
            set_addinfo(yc, 'Prod_YC', 'Yes')
        elif (yc.yield_curve_name not in acmb_yc) and (get_addinfo(yc, 'Prod_YC') != 'No'):
            set_addinfo(yc, 'Prod_YC', 'No')
           
update_yield_curve_addinfo()

ael.poll()

update_benchmark_ins()

ael.poll()

set_to_No()

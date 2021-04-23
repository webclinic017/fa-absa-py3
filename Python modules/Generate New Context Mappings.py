# once off script to create context mappings when upgrading to 2013.3
# coded by Anil

import acm

ael_variables = []

def ael_main(dict):

    curr_list = []


    context = acm.FContext['ACMB Global'].ContextLinks()

    for cl in context:
        if cl.Instrument():
            if cl.Instrument().InsType()=='Curr':
                
                if cl.Instrument().Name()==cl.Currency().Name():
                    if cl.Instrument().Name() not in ['USD', 'BWP', 'KES', 'MXN', 'ZMK']:
                    #the repo curves of 'BWP','KES','MXN' and 'ZMK' are different from the usd/curr basis curves - dont use repo curves
                    
                        if cl.Type()=='Repo':
                            
                            curr_list.append((cl.Instrument().Name(), cl.Name()))
                        
                if cl.Instrument().Name()=='USD':
                    if cl.Type() =='Yield Curve':
                        if cl.Currency().Name() not in ['USD']:
                            curr_list.append((cl.Currency().Name(), cl.Name()))
                


    ins_curve_set = set(curr_list)

    new_context_links = list(ins_curve_set)

    new_context_links.sort()
    
    for c in new_context_links:

        print acm.FCurrency[c[0]].Name(), acm.FYieldCurve[c[1]].Name()
    
    
    for cls in new_context_links:
        
        
        ins = acm.FCurrency[cls[0]]
        yc = acm.FYieldCurve[cls[1]]
        
        dt = acm.FChoiceList.Select01("list = 'DiscType' and name ='CCYBasis'", None)
        
        con_list = ['ACMB Global']
        
        for con in con_list:
            
        
            
            con = acm.FContext[con]
            cl = acm.FContextLink()

            cl.Instrument(ins)
            cl.Currency(ins)
            cl.DiscountingType(dt)
            cl.MappingType('Instrument')
            cl.Name(yc)
            cl.Type('Yield Curve')
            cl.Context(con)

            try:
                cl.Commit()
                acm.Log('cl commited for %s for the context %s' %(cls[1], con.Name()))
            except:
                acm.Log('could NOT commit cl for %s' %(cls[1], con.Name()))
            
                
    

    




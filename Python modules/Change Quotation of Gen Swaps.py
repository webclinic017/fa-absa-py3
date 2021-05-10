import acm

ael_variables = []

def ael_main(dict):
    
    swap_ccs = []
    gen = "generic = true"
    
    ccs = acm.FCurrencySwap.Select(gen)
    for cs in ccs:
        if cs.Quotation().Name()== 'Spread bps':
            swap_ccs.append(cs.Name())
            #print cs.Name(),cs.InsType(), cs.Quotation().Name()
            
    swaps = acm.FSwap.Select(gen)
    for s in swaps:
        if s.Quotation().Name()== 'Spread bps':
            swap_ccs.append(s.Name())
            #print s.Name(), s.InsType(),  s.Quotation().Name()
            
    
    
    for i in swap_ccs:
        ins = acm.FInstrument[i]
        
        
        q = acm.FQuotation['Spread percent']
        ins.Quotation(q)
        ins.Commit()
        
  
        
        
        
       


            



            
    
            
            
    

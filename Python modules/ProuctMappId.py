def ProdInsId(t,*rest):

    
    
    Ins1 = t.insaddr.insid
    Ins2 = t.curr.insid
    
    
    if Ins1 == 'XAU' or Ins2 == 'XAU':
    
        Output = 'XAU'
    else:
    
        Output = 'FX' + '/' + Ins1 + '/' + Ins2
    return Output
    
    
    
def ProdId(t,*rest):

    
    Ins1 = t.insaddr.insid
    Ins2 = t.curr.insid
    
    if Ins1 == 'XAU' or Ins2 == 'XAU':
    
        Output = '037588'
    else:
      
        Output = '0' + str(t.insaddr.insaddr)
    
    return Output
    
def ConvertProdId(i,*rest):
    
    P2 = str(i.insaddr)
      
    Output = P2
    return Output

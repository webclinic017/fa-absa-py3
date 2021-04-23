import ael, acm


def update_portfolio(tf, new_port,*rest):
    errors = []
    
    for trd in tf.trades():
        t_c = trd.clone()
        try:
            t_c.prfnbr = new_port
            t_c.commit()
        except:
            errors.append(trd)
         
    if len(errors) == 0:
        func=acm.GetFunction('msgBox', 3)
        func("SUCCESS", "All trade portfolios have been successful changed", 0)

def update_cp(tf, new_cp,*rest):
    errors = []
    
       
    for trd in tf.trades():
        t_c = trd.clone()
        try:
            t_c.counterparty_ptynbr = new_cp
            t_c.commit()
        except:
            errors.append(trd)
         
    if len(errors) == 0:
        func=acm.GetFunction('msgBox', 3)
        func("SUCCESS", "All trade counterparties have been successful changed", 0)        

def update_aq(tf, new_aq,*rest):
    errors = []
    
       
    for trd in tf.trades():
        t_c = trd.clone()
        try:
            t_c.acquirer_ptynbr = new_aq
            t_c.commit()
        except:
            errors.append(trd)
         
    if len(errors) == 0:
        func=acm.GetFunction('msgBox', 3)
        func("SUCCESS", "All trade aquirers have been successful changed", 0) 

                        
        
def CParty():
    cp = []
    cps = ael.Party#.select("type = Counterparty")
    for c in cps:
        cp.append(c.ptyid)
    cp.sort()
    return cp

def NewPortfolio():

    NewPortfolio=[]
    
    for p in ael.Portfolio:
        if p.compound == 0:
            NewPortfolio.append(p.prfid)
    NewPortfolio.sort()
    return NewPortfolio
    
def Aquirer():
    aq = []
    aqs = ael.Party.select("type = 'Intern Dept'")
    for c in aqs:
        aq.append(c.ptyid)
    aq.sort()
    return aq

    
def TrdFilter():

    TrdFilter=[]
    
    for t in ael.TradeFilter:
        TrdFilter.append(t.fltid)
    TrdFilter.sort()
    return TrdFilter

ael_variables = [ ('NewCP', 'New Counterparty: ', 'string', CParty(), ''),
                    ('NewAQ', 'New Aquirer: ', 'string', Aquirer(), ''),
                 ('NewPortfolio', 'New Portfolio: ', 'string', NewPortfolio(), ''),
                 ('TrdFilter', 'Trade Filter', 'string', TrdFilter(), '', 1)  
                 ]   

def ael_main(ael_dict):
    try:
        tf = ael.TradeFilter[(ael_dict["TrdFilter"])]
        print tf
        if ael_dict["NewPortfolio"]:
            try:
                new_port = ael.Portfolio[str(ael_dict["NewPortfolio"])].prfnbr
                update_portfolio(tf, new_port)
            except:
                print 'ERROR: Invalid Portfolio'
            
        if ael_dict["NewCP"]:
            try:
                new_cp = ael.Party[str(ael_dict["NewCP"])].ptynbr
                update_cp(tf, new_cp)
            except:
                print 'ERROR: Invalid Counterparty'    
                
        if ael_dict["NewAQ"]:
            try:
                new_aq = ael.Party[str(ael_dict["NewAQ"])].ptynbr
                update_aq(tf, new_aq)
            except:
                print 'ERROR: Invalid Acquirer'
                
    except:
        print 'ERROR: Invalid Trade Filter Name'
    
    
    



   

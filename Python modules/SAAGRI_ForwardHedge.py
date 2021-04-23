import ael

def Agri(temp,Filter,Port,TrdNbr,Cost,Server,*rest):
    
    Cost = (Cost/100)
    Blank=[]
    Global=[]
    AGRIdic={}
    InsList=[]
    DecInc=[-600, -400, -200, 0, 200, 400, 600]
    
    if Filter != '':
        
        Filt = ael.TradeFilter[Filter]
        
        for t in Filt.trades():
        
            ins = t.insaddr
            
            if ins.instype == 'Future/Forward' and ins.exp_day >= ael.date_today():
            
                if ins.insid not in InsList:
                    InsList.append(ins.insid)
                    
                if AGRIdic.has_key(ins.insid):            
                    value = int(AGRIdic[ins.insid])
                    AGRIdic[ins.insid] = value + (int(t.quantity)*int(ins.contr_size))
                    
                else:        
                    AGRIdic[ins.insid] = (int(t.quantity)*int(ins.contr_size))
                    
    elif Port != '':
        
        Prt = ael.Portfolio[Port]
        
        for t in Prt.trades():
        
            ins = t.insaddr
            
            if ins.instype == 'Future/Forward' and ins.exp_day >= ael.date_today():
            
                if ins.insid not in InsList:
                    InsList.append(ins.insid)
                    
                if AGRIdic.has_key(ins.insid):            
                    value = int(AGRIdic[ins.insid])
                    AGRIdic[ins.insid] = value + (int(t.quantity)*int(ins.contr_size))
                    
                else:        
                    AGRIdic[ins.insid] = (int(t.quantity)*int(ins.contr_size))
                
    elif TrdNbr != '':
    
        t = ael.Trade[TrdNbr]
      
        ins = t.insaddr
    
        if ins.instype == 'Future/Forward' and ins.exp_day >= ael.date_today():
        
            if ins.insid not in InsList:
                InsList.append(ins.insid)
                
            if AGRIdic.has_key(ins.insid):            
                value = int(AGRIdic[ins.insid])
                AGRIdic[ins.insid] = value + (int(t.quantity)*int(ins.contr_size))
                
            else:        
                AGRIdic[ins.insid] = (int(t.quantity)*int(ins.contr_size))
                
                
    for i in InsList:
        
        a = []          #Column Headers
        b = []
        
        inst = ael.Instrument[i]
        
        InsName = inst.insid
                
        UndInsName = inst.und_insaddr.insid
        ConTR = inst.contr_size         
        UndUsedPrice = inst.und_insaddr.used_price(ael.date_today(), inst.und_insaddr.curr.insid)
        ExpDay = inst.exp_day
        DaysToExpiry = ael.date_today().days_between(ExpDay)
        DaysToExpiryTemp = DaysToExpiry
        ConQuant = AGRIdic[i]
                
        a.append('InsName')
        b.append('')
        a.append('UndInsName')
        b.append('')
        a.append('ExpDate')
        b.append('')
        a.append('Quantity')
        b.append('')
        a.append('Price')
        b.append('')
        
        tellers = 0
        while DaysToExpiryTemp != 0:
            
            a.append(DaysToExpiryTemp)
            Hedge = ((ConQuant * Cost * (DaysToExpiryTemp+tellers))/365) * (1/ConTR)
            b.append(Hedge)
            DaysToExpiryTemp -= 1
            tellers += 1
        
        Global.append(a)
        Global.append(b)
            
        DaysToExpiryTemp = DaysToExpiry
        
        for i in DecInc:    
            TempList=[]
            TempList.append(InsName)              
            TempList.append(UndInsName)
            monthYear = ExpDay.to_string('%b%y')
            TempList.append(monthYear)
            TempList.append(ConQuant)  
            Price = UndUsedPrice + i
            TempList.append(Price)
            
            DaysToExpiryTemp = DaysToExpiry
            Hedge = ((ConQuant * Cost * DaysToExpiryTemp)/365) * (1/ConTR)
        
            while DaysToExpiryTemp != 0:
            
                #Hedge = ((ConQuant * Cost * DaysToExpiryTemp)/365) * (1/ConTR)
                #print Hedge
            
                Price = UndUsedPrice + i
                                
                Val = Price * ConQuant
                
                MargReg = Val - (UndUsedPrice * ConQuant)
                
                FundCostProf = (-1 * MargReg * Cost * DaysToExpiryTemp)/365
                
                MakeLoseOnHedge = (Price - UndUsedPrice)* Hedge * inst.contr_size
                
                LossProfit = MakeLoseOnHedge + FundCostProf
                TempList.append(LossProfit)
                
                DaysToExpiryTemp -= 1
                
            Global.append(TempList)
        
        Global.append(Blank)
                        
    outfile = Server + 'AGRIHedge.csv'
    
    report = open(outfile, 'w')
    
    for lsts in Global:
        
        for ls in lsts:
            
            report.write((str)(ls))
            report.write(',')
        report.write('\n')  
        
    report.close()
    
    print'Success'
    return 'The file has been saved at:' + Server + 'AGRIHedge.csv'
    
def Filter():
    Filter = []
    for p in ael.TradeFilter:
        Filter.append(p.fltid)
    Filter.sort()
    return Filter
    
def Port():
    Port = []
    for p in ael.Portfolio:
        Port.append(p.prfid)
    Port.sort()
    return Port
    
ael_variables = [('Filter', 'Filter', 'string', Filter(), '', 0),
                 ('Port', 'Portfolio', 'string', Port(), '', 0),
                 ('TrdNbr', 'TrdNbr', 'int', None, '', 0),
                 ('Cost', 'Cost', 'float', None, '', 1),
                 ('Server', 'Server', 'string', None, 'C:\\', 1)]   
                 
                
#main

def ael_main(ael_dict):

    Filter = ael_dict["Filter"]
    Port = ael_dict["Port"]
    TrdNbr = ael_dict["TrdNbr"]
    Cost = ael_dict["Cost"] 
    Server = ael_dict["Server"]
    print Agri(1, Filter, Port, TrdNbr, Cost, Server)
    
    
 
    


    
    
    

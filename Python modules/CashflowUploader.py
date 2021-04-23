import acm, ael
import time
import csv

from at_ael_variables import AelVariableHandler


ael_variables = AelVariableHandler()


ael_variables.add('inputFile',
    label='Input File',
    default=r'C:\temp\CashflowUploader.csv')
    

def getLegs(ins, legType):
    
    if len(ins.Legs()) == 1:
        return ins.Legs()[0]
    
    if ins.Legs()[0].PayLeg():
        pay = ins.Legs()[0]
        rec = ins.Legs()[1]
    else:
        pay = ins.Legs()[1]
        rec = ins.Legs()[0]
    
    if legType == 'Pay':
        return pay
    elif legType == 'Rec':
        return rec
    else:
        return None


def ael_main(config):
    
    sfile = config['inputFile']

    with open(sfile, 'rU') as csv_file:
        reader = csv.reader(csv_file)
        reader.next() 
        
        for line in reader:
                             
            insid = line[0]            
            legtype = line[1]
            cftype = line[2]
            startday = line[3]
            endday = line[4]
            payday = line[5]
            nominal = line[6].replace(',', '')
            rt = line[7]
                
            ins = acm.FInstrument[insid]
            
            if ins is not None:
                leg = getLegs(ins, legtype)
                contr_size = ins.ContractSize()
                leg_fact = leg.NominalFactor()                
                
                if cftype == '<CLEAR>':
                    
                    for cf in leg.CashFlows():
                        cf.Delete()
                    ins.Commit()                
                
                if cftype in ['Fixed Rate', 'Float Rate', 'Zero Coupon Fixed']:
                    startday = ael.date(startday)
                    endday = ael.date(endday)
                    payday = ael.date(payday)
                    nominal = float(nominal)
                    rt = float(rt) * 100.0
                    
                    if nominal <> 0.0:
                        cf = leg.CreateCashFlow()                                           
                        cf.CashFlowType = cftype
                        cf.StartDate = startday
                        cf.EndDate = endday
                        cf.PayDate = payday
                        cf.NominalFactor = nominal/(contr_size/leg_fact)
                        
                        if cftype in ['Fixed Rate', 'Zero Coupon Fixed']:
                            cf.FixedRate = rt
                        elif cftype in ['Float Rate']:
                            cf.Spread = rt
                            cf.FloatRateFactor = 1.0
                        else:
                            print('incorrect leg type')
                        cf.Commit()
                    
                elif cftype in ['Fixed Amount']:
                    payday = ael.date(payday)
                    nominal = float(nominal)
                    cf = leg.CreateCashFlow()                    
                    cf.CashFlowType = cftype
                    cf.PayDate = payday
                    cf.FixedAmount = nominal/(contr_size / leg_fact)
                    cf.NominalFactor = 1.0
                    cf.Commit()
                    
                else:
                    print('Unknown cashflow type', cftype)
    
    if  ins is not None:
        try:
            ins.Commit()
            '***** Cashflows uploaded succesfully *****'
        except Exception as e:
            print('Failed to commit instrument', e)
    
    
                
                        
                        
                        
                        

                    
            
                    
                
            

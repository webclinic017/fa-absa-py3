import acm
import ael
import sys

def UpdateValAndAccParam():
    valParameters=acm.FValuationParameters.Select('')
    for valParameter in valParameters:
        try:
            valParameter.ValuationClockInterval(1)
            valParameter.Commit()
            print("Clock Interval is set to Full Day for ValuationParameter ", valParameter.Name(), file=sys.stderr) 
        except:
            print("Can not set Clock Interval for ValuationParameter  ", valParameter.Name(), file=sys.stderr) 
        try:
            valParameter.FxBaseCurrency(acm.FCurrency['USD']) 
            valParameter.Commit()
            print("FX Base Currency set to USD for ValuationParameter ", valParameter.Name(), file=sys.stderr) 
        except:
            print("Can not set FX Base Currency for ValuationParameter  ", valParameter.Name(), file=sys.stderr) 
        try:
            valParameter.UseImmediateFxRates(True)
            valParameter.Commit()
            print("Present FX Rate for Display Curr Conversion set to True for ValuationParameter ", valParameter.Name(), file=sys.stderr) 
        except:
            print("Can not set Present FX Rate for Display Curr Conversion for ValuationParameter  ", valParameter.Name(), file=sys.stderr) 

            
    accParameters=acm.FAccountingParameters.Select('')
    for accParameter in accParameters:
         if ((accParameter.MatchMethod()== "FIFO")  or (accParameter.MatchMethod()== "LIFO")):
            try:
                accParameter.UseTaxLots(1)
                accParameter.Commit()
                print("Tax Lots is toggled for AccountingParameter ", accParameter.Name(), file=sys.stderr) 
            except:
                print("Can not toggle Tax Lots for AccountingParameter  ", accParameter.Name(), file=sys.stderr) 
    
    return 0
    
     
p = UpdateValAndAccParam()

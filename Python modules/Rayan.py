import acm
import OptionFunctions


options = acm.FOption.Select('')

for option in options:
    if option.ExpiryDate()>'2019-01-01':
        for trade in option.Trades():
            approxLoad = trade.AdditionalInfo().Approx_46_load()
            #print approxLoad
            #print type(approxLoad)
            if approxLoad is not None and approxLoad==True:
                continue
            acquirer = trade.Acquirer()
            
                
            baseType = OptionFunctions.GetExoticOptionBaseType(option)
            productType = option.ProductTypeChlItem()
            if productType is not None:
                productType = productType.Name()
            if acquirer and acquirer.Name() == "NLD DESK":
                print(str(trade.Oid())+','+str(trade.Type())+","+str(baseType) + ","+str(productType)+",")
    
            
        

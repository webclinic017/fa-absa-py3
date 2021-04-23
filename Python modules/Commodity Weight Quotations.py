import acm


qd={'Kilogram':1.0,
'Ounce':35.273962,
'Short Ton':0.001102,
'Pound':2.204623,
'Soybean Bushel':0.036744,
'Troy Ounce':32.150747,
'Wheat Bushel':0.036744,
'Metric Tonne':0.001,
'NAASAC LME Lot':0.02,
'AL Alloy LME Lot':0.02,
'Corn Bushel':0.039368,
'ICE GASOIL Liters':1.183432,
'LME LOT Normal':0.025,
'LME mini Lot':0.005,
'LME Nickel lot': 0.006,
'LME Tin Lot':0.005}



for sq in qd.keys():
    #print sq, qd[sq]
    
    
    
    try:
        q = acm.FQuotation()
        q.Name(sq)
        q.QuotationType('Weight')
        q.QuotationFactor(qd[sq])
        q.QuotationAddEnd(0)
        q.Clean(0)
        q.Commit()
        print(q.Name(), q.QuotationType(), q.QuotationFactor(), q.QuotationAddEnd(), q.Clean())
    except Exception, e:
        acm.Log(sq + ' this new quotation cannot be committed - %s' %(e.message))


        
        
    
    
    
    
    


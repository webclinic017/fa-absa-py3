import acm

# Once off script to ensure thet the leg currency of the CNY Currency is also CNY
# and other currencies


ael_variables = []

def ael_main(dict):

    curr_list =['CNY',
    'AU1',
    'KMF',
    'Med_Fuel_Oil',
    'NZ1',
    'Sin_Fuel_Oil']
    
    for c in curr_list:
        i = acm.FInstrument[c]
        l = i.Legs()[0]
        l.Currency(i)
        l.Commit()
        
    
    

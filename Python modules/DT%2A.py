import ael

 

tf = ael.TradeFilter['HennieTestAdaptor']

 

for t in tf.trades():

    ind = t.optional_key.find('/')

    tc = t.clone()

    tc.optional_key=t.optional_key[0:ind]

    try:

        tc.commit()

    except:

        print('Trade not commited') 

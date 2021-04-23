import acm

tradeSet = ['2326805']

for t in tradeSet:
    try: 
        trd = acm.FLeg[t]
        trd.Touch()
        trd.Commit()
        print('Leg %s touched successfully' %t)

    except:
        print('could not touch leg %s' %t)

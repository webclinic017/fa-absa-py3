import acm

cfSet = [20656545]
for c in cfSet:
    try:
        cfw = acm.FCashFlow[c]
        #cfw.Touch()
        #cfw.Commit()
        print(cfw.Trade().Oid())
        print('Cashflow %s touched successfully' %c)
    except:
        print('could not touch cashflow %s' %c)

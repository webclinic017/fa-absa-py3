import acm
tradeSet = [57985290, 57985291, 57985292, 57985293, 57985294, 57985295, 57985296, 57985297, 57985299, 57985301, 57985302, 57985304, 57985305, 57985306, 57985307, 57985308]
for t in tradeSet:
    trd = acm.FTrade[t]
    try:
        trd.Touch()
        trd.Commit()
        print('commiting trade', t)
    except:
        print('could not commit trade', t)

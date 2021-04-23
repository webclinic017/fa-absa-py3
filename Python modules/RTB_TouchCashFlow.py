import acm

cfSet = [22459648,
22459905,
22459586,
22459915,
22459906,
22459652,
22459655,
22459647,
22459907,
22459914,
22459571,
22459662,
22459926,
22459929,
22459930,
22459931,
22459934,
22459935,
22459936,
22459937,
22459939,
22459940,
22459941,
22459946,
22459951,
22459938,
22459955
]
for c in cfSet:
    try:
        cfw = acm.FCashFlow[c]
        cfw.Touch()
        cfw.Commit()
        print('Cashflow %s touched successfully' %c)
    except:
        print('could not touch cashflow %s' %c)

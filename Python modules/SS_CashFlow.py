import acm, ael


list = [6915270,
6914628,
6914635,
6914625,
6915184,
6915026,
6915023,
6914641,
6914643,
6915069,
6915057,
6915058]

for l in list:
    c = acm.FCashFlow[l]
    dateTemp = c.PayDate()
    print(dateTemp)
    c.PayDate('2010-09-09')
    
    c = acm.FCashFlow[l]
    c.PayDate(dateTemp)
    c.Commit()

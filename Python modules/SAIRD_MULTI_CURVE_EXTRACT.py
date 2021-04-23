'''
Date                    : 2010-12-08
Purpose                 : Extracts curve discount and spot values for specified period for specified curves
Department and Desk     : Securities Lending
Requester               : Riweena Perumal
Developer               : Rohan van der Walt
CR Number               : 520199
'''

import acm, ael, ABSA_Rate, csv

ael_variables = [
                  ['inst', 'Instrument', acm.FCurrency,acm.FCurrency.Select(''), acm.FCurrency['ZAR'],1,0],
                  ['yc', 'Yield Curves', acm.FYieldCurve, acm.FYieldCurve.Select(''), "ZAR-SWAP,ZAR-CPI,ZAR-REAL", 1,1],
                  ['days', 'Days', 'string', None, '365',1,0],
                  ['ASQLOutput', 'Old ASQL Output', 'string', ['No', 'Yes'], 'No', 1, 0, 'Write output in same format as old ASQL query that generated the values?', None, 1],
                  ['Filename', 'File Name_Output', 'string', None, 'YCRate.csv', 1],
                  ['Filepath', 'File Path_Output', 'string', None, 'F:\\', 1]
                ]

def ael_main(dict):
    ycidList = [i.Name() for i in dict['yc']]
    date1 = ael.date_today()
    date2 = date1
    rateType = 'Annual Comp'
    dayCount = 'Act/365'
    dispRate1 = 'Discount'
    dispRate2 = 'Spot Rate'
    instrument = dict['inst'].Name()
    resultVector = []
    vector = []
    vector.append('Date')
    for ycid in ycidList:
        vector.append(ycid + ' Discount')
    if dict['ASQLOutput'] == 'Yes':
        if len(ycidList) < 3:
            for i in range(3 - len(ycidList)):
                vector.append('Curve X')
        vector.append('Nbr')
        vector.append('Daycount')
        vector.append('Data_Date')
        vector.append('CURVE 1')
        vector.append('CURVE 2')
        vector.append('CURVE 3')
    for ycid in ycidList:
        vector.append(ycid + ' Spot')
    resultVector.append(vector)
    for i in range(int(dict['days'])):
        date2 = date2.add_delta(1,0,0)
        vector = []
        vector.append(date2)
        for ycid in ycidList:
            vector.append(ABSA_Rate.ABSA_yc_rate(None,ycid,date1,date2,rateType,dayCount,dispRate1,instrument))
        if dict['ASQLOutput'] == 'Yes':
            if len(ycidList) < 3:
                for y in range(3 - len(ycidList)):
                    vector.append('')        
            vector.append(i+1)
            vector.append(dayCount)
            vector.append(date1)
            vector.append('')
            vector.append('')
            vector.append('')
        for ycid in ycidList:
            vector.append(ABSA_Rate.ABSA_yc_rate(None,ycid,date1,date2,rateType,dayCount,dispRate2,instrument))
        resultVector.append(vector)
    filename = dict['Filepath'] + '/' + dict['Filename']
    try:
        outFile = open(filename,'wb')
        myWriter = csv.writer(outFile)
        for row in resultVector:
            myWriter.writerow(row)
        outFile.close()
        print 'Output written to::: ' + filename
    except Exception, e:
        print 'Error while opening/writing to file: ', e

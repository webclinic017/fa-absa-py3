import acm, csv

ael_variables = [
                    ['input', 'Input File', 'string', None, None],
                ]

def readInput(input):
    output = []

    with open(input, 'rb') as file:
        contents = csv.reader(file)
        
        for row in contents:
            output.append(row[0].replace(' ', ''))

    return output

def ael_main(aelDict):
    trades = readInput(aelDict['input'])
    
    acm.BeginTransaction()
    try:
        for trade in trades:
            ftrade = acm.FTrade[trade]
            aggregateStatus = ftrade.Aggregate()
            ftrade.Trader(acm.FUser['FMAINTENANCE'])
            ftrade.Counterparty(acm.FParty['FMAINTENANCE'])
            ftrade.Aggregate(aggregateStatus)
            ftrade.Commit()
        acm.CommitTransaction()
        print "Success"
    except:
        print "Failure"
        acm.AbortTransaction()

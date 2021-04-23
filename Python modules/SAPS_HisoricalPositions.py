'''
Date                    : 2010-12-02
Purpose                 : To extract position data in a trade filter over a specified period at specified intervals 
Department and Desk     : Prime Services
Requester               : Francois Henrion
Developer               : Rohan van der Walt
JIRA Ref                : ABITFA-426
CR Number               : 513380
'''

import acm, ael, csv

today = ael.date_today()
ael_variables = [
                  ['TradeFilter', 'TradeFilter', acm.FTradeSelection, acm.FTradeSelection.Select(''), None, 1, 0, "Trade Filter to check historic positions for"],
                  ['StartDate', 'Start Date', 'date', None, today.add_delta(0, 0, -1), 1, 0],
                  ['EndDate', 'End Date', 'date', None, today, 1, 0],
                  ['Increment', 'Interval', 'int', None, 7, 1, 0],
                  ['Filename', 'Filename', 'string', None, 'HistPosReport.csv', 1],
                  ['Filepath', 'Filepath', 'string', None, 'F:\\', 1]
                ]

def DateGenerator(start_date, end_date, inc):
    ''' Generate a stream of dates from start_date to end_date inclusive using specified intervals from the start_date.
    '''
    next_date = start_date
    while next_date <= end_date:
        yield next_date
        next_date = next_date.add_delta(inc, 0, 0)
    
def ael_main(dict):
    context = acm.GetDefaultContext()
    sheet_type = 'FPortfolioSheet'
    calc_space = acm.Calculations().CreateCalculationSpace( context, sheet_type )
    PLPOSEND_column_id = 'Portfolio Profit Loss Position End'
    ENDDATE_id1 = 'Portfolio Profit Loss End Date'
    ENDDATE_id2 = 'Portfolio Profit Loss End Date Custom'
    resultDict = {}
    print 'Retrieving historical positions'
    try:
        calc_space.InsertItem(dict['TradeFilter'])
        calc_space.Refresh()
        calc_space.SimulateGlobalValue('Portfolio Profit Loss End Date', 'Custom Date') 
        for currDate in DateGenerator(dict['StartDate'], dict['EndDate'], dict['Increment']):
            calc_space.SimulateGlobalValue('Portfolio Profit Loss End Date Custom', currDate) 
            portfolioIter = calc_space.RowTreeIterator().FirstChild()
            temp = str(portfolioIter.Tree().Item())
            if temp not in resultDict.keys():
                resultDict[temp] = {}
                resultDict[temp][str(currDate)] = calc_space.CalculateValue(portfolioIter.Tree(), PLPOSEND_column_id)
            else:
                resultDict[temp][str(currDate)] = calc_space.CalculateValue(portfolioIter.Tree(), PLPOSEND_column_id)
            childNode = portfolioIter.FirstChild()
            while childNode:
                temp = str(childNode.Tree().Item())
                if temp not in resultDict.keys():
                    resultDict[temp] = {}
                    resultDict[temp][str(currDate)] = calc_space.CalculateValue(childNode.Tree(), PLPOSEND_column_id)
                else:
                    resultDict[temp][str(currDate)] = calc_space.CalculateValue(childNode.Tree(), PLPOSEND_column_id)
                childNode = childNode.NextSibling()
        print 'Done'
    except Exception, e:
        print 'FAILED: ', e
        calc_space.RemoveGlobalSimulation(ENDDATE_id1)
        calc_space.RemoveGlobalSimulation(ENDDATE_id2)
    
    if len(resultDict.keys()) > 0:
        #Write dict to csv output
        fileName = dict['Filepath'] + '/' + dict['Filename']
        print 'Writing results to file'
        try:
            outFile = open(fileName, 'wb')
            myWriter = csv.writer(outFile)
            dates =  resultDict[resultDict.keys()[0]].keys()
            dates.sort()
            myWriter.writerow(['Instrument'] + dates)
            for ins in resultDict.keys():
                myWriter.writerow([ins] + [resultDict[ins][date] for date in dates])
            outFile.close()
            print 'Wrote output to::: ' + fileName
        except Exception, e:
            print 'Error while opening/writing to file: ', e
        print 'Console Output Complete'

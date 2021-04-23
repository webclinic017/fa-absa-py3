
import acm
import IntraDayLimitMonitoring as limits
from datetime import datetime

ael_variables = [
                ['portfolios', 'Portfolio(s)', 'FPhysicalPortfolio', None, None, 1, 1, 'Portfolios', None, 1],
                ] 

 
def ael_main(dict):
    portfolios = dict['portfolios']
    limits.runTask(portfolios)
    
    print '\nCompleted Calculation part.  Will now delete old time series entries.'
    period = '1w'
    max_delete = 5000
    date = datetime.now()
    deleteDate = limits.addDeltaToTime(date, '-'+period)
    limits.deleteTimeSeries(deleteDate, max_delete)
    
    print '\nCompleted time series delete'
    
    print '\n\nCompleted Successfully'

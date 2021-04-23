'''
Developer   : Lawrence Mucheka
Module      : BondPositionSecurityTrades
Date        : 2015-07-15
Description : Gets trades for a security as at a date equal to the Date Today specified when logging into
              Front Arena. The script gets the list of trades from the Bond Position Recon query as at that day 
              and then picks up the trades on the specified security/bond. The returned FaV Projected Value for the 
              security in the output of this script should exactly = the Fav Projected Value on the Bond Position Recon workbook
              if one logs in to Front with the same date.

History
=======

Date            CR                              Developer                           Description
==========      ======                          ================                    ===========
2015-07-15      CHNG0003156285                  Lawrence Mucheka                    Initial Implementation

'''
import ael, acm,  time, csv
from datetime               import datetime
 
           
class FavTradesSearchEngine():
    """ Security's Fav value Trades Report"""
    
    reportName = 'FavProjectedValueTrades'
    
    def __init__(self, queryName):     
        """ FavTradesSearchEngine Constructor"""
        
        self.queryName = queryName
        self.header = [
                                    'Trade No', 
                                    'Trade Status',
                                    'Instrument',
                                    'Instrument Type',
                                    'Counterparty',
                                    'Acquirer', 
                                    'Portfolio',
                                    'Parent (Portfolio Owner)',
                                    'Fav Projected',
                                    'Nominal', 
                                    'Value Day'
                                ]        
        
        
    def WriteOutput(self, rows, fileName, access='wb'):
        """ Persist data to file"""
        
        outputFile = open(fileName, access)
        try:    
            outputFile.write(self.GetBanner())
            csv.writer(outputFile,  dialect='excel-tab').writerows(rows)
            print 'Wrote secondary output to: %s' %(fileName)        
        except IOError:
            print 'Error writing output to: %s' %(fileName)         
        finally:
            outputFile.close() 
    
    
    def GetBanner(self):
        """Create the banner """
    
        generatedTime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        generatedTime += ' (UTC+0%i:00)'% ((datetime.now() - datetime.utcnow()).seconds/3600)
        
        return ''.join([
                            '            Type: Capital Markets - Bond Position\n',
                            '            Report Name: {0}\n'.format(self.reportName),
                            '            Generated Time: {0}\n\n'.format(generatedTime)
                       ])                      
   
         
    def GetRows(self, ins, *rest): 
        """ Get Trade Rows"""
        
        FVPP = 'Face Value Position Projected'

        rows = []   
        bondPositionTrades = []

        calcSpace = acm.FCalculationSpaceCollection().GetSpace("FPortfolioSheet", "Standard") 
        columns, data = ael.asql(acm.FSQL.Select('name="{0}"'.format(self.queryName))[0].Text())

        map(lambda table:map(lambda (i, row):bondPositionTrades.append(row[0]), enumerate(table, 1)), data)
        
        trades = filter(lambda trade:(((acm.FTrade[trade].Instrument().Underlying() 
            and acm.FTrade[trade].Instrument().Underlying().Name() == ins) 
                or (acm.FTrade[trade].Instrument().Name() == ins)) or (ins == '')), bondPositionTrades)

        rows.append(self.header)

        for tradeOid in trades:
            trade = acm.FTrade[tradeOid]  
            rows.append([
                            trade.Oid(),
                            trade.Status(),
                            trade.Instrument().Name(),
                            trade.Instrument().InsType(),
                            trade.Counterparty().Name() if trade.Counterparty() else '',
                            trade.Acquirer().Name(),
                            trade.Portfolio().Name(),
                            trade.Portfolio().PortfolioOwner().Name() if trade.Portfolio().PortfolioOwner() else '',
                            calcSpace.CreateCalculation(trade, FVPP).FormattedValue(),
                            trade.FaceValue(),
                            trade.ValueDay()
                        ])
                    
        return rows

'''
AEL Variables :
Variable Name, Display Name, Type, Candidate Values, Default, Mandatory,
Multiple, Description, Input Hook, Enabled
'''
ael_gui_parameters = {'runButtonLabel': '&&Search...',
                      'hideExtraControls': True,
                      'windowCaption': 'Search for Fav Trades',
                      'closeWhenFinished': True}


ael_variables = [   
                    ['fileRoot', 'File Root', 'string', 
                        None, 'f:/', 1, 0, 'Location to persist output', None, 1],
                    ['instrument', 'Instrument', 'string', 
                        None, 'ZAR/R186', 1, 0, 'Instrument', None, 1],
                    ['queryName', 'Query Name', 'string',
                        None, 'SAOPS_CM_Bond_Positions', 1, 0, 'Query Name', None, 1]
                ]
    
def ael_main(dict):
    """ Main method"""
    
    try:
        fileRoot = dict['fileRoot']  
        instrument = dict['instrument']
        queryName = dict['queryName']       
    except:
        return 'Could not get parameter values!'
    
    report = FavTradesSearchEngine(queryName)
                                    
    fileName = '{0}{1}_{2}{3}.xls'.format(fileRoot, report.reportName, instrument.replace('/', '_'), acm.Time.DateToday())
    report.WriteOutput(report.GetRows(instrument), fileName)
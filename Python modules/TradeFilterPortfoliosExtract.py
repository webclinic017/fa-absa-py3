"""
This script takes a list of trade filters and creates a feed with all the
portfolios that are included each trade filter.

Limitations:
    The script assumes that the trade filters are set up in a way that 
    explicitly states which portflios are included.
    
    i.e It looks at the symbols which make up the trade filter and extracts 
        the values where the symbol is of the form:
        
        "[, (, Portfolio, equal to, @PrfName, ]" 
        
        where @PrfName is the value to extract.

The output sources a reconciliation process which checks which portfolios
are included in the trade filters that are not included under the
MIS Reporting Line Node in the Chorus hierarchy (and vice versa).


Project                  : 
Department and Desk      : 
Requester                : 
Developer                : Nico Louw
CR Number                :

HISTORY
==============================================================================
Date        CR number    Developer       Description
------------------------------------------------------------------------------


------------------------------------------------------------------------------
"""
import csv
import acm
import FBDPGui
import FBDPString
from at_ael_variables import AelVariableHandler

# ============================ Script Functions ==============================

def write_file(name, data, access='wb'):
    """ Write data to file

    Arguments:
        name - the name of the file.
        data - the data to write to file.
    """
    file_obj = open(name, access)
    csv_writer = csv.writer(file_obj, dialect='excel')
    csv_writer.writerows(data)
    file_obj.close()
       
# ============================ Class Definition ==============================

class PortfolioRecon(object):
    """ Portfolio Recon class
    """
    def __init__(self, data):
        self.outpath = data['Outpath']
        self.trade_filters = data['TradeFilters']
        self.feed_name = '%s%s' % (self.outpath, data['FileName'])
        self.headers = []
        self.output = []
        self._headers()
        
    def _headers(self):
        """ Populate headers for feed output
        """
        self.headers.append(['Trade Filter', 'Portfolio'])
        
    def extract_portfolios(self):
        """ Get all distinct portfolios from the trade filters.
        """
        for trf in self.trade_filters:
            logme(str.format('Exctracting portfolios from {0}...', 
                trf.Name()), 'INFO')
                
            # Get conditions
            conditions = trf.FilterCondition() #Returns a collection of FSymbol
            for condition in conditions:
                # List of FSymbol to single statements 
                # Len of a condition is always 6 - each element is of type 
                # FSymbol.
                # eg1. [, (, Portfolio, equal to, Africa_Bonds, ]
                # eg2. [And, , Status, not equal to, Void, ]           
                line = []           
                for symbol in condition:
                    line.append(symbol)
                    
                # Get portfolio from line
                if str(line[2].Value()) == 'Portfolio' and str(
                        line[3].Value()) == 'equal to':
                    self.output.append([trf.Name(), str(line[4].Value())])
                    logme(str.format(
                        'Found: {0}', str(line[4].Value())), 'INFO')
        
        # Final output
        self.output = self.headers + self.output
        

# ============================== Main ========================================
# AEL Variables :
# Variable Name, Display Name, Type, Candidate Values, Default, Mandatory,
# Multiple, Description, Input Hook, Enabled

ael_variables = AelVariableHandler()
ael_variables.add('TradeFilters',
    label='Trade Filters: ',
    cls='FTradeSelection',
    collection=acm.FTradeSelection.Instances(),
    mandatory=True,
    multiple=True)
    
ael_variables.add('Outpath',
    label='Output Path: ',
    default='/services/frontnt/Task/')
    
ael_variables.add('FileName',
    label='File Name: ',
    default='temp.csv')

# Add logme options to ael_variables
logme = FBDPString.logme
ael_variables.extend(FBDPGui.LogVariables())
    

def ael_main(data):
    """ Main execution point of the feed
    """
    recon = PortfolioRecon(data)
    
    logme.setLogmeVar(__name__,
        data['Logmode'],
        data['LogToConsole'],
        data['LogToFile'],
        data['Logfile'],
        data['SendReportByMail'],
        data['MailList'],
        data['ReportMessageType'])
     
    logme(None, 'START')
    logme('Portfolio Extraction ...', 'INFO')
    
    # Call portfolio extraction
    recon.extract_portfolios()
                
    logme('Portfolio exctraction completed', 'INFO')

    try:
        write_file(recon.feed_name, recon.output)
        logme(('Wrote secondary output to: %s' % recon.feed_name), 'INFO')
    except IOError:
        logme(('Error writing file: %s' % recon.feed_name), 'ERROR')

    logme('Feed completed successfully.', 'INFO')
    logme(None, 'FINISH')

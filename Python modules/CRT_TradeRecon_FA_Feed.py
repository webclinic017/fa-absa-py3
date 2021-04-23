"""
Implementation of the FA feed for use in CRT Trade Recon.

Extracts data from front/Midas feed to compare with Seahawk feed.

Project                  : CRT Trade Recon - FA Feed
Department and Desk      : CRT
Requester                : Mare, Eben
Developer                : Nico Louw
CR Number                :

HISTORY
==============================================================================
Date            CR number       Developer       Description
------------------------------------------------------------------------------
24/04/2015      CHNG0002995026  Nico Louw       Added Front Arena Cpty Id.

------------------------------------------------------------------------------
"""
import csv
import ael
import acm
import os
import FRunScriptGUI
import FBDPGui
import FBDPString
import at_addInfo as addInf


# =========================== Script functions ===============================


logme = FBDPString.logme
SCRIPT_NAME = __name__

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


class CRT_FA_Feed(object):
    """ CRT feed class
    """
    def __init__(self, data):
        self.outpath = data['Outpath']
        self.portfolios = data['Portfolios']
        #self.trdFilter = data['TrdFilter']
        self.start_date = ael.date_today()
        self.feed_name = '%s%s' % (self.outpath, 'CRT_Recon_Feed.csv')
        self.headers = []
        self.output = []
        self._headers()

    def _headers(self):
        """ Populate headers for feed output
        """
        self.headers.append([
            'Trd Nbr', 'CPTY Name', 'Eagle SDSID', 'CPTY SDSID',
            'Legal Entity SDSID', 'Cpty Type', 'Cpty Id', 'Cpty Prf',
            'CSA', 'Bus Date'
            ])


# ============================== Main ========================================
# AEL Variables :
# Variable Name, Display Name, Type, Candidate Values, Default, Mandatory,
# Multiple, Description, Input Hook, Enabled

ael_variables = FBDPGui.LogVariables([
    'Outpath', 'Output Path: ', 'string', None, 'F:\\\\', 1])
ael_variables.append([
    'Portfolios', 'Portfolios: ', 'FCompoundPortfolio',
    acm.FCompoundPortfolio.Instances(), None, 1, 1, 'Portfolio parameter',
    None, 1
    ])
    
    
def ael_main(data):
    """ Main execution point of the feed
    """
    
    feed = CRT_FA_Feed(data)
    
    logme.setLogmeVar(feed.feed_name,
        data['Logmode'],
        data['LogToConsole'],
        data['LogToFile'],
        data['Logfile'],
        data['SendReportByMail'],
        data['MailList'],
        data['ReportMessageType'])
     
    
    logme(None, 'START')
    logme('Starting CRT_FA_Feed feed...', 'INFO')
    
    for prf in feed.portfolios:
        for trade in prf.Trades():
            if trade.Status() not in ['Simulated', 'Void']:
                try:
                    # Get SDSID's from Counterparty AdditionalInfo.
                    eagle_SDSID = addInf.get_value(
                        trade.Counterparty(), 'BarCap_Eagle_SDSID')
                    cp_SDSID = addInf.get_value(
                        trade.Counterparty(), 'BarCap_SMS_CP_SDSID')
                    le_SDSID = addInf.get_value(
                        trade.Counterparty(), 'BarCap_SMS_LE_SDSID')
                    cpty_type = trade.Counterparty().Type()
                    cpty_id = trade.Counterparty().Oid()
                    if trade.CounterPortfolio():
                        cpty_prf = trade.CounterPortfolio().Name()
                    else:
                        cpty_prf = ''
                   
                    feed.output.append([
                        trade.Oid(), trade.Counterparty().Name(), eagle_SDSID, 
                        cp_SDSID, le_SDSID, cpty_type, cpty_id,
                        cpty_prf, trade.Counterparty().add_info('CSA'),
                        feed.start_date
                        ])
                    
                except Exception, e:
                    logme(e.__repr__(), 'ERROR')
        
    logme('Exctraction complete', 'INFO')

    feed.output = feed.headers + feed.output
    try:
        write_file(feed.feed_name, feed.output)
        logme(('Wrote secondary output to: %s' % feed.feed_name), 'INFO')
    except IOError:
        logme(('Error writing file: %s' % feed.feed_name), 'ERROR')

    logme('Feed completed successfully.', 'INFO')

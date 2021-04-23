#------------------------------------------------------------------------------
#Name:           TMS_Recon_Extract
#Purpose:        This AEL will generate the XML for the recon between Front Arena and BarCap TMS
#Developer:      Neil Retief
#Create Date:    2008-06-03
#
#Changes
#
#Developer:      Peter Kutnik
#Date:           2010-02-22
#Detail:         Added 'sanitized' trade filter name to the extract XML file name
#CR:		243826
#
#Changes
#
#Developer:      Babalo Edwana
#Date:           2010-11-12
#Detail:         Updated Module to use the New TMS_Recon_Template Module
#CR:
#
#Changes
#
#Developer:      Michal Spurny
#Date:           2012-04-25
#Detail:         Updated Module to use the New TMS_Recon_Template Module
#CR:		 154268
#------------------------------------------------------------------------------

import ael, amb, time
import string
import TMS_Recon_Template
import sys
import traceback

def ael_main(ael_dict):

    ReportDate = ael_dict["ReportDate"]
    Server = ael_dict["Server"]
    TradeFilter = ael_dict["TradeFilter"]
    UniqueFileNames = ael_dict["UniqueFileNames"]

    TMS_Generate_XML(1, TradeFilter, Server, ReportDate, UniqueFileNames)

ael_variables = [('ReportDate', 'ReportDate', 'date', None, ael.date_today(), 1),
                  ('Server', 'Server', 'string', None, '//services/frontnt/BackOffice/Atlas-End-Of-Day/', 1),
                  ('TradeFilter', 'TradeFilter', 'string', None, 'NLDO & Hedg8', 1),
                  ('UniqueFileNames', 'UniqueFileNames', 'string', ['Yes', 'No'], 'No', 0)]
                  
    
def TMS_Generate_XML(temp,TrdFilter,Server,ReportDate,UniqueFileNames,*rest):

    FileDate = ael.date_from_string(ReportDate)
    FileDate = FileDate.to_string('%Y%m%d')
    
    outFileName = ''
    logFileName = ''
    
    if UniqueFileNames == 'Yes':
        transtable = string.maketrans('<>:/\\*=?|^', 'LGCSEXIQJA')
        sanitizedTrdFilter = TrdFilter.translate(transtable)
        outFileName = '%sABCAP_FRONTTMS_Extract_%s_%s.xml' % (Server, sanitizedTrdFilter, FileDate)
        logFileName = '%sABCAP_FRONTTMS_Extract_Log_%s.txt' % (Server, sanitizedTrdFilter)
    
    else:
        outFileName = '%sABCAP_FRONTTMS_Extract_%s.xml' % (Server, FileDate)
        logFileName = '%sABCAP_FRONTTMS_Extract_Log.txt' % Server 
    
    outfile = open(outFileName, 'w')
    Log = open(logFileName, 'w')

    outfile.write('<?xml version="1.0"?>\n')
    outfile.write('<TRADES>\n')

    for t in ael.TradeFilter[TrdFilter].trades():
        try:
            TradeXMLstr = TMS_Recon_Template.TMS_Generate_XML(t.trdnbr) 
            outfile.write(TradeXMLstr)                       
        except Exception, e:
            Log.write('Trade cannot be extracted - %i\n' % t.trdnbr)
                        

    outfile.write('</TRADES>')
    outfile.close()
    Log.close()

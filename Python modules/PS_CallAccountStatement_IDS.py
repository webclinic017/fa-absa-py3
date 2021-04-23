#Script Name             :PS_CallAccountStatement_IDS
#************************************************************************************************************************
#Script Name             :PS_CallAccountStatement_IDS
#Description             :Call statement for a client's call account to fund administrator IDS
#Developer               :Momberg Heinrich
#CR Number(s)            :ABITFA-605(IDS)
#************************************************************************************************************************
import acm, ael
import FReportSettings
import os
import PS_Functions_IDS

from xml.etree import ElementTree
from xml.etree.ElementTree import Element, SubElement
from SAMM_Statements import GenStatementXML
from gen_ael_variables_date_param import DateParameter
from gen_ael_variables_date_param import DateEnum
from string import Template

#***********************************************************************************************


#***********************************************************************************************
# Method name:  _genCallAccountStatements
# Description:  Generates a call account for each party 
# Parameters:   parties - a tuple of part names for which to generate call account statements
# Return Type:  0 = success, -1 = failure
#***********************************************************************************************
def _genCallAccountStatements(portfolio, party, outputPath, fileName, startDate, endDate, xslTemplate, contactIndex, att):
    
    #Retrieve the actual party and portfolio
    pf          = acm.FPhysicalPortfolio[portfolio]
    p           = acm.FParty[party]
    
    if(p):
        #Find the call account (FDeposit instrument and trade for the call account)
        callAccounts = PS_Functions_IDS.getCallAccounts(pf, p)
        if(len(callAccounts)!=1):
            raise Exception("Zero or more than one call account found for party '%s' in specified portfolio. Cannot continue" % party)
        ca = callAccounts[0]
        ca_trades = [t for t in ca.Trades() if t.Status() not in ('Simulated', 'Void')]
        if(len(ca_trades)!=1):
            raise Exception("Zero or more than one trade found for account '%s'" % ca)
            
        #Use SAMM_Statements to generate the call account statement XML
        acmTrade        = ca_trades[0]
        t               = ael.Trade[acmTrade.Oid()]
        startd          = ael.date(startDate)
        endd            = ael.date(endDate)
        
        stat            = GenStatementXML(t, startd, endd, 1, 0, 0, 'Daily', 0, 'C:\\', None)
        
        if(stat=="FAIL"):
            print "Could not generate the call account statement. No balances found, nothing to report"
            return 0
        
        #Add the Client Detail
        cp = acmTrade.Counterparty()
        if(cp):
            try:
                clientDetail = acmTrade.Counterparty().Contacts()[contactIndex]
            except:
                raise Exception("Invalid Party contact index provided")
            if(clientDetail):
                CLIENTDETAIL = SubElement(stat, "CLIENTDETAIL")
                SubElement(CLIENTDETAIL, "CNAM").text = cp.Name()
                SubElement(CLIENTDETAIL, "ADDR1").text = clientDetail.Address()
                SubElement(CLIENTDETAIL, "ADDR2").text = clientDetail.Address2()
                SubElement(CLIENTDETAIL, "CIT").text = clientDetail.City()
                SubElement(CLIENTDETAIL, "ZIP").text = clientDetail.Zipcode()
                SubElement(CLIENTDETAIL, "CTY").text = clientDetail.Country()
                SubElement(CLIENTDETAIL, "ATT").text = clientDetail.Attention()
        
        #Add the Prime Services Detail
        PRIMEDETAIL = SubElement(stat, "PRIMEDETAIL")
        SubElement(PRIMEDETAIL, "CNAM").text = 'ABSA CAPITAL Prime Broking'
        SubElement(PRIMEDETAIL, "ADDR").text = 'PRIVATE BAG X10056'
        SubElement(PRIMEDETAIL, "CIT").text = 'SANDTON'
        SubElement(PRIMEDETAIL, "ZIP").text = '2146'
        SubElement(PRIMEDETAIL, "CTY").text = 'SOUTH AFRICA'
        SubElement(PRIMEDETAIL, "TEL").text = '+27 11 895 5422/7245'
        SubElement(PRIMEDETAIL, "EMAIL").text = 'primeservices@absacapital.com'
        SubElement(PRIMEDETAIL, "ATT").text = att
        #print t.trdnbr, startd, endd
        
       
        #Get the xml from the element tree
        xml = ElementTree.tostring(stat)
        
              
        #Now transform the xml
        context         = acm.GetDefaultContext()
        pt              = context.GetExtension('FXSLTemplate', 'FObject', xslTemplate)       
        if not pt:
            raise Exception("Prime Services FXSLTemplate extension '%s' not found " % xslTemplate)
        xsl             = pt.Value()
        transformer     = acm.CreateWithParameter('FXSLTTransform', xsl)
        FOP             = transformer.Transform(xml)
        
        foFile          = outputPath +  fileName + '.fo'
        outfile         = open(foFile, "w")  
        outfile.write(FOP)
        outfile.close()
        print "Formatting objects (FO) output file written to '%s'" % foFile
        
        pdfFile = outputPath +  fileName
        try:
            print "Calling FOP with settings '%s'" % FReportSettings.FOP_BAT
            fopCommand     = Template(FReportSettings.FOP_BAT)
            fopCommand     = fopCommand.substitute({'extension':'pdf', 'filename':pdfFile})
            os.system(fopCommand)
        except Exception, e:
        #Problems
           print "An error occured while generating the pdf file '%s'" % str(e)
           return -1
        
        #Success!!!
        print "PDF generated to %s.pdf" % pdfFile
        return 0

#*******************************************************************************************************************************************************************
#Main entry point and Variables
#*******************************************************************************************************************************************************************
#Variable Name, Display Name, Type, Candidate Values, Default, Mandatory, Multiple, Description, Input Hook, Enabled
ael_variables = [
                    ['portfolio', 'Portfolio', 'string', acm.FPhysicalPortfolio.Select(''), 'PB_FINANCING_ARI', 1, 0, 'The portfolios which contains call account statements.', None, 1],
                    ['party', 'Party', 'string', acm.FParty.Select(''), 'MAP 280 FUND GP PTY LTD', 1, 0, 'The parties for whom to generate call account statements.', None, 1],
                    ['outputPath', 'Output Path', 'string', None, '/services/frontnt/Task/', 1, 0, 'The path where the output files should be writter', None, 1],
                    ['fileName', 'File Name', 'string', None, 'PS_CallAccountStatement_IDS_Test', 1, 0, 'The name of the output files.', None, 1],
                    ['startDate', 'Start Date', 'string', None, PS_Functions_IDS.FIRSTOFMONTH, 0, 0, 'Start date of statement. Leave blank for the first day of the month', None, 1],
                    ['endDate', 'End Date', 'string', None, PS_Functions_IDS.TODAY, 0, 0, 'End date of statement. Leave blank for today', None, 1],
                    ['xslTemplate', 'XSL Template', 'string', PS_Functions_IDS.getXSLTemplates(), 'PS_CallAccountStatement_IDS', 1, 0, 'The FO-XSL stylesheet to use for the PDF conversion', None, 1],
                    ['attPrimeServices', 'Attention', 'string', None, 'Attention Who', 1, 0, 'The attention line that app', None, 1],
                    ['contactIndex', 'Party Contact Index', 'int', 0, 1, 0, 0, 'The index of the contact detail to use on the report for the party', None, 1]
                ]

def ael_main(dict):

    try:
        #get all the passed parameters
        portfolio = dict['portfolio']
        party = dict['party']
        outputPath = dict['outputPath']
        fileName = dict['fileName']
        startDate = dict['startDate']
        if(startDate==''):
            startDate = PS_Functions_IDS.FIRSTOFMONTH
        endDate = dict['endDate']
        if(endDate==''):
            endDate = PS_Functions_IDS.TODAY
        xslTemplate = dict['xslTemplate']
        contactIndex = dict['contactIndex']
        att = dict['attPrimeServices']
        
        #Generate the PDF based on the passed parameters
        result = _genCallAccountStatements(portfolio, party, outputPath, fileName, startDate, endDate, xslTemplate, contactIndex, att)
        
        if(result==0):
            print 'Completed Successfully!'
        else:
            print 'Failed!'
        
    except Exception, e:
        print "Failed. Reason: %s" % str(e)
    
    
#*******************************************************************************************************************************************************************
        


    
    
    
 


'''----------------------------------------------------------------------------------------------------------------------------------
Description                    :  Extract the trades for Operations for Group Treasury


Purpose                       :  [Initial Deployment]
Department and Desk           :  [OPS - GT]
Requester                     :  [Martin Wortmann]
Developer                     :  [Bushy Ngwako]
CR Number                     :  []
----------------------------------------------------------------------------------------------------------------------------------
----------------------------------------------------------------------------------------------------------------------------------
* Purpose                       : [Apply Change to the Security Nominal Calculation of trades with Amortizing Profile on all Recons]
* Department and Desk           : [OPS - GT]
* Requester                     : [Linda Breytenbach]
* Developer                     : [Bushy Ngwako]
* CR Number                     : [CHNG0003965110 - ABITFA-4189]
----------------------------------------------------------------------------------------------------------------------------------
----------------------------------------------------------------------------------------------------------------------------------
* Purpose                       : [Security Recon - Amend Report Date]
* Department and Desk           : [OPS - GT]
* Requester                     : [Linda Breytenbach]
* Developer                     : [Bushy Ngwako]
* CR Number                     : [CHNG0004345910 - ABITFA-4717]
----------------------------------------------------------------------------------------------------------------------------------
----------------------------------------------------------------------------------------------------------------------------------
* Purpose                       : 
* Department and Desk           : 
* Requester                     :
* Developer                     :
* CR Number                     :

'''


import acm, ael, csv, os, FRunScriptGUI, re, datetime
from itertools import groupby
from operator import itemgetter

# For ReportDate to populate with T-1 date as requested by Business User
TODAY           = ael.date_today().add_banking_day(ael.Calendar['ZAR Johannesburg'], 0)
YESTERDAY       = TODAY.add_days(-1)
TOMORROW        = TODAY.add_banking_day(ael.Calendar['ZAR Johannesburg'], +1)
PREVBUSDAY      = TODAY.add_banking_day(ael.Calendar['ZAR Johannesburg'], -1)
FUNCDATE        = datetime.datetime.today().weekday()
CALC_SPACE = acm.Calculations().CreateCalculationSpace(acm.GetDefaultContext(), acm.FTradeSheet)

                     
def InstrOrUnderISIN(trade):
	return (trade.Instrument() and trade.Instrument().Isin()) or \
            (trade.Instrument().Underlying() and \
                trade.Instrument().Underlying().Isin())

def listOfFilters():
    return acm.FTradeSelection.Select('')

def getFilePath(filePath, fileName):

    return os.path.join(filePath, fileName)

def isAmortizingBond(instrument):
    is_amortizing = False
    if instrument.FirstFixedLeg():
        if instrument.FirstFixedLeg().AmortType() not in ('', 'None'):
            is_amortizing = True

    return is_amortizing


def nominal_calc(trade):
    return CALC_SPACE.CreateCalculation(trade, 'Structure Nominal').Value()
    

class TradingManagerReport(object):

   def __init__(self, tradeFilter):

        self.trdfltr = tradeFilter
        self.trades = None
        self.rows = {}
        self.rows = {}
        self.reportdata = []
        self.groupdata = []
        self.heading = ['', 'Security_Name', 'Settle Category', 'Trade ExternalId', 'Report Date', 'Value Day', 'Ins Expiry Date', 'Trade No',
		        'Mirror Trade', 'Trans Trade',  'Acquirer', 'Counterparty', 'Issuer', 'Instrument Type',
                        'Ins Name', 'Portfolio Name', 'Ins External Id1', 'Ins External Id2', 'ISIN',
                        'Currency', 'BuySell', 'Total Issue Size', 'Price', 'Security Nominal', 'Premium', 'SND Trade Type',
                        'SNMI Asset Class', 'SNMI Master Program', 'SNMI STR Reference', 'ECA Number']		


        self.groupheading_agg = ['', 'Security_Name', 'Report Date', 'Issuer', 'Instrument Type', 'Ins External Id1', 'ISIN', 'Currency', 'Security Nominal', 'Premium', 'Total Issue Size']		
        self.groupheading = ['', 'Security_Name', 'Report Date', 'Issuer', 'Instrument Type', 'Ins External Id1', 'ISIN', 'Currency', 'Security Nominal', 'Premium']
    
   
   # Function to handle dictionary for Aggregated Trades report 
   def GetRows(self):

        if self.trdfltr:

            self.trades = self.trdfltr.Trades()

            

            for trd in self.trades:
                ins_or_und = str(InstrOrUnderISIN(trd) if InstrOrUnderISIN(trd) <> None else '')
                ins_or_und = len(ins_or_und) > 12 and ins_or_und[0:12] or ins_or_und
                
                externalID1 = trd.Instrument().ExternalId1()[:6]
                isin = trd.Instrument().Isin()[:12]
                Expiry_Date = trd.Instrument().ExpiryDate()[0:11]
                reportdate = TODAY
                

                self.rows.setdefault(externalID1, []).append(['',   trd.Instrument().Underlying() and trd.Instrument().Underlying().Name() or trd.Instrument().Name(),
                                                                    trd.SettleCategoryChlItem() and trd.SettleCategoryChlItem().Name() or None,   
                                                                    trd.OptionalKey(),
                                                                    reportdate,
                                                                    trd.ValueDay(), 
                                                                    Expiry_Date,
                                                                    trd.Oid(),                                                                    
                                                                    trd.MirrorTrade() and trd.MirrorTrade().Oid() or None,
                                                                    trd.TrxTrade() and trd.TrxTrade().Oid() or None,
                                                                    trd.Acquirer() and trd.Acquirer().Name() or None,                                                                    
                                                                    trd.Counterparty() and trd.Counterparty().Name() or None,
                                                                    trd.Instrument().Issuer() and trd.Instrument().Issuer().Name() or None,
                                                                    trd.Instrument().InsType(),
                                                                    trd.Instrument().Name(),
                                                                    trd.Portfolio() and trd.Portfolio().Name() or None,
                                                                    trd.Instrument().ExternalId1() or (trd.Instrument().Underlying() and trd.Instrument().Underlying().Name()) or None,
                                                                    trd.Instrument().ExternalId2(),
                                                                    ins_or_und,
                                                                    trd.Instrument().Currency() and trd.Instrument().Currency().Name() or None,   
                                                                    nominal_calc(trd) < 0 and 'Sell' or 'Buy',
                                                                    trd.Instrument().TotalIssued(),
                                                                    trd.Price(),
                                                                    nominal_calc(trd),
                                                                    trd.Premium(),
                                                                    str(trd.add_info('SND_Trade_Type')),
                                                                    str(trd.add_info('SNMI_Asset_Class')),
                                                                    str(trd.add_info('SNMI_Master_Program')),
                                                                    str(trd.add_info('SNMI_STR_Reference')),
                                                                    str(trd.add_info('ECA Number')),
                                                                ])


   # Function to handle dictionary for Aggregated Trades report
   def GetRows_agg(self):
        if self.trdfltr:

            self.trades = self.trdfltr.Trades()  
            self.rows = {}
            for trd in self.trades:
                ins_or_und = str(InstrOrUnderISIN(trd))
                ins_or_und = len(ins_or_und) > 12 and ins_or_und[0:12] or ins_or_und
                
                externalID1 = trd.Instrument().ExternalId1()[:6]
                isin = trd.Instrument().Isin()[:12]
                reportdate = TODAY 

                self.rows.setdefault(externalID1, []).append(['', trd.Instrument().Underlying() and trd.Instrument().Underlying().Name() or trd.Instrument().Name(),   
                                                        reportdate,
                                                        trd.Instrument().Issuer() and trd.Instrument().Issuer().Name() or None,
                                                        trd.Instrument().InsType(),                                                        
                                                        externalID1,
                                                        ins_or_und,
                                                        trd.Instrument().Currency() and trd.Instrument().Currency().Name() or None, 
                                                        nominal_calc(trd),
                                                        trd.Premium(),
                                                        trd.Instrument().TotalIssued(),
                                                        ])
                                                                   
                
   # Function to handle grouping and head grouping for Trade Report
   def WriteOutput(self, fileName, filePath ):

        outputrows = []
        reportdate = 'Report Date : %s' % (acm.Time.DateToday())
        

        self.heading[0] = reportdate

        self.reportdata.append(self.heading )
        for key in self.rows.keys():
            trdrows = self.rows[key]
            grouprow = None
            
            instype_ind     = self.heading.index('Instrument Type')
            instype_val     = reduce(lambda x, y: x or y, [ tr[instype_ind] for tr in trdrows])
            
            premium_ind     = self.heading.index('Premium')
            premium_val     = reduce(lambda x, y: x+y, [ tr[premium_ind] for tr in trdrows])
            
            report_date_ind = self.heading.index('Report Date')
            report_date_val = reduce(lambda x, y: x or y, [ tr[report_date_ind] for tr in trdrows])
            
            issuer_ind      = self.heading.index('Issuer')
            issuer_val      = reduce(lambda x, y: x or y, [ tr[issuer_ind] for tr in trdrows])

            total_issu_ind  = self.heading.index('Total Issue Size')
            total_issu_val  = reduce(lambda x, y: x or y, [ tr[total_issu_ind] for tr in trdrows])
            
            fac_val_ind     = self.heading.index('Security Nominal')
            
            buysell_ind     = self.heading.index('BuySell')
            
            sec_name_ind    = self.heading.index('Security_Name')
            sec_name_val    = reduce(lambda x, y: x+y, [ tr[sec_name_ind] for tr in trdrows])
            
            exclude_isin = ['None', '']
            isin_ind        = self.heading.index('ISIN')
            isin_val        = reduce(lambda x, y: y if (x in exclude_isin) else x, [ tr[isin_ind] for tr in trdrows ] )
            
            curr_ind        = self.heading.index('Currency')
            curr_val        = reduce(lambda x, y: x or y, [ tr[curr_ind] for tr in trdrows])

            set_cat_ind     = self.heading.index('Settle Category')
            set_cat_val     = reduce(lambda x, y: x or y, [ tr[set_cat_ind] for tr in trdrows])						

            extern_id1_ind  = self.heading.index('Ins External Id1')
            extern_id1_val  = reduce(lambda x, y: x or y, [ tr[extern_id1_ind] for tr in trdrows])			

            extern_id2_ind  = self.heading.index('Ins External Id2')
            extern_id2_val  = reduce(lambda x, y: x or y, [ tr[extern_id2_ind] for tr in trdrows])	
            
            
            for trdrow in trdrows:
                if not grouprow:
                    cols                       = len(trdrow) 
                    grouprow                   = [''] * len(trdrow)
                    grouprow[0]                = key
                    grouprow[sec_name_ind]     = "ISSUED NOMINAL"
                    grouprow[buysell_ind]      = "ISS"
                    grouprow[set_cat_ind]      = set_cat_val
                    grouprow[report_date_ind]  = report_date_val
                    grouprow[issuer_ind]       = issuer_val
                    grouprow[extern_id1_ind]   = extern_id1_val
                    grouprow[extern_id2_ind]   = extern_id2_val
                    grouprow[isin_ind]         = isin_val
                    grouprow[curr_ind]         = curr_val
                    
                    exclude_issuer = ['ABSA BANK LTD']
                    
                    if issuer_val in exclude_issuer:  
                        grouprow[fac_val_ind]      = total_issu_val
                    else:
                        grouprow[fac_val_ind]      = 0.0
                        

                    self.reportdata.append(grouprow)

                self.reportdata.append(trdrow)

        f = open(getFilePath( filePath, fileName), 'wb')

        recon = csv.writer(f, dialect = 'excel')
        recon.writerows(self.reportdata)
        print getFilePath( filePath, fileName)
        f.close()

   
   # Function to handle grouping and head grouping  for Aggregated Trades report             
   def WriteOutput_agg(self, fileName, filePath ):

            outputrows = []
            reportdate = 'Report Date : %s' % (acm.Time.DateToday())

            
            self.groupdata.append(self.groupheading )
            premium_val = 0.0
            
            for key in self.rows.keys(): # Iterating through the External ID1
                trdrows = self.rows[key]
                grouprow = None
                
                sec_name_ind    = self.groupheading_agg.index('Security_Name')
                sec_name_val    = reduce(lambda x, y: x+y, [ tr[sec_name_ind] for tr in trdrows])
                
                report_date_ind = self.groupheading_agg.index('Report Date')
                report_date_val = reduce(lambda x, y: x or y, [ tr[report_date_ind] for tr in trdrows])   
                
                issuer_ind      = self.groupheading_agg.index('Issuer')
                issuer_val      = reduce(lambda x, y: x or y, [ tr[issuer_ind] for tr in trdrows])                
                
                instype_ind     = self.groupheading_agg.index('Instrument Type')
                
                externid1_ind   = self.groupheading_agg.index('Ins External Id1')
                externid1_val   = reduce(lambda x, y: x or y, [ tr[externid1_ind] for tr in trdrows])
                
                externid1_val2   = reduce(lambda x, y: x or y, [ tr[externid1_ind] for tr in trdrows])
                
                exclude_isin = ['None', '']
                isin_ind        = self.groupheading_agg.index('ISIN')
                isin_val        = reduce(lambda x, y: y if (x in exclude_isin) else x, [ tr[isin_ind] for tr in trdrows ] )
                    
                curr_ind        = self.groupheading_agg.index('Currency')
                curr_val        = reduce(lambda x, y: x or y, [ tr[curr_ind] for tr in trdrows])               
                
                total_issu_ind  = self.groupheading_agg.index('Total Issue Size')
                total_issu_val  = reduce(lambda x, y: x or y, [ tr[total_issu_ind] for tr in trdrows])                
                
                sec_nom_ind     = self.groupheading_agg.index('Security Nominal')
                sec_nom_val     = reduce(lambda x, y: x+y, [ tr[sec_nom_ind] for tr in trdrows])
                
                premium_ind     = self.groupheading_agg.index('Premium')
                premium_val     = reduce(lambda x, y: x+y, [ tr[premium_ind] for tr in trdrows])
                

                if not grouprow:

                    cols                      = len(self.groupheading_agg)
                    grouprow                  = [''] * len(self.groupheading_agg)
                    grouprow[0]               = key
                    grouprow[sec_name_ind]    = 'Issued Nominal'
                    grouprow[report_date_ind] = report_date_val
                    grouprow[issuer_ind]      = issuer_val
                    grouprow[isin_ind]        = isin_val
                    grouprow[curr_ind]        = curr_val                    
                    grouprow[externid1_ind]   = externid1_val
                    
                    exclude_issuer = ['ABSA BANK LTD']
                    if issuer_val in exclude_issuer:  
                        grouprow[sec_nom_ind]     = total_issu_val
                    else:
                        grouprow[sec_nom_ind]      = 0.0
                        
                    


                    
                    self.groupdata.append(grouprow)
                
                d = dict((tr[instype_ind], []) for tr in trdrows) # Creating a distinct list of Instruments per External ID1
                for insKey in d.keys(): # Looping through the Instrument types to aggregate Nominal and Premium
                    instype_Sec         = reduce(lambda x, y: x+y, [ tr[sec_nom_ind] for tr in trdrows if tr[instype_ind] == insKey]) # Aggregation of NominalAmount on Instrument type level
                    instype_Pre         = reduce(lambda x, y: x+y, [ tr[premium_ind] for tr in trdrows if tr[instype_ind] == insKey]) # Aggregation of Premium on Instrument type level
                    instype_SecName     = reduce(lambda x, y: x or y, [ tr[sec_name_ind] for tr in trdrows if tr[instype_ind] == insKey]) # Aggregation of Security Name on Instrument type level
                    instype_Curr        = reduce(lambda x, y: x or y, [ tr[curr_ind] for tr in trdrows if tr[instype_ind] == insKey]) # Aggregation of Currency on Instrument type level

                    grpcols = len(self.groupheading_agg)
                    grpheadrow = [''] * grpcols
                    
                    grpheadrow[1]  = instype_SecName
                    grpheadrow[2]  = report_date_val
                    grpheadrow[3]  = issuer_val
                    grpheadrow[4]  = insKey
                    grpheadrow[5]  = externid1_val
                    grpheadrow[6]  = isin_val
                    grpheadrow[7]  = curr_val
                    grpheadrow[8]  = instype_Sec
                    grpheadrow[9]  = instype_Pre
                    
                    self.groupdata.append(grpheadrow)         
           
                
            agg_file = re.sub(".csv", "_Aggregate.csv", fileName)
            fg = open(getFilePath( filePath, agg_file ), 'wb')

            recon = csv.writer(fg, dialect = 'excel')
            recon.writerows(self.groupdata)
            print getFilePath( filePath, agg_file )
            print 'completed successfully'
            fg.close()


outputSelection = FRunScriptGUI.DirectorySelection()

FILE_NAME_KEY = 'FileName'
FILE_PATH_KEY = 'Path'
TRADE_FILTER_KEY = 'Trade Filter'

ael_variables = [ [FILE_NAME_KEY, 'File Name', 'string', None, 'Structured_Notes.csv', 1, 1, 'Name of the file.', None, 1],
                  [FILE_PATH_KEY, 'Output Directory', outputSelection, None, outputSelection, 1, 1, 'Directory where the file will be created.', None, 1],
                  [TRADE_FILTER_KEY, 'Filter', 'FTradeSelection', listOfFilters(), 'GT_Recon_Corp', 1, 0, 'select trade filter', None, 1]]
        
        
def ael_main(parameters):

    fileName 	= parameters[FILE_NAME_KEY][0]
    filePath 	= parameters[FILE_PATH_KEY]
    trdFilter 	= parameters[TRADE_FILTER_KEY]

    reconReport =  TradingManagerReport(trdFilter)
    
    reconReport.GetRows()
    reconReport.WriteOutput(fileName, filePath.SelectedDirectory().Text() )   
    reconReport.GetRows_agg()
    reconReport.WriteOutput_agg(fileName, filePath.SelectedDirectory().Text() )

'''-------------------------------------------------------------------------------------------------------------------------------
* Description                    :  Extract the trades for Operations for Group Treasury
* Purpose                       :  [Initial deployment]
* Department and Desk           :  [OPS - GT]
* Requester                     :  [Linda Breytenbach]
* Developer                     :  [Manan Ghosh]
* CR Number                     :  []
----------------------------------------------------------------------------------------------------------------------------------
----------------------------------------------------------------------------------------------------------------------------------
* Description                    :  Extract the trades for Operations for Group Treasury
* Purpose                       :  [Trim all ISIN or Underlying ISIN; Nominal Calculation to accomodate other instype(Buy-Sellback);
                                  Issuer Exception function; include new columns (i.e. Total Issue Size, ReportDate) and change 
                                  column name "Face Value" to "Security Nominal", Add new Group headers (i.e. Issuer and more; New
                                  dictionary to handle all Aggregated Trades]
* Department and Desk           :  [OPS - GT]
* Requester                     :  [Linda Breytenbach]
* Developer                     :  [Bushy Ngwako]
* CR Number                     :  [CHNG0003317856]
----------------------------------------------------------------------------------------------------------------------------------
----------------------------------------------------------------------------------------------------------------------------------
* Description                   : 
* Purpose                       : [Additional underlying attributes populated; Trans Ref column populated; removed "None" for ISIN
                                 column]
* Department and Desk           : [OPS - GT]
* Requester                     : [Linda Breytenbach]
* Developer                     : [Bushy Ngwako]
* CR Number                     : [CHNG0003421905 ABITFA-4020 & ABITFA-4053]

----------------------------------------------------------------------------------------------------------------------------------
----------------------------------------------------------------------------------------------------------------------------------
* Description                   : 
* Purpose                       : [Calculate Correct Security Nominal on BasketRepo/Reverse trades; Use "Acquire Day" instead of "Value
                                 day" and "Re-Acquire Day" instead of "Instrument Expiry Day" for Collateral Trades Entries]
* Department and Desk           : [OPS - GT]
* Requester                     : [Linda Breytenbach]
* Developer                     : [Bushy Ngwako]
* CR Number                     : [CHNG0003539170 - ABITFA-4052]
----------------------------------------------------------------------------------------------------------------------------------
----------------------------------------------------------------------------------------------------------------------------------
* Description                   : ''
* Purpose                       : [Fixing Settle Category underlying column; Collaborating Offshore and AfricaOffshore Files]
* Department and Desk           : [OPS - GT]
* Requester                     : [Linda Breytenbach]
* Developer                     : [Bushy Ngwako]
* CR Number                     : [CHNG0003595114 - ABITFA-4188]
----------------------------------------------------------------------------------------------------------------------------------
----------------------------------------------------------------------------------------------------------------------------------
* Purpose                       : [Remove Exponential Notations]
* Department and Desk           : [OPS - GT]
* Requester                     : [Linda Breytenbach]
* Developer                     : [Bushy Ngwako]
* CR Number                     : [CHNG0003721862 - ABITFA-4302]
----------------------------------------------------------------------------------------------------------------------------------
----------------------------------------------------------------------------------------------------------------------------------
* Purpose                       : [Collateral Trade Entry without ReAcquireDay to Populate]
* Department and Desk           : [OPS - GT]
* Requester                     : [Linda Breytenbach]
* Developer                     : [Bushy Ngwako]
* CR Number                     : [ - ABITFA-4189]
----------------------------------------------------------------------------------------------------------------------------------
----------------------------------------------------------------------------------------------------------------------------------
* Purpose                       : [Apply Change to the Security Nominal Calculation of trades with Amortizing Profile on all Recons]
* Department and Desk           : [OPS - GT]
* Requester                     : [Linda Breytenbach]
* Developer                     : [Bushy Ngwako]
* CR Number                     : [CHNG0003965110 - ABITFA-4189]
----------------------------------------------------------------------------------------------------------------------------------
----------------------------------------------------------------------------------------------------------------------------------
* Purpose                       : [If trades are booked on a 'Collateral Trade Entry' ticket then the inclusion period should be 
                                   based on Acquire & Reacquire Day instead of Value & Expiry Day.Trades that do not have a 
                                   Reacquire Day populated should also be included as these are open ended trades.]
* Department and Desk           : [OPS - GT]
* Requester                     : [Linda Breytenbach]
* Developer                     : [Bushy Ngwako]
* CR Number                     : [CHNGxxxxxxxxxx - ABITFA-4566]
----------------------------------------------------------------------------------------------------------------------------------
----------------------------------------------------------------------------------------------------------------------------------
* Purpose                       : [To include 'ZAG' ISIN on GT and Local Securities filters; Exclude on the Africa Offshore Securities 
                                  and include all ISIN for BAGL fiilter
* Department and Desk           : [OPS - GT]
* Requester                     : [Linda Breytenbach]
* Developer                     : [Bushy Ngwako]
* CR Number                     : [CHNG0004320046 - ABITFA-4595]
----------------------------------------------------------------------------------------------------------------------------------
----------------------------------------------------------------------------------------------------------------------------------
* Purpose                       : [Populate Public Holiday date on the ReportDate fields when tasks run day after holiday] 
* Department and Desk           : [OPS - GT]
* Requester                     : [Linda Breytenbach]
* Developer                     : [Bushy Ngwako]
* CR Number                     : [CHNG0004320046 - ABITFA-4436]
----------------------------------------------------------------------------------------------------------------------------------
----------------------------------------------------------------------------------------------------------------------------------
* Purpose                       : [Security Recon - Amend Report Date]
* Department and Desk           : [OPS - GT]
* Requester                     : [Linda Breytenbach]
* Developer                     : [Bushy Ngwako]
* CR Number                     : [CHNG0004345910 - ABITFA-4717]
----------------------------------------------------------------------------------------------------------------------------------
----------------------------------------------------------------------------------------------------------------------------------
2017-12-20      CHNG0005244993  Willie vd Bank	Modified ISSUER_X_EXCEPTION to include new acquirers for DIS

'''


import acm, ael, csv, os, FRunScriptGUI, re, datetime
import at_choice

# For ReportDate to populate with T-1 date as requested by Business User
TODAY           = ael.date_today().add_banking_day(ael.Calendar['ZAR Johannesburg'], 0)
YESTERDAY       = TODAY.add_days(-1)
TOMORROW        = TODAY.add_banking_day(ael.Calendar['ZAR Johannesburg'], +1)
PREVBUSDAY      = TODAY.add_banking_day(ael.Calendar['ZAR Johannesburg'], -1)
FUNCDATE        = datetime.datetime.today().weekday()

# Issuer Exception Function as required for the "BAGL" Trade filter 
ISSUER_X_EXCEPTION = { 'Position_Recon_BAGL': ['BAGL', 'BAGL ACQUIRER'],
                       'All': ['ABSA BANK LTD', 'GROUP TREASURY']}

CALC_SPACE = acm.Calculations().CreateCalculationSpace(acm.GetDefaultContext(), acm.FTradeSheet)

def ValDayOrAcqDay(trade):
    ''' Function to Use "Acquire Day" instead of "Value day" for Collateral Trades - ABITFA-4052'''
    if trade.TradeCategory() == 'Collateral':
        return trade.AcquireDay()
    else:
        return trade.ValueDay()

        
def insExpDayOrReAcqDay(trade):
    ''' Function to Use "Re-Acquire Day" instead of "Instrument Expiry Day" for Collateral Trades - ABITFA-4052
    '''
    if trade.TradeCategory() == 'Collateral':
        return trade.ReAcquireDay()
    else:
        return trade.Instrument().ExpiryDate()[0:11]


def InstrOrUnderISIN(trade):
        '''Function to get either instrument's or underlying Instrument's ISIN'''
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
    ''' Function to calculate Nominal based on type of instrument '''
    trd = acm.FTrade[trade.Oid()]
    nominal = trd.Nominal()
    instrument = trd.Instrument()
    
    if trd.Instrument().InsType() in ('IndexLinkedBond', 'Bond', 'FRN', 'Bill', 'Zero'):
        if not isAmortizingBond(instrument):
            nominal = trd.Quantity() * trd.Instrument().NominalAmount()
        else :
            nominal = CALC_SPACE.CreateCalculation(trade, 'Current Nominal').Value()
    elif trd.Instrument() and trd.Instrument().InsType() in ('Repo/Reverse', 'SecurityLoan', 'Buy-Sellback') \
                and trd.Instrument().Underlying() and trd.Instrument().Underlying().InsType() in ('IndexLinkedBond', 'Bond', 'FRN', 'Bill', 'Zero'):
        deco = acm.FTradeLogicDecorator(trd, None)
        quantity = deco.QuantityOfUnderlying()
        und_ins_Nom = trd.Instrument().Underlying().NominalAmount()
        nominal = quantity * und_ins_Nom

    #ABITFA-4302
    return round(nominal, 2)



class TradingManagerReport(object):

    def __init__(self, tradeFilter):

        self.trdfltr = tradeFilter
        self.trades = None
        self.rows = {}
        self.rows = {}
        self.listCollateral = []
        self.reportdata = []
        self.groupdata = []
        self.heading = ['', 'Security_Name', 'Settle Category', 'Trade ExternalId', 'Report Date', 'Value Day', 'Ins Expiry Date', 'Trade No',
		        'Mirror Trade', 'Trans Trade',  'Acquirer', 'Counterparty', 'Issuer', 'Instrument Type',
                        'Ins Name', 'Portfolio Name', 'Ins External Id1', 'Ins External Id2', 'ISIN', 
                        'Currency', 'BuySell', 'Total Issue Size', 'Price', 'Security Nominal', 'SND Trade Type', 'SNMI Asset Class', 
                        'SNMI Master Program', 'SNMI STR Reference', 'ECA Number']		


        self.heading_agg = ['', 'Security_Name', 'Report Date', 'Issuer', 'Ins External Id1', 'ISIN', 'Currency', 'Security Nominal', 'Total Issue Size']	
        self.groupheading = ['', 'Security_Name', 'Report Date', 'Issuer', 'Ins External Id1', 'ISIN', 'Currency', 'Security Nominal']	


    
    def GetRows(self):
        ''' Function to handle dictionary for Trades report '''
        
        if self.trdfltr:
            
            
            self.trades = self.trdfltr.Trades()
            '''Get trades of that filter '''
            
            africa_struct_port = acm.FPhysicalPortfolio['Africa Structures'].AllPhysicalPortfolios()
            for trade in self.trades:
            
                ''' Check for Collateral and append to list Else AppendRows [ABITFA-4052] '''
                ''' Also, check correct filter for the right ISIN [ABITFA-4595]'''
                if trade.Instrument().InsType() == 'BasketRepo/Reverse' :
                        connectedTrades = acm.FTrade.Select("connectedTrdnbr=%s"%trade.Oid())
                        for collateralTrade in connectedTrades:
                        
                            if trade.Oid() <> collateralTrade.Oid() and 'ZA' not in collateralTrade.Instrument().Isin() and \
                            self.trdfltr.Name() == 'Position_Recon_AfricaOffshore':
                                if collateralTrade.AcquireDay() <= str(TODAY) and (collateralTrade.ReAcquireDay() >= str(TOMORROW) or \
                                    collateralTrade.ReAcquireDay() is None or collateralTrade.ReAcquireDay() == '' ): 
                                    self.listCollateral.append(collateralTrade)
                                    
                            elif trade.Oid() <> collateralTrade.Oid() and 'ZA' in collateralTrade.Instrument().Isin() and \
                            self.trdfltr.Name() in ('Position_Recon_Local', 'Position_Recon_Group_Treasury'):
                                if trade.Oid() <> collateralTrade.Oid() and 'ZA' in collateralTrade.Instrument().Isin():
                                    if collateralTrade.AcquireDay() <= str(TODAY) and (collateralTrade.ReAcquireDay() >= str(TOMORROW) or \
                                    collateralTrade.ReAcquireDay() is None or collateralTrade.ReAcquireDay() == ''): 
                                        self.listCollateral.append(collateralTrade)
        
                            elif trade.Oid() <> collateralTrade.Oid() and self.trdfltr.Name() == 'Position_Recon_BAGL':
                                if collateralTrade.AcquireDay() <= str(TODAY) and (collateralTrade.ReAcquireDay() >= str(TOMORROW) or \
                                    collateralTrade.ReAcquireDay() is None or collateralTrade.ReAcquireDay() == '' ): 
                                    self.listCollateral.append(collateralTrade)
                                    
                                    
                elif trade.Instrument().InsType() == 'Stock' :
                    if self.trdfltr.Name() == 'Position_Recon_AfricaOffshore' :
                        if trade.Portfolio() in africa_struct_port : 
                            self.listCollateral.append(trade)
                                   
        
                elif trade.TradeCategory() == 'Collateral' : 
                    if trade.AcquireDay() <= str(TODAY) and (trade.ReAcquireDay() >= str(TOMORROW) or trade.ReAcquireDay() is None or \
                    trade.ReAcquireDay() == '' ):
                        self.listCollateral.append(trade)
                else:
                    self.listCollateral.append(trade)

                    


                    
                             
            for colTrd in set(self.listCollateral):
                self.appendRows(colTrd)
                                
    
    def appendRows(self, trd):
    
        ins_or_und = str(InstrOrUnderISIN(trd) if InstrOrUnderISIN(trd) <> None else '')
        ins_or_und = len(ins_or_und) > 12 and ins_or_und[0:12] or ins_or_und
        
        ''' ReportDate Public Holiday check [ABITFA-4436] '''
        
        reportdate = TODAY
        
        
        self.rows.setdefault(ins_or_und, []).append(['',    trd.Instrument().Underlying() and trd.Instrument().Underlying().Name() or trd.Instrument().Name(),
                                                    trd.SettleCategoryChlItem() and trd.SettleCategoryChlItem().Name() or None,   
                                                    trd.OptionalKey(),
                                                    reportdate,
                                                    ValDayOrAcqDay(trd),
                                                    insExpDayOrReAcqDay(trd),
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
                                                    str(trd.add_info('SND_Trade_Type')),
                                                    str(trd.add_info('SNMI_Asset_Class')),
                                                    str(trd.add_info('SNMI_Master_Program')),
                                                    str(trd.add_info('SNMI_STR_Reference')),
                                                    str(trd.add_info('ECA Number')),
                                                ])            


    def GetRows2(self):
        ''' Function to handle dictionary for Aggregated Trades report '''
        if self.trdfltr:
            
            
            self.trades = self.trdfltr.Trades()
            self.rows = {}
            '''Get trades of that filter '''
            
            africa_struct_port = acm.FPhysicalPortfolio['Africa Structures'].AllPhysicalPortfolios()
            for trade in self.trades:
            
                ''' Check for Collateral and append to list Else AppendRows - ABITFA-4052 '''
                if trade.Instrument().InsType() == 'BasketRepo/Reverse' :
                        connectedTrades = acm.FTrade.Select("connectedTrdnbr=%s"%trade.Oid())
                        for collateralTrade in connectedTrades:
                        
                            if trade.Oid() <> collateralTrade.Oid() and 'ZA' not in collateralTrade.Instrument().Isin() and \
                            self.trdfltr.Name() == 'Position_Recon_AfricaOffshore':
                                if collateralTrade.AcquireDay() <= str(TODAY) and (collateralTrade.ReAcquireDay() >= str(TOMORROW) or \
                                    collateralTrade.ReAcquireDay() is None or collateralTrade.ReAcquireDay() == '' ): 
                                    self.listCollateral.append(collateralTrade)
                                    
                            elif trade.Oid() <> collateralTrade.Oid() and 'ZA' in collateralTrade.Instrument().Isin() and \
                            self.trdfltr.Name() in ('Position_Recon_Local', 'Position_Recon_Group_Treasury'):
                                if trade.Oid() <> collateralTrade.Oid() and 'ZA' in collateralTrade.Instrument().Isin():
                                    if collateralTrade.AcquireDay() <= str(TODAY) and (collateralTrade.ReAcquireDay() >= str(TOMORROW) or \
                                    collateralTrade.ReAcquireDay() is None or collateralTrade.ReAcquireDay() == ''): 
                                        self.listCollateral.append(collateralTrade)
        
                            elif trade.Oid() <> collateralTrade.Oid() and self.trdfltr.Name() == 'Position_Recon_BAGL':
                                if collateralTrade.AcquireDay() <= str(TODAY) and (collateralTrade.ReAcquireDay() >= str(TOMORROW) or \
                                    collateralTrade.ReAcquireDay() is None or collateralTrade.ReAcquireDay() == '' ): 
                                    self.listCollateral.append(collateralTrade)
                                    
                elif trade.Instrument().InsType() == 'Stock' :
                    if self.trdfltr.Name() == 'Position_Recon_AfricaOffshore' :
                        if trade.Portfolio() in africa_struct_port : 
                            self.listCollateral.append(trade)
                          
                else:
                    if trade.TradeCategory() == 'Collateral' : 
                        if trade.AcquireDay() <= str(TODAY) and (trade.ReAcquireDay() >= str(TOMORROW) or trade.ReAcquireDay() is None or \
                        trade.ReAcquireDay() == ''):
                            self.listCollateral.append(trade)
                    else:
                        self.listCollateral.append(trade)

                        
            for colTrd in set(self.listCollateral):
                self.appendRows2(colTrd)



    def appendRows2(self, trd):
    
        ins_or_und = str(InstrOrUnderISIN(trd))
        ins_or_und = len(ins_or_und) > 12 and ins_or_und[0:12] or ins_or_und
        
        reportdate = TODAY
        
        self.rows.setdefault(ins_or_und, []).append(['', trd.Instrument().Underlying() and trd.Instrument().Underlying().Name() or trd.Instrument().Name(),   
                                        reportdate,
                                        trd.Instrument().Issuer() and trd.Instrument().Issuer().Name() or None,
                                        trd.Instrument().ExternalId1(),
                                        ins_or_und,
                                        trd.Instrument().Currency() and trd.Instrument().Currency().Name() or None, 
                                        nominal_calc(trd),
                                        trd.Instrument().TotalIssued(),
                                        ])
    
    
    def WriteOutput(self, fileName, filePath ):
        ''' Function to handle grouping and head grouping for Trade Report '''
        outputrows = []
        reportdate = 'Report Date : %s' % (acm.Time.DateToday())

        self.heading[0] = reportdate
        
        self.reportdata.append(self.heading )
        for key in self.rows.keys():
            trdrows = self.rows[key]
            grouprow = None
            
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
            
            isin_ind        = self.heading.index('ISIN')
            isin_val        = reduce(lambda x, y: x or y, [ tr[isin_ind] for tr in trdrows])
            
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
                    grouprow[set_cat_ind]      = set_cat_val
                    grouprow[report_date_ind]  = report_date_val
                    grouprow[issuer_ind]       = issuer_val
                    grouprow[buysell_ind]      = "ISS"
                    grouprow[extern_id1_ind]   = extern_id1_val
                    grouprow[extern_id2_ind]   = extern_id2_val
                    grouprow[isin_ind]         = isin_val
                    grouprow[curr_ind]         = curr_val
                    
                    exclude_issuer = []
                    if self.trdfltr.Name() in ISSUER_X_EXCEPTION: 
                        exclude_issuer = ISSUER_X_EXCEPTION[self.trdfltr.Name()]
                    else:
                            if self.trdfltr.Name() == 'Position_Recon_Local':
                                if extern_id1_val and ('ASN' in extern_id1_val or 'ABN' in extern_id1_val or 'ACL' in extern_id1_val):
                                    exclude_issuer = ISSUER_X_EXCEPTION['All']
                            elif self.trdfltr.Name() == 'Position_Recon_Group_Treasury':
                                if extern_id1_val and 'ASN' not in extern_id1_val and 'ABN' not in extern_id1_val and 'ACL' not in extern_id1_val: 
                                    exclude_issuer = ISSUER_X_EXCEPTION['All']
                            else:
                                exclude_issuer = ISSUER_X_EXCEPTION['All']
                        
                    if issuer_val in exclude_issuer:    
                        grouprow[fac_val_ind]      = total_issu_val
                    else:
                        grouprow[fac_val_ind]       = 0.0
                    
                    self.reportdata.append(grouprow)

                self.reportdata.append(trdrow)

        f = open(getFilePath( filePath, fileName), 'wb')

        recon = csv.writer(f, dialect = 'excel')
        recon.writerows(self.reportdata)
        print getFilePath( filePath, fileName)
        f.close()
       
       
    def WriteOutput_AGG(self, fileName, filePath ):
        ''' Function to handle grouping and head grouping  for Aggregated Trades report'''
        outputrows = []

        reportdate = 'Report Date : %s' % (acm.Time.DateToday())

        self.heading[0] = reportdate

        self.groupdata.append(self.groupheading )
        for key in self.rows.keys():
            trdrows = self.rows[key]
            grouprow = None

            report_date_ind = self.heading_agg.index('Report Date')
            report_date_val = reduce(lambda x, y: x or y, [ tr[report_date_ind] for tr in trdrows])
            
            fac_val_ind     = self.heading_agg.index('Security Nominal')
            total_fac_val   = reduce(lambda x, y: x+y, [ tr[fac_val_ind] for tr in trdrows])

            total_issu_ind  = self.heading_agg.index('Total Issue Size')
            total_issu_val  = reduce(lambda x, y: x or y, [ tr[total_issu_ind] for tr in trdrows])
            
            sec_name_ind    = self.heading_agg.index('Security_Name')
            sec_name_val    = reduce(lambda x, y: x or y, [ tr[sec_name_ind] for tr in trdrows])						
            
            isin_ind        = self.heading_agg.index('ISIN')
            isin_val        = reduce(lambda x, y: x or y, [ tr[isin_ind] for tr in trdrows])
            
            extern_id1_ind  = self.heading_agg.index('Ins External Id1')
            extern_id1_val  = reduce(lambda x, y: x or y, [ tr[extern_id1_ind] for tr in trdrows])
            
            curr_ind        = self.heading_agg.index('Currency')
            curr_val        = reduce(lambda x, y: x or y, [ tr[curr_ind] for tr in trdrows])            

            issuer_ind = self.heading_agg.index('Issuer')
            issuer_val = reduce(lambda x, y: x or y, [ tr[issuer_ind] for tr in trdrows])			

            for trdrow in trdrows:
                if not grouprow:
                    cols                      = len(trdrow) 
                    grouprow                  = [''] * len(trdrow)
                    grouprow[0]               = key
                    grouprow[sec_name_ind]    = "ISSUED NOMINAL"
                    grouprow[issuer_ind]      = issuer_val
                    grouprow[report_date_ind] = report_date_val
                    grouprow[extern_id1_ind]  = extern_id1_val
                    grouprow[isin_ind]        = isin_val
                    grouprow[curr_ind]        = curr_val
                    
                    exclude_issuer = []
                    if self.trdfltr.Name() in ISSUER_X_EXCEPTION: 
                        exclude_issuer = ISSUER_X_EXCEPTION[self.trdfltr.Name()]
                    else:
                            if self.trdfltr.Name() == 'Position_Recon_Local' and 'ASN' in extern_id1_val or 'ABN' in extern_id1_val or \
                                'ACL' in extern_id1_val: 
                                exclude_issuer = ISSUER_X_EXCEPTION['All']
                            elif self.trdfltr.Name() == 'Position_Recon_Group_Treasury' and 'ASN' not in extern_id1_val or 'ABN' not in extern_id1_val \
                                or 'ACL' not in extern_id1_val:
                                exclude_issuer = ISSUER_X_EXCEPTION['All']
                            else:
                                exclude_issuer = ISSUER_X_EXCEPTION['All']

                    if issuer_val in exclude_issuer:
                        grouprow[fac_val_ind]     = total_issu_val
                    else:
                        grouprow[fac_val_ind]     = 0.0
                     
                    grpcols = len(self.groupheading)
                    grpheadrow = [''] * grpcols

                    grpheadrow[0] = key
                    grpheadrow[1] = sec_name_val
                    grpheadrow[2] = report_date_val
                    grpheadrow[3] = issuer_val
                    grpheadrow[4] = extern_id1_val
                    grpheadrow[5] = isin_val
                    grpheadrow[6] = curr_val
                    grpheadrow[7] = total_fac_val
                    
                    self.groupdata.append(grouprow)

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

ael_variables = [ [FILE_NAME_KEY, 'File Name', 'string', None, 'Position_Recon.csv', 1, 1, 'Name of the file.', None, 1],
                  [FILE_PATH_KEY, 'Output Directory', outputSelection, None, outputSelection, 1, 1, 'Directory where the file will be created.', None, 1],
                  [TRADE_FILTER_KEY, 'Filter', 'FTradeSelection', listOfFilters(), 'GT_Recon_Corp', 1, 0, 'select trade filter', None, 1]]


def ael_main(parameters):

    fileName 	= parameters[FILE_NAME_KEY][0]
    filePath 	= parameters[FILE_PATH_KEY]
    trdFilter 	= parameters[TRADE_FILTER_KEY]

    reconReport =  TradingManagerReport(trdFilter)

    reconReport.GetRows()
    reconReport.WriteOutput(fileName, filePath.SelectedDirectory().Text() )
    reconReport.GetRows2()
    reconReport.WriteOutput_AGG(fileName, filePath.SelectedDirectory().Text() )

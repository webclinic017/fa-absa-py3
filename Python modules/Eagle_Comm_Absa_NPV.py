'''----------------------------------------------------------------------------------------------------------------
MODULE
    PS_CommodityMapping
DESCRIPTION
    Developer           : Phumzile Mgcima
    Date                : 2012-11-09
    Purpose             : Creates a count per porfolio and counterparty
    Requestor           : Phumzile Mgcima
    CR Number           : 
ENDDESCRIPTION

HISTORY
    Date:       CR Number:      Developer:              Description:
----------------------------------------------------------------------------------------------------------------'''

import acm
import csv
import sys
import FBDPGui
import FRunScriptGUI
import datetime
import math
from Eagle_Comm_Absa_Util import _insValEnd, _optionDela, get_trades_data, date_from_timestamp, maturitydate_from_timestamp, _TradePresentValue, _LegPresentValue
from decimal import *
import os

directorySelection=FRunScriptGUI.DirectorySelection()
today = acm.Time().DateToday()



class BaseNPV:
    def __init__(self,trade,leg,index=None):
        self.trade = trade
        self.instrument = trade.Instrument()
        self.spaceCollection = self._tradeSpaceCollection()
        self.leg = leg
        self.index = index
        
        
    def _sourceTradeId(self):
        return self.trade.Oid()
        
    def	_legNumber(self):
    #For products besides Swaps, leg refers to an intger(0 or 1) and for Swaps it refers to FLeg object.
        legNumber = self.leg 
        if ((self.instrument.InsType()=='Future/Forward') and ((self.instrument.AdditionalInfo().Commodity_SubAsset()=='Base Metal') 
            or (self.instrument.AdditionalInfo().Commodity_SubAsset()=='Precious Metal'))):
            legNumber = 0
        elif self.instrument.InsType()=='Curr' :
            legNumber = 0
        elif self.instrument.InsType()=='PriceSwap':
            legNumber = self.leg.Oid()
        return legNumber
        
    def	_accountingDate(self):
        return datetime.datetime.strptime(str(today), '%Y-%m-%d').strftime('%Y%m%d')
    
    def	_origCCY1(self):
        return self.trade.Currency().Name()
        
    
    def	_ccy1AmountNPVccy(self):
               
        npv = _TradePresentValue(self.trade)
        
        if self.leg == 1:
            npv = 0
        if self.trade.Instrument().InsType() == 'PriceSwap':
            npv = _LegPresentValue(self.leg, self.trade)
            
        if self.instrument.InsType()=='Curr' :
            npv = npv * self.getExchangeRate(self.trade.Currency().Name())

        if math.isnan(npv):
            npv = 0
            
        return npv
        
    def	_ccy1AmountNPVgbp(self):
        ccyamtgbp = self.getExchangeRate('GBP')*self._ccy1AmountNPVccy()
        if self.instrument.InsType()=='Curr' :
                ccyamtgbp = self._ccy1AmountNPVccy() / self.getExchangeRate(self.trade.Currency().Name()) * self.getExchangeRate('GBP')
        return ccyamtgbp
        
        
    def	_origCCY2(self):
        return ''
        
    def	_ccy2AmountNPVccy(self):
        return ''
        
    def	_ccy2AmountNPVgbp(self):
        return ''
        
    def	_marketRate(self):
        return 0
        
    def	_delta(self):
        
        if self.instrument.InsType() == 'Option':
            delta = 0
            try:
                delta = _optionDela(self.instrument)
                
            except:
                pass
            if math.isnan(delta):
                delta = 0
            return delta
        else:
            return ''
        
        
    def	_latestBalance(self):
        return 0
        
    
    def	_ytdPNL(self):
        return 0
        
    
    def	_accruedInterest(self):
        return 0
        
        
    def	_underlyingCurrentPrice(self):
        return 0
        
    def	_mtmNoPremium(self):
        return self._ccy1AmountNPVccy()
        
    def	_premiumMTM(self):
        return self._ccy1AmountNPVccy()
    
    def	_usdNetNPV(self):
        netPV = self.getExchangeRate('USD')*self._ccy1AmountNPVccy()
        if self.instrument.InsType()=='Curr' :
                netPV = self._ccy1AmountNPVccy()
        return netPV
        
        
    def	_usdAccruedInterest(self):
        return self.getExchangeRate('USD')*self._interestAccrued()
        
    def	_ccy1AmountMTMccy(self):
        return self._ccy1AmountNPVccy()
        
    def	_ccy1AmountMTMusd(self):
        ccyamt = self.getExchangeRate('USD')*self._ccy1AmountNPVccy()
        if self.instrument.InsType()=='Curr' :
                ccyamt = self._ccy1AmountNPVccy()
        return ccyamt
        
        
    def	_ccy2AmountMTMccy(self):
        return 0.00
        
    def	_ccy2AmountMTMusd(self):
        return 0.00
        
    def	_ytdPNLusd(self):
        return 0.00
        
    def	_gamma(self):
        return 0.00
        
    def	_vega(self):
        return 0.00
        
    def	_theta(self):
        return 0.00
        
        
    def	_resevedBrokerage(self):
        return 0.00
        
    def	_reservedBrokerageCurrency(self):
        return self.instrument.Currency().Name()
        
    def	_reservedBrokerageUSD(self):
        return 0.00
    
    def	_npvExcludingPremiumGBP(self):
        return 0.00
    
    def	_accruedInterestGBP(self):
        return 0.00
        
    def	_ytdPNLgbp(self):
        return 0.00
        
        
    def	_accruedEnergyBrokerage(self):
        return 0.00
        
    def	_nextCashSettAmt(self):
        return ''
        
    def	_nextCashSettDate(self):
        return maturitydate_from_timestamp(self.trade.ValueDay())
        
    def	_nextPhysSettAmt(self):
        return ''
    def	_nextPhysSettDate(self):
        return maturitydate_from_timestamp(self.trade.ValueDay())
          
    def	_currentDeliveredPhysMTM(self):
        return ''
    
    def	_todaysCashSettlement(self):
        return ''
        
    def	_todaysPhysicalSettlement(self):
        return ''
    
    def	_currentDeliveredPhysical(self):
        return ''
        
    def	_currentResetAverage(self):
        return ''
        
    def	_currDLVRDphysMTMgbp(self):
        return ''
        
    def	_deliveredPhysCCYequiv(self):
        return ''
        
    def	_settledCCYamt(self):
        return '' 
        

    def _tradeSpaceCollection(self):
        cs = acm.Calculations().CreateStandardCalculationsSpaceCollection()
        
        return cs 
    
    def _mtmValue(self, MTMcurrency):   
        if isinstance(MTMcurrency, str):
            currency = acm.FCurrency[MTMcurrency]
        else:
            currency = MTMcurrency
                
        mtm = 0.0
        try:
            mtm = self.trade.Calculation().PresentValue(self.spaceCollection)
            return mtm.Number()
        except:
            return mtm
            
    def _paymentPV(self):
        pmnts = self.trade.Payments()
        payments_pv = 0.0
        for p in pmnts:
            payments_pv = payments_pv+p.Calculation().PresentValue(self.spaceCollection, self.trade).Number()
            
              
            
        return payments_pv
            
    def getExchangeRate(self, curr):
        curr1 = self.instrument.Currency()
        curr2 = acm.FCurrency[curr]
        #print curr
        #print curr1
        #print curr2
        exRate =  curr1.Calculation().HistoricalFXRate(self.spaceCollection, curr2, today)
        try:
            return exRate.Value().Number()
        except:
            return exRate
        
        
        
    def _interestAccrued(self):
        interest = 0
        try:
            interest = self.trade.Calculation().AccruedInterest(self.spaceCollection).interest.Value().Number()
        except:
            pass
        return interest
        
        
        

    def _timpeStampString(self):
        return datetime.datetime.strptime(str(today), '%Y-%m-%d').strftime('%Y-%m-%d %H:%M:%S')

class CommAbsaNPVReport:
    def __init__(self, file):
        self.file  = file

    def _fieldNames(self):
        fieldNames = ['010',
        'SOURCE_TRADE_ID',
        'LEG_NUMBER',	
        'ACCOUNTING_DATE',	
        'ORIG_CCY1',	
        'CCY1_AMOUNT_NPVCCY',	
        'CCY1_AMOUNT_NPVGBP',	
        'ORIG_CCY2',	
        'CCY2_AMOUNT_NPVCCY',	
        'CCY2_AMOUNT_NPVGBP',	
        'MARKET_RATE',	
        'DELTA',
        'LATEST_BALANCE',
        'YTD_PNL',	
        'ACCRUED_INTEREST',	
        'UNDERLYING_CURRENT_PRICE',	
        'MTM_NO_PREMIUM',	
        'PREMIUM_MTM',	
        'USD_NET_NPV',	
        'USD_ACCRUED_INTEREST',	
        'CCY1AMOUNTMTMCCY',	
        'CCY1AMOUNTMTMUSD',	
        'CCY2AMOUNTMTMCCY',	
        'CCY2AMOUNTMTMUSD',	
        'YTD_PNL_USD',	
        'GAMMA',	
        'VEGA',
        'THETA',	
        'RESERVED_BROKERAGE',	
        'RESERVED_BROKERAGE_CURRENCY',	
        'RESERVED_BROKERAGE_USD',	
        'NPV_excluding_premium_gbp',	
        'Accrued_interest_gbp',	
        'ytd_pnl_gbp',	
        'Accrued energy brokerage gbp',	
        'next_cash_sett_amt',	
        'next_cash_sett_date',
        'next_phys_sett_amt',	
        'next_phys_sett_date',	
        'current_delivered_phys_mtm',	
        'todays_cash_settlement',	
        'todays_physical_settlement',	
        'current_delivered_physical',	
        'CURRENT_RESET_AVERAGE',	
        'CURR_DLVRD_PHYS_MTM_GBP',	
        'delivered_phys_ccy_equiv',	
        'settled_ccy_amt']

        return fieldNames
    
    def _writeHeader(self):
        writer = csv.writer(self.file, delimiter='|', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        fields = ['010', 'JHB', datetime.datetime.strptime(str(today), '%Y-%m-%d').strftime('%Y%m%d')]
        writer.writerow(fields)
        
    def _writeColumnNames(self):
        fieldnames = self._fieldNames()
        try:
            writer = csv.DictWriter(self.file, delimiter='|', fieldnames=fieldnames)
            writer.writerow(dict((fn, fn) for fn in fieldnames))
        
        finally:
            #self.file.close()
            print ''
            
    def _writeNPVRow(self, baseNPV):
        fields = ['030',
            baseNPV._sourceTradeId(),
            baseNPV._legNumber(),
            baseNPV._accountingDate(),
            baseNPV._origCCY1(),
           
            baseNPV._ccy1AmountNPVccy(),
            baseNPV._ccy1AmountNPVgbp(),
            baseNPV._origCCY2(),
            baseNPV._ccy2AmountNPVccy(),
            baseNPV._ccy2AmountNPVgbp(),
            baseNPV._marketRate	(),
            baseNPV._delta(),
            baseNPV._latestBalance(),
            baseNPV._ytdPNL(),
            baseNPV._accruedInterest(),
            baseNPV._underlyingCurrentPrice(),
            baseNPV._mtmNoPremium(),
            baseNPV._premiumMTM	(),
            baseNPV._usdNetNPV(),
            baseNPV._usdAccruedInterest	(),
            baseNPV._ccy1AmountMTMccy(),
            baseNPV._ccy1AmountMTMusd(),
            baseNPV._ccy2AmountMTMccy(),
            baseNPV._ccy2AmountMTMusd(),
            baseNPV._ytdPNLusd(),
            baseNPV._gamma(),
            baseNPV._vega(),
            baseNPV._theta(),
            baseNPV._resevedBrokerage(),
            baseNPV._reservedBrokerageCurrency(),
            baseNPV._reservedBrokerageUSD(),
            baseNPV._npvExcludingPremiumGBP(),
            baseNPV._accruedInterestGBP	(),
            baseNPV._ytdPNLgbp(),
            baseNPV._accruedEnergyBrokerage(),
            baseNPV._nextCashSettAmt(),
            baseNPV._nextCashSettDate(),
            baseNPV._nextPhysSettAmt(),
            baseNPV._nextPhysSettDate(),
            baseNPV._currentDeliveredPhysMTM(),
            baseNPV._todaysCashSettlement(),
            baseNPV._todaysPhysicalSettlement(),
            baseNPV._currentDeliveredPhysical(),
            baseNPV._currentResetAverage(),
            baseNPV._currDLVRDphysMTMgbp(),
            baseNPV._deliveredPhysCCYequiv(),
            baseNPV._settledCCYamt()]
            
        writer = csv.writer(self.file, delimiter='|', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(fields)
        
    def _writeFooter(self, count, checksum):
        writer = csv.writer(self.file, delimiter='|', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        fields = ['090', count, checksum]
        writer.writerow(fields)
           
ael_variables = FBDPGui.DefaultVariables(['filePath', 'File Path', directorySelection, None, directorySelection, 0, 1, 'The file path to the directory where the report should be put. Environment variables can be specified for Windows (%VAR%) or Unix ($VAR).', None, 1]
)
      
def get_filename():
    #date_str = maturitydate_from_timestamp(today)
    return '_'.join(['ABSA_COMM_TDB_NPV']) + '.DAT'

def ael_main(ael_dict):
    
        
    filePath = ael_dict['filePath']
    output_dir = str(ael_dict['filePath'])
    filename = os.path.join(output_dir, get_filename())

    file = open(str(filename), 'wb')  
    
    
    all_trades = get_trades_data()
        
    
    report = CommAbsaNPVReport(file)
    report._writeHeader()
    report._writeColumnNames()
    checksum = Decimal(0)
    check = 0
    count = len(all_trades) 
    for trade in all_trades:
           
        if trade.Instrument().InsType() == 'Future/Forward':
            
            if ((trade.Instrument().AdditionalInfo().Commodity_SubAsset()=='Energy') 
                or (trade.Instrument().AdditionalInfo().Commodity_SubAsset()=='Agri')):
                for i in range(0, 2):
                    
                    baseNPV = BaseNPV(trade, i)
                    report._writeNPVRow(baseNPV)
                    checksum = checksum + Decimal(str(baseNPV._ccy1AmountNPVccy()))
                    if i > 0:
                        count = count + i
                    
            else:
                baseNPV = BaseNPV(trade, 0)
                report._writeNPVRow(baseNPV)
                checksum = checksum + Decimal(str(baseNPV._ccy1AmountNPVccy()))
                
        elif trade.Instrument().InsType() == 'PriceSwap':
                
                j = 0
                for leg in trade.Instrument().Legs():
                    baseNPV = BaseNPV(trade, leg, j)
                    report._writeNPVRow(baseNPV)
                    checksum = checksum + Decimal(str(baseNPV._ccy1AmountNPVccy()))
                    
                    
                    count = count + j
                    j =j+1
     
        else:
            baseNPV = BaseNPV(trade, 0)
            report._writeNPVRow(baseNPV)
            checksum = checksum + Decimal(str(baseNPV._ccy1AmountNPVccy()))
        
           
    
    checksum =checksum
    report._writeFooter(count, '%.2f' % checksum)
    
    
    
    file.close()
    print 'File Created Successfully'
    print 'Wrote secondary output to:::' + str(filePath)+get_filename()

        
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
        

    
    
        

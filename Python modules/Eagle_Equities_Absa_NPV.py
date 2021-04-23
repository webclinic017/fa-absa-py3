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

rundate = datetime.datetime.strptime(today, '%Y-%m-%d').strftime('%Y%m%d')


class BaseNPV:
    def __init__(self,trade,leg,index=None):
        self.trade = trade
        self.instrument = trade.Instrument()
        self.spaceCollection = self._tradeSpaceCollection()
        self.leg = leg
        self.index = index
        
        
    def _sourceTradeId(self):
        if self.trade.Instrument().InsType() == 'Future/Forward':
            return str(self.trade.Oid())+'-'+str(self.leg)
        else:
            return self.trade.Oid()
        
    def	_legNumber(self):
    #For products besides Swaps, leg refers to an intger(0 or 1) and for Swaps it refers to FLeg object.
        legNumber = 0
        if ((self.instrument.InsType()=='Future/Forward')):
            legNumber = self.leg
        elif self.instrument.InsType()=='Option' :
            legNumber = 1
        elif self.instrument.InsType()=='TotalReturnSwap':
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
        if self.trade.Instrument().InsType() == 'TotalReturnSwap':
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
        'TRADE_ID',
        'LEG_NUMBER',	
        'NPV',	
        'NPV_CCY']

        return fieldNames
    
    def _writeHeader(self):
        writer = csv.writer(self.file, delimiter=',', quotechar=',', quoting=csv.QUOTE_MINIMAL)
        fields = ['010', 'JHB', rundate]
        writer.writerow(fields)
        
    def _writeColumnNames(self):
        fieldnames = self._fieldNames()
        try:
            writer = csv.DictWriter(self.file, delimiter=',', fieldnames=fieldnames)
            writer.writerow(dict((fn, fn) for fn in fieldnames))
        
        finally:
            #self.file.close()
            print ''
            
    def _writeNPVRow(self, baseNPV):
        fields = ['030',
            baseNPV._sourceTradeId(),
            baseNPV._legNumber(),
            baseNPV._ccy1AmountNPVccy(),
            baseNPV._origCCY1()]
            
        writer = csv.writer(self.file, delimiter=',', quotechar=',', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(fields)
        
    def _writeFooter(self, count, checksum):
        writer = csv.writer(self.file, delimiter=',', quotechar=',', quoting=csv.QUOTE_MINIMAL)
        fields = ['090', count, checksum]
        writer.writerow(fields)
           
ael_variables = [
['tradeFilter', 'Trade Filters', 'FTradeSelection', acm.FTradeSelection.Select(''), 'Eagle_Equities_DerivsV3', 1, 1],
['filePath', 'File Path', 'string', None, '/services/frontnt/Task/', 0],
['fileName', 'File Name', 'string', None, 'ABSA_EQT_TDB_NPV_'+rundate+'.DAT', 0],]

      
def get_filename():
    #date_str = maturitydate_from_timestamp(today)
    return '_'.join(['ABSA_COMM_TDB_NPV']) + '.DAT'

def ael_main(parameters):
    
        
    filename = parameters['filePath'] + parameters['fileName']

    tfname = parameters['tradeFilter'][0]
    
    file = open(str(filename), 'wb') 
    
    report = CommAbsaNPVReport(file)
    report._writeHeader()
    report._writeColumnNames()
    checksum = Decimal(0)
    check = 0
    count = 0
    i=0
    for trade in  tfname.Trades():
           
        if trade.Instrument().InsType() == 'Future/Forward':
            
            if ((trade.Instrument().AdditionalInfo().Commodity_SubAsset()=='Energy') 
                or (trade.Instrument().AdditionalInfo().Commodity_SubAsset()=='Agri')):

                    baseNPV = BaseNPV(trade, 0)
                    report._writeNPVRow(baseNPV)
                    checksum = checksum + Decimal(str(baseNPV._ccy1AmountNPVccy()))
                    count = count + 1
                    
                    baseNPV = BaseNPV(trade, 1)
                    report._writeNPVRow(baseNPV)
                    checksum = checksum + Decimal(str(baseNPV._ccy1AmountNPVccy()))
                    count = count + 1
                    
            else:
                baseNPV = BaseNPV(trade, 0)
                report._writeNPVRow(baseNPV)
                checksum = checksum + Decimal(str(baseNPV._ccy1AmountNPVccy()))
                count = count + 1

                baseNPV = BaseNPV(trade, 1)
                report._writeNPVRow(baseNPV)
                checksum = checksum + Decimal(str(baseNPV._ccy1AmountNPVccy()))
                count = count + 1

        elif trade.Instrument().InsType() == 'TotalReturnSwap':
                
                j = 0
                for leg in trade.Instrument().Legs():
                    baseNPV = BaseNPV(trade, leg, j)
                    report._writeNPVRow(baseNPV)
                    checksum = checksum + Decimal(str(baseNPV._ccy1AmountNPVccy()))                   
                    count = count + 1
                    j =j+1
     
        else:
            baseNPV = BaseNPV(trade, 0)
            report._writeNPVRow(baseNPV)
            checksum = checksum + Decimal(str(baseNPV._ccy1AmountNPVccy()))
            count = count + 1

           
    
    checksum =checksum
    report._writeFooter(count, '%.2f' % checksum)
    
    
    
    file.close()
    print 'File Created Successfully'
    print 'Wrote secondary output to:::' + filename
        
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
        

    
    
        

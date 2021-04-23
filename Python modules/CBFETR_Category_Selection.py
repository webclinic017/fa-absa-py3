'''----------------------------------------------------------------------------------------------------------
MODULE                  :       CBFETR_Category_Selection
PROJECT                 :       Cross Border Foreign Exchange Transaction Reporting
PURPOSE                 :       This module contains all the specific CBFETR Category rules that should apply.
DEPARTMENT AND DESK     :       Operations
REQUASTER               :       CBFETR Project
DEVELOPER               :       Heinrich Cronje
CR NUMBER               :       235281
-------------------------------------------------------------------------------------------------------------

HISTORY
=============================================================================================================
Date            Change no       Developer                       Description
-------------------------------------------------------------------------------------------------------------
2012-02-22      235281          Heinrich Cronje                 Initial Implementation
2013-08-17      CHNG0001209844  Heinrich Cronje                 BOPCUS 3 Upgrade
2013-08-20      CHNG0001274026  Heinrich Cronje                 Post Production Changes - Changed ETF Category
                                                                and Priority
2014-06-19                      Melusi Maseko                   Pull through Palladium trades ABITFA-2620
                                                                ETF and Gold Enhancements FXMW-428
2015-02-12      JIRA BOP-3      Melusi Maseko                   Remove 'BARCLAYS BANK PLC','BARCLAYS BNK PLC GERMISTON' from the existing rule
                                                                Exclude all CFC account transactions which should be reported as 'Non Reportable'
2015-03-25      BOP-15          Melusi Maseko                   NewGold & NewPlat ETF Secondary Listings

2015-05-05                      Kirsten Good                    BARX Fixed and Call Deposits - Non ZAR set to Non Reportable

2015-12-04      MINT-456        Melusi Maseko                   Changed Category.CATEGORY_MAPPING to make use of new method  defined in CBFETR_Category_Mapping
-------------------------------------------------------------------------------------------------------------

DESCRIPTION OF MODULE:

    Category rules are applied from most important to least in the following manner:
    
    1 - Precious Metals Import/Exports
    2 - ETF in Africa Currencies except ZAR.
    3 - Interbank Deals
    4 - Termination Feeds on the following type for Deposits: FDC, FDE, FDI, FLI, FTL
    5 - Future/Forwards
    6 - Mapping matrix for all money flows that passed above rules.
'''

import acm
import CBFETR_Parameters as Params
import CBFETR_Category_Mapping as Category

class CBFETR_Category_Selection():
    def __init__(self, moneyFlow, trade):
        self.MoneyFlow = moneyFlow
        self.Trade = trade
        self.Instrument = self.Trade.Instrument()
        self.InsType = self.Instrument.InsType()
        self.Counterparty = self.MoneyFlow.Counterparty()
        self.Category = None
        self.Gold_Import = False
        self.Platinum_Import = False
        self.Silver_Import = False
        self.Palladium_Import = False
        self.Gold_Export = False
        self.Platinum_Export = False
        self.Silver_Export = False
        self.Palladium_Export = False
        self.is_Gold_Import()
        self.is_Platinum_Import()
        self.is_Silver_Import()
        self.is_Palladium_Import()
        self.is_Gold_Export()
        self.is_Platinum_Export()
        self.is_Silver_Export()
        self.is_Palladium_Export()
        self.get_Category()
    
    def is_Gold_Import(self):
        if self.InsType == 'Curr' and self.Instrument.Currency().Name() == 'XAU' and self.Trade.Portfolio().Name() == 'OTC GOLD' and self.Trade.Quantity() > 0:
            self.Gold_Import = True
    
    def is_Platinum_Import(self):
        if self.InsType == 'Curr' and self.Instrument.Currency().Name() == 'XPT' and self.Trade.Portfolio().Name() == 'OTC Platinum' and self.Trade.Quantity() > 0:
            self.Platinum_Import = True

    def is_Silver_Import(self):
        if self.InsType == 'Curr' and self.Instrument.Currency().Name() == 'XAG' and self.Trade.Portfolio().Name() == 'OTC Silver' and self.Trade.Quantity() > 0:
            self.Silver_Import = True

    def is_Palladium_Import(self):
        if self.InsType == 'Curr' and self.Instrument.Currency().Name() == 'XPD' and self.Trade.Portfolio().Name() == 'OTC Palladium' and self.Trade.Quantity() > 0:
            self.Palladium_Import = True
            
    def is_Gold_Export(self):
        if self.InsType == 'Curr' and self.Instrument.Currency().Name() == 'XAU' and self.Trade.Portfolio().Name() == 'OTC GOLD' and self.Trade.Quantity() < 0:
            self.Gold_Export = True
    
    def is_Platinum_Export(self):
        if self.InsType == 'Curr' and self.Instrument.Currency().Name() == 'XPT' and self.Trade.Portfolio().Name() == 'OTC Platinum' and self.Trade.Quantity() < 0:
            self.Platinum_Export = True

    def is_Silver_Export(self):
        if self.InsType == 'Curr' and self.Instrument.Currency().Name() == 'XAG' and self.Trade.Portfolio().Name() == 'OTC Silver' and self.Trade.Quantity() < 0:
            self.Silver_Export = True

    def is_Palladium_Export(self):
        if self.InsType == 'Curr' and self.Instrument.Currency().Name() == 'XPD' and self.Trade.Portfolio().Name() == 'OTC Palladium' and self.Trade.Quantity() < 0:
            self.Palladium_Export = True
            
    def get_Category(self):
        moneyFlowType = self.MoneyFlow.Type()


        '''---------------------------------------------------------
            BARX Fixed and Call Deposits - Non ZAR
        ---------------------------------------------------------'''
        if self.InsType in ('Deposit'):
            if self.Trade.OptionalKey().upper().startswith('BARXMM') and self.MoneyFlow.Currency().Name() <> 'ZAR':
                self.Category = '900'
                return
        
        '''--------------------------------------------------------------
                                Precious Metals Imports / Export
        --------------------------------------------------------------'''
        if self.Silver_Import == True or self.Silver_Export == True or self.Gold_Import == True or self.Gold_Export == True or self.Platinum_Import == True \
            or self.Platinum_Export == True or self.Palladium_Import == True or self.Palladium_Export == True:
            self.Category = '109'
            if self.Trade.Counterparty().BusinessStatus():
                if self.Trade.Counterparty().BusinessStatus().Name() <> 'Interbank':
                    self.Category = '900'
            
            if self.Trade.Counterparty().Country()== 'SOUTH AFRICA':
                self.Category = '900'
            return
            
        '''---------------------------------------------------------
                                ETF
        ---------------------------------------------------------'''
        if self.InsType == 'ETF' and self.MoneyFlow.Currency().Name() in Params.AFRICAN_CURRENCIES:
            self.Category = Category.get_Category_Mapping(acm.EnumFromString('SettlementCashFlowType', moneyFlowType))[acm.EnumFromString('InsType', self.InsType)]
            return

        '''---------------------------------------------------------
                            Interbank Deals
        ---------------------------------------------------------'''
        if self.InsType != 'TotalReturnSwap':
            businessStatus = self.Counterparty.BusinessStatus()
            if businessStatus and businessStatus.Name() == 'Interbank':
                self.Category = '900'
                return

        '''---------------------------------------------------------
                            Inward Listings
        ---------------------------------------------------------'''
        '''
        if self.Instrument.ExternalId2().__contains__('Inward Listed'):
            if self.InsType == 'Equity':
                return '610'
            elif self.InsType == 'CLN':
                return '611'
            return '612'
        '''
        '''---------------------------------------------------------
                    Funding Instype Deposit Override
        ---------------------------------------------------------'''
        if moneyFlowType == 'Termination Fee' and self.InsType == 'Deposit':
            fundingInsType = self.Trade.add_info('Funding Instype')
            if fundingInsType in Params.FUNDING_INSTYPE_OVERRIDES:
                self.Category = '287'
                return
        
        '''---------------------------------------------------------
                                FX Swaps
        ---------------------------------------------------------'''
        '''
        if self.InsType == 'Curr' and self.Trade.TradeProcess() in (16384,32768):
            self.Category = '900'
            return
        '''
            
        '''---------------------------------------------------------
                            Future Forwards
        ---------------------------------------------------------'''
        if self.InsType == 'Future/Forward':
            self.Category = '900'
            return
            
        '''---------------------------------------------------------
                            Category Mapping
        ---------------------------------------------------------'''
        if not self.Category:
            self.Category = Category.get_Category_Mapping(acm.EnumFromString('SettlementCashFlowType', moneyFlowType))[acm.EnumFromString('InsType', self.InsType)]

        '''---------------------------------------------------------
                        Instrument Product Mapping
        ---------------------------------------------------------'''
        #if not self.Category:
        #    product = Category.INSTRUMENT_PRODUCT_MAPPING[insType]
        #    self.Category = Category.PRODUCT_CODE[product]


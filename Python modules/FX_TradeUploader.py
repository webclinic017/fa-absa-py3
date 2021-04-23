from xml.etree import ElementTree
import acm, csv, FRunScriptGUI, sys, os, datetime
'''--------------------------------------------------------------------------------------------------------
Date                    : 2011-09-26
Purpose                 : This script retrieves trade data from TMS using MX connector. Then books the trades in Front Arena
Department and Desk     : Front Office - FX Option
Requester               : Justin Nichols and Wesley Sukdao
Developer               : Rohan van der Walt
CR Number               : 713436
--------------------------------------------------------------------------------------------------------

HISTORY
================================================================================
Date       Change no Developer                 Description
--------------------------------------------------------------------------------
2011-09-26 713436    Rohan vd Walt             Initial Implementation
2012-02-14 891689    Rohan van der Walt        Add Trade Process number on FX Forward trades so that Midbase flow works correctly
2012-02-20 XXXXXX    Rohan van der Walt        Set Strike Quotation on FX Option Instrument
2014-06-04 XXXXXX    Mohamed Ismail            Changed Moniker to point to BARX TS
2015-02-24 XXXXXX    Anwar Banoo               Updated script with to choose the MX version to default to
2015-02-25 XXXXXX    Edmundo Chissungo         Fixed a global name issue and set default MX version to 0
2015-06-19 XXXXXX    Gavin Brennan             Expanded scope to cover barrier options and digitals, includes code from Nico to cancel trades
'''

def deleteTrade(optional_key):
    # Create query
    query = acm.CreateFASQLQuery(acm.FTrade, 'AND')
    query.AddAttrNode('OptionalKey', 'EQUAL', optional_key)
    try:
        # Get first result in query as this is a unique key and should return 
        # one or zero trades.
        trade = query.Select()[0]
        trdNbr = trade.Oid()
        trade.Delete()
        
        print 'Deleted trade: %s successfully' % trdNbr
        
    except Exception, e:
        # Throws Index out of bounds error if trade does not exist with
        # the passed in optional key.
        print 'Failed to delete trade. Either the trade does not exist or it cannot be deleted. See error below.'
        print e.__repr__()


def getOperatingEnvironment():
    if str(acm.Class()) == 'FTmServer':
        return 'Frontend'
    else:
        return 'Backend'
        
def getMXApiVersion():        
    if os.path.exists('C:\Program Files (x86)'):
        MXApiVersion = '700'
    else:
        MXApiVersion = '600'
    #print 'Using TX Version %s' %MXApiVersion
    return MXApiVersion

if getOperatingEnvironment() == "Frontend":
    import sys
    sys.path.append(r'Y:\Jhb\Arena\CommonLib\PythonLib26\site-packages\win32com')
    import win32com, win32com.client

GMT_PREFIX = r"{http://gmt/Schema/TradeCommon/2.Murex}"
ABSAJBG = '40010879'
ADJUST = '40078188'
fileSelection = FRunScriptGUI.InputFileSelection()
fileSelection.FileFilter('CSV Files (*.csv)|*.csv')

class MXConnection():
    def __init__(self, env):
        if getOperatingEnvironment() == "Frontend":
            self.MXSessionFactory = win32com.client.Dispatch('MXApi.MXSessionFactory.%s' %getMXApiVersion()).Create(env)
            
    def getTradeData(self, BARXTSSource, MurexTrdnbr):
        '''
        Returns XML trade data from mx moniker query
        '''
        try:
            mxMoniker = win32com.client.Dispatch('MXApi.MXMoniker.%s' %getMXApiVersion())
            '''mxMoniker.ParseDisplayName('official/trade.fx/global/murex/' + str(MurexTrdnbr))'''
            if BARXTSSource == "Yes":
                '''print 'official/trade.fx/global/barxfxts/'''
                mxMoniker.ParseDisplayName('official/trade.fx/global/barxfxts/' + str(MurexTrdnbr))
            else:
                '''print 'official/trade.fx/global/murex/'''
                mxMoniker.ParseDisplayName('official/trade.fx/global/murex/' + str(MurexTrdnbr))
            objRef = win32com.client.Dispatch('MXApi.MXObjRef.%s' %getMXApiVersion())
            objRef.Attach(self.MXSessionFactory, mxMoniker)
            if objRef.Exists():
                objRef.Load()
                message = objRef.Instance
                return message.Content
            else:
                return None
        except Exception, e:
            if BARXTSSource == "Yes":
                print 'Error occured when trying to get Trade Data from BARX FX TS %s from TMS\n' % MurexTrdnbr, e
            else:
                print 'Error occured when trying to get Trade Data from MurexId %s from TMS\n' % MurexTrdnbr, e
            raise e

class FXForwardTrade():
    def __init__(self, datadict = None):
        '''
        Using the trade dictionary, create a new FXOTrade object mapping the murex values to Front Arena.
        Also do some data verification checks.
        '''    
        if ( not datadict):
            datadict = {}
            
        self.Details = datadict
   
    def CreateTrade(self): 
        t = acm.FTrade()
        t.Instrument( acm.FCurrency[self.Details['BaseCurrency']] )
        t.Currency( acm.FCurrency[self.Details['QuotedCurrency']] )
        t.Price( float(self.Details['Rate']) )
        if self.Details['Reversed'] == "No":
            if self.Details['AmountCurrency'] == self.Details['BaseCurrency']:
                t.Quantity( -1 * float(self.Details['Amount'] ))
                t.Premium( float(self.Details['Amount']) * float(self.Details['Rate']) )
            else:
                t.Quantity( float(self.Details['Amount']) / float(self.Details['Rate']) ) 
                t.Premium( -1 * float(self.Details['Amount']) )
        elif self.Details['Reversed'] == "Yes":
            if self.Details['AmountCurrency'] == self.Details['BaseCurrency']:
                t.Quantity( float(self.Details['Amount'] ))
                t.Premium( (-1 * float(self.Details['Amount'])) * float(self.Details['Rate']) )
            else:
                t.Quantity( (-1 * float(self.Details['Amount'])) / float(self.Details['Rate']) ) 
                t.Premium( float(self.Details['Amount']) )
        t.TradeTime( self.Details['TradeDate'] )
        t.ValueDay( self.Details['ForwardDate'] )
        t.AcquireDay( self.Details['PaymentDate'] )
        if self.Details['SetOptionalKeys'] == "Yes":        
            if self.Details['BARXTSSource'] == "Yes":
                t.OptionalKey('BARXTS_' + self.Details['TradeID']) #Sets ExternalID to murex.originTradeId
            else:
                t.OptionalKey('MUREX_' + self.Details['TradeID']) #Sets ExternalID to murex.originTradeId
        t.Trader(acm.FUser[self.Details['Trader']])
        t.Counterparty(self.Details['Counterparty'])
        t.Acquirer(self.Details['Acquirer'])
        t.Portfolio(self.Details['FAPortfolio'])
        t.Status(self.Details['Status'])
        t.TradeProcess(8192)
        t.Type('Normal')
        t.DiscountingType('CCYBasis')
        t.Commit()
        return t.Instrument().Name(), t.Name()
 
class FXOTrade():
    def __init__(self, datadict = None):
        '''
        Using the trade dictionary, create a new FXOTrade object mapping the murex values to Front Arena.
        Also do some data verification checks.
        '''    
        if ( not datadict):
            datadict = {}        
        self.Details = datadict
        self.CutCodeMapping = {'NY':acm.FParty['NY 10:00 am'],
                               'TKY':acm.FParty['TK 3:00 pm'],
                               'ECB':acm.FParty['ECB 2:15 pm'],
                               'WMR':acm.FParty['WMR 4:00 pm']}
        
    @staticmethod
    def getPremiumDateAmountCurrency(flowlist):
        for flow in flowlist:
            if flow.attrib[GMT_PREFIX+'FlowType'] == "Premium":
                dt = flow.attrib[GMT_PREFIX+'Date']
                amt = flow.find(GMT_PREFIX+'Amount').text
                cur = flow.find(GMT_PREFIX+'Currency').attrib[GMT_PREFIX+'Id']
                return (dt, amt, cur)
                
    def CreateTrade(self): 
        insOriginal = acm.FOption()
        businessLogicGUIDefaultHandler = acm.FBusinessLogicGUIDefault()
        businessLogicGUIDefaultHandler.AskAdjustToFollowingBusinessDay(True)
        businessLogicGUIDefaultHandler.AskAdjustAcquireDate(True)
        businessLogicGUIDefaultHandler.AskAdjustValueDate(True)
        insDecorator = acm.FOptionDecorator(insOriginal, businessLogicGUIDefaultHandler)
        defaultID = 'Option-Curr-Default'
        defaultIns = acm.FOption[defaultID]
        insDecorator.ValuationGrpChlItem(defaultIns.ValuationGrpChlItem())
        insDecorator.PayType(defaultIns.PayType())
        insDecorator.ExpiryDate(self.Details['ExpiryEventDate'])
        insDecorator.DeliveryDate(self.Details['PayoffDate'])
        insDecorator.OptionType(self.Details['CallPut'])
        insDecorator.Currency(acm.FCurrency[self.Details['EconomicUnderlyingCurrency']])                 #Trade Currency
        insDecorator.DomesticCurrency(acm.FCurrency[self.Details['EconomicUnderlyingCurrency']])
        insDecorator.ForeignCurrency(acm.FCurrency[self.Details['EconomicBaseCurrency']])
        insDecorator.ExerciseType(self.Details['OptionType'])
        insDecorator.StrikePrice(float(self.Details['Strike']))
        insDecorator.StrikeType('Absolute')
        insDecorator.StrikeQuotation(acm.FQuotation['Per Unit'])
        insDecorator.StrikeCurrency(acm.FCurrency[self.Details['EconomicUnderlyingCurrency']])
        insDecorator.OriginalCurrency(acm.FCurrency[self.Details['EconomicBaseCurrency']])
        insDecorator.FixingSource(self.CutCodeMapping[self.Details['ExpiryEventCutCode']])
        insDecorator.FxoPremiumCurr(acm.FCurrency[self.Details['PremiumCurrency']])
        insOriginal.RegisterInStorage()   
        #Re-apply Delivery Date since dual Currency rule overrides 
        acm.PollDbEvents()
        insDecorator.DeliveryDate(self.Details['PayoffDate'])        
        insDecorator.SettlementType(acm.FEnumeration['enum(settlementTypeShortName)'].Enumeration('Physical') if self.Details['PayoffType'] == 'Asset' else acm.FEnumeration['enum(settlementTypeShortName)'].Enumeration('Cash'))
        insOriginal.Commit()
        
        tradeOrig = acm.FTrade()
        tradeClone = tradeOrig.Clone()
        tradeClone.Type('Normal')
        tradeDecorator = acm.FTradeLogicDecorator(tradeClone, businessLogicGUIDefaultHandler)
        tradeDecorator.Instrument(insOriginal)
        tradeDecorator.Trader(acm.FUser[self.Details['Trader']])
        tradeDecorator.Counterparty(self.Details['Counterparty'])
        tradeDecorator.Acquirer(self.Details['Acquirer'])
        tradeDecorator.Portfolio(self.Details['FAPortfolio'])
        tradeDecorator.Status(self.Details['Status'])
        tradeDecorator.TradeTime(self.Details['TradeDate'])
        tradeDecorator.ValueDay(self.Details['PremiumDate'])
        tradeDecorator.Currency(acm.FCurrency[self.Details['PremiumCurrency']])
        tradeCalc = tradeDecorator.Calculation()
        calcSpace = acm.Calculations().CreateStandardCalculationsSpaceCollection()
        tradeDecorator.FxoPremiumCurr(acm.FCurrency[self.Details['PremiumCurrency']])
        if self.Details['Reversed'] == "No":
            tradeDecorator.AmountDomestic(float(self.Details['Amount']) if self.Details['BuyOrSell'] == "Buy" else -1 * float(self.Details['Amount']))
            tradeDecorator.Premium(float(self.Details['PremiumAmount']) if self.Details['BuyOrSell'] == "Sell" else -1 * float(self.Details['PremiumAmount']))
        elif self.Details['Reversed'] == "Yes":
            tradeDecorator.AmountDomestic((-1 * float(self.Details['Amount'])) if self.Details['BuyOrSell'] == "Buy" else float(self.Details['Amount']))
            tradeDecorator.Premium((-1 * float(self.Details['PremiumAmount'])) if self.Details['BuyOrSell'] == "Sell" else float(self.Details['PremiumAmount']))
        tradeDecorator.Price(tradeCalc.PremiumToPrice(calcSpace, acm.Time().DateToday(), tradeDecorator.Premium()).Number())
        tradeDecorator.ValueDay(self.Details['PremiumDate'])
        
        if self.Details['SetOptionalKeys'] == "Yes":
            if self.Details['BARXTSSource'] == "Yes":
                tradeDecorator.OptionalKey('BARXTS_' + self.Details['TradeID']) #Sets ExternalID to murex.originTradeId
            else:
                tradeDecorator.OptionalKey('MUREX_' + self.Details['TradeID']) #Sets ExternalID to murex.originTradeId
        tradeOrig.Apply(tradeClone)
        tradeOrig.Commit()
        return insOriginal.Name(), tradeOrig.Name()

class DigitalEuropeanTrade():
    def __init__(self, datadict = None):
        '''
        Using the trade dictionary, create a new FXOTrade object mapping the murex values to Front Arena.
        Also do some data verification checks.
        '''    
        if ( not datadict):
            datadict = {}        
        self.Details = datadict
        self.CutCodeMapping = {'NY':acm.FParty['NY 10:00 am'],
                               'TKY':acm.FParty['TK 3:00 pm'],
                               'ECB':acm.FParty['ECB 2:15 pm'],
                               'WMR':acm.FParty['WMR 4:00 pm']}
        
    @staticmethod
    def getPremiumDateAmountCurrency(flowlist):
        for flow in flowlist:
            if flow.attrib[GMT_PREFIX+'FlowType'] == "Premium":
                dt = flow.attrib[GMT_PREFIX+'Date']
                amt = flow.find(GMT_PREFIX+'Amount').text
                cur = flow.find(GMT_PREFIX+'Currency').attrib[GMT_PREFIX+'Id']
                return (dt, amt, cur)
                
    def CreateTrade(self): 
        insOriginal = acm.FOption()
        businessLogicGUIDefaultHandler = acm.FBusinessLogicGUIDefault()
        businessLogicGUIDefaultHandler.AskAdjustToFollowingBusinessDay(True)
        businessLogicGUIDefaultHandler.AskAdjustAcquireDate(True)
        businessLogicGUIDefaultHandler.AskAdjustValueDate(True)
        insDecorator = acm.FOptionDecorator(insOriginal, businessLogicGUIDefaultHandler)
        defaultID = 'Option-Curr-Default'
        defaultIns = acm.FOption[defaultID]        

        insDecorator.ValuationGrpChlItem(defaultIns.ValuationGrpChlItem())
        insDecorator.PayType(defaultIns.PayType())
        insDecorator.SettlementType(acm.FEnumeration['enum(settlementTypeShortName)'].Enumeration('Physical') if self.Details['PayoffType'] == 'Asset' else acm.FEnumeration['enum(settlementTypeShortName)'].Enumeration('Cash'))
        insDecorator.ExpiryDate(self.Details['ExpiryEventDate'])
        insDecorator.DeliveryDate(self.Details['PayoffDate'])
        insDecorator.OptionType('Call' if self.Details['CallPut']=='DigitalCall' else 'Put')
        insDecorator.Currency(acm.FCurrency[self.Details['EconomicUnderlyingCurrency']])                 #Trade Currency
        insDecorator.DomesticCurrency(acm.FCurrency[self.Details['EconomicUnderlyingCurrency']])
        insDecorator.ForeignCurrency(acm.FCurrency[self.Details['EconomicBaseCurrency']])
        insDecorator.ExerciseType(self.Details['OptionType'])
        insDecorator.StrikePrice(float(self.Details['Strike']))
        insDecorator.StrikeType('Absolute')
        insDecorator.StrikeQuotation(acm.FQuotation['Per Unit'])
        insDecorator.StrikeCurrency(acm.FCurrency[self.Details['EconomicUnderlyingCurrency']])
        insDecorator.OriginalCurrency(acm.FCurrency[self.Details['EconomicBaseCurrency']])
        insDecorator.FixingSource(self.CutCodeMapping[self.Details['ExpiryEventCutCode']])
        insDecorator.FxoPremiumCurr(acm.FCurrency[self.Details['PremiumCurrency']])
        
        insOriginal.RegisterInStorage()
        
        insDecorator.SettlementType(acm.FEnumeration['enum(settlementTypeShortName)'].Enumeration('Physical') if self.Details['PayoffType'] == 'Asset' else acm.FEnumeration['enum(settlementTypeShortName)'].Enumeration('Cash'))
        insDecorator.Exotic().BaseType(acm.FEnumeration['enum(ExoticBaseType)'].Enumeration('Digital European'))
        #Re-apply Delivery Date since duel Currency rule overrides 
        acm.PollDbEvents()
        insDecorator.DeliveryDate(self.Details['PayoffDate'])        
        insDecorator.StrikePrice(float(self.Details['Strike']))
        insOriginal.Commit()

        tradeOrig = acm.FTrade()
        tradeClone = tradeOrig.Clone()
        tradeClone.Type('Normal')
        tradeDecorator = acm.FTradeLogicDecorator(tradeClone, businessLogicGUIDefaultHandler)
        tradeDecorator.Instrument(insOriginal)
        tradeDecorator.Trader(acm.FUser[self.Details['Trader']])
        tradeDecorator.Counterparty(self.Details['Counterparty'])
        tradeDecorator.Acquirer(self.Details['Acquirer'])
        tradeDecorator.Portfolio(self.Details['FAPortfolio'])
        tradeDecorator.Status(self.Details['Status'])
        tradeDecorator.TradeTime(self.Details['TradeDate'])
        tradeDecorator.ValueDay(self.Details['PremiumDate'])
        tradeDecorator.Currency(acm.FCurrency[self.Details['PremiumCurrency']])
        tradeCalc = tradeDecorator.Calculation()
        calcSpace = acm.Calculations().CreateStandardCalculationsSpaceCollection()
        tradeDecorator.FxoPremiumCurr(acm.FCurrency[self.Details['PremiumCurrency']])
        if self.Details['Reversed'] == "No":
            tradeDecorator.AmountDomestic(float(self.Details['Amount']) if self.Details['BuyOrSell'] == "Buy" else -1 * float(self.Details['Amount']))
            tradeDecorator.Premium(float(self.Details['PremiumAmount']) if self.Details['BuyOrSell'] == "Sell" else -1 * float(self.Details['PremiumAmount']))
        elif self.Details['Reversed'] == "Yes":
            tradeDecorator.AmountDomestic((-1 * float(self.Details['Amount'])) if self.Details['BuyOrSell'] == "Buy" else float(self.Details['Amount']))
            tradeDecorator.Premium((-1 * float(self.Details['PremiumAmount'])) if self.Details['BuyOrSell'] == "Sell" else float(self.Details['PremiumAmount']))
        tradeDecorator.Price(tradeCalc.PremiumToPrice(calcSpace, acm.Time().DateToday(), tradeDecorator.Premium()).Number())
        
        if self.Details['SetOptionalKeys'] == "Yes":
            if self.Details['BARXTSSource'] == "Yes":
                tradeDecorator.OptionalKey('BARXTS_' + self.Details['TradeID']) #Sets ExternalID to murex.originTradeId
            else:
                tradeDecorator.OptionalKey('MUREX_' + self.Details['TradeID']) #Sets ExternalID to murex.originTradeId
        tradeOrig.Apply(tradeClone)
        tradeOrig.Commit()
        return insOriginal.Name(), tradeOrig.Name()

class FXOSingleBarrierTrade():
    def __init__(self, datadict = None):
        '''
        Using the trade dictionary, create a new FXOTrade object mapping the murex values to Front Arena.
        Also do some data verification checks.
        '''    
        if ( not datadict):
            datadict = {}        
        self.Details = datadict
        self.CutCodeMapping = {'NY':acm.FParty['NY 10:00 am'],
                               'TKY':acm.FParty['TK 3:00 pm'],
                               'ECB':acm.FParty['ECB 2:15 pm'],
                               'ECB37 Mid':acm.FParty['ECB 2:15 pm'],
                               'WMR':acm.FParty['WMR 4:00 pm']}
        
    @staticmethod
    def getPremiumDateAmountCurrency(flowlist):
        for flow in flowlist:
            if flow.attrib[GMT_PREFIX+'FlowType'] == "Premium":
                dt = flow.attrib[GMT_PREFIX+'Date']
                amt = flow.find(GMT_PREFIX+'Amount').text
                cur = flow.find(GMT_PREFIX+'Currency').attrib[GMT_PREFIX+'Id']
                return (dt, amt, cur)
            
    def CreateTrade(self): 
        insOriginal = acm.FOption()
        businessLogicGUIDefaultHandler = acm.FBusinessLogicGUIDefault()
        businessLogicGUIDefaultHandler.AskAdjustToFollowingBusinessDay(True)
        businessLogicGUIDefaultHandler.AskAdjustAcquireDate(True)
        businessLogicGUIDefaultHandler.AskAdjustValueDate(True)
        insDecorator = acm.FOptionDecorator(insOriginal, businessLogicGUIDefaultHandler)
        defaultID = 'Option-Curr-Default'
        defaultIns = acm.FOption[defaultID]
        insDecorator.StrikePrice(float(self.Details['Strike']))
        insDecorator.StrikeType('Absolute')
        insDecorator.StrikeQuotation(acm.FQuotation['Per Unit'])
        insDecorator.ValuationGrpChlItem(defaultIns.ValuationGrpChlItem())
        insDecorator.PayType(defaultIns.PayType())
        insDecorator.SettlementType(acm.FEnumeration['enum(settlementTypeShortName)'].Enumeration('Physical') if self.Details['PayoffType'] == 'Asset' else acm.FEnumeration['enum(settlementTypeShortName)'].Enumeration('Cash'))
        insDecorator.ExpiryDate(self.Details['ExpiryEventDate'])        
        insDecorator.DeliveryDate(self.Details['PayoffDate'])
        insDecorator.OptionType(self.Details['CallPut'])
        insDecorator.Currency(acm.FCurrency[self.Details['EconomicUnderlyingCurrency']])                 #Trade Currency
        insDecorator.DomesticCurrency(acm.FCurrency[self.Details['EconomicUnderlyingCurrency']])
        insDecorator.ForeignCurrency(acm.FCurrency[self.Details['EconomicBaseCurrency']])

        insDecorator.StrikePrice(float(self.Details['Strike']))
        insDecorator.StrikeType('Absolute')
        insDecorator.StrikeQuotation(acm.FQuotation['Per Unit'])
        insDecorator.StrikeCurrency(acm.FCurrency[self.Details['EconomicUnderlyingCurrency']])
        insDecorator.OriginalCurrency(acm.FCurrency[self.Details['EconomicBaseCurrency']])
        
        if (self.Details['FixingSource']=='' or self.Details['FixingSource']=='SPOTMARKET Mid'):
            insDecorator.FixingSource(self.CutCodeMapping[self.Details['ExpiryEventCutCode']])
        else:
            insDecorator.FixingSource(self.CutCodeMapping[self.Details['FixingSource']])
            
        insDecorator.FxoPremiumCurr(acm.FCurrency[self.Details['PremiumCurrency']])
        insDecorator.Barrier(float(self.Details['BarrierLevel']))
        insDecorator.Rebate(float(self.Details['Rebate']))
        insDecorator.ContractSize(1)
        insDecorator.QuoteType(acm.FEnumeration['enum(QuoteType)'].Enumeration('Per Unit'))
        insDecorator.ExerciseType(acm.FEnumeration['enum(ExerciseType)'].Enumeration('European')) #European
        
        insOriginal.RegisterInStorage()      
        
        exoDecorator = insDecorator.Exotic()
        exoDecorator.PayAtExpiry(self.Details['PayAtExpiry'])
        #exoDecorator.RebateCurrency(acm.FCurrency[self.Details['RebateCurrency']])
        exoDecorator.BaseType(acm.FEnumeration['enum(ExoticBaseType)'].Enumeration('Barrier')) #2==Barrier
        exoDecorator.BarrierMonitoring(self.Details['BarrierMonitoring'])
        exoDecorator.BarrierOptionType(acm.FEnumeration['enum(BarrierOptionType)'].Enumeration(self.Details['BarrierType']))
        
        if self.Details['BarrierMonitoring']>1: #Barrier type is Window (2) or Discrete (3)
            for event in self.Details['BarrierEventDates']:
                exe = acm.FExoticEvent()
                exe.Instrument(insOriginal)
                exe.ComponentInstrument(insOriginal)
                exe.Date(event[0])
                if len(event)>1:
                    exe.EndDate(event[1])
                exe.Type(acm.FEnumeration['enum(ExoticEventType)'].Enumeration('Barrier date')) #Barrier date 
                insDecorator.ExoticEvents().Add(exe)
        
        acm.PollDbEvents()
        insDecorator.DeliveryDate(self.Details['PayoffDate'])        
        insDecorator.StrikePrice(float(self.Details['Strike']))
        insDecorator.Barrier(float(self.Details['BarrierLevel']))
        insDecorator.SettlementType(acm.FEnumeration['enum(settlementTypeShortName)'].Enumeration('Physical') if self.Details['PayoffType'] == 'Asset' else acm.FEnumeration['enum(settlementTypeShortName)'].Enumeration('Cash'))
        insOriginal.Commit()

        
        tradeOrig = acm.FTrade()
        tradeOrig.Type('Normal')
        tradeDecorator = acm.FTradeLogicDecorator(tradeOrig, businessLogicGUIDefaultHandler)
        tradeDecorator.Instrument(insOriginal)
        tradeDecorator.Trader(acm.FUser[self.Details['Trader']])
        tradeDecorator.Counterparty(self.Details['Counterparty'])
        tradeDecorator.Acquirer(self.Details['Acquirer'])
        tradeDecorator.Portfolio(self.Details['FAPortfolio'])
        tradeDecorator.Status(self.Details['Status'])
        tradeDecorator.TradeTime(self.Details['TradeDate'])
        tradeDecorator.ValueDay(self.Details['PremiumDate'])
        tradeDecorator.Currency(acm.FCurrency[self.Details['PremiumCurrency']])
        tradeCalc = tradeDecorator.Calculation()
        calcSpace = acm.Calculations().CreateStandardCalculationsSpaceCollection()
        #print 'CCY='+self.Details['PremiumCurrency']
        tradeDecorator.FxoPremiumCurr(acm.FCurrency[self.Details['PremiumCurrency']])
        if self.Details['Reversed'] == "No":
            tradeDecorator.AmountDomestic(float(self.Details['Amount']) if self.Details['BuyOrSell'] == "Buy" else -1 * float(self.Details['Amount']))
            tradeDecorator.Premium(float(self.Details['PremiumAmount']) if self.Details['BuyOrSell'] == "Sell" else -1 * float(self.Details['PremiumAmount']))
        elif self.Details['Reversed'] == "Yes":
            tradeDecorator.AmountDomestic((-1 * float(self.Details['Amount'])) if self.Details['BuyOrSell'] == "Buy" else float(self.Details['Amount']))
            tradeDecorator.Premium((-1 * float(self.Details['PremiumAmount'])) if self.Details['BuyOrSell'] == "Sell" else float(self.Details['PremiumAmount']))
        #print tradeDecorator.Premium()
        #print tradeCalc.PremiumToPrice(calcSpace, acm.Time().DateToday(), tradeDecorator.Premium())
        if float(self.Details['PremiumAmount'])==0:
            tradeDecorator.Price(0)
        else:
            tradeDecorator.Price(tradeCalc.PremiumToPrice(calcSpace, acm.Time().DateToday(), tradeDecorator.Premium()).Number())
        
        
        if self.Details['SetOptionalKeys'] == "Yes":
            if self.Details['BARXTSSource'] == "Yes":
                tradeDecorator.OptionalKey('BARXTS_' + self.Details['TradeID']) #Sets ExternalID to murex.originTradeId
            else:
                tradeDecorator.OptionalKey('MUREX_' + self.Details['TradeID']) #Sets ExternalID to murex.originTradeId
        
        tradeOrig.Commit()
        return insOriginal.Name(), tradeOrig.Name()

class OneTouchTrade():
    def __init__(self, datadict = None):
        '''
        Using the trade dictionary, create a new FXOTrade object mapping the murex values to Front Arena.
        Also do some data verification checks.
        '''    
        if ( not datadict):
            datadict = {}        
        self.Details = datadict
        self.CutCodeMapping = {'NY':acm.FParty['NY 10:00 am'],
                               'TKY':acm.FParty['TK 3:00 pm'],
                               'ECB':acm.FParty['ECB 2:15 pm'],
                               'WMR':acm.FParty['WMR 4:00 pm']}
        
    @staticmethod
    def getPremiumDateAmountCurrency(flowlist):
        for flow in flowlist:
            if flow.attrib[GMT_PREFIX+'FlowType'] == "Premium":
                dt = flow.attrib[GMT_PREFIX+'Date']
                amt = flow.find(GMT_PREFIX+'Amount').text
                cur = flow.find(GMT_PREFIX+'Currency').attrib[GMT_PREFIX+'Id']
                return (dt, amt, cur)
            
    def CreateTrade(self): 
        insOriginal = acm.FOption()
        businessLogicGUIDefaultHandler = acm.FBusinessLogicGUIDefault()
        businessLogicGUIDefaultHandler.AskAdjustToFollowingBusinessDay(True)
        businessLogicGUIDefaultHandler.AskAdjustAcquireDate(True)
        businessLogicGUIDefaultHandler.AskAdjustValueDate(True)
        insDecorator = acm.FOptionDecorator(insOriginal, businessLogicGUIDefaultHandler)
        defaultID = 'Option-Curr-Default'
        defaultIns = acm.FOption[defaultID]
        insDecorator.ValuationGrpChlItem(defaultIns.ValuationGrpChlItem())
        insDecorator.PayType(defaultIns.PayType())
        insDecorator.SettlementType(acm.FEnumeration['enum(settlementTypeShortName)'].Enumeration('Physical') if self.Details['PayoffType'] == 'Asset' else acm.FEnumeration['enum(settlementTypeShortName)'].Enumeration('Cash'))
        insDecorator.ExpiryDate(self.Details['ExpiryEventDate'])        
        insDecorator.DeliveryDate(self.Details['PayoffDate'])
        insDecorator.Currency(acm.FCurrency[self.Details['EconomicUnderlyingCurrency']])                 #Trade Currency
        insDecorator.DomesticCurrency(acm.FCurrency[self.Details['EconomicUnderlyingCurrency']])
        insDecorator.ForeignCurrency(acm.FCurrency[self.Details['EconomicBaseCurrency']])
        insDecorator.OptionType('Call' if self.Details['CallPut']=='Call' else 'Put') #attempt to get Up / Down currencies correct
        insDecorator.OriginalCurrency(acm.FCurrency[self.Details['EconomicBaseCurrency']])
        insDecorator.FixingSource(self.CutCodeMapping[self.Details['ExpiryEventCutCode']])
        insDecorator.FxoPremiumCurr(acm.FCurrency[self.Details['PremiumCurrency']])
        insDecorator.Barrier(float(self.Details['BarrierLevel']))
        insDecorator.Rebate(float(self.Details['Rebate']))
        insDecorator.ContractSize(1)
        insDecorator.QuoteType(acm.FEnumeration['enum(QuoteType)'].Enumeration('Per Unit'))
        insDecorator.ExerciseType(acm.FEnumeration['enum(ExerciseType)'].Enumeration('American')) #European
        insDecorator.PayoutCurrency(acm.FCurrency[self.Details['PayoutCurrency']])
        
        insOriginal.RegisterInStorage()      
        
        exoDecorator = insDecorator.Exotic()
        exoDecorator.PayAtExpiry(self.Details['PayAtExpiry'])
        #exoDecorator.RebateCurrency(acm.FCurrency[self.Details['RebateCurrency']])
        exoDecorator.BaseType(acm.FEnumeration['enum(ExoticBaseType)'].Enumeration('Digital American')) #2==Barrier
        exoDecorator.BarrierMonitoring(self.Details['BarrierMonitoring'])
        exoDecorator.BarrierOptionType(acm.FEnumeration['enum(BarrierOptionType)'].Enumeration(self.Details['BarrierType']))
        
        if self.Details['BarrierMonitoring']>1: #Barrier type is Window (2) or Discrete (3)
            for event in self.Details['BarrierEventDates']:
                exe = acm.FExoticEvent()
                exe.Instrument(insOriginal)
                exe.ComponentInstrument(insOriginal)
                exe.Date(event[0])
                if len(event)>1:
                    exe.EndDate(event[1])
                exe.Type(acm.FEnumeration['enum(ExoticEventType)'].Enumeration('Barrier date')) #Barrier date 
                insDecorator.ExoticEvents().Add(exe)
        
        acm.PollDbEvents()
        insDecorator.DeliveryDate(self.Details['PayoffDate'])        
        insDecorator.Barrier(float(self.Details['BarrierLevel']))
        insDecorator.OptionType('Call' if self.Details['CallPut']=='Call' else 'Put') #attempt to get Up / Down currencies correct
        insDecorator.PayoutCurrency(acm.FCurrency[self.Details['PayoutCurrency']])
        insDecorator.SettlementType(acm.FEnumeration['enum(settlementTypeShortName)'].Enumeration('Physical') if self.Details['PayoffType'] == 'Asset' else acm.FEnumeration['enum(settlementTypeShortName)'].Enumeration('Cash'))
        exoDecorator.PayAtExpiry(self.Details['PayAtExpiry'])
        insOriginal.Commit()

        
        tradeOrig = acm.FTrade()
        tradeOrig.Type('Normal')
        tradeDecorator = acm.FTradeLogicDecorator(tradeOrig, businessLogicGUIDefaultHandler)
        tradeDecorator.Instrument(insOriginal)
        tradeDecorator.Trader(acm.FUser[self.Details['Trader']])
        tradeDecorator.Counterparty(self.Details['Counterparty'])
        tradeDecorator.Acquirer(self.Details['Acquirer'])
        tradeDecorator.Portfolio(self.Details['FAPortfolio'])
        tradeDecorator.Status(self.Details['Status'])
        tradeDecorator.TradeTime(self.Details['TradeDate'])
        tradeDecorator.ValueDay(self.Details['PremiumDate'])
        tradeDecorator.Currency(acm.FCurrency[self.Details['PremiumCurrency']])
        tradeCalc = tradeDecorator.Calculation()
        calcSpace = acm.Calculations().CreateStandardCalculationsSpaceCollection()
        #print 'CCY='+self.Details['PremiumCurrency']
        tradeDecorator.FxoPremiumCurr(acm.FCurrency[self.Details['PremiumCurrency']])
        if self.Details['Reversed'] == "No":
            tradeDecorator.AmountDomestic(float(self.Details['Amount']) if self.Details['BuyOrSell'] == "Buy" else -1 * float(self.Details['Amount']))
            tradeDecorator.Premium(float(self.Details['PremiumAmount']) if self.Details['BuyOrSell'] == "Sell" else -1 * float(self.Details['PremiumAmount']))
        elif self.Details['Reversed'] == "Yes":
            tradeDecorator.AmountDomestic((-1 * float(self.Details['Amount'])) if self.Details['BuyOrSell'] == "Buy" else float(self.Details['Amount']))
            tradeDecorator.Premium((-1 * float(self.Details['PremiumAmount'])) if self.Details['BuyOrSell'] == "Sell" else float(self.Details['PremiumAmount']))
        #print tradeDecorator.Premium()
        #print tradeCalc.PremiumToPrice(calcSpace, acm.Time().DateToday(), tradeDecorator.Premium())
        if float(self.Details['PremiumAmount'])==0:
            tradeDecorator.Price(0)
        else:
            tradeDecorator.Price(tradeCalc.PremiumToPrice(calcSpace, acm.Time().DateToday(), tradeDecorator.Premium()).Number())
        
        
        if self.Details['SetOptionalKeys'] == "Yes":
            if self.Details['BARXTSSource'] == "Yes":
                tradeDecorator.OptionalKey('BARXTS_' + self.Details['TradeID']) #Sets ExternalID to murex.originTradeId
            else:
                tradeDecorator.OptionalKey('MUREX_' + self.Details['TradeID']) #Sets ExternalID to murex.originTradeId
        
        tradeOrig.Commit()
        return insOriginal.Name(), tradeOrig.Name()

class FXODoubleBarrierTrade():
    def __init__(self, datadict = None):
        '''
        Using the trade dictionary, create a new FXOTrade object mapping the murex values to Front Arena.
        Also do some data verification checks.
        '''    
        if ( not datadict):
            datadict = {}        
        self.Details = datadict
        self.CutCodeMapping = {'NY':acm.FParty['NY 10:00 am'],
                               'TKY':acm.FParty['TK 3:00 pm'],
                               'ECB':acm.FParty['ECB 2:15 pm'],
                               'WMR':acm.FParty['WMR 4:00 pm']}
        
    @staticmethod
    def getPremiumDateAmountCurrency(flowlist):
        for flow in flowlist:
            if flow.attrib[GMT_PREFIX+'FlowType'] == "Premium":
                dt = flow.attrib[GMT_PREFIX+'Date']
                amt = flow.find(GMT_PREFIX+'Amount').text
                cur = flow.find(GMT_PREFIX+'Currency').attrib[GMT_PREFIX+'Id']
                return (dt, amt, cur)
            
    def CreateTrade(self): 
        insOriginal = acm.FOption()
        businessLogicGUIDefaultHandler = acm.FBusinessLogicGUIDefault()
        businessLogicGUIDefaultHandler.AskAdjustToFollowingBusinessDay(True)
        businessLogicGUIDefaultHandler.AskAdjustAcquireDate(True)
        businessLogicGUIDefaultHandler.AskAdjustValueDate(True)
        insDecorator = acm.FOptionDecorator(insOriginal, businessLogicGUIDefaultHandler)
        defaultID = 'Option-Curr-Default'
        defaultIns = acm.FOption[defaultID]
        insDecorator.StrikePrice(float(self.Details['Strike']))
        insDecorator.StrikeType('Absolute')
        insDecorator.StrikeQuotation(acm.FQuotation['Per Unit'])
        insDecorator.ValuationGrpChlItem(defaultIns.ValuationGrpChlItem())
        insDecorator.PayType(defaultIns.PayType())
        insDecorator.SettlementType(acm.FEnumeration['enum(settlementTypeShortName)'].Enumeration('Physical') if self.Details['PayoffType'] == 'Asset' else acm.FEnumeration['enum(settlementTypeShortName)'].Enumeration('Cash'))
        insDecorator.ExpiryDate(self.Details['ExpiryEventDate'])        
        insDecorator.DeliveryDate(self.Details['PayoffDate'])
        insDecorator.OptionType(self.Details['CallPut'])
        insDecorator.Currency(acm.FCurrency[self.Details['EconomicUnderlyingCurrency']])                 #Trade Currency
        insDecorator.DomesticCurrency(acm.FCurrency[self.Details['EconomicUnderlyingCurrency']])
        insDecorator.ForeignCurrency(acm.FCurrency[self.Details['EconomicBaseCurrency']])

        insDecorator.StrikePrice(float(self.Details['Strike']))
        insDecorator.StrikeType('Absolute')
        insDecorator.StrikeQuotation(acm.FQuotation['Per Unit'])
        insDecorator.StrikeCurrency(acm.FCurrency[self.Details['EconomicUnderlyingCurrency']])
        insDecorator.OriginalCurrency(acm.FCurrency[self.Details['EconomicBaseCurrency']])
        insDecorator.FixingSource(self.CutCodeMapping[self.Details['ExpiryEventCutCode']])
        insDecorator.FxoPremiumCurr(acm.FCurrency[self.Details['PremiumCurrency']])
        insDecorator.Barrier(float(self.Details['BarrierLevel1']))
        insDecorator.Rebate(float(self.Details['Rebate']))
        insDecorator.ContractSize(1)
        insDecorator.QuoteType(acm.FEnumeration['enum(QuoteType)'].Enumeration('Per Unit'))
        insDecorator.ExerciseType(acm.FEnumeration['enum(ExerciseType)'].Enumeration('European')) #European
        
        insOriginal.RegisterInStorage()      
        
        exoDecorator = insDecorator.Exotic()
        exoDecorator.PayAtExpiry(self.Details['PayAtExpiry'])
        #exoDecorator.RebateCurrency(acm.FCurrency[self.Details['RebateCurrency']])
        exoDecorator.BaseType(acm.FEnumeration['enum(ExoticBaseType)'].Enumeration('Barrier')) #2==Barrier
        exoDecorator.BarrierMonitoring(self.Details['BarrierMonitoring'])
        exoDecorator.BarrierOptionType(acm.FEnumeration['enum(BarrierOptionType)'].Enumeration(self.Details['BarrierType']))
        exoDecorator.DoubleBarrier(float(self.Details['BarrierLevel2']))
        
        if self.Details['BarrierMonitoring']>1: #Barrier type is Window (2) or Discrete (3)
            for event in self.Details['BarrierEventDates']:
                exe = acm.FExoticEvent()
                exe.Instrument(insOriginal)
                exe.ComponentInstrument(insOriginal)
                exe.Date(event[0])
                if len(event)>1:
                    exe.EndDate(event[1])
                exe.Type(acm.FEnumeration['enum(ExoticEventType)'].Enumeration('Barrier date')) #Barrier date 
                insDecorator.ExoticEvents().Add(exe)
        
        acm.PollDbEvents()
        #re-set some values which seems to disapepar
        insDecorator.DeliveryDate(self.Details['PayoffDate'])        
        insDecorator.StrikePrice(float(self.Details['Strike']))
        insDecorator.Barrier(float(self.Details['BarrierLevel1']))
        insDecorator.SettlementType(acm.FEnumeration['enum(settlementTypeShortName)'].Enumeration('Physical') if self.Details['PayoffType'] == 'Asset' else acm.FEnumeration['enum(settlementTypeShortName)'].Enumeration('Cash'))
        exoDecorator.DoubleBarrier(float(self.Details['BarrierLevel2']))
        insOriginal.Commit()

        
        tradeOrig = acm.FTrade()
        tradeOrig.Type('Normal')
        tradeDecorator = acm.FTradeLogicDecorator(tradeOrig, businessLogicGUIDefaultHandler)
        tradeDecorator.Instrument(insOriginal)
        tradeDecorator.Trader(acm.FUser[self.Details['Trader']])
        tradeDecorator.Counterparty(self.Details['Counterparty'])
        tradeDecorator.Acquirer(self.Details['Acquirer'])
        tradeDecorator.Portfolio(self.Details['FAPortfolio'])
        tradeDecorator.Status(self.Details['Status'])
        tradeDecorator.TradeTime(self.Details['TradeDate'])
        tradeDecorator.ValueDay(self.Details['PremiumDate'])
        tradeDecorator.Currency(acm.FCurrency[self.Details['PremiumCurrency']])
        tradeCalc = tradeDecorator.Calculation()
        calcSpace = acm.Calculations().CreateStandardCalculationsSpaceCollection()
        #print 'CCY='+self.Details['PremiumCurrency']
        tradeDecorator.FxoPremiumCurr(acm.FCurrency[self.Details['PremiumCurrency']])
        if self.Details['Reversed'] == "No":
            tradeDecorator.AmountDomestic(float(self.Details['Amount']) if self.Details['BuyOrSell'] == "Buy" else -1 * float(self.Details['Amount']))
            tradeDecorator.Premium(float(self.Details['PremiumAmount']) if self.Details['BuyOrSell'] == "Sell" else -1 * float(self.Details['PremiumAmount']))
        elif self.Details['Reversed'] == "Yes":
            tradeDecorator.AmountDomestic((-1 * float(self.Details['Amount'])) if self.Details['BuyOrSell'] == "Buy" else float(self.Details['Amount']))
            tradeDecorator.Premium((-1 * float(self.Details['PremiumAmount'])) if self.Details['BuyOrSell'] == "Sell" else float(self.Details['PremiumAmount']))
        #print tradeDecorator.Premium()
        #print tradeCalc.PremiumToPrice(calcSpace, acm.Time().DateToday(), tradeDecorator.Premium())
        if float(self.Details['PremiumAmount'])==0:
            tradeDecorator.Price(0)
        else:
            tradeDecorator.Price(tradeCalc.PremiumToPrice(calcSpace, acm.Time().DateToday(), tradeDecorator.Premium()).Number())
        
        
        if self.Details['SetOptionalKeys'] == "Yes":
            if self.Details['BARXTSSource'] == "Yes":
                tradeDecorator.OptionalKey('BARXTS_' + self.Details['TradeID']) #Sets ExternalID to murex.originTradeId
            else:
                tradeDecorator.OptionalKey('MUREX_' + self.Details['TradeID']) #Sets ExternalID to murex.originTradeId
        
        tradeOrig.Commit()
        return insOriginal.Name(), tradeOrig.Name()

class DoubleTouchTrade():
    def __init__(self, datadict = None):
        '''
        Using the trade dictionary, create a new FXOTrade object mapping the murex values to Front Arena.
        Also do some data verification checks.
        '''    
        if ( not datadict):
            datadict = {}        
        self.Details = datadict
        self.CutCodeMapping = {'NY':acm.FParty['NY 10:00 am'],
                               'TKY':acm.FParty['TK 3:00 pm'],
                               'ECB':acm.FParty['ECB 2:15 pm'],
                               'WMR':acm.FParty['WMR 4:00 pm']}
        
    @staticmethod
    def getPremiumDateAmountCurrency(flowlist):
        for flow in flowlist:
            if flow.attrib[GMT_PREFIX+'FlowType'] == "Premium":
                dt = flow.attrib[GMT_PREFIX+'Date']
                amt = flow.find(GMT_PREFIX+'Amount').text
                cur = flow.find(GMT_PREFIX+'Currency').attrib[GMT_PREFIX+'Id']
                return (dt, amt, cur)
            
    def CreateTrade(self): 
        insOriginal = acm.FOption()
        businessLogicGUIDefaultHandler = acm.FBusinessLogicGUIDefault()
        businessLogicGUIDefaultHandler.AskAdjustToFollowingBusinessDay(True)
        businessLogicGUIDefaultHandler.AskAdjustAcquireDate(True)
        businessLogicGUIDefaultHandler.AskAdjustValueDate(True)
        insDecorator = acm.FOptionDecorator(insOriginal, businessLogicGUIDefaultHandler)
        defaultID = 'Option-Curr-Default'
        defaultIns = acm.FOption[defaultID]
        insDecorator.ValuationGrpChlItem(defaultIns.ValuationGrpChlItem())
        insDecorator.PayType(defaultIns.PayType())
        insDecorator.SettlementType(acm.FEnumeration['enum(settlementTypeShortName)'].Enumeration('Physical') if self.Details['PayoffType'] == 'Asset' else acm.FEnumeration['enum(settlementTypeShortName)'].Enumeration('Cash'))
        insDecorator.ExpiryDate(self.Details['ExpiryEventDate'])        
        insDecorator.DeliveryDate(self.Details['PayoffDate'])
        insDecorator.Currency(acm.FCurrency[self.Details['EconomicUnderlyingCurrency']])                 #Trade Currency
        insDecorator.DomesticCurrency(acm.FCurrency[self.Details['EconomicUnderlyingCurrency']])
        insDecorator.ForeignCurrency(acm.FCurrency[self.Details['EconomicBaseCurrency']])
        #insDecorator.OptionType('Call' if self.Details['CallPut']=='Call' else 'Put') #attempt to get Up / Down currencies correct
        insDecorator.OriginalCurrency(acm.FCurrency[self.Details['EconomicBaseCurrency']])
        insDecorator.FixingSource(self.CutCodeMapping[self.Details['ExpiryEventCutCode']])
        insDecorator.FxoPremiumCurr(acm.FCurrency[self.Details['PremiumCurrency']])
        insDecorator.Barrier(float(self.Details['BarrierLevel1']))
        insDecorator.Rebate(float(self.Details['Rebate']))
        insDecorator.ContractSize(1)
        insDecorator.QuoteType(acm.FEnumeration['enum(QuoteType)'].Enumeration('Per Unit'))
        insDecorator.ExerciseType(acm.FEnumeration['enum(ExerciseType)'].Enumeration('American')) #European
        
        insDecorator.PayoutCurrency(acm.FCurrency[self.Details['PayoutCurrency']])
        
        insOriginal.RegisterInStorage()      
        
        exoDecorator = insDecorator.Exotic()
        exoDecorator.PayAtExpiry(self.Details['PayAtExpiry'])
        #exoDecorator.RebateCurrency(acm.FCurrency[self.Details['RebateCurrency']])
        exoDecorator.BaseType(acm.FEnumeration['enum(ExoticBaseType)'].Enumeration('Digital American')) #2==Barrier
        exoDecorator.BarrierMonitoring(self.Details['BarrierMonitoring'])
        exoDecorator.BarrierOptionType(acm.FEnumeration['enum(BarrierOptionType)'].Enumeration(self.Details['BarrierType']))
        exoDecorator.DoubleBarrier(float(self.Details['BarrierLevel2']))
        
        if self.Details['BarrierMonitoring']>1: #Barrier type is Window (2) or Discrete (3)
            for event in self.Details['BarrierEventDates']:
                exe = acm.FExoticEvent()
                exe.Instrument(insOriginal)
                exe.ComponentInstrument(insOriginal)
                exe.Date(event[0])
                if len(event)>1:
                    exe.EndDate(event[1])
                exe.Type(acm.FEnumeration['enum(ExoticEventType)'].Enumeration('Barrier date')) #Barrier date 
                insDecorator.ExoticEvents().Add(exe)
        
        acm.PollDbEvents()
        insDecorator.DeliveryDate(self.Details['PayoffDate'])        
        insDecorator.Barrier(float(self.Details['BarrierLevel1']))
        exoDecorator.DoubleBarrier(float(self.Details['BarrierLevel2']))
        exoDecorator.PayAtExpiry(self.Details['PayAtExpiry'])
        insDecorator.PayoutCurrency(acm.FCurrency[self.Details['PayoutCurrency']])
        insDecorator.SettlementType(acm.FEnumeration['enum(settlementTypeShortName)'].Enumeration('Physical') if self.Details['PayoffType'] == 'Asset' else acm.FEnumeration['enum(settlementTypeShortName)'].Enumeration('Cash'))
        insOriginal.Commit()

        
        tradeOrig = acm.FTrade()
        tradeOrig.Type('Normal')
        tradeDecorator = acm.FTradeLogicDecorator(tradeOrig, businessLogicGUIDefaultHandler)
        tradeDecorator.Instrument(insOriginal)
        tradeDecorator.Trader(acm.FUser[self.Details['Trader']])
        tradeDecorator.Counterparty(self.Details['Counterparty'])
        tradeDecorator.Acquirer(self.Details['Acquirer'])
        tradeDecorator.Portfolio(self.Details['FAPortfolio'])
        tradeDecorator.Status(self.Details['Status'])
        tradeDecorator.TradeTime(self.Details['TradeDate'])
        tradeDecorator.ValueDay(self.Details['PremiumDate'])
        tradeDecorator.Currency(acm.FCurrency[self.Details['PremiumCurrency']])
        tradeCalc = tradeDecorator.Calculation()
        calcSpace = acm.Calculations().CreateStandardCalculationsSpaceCollection()
        #print 'CCY='+self.Details['PremiumCurrency']
        tradeDecorator.FxoPremiumCurr(acm.FCurrency[self.Details['PremiumCurrency']])
        if self.Details['Reversed'] == "No":
            tradeDecorator.AmountDomestic(float(self.Details['Amount']) if self.Details['BuyOrSell'] == "Buy" else -1 * float(self.Details['Amount']))
            tradeDecorator.Premium(float(self.Details['PremiumAmount']) if self.Details['BuyOrSell'] == "Sell" else -1 * float(self.Details['PremiumAmount']))
        elif self.Details['Reversed'] == "Yes":
            tradeDecorator.AmountDomestic((-1 * float(self.Details['Amount'])) if self.Details['BuyOrSell'] == "Buy" else float(self.Details['Amount']))
            tradeDecorator.Premium((-1 * float(self.Details['PremiumAmount'])) if self.Details['BuyOrSell'] == "Sell" else float(self.Details['PremiumAmount']))
        #print tradeDecorator.Premium()
        #print tradeCalc.PremiumToPrice(calcSpace, acm.Time().DateToday(), tradeDecorator.Premium())
        if float(self.Details['PremiumAmount'])==0:
            tradeDecorator.Price(0)
        else:
            tradeDecorator.Price(tradeCalc.PremiumToPrice(calcSpace, acm.Time().DateToday(), tradeDecorator.Premium()).Number())
        
        
        if self.Details['SetOptionalKeys'] == "Yes":
            if self.Details['BARXTSSource'] == "Yes":
                tradeDecorator.OptionalKey('BARXTS_' + self.Details['TradeID']) #Sets ExternalID to murex.originTradeId
            else:
                tradeDecorator.OptionalKey('MUREX_' + self.Details['TradeID']) #Sets ExternalID to murex.originTradeId
        
        tradeOrig.Commit()
        return insOriginal.Name(), tradeOrig.Name()


def _get_counterparty_list():
    part_list = acm.FCounterParty.Instances().AsSet()
    part_list.Union(acm.FClient.Instances())
    return part_list


ael_variables = []
ael_variables.append(['env', 'TMS Instance', 'string', None, 'FXOTMSPDN', 1, 0, 'TMS Instance: FXOTMSGROUP or FXOTMSPDN', None, 1])
ael_variables.append(['fileLocation', 'CSV File Location', fileSelection, None, fileSelection, 1, 1, 'Traction CSV extract', None, 1])
#ael_variables.append(['env', 'TMS Instance', 'string', None, 'FXOTMSDEVTS1', 1, 0, 'TMS Instance: FXOTMSGROUP or FXOTMSPDN', None, 1])
#ael_variables.append(['fileLocation', 'CSV File Location', fileSelection, None, r'c:\temp\trades.csv', 1, 1, 'Traction CSV extract', None, 1])
ael_variables.append(['FAPortfolio', 'Trade Portfolio', acm.FPhysicalPortfolio, acm.FPhysicalPortfolio.Instances(), acm.FPhysicalPortfolio['VOE'], 1, 0, 'Portfolio where trade will be booked', None, 1])
ael_variables.append(['Acquirer', 'Trade Acquirer', acm.FParty, acm.FParty.Instances(), acm.FParty['NLD DESK'], 1, 0, 'Acquirer', None, 1])
ael_variables.append(['Counterparty', 'Trade Counterparty', acm.FParty, _get_counterparty_list(), acm.FParty['BARCLAYS BANK PLC MUREX'], 1, 0, 'Counterparty', None, 1])
ael_variables.append(['Status', 'Trade Status', 'string', ['FO Confirmed', 'BO Confirmed'], 'FO Confirmed', 1, 0, 'Status', None, 1])
ael_variables.append(['SetOptionalKeys', 'Set Optional Keys', 'string', ['Yes', 'No'], 'Yes', 1, 0, 'Set the optional keys on the trades to BARXTS_TrdNbr or MUREX_TrdNbr', None, 1])
ael_variables.append(['BARXTSSource', 'BARXTSSource', 'string', ['Yes', 'No'], 'Yes', 1, 0, 'Choosing Trade Source', None, 1])
ael_variables.append(['Reversed', 'Book Opposite Trade', 'string', ['Yes', 'No'], 'No', 1, 0, 'Books the opposite trade', None, 1])
    
def ael_main(dict):
    dict['Trader'] = acm.User().Name()
    if getOperatingEnvironment() == "Frontend":                             
        with open(str(dict['fileLocation']), 'r') as csvFile:
            nRows = sum(1 for row in csvFile) - 1
            csvFile.seek(0)
            try:
                mxcon = MXConnection(dict['env'])
                reader = csv.DictReader(csvFile)
            except Exception, e:
                print "Fatal error occured\t", e
                print e
                #sys.exit(0)
            print 'Starting upload @ ' + str(datetime.datetime.now()) + ' / ' + str(nRows) + ' rows'
            for row in reader:
                try:
                    tradeData = mxcon.getTradeData(dict['BARXTSSource'], row['TradeId'])
                    root = ElementTree.XML(tradeData)
                    InsType = root.find(GMT_PREFIX+'Instrument').attrib[GMT_PREFIX+'Type']
                    InsSubType = root.find(GMT_PREFIX+'Instrument').attrib[GMT_PREFIX+'SubType']
                    cptyPath = GMT_PREFIX.join([GMT_PREFIX+'Instrument/', 'BookingDetail/', 'Counterparty'])
                    CounterpartyID= root.find(cptyPath).attrib[GMT_PREFIX+'Id']
                    eventType = root.find(GMT_PREFIX.join([GMT_PREFIX+'TradeDetail/', 'Audit'])).attrib[GMT_PREFIX+'EventType']
                    action = root.find(GMT_PREFIX.join([GMT_PREFIX+'TradeDetail/', 'Action'])).text
                    tradeId = root.find(GMT_PREFIX+"TradeDetail").attrib[GMT_PREFIX+'Id']
                    alternateIDs = root.find(GMT_PREFIX+"TradeDetail").findall(GMT_PREFIX+'AlternateId')
                    print InsType + '_' + InsSubType + ' / ' + tradeId
                    #--------------ABSA facing trades--------------
                    if CounterpartyID in [ABSAJBG, ADJUST]:
                        print 'Trade is ABSA facing leg ' + tradeId
                    #--------------Cancellation--------------
                    elif eventType == 'Cancel' or action == 'Cancel':
                        print 'Cancelling trade ' + tradeId
                        deleteTrade('BARXTS_' + tradeId)
                    else:
                        #--------------FX Forward from option exercise ----------------
                        #if InsType == 'FX Forward' and InsSubType == 'Forward' and alternateIDs!= None:
                        #    print 'Skipping FX Forward trade as is appears to be from option expiry - source Id is ' + alternateIDs[0].attrib[GMT_PREFIX+'Id']
                        #--------------FX Forward----------------
                        if InsType == 'FX Forward' and InsSubType == 'Forward':
                            isFromExercise = 0
                            for altId in alternateIDs:
                                if altId.attrib[GMT_PREFIX+'Source']=='murex.sourceTradeId':
                                    isFromExercise=1
                            
                            if isFromExercise==1:
                                print "Skipping FX Forward as it appears to be from option exercise"
                                continue
                            
                            XPATH = {
                            'TradeDate': GMT_PREFIX.join([GMT_PREFIX+'TradeDetail/', 'TradeDate']),
                            'PaymentDate': GMT_PREFIX.join([GMT_PREFIX+'Instrument/', 'EconomicDetail/', 'AssetDetail/', 'PaymentDate']),
                            'ForwardDate': GMT_PREFIX.join([GMT_PREFIX+'Instrument/', 'EconomicDetail/', 'AssetDetail/', 'ForwardDate']),
                            'Amount': GMT_PREFIX.join([GMT_PREFIX+'Instrument/', 'EconomicDetail/', 'AssetDetail/', 'FXDetails/', 'Amount']),
                            'AmountCurrency': GMT_PREFIX.join([GMT_PREFIX+'Instrument/', 'EconomicDetail/', 'AssetDetail/', 'FXDetails/', 'Currency']),
                            'BaseCurrency': GMT_PREFIX.join([GMT_PREFIX+'Instrument/', 'EconomicDetail/', 'AssetDetail/', 'FXDetails/', 'BaseCurrency']),
                            'QuotedCurrency': GMT_PREFIX.join([GMT_PREFIX+'Instrument/', 'EconomicDetail/', 'AssetDetail/', 'FXDetails/', 'QuotedCurrency']),
                            'Rate': GMT_PREFIX.join([GMT_PREFIX+'Instrument/', 'EconomicDetail/', 'AssetDetail/', 'FXDetails/', 'Rate']),
                            'EventType': GMT_PREFIX.join([GMT_PREFIX+'TradeDetail/', 'Audit']),
                            }
                            tradeDictionary = dict.copy()
                            tradeDictionary['TradeID'] = tradeId
                            tradeDictionary['PaymentDate']= root.find(XPATH['PaymentDate']).text
                            tradeDictionary['ForwardDate']= root.find(XPATH['ForwardDate']).text
                            tradeDictionary['Amount']= root.find(XPATH['Amount']).text
                            tradeDictionary['AmountCurrency']= root.find(XPATH['AmountCurrency']).attrib[GMT_PREFIX+'Id']
                            tradeDictionary['BaseCurrency']= root.find(XPATH['BaseCurrency']).attrib[GMT_PREFIX+'Id']
                            tradeDictionary['QuotedCurrency']= root.find(XPATH['QuotedCurrency']).attrib[GMT_PREFIX+'Id']
                            tradeDictionary['Rate']= root.find(XPATH['Rate']).text
                            tradeDictionary['TradeDate']= root.find(XPATH['TradeDate']).text.split('T')[0]
                            tradeDictionary['EventType']= root.find(XPATH['EventType']).attrib[GMT_PREFIX+'EventType']
                            tradeDictionary['EventReason']= root.find(XPATH['EventType']).attrib[GMT_PREFIX+'EventReason']                                
                            if tradeDictionary['EventType'] == "NewTrade" and tradeDictionary['EventReason'] == "":
                                trade = FXForwardTrade(tradeDictionary)
                                insName, trdNbr = trade.CreateTrade()
                                if dict['BARXTSSource'] == "Yes":
                                        print "CREATED FX Forward:\tInstrument:\t%s\t\t\t\tBARX FX TS Trade:\t%s\t\tFA Trade:\t%s" % (insName, tradeDictionary['TradeID'], trdNbr)
                                else:
                                        print "CREATED FX Forward:\tInstrument:\t%s\t\t\t\tMurex Trade:\t%s\t\tFA Trade:\t%s" % (insName, tradeDictionary['TradeID'], trdNbr)
                            else:
                                print "SKIPPED FX Forward:\tEventType:\t%s\tEventReason:\t%s" % (tradeDictionary['EventType'], tradeDictionary['EventReason'])
                        #--------------Vanilla Option ---------------
                        elif InsType == 'FX Option' and InsSubType == 'Vanilla':
                            XPATH = {
                            'EconomicUnderlyingCurrency': GMT_PREFIX.join([GMT_PREFIX+'Instrument/', 'EconomicDetail/', 'AssetDetail/', 'OptionUnderlying/', 'Underlying/', 'EconomicDetail/', 'FXDetails/', 'Currency']),
                            'EconomicBaseCurrency': GMT_PREFIX.join([GMT_PREFIX+'Instrument/', 'EconomicDetail/', 'AssetDetail/', 'OptionUnderlying/', 'Underlying/', 'EconomicDetail/', 'FXDetails/', 'BaseCurrency']),
                            'Amount': GMT_PREFIX.join([GMT_PREFIX+'Instrument/', 'EconomicDetail/', 'AssetDetail/', 'OptionUnderlying/', 'Underlying/', 'EconomicDetail/', 'FXDetails/', 'Amount']),
                            'QuotedCurrency': GMT_PREFIX.join([GMT_PREFIX+'Instrument/', 'EconomicDetail/', 'AssetDetail/', 'OptionUnderlying/', 'Underlying/', 'EconomicDetail/', 'FXDetails/', 'QuotedCurrency']),
                            'CallPut': GMT_PREFIX.join([GMT_PREFIX+'Instrument/', 'EconomicDetail/', 'AssetDetail/', 'OptionUnderlying/', 'LocalPayoffDetails/', 'OptionPayoffStyle']),
                            'Strike': GMT_PREFIX.join([GMT_PREFIX+'Instrument/', 'EconomicDetail/', 'AssetDetail/', 'OptionUnderlying/', 'LocalPayoffDetails/', 'OptionStrike']),
                            'PayoffDate': GMT_PREFIX.join([GMT_PREFIX+'Instrument/', 'EconomicDetail/', 'AssetDetail/', 'OptionUnderlying/', 'LocalPayoffDetails/', 'PayoffDate']),
                            'PayoffType': GMT_PREFIX.join([GMT_PREFIX+'Instrument/', 'EconomicDetail/', 'AssetDetail/', 'PayoffInCashOrAsset']),
                            'OptionType': GMT_PREFIX.join([GMT_PREFIX+'Instrument/', 'EconomicDetail/', 'AssetDetail/', 'OptionExpiryStyle']),
                            'ExpiryEvent': GMT_PREFIX.join([GMT_PREFIX+'Instrument/', 'EconomicDetail/', 'AssetDetail/', 'OptionExpiryEvent']),
                            'Portfolio': GMT_PREFIX.join([GMT_PREFIX+'Instrument/', 'BookingDetail/', 'Book']),
                            'Counterparty': GMT_PREFIX.join([GMT_PREFIX+'Instrument/', 'BookingDetail/', 'Counterparty']),
                            'BuyOrSell': GMT_PREFIX.join([GMT_PREFIX+'Instrument/', 'BookingDetail/', 'BuyOrSell']),
                            'TradePrice': GMT_PREFIX.join([GMT_PREFIX+'Instrument/', 'BookingDetail/', 'TradePrice/', 'Rate']),
                            'BookingBaseCurrency': GMT_PREFIX.join([GMT_PREFIX+'Instrument/', 'BookingDetail/', 'TradePrice/', 'BaseCurrency']),
                            'BookingQuotedCurrency': GMT_PREFIX.join([GMT_PREFIX+'Instrument/', 'BookingDetail/', 'TradePrice/', 'QuotedCurrency']),
                            'BasePerQuoted': GMT_PREFIX.join([GMT_PREFIX+'Instrument/', 'BookingDetail/', 'TradePrice/', 'Rate']),
                            'FlowList': GMT_PREFIX.join([GMT_PREFIX+'Instrument/', 'BookingDetail/', 'FlowList']),
                            'EventType': GMT_PREFIX.join([GMT_PREFIX+'TradeDetail/', 'Audit']),
                            'TradeDate': GMT_PREFIX.join([GMT_PREFIX+'TradeDetail/', 'TradeDate']),
                            }
                            tradeDictionary = dict.copy()
                            tradeDictionary['TradeID'] = root.find(GMT_PREFIX+"TradeDetail").attrib[GMT_PREFIX+'Id']
                            tradeDictionary['InsType'] = root.find(GMT_PREFIX+'Instrument').attrib[GMT_PREFIX+'Type']
                            tradeDictionary['InsSubType']=root.find(GMT_PREFIX+'Instrument').attrib[GMT_PREFIX+'SubType']
                            tradeDictionary['EconomicUnderlyingCurrency']= root.find(XPATH['EconomicUnderlyingCurrency']).attrib[GMT_PREFIX+'Id']
                            tradeDictionary['EconomicBaseCurrency']= root.find(XPATH['EconomicBaseCurrency']).attrib[GMT_PREFIX+'Id']
                            tradeDictionary['Amount']= root.find(XPATH['Amount']).text
                            tradeDictionary['QuotedCurrency']= root.find(XPATH['QuotedCurrency']).attrib[GMT_PREFIX+'Id']
                            tradeDictionary['CallPut']= 'Put' if root.find(XPATH['CallPut']).text == 'Call' else 'Call'
                            tradeDictionary['Strike']= root.find(XPATH['Strike']).text
                            tradeDictionary['PayoffDate']= root.find(XPATH['PayoffDate']).text
                            tradeDictionary['PayoffType']= root.find(XPATH['PayoffType']).text
                            tradeDictionary['OptionType']= root.find(XPATH['OptionType']).text
                            tradeDictionary['ExpiryEventDate']= root.find(XPATH['ExpiryEvent']).attrib[GMT_PREFIX+'ExpiryDate']
                            tradeDictionary['ExpiryEventCutCode']= root.find(XPATH['ExpiryEvent']).attrib[GMT_PREFIX+'ExpiryCutCode']
                            tradeDictionary['Portfolio']= root.find(XPATH['Portfolio']).attrib[GMT_PREFIX+'Id']
                            tradeDictionary['CounterpartyID']= root.find(XPATH['Counterparty']).attrib[GMT_PREFIX+'Id']
                            tradeDictionary['BuyOrSell']=root.find(XPATH['BuyOrSell']).text
                            tradeDictionary['TradePrice']= root.find(XPATH['TradePrice']).text
                            tradeDictionary['BookingBaseCurrency']= root.find(XPATH['BookingBaseCurrency']).attrib[GMT_PREFIX+'Id']
                            tradeDictionary['BookingQuotedCurrency']= root.find(XPATH['BookingQuotedCurrency']).attrib[GMT_PREFIX+'Id']
                            tradeDictionary['BasePerQuoted']= root.find(XPATH['BasePerQuoted']).attrib[GMT_PREFIX+'BasePerQuoted']
                            tradeDictionary['PremiumDate'], tradeDictionary['PremiumAmount'], tradeDictionary['PremiumCurrency'] = FXOTrade.getPremiumDateAmountCurrency(root.find(XPATH['FlowList']))
                            tradeDictionary['EventType']= root.find(XPATH['EventType']).attrib[GMT_PREFIX+'EventType']
                            tradeDictionary['EventReason']= root.find(XPATH['EventType']).attrib[GMT_PREFIX+'EventReason']
                            tradeDictionary['TradeDate']= root.find(XPATH['TradeDate']).text.split('T')[0]
                            
                            #print tradeDictionary['PayoffType']
                            
                            if tradeDictionary['EventType'] == "NewTrade" and tradeDictionary['EventReason'] == "":
                                trade = FXOTrade(tradeDictionary)
                                insName, trdNbr = trade.CreateTrade()
                                if dict['BARXTSSource'] == "Yes":
                                        print "CREATED FX Option:\tInstrument:\t%s\tBARX FX TS Trade:\t%s\t\tFA Trade:\t%s" % (insName, tradeDictionary['TradeID'], trdNbr)
                                else:
                                        print "CREATED FX Option:\tInstrument:\t%s\tMurex Trade:\t%s\t\tFA Trade:\t%s" % (insName, tradeDictionary['TradeID'], trdNbr)
                            else:
                                print "SKIPPED FX Option:\tEventType:\t%s\tEventReason:\t%sId:\t%s" % (tradeDictionary['EventType'], tradeDictionary['EventReason'], tradeDictionary['TradeID'])
                        #--------------Digital European Option ---------------
                        elif InsType == 'FX Option' and InsSubType == 'Digital':
                            XPATH = {
                            'EconomicUnderlyingCurrency' : GMT_PREFIX.join([GMT_PREFIX+'Instrument/', 'EconomicDetail/', 'AssetDetail/', 'OptionUnderlying/', 'Underlying/', 'EconomicDetail/', 'FXDetails/', 'QuotedCurrency']),
                            'EconomicBaseCurrency' : GMT_PREFIX.join([GMT_PREFIX+'Instrument/', 'EconomicDetail/', 'AssetDetail/', 'OptionUnderlying/', 'Underlying/', 'EconomicDetail/', 'FXDetails/', 'BaseCurrency']),
                            'Amount' : GMT_PREFIX.join([GMT_PREFIX+'Instrument/', 'EconomicDetail/', 'AssetDetail/', 'OptionUnderlying/', 'Underlying/', 'EconomicDetail/', 'FXDetails/', 'Amount']),
                            'QuotedCurrency' : GMT_PREFIX.join([GMT_PREFIX+'Instrument/', 'EconomicDetail/', 'AssetDetail/', 'OptionUnderlying/', 'Underlying/', 'EconomicDetail/', 'FXDetails/', 'QuotedCurrency']),
                            'CallPut' : GMT_PREFIX.join([GMT_PREFIX+'Instrument/', 'EconomicDetail/', 'AssetDetail/', 'OptionUnderlying/', 'LocalPayoffDetails/', 'OptionPayoffStyle']),
                            'Strike' : GMT_PREFIX.join([GMT_PREFIX+'Instrument/', 'EconomicDetail/', 'AssetDetail/', 'OptionUnderlying/', 'LocalPayoffDetails/', 'OptionStrike']),
                            'PayoffDate' : GMT_PREFIX.join([GMT_PREFIX+'Instrument/', 'EconomicDetail/', 'AssetDetail/', 'OptionUnderlying/', 'LocalPayoffDetails/', 'PayoffDate']),
                            'PayoffType' : GMT_PREFIX.join([GMT_PREFIX+'Instrument/', 'EconomicDetail/', 'AssetDetail/', 'PayoffInCashOrAsset']),
                            'OptionType' : GMT_PREFIX.join([GMT_PREFIX+'Instrument/', 'EconomicDetail/', 'AssetDetail/', 'OptionExpiryStyle']),
                            'ExpiryEvent' : GMT_PREFIX.join([GMT_PREFIX+'Instrument/', 'EconomicDetail/', 'AssetDetail/', 'OptionExpiryEvent']),
                            'Portfolio' : GMT_PREFIX.join([GMT_PREFIX+'Instrument/', 'BookingDetail/', 'Book']),
                            'Counterparty' : GMT_PREFIX.join([GMT_PREFIX+'Instrument/', 'BookingDetail/', 'Counterparty']),
                            'BuyOrSell' : GMT_PREFIX.join([GMT_PREFIX+'Instrument/', 'BookingDetail/', 'BuyOrSell']),
                            'TradePrice' : GMT_PREFIX.join([GMT_PREFIX+'Instrument/', 'BookingDetail/', 'TradePrice/', 'Rate']),
                            'BookingBaseCurrency' : GMT_PREFIX.join([GMT_PREFIX+'Instrument/', 'BookingDetail/', 'TradePrice/', 'BaseCurrency']),
                            'BookingQuotedCurrency' : GMT_PREFIX.join([GMT_PREFIX+'Instrument/', 'BookingDetail/', 'TradePrice/', 'QuotedCurrency']),
                            'BasePerQuoted' : GMT_PREFIX.join([GMT_PREFIX+'Instrument/', 'BookingDetail/', 'TradePrice/', 'Rate']),
                            'FlowList' : GMT_PREFIX.join([GMT_PREFIX+'Instrument/', 'BookingDetail/', 'FlowList']),
                            'EventType' : GMT_PREFIX.join([GMT_PREFIX+'TradeDetail/', 'Audit']),
                            'TradeDate' : GMT_PREFIX.join([GMT_PREFIX+'TradeDetail/', 'TradeDate'])
                            }
                            tradeDictionary = dict.copy()
                            tradeDictionary['TradeID'] = root.find(GMT_PREFIX+"TradeDetail").attrib[GMT_PREFIX+'Id']
                            tradeDictionary['InsType'] = root.find(GMT_PREFIX+'Instrument').attrib[GMT_PREFIX+'Type']
                            tradeDictionary['InsSubType']=root.find(GMT_PREFIX+'Instrument').attrib[GMT_PREFIX+'SubType']
                            tradeDictionary['EconomicUnderlyingCurrency']= root.find(XPATH['EconomicUnderlyingCurrency']).attrib[GMT_PREFIX+'Id']
                            tradeDictionary['EconomicBaseCurrency']= root.find(XPATH['EconomicBaseCurrency']).attrib[GMT_PREFIX+'Id']
                            tradeDictionary['Amount']= root.find(XPATH['Amount']).text
                            tradeDictionary['QuotedCurrency']= root.find(XPATH['QuotedCurrency']).attrib[GMT_PREFIX+'Id']
                            tradeDictionary['CallPut']= 'Put' if root.find(XPATH['CallPut']).text == 'Call' else 'Call'
                            tradeDictionary['Strike']= root.find(XPATH['Strike']).text
                            tradeDictionary['PayoffDate']= root.find(XPATH['PayoffDate']).text
                            tradeDictionary['PayoffType']= root.find(XPATH['PayoffType']).text
                            tradeDictionary['OptionType']= root.find(XPATH['OptionType']).text
                            tradeDictionary['ExpiryEventDate']= root.find(XPATH['ExpiryEvent']).attrib[GMT_PREFIX+'ExpiryDate']
                            tradeDictionary['ExpiryEventCutCode']= root.find(XPATH['ExpiryEvent']).attrib[GMT_PREFIX+'ExpiryCutCode']
                            tradeDictionary['Portfolio']= root.find(XPATH['Portfolio']).attrib[GMT_PREFIX+'Id']
                            tradeDictionary['CounterpartyID']= root.find(XPATH['Counterparty']).attrib[GMT_PREFIX+'Id']
                            tradeDictionary['BuyOrSell']=root.find(XPATH['BuyOrSell']).text
                            tradeDictionary['TradePrice']= root.find(XPATH['TradePrice']).text
                            tradeDictionary['BookingBaseCurrency']= root.find(XPATH['BookingBaseCurrency']).attrib[GMT_PREFIX+'Id']
                            tradeDictionary['BookingQuotedCurrency']= root.find(XPATH['BookingQuotedCurrency']).attrib[GMT_PREFIX+'Id']
                            tradeDictionary['BasePerQuoted']= root.find(XPATH['BasePerQuoted']).attrib[GMT_PREFIX+'BasePerQuoted']
                            tradeDictionary['PremiumDate'], tradeDictionary['PremiumAmount'], tradeDictionary['PremiumCurrency'] = FXOTrade.getPremiumDateAmountCurrency(root.find(XPATH['FlowList']))
                            tradeDictionary['EventType']= root.find(XPATH['EventType']).attrib[GMT_PREFIX+'EventType']
                            tradeDictionary['EventReason']= root.find(XPATH['EventType']).attrib[GMT_PREFIX+'EventReason']
                            tradeDictionary['TradeDate']= root.find(XPATH['TradeDate']).text.split('T')[0]
                            if tradeDictionary['EventType'] == "NewTrade" and tradeDictionary['EventReason'] == "":
                                trade = DigitalEuropeanTrade(tradeDictionary)
                                insName, trdNbr = trade.CreateTrade()
                                if dict['BARXTSSource'] == "Yes":
                                        print "CREATED FX Digital Option:\tInstrument:\t%s\tBARX FX TS Trade:\t%s\t\tFA Trade:\t%s" % (insName, tradeDictionary['TradeID'], trdNbr)
                                else:
                                        print "CREATED FX Digital Option:\tInstrument:\t%s\tMurex Trade:\t%s\t\tFA Trade:\t%s" % (insName, tradeDictionary['TradeID'], trdNbr)
                            else:
                                print "SKIPPED FX Digital Option:\tEventType:\t%s\tEventReason:\t%sId:\t%s" % (tradeDictionary['EventType'], tradeDictionary['EventReason'], tradeDictionary['TradeID'])
                        #--------------Single Barrier Option ---------------
                        elif InsType == 'FX Option' and InsSubType == 'SingleBarrier':
                            XPATH = {
                            'EconomicUnderlyingCurrency' : GMT_PREFIX.join([GMT_PREFIX+'Instrument/', 'EconomicDetail/', 'AssetDetail/', 'OptionUnderlying/', 'Underlying/', 'EconomicDetail/', 'FXDetails/', 'Currency']),
                            'EconomicBaseCurrency' : GMT_PREFIX.join([GMT_PREFIX+'Instrument/', 'EconomicDetail/', 'AssetDetail/', 'OptionUnderlying/', 'Underlying/', 'EconomicDetail/', 'FXDetails/', 'BaseCurrency']),
                            'Amount' : GMT_PREFIX.join([GMT_PREFIX+'Instrument/', 'EconomicDetail/', 'AssetDetail/', 'OptionUnderlying/', 'Underlying/', 'EconomicDetail/', 'FXDetails/', 'Amount']),
                            'QuotedCurrency' : GMT_PREFIX.join([GMT_PREFIX+'Instrument/', 'EconomicDetail/', 'AssetDetail/', 'OptionUnderlying/', 'Underlying/', 'EconomicDetail/', 'FXDetails/', 'QuotedCurrency']),
                            'CallPut' : GMT_PREFIX.join([GMT_PREFIX+'Instrument/', 'EconomicDetail/', 'AssetDetail/', 'OptionUnderlying/', 'LocalPayoffDetails/', 'OptionPayoffStyle']),
                            'Strike' : GMT_PREFIX.join([GMT_PREFIX+'Instrument/', 'EconomicDetail/', 'AssetDetail/', 'OptionUnderlying/', 'LocalPayoffDetails/', 'OptionStrike']),
                            'PayoffDate' : GMT_PREFIX.join([GMT_PREFIX+'Instrument/', 'EconomicDetail/', 'AssetDetail/', 'OptionUnderlying/', 'LocalPayoffDetails/', 'PayoffDate']),
                            'PayoffType' : GMT_PREFIX.join([GMT_PREFIX+'Instrument/', 'EconomicDetail/', 'AssetDetail/', 'PayoffInCashOrAsset']),
                            'OptionType' : GMT_PREFIX.join([GMT_PREFIX+'Instrument/', 'EconomicDetail/', 'AssetDetail/', 'OptionExpiryStyle']),
                            'ExpiryEvent' : GMT_PREFIX.join([GMT_PREFIX+'Instrument/', 'EconomicDetail/', 'AssetDetail/', 'OptionExpiryEvent']),
                            'Portfolio' : GMT_PREFIX.join([GMT_PREFIX+'Instrument/', 'BookingDetail/', 'Book']),
                            'Counterparty' : GMT_PREFIX.join([GMT_PREFIX+'Instrument/', 'BookingDetail/', 'Counterparty']),
                            'BuyOrSell' : GMT_PREFIX.join([GMT_PREFIX+'Instrument/', 'BookingDetail/', 'BuyOrSell']),
                            'TradePrice' : GMT_PREFIX.join([GMT_PREFIX+'Instrument/', 'BookingDetail/', 'TradePrice/', 'Rate']),
                            'BookingBaseCurrency' : GMT_PREFIX.join([GMT_PREFIX+'Instrument/', 'BookingDetail/', 'TradePrice/', 'BaseCurrency']),
                            'BookingQuotedCurrency' : GMT_PREFIX.join([GMT_PREFIX+'Instrument/', 'BookingDetail/', 'TradePrice/', 'QuotedCurrency']),
                            'BasePerQuoted' : GMT_PREFIX.join([GMT_PREFIX+'Instrument/', 'BookingDetail/', 'TradePrice/', 'Rate']),
                            'FlowList' : GMT_PREFIX.join([GMT_PREFIX+'Instrument/', 'BookingDetail/', 'FlowList']),
                            'EventType' : GMT_PREFIX.join([GMT_PREFIX+'TradeDetail/', 'Audit']),
                            'TradeDate' : GMT_PREFIX.join([GMT_PREFIX+'TradeDetail/', 'TradeDate']),
                            'BarrierStartLevel' : GMT_PREFIX.join([GMT_PREFIX+'Instrument/', 'EconomicDetail/', 'AssetDetail/', 'OptionUnderlying/', 'Barrier/', 'BarrierEvent/', 'StartEvent/', 'Amount']),
                            'BarrierEndLevel' : GMT_PREFIX.join([GMT_PREFIX+'Instrument/', 'EconomicDetail/', 'AssetDetail/', 'OptionUnderlying/', 'Barrier/', 'BarrierEvent/', 'EndEvent/', 'Amount']),
                            'BarrierSettings' : GMT_PREFIX.join([GMT_PREFIX+'Instrument/', 'EconomicDetail/', 'AssetDetail/', 'OptionUnderlying/', 'Barrier/', 'BarrierEvent/', 'SettingSchedule']),
                            'BarrierStart' : GMT_PREFIX.join([GMT_PREFIX+'Instrument/', 'EconomicDetail/', 'AssetDetail/', 'OptionUnderlying/', 'Barrier/', 'BarrierEvent/', 'StartEvent']),
                            'BarrierEnd' : GMT_PREFIX.join([GMT_PREFIX+'Instrument/', 'EconomicDetail/', 'AssetDetail/', 'OptionUnderlying/', 'Barrier/', 'BarrierEvent/', 'EndEvent']),
                            'Rebate' : GMT_PREFIX.join([GMT_PREFIX+'Instrument/', 'EconomicDetail/', 'AssetDetail/', 'OptionUnderlying/', 'Barrier/', 'BarrierRebateOnSchedule/', 'Rebate/', 'Rate']),
                            'DelayRebate' : GMT_PREFIX.join([GMT_PREFIX+'Instrument/', 'EconomicDetail/', 'AssetDetail/', 'OptionUnderlying/', 'Barrier/', 'BarrierRebateOnSchedule/', 'DelayRebate']),
                            'Barrier' : GMT_PREFIX.join([GMT_PREFIX+'Instrument/', 'EconomicDetail/', 'AssetDetail/', 'OptionUnderlying/', 'Barrier']),
                            'BarrierEvent' : GMT_PREFIX.join([GMT_PREFIX+'Instrument/', 'EconomicDetail/', 'AssetDetail/', 'OptionUnderlying/', 'Barrier/', 'BarrierEvent'])
                            }
                            tradeDictionary = dict.copy()
                            tradeDictionary['TradeID'] = root.find(GMT_PREFIX+"TradeDetail").attrib[GMT_PREFIX+'Id']
                            tradeDictionary['InsType'] = root.find(GMT_PREFIX+'Instrument').attrib[GMT_PREFIX+'Type']
                            tradeDictionary['InsSubType']=root.find(GMT_PREFIX+'Instrument').attrib[GMT_PREFIX+'SubType']
                            tradeDictionary['EconomicUnderlyingCurrency']= root.find(XPATH['EconomicUnderlyingCurrency']).attrib[GMT_PREFIX+'Id']
                            tradeDictionary['EconomicBaseCurrency']= root.find(XPATH['EconomicBaseCurrency']).attrib[GMT_PREFIX+'Id']
                            tradeDictionary['Amount']= root.find(XPATH['Amount']).text
                            tradeDictionary['QuotedCurrency']= root.find(XPATH['QuotedCurrency']).attrib[GMT_PREFIX+'Id']
                            tradeDictionary['CallPut']= 'Put' if root.find(XPATH['CallPut']).text == 'Call' else 'Call'
                            tradeDictionary['Strike']= root.find(XPATH['Strike']).text
                            tradeDictionary['PayoffDate']= root.find(XPATH['PayoffDate']).text
                            tradeDictionary['PayoffType']= root.find(XPATH['PayoffType']).text
                            tradeDictionary['OptionType']= root.find(XPATH['OptionType']).text
                            tradeDictionary['ExpiryEventDate']= root.find(XPATH['ExpiryEvent']).attrib[GMT_PREFIX+'ExpiryDate']
                            tradeDictionary['ExpiryEventCutCode']= root.find(XPATH['ExpiryEvent']).attrib[GMT_PREFIX+'ExpiryCutCode']
                            tradeDictionary['Portfolio']= root.find(XPATH['Portfolio']).attrib[GMT_PREFIX+'Id']
                            tradeDictionary['CounterpartyID']= root.find(XPATH['Counterparty']).attrib[GMT_PREFIX+'Id']
                            tradeDictionary['BuyOrSell']=root.find(XPATH['BuyOrSell']).text
                            tradeDictionary['TradePrice']= root.find(XPATH['TradePrice']).text
                            tradeDictionary['BookingBaseCurrency']= root.find(XPATH['BookingBaseCurrency']).attrib[GMT_PREFIX+'Id']
                            tradeDictionary['BookingQuotedCurrency']= root.find(XPATH['BookingQuotedCurrency']).attrib[GMT_PREFIX+'Id']
                            tradeDictionary['BasePerQuoted']= root.find(XPATH['BasePerQuoted']).attrib[GMT_PREFIX+'BasePerQuoted']
                            tradeDictionary['PremiumDate'], tradeDictionary['PremiumAmount'], tradeDictionary['PremiumCurrency'] = FXOTrade.getPremiumDateAmountCurrency(root.find(XPATH['FlowList']))
                            tradeDictionary['EventType']= root.find(XPATH['EventType']).attrib[GMT_PREFIX+'EventType']
                            tradeDictionary['EventReason']= root.find(XPATH['EventType']).attrib[GMT_PREFIX+'EventReason']
                            tradeDictionary['TradeDate']= root.find(XPATH['TradeDate']).text.split('T')[0]
                            
                            isValid = 1
                            if root.find(XPATH['BarrierStartLevel']).text!=root.find(XPATH['BarrierEndLevel']).text:
                                isValid=0
                            else:
                                tradeDictionary['BarrierLevel']=root.find(XPATH['BarrierStartLevel']).text
                                tradeDictionary['BarrierType']=root.find(XPATH['Barrier']).attrib[GMT_PREFIX+'UpOrDown'] + ' & ' + root.find(XPATH['Barrier']).attrib[GMT_PREFIX+'KnockInOrOut']
                                tradeDictionary['Rebate']=root.find(XPATH['Rebate']).text
                                
                                if root.find(XPATH['BarrierEvent']).find(GMT_PREFIX+'BarrierRebateOnSchedule')!=None:
                                    tradeDictionary['PayAtExpiry']=0 if root.find(XPATH['BarrierEvent']).find(GMT_PREFIX+'BarrierRebateOnSchedule').find(GMT_PREFIX+'DelayRebate').text=='true' else 1
                                elif root.find(XPATH['Barrier']).find(GMT_PREFIX+'BarrierRebateOnSchedule')!=None:
                                    tradeDictionary['PayAtExpiry']=0 if root.find(XPATH['Barrier']).find(GMT_PREFIX+'BarrierRebateOnSchedule').find(GMT_PREFIX+'DelayRebate').text=='true' else 1
                                else:
                                    tradeDictionary['PayAtExpiry']=0
                                
                                barrierEventDates = []
                                c=0
                                for be in root.findall(XPATH['BarrierEvent']):

                                    try:
                                        if be.attrib[GMT_PREFIX+'Discrete']=='true':
                                            tradeDictionary['BarrierMonitoring']=3
                                    except:
                                        tradeDictionary['BarrierMonitoring']=2 #for now, if its not discrete it must be window

                                    startDate = be.find(GMT_PREFIX+'StartEvent').attrib[GMT_PREFIX+'Date']
                                    endDate = be.find(GMT_PREFIX+'EndEvent').attrib[GMT_PREFIX+'Date'] 
                                    barrierEventDates.append((startDate, endDate))
                                    ++c
                                      
                                tradeDictionary['BarrierEventDates']=barrierEventDates
                                if root.find(XPATH['BarrierSettings'])!=None:
                                    if root.find(XPATH['BarrierSettings']).find(GMT_PREFIX+'FixingSource')!=None:
                                        tradeDictionary['FixingSource']=root.find(XPATH['BarrierSettings']).find(GMT_PREFIX+'FixingSource').find(GMT_PREFIX+'Label').text
                                else:
                                    tradeDictionary['FixingSource']=''

                            if isValid==1 and tradeDictionary['EventType'] == "NewTrade" and tradeDictionary['EventReason'] == "":
                                trade = FXOSingleBarrierTrade(tradeDictionary)
                                insName, trdNbr = trade.CreateTrade()
                                if dict['BARXTSSource'] == "Yes":
                                        print "CREATED FX Single Barrier Option:\tInstrument:\t%s\tBARX FX TS Trade:\t%s\t\tFA Trade:\t%s" % (insName, tradeDictionary['TradeID'], trdNbr)
                                else:
                                        print "CREATED FX Single Barrier Option:\tInstrument:\t%s\tMurex Trade:\t%s\t\tFA Trade:\t%s" % (insName, tradeDictionary['TradeID'], trdNbr)
                            else:
                                print "SKIPPED FX Single Barrier Option:\tisValid:\t%s\t\tEventType:\t%s\tEventReason:\t%sId:\t%s" % isValid, (tradeDictionary['EventType'], tradeDictionary['EventReason'], tradeDictionary['TradeID'])
                        #--------------Double Barrier Option ---------------
                        elif InsType == 'FX Option' and InsSubType == 'DoubleBarrier':
                            XPATH = {
                            'EconomicUnderlyingCurrency' : GMT_PREFIX.join([GMT_PREFIX+'Instrument/', 'EconomicDetail/', 'AssetDetail/', 'OptionUnderlying/', 'Underlying/', 'EconomicDetail/', 'FXDetails/', 'QuotedCurrency']),
                            'EconomicBaseCurrency' : GMT_PREFIX.join([GMT_PREFIX+'Instrument/', 'EconomicDetail/', 'AssetDetail/', 'OptionUnderlying/', 'Underlying/', 'EconomicDetail/', 'FXDetails/', 'BaseCurrency']),
                            'Amount' : GMT_PREFIX.join([GMT_PREFIX+'Instrument/', 'EconomicDetail/', 'AssetDetail/', 'OptionUnderlying/', 'Underlying/', 'EconomicDetail/', 'FXDetails/', 'Amount']),
                            'QuotedCurrency' : GMT_PREFIX.join([GMT_PREFIX+'Instrument/', 'EconomicDetail/', 'AssetDetail/', 'OptionUnderlying/', 'Underlying/', 'EconomicDetail/', 'FXDetails/', 'QuotedCurrency']),
                            'CallPut' : GMT_PREFIX.join([GMT_PREFIX+'Instrument/', 'EconomicDetail/', 'AssetDetail/', 'OptionUnderlying/', 'LocalPayoffDetails/', 'OptionPayoffStyle']),
                            'Strike' : GMT_PREFIX.join([GMT_PREFIX+'Instrument/', 'EconomicDetail/', 'AssetDetail/', 'OptionUnderlying/', 'LocalPayoffDetails/', 'OptionStrike']),
                            'PayoffDate' : GMT_PREFIX.join([GMT_PREFIX+'Instrument/', 'EconomicDetail/', 'AssetDetail/', 'OptionUnderlying/', 'LocalPayoffDetails/', 'PayoffDate']),
                            'PayoffType' : GMT_PREFIX.join([GMT_PREFIX+'Instrument/', 'EconomicDetail/', 'AssetDetail/', 'PayoffInCashOrAsset']),
                            'OptionType' : GMT_PREFIX.join([GMT_PREFIX+'Instrument/', 'EconomicDetail/', 'AssetDetail/', 'OptionExpiryStyle']),
                            'ExpiryEvent' : GMT_PREFIX.join([GMT_PREFIX+'Instrument/', 'EconomicDetail/', 'AssetDetail/', 'OptionExpiryEvent']),
                            'Portfolio' : GMT_PREFIX.join([GMT_PREFIX+'Instrument/', 'BookingDetail/', 'Book']),
                            'Counterparty' : GMT_PREFIX.join([GMT_PREFIX+'Instrument/', 'BookingDetail/', 'Counterparty']),
                            'BuyOrSell' : GMT_PREFIX.join([GMT_PREFIX+'Instrument/', 'BookingDetail/', 'BuyOrSell']),
                            'TradePrice' : GMT_PREFIX.join([GMT_PREFIX+'Instrument/', 'BookingDetail/', 'TradePrice/', 'Rate']),
                            'BookingBaseCurrency' : GMT_PREFIX.join([GMT_PREFIX+'Instrument/', 'BookingDetail/', 'TradePrice/', 'BaseCurrency']),
                            'BookingQuotedCurrency' : GMT_PREFIX.join([GMT_PREFIX+'Instrument/', 'BookingDetail/', 'TradePrice/', 'QuotedCurrency']),
                            'BasePerQuoted' : GMT_PREFIX.join([GMT_PREFIX+'Instrument/', 'BookingDetail/', 'TradePrice/', 'Rate']),
                            'FlowList' : GMT_PREFIX.join([GMT_PREFIX+'Instrument/', 'BookingDetail/', 'FlowList']),
                            'EventType' : GMT_PREFIX.join([GMT_PREFIX+'TradeDetail/', 'Audit']),
                            'TradeDate' : GMT_PREFIX.join([GMT_PREFIX+'TradeDetail/', 'TradeDate']),
                            'Barriers' : GMT_PREFIX.join([GMT_PREFIX+'Instrument/', 'EconomicDetail/', 'AssetDetail/', 'OptionUnderlying/', 'Barrier'])
                            }
                            tradeDictionary = dict.copy()
                            tradeDictionary['TradeID'] = root.find(GMT_PREFIX+"TradeDetail").attrib[GMT_PREFIX+'Id']
                            tradeDictionary['InsType'] = root.find(GMT_PREFIX+'Instrument').attrib[GMT_PREFIX+'Type']
                            tradeDictionary['InsSubType']=root.find(GMT_PREFIX+'Instrument').attrib[GMT_PREFIX+'SubType']
                            tradeDictionary['EconomicUnderlyingCurrency']= root.find(XPATH['EconomicUnderlyingCurrency']).attrib[GMT_PREFIX+'Id']
                            tradeDictionary['EconomicBaseCurrency']= root.find(XPATH['EconomicBaseCurrency']).attrib[GMT_PREFIX+'Id']
                            tradeDictionary['Amount']= root.find(XPATH['Amount']).text
                            tradeDictionary['QuotedCurrency']= root.find(XPATH['QuotedCurrency']).attrib[GMT_PREFIX+'Id']
                            tradeDictionary['CallPut']= 'Put' if root.find(XPATH['CallPut']).text == 'Call' else 'Call'
                            tradeDictionary['Strike']= root.find(XPATH['Strike']).text
                            tradeDictionary['PayoffDate']= root.find(XPATH['PayoffDate']).text
                            tradeDictionary['PayoffType']= root.find(XPATH['PayoffType']).text
                            tradeDictionary['OptionType']= root.find(XPATH['OptionType']).text
                            tradeDictionary['ExpiryEventDate']= root.find(XPATH['ExpiryEvent']).attrib[GMT_PREFIX+'ExpiryDate']
                            tradeDictionary['ExpiryEventCutCode']= root.find(XPATH['ExpiryEvent']).attrib[GMT_PREFIX+'ExpiryCutCode']
                            tradeDictionary['Portfolio']= root.find(XPATH['Portfolio']).attrib[GMT_PREFIX+'Id']
                            tradeDictionary['CounterpartyID']= root.find(XPATH['Counterparty']).attrib[GMT_PREFIX+'Id']
                            tradeDictionary['BuyOrSell']=root.find(XPATH['BuyOrSell']).text
                            tradeDictionary['TradePrice']= root.find(XPATH['TradePrice']).text
                            tradeDictionary['BookingBaseCurrency']= root.find(XPATH['BookingBaseCurrency']).attrib[GMT_PREFIX+'Id']
                            tradeDictionary['BookingQuotedCurrency']= root.find(XPATH['BookingQuotedCurrency']).attrib[GMT_PREFIX+'Id']
                            tradeDictionary['BasePerQuoted']= root.find(XPATH['BasePerQuoted']).attrib[GMT_PREFIX+'BasePerQuoted']
                            tradeDictionary['PremiumDate'], tradeDictionary['PremiumAmount'], tradeDictionary['PremiumCurrency'] = FXOTrade.getPremiumDateAmountCurrency(root.find(XPATH['FlowList']))
                            tradeDictionary['EventType']= root.find(XPATH['EventType']).attrib[GMT_PREFIX+'EventType']
                            tradeDictionary['EventReason']= root.find(XPATH['EventType']).attrib[GMT_PREFIX+'EventReason']
                            tradeDictionary['TradeDate']= root.find(XPATH['TradeDate']).text.split('T')[0]
                            #tradeDictionary['RebateCurrency']= root.find(XPATH['Rebate']).find(GMT_PREFIX+'QuotedCurrency').attrib[GMT_PREFIX+'Id']
                            
                            isValid = 1
                            barriers = root.findall(XPATH['Barriers'])
                            #print barriers[1].find(GMT_PREFIX+'BarrierEvent').find(GMT_PREFIX+'StartEvent').find(GMT_PREFIX+'Amount').text
                            if len(barriers)!=2 or \
                                barriers[0].find(GMT_PREFIX+'BarrierEvent').find(GMT_PREFIX+'StartEvent').attrib[GMT_PREFIX+'Date']!=barriers[1].find(GMT_PREFIX+'BarrierEvent').find(GMT_PREFIX+'StartEvent').attrib[GMT_PREFIX+'Date'] or \
                                barriers[0].find(GMT_PREFIX+'BarrierEvent').find(GMT_PREFIX+'StartEvent').find(GMT_PREFIX+'Amount').text!=barriers[0].find(GMT_PREFIX+'BarrierEvent').find(GMT_PREFIX+'EndEvent').find(GMT_PREFIX+'Amount').text or \
                                barriers[0].find(GMT_PREFIX+'BarrierEvent').find(GMT_PREFIX+'EndEvent').attrib[GMT_PREFIX+'Date']!=barriers[1].find(GMT_PREFIX+'BarrierEvent').find(GMT_PREFIX+'EndEvent').attrib[GMT_PREFIX+'Date'] or \
                                barriers[1].find(GMT_PREFIX+'BarrierEvent').find(GMT_PREFIX+'StartEvent').find(GMT_PREFIX+'Amount').text!=barriers[1].find(GMT_PREFIX+'BarrierEvent').find(GMT_PREFIX+'EndEvent').find(GMT_PREFIX+'Amount').text or \
                                barriers[0].attrib[GMT_PREFIX+'KnockInOrOut']!=barriers[1].attrib[GMT_PREFIX+'KnockInOrOut']:
                                
                                isValid=0
                            else:
                                #print 'gets this far'
                                tradeDictionary['BarrierLevel1']=barriers[0].find(GMT_PREFIX+'BarrierEvent').find(GMT_PREFIX+'StartEvent').find(GMT_PREFIX+'Amount').text
                                tradeDictionary['BarrierLevel2']=barriers[1].find(GMT_PREFIX+'BarrierEvent').find(GMT_PREFIX+'StartEvent').find(GMT_PREFIX+'Amount').text
                                tradeDictionary['BarrierType']='Double ' + barriers[0].attrib[GMT_PREFIX+'KnockInOrOut']
                                tradeDictionary['Rebate']=0
                                tradeDictionary['PayAtExpiry']=0 if barriers[0].find(GMT_PREFIX+'BarrierRebateOnSchedule').find(GMT_PREFIX+'DelayRebate').text=='true' else 1

                                barrierEventDates = []
                                
                                be=barriers[0].find(GMT_PREFIX+'BarrierEvent')

                                try:
                                    if be.attrib[GMT_PREFIX+'Discrete']=='true':
                                        tradeDictionary['BarrierMonitoring']=3
                                    else:
                                        tradeDictionary['BarrierMonitoring']=2
                                except:
                                    tradeDictionary['BarrierMonitoring']=2 #for now, if its not discrete it must be window
                                        
                                startDate = be.find(GMT_PREFIX+'StartEvent').attrib[GMT_PREFIX+'Date']
                                endDate = be.find(GMT_PREFIX+'EndEvent').attrib[GMT_PREFIX+'Date'] 
                                barrierEventDates.append((startDate, endDate))
                                    
                                tradeDictionary['BarrierEventDates']=barrierEventDates
                            if isValid==1 and tradeDictionary['EventType'] == "NewTrade" and tradeDictionary['EventReason'] == "":
                                trade = FXODoubleBarrierTrade(tradeDictionary)
                                insName, trdNbr = trade.CreateTrade()
                                if dict['BARXTSSource'] == "Yes":
                                        print "CREATED FX Double Barrier Option:\tInstrument:\t%s\tBARX FX TS Trade:\t%s\t\tFA Trade:\t%s" % (insName, tradeDictionary['TradeID'], trdNbr)
                                else:
                                        print "CREATED FX Double Barrier Option:\tInstrument:\t%s\tMurex Trade:\t%s\t\tFA Trade:\t%s" % (insName, tradeDictionary['TradeID'], trdNbr)
                            else:
                                print "SKIPPED FX Double Barrier Option:\tisValid:\t%s\t\tEventType:\t%s\tEventReason:\t%sId:\t%s" % isValid, (tradeDictionary['EventType'], tradeDictionary['EventReason'], tradeDictionary['TradeID'])
                        #--------------One Touch Option ---------------
                        elif InsType == 'FX Option' and (InsSubType == 'OneTouchUp' or InsSubType == 'OneTouchDown' or InsSubType == 'NoTouchUp'or InsSubType == 'NoTouchDown'):
                            XPATH = {
                            'EconomicUnderlyingCurrency' : GMT_PREFIX.join([GMT_PREFIX+'Instrument/', 'EconomicDetail/', 'AssetDetail/', 'OptionUnderlying/', 'Underlying/', 'EconomicDetail/', 'FXDetails/', 'QuotedCurrency']),
                            'EconomicBaseCurrency' : GMT_PREFIX.join([GMT_PREFIX+'Instrument/', 'EconomicDetail/', 'AssetDetail/', 'OptionUnderlying/', 'Underlying/', 'EconomicDetail/', 'FXDetails/', 'BaseCurrency']),
                            'Amount' : GMT_PREFIX.join([GMT_PREFIX+'Instrument/', 'EconomicDetail/', 'AssetDetail/', 'OptionUnderlying/', 'Underlying/', 'EconomicDetail/', 'FXDetails/', 'Amount']),
                            'QuotedCurrency' : GMT_PREFIX.join([GMT_PREFIX+'Instrument/', 'EconomicDetail/', 'AssetDetail/', 'OptionUnderlying/', 'Underlying/', 'EconomicDetail/', 'FXDetails/', 'QuotedCurrency']),
                            'PayoffDate' : GMT_PREFIX.join([GMT_PREFIX+'Instrument/', 'EconomicDetail/', 'AssetDetail/', 'OptionUnderlying/', 'LocalPayoffDetails/', 'PayoffDate']),
                            'PayoffType' : GMT_PREFIX.join([GMT_PREFIX+'Instrument/', 'EconomicDetail/', 'AssetDetail/', 'PayoffInCashOrAsset']),
                            'OptionType' : GMT_PREFIX.join([GMT_PREFIX+'Instrument/', 'EconomicDetail/', 'AssetDetail/', 'OptionExpiryStyle']),
                            'TradeCurrency' : GMT_PREFIX.join([GMT_PREFIX+'Instrument/', 'EconomicDetail/', 'AssetDetail/', 'Currency']),
                            'ExpiryEvent' : GMT_PREFIX.join([GMT_PREFIX+'Instrument/', 'EconomicDetail/', 'AssetDetail/', 'OptionExpiryEvent']),
                            'Portfolio' : GMT_PREFIX.join([GMT_PREFIX+'Instrument/', 'BookingDetail/', 'Book']),
                            'Counterparty' : GMT_PREFIX.join([GMT_PREFIX+'Instrument/', 'BookingDetail/', 'Counterparty']),
                            'BuyOrSell' : GMT_PREFIX.join([GMT_PREFIX+'Instrument/', 'BookingDetail/', 'BuyOrSell']),
                            'TradePrice' : GMT_PREFIX.join([GMT_PREFIX+'Instrument/', 'BookingDetail/', 'TradePrice/', 'Rate']),
                            'BookingBaseCurrency' : GMT_PREFIX.join([GMT_PREFIX+'Instrument/', 'BookingDetail/', 'TradePrice/', 'BaseCurrency']),
                            'BookingQuotedCurrency' : GMT_PREFIX.join([GMT_PREFIX+'Instrument/', 'BookingDetail/', 'TradePrice/', 'QuotedCurrency']),
                            'BasePerQuoted' : GMT_PREFIX.join([GMT_PREFIX+'Instrument/', 'BookingDetail/', 'TradePrice/', 'Rate']),
                            'FlowList' : GMT_PREFIX.join([GMT_PREFIX+'Instrument/', 'BookingDetail/', 'FlowList']),
                            'EventType' : GMT_PREFIX.join([GMT_PREFIX+'TradeDetail/', 'Audit']),
                            'TradeDate' : GMT_PREFIX.join([GMT_PREFIX+'TradeDetail/', 'TradeDate']),
                            'Barriers' : GMT_PREFIX.join([GMT_PREFIX+'Instrument/', 'EconomicDetail/', 'AssetDetail/', 'OptionUnderlying/', 'Barrier'])
                            }
                            tradeDictionary = dict.copy()
                            tradeDictionary['TradeID'] = root.find(GMT_PREFIX+"TradeDetail").attrib[GMT_PREFIX+'Id']
                            tradeDictionary['InsType'] = root.find(GMT_PREFIX+'Instrument').attrib[GMT_PREFIX+'Type']
                            tradeDictionary['InsSubType']=root.find(GMT_PREFIX+'Instrument').attrib[GMT_PREFIX+'SubType']
                            tradeDictionary['EconomicUnderlyingCurrency']= root.find(XPATH['EconomicUnderlyingCurrency']).attrib[GMT_PREFIX+'Id']
                            tradeDictionary['EconomicBaseCurrency']= root.find(XPATH['EconomicBaseCurrency']).attrib[GMT_PREFIX+'Id']
                            tradeDictionary['Amount']= root.find(XPATH['Amount']).text
                            tradeDictionary['QuotedCurrency']= root.find(XPATH['QuotedCurrency']).attrib[GMT_PREFIX+'Id']
                            tradeDictionary['PayoffDate']= root.find(XPATH['PayoffDate']).text
                            tradeDictionary['PayoffType']= root.find(XPATH['PayoffType']).text
                            tradeDictionary['OptionType']= root.find(XPATH['OptionType']).text
                            tradeDictionary['ExpiryEventDate']= root.find(XPATH['ExpiryEvent']).attrib[GMT_PREFIX+'ExpiryDate']
                            tradeDictionary['ExpiryEventCutCode']= root.find(XPATH['ExpiryEvent']).attrib[GMT_PREFIX+'ExpiryCutCode']
                            tradeDictionary['Portfolio']= root.find(XPATH['Portfolio']).attrib[GMT_PREFIX+'Id']
                            tradeDictionary['CounterpartyID']= root.find(XPATH['Counterparty']).attrib[GMT_PREFIX+'Id']
                            tradeDictionary['BuyOrSell']=root.find(XPATH['BuyOrSell']).text
                            tradeDictionary['TradePrice']= root.find(XPATH['TradePrice']).text
                            tradeDictionary['BookingBaseCurrency']= root.find(XPATH['BookingBaseCurrency']).attrib[GMT_PREFIX+'Id']
                            tradeDictionary['BookingQuotedCurrency']= root.find(XPATH['BookingQuotedCurrency']).attrib[GMT_PREFIX+'Id']
                            tradeDictionary['BasePerQuoted']= root.find(XPATH['BasePerQuoted']).attrib[GMT_PREFIX+'BasePerQuoted']
                            tradeDictionary['PremiumDate'], tradeDictionary['PremiumAmount'], tradeDictionary['PremiumCurrency'] = FXOTrade.getPremiumDateAmountCurrency(root.find(XPATH['FlowList']))
                            tradeDictionary['EventType']= root.find(XPATH['EventType']).attrib[GMT_PREFIX+'EventType']
                            tradeDictionary['EventReason']= root.find(XPATH['EventType']).attrib[GMT_PREFIX+'EventReason']
                            tradeDictionary['TradeDate']= root.find(XPATH['TradeDate']).text.split('T')[0]
                            tradeDictionary['PayoutCurrency']= root.find(XPATH['TradeCurrency']).attrib[GMT_PREFIX+'Id']
                            
                            tradeDictionary['CallPut']= 'Put' if InsSubType[-4:] == 'Down' else 'Call' #needed to get the correct currencies in Up/Down in FA
                           
                            
                            isValid = 1
                            barriers = root.findall(XPATH['Barriers'])
                            if len(barriers)!=1 or \
                                barriers[0].find(GMT_PREFIX+'BarrierEvent').find(GMT_PREFIX+'StartEvent').find(GMT_PREFIX+'Amount').text!=barriers[0].find(GMT_PREFIX+'BarrierEvent').find(GMT_PREFIX+'EndEvent').find(GMT_PREFIX+'Amount').text:
                                
                                isValid=0
                            else:
                                tradeDictionary['BarrierLevel']=barriers[0].find(GMT_PREFIX+'BarrierEvent').find(GMT_PREFIX+'StartEvent').find(GMT_PREFIX+'Amount').text
                                tradeDictionary['BarrierType']= barriers[0].attrib[GMT_PREFIX+'UpOrDown'] + " & " + barriers[0].attrib[GMT_PREFIX+'KnockInOrOut']
                                tradeDictionary['Rebate']=barriers[0].find(GMT_PREFIX+'BarrierRebateOnSchedule').find(GMT_PREFIX+'Rebate').find(GMT_PREFIX+'Rate').text
                                tradeDictionary['PayAtExpiry']=0 if barriers[0].find(GMT_PREFIX+'BarrierRebateOnSchedule').find(GMT_PREFIX+'DelayRebate').text=='true' else 1
                                
                                barrierEventDates = []
                                
                                be=barriers[0].find(GMT_PREFIX+'BarrierEvent')
                                
                                tradeDictionary['BarrierMonitoring']=2
                                        
                                startDate = be.find(GMT_PREFIX+'StartEvent').attrib[GMT_PREFIX+'Date']
                                endDate = be.find(GMT_PREFIX+'EndEvent').attrib[GMT_PREFIX+'Date'] 
                                barrierEventDates.append((startDate, endDate))
                                    
                                tradeDictionary['BarrierEventDates']=barrierEventDates
                            
                            if isValid==1 and tradeDictionary['EventType'] == "NewTrade" and tradeDictionary['EventReason'] == "":
                                trade = OneTouchTrade(tradeDictionary)
                                insName, trdNbr = trade.CreateTrade()
                                if dict['BARXTSSource'] == "Yes":
                                        print "CREATED FX One Touch Option:\tInstrument:\t%s\tBARX FX TS Trade:\t%s\t\tFA Trade:\t%s" % (insName, tradeDictionary['TradeID'], trdNbr)
                                else:
                                        print "CREATED FX One Touch Option:\tInstrument:\t%s\tMurex Trade:\t%s\t\tFA Trade:\t%s" % (insName, tradeDictionary['TradeID'], trdNbr)
                            else:
                                print "SKIPPED FX One Touch Option:\tisValid:\t%s\t\tEventType:\t%s\tEventReason:\t%sId:\t%s" % isValid, (tradeDictionary['EventType'], tradeDictionary['EventReason'], tradeDictionary['TradeID'])
                        #--------------Double No Touch Option ---------------
                        elif InsType == 'FX Option' and (InsSubType == 'NoTouch' or InsSubType == 'DoubleOneTouch'): #note inconsistent naming on the NoTouch
                            XPATH = {
                            'EconomicUnderlyingCurrency' : GMT_PREFIX.join([GMT_PREFIX+'Instrument/', 'EconomicDetail/', 'AssetDetail/', 'OptionUnderlying/', 'Underlying/', 'EconomicDetail/', 'FXDetails/', 'QuotedCurrency']),
                            'EconomicBaseCurrency' : GMT_PREFIX.join([GMT_PREFIX+'Instrument/', 'EconomicDetail/', 'AssetDetail/', 'OptionUnderlying/', 'Underlying/', 'EconomicDetail/', 'FXDetails/', 'BaseCurrency']),
                            'Amount' : GMT_PREFIX.join([GMT_PREFIX+'Instrument/', 'EconomicDetail/', 'AssetDetail/', 'OptionUnderlying/', 'Underlying/', 'EconomicDetail/', 'FXDetails/', 'Amount']),
                            'QuotedCurrency' : GMT_PREFIX.join([GMT_PREFIX+'Instrument/', 'EconomicDetail/', 'AssetDetail/', 'OptionUnderlying/', 'Underlying/', 'EconomicDetail/', 'FXDetails/', 'QuotedCurrency']),
                            'PayoffDate' : GMT_PREFIX.join([GMT_PREFIX+'Instrument/', 'EconomicDetail/', 'AssetDetail/', 'OptionUnderlying/', 'LocalPayoffDetails/', 'PayoffDate']),
                            'PayoffType' : GMT_PREFIX.join([GMT_PREFIX+'Instrument/', 'EconomicDetail/', 'AssetDetail/', 'PayoffInCashOrAsset']),
                            'OptionType' : GMT_PREFIX.join([GMT_PREFIX+'Instrument/', 'EconomicDetail/', 'AssetDetail/', 'OptionExpiryStyle']),
                            'TradeCurrency' : GMT_PREFIX.join([GMT_PREFIX+'Instrument/', 'EconomicDetail/', 'AssetDetail/', 'Currency']),
                            'ExpiryEvent' : GMT_PREFIX.join([GMT_PREFIX+'Instrument/', 'EconomicDetail/', 'AssetDetail/', 'OptionExpiryEvent']),
                            'Portfolio' : GMT_PREFIX.join([GMT_PREFIX+'Instrument/', 'BookingDetail/', 'Book']),
                            'Counterparty' : GMT_PREFIX.join([GMT_PREFIX+'Instrument/', 'BookingDetail/', 'Counterparty']),
                            'BuyOrSell' : GMT_PREFIX.join([GMT_PREFIX+'Instrument/', 'BookingDetail/', 'BuyOrSell']),
                            'TradePrice' : GMT_PREFIX.join([GMT_PREFIX+'Instrument/', 'BookingDetail/', 'TradePrice/', 'Rate']),
                            'BookingBaseCurrency' : GMT_PREFIX.join([GMT_PREFIX+'Instrument/', 'BookingDetail/', 'TradePrice/', 'BaseCurrency']),
                            'BookingQuotedCurrency' : GMT_PREFIX.join([GMT_PREFIX+'Instrument/', 'BookingDetail/', 'TradePrice/', 'QuotedCurrency']),
                            'BasePerQuoted' : GMT_PREFIX.join([GMT_PREFIX+'Instrument/', 'BookingDetail/', 'TradePrice/', 'Rate']),
                            'FlowList' : GMT_PREFIX.join([GMT_PREFIX+'Instrument/', 'BookingDetail/', 'FlowList']),
                            'EventType' : GMT_PREFIX.join([GMT_PREFIX+'TradeDetail/', 'Audit']),
                            'TradeDate' : GMT_PREFIX.join([GMT_PREFIX+'TradeDetail/', 'TradeDate']),
                            'Barriers' : GMT_PREFIX.join([GMT_PREFIX+'Instrument/', 'EconomicDetail/', 'AssetDetail/', 'OptionUnderlying/', 'Barrier'])
                            }
                            tradeDictionary = dict.copy()
                            tradeDictionary['TradeID'] = root.find(GMT_PREFIX+"TradeDetail").attrib[GMT_PREFIX+'Id']
                            tradeDictionary['InsType'] = root.find(GMT_PREFIX+'Instrument').attrib[GMT_PREFIX+'Type']
                            tradeDictionary['InsSubType']=root.find(GMT_PREFIX+'Instrument').attrib[GMT_PREFIX+'SubType']
                            tradeDictionary['EconomicUnderlyingCurrency']= root.find(XPATH['EconomicUnderlyingCurrency']).attrib[GMT_PREFIX+'Id']
                            tradeDictionary['EconomicBaseCurrency']= root.find(XPATH['EconomicBaseCurrency']).attrib[GMT_PREFIX+'Id']
                            tradeDictionary['Amount']= root.find(XPATH['Amount']).text
                            tradeDictionary['QuotedCurrency']= root.find(XPATH['QuotedCurrency']).attrib[GMT_PREFIX+'Id']
                            tradeDictionary['PayoffDate']= root.find(XPATH['PayoffDate']).text
                            tradeDictionary['PayoffType']= root.find(XPATH['PayoffType']).text
                            tradeDictionary['OptionType']= root.find(XPATH['OptionType']).text
                            tradeDictionary['ExpiryEventDate']= root.find(XPATH['ExpiryEvent']).attrib[GMT_PREFIX+'ExpiryDate']
                            tradeDictionary['ExpiryEventCutCode']= root.find(XPATH['ExpiryEvent']).attrib[GMT_PREFIX+'ExpiryCutCode']
                            tradeDictionary['Portfolio']= root.find(XPATH['Portfolio']).attrib[GMT_PREFIX+'Id']
                            tradeDictionary['CounterpartyID']= root.find(XPATH['Counterparty']).attrib[GMT_PREFIX+'Id']
                            tradeDictionary['BuyOrSell']=root.find(XPATH['BuyOrSell']).text
                            tradeDictionary['TradePrice']= root.find(XPATH['TradePrice']).text
                            tradeDictionary['BookingBaseCurrency']= root.find(XPATH['BookingBaseCurrency']).attrib[GMT_PREFIX+'Id']
                            tradeDictionary['BookingQuotedCurrency']= root.find(XPATH['BookingQuotedCurrency']).attrib[GMT_PREFIX+'Id']
                            tradeDictionary['BasePerQuoted']= root.find(XPATH['BasePerQuoted']).attrib[GMT_PREFIX+'BasePerQuoted']
                            tradeDictionary['PremiumDate'], tradeDictionary['PremiumAmount'], tradeDictionary['PremiumCurrency'] = FXOTrade.getPremiumDateAmountCurrency(root.find(XPATH['FlowList']))
                            tradeDictionary['EventType']= root.find(XPATH['EventType']).attrib[GMT_PREFIX+'EventType']
                            tradeDictionary['EventReason']= root.find(XPATH['EventType']).attrib[GMT_PREFIX+'EventReason']
                            tradeDictionary['TradeDate']= root.find(XPATH['TradeDate']).text.split('T')[0]
                            tradeDictionary['PayoutCurrency']= root.find(XPATH['TradeCurrency']).attrib[GMT_PREFIX+'Id']
                            
                            isValid = 1
                            barriers = root.findall(XPATH['Barriers'])
                            if len(barriers)!=2 or \
                                barriers[0].find(GMT_PREFIX+'BarrierEvent').find(GMT_PREFIX+'StartEvent').attrib[GMT_PREFIX+'Date']!=barriers[1].find(GMT_PREFIX+'BarrierEvent').find(GMT_PREFIX+'StartEvent').attrib[GMT_PREFIX+'Date'] or \
                                barriers[0].find(GMT_PREFIX+'BarrierEvent').find(GMT_PREFIX+'StartEvent').find(GMT_PREFIX+'Amount').text!=barriers[0].find(GMT_PREFIX+'BarrierEvent').find(GMT_PREFIX+'EndEvent').find(GMT_PREFIX+'Amount').text or \
                                barriers[0].find(GMT_PREFIX+'BarrierEvent').find(GMT_PREFIX+'EndEvent').attrib[GMT_PREFIX+'Date']!=barriers[1].find(GMT_PREFIX+'BarrierEvent').find(GMT_PREFIX+'EndEvent').attrib[GMT_PREFIX+'Date'] or \
                                barriers[1].find(GMT_PREFIX+'BarrierEvent').find(GMT_PREFIX+'StartEvent').find(GMT_PREFIX+'Amount').text!=barriers[1].find(GMT_PREFIX+'BarrierEvent').find(GMT_PREFIX+'EndEvent').find(GMT_PREFIX+'Amount').text or \
                                barriers[0].attrib[GMT_PREFIX+'KnockInOrOut']!=barriers[1].attrib[GMT_PREFIX+'KnockInOrOut']:
                                
                                isValid=0
                            else:
                                tradeDictionary['BarrierLevel1']=barriers[0].find(GMT_PREFIX+'BarrierEvent').find(GMT_PREFIX+'StartEvent').find(GMT_PREFIX+'Amount').text
                                tradeDictionary['BarrierLevel2']=barriers[1].find(GMT_PREFIX+'BarrierEvent').find(GMT_PREFIX+'StartEvent').find(GMT_PREFIX+'Amount').text
                                tradeDictionary['BarrierType']='Double ' + barriers[0].attrib[GMT_PREFIX+'KnockInOrOut']
                                tradeDictionary['Rebate']=barriers[0].find(GMT_PREFIX+'BarrierRebateOnSchedule').find(GMT_PREFIX+'Rebate').find(GMT_PREFIX+'Rate').text
                                tradeDictionary['PayAtExpiry']=0 if barriers[0].find(GMT_PREFIX+'BarrierRebateOnSchedule').find(GMT_PREFIX+'DelayRebate')=='true' else 1
                                
                                barrierEventDates = []
                                
                                be=barriers[0].find(GMT_PREFIX+'BarrierEvent')
                                
                                tradeDictionary['BarrierMonitoring']=2 #for now, if its not discrete it must be window
                                        
                                startDate = be.find(GMT_PREFIX+'StartEvent').attrib[GMT_PREFIX+'Date']
                                endDate = be.find(GMT_PREFIX+'EndEvent').attrib[GMT_PREFIX+'Date'] 
                                barrierEventDates.append((startDate, endDate))
                                    
                                tradeDictionary['BarrierEventDates']=barrierEventDates
                            if isValid==1 and tradeDictionary['EventType'] == "NewTrade" and tradeDictionary['EventReason'] == "":
                                trade = DoubleTouchTrade(tradeDictionary)
                                insName, trdNbr = trade.CreateTrade()
                                if dict['BARXTSSource'] == "Yes":
                                        print "CREATED FX Double No Touch Option:\tInstrument:\t%s\tBARX FX TS Trade:\t%s\t\tFA Trade:\t%s" % (insName, tradeDictionary['TradeID'], trdNbr)
                                else:
                                        print "CREATED FX Double No Touch Option:\tInstrument:\t%s\tMurex Trade:\t%s\t\tFA Trade:\t%s" % (insName, tradeDictionary['TradeID'], trdNbr)
                            else:
                                print "SKIPPED FX Double No Touch Option:\tisValid:\t%s\t\tEventType:\t%s\tEventReason:\t%sId:\t%s" % isValid, (tradeDictionary['EventType'], tradeDictionary['EventReason'], tradeDictionary['TradeID'])
                        elif InsType != '' or InsSubType != '':
                            try:
                                tt, st = row['TradeType'], row['Subtype'] 
                                print 'Unexpected TradeType:', tt, '\tSubtype:', st
                            except:
                                print 'Unexpected TradeType ' + InsType + ' ' + InsSubType
                except Exception, e:
                    print "Uploading trade failed\n\t", e
    else:
        print "Cannot run trade uploader from Commandline or Backend"


"""-----------------------------------------------------------------------
MODULE
    ABSAPortfolioSwapException

DESCRIPTION
    Institutional CFD Project
    
    Date                : 2010-10-05
    Purpose             : Validates the Portfolio Swaps and sends an email if there are any exceptions related to a Portfolio Swap.
    Department and Desk : Prime Services
    Requester           : Herman Levin
    Developer           : Herman Hoon
    CR Number           : 455227

ENDDESCRIPTION

HISTORY
         When: 	  CR Number:                  Who:	  What:       
    2012-03-01        133698       Nidheesh Sharma	  Fixed bug - code was generating an exception message in the case where a pswap has two trades booked against it, one voided and one Bo-Confirmed 
    2013-02-20        814914       Nidheesh Sharma        Removed checks on the instrument's additional information PSSectorCode and PSSectorMargin as its not required in Exception Report
-----------------------------------------------------------------------"""

import acm
import ael

import FBDPCommon
import ABSAPortfolioSwapUtil as Util
reload(Util)
import ABSAPortfolioSwapGuiUtil
reload(ABSAPortfolioSwapGuiUtil)


def ValidatePfSwap(pfSwap, list):
    
    pfSwapName   = pfSwap.Name()
    
    #Instrument Validations
    if pfSwap.OpenEnd() == "Terminated":
        list.append("%s will not be fixed: Portfolio swap is terminated." %(pfSwapName))
        
    
    #Trades Validations
    allowedStatus = Util.AllowedTrades.allowedTradeStatus
    trades = pfSwap.Trades()
    trade = ''
        
    if len(trades) == 0:
        list.append("%s will not be fixed: No trade defined." %(pfSwapName))
        
    else:
        allowedTrades = []
        for t in trades:
            if t.Status() in allowedStatus:
                allowedTrades.append(t)
            

        if len(allowedTrades) == 0:
            list.append("%s will not be fixed: Does not contain a trade in %s status." %(pfSwapName, allowedStatus))
                
        elif len(allowedTrades) > 1:
            list.append("%s will not be fixed: Contains more than one trade in %s status." %(pfSwapName, allowedStatus))
                
        else:
            trade = trades[0]
                
            startDay = pfSwap.StartDate()        
            if trade.ValueDay() != startDay:
                list.append("%s will not be fixed: Trade %s value day is not equal to the start date %s of the Portfolio Swap." %(pfSwapName, trade.Oid(), startDay))
                    
                    
            if trade.AcquireDay() != startDay:
                list.append("%s will not be fixed: Trade %s acquire day is not equal to the start date %s of the Portfolio Swap." %(pfSwapName, trade.Oid(), startDay))
  
    
        
    #Overnight Premium Index Validations
    onPremIndex = pfSwap.add_info('PSONPremIndex')
    if onPremIndex == '':
        list.append("%s will not be fixed: No Overnight Premium Index defined." %(pfSwapName))
        
    
    floatRef = acm.FRateIndex[onPremIndex]
    if floatRef == None:
        list.append("%s will not be fixed: Overnight Premium Index is not a Rate Index." %(pfSwapName))
        
    
    else:
        bidPrice = ''
        askPrice = ''
        for p in floatRef.Prices():
            if p.Market().Name() == 'SPOT':
                bidPrice = str(p.Bid())
                askPrice = str(p.Ask())
                
        if bidPrice == '':
            list.append("%s will not be fixed: No ask SPOT price populated for the %s Overnight Premium Index." %(pfSwapName, onPremIndex))
            
            
        if askPrice == '':
            list.append("%s will not be fixed: No bid SPOT price populated for the %s Overnight Premium Index." %(pfSwapName, onPremIndex))
            
    
    
    #Portfolio Validations
    fundPort = pfSwap.FundPortfolio()
    ownerPort = ''
    fundPortName = ''
    if fundPort:
        fundPortName = fundPort.Name()
        links = fundPort.MemberLinks()
        
        if fundPort.add_info('PSExtExecPremRate') == '':
            list.append("%s will not be fixed: No PSExtExecPremRate defined on Stock Portfolio %s." %(pfSwapName, fundPortName))
            
        
        if links:
            ownerPort = links[0].OwnerPortfolio()
            ownerPortName = ownerPort.Name()

            if ownerPort:
                if ownerPort.AdditionalInfo().PSClientCallAcc() == None:
                    list.append("%s will not be swept: No PSClientCallAcc defined on Compound Portfolio %s." %(pfSwapName, ownerPortName))
                    
                
                if ownerPort.AdditionalInfo().PSMarginFactor() == None:
                    list.append("%s Margin: No PSMarginFactor defined on Compound Portfolio %s." %(pfSwapName, ownerPortName))
                    
                
                if ownerPort.AdditionalInfo().PSClientName() == None:
                    list.append("%s Client Name: No Client Name defined on Compound Portfolio %s." %(pfSwapName, ownerPortName))
                    

    else:
        list.append("%s will not be fixed: No valid Stock Portfolio selected." %(pfSwapName))
        
    
    
    #Short Premium Validations
    shortPremType = pfSwap.add_info('PSShortPremiumType')
    if shortPremType == '':
        list.append("%s will not be fixed: No Short Premium Type defined." %(pfSwapName))
        
    
    #Loop through the stock portfolio to determine if the stocks have a short premium rate and margin factors defined 
    if fundPort:
        for ins in fundPort.Instruments():
            if ins.InsType() == 'Stock':
                insName = ins.Name()
                if shortPremType == 'Float':
                    shortPrem = ins.add_info('PSShortPremCost')
                    shortPremIndex = acm.FRateIndex[shortPrem]
                    if shortPremIndex == None:
                        list.append("%s will not be fixed: PSShortPremCost for underlying Stock %s, is not a Rate Index." %(pfSwapName, insName))
                        
                    else:
                        price = ''
                        prices = shortPremIndex.Prices()
                        for p in prices:
                            if p.Market().Name() == 'SPOT':
                                price = p.Settle()
                        
                        if price == '':
                            list.append("%s will not be fixed: Short Premium Rate index %s for underlying Stock %s, does not have a SPOT price populated ." %(pfSwapName, shortPrem, insName))
                            
                    
    #Sweeping Validations
    if pfSwap.AdditionalInfo().PSSweepBaseDay() == None:
        list.append("%s will not be swept: No Sweeping Base day defined." %(pfSwapName))
        
        
    if pfSwap.AdditionalInfo().PSSweepFreq() == None:
        list.append("%s will not be swept: No Sweeping Frequency defined." %(pfSwapName))
        
        
    return list


psquery   = ABSAPortfolioSwapGuiUtil.instrumentQuery(instype=('Portfolio Swap',))

# [fieldId, fieldLabel, fieldType, fieldValues, defaultValue, isMandatory, insertItemsDialog, toolTip, callback, enabled]
ael_variables = [['portfolioSwaps', 'Portfolio Swap(s)', 'FInstrument', None, psquery, 1, 1, 'Portfolio swap instrument(s)'],
                 ['emailTo', 'Email Recipients', 'string', None, None, 0, 1, 'Exceptions will be send to the following email adresses.', None, 1]
                ]

def ael_main(dictionary):
    list = []
    pfSwaps = dictionary["portfolioSwaps"]
    emailTo = dictionary["emailTo"]
    emailTo = ";".join(emailTo)
    
    for pfSwap in pfSwaps:
        list = ValidatePfSwap(pfSwap, list)

    slist = 'Exceptions have been found for the following Portfolio Swaps: \n\n'
    for l in list:
        slist = slist + l + '\n'
    
    
    if len(list) > 0:
        if len(emailTo)>0:
            FBDPCommon.sendMail(emailTo, "Portfolio Swap Exceptions", slist)
        else:
            print slist

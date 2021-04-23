#*********************************************************************************************************************************
#*********************************************************  TMS Filter  **********************************************************
#*********************************************************************************************************************************

#Sub-function for the TMS_FIlter function to determine if the portfolio is a valid PRD portfolio
def isPrdPortfolio(TObject,IObject,*rest):

    validPrdPortfolio = 0

    if TObject and TObject.prfnbr:
        if TObject.prfnbr.add_info('BarCap_TMS_Feed') == 'Production' \
            and TObject.status != 'FO Sales' \
            and TObject.status != 'Simulated':

            validPrdPortfolio = 1
       
    return validPrdPortfolio
    
#Sub-function for the TMS_FIlte function to determine if the portfolio is a valid Test portfolio
def isTestPortfolio(TObject,IObject,*rest):

    TestPortfolio = 0

    if TObject and TObject.prfnbr:
        if TObject.prfnbr.add_info('BarCap_TMS_Feed') == 'Test' \
            and TObject.status == 'Simulated':

            validTestPortfolio = 1
        
    return validTestPortfolio

#Sub-function for the TMS_FIlter function to determine if the instrument is a valid PRD instrument
def isSupportedInstrument(TObject,IObject,*rest):

    ValidInstrument = 0

    #Determine whether the instrument is a valid TMS instrument
    if TObject and TObject.prfnbr:
        if ((IObject.instype == 'Option' and IObject.und_instype == 'Swap') or \
                (IObject.instype == 'Option' and IObject.und_instype == 'FRA') or \
                IObject.instype == 'FxSwap' or \
                IObject.instype == 'CurrSwap' or \
                IObject.instype == 'Swap' or \
                IObject.instype == 'FRA' or \
                IObject.instype == 'Cap' or \
                IObject.instype == 'Floor') and IObject.exp_day.to_string('%Y-%m-%d') >= Expired_Date():

            ValidInstrument = 1
        
    return ValidInstrument

   
'''
Main TMS Filter
'''
def TMS_Filter (TObject,IObject,*rest):    

    '''
        This function determines whether a trade is valid for TMS feeding.
        
        3 Functions determine the validity of the trade:
        
        isPrdPortfolio()
        isTestPortfolio()
        isSupportedInstrument()
    '''
    if (isPrdPortfolio(TObject, IObject) == 1 or isTestPortfolio(TObject, IObject) == 1) \
        and isSupportedInstrument(TObject, IObject) == 1:
            
            SendTrade = 1
    else:
        SendTrade = 0
        
    return SendTrade
#*********************************************************************************************************************************
#*********************************************************  TMS Filter  **********************************************************
#*********************************************************************************************************************************


































import ael, time, sys, string

#Trade = ael.Trade[2602876]

#Owner = Trade.insaddr.insaddr


#for l in ael.CombinationLink.select('owner_insaddr=%d' %Trade.insaddr.insaddr):
#    print l.member_insaddr.instype
    


#print Trade.insaddr.columns()
#print Owner

#for l in ael.CombinationLink:
#    print l.member_insaddr

#print dir(ael.CombinationLink.columns())

print dir(string)

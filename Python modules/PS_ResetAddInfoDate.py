#************************************************************************************************************************
#Script Name             :PB_SetAddInfoDateFlag
#Description             :Reset the add info date flag on prime broker trades to default
#Developer               :Sarawab Bhavnisha, Momberg Heinrich
#CR Number(s)            :ABITFA-605(IDS)
#************************************************************************************************************************
import acm, ael
from PS_Functions import SetAdditionalInfo

#***********************************************************************************************
#Global constants
#***********************************************************************************************
PB_ADD_INFO_FLAG = 'PS_MsgSentDate'
BO_CONFIRMED_STATUS =  'BO Confirmed'
BO_BO_CONFIRMED_STATUS = 'BO-BO Confirmed'
VOID_STATUS = 'Void'
ADD_INFO_DEFAULT = acm.Time.AsDate('1700-01-01')
TODAY = acm.Time.DateToday()

#***********************************************************************************************
#Main entry point and Variables
#***********************************************************************************************
ael_variables = [
                 ['tradeFilters', 'Trade Filters', 'FTradeSelection', acm.FTradeSelection.Select(''), 'PS_SetAddInfoDate_IDS', 1, 1]
                ]
                
def ael_main(parameters):
    try:
        
        #Test if the Additional Info spec exists on table trade 
        addInfoSpec  = acm.FAdditionalInfoSpec[PB_ADD_INFO_FLAG]
        
        if(not addInfoSpec):
            raise Exception("Additional Info Spec '%s' not defined" % (PB_ADD_INFO_FLAG)) 
        elif  (addInfoSpec.RecType()!='Trade'):
            raise Exception("Additional Info Spec '%s' not defined for record type 'Trade'" % (PB_ADD_INFO_FLAG)) 
        
        #Get the trade filters from parameters
        tradeFilters = parameters['tradeFilters']
        
        #Find all the new trades in each trade filter and add them to the list for update
        tradesForUpdate = []
        for tf in tradeFilters:
            for t in tf.Trades():
                
                addInfoValue = eval('t.AdditionalInfo().%s()' % PB_ADD_INFO_FLAG)
                status = t.Status()
               
                #NEW - BO or BO-BO Confirmed Status and add info flag default or empty
                if(status==BO_CONFIRMED_STATUS or status==BO_BO_CONFIRMED_STATUS or status==VOID_STATUS) and (not addInfoValue or addInfoValue==ADD_INFO_DEFAULT):
                    tradesForUpdate.append(t)
        
        if(len(tradesForUpdate)==0):
            print "WARNING: No trades was identified for update!"
        else:
            for t in tradesForUpdate:
                print "Trade %s identified for update (status=%s)" % (t.Oid(), t.Status())
            
        #Now update the add-info date flag
        set_AddInfoDate(tradesForUpdate)
        
        #Report completed
        ael.log('Completed Successfully')
        print 'Completed Successfully'
        return 0
        
    except Exception, e:
        #Error, log and print
        errMsg = 'Failed! %s' % (e.message)
        ael.log(errMsg)
        print errMsg
        return -1   
 
        
#***************************************************************************************
#Name:          set_AddInfoForTradesCollection
#Description:   Enumerates through a collection of trades and update the add info value 
#Parameters:    trades (FPersistentSet) - The collection of trades to update
#               date (Date) - The date value to use in the update
#Return Type:   None
#***************************************************************************************
def set_AddInfoDate(trades):
    
    #Enumerate through the FArray(of FTradeSelection)
    for t in trades:
        tradeNumber = t.Oid()
        print 'Trying to update trade %s.....setting %s=%s' %(tradeNumber, PB_ADD_INFO_FLAG, ADD_INFO_DEFAULT)
        SetAdditionalInfo(t, PB_ADD_INFO_FLAG, ADD_INFO_DEFAULT)
            
        
  
    




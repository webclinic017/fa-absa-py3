"""-----------------------------------------------------------------------
MODULE
    CCR_ForeignDivStreamSubscr_ATS

DESCRIPTION
    Subscription module

    Date                : 2015-03-20
    Purpose             : Creates a subscription service to listen on dividend estimate alterations.
    Department and Desk : Market Risk
    Developer           : Ryan Warne

HISTORY

ENDDESCRIPTION
-----------------------------------------------------------------------"""

import acm, ael

import traceback
import FUxCore
import time
import ast
import CCR_ReconcileDivEstimates as reconcileDivs
import datetime
from at_time import ael_date

# Contains linkage between parallel dividend streams (setup as FParameter in CCR Project module)
global FOREIGNDIVIDENDINS
global TIMEDELAY
TODAY = acm.Time().DateToday()

def error_message_construct(ex):

    template = "An exception of type {0} occured. Message:{1!r}"
    message = template.format(type(ex).__name__, ex.args[0])
    
    return message

def get_parameter_dict(name):
    """get values from FParameter by name"""
    values = {}
    p = acm.GetDefaultContext().GetExtension('FParameters', 'FObject', name)
    try:
        template = p.Value()
    except AttributeError, e:
        logger.ELOG( "Error getting parameters ( %s ): %s", name, str( e ) )
    for k in template.Keys():
        k = str(k)
        value = str( template.At(k) )
        value = None if value == "" else value
        values[ str(k) ] = value
    return values

class StandardCalcSpace( object ):
    CALC_SPACE = acm.Calculations().CreateStandardCalculationsSpaceCollection()

def get_domestic_div_stream_name(divEstimate):

    domesticDivStreamName = (FOREIGNDIVIDENDINS[divEstimate.DividendStream().Instrument().Name()])[0]

    return domesticDivStreamName

def get_domestic_div_estimates(divEstimate):

    domesticDivStreamName = get_domestic_div_stream_name(divEstimate)

    #Obtain corresponding stream
    
    domesticDivEstimates = acm.FDividendStream[domesticDivStreamName].Dividends()

    return domesticDivEstimates

#Delete domestic dividend
def delete_domestic_div_estimate(divEstimate):

    domesticDivStreamName = get_domestic_div_stream_name(divEstimate)

    print "Deleting estimate from %s dividend stream" %(domesticDivStreamName)
    
    domesticDivEstimates = get_domestic_div_estimates(divEstimate)
    
    for currDomesticEstimate in domesticDivEstimates:
        if (ael_date(divEstimate.ExDivDay()) == ael_date(currDomesticEstimate.ExDivDay())) or \
            (ael_date(divEstimate.PayDay()) == ael_date(currDomesticEstimate.PayDay())) or \
            (ael_date(divEstimate.RecordDay()) == ael_date(currDomesticEstimate.RecordDay())):
    
            #Delete exisiting dividend estimate
            
            try:
                currDomesticEstimate.Delete()

            except Exception as ex:
                message = error_message_construct(ex)
                print "Dividend estimate deletion failure for stream " + domesticDivStreamName +":" + message
    
#Insert new domestic dividend
def insert_domestic_div_estimate(divEstimate):
    
    domesticDivStreamName = get_domestic_div_stream_name(divEstimate)
    
    print "Inserting estimate into %s dividend stream" %(domesticDivStreamName)
    
    fxRate = divEstimate.Currency().Calculation().FXRate(StandardCalcSpace.CALC_SPACE, acm.FCurrency['ZAR'], divEstimate.PayDay())
    
    # Create new dividend estimate
    try:
        newDomesticEstimate = acm.FDividendEstimate()
        newDomesticEstimate.DividendStream = acm.FDividendStream[domesticDivStreamName]
        newDomesticEstimate.Amount = divEstimate.Amount() * fxRate
        newDomesticEstimate.TaxFactor = divEstimate.TaxFactor()
        newDomesticEstimate.Description = divEstimate.Description()
        newDomesticEstimate.DividendType = divEstimate.DividendType()
        newDomesticEstimate.AmountProportional = divEstimate.AmountProportional()
        newDomesticEstimate.AbsoluteAsProportional = divEstimate.AbsoluteAsProportional()
        newDomesticEstimate.PayDay = divEstimate.PayDay()
        newDomesticEstimate.ExDivDay = divEstimate.ExDivDay()
        newDomesticEstimate.RecordDay = divEstimate.RecordDay()
        newDomesticEstimate.Currency = acm.FCurrency['ZAR']
        
        # Commit the new domestic dividend estimate
        newDomesticEstimate.Commit()

    except Exception as ex:
        message = error_message_construct(ex)
        print "Dividend estimate creation failure for stream " + domesticDivStreamName +":" + message
    
#Update foreign dividend
def update_foreign_div_estimate(foreignDivEstimate, domesticDivEstimate):
            
    print "="*100
     
    acm.BeginTransaction()
       
    try:
        print 'Found corresponding foreign dividend...'
        updatedForeignEstimate = foreignDivEstimate.Clone()
        updatedForeignEstimate.Amount = domesticDivEstimate.Amount()
        updatedForeignEstimate.TaxFactor = domesticDivEstimate.TaxFactor()
        updatedForeignEstimate.Description = domesticDivEstimate.Description()
        updatedForeignEstimate.DividendType = domesticDivEstimate.DividendType()
        updatedForeignEstimate.AmountProportional = domesticDivEstimate.AmountProportional()
        updatedForeignEstimate.AbsoluteAsProportional = domesticDivEstimate.AbsoluteAsProportional()
        updatedForeignEstimate.PayDay = domesticDivEstimate.PayDay()
        updatedForeignEstimate.ExDivDay = domesticDivEstimate.ExDivDay()
        updatedForeignEstimate.RecordDay = domesticDivEstimate.RecordDay()
        updatedForeignEstimate.Currency = domesticDivEstimate.Currency()

        # Commit the changes to the domestic dividend estimate
        foreignDivEstimate.Apply(updatedForeignEstimate)
        foreignDivEstimate.Commit()
                
    except Exception as ex:
        message = error_message_construct(ex)
        print "Dividend estimate update failure for stream " + foreignDivEstimate.DividendStream().Name() +":" + message
    
    acm.CommitTransaction()

  
#Determine if update is a declaration and if so update foreign counterpart
def domestic_div_declared(divEstimate):
        
    foreignDivStreamName =(FOREIGNDIVIDENDINS[divEstimate.DividendStream().Instrument().Name()])[1]
    foreignDivEstimates =  acm.FDividendStream[foreignDivStreamName].Dividends()

    for currForeignEstimate in foreignDivEstimates:
        if (ael_date(divEstimate.ExDivDay()) == ael_date(currForeignEstimate.ExDivDay())) or \
            (ael_date(divEstimate.PayDay()) == ael_date(currForeignEstimate.PayDay())) or \
            (ael_date(divEstimate.RecordDay()) == ael_date(currForeignEstimate.RecordDay())):
            
            if currForeignEstimate.DividendType() != "Declared" and divEstimate.DividendType() == "Declared" and \
                currForeignEstimate.UpdateTime() < divEstimate.UpdateTime() and not \
                (datetime.datetime.strptime(acm.Time.DateTimeFromTime(currForeignEstimate.UpdateTime()), "%Y-%m-%d %H:%M:%S")) > \
			(datetime.datetime.now() - datetime.timedelta(seconds=TIMEDELAY)):
                
                print "Declaration in Domestic Dividend Stream Detected..."
                update_foreign_div_estimate(currForeignEstimate, divEstimate)  
  
#Determine if dividend has a domestic counterpart
def is_foreign_dividend(divEstimate):

    isForeign = False

    divStreamMappedInsid = divEstimate.DividendStream().Instrument().Name()
    
    if divStreamMappedInsid in FOREIGNDIVIDENDINS:
        if divEstimate.DividendStream().Name() == (FOREIGNDIVIDENDINS[divStreamMappedInsid])[1]:
            isForeign = True
            #print 'Instrument has foreign dividends'
        
    return isForeign

#Subscription Service
class DivEstimateUpdateHandler:
    def ServerUpdate(self, sender, aspect, param):
    
        operation = str(aspect)
        
        isForeign = is_foreign_dividend(param)
    
        if isForeign:
            #In case of updating of a foreign dividend estimate, don't do anything. There is already the script CCR_ReconcileDivEstimates running every 10 minutes, which will update the ZAR dividend estimates.
            if operation == 'remove':
                delete_domestic_div_estimate(param)
            
            elif operation == 'insert':
                insert_domestic_div_estimate(param)
                
        else:
            domestic_div_declared(param)
     
def start():        
    handler = DivEstimateUpdateHandler()
    divEstimateObj = acm.FDividendEstimate.Select('')
    divEstimateObj.AddDependent(handler)
    print "Started subscription"
    reconcileDivs.main()
    
def stop():    
    divEstimateObj = acm.FDividendEstimate.Select('')
    for dependent in divEstimateObj.Dependents():
        divEstimateObj.RemoveDependent(dependent)
    print "Stopped subscription"

FOREIGNDIVIDENDINS = ast.literal_eval((get_parameter_dict("foreignDividendIns"))['stockDictionary'])
TIMEDELAY = 5 #time delay to catch updates that are called by ATS directly after insert


stop()
#start()

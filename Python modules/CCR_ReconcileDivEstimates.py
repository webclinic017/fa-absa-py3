"""-----------------------------------------------------------------------
MODULE
    CCR_ReconcileDivEstimates

DESCRIPTION
    Subscription module

    Date                : 2015-03-23
    Purpose             : Reconciles dividends for stocks with parallel dividend streams. 
    Department and Desk : Market Risk
    Developer           : Ryan Warne

HISTORY

2017-01-12      Faize Adams     Added functionality for the fx dividend automation.
                                When run as a part of the automation process, it will
                                update all mapped dividends every 1 minute.

ENDDESCRIPTION
-----------------------------------------------------------------------"""

import acm, ael

import traceback
import FUxCore
import time
import datetime
import ast
from at_time import ael_date
from at_ael_variables import AelVariableHandler


#This should be a defined list maintained somewhere. Contains linkage between parallel dividend streams

TODAY = acm.Time().DateToday()
DIVAUTOMATIONPROCESSFLAG = False

ael_variables = AelVariableHandler()
ael_variables.add_bool('update',
                  label='Force update domestic dividends',
                  default=False)

class StandardCalcSpace( object ):
    CALC_SPACE = acm.Calculations().CreateStandardCalculationsSpaceCollection()

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

def get_dividends(streamName):

    try:
        divList = acm.FDividendStream[streamName].Dividends()
        return divList

    except:
        return "None"

#Update dividend
def update_div_estimate(divEstimateToUpdate, divEstimate):
    print "\tUpdating estimate in %s dividend stream" % (divEstimateToUpdate.DividendStream().Name())
    fxRate = divEstimate.Currency().Calculation().FXRate(StandardCalcSpace.CALC_SPACE, divEstimateToUpdate.Currency(), divEstimate.PayDay()) 
       
    # Update exisiting dividend estimate
    try:
        updatedEstimate = divEstimateToUpdate.Clone()
        updatedEstimate.Amount = divEstimate.Amount() * fxRate
        updatedEstimate.TaxFactor = divEstimate.TaxFactor()
        updatedEstimate.Description = divEstimate.Description()
        updatedEstimate.DividendType = divEstimate.DividendType()
        updatedEstimate.AmountProportional = divEstimate.AmountProportional()
        updatedEstimate.AbsoluteAsProportional = divEstimate.AbsoluteAsProportional()
        updatedEstimate.PayDay = divEstimate.PayDay()
        updatedEstimate.ExDivDay = divEstimate.ExDivDay()
        updatedEstimate.RecordDay = divEstimate.RecordDay()

        # Commit the changes to the outdated dividend estimate
        divEstimateToUpdate.Apply(updatedEstimate)
        divEstimateToUpdate.Touch()
        divEstimateToUpdate.Commit()
        #Recommit up-to-date one to synchorize times (not working exactly right)!!!
        divEstimate.Touch()
        divEstimate.Commit()
    except Exception as ex:
        message = error_message_construct(ex)
        print "Dividend estimate update failure for stream " + divEstimateToUpdate.DividendStream().Name()+":" + message
        

#Insert new domestic dividend
def insert_domestic_div_estimate(divEstimate, domesticDivStreamName):
    
    print "\tInserting estimate into %s dividend stream" %(domesticDivStreamName)
    
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

def delete_est(stream):
   
    for e in stream.Dividends():
        try: 
            e.Delete()
        except:
            print "ERROR: Dividend estimate deletion failed!"
    
def recreate_div_estimates(foreignDivs, domesticDivStreamName):

    domesticDivStream = acm.FDividendStream[domesticDivStreamName]

    #Delete domestic estimates
    acm.BeginTransaction()
    delete_est(domesticDivStream)
    acm.CommitTransaction()
    
    #Recreate dividend estimates
    for currForeignDiv in foreignDivs:
        insert_domestic_div_estimate(currForeignDiv, domesticDivStreamName)
        
def validate_div_stream(foreignDivs, domesticDivs, errorLevel, stock):
    
    domesticDivStreamName = (foreignDividendIns[stock])[0]
    
    checkVector = [0] * len(foreignDivs)
    
    #Check dividend estimate count
    if len(foreignDivs) != len(domesticDivs):
        print 'Parallel steam lengths do not match...recreating domestic stream'
        recreate_div_estimates(foreignDivs, domesticDivStreamName)
        
    #Check 
    index = 0

    for currForeignDiv in foreignDivs:
        for currDomesticDiv in domesticDivs:
            if (ael_date(currForeignDiv.ExDivDay()) == ael_date(currDomesticDiv.ExDivDay())) or \
                (ael_date(currForeignDiv.PayDay()) == ael_date(currDomesticDiv.PayDay())) or \
                (ael_date(currForeignDiv.RecordDay()) == ael_date(currDomesticDiv.RecordDay())):
                if (currForeignDiv.UpdateTime() >= (currDomesticDiv.UpdateTime() + errorLevel)):
                    print 'Found more recent Foreign Dividend...correcting...'
                    update_div_estimate(currDomesticDiv, currForeignDiv)
                        
                elif (currForeignDiv.UpdateTime() <= (currDomesticDiv.UpdateTime() - errorLevel)):
                    print 'Found more recent Domestic Dividend...correcting...'
                    update_div_estimate(currForeignDiv, currDomesticDiv)
                #break
        checkVector[index] = 1
        index += 1
                
    #Final validation
    if sum(checkVector) != len(foreignDivs):
        print 'Unsynchronized streams...recreating domestic stream'
        recreate_div_estimates(foreignDivs, domesticDivStreamName)

def fx_automation_process(foreignDivs, domesticDivs, foreignDivStreamName, domesticDivStreamName):
    foreignDivsDict = dict([("%s%s%s" % (div.ExDivDay(), div.RecordDay(), div.PayDay()), div) for div in foreignDivs])
    domesticDivsDict = dict([("%s%s%s" % (div.ExDivDay(), div.RecordDay(), div.PayDay()), div) for div in domesticDivs])
    domesticDivsToDelete = [divDates for divDates in domesticDivsDict.keys() if divDates not in foreignDivsDict.keys()]
    acm.BeginTransaction()
    try:
        if len(domesticDivsToDelete) > 0:
            print "Deleting %d unmatched domestic dividends in %s" % (len(domesticDivsToDelete), domesticDivStreamName)
            for div in domesticDivsToDelete:
                domesticDivsDict[div].Delete()
                del domesticDivsDict[div]
                
        for currForeignDivDates in foreignDivsDict.keys():
            if domesticDivsDict.get(currForeignDivDates, False):
                update_div_estimate(domesticDivsDict[currForeignDivDates], foreignDivsDict[currForeignDivDates])
            else:
                insert_domestic_div_estimate(foreignDivsDict[currForeignDivDates], domesticDivStreamName)
        acm.CommitTransaction()
    except Exception, e:
        acm.AbortTransaction()
        print "Updating domestic dividends failed: %s" % str(e)

def ael_main(ael_variables):
    global DIVAUTOMATIONPROCESSFLAG
    DIVAUTOMATIONPROCESSFLAG = ael_variables['update']
    main()
      
def main():
      
    #Loop through dividend streams to check for inconsistencies
    errorLevel = 10
    global foreignDividendIns
    global DIVAUTOMATIONPROCESSFLAG
    foreignDividendIns = ast.literal_eval((get_parameter_dict("foreignDividendIns"))['stockDictionary'])

    for stock in foreignDividendIns.keys():

        print 'Reconciling %s' %stock
        foreignDivStreamName = (foreignDividendIns[stock])[1]
        domesticDivStreamName = (foreignDividendIns[stock])[0]

        foreignDivs = get_dividends(foreignDivStreamName)
        domesticDivs = get_dividends(domesticDivStreamName)
        
        if foreignDivs == "None":
            print "No foreign dividend stream detected. Moving to next stock..."
        else:
            #Check bidirectionally if streams are correct/up-to-date
            if DIVAUTOMATIONPROCESSFLAG:
                fx_automation_process(foreignDivs, domesticDivs, foreignDivStreamName, domesticDivStreamName)
            else:
                validate_div_stream(foreignDivs, domesticDivs, errorLevel, stock)

    print 'Reconciliation Complete'



